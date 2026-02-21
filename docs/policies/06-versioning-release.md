# Versioning and Release Policy

Policy Owner: Engineering Maintainers

Releases must follow Semantic Versioning 2.0.0.

## Tag Format
Stable releases use:
- `vMAJOR.MINOR.PATCH` (example: `v1.4.2`)

Allowed pre-release forms:
- `vX.Y.Z-alpha.N`
- `vX.Y.Z-beta.N`
- `vX.Y.Z-rc.N`

Build metadata is optional (example: `v1.4.2+build.7`).

## Version Increment Rules
- `PATCH`: backward-compatible fixes
- `MINOR`: backward-compatible features
- `MAJOR`: breaking/incompatible changes

## Mixed Bump Policy
Default bump from Conventional Commits:
- `fix` -> patch
- `feat` -> minor
- `!` or `BREAKING CHANGE` -> major

Manual override is allowed only in the release PR with explicit rationale.

## Release PR Requirements
- Target version
- Bump rationale
- Breaking change list (if any)
- Release notes summary

## Non-Compliant
- Tags not matching allowed SemVer forms.
- Release PR missing bump rationale.
