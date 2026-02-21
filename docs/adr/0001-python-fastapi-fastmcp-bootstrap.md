# ADR 0001: Python FastAPI and FastMCP Bootstrap

- Status: Accepted
- Date: 2026-02-21
- Parent issue: [#1](https://github.com/Albe83/openapi-to-mcp/issues/1)
- Related sub-issues: [#2](https://github.com/Albe83/openapi-to-mcp/issues/2), [#3](https://github.com/Albe83/openapi-to-mcp/issues/3), [#4](https://github.com/Albe83/openapi-to-mcp/issues/4), [#5](https://github.com/Albe83/openapi-to-mcp/issues/5), [#6](https://github.com/Albe83/openapi-to-mcp/issues/6), [#7](https://github.com/Albe83/openapi-to-mcp/issues/7), [#8](https://github.com/Albe83/openapi-to-mcp/issues/8), [#9](https://github.com/Albe83/openapi-to-mcp/issues/9), [#10](https://github.com/Albe83/openapi-to-mcp/issues/10), [#11](https://github.com/Albe83/openapi-to-mcp/issues/11)

## Context
The repository has governance and documentation, but no runnable application code.
The first increment must provide a real technical foundation that can load an OpenAPI contract and expose mapped tools through MCP over HTTP streamable transport.

## Decision
Use Python with FastAPI and FastMCP.
Adopt a Hexagonal Architecture shape with explicit ports and adapters:
- Inbound: FastAPI/FastMCP transport adapter.
- Application services: startup orchestration, operation mapping, tool generation.
- Outbound: OpenAPI source loaders and downstream HTTP invoker.

Configuration is environment driven:
- `OPENAPI_SPEC_PATH`
- `OPENAPI_SPEC_URL`
- `MCP_HOST`
- `MCP_PORT`
- `LOG_LEVEL`

Tool naming rule:
- First choice: `operationId`.
- Fallback: deterministic `<method>_<sanitized_path>`.

Validation rule:
- Fail fast for critical OpenAPI contract errors.
- Keep warning-only behavior for non-critical metadata quality issues.

Server resolution rule:
- Resolve server URL in this order: operation -> path -> root.
- If no server URL is resolvable for an operation, fail startup.

## DDD Assessment
DDD is applicable because this increment introduces domain models for operations and generated tools.

### Ubiquitous Language
- Operation: one executable REST API action from OpenAPI.
- Generated Tool: MCP tool produced from one Operation.
- Port: interface that isolates domain/application from frameworks or IO.
- Adapter: concrete implementation of a Port.

### Bounded Context
- Context name: `Tool Generation Context`.
- Boundary: from OpenAPI contract ingestion to MCP tool registration and invocation wiring.

### Aggregates and Invariants
- Aggregate root: `ApiOperation`.
  - Invariant: method and path must be present.
- Aggregate root: `GeneratedTool`.
  - Invariant: tool name must be deterministic and not empty.
- Aggregate root: `GenerationReport`.
  - Invariant: generated + skipped equals total input operations processed.

## Alternatives Considered
1. Go + custom MCP integration.
   - Rejected for first increment due slower bootstrap.
2. Python without Hexagonal boundaries.
   - Rejected due coupling risk and weaker testability.
3. Best-effort validation only.
   - Rejected because startup should fail on invalid critical contracts.

## Consequences and Tradeoffs
- Positive: clear testable boundaries, faster bootstrap, policy compliance.
- Negative: more files and abstractions in first increment.
- Risk: FastMCP API evolution can break integration; mitigated by transport adapter isolation.

## Required Artifact Links
- Class diagram: [docs/diagrams/0002-class-bootstrap-core.md](../diagrams/0002-class-bootstrap-core.md)
- Sequence diagram: [docs/diagrams/0003-sequence-startup-and-tool-call.md](../diagrams/0003-sequence-startup-and-tool-call.md)
- Hexagonal diagram: [docs/diagrams/0004-hexagonal-bootstrap-boundaries.md](../diagrams/0004-hexagonal-bootstrap-boundaries.md)
- Public API IDL: [docs/interfaces/0001-openapi-to-mcp-server-openapi.yaml](../interfaces/0001-openapi-to-mcp-server-openapi.yaml)
- Domain schema: [docs/schemas/0001-core-domain-models.schema.yaml](../schemas/0001-core-domain-models.schema.yaml)
