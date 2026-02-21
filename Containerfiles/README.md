# Container Build Guide

This directory defines OCI container build profiles for this repository.
The design is tool-agnostic and works with any compatible OCI builder/runner.

## Profiles
- `Containerfile.prod`: production runtime image (`mount` variant).
- `Containerfile.dev`: local development image (`mount` variant).
- `Containerfile.test`: lint and test image (`mount` variant).
- `Containerfile.<profile>.compat`: fallback variant without `RUN --mount`.

## Rules
- Keep files in `Containerfiles/` only.
- Use multi-stage builds to reduce final image size.
- Keep `prod` minimal: runtime deps only, non-root user, no shell tools unless required.
- Keep dependency install steps before app copy to improve cache reuse.
- Keep build context small with `.dockerignore` and `.containerignore`.
- Do not require one specific tool (Docker/Podman/Buildah/etc.).
- For mutating dependency steps, use mount isolation when builder supports it:
  - `type=cache` for cache directories.
  - `type=tmpfs` for temp/log directories.
- Use `.compat` only when mount syntax is not supported by the selected builder.

## Wrapper Scripts
Use repository wrappers to keep commands consistent:

```bash
./scripts/container-build.sh prod openapi-to-mcp:prod
./scripts/container-build.sh dev openapi-to-mcp:dev
./scripts/container-build.sh test openapi-to-mcp:test
```

Variant selection:

```bash
CONTAINERFILE_VARIANT=mount  ./scripts/container-build.sh prod openapi-to-mcp:prod
CONTAINERFILE_VARIANT=compat ./scripts/container-build.sh prod openapi-to-mcp:prod
```

Smoke and quality checks:

```bash
./scripts/container-test.sh smoke openapi-to-mcp:prod
./scripts/container-test.sh quality openapi-to-mcp:test
```

## Optional PIP Build Args
Keep defaults clean. Only inject PIP overrides when the environment requires them.

Use optional environment variables:
- `PIP_INSTALL_ARGS` for extra pip flags.
- `PIP_INDEX_URL` for custom index URL.
- `PIP_EXTRA_INDEX_URL` for additional index URL.

Example for environments with TLS interception:

```bash
PIP_INSTALL_ARGS="--trusted-host pypi.org --trusted-host files.pythonhosted.org" \
./scripts/container-build.sh prod openapi-to-mcp:prod
```

## Tool Selection
Override tool auto-detection when needed:

```bash
OCI_BUILDER=podman ./scripts/container-build.sh prod openapi-to-mcp:prod
OCI_RUNNER=nerdctl ./scripts/container-test.sh smoke openapi-to-mcp:prod
```

If your platform uses different commands, extend the wrapper scripts without changing the policy goals.
