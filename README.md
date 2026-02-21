# OpenAPI to MCP

## Project Goal
OpenAPI to MCP exposes a generic REST API as MCP tools for AI agents.
At startup, the server loads an OpenAPI specification and generates MCP tools from API operations.
The runtime model is container-first, with Kubernetes as the primary deployment target.
Main transport is HTTP-Streamable.

## How It Works
1. Start the MCP server.
2. Load an OpenAPI spec (local file or URL).
3. Generate MCP tools from operations.
4. Serve tools to agents via HTTP-Streamable MCP.

## Key Features
- Dynamic tool generation from OpenAPI definitions.
- Generic bridge between REST backends and MCP agents.
- Containerized runtime design.
- Kubernetes-oriented deployment model.
- HTTP-Streamable-first integration path.

## Architecture Overview
- OpenAPI Loader: reads and validates the spec.
- Tool Generator: maps operations into MCP tool contracts.
- MCP Transport Layer: exposes tools through MCP protocol semantics.
- HTTP-Streamable Interface: provides transport endpoints for clients.

## Configuration
Runtime configuration is environment-variable based.

| Variable | Required | Default | Description | Example |
| --- | --- | --- | --- | --- |
| `OPENAPI_SPEC_PATH` | No* | `""` | Local OpenAPI file path. | `/app/specs/petstore.yaml` |
| `OPENAPI_SPEC_URL` | No* | `""` | Remote OpenAPI URL. | `https://api.example.com/openapi.json` |
| `MCP_TRANSPORT` | No | `http-streamable` | MCP transport mode. | `http-streamable` |
| `MCP_HOST` | No | `0.0.0.0` | Bind host. | `0.0.0.0` |
| `MCP_PORT` | No | `8080` | Listening port. | `8080` |
| `LOG_LEVEL` | No | `info` | Log verbosity. | `debug` |

\* Set at least one of `OPENAPI_SPEC_PATH` or `OPENAPI_SPEC_URL`.

## Quickstart
1. Provide an OpenAPI spec.
2. Run the container with the required environment variables.
3. Expose server port `MCP_PORT`.
4. Connect an AI agent to the HTTP-Streamable MCP endpoint and verify tool discovery.

## Deployment on Kubernetes
Recommended pattern:
- `Deployment` for server replicas.
- `Service` for network exposure.
- `ConfigMap` for non-sensitive settings.
- `Secret` for sensitive values (if/when auth is enabled).
- Optional `Ingress` or API gateway for external access.

## Versioning
Release versions follow Semantic Versioning (`SemVer 2.0.0`) using tags in the format `vMAJOR.MINOR.PATCH` (for example, `v1.2.0`).
Pre-release tags are supported (`-alpha.N`, `-beta.N`, `-rc.N`).
Full release and bump policy is defined in [docs/policies/06-versioning-release.md](docs/policies/06-versioning-release.md).

## Contribution Workflow
Contribution rules are modular to keep policy files short and AI-friendly.
Use [CONTRIBUTING.md](CONTRIBUTING.md) as entrypoint, then follow [docs/policies/01-index.md](docs/policies/01-index.md).
For feature/bugfix work, the mandatory sequence is lifecycle -> architecture-first -> TDD -> git/PR -> compliance modules.

## Current Status
The repository is in bootstrap phase and currently contains no production code, container build files, or Kubernetes manifests.
This README defines the target architecture and operating model.

## Roadmap
- Stronger OpenAPI validation and error reporting.
- Authentication and authorization support.
- Observability (metrics, tracing, structured logs).
- Tool metadata enrichment and caching.
