"""FastMCP transport adapter with local fallback when package is unavailable."""

from __future__ import annotations

import inspect
from typing import Any, Callable, Dict

from openapi_to_mcp.domain.models import GeneratedTool
from openapi_to_mcp.errors import InvocationError, ToolRegistrationError
from openapi_to_mcp.ports import HttpInvokerPort

try:
    from mcp.server.fastmcp import FastMCP  # type: ignore
except Exception:  # pragma: no cover - environment dependent
    FastMCP = None  # type: ignore


class _LocalMcpServer:
    """Very small fallback MCP-like runtime for environments without FastMCP."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._tools: Dict[str, Callable[..., Any]] = {}

    def tool(self, name: str | None = None, description: str | None = None) -> Callable[..., Any]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            tool_name = name or func.__name__
            self._tools[tool_name] = func
            return func

        return decorator

    async def invoke(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        func = self._tools.get(tool_name)
        if func is None:
            raise InvocationError(f"Tool not found: {tool_name}")

        result = func(**arguments)
        if inspect.isawaitable(result):
            return await result
        return result


class FastMcpAdapter:
    """Adapter that registers generated tools into FastMCP or local fallback."""

    def __init__(self, invoker: HttpInvokerPort, server_name: str = "openapi-to-mcp") -> None:
        self._invoker = invoker
        self._server_name = server_name
        self._native = FastMCP is not None
        self._runtime = FastMCP(server_name) if self._native else _LocalMcpServer(server_name)

    @property
    def supports_streamable_http(self) -> bool:
        return self._native and hasattr(self._runtime, "streamable_http_app")

    def streamable_http_app(self) -> Any:
        if not self.supports_streamable_http:
            raise ToolRegistrationError("FastMCP streamable HTTP app is not available.")
        return self._runtime.streamable_http_app()  # type: ignore[no-any-return]

    def register_tools(self, tools: list[GeneratedTool]) -> None:
        for tool in tools:
            self._register_single_tool(tool)

    async def invoke_fallback(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        if self._native:
            raise InvocationError("Fallback invoke is only available in local MCP mode.")
        return await self._runtime.invoke(tool_name, arguments)

    def _register_single_tool(self, tool: GeneratedTool) -> None:
        async def dynamic_tool(**kwargs: Any) -> Dict[str, Any]:
            return await self._invoker.invoke(tool.binding, kwargs)

        try:
            decorator = self._runtime.tool(name=tool.name, description=tool.description)
            decorator(dynamic_tool)
        except Exception as exc:  # pragma: no cover - defensive against runtime API changes
            raise ToolRegistrationError(f"Cannot register tool: {tool.name}") from exc
