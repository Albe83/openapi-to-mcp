# Architecture-First Policy

Policy Owner: Engineering Maintainers

Architecture artifacts are required before feature/bugfix implementation.

## Required Artifacts
- At least one ADR in `docs/adr/`.
- One Class Diagram in Markdown Mermaid in `docs/diagrams/`.
- One Sequence Diagram in Markdown Mermaid in `docs/diagrams/`.
- ADR must link required diagram files in `docs/diagrams/`.
- If data model changes: JSON Schema in `docs/schemas/`.
- If public API changes: IDL contract in `docs/interfaces/`.

## Diagram as Code Rule
- Diagrams are code in Markdown files under `docs/diagrams/`.
- Use fenced ` ```mermaid ` blocks.
- Required diagrams cannot use `.mmd`.
- Diagrams must render directly in GitHub UI.
- Each diagram file must include parent issue and ADR references.

## Required Content
- ADR: context, decision, alternatives, consequences, issue/sub-issue links, class/sequence diagram file links.
- Diagram files: title, purpose, parent issue, ADR reference.
- If data model changes: schema entities align with the Class Diagram.
- If data model/schema changes: apply `08`; if boundaries/ports/adapters change, apply `12`.
- If public API changes: apply `11-public-api-idl.md`.
- Prefer YAML schemas; JSON allowed when needed.

## Execution Rule
Implementation starts by analyzing ADR plus linked class and sequence diagrams.
Code changes must derive from these decisions.

## Traceability
Sub-issues and PRs link parent issue, ADR(s), diagram files, and schema/IDL files.

## Change Rule
If architecture decisions change during delivery:
1. Update ADR and diagram files first.
2. Update issue/PR context.
3. Resume implementation only after alignment.

## Non-Compliant
- No ADR before coding.
- Missing class or sequence diagram file in `docs/diagrams/`.
- Diagram file not written as Markdown Mermaid.
- ADR missing links to required diagram files.
- Data model changed without JSON Schema update.
- Public API changed without IDL update.
- PR missing required architecture links.
- Code changes without architecture links in PR.
