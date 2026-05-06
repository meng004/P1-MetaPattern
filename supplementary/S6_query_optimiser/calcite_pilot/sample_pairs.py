"""
Sample 50 query pairs from QED's Calcite test corpus, stratified by complexity.

The QED artifact ships 444 .json files at $QED_ROOT/tests/calcite/. Each file
is one rewrite-pair. We stratify by total node count of (q1 + q2):
  - easy   (small):  < 12 plan nodes
  - medium:           12-25 plan nodes
  - hard   (large):   > 25 plan nodes
and sample 20/20/10 with seed=11.

Output: pairs_sample.json — list of {pair_id, complexity, n_nodes_total}.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Dict, List

from qed_adapter import Node, iterate_calcite_pairs, load_pair


def _count_nodes(node: Node | None) -> int:
    if node is None:
        return 0
    return 1 + sum(_count_nodes(c) for c in node.children)


def _classify(total_nodes: int) -> str:
    """Classify by total plan-node count.

    Tuned to QED-Calcite's actual distribution (median = 8, IQR 6-11, max 33):
      easy   < 8 nodes
      medium 8-13 nodes
      hard   ≥ 14 nodes
    """
    if total_nodes < 8:
        return "easy"
    if total_nodes <= 13:
        return "medium"
    return "hard"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qed-path", required=True, type=Path)
    parser.add_argument("--output", default="pairs_sample.json", type=Path)
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--counts", default="20,20,10", help="easy,medium,hard counts")
    args = parser.parse_args()

    counts = dict(zip(["easy", "medium", "hard"], (int(c) for c in args.counts.split(","))))

    by_complexity: Dict[str, List[dict]] = {"easy": [], "medium": [], "hard": []}
    total_seen = 0
    for path in iterate_calcite_pairs(args.qed_path):
        total_seen += 1
        try:
            pair = load_pair(path)
        except Exception:
            continue
        n_nodes = _count_nodes(pair.q1) + _count_nodes(pair.q2)
        complexity = _classify(n_nodes)
        by_complexity[complexity].append({
            "pair_id": pair.pair_id,
            "complexity": complexity,
            "n_nodes_total": n_nodes,
            "is_equivalent": pair.is_equivalent,
        })

    rng = random.Random(args.seed)
    sample: List[dict] = []
    for level in ("easy", "medium", "hard"):
        bucket = by_complexity[level]
        want = counts[level]
        if len(bucket) <= want:
            sample.extend(bucket)
            print(f"WARN: only {len(bucket)} {level} pairs available, using all")
        else:
            sample.extend(rng.sample(bucket, want))

    sample.sort(key=lambda x: x["pair_id"])
    args.output.write_text(json.dumps(sample, indent=2))
    print(f"Wrote {len(sample)} pair IDs (from {total_seen} total) to {args.output}")
    print("Stratification:", {k: len(v) for k, v in by_complexity.items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
