#!/usr/bin/env python3
"""tests/test_setn_e2e.py — guarded end-to-end smoke for the Set N eval path.

If a Set N `mutants_killed.csv` has been produced by eval_mr_set.py in the
(ephemeral) toolchain output dir, validate its contract:
  * header is EXPERIMENT,MR,M1..Mn,COUNT
  * every row's COUNT equals the sum of its per-mutant kill flags
  * at least one Set N MR row is present
Otherwise SKIP (exit 0) — the toolchain output is not part of the repo and is
absent on a fresh container; the unit tests still cover the pure logic.
"""
import csv
import glob
import sys

CANDS = glob.glob(
    "/tmp/genmorph_pilot/genmorph_full/genmorph/output_dir_*/pitest_setn*/*/mutants_killed.csv"
)


def main():
    if not CANDS:
        print("SKIP test_setn_e2e: no Set N mutants_killed.csv present "
              "(toolchain not run in this container)")
        return
    ok = 0
    for path in CANDS:
        with open(path) as f:
            rows = list(csv.reader(f))
        hdr = rows[0]
        assert hdr[0] == "EXPERIMENT" and hdr[1] == "MR" and hdr[-1] == "COUNT", hdr
        mcols = hdr[2:-1]
        assert mcols and all(c.startswith("M") for c in mcols), f"bad mutant cols: {mcols}"
        setn_rows = 0
        for r in rows[1:]:
            kills = [int(x) for x in r[2:-1]]
            assert sum(kills) == int(r[-1]), f"COUNT mismatch in {path}: {r[:2]}"
            if r[0].startswith("setn"):
                setn_rows += 1
        assert setn_rows > 0, f"no Set N rows in {path}"
        ok += 1
    print(f"OK: validated schema + COUNT consistency of {ok} Set N mutants_killed.csv")


if __name__ == "__main__":
    main()
