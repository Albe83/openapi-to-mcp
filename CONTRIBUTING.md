# Contributing (Entry Point)

This file is the onboarding entry point.
The normative source of truth is [docs/policies/](docs/policies).
Meta-governance is in [docs/policies/00-policy-of-policies.md](docs/policies/00-policy-of-policies.md).
If this file conflicts with a policy module, the policy module wins.

## Start Here
1. Open [docs/policies/01-index.md](docs/policies/01-index.md).
2. Load only the modules needed for your task.
3. For `feat`/`fix`, follow the "Feature/Bugfix core path" in the index. Baseline modules are mandatory.
4. Check each trigger in the index. If a trigger applies, that conditional module is normative and mandatory for the task.
5. For ADR/docs/comments/code comments, apply [docs/policies/09-language-simple-english.md](docs/policies/09-language-simple-english.md).

## Workflow Snapshot (Non-Normative)
Use this as onboarding only:
1. Open parent analysis issue and add the operational plan comment.
2. Create one sub-issue per task from the plan.
3. Implement and validate (tests/lint).
4. Open PR to `main`.
5. Complete mandatory review and track each finding with one sub-issue.

## Required Templates
- Parent issue: [.github/ISSUE_TEMPLATE/feature-or-bug-analysis.yml](.github/ISSUE_TEMPLATE/feature-or-bug-analysis.yml)
- Sub-task issue: [.github/ISSUE_TEMPLATE/sub-task.yml](.github/ISSUE_TEMPLATE/sub-task.yml)
- Pull request: [.github/pull_request_template.md](.github/pull_request_template.md)

## Useful Links
- Policy set: [docs/policies/](docs/policies)
- Governance mindmap: [docs/diagrams/0001-governance-mindmap.md](docs/diagrams/0001-governance-mindmap.md)
- ADRs: [docs/adr/](docs/adr)
- Diagrams: [docs/diagrams/](docs/diagrams)

## Governance Quality Gate
Run before opening PR:
- `make governance-check`

## CI Checks
PRs to `main` are expected to pass governance, CI, and security workflows.
Release workflow runs on SemVer tags only.
