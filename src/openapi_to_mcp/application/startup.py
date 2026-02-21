"""Startup orchestration service."""

from __future__ import annotations

from dataclasses import dataclass

from openapi_to_mcp.application.mapper import OperationMapper
from openapi_to_mcp.application.tool_generator import ToolGenerationService
from openapi_to_mcp.domain.models import GenerationReport
from openapi_to_mcp.ports import OpenApiSourcePort, OpenApiValidatorPort
from openapi_to_mcp.transport.fastmcp_adapter import FastMcpAdapter


@dataclass
class StartupOrchestrator:
    """Coordinates bootstrap sequence from spec loading to tool registration."""

    source: OpenApiSourcePort
    validator: OpenApiValidatorPort
    mapper: OperationMapper
    generator: ToolGenerationService
    mcp_adapter: FastMcpAdapter

    def bootstrap(self) -> GenerationReport:
        raw_spec = self.source.load_raw()
        validation = self.validator.validate(raw_spec)
        operations = self.mapper.map_operations(validation.spec)
        generated_tools, report = self.generator.generate(operations)
        report.warnings.extend(validation.warnings)
        self.mcp_adapter.register_tools(generated_tools)
        return report
