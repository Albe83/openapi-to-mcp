# Policy Index

Policy Owner: Engineering Maintainers

This is the entrypoint for all contribution policy rules.
For feature and bugfix code changes, policies are mandatory for humans and AI agents.

## Read Order
1. `01-index.md`
2. `00-policy-of-policies.md` (meta rules)
3. Task-specific modules only

## Quick Map
- `02-lifecycle.md`: issue -> junior-first task decomposition -> labeled sub-issues -> PR flow.
- `03-architecture-first.md`: ADR + separate Class/Sequence Markdown Mermaid in `docs/diagrams/` + data model JSON Schema (YAML preferred).
- `04-testing-tdd.md`: TDD + test/lint evidence rules for feature and bugfix.
- `05-git-and-pr.md`: trunk workflow, branch naming, commits, PR, merge.
- `06-versioning-release.md`: SemVer and release rules.
- `07-compliance-dod.md`: DoD checks, enforcement, non-compliance.
- `08-domain-driven-design.md`: DDD assessment/rules for model/schema changes.
- `09-language-simple-english.md`: repository language and simple English rules.
- `10-review-and-findings.md`: mandatory review workflow and finding priorities.
- `11-public-api-idl.md`: formal IDL rules for public API changes.
- `12-hexagonal-architecture.md`: Hexagonal assessment/rules for boundary and integration changes.

## Default Paths
- Feature/bugfix code: `02` -> `03` -> `04` -> `05` -> `10` -> `07`
- If model/schema changes: also read `08`.
- For ADR/docs/comments/code comments: also read `09`.
- If public API changes: also read `11`.
- If boundaries/integrations/ports/adapters change: also read `12`.
- Release activity: add `06`

## Context-Efficient Rule
Load only the modules needed for the active task.
Do not load the full policy set unless auditing governance.
