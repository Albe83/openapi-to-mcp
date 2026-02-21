# Container Native Isolation Policy

Policy Owner: Engineering Maintainers

## Purpose and Scope
This policy applies when installing or running software inside containers.
It covers `Containerfiles/*`, container build scripts, run scripts, and container command examples in docs.

## Default Rule
Treat the container as the primary isolation boundary.
Do not add extra environment isolation layers inside the container unless technically required.

## Disallowed by Default
- Python virtual environments (`venv`, `virtualenv`) inside container images or runtime commands.
- Extra Node environment isolation patterns used only to duplicate container isolation.
- Similar nested isolation wrappers that add complexity without a technical need.

## Allowed Exceptions
An exception is allowed only when a tool or platform constraint requires nested isolation.
Preference or habit is not a valid reason.

## Required Evidence for Exceptions
If an exception is used, the PR must include:
- technical reason and constraint,
- impacted files/commands,
- why container-level isolation is not sufficient,
- `N/A` when this policy is not applicable to the change.

## Non-Compliant
- Introducing `venv` or equivalent inside container workflows without a required technical reason.
- Keeping nested isolation after the original technical constraint no longer exists.
- Using an exception without the required PR evidence.
