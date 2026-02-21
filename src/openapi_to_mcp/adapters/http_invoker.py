"""HTTP invocation adapter for downstream REST calls."""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional
from urllib.parse import quote

import httpx

from openapi_to_mcp.errors import InvocationError


class HttpxInvokerAdapter:
    """Invoke downstream REST operations using HTTPX."""

    def __init__(
        self,
        timeout_seconds: float = 10.0,
        client_factory: Optional[Callable[[], httpx.AsyncClient]] = None,
    ) -> None:
        self._timeout_seconds = timeout_seconds
        self._client_factory = client_factory

    async def invoke(self, binding: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        method = str(binding.get("method", "")).upper()
        path = str(binding.get("path", ""))
        server_url = str(binding.get("server_url", "")).strip()

        if not method or not path:
            raise InvocationError("Invalid binding: missing method or path.")

        url_path = _render_path(path, binding.get("path_params", []), payload)
        url = _build_url(server_url, url_path)

        query_params = {
            name: payload[name]
            for name in binding.get("query_params", [])
            if name in payload and payload[name] is not None
        }
        headers = {
            name: str(payload[name])
            for name in binding.get("header_params", [])
            if name in payload and payload[name] is not None
        }
        json_body = payload.get("body")

        async with self._make_client() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    params=query_params,
                    headers=headers,
                    json=json_body,
                )
            except httpx.HTTPError as exc:
                raise InvocationError(f"HTTP invocation failed for {method} {url}.") from exc

        body: Any
        try:
            body = response.json()
        except ValueError:
            body = response.text

        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": body,
        }

    def _make_client(self) -> httpx.AsyncClient:
        if self._client_factory is not None:
            return self._client_factory()
        return httpx.AsyncClient(timeout=self._timeout_seconds)


def _build_url(server_url: str, path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not server_url:
        raise InvocationError("No server_url available for relative path invocation.")
    return f"{server_url.rstrip('/')}{path}"


def _render_path(path: str, path_params: list[str], payload: Dict[str, Any]) -> str:
    rendered = path
    for key in path_params:
        if key not in payload:
            raise InvocationError(f"Missing required path parameter: {key}")
        rendered = rendered.replace(f"{{{key}}}", quote(str(payload[key]), safe=""))
    return rendered
