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

## Release Changelog (GitHub Release Notes)
- Each release MUST include a curated changelog in GitHub Release notes.
- `CHANGELOG.md` in repository is optional and is not required by this policy.
- Changelog content source is annotated tag notes.
- Required changelog sections:
  - `## Summary`
  - `## Added`
  - `## Changed`
  - `## Fixed`
  - `## Breaking Changes` (use `None` if not applicable)
  - `## Migration Notes` (use `None` if not applicable)
  - `## References` (issues/PR links)
- Required section headings must exist and section content must not be empty.

## Release PR Requirements
- Target version
- Bump rationale
- Breaking change list (if any)
- Release notes summary
- Curated changelog draft with required sections.

## Non-Compliant
- Tags not matching allowed SemVer forms.
- Release PR missing bump rationale.
- Release without curated changelog in GitHub Release notes.
- Missing required changelog section.
- Lightweight tag release without annotated changelog notes.
