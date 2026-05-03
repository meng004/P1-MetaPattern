"""
runner_pilot.py — DeepCrime-style real-fault pilot (§6.6.1).

Runs the same N/L/B MR sets as runner.py but against the 5 DeepCrime-style
mutation operators (cat_v) instead of the original hand-crafted 20. This
produces deepcrime_pilot_results.csv used by §6.6.1's pilot table.

Detection criterion: identical to runner.py (strict transition).
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
from mutations import DEEPCRIME_PILOT_MUTATIONS  # type: ignore[import-not-found]


NUM_INPUTS = 8
INPUT_SEED = 5_000
N_POINTS = 128


def _make_test_inputs(num: int = NUM_INPUTS, seed: int = INPUT_SEED) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    return [rng.standard_normal((N_POINTS, 3)) for _ in range(num)]


def _evaluate_set(model, mrs, inputs):
    out: dict = {}
    for mr in mrs:
        per_input: list = []
        for x in inputs:
            r = mr.evaluate(model, x)
            per_input.append(r.holds)
        out[mr.name] = per_input
    return out


def _detection(holds_base, holds_mut) -> bool:
    for b, m in zip(holds_base, holds_mut):
        if b is True and m is False:
            return True
    return False


def main(checkpoint_path, output_csv: str, *, stub: bool) -> None:
    print(f"[pilot] loading model (stub={stub}, ckpt={checkpoint_path})")
    model = load_model(checkpoint_path, stub=stub)
    fp_base = model_fingerprint(model)
    print(f"[pilot] baseline fingerprint: {fp_base}")
    inputs = _make_test_inputs()

    all_mrs = [(mr, "N") for mr in SET_N] + \
              [(mr, "L") for mr in SET_L] + \
              [(mr, "B") for mr in SET_B]

    print(f"[pilot] {len(all_mrs)} MRs across N, L, B")

    print("[pilot] evaluating MRs on baseline")
    baseline_per_mr = _evaluate_set(model, [mr for mr, _ in all_mrs], inputs)

    rows = []
    for mut in DEEPCRIME_PILOT_MUTATIONS:
        print(f"[pilot]   mutation {mut.id} ({mut.label})")
        try:
            mutated = mut.apply(model)
        except Exception as exc:
            print(f"[pilot]     FAILED to apply: {exc}")
            for mr, set_label in all_mrs:
                rows.append({
                    "set": set_label, "mr": mr.name, "block": mr.block,
                    "mutation_id": mut.id, "mutation_category": mut.category,
                    "detected": False, "baseline_violations": "n/a",
                    "mutated_violations": "n/a", "error": str(exc),
                })
            continue
        mutated_per_mr = _evaluate_set(mutated, [mr for mr, _ in all_mrs], inputs)
        for mr, set_label in all_mrs:
            hb = baseline_per_mr[mr.name]
            hm = mutated_per_mr[mr.name]
            detected = _detection(hb, hm)
            rows.append({
                "set": set_label, "mr": mr.name, "block": mr.block,
                "mutation_id": mut.id, "mutation_category": mut.category,
                "detected": detected,
                "baseline_violations": sum(1 for h in hb if h is False),
                "mutated_violations": sum(1 for h in hm if h is False),
                "error": "",
            })

    out_path = Path(output_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"[pilot] wrote {len(rows)} rows to {out_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Run the §6.6.1 DeepCrime-style pilot")
    ap.add_argument("--checkpoint", default=None)
    ap.add_argument("--output", default="deepcrime_pilot_results.csv")
    ap.add_argument("--stub", action="store_true")
    args = ap.parse_args()
    main(args.checkpoint, args.output, stub=args.stub or args.checkpoint in (None, ""))
