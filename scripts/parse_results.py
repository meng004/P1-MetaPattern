#!/usr/bin/env python3
"""
Parse one subject's EvaluateMRs output into per-set kill matrices.

Inputs:
  --csv         mutants_killed.csv from EvaluateMRs
                Schema: EXPERIMENT,MR,M1..Mn,COUNT (one row per MR per seed)
  --status      mrs_status.csv from EvaluateMRs
                Schema: EXPERIMENT,MR,FP,MS,...  (FP rate column for invalidity check)
  --set-n-dir   directory holding our Set N MR files (used to discriminate
                MR rows belonging to Set N vs Set G)
  --output      aligned_metrics.json output path

Output JSON:
  {
    "subject":          "<subject>",
    "n_mutants":        25,
    "n_total_mrs":      8,
    "set_n":  {"n_mrs": 4, "n_effective_mrs": 3, "effective_mr_ratio": 0.75,
               "kill_vector": [..], "n_killed": 5},
    "set_g":  {"n_mrs": 4, "n_effective_mrs": 2, "effective_mr_ratio": 0.50,
               "kill_vector": [..], "n_killed": 17},
    "per_mr":  [{"mr": "rho_perm", "set": "N", "fp": 0.0, "n_killed": 2,
                 "killed_indices": [4, 12]}, ...],
    "m_metrics": {"M1_kill_rate_N": ..., ..., "M5_complementarity_lift": ...}
  }

See docs/METRICS.md for the full definition of each field.
"""

import argparse
import csv
import json
import os
import re
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--csv",       required=True)
    p.add_argument("--status",    default=None)
    p.add_argument("--set-n-dir", required=True)
    p.add_argument("--output",    required=True)
    return p.parse_args()


def load_set_n_mr_names(set_n_dir):
    """Return set of Set N MR identifiers expected in the CSV (e.g. {'rho_perm', ...})."""
    names = set()
    if not os.path.isdir(set_n_dir):
        return names
    for fn in os.listdir(set_n_dir):
        m = re.match(r".+@(.+)\.jir\.txt$", fn)
        if m:
            names.add(m.group(1))
    return names


