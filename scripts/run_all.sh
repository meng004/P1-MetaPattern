#!/usr/bin/env bash
# ============================================================================
# S5 Aligned Experiment — Set N (NOETHER) vs Set G (GenMorph) detection compare
# ============================================================================
# Thin orchestrator over GenMorph's own toolchain (see PLANS/003). Per subject:
#   1. substrate   : eval_substrate.py  -> source .methodinputs (Randoop, seed)
#   2. Set N follow-ups : setn_followups.py (constructed from each MR's .jir)
#   3. score Set N : eval_mr_set.py -> PITestGenerator + PIT (upstream-native)
#   4. Set G       : adopt upstream-published pitest_seed<seed>/<subj>/mutants_killed.csv
# Then compare_sets.py aggregates Set N vs Set G on the shared mutant set.
#
# GAssert MR-learning and the per-mutant gen loop are skipped on this path: we
# use published Set G MRs and hand-authored Set N MRs, so no MR is *learned*.
#
# Usage:
#   bash scripts/run_all.sh                         # all 23, --jobs 2
#   bash scripts/run_all.sh --subjects 'MathClass?gcd?0,MathClass?pow?0'
#   bash scripts/run_all.sh --jobs 3 --randoop-budget 300
#   bash scripts/run_all.sh --compare-only          # just re-aggregate results/
# Long runs: nohup bash scripts/run_all.sh > results/seed11/_logs/run.log 2>&1 &
# Resumable: a subject whose results/seed<seed>/<subj>/setn_mutants_killed.csv
# already exists is skipped.

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

[[ -f .env ]] || { echo "FATAL: .env not found. Run setup.sh first."; exit 1; }
set -a; source .env; set +a
: "${GENMORPH:?}"; : "${MAJOR_HOME:?}"; : "${SEED:=11}"
export JAVA_HOME="${JAVA8:?}"; export PATH="$JAVA_HOME/bin:$PATH"; export MAJOR_HOME

PILOT="${GENMORPH%/genmorph_full/genmorph}"
SETG_PITEST_DIR="$PILOT/evaluation/pitest_seed${SEED}"
RESULTS_DIR="$REPO_ROOT/results/seed${SEED}"
LOG_DIR="$RESULTS_DIR/_logs"
CONF_DIR="$GENMORPH/configs"

JOBS=2
RANDOOP_BUDGET=120
RANDOOP_EXECS=1
COMPARE_ONLY=0
SUBJECTS_ARG="all"

ALL_SUBJECTS=(
    'MathClass?gcd?0' 'MathClass?sin?0' 'MathClass?acos?0' 'MathClass?log10?0'
    'MathClass?millerRabinPrimeTest?0' 'MathClass?nextPrime?0' 'MathClass?pow?0'
    'MathClass?sinh?0' 'MathClass?stirlingS2?0' 'MathClass?tan?0'
    'LangClass?abbreviate?0' 'LangClass?capitalize?0' 'LangClass?center?0'
    'LangClass?difference?0' 'LangClass?isSorted?0'
    'GuavaClass?indexOf?0' 'GuavaClass?join?0' 'GuavaClass?meanOf?0'
    'GuavaClass?min?0' 'GuavaClass?padStart?0' 'GuavaClass?repeat?0'
    'GuavaClass?sort?0' 'GuavaClass?truncate?0'
)

while [[ $# -gt 0 ]]; do
    case "$1" in
        --subjects) SUBJECTS_ARG="$2"; shift 2 ;;
        --jobs) JOBS="$2"; shift 2 ;;
        --randoop-budget) RANDOOP_BUDGET="$2"; shift 2 ;;
        --randoop-execs) RANDOOP_EXECS="$2"; shift 2 ;;
        --compare-only) COMPARE_ONLY=1; shift ;;
        *) echo "Usage: $0 [--subjects all|csv] [--jobs N] [--randoop-budget S] [--compare-only]"; exit 1 ;;
    esac
done

mkdir -p "$RESULTS_DIR" "$LOG_DIR"
if [[ "$SUBJECTS_ARG" == "all" ]]; then SUBJECTS=("${ALL_SUBJECTS[@]}"); else IFS=',' read -r -a SUBJECTS <<< "$SUBJECTS_ARG"; fi

subject_lib()  { case "$1" in MathClass*) echo math;; LangClass*) echo lang;; GuavaClass*) echo guava;; *) echo "FATAL unknown $1" >&2; exit 1;; esac; }
slug() { echo "$1" | tr '?' '_'; }

