"""Project-specific exceptions."""


class OpenApiToMcpError(Exception):
    """Base exception for application errors."""


class ConfigurationError(OpenApiToMcpError):
    """Raised when runtime configuration is invalid."""


class SourceLoadError(OpenApiToMcpError):
    """Raised when OpenAPI source loading fails."""


class OpenApiValidationError(OpenApiToMcpError):
    """Raised when critical OpenAPI validation fails."""


class InvocationError(OpenApiToMcpError):
    """Raised when downstream invocation fails."""


class ToolRegistrationError(OpenApiToMcpError):
    """Raised when MCP tool registration fails."""
