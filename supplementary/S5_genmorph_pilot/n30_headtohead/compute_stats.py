#!/usr/bin/env python3
"""
Statistics for the n>=30 commons-math head-to-head, from kill_matrix.csv.

Per the pre-registered analysis plan (protocol_path_a_headtohead.md S6 +
CLAUDE.md C6):
  - per-set detection rate with Wilson 95% CI (pooled over all SUTs' mutants);
  - pairwise McNemar exact two-sided p (paired by mutant) for Set N vs each
    baseline that actually ran (Set B literature, Set M METRIC+);
  - effect size per pair: risk difference (RD) with Newcombe 95% CI, and odds
    ratio (OR) on the paired 2x2 with 95% CI;
  - Bonferroni correction across the pairwise family (here 2 pairs -> alpha/2);
  - D1 (algebra-disrupting) vs D2 (algebra-preserving) stratified rates;
  - power note: report the discordant-pair count b+c for each McNemar test and
    flag if the paired test is underpowered at alpha=0.05.

The mutant is the matched unit: every SUT class runs Set N + Set B + Set M
against the identical PIT mutant population, so kills are paired row-wise.

Output: results/headtohead_stats.json  and a printed summary table.
"""
import argparse
import json
import math
import pathlib

import numpy as np
import pandas as pd
from scipy.stats import binomtest
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.proportion import proportion_confint

HERE = pathlib.Path(__file__).parent


def wilson(k, n):
    if n == 0:
        return [0.0, 1.0]
    lo, hi = proportion_confint(k, n, alpha=0.05, method="wilson")
    return [round(float(lo), 4), round(float(hi), 4)]


def set_summary(df, col):
    n = len(df)
    k = int(df[col].sum())
    return {"detected": k, "n": n, "rate": round(k / n, 4) if n else 0.0,
            "wilson_95ci": wilson(k, n)}


def newcombe_rd_ci(a, b, c, d):
    """Newcombe (1998) method-10 CI for the difference of paired proportions
    p1 - p2 where p1=(a+b)/n (set A rate), p2=(a+c)/n (set B rate), with
    n=a+b+c+d, b = A-only, c = B-only. Returns (rd, lo, hi)."""
    n = a + b + c + d
    if n == 0:
        return 0.0, -1.0, 1.0
    p1 = (a + b) / n
    p2 = (a + c) / n
    rd = p1 - p2

    def wilson_pair(k, m):
        if m == 0:
            return 0.0, 1.0
        lo, hi = proportion_confint(k, m, alpha=0.05, method="wilson")
        return lo, hi

    l1, u1 = wilson_pair(a + b, n)
    l2, u2 = wilson_pair(a + c, n)
    # correlation correction term
    # phi estimate per Newcombe method 10
    denom = (a + b) * (c + d) * (a + c) * (b + d)
    if denom > 0:
        phi = (a * d - b * c) / math.sqrt(denom)
    else:
        phi = 0.0
    # bound phi
    phi = max(min(phi, 1.0), -1.0)
    lo = rd - math.sqrt((p1 - l1) ** 2 - 2 * phi * (p1 - l1) * (u2 - p2) + (u2 - p2) ** 2)
    hi = rd + math.sqrt((u1 - p1) ** 2 - 2 * phi * (u1 - p1) * (p2 - l2) + (p2 - l2) ** 2)
    return round(rd, 4), round(lo, 4), round(hi, 4)


def odds_ratio_paired(b, c):
    """Paired OR for McNemar table = b/c (ratio of discordant cells), with
    a Haldane-Anscombe 0.5 continuity correction and 95% CI on log scale.
    b = A-only kills (A=1,B=0), c = B-only kills (A=0,B=1)."""
    bb, cc = b + 0.5, c + 0.5
    or_ = bb / cc
    se = math.sqrt(1.0 / bb + 1.0 / cc)
    lo = math.exp(math.log(or_) - 1.96 * se)
    hi = math.exp(math.log(or_) + 1.96 * se)
    return round(or_, 4), round(lo, 4), round(hi, 4)


