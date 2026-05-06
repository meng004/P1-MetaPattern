#!/usr/bin/env bash
# run_all.sh — main S5 aligned-pilot driver.
#
# Pre: bootstrap.sh + verify_env.sh have completed cleanly.
# Post: aligned/results/seed11/<subject>/{mutants_killed.csv, aligned_metrics.json}
#       and parallel/results/<subject>/{...} for the un-aligned data.
#
# Stages:
#   1. Inject Set N MRs (.jir/.jor) into upstream's mrs/assertions_seed11/
#   2. Run upstream's eval pipeline once (this populates output_dir_math/...)
#   3. Parse augmented mutants_killed.csv per subject
#   4. Aggregate cross-subject efficiency metrics
#
# Usage:
#   bash run_all.sh                         # default subjects: gcd, sin
#   bash run_all.sh 'MathClass?pow?0'       # add more subjects
#   bash run_all.sh --fallback              # skip stage 2 if upstream pipeline broken

set -e

# Source env
[[ -f "$HOME/.bashrc-genmorph" ]] && source "$HOME/.bashrc-genmorph"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PILOT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ALIGNED_DIR="$PILOT_ROOT/aligned"

# Default subject list
SUBJECTS=("MathClass?gcd?0" "MathClass?sin?0")
SEED=11
FALLBACK=0

# Parse args
for arg in "$@"; do
    if [[ "$arg" == "--fallback" ]]; then
        FALLBACK=1
    elif [[ "$arg" == MathClass* || "$arg" == GuavaClass* || "$arg" == LangClass* ]]; then
        SUBJECTS+=("$arg")
    fi
done

GENMORPH=${GENMORPH:-/tmp/genmorph_pilot/genmorph_full/genmorph}
EVAL_CONFIG="$GENMORPH/configs/config-all-evaluation-math.json"

echo "=== run_all.sh ==="
echo "Subjects: ${SUBJECTS[*]}"
echo "Seed:     $SEED"
echo "Fallback: $FALLBACK"
echo ""

