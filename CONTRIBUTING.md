# Contributing (Entry Point)

This file is the onboarding entry point.
The normative policy source of truth is the policy set in `docs/policies/`.
Meta-governance is defined in `docs/policies/00-policy-of-policies.md`.

## Read This First
For feature and bugfix code changes, start from:
1. `docs/policies/01-index.md`
2. `docs/policies/02-lifecycle.md`
3. `docs/policies/03-architecture-first.md`
4. `docs/policies/04-testing-tdd.md`
5. `docs/policies/05-git-and-pr.md`
6. `docs/policies/10-review-and-findings.md`
7. `docs/policies/07-compliance-dod.md`

If model/schema changes, also read:
- `docs/policies/08-domain-driven-design.md`
- `docs/policies/11-public-api-idl.md` (if public API changes)
- `docs/policies/12-hexagonal-architecture.md` (if boundaries/integrations/ports/adapters change)

For ADR/docs/comments/code comments, also read:
- `docs/policies/09-language-simple-english.md`

For release work, also read:
- `docs/policies/06-versioning-release.md`

## Mandatory Flow (Summary)
- Open a parent issue with formal functional analysis.
- Add an operational plan comment.
- Decompose into junior-executable tasks when possible.
- Create one sub-issue per task and classify it as `basic` or `advanced` (`task` label remains required).
- Before implementation, verify correct branch and ensure it is updated from base branch (`05-git-and-pr.md`).
- Publish architecture artifacts first (`docs/adr/` and `docs/diagrams/`).
- Keep architecture diagrams only in `docs/diagrams/`; ADRs must link them.
- For boundary/integration changes, assess Hexagonal architecture and add required artifacts or explicit `N/A` rationale.
- Implement with TDD for feature/bugfix code.
- Run lint for changed artifacts when available; otherwise document `N/A` with reason in PR.
- Open PR to `main` with links to issues, artifacts, and test evidence.
- Complete mandatory review and open one sub-issue per finding.
- Merge by squash only.

## Required Templates
- Parent issue: `.github/ISSUE_TEMPLATE/feature-or-bug-analysis.yml`
- Sub-task issue: `.github/ISSUE_TEMPLATE/sub-task.yml`
- Pull request: `.github/pull_request_template.md`

## Artifact Locations
- ADRs: `docs/adr/`
- Mermaid diagrams: `docs/diagrams/`
- Policies: `docs/policies/`

If this file conflicts with a module in `docs/policies/`, the module wins.
