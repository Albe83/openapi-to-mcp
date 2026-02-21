"""OpenAPI validation adapter with strict critical checks."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List

from openapi_to_mcp.errors import OpenApiValidationError
from openapi_to_mcp.ports import OpenApiValidationResult

_ALLOWED_HTTP_METHODS = {
    "get",
    "post",
    "put",
    "delete",
    "patch",
    "options",
    "head",
    "trace",
}


class OpenApiValidatorAdapter:
    """Validate critical OpenAPI structure and emit non-fatal warnings."""

    def validate(self, raw_spec: Dict[str, Any]) -> OpenApiValidationResult:
        if not isinstance(raw_spec, dict):
            raise OpenApiValidationError("OpenAPI content must be an object.")

        spec = deepcopy(raw_spec)
        warnings: List[str] = []

        openapi_version = spec.get("openapi")
        if not isinstance(openapi_version, str) or not openapi_version.strip():
            raise OpenApiValidationError("Missing or invalid 'openapi' version.")

        paths = spec.get("paths")
        if not isinstance(paths, dict) or not paths:
            raise OpenApiValidationError("Missing or invalid 'paths' section.")

        root_server_url = _extract_first_server_url(spec.get("servers"))
        for path, path_item in paths.items():
            if not isinstance(path, str) or not path.startswith("/"):
                raise OpenApiValidationError("Each path key must be a string starting with '/'.")
            if not isinstance(path_item, dict):
                raise OpenApiValidationError(f"Path item must be an object for '{path}'.")

            path_server_url = _extract_first_server_url(path_item.get("servers"))
            for method, operation in path_item.items():
                if method not in _ALLOWED_HTTP_METHODS:
                    # Non-method keys such as parameters are allowed at path-item level.
                    continue
                if not isinstance(operation, dict):
                    raise OpenApiValidationError(
                        f"Operation '{method.upper()} {path}' must be an object."
                    )
                if not operation.get("operationId"):
                    warnings.append(f"Missing operationId for {method.upper()} {path}.")
                operation_server_url = _extract_first_server_url(operation.get("servers"))
                resolved_server_url = operation_server_url or path_server_url or root_server_url
                if not resolved_server_url:
                    raise OpenApiValidationError(
                        f"Missing server URL for operation '{method.upper()} {path}'. "
                        "Define servers at operation, path, or root level."
                    )

        return OpenApiValidationResult(spec=spec, warnings=warnings)


def _extract_first_server_url(servers: Any) -> str | None:
    if not isinstance(servers, list) or not servers:
        return None
    first = servers[0]
    if not isinstance(first, dict):
        return None
    url = first.get("url")
    if isinstance(url, str) and url.strip():
        return url.strip()
    return None
