# AI Agent Reasoning Level Policy

Policy Owner: Engineering Maintainers

This policy defines reasoning-effort selection for AI agents based on task complexity labels.

## Scope
This applies to all AI-executed tasks and finding sub-issues with `basic` or `advanced` labels.

## Rules
- Before execution, check the linked issue/sub-issue labels and confirm one complexity label.
- If label is `basic`, set reasoning effort to a balanced level (`medium` when available).
- If label is `advanced`, set reasoning effort to the highest available level.
- If platform/model does not expose reasoning-level control, continue in best-effort mode and record: `N/A - reasoning level control not supported`.
- If complexity label is missing or invalid, use a balanced default, then record the labeling gap in traceability evidence.

## Evidence
Record in PR, issue comment, or task log:
- complexity label found,
- reasoning level selected,
- fallback note when unsupported,
- link to the task/finding sub-issue.

## Non-Compliant
- No complexity-label check before AI execution.
- `advanced` execution without maximum reasoning when a maximum level is available.
- Missing evidence for unsupported reasoning control.
