#!/usr/bin/env python3
"""scripts/compare_sets.py — Set N (NOETHER) vs Set G (GenMorph) detection.

Reads per-subject results/seed<seed>/<subject>/{setn,setg}_mutants_killed.csv
(per-MR x per-mutant kill matrices) and reports, per subject and stratified by
domain (Math / Lang / Guava), each set's *union* kill vector over the subject's
shared mutant set.

Set N is deterministic (one hand-authored MR set). Set G (GenMorph) is
stochastic — the published CSV holds up to 12 seeds. We therefore bracket Set G
between two honest references:
  * Set G @ seed<seed>  — a single GP run (strict; 0 if that seed found no
                          FP-free MR, which genuinely happens, esp. on Lang/Guava)
  * Set G @ all-seeds   — union across all published seeds (GenMorph's best-case
                          potential across 12 runs)
and also report Set G's per-seed distribution (how many seeds yield any valid
MR, and the spread of kills). Paired McNemar (per-mutant, pooled) is computed
against each reference. Domains are never pooled blindly: meta-pattern MRs draw
power from explicit mathematical structure with algebraic operators, so Set N's
applicability scope differs from GenMorph's.
"""
import argparse
import csv
import glob
import json
import math
import os
import re
from collections import defaultdict
from math import comb

SEED_RE = re.compile(r"^assertions_seed(\d+)$")


def wilson(k, n, z=1.96):
    if n == 0:
        return [0.0, 0.0]
    p = k / n
    d = 1 + z * z / n
    center = p + z * z / (2 * n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round((center - half) / d, 4), round((center + half) / d, 4)]


