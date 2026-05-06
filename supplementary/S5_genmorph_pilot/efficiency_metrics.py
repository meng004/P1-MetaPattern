"""
Efficiency / separation metrics on top of per-MR kill data.

Implements the 5-tier metric framework for disentangling kill-rate effects:
  M1  Effective MR Ratio (EMR_τ)         — fraction of MRs covering top-τ kill volume
  M2  Workhorse MR Detection Power (WDP) — single-MR maximum kill rate
  M3  Generation Cost per Effective MR   — per-EMR human/CPU effort
  M4  Mutator-Class Diversity (MCD)      — distinct PIT mutators each MR catches
  M5  Pareto Frontier (kill-rate, cost)  — multi-objective comparison

Inputs: results.csv from parse_pit_xml.py (with mr_<test_name> per-MR columns)

Output: efficiency_metrics.json — pooled or per-subject metric report.

Usage:
    python efficiency_metrics.py \\
        --results results/gcd/results.csv results/sin/results.csv \\
        --subjects gcd sin \\
        --output results/efficiency_metrics.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import pandas as pd  # type: ignore[import-untyped]


# Per-subject MR-name → set membership (must match parse_pit_xml.py SUBJECT_REGISTRY)
MR_SETS = {
    "gcd": {
        "set_n": {"testRhoPerm", "testRhoScale", "testRhoMono", "testRhoEqRef"},
        "set_g": {"testGenMorphMR0", "testGenMorphMR1", "testGenMorphMR2", "testGenMorphMR3"},
    },
    "sin": {
        "set_n": {"testRhoOddSym", "testRhoPeriod", "testRhoBound", "testRhoComplement"},
        "set_g": {"testGenMorphMR20", "testGenMorphMR21", "testGenMorphMR22", "testGenMorphMR23"},
    },
}

# Generation-cost approximations (seconds per MR-set-of-4).
# NOETHER: human algebraic derivation + CONSTRUCT-MP runtime (well under 1 s).
# GenMorph: GP runtime per upstream paper (Ayerdi et al. 2023 reports
# ~hour-scale per subject for evolutionary MR synthesis on a single
# Java method; we use 1 hour = 3600 s as a defensible mid-estimate).
GEN_COST_PER_SET = {
    "set_n": 600,    # 10 min algebraic derivation by domain expert
    "set_g": 3600,   # 1 hour GP runtime per subject (upstream estimate)
    "set_b": 60,     # 1 min trivial baseline
}


def _emr(per_mr_kills: Dict[str, int], threshold: float = 1.0) -> Dict:
    """Effective MR Ratio at coverage threshold τ."""
    if not per_mr_kills:
        return {"emr": 0.0, "k": 0, "m": 0, "covered_fraction": 0.0}
    sorted_kills = sorted(per_mr_kills.values(), reverse=True)
    total = sum(sorted_kills)
    m = len(sorted_kills)
    if total == 0:
        return {"emr": 0.0, "k": 0, "m": m, "covered_fraction": 0.0}
    cum = 0
    for k, v in enumerate(sorted_kills, start=1):
        cum += v
        if cum >= threshold * total:
            return {
                "emr": round(k / m, 4),
                "k": k,
                "m": m,
                "covered_fraction": round(cum / total, 4),
            }
    return {"emr": 1.0, "k": m, "m": m, "covered_fraction": 1.0}


def _wdp(per_mr_kills: Dict[str, int], n_mutants: int) -> Dict:
    """Workhorse MR Detection Power."""
    if not per_mr_kills or n_mutants == 0:
        return {"workhorse": None, "kills": 0, "wdp": 0.0}
    workhorse = max(per_mr_kills, key=lambda k: per_mr_kills[k])
    kills = per_mr_kills[workhorse]
    return {
        "workhorse": workhorse,
        "kills": int(kills),
        "wdp": round(kills / n_mutants, 4),
    }


def _gce(set_name: str, emr_dict: Dict) -> Dict:
    """Generation Cost per Effective MR."""
    cost = GEN_COST_PER_SET.get(set_name, 0)
    n_eff = emr_dict["k"] if emr_dict else 0
    if n_eff == 0:
        return {"set": set_name, "total_cost_sec": cost, "n_effective_mrs": 0,
                "cost_per_effective_mr": float("inf")}
    return {
        "set": set_name,
        "total_cost_sec": cost,
        "n_effective_mrs": n_eff,
        "cost_per_effective_mr_sec": round(cost / n_eff, 1),
    }


def _mcd(df: pd.DataFrame, mr_columns: List[str]) -> Dict:
    """Mutator-Class Diversity per workhorse MR."""
    out = {}
    for c in mr_columns:
        kills = df[df[c] == 1]
        classes = kills["mutation_class"].unique().tolist()
        # Strip status-only kills (TIMED_OUT) which don't belong to a real mutator
        # — actually mutation_class IS the real mutator regardless of pit_status,
        # so we keep them.
        out[c.replace("mr_", "")] = {
            "kills": int(len(kills)),
            "n_mutator_classes": len(classes),
            "mutator_classes": sorted(classes),
        }
    return out


def _per_subject_metrics(df: pd.DataFrame, subject: str) -> Dict:
    """Compute M1-M4 for a single subject's results.csv."""
    n = len(df)
    if n == 0:
        return {"subject": subject, "n_mutants": 0, "error": "empty"}

    mr_cols = [c for c in df.columns if c.startswith("mr_")]
    n_set_cfg = MR_SETS.get(subject, {})
    set_n_tests = n_set_cfg.get("set_n", set())
    set_g_tests = n_set_cfg.get("set_g", set())

    # Per-MR kills (excluding TIMED_OUT inflation — count only real assertion failures)
    real_kills = df[df["pit_status"] == "KILLED"]

    set_n_kills = {tm: int(real_kills[f"mr_{tm}"].sum()) for tm in set_n_tests if f"mr_{tm}" in df.columns}
    set_g_kills = {tm: int(real_kills[f"mr_{tm}"].sum()) for tm in set_g_tests if f"mr_{tm}" in df.columns}

    metrics = {
        "subject": subject,
        "n_mutants": int(n),
        "set_n": {
            "per_mr_kills": set_n_kills,
            "total_real_kills": sum(set_n_kills.values()),
            "kill_rate_with_infra": round(int(df["set_n_detected"].sum()) / n, 4),
            "M1_emr_1.0": _emr(set_n_kills, threshold=1.0),
            "M1_emr_0.8": _emr(set_n_kills, threshold=0.8),
            "M2_wdp": _wdp(set_n_kills, n),
            "M3_gce": _gce("set_n", _emr(set_n_kills, threshold=1.0)),
            "M4_mcd": _mcd(real_kills, [f"mr_{t}" for t in set_n_tests if f"mr_{t}" in df.columns]),
        },
        "set_g": {
            "per_mr_kills": set_g_kills,
            "total_real_kills": sum(set_g_kills.values()),
            "kill_rate_with_infra": round(int(df["set_g_detected"].sum()) / n, 4),
            "M1_emr_1.0": _emr(set_g_kills, threshold=1.0),
            "M1_emr_0.8": _emr(set_g_kills, threshold=0.8),
            "M2_wdp": _wdp(set_g_kills, n),
            "M3_gce": _gce("set_g", _emr(set_g_kills, threshold=1.0)),
            "M4_mcd": _mcd(real_kills, [f"mr_{t}" for t in set_g_tests if f"mr_{t}" in df.columns]),
        },
    }
    return metrics


