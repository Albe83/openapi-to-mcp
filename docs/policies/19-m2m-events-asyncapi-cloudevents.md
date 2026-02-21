# M2M Event Messaging Policy

Policy Owner: Engineering Maintainers

## Scope
This policy applies to machine-to-machine Event-Driven and Pub/Sub integrations, both internal and public.

## Default Rule
Event interfaces MUST be defined with AsyncAPI.
For new event flows, emitted events MUST be modeled as CloudEvents.

## Exception Rule
Deviation from AsyncAPI or CloudEvents is allowed only with an ADR exception that documents:
- technical constraint,
- impact and risk,
- mitigation,
- convergence plan and timeline.

## Required Artifacts
- Event contracts are stored in [docs/interfaces/](../interfaces).
- PR MUST link the ADR decision and the related interface artifact.
- If an exception is used, PR MUST link the ADR exception section.

## Rollout
This policy applies to new event integrations and material changes to existing event flows.
Existing flows are not retrofitted unless they are changed.

## Non-Compliant
- Event-Driven/PubSub integration without AsyncAPI contract.
- New event flow not modeled as CloudEvents and missing ADR exception.
- Event contract changed in code without matching interface update.
