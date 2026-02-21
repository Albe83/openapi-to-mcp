# Compliance and Definition of Done

Policy Owner: Engineering Maintainers

## Definition of Done (Code Changes)
A feature/bugfix change is done only when all are true:
- Parent issue, plan comment, and required sub-issues exist.
- ADR is referenced.
- Class/sequence Mermaid files exist in [docs/diagrams/](../diagrams) and are linked.
- ADR links required class/sequence diagram files.
- If data model changed: JSON Schema exists in [docs/schemas/](../schemas) and is linked.
- If public API changed: formal IDL exists in [docs/interfaces/](../interfaces) and is linked.
- If data model/schema changed: DDD assessment exists per `08`.
- If DDD is applicable: UL/BC/Aggregates are documented and referenced.
- If boundaries/integrations changed: Hexagonal assessment exists per `12`.
- If Hexagonal is applicable: ADR mapping and dedicated diagram are referenced.
- New or updated ADR/docs/comments use simple English.
- PR includes test and lint evidence per [04-testing-tdd.md](04-testing-tdd.md).
- If no linter exists for a changed artifact type, PR includes `N/A` with reason.
- Task decomposition/labels comply with `02`; branch guard complies with `05`.
- Mandatory review is completed before merge.
- Review and finding issue labels comply with [10-review-and-findings.md](10-review-and-findings.md).
- Relevant tests pass.
- PR is squash-merged to `main`.

## Non-Compliant Examples
- Merge without mandatory review.
- Review/findings process not compliant with [10-review-and-findings.md](10-review-and-findings.md).
- Data model change without schema update.
- Public API change without IDL update.
- Boundary/integration change without Hexagonal assessment/artifacts per `12`.
- Missing test/lint evidence required by [04-testing-tdd.md](04-testing-tdd.md).
- Task decomposition/labels not compliant with `02` or branch guard not compliant with `05`.
- Finding issue labels not compliant with [10-review-and-findings.md](10-review-and-findings.md).
- PR missing links to required architecture artifacts.
- New or updated ADR/docs/comments not in simple English.

## Escalation
If any mandatory artifact is missing, stop implementation and restore compliance before proceeding.
