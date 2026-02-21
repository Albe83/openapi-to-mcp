# Domain-Driven Design Policy

Policy Owner: Engineering Maintainers

Apply Domain-Driven Design practices where useful and appropriate.
In this repository, DDD assessment is mandatory when a feature/bugfix changes data model/schema.

## Applicability Trigger
DDD assessment is required if change scope includes:
- new or changed domain entities/value objects,
- schema changes in [docs/schemas/](../schemas),
- non-trivial domain invariants or lifecycle rules.

## Required DDD Artifacts
When DDD is applicable, provide:
- Ubiquitous Language terms (core domain vocabulary),
- Bounded Context definition (scope and boundaries),
- Aggregate boundaries and invariants.

## Documentation Location
Preferred: dedicated sections in ADR markdown.
Allowed support: references to [docs/schemas/](../schemas) and Class Diagram artifacts.

## PR Traceability
If data model/schema changes, PR must include:
- DDD applicability assessment,
- links to ADR section(s) with UL/BC/Aggregates,
- rationale when DDD is assessed as not applicable.

## Non-Compliant
- Model/schema change without DDD assessment.
- DDD applicable but missing UL/BC/Aggregates.
- PR missing links or rationale for DDD decision.
