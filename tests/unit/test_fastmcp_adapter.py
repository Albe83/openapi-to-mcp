from __future__ import annotations

import pytest

pytest.importorskip("mcp.server.fastmcp")

from openapi_to_mcp.domain.models import GeneratedTool
from openapi_to_mcp.transport.fastmcp_adapter import FastMcpAdapter


class StubInvoker:
    async def invoke(self, binding, payload):
        return {"ok": True, "binding": binding, "payload": payload}


def test_fastmcp_adapter_native_streamable_app() -> None:
    adapter = FastMcpAdapter(invoker=StubInvoker())

    if not adapter.supports_streamable_http:
        pytest.skip("FastMCP streamable HTTP transport not available in this environment")

    tool = GeneratedTool(
        name="getPet",
        description="Get a pet",
        input_schema={"type": "object"},
        binding={"method": "get", "path": "/pets/{petId}", "server_url": "https://api.example.com"},
    )

    adapter.register_tools([tool])
    app = adapter.streamable_http_app()
    cached = adapter.streamable_http_app()

    assert app is not None
    assert callable(app)
    assert app is cached
    paths = [getattr(route, "path", None) for route in getattr(app, "routes", [])]
    assert "/" in paths
