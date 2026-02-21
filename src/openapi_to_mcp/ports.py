"""Hexagonal ports for IO and integration boundaries."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Protocol


@dataclass(frozen=True)
class OpenApiValidationResult:
    """Validation output with normalized spec and non-fatal warnings."""

    spec: Dict[str, Any]
    warnings: List[str] = field(default_factory=list)


class OpenApiSourcePort(Protocol):
    """Port for reading an OpenAPI document from a source."""

    def load_raw(self) -> Dict[str, Any]:
        """Load raw OpenAPI content as a dictionary."""


class OpenApiValidatorPort(Protocol):
    """Port for validating and normalizing an OpenAPI document."""

    def validate(self, raw_spec: Dict[str, Any]) -> OpenApiValidationResult:
        """Validate and normalize OpenAPI content."""


class HttpInvokerPort(Protocol):
    """Port for invoking downstream REST endpoints."""

    async def invoke(self, binding: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke a downstream operation and return normalized response payload."""
