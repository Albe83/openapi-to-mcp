# Sequence Diagram - Startup and Tool Call

- Parent issue: [#1](https://github.com/Albe83/openapi-to-mcp/issues/1)
- ADR: [docs/adr/0001-python-fastapi-fastmcp-bootstrap.md](../adr/0001-python-fastapi-fastmcp-bootstrap.md)
- Purpose: Show startup bootstrap flow and tool invocation flow.

```mermaid
sequenceDiagram
  participant Runtime as App Runtime
  participant Config as Settings Loader
  participant Source as OpenApiSourcePort Adapter
  participant Validator as OpenApiValidatorPort Adapter
  participant Mapper as OperationMapper
  participant Generator as ToolGenerationService
  participant MCP as FastMcpAdapter
  participant HTTP as HttpInvokerPort Adapter

  Runtime->>Config: load env configuration
  Config-->>Runtime: Settings
  Runtime->>Source: load_raw()
  Source-->>Runtime: Raw OpenAPI
  Runtime->>Validator: validate(raw)
  Validator-->>Runtime: Validated OpenAPI
  Runtime->>Mapper: map_operations(spec)
  Mapper-->>Runtime: ApiOperation[]
  Runtime->>Generator: generate(operations)
  Generator-->>Runtime: GeneratedTool[] + GenerationReport
  Runtime->>MCP: register_tools(generated_tools)
  MCP-->>Runtime: registration complete

  Note over Runtime,MCP: Runtime ready and MCP endpoint exposed

  participant Agent as AI Agent
  Agent->>MCP: tool call(name, input)
  MCP->>HTTP: invoke(binding, input)
  HTTP-->>MCP: downstream REST response
  MCP-->>Agent: tool result payload
```
