"""
Compute pilot statistics from results.csv → pilot_stats.json.

Outputs:
  - per-set detection rate with Wilson 95% CI
  - pairwise McNemar exact and Fisher exact for (N vs G), (N vs B), (G vs B)
  - union(N, G) detection rate

Usage:
    python stats.py --results results/results.csv --output results/pilot_stats.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd  # type: ignore[import-untyped]
from scipy.stats import fisher_exact  # type: ignore[import-untyped]
from statsmodels.stats.contingency_tables import mcnemar  # type: ignore[import-untyped]
from statsmodels.stats.proportion import proportion_confint  # type: ignore[import-untyped]


def _wilson_ci(detected: int, total: int) -> list[float]:
    if total == 0:
        return [0.0, 1.0]
    lo, hi = proportion_confint(detected, total, alpha=0.05, method="wilson")
    return [round(float(lo), 4), round(float(hi), 4)]


def _set_summary(df: pd.DataFrame, col: str) -> dict:
    n = len(df)
    detected = int(df[col].sum())
    rate = detected / n if n else 0.0
    return {
        "detected": detected,
        "n": n,
        "rate": round(rate, 4),
        "wilson_95ci": _wilson_ci(detected, n),
    }


def _pairwise(df: pd.DataFrame, col_a: str, col_b: str) -> dict:
    # 2x2 table: rows = a (1 / 0), cols = b (1 / 0)
    both = int(((df[col_a] == 1) & (df[col_b] == 1)).sum())
    a_only = int(((df[col_a] == 1) & (df[col_b] == 0)).sum())
    b_only = int(((df[col_a] == 0) & (df[col_b] == 1)).sum())
    neither = int(((df[col_a] == 0) & (df[col_b] == 0)).sum())

    # McNemar exact on the discordant pairs (a_only, b_only)
    table = [[both, a_only], [b_only, neither]]
    try:
        mcnemar_res = mcnemar(table=table, exact=True, correction=False)
        mcnemar_p = float(mcnemar_res.pvalue)
    except Exception:  # noqa: BLE001
        mcnemar_p = float("nan")

    # Fisher exact on the marginals
    a_total = both + a_only
    a_undet = b_only + neither
    b_total = both + b_only
    b_undet = a_only + neither
    fisher_table = [[a_total, a_undet], [b_total, b_undet]]
    _, fisher_p = fisher_exact(fisher_table)
    fisher_p = float(fisher_p)

    return {
        "both": both,
        f"{col_a}_only": a_only,
        f"{col_b}_only": b_only,
        "neither": neither,
        "mcnemar_p": round(mcnemar_p, 4) if mcnemar_p == mcnemar_p else None,
        "fisher_p": round(fisher_p, 4),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    df = pd.read_csv(args.results)
    if df.empty:
        raise ValueError(f"results.csv at {args.results} is empty")

    out = {
        "subject": df["subject"].iloc[0] if "subject" in df.columns else "unknown",
        "n_mutations": int(len(df)),
        "set_n": _set_summary(df, "set_n_detected"),
        "set_g": _set_summary(df, "set_g_detected"),
        "set_b": _set_summary(df, "set_b_detected"),
        "pairwise": {
            "n_vs_g": _pairwise(df, "set_n_detected", "set_g_detected"),
            "n_vs_b": _pairwise(df, "set_n_detected", "set_b_detected"),
            "g_vs_b": _pairwise(df, "set_g_detected", "set_b_detected"),
        },
    }

    union_detected = int(((df["set_n_detected"] == 1) | (df["set_g_detected"] == 1)).sum())
    out["union_n_g"] = {
        "detected": union_detected,
        "n": int(len(df)),
        "rate": round(union_detected / len(df), 4),
        "wilson_95ci": _wilson_ci(union_detected, len(df)),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
