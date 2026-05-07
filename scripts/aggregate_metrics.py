#!/usr/bin/env python3
"""
Aggregate per-subject aligned_metrics.json files into a cross-subject summary.

Computes:
  • Pooled kill rates for Set N and Set G (sum of kills / sum of mutants)
  • Wilson 95% CI on each rate
  • Per-subject delta (kill_rate_N - kill_rate_G)
  • McNemar exact test on paired (mutant-level) Set N vs Set G outcomes
  • M1-M5 cross-subject means
"""

import argparse
import json
import math
from pathlib import Path

try:
    from scipy.stats import binomtest as _binomtest
    HAS_SCIPY = True
except ImportError:
    _binomtest = None
    HAS_SCIPY = False


def wilson_ci(k, n, z=1.96):
    """Wilson score interval for binomial proportion."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def mcnemar_exact(b, c):
    """
    Exact McNemar test on paired binary outcomes.
    b = N kills, G doesn't; c = G kills, N doesn't.
    H0: P(N kill alone) == P(G kill alone).
    Returns p-value (two-sided).
    """
    n = b + c
    if n == 0:
        return 1.0
    if HAS_SCIPY and _binomtest is not None:
        return _binomtest(min(b, c), n, p=0.5, alternative="two-sided").pvalue
    # Fallback exact binomial p-value
    k = min(b, c)
    p = 0.0
    for i in range(k + 1):
        p += math.comb(n, i) / (2 ** n)
    return min(1.0, 2 * p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", required=True)
    ap.add_argument("--output",      required=True)
    args = ap.parse_args()

    results_dir = Path(args.results_dir)
    per_subject = []
    for subj_dir in sorted(results_dir.iterdir()):
        if not subj_dir.is_dir():
            continue
        metrics_path = subj_dir / "aligned_metrics.json"
        if not metrics_path.exists():
            continue
        with open(metrics_path) as f:
            per_subject.append(json.load(f))

    if not per_subject:
        print(f"WARN: no aligned_metrics.json files under {results_dir}")
        return

    # Pooled totals
    total_mutants = sum(s["n_mutants"] for s in per_subject)
    total_n_kills = sum(s["set_n"]["n_killed"] for s in per_subject)
    total_g_kills = sum(s["set_g"]["n_killed"] for s in per_subject)

    # Effective-MR pool (see docs/METRICS.md §"Pooled Effective-MR Ratio").
    # `.get(..., 0)` keeps backward compatibility with per-subject JSONs
    # written before the field existed.
    total_n_mrs = sum(s["set_n"].get("n_mrs", 0) for s in per_subject)
    total_g_mrs = sum(s["set_g"].get("n_mrs", 0) for s in per_subject)
    total_n_eff = sum(s["set_n"].get("n_effective_mrs", 0) for s in per_subject)
    total_g_eff = sum(s["set_g"].get("n_effective_mrs", 0) for s in per_subject)

    # Per-mutant paired comparison (across all subjects)
    pair_b = pair_c = 0
    for s in per_subject:
        nv = s["set_n"]["kill_vector"]
        gv = s["set_g"]["kill_vector"]
        for i in range(len(nv)):
            if nv[i] and not gv[i]:
                pair_b += 1
            elif gv[i] and not nv[i]:
                pair_c += 1

    # Per-subject delta
    deltas = []
    for s in per_subject:
        if s["n_mutants"] == 0:
            continue
        kr_n = s["set_n"]["n_killed"] / s["n_mutants"]
        kr_g = s["set_g"]["n_killed"] / s["n_mutants"]
        deltas.append({
            "subject": s["subject"],
            "n_mutants": s["n_mutants"],
            "kill_rate_N": kr_n,
            "kill_rate_G": kr_g,
            "delta_NG": kr_n - kr_g,
        })

    summary = {
        "n_subjects": len(per_subject),
        "total_mutants": total_mutants,
        "set_n": {
            "kills": total_n_kills,
            "kill_rate": total_n_kills / max(1, total_mutants),
            "wilson_95_ci": wilson_ci(total_n_kills, total_mutants),
            "total_mrs": total_n_mrs,
            "effective_mrs": total_n_eff,
            "effective_mr_ratio": total_n_eff / max(1, total_n_mrs),
        },
        "set_g": {
            "kills": total_g_kills,
            "kill_rate": total_g_kills / max(1, total_mutants),
            "wilson_95_ci": wilson_ci(total_g_kills, total_mutants),
            "total_mrs": total_g_mrs,
            "effective_mrs": total_g_eff,
            "effective_mr_ratio": total_g_eff / max(1, total_g_mrs),
        },
        "paired_mcnemar": {
            "n_only_kills": pair_b,
            "g_only_kills": pair_c,
            "p_value_two_sided": mcnemar_exact(pair_b, pair_c),
        },
        "per_subject": deltas,
        "m_metrics_means": {
            metric: sum(s["m_metrics"].get(metric, 0.0) for s in per_subject) / len(per_subject)
            for metric in per_subject[0].get("m_metrics", {})
        },
    }

    with open(args.output, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nCross-subject summary written to {args.output}")
    print(f"  Set N: {total_n_kills}/{total_mutants} = {summary['set_n']['kill_rate']:.3f} "
          f"(95% CI: [{summary['set_n']['wilson_95_ci'][0]:.3f}, {summary['set_n']['wilson_95_ci'][1]:.3f}]) "
          f"| ER {total_n_eff}/{total_n_mrs} = {summary['set_n']['effective_mr_ratio']:.3f}")
    print(f"  Set G: {total_g_kills}/{total_mutants} = {summary['set_g']['kill_rate']:.3f} "
          f"(95% CI: [{summary['set_g']['wilson_95_ci'][0]:.3f}, {summary['set_g']['wilson_95_ci'][1]:.3f}]) "
          f"| ER {total_g_eff}/{total_g_mrs} = {summary['set_g']['effective_mr_ratio']:.3f}")
    print(f"  McNemar exact p = {summary['paired_mcnemar']['p_value_two_sided']:.4f}")


if __name__ == "__main__":
    main()
