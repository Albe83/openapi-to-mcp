# Lifecycle Policy

Policy Owner: Engineering Maintainers

For feature and bugfix code changes, use this mandatory sequence:
1. Open a parent issue with formal functional analysis.
2. Add an operational plan comment in that issue.
3. Create one sub-issue per technical task, with complexity label.
4. Produce architecture artifacts (ADR in [docs/adr/](../adr) + diagrams in [docs/diagrams/](../diagrams)).
5. Create a short-lived branch from `main`.
6. Implement tasks and open a PR to `main`.
7. Complete mandatory review and register findings.
8. Merge after review and required checks.

## Parent Issue Minimum Content
- Problem or need
- Functional goals and expected outcome
- Scope and out-of-scope
- Constraints, dependencies, risks
- Acceptance criteria

Use [.github/ISSUE_TEMPLATE/feature-or-bug-analysis.yml](../../.github/ISSUE_TEMPLATE/feature-or-bug-analysis.yml).

## Operational Plan and Sub-Issues
The parent issue plan comment must include task order, dependencies, validation approach, and rollout notes when needed.
Decompose work into the smallest independent tasks that are executable by a junior developer.
For each planned task, assign complexity target: `basic` (junior executable) or `advanced` (not reasonably decomposable).
Create one sub-issue per task using [.github/ISSUE_TEMPLATE/sub-task.yml](../../.github/ISSUE_TEMPLATE/sub-task.yml).
Each task/finding sub-issue must have label `task` plus exactly one label: `basic` or `advanced`.
If a sub-issue is `advanced`, document why further decomposition is not feasible or not appropriate.
After implementation review, create one sub-issue per finding per [10-review-and-findings.md](10-review-and-findings.md), using [.github/ISSUE_TEMPLATE/finding.yml](../../.github/ISSUE_TEMPLATE/finding.yml).

## Non-Compliant
- Coding before parent issue + plan + sub-issues.
- Task decomposition that keeps avoidable high-complexity work.
- PR without links to parent and sub-issues.
- Sub-issue missing `basic`/`advanced` label classification.
- `advanced` sub-issue without decomposition rationale.
- Review findings without dedicated sub-issues.
- Finding sub-issue labels not compliant with [10-review-and-findings.md](10-review-and-findings.md).
