# Policy Index

Policy Owner: Engineering Maintainers

Entrypoint for governance policies.
Use this index to load only the modules needed for the current task.

## Read Order
1. [01-index.md](01-index.md)
2. [00-policy-of-policies.md](00-policy-of-policies.md) (meta rules)
3. Task-specific modules only

## Module Catalog (When to Read / What It Covers)
- [02-lifecycle.md](02-lifecycle.md): Read for any `feat`/`fix`. Covers issue -> plan -> sub-issues flow and `basic`/`advanced` task labels.
- [03-architecture-first.md](03-architecture-first.md): Read when solution design is needed. Covers ADR-first flow, diagrams, schemas, and IDL linkage.
- [04-testing-tdd.md](04-testing-tdd.md): Read for implementation/testing work. Covers TDD, bug reproduction-first, and lint/test evidence.
- [05-git-and-pr.md](05-git-and-pr.md): Read when creating branches, commits, and PRs. Covers trunk rules, naming, branch guard, merge policy.
- [06-versioning-release.md](06-versioning-release.md): Read for release work. Covers SemVer tags, bump logic, and changelog requirements.
- [07-compliance-dod.md](07-compliance-dod.md): Read before merge. Defines Definition of Done and compliance gate expectations.
- [08-domain-driven-design.md](08-domain-driven-design.md): Read if model/schema changes. Covers DDD applicability and required outputs.
- [09-language-simple-english.md](09-language-simple-english.md): Read for ADR/docs/comments. Defines simple-English repository language rules.
- [10-review-and-findings.md](10-review-and-findings.md): Read for review phase. Covers mandatory review flow, findings, priorities, labels.
- [11-public-api-idl.md](11-public-api-idl.md): Read if public API changes. Covers formal IDL requirements and traceability.
- [12-hexagonal-architecture.md](12-hexagonal-architecture.md): Read if boundaries/integrations/ports/adapters change. Covers Hexagonal assessment and artifacts.
- [13-container-build-rules.md](13-container-build-rules.md): Read for container build profile decisions and evidence.
- [14-container-run-mounts.md](14-container-run-mounts.md): Read for `RUN` mount usage, cache/tmpfs isolation, and compat fallback.
- [15-container-no-extra-env-isolation.md](15-container-no-extra-env-isolation.md): Read for container runtime/tool env isolation policy and exceptions.
- [16-ai-agent-reasoning-level.md](16-ai-agent-reasoning-level.md): Read when AI works on labeled tasks/findings. Maps `basic`/`advanced` to reasoning level.
- [17-logging-stdout-json.md](17-logging-stdout-json.md): Read when logging behavior changes. Covers stdout-first and JSON single-line preference.
- [18-m2m-protocol-selection.md](18-m2m-protocol-selection.md): Read for Command/Reply M2M protocol choices. REST/OpenAPI default, gRPC by ADR exception.
- [19-m2m-events-asyncapi-cloudevents.md](19-m2m-events-asyncapi-cloudevents.md): Read for Event-Driven/PubSub contracts. AsyncAPI + CloudEvents default, ADR exception path.
- [20-persistence-dapr-statestore.md](20-persistence-dapr-statestore.md): Read when persistence flows are added or changed. Dapr StateStore default with ADR exception path.
- [21-m2m-dapr-pubsub-decoupling.md](21-m2m-dapr-pubsub-decoupling.md): Read when broker publish/subscribe integrations are added or changed. Dapr Pub/Sub default with ADR exception path.
- [22-metrics-transport-standard.md](22-metrics-transport-standard.md): Read when telemetry export behavior changes. Defines OTLP-to-Collector transport rules and required telemetry resource attributes.
- [23-metrics-design-use-red.md](23-metrics-design-use-red.md): Read when metric semantics change. Covers naming, units, USE for bounded resources, and RED for request-driven interfaces.

## Task Entry Paths
- Feature/Bugfix core path: `02` -> `03` -> `04` -> `05` -> `10` -> `07`.
- If model/schema changes: add `08`.
- If public API changes: add `11`.
- If boundaries/integrations/ports/adapters change: add `12`.
- If container install/run workflows change: add `13`, `14`, `15`.
- If application logging behavior changes: add `17`.
- If Command/Reply M2M protocol changes: add `18`.
- If Event-Driven/PubSub contracts change: add `19`.
- If persistence flow is added/changed: add `20`.
- If event broker publish/subscribe integration changes: add `21`.
- If telemetry export/transport behavior changes: add `22`.
- If metric design changes (name/unit/USE/RED/histograms): add `23`.
- If AI executes a labeled task/finding: add `16`.
- If release activity is in scope: add `06`.
- For ADR/docs/comments/code comments: always add `09`.

## Context-Efficient Rule
Load only modules needed for the active task.

## Visual Overview
Governance map:
[docs/diagrams/0001-governance-mindmap.md](../diagrams/0001-governance-mindmap.md)
