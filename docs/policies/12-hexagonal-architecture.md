# Hexagonal Architecture Policy

Policy Owner: Engineering Maintainers

Apply Hexagonal Architecture principles where useful and appropriate.
For `feat`/`fix` code changes, Hexagonal assessment is mandatory when architectural boundaries are touched.

## Applicability Trigger
Assessment is required if change scope includes:
- new or changed inbound/outbound integrations,
- new or changed ports/adapters,
- dependency direction changes across domain, application, and infrastructure layers.

## Required Outcomes (When Applicable)
- Define inbound and outbound ports.
- Map adapters to each port.
- Keep dependencies pointing inward to the domain/application core.
- Document anti-corruption boundaries for external systems when relevant.

## Required Artifacts
- ADR section with port/adapter mapping and dependency direction.
- Dedicated Markdown Mermaid diagram in `docs/diagrams/` for Hexagonal structure.
- PR links to ADR section and diagram file.

## Not Applicable Path
If Hexagonal is assessed as not applicable, PR must include:
`N/A - Hexagonal not applicable: <reason>`.

## Non-Compliant
- No Hexagonal assessment for `feat`/`fix` boundary changes.
- Hexagonal applicable but missing ADR mapping or diagram.
- PR missing required links or missing `N/A` rationale.
