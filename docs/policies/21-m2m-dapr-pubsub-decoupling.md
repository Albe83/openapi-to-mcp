# M2M Broker Decoupling via Dapr Pub/Sub Policy

Policy Owner: Engineering Maintainers

## Scope
This policy applies when machine-to-machine publish/subscribe broker integrations are introduced or materially changed.
It applies to both event producers and event consumers.

## Default Rule
When possible, applications MUST decouple message broker interactions through Dapr Pub/Sub.

## Exception Rule
If Dapr Pub/Sub is not feasible, an ADR exception is required before implementation.
The ADR must document:
- technical constraint that blocks Dapr Pub/Sub,
- impact and risk of the alternative approach,
- mitigation and operational controls,
- convergence plan and target timeline.

## Required Artifacts
- ADR with the broker decoupling decision and rationale.
- PR link to the ADR and affected integration interfaces.
- Event contracts remain governed by [19-m2m-events-asyncapi-cloudevents.md](19-m2m-events-asyncapi-cloudevents.md).
- If boundaries/ports/adapters change, apply [12-hexagonal-architecture.md](12-hexagonal-architecture.md).

## Rollout
This policy applies to new publish/subscribe integrations and material changes to existing ones.
Unchanged legacy integrations are not retrofitted.

## Non-Compliant
- New or changed broker publish/subscribe integration without Dapr Pub/Sub assessment.
- Alternative broker coupling selected without ADR exception.
- ADR exception missing constraints, risks, mitigations, or convergence timeline.
- PR missing required ADR and interface references.
