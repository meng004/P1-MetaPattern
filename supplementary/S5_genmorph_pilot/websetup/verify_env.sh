#!/usr/bin/env bash
# verify_env.sh — sanity-check S5 aligned-pilot environment.
#
# Run after bootstrap.sh. Reports a checklist of green / red items.

set +e   # we want to keep going through all checks even if some fail

# Source env vars if not already
[[ -f "$HOME/.bashrc-genmorph" ]] && source "$HOME/.bashrc-genmorph"

PASS=0
FAIL=0
WARN=0

ok()    { echo "  ✓  $*"; PASS=$((PASS+1)); }
fail()  { echo "  ✗  $*"; FAIL=$((FAIL+1)); }
warn()  { echo "  ⚠  $*"; WARN=$((WARN+1)); }

echo "=== verify_env.sh ==="
echo ""

# ---------------------------------------------------------------------------
echo "[1] OS dependencies"
command -v java >/dev/null && ok "java in PATH ($(java -version 2>&1 | head -1))" || fail "java not in PATH"
command -v mvn >/dev/null && ok "mvn in PATH ($(mvn -version 2>&1 | head -1))"   || fail "mvn not in PATH"
command -v python3 >/dev/null && ok "python3 ($(python3 --version))"             || fail "python3 missing"
command -v unzip >/dev/null && ok "unzip available"                              || fail "unzip missing"
command -v wget >/dev/null && ok "wget available"                                || fail "wget missing"

# ---------------------------------------------------------------------------
echo ""
echo "[2] Java version paths"
[[ -d "${JAVA8:-}" ]] && ok "JAVA8 = $JAVA8"   || fail "JAVA8 not set or invalid"
[[ -d "${JAVA11:-}" ]] && ok "JAVA11 = $JAVA11" || fail "JAVA11 not set or invalid"
"${JAVA8}/bin/java" -version 2>&1 | grep -q "1.8" && ok "JDK 8 invocable" || warn "JDK 8 invocation: $($JAVA8/bin/java -version 2>&1 | head -1)"
"${JAVA11}/bin/java" -version 2>&1 | grep -q "11"  && ok "JDK 11 invocable" || warn "JDK 11 invocation: $($JAVA11/bin/java -version 2>&1 | head -1)"

# ---------------------------------------------------------------------------
echo ""
echo "[3] GenMorph Zenodo package"
GENMORPH_ROOT=/tmp/genmorph_pilot
[[ -d "$GENMORPH_ROOT" ]] && ok "$GENMORPH_ROOT exists" || fail "$GENMORPH_ROOT missing — re-run bootstrap.sh step 2"

REQUIRED=(
    "$GENMORPH_ROOT/genmorph_full/genmorph/build/libs/GAssert-1.0-SNAPSHOT-all.jar"
    "$GENMORPH_ROOT/genmorph_full/genmorph/pitest-wrapper-1.7.4.jar"
    "$GENMORPH_ROOT/genmorph_full/genmorph/randoop-all-4.3.0.jar"
    "$GENMORPH_ROOT/genmorph_full/genmorph/evosuite-1.1.0.jar"
    "$GENMORPH_ROOT/genmorph_full/genmorph/configs/math-sut/src/main/java/MathClass.java"
    "$GENMORPH_ROOT/genmorph_full/genmorph/scripts/run/genmorph.py"
    "$GENMORPH_ROOT/mrs/mrs/assertions_seed11/MathClass?gcd?0/MathClass?gcd?0@MR0.jir.txt"
    "$GENMORPH_ROOT/mrs/mrs/assertions_seed11/MathClass?sin?0/MathClass?sin?0@MR20.jir.txt"
    "$GENMORPH_ROOT/evaluation/evaluation/pitest_seed11/MathClass?gcd?0/mutants_killed.csv"
)
for f in "${REQUIRED[@]}"; do
    if [[ -f "$f" ]]; then
        ok "$(echo "$f" | sed "s|$GENMORPH_ROOT/||")"
    else
        fail "missing: $(echo "$f" | sed "s|$GENMORPH_ROOT/||")"
    fi
done

# ---------------------------------------------------------------------------
echo ""
echo "[4] Set N MR DSL files (ours)"
# Locate the websetup dir relative to this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PILOT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SET_N_FILES=(
    "$PILOT_ROOT/aligned/set_n_mrs/MathClass?gcd?0/MathClass?gcd?0@rho_perm.jir.txt"
    "$PILOT_ROOT/aligned/set_n_mrs/MathClass?gcd?0/MathClass?gcd?0@rho_perm.jor.txt"
    "$PILOT_ROOT/aligned/set_n_mrs/MathClass?gcd?0/MathClass?gcd?0@rho_scale.jir.txt"
    "$PILOT_ROOT/aligned/set_n_mrs/MathClass?gcd?0/MathClass?gcd?0@rho_eqref.jir.txt"
    "$PILOT_ROOT/aligned/set_n_mrs/MathClass?gcd?0/MathClass?gcd?0@rho_mono.jor.txt"
    "$PILOT_ROOT/aligned/set_n_mrs/MathClass?sin?0/MathClass?sin?0@rho_oddsym.jir.txt"
    "$PILOT_ROOT/aligned/set_n_mrs/MathClass?sin?0/MathClass?sin?0@rho_period.jir.txt"
    "$PILOT_ROOT/aligned/set_n_mrs/MathClass?sin?0/MathClass?sin?0@rho_complement.jir.txt"
    "$PILOT_ROOT/aligned/set_n_mrs/MathClass?sin?0/MathClass?sin?0@rho_bound.jor.txt"
)
for f in "${SET_N_FILES[@]}"; do
    if [[ -f "$f" ]]; then
        ok "$(basename "$f")"
    else
        fail "missing: $f"
    fi
done

# ---------------------------------------------------------------------------
echo ""
echo "[5] Python deps"
for pkg in pandas numpy scipy statsmodels; do
    if python3 -c "import $pkg" 2>/dev/null; then
        ok "python3 -c 'import $pkg' OK"
    else
        fail "python3 cannot import $pkg — pip install -r requirements.txt"
    fi
done

# ---------------------------------------------------------------------------
echo ""
echo "[6] GAssert evaluator self-check"
GASSERT_JAR="$GENMORPH_ROOT/genmorph_full/genmorph/build/libs/GAssert-1.0-SNAPSHOT-all.jar"
if [[ -f "$GASSERT_JAR" ]]; then
    USAGE=$("$JAVA11/bin/java" -cp "$GASSERT_JAR" ch.usi.gassert.EvaluateMRs 2>&1 | head -1 || true)
    if [[ "$USAGE" == *"Wrong number of parameters"* ]]; then
        ok "ch.usi.gassert.EvaluateMRs invocable (printed usage as expected)"
    else
        warn "EvaluateMRs invocation produced unexpected output: $USAGE"
    fi
else
    fail "GAssert jar not present"
fi

# ---------------------------------------------------------------------------
echo ""
echo "============================================="
echo "PASS:  $PASS"
echo "FAIL:  $FAIL"
echo "WARN:  $WARN"
echo "============================================="

if [[ $FAIL -eq 0 ]]; then
    echo ""
    echo "Environment is ready. Next: bash run_all.sh"
    exit 0
else
    echo ""
    echo "Environment is NOT ready. Fix failures above; re-run verify_env.sh."
    exit 1
fi
