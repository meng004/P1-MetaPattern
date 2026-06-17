"""Expert-monotonicity vs algebra-complete: the detection gap.

Thesis (from the N5 industrial finding that 110/110 expert MRs are O<= monotone):
experts reason from sensitivity intuition and produce single-block (O<=) MRs;
NOETHER enumerates ALL blocks deductively. By the Invariance-Blindness Theorem an
O<=-only battery inherits O<='s kernel and is blind to faults only the other blocks
catch. This script QUANTIFIES that gap on the executed S10 home-field SUTs: how many
real faults are caught by the O<= subset alone (an "expert-like" battery) versus the
full algebra-derived battery, and the set caught ONLY by non-O<= blocks.

No new model: re-analysis of the existing S10 detection records by block label.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from suts import heat_sut, wave_sut, poisson_sut, advdiff_sut
import noether_metrics as nm

SUTS = {"heat-1d": heat_sut.evaluate, "wave-1d": wave_sut.evaluate,
        "poisson-1d": poisson_sut.evaluate, "advdiff-2d": advdiff_sut.evaluate}


def analyse(evaluate):
    r = evaluate()
    blocks = r["mr_blocks"]
    ole = {m for m, b in blocks.items() if b == "O_le"}
    other = {m for m, b in blocks.items() if b != "O_le"}
    reals = [rec for rec in r["records"] if not rec.get("baseline")]
    n = len(reals)
    det_ole = det_all = only_other = only_ole = 0
    for rec in reals:
        k = rec["kills"]
        by_ole = any(k.get(m, False) for m in ole)
        by_other = any(k.get(m, False) for m in other)
        by_all = by_ole or by_other
        det_ole += by_ole
        det_all += by_all
        only_other += (by_all and not by_ole)   # caught only thanks to non-O<= blocks
        only_ole += (by_ole and not by_other)
    return {"n": n, "blocks": sorted(set(blocks.values())),
            "n_ole_mrs": len(ole), "n_other_mrs": len(other),
            "det_ole": det_ole, "det_all": det_all,
            "gap_only_nonOle": only_other, "only_Ole": only_ole}


def main():
    print("Expert-monotonicity (O<= only) vs algebra-complete battery — S10 SUTs\n")
    print(f"{'SUT':12}{'n':>4}{'O<=det':>8}{'ALLdet':>8}{'gap(only non-O<=)':>20}  blocks")
    tot_n = tot_ole = tot_all = tot_gap = 0
    for name, ev in SUTS.items():
        a = analyse(ev)
        tot_n += a["n"]; tot_ole += a["det_ole"]; tot_all += a["det_all"]
        tot_gap += a["gap_only_nonOle"]
        print(f"{name:12}{a['n']:>4}{a['det_ole']:>8}{a['det_all']:>8}"
              f"{a['gap_only_nonOle']:>20}  {a['blocks']}")
    lo_o, hi_o = nm.wilson_ci(tot_ole, tot_n)
    lo_a, hi_a = nm.wilson_ci(tot_all, tot_n)
    print(f"\nPOOLED  n={tot_n}")
    print(f"  O<=-only detection (expert-like): {tot_ole}/{tot_n} = {tot_ole/tot_n:.3f} "
          f"Wilson95 [{lo_o:.3f},{hi_o:.3f}]")
    print(f"  algebra-complete detection:       {tot_all}/{tot_n} = {tot_all/tot_n:.3f} "
          f"Wilson95 [{lo_a:.3f},{hi_a:.3f}]")
    print(f"  GAP (faults caught ONLY by non-O<= blocks): {tot_gap}/{tot_n} = "
          f"{tot_gap/tot_n:.3f}")
    print("\n  Reading: an expert battery limited to monotonicity (O<=) leaves the GAP")
    print("  undetected; those faults are caught only by the algebra's other blocks")
    print("  (G symmetry, L* limit, Conservation, T_rev*), which NOETHER derives")
    print("  without expert input. This is the IBT kernel made quantitative.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
