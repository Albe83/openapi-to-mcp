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

trim() {
    local value="$1"
    value="${value#"${value%%[![:space:]]*}"}"
    value="${value%"${value##*[![:space:]]}"}"
    printf '%s' "${value}"
}

normalize_value() {
    local value
    value="${1//\`/}"
    value="$(printf '%s' "${value}" | tr '[:upper:]' '[:lower:]' | xargs)"
    printf '%s' "${value}"
}

extract_value_after_colon() {
    local line="$1"
    if [[ "${line}" == *:* ]]; then
        line="${line#*:}"
    fi
    printf '%s' "${line}"
}

is_valid_na_reason() {
    local value
    value="$(normalize_value "$1")"
    [[ "${value}" =~ ^n/?a[[:space:]]*-[[:space:]]+.+$ ]]
}

extract_compliance_row() {
    local module="$1"
    printf '%s\n' "${pr_body}" | awk -F'|' -v module="${module}" '
    function trim_cell(s) { gsub(/^[ \t\r\n]+|[ \t\r\n]+$/, "", s); return s }
    BEGIN { IGNORECASE=1; in_section=0; in_table=0 }
    /^##[[:space:]]+/ {
        line=tolower($0)
        if (line ~ /^##[[:space:]]*compliance map[[:space:]]*\(owner modules\)[[:space:]]*$/ ||
            line ~ /^##[[:space:]]*compliance map[[:space:]]*$/) {
            in_section=1
            in_table=0
            next
        }
        if (in_section) {
            exit
        }
    }
    {
        if (!in_section || $0 !~ /^\|/) {
            next
        }
        c1=trim_cell($2)
        c2=trim_cell($3)
        c3=trim_cell($4)
        c4=trim_cell($5)
        c1_lower=tolower(c1)
        c2_lower=tolower(c2)
        if (c1_lower=="module" && c2_lower=="applies") {
            in_table=1
            next
        }
        if (!in_table) {
            next
        }
        if (c1==module) {
            print c1 "\t" c2 "\t" c3 "\t" c4
            exit
        }
    }'
}

count_populated_finding_rows() {
    printf '%s\n' "${pr_body}" | awk -F'|' '
    function trim_cell(s) { gsub(/^[ \t\r\n]+|[ \t\r\n]+$/, "", s); return s }
    BEGIN { IGNORECASE=1; in_section=0; in_table=0; count=0 }
    /^##[[:space:]]+/ {
        line=tolower($0)
        if (line ~ /^##[[:space:]]*review findings[[:space:]]*\(mandatory\)[[:space:]]*$/ ||
            line ~ /^##[[:space:]]*review findings[[:space:]]*$/) {
            in_section=1
            in_table=0
            next
        }
        if (in_section) {
            in_section=0
            in_table=0
        }
    }
    {
        if (!in_section || $0 !~ /^\|/) {
            next
        }
        c1=trim_cell($2)
        c2=trim_cell($3)
        c3=trim_cell($4)
        c4=trim_cell($5)
        c1_lower=tolower(c1)
        c2_lower=tolower(c2)
        c3_lower=tolower(c3)
        c4_lower=tolower(c4)
        if (c1_lower=="finding" && c2_lower=="category" && c3_lower=="priority" && c4_lower=="sub-issue") {
            in_table=1
            next
        }
        if (!in_table) {
            next
        }
        if (c1_lower ~ /^-+$/ && c2_lower ~ /^-+$/ && c3_lower ~ /^-+$/ && c4_lower ~ /^-+$/) {
            next
        }
        if (c1 == "" && c2 == "" && c3 == "" && c4 == "") {
            next
        }
        if (c1 != "" && c4 != "") {
            count++
        }
    }
    END { print count }'
}

