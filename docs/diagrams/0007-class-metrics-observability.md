# Class Diagram: Metrics Observability Components

- Parent issue: [#22](https://github.com/Albe83/openapi-to-mcp/issues/22)
- ADR: [docs/adr/0003-metrics-endpoint-opentelemetry-use-alignment.md](../adr/0003-metrics-endpoint-opentelemetry-use-alignment.md)
- Purpose: Show runtime components used to collect and expose metrics.

```mermaid
classDiagram
  class FastAPIApp {
    +GET /healthz
    +GET /metrics
    +POST /mcp
  }

  class MetricsRegistry {
    +render_openmetrics() bytes
    +on_invocation_started()
    +on_invocation_finished()
    +on_invocation_error()
  }

  class HttpxInvokerAdapter {
    +invoke(binding, payload) Dict
  }

  class HttpxAsyncClient {
    +request(method, url, ...)
  }

  FastAPIApp --> MetricsRegistry : reads /metrics payload
  HttpxInvokerAdapter --> MetricsRegistry : records usage/saturation/errors
  HttpxInvokerAdapter --> HttpxAsyncClient : executes outbound REST calls
```
