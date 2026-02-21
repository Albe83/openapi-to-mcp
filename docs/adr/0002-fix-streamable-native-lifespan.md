# ADR 0002: Fix Native Streamable MCP Lifespan and Path Wiring

- Status: Accepted
- Date: 2026-02-21
- Parent issue: [#19](https://github.com/Albe83/openapi-to-mcp/issues/19)
- Related sub-issues: [#20](https://github.com/Albe83/openapi-to-mcp/issues/20), [#18](https://github.com/Albe83/openapi-to-mcp/issues/18)

## Context
In native FastMCP mode, streamable requests fail with HTTP 500 and runtime error:
`Task group is not initialized. Make sure to use run().`

Previous transport wiring mounted FastMCP streamable app under `/mcp` while using a root route in the sub-app.
This created trailing-slash redirect behavior (`/mcp` -> `/mcp/`) and did not guarantee native session manager lifecycle activation inside the parent FastAPI app lifecycle.

## Decision
Use explicit native lifecycle management and canonicalize the public endpoint to `POST /mcp` (no trailing slash).

- Create native FastMCP runtime with `streamable_http_path="/mcp"`.
- Mount the resulting streamable app at root (`""`) in the parent FastAPI app.
- Reuse a single streamable app instance from the adapter.
- Expose adapter-native lifespan context and enter it inside FastAPI lifespan when native mode is enabled.

## DDD and Hexagonal Assessment
- DDD impact: not applicable for domain model changes (no entity/value object changes).
- Hexagonal impact: applicable for inbound transport adapter behavior only.
  - Core application/domain contracts remain unchanged.
  - Change is isolated in inbound transport wiring.

## Alternatives Considered
1. Force fallback mode only.
   - Rejected: removes native streamable target behavior.
2. Keep path as `/mcp` inside FastMCP and mount elsewhere.
   - Rejected: external contract should remain `POST /mcp`.
3. Do not add CI MCP dependency.
   - Rejected: regression would remain untested in pipeline.

## Consequences and Tradeoffs
- Positive: native streamable mode works without runtime 500 and keeps `/mcp` as direct canonical endpoint.
- Positive: CI can detect native streamable regressions.
- Negative: additional lifecycle wiring complexity in transport adapter.

## Required Artifact Links
- Class diagram: [docs/diagrams/0005-class-streamable-lifecycle-fix.md](../diagrams/0005-class-streamable-lifecycle-fix.md)
- Sequence diagram: [docs/diagrams/0006-sequence-streamable-request-lifecycle-fix.md](../diagrams/0006-sequence-streamable-request-lifecycle-fix.md)
