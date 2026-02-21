#!/usr/bin/env bash
set -euo pipefail

event_name="${GITHUB_EVENT_NAME:-}"
if [[ "${event_name}" != "pull_request" && "${event_name}" != "pull_request_target" ]]; then
    echo "PR traceability check skipped: event is '${event_name:-unknown}'."
    exit 0
fi

pr_title="${PR_TITLE:-}"
pr_body="${PR_BODY:-}"

if [[ -z "${pr_title}" && -z "${pr_body}" ]]; then
    echo "ERROR: PR metadata is empty; cannot validate traceability." >&2
    exit 1
fi

extract_line() {
    local pattern="$1"
    printf '%s\n' "${pr_body}" | awk -v p="${pattern}" 'tolower($0) ~ tolower(p) {print; exit}'
}

detect_change_type() {
    local body_line title_prefix value
    body_line="$(extract_line "change type:")"
    if [[ -n "${body_line}" ]]; then
        value="${body_line#*:}"
        value="$(printf '%s' "${value}" | tr '[:upper:]' '[:lower:]' | xargs)"
        value="${value%%/*}"
        value="$(printf '%s' "${value}" | xargs)"
        if [[ -n "${value}" ]]; then
            printf '%s\n' "${value}"
            return
        fi
    fi

    title_prefix="${pr_title%%:*}"
    title_prefix="$(printf '%s' "${title_prefix}" | tr '[:upper:]' '[:lower:]' | xargs)"
    printf '%s\n' "${title_prefix}"
}

change_type="$(detect_change_type)"

if [[ "${change_type}" != "feat" && "${change_type}" != "fix" ]]; then
    echo "PR traceability check skipped: change type '${change_type:-unknown}' is not feat/fix."
    exit 0
fi

failures=0
fail() {
    echo "ERROR: $*" >&2
    failures=$((failures + 1))
}

parent_line="$(extract_line "parent issue:")"
subissues_line="$(extract_line "sub-issues:")"
analysis_line="$(extract_line "functional analysis issue")"
plan_line="$(extract_line "operational plan comment")"

if [[ ! "${parent_line}" =~ \#[0-9]+ ]]; then
    fail "Parent issue is required for feat/fix PRs."
fi

if [[ ! "${subissues_line}" =~ \#[0-9]+ ]]; then
    fail "At least one sub-issue link is required for feat/fix PRs."
fi

if [[ ! "${analysis_line}" =~ \#[0-9]+ ]]; then
    fail "Functional analysis issue link is required for feat/fix PRs."
fi

if [[ ! "${plan_line}" =~ issuecomment-[0-9]+ ]]; then
    fail "Operational plan comment permalink is required for feat/fix PRs."
fi

if ((failures > 0)); then
    echo "PR traceability check failed (${failures})." >&2
    exit 1
fi

echo "PR traceability check passed."
