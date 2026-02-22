# Compliance and Definition of Done

Policy Owner: Engineering Maintainers

## Definition of Done (Code Changes)
A feature/bugfix change is done only when all are true:
- Parent issue, plan comment, and required sub-issues exist.
- ADR and required diagrams are linked.
- If data model changed: JSON Schema exists in [docs/schemas/](../schemas).
- If public API changed: formal IDL exists in [docs/interfaces/](../interfaces).
- PR includes a compliance map for owner modules with fields:
  - module id,
  - applies (`yes`/`no`),
  - evidence link or command result,
  - `N/A` reason when not applicable.
- Baseline modules always listed in the map: `02`, `03`, `04`, `05`, `07`, `10`.
- Conditional modules listed when triggered: `08`, `09`, `11`, `12`, `13`, `14`, `15`, `17`, `18`, `19`, `20`, `21`, `22`, `23`.
- Relevant validation commands pass.
- PR is squash-merged to `main`.

## Evidence Acceptance
- Evidence must point to concrete artifacts (issue/comment permalink, ADR/diagram/schema/IDL path, PR section, command output, or workflow log).
- Checklist ticks without links or results are not sufficient.
- Command evidence must include executed command and pass/fail status.

## Non-Compliant Examples
- Merge without mandatory review.
- Missing required schema/IDL/architecture artifacts.
- Missing compliance-map row for an applicable owner module.
- Compliance-map row without evidence link/result and without valid `N/A` reason.
- Missing TDD/test/lint evidence required by [04-testing-tdd.md](04-testing-tdd.md).

## Escalation
If any mandatory artifact is missing, stop implementation and restore compliance before proceeding.
