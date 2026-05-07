#!/usr/bin/env bash
# ============================================================================
# S5 Aligned Experiment — main orchestrator
# ============================================================================
# Runs the aligned pipeline for all 23 GenMorph subjects with seed 11.
#
# Two stages:
#   Stage 1 (--reproduce): Randoop + PIT — slow (~4-7 h total), run once.
#   Stage 2 (--evaluate):  inject Set N MRs + re-run EvaluateMRs — fast (~30 min),
#                          repeatable as Set N evolves.
#   --all                  runs both in sequence (default).
#
# Usage:
#   bash run_all.sh                  # full pipeline (Stage 1 + Stage 2)
#   bash run_all.sh --reproduce      # only Stage 1
#   bash run_all.sh --evaluate       # only Stage 2 (assumes Stage 1 done)
#   bash run_all.sh --subject 'MathClass?gcd?0'   # single subject
#
# Long cloud runs (Stage 1 ~4–7 h): launch with nohup so it survives session
# disconnects, e.g.:
#   nohup bash scripts/run_all.sh --reproduce > results/seed11/_logs/run.log 2>&1 &
#
# Resume after a crash: just re-run; per-subject artifacts are cached
# (Randoop states + PIT mutants_killed.csv are checked before regenerating).
#
# Output: results/seed11/<subject>/{aligned_metrics.json, mutants_killed.csv}
#         results/seed11/_logs/{stage1_*,stage2_*}.log  (per-subject logs)
#         results/aligned_summary.json                  (cross-subject)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Source .env
if [[ ! -f .env ]]; then
    echo "FATAL: .env not found. Run 'bash setup.sh' first."
    exit 1
fi
set -a; source .env; set +a

# Sanity checks
[[ -d "$GENMORPH" ]]            || { echo "FATAL: GENMORPH=$GENMORPH not found"; exit 2; }
[[ -f "$GASSERT_JAR" ]]         || { echo "FATAL: GASSERT_JAR=$GASSERT_JAR not built"; exit 2; }
[[ -d "$REPO_ROOT/set_n_mrs" ]] || { echo "FATAL: set_n_mrs/ not found"; exit 2; }

export JAVA_HOME=$JAVA8
export PATH=$JAVA_HOME/bin:$PATH

# All 23 subjects (matching GenMorph's published evaluation)
ALL_SUBJECTS=(
    'MathClass?gcd?0' 'MathClass?sin?0' 'MathClass?acos?0'
    'MathClass?log10?0' 'MathClass?millerRabinPrimeTest?0'
    'MathClass?nextPrime?0' 'MathClass?pow?0' 'MathClass?sinh?0'
    'MathClass?stirlingS2?0' 'MathClass?tan?0'
    'LangClass?abbreviate?0' 'LangClass?capitalize?0'
    'LangClass?center?0' 'LangClass?difference?0' 'LangClass?isSorted?0'
    'GuavaClass?indexOf?0' 'GuavaClass?join?0' 'GuavaClass?meanOf?0'
    'GuavaClass?min?0' 'GuavaClass?padStart?0' 'GuavaClass?repeat?0'
    'GuavaClass?sort?0' 'GuavaClass?truncate?0'
)

# Argument parsing
DO_REPRODUCE=0
DO_EVALUATE=0
SINGLE_SUBJECT=""
case "${1:-}" in
    --reproduce) DO_REPRODUCE=1 ;;
    --evaluate)  DO_EVALUATE=1 ;;
    --all|"")    DO_REPRODUCE=1; DO_EVALUATE=1 ;;
    --subject)
        SINGLE_SUBJECT="${2:?--subject requires a name}"
        DO_REPRODUCE=1; DO_EVALUATE=1
        ;;
    *) echo "Usage: $0 [--reproduce|--evaluate|--all] [--subject <name>]"; exit 1 ;;
esac

# Determine subject list
if [[ -n "$SINGLE_SUBJECT" ]]; then
    SUBJECTS=("$SINGLE_SUBJECT")
else
    SUBJECTS=("${ALL_SUBJECTS[@]}")
fi

# Map subject → library (for which scripts/configs to use)
subject_library() {
    case "$1" in
        MathClass*) echo "math" ;;
        LangClass*) echo "lang" ;;
        GuavaClass*) echo "guava" ;;
        *) echo "FATAL: unknown subject $1" >&2; exit 1 ;;
    esac
}

RESULTS_DIR="$REPO_ROOT/results/seed${SEED}"
LOG_DIR="$RESULTS_DIR/_logs"
mkdir -p "$RESULTS_DIR" "$LOG_DIR"

# Sanitize subject name to a filesystem-safe slug for log files.
# GenMorph subjects contain '?' (e.g. MathClass?gcd?0); fine on Linux but
# noisy for tab-completion / glob, so log files use '_' instead.
slug() { echo "$1" | tr '?' '_'; }

