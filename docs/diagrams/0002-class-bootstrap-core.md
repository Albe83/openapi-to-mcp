# Class Diagram - Bootstrap Core

- Parent issue: [#1](https://github.com/Albe83/openapi-to-mcp/issues/1)
- ADR: [docs/adr/0001-python-fastapi-fastmcp-bootstrap.md](../adr/0001-python-fastapi-fastmcp-bootstrap.md)
- Purpose: Show the core domain, ports, and adapters for startup and runtime mapping.

```mermaid
classDiagram
  class Settings {
    +openapi_spec_path: str?
    +openapi_spec_url: str?
    +mcp_host: str
    +mcp_port: int
    +log_level: str
    +validate()
  }

  class ApiOperation {
    +method: str
    +path: str
    +operation_id: str?
    +summary: str?
    +parameters: list
    +request_body_schema: object?
  }

  class GeneratedTool {
    +name: str
    +description: str
    +input_schema: object
    +binding: object
  }

  class GenerationReport {
    +generated_count: int
    +skipped_count: int
    +errors: list
    +warnings: list
  }

  class OpenApiSourcePort {
    <<interface>>
    +load_raw() dict
  }

  class OpenApiValidatorPort {
    <<interface>>
    +validate(raw) dict
  }

  class OperationMapper {
    +map_operations(spec) list~ApiOperation~
  }

  class ToolGenerationService {
    +generate(operations) tuple~list~GeneratedTool~, GenerationReport~
  }

  class HttpInvokerPort {
    <<interface>>
    +invoke(binding, payload) object
  }

  class FastMcpAdapter {
    +register_tools(tools)
    +mount_http_transport(app)
  }

  class StartupOrchestrator {
    +bootstrap() GenerationReport
  }

  Settings --> StartupOrchestrator
  OpenApiSourcePort <|.. FileOpenApiSourceAdapter
  OpenApiSourcePort <|.. UrlOpenApiSourceAdapter
  OpenApiValidatorPort <|.. OpenApiValidatorAdapter
  HttpInvokerPort <|.. HttpxInvokerAdapter
  StartupOrchestrator --> OpenApiSourcePort
  StartupOrchestrator --> OpenApiValidatorPort
  StartupOrchestrator --> OperationMapper
  StartupOrchestrator --> ToolGenerationService
  StartupOrchestrator --> FastMcpAdapter
  FastMcpAdapter --> HttpInvokerPort
  ToolGenerationService --> GeneratedTool
  ToolGenerationService --> GenerationReport
  OperationMapper --> ApiOperation
```