def mcnemar_exact_p(b, c):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(comb(n, i) for i in range(k + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


def _rows(path):
    with open(path) as f:
        return list(csv.reader(f))


def union_vec(rows, experiment):
    """Exact (experiment, '*') union row -> kill vector, or None if absent."""
    for r in rows[1:]:
        if r[0] == experiment and r[1] == "*":
            return [int(x) for x in r[2:-1]]
    return None


def valid_mrs(rows, experiment):
    return sum(1 for r in rows[1:] if r[0] == experiment and r[1] != "*")


def setg_seed_distribution(rows):
    """{seed:int -> union kills} across all assertions_seed<NN> experiments."""
    dist = {}
    for r in rows[1:]:
        m = SEED_RE.match(r[0])
        if m and r[1] == "*":
            dist[int(m.group(1))] = sum(int(x) for x in r[2:-1])
    return dist


def lib_of(subject):
    return {"M": "Math", "L": "Lang", "G": "Guava"}[subject[0]]


def _paired(vn, vg):
    b = sum(1 for kn, kg in zip(vn, vg) if kg and not kn)   # Set G only
    c = sum(1 for kn, kg in zip(vn, vg) if kn and not kg)   # Set N only
    return b, c


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--results-dir", required=True)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    setg_exp = f"assertions_seed{args.seed}"
    setn_exp = f"setn_seed{args.seed}"

    per_subject = []
    agg = defaultdict(lambda: {"n_mut": 0, "subjects": 0,
                               "setn": 0, "setn_valid": 0,
                               "g_seed": 0, "g_seed_valid": 0, "b_seed": 0, "c_seed": 0,
                               "g_all": 0, "b_all": 0, "c_all": 0,
                               "g_seed_zero_subjects": 0})

    for setn_csv in sorted(glob.glob(os.path.join(args.results_dir, "*", "setn_mutants_killed.csv"))):
        subj = os.path.basename(os.path.dirname(setn_csv))
        setg_csv = os.path.join(os.path.dirname(setn_csv), "setg_mutants_killed.csv")
        rn = _rows(setn_csv)
        vn = union_vec(rn, setn_exp)
        if vn is None:
            continue
        nmut = len(vn)
        dom = lib_of(subj)
        setn_k = sum(vn)
        nv = valid_mrs(rn, setn_exp)

        g_seed_vec = g_all_vec = None
        g_seed_valid = 0
        seed_dist = {}
        if os.path.isfile(setg_csv):
            rg = _rows(setg_csv)
            g_seed_vec = union_vec(rg, setg_exp) or [0] * nmut
            g_all_vec = union_vec(rg, "*") or [0] * nmut
            g_seed_valid = valid_mrs(rg, setg_exp)
            seed_dist = setg_seed_distribution(rg)
            if len(g_seed_vec) != nmut or len(g_all_vec) != nmut:
                print(f"WARN {subj}: mutant-count mismatch; skipping Set G pairing")
                g_seed_vec = g_all_vec = None

        seeds_valid = sum(1 for v in seed_dist.values() if v > 0)
        rec = {"subject": subj, "domain": dom, "n_mutants": nmut,
               "setn_kills": setn_k, "setn_valid_mrs": nv,
               "setg_seed_kills": sum(g_seed_vec) if g_seed_vec else None,
               "setg_seed_valid_mrs": g_seed_valid,
               "setg_allseeds_kills": sum(g_all_vec) if g_all_vec else None,
               "setg_seeds_with_valid_mr": seeds_valid,
               "setg_seed_kill_dist": dict(sorted(seed_dist.items()))}
        per_subject.append(rec)

        for key in ("ALL", dom):
            a = agg[key]
            a["subjects"] += 1
            a["n_mut"] += nmut
            a["setn"] += setn_k
            a["setn_valid"] += nv
            if g_seed_vec is not None:
                a["g_seed"] += sum(g_seed_vec)
                a["g_seed_valid"] += g_seed_valid
                if sum(g_seed_vec) == 0:
                    a["g_seed_zero_subjects"] += 1
                b, c = _paired(vn, g_seed_vec); a["b_seed"] += b; a["c_seed"] += c
                a["g_all"] += sum(g_all_vec)
                b, c = _paired(vn, g_all_vec); a["b_all"] += b; a["c_all"] += c

    strata = {}
    for key, a in agg.items():
        nm = a["n_mut"] or 1
        strata[key] = {
            "subjects": a["subjects"], "mutants_total": a["n_mut"],
            "setn": {"kills": a["setn"], "rate": round(a["setn"] / nm, 4),
                     "wilson95": wilson(a["setn"], a["n_mut"]), "valid_mrs": a["setn_valid"]},
            "setg_seed": {"kills": a["g_seed"], "rate": round(a["g_seed"] / nm, 4),
                          "wilson95": wilson(a["g_seed"], a["n_mut"]),
                          "valid_mrs": a["g_seed_valid"],
                          "subjects_with_zero_valid_mr": a["g_seed_zero_subjects"]},
            "setg_allseeds": {"kills": a["g_all"], "rate": round(a["g_all"] / nm, 4),
                              "wilson95": wilson(a["g_all"], a["n_mut"])},
            "mcnemar_vs_seed": {"b_setg_only": a["b_seed"], "c_setn_only": a["c_seed"],
                                "exact_p": round(mcnemar_exact_p(a["b_seed"], a["c_seed"]), 4)},
            "mcnemar_vs_allseeds": {"b_setg_only": a["b_all"], "c_setn_only": a["c_all"],
                                    "exact_p": round(mcnemar_exact_p(a["b_all"], a["c_all"]), 4)},
        }

    out = {"seed": args.seed, "n_subjects": len(per_subject), "strata": strata,
           "per_subject": sorted(per_subject, key=lambda r: r["subject"])}
    with open(args.output, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Comparison written to {args.output}")
    for key in ("ALL", "Math", "Lang", "Guava"):
        if key in strata:
            s = strata[key]
            print(f"[{key}] {s['subjects']}subj {s['mutants_total']}mut | "
                  f"N {s['setn']['kills']}({s['setn']['rate']:.2f}) | "
                  f"G@seed {s['setg_seed']['kills']}({s['setg_seed']['rate']:.2f}) | "
                  f"G@all {s['setg_allseeds']['kills']}({s['setg_allseeds']['rate']:.2f}) | "
                  f"McN(N v seed) b={s['mcnemar_vs_seed']['b_setg_only']} "
                  f"c={s['mcnemar_vs_seed']['c_setn_only']} p={s['mcnemar_vs_seed']['exact_p']}")


if __name__ == "__main__":
    main()