# ---------------------------------------------------------------------------
# STAGE 1 — Inject Set N MRs into upstream's directory tree
# ---------------------------------------------------------------------------
echo "[Stage 1] Injecting Set N MRs into upstream mrs/assertions_seed${SEED}/..."
for SUB in "${SUBJECTS[@]}"; do
    SET_N_DIR="$ALIGNED_DIR/set_n_mrs/$SUB"
    UPSTREAM_DIR="/tmp/genmorph_pilot/mrs/mrs/assertions_seed${SEED}/$SUB"

    if [[ ! -d "$SET_N_DIR" ]]; then
        echo "  SKIP $SUB: no Set N DSL files at $SET_N_DIR"
        continue
    fi
    if [[ ! -d "$UPSTREAM_DIR" ]]; then
        echo "  SKIP $SUB: no upstream MR directory at $UPSTREAM_DIR"
        continue
    fi

    cp "$SET_N_DIR"/*.txt "$UPSTREAM_DIR/"
    INJECTED=$(ls "$SET_N_DIR" | grep -c "\.jir\.txt$" || echo 0)
    echo "  $SUB: injected $INJECTED Set N MRs (rho_*.{jir,jor}.txt)"
done

# ---------------------------------------------------------------------------
# STAGE 2 — Run upstream pipeline (or skip in fallback mode)
# ---------------------------------------------------------------------------
if [[ $FALLBACK -eq 0 ]]; then
    echo ""
    echo "[Stage 2] Running upstream eval pipeline..."
    echo "  cd $GENMORPH"
    echo "  python3 scripts/run/genmorph.py eval $EVAL_CONFIG"
    echo "  (this may take 15-30 min: Randoop + EvoSuite + PIT 1.7 + EvaluateMRs)"

    cd "$GENMORPH"
    if ! python3 scripts/run/genmorph.py eval "$EVAL_CONFIG" 2>&1 | tee "$PILOT_ROOT/aligned/results/upstream_eval.log"; then
        echo ""
        echo "ERROR: upstream pipeline failed. Common causes:"
        echo "  (a) Maven dependency download blocked by network firewall"
        echo "  (b) Major mutation tool missing (only needed for `gen`, not `eval` — verify)"
        echo "  (c) JDK 8 path mismatch in scripts/config.py"
        echo "  (d) RAM insufficient: GAssert default heap is 16g; reduce via GASSERT_HEAP env"
        echo ""
        echo "Re-run with --fallback to skip Stage 2 and use upstream's published mutants_killed.csv."
        exit 5
    fi
    cd "$SCRIPT_DIR"
else
    echo ""
    echo "[Stage 2] SKIPPED (--fallback). Will use upstream's pre-computed mutants_killed.csv."
fi

# ---------------------------------------------------------------------------
# STAGE 3 — Parse augmented mutants_killed.csv per subject
# ---------------------------------------------------------------------------
echo ""
echo "[Stage 3] Parsing per-subject results..."
mkdir -p "$ALIGNED_DIR/results/seed${SEED}"

for SUB in "${SUBJECTS[@]}"; do
    SUB_DIR="$ALIGNED_DIR/results/seed${SEED}/$SUB"
    mkdir -p "$SUB_DIR"

    # Locate the augmented mutants_killed.csv
    if [[ $FALLBACK -eq 1 ]]; then
        # Fallback: copy upstream's published file as-is (Set N rows will be missing)
        SRC="/tmp/genmorph_pilot/evaluation/evaluation/pitest_seed${SEED}/$SUB/mutants_killed.csv"
        STATUS_SRC="/tmp/genmorph_pilot/evaluation/evaluation/pitest_seed${SEED}/$SUB/mrs_status.csv"
    else
        # Upstream output_dir layout
        SRC="$GENMORPH/output_dir_math/pitest_seed${SEED}/$SUB/mutants_killed.csv"
        STATUS_SRC="$GENMORPH/output_dir_math/pitest_seed${SEED}/$SUB/mrs_status.csv"
    fi

    if [[ ! -f "$SRC" ]]; then
        echo "  SKIP $SUB: augmented mutants_killed.csv not at $SRC"
        continue
    fi

    cp "$SRC" "$SUB_DIR/mutants_killed.csv"
    [[ -f "$STATUS_SRC" ]] && cp "$STATUS_SRC" "$SUB_DIR/mrs_status.csv"

    # Parse to aligned_metrics.json
    python3 "$ALIGNED_DIR/parse_aligned_results.py" \
        --csv "$SUB_DIR/mutants_killed.csv" \
        $([[ -f "$SUB_DIR/mrs_status.csv" ]] && echo "--status-csv $SUB_DIR/mrs_status.csv") \
        --subject "$SUB" \
        --seed "$SEED" \
        --output "$SUB_DIR/aligned_metrics.json"
    echo "  $SUB: aligned_metrics.json written"
done

# ---------------------------------------------------------------------------
# STAGE 4 — Cross-subject efficiency metrics
# ---------------------------------------------------------------------------
echo ""
echo "[Stage 4] Cross-subject aggregation..."
RESULTS_CSVS=()
SUB_KEYS=()
for SUB in "${SUBJECTS[@]}"; do
    SUB_KEY=$(echo "$SUB" | sed -E 's/MathClass\?(.+)\?0/\1/')
    CSV="$ALIGNED_DIR/results/seed${SEED}/$SUB/mutants_killed.csv"
    if [[ -f "$CSV" ]]; then
        # Convert mutants_killed.csv (upstream format) to results.csv (our parser format)
        # …or write a direct cross-subject aggregator for the upstream format.
        # For now, just record paths.
        RESULTS_CSVS+=("$CSV")
        SUB_KEYS+=("$SUB_KEY")
    fi
done

if [[ ${#RESULTS_CSVS[@]} -gt 0 ]]; then
    echo "  per-subject inputs: ${RESULTS_CSVS[*]}"
    echo "  cross-subject metric file: $ALIGNED_DIR/results/efficiency_metrics_aligned.json"
    # Note: efficiency_metrics.py expects our parser's results.csv schema, not upstream's.
    # parse_aligned_results.py output (aligned_metrics.json) already has M1-M5 per subject.
    # Aggregating across subjects:
    python3 - <<EOF
import json
from pathlib import Path
seeds_dir = Path("$ALIGNED_DIR/results/seed${SEED}")
out = {"per_subject": [], "n_subjects": 0}
for sub_dir in sorted(seeds_dir.iterdir()):
    metrics_file = sub_dir / "aligned_metrics.json"
    if metrics_file.exists():
        out["per_subject"].append(json.loads(metrics_file.read_text()))
out["n_subjects"] = len(out["per_subject"])
out_path = Path("$ALIGNED_DIR/results/efficiency_metrics_aligned.json")
out_path.write_text(json.dumps(out, indent=2))
print(f"Wrote {out_path}")
EOF
else
    echo "  no per-subject results found; check earlier stages"
fi

echo ""
echo "=== run_all.sh complete ==="
echo "Output:    $ALIGNED_DIR/results/seed${SEED}/"
echo "Aggregate: $ALIGNED_DIR/results/efficiency_metrics_aligned.json"
echo ""
echo "Compare with parallel pipeline:"
echo "  $PILOT_ROOT/results/efficiency_metrics.json   (PIT 1.15 + JUnit, single-pipeline)"
echo "  $ALIGNED_DIR/results/efficiency_metrics_aligned.json   (PIT 1.7 + GAssert, fully aligned)"