has_explicit_no_findings_statement() {
    printf '%s\n' "${pr_body}" | awk '
    function trim_line(s) { gsub(/^[ \t\r\n]+|[ \t\r\n]+$/, "", s); return s }
    BEGIN { IGNORECASE=1; found=0 }
    {
        line=tolower(trim_line($0))
        if (line ~ /^[-*]?[[:space:]]*`?no findings`?[[:space:]]*$/) {
            found=1
            exit
        }
    }
    END { exit(found ? 0 : 1) }'
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

validate_compliance_baseline_row() {
    local module="$1"
    local row module_cell applies evidence na_reason
    local applies_normalized evidence_trimmed na_reason_trimmed

    row="$(extract_compliance_row "${module}")"
    if [[ -z "${row}" ]]; then
        fail "Compliance map row '${module}' is required for feat/fix PRs."
        return
    fi

    module_cell="$(printf '%s' "${row}" | cut -f1)"
    applies="$(printf '%s' "${row}" | cut -f2)"
    evidence="$(printf '%s' "${row}" | cut -f3)"
    na_reason="$(printf '%s' "${row}" | cut -f4-)"
    applies_normalized="$(normalize_value "${applies}")"
    evidence_trimmed="$(trim "${evidence//\`/}")"
    na_reason_trimmed="$(trim "${na_reason//\`/}")"

    if [[ "${applies_normalized}" != "yes" && "${applies_normalized}" != "no" ]]; then
        fail "Compliance map row '${module}' must set Applies to 'yes' or 'no'."
        return
    fi

    if [[ -z "${evidence_trimmed}" && -z "${na_reason_trimmed}" ]]; then
        fail "Compliance map row '${module}' must include evidence or an N/A reason."
    fi

    if [[ "${applies_normalized}" == "yes" && -z "${evidence_trimmed}" ]]; then
        fail "Compliance map row '${module}' has Applies='yes' but missing evidence."
    fi

    if [[ "${applies_normalized}" == "no" ]]; then
        if [[ -z "${na_reason_trimmed}" ]]; then
            fail "Compliance map row '${module}' has Applies='no' but missing N/A reason."
        elif ! is_valid_na_reason "${na_reason_trimmed}"; then
            fail "Compliance map row '${module}' N/A reason must use 'N/A - <reason>'."
        fi
    fi
}

parent_line="$(extract_line "parent issue:")"
subissues_line="$(extract_line "sub-issues:")"
analysis_line="$(extract_line "functional analysis issue")"
plan_line="$(extract_line "operational plan comment")"
author_review_line="$(extract_line "author self-review completed:")"
independent_review_line="$(extract_line "independent review completed:")"
findings_outcome_line="$(extract_line "findings outcome:")"

author_review_value="$(normalize_value "$(extract_value_after_colon "${author_review_line}")")"
independent_review_value="$(normalize_value "$(extract_value_after_colon "${independent_review_line}")")"
findings_outcome_value="$(normalize_value "$(extract_value_after_colon "${findings_outcome_line}")")"

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

for module in 02 03 04 05 07 10; do
    validate_compliance_baseline_row "${module}"
done

if [[ "${author_review_value}" != "yes" ]]; then
    fail "Author self-review must be marked 'yes' for feat/fix PRs."
fi

if [[ "${independent_review_value}" != "yes" ]]; then
    fail "Independent review must be marked 'yes' for feat/fix PRs."
fi

if [[ "${findings_outcome_value}" != "no findings" && "${findings_outcome_value}" != "findings listed" ]]; then
    fail "Findings outcome must be 'no findings' or 'findings listed'."
elif [[ "${findings_outcome_value}" == "no findings" ]]; then
    if ! has_explicit_no_findings_statement; then
        fail "Findings outcome is 'no findings' but explicit 'no findings' statement is missing."
    fi
else
    populated_finding_rows="$(count_populated_finding_rows)"
    if [[ "${populated_finding_rows}" -lt 1 ]]; then
        fail "Findings outcome is 'findings listed' but no populated finding table row was found."
    fi
fi

if ((failures > 0)); then
    echo "PR traceability check failed (${failures})." >&2
    exit 1
fi

echo "PR traceability check passed."
