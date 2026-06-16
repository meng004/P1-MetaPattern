#!/usr/bin/env bash
# tests/run.sh — repo's test gate (rule 6: no merge without tests)
#
# Runs all Python smoke tests and the secret-leak grep check.
# Exit 0 = green, exit non-zero = stop the merge.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "=== tests/run.sh — S5 aligned experiment test gate ==="

fail=0

run_test() {
    local label="$1"; shift
    if "$@"; then
        echo "  PASS  $label"
    else
        echo "  FAIL  $label"
        fail=$((fail + 1))
    fi
}

# 1. Python unit tests
echo ""
echo "--- Python tests ---"
run_test "test_generate_mrs"     python3 tests/test_generate_mrs.py
run_test "test_parse_results"    python3 tests/test_parse_results.py
run_test "test_aggregate_metrics" python3 tests/test_aggregate_metrics.py
run_test "test_setn_followups"   python3 tests/test_setn_followups.py
run_test "test_setn_e2e"         python3 tests/test_setn_e2e.py

# 1a. Shell syntax check for orchestration scripts
echo ""
echo "--- Shell syntax (bash -n) ---"
run_test "setup.sh syntax"          bash -n setup.sh
run_test "scripts/run_all.sh syntax" bash -n scripts/run_all.sh
run_test "tests/run.sh syntax"      bash -n tests/run.sh

# 2. Secret/path leak grep (rule 7)
# Pattern requires actual path/token characters (alphanum + underscore/dot/dash);
# documentation that uses placeholders like /Users/<name>/... is correctly skipped.
# Self-references (this script, CLAUDE.md) are excluded so the doc-of-the-rule
# does not trip the check on itself.
echo ""
echo "--- Secret/path leak grep (rule 7) ---"
LEAK=$(grep -rIn -E "(/Users/[A-Za-z0-9._-]+/[A-Za-z0-9._-]+|sk-[A-Za-z0-9]{20,}|Bearer[[:space:]]+[A-Za-z0-9._-]{20,}|(api_key|API_KEY)[[:space:]]*=[[:space:]]*['\"][A-Za-z0-9._-]{8,}['\"])" \
    --include="*.py" --include="*.sh" --include="*.md" --include="*.txt" --include="*.json" --include="*.yaml" --include=".env*" \
    --exclude-dir=.git --exclude-dir=tests/fixtures --exclude-dir=results \
    --exclude="run.sh" --exclude="CLAUDE.md" \
    . 2>/dev/null || true)
if [[ -z "$LEAK" ]]; then
    echo "  PASS  no leaked secrets / personal absolute paths"
else
    echo "  FAIL  leaked content:"
    echo "$LEAK" | head -10 | sed 's/^/        /'
    fail=$((fail + 1))
fi

# 3. Generator output schema check
echo ""
echo "--- Generator output schema ---"
EXPECTED_SUBJECTS=23
EXPECTED_FILES=142
n_sub=$(ls set_n_mrs/ 2>/dev/null | wc -l | tr -d ' ')
n_files=$(find set_n_mrs -name "*.txt" 2>/dev/null | wc -l | tr -d ' ')
if [[ "$n_sub" -eq "$EXPECTED_SUBJECTS" ]]; then
    echo "  PASS  set_n_mrs has $n_sub subjects (expected $EXPECTED_SUBJECTS)"
else
    echo "  FAIL  set_n_mrs has $n_sub subjects, expected $EXPECTED_SUBJECTS"
    fail=$((fail + 1))
fi
if [[ "$n_files" -eq "$EXPECTED_FILES" ]]; then
    echo "  PASS  set_n_mrs has $n_files DSL files (expected $EXPECTED_FILES)"
else
    echo "  FAIL  set_n_mrs has $n_files DSL files, expected $EXPECTED_FILES"
    fail=$((fail + 1))
fi

echo ""
if [[ $fail -eq 0 ]]; then
    echo "=== ALL GREEN ==="
    exit 0
else
    echo "=== $fail FAILURE(S) ==="
    exit 1
fi
