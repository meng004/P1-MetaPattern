"""
Parse upstream's mutants_killed.csv (augmented with Set N rows) into
aligned_metrics.json.

The CSV from EvaluateMRs has format:
    EXPERIMENT,MR,M1,M2,...,M25,COUNT
where MR can be MR0..MR3 (Set G) or rho_perm/rho_scale/... (Set N).

Output JSON contains the full per-MR per-mutant kill matrix plus the
M1-M5 efficiency metrics computed in aligned conditions.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List

import pandas as pd  # type: ignore[import-untyped]


SET_N_PATTERNS = [r"^rho_", r"^Rho", r"^Greek_"]  # heuristic: anything not "MR\d+"
SET_G_PATTERNS = [r"^MR\d+$"]


def _classify(mr_name: str) -> str:
    for p in SET_G_PATTERNS:
        if re.match(p, mr_name):
            return "set_g"
    for p in SET_N_PATTERNS:
        if re.match(p, mr_name):
            return "set_n"
    return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, type=Path,
                        help="Augmented mutants_killed.csv from EvaluateMRs")
    parser.add_argument("--status-csv", type=Path, default=None,
                        help="Optional mrs_status.csv for FP rates")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"ERROR: {args.csv} not found")
        return 1

    df = pd.read_csv(args.csv)
    seed_label = f"assertions_seed{args.seed}"
    df_seed = df[df["EXPERIMENT"] == seed_label]
    if df_seed.empty:
        print(f"ERROR: no rows match EXPERIMENT={seed_label}")
        return 2

    # Drop the "*" union row if present; we'll recompute per-set unions
    df_per_mr = df_seed[df_seed["MR"] != "*"].copy()

    mut_cols = [c for c in df.columns if c.startswith("M") and c[1:].isdigit()]

    # Per-MR kill counts
    df_per_mr["kill_count"] = df_per_mr[mut_cols].sum(axis=1)
    df_per_mr["set_label"] = df_per_mr["MR"].apply(_classify)

    # Aggregate per-set kill: union over MRs in each set
    set_n_kill_vec = (df_per_mr[df_per_mr["set_label"] == "set_n"][mut_cols].sum(axis=0) > 0).astype(int)
    set_g_kill_vec = (df_per_mr[df_per_mr["set_label"] == "set_g"][mut_cols].sum(axis=0) > 0).astype(int)
    n_mutants = len(mut_cols)

    # M1: EMR
    def _emr(per_mr_kills: Dict[str, int], threshold: float = 1.0) -> Dict:
        if not per_mr_kills:
            return {"emr": 0.0, "k": 0, "m": 0}
        sorted_v = sorted(per_mr_kills.values(), reverse=True)
        m = len(sorted_v)
        total = sum(sorted_v)
        if total == 0:
            return {"emr": 0.0, "k": 0, "m": m}
        cum = 0
        for k, v in enumerate(sorted_v, start=1):
            cum += v
            if cum >= threshold * total:
                return {"emr": round(k / m, 4), "k": k, "m": m}
        return {"emr": 1.0, "k": m, "m": m}

    set_n_kills_per_mr = {row["MR"]: int(row["kill_count"])
                          for _, row in df_per_mr[df_per_mr["set_label"] == "set_n"].iterrows()}
    set_g_kills_per_mr = {row["MR"]: int(row["kill_count"])
                          for _, row in df_per_mr[df_per_mr["set_label"] == "set_g"].iterrows()}

    # M2: WDP
    def _wdp(per_mr_kills: Dict[str, int]) -> Dict:
        if not per_mr_kills:
            return {"workhorse": None, "kills": 0, "wdp": 0.0}
        wh = max(per_mr_kills, key=lambda k: per_mr_kills[k])
        return {"workhorse": wh, "kills": int(per_mr_kills[wh]),
                "wdp": round(per_mr_kills[wh] / n_mutants, 4)}

    # Per-mutant overlap analysis
    overlap = {
        "both_sets": int(((set_n_kill_vec == 1) & (set_g_kill_vec == 1)).sum()),
        "n_only": int(((set_n_kill_vec == 1) & (set_g_kill_vec == 0)).sum()),
        "g_only": int(((set_n_kill_vec == 0) & (set_g_kill_vec == 1)).sum()),
        "neither": int(((set_n_kill_vec == 0) & (set_g_kill_vec == 0)).sum()),
    }

    # FP rates if available
    fp_data: Dict[str, str] = {}
    if args.status_csv and args.status_csv.exists():
        status_df = pd.read_csv(args.status_csv)
        status_df = status_df[status_df["EXPERIMENT"] == seed_label]
        for _, row in status_df.iterrows():
            fp_data[str(row["MR"])] = str(row.get("FP", ""))

    out = {
        "subject": args.subject,
        "seed": args.seed,
        "n_mutants": n_mutants,
        "alignment_mode": "upstream_pipeline_substrate",
        "set_n": {
            "members": list(set_n_kills_per_mr.keys()),
            "per_mr_kills": set_n_kills_per_mr,
            "union_kills": int(set_n_kill_vec.sum()),
            "rate": round(int(set_n_kill_vec.sum()) / n_mutants, 4),
            "M1_emr_1.0": _emr(set_n_kills_per_mr, 1.0),
            "M1_emr_0.8": _emr(set_n_kills_per_mr, 0.8),
            "M2_wdp": _wdp(set_n_kills_per_mr),
        },
        "set_g": {
            "members": list(set_g_kills_per_mr.keys()),
            "per_mr_kills": set_g_kills_per_mr,
            "union_kills": int(set_g_kill_vec.sum()),
            "rate": round(int(set_g_kill_vec.sum()) / n_mutants, 4),
            "M1_emr_1.0": _emr(set_g_kills_per_mr, 1.0),
            "M1_emr_0.8": _emr(set_g_kills_per_mr, 0.8),
            "M2_wdp": _wdp(set_g_kills_per_mr),
        },
        "overlap": overlap,
        "fp_rates": fp_data,
        "raw_kill_matrix": {
            row["MR"]: {col: int(row[col]) for col in mut_cols}
            for _, row in df_per_mr.iterrows()
        },
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2))
    print(f"Wrote {args.output}")
    print(f"  Set N: {out['set_n']['union_kills']}/{n_mutants} ({out['set_n']['rate']*100:.1f}%)")
    print(f"  Set G: {out['set_g']['union_kills']}/{n_mutants} ({out['set_g']['rate']*100:.1f}%)")
    print(f"  Overlap: both={overlap['both_sets']}, n_only={overlap['n_only']}, g_only={overlap['g_only']}, neither={overlap['neither']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