def _pooled_metrics(per_subject_metrics: List[Dict]) -> Dict:
    """Aggregate metrics across subjects (M5 Pareto context)."""
    n_subjects = len(per_subject_metrics)
    if n_subjects == 0:
        return {}

    pooled_n = sum(m["n_mutants"] for m in per_subject_metrics)
    pooled_set_n_kills = sum(m["set_n"]["total_real_kills"] for m in per_subject_metrics)
    pooled_set_g_kills = sum(m["set_g"]["total_real_kills"] for m in per_subject_metrics)

    # For Pareto plot context:
    pareto_points = []
    for m in per_subject_metrics:
        for set_name in ("set_n", "set_g"):
            kr = m[set_name]["kill_rate_with_infra"]
            cost = m[set_name]["M3_gce"].get("total_cost_sec", 0)
            pareto_points.append({
                "subject": m["subject"],
                "set": set_name,
                "kill_rate": kr,
                "generation_cost_sec": cost,
            })

    return {
        "n_subjects": n_subjects,
        "pooled_n_mutants": pooled_n,
        "pooled_set_n_real_kills": pooled_set_n_kills,
        "pooled_set_g_real_kills": pooled_set_g_kills,
        "pooled_set_n_rate": round(pooled_set_n_kills / pooled_n, 4) if pooled_n else 0,
        "pooled_set_g_rate": round(pooled_set_g_kills / pooled_n, 4) if pooled_n else 0,
        "pareto_points": pareto_points,
        "transfer_cost_ratio_for_n_subjects": {
            "n": n_subjects,
            "noether_total_sec": GEN_COST_PER_SET["set_n"] * n_subjects,
            "genmorph_total_sec": GEN_COST_PER_SET["set_g"] * n_subjects,
            "ratio": round(GEN_COST_PER_SET["set_g"] / GEN_COST_PER_SET["set_n"], 2),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True, nargs="+", type=Path,
                        help="One or more results.csv paths (per subject)")
    parser.add_argument("--subjects", required=True, nargs="+",
                        help="Subject names (gcd, sin, ...) matching --results order")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if len(args.results) != len(args.subjects):
        print("ERROR: --results and --subjects must have same length")
        return 1

    per_subject = []
    for results_path, subject in zip(args.results, args.subjects):
        df = pd.read_csv(results_path)
        per_subject.append(_per_subject_metrics(df, subject))

    pooled = _pooled_metrics(per_subject)

    out = {
        "per_subject": per_subject,
        "pooled": pooled,
        "metric_definitions": {
            "M1_emr": "Effective MR Ratio: smallest fraction of MRs covering threshold τ of total kills (real KILLED status only).",
            "M2_wdp": "Workhorse Detection Power: best single MR's kill rate over the full mutant set.",
            "M3_gce": "Generation Cost per Effective MR: total set generation cost / number of effective MRs.",
            "M4_mcd": "Mutator-Class Diversity: distinct PIT mutator classes among each MR's kills.",
            "M5_pareto": "Multi-objective points (kill_rate, generation_cost) for Pareto-frontier analysis.",
        },
        "cost_assumptions": GEN_COST_PER_SET,
        "notes": [
            "Real kills exclude PIT TIMED_OUT/MEMORY_ERROR/RUN_ERROR (those are infrastructure-attributed to all sets).",
            "GenMorph generation cost (3600s = 1h per subject) is from upstream paper estimation; replace with measured runtime if available.",
            "Pareto comparison should be plotted in 2D (kill_rate vs cost); on a log-cost axis the trade-off is clearer.",
        ],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2))
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
