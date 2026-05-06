#!/usr/bin/env bash
# Aligned S5 — full controlled pipeline orchestrator (codex skeleton).
#
# This script executes the 4-stage aligned experiment:
#   Stage 1: reproduce upstream's Randoop+EvoSuite+PIT state captures
#   Stage 2: copy our Set N .jir/.jor files into upstream's MR directory
#   Stage 3: invoke ch.usi.gassert.EvaluateMRs once on combined MR set
#   Stage 4: parse output mutants_killed.csv and compute aligned metrics
#
# Usage:
#   bash run_aligned_pipeline.sh <subject> <seed>
#
# Example:
#   bash run_aligned_pipeline.sh 'MathClass?gcd?0' 11
#   bash run_aligned_pipeline.sh 'MathClass?sin?0' 11
#
# Stage 1 may take 5-15 minutes per (subject, seed) depending on
# Randoop / EvoSuite time budgets. Stages 2-4 take seconds.

set -euo pipefail

SUBJECT="${1:-MathClass?gcd?0}"
SEED="${2:-11}"

# === Environment ===
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@11}"
export PATH="$JAVA_HOME/bin:$PATH"

GENMORPH=/tmp/genmorph_pilot/genmorph_full/genmorph
ALIGNED_DIR="$(cd "$(dirname "$0")" && pwd)"
GASSERT_JAR="$GENMORPH/build/libs/GAssert-1.0-SNAPSHOT-all.jar"

# Where upstream's pipeline writes its state captures.
# Note: paths come from $GENMORPH/configs/evaluation-config-math.json:
#   output_dir_math/states_seed{seed}/...
UPSTREAM_OUT="$GENMORPH/output_dir_math"
MRS_DIR="$UPSTREAM_OUT/assertions_seed${SEED}/${SUBJECT}"
STATES_DIR="$UPSTREAM_OUT/states_seed${SEED}"
RESULTS_DIR="$ALIGNED_DIR/results/seed${SEED}/${SUBJECT}"

mkdir -p "$RESULTS_DIR"

echo "=== Aligned S5 pipeline ==="
echo "Subject:     $SUBJECT"
echo "Seed:        $SEED"
echo "GenMorph:    $GENMORPH"
echo "GAssert jar: $GASSERT_JAR"
echo ""

# === Stage 1: Reproduce upstream's pipeline state captures ===
# These commands invoke upstream's Python scripts that internally launch
# Randoop / EvoSuite / PIT. The scripts depend on upstream's config layout.
# If `output_dir_math/states_seed${SEED}/<subject>/` already exists, skip
# this stage to save time.

if [[ -d "$STATES_DIR/source/$SUBJECT" ]]; then
    echo "[Stage 1] State captures already exist at $STATES_DIR — skipping reproduction."
else
    echo "[Stage 1] Reproducing upstream pipeline (this may take 5-15 min)..."

    # 1a. Compile SUT (idempotent)
    pushd "$GENMORPH" > /dev/null
    if [[ ! -f "configs/math-sut/build/classes/java/main/MathClass.class" ]]; then
        echo "  - compiling MathClass via gradle..."
        ./gradlew :configs:math-sut:compileJava || {
            echo "ERROR: gradle compile failed. Verify $GENMORPH/configs/math-sut has its own gradle subproject."
            exit 1
        }
    fi

    # 1b. Run Randoop to generate test inputs (writes to UPSTREAM_OUT/randoop_seed${SEED}/)
    echo "  - running Randoop seed=${SEED}..."
    python3 scripts/run/randoop.py \
        --config "$GENMORPH/configs/evaluation-config-math.json" \
        --seed "$SEED" \
        --subject "$SUBJECT" 2>&1 | tail -20 || {
        echo "WARN: scripts/run/randoop.py failed or not yet implemented for direct invocation."
        echo "      Check upstream README; may need to invoke ch.usi.gassert.<RandoopRunner> directly via java -cp."
    }

    # 1c. Run PIT 1.7 to generate mutants
    echo "  - running PIT 1.7 seed=${SEED}..."
    python3 scripts/run/pitest.py \
        --config "$GENMORPH/configs/evaluation-config-math.json" \
        --seed "$SEED" \
        --subject "$SUBJECT" 2>&1 | tail -20 || {
        echo "WARN: scripts/run/pitest.py failed or not yet implemented for direct invocation."
        echo "      Check upstream README; may need to invoke pitest-wrapper-1.7.4.jar directly."
    }

    popd > /dev/null

    if [[ ! -d "$STATES_DIR/source/$SUBJECT" ]]; then
        echo "ERROR: State captures still not present at $STATES_DIR/source/$SUBJECT"
        echo "       Stage 1 reproduction failed. See upstream's README for manual invocation."
        echo "       Falling back to Stage 1-bypass: use upstream's published mutants_killed.csv"
        echo "       directly as Set G ground truth, run Set N alone via java_bridge/, and accept"
        echo "       a pipeline-aligned-but-not-substrate-aligned comparison."
        exit 2
    fi
fi

# === Stage 2: Inject Set N MRs into upstream's MR directory ===
SET_N_SOURCE="$ALIGNED_DIR/set_n_mrs/$SUBJECT"
if [[ ! -d "$SET_N_SOURCE" ]]; then
    echo "ERROR: Set N MR files for $SUBJECT not found at $SET_N_SOURCE"
    echo "       Author them first (see aligned/README.md §'Set N MRs')"
    exit 3
fi

echo "[Stage 2] Injecting Set N MRs into $MRS_DIR..."
mkdir -p "$MRS_DIR"
cp "$SET_N_SOURCE"/*.txt "$MRS_DIR/"
echo "  MR files in $MRS_DIR after injection:"
ls "$MRS_DIR" | sed 's/^/    /'
echo ""

# === Stage 3: Invoke EvaluateMRs ===
echo "[Stage 3] Running ch.usi.gassert.EvaluateMRs..."
java -cp "$GASSERT_JAR" \
    ch.usi.gassert.EvaluateMRs \
    "$MRS_DIR" \
    "$STATES_DIR/source/$SUBJECT" \
    "$STATES_DIR/followup/$SUBJECT" \
    "$STATES_DIR/source_classification/$SUBJECT" \
    "$STATES_DIR/followup_classification/$SUBJECT" \
    "MathClass" \
    "$RESULTS_DIR/" \
  2>&1 | tee "$RESULTS_DIR/evaluator.log" \
  || {
      echo "ERROR: EvaluateMRs failed. See $RESULTS_DIR/evaluator.log"
      echo "       Common causes:"
      echo "         (a) State capture format mismatch — Stage 1 may have used a different"
      echo "             config than what EvaluateMRs expects."
      echo "         (b) Missing classifications/ subdirs (some upstream pipelines split"
      echo "             classification into a separate stage)."
      exit 4
  }

# === Stage 4: Parse and compute aligned metrics ===
echo "[Stage 4] Parsing aligned results..."
python3 "$ALIGNED_DIR/parse_aligned_results.py" \
    --csv "$RESULTS_DIR/mutants_killed.csv" \
    --status-csv "$RESULTS_DIR/mrs_status.csv" \
    --subject "$SUBJECT" \
    --seed "$SEED" \
    --output "$RESULTS_DIR/aligned_metrics.json"

echo ""
echo "=== Done ==="
echo "Aligned metrics: $RESULTS_DIR/aligned_metrics.json"
echo "Compare against upstream's published baseline at:"
echo "  $GENMORPH/evaluation/evaluation/pitest_seed${SEED}/${SUBJECT}/mutants_killed.csv"
