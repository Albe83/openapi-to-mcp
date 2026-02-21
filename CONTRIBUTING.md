# Contributing (Entry Point)

This file is the onboarding entry point.
The normative policy source of truth is the policy set in [docs/policies/](docs/policies).
Meta-governance is defined in [docs/policies/00-policy-of-policies.md](docs/policies/00-policy-of-policies.md).

## Read This First
For feature and bugfix code changes, start from:
1. [docs/policies/01-index.md](docs/policies/01-index.md)
2. [docs/policies/02-lifecycle.md](docs/policies/02-lifecycle.md)
3. [docs/policies/03-architecture-first.md](docs/policies/03-architecture-first.md)
4. [docs/policies/04-testing-tdd.md](docs/policies/04-testing-tdd.md)
5. [docs/policies/05-git-and-pr.md](docs/policies/05-git-and-pr.md)
6. [docs/policies/10-review-and-findings.md](docs/policies/10-review-and-findings.md)
7. [docs/policies/07-compliance-dod.md](docs/policies/07-compliance-dod.md)

If model/schema changes, also read:
- [docs/policies/08-domain-driven-design.md](docs/policies/08-domain-driven-design.md)
- [docs/policies/11-public-api-idl.md](docs/policies/11-public-api-idl.md) (if public API changes)
- [docs/policies/12-hexagonal-architecture.md](docs/policies/12-hexagonal-architecture.md) (if boundaries/integrations/ports/adapters change)

For ADR/docs/comments/code comments, also read:
- [docs/policies/09-language-simple-english.md](docs/policies/09-language-simple-english.md)

For release work, also read:
- [docs/policies/06-versioning-release.md](docs/policies/06-versioning-release.md)

If container install/run workflows change, also read:
- [docs/policies/13-container-build-rules.md](docs/policies/13-container-build-rules.md)
- [docs/policies/14-container-run-mounts.md](docs/policies/14-container-run-mounts.md)
- [docs/policies/15-container-no-extra-env-isolation.md](docs/policies/15-container-no-extra-env-isolation.md)

## Workflow Snapshot (Non-Normative)
Use this as onboarding only. Exact requirements are owned by policy modules.
1. Open parent analysis issue and add the operational plan comment.
2. Create one sub-issue per task from the plan.
3. For `feat`/`fix`, publish architecture artifacts before implementation.
4. Implement, validate (tests/lint), and open PR to `main`.
5. Complete mandatory review and track each finding with one sub-issue.

## Required Templates
- Parent issue: [.github/ISSUE_TEMPLATE/feature-or-bug-analysis.yml](.github/ISSUE_TEMPLATE/feature-or-bug-analysis.yml)
- Sub-task issue: [.github/ISSUE_TEMPLATE/sub-task.yml](.github/ISSUE_TEMPLATE/sub-task.yml)
- Pull request: [.github/pull_request_template.md](.github/pull_request_template.md)

## Artifact Locations
- ADRs: [docs/adr/](docs/adr)
- Mermaid diagrams: [docs/diagrams/](docs/diagrams)
- Governance mindmap: [docs/diagrams/0001-governance-mindmap.md](docs/diagrams/0001-governance-mindmap.md)
- Policies: [docs/policies/](docs/policies)

## Governance Quality Gate
Run before opening PR:
- `make governance-check`

If this file conflicts with a module in [docs/policies/](docs/policies), the module wins.
