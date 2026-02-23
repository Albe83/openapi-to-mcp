# Sequence Diagram: Conditional Metrics Scrape Flow

Purpose: Show request behavior for `/metrics` when Prometheus compatibility is enabled or disabled.
Parent issue: #59
ADR reference: [docs/adr/0005-optional-prometheus-compatibility-toggle.md](../adr/0005-optional-prometheus-compatibility-toggle.md)

```mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant Settings
    participant RuntimeMetrics
    participant OTelProvider

    Note over FastAPI,Settings: Startup
    FastAPI->>Settings: read PROMETHEUS_METRICS_ENABLED
    FastAPI->>RuntimeMetrics: initialize(enable_prometheus)
    RuntimeMetrics->>OTelProvider: configure OTLP reader (always)
    alt enable_prometheus = true
        RuntimeMetrics->>OTelProvider: add Prometheus-compatible reader
        FastAPI->>FastAPI: register GET /metrics
    else enable_prometheus = false
        FastAPI->>FastAPI: do not register /metrics
    end

    Note over Client,FastAPI: Runtime scrape request
    Client->>FastAPI: GET /metrics
    alt endpoint enabled
        FastAPI->>RuntimeMetrics: render_prometheus_payload()
        RuntimeMetrics-->>FastAPI: metrics text + content type
        FastAPI-->>Client: 200 Prometheus-compatible payload
    else endpoint disabled
        FastAPI-->>Client: 404 Not Found
    end
```
