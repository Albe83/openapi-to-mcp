#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

failures=0

fail() {
    echo "ERROR: $*"
    failures=$((failures + 1))
}

has_rg() {
    command -v rg >/dev/null 2>&1
}

match_file_pattern() {
    local pattern="$1"
    local file="$2"
    if has_rg; then
        rg -n -e "${pattern}" "${file}" >/dev/null
    else
        grep -Eq "${pattern}" "${file}"
    fi
}

check_policy_word_count() {
    local default_max_words=300
    local index_max_words=500
    local file base count max_words
    for file in docs/policies/*.md; do
        base="$(basename "${file}")"
        max_words="${default_max_words}"
        if [[ "${base}" == "01-index.md" ]]; then
            max_words="${index_max_words}"
        fi
        count="$(wc -w < "${file}" | tr -d ' ')"
        if ((count > max_words)); then
            fail "${file} exceeds ${max_words} words (${count})."
        fi
    done
}

check_policy_index_coverage() {
    local index_file="docs/policies/01-index.md"
    local file base
    for file in docs/policies/*.md; do
        base="$(basename "${file}")"
        if [[ "${base}" == "01-index.md" ]]; then
            continue
        fi
        if ! grep -Fq "${base}" "${index_file}"; then
            fail "${base} is not referenced in ${index_file}."
        fi
    done
}

check_markdown_links() {
    python3 - "${repo_root}" <<'PY'
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
patterns = [
    "AGENTS.md",
    "CONTRIBUTING.md",
    "README.md",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/*.yml",
    "docs/policies/*.md",
    "docs/adr/*.md",
    "docs/diagrams/*.md",
    "docs/interfaces/*.md",
    "docs/schemas/*.md",
    "Containerfiles/README.md",
]

files = []
for pattern in patterns:
    files.extend(root.glob(pattern))

link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
errors = []

for file_path in sorted({p.resolve() for p in files if p.exists()}):
    text = file_path.read_text(encoding="utf-8")
    rel_file = file_path.relative_to(root)
    for match in link_re.finditer(text):
        raw_link = match.group(1).strip()
        if not raw_link:
            continue
        if raw_link.startswith(("http://", "https://", "mailto:")):
            continue
        if raw_link.startswith("#"):
            continue
        if raw_link.startswith("<") and raw_link.endswith(">"):
            raw_link = raw_link[1:-1]

        normalized = raw_link.split("#", 1)[0].split("?", 1)[0].strip()
        if not normalized:
            continue

        target = (file_path.parent / normalized).resolve()
        if not target.exists():
            errors.append((str(rel_file), raw_link))

if errors:
    for rel_file, raw_link in errors:
        print(f"ERROR: broken link in {rel_file}: {raw_link}")
    raise SystemExit(1)
PY
}

check_container_native_isolation() {
    local file
    for file in Containerfiles/Containerfile*; do
        if match_file_pattern "python -m venv|virtualenv|/opt/venv/bin" "${file}"; then
            if ! match_file_pattern "policy15-exception" "${file}"; then
                fail "${file} uses nested env isolation without policy15 exception marker."
            fi
        fi
    done
}

check_normative_owner_phrases() {
    local rule owner phrase matches file
    local -a rules=(
        "docs/policies/17-logging-stdout-json.md|Application logs MUST be emitted to standard output"
        "docs/policies/18-m2m-protocol-selection.md|For Command/Reply communication, the default protocol MUST be REST API with a formal OpenAPI contract."
        "docs/policies/19-m2m-events-asyncapi-cloudevents.md|Event interfaces MUST be defined with AsyncAPI."
        "docs/policies/20-persistence-dapr-statestore.md|When possible, applications MUST decouple state persistence through Dapr StateStore."
        "docs/policies/21-m2m-dapr-pubsub-decoupling.md|When possible, applications MUST decouple message broker interactions through Dapr Pub/Sub."
        "docs/policies/22-metrics-transport-standard.md|All telemetry MUST be exported using OTLP to the platform-managed OpenTelemetry Collector."
        "docs/policies/23-metrics-design-use-red.md|For request-driven interfaces, RED metrics (Rate, Errors, Duration) MUST be implemented."
    )

    for rule in "${rules[@]}"; do
        owner="${rule%%|*}"
        phrase="${rule#*|}"
        matches=""
        for file in docs/policies/*.md; do
            if has_rg; then
                if rg -Fq -- "${phrase}" "${file}"; then
                    matches+="${file}"$'\n'
                fi
            else
                if grep -Fq -- "${phrase}" "${file}"; then
                    matches+="${file}"$'\n'
                fi
            fi
        done

        if [[ -z "${matches}" ]]; then
            fail "Owner phrase not found: ${owner}"
            continue
        fi

        while IFS= read -r file; do
            [[ -z "${file}" ]] && continue
            if [[ "${file}" != "${owner}" ]]; then
                fail "Normative phrase owned by ${owner} duplicated in ${file}."
            fi
        done <<< "${matches}"
    done
}

check_policy_word_count
check_policy_index_coverage
if ! check_markdown_links; then
    fail "Broken markdown links detected."
fi
check_container_native_isolation
check_normative_owner_phrases

if ((failures > 0)); then
    echo "Governance checks failed (${failures})."
    exit 1
fi

echo "Governance checks passed."
