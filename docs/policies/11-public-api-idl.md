# Public API IDL Policy

Policy Owner: Engineering Maintainers

Public API definition is an architectural responsibility.
When a public API changes, the contract must be formally defined in an Interface Definition Language (IDL).

## Applicability Trigger
Apply this policy when:
- a new public API is introduced,
- an existing public API contract changes,
- API behavior changes require contract updates.

## IDL Standard
- Default for HTTP REST: OpenAPI specification.
- Use protocol-specific IDL when needed (for example AsyncAPI, GraphQL schema, Protobuf).

## Location and Format
- Store API contracts in `docs/interfaces/`.
- Prefer YAML when the IDL supports it.
- JSON is allowed when tooling or integration requires it.

## PR Traceability
If public API changes, PR must include:
- API change declaration,
- IDL type used,
- link to updated IDL file in `docs/interfaces/`.

## Non-Compliant
- Public API change without formal IDL update.
- PR missing IDL link for API change.
- Contract change implemented in code but not reflected in IDL.
