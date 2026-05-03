"""
runner.py — execute the §6.6 case study comparison.

Pipeline:
  1. Load model (real e3nn checkpoint or StubModel for pipeline validation).
  2. Compute baseline MR results: each MR evaluated on the unmutated model
     across NUM_INPUTS test point clouds. Records (mr, input_id) -> holds_baseline.
  3. For each of 20 mutations:
     a. Apply the mutation to a fresh copy of the model.
     b. Evaluate each MR on the mutated model across the same NUM_INPUTS clouds.
     c. Detection criterion: a mutation is *detected by mr* if there exists at
        least one input where the MR holds on the baseline AND fails on the
        mutated model. (Strict transition; baseline-failure does not count
        as detection. This is the criterion that handles set L's L_scale-
        type out-of-scope MRs cleanly.)
  4. Emit results.csv with one row per (set, mr, mutation) triple.

Detection at the SET level (used for H1/H2):
  set S detects mutation mu if at least one mr in S detects mu.

Coverage_NOETHER for an MR set is computed against the seven NOETHER blocks:
  coverage = |{block : some mr in S has block != "(out)" and block exists}|
             / |{non-empty NOETHER blocks for A_equi}|
The denominator is 5 (G, O_le, T*, T_rev*, L*) for A_equi.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from model_interface import load_model, model_fingerprint  # type: ignore[import-not-found]
from mr_sets.set_N_noether import SET_N  # type: ignore[import-not-found]
from mr_sets.set_L_llm import SET_L  # type: ignore[import-not-found]
from mr_sets.set_B_literature import SET_B  # type: ignore[import-not-found]
from mutations import ALL_MUTATIONS  # type: ignore[import-not-found]


NUM_INPUTS = 8           # number of test point clouds per (mr, mutation)
INPUT_SEED = 5_000        # seed for the test cloud sequence
N_POINTS = 128            # points per cloud


def _make_test_inputs(num: int = NUM_INPUTS, seed: int = INPUT_SEED) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    return [rng.standard_normal((N_POINTS, 3)) for _ in range(num)]


def _evaluate_set(model, mrs, inputs):
    """Returns dict: mr.name -> list[bool|None] (per-input holds)."""
    out = {}
    for mr in mrs:
        per_input: list = []
        for x in inputs:
            r = mr.evaluate(model, x)
            per_input.append(r.holds)
        out[mr.name] = per_input
    return out


def _detection(holds_base: list, holds_mut: list) -> bool:
    """Strict-transition criterion: detect iff some input has
    base=True and mut=False."""
    for b, m in zip(holds_base, holds_mut):
        if b is True and m is False:
            return True
    return False


def main(checkpoint_path: str | None, output_csv: str, *, stub: bool) -> None:
    print(f"[runner] loading model (stub={stub}, ckpt={checkpoint_path})")
    model = load_model(checkpoint_path, stub=stub)
    fp_base = model_fingerprint(model)
    print(f"[runner] model fingerprint: {fp_base}")
    inputs = _make_test_inputs()
    print(f"[runner] test inputs: {len(inputs)} clouds of {N_POINTS} points")

    all_mrs = [(mr, "N") for mr in SET_N] + \
              [(mr, "L") for mr in SET_L] + \
              [(mr, "B") for mr in SET_B]

    print("[runner] evaluating MRs on baseline (unmutated)")
    baseline_per_mr = _evaluate_set(model, [mr for mr, _ in all_mrs], inputs)

    rows = []
    for mut in ALL_MUTATIONS:
        print(f"[runner]   mutation {mut.id} ({mut.label})")
        try:
            mutated = mut.apply(model)
        except Exception as exc:
            print(f"[runner]     FAILED to apply: {exc}")
            for mr_name, mr_obj in [(mr.name, mr) for mr, _ in all_mrs]:
                rows.append({
                    "set": [s for m, s in all_mrs if m.name == mr_name][0],
                    "mr": mr_name,
                    "block": mr_obj.block,
                    "mutation_id": mut.id,
                    "mutation_category": mut.category,
                    "detected": False,
                    "baseline_violations": "n/a",
                    "mutated_violations": "n/a",
                    "error": str(exc),
                })
            continue
        fp_mut = model_fingerprint(mutated)
        if fp_mut == fp_base:
            print(f"[runner]     WARNING: mutation {mut.id} did not change model fingerprint")

        mutated_per_mr = _evaluate_set(mutated, [mr for mr, _ in all_mrs], inputs)
        for mr, set_label in all_mrs:
            holds_base = baseline_per_mr[mr.name]
            holds_mut = mutated_per_mr[mr.name]
            detected = _detection(holds_base, holds_mut)
            rows.append({
                "set": set_label,
                "mr": mr.name,
                "block": mr.block,
                "mutation_id": mut.id,
                "mutation_category": mut.category,
                "detected": detected,
                "baseline_violations": sum(1 for h in holds_base if h is False),
                "mutated_violations": sum(1 for h in holds_mut if h is False),
                "error": "",
            })

    out_path = Path(output_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"[runner] wrote {len(rows)} rows to {out_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Run the §6.6 case study")
    ap.add_argument("--checkpoint", default=None,
                    help="path to e3nn SE(3)-Transformer checkpoint (.pt); "
                         "omit or pass '' to use StubModel")
    ap.add_argument("--output", default="results.csv",
                    help="CSV path for output (default: results.csv)")
    ap.add_argument("--stub", action="store_true",
                    help="force StubModel even if --checkpoint is given")
    args = ap.parse_args()
    main(args.checkpoint, args.output, stub=args.stub or args.checkpoint in (None, ""))
