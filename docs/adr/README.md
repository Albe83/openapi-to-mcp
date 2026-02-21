# ADR Guidelines

This directory stores Architecture Decision Records (ADRs) required before implementation of feature/bugfix code changes.

## Naming
- File format: `NNNN-short-title.md` (for example, `0001-tool-generation-strategy.md`).
- Use incremental numbering.

## Minimum ADR Content
1. Title and status (`Proposed`, `Accepted`, `Superseded`).
2. Context and problem statement.
3. Decision.
4. Alternatives considered.
5. Consequences and tradeoffs.
6. Links to parent issue and related sub-issues.
7. Links to Class and Sequence diagram files in [docs/diagrams/](../diagrams).
8. If data model changes: links to schema files in [docs/schemas/](../schemas).

## Process
1. Create/update ADR(s) before implementation.
2. Reference ADR(s) in sub-issues and PR.
3. If data model changes, update JSON Schema artifacts (YAML preferred) in [docs/schemas/](../schemas).
4. Update status when decision is accepted or superseded.
