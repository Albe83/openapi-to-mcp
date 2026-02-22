"""Environment-driven runtime configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping, Optional

from .errors import ConfigurationError

_ALLOWED_LOG_LEVELS = {"critical", "error", "warning", "info", "debug"}
_ALLOWED_TELEMETRY_PROTOCOLS = {"grpc", "http"}


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    openapi_spec_path: Optional[str]
    openapi_spec_url: Optional[str]
    mcp_host: str = "0.0.0.0"
    mcp_port: int = 8080
    log_level: str = "info"
    http_max_in_flight: int = 128
    http_max_connections: int = 100
    http_max_keepalive_connections: int = 20
    telemetry_otlp_protocol: str = "grpc"
    telemetry_otlp_endpoint: str = "http://127.0.0.1:4317"
    telemetry_export_interval_ms: int = 60000
    service_name: str = "openapi-to-mcp"
    service_namespace: str = "openapi-to-mcp"
    deployment_environment: str = "dev"

    @classmethod
    def from_env(cls, env: Optional[Mapping[str, str]] = None) -> "Settings":
        values = env or os.environ
        telemetry_protocol = values.get("TELEMETRY_OTLP_PROTOCOL", "grpc").strip().lower()
        telemetry_endpoint = (
            _normalize_optional(values.get("TELEMETRY_OTLP_ENDPOINT"))
            or _default_otlp_endpoint(telemetry_protocol)
        )
        settings = cls(
            openapi_spec_path=_normalize_optional(values.get("OPENAPI_SPEC_PATH")),
            openapi_spec_url=_normalize_optional(values.get("OPENAPI_SPEC_URL")),
            mcp_host=values.get("MCP_HOST", "0.0.0.0"),
            mcp_port=_parse_port(values.get("MCP_PORT", "8080")),
            log_level=values.get("LOG_LEVEL", "info").strip().lower(),
            http_max_in_flight=_parse_positive_int(
                values.get("HTTP_MAX_IN_FLIGHT", "128"), "HTTP_MAX_IN_FLIGHT"
            ),
            http_max_connections=_parse_positive_int(
                values.get("HTTP_MAX_CONNECTIONS", "100"), "HTTP_MAX_CONNECTIONS"
            ),
            http_max_keepalive_connections=_parse_non_negative_int(
                values.get("HTTP_MAX_KEEPALIVE_CONNECTIONS", "20"),
                "HTTP_MAX_KEEPALIVE_CONNECTIONS",
            ),
            telemetry_otlp_protocol=telemetry_protocol,
            telemetry_otlp_endpoint=telemetry_endpoint,
            telemetry_export_interval_ms=_parse_positive_int(
                values.get("TELEMETRY_EXPORT_INTERVAL_MS", "60000"),
                "TELEMETRY_EXPORT_INTERVAL_MS",
            ),
            service_name=_parse_non_empty_string(
                values.get("SERVICE_NAME", "openapi-to-mcp"), "SERVICE_NAME"
            ),
            service_namespace=_parse_non_empty_string(
                values.get("SERVICE_NAMESPACE", "openapi-to-mcp"), "SERVICE_NAMESPACE"
            ),
            deployment_environment=_parse_non_empty_string(
                values.get("DEPLOYMENT_ENVIRONMENT", "dev"), "DEPLOYMENT_ENVIRONMENT"
            ),
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        if not self.openapi_spec_path and not self.openapi_spec_url:
            raise ConfigurationError(
                "At least one of OPENAPI_SPEC_PATH or OPENAPI_SPEC_URL must be set."
            )
        if self.mcp_port <= 0 or self.mcp_port > 65535:
            raise ConfigurationError("MCP_PORT must be in range 1..65535.")
        if not self.mcp_host.strip():
            raise ConfigurationError("MCP_HOST must not be empty.")
        if self.log_level not in _ALLOWED_LOG_LEVELS:
            allowed = ", ".join(sorted(_ALLOWED_LOG_LEVELS))
            raise ConfigurationError(f"LOG_LEVEL must be one of: {allowed}.")
        if self.http_max_keepalive_connections > self.http_max_connections:
            raise ConfigurationError(
                "HTTP_MAX_KEEPALIVE_CONNECTIONS must be <= HTTP_MAX_CONNECTIONS."
            )
        if self.telemetry_otlp_protocol not in _ALLOWED_TELEMETRY_PROTOCOLS:
            allowed = ", ".join(sorted(_ALLOWED_TELEMETRY_PROTOCOLS))
            raise ConfigurationError(
                f"TELEMETRY_OTLP_PROTOCOL must be one of: {allowed}."
            )
        if not self.telemetry_otlp_endpoint.strip():
            raise ConfigurationError("TELEMETRY_OTLP_ENDPOINT must not be empty.")

    def resolve_openapi_source(self) -> tuple[str, str]:
        """Resolve source type and value with path precedence when both are set."""
        if self.openapi_spec_path:
            return ("path", self.openapi_spec_path)
        if self.openapi_spec_url:
            return ("url", self.openapi_spec_url)
        raise ConfigurationError("No OpenAPI source configured.")


def _normalize_optional(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = value.strip()
    return text or None


def _parse_port(value: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise ConfigurationError("MCP_PORT must be an integer.") from exc


def _parse_positive_int(value: str, field_name: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ConfigurationError(f"{field_name} must be an integer.") from exc
    if parsed <= 0:
        raise ConfigurationError(f"{field_name} must be > 0.")
    return parsed


def _parse_non_negative_int(value: str, field_name: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ConfigurationError(f"{field_name} must be an integer.") from exc
    if parsed < 0:
        raise ConfigurationError(f"{field_name} must be >= 0.")
    return parsed


def _parse_non_empty_string(value: str, field_name: str) -> str:
    text = value.strip()
    if not text:
        raise ConfigurationError(f"{field_name} must not be empty.")
    return text


def _default_otlp_endpoint(protocol: str) -> str:
    if protocol == "http":
        return "http://127.0.0.1:4318/v1/metrics"
    return "http://127.0.0.1:4317"
