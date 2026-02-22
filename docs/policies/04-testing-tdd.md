# Testing and TDD Policy

Policy Owner: Engineering Maintainers

## Scope
- TDD is mandatory for `feat` and `fix` code changes.
- For `docs`/`chore`/`refactor`/`ci` only changes, TDD sequence may be `N/A`, but validation evidence is still required.

## Feature Flow
1. Write or update tests first.
2. Confirm tests express missing behavior.
3. Implement minimal code to pass tests.
4. Refactor while tests stay green.

## Bugfix Flow (Strict)
1. Add a test that reproduces the bug.
2. Verify the test fails on current behavior.
3. Implement the fix.
4. Verify reproduction and regression tests pass.

## Matching Linter Rule
A matching linter exists when the repository has a maintained command for the changed artifact type.

For this repository:
- Python source/tests: `make lint`.
- Policy/Markdown/governance artifacts: `make governance-check`.

If no matching linter exists, PR must include:
`N/A - no matching linter for <artifact-type>: <reason>`.

## PR Evidence
Feature PRs must include test-first sequence, commands run, and result summary.
Bugfix PRs must include reproduction test, pre-fix failure evidence, and post-fix success evidence.

Minimum evidence record for each validation command:
- command,
- scope,
- result (`pass`/`fail`) with short output summary.

Use [.github/pull_request_template.md](../../.github/pull_request_template.md).

## Mixed-Scope Rule
If any `feat` or `fix` code is present, full TDD evidence is required for changed code paths.
Non-`feat`/`fix` sections may use explicit `N/A` where applicable.

## Non-Compliant
- Feature/bugfix implementation before tests.
- Bugfix without reproduction test.
- PR without TDD evidence.
- PR missing lint evidence for changed artifacts when a matching linter exists.
