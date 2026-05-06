#!/usr/bin/env python3
"""
tests/test_parse_results.py

Runs scripts/parse_results.py against a fixture mutants_killed.csv and
asserts the output JSON has correct kill counts, set assignment, and
M-metric values.

Fixture has 7 MRs (4 GenMorph MR0-3, 3 NOETHER rho_*) over 5 mutants.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PARSE_SCRIPT = REPO / "scripts" / "parse_results.py"
FIXTURE_CSV = REPO / "tests" / "fixtures" / "sample_mutants_killed.csv"
FIXTURE_STATUS = REPO / "tests" / "fixtures" / "sample_mrs_status.csv"

failures = []


def fail(msg):
    failures.append(msg)


def main():
    # Set N: rho_perm, rho_scale, rho_mono — simulate by creating dummy MR files
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        set_n_dir = tmp / "MathClass?gcd?0"
        set_n_dir.mkdir()
        for name in ["rho_perm", "rho_scale", "rho_mono"]:
            (set_n_dir / f"MathClass?gcd?0@{name}.jir.txt").write_text("dummy")
            (set_n_dir / f"MathClass?gcd?0@{name}.jor.txt").write_text("dummy")

        # Run parse_results.py
        out = tmp / "out.json"
        subprocess.run([
            sys.executable, str(PARSE_SCRIPT),
            "--csv", str(FIXTURE_CSV),
            "--status", str(FIXTURE_STATUS),
            "--set-n-dir", str(set_n_dir),
            "--output", str(out),
        ], check=True)

        with open(out) as f:
            result = json.load(f)

    # Assertions
    if result["n_mutants"] != 5:
        fail(f"n_mutants = {result['n_mutants']}, expected 5")
    if result["n_total_mrs"] != 7:
        fail(f"n_total_mrs = {result['n_total_mrs']}, expected 7")
    if result["set_n"]["n_mrs"] != 3:
        fail(f"set_n.n_mrs = {result['set_n']['n_mrs']}, expected 3")
    if result["set_g"]["n_mrs"] != 4:
        fail(f"set_g.n_mrs = {result['set_g']['n_mrs']}, expected 4")

    # Set N union: rho_perm kills M1+M5, rho_scale kills M2+M5, rho_mono kills M3
    # Union = {M1, M2, M3, M5} → 4 kills
    if result["set_n"]["n_killed"] != 4:
        fail(f"set_n.n_killed = {result['set_n']['n_killed']}, expected 4")
    expected_n_vec = [1, 1, 1, 0, 1]
    if result["set_n"]["kill_vector"] != expected_n_vec:
        fail(f"set_n.kill_vector = {result['set_n']['kill_vector']}, expected {expected_n_vec}")

    # Set G union: MR0 kills M1+M3, MR1 kills M2+M3, MR2 kills M4, MR3 kills M3+M4
    # Union = {M1, M2, M3, M4} → 4 kills
    if result["set_g"]["n_killed"] != 4:
        fail(f"set_g.n_killed = {result['set_g']['n_killed']}, expected 4")
    expected_g_vec = [1, 1, 1, 1, 0]
    if result["set_g"]["kill_vector"] != expected_g_vec:
        fail(f"set_g.kill_vector = {result['set_g']['kill_vector']}, expected {expected_g_vec}")

    # M3_unique_to_N: mutants only N kills = {M5} → 1
    # M3_unique_to_G: mutants only G kills = {M4} → 1
    # M3_overlap: {M1, M2, M3} → 3
    m = result["m_metrics"]
    if m["M3_unique_to_N"] != 1:
        fail(f"M3_unique_to_N = {m['M3_unique_to_N']}, expected 1")
    if m["M3_unique_to_G"] != 1:
        fail(f"M3_unique_to_G = {m['M3_unique_to_G']}, expected 1")
    if m["M3_overlap"] != 3:
        fail(f"M3_overlap = {m['M3_overlap']}, expected 3")

    # Per-MR FP rates parsed
    fp_perm = next((p for p in result["per_mr"] if p["mr"] == "rho_perm"), None)
    if fp_perm is None or fp_perm.get("fp") != 0.0:
        fail(f"rho_perm fp = {fp_perm}, expected fp=0.0")

    if failures:
        print(f"FAIL ({len(failures)}):")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)
    print("OK: parse_results.py correctly classifies sets, computes kills, M3 metrics")


if __name__ == "__main__":
    main()
