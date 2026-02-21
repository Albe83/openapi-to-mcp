# Metrics Design Standard (USE and RED)

Policy Owner: Engineering Maintainers

## Scope
Apply this policy when a service introduces or changes metric definitions.

## Naming and Semantics
- Metric names MUST be clear, stable, and unambiguous.
- Use OpenTelemetry semantic conventions when a standard metric exists.
- Custom metrics MUST use a service-prefixed namespace.
- Every metric MUST include a clear description and explicit base unit (`seconds`, `bytes`, `requests`, `items`, `ratio`).
- The same intent MUST NOT be represented by multiple metric names.
- Counters MUST be monotonic and cumulative.

## USE for Bounded Resources
For each bounded resource (for example thread pool, connection pool, queue, buffer, and similar resources), capacity MUST be measurable or derivable and services MUST model:
- Usage,
- Saturation,
- Errors.

Missing a USE dimension requires an ADR exception with risk, mitigation, and convergence plan.

## RED for Request-Driven Interfaces
For request-driven interfaces, RED metrics (Rate, Errors, Duration) MUST be implemented.
This applies to HTTP endpoints and equivalent request/reply interfaces.

Duration (latency) MUST be implemented as a histogram.
Histogram bucket limits MUST be explicitly defined and documented.
Buckets MUST avoid excessive granularity and remain operationally meaningful.

## Cardinality Control
Attributes MUST be stable and low-cardinality.

User identifiers, request identifiers, session IDs, and payload-derived values are prohibited without ADR approval.
Cardinality explosions are considered production-impacting defects.

## Required Artifacts
PR evidence must include:
- metric catalog (`name`, `description`, `unit`),
- USE mapping for bounded resources,
- RED mapping and latency histogram bucket list.

## Non-Compliant
- Ambiguous metric naming or missing unit/description.
- Missing USE coverage for bounded resources without ADR.
- Request-driven interfaces without RED metrics.
- Latency modeled without histogram or with undocumented bucket limits.
