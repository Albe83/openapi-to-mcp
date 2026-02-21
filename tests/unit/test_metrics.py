from __future__ import annotations

from openapi_to_mcp.metrics import RuntimeMetrics


def test_runtime_metrics_exposes_core_families() -> None:
    metrics = RuntimeMetrics(max_in_flight=8, max_connections=16)
    payload = metrics.render_openmetrics().decode("utf-8")

    assert "openapi_to_mcp_http_invoker_in_flight" in payload
    assert "openapi_to_mcp_http_invoker_max_in_flight" in payload
    assert "openapi_to_mcp_http_connection_pool_max_connections" in payload
    assert "openapi_to_mcp_http_invoker_errors_total" in payload


def test_runtime_metrics_tracks_errors_and_usage() -> None:
    metrics = RuntimeMetrics(max_in_flight=2, max_connections=4)

    metrics.on_invocation_started(wait_seconds=0.01)
    metrics.on_invocation_error()
    metrics.on_invocation_finished()

    payload = metrics.render_openmetrics().decode("utf-8")
    assert "openapi_to_mcp_http_invoker_requests_total 1.0" in payload
    assert "openapi_to_mcp_http_invoker_errors_total 1.0" in payload
