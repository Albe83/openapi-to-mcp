# Git and PR Policy

Policy Owner: Engineering Maintainers

## Trunk-Based Workflow
- `main` is the trunk.
- Use short-lived branches (hours; max 1-2 days).
- Keep PRs small and single-purpose.

## Branch Naming
Use `type/issue-id-slug`, for example:
- `feat/123-openapi-loader`
- `fix/245-null-operationid`

## Commit Convention
Use Conventional Commits:
`<type>(<scope>): <summary>`

Allowed types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `build`, `perf`.
Breaking changes require `!` and/or `BREAKING CHANGE:` footer.

## Pull Request Rules
- Target branch must be `main`.
- PR title should be `<type>: <summary> (#issue-id)`.
- Link parent issue and relevant sub-issues.
- Link ADR/diagram artifacts.
- Include required test and TDD evidence.

## Merge Rules
- Use `Squash merge` only.
- Squash commit message must follow Conventional Commits.
