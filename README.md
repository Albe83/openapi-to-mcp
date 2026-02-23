# OpenAPI to MCP

OpenAPI to MCP exposes a generic REST API as MCP tools for AI agents.
At startup, the server loads an OpenAPI specification, validates it, maps operations, and registers tools.
The main runtime target is HTTP-Streamable MCP.

## Current Implementation Status
This repository now includes a working Python technical foundation:
- FastAPI application bootstrap.
- OpenAPI source loading from file path or URL.
- Critical OpenAPI validation with warning support for non-critical gaps.
- Operation mapping and MCP tool generation (`operationId` first, deterministic fallback).
- Health endpoint (`GET /healthz`).
- OTLP telemetry export with OpenTelemetry SDK instrumentation.
- Optional Prometheus-compatible metrics endpoint (`GET /metrics`) behind feature toggle.
- Local fallback MCP endpoint (`POST /mcp`) when FastMCP is not available.

Architecture and governance artifacts:
- ADR: [docs/adr/0001-python-fastapi-fastmcp-bootstrap.md](docs/adr/0001-python-fastapi-fastmcp-bootstrap.md)
- Diagrams: [docs/diagrams/](docs/diagrams)
- Public API IDL: [docs/interfaces/0001-openapi-to-mcp-server-openapi.yaml](docs/interfaces/0001-openapi-to-mcp-server-openapi.yaml)

## Requirements
- Python 3.11+
- pip
- Optional for native MCP transport: `mcp` package (`pip install -e .[mcp]`)

## Configuration
Set at least one source:
- `OPENAPI_SPEC_PATH=/path/to/openapi.yaml`
- `OPENAPI_SPEC_URL=https://example.com/openapi.yaml`

Optional:
- `MCP_HOST` (default `0.0.0.0`)
- `MCP_PORT` (default `8080`)
- `LOG_LEVEL` (default `info`)
- `HTTP_MAX_IN_FLIGHT` (default `128`)
- `HTTP_MAX_CONNECTIONS` (default `100`)
- `HTTP_MAX_KEEPALIVE_CONNECTIONS` (default `20`)
- `TELEMETRY_OTLP_PROTOCOL` (`grpc` default, `http` fallback)
- `TELEMETRY_OTLP_ENDPOINT` (default `http://127.0.0.1:4317` for `grpc`)
- `TELEMETRY_EXPORT_INTERVAL_MS` (default `60000`)
- `PROMETHEUS_METRICS_ENABLED` (`false` default; when `true`, enables `GET /metrics`)
- `SERVICE_NAME` (default `openapi-to-mcp`)
- `SERVICE_NAMESPACE` (default `openapi-to-mcp`)
- `DEPLOYMENT_ENVIRONMENT` (default `dev`)

OpenAPI runtime rule:
- Each operation must resolve a server URL from `servers` declared at operation, path, or root level.

## Run Locally
```bash
python3.11 -m pip install -e .[dev]
OPENAPI_SPEC_PATH=tests/fixtures/sample-openapi.yaml python3.11 -m openapi_to_mcp.main
```

## Build, Test, Lint
```bash
make test
make lint
```

Or directly:
```bash
python3.11 -m pytest -q
python3.11 -m ruff check src tests
```

## Container Builds (Tool-Agnostic OCI)
Build container profiles with repository wrappers:

```bash
make container-build-all
```

Run smoke and quality checks:

```bash
make container-smoke-prod
make container-quality-test
```

Override auto-detection when needed:

```bash
OCI_BUILDER=podman ./scripts/container-build.sh prod openapi-to-mcp:prod
OCI_RUNNER=nerdctl ./scripts/container-test.sh smoke openapi-to-mcp:prod
```

Select variant (`mount` default, `compat` fallback when mount is unsupported):

```bash
CONTAINERFILE_VARIANT=mount ./scripts/container-build.sh prod openapi-to-mcp:prod
CONTAINERFILE_VARIANT=compat ./scripts/container-build.sh prod openapi-to-mcp:prod
```

