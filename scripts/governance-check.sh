#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

failures=0

fail() {
    echo "ERROR: $*"
    failures=$((failures + 1))
}

check_policy_word_count() {
    local max_words=300
    local file count
    for file in docs/policies/*.md; do
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
        if rg -n -e "python -m venv|virtualenv|/opt/venv/bin" "${file}" >/dev/null; then
            if ! rg -n "policy15-exception" "${file}" >/dev/null; then
                fail "${file} uses nested env isolation without policy15 exception marker."
            fi
        fi
    done
}

check_policy_word_count
check_policy_index_coverage
if ! check_markdown_links; then
    fail "Broken markdown links detected."
fi
check_container_native_isolation

if ((failures > 0)); then
    echo "Governance checks failed (${failures})."
    exit 1
fi

echo "Governance checks passed."
