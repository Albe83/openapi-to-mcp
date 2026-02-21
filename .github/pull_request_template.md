## Summary
- Parent issue: # (Required for `feat`/`fix`; otherwise `N/A - <reason>`)
- Sub-issues: #
- Change type: feat / fix / docs / refactor / test / chore / ci / build / perf

Applicability rule:
- For `feat`/`fix`, lifecycle, architecture, and TDD requirements are mandatory.
- For non-`feat`/`fix` PRs, complete only applicable items and use `N/A - <reason>` for out-of-scope fields.
- If PR scope is mixed, apply the strictest relevant requirements.

## Mandatory Links (Scope-Conditional)
- Functional analysis issue (Required for `feat`/`fix`): #
- Operational plan comment (Required for `feat`/`fix`, issue permalink):
- ADR(s) (Required for `feat`/`fix`): `docs/adr/...`
- Class diagram file (Required for `feat`/`fix`): `docs/diagrams/...`
- Sequence diagram file (Required for `feat`/`fix`): `docs/diagrams/...`
- Data model schema location(s) (Required if model changed): `docs/schemas/...`
- Hexagonal applicable for this change? `yes/no`
- Hexagonal ADR mapping location (Required if applicable): `docs/adr/...`
- Hexagonal diagram file (Required if applicable): `docs/diagrams/...`
- If not applicable: `N/A - Hexagonal not applicable: <reason>`
- Public API change? `yes/no`
- IDL type (Required if API changed): `OpenAPI/AsyncAPI/GraphQL/Proto/Other`
- IDL spec location (Required if API changed): `docs/interfaces/...`
- DDD artifacts location(s) (Required if model/schema changed): ADR section(s) with UL / BC / Aggregates
- Container install/run workflow changed? `yes/no`
- Container policy evidence (Required if `yes`): compliance with `13`/`14`/`15` or `N/A - <reason>`

## TDD Evidence (Required for `feat`/`fix`)
If change type is not `feat`/`fix`, set this section to `N/A - <reason>`.

### Feature
- [ ] Test-first sequence documented.
- [ ] New/updated tests were written before implementation.

### Bugfix
- [ ] Reproduction test added first.
- [ ] Reproduction test failed before fix.
- [ ] Reproduction + regression tests pass after fix.

## Validation
- [ ] Test commands run (or `N/A - <reason>`):
  - `...`
- [ ] Task-start branch guard evidence:
  - `git branch --show-current`
  - `git fetch origin`
  - `git merge --ff-only origin/main` (or equivalent)
- [ ] Lint commands run for changed artifacts with available linter:
  - `...`
- [ ] `N/A` with reason for changed artifacts without linter (if any):
  - `...`
- [ ] Results summary:
  - `...`

## Review Findings (Mandatory)
- Author self-review completed: `yes/no`
- Independent review completed: `yes/no`
- Findings outcome: `no findings` / `findings listed`
- If outcome is `no findings`, include exact statement: `no findings`
- If outcome is `findings listed`, fill one table row per finding.
- For findings, create sub-issues with [.github/ISSUE_TEMPLATE/finding.yml](./ISSUE_TEMPLATE/finding.yml).
- Each finding sub-issue must include labels: `task`, `finding`, one of `basic`/`advanced`, and one priority label.

| Finding | Category | Priority | Sub-issue |
| --- | --- | --- | --- |

## Impact and Risk
- Scope of impact:
- Compatibility notes:
- Rollout notes:

## Checklist
- [ ] PR targets `main`.
- [ ] Branch follows `type/issue-id-slug`.
- [ ] Conventional Commits used.
- [ ] Task started on the correct branch and branch was synced with base before implementation.
- [ ] For `feat`/`fix`, required lifecycle links are present (analysis issue + plan comment + sub-issues).
- [ ] For `feat`/`fix`, class and sequence diagrams are in Markdown Mermaid and render in GitHub.
- [ ] For `feat`/`fix`, diagram files are in `docs/diagrams/*.md` and linked in ADR and PR.
- [ ] For `feat`/`fix` boundary/integration changes, Hexagonal applicability is assessed.
- [ ] If Hexagonal is applicable, ADR mapping + dedicated Hexagonal diagram are linked.
- [ ] If Hexagonal is not applicable, explicit `N/A` rationale is provided.
- [ ] If data model changed, JSON Schema is updated in [docs/schemas/](../docs/schemas) (YAML preferred).
- [ ] If public API changed, formal IDL is updated in [docs/interfaces/](../docs/interfaces) and linked.
- [ ] If IDL format supports YAML, YAML is preferred (JSON only if needed).
- [ ] If data model/schema changed, DDD applicability is assessed.
- [ ] If DDD is applicable, UL/BC/Aggregates are documented and linked.
- [ ] If container install/run workflows changed, compliance with `13`/`14`/`15` is evidenced.
- [ ] If policy `15` exception is used, technical rationale and impacted files/commands are documented.
- [ ] New/updated ADR/docs/comments are written in simple English.
- [ ] Any non-simple wording is justified when required for precision.
- [ ] Mandatory review completed (author + independent reviewer).
- [ ] Review outcome is explicit (`no findings` or findings listed in table).
- [ ] If findings exist, one sub-issue exists for each finding.
- [ ] If findings exist, each finding sub-issue has labels `task` + `finding` + exactly one `basic`/`advanced` + exactly one priority label.
- [ ] Task/finding sub-issues use `task` + exactly one `basic`/`advanced` label.
- [ ] `advanced` sub-issues include rationale for non-decomposable complexity.
- [ ] Finding priorities use policy mapping (Bug/Security=High, Optimization/Code Quality=Medium, other=Low).
- [ ] Lint executed for changed artifacts where available; missing linter coverage documented as `N/A` with reason.
- [ ] Related docs updated.
- [ ] SemVer impact evaluated (if release-related).
