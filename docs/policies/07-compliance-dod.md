# Compliance and Definition of Done

Policy Owner: Engineering Maintainers

## Definition of Done (Code Changes)
A feature/bugfix change is done only when all are true:
- Parent issue, plan comment, and required sub-issues exist.
- ADR is referenced.
- Class + Sequence diagrams exist as Markdown Mermaid files in `docs/diagrams/` and are referenced.
- ADR links required class/sequence diagram files.
- If data model changed: JSON Schema exists in `docs/schemas/` and is referenced.
- If public API changed: formal IDL exists in `docs/interfaces/` and is referenced.
- If data model/schema changed: DDD assessment exists per `08-domain-driven-design.md`.
- If DDD is applicable: UL/BC/Aggregates are documented and referenced.
- If boundaries/integrations/ports/adapters changed: Hexagonal assessment exists per `12-hexagonal-architecture.md`.
- If Hexagonal is applicable: ADR mapping and dedicated diagram are referenced.
- New or updated ADR/docs/comments use simple English.
- Test and lint evidence is present in PR per `04-testing-tdd.md`.
- If no linter exists for a changed artifact type, PR includes explicit `N/A` and reason.
- Task decomposition and labeling comply with `02-lifecycle.md`.
- Mandatory review is completed before merge.
- Review and findings management comply with `10-review-and-findings.md`.
- Relevant tests pass.
- PR is reviewed and merged to `main` with squash.

## Human and AI Parity
Humans and AI agents follow the same lifecycle and compliance requirements.

## Non-Compliant Examples
- Merge without mandatory review.
- Review/findings process not compliant with `10-review-and-findings.md`.
- Data model change without schema update.
- Public API change without IDL update.
- Boundary/integration change without Hexagonal assessment/artifacts per `12`.
- Missing test/lint evidence required by `04-testing-tdd.md`.
- Task decomposition/labels not compliant with `02-lifecycle.md`.
- PR missing links to required architecture artifacts.
- New or updated ADR/docs/comments not in simple English.

## Escalation
If any mandatory artifact is missing, stop implementation and restore compliance before proceeding.
