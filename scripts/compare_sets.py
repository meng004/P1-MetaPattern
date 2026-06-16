#!/usr/bin/env python3
"""scripts/compare_sets.py — Set N (NOETHER) vs Set G (GenMorph) detection.

Reads per-subject results/seed<seed>/<subject>/{setn,setg}_mutants_killed.csv
(the per-MR x per-mutant kill matrices), takes each set's *union* kill vector
over the subject's shared mutant set, and reports:
  * per subject: mutants, Set N union kills, Set G union kills, valid-MR counts
  * pooled (overall) and stratified by domain (Math / Lang / Guava):
        kill rate + Wilson 95% CI for each set, and paired McNemar on the
        per-mutant outcomes (b = Set G only, c = Set N only).

Domain matters: meta-pattern (NOETHER) MRs draw their power from explicit
mathematical/physical structure with algebraic operators, so Set N is expected
to be strong on Math and to have a narrower applicability scope on the
String/Sequence (Lang/Guava) subjects — hence we never pool blindly.
"""
import argparse
import csv
import glob
import json
import math
import os
from collections import defaultdict
from math import comb


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


def union_vec(path, experiment):
    """Union (logical-OR) kill vector for `experiment`'s MRs; fallback to *,*.."""
    rows = _rows(path)
    muts = rows[0][2:-1]
    for want in ((experiment, "*"), ("*", "*")):
        for r in rows[1:]:
            if (r[0], r[1]) == want:
                return muts, [int(x) for x in r[2:-1]]
    return muts, None


def valid_mrs(path, experiment):
    """Count of valid (FP-free, hence present) MR rows for `experiment`."""
    return sum(1 for r in _rows(path)[1:] if r[0] == experiment and r[1] != "*")


def lib_of(subject):
    return {"M": "Math", "L": "Lang", "G": "Guava"}[subject[0]]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--results-dir", required=True)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    setg_exp = f"assertions_seed{args.seed}"
    setn_exp = f"setn_seed{args.seed}"

    per_subject = []
    # pooled paired counts, overall + per domain
    agg = defaultdict(lambda: {"n_mut": 0, "setn": 0, "setg": 0, "b": 0, "c": 0,
                               "setn_valid": 0, "setg_valid": 0, "subjects": 0})

    for setn_csv in sorted(glob.glob(os.path.join(args.results_dir, "*", "setn_mutants_killed.csv"))):
        subj = os.path.basename(os.path.dirname(setn_csv))
        setg_csv = os.path.join(os.path.dirname(setn_csv), "setg_mutants_killed.csv")
        muts_n, vn = union_vec(setn_csv, setn_exp)
        if vn is None:
            continue
        vg = None
        if os.path.isfile(setg_csv):
            muts_g, vg = union_vec(setg_csv, setg_exp)
            if vg is not None and len(vg) != len(vn):
                print(f"WARN {subj}: mutant count mismatch N={len(vn)} G={len(vg)}; skipping G")
                vg = None
        dom = lib_of(subj)
        setn_k = sum(vn)
        setg_k = sum(vg) if vg else None
        nv = valid_mrs(setn_csv, setn_exp)
        gv = valid_mrs(setg_csv, setg_exp) if os.path.isfile(setg_csv) else 0
        rec = {"subject": subj, "domain": dom, "n_mutants": len(vn),
               "setn_kills": setn_k, "setg_kills": setg_k,
               "setn_valid_mrs": nv, "setg_valid_mrs": gv}
        per_subject.append(rec)

        for key in ("ALL", dom):
            a = agg[key]
            a["subjects"] += 1
            a["n_mut"] += len(vn)
            a["setn"] += setn_k
            a["setn_valid"] += nv
            if vg is not None:
                a["setg"] += setg_k
                a["setg_valid"] += gv
                for kn, kg in zip(vn, vg):
                    if kg and not kn:
                        a["b"] += 1
                    elif kn and not kg:
                        a["c"] += 1

    strata = {}
    for key, a in agg.items():
        nm = a["n_mut"]
        strata[key] = {
            "subjects": a["subjects"],
            "mutants_total": nm,
            "setn": {"kills": a["setn"], "rate": round(a["setn"] / nm, 4) if nm else 0,
                     "wilson95": wilson(a["setn"], nm), "valid_mrs": a["setn_valid"]},
            "setg": {"kills": a["setg"], "rate": round(a["setg"] / nm, 4) if nm else 0,
                     "wilson95": wilson(a["setg"], nm), "valid_mrs": a["setg_valid"]},
            "mcnemar": {"b_setg_only": a["b"], "c_setn_only": a["c"],
                        "exact_p": round(mcnemar_exact_p(a["b"], a["c"]), 4)},
        }

    out = {"seed": args.seed, "n_subjects": len(per_subject),
           "strata": strata, "per_subject": sorted(per_subject, key=lambda r: r["subject"])}
    with open(args.output, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Comparison written to {args.output}")
    for key in ("ALL", "Math", "Lang", "Guava"):
        if key in strata:
            s = strata[key]
            print(f"[{key}] {s['subjects']} subj, {s['mutants_total']} mutants | "
                  f"Set N {s['setn']['kills']} ({s['setn']['rate']:.3f}) vs "
                  f"Set G {s['setg']['kills']} ({s['setg']['rate']:.3f}) | "
                  f"McNemar b={s['mcnemar']['b_setg_only']} c={s['mcnemar']['c_setn_only']} "
                  f"p={s['mcnemar']['exact_p']}")


if __name__ == "__main__":
    main()
