# Class Diagram: Optional Prometheus Compatibility Telemetry

Purpose: Describe runtime components and dependencies for OTLP default telemetry plus optional Prometheus-compatible exposition.
Parent issue: #59
ADR reference: [docs/adr/0005-optional-prometheus-compatibility-toggle.md](../adr/0005-optional-prometheus-compatibility-toggle.md)

```mermaid
classDiagram
    class Settings {
        +bool prometheus_metrics_enabled
        +str telemetry_otlp_protocol
        +str telemetry_otlp_endpoint
    }

    class RuntimeMetrics {
        -MeterProvider _meter_provider
        -bool _prometheus_enabled
        +on_http_request_completed(route, method, status_code, duration)
        +render_prometheus_payload() bytes
        +prometheus_content_type() str
        +shutdown() None
    }

    class TelemetryRuntime {
        +MeterProvider provider
        +Meter meter
    }

    class TelemetryBuilder {
        +build_telemetry_runtime(..., enable_prometheus) TelemetryRuntime
    }

    class FastAPIApp {
        +GET /healthz
        +GET /metrics (conditional)
        +POST /mcp
    }

    Settings --> RuntimeMetrics : configures
    RuntimeMetrics --> TelemetryBuilder : calls
    TelemetryBuilder --> TelemetryRuntime : creates
    FastAPIApp --> RuntimeMetrics : uses for RED/USE + scrape
```
