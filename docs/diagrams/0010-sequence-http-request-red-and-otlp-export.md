# Sequence Diagram: HTTP RED Collection and OTLP Export

- Parent issue: #TBD
- ADR: [docs/adr/0004-otlp-telemetry-red-use-and-metrics-deprecation.md](../adr/0004-otlp-telemetry-red-use-and-metrics-deprecation.md)
- Purpose: Describe request instrumentation, outbound USE updates, and periodic OTLP export.

```mermaid
sequenceDiagram
  autonumber
  participant Client as MCP Client
  participant App as FastAPI App
  participant MW as RED Middleware
  participant Invoker as HttpxInvokerAdapter
  participant Metrics as RuntimeMetrics
  participant OTel as MeterProvider
  participant Collector as OTel Collector

  Client->>App: POST /mcp
  App->>MW: process request
  MW->>Invoker: invoke downstream REST call
  Invoker->>Metrics: on_invocation_started(wait)
  Invoker-->>Metrics: on_invocation_finished()/on_invocation_error()
  MW->>Metrics: on_http_request_completed(route, method, status, duration)
  App-->>Client: MCP response

  loop periodic export interval
    OTel->>Collector: export OTLP metrics
  end
```
