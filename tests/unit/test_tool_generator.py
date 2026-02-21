from __future__ import annotations

from openapi_to_mcp.application.tool_generator import ToolGenerationService
from openapi_to_mcp.domain.models import ApiOperation


def test_generator_uses_operation_id_when_present() -> None:
    operation = ApiOperation(
        method="get",
        path="/pets/{petId}",
        operation_id="getPet",
        summary="Get pet",
        parameters=[],
        request_body_schema=None,
        request_body_required=False,
        server_url="https://api.example.com",
    )

    tools, report = ToolGenerationService().generate([operation])

    assert report.generated_count == 1
    assert tools[0].name == "getPet"


def test_generator_uses_fallback_name_and_input_schema() -> None:
    operation = ApiOperation(
        method="post",
        path="/pets/{petId}",
        operation_id=None,
        summary=None,
        parameters=[
            {"name": "petId", "in": "path", "required": True, "schema": {"type": "string"}},
            {
                "name": "includeHistory",
                "in": "query",
                "required": False,
                "schema": {"type": "boolean"},
            },
        ],
        request_body_schema={"type": "object"},
        request_body_required=True,
        server_url="https://api.example.com",
    )

    tools, _ = ToolGenerationService().generate([operation])
    tool = tools[0]

    assert tool.name == "post_pets_by_petId"
    assert tool.input_schema["required"] == ["body", "petId"]
    assert tool.binding["path_params"] == ["petId"]
    assert tool.binding["query_params"] == ["includeHistory"]