def pairwise(df, col_a, col_b, alpha_bonf):
    a = int(((df[col_a] == 1) & (df[col_b] == 1)).sum())  # both
    b = int(((df[col_a] == 1) & (df[col_b] == 0)).sum())  # A only
    c = int(((df[col_a] == 0) & (df[col_b] == 1)).sum())  # B only
    d = int(((df[col_a] == 0) & (df[col_b] == 0)).sum())  # neither
    # The exact McNemar test is a two-sided binomial test on b successes out of
    # (b+c) discordant pairs with H0 p=0.5. scipy's binomtest is numerically
    # robust for very small p (statsmodels.mcnemar underflows to 0.0 here).
    discordant = b + c
    if discordant > 0:
        p = float(binomtest(b, discordant, 0.5, alternative="two-sided").pvalue)
    else:
        p = float("nan")
    # cross-check with statsmodels (may underflow to 0.0; kept for transparency)
    try:
        p_sm = float(mcnemar([[a, b], [c, d]], exact=True, correction=False).pvalue)
    except Exception:
        p_sm = float("nan")
    rd, rdlo, rdhi = newcombe_rd_ci(a, b, c, d)
    or_, orlo, orhi = odds_ratio_paired(b, c)
    # exact binomial power check on discordant pairs: a McNemar exact at alpha is
    # incapable of reaching p<alpha unless 0.5**discordant <= alpha (all-on-one-side).
    min_achievable_p = 0.5 ** discordant if discordant > 0 else 1.0
    underpowered = (discordant == 0) or (min_achievable_p > 0.05)

    def _pfmt(x):
        if math.isnan(x):
            return None
        return float(f"{x:.3e}")  # keep small p as scientific float, no underflow-to-0

    return {
        "both": a, f"{col_a}_only": b, f"{col_b}_only": c, "neither": d,
        "discordant_b_plus_c": discordant,
        "mcnemar_exact_p_two_sided": _pfmt(p),
        "mcnemar_exact_p_statsmodels_crosscheck": _pfmt(p_sm),
        "bonferroni_alpha": round(alpha_bonf, 5),
        "significant_after_bonferroni": (not math.isnan(p)) and (p < alpha_bonf),
        "risk_difference": rd, "rd_95ci": [rdlo, rdhi],
        "odds_ratio_paired": or_, "or_95ci": [orlo, orhi],
        "min_achievable_exact_p": _pfmt(min_achievable_p),
        "paired_test_underpowered_at_0.05": bool(underpowered),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--matrix", default=str(HERE / "results" / "kill_matrix.csv"))
    ap.add_argument("--out", default=str(HERE / "results" / "headtohead_stats.json"))
    args = ap.parse_args()

    df = pd.read_csv(args.matrix)
    if df.empty:
        raise SystemExit("kill_matrix.csv is empty")

    n_suts = df["sut"].nunique()
    n_mut = len(df)

    # which baselines actually ran (have >=1 kill anywhere -> they ran;
    # set_b and set_m are always present columns since all SUTs carry them)
    baselines = []
    for col, name in (("set_b", "Set B (literature)"), ("set_m", "Set M (METRIC+)")):
        baselines.append((col, name))

    n_pairs = len(baselines)
    alpha_bonf = 0.05 / n_pairs if n_pairs else 0.05

    out = {
        "n_suts": int(n_suts),
        "n_mutants_total": int(n_mut),
        "n_mutants_covered": int(df["covered"].sum()),
        "pre_registration": "supplementary/S8_metricplus_sun2021_subjects/protocol_path_a_headtohead.md",
        "matched_unit": "mutant (each SUT class runs Set N + Set B + Set M on identical PIT mutant population)",
        "pooled": {
            "set_n": set_summary(df, "set_n"),
            "set_b": set_summary(df, "set_b"),
            "set_m": set_summary(df, "set_m"),
        },
        "pairwise_setN_vs_baselines": {},
        "bonferroni": {"n_pairwise_tests": n_pairs, "family_alpha": 0.05,
                       "per_test_alpha": round(alpha_bonf, 5)},
        "stratified": {},
        "per_sut": {},
    }

    out["pairwise_setN_vs_baselines"]["N_vs_B"] = pairwise(df, "set_n", "set_b", alpha_bonf)
    out["pairwise_setN_vs_baselines"]["N_vs_M"] = pairwise(df, "set_n", "set_m", alpha_bonf)

    # D1 / D2 stratified
    for strat in ("D1", "D2"):
        sub = df[df["stratum"] == strat]
        out["stratified"][strat] = {
            "n_mutants": int(len(sub)),
            "set_n": set_summary(sub, "set_n"),
            "set_b": set_summary(sub, "set_b"),
            "set_m": set_summary(sub, "set_m"),
            "N_vs_B": pairwise(sub, "set_n", "set_b", alpha_bonf) if len(sub) else None,
            "N_vs_M": pairwise(sub, "set_n", "set_m", alpha_bonf) if len(sub) else None,
        }

    # per-SUT
    for sut, g in df.groupby("sut"):
        out["per_sut"][sut] = {
            "n_mutants": int(len(g)),
            "block": g["block"].iloc[0],
            "covered": int(g["covered"].sum()),
            "set_n": set_summary(g, "set_n"),
            "set_b": set_summary(g, "set_b"),
            "set_m": set_summary(g, "set_m"),
        }

    pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=2)

    # printed summary
    print("=" * 78)
    print(f"n_SUTs = {n_suts}   n_mutants = {n_mut}   covered = {out['n_mutants_covered']}")
    print("=" * 78)
    p = out["pooled"]
    for nm, k in (("Set N", "set_n"), ("Set B (lit)", "set_b"), ("Set M (METRIC+)", "set_m")):
        s = p[k]
        print(f"  {nm:16s}  {s['detected']:3d}/{s['n']:3d} = {s['rate']:.3f}  "
              f"Wilson95 [{s['wilson_95ci'][0]:.3f}, {s['wilson_95ci'][1]:.3f}]")
    print("-" * 78)
    for pair, key in (("Set N vs Set B", "N_vs_B"), ("Set N vs Set M", "N_vs_M")):
        d = out["pairwise_setN_vs_baselines"][key]
        print(f"  {pair}: both={d['both']} N_only={d['set_n_only']} "
              f"B/M_only={d[[x for x in d if x.endswith('_only') and x!='set_n_only'][0]]} "
              f"neither={d['neither']}")
        print(f"     McNemar exact p={d['mcnemar_exact_p_two_sided']} "
              f"(Bonferroni alpha={d['bonferroni_alpha']}, sig={d['significant_after_bonferroni']})")
        print(f"     RD={d['risk_difference']} {d['rd_95ci']}  "
              f"OR(paired)={d['odds_ratio_paired']} {d['or_95ci']}  "
              f"discordant b+c={d['discordant_b_plus_c']}  "
              f"underpowered@0.05={d['paired_test_underpowered_at_0.05']}")
    print("-" * 78)
    for strat in ("D1", "D2"):
        st = out["stratified"][strat]
        print(f"  [{strat}] n={st['n_mutants']}  "
              f"N={st['set_n']['rate']:.3f} B={st['set_b']['rate']:.3f} M={st['set_m']['rate']:.3f}")
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
