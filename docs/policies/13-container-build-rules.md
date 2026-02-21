# Container Build Rules

Policy Owner: Engineering Maintainers

## Purpose and Scope
This policy applies when adding or updating container build artifacts.
Artifacts include `Containerfiles/*`, container wrapper scripts, and related docs.

## Location and Profiles
- Containerfiles must be stored in root `Containerfiles/`.
- Keep profile split:
  - `Containerfile.prod` for runtime,
  - `Containerfile.dev` for local development,
  - `Containerfile.test` for lint and tests.

## Tool-Agnostic Requirement
- Do not require one specific container tool.
- Build and run flows must support tool selection by environment variables.
- Use neutral terms like OCI builder/runner in documentation.
- Apply mount rules from `14` when builder support is available.

## Build Best Practices
- Use multi-stage builds.
- Keep `prod` image minimal and run as non-root.
- Install dependencies in cache-friendly order.
- Keep build context small with ignore rules.
- Avoid adding packages that are not required by runtime or tests.
- Keep PIP TLS workarounds opt-in via build arguments only.
- Do not hard-code insecure pip flags in Containerfiles.

## Validation Evidence
For container-related PRs include:
- build evidence for all changed profiles,
- smoke result for `prod` (`/healthz`),
- lint/test evidence from `test` profile when applicable,
- image size and build-time notes for before/after comparison when available.
- reason and exact opt-in PIP args when TLS workarounds are used.

## Non-Compliant
- Containerfiles outside `Containerfiles/`.
- Hard-coded dependency on one builder/runner.
- `prod` image running as root without explicit approved reason.
- Hard-coded insecure pip TLS bypass in Containerfiles.
- Missing smoke/lint/test evidence for changed profiles.
