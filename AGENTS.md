# Repository Guidelines

This file is intentionally minimal to reduce AI context usage.
Detailed contribution rules are split into focused policy modules.

## Source of Truth
- Primary policy index: `docs/policies/01-index.md`
- Policy governance rules: `docs/policies/00-policy-of-policies.md`
- If any guidance conflicts, `docs/policies/*` takes precedence.

## AI Agent Operating Rule
Before planning or coding:
1. Open `docs/policies/01-index.md`.
2. Load only the relevant policy module(s) for the current task.
3. Avoid loading unrelated policy files.

## Mandatory for Feature/Bugfix Code Changes
- Follow lifecycle policy: `docs/policies/02-lifecycle.md`.
- Decompose work to junior-executable tasks where possible.
- Label each task/finding sub-issue as `task` + exactly one of `basic` or `advanced`.
- Create architecture artifacts first: `docs/policies/03-architecture-first.md`.
- Keep required architecture diagrams in `docs/diagrams/` and link them from ADRs.
- For boundary/integration changes, apply Hexagonal assessment/rules: `docs/policies/12-hexagonal-architecture.md`.
- Apply TDD: `docs/policies/04-testing-tdd.md`.
- Run lint for changed artifacts when available; record `N/A` with reason when not available.
- Follow trunk/PR/commit rules: `docs/policies/05-git-and-pr.md`.
- Run mandatory review and findings flow: `docs/policies/10-review-and-findings.md`.
- Meet DoD and compliance checks: `docs/policies/07-compliance-dod.md`.

## Conditional Modules
- If model/schema changes: `docs/policies/08-domain-driven-design.md`.
- If public API changes: `docs/policies/11-public-api-idl.md`.
- If boundaries/integrations/ports/adapters change: `docs/policies/12-hexagonal-architecture.md`.
- For ADR/docs/comments/code comments: `docs/policies/09-language-simple-english.md`.

## Release Work
- Use SemVer and release rules in `docs/policies/06-versioning-release.md`.

## Project Layout Baseline
- `src/` implementation
- `tests/` automated tests
- `examples/` sample I/O
- `scripts/` local automation
