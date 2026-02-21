# Container RUN Mount Policy

Policy Owner: Engineering Maintainers

## Purpose and Scope
This policy defines how `RUN` (and equivalent mutating build steps) must handle filesystem side effects.
It applies to all files in `Containerfiles/`.

## Core Rule
When a build tool supports mount options, mutating steps must use mount overlays to isolate indirect writes.
Keep direct, intended image changes in layers.
Move transient side effects (cache, logs, temp files) to mounted filesystems.

## Required Mount Patterns (When Applicable)
- Use `type=cache` for package/dependency caches.
  Example targets: pip cache directories, package manager cache directories.
- Use `type=tmpfs` for temporary/log paths not needed in final image.
  Example targets: `/tmp`, tool-specific temp/log directories.

## Compatibility Fallback
- If builder does not support mount syntax, use the `.compat` containerfile variant.
- This fallback is allowed only with explicit PR evidence:
  - builder limitation,
  - selected variant,
  - `N/A` with reason for unavailable mount isolation.

## Non-Compliant
- Mutating dependency install step without mount isolation when supported.
- Writing cache/log artifacts to image layers without technical reason.
- Using `.compat` variant without documenting why mount variant was not possible.
