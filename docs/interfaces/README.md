# Public API Interface Guidelines

This directory stores formal contracts for public APIs.

## Scope
When a public API changes, update an IDL contract here.

## Preferred Standards
- OpenAPI for HTTP REST APIs.
- Protocol-specific alternatives when appropriate (for example AsyncAPI, GraphQL schema, Protobuf).

## Format
- Prefer YAML for readability.
- JSON is allowed when required by tooling.

## Naming
Use:
- `NNNN-<api>-openapi.yaml` (preferred)
- `NNNN-<api>-openapi.json` (fallback)
- Equivalent naming for other IDL types.

## Minimum Metadata
Each IDL file (or adjacent markdown note) should include:
- parent issue reference,
- related ADR reference,
- short purpose statement,
- declared API change type.

## Process
1. Update IDL when public API changes.
2. Keep implementation and IDL aligned.
3. Link IDL location in sub-issues and PR.
4. If JSON is used, document why YAML was not used.
