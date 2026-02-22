# Container Build Rules

Policy Owner: Engineering Maintainers

## Purpose and Scope
This policy applies when adding or updating container build artifacts.
Artifacts include `Containerfiles/*`, container wrapper scripts, and related docs.

## Tool-Agnostic Requirement
- Do not require one specific container tool.
- Build and run flows must support tool selection by environment variables.
- Standard variables are:
  - `OCI_BUILDER` (build),
  - `OCI_RUNNER` (run/smoke),
  - `CONTAINERFILE_VARIANT` (`mount`/`compat`).
- Use neutral terms like OCI builder/runner in documentation.
- Apply mount rules from `14` when builder support is available.
- Apply no-extra-env-isolation rule from `15` for container install/run workflows.

## Artifact Types
- HTTP service image (serves HTTP endpoints).
- Non-HTTP image (job/worker/CLI).
- Test image (lint/test execution).

## Build Best Practices
- Use multi-stage builds.
- Keep `prod` image minimal and run as non-root.
- Install dependencies in cache-friendly order.
- Keep build context small with ignore rules.
- Keep PIP TLS workarounds opt-in via build arguments only.
- Do not hard-code insecure pip flags in Containerfiles.

## Validation Evidence
For container-related PRs include:
- build evidence for all changed profiles,
- smoke evidence by artifact type:
  - HTTP service: HTTP check to documented health endpoint (default `/healthz`),
  - non-HTTP image: command execution with successful exit code,
- lint/test evidence from `test` profile when applicable,
- image size and build-time notes for before/after comparison when available, otherwise explicit `N/A - <reason>`,
- reason and exact opt-in PIP args when TLS workarounds are used.

Evidence records must include command and pass/fail result.

## Non-Compliant
- Containerfiles outside `Containerfiles/`.
- Hard-coded dependency on one builder/runner.
- `prod` image running as root without explicit approved reason.
- Hard-coded insecure pip TLS bypass in Containerfiles.
- Missing smoke/lint/test evidence required by artifact type.