# ----------------------------------------------------------------------------
# Stage 1: Reproduce upstream's pipeline state (Randoop + PIT)
# ----------------------------------------------------------------------------
if [[ $DO_REPRODUCE -eq 1 ]]; then
    echo ""
    echo "=== [$(date +%Y-%m-%dT%H:%M:%S)] Stage 1: Reproduce upstream pipeline (Randoop + PIT 1.7.4) ==="
    cd "$GENMORPH"
    for subject in "${SUBJECTS[@]}"; do
        lib=$(subject_library "$subject")
        config="configs/evaluation-config-${lib}.json"
        s=$(slug "$subject")
        echo ""
        echo "--- [$(date +%H:%M:%S)] Subject: $subject (lib=$lib) ---"
        # Randoop test generation + state capture
        if [[ -d "$GENMORPH/output_dir_${lib}/states_seed${SEED}/source/${subject}" ]]; then
            echo "  Randoop states already present, skip"
        else
            randoop_log="$LOG_DIR/stage1_randoop_${s}.log"
            echo "  Running Randoop (seed=${SEED}); full log → $randoop_log"
            python3 scripts/run/randoop.py \
                --config "$config" \
                --seed  "$SEED" \
                --subject "$subject" 2>&1 \
                | tee "$randoop_log" | tail -5 || \
                echo "  WARN: Randoop failed for $subject (see $randoop_log)"
        fi
        # PIT mutation testing
        if [[ -f "$GENMORPH/output_dir_${lib}/pitest_seed${SEED}/${subject}/mutants_killed.csv" ]]; then
            echo "  PIT mutants already present, skip"
        else
            pit_log="$LOG_DIR/stage1_pit_${s}.log"
            echo "  Running PIT 1.7.4 (seed=${SEED}); full log → $pit_log"
            python3 scripts/run/pitest.py \
                --config "$config" \
                --seed  "$SEED" \
                --subject "$subject" 2>&1 \
                | tee "$pit_log" | tail -5 || \
                echo "  WARN: PIT failed for $subject (see $pit_log)"
        fi
    done
    cd "$REPO_ROOT"
    echo ""
    echo "=== [$(date +%Y-%m-%dT%H:%M:%S)] Stage 1 done ==="
fi

# ----------------------------------------------------------------------------
# Stage 2: Inject Set N MRs and re-run EvaluateMRs
# ----------------------------------------------------------------------------
if [[ $DO_EVALUATE -eq 1 ]]; then
    echo ""
    echo "=== [$(date +%Y-%m-%dT%H:%M:%S)] Stage 2: Inject Set N MRs + re-run EvaluateMRs ==="

    for subject in "${SUBJECTS[@]}"; do
        lib=$(subject_library "$subject")
        s=$(slug "$subject")
        echo ""
        echo "--- [$(date +%H:%M:%S)] Subject: $subject ---"

        # Locate upstream MR directory + state directories
        UPSTREAM_MRS_DIR="$GENMORPH/output_dir_${lib}/assertions_seed${SEED}/${subject}"
        STATES_SRC="$GENMORPH/output_dir_${lib}/states_seed${SEED}/source/${subject}"
        STATES_FOL="$GENMORPH/output_dir_${lib}/states_seed${SEED}/followup/${subject}"
        CLS_SRC="$GENMORPH/output_dir_${lib}/states_seed${SEED}/source_classification/${subject}"
        CLS_FOL="$GENMORPH/output_dir_${lib}/states_seed${SEED}/followup_classification/${subject}"

        # Skip if upstream pipeline state missing
        if [[ ! -d "$UPSTREAM_MRS_DIR" ]] || [[ ! -d "$STATES_SRC" ]]; then
            echo "  SKIP: upstream pipeline state missing (run Stage 1 first)"
            continue
        fi

        # Source class name (strip ?xxx?N)
        SRC_CLASS=$(echo "$subject" | cut -d'?' -f1)

        # Inject our Set N MRs
        SET_N_DIR="$REPO_ROOT/set_n_mrs/${subject}"
        if [[ -d "$SET_N_DIR" ]]; then
            cp "$SET_N_DIR"/*.jir.txt "$UPSTREAM_MRS_DIR/" 2>/dev/null || true
            cp "$SET_N_DIR"/*.jor.txt "$UPSTREAM_MRS_DIR/" 2>/dev/null || true
            n_set_n=$(ls "$SET_N_DIR"/*.jir.txt 2>/dev/null | wc -l | tr -d ' ')
            echo "  Injected $n_set_n Set N MRs into $UPSTREAM_MRS_DIR"
        else
            echo "  WARN: no Set N MRs for $subject, evaluating Set G only"
        fi

        # Output directory for this subject's results
        OUT_DIR="$REPO_ROOT/results/seed${SEED}/${subject}"
        mkdir -p "$OUT_DIR"

        # Invoke EvaluateMRs
        eval_log="$LOG_DIR/stage2_evaluate_${s}.log"
        echo "  Running EvaluateMRs; full log → $eval_log"
        java -cp "$GASSERT_JAR" \
             ch.usi.gassert.EvaluateMRs \
             "$UPSTREAM_MRS_DIR" \
             "$STATES_SRC" "$STATES_FOL" \
             "$CLS_SRC" "$CLS_FOL" \
             "$SRC_CLASS" \
             "$OUT_DIR/" 2>&1 \
             | tee "$eval_log" | tail -3 || \
             echo "  WARN: EvaluateMRs failed for $subject (see $eval_log)"

        # Parse per-subject metrics
        if [[ -f "$OUT_DIR/mutants_killed.csv" ]]; then
            python3 "$REPO_ROOT/scripts/parse_results.py" \
                --csv "$OUT_DIR/mutants_killed.csv" \
                --status "$OUT_DIR/mrs_status.csv" \
                --set-n-dir "$SET_N_DIR" \
                --output "$OUT_DIR/aligned_metrics.json"
        fi
    done

    # ------------------------------------------------------------------------
    # Aggregate across subjects
    # ------------------------------------------------------------------------
    echo ""
    echo "=== Aggregating cross-subject metrics ==="
    python3 "$REPO_ROOT/scripts/aggregate_metrics.py" \
        --results-dir "$REPO_ROOT/results/seed${SEED}" \
        --output "$REPO_ROOT/results/aligned_summary.json"
fi

echo ""
echo "=== Done ==="
echo "Per-subject results: $REPO_ROOT/results/seed${SEED}/<subject>/aligned_metrics.json"
echo "Cross-subject summary: $REPO_ROOT/results/aligned_summary.json"
