# Compliance and Definition of Done

Policy Owner: Engineering Maintainers

## Definition of Done (Code Changes)
A feature/bugfix change is done only when all are true:
- Parent issue, plan comment, and required sub-issues exist.
- ADR and required diagrams are linked.
- If data model changed: JSON Schema exists in [docs/schemas/](../schemas).
- If public API changed: formal IDL exists in [docs/interfaces/](../interfaces).
- If data model/schema changed: DDD assessment exists per `08`, and applicable UL/BC/Aggregates are documented.
- If boundaries/integrations changed: Hexagonal assessment exists per `12`, and applicable mapping/diagram are linked.
- If container install/run workflows changed: compliance with `13`/`14`/`15` is evidenced.
- If application logging behavior changed: compliance with `17` is evidenced.
- If Command/Reply M2M protocol changed: compliance with `18` is evidenced.
- If Event-Driven/PubSub contracts changed: compliance with `19` is evidenced.
- New or updated ADR/docs/comments use simple English (`09`).
- PR includes TDD/test/lint evidence per [04-testing-tdd.md](04-testing-tdd.md), with `N/A` rationale when needed.
- Task decomposition/labels and branch guard comply with `02` and `05`.
- Mandatory review is completed; finding labels/priorities comply with [10-review-and-findings.md](10-review-and-findings.md).
- Relevant tests pass.
- PR is squash-merged to `main`.

## Non-Compliant Examples
- Merge without mandatory review.
- Missing required schema/IDL/architecture artifacts.
- Missing conditional compliance evidence for `12`, `13`/`14`/`15`, `17`, `18`, or `19`.
- Missing TDD/test/lint evidence required by [04-testing-tdd.md](04-testing-tdd.md).
- Task/finding labels or priorities not compliant with `02` or [10-review-and-findings.md](10-review-and-findings.md).
- New or updated ADR/docs/comments not in simple English.

## Escalation
If any mandatory artifact is missing, stop implementation and restore compliance before proceeding.
