# ADR 0005: Optional Prometheus Compatibility Metrics Endpoint

- Status: Accepted
- Date: 2026-02-23
- Parent issue: #59
- Related sub-issues: #60, #61, #62, #63, #64, #65, #66

## Context
Policy `22` requires OpenTelemetry instrumentation and OTLP export as the default telemetry transport.
Policy `23` requires stable USE and RED semantics for metrics.

ADR 0004 removed `/metrics` to simplify runtime telemetry to a single OTLP path.
A compatibility need now exists for environments that still rely on Prometheus scrape workflows.

The required behavior is:
- Prometheus compatibility available when explicitly enabled.
- Disabled by default.
- No behavior change for current default runtime.

## Decision
Introduce an optional Prometheus-compatible metrics feature toggle.

### Toggle
- New runtime setting: `PROMETHEUS_METRICS_ENABLED`.
- Default: `false`.
- When `false`, `GET /metrics` is not mounted and returns `404`.
- When `true`, `GET /metrics` returns Prometheus-compatible exposition.

### Telemetry Architecture
- Keep OpenTelemetry SDK instrumentation as the single metrics instrumentation source.
- Keep OTLP export to Collector enabled as default path.
- Add Prometheus-compatible reader/exposition only when toggle is enabled.
- Do not change existing metric names, units, RED/USE model, or histogram boundaries.

## DDD and Hexagonal Assessment
- DDD: not applicable. No domain model changes.
- Hexagonal: applicable only at infrastructure observability adapter level; domain and application boundaries are unchanged.

## Alternatives Considered
1. Keep OTLP-only and reject Prometheus compatibility.
   - Rejected: does not meet compatibility need.
2. Reintroduce `/metrics` always enabled.
   - Rejected: changes default behavior and increases operational surface for all environments.
3. Introduce separate metrics sidecar/service.
   - Rejected: adds deployment complexity for this scope.

## Consequences
- Positive: preserves current OTLP-first architecture.
- Positive: supports Prometheus scraping where needed.
- Positive: default behavior remains unchanged.
- Negative: optional path increases observability runtime complexity.
- Mitigation: strict toggle default off and explicit tests for both modes.

## Required Artifact Links
- Class diagram: [docs/diagrams/0011-class-optional-prometheus-telemetry.md](../diagrams/0011-class-optional-prometheus-telemetry.md)
- Sequence diagram: [docs/diagrams/0012-sequence-conditional-metrics-scrape.md](../diagrams/0012-sequence-conditional-metrics-scrape.md)
- Public API IDL: [docs/interfaces/0001-openapi-to-mcp-server-openapi.yaml](../interfaces/0001-openapi-to-mcp-server-openapi.yaml)
- Previous decision reference: [docs/adr/0004-otlp-telemetry-red-use-and-metrics-deprecation.md](0004-otlp-telemetry-red-use-and-metrics-deprecation.md)
