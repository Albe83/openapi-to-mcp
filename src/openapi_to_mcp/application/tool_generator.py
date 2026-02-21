"""Generate MCP tools from mapped OpenAPI operations."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

from openapi_to_mcp.domain.models import ApiOperation, GeneratedTool, GenerationReport


class ToolGenerationService:
    """Generate tool contracts and invocation bindings."""

    def generate(
        self, operations: List[ApiOperation]
    ) -> Tuple[List[GeneratedTool], GenerationReport]:
        tools: List[GeneratedTool] = []
        report = GenerationReport()
        seen_names: set[str] = set()

        for operation in operations:
            tool_name = _build_tool_name(operation)
            if tool_name in seen_names:
                report.skipped_count += 1
                report.errors.append(
                    f"Duplicate tool name '{tool_name}' "
                    f"for {operation.method.upper()} {operation.path}."
                )
                continue

            seen_names.add(tool_name)
            tools.append(
                GeneratedTool(
                    name=tool_name,
                    description=_build_description(operation),
                    input_schema=_build_input_schema(operation),
                    binding=_build_binding(operation),
                )
            )
            report.generated_count += 1

        return tools, report


def _build_tool_name(operation: ApiOperation) -> str:
    if operation.operation_id:
        return _sanitize_identifier(operation.operation_id)
    return f"{operation.method.lower()}_{_sanitize_path(operation.path)}"


def _build_description(operation: ApiOperation) -> str:
    if operation.summary:
        return operation.summary
    return f"Invoke {operation.method.upper()} {operation.path}"


def _build_input_schema(operation: ApiOperation) -> Dict[str, Any]:
    properties: Dict[str, Any] = {}
    required: List[str] = []

    for parameter in operation.parameters:
        name = parameter.get("name")
        if not isinstance(name, str) or not name:
            continue

        schema = parameter.get("schema")
        if not isinstance(schema, dict):
            schema = {"type": "string"}

        properties[name] = schema
        if parameter.get("required") is True:
            required.append(name)

    if operation.request_body_schema is not None:
        properties["body"] = operation.request_body_schema
        if operation.request_body_required:
            required.append("body")

    output: Dict[str, Any] = {"type": "object", "properties": properties}
    if required:
        output["required"] = sorted(set(required))
    return output


def _build_binding(operation: ApiOperation) -> Dict[str, Any]:
    path_params = []
    query_params = []
    header_params = []

    for parameter in operation.parameters:
        name = parameter.get("name")
        where = parameter.get("in")
        if not isinstance(name, str) or not isinstance(where, str):
            continue
        if where == "path":
            path_params.append(name)
        elif where == "query":
            query_params.append(name)
        elif where == "header":
            header_params.append(name)

    return {
        "method": operation.method,
        "path": operation.path,
        "server_url": operation.server_url,
        "path_params": path_params,
        "query_params": query_params,
        "header_params": header_params,
    }


def _sanitize_identifier(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip())
    normalized = re.sub(r"_+", "_", normalized)
    return normalized.strip("_") or "tool"


def _sanitize_path(path: str) -> str:
    transformed = path.strip("/")
    transformed = transformed.replace("{", "by_").replace("}", "")
    transformed = transformed.replace("/", "_")
    return _sanitize_identifier(transformed or "root")
