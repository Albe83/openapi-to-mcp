# Hexagonal Diagram - Bootstrap Boundaries

- Parent issue: [#1](https://github.com/Albe83/openapi-to-mcp/issues/1)
- ADR: [docs/adr/0001-python-fastapi-fastmcp-bootstrap.md](../adr/0001-python-fastapi-fastmcp-bootstrap.md)
- Purpose: Show inbound and outbound ports/adapters and dependency direction.

```mermaid
flowchart LR
  subgraph InboundAdapters[Inbound Adapters]
    FastAPI[FastAPI App]
    FastMCP[FastMCP Transport]
  end

  subgraph Core[Application and Domain Core]
    Orchestrator[StartupOrchestrator]
    Mapper[OperationMapper]
    Generator[ToolGenerationService]
    Domain[(ApiOperation / GeneratedTool / GenerationReport)]
    SourcePort[[OpenApiSourcePort]]
    ValidatorPort[[OpenApiValidatorPort]]
    InvokerPort[[HttpInvokerPort]]
  end

  subgraph OutboundAdapters[Outbound Adapters]
    FileLoader[FileOpenApiSourceAdapter]
    UrlLoader[UrlOpenApiSourceAdapter]
    Validator[OpenApiValidatorAdapter]
    HttpxInvoker[HttpxInvokerAdapter]
    RemoteApi[(Target REST API)]
  end

  FastAPI --> Orchestrator
  FastMCP --> Orchestrator

  Orchestrator --> SourcePort
  Orchestrator --> ValidatorPort
  Orchestrator --> Mapper
  Orchestrator --> Generator
  Generator --> Domain
  Mapper --> Domain

  SourcePort --> FileLoader
  SourcePort --> UrlLoader
  ValidatorPort --> Validator
  InvokerPort --> HttpxInvoker
  HttpxInvoker --> RemoteApi

  note1[Dependencies point inward to Core]:::note
  note2[External systems isolated by ports/adapters]:::note

  classDef note fill:#f5f5f5,stroke:#666,stroke-width:1px,color:#222;
```
