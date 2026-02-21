# Review and Findings Policy

Policy Owner: Engineering Maintainers

Every code change must include a mandatory review before PR merge.

## Review Timing and Roles
- Review is required before merge to `main`.
- Author must complete a structured self-review.
- At least one independent reviewer must complete a second review.

## Finding Management
- Each finding must create one dedicated sub-issue.
- Use [.github/ISSUE_TEMPLATE/finding.yml](../../.github/ISSUE_TEMPLATE/finding.yml) for tracking.
- Each sub-issue must link the PR and describe resolution criteria.
- Each finding sub-issue must include labels: `task`, `finding`, exactly one of `basic` or `advanced`, and exactly one priority label.
- Priority labels are `priority:high`, `priority:medium`, `priority:low`.
- Finding sub-issues must follow task decomposition/labeling rules in [02-lifecycle.md](02-lifecycle.md).

## Priority Rules
- High: Bug, Security.
- Medium: Optimization, Code Quality.
- Low: all other findings.

Priority must be assigned when creating the finding sub-issue.

## PR Traceability
PR must include:
- review completion evidence (author + independent reviewer),
- list of findings,
- one sub-issue link per finding,
- finding category and priority.

If no findings are detected, PR must explicitly state "no findings".

## Non-Compliant
- Merge without mandatory review.
- Finding without dedicated sub-issue.
- Finding sub-issue not compliant with [02-lifecycle.md](02-lifecycle.md).
- Finding sub-issue missing `finding` label.
- Finding sub-issue missing required priority label.
- Bug/Security finding not marked High.
- Optimization/Code Quality finding not marked Medium.
