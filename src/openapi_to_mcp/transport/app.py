"""FastAPI application wiring and runtime bootstrap."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from time import perf_counter
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

from openapi_to_mcp import __version__
from openapi_to_mcp.adapters.http_invoker import HttpxInvokerAdapter
from openapi_to_mcp.adapters.openapi_source import FileOpenApiSourceAdapter, UrlOpenApiSourceAdapter
from openapi_to_mcp.adapters.openapi_validator import OpenApiValidatorAdapter
from openapi_to_mcp.application.mapper import OperationMapper
from openapi_to_mcp.application.startup import StartupOrchestrator
from openapi_to_mcp.application.tool_generator import ToolGenerationService
from openapi_to_mcp.config import Settings
from openapi_to_mcp.errors import InvocationError
from openapi_to_mcp.metrics import RuntimeMetrics
from openapi_to_mcp.ports import HttpInvokerPort, OpenApiSourcePort
from openapi_to_mcp.transport.fastmcp_adapter import FastMcpAdapter

logger = logging.getLogger(__name__)


class FallbackToolCallRequest(BaseModel):
    """Compatibility request model for local fallback MCP endpoint."""

    tool: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)


def create_app(
    settings: Settings,
    source_override: Optional[OpenApiSourcePort] = None,
    invoker_override: Optional[HttpInvokerPort] = None,
) -> FastAPI:
    """Create and configure the FastAPI application."""

    source = source_override or _build_openapi_source(settings)
    metrics = RuntimeMetrics(
        max_in_flight=settings.http_max_in_flight,
        max_connections=settings.http_max_connections,
        telemetry_otlp_protocol=settings.telemetry_otlp_protocol,
        telemetry_otlp_endpoint=settings.telemetry_otlp_endpoint,
        telemetry_export_interval_ms=settings.telemetry_export_interval_ms,
        service_name=settings.service_name,
        service_namespace=settings.service_namespace,
        service_version=__version__,
        deployment_environment=settings.deployment_environment,
    )
    invoker = invoker_override or HttpxInvokerAdapter(
        metrics=metrics,
        max_connections=settings.http_max_connections,
        max_keepalive_connections=settings.http_max_keepalive_connections,
        max_in_flight=settings.http_max_in_flight,
    )
    mcp_adapter = FastMcpAdapter(invoker=invoker)
    validator = OpenApiValidatorAdapter()
    mapper = OperationMapper()
    generator = ToolGenerationService()

    orchestrator = StartupOrchestrator(
        source=source,
        validator=validator,
        mapper=mapper,
        generator=generator,
        mcp_adapter=mcp_adapter,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info("bootstrap_started", extra={"event": "bootstrap_start"})
        report = orchestrator.bootstrap()
        app.state.generation_report = report
        app.state.mcp_adapter = mcp_adapter
        app.state.mcp_native = mcp_adapter.supports_streamable_http
        app.state.runtime_metrics = metrics
        logger.info(
            "bootstrap_completed",
            extra={
                "event": "bootstrap_complete",
                "generated_count": report.generated_count,
                "warning_count": len(report.warnings),
                "mcp_native": app.state.mcp_native,
            },
        )
        if mcp_adapter.supports_streamable_http:
            async with mcp_adapter.native_lifespan():
                try:
                    yield
                finally:
                    metrics.shutdown()
            return
        try:
            yield
        finally:
            metrics.shutdown()

    app = FastAPI(title="openapi-to-mcp", version=__version__, lifespan=lifespan)

    @app.middleware("http")
    async def http_red_metrics_middleware(request, call_next):  # type: ignore[no-untyped-def]
        started = perf_counter()
        route = request.url.path
        method = request.method
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            metrics.on_http_request_completed(
                route=route,
                method=method,
                status_code=status_code,
                duration_seconds=perf_counter() - started,
            )

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/metrics")
    async def metrics_endpoint() -> Response:
        rendered = metrics.render()
        return Response(
            content=rendered.payload,
            media_type=rendered.content_type,
            headers={
                "Deprecation": "true",
                "Warning": '299 - "GET /metrics is deprecated; use OTLP export to Collector."',
            },
        )

    if mcp_adapter.supports_streamable_http:
        app.mount("", mcp_adapter.streamable_http_app())
    else:

        @app.post("/mcp")
        async def fallback_mcp_endpoint(request: FallbackToolCallRequest) -> Any:
            logger.info(
                "fallback_tool_invoke",
                extra={"event": "fallback_tool_invoke", "tool": request.tool},
            )
            try:
                return await mcp_adapter.invoke_fallback(request.tool, request.arguments)
            except InvocationError as exc:
                logger.warning(
                    "fallback_tool_not_found",
                    extra={"event": "fallback_tool_not_found", "tool": request.tool},
                )
                raise HTTPException(status_code=404, detail=str(exc)) from exc

    return app


def _build_openapi_source(settings: Settings) -> OpenApiSourcePort:
    source_type, source_value = settings.resolve_openapi_source()
    if source_type == "path":
        return FileOpenApiSourceAdapter(source_value)
    return UrlOpenApiSourceAdapter(source_value)
