# Logging to Stdout and JSON

Policy Owner: Engineering Maintainers

## Scope
This policy applies to all applications in this repository, including runtime services, CLIs, and jobs.

## Rules
- Application logs MUST be emitted to standard output (`stdout`).
- Service/job application logs follow this rule without exception.
- Application logs SHOULD be single-line JSON records.
- CLI functional output (command result consumed by user/script) may use `stdout` and is not considered a log record.
- For services/jobs, `stderr` is reserved for critical/fatal errors requiring immediate operator attention.
- For CLI commands, `stderr` may be used for user-facing failure diagnostics when command exit code is non-zero.
- If JSON logging is not feasible for a component, the PR MUST document:
  - the technical reason,
  - the impacted component,
  - the fallback format used,
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
- Sending service/job non-critical warnings/info logs to `stderr`.
- Using plain text logs without documented reason when JSON logging is feasible.
