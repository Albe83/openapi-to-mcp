# Repository Guidelines

This file is intentionally minimal to reduce AI context usage.
Detailed contribution rules are split into focused policy modules.

## Source of Truth
- Primary policy index: [docs/policies/01-index.md](docs/policies/01-index.md)
- Policy governance rules: [docs/policies/00-policy-of-policies.md](docs/policies/00-policy-of-policies.md)
- If any guidance conflicts, `docs/policies/*` takes precedence.

## AI Agent Operating Rule
Before planning or coding:
1. Open [docs/policies/01-index.md](docs/policies/01-index.md).
2. Load only the relevant policy module(s) for the current task.
3. Avoid loading unrelated policy files.

## Mandatory Modules for Feature/Bugfix
Load these owner modules in this order:
1. [docs/policies/02-lifecycle.md](docs/policies/02-lifecycle.md)
2. [docs/policies/03-architecture-first.md](docs/policies/03-architecture-first.md)
3. [docs/policies/04-testing-tdd.md](docs/policies/04-testing-tdd.md)
4. [docs/policies/05-git-and-pr.md](docs/policies/05-git-and-pr.md)
5. [docs/policies/10-review-and-findings.md](docs/policies/10-review-and-findings.md)
6. [docs/policies/07-compliance-dod.md](docs/policies/07-compliance-dod.md)

All normative details are owned by these modules.

## Conditional Modules
- If model/schema changes: [docs/policies/08-domain-driven-design.md](docs/policies/08-domain-driven-design.md).
- If public API changes: [docs/policies/11-public-api-idl.md](docs/policies/11-public-api-idl.md).
- If boundaries/integrations/ports/adapters change: [docs/policies/12-hexagonal-architecture.md](docs/policies/12-hexagonal-architecture.md).
- If container install/run workflows change: [docs/policies/13-container-build-rules.md](docs/policies/13-container-build-rules.md), [docs/policies/14-container-run-mounts.md](docs/policies/14-container-run-mounts.md), and [docs/policies/15-container-no-extra-env-isolation.md](docs/policies/15-container-no-extra-env-isolation.md).
- If AI executes a labeled task/finding (`basic`/`advanced`): [docs/policies/16-ai-agent-reasoning-level.md](docs/policies/16-ai-agent-reasoning-level.md).
- If application logging behavior changes: [docs/policies/17-logging-stdout-json.md](docs/policies/17-logging-stdout-json.md).
- For ADR/docs/comments/code comments: [docs/policies/09-language-simple-english.md](docs/policies/09-language-simple-english.md).

## Release Work
- Use SemVer and release rules in [docs/policies/06-versioning-release.md](docs/policies/06-versioning-release.md).

## Project Layout Baseline
- `src/` implementation
- `tests/` automated tests
- `Containerfiles/` OCI build profiles
- `scripts/` local automation
- `docs/` ADRs, diagrams, interfaces, policies, schemas
