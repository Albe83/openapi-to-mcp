# M2M Protocol Selection Policy

Policy Owner: Engineering Maintainers

## Scope
This policy applies to machine-to-machine communication for both public and internal integrations.

## Default Rule
For Command/Reply communication, the default protocol MUST be REST API with a formal OpenAPI contract.

## gRPC Exception Rule
gRPC MAY be used only when latency or call-volume constraints cannot be met with the default REST approach.
The exception MUST be documented in an ADR with explicit measurable targets and rationale, including:
- latency target (for example p95),
- throughput/volume target,
- reason the default REST option is not sufficient.

## Required Artifacts
- REST choice: OpenAPI contract in [docs/interfaces/](../interfaces).
- gRPC choice: Protobuf contract in [docs/interfaces/](../interfaces).
- PR MUST link ADR and the related IDL artifact.

## Rollout
This policy applies to new integrations and material protocol changes from adoption time.
Existing integrations are not retrofitted unless they are changed.

## Non-Compliant
- Command/Reply M2M implemented with a non-REST default without an ADR exception.
- gRPC adopted without explicit latency/volume targets in ADR.
- Protocol implemented in code without matching IDL update.
