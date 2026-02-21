# Data Model Schema Guidelines

This directory stores technical schema formalization for data models.

## Scope
When a feature/bugfix changes the data model, JSON Schema artifacts are required.
These artifacts complement architecture ADRs and Class Diagrams.

## Format Rule
- Preferred format: YAML (`.yaml` / `.yml`) for human readability.
- Allowed fallback: JSON (`.json`) when tooling or integration requires it.
- Schemas must remain valid JSON Schema semantics regardless of file format.

## Naming
Use:
- `NNNN-<domain>-schema.yaml` (preferred)
- `NNNN-<domain>-schema.json` (fallback)

Keep numbering aligned with related ADR when possible.

## Minimum Metadata
Each schema file (or adjacent markdown wrapper) should include:
- Parent issue reference.
- Related ADR reference.
- Short purpose statement.

## Process
1. Update schema when data model changes.
2. Keep schema aligned with Class Diagram entities and relationships.
3. Link schema location in sub-issues and PR.
4. If schema format is JSON, document why YAML was not used.
