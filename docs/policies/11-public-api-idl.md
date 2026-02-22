# Public API IDL Policy

Policy Owner: Engineering Maintainers

Public API definition is an architectural responsibility.
When a public API changes, the contract must be formally defined in an Interface Definition Language (IDL).

## Public API Boundary
Public API means an interface intentionally exposed to consumers outside the service process.

Included:
- external HTTP endpoints,
- externally consumed RPC/event contracts,
- documented external automation interfaces (for example CLI contract) when explicitly declared public.

Excluded:
- internal-only endpoints and debug/admin routes not exposed externally,
- internal callbacks and in-process interfaces,
- environment variables and internal implementation details.

## Applicability Trigger
Apply this policy when:
- a new public API is introduced,
- an existing public API contract changes,
- externally observable behavior changes require contract updates.

Behavior-change triggers include:
- request/response/event schema changes,
- required/optional field changes,
- enum/default/validation rule changes,
- status code or error-shape changes,
- authentication or parameter semantics changes.

## IDL Standard
- Default for HTTP REST: OpenAPI specification.
- Use protocol-specific IDL when needed (for example AsyncAPI, GraphQL schema, Protobuf).

## Location and Format
- Store API contracts in [docs/interfaces/](../interfaces).
- Prefer YAML when the IDL supports it.
- JSON is allowed when tooling or integration requires it.

## PR Traceability
If public API changes, PR must include:
- API change declaration (`yes`/`no`),
- IDL type used,
- link to updated IDL file in [docs/interfaces/](../interfaces).
- If `no`, provide `N/A - public API not affected: <reason>`.

## Non-Compliant
- Public API change without formal IDL update.
- PR missing IDL link for API change.
- Contract change implemented in code but not reflected in IDL.
