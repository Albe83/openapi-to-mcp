from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from openapi_to_mcp import __version__
from openapi_to_mcp.config import Settings
from openapi_to_mcp.transport.app import create_app


class StubInvoker:
    async def invoke(self, binding, payload):
        return {"ok": True, "binding": binding, "payload": payload}


def test_app_healthz_and_fallback_mcp(tmp_path: Path) -> None:
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

    settings = Settings.from_env({"OPENAPI_SPEC_PATH": str(spec_file)})
    app = create_app(settings, invoker_override=StubInvoker())
    assert app.version == __version__

    with TestClient(app) as client:
        health = client.get("/healthz")
        assert health.status_code == 200
        assert health.json() == {"status": "ok"}

        metrics = client.get("/metrics")
        assert metrics.status_code == 404

        if not app.state.mcp_native:
            response = client.post("/mcp", json={"tool": "getPet", "arguments": {"petId": "123"}})
            assert response.status_code == 200
            body = response.json()
            assert body["ok"] is True
            assert body["payload"]["petId"] == "123"


def test_app_exposes_metrics_only_when_prometheus_toggle_enabled(tmp_path: Path) -> None:
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

    settings = Settings.from_env(
        {
            "OPENAPI_SPEC_PATH": str(spec_file),
            "PROMETHEUS_METRICS_ENABLED": "true",
        }
    )
    app = create_app(settings, invoker_override=StubInvoker())

    with TestClient(app) as client:
        health = client.get("/healthz")
        assert health.status_code == 200

        metrics = client.get("/metrics")
        assert metrics.status_code == 200
        assert "text/plain" in metrics.headers["content-type"]
        assert "openapi_to_mcp_http_server_requests" in metrics.text
