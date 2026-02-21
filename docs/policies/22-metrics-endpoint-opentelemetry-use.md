# Metrics Endpoint, OpenTelemetry, and USE Policy

Policy Owner: Engineering Maintainers

## Scope
This policy applies when an application introduces or changes runtime metrics exposure.

## Default Rule
Applications MUST expose a dedicated metrics fetching endpoint.
The endpoint SHOULD be `/metrics` unless a platform standard requires a different path.
Metrics output MUST use OpenMetrics scraping format.
Metrics naming and attributes MUST follow OpenTelemetry semantic conventions where applicable.

## USE Model Rule
Metrics SHOULD follow the USE model (Usage, Saturation, Errors) where applicable.
For each limited internal resource, implementers must evaluate all three USE dimensions and emit the applicable metrics.

## Required Resource Coverage
If present, metrics coverage MUST include:
- thread pool,
- connection pool,
- queue or buffer capacity.

Any other relevant bounded internal resource MUST be included when present.

## Exception Rule
If a required USE dimension or resource metric is not feasible, an ADR exception is required.
The ADR must document constraint, risk, mitigation, and convergence plan.

## Required Artifacts
- ADR with resource inventory and USE mapping.
- PR link to ADR and metrics endpoint details.

## Rollout
Applies to new services and material changes to existing metrics behavior.

## Non-Compliant
- No dedicated metrics endpoint.
- Metrics exposed without OpenMetrics or without OpenTelemetry semantic conventions.
- Limited resources present but missing USE assessment.
- Missing ADR exception for gaps.
