# Policy of Policies

Policy Owner: Engineering Maintainers

## Purpose and Scope
This policy governs how all files in `docs/policies/` are authored, changed, and consumed.
It applies to humans and AI agents.

## Structure and Naming
- Use numeric prefixes to enforce reading order.
- Keep one topic per module.
- Keep normative rules in policy modules only; do not duplicate them in entrypoint files.

## Word Limit (Hard Rule)
- Each policy module must stay at or below 300 words.
- If a module exceeds the limit, split it into focused modules and update the index.

## Single-Owner Rule
- Every normative rule must have one owner module.
- Cross-module references are allowed; duplicated normative text is not.

## Ownership and Review
- Each module must declare a policy owner.
- Any policy change requires an issue and PR with rationale, impact, and updated references.
- At least one maintainer review is mandatory before merge.

## AI Context Rule
Agents must load `01-index.md` first, then only the modules required for the task.

## Compliance Checks
Before merge, verify:
- word count <= 300 per module,
- links and numbering are valid,
- owner field exists,
- no duplicated normative rules,
- policy text uses simple English.
