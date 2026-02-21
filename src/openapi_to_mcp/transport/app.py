"""FastAPI application wiring and runtime bootstrap."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from openapi_to_mcp.adapters.http_invoker import HttpxInvokerAdapter
from openapi_to_mcp.adapters.openapi_source import FileOpenApiSourceAdapter, UrlOpenApiSourceAdapter
from openapi_to_mcp.adapters.openapi_validator import OpenApiValidatorAdapter
from openapi_to_mcp.application.mapper import OperationMapper
from openapi_to_mcp.application.startup import StartupOrchestrator
from openapi_to_mcp.application.tool_generator import ToolGenerationService
from openapi_to_mcp.config import Settings
from openapi_to_mcp.errors import InvocationError
from openapi_to_mcp.ports import HttpInvokerPort, OpenApiSourcePort
from openapi_to_mcp.transport.fastmcp_adapter import FastMcpAdapter


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
    invoker = invoker_override or HttpxInvokerAdapter()
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
        report = orchestrator.bootstrap()
        app.state.generation_report = report
        app.state.mcp_adapter = mcp_adapter
        app.state.mcp_native = mcp_adapter.supports_streamable_http
        yield

    app = FastAPI(title="openapi-to-mcp", version="0.0.1", lifespan=lifespan)

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    if mcp_adapter.supports_streamable_http:
        app.mount("/mcp", mcp_adapter.streamable_http_app())
    else:

        @app.post("/mcp")
        async def fallback_mcp_endpoint(request: FallbackToolCallRequest) -> Any:
            try:
                return await mcp_adapter.invoke_fallback(request.tool, request.arguments)
            except InvocationError as exc:
                raise HTTPException(status_code=404, detail=str(exc)) from exc

    return app


def _build_openapi_source(settings: Settings) -> OpenApiSourcePort:
    source_type, source_value = settings.resolve_openapi_source()
    if source_type == "path":
        return FileOpenApiSourceAdapter(source_value)
    return UrlOpenApiSourceAdapter(source_value)
