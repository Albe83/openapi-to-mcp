# Governance Structure Mindmap

- Parent issue: N/A - governance documentation update
- ADR: N/A - policy-level governance overview
- Purpose: Visual overview of policy modules and governance flow.

```mermaid
mindmap
  root((Governance Model))
    Entry Points
      01 Index
        Read order and module selection
      00 Policy of Policies
        Word limit and single-owner rules
    Core Flow (feat/fix)
      02 Lifecycle
        Issue -> plan -> sub-issues
        task + basic/advanced labels
      03 Architecture First
        ADR + Class/Sequence diagrams
        Schema and conditional module links
      04 Testing and TDD
        Test-first and bug reproduction flow
        Lint evidence or N/A reason
      05 Git and PR
        Trunk-based workflow and naming
        Task-start branch guard
      10 Review and Findings
        Author + independent review
        One sub-issue per finding
      07 Compliance and DoD
        Merge gate and escalation
    Conditional Modules
      08 DDD
        Model/schema trigger
      11 Public API IDL
        API-change trigger
      12 Hexagonal Architecture
        Boundary/integration trigger
      17 Logging Stdout/JSON
        stdout required, JSON preferred
      18 M2M Command/Reply
        REST/OpenAPI default
        gRPC by ADR exception
      19 M2M Event Messaging
        AsyncAPI + CloudEvents default
        ADR exception path
      20 Persistence via Dapr StateStore
        Dapr StateStore default when possible
        ADR exception path
      21 M2M Dapr Pub/Sub Decoupling
        Dapr Pub/Sub default when possible
        ADR exception path
      22 Metrics Endpoint and USE
        Dedicated fetch endpoint
        OpenTelemetry semantics and USE model
      13 Container Build Rules
        Tool-agnostic build profiles
      14 Container RUN Mounts
        Cache/tmpfs isolation and compat fallback
      15 Container Native Isolation
        No nested env isolation by default
      16 AI Reasoning Level
        basic -> medium, advanced -> max
        Best-effort fallback when unsupported
      09 Simple English
        ADR/docs/comments language rule
    Release
      06 Versioning and Release
        SemVer and release rules
    Governance Automation
      CI Governance Job
        Policy word limit and index coverage
        Link checks and container isolation checks
        Owner-phrase duplicate guards for 17/18/19/20/21/22
```
