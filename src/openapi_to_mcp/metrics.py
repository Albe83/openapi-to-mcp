"""Runtime metrics registry and helpers."""

from __future__ import annotations

from dataclasses import dataclass
from threading import Lock

from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram
from prometheus_client.openmetrics.exposition import CONTENT_TYPE_LATEST, generate_latest


@dataclass(frozen=True)
class MetricsRenderResult:
    """Rendered OpenMetrics payload."""

    payload: bytes
    content_type: str


class RuntimeMetrics:
    """Collect and expose runtime metrics in OpenMetrics format."""

    def __init__(self, max_in_flight: int, max_connections: int) -> None:
        self._registry = CollectorRegistry()
        self._lock = Lock()
        self._in_flight_value = 0

        self._requests_total = Counter(
            "openapi_to_mcp_http_invoker_requests",
            "Total outbound HTTP invocations.",
            registry=self._registry,
        )
        self._errors_total = Counter(
            "openapi_to_mcp_http_invoker_errors",
            "Total outbound HTTP invocation errors.",
            registry=self._registry,
        )
        self._in_flight = Gauge(
            "openapi_to_mcp_http_invoker_in_flight",
            "Current number of in-flight outbound HTTP invocations.",
            registry=self._registry,
        )
        self._max_in_flight = Gauge(
            "openapi_to_mcp_http_invoker_max_in_flight",
            "Configured max in-flight outbound HTTP invocations.",
            registry=self._registry,
        )
        self._connection_pool_max = Gauge(
            "openapi_to_mcp_http_connection_pool_max_connections",
            "Configured max outbound HTTP connection pool size.",
            registry=self._registry,
        )
        self._queue_wait_seconds = Histogram(
            "openapi_to_mcp_http_invoker_queue_wait_seconds",
            "Seconds spent waiting for an outbound HTTP invocation slot.",
            registry=self._registry,
        )

        self._max_in_flight.set(float(max_in_flight))
        self._connection_pool_max.set(float(max_connections))

    def on_invocation_started(self, wait_seconds: float) -> None:
        self._requests_total.inc()
        self._queue_wait_seconds.observe(max(wait_seconds, 0.0))
        with self._lock:
            self._in_flight_value += 1
            self._in_flight.set(float(self._in_flight_value))

    def on_invocation_error(self) -> None:
        self._errors_total.inc()

    def on_invocation_finished(self) -> None:
        with self._lock:
            if self._in_flight_value > 0:
                self._in_flight_value -= 1
            self._in_flight.set(float(self._in_flight_value))

    def render_openmetrics(self) -> bytes:
        return generate_latest(self._registry)

    def render(self) -> MetricsRenderResult:
        return MetricsRenderResult(
            payload=self.render_openmetrics(),
            content_type=CONTENT_TYPE_LATEST,
        )
