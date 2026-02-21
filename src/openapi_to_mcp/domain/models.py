"""Domain models for OpenAPI operation mapping and tool generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ApiOperation:
    """A normalized representation of one API operation."""

    method: str
    path: str
    operation_id: Optional[str]
    summary: Optional[str]
    parameters: List[Dict[str, Any]]
    request_body_schema: Optional[Dict[str, Any]]
    request_body_required: bool
    server_url: Optional[str]


@dataclass(frozen=True)
class GeneratedTool:
    """A generated MCP tool contract and invocation binding."""

    name: str
    description: str
    input_schema: Dict[str, Any]
    binding: Dict[str, Any]


@dataclass
class GenerationReport:
    """Tool generation summary."""

    generated_count: int = 0
    skipped_count: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