With `make`:

```bash
make CONTAINERFILE_VARIANT=compat container-build-prod
```

Optional PIP build args (only when needed by your environment):

```bash
PIP_INSTALL_ARGS="--trusted-host pypi.org --trusted-host files.pythonhosted.org" \
./scripts/container-build.sh prod openapi-to-mcp:prod
```

Container isolation rule:
- Container images use the container itself as the isolation boundary.
- Do not add nested env layers (for example `venv`) unless a technical exception is required and documented.

Detailed rules and profile intent: [Containerfiles/README.md](Containerfiles/README.md)

Governance checks:

```bash
make governance-check
```

## GitHub Pipelines
This repository uses GitHub Actions with dedicated workflows:
- Governance: [`.github/workflows/governance.yml`](.github/workflows/governance.yml)
  - Runs governance consistency checks on PRs and `main`.
- CI: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)
  - Runs lint/test plus container build/quality/smoke verification.
- Security: [`.github/workflows/security.yml`](.github/workflows/security.yml)
  - Runs CodeQL and Trivy scans (filesystem + container image).
- Release: [`.github/workflows/release.yml`](.github/workflows/release.yml)
  - Runs on SemVer tags, publishes image to GHCR, scans image, creates GitHub Release.
  - Enforces public visibility for the GHCR package before publishing the GitHub Release.

Release trigger examples:
```bash
cat > /tmp/release-v0.3.1.md <<'EOF'
## Summary
- Short release summary.

## Added
- New features.

## Changed
- Behavior updates.

## Fixed
- Bug fixes.

## Breaking Changes
- None

## Migration Notes
- None

## References
- #123
- #124
EOF

git tag -a v0.3.1 -F /tmp/release-v0.3.1.md
git push origin v0.3.1
```

Release notes must include the required changelog sections defined by [docs/policies/06-versioning-release.md](docs/policies/06-versioning-release.md).

GHCR visibility prerequisite:
- Set package visibility to `public` in GitHub Package settings before release.
- If visibility is `private`, the release workflow fails with a direct settings link.

## Project Structure
- `src/openapi_to_mcp/` core implementation
- `tests/` unit and integration tests
- `Containerfiles/` OCI container build profiles
- `scripts/` automation wrappers (including OCI build/run wrappers)
- `docs/adr/` architecture decisions
- `docs/diagrams/` Mermaid architecture diagrams
- `docs/interfaces/` public API IDL contracts
- `docs/policies/` contribution and governance rules

## Versioning
Releases follow SemVer (`vMAJOR.MINOR.PATCH`).
Detailed rules: [docs/policies/06-versioning-release.md](docs/policies/06-versioning-release.md)

## Logging Policy
Application logging rules are defined in [docs/policies/17-logging-stdout-json.md](docs/policies/17-logging-stdout-json.md):
- logs to `stdout` are mandatory,
- single-line JSON is preferred,
- `stderr` is reserved for critical/fatal errors.

## M2M Protocol Selection Policy
Protocol selection rules for machine-to-machine communication are defined in [docs/policies/18-m2m-protocol-selection.md](docs/policies/18-m2m-protocol-selection.md).

## M2M Event Messaging Policy
Event-Driven and Pub/Sub governance rules are defined in [docs/policies/19-m2m-events-asyncapi-cloudevents.md](docs/policies/19-m2m-events-asyncapi-cloudevents.md).

## Metrics and Telemetry Transport Policy
Telemetry export and transport rules are defined in [docs/policies/22-metrics-transport-standard.md](docs/policies/22-metrics-transport-standard.md).
Current runtime exports metrics via OTLP to a Collector target configured through environment variables.
Prometheus-compatible scraping is optional and disabled by default (`PROMETHEUS_METRICS_ENABLED=false`).

## Metrics Design Policy
Metrics semantic design rules (naming, units, USE, RED, and latency histograms) are defined in [docs/policies/23-metrics-design-use-red.md](docs/policies/23-metrics-design-use-red.md).
