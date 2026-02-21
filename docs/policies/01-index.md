# Policy Index

Policy Owner: Engineering Maintainers

Entrypoint for contribution policy rules.
For feature and bugfix code changes, policies are mandatory.

## Read Order
1. [01-index.md](01-index.md)
2. [00-policy-of-policies.md](00-policy-of-policies.md) (meta rules)
3. Task-specific modules only

## Quick Map
- [02-lifecycle.md](02-lifecycle.md): issue -> junior-first task decomposition -> labeled sub-issues -> PR flow.
- [03-architecture-first.md](03-architecture-first.md): ADR + separate Class/Sequence Markdown Mermaid in [docs/diagrams/](../diagrams) + data model JSON Schema (YAML preferred).
- [04-testing-tdd.md](04-testing-tdd.md): TDD + test/lint evidence rules for feature and bugfix.
- [05-git-and-pr.md](05-git-and-pr.md): trunk workflow, branch naming, commits, PR, merge.
- [06-versioning-release.md](06-versioning-release.md): SemVer and release rules.
- [07-compliance-dod.md](07-compliance-dod.md): DoD checks, enforcement, non-compliance.
- [08-domain-driven-design.md](08-domain-driven-design.md): DDD assessment/rules for model/schema changes.
- [09-language-simple-english.md](09-language-simple-english.md): repository language and simple English rules.
- [10-review-and-findings.md](10-review-and-findings.md): mandatory review workflow and finding priorities.
- [11-public-api-idl.md](11-public-api-idl.md): formal IDL rules for public API changes.
- [12-hexagonal-architecture.md](12-hexagonal-architecture.md): Hexagonal assessment/rules for boundary and integration changes.
- [13-container-build-rules.md](13-container-build-rules.md): tool-agnostic container profile and build evidence rules.
- [14-container-run-mounts.md](14-container-run-mounts.md): RUN mount isolation and compat fallback rules.
- [15-container-no-extra-env-isolation.md](15-container-no-extra-env-isolation.md): avoid nested env isolation inside containers unless required.
- [16-ai-agent-reasoning-level.md](16-ai-agent-reasoning-level.md): AI reasoning level by `basic`/`advanced` complexity label.

## Default Paths
- Feature/bugfix code: `02` -> `03` -> `04` -> `05` -> `10` -> `07`
- If model/schema changes: also read `08`.
- For ADR/docs/comments/code comments: also read `09`.
- If public API changes: also read `11`.
- If boundaries/integrations/ports/adapters change: also read `12`.
- If container install/run workflows change: also read `13`, `14`, and `15`.
- If AI executes a labeled task/finding: also read `16`.
- Release activity: add `06`

## Context-Efficient Rule
Load only the modules needed for the active task.
Do not load the full policy set unless auditing governance.

## Visual Overview
For a high-level governance map, see:
[docs/diagrams/0001-governance-mindmap.md](../diagrams/0001-governance-mindmap.md)
This diagram is descriptive and does not replace normative policy text.