def parse_csv(csv_path):
    """Yield (experiment, mr_name, kill_vector_int_list, count) per CSV row."""
    rows = []
    with open(csv_path, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        # Header: EXPERIMENT,MR,M1,M2,...,Mn,COUNT
        m_cols = [i for i, c in enumerate(header) if re.match(r"^M\d+$", c)]
        count_col = header.index("COUNT") if "COUNT" in header else len(header) - 1
        for row in reader:
            exp = row[0]
            mr = row[1]
            kills = [int(row[i]) for i in m_cols]
            count = int(row[count_col])
            rows.append({"exp": exp, "mr": mr, "kills": kills, "count": count})
    return rows, len(m_cols)


def parse_status(status_path):
    """Return dict {(exp, mr): fp_rate (float in [0, 1])}."""
    fp = {}
    if status_path is None or not os.path.isfile(status_path):
        return fp
    with open(status_path, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        try:
            i_exp = header.index("EXPERIMENT")
            i_mr  = header.index("MR")
            i_fp  = header.index("FP")
        except ValueError:
            return fp
        for row in reader:
            try:
                # FP column may be like "0.00%" or "5.0%"
                v = row[i_fp].strip().rstrip("%")
                fp_val = float(v) / 100.0 if "%" in row[i_fp] else float(v)
                fp[(row[i_exp], row[i_mr])] = fp_val
            except (ValueError, IndexError):
                continue
    return fp


def classify_mr(mr_name, set_n_names):
    """Return 'N' if MR belongs to Set N, else 'G' (GenMorph upstream)."""
    return "N" if mr_name in set_n_names else "G"


def union_kills(rows, n_mutants):
    union = [0] * n_mutants
    for r in rows:
        for i, k in enumerate(r["kills"]):
            if k:
                union[i] = 1
    return union


def kill_count(vec):
    return sum(1 for k in vec if k)


def n_effective_mrs(rows):
    """Count MRs in `rows` that kill at least one mutant.

    Effective-MR Ratio (docs/METRICS.md §"Effective-MR Ratio") = this
    count / len(rows). Captures MR-level utilization, complementing M2.
    """
    return sum(1 for r in rows if any(r["kills"]))


def m_metrics(set_n_rows, set_g_rows, n_mutants):
    """Compute M1-M5 efficiency metrics (per the paper's protocol)."""
    n_kills = union_kills(set_n_rows, n_mutants)
    g_kills = union_kills(set_g_rows, n_mutants)

    n_only = [n_kills[i] and not g_kills[i] for i in range(n_mutants)]
    g_only = [g_kills[i] and not n_kills[i] for i in range(n_mutants)]
    both   = [n_kills[i] and g_kills[i] for i in range(n_mutants)]

    n_set_size = max(1, len(set_n_rows))
    g_set_size = max(1, len(set_g_rows))

    return {
        "M1_kill_rate_N": kill_count(n_kills) / max(1, n_mutants),
        "M1_kill_rate_G": kill_count(g_kills) / max(1, n_mutants),
        "M2_kills_per_mr_N": kill_count(n_kills) / n_set_size,
        "M2_kills_per_mr_G": kill_count(g_kills) / g_set_size,
        "M3_unique_to_N": kill_count(n_only),
        "M3_unique_to_G": kill_count(g_only),
        "M3_overlap": kill_count(both),
        "M4_jaccard_NG": kill_count(both) / max(1, kill_count(n_kills) + kill_count(g_kills) - kill_count(both)),
        "M5_complementarity_lift": (kill_count(n_kills) + kill_count(g_kills) - kill_count(both)) / max(1, n_mutants)
                                   - max(kill_count(n_kills), kill_count(g_kills)) / max(1, n_mutants),
    }


def main():
    args = parse_args()

    set_n_names = load_set_n_mr_names(args.set_n_dir)
    rows, n_mutants = parse_csv(args.csv)
    fp_map = parse_status(args.status)

    # Group by set
    set_n_rows = [r for r in rows if classify_mr(r["mr"], set_n_names) == "N"]
    set_g_rows = [r for r in rows if classify_mr(r["mr"], set_n_names) == "G"]

    # Per-MR detail
    per_mr = []
    for r in rows:
        sset = classify_mr(r["mr"], set_n_names)
        fp = fp_map.get((r["exp"], r["mr"]), None)
        per_mr.append({
            "experiment": r["exp"],
            "mr": r["mr"],
            "set": sset,
            "fp": fp,
            "n_killed": kill_count(r["kills"]),
            "killed_indices": [i for i, k in enumerate(r["kills"]) if k],
        })

    # Subject from output path heuristic
    subject = Path(args.csv).parent.name

    n_eff_n = n_effective_mrs(set_n_rows)
    n_eff_g = n_effective_mrs(set_g_rows)
    out = {
        "subject": subject,
        "n_mutants": n_mutants,
        "n_total_mrs": len(rows),
        "set_n": {
            "n_mrs": len(set_n_rows),
            "n_effective_mrs": n_eff_n,
            "effective_mr_ratio": n_eff_n / max(1, len(set_n_rows)),
            "kill_vector": union_kills(set_n_rows, n_mutants),
            "n_killed": kill_count(union_kills(set_n_rows, n_mutants)),
        },
        "set_g": {
            "n_mrs": len(set_g_rows),
            "n_effective_mrs": n_eff_g,
            "effective_mr_ratio": n_eff_g / max(1, len(set_g_rows)),
            "kill_vector": union_kills(set_g_rows, n_mutants),
            "n_killed": kill_count(union_kills(set_g_rows, n_mutants)),
        },
        "per_mr": per_mr,
        "m_metrics": m_metrics(set_n_rows, set_g_rows, n_mutants),
    }

    with open(args.output, "w") as f:
        json.dump(out, f, indent=2)
    print(f"  parsed {len(set_n_rows)} Set N + {len(set_g_rows)} Set G MRs against {n_mutants} mutants → {args.output}")


if __name__ == "__main__":
    main()
