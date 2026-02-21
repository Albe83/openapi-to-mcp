# Metrics Transport Standard

Policy Owner: Engineering Maintainers

## Scope
Apply this policy when telemetry export, protocol, or routing behavior changes.

## Default Rule
All services MUST use OpenTelemetry SDK instrumentation for telemetry signals that are in scope.
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

Additional mandatory attributes may be defined by the platform.

## Security and Access
Telemetry transport MUST comply with platform security standards.
When required by platform baseline, mTLS and restricted network access to Collector endpoints MUST be applied.
Collector endpoints MUST NOT be publicly exposed.

## Exception Rule
If a requirement is not feasible, create an ADR exception before implementation.
The ADR must include constraint, risk, mitigation, and convergence plan.

## Required Artifacts
For new or changed telemetry export behavior, PR must include:
- OTLP protocol/endpoint configuration evidence,
- required resource attributes evidence,
- ADR link when exception is used.

## Non-Compliant
- No OTLP export to platform Collector.
- Direct export to external backend without ADR.
- Non-OpenTelemetry instrumentation framework.
- Missing required resource attributes.
- Custom transport mechanism without ADR.
