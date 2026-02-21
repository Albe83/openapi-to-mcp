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

Detailed rules and profile intent: [Containerfiles/README.md](Containerfiles/README.md)

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
