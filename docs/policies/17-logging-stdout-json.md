# Logging to Stdout and JSON

Policy Owner: Engineering Maintainers

## Scope
This policy applies to all applications in this repository, including runtime services, CLIs, and jobs.

## Rules
- Application logs MUST be emitted to standard output (`stdout`).
- Application logs SHOULD be single-line JSON records.
- `stderr` MUST be used only for critical/fatal errors where immediate operator attention is required.
- If JSON logging is not feasible for a component, the PR MUST document:
  - the technical reason,
  - the impacted component,
  - and the planned follow-up (or explicit rationale for no follow-up).

## Recommended JSON Fields
When JSON is used, each log line should include at least:
- `timestamp`
- `level`
- `message`
- `service`

Optional fields such as `trace_id`, `request_id`, and `task_id` are strongly recommended when available.

## Non-Compliant
- Writing normal application logs to local files instead of `stdout`.
- Multi-line stack traces as default log format for normal events.
- Sending non-critical warnings/info logs to `stderr`.
- Using plain text logs without documented reason when JSON logging is feasible.
