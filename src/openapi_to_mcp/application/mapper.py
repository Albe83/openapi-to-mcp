"""Map validated OpenAPI documents to domain operations."""

from __future__ import annotations

from typing import Any, Dict, List

from openapi_to_mcp.domain.models import ApiOperation

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


class OperationMapper:
    """Translate OpenAPI path/operation objects into ApiOperation models."""

    def map_operations(self, spec: Dict[str, Any]) -> List[ApiOperation]:
        paths = spec.get("paths", {})
        root_server_url = _extract_first_server_url(spec.get("servers"))
        mapped: List[ApiOperation] = []

        for path, path_item in paths.items():
            if not isinstance(path_item, dict):
                continue

            path_server_url = _extract_first_server_url(path_item.get("servers"))
            path_level_parameters = _extract_parameters(path_item.get("parameters", []))

            for method, operation in path_item.items():
                if method not in _ALLOWED_HTTP_METHODS or not isinstance(operation, dict):
                    continue

                op_parameters = _extract_parameters(operation.get("parameters", []))
                merged_parameters = _merge_parameters(path_level_parameters, op_parameters)

                mapped.append(
                    ApiOperation(
                        method=method,
                        path=path,
                        operation_id=operation.get("operationId"),
                        summary=operation.get("summary") or operation.get("description"),
                        parameters=merged_parameters,
                        request_body_schema=_extract_request_body_schema(operation),
                        request_body_required=bool(
                            operation.get("requestBody", {}).get("required", False)
                        ),
                        server_url=_resolve_server_url(operation, path_server_url, root_server_url),
                    )
                )

        return mapped


def _extract_first_server_url(servers: Any) -> str | None:
    if not isinstance(servers, list) or not servers:
        return None
    first = servers[0]
    if not isinstance(first, dict):
        return None
    value = first.get("url")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _resolve_server_url(
    operation: Dict[str, Any], path_server_url: str | None, root_server_url: str | None
) -> str | None:
    operation_server_url = _extract_first_server_url(operation.get("servers"))
    return operation_server_url or path_server_url or root_server_url


def _extract_parameters(raw_parameters: Any) -> List[Dict[str, Any]]:
    if not isinstance(raw_parameters, list):
        return []
    return [p for p in raw_parameters if isinstance(p, dict)]


def _merge_parameters(
    path_level: List[Dict[str, Any]],
    operation_level: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    merged: Dict[tuple[str, str], Dict[str, Any]] = {}
    for candidate in path_level + operation_level:
        name = str(candidate.get("name", ""))
        where = str(candidate.get("in", ""))
        if not name or not where:
            continue
        merged[(name, where)] = candidate
    return list(merged.values())


def _extract_request_body_schema(operation: Dict[str, Any]) -> Dict[str, Any] | None:
    request_body = operation.get("requestBody")
    if not isinstance(request_body, dict):
        return None

    content = request_body.get("content")
    if not isinstance(content, dict):
        return None

    if "application/json" in content and isinstance(content["application/json"], dict):
        schema = content["application/json"].get("schema")
        if isinstance(schema, dict):
            return schema

    for media_entry in content.values():
        if isinstance(media_entry, dict) and isinstance(media_entry.get("schema"), dict):
            return media_entry["schema"]
    return None
