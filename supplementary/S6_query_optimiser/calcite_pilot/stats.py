"""
Compute Calcite pilot statistics from results.csv → pilot_stats.json.

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


def _set_summary(df: pd.DataFrame, applicable_col: str, detected_col: str) -> dict:
    n = len(df)
    n_app = int(df[applicable_col].sum())
    detected = int(df[detected_col].sum())
    return {
        "n_applicable": n_app,
        "detected": detected,
        "n": n,
        "rate_overall": round(detected / n if n else 0.0, 4),
        "rate_when_applicable": round(detected / n_app if n_app else 0.0, 4),
        "wilson_95ci_overall": _wilson_ci(detected, n),
    }


def _pairwise(df: pd.DataFrame) -> dict:
    a = df["set_n_detected"]
    b = df["set_segura_detected"]
    both = int(((a == 1) & (b == 1)).sum())
    a_only = int(((a == 1) & (b == 0)).sum())
    b_only = int(((a == 0) & (b == 1)).sum())
    neither = int(((a == 0) & (b == 0)).sum())
    table = [[both, a_only], [b_only, neither]]
    try:
        m = mcnemar(table=table, exact=True, correction=False)
        m_p = float(m.pvalue)
    except Exception:  # noqa: BLE001
        m_p = float("nan")
    a_total = both + a_only
    a_undet = b_only + neither
    b_total = both + b_only
    b_undet = a_only + neither
    _, fp = fisher_exact([[a_total, a_undet], [b_total, b_undet]])
    return {
        "both": both,
        "n_only": a_only,
        "segura_only": b_only,
        "neither": neither,
        "mcnemar_p": round(m_p, 4) if m_p == m_p else None,
        "fisher_p_n_vs_segura": round(float(fp), 4),
    }


def _by_complexity(df: pd.DataFrame) -> dict:
    out = {}
    for d in ("easy", "medium", "hard"):
        sub = df[df["complexity"] == d]
        if len(sub) == 0:
            out[d] = {"n": 0, "set_n_rate": 0.0, "set_segura_rate": 0.0}
            continue
        out[d] = {
            "n": int(len(sub)),
            "set_n_rate": round(float(sub["set_n_detected"].mean()), 4),
            "set_segura_rate": round(float(sub["set_segura_detected"].mean()), 4),
        }
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--label", default=None,
                        help="Subject label written to pilot_stats.json (defaults to 'Calcite_QED_<n>pair')")
    args = parser.parse_args()

    df = pd.read_csv(args.results)
    if df.empty:
        raise ValueError(f"results.csv at {args.results} is empty")

    set_n = _set_summary(df, "set_n_applicable", "set_n_detected")
    set_segura = _set_summary(df, "set_segura_applicable", "set_segura_detected")
    union_detected = int(((df["set_n_detected"] == 1) | (df["set_segura_detected"] == 1)).sum())

    label = args.label or f"Calcite_QED_{len(df)}pair"
    out = {
        "subject": label,
        "n_pairs": int(len(df)),
        "stratification": {
            d: int((df["complexity"] == d).sum()) for d in ("easy", "medium", "hard")
        },
        "set_n": set_n,
        "set_segura": set_segura,
        "union_n_segura": {
            "detected": union_detected,
            "n": int(len(df)),
            "rate": round(union_detected / len(df), 4),
            "wilson_95ci": _wilson_ci(union_detected, int(len(df))),
        },
        "complementary_value": _pairwise(df),
        "by_complexity": _by_complexity(df),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