# Emit a one-subject SUT config into the upstream configs/ dir; echo its repo-rel path.
emit_sut_config() {
    local subj="$1" lib cls method idx cfg
    lib=$(subject_lib "$subj")
    cls="${subj%%\?*}"; method="$(echo "$subj" | cut -d'?' -f2)"; idx="$(echo "$subj" | cut -d'?' -f3)"
    cfg="$CONF_DIR/sut-config-${lib}-$(echo "$method")-${idx}.json"
    cat > "$cfg" <<JSON
{
    "root": "configs/${lib}-sut",
    "classpaths": ["configs/${lib}-sut/target/classes"],
    "sources": "configs/${lib}-sut/src/main/java",
    "suts": { "${cls}": { "${method}": [${idx}] } }
}
JSON
    echo "configs/$(basename "$cfg")"
}

run_subject() {
    local subj="$1" s lib outdir setn_out setg_src setn_dst setg_dst sut_cfg
    s=$(slug "$subj"); lib=$(subject_lib "$subj")
    outdir="output_dir_${lib}"
    local res="$RESULTS_DIR/$subj"; mkdir -p "$res"
    setn_dst="$res/setn_mutants_killed.csv"
    if [[ -f "$setn_dst" ]]; then echo "[$subj] cached, skip"; return 0; fi
    local log="$LOG_DIR/run_${s}.log"
    {
        echo "=== [$(date -u +%H:%M:%S)] $subj (lib=$lib) ==="
        sut_cfg=$(emit_sut_config "$subj")
        echo "-- substrate --"
        python3 scripts/eval_substrate.py --genmorph "$GENMORPH" --sut-config "$sut_cfg" \
            --output-dir "$outdir" --seed "$SEED" \
            --randoop-budget "$RANDOOP_BUDGET" --randoop-execs "$RANDOOP_EXECS" --max-tests 100
        echo "-- Set N follow-ups --"
        rm -rf "$GENMORPH/$outdir/setn_followups/setn_seed${SEED}/$subj" \
               "$GENMORPH/$outdir/setn_mrs/setn_seed${SEED}/$subj" 2>/dev/null || true
        python3 scripts/setn_followups.py --subject "$subj" \
            --set-n-dir "set_n_mrs/$subj" \
            --sources-dir "$GENMORPH/$outdir/evaluation_test_inputs_seed${SEED}" \
            --followups-dir "$GENMORPH/$outdir/setn_followups" \
            --mrs-dir "$GENMORPH/$outdir/setn_mrs" --experiment "setn_seed${SEED}"
        echo "-- score Set N (PITestGenerator + PIT) --"
        python3 scripts/eval_mr_set.py --genmorph "$GENMORPH" --sut-config "$sut_cfg" \
            --output-dir "$outdir" --experiment-template "setn_seed{seed}" --seed "$SEED" \
            --sources-subdir "evaluation_test_inputs_seed${SEED}" \
            --followups-subdir setn_followups --mrs-subdir setn_mrs \
            --pitest-suite-subdir "pitest_setn_suite_${s}" --pitest-workdir "pitest_setn_${s}"
        setn_out="$GENMORPH/$outdir/pitest_setn_${s}/$subj/mutants_killed.csv"
        [[ -f "$setn_out" ]] && cp "$setn_out" "$setn_dst" || { echo "WARN: no Set N CSV for $subj"; }
        # Set G: adopt upstream-published seed-<seed> result
        setg_src="$SETG_PITEST_DIR/$subj/mutants_killed.csv"
        [[ -f "$setg_src" ]] && cp "$setg_src" "$res/setg_mutants_killed.csv" || echo "WARN: no published Set G for $subj"
        [[ -f "$SETG_PITEST_DIR/$subj/mrs_status.csv" ]] && cp "$SETG_PITEST_DIR/$subj/mrs_status.csv" "$res/setg_mrs_status.csv" || true
        echo "=== [$(date -u +%H:%M:%S)] $subj done ==="
    } > "$log" 2>&1 && echo "[$subj] OK (-> $log)" || echo "[$subj] FAILED (see $log)"
}

if [[ $COMPARE_ONLY -eq 0 ]]; then
    echo "=== Stage: per-subject Set N scoring (${#SUBJECTS[@]} subjects, --jobs $JOBS) ==="
    pids=()
    for subj in "${SUBJECTS[@]}"; do
        run_subject "$subj" &
        pids+=($!)
        while (( $(jobs -rp | wc -l) >= JOBS )); do wait -n 2>/dev/null || true; done
    done
    wait
fi

echo "=== Stage: compare Set N vs Set G ==="
python3 scripts/compare_sets.py --results-dir "$RESULTS_DIR" \
    --output "$REPO_ROOT/results/comparison_seed${SEED}.json"
echo "=== Done. Summary: results/comparison_seed${SEED}.json ==="
