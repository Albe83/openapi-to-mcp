"""OpenTelemetry provider and exporter wiring."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter as OtlpGrpcMetricExporter,
)
from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    OTLPMetricExporter as OtlpHttpMetricExporter,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.metrics.view import ExplicitBucketHistogramAggregation, View
from opentelemetry.sdk.resources import (
    DEPLOYMENT_ENVIRONMENT,
    SERVICE_NAME,
    SERVICE_NAMESPACE,
    SERVICE_VERSION,
    Resource,
)


@dataclass(frozen=True)
class TelemetryRuntime:
    """Telemetry runtime holder used by instrumentation code."""

    provider: MeterProvider
    meter: Any


def build_telemetry_runtime(
    *,
    protocol: str,
    endpoint: str,
    export_interval_ms: int,
    service_name: str,
    service_namespace: str,
    service_version: str,
    deployment_environment: str,
    http_server_duration_buckets: tuple[float, ...] | None = None,
) -> TelemetryRuntime:
    """Build a local meter provider with OTLP exporter."""

    exporter = _build_otlp_metric_exporter(protocol=protocol, endpoint=endpoint)
    metric_reader = PeriodicExportingMetricReader(
        exporter=exporter,
        export_interval_millis=export_interval_ms,
    )
    resource = Resource.create(
        {
            SERVICE_NAME: service_name,
            SERVICE_NAMESPACE: service_namespace,
            SERVICE_VERSION: service_version,
            DEPLOYMENT_ENVIRONMENT: deployment_environment,
        }
    )
    views: list[View] = []
    if http_server_duration_buckets:
        views.append(
            View(
                instrument_name="openapi_to_mcp.http_server.duration",
                aggregation=ExplicitBucketHistogramAggregation(
                    boundaries=list(http_server_duration_buckets)
                ),
            )
        )

    provider = MeterProvider(
        metric_readers=[metric_reader],
        resource=resource,
        views=views,
    )
    meter = provider.get_meter("openapi_to_mcp.runtime", service_version)
    return TelemetryRuntime(provider=provider, meter=meter)


def _build_otlp_metric_exporter(*, protocol: str, endpoint: str):
    if protocol == "http":
        return OtlpHttpMetricExporter(endpoint=endpoint)
    insecure = endpoint.startswith("http://")
    return OtlpGrpcMetricExporter(endpoint=endpoint, insecure=insecure)
