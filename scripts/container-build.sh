#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'USAGE'
Usage: scripts/container-build.sh <profile> <tag> [context]

Profiles:
  prod | dev | test

Environment:
  OCI_BUILDER  Optional. Force a specific OCI builder binary.
               If not set, auto-detects one of: docker, podman, nerdctl, buildah.
  CONTAINERFILE_VARIANT  Optional. Select containerfile variant:
                         - mount (default): uses RUN --mount enabled files.
                         - compat: fallback without RUN --mount.
  PIP_INSTALL_ARGS     Optional. Extra pip arguments passed as build arg.
  PIP_INDEX_URL        Optional. pip index URL passed as build arg.
  PIP_EXTRA_INDEX_URL  Optional. pip extra index URL passed as build arg.
USAGE
}

detect_builder() {
    if [[ -n "${OCI_BUILDER:-}" ]]; then
        echo "${OCI_BUILDER}"
        return 0
    fi

    for candidate in docker podman nerdctl buildah; do
        if command -v "${candidate}" >/dev/null 2>&1 && is_builder_usable "${candidate}"; then
            echo "${candidate}"
            return 0
        fi
    done

    return 1
}

is_builder_usable() {
    local candidate="$1"
    case "${candidate}" in
    docker | podman | nerdctl)
        "${candidate}" info >/dev/null 2>&1
        ;;
    buildah)
        "${candidate}" version >/dev/null 2>&1
        ;;
    *)
        return 1
        ;;
    esac
}

if [[ $# -lt 2 || $# -gt 3 ]]; then
    usage
    exit 1
fi

profile="$1"
tag="$2"
context="${3:-.}"
variant="${CONTAINERFILE_VARIANT:-mount}"

case "${profile}" in
prod | dev | test) ;;
*)
    echo "Unsupported profile: ${profile}" >&2
    usage
    exit 1
    ;;
esac

containerfile="Containerfiles/Containerfile.${profile}"
if [[ "${variant}" == "compat" ]]; then
    containerfile="Containerfiles/Containerfile.${profile}.compat"
elif [[ "${variant}" != "mount" ]]; then
    echo "Unsupported CONTAINERFILE_VARIANT '${variant}'. Supported: mount, compat." >&2
    exit 1
fi

if [[ ! -f "${containerfile}" ]]; then
    echo "Missing containerfile: ${containerfile}" >&2
    exit 1
fi

builder="$(detect_builder || true)"
if [[ -z "${builder}" ]]; then
    echo "No usable OCI builder found. Set OCI_BUILDER or install/start docker/podman/nerdctl/buildah." >&2
    exit 1
fi

build_args=()
if [[ -n "${PIP_INSTALL_ARGS:-}" ]]; then
    build_args+=(--build-arg "PIP_INSTALL_ARGS=${PIP_INSTALL_ARGS}")
fi
if [[ -n "${PIP_INDEX_URL:-}" ]]; then
    build_args+=(--build-arg "PIP_INDEX_URL=${PIP_INDEX_URL}")
fi
if [[ -n "${PIP_EXTRA_INDEX_URL:-}" ]]; then
    build_args+=(--build-arg "PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL}")
fi

echo "Using builder: ${builder}"
echo "Profile: ${profile}"
echo "Variant: ${variant}"
echo "Tag: ${tag}"
echo "Context: ${context}"
if [[ ${#build_args[@]} -gt 0 ]]; then
    echo "Optional PIP build args enabled."
fi

case "${builder}" in
docker | podman | nerdctl)
    exec "${builder}" build "${build_args[@]}" -f "${containerfile}" -t "${tag}" "${context}"
    ;;
buildah)
    exec "${builder}" bud "${build_args[@]}" -f "${containerfile}" -t "${tag}" "${context}"
    ;;
*)
    echo "Unsupported OCI_BUILDER '${builder}'. Supported: docker, podman, nerdctl, buildah." >&2
    exit 1
    ;;
esac
