# Class Diagram: OTLP Telemetry and RED/USE Metrics

- Parent issue: #TBD
- ADR: [docs/adr/0004-otlp-telemetry-red-use-and-metrics-deprecation.md](../adr/0004-otlp-telemetry-red-use-and-metrics-deprecation.md)
- Purpose: Show telemetry components and RED/USE instrumentation with OTLP-only export.

```mermaid
classDiagram
  class FastAPIApp {
    +GET /healthz
    +POST /mcp
    +http_red_metrics_middleware()
  }

  class RuntimeMetrics {
    +on_http_request_completed(route, method, status, duration)
    +on_invocation_started(wait)
    +on_invocation_error()
    +on_invocation_finished()
    +shutdown()
  }

  class TelemetryRuntime {
    +provider: MeterProvider
    +meter: Meter
  }

  class OtlpMetricExporter {
    +export()
  }

  class Collector {
    +ingest OTLP
  }

  class HttpxInvokerAdapter {
    +invoke(binding, payload)
  }

  FastAPIApp --> RuntimeMetrics : records RED
  HttpxInvokerAdapter --> RuntimeMetrics : records USE metrics
  RuntimeMetrics --> TelemetryRuntime : creates OTel instruments
  TelemetryRuntime --> OtlpMetricExporter : periodic export
  OtlpMetricExporter --> Collector : OTLP/gRPC or OTLP/HTTP
```
