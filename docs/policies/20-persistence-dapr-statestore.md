# Persistence via Dapr StateStore Policy

Policy Owner: Engineering Maintainers

## Scope
This policy applies when a change introduces or modifies application state persistence flows.
It applies to both internal and public-facing services.

## Default Rule
When possible, applications MUST decouple state persistence through Dapr StateStore.

## Exception Rule
If Dapr StateStore is not feasible, an ADR exception is required before implementation.
The ADR must describe:
- technical constraint blocking Dapr StateStore,
- impact and risk of the alternative,
- mitigation and operational controls,
- convergence plan and target timeline.

## Required Artifacts
- ADR with the persistence decision and rationale.
- PR link to the ADR and affected persistence interfaces/adapters.
- If data model changes, update schemas per [03-architecture-first.md](03-architecture-first.md) and [08-domain-driven-design.md](08-domain-driven-design.md).
- If boundaries/ports/adapters are changed, apply [12-hexagonal-architecture.md](12-hexagonal-architecture.md).

## Rollout
This policy applies to new persistence flows and material changes to existing flows.
Unchanged legacy persistence is not retrofitted.

## Non-Compliant
- New or changed persistence implemented without a Dapr StateStore assessment.
- Alternative persistence chosen without ADR exception.
- ADR exception missing constraints, risks, mitigations, or convergence timeline.
- PR missing required architecture links for the persistence decision.
