# Sequence Diagram: Invocation and Metrics Scrape Flow

- Parent issue: [#22](https://github.com/Albe83/openapi-to-mcp/issues/22)
- ADR: [docs/adr/0003-metrics-endpoint-opentelemetry-use-alignment.md](../adr/0003-metrics-endpoint-opentelemetry-use-alignment.md)
- Purpose: Describe metric recording during invocation and exposure through `/metrics`.

```mermaid
sequenceDiagram
  autonumber
  participant Agent as MCP Client
  participant App as FastAPI App
  participant Adapter as HttpxInvokerAdapter
  participant Downstream as REST API
  participant Metrics as MetricsRegistry

  Agent->>App: POST /mcp
  App->>Adapter: invoke(binding, payload)
  Adapter->>Metrics: on_invocation_started()
  Adapter->>Downstream: HTTP request
  Downstream-->>Adapter: HTTP response / error
  alt success
    Adapter->>Metrics: on_invocation_finished()
  else error
    Adapter->>Metrics: on_invocation_error()
    Adapter->>Metrics: on_invocation_finished()
  end
  Adapter-->>App: invocation result
  App-->>Agent: MCP response

  Agent->>App: GET /metrics
  App->>Metrics: render_openmetrics()
  Metrics-->>App: OpenMetrics payload
  App-->>Agent: 200 text/plain; version=0.0.4
```
