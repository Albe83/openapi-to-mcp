"""Runtime metrics instrumentation helpers."""

from __future__ import annotations

from threading import Lock
from typing import Any

from opentelemetry.metrics import Observation

from openapi_to_mcp.telemetry import build_telemetry_runtime

_HTTP_SERVER_DURATION_BUCKETS = (
    0.005,
    0.01,
    0.025,
    0.05,
    0.1,
    0.25,
    0.5,
    1.0,
    2.5,
    5.0,
    10.0,
)


class RuntimeMetrics:
    """Collect and emit runtime metrics through OpenTelemetry."""

    def __init__(
        self,
        max_in_flight: int,
        max_connections: int,
        *,
        telemetry_otlp_protocol: str = "grpc",
        telemetry_otlp_endpoint: str = "http://127.0.0.1:4317",
        telemetry_export_interval_ms: int = 60000,
        service_name: str = "openapi-to-mcp",
        service_namespace: str = "openapi-to-mcp",
        service_version: str = "0.0.0",
        deployment_environment: str = "dev",
    ) -> None:
        self._lock = Lock()
        self._in_flight_value = 0
        self._max_in_flight_value = max_in_flight
        self._max_connections_value = max_connections

        telemetry = build_telemetry_runtime(
            protocol=telemetry_otlp_protocol,
            endpoint=telemetry_otlp_endpoint,
            export_interval_ms=telemetry_export_interval_ms,
            service_name=service_name,
            service_namespace=service_namespace,
            service_version=service_version,
            deployment_environment=deployment_environment,
            http_server_duration_buckets=_HTTP_SERVER_DURATION_BUCKETS,
        )
        self._meter_provider = telemetry.provider
        meter = telemetry.meter

        self._otlp_invoker_requests = meter.create_counter(
            "openapi_to_mcp.http_invoker.requests",
            unit="requests",
            description="Total outbound HTTP invocations.",
        )
        self._otlp_invoker_errors = meter.create_counter(
            "openapi_to_mcp.http_invoker.errors",
            unit="errors",
            description="Total outbound HTTP invocation errors.",
        )
        self._otlp_invoker_in_flight = meter.create_up_down_counter(
            "openapi_to_mcp.http_invoker.in_flight",
            unit="requests",
            description="Current in-flight outbound HTTP invocations.",
        )
        self._otlp_invoker_queue_wait = meter.create_histogram(
            "openapi_to_mcp.http_invoker.queue_wait",
            unit="seconds",
            description="Seconds spent waiting for an outbound HTTP slot.",
        )
        self._otlp_invoker_max_in_flight = meter.create_observable_gauge(
            "openapi_to_mcp.http_invoker.max_in_flight",
            callbacks=[self._observe_max_in_flight],
            unit="requests",
            description="Configured max in-flight outbound HTTP invocations.",
        )
        self._otlp_connection_pool_max = meter.create_observable_gauge(
            "openapi_to_mcp.http_connection_pool.max_connections",
            callbacks=[self._observe_connection_pool_max],
            unit="connections",
            description="Configured max outbound HTTP connection pool size.",
        )
        self._otlp_invoker_utilization = meter.create_observable_gauge(
            "openapi_to_mcp.http_invoker.utilization",
            callbacks=[self._observe_invoker_utilization],
            unit="ratio",
            description="Outbound HTTP invoker usage ratio compared to configured capacity.",
        )
        self._otlp_http_server_requests = meter.create_counter(
            "openapi_to_mcp.http_server.requests",
            unit="requests",
            description="Total inbound HTTP requests.",
        )
        self._otlp_http_server_errors = meter.create_counter(
            "openapi_to_mcp.http_server.errors",
            unit="errors",
            description="Total inbound HTTP 5xx responses.",
        )
        self._otlp_http_server_duration = meter.create_histogram(
            "openapi_to_mcp.http_server.duration",
            unit="seconds",
            description="Inbound HTTP request duration.",
        )

    def on_invocation_started(self, wait_seconds: float) -> None:
        self._otlp_invoker_requests.add(1)
        self._otlp_invoker_queue_wait.record(max(wait_seconds, 0.0))
        with self._lock:
            self._in_flight_value += 1
        self._otlp_invoker_in_flight.add(1)

    def on_invocation_error(self) -> None:
        self._otlp_invoker_errors.add(1)

    def on_invocation_finished(self) -> None:
        decremented = False
        with self._lock:
            if self._in_flight_value > 0:
                self._in_flight_value -= 1
                decremented = True
        if decremented:
            self._otlp_invoker_in_flight.add(-1)

    def on_http_request_completed(
        self,
        *,
        route: str,
        method: str,
        status_code: int,
        duration_seconds: float,
    ) -> None:
        http_method = method.upper() if method else "UNKNOWN"
        http_route = route or "unknown"
        attributes = {
            "http.method": http_method,
            "http.route": http_route,
            "http.status_class": _status_class(status_code),
        }

        self._otlp_http_server_requests.add(1, attributes=attributes)
        self._otlp_http_server_duration.record(max(duration_seconds, 0.0), attributes=attributes)

        if status_code >= 500:
            self._otlp_http_server_errors.add(1, attributes=attributes)

    def shutdown(self) -> None:
        try:
            self._meter_provider.shutdown()
        except Exception:
            # Avoid crashing shutdown path if exporter/network is unavailable.
            return

    def _observe_max_in_flight(self, options: Any) -> list[Observation]:
        del options
        return [Observation(float(self._max_in_flight_value))]

    def _observe_connection_pool_max(self, options: Any) -> list[Observation]:
        del options
        return [Observation(float(self._max_connections_value))]

    def _observe_invoker_utilization(self, options: Any) -> list[Observation]:
        del options
        with self._lock:
            current = self._in_flight_value
        if self._max_in_flight_value <= 0:
            ratio = 0.0
        else:
            ratio = max(0.0, min(float(current) / float(self._max_in_flight_value), 1.0))
        return [Observation(ratio)]


def _status_class(status_code: int) -> str:
    if status_code < 100:
        return "unknown"
    return f"{status_code // 100}xx"
