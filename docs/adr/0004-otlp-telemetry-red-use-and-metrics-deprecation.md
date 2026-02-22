# ADR 0004: OTLP Telemetry with RED and USE Metrics (Remove `/metrics`)

- Status: Accepted
- Date: 2026-02-22
- Parent issue: #TBD
- Related sub-issues: #TBD

## Context
Policy `22` requires OpenTelemetry SDK instrumentation and OTLP export to a platform Collector.
Policy `23` requires clear metric semantics, USE coverage for bounded resources, and RED metrics for request-driven interfaces.

The runtime previously exposed `GET /metrics` as an OpenMetrics compatibility endpoint.
That compatibility path created duplicate telemetry behavior and extra maintenance cost.

## Decision
Adopt OpenTelemetry as the primary telemetry implementation:
- configure a local MeterProvider with OTLP exporter;
- export metrics to Collector with OTLP/gRPC by default and OTLP/HTTP as fallback;
- attach mandatory resource attributes:
  - `service.name`,
  - `service.namespace`,
  - `service.version`,
  - `deployment.environment`.

Implement RED for inbound HTTP request-driven interfaces:
- request rate counter,
- error counter (5xx),
- duration histogram with explicit bucket boundaries.

Implement USE for outbound HTTP bounded resources:
- usage: in-flight outbound requests;
- saturation: queue wait histogram, configured max in-flight, configured max connections, utilization ratio;
- errors: outbound invocation error counter.

Remove `GET /metrics` and remove OpenMetrics/Prometheus compatibility code.
Telemetry is exported only through OTLP to the Collector.

### RED Duration Bucket Limits
For `openapi_to_mcp.http_server.duration`, boundaries are:
`[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]` seconds.

### Metric Catalog (Name / Unit / Intent)
- `openapi_to_mcp.http_server.requests` / `requests` / RED rate.
- `openapi_to_mcp.http_server.errors` / `errors` / RED errors.
- `openapi_to_mcp.http_server.duration` / `seconds` / RED duration histogram.
- `openapi_to_mcp.http_invoker.requests` / `requests` / USE usage flow.
- `openapi_to_mcp.http_invoker.errors` / `errors` / USE errors.
- `openapi_to_mcp.http_invoker.in_flight` / `requests` / USE usage.
- `openapi_to_mcp.http_invoker.queue_wait` / `seconds` / USE saturation signal.
- `openapi_to_mcp.http_invoker.max_in_flight` / `requests` / USE saturation capacity.
- `openapi_to_mcp.http_connection_pool.max_connections` / `connections` / USE saturation capacity.
- `openapi_to_mcp.http_invoker.utilization` / `ratio` / USE saturation ratio.

## DDD and Hexagonal Assessment
- DDD: not applicable for domain model changes; no entity/value changes.
- Hexagonal: applicable only to infrastructure observability adapter behavior; domain/application boundaries remain stable.

## Alternatives Considered
1. Keep Prometheus-only instrumentation.
   - Rejected: does not satisfy OTLP export policy.
2. Keep deprecated `GET /metrics` in parallel.
   - Rejected: keeps duplicate telemetry paths and extra complexity.
3. Delay cleanup with ADR exception.
   - Rejected: policy alignment is required now.

## Consequences and Tradeoffs
- Positive: transport and metric design align with policy `22` and `23`.
- Positive: RED and USE become explicit and testable.
- Positive: runtime is simpler with one telemetry path.
- Negative: users that still scrape `/metrics` must migrate to Collector-based telemetry access.

## Required Artifact Links
- Class diagram: [docs/diagrams/0009-class-telemetry-otlp-red-use.md](../diagrams/0009-class-telemetry-otlp-red-use.md)
- Sequence diagram: [docs/diagrams/0010-sequence-http-request-red-and-otlp-export.md](../diagrams/0010-sequence-http-request-red-and-otlp-export.md)
- Public API IDL: [docs/interfaces/0001-openapi-to-mcp-server-openapi.yaml](../interfaces/0001-openapi-to-mcp-server-openapi.yaml)
