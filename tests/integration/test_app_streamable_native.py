from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from openapi_to_mcp import __version__
from openapi_to_mcp.config import Settings
from openapi_to_mcp.transport.app import create_app

pytest.importorskip("mcp.server.fastmcp")


class StubInvoker:
    async def invoke(self, binding, payload):
        return {"ok": True, "binding": binding, "payload": payload}


def _write_spec(tmp_path: Path) -> Path:
    spec_file = tmp_path / "openapi.yaml"
    spec_file.write_text(
        """
openapi: 3.1.0
info:
  title: Demo
  version: 1.0.0
servers:
  - url: https://api.example.com
paths:
  /pets/{petId}:
    get:
      operationId: getPet
      parameters:
        - name: petId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: ok
""".strip(),
        encoding="utf-8",
    )
    return spec_file


def test_native_streamable_request_uses_canonical_mcp_path_without_trailing_slash(
    tmp_path: Path,
) -> None:
    spec_file = _write_spec(tmp_path)
    settings = Settings.from_env({"OPENAPI_SPEC_PATH": str(spec_file)})
    app = create_app(settings, invoker_override=StubInvoker())

    with TestClient(app) as client:
        if not app.state.mcp_native:
            pytest.skip("FastMCP native mode not available in this environment")

        headers = {
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
            "Host": "127.0.0.1",
        }
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "pytest", "version": __version__},
            },
        }

        canonical = client.post("/mcp", json=payload, headers=headers, follow_redirects=False)
        trailing = client.post("/mcp/", json=payload, headers=headers, follow_redirects=False)

        assert canonical.status_code != 307
        assert canonical.status_code != 500
        assert trailing.status_code == 307
        assert trailing.headers.get("location", "").endswith("/mcp")
