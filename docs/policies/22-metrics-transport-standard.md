# Metrics Transport Standard

Policy Owner: Engineering Maintainers

## Scope
Apply this policy when telemetry export, protocol, or routing changes.

## Signals in Scope
Signals in scope are telemetry signals intentionally emitted by service instrumentation or runtime configuration.
Metrics are mandatory when telemetry is implemented.
Traces/logs are in scope only when explicitly enabled.

## Default Rule
All services MUST use OpenTelemetry SDK instrumentation for in-scope telemetry signals.
All telemetry MUST be exported using OTLP to the platform-managed OpenTelemetry Collector.

Protocol policy:
- default: OTLP/gRPC (`4317`);
- OTLP/HTTP (`4318`) as fallback.

Services MUST NOT export telemetry directly to SaaS backends, vendor agents, or external collectors unless approved by ADR.

## Required Resource Attributes
Services MUST include:
- `service.name`
- `service.namespace`
- `service.version`
- `deployment.environment`

If additional attributes are mandatory, PR must link the source of truth (platform doc, deployment manifest, or environment specification).

## Security and Access
Telemetry transport MUST comply with the platform security baseline for the service.
PR must link the baseline source.
When baseline requires it, mTLS and restricted network access to Collector endpoints MUST be applied.
Collector endpoints MUST NOT be publicly exposed.

## Exception Rule
If a requirement is not feasible, create an ADR exception before implementation.
The ADR must include constraint, risk, mitigation, and convergence plan.

## Required Artifacts
For new or changed telemetry export behavior, PR must include:
- OTLP protocol/endpoint configuration evidence,
- required resource attributes evidence,
- baseline source link used for security validation,
- ADR link when exception is used.

## Non-Compliant
- No OTLP export to platform Collector.
- Direct export to external backend without ADR.
- Non-OpenTelemetry instrumentation framework.
- Missing required resource attributes.
- Missing source link for additional mandatory attributes when claimed.
- Missing baseline source link for transport security validation.
- Custom transport mechanism without ADR.
