#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'USAGE'
Usage:
  scripts/container-test.sh smoke <image> [host-port]
  scripts/container-test.sh quality <image> [command...]

Modes:
  smoke    Run image, wait for /healthz, and fail if healthcheck does not pass.
  quality  Run test/lint command inside image (default: image CMD).

Environment:
  OCI_RUNNER  Optional. Force a specific OCI runner binary.
              If not set, auto-detects one of: docker, podman, nerdctl.
USAGE
}

detect_runner() {
    if [[ -n "${OCI_RUNNER:-}" ]]; then
        echo "${OCI_RUNNER}"
        return 0
    fi

    for candidate in docker podman nerdctl; do
        if command -v "${candidate}" >/dev/null 2>&1 && is_runner_usable "${candidate}"; then
            echo "${candidate}"
            return 0
        fi
    done

    return 1
}

is_runner_usable() {
    local candidate="$1"
    case "${candidate}" in
    docker | podman | nerdctl)
        "${candidate}" info >/dev/null 2>&1
        ;;
    *)
        return 1
        ;;
    esac
}

detect_python() {
    if command -v python3 >/dev/null 2>&1; then
        echo "python3"
        return 0
    fi

    if command -v python >/dev/null 2>&1; then
        echo "python"
        return 0
    fi

    return 1
}

if [[ $# -lt 2 ]]; then
    usage
    exit 1
fi

mode="$1"
image="$2"
shift 2

runner="$(detect_runner || true)"
if [[ -z "${runner}" ]]; then
    echo "No usable OCI runner found. Set OCI_RUNNER or install/start docker/podman/nerdctl." >&2
    exit 1
fi

case "${mode}" in
smoke)
    pybin="$(detect_python || true)"
    if [[ -z "${pybin}" ]]; then
        echo "Python is required on host for smoke checks (python3 or python)." >&2
        exit 1
    fi

    port="${1:-18080}"
    url="http://127.0.0.1:${port}/healthz"

    echo "Using runner: ${runner}"
    echo "Starting smoke container from image: ${image}"
    cid="$("${runner}" run -d -p "${port}:8080" "${image}")"

    cleanup() {
        "${runner}" rm -f "${cid}" >/dev/null 2>&1 || true
    }
    trap cleanup EXIT

    for _ in $(seq 1 30); do
        if "${pybin}" - "${url}" <<'PY'
import sys
import urllib.error
import urllib.request

url = sys.argv[1]
try:
    with urllib.request.urlopen(url, timeout=1) as response:
        raise SystemExit(0 if response.status == 200 else 1)
except (urllib.error.URLError, TimeoutError, ConnectionError):
    raise SystemExit(1)
PY
        then
            echo "Smoke check passed: ${url}"
            exit 0
        fi
        sleep 1
    done

    echo "Smoke check failed: ${url}" >&2
    exit 1
    ;;
quality)
    echo "Using runner: ${runner}"
    if [[ $# -gt 0 ]]; then
        exec "${runner}" run --rm "${image}" "$@"
    fi
    exec "${runner}" run --rm "${image}"
    ;;
*)
    echo "Unsupported mode: ${mode}" >&2
    usage
    exit 1
    ;;
esac
