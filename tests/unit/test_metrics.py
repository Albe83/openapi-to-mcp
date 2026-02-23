from __future__ import annotations

from openapi_to_mcp.metrics import RuntimeMetrics


def test_runtime_metrics_tracks_invocation_lifecycle_without_negative_in_flight() -> None:
    metrics = RuntimeMetrics(max_in_flight=8, max_connections=16)

    assert metrics._in_flight_value == 0  # noqa: SLF001
    metrics.on_invocation_started(wait_seconds=0.01)
    assert metrics._in_flight_value == 1  # noqa: SLF001
    metrics.on_invocation_error()
    metrics.on_invocation_finished()
    assert metrics._in_flight_value == 0  # noqa: SLF001

    # Defensive call: value must not become negative.
    metrics.on_invocation_finished()
    assert metrics._in_flight_value == 0  # noqa: SLF001
    metrics.shutdown()


def test_runtime_metrics_records_red_http_metrics_without_exception() -> None:
    metrics = RuntimeMetrics(max_in_flight=2, max_connections=4)
    metrics.on_http_request_completed(
        route="/mcp",
        method="POST",
        status_code=200,
        duration_seconds=0.012,
    )
    metrics.on_http_request_completed(
        route="/mcp",
        method="POST",
        status_code=503,
        duration_seconds=0.018,
    )
    metrics.shutdown()


def test_runtime_metrics_prometheus_payload_disabled_by_default() -> None:
    metrics = RuntimeMetrics(max_in_flight=2, max_connections=4)
    assert metrics.render_prometheus_payload() is None
    assert metrics.prometheus_content_type() is None
    metrics.shutdown()


def test_runtime_metrics_renders_prometheus_payload_when_enabled() -> None:
    metrics = RuntimeMetrics(max_in_flight=2, max_connections=4, prometheus_metrics_enabled=True)
    metrics.on_http_request_completed(
        route="/healthz",
        method="GET",
        status_code=200,
        duration_seconds=0.01,
    )

    payload = metrics.render_prometheus_payload()
    assert payload is not None
    assert b"openapi_to_mcp_http_server_requests" in payload
    assert metrics.prometheus_content_type() is not None
    metrics.shutdown()
