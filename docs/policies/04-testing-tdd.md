# Testing and TDD Policy

Policy Owner: Engineering Maintainers

TDD is mandatory for feature and bugfix code changes.

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

## PR Evidence
Feature PRs must include test-first sequence, commands run, and result summary.
Bugfix PRs must include reproduction test, pre-fix failure evidence, and post-fix success evidence.
Run lint for each changed artifact when a matching linter exists.
If no linter exists for a changed artifact type, record explicit `N/A` with reason in PR validation.

Use [.github/pull_request_template.md](../../.github/pull_request_template.md).

## Scope
Mandatory for feature and bugfix code changes.
Refactor-only changes should still preserve behavior and keep tests green.

## Non-Compliant
- Feature/bugfix implementation before tests.
- Bugfix without reproduction test.
- PR without TDD evidence.
- PR missing lint evidence for changed artifacts.
