"""
Parse PIT mutation report XML → unified results.csv (one row per mutation).

PIT writes mutations.xml at build/reports/pitest/ with one <mutation> entry
per mutated location, recording which test(s) killed it. By inspecting the
killing-test method names, we can reconstruct per-MR detection.

Output schema (matches the rest of the pilot harness):

    mutation_id,mutation_class,subject,
    set_n_detected,set_g_detected,set_b_detected,
    seed,timestamp

Where:
  - set_n_detected = 1 if ANY of {testRhoPerm, testRhoScale, testRhoMono,
                                  testRhoEqRef} appears in killingTest.
  - set_g_detected = 1 if ANY of {testGenMorphMR0..MR3} appears.
  - set_b_detected = 1 if testRhoPerm alone appears (Set B = {ρ_perm}).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List


# Per-subject test method registry. Add a new subject here when extending.
SUBJECT_REGISTRY = {
    "gcd": {
        "set_n": {"testRhoPerm", "testRhoScale", "testRhoMono", "testRhoEqRef"},
        "set_g": {"testGenMorphMR0", "testGenMorphMR1", "testGenMorphMR2", "testGenMorphMR3"},
        "set_b": {"testRhoPerm"},
    },
    "sin": {
        "set_n": {"testRhoOddSym", "testRhoPeriod", "testRhoBound", "testRhoComplement"},
        "set_g": {"testGenMorphMR20", "testGenMorphMR21", "testGenMorphMR22", "testGenMorphMR23"},
        "set_b": {"testRhoBound"},  # Trivial baseline: bounded-output check
    },
}


def _killing_methods(mutation: ET.Element) -> set:
    """Extract test-method names that killed this mutation."""
    raw = mutation.findtext("killingTest", default="")
    if not raw:
        return set()
    junit5_methods = set(re.findall(r"\[method:([A-Za-z_][A-Za-z0-9_]*)\(\)\]", raw))
    if junit5_methods:
        return junit5_methods
    # PIT format: "fullyQualifiedClass.testMethod(parameters)"
    # we want just the testMethod name
    methods = set()
    for entry in raw.split("|"):
        entry = entry.strip()
        if not entry:
            continue
        # Drop the parameters parenthetical
        head = entry.split("(")[0]
        # Drop the FQCN, keep last segment
        method = head.split(".")[-1]
        methods.add(method)
    return methods


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pit-report-dir", required=True, type=Path,
                        help="Directory containing mutations.xml")
    parser.add_argument("--output", default="results/results.csv", type=Path)
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--subject", default="gcd",
                        help="Subject key in SUBJECT_REGISTRY (gcd, sin, ...)")
    args = parser.parse_args()

    if args.subject not in SUBJECT_REGISTRY:
        print(f"ERROR: unknown subject '{args.subject}'. Known: {list(SUBJECT_REGISTRY.keys())}")
        return 1
    subject_cfg = SUBJECT_REGISTRY[args.subject]
    set_n_tests = subject_cfg["set_n"]
    set_g_tests = subject_cfg["set_g"]
    set_b_tests = subject_cfg["set_b"]

    xml_path = args.pit_report_dir / "mutations.xml"
    if not xml_path.exists():
        # PIT 1.15 sometimes nests one level deeper (e.g. by date or by class)
        candidates = list(args.pit_report_dir.glob("**/mutations.xml"))
        if not candidates:
            print(f"ERROR: mutations.xml not found under {args.pit_report_dir}")
            return 1
        xml_path = candidates[0]
        print(f"Using {xml_path}")

    tree = ET.parse(xml_path)
    root = tree.getroot()

    rows: List[dict] = []
    timestamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    for i, mut in enumerate(root.findall("mutation")):
        status = mut.get("status", "UNKNOWN")
        killers = _killing_methods(mut)
        mut_class = mut.findtext("mutator", default="UNKNOWN").split(".")[-1]

        # PIT status semantics for our cross-validation against GenMorph:
        #   KILLED      → attribute to specific test method(s) that failed
        #   TIMED_OUT   → mutation caused infinite loop / timeout. ANY test
        #                 hitting the mutated code path would time out, so
        #                 GenMorph's per-MR binary matrix attributes timeout
        #                 to every enabled MR. We do the same.
        #   MEMORY_ERROR / RUN_ERROR → infrastructure-level kill, same
        #                 attribution as TIMED_OUT.
        #   SURVIVED / NO_COVERAGE → not detected by any set.
        infra_kill = status in ("TIMED_OUT", "MEMORY_ERROR", "RUN_ERROR")
        set_n = int(bool(killers & set_n_tests) or infra_kill)
        set_g = int(bool(killers & set_g_tests) or infra_kill)
        set_b = int(bool(killers & set_b_tests) or infra_kill)

        # Per-MR detection (one column per individual MR test method)
        per_mr = {}
        for tm in sorted(set_n_tests | set_g_tests):
            per_mr[f"mr_{tm}"] = int(tm in killers or infra_kill)

        row = {
            "mutation_id": f"M{i+1:03d}",
            "mutation_class": mut_class,
            "subject": args.subject,
            "pit_status": status,
            "set_n_detected": set_n,
            "set_g_detected": set_g,
            "set_b_detected": set_b,
            "seed": args.seed,
            "timestamp": timestamp,
        }
        row.update(per_mr)
        rows.append(row)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else
                                ["mutation_id", "mutation_class", "subject",
                                 "set_n_detected", "set_g_detected", "set_b_detected",
                                 "seed", "timestamp"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} mutation rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
