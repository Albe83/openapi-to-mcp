from __future__ import annotations

from openapi_to_mcp.application.mapper import OperationMapper
from openapi_to_mcp.application.startup import StartupOrchestrator
from openapi_to_mcp.application.tool_generator import ToolGenerationService
from openapi_to_mcp.ports import OpenApiValidationResult


class StubSource:
    def load_raw(self):
        return {
            "openapi": "3.1.0",
            "servers": [{"url": "https://api.example.com"}],
            "paths": {
                "/items": {
                    "get": {
                        "operationId": "listItems",
                        "responses": {"200": {"description": "ok"}},
                    }
                }
            },
        }


class StubValidator:
    def validate(self, raw_spec):
        return OpenApiValidationResult(spec=raw_spec, warnings=["sample warning"])


class StubMcpAdapter:
    def __init__(self):
        self.registered_tools = []

    def register_tools(self, tools):
        self.registered_tools.extend(tools)


def test_startup_orchestrator_bootstraps_and_registers_tools() -> None:
    mcp = StubMcpAdapter()
    orchestrator = StartupOrchestrator(
        source=StubSource(),
        validator=StubValidator(),
        mapper=OperationMapper(),
        generator=ToolGenerationService(),
        mcp_adapter=mcp,
    )

    report = orchestrator.bootstrap()

    assert report.generated_count == 1
    assert len(mcp.registered_tools) == 1
    assert report.warnings == ["sample warning"]
