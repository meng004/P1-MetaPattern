#!/usr/bin/env python3
"""
tests/test_aggregate_metrics.py

Runs scripts/aggregate_metrics.py against synthetic per-subject metrics
JSON files and verifies pooled rates + Wilson CI shape + McNemar pairing.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AGG_SCRIPT = REPO / "scripts" / "aggregate_metrics.py"

failures = []


def fail(msg):
    failures.append(msg)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        results = Path(tmp) / "results"
        results.mkdir()

        # Subject A: 10 mutants; N kills 3, G kills 5; overlap 2; N-only=1 G-only=3
        (results / "subjA").mkdir()
        with open(results / "subjA" / "aligned_metrics.json", "w") as f:
            json.dump({
                "subject": "subjA",
                "n_mutants": 10,
                "set_n": {"n_mrs": 3, "kill_vector": [1, 1, 1, 0, 0, 0, 0, 0, 0, 0], "n_killed": 3},
                "set_g": {"n_mrs": 4, "kill_vector": [0, 1, 1, 1, 1, 1, 0, 0, 0, 0], "n_killed": 5},
                "m_metrics": {"M1_kill_rate_N": 0.3, "M1_kill_rate_G": 0.5,
                              "M3_unique_to_N": 1, "M3_unique_to_G": 3, "M3_overlap": 2},
            }, f)
        # Subject B: 8 mutants; N kills 4, G kills 2; overlap 1; N-only=3 G-only=1
        (results / "subjB").mkdir()
        with open(results / "subjB" / "aligned_metrics.json", "w") as f:
            json.dump({
                "subject": "subjB",
                "n_mutants": 8,
                "set_n": {"n_mrs": 2, "kill_vector": [1, 1, 1, 1, 0, 0, 0, 0], "n_killed": 4},
                "set_g": {"n_mrs": 3, "kill_vector": [1, 0, 0, 0, 1, 0, 0, 0], "n_killed": 2},
                "m_metrics": {"M1_kill_rate_N": 0.5, "M1_kill_rate_G": 0.25,
                              "M3_unique_to_N": 3, "M3_unique_to_G": 1, "M3_overlap": 1},
            }, f)

        out = Path(tmp) / "summary.json"
        subprocess.run([
            sys.executable, str(AGG_SCRIPT),
            "--results-dir", str(results),
            "--output", str(out),
        ], check=True)

        with open(out) as f:
            summary = json.load(f)

    # 2 subjects × (10+8) = 18 mutants total
    if summary["n_subjects"] != 2:
        fail(f"n_subjects = {summary['n_subjects']}, expected 2")
    if summary["total_mutants"] != 18:
        fail(f"total_mutants = {summary['total_mutants']}, expected 18")

    # Pooled N kills: 3 + 4 = 7; G kills: 5 + 2 = 7
    if summary["set_n"]["kills"] != 7:
        fail(f"set_n.kills = {summary['set_n']['kills']}, expected 7")
    if summary["set_g"]["kills"] != 7:
        fail(f"set_g.kills = {summary['set_g']['kills']}, expected 7")
    if abs(summary["set_n"]["kill_rate"] - 7 / 18) > 1e-6:
        fail(f"set_n.kill_rate = {summary['set_n']['kill_rate']}, expected {7/18}")

    # Wilson CI: should be a 2-tuple containing the kill rate
    ci = summary["set_n"]["wilson_95_ci"]
    if not (isinstance(ci, list) and len(ci) == 2):
        fail(f"set_n.wilson_95_ci shape unexpected: {ci}")
    elif not (ci[0] <= summary["set_n"]["kill_rate"] <= ci[1]):
        fail(f"set_n.kill_rate {summary['set_n']['kill_rate']} not in CI {ci}")

    # McNemar paired: subjA n_only={M1} ; subjB n_only={M2,M3,M4} → b = 1+3 = 4
    #                 subjA g_only={M4,M5,M6} ; subjB g_only={M5} → c = 3+1 = 4
    if summary["paired_mcnemar"]["n_only_kills"] != 4:
        fail(f"n_only_kills = {summary['paired_mcnemar']['n_only_kills']}, expected 4")
    if summary["paired_mcnemar"]["g_only_kills"] != 4:
        fail(f"g_only_kills = {summary['paired_mcnemar']['g_only_kills']}, expected 4")

    # Per-subject deltas exist
    if len(summary["per_subject"]) != 2:
        fail(f"per_subject count = {len(summary['per_subject'])}, expected 2")

    if failures:
        print(f"FAIL ({len(failures)}):")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)
    print("OK: aggregate_metrics.py pools correctly, Wilson CI brackets rate, McNemar pairs counted")


if __name__ == "__main__":
    main()
