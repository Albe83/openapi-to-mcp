# ADR 0003: Metrics Endpoint and USE-Aligned Observability

- Status: Accepted
- Date: 2026-02-21
- Parent issue: [#22](https://github.com/Albe83/openapi-to-mcp/issues/22)
- Related sub-issues: [#23](https://github.com/Albe83/openapi-to-mcp/issues/23), [#24](https://github.com/Albe83/openapi-to-mcp/issues/24), [#25](https://github.com/Albe83/openapi-to-mcp/issues/25), [#26](https://github.com/Albe83/openapi-to-mcp/issues/26), [#27](https://github.com/Albe83/openapi-to-mcp/issues/27), [#28](https://github.com/Albe83/openapi-to-mcp/issues/28)

## Context
The repository policy requires a dedicated metrics endpoint, OpenMetrics output, and USE-oriented coverage for bounded resources.
Current runtime exposes `/healthz` and MCP endpoints but does not expose `/metrics`.

The runtime has one application-managed bounded resource for machine-to-machine calls:
- HTTP client connection and request concurrency limits.

Framework-managed resources exist (for example thread pools), but they are not directly controlled by application code in this increment.

## Decision
Introduce a dedicated `GET /metrics` endpoint in the FastAPI application.
Expose metrics as OpenMetrics text and keep metric names and attributes aligned with OpenTelemetry semantic conventions where applicable.

Add incremental instrumentation for outbound HTTP invocation:
- usage: active in-flight requests,
- saturation: configured capacity and queueing wait time before slot acquisition,
- errors: failed invocation count.

Represent connection-pool capacity through configured HTTP client limits.

## Resource Inventory and USE Mapping
1. HTTP request concurrency slots (application-managed)
- Usage: active in-flight requests.
- Saturation: queue wait duration and configured max concurrent requests.
- Errors: invocation error counter.

2. HTTP connection pool (application-managed via HTTPX limits)
- Usage: active request approximation.
- Saturation: max connection capacity metric.
- Errors: counted through invocation failures.

3. Thread pool (framework-managed)
- Constraint: no stable public runtime API for direct collection in this increment.
- Risk: partial USE visibility for framework internals.
- Mitigation: document gap and keep adapter-level telemetry for impacted paths.
- Convergence: add dedicated framework-runtime metrics if/when a stable source is introduced.

4. Queue/buffer capacity
- Constraint: no explicit application queue/buffer component in current design.
- Decision: no queue-specific metric is emitted in this increment.

## Hexagonal Assessment
Hexagonal assessment result: not applicable.
Reason: no new ports or adapters are introduced, and dependency direction remains unchanged.
This change adds observability instrumentation to existing transport/application wiring.

## Alternatives Considered
1. Keep no metrics endpoint.
- Rejected: violates policy requirements.

2. Expose metrics on separate side server.
- Rejected: unnecessary operational complexity for this increment.

3. Instrument every framework internal resource immediately.
- Rejected: high complexity and unstable internal APIs.

## Consequences and Tradeoffs
- Positive: policy-compliant endpoint and measurable runtime behavior.
- Positive: low-risk incremental refactor with testable output.
- Negative: thread-pool coverage remains partial pending stable integration source.

## Required Artifact Links
- Class diagram: [docs/diagrams/0007-class-metrics-observability.md](../diagrams/0007-class-metrics-observability.md)
- Sequence diagram: [docs/diagrams/0008-sequence-metrics-scrape-and-invocation.md](../diagrams/0008-sequence-metrics-scrape-and-invocation.md)
- Public API IDL: [docs/interfaces/0001-openapi-to-mcp-server-openapi.yaml](../interfaces/0001-openapi-to-mcp-server-openapi.yaml)
