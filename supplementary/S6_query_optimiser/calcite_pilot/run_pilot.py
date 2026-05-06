"""
Main harness: run Set N + Set Segura oracles against QED Calcite plan-JSON pairs.

Flow:
  1. Load pair IDs from pairs_sample.json (produced by sample_pairs.py).
  2. For each pair, parse $QED_ROOT/tests/calcite/<pair_id>.json into a Pair.
  3. Run all Set N oracles → set_n_applicable / set_n_detected / fired rule.
  4. Run all Set Segura oracles likewise.
  5. Write results.csv.

Then run stats.py on results.csv → pilot_stats.json.

Usage:
    python run_pilot.py --qed-path /tmp/calcite_pilot/QED \\
        --pairs-sample pairs_sample.json \\
        --output results/results.csv
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Dict, List

from qed_adapter import Pair, load_pair
from set_n_oracle import SET_N_ORACLES
from set_segura_oracle import SET_SEGURA_ORACLES


def _evaluate_oracles(oracles, pair: Pair):
    """Aggregate (applicable, detected, fired_rule) for an oracle bundle.

    Detection criterion under the QED corpus's certified-equivalence model:
      A pair is 'detected' by the bundle if any oracle returns 'match'. The
      'mismatch' verdict counts as applicable but not detected. 'na' is the
      out-of-pattern case and contributes neither.
    """
    applicable = 0
    detected = 0
    fired_rules = []
    for oracle in oracles:
        try:
            verdict, rule = oracle(pair)
        except Exception:  # noqa: BLE001
            verdict, rule = ("na", None)
        if verdict != "na":
            applicable = 1
            if verdict == "match":
                detected = 1
                if rule:
                    fired_rules.append(rule)
    return applicable, detected, ";".join(sorted(set(fired_rules)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qed-path", required=True, type=Path)
    parser.add_argument("--pairs-sample", default="pairs_sample.json", type=Path)
    parser.add_argument("--output", default="results/results.csv", type=Path)
    parser.add_argument("--seed", type=int, default=11)
    args = parser.parse_args()

    if not args.pairs_sample.exists():
        print(f"ERROR: {args.pairs_sample} not found; run sample_pairs.py first.", file=sys.stderr)
        return 1

    sample: List[Dict] = json.loads(args.pairs_sample.read_text())
    pairs_dir = args.qed_path / "tests" / "calcite"
    if not pairs_dir.exists():
        print(f"ERROR: QED Calcite tests dir not found: {pairs_dir}", file=sys.stderr)
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    rows: List[Dict] = []
    timestamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

    for entry in sample:
        pid = entry["pair_id"]
        path = pairs_dir / f"{pid}.json"
        if not path.exists():
            print(f"WARN: pair {pid} not found at {path}", file=sys.stderr)
            continue
        try:
            pair = load_pair(path)
        except Exception as exc:  # noqa: BLE001
            print(f"WARN: skip {pid}: {exc}", file=sys.stderr)
            continue

        n_app, n_det, n_fired = _evaluate_oracles(SET_N_ORACLES, pair)
        s_app, s_det, s_fired = _evaluate_oracles(SET_SEGURA_ORACLES, pair)

        rows.append({
            "pair_id": pid,
            "complexity": entry.get("complexity", "unknown"),
            "n_nodes_total": entry.get("n_nodes_total", 0),
            "is_equivalent_ground_truth": pair.is_equivalent,
            "set_n_applicable": n_app,
            "set_n_detected": n_det,
            "set_n_mr_fired": n_fired,
            "set_segura_applicable": s_app,
            "set_segura_detected": s_det,
            "set_segura_mr_fired": s_fired,
            "seed": args.seed,
            "timestamp": timestamp,
        })

    if not rows:
        print("ERROR: no rows produced", file=sys.stderr)
        return 3

    fieldnames = list(rows[0].keys())
    with args.output.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
