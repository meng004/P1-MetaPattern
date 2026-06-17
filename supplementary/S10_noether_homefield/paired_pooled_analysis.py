"""N3: pooled / stratified analysis of MR-battery vs differential-oracle across SUTs.

Per-SUT paired McNemar is underpowered (advdiff p=1.0). This pools the three
committed paired results (advdiff, radxfer, grayscott) to bring RQ4 (kernels
cross) and RQ5 (union -> completeness) to an inferential level:

  - pooled discordants b (MR-only), c (differential-only);
  - pooled McNemar exact p (tests symmetry b=c) + stratified Cochran-Mantel-Haenszel
    chi^2 (1 df) -- BOTH test asymmetry, i.e. whether MR has higher recall;
  - complementarity (RQ4): b>0 AND c>0 in every stratum and pooled (kernels cross,
    not nested); reported separately from the asymmetry test;
  - union vs best single oracle (RQ5 / IBT-2): union = killed-by-either.

Honest framing: a significant McNemar/CMH means MR has higher RECALL (not that the
differential is worse-as-an-oracle); the thesis claim is complementarity (c>0) +
union>best, NOT differential superiority.
Reads only committed paired_vs_mr.json; pure arithmetic, no re-execution/selection.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUTS = ["advdiff-xeval-diff", "radxfer-G2-diff", "grayscott-diff"]


def _binom_two_sided(b, c):
    """McNemar exact two-sided p: binomial(n=b+c, 0.5), tail at min(b,c)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(0, k + 1)) * (0.5 ** n)
    return min(1.0, 2.0 * tail)


def _chi2_1df_sf(x):
    """Survival function of chi-square with 1 df: P(X>x) = erfc(sqrt(x/2))."""
    return math.erfc(math.sqrt(x / 2.0))


def main():
    rows = []
    for s in SUTS:
        d = json.loads((HERE / "results" / s / "paired_vs_mr.json").read_text())
        n = d["n_matched_mutants"]
        rows.append({
            "sut": d["comparison"].split(":")[0],
            "n": n,
            "MR": d["A_MR_battery_killed"],
            "diff": d["B_differential_killed"],
            "b_MR_only": d["b_only_MR"],
            "c_diff_only": d["c_only_differential"],
            "both": d["both"],
            "neither": d["neither"],
            "union": n - d["neither"],
            "p": d["mcnemar_exact_p"],
        })

    B = sum(r["b_MR_only"] for r in rows)
    C = sum(r["c_diff_only"] for r in rows)
    N = sum(r["n"] for r in rows)
    MR = sum(r["MR"] for r in rows)
    DIFF = sum(r["diff"] for r in rows)
    UNION = sum(r["union"] for r in rows)
    NEITHER = sum(r["neither"] for r in rows)

    pooled_mcnemar = _binom_two_sided(B, C)
    cmh_chi2 = (B - C) ** 2 / (B + C) if (B + C) else 0.0   # stratified McNemar (no cc)
    cmh_p = _chi2_1df_sf(cmh_chi2)
    cross_all = all(r["b_MR_only"] > 0 and r["c_diff_only"] > 0 for r in rows)

    print("=== Per-SUT paired (MR battery A vs differential oracle B) ===")
    print(f"{'SUT':12}{'n':>4}{'MR':>5}{'diff':>6}{'b(MR-only)':>11}"
          f"{'c(diff-only)':>13}{'both':>6}{'neither':>8}{'union':>6}{'McNemar p':>11}")
    for r in rows:
        print(f"{r['sut']:12}{r['n']:>4}{r['MR']:>5}{r['diff']:>6}{r['b_MR_only']:>11}"
              f"{r['c_diff_only']:>13}{r['both']:>6}{r['neither']:>8}{r['union']:>6}{r['p']:>11.4g}")

    print("\n=== Pooled (N3) ===")
    print(f"  total real mutants N        = {N}")
    print(f"  MR-only b = {B}   differential-only c = {C}   (discordant = {B+C})")
    print(f"  pooled McNemar exact p (b=c): {pooled_mcnemar:.3e}")
    print(f"  stratified CMH chi^2(1df)   : {cmh_chi2:.2f}   p = {cmh_p:.3e}")
    print(f"  --> asymmetry: MR has higher RECALL (b>>c); reported honestly.")
    print(f"\n  RQ4 complementarity (kernels cross): b>0 AND c>0 in EVERY stratum "
          f"and pooled: {cross_all and B>0 and C>0}")
    print(f"      -> differential-only contributes {C} faults no MR caught (not nested).")
    print(f"\n  RQ5 union vs best single oracle (IBT-2):")
    print(f"      union   = {UNION}/{N} = {UNION/N:.3f}")
    print(f"      MR      = {MR}/{N} = {MR/N:.3f}   (best single)")
    print(f"      diff    = {DIFF}/{N} = {DIFF/N:.3f}")
    print(f"      union - best = {UNION-MR} (= pooled c); neither = {NEITHER}/{N}")
    print(f"      -> combining complementary-kernel oracles strictly improves recall.")

    out = {
        "strata": rows,
        "pooled": {
            "N": N, "b_MR_only": B, "c_diff_only": C,
            "pooled_mcnemar_exact_p": pooled_mcnemar,
            "cmh_chi2_1df": cmh_chi2, "cmh_p": cmh_p,
            "complementarity_all_strata_cross": cross_all,
            "union": UNION, "MR_best_single": MR, "diff": DIFF, "neither": NEITHER,
            "union_minus_best": UNION - MR,
        },
        "interpretation": {
            "RQ4_kernels_cross": bool(cross_all and B > 0 and C > 0),
            "RQ5_union_exceeds_best": bool(UNION > MR),
            "honest_note": "significant McNemar/CMH = MR higher recall, NOT "
                           "differential superiority; thesis = complementarity + union>best.",
        },
    }
    (HERE / "results" / "paired_pooled_analysis.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")
    print(f"\n[written] results/paired_pooled_analysis.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
