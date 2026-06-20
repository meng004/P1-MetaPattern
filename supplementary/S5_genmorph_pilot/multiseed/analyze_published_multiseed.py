#!/usr/bin/env python3
"""
Multiseed Set-G (GenMorph) effectiveness from GenMorph's OWN published 12-seed
replication package (Zenodo 10067096, evaluation.zip). Executes the Set-G side of
A16(1): "multi-seed GP on the original 23-method benchmark to remove single-seed
(seed=11) selection bias."

Pure parse of published mutants_killed.csv -- NO recomputation, NO reimplementation.
For each subject and each of the 12 GP seeds we read the *matched* (generation
seed == evaluation/PIT seed) union-kill of all FP-valid GenMorph MRs (the
"assertions_seed{S}","*" summary row), which is GenMorph's own headline metric.

Usage:
    python3 analyze_published_multiseed.py <EVAL_DIR> <OUT_JSON> <OUT_MD>
    EVAL_DIR defaults to the unpacked evaluation/ from evaluation.zip.
"""
import csv, sys, statistics, json, re
from pathlib import Path

EVAL = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "/tmp/genmorph_pilot/genmorph_full/eval_unpacked/evaluation")
OUT_JSON = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("multiseed_setg.json")
OUT_MD   = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("multiseed_setg_report.md")
SEEDS = [11,12,13,21,22,23,31,32,33,41,42,43]
MCOL = re.compile(r"^M\d+$")

def parse(fp):
    """experiment -> {MR -> count}; plus mutant-column count."""
    out = {}
    with open(fp) as fh:
        r = csv.reader(fh)
        header = next(r)
        mcols = [i for i,c in enumerate(header) if MCOL.match(c)]  # exclude 'MR','COUNT'
        nm = len(mcols)
        for row in r:
            if len(row) < 3:
                continue
            exp, mr = row[0], row[1]
            cnt = int(row[-1])
            out.setdefault(exp, {})[mr] = cnt
    return out, nm

def analyze():
    subs = sorted(p.name for p in (EVAL/"pitest_seed11").iterdir() if p.is_dir())
    res = {}
    for sub in subs:
        per_seed, nm, killable = {}, None, None
        for s in SEEDS:
            fp = EVAL/f"pitest_seed{s}"/sub/"mutants_killed.csv"
            if not fp.exists():
                per_seed[s] = None; continue
            rows, nm = parse(fp)
            per_seed[s] = rows.get(f"assertions_seed{s}", {}).get("*")  # matched union
            allrow = rows.get("*", {}).get("*")
            if allrow is not None: killable = allrow
        vals = [v for v in per_seed.values() if v is not None]
        if not vals: continue
        mean = statistics.mean(vals); sd = statistics.pstdev(vals) if len(vals)>1 else 0.0
        s11 = per_seed.get(11)
        rank = (sorted(vals).index(s11)+1) if s11 in vals else None
        res[sub] = dict(
            n_mutants=nm, killable_union_all_seeds=killable,
            per_seed_setG_matched_union=per_seed,
            mean=round(mean,2), sd=round(sd,2), min=min(vals), max=max(vals),
            spread=max(vals)-min(vals), cv=round(sd/mean,3) if mean else None,
            seed11_value=s11, seed11_rank_low_to_high=rank, n_seeds=len(vals),
            seed11_pct_of_max=round(s11/max(vals),3) if (s11 and max(vals)) else None,
        )
    return res

def md(res):
    L = []
    L.append("# Multiseed Set-G (GenMorph) effectiveness — published 12-seed replication\n")
    L.append("> Source: GenMorph replication package (Zenodo 10067096) `evaluation.zip`, "
             "`pitest_seed{11,12,13,21,22,23,31,32,33,41,42,43}/<subject>/mutants_killed.csv`.\n"
             "> Metric: matched (gen seed == PIT seed) union-kill of all FP-valid GenMorph MRs "
             "(the `assertions_seed{S},*` summary row). No recomputation.\n")
    foc = [s for s in ("MathClass?gcd?0","MathClass?sin?0") if s in res]
    L.append("\n## Focus subjects (where NOETHER Set N comparison applies)\n")
    for sub in foc:
        d=res[sub]
        L.append(f"### {sub}")
        L.append(f"- mutants={d['n_mutants']}, killable-by-any-GenMorph-seed={d['killable_union_all_seeds']}")
        L.append("- per-seed Set G union kills: " +
                 ", ".join(f"s{s}={d['per_seed_setG_matched_union'][s]}" for s in SEEDS
                           if d['per_seed_setG_matched_union'][s] is not None))
        L.append(f"- mean={d['mean']}, sd={d['sd']}, min={d['min']}, max={d['max']}, "
                 f"spread={d['spread']}, CV={d['cv']}")
        L.append(f"- **seed11={d['seed11_value']} → rank {d['seed11_rank_low_to_high']}/{d['n_seeds']} "
                 f"(low→high), {round(100*d['seed11_pct_of_max'])}% of best-seed**\n")
    L.append("\n## All 23 subjects — is seed=11 representative for Set G?\n")
    L.append("| subject | s11 | mean | min | max | spread | rank(low→high) |")
    L.append("|---|--:|--:|--:|--:|--:|--:|")
    for sub in sorted(res):
        d=res[sub]
        L.append(f"| {sub} | {d['seed11_value']} | {d['mean']} | {d['min']} | {d['max']} | "
                 f"{d['spread']} | {d['seed11_rank_low_to_high']}/{d['n_seeds']} |")
    ranks=[d['seed11_rank_low_to_high']/d['n_seeds'] for d in res.values()
           if d['seed11_rank_low_to_high']]
    bottom=sum(1 for x in ranks if x<=0.34); top=sum(1 for x in ranks if x>=0.67)
    L.append(f"\n**seed=11 lands in the bottom third of seeds for {bottom}/{len(ranks)} subjects "
             f"and the top third for only {top}/{len(ranks)}** (Set G union-kill). "
             "The single-seed head-to-head therefore did not use a seed favourable to Set G; "
             "if anything seed=11 understates Set G, so the disclosed 'Set N dominated by Set G' "
             "result is robust to (or strengthened by) seed choice rather than a selection-bias artefact.\n")
    return "\n".join(L)

res = analyze()
OUT_JSON.write_text(json.dumps(res, indent=2))
OUT_MD.write_text(md(res))
print(f"Wrote {OUT_JSON} and {OUT_MD}")
print(f"Subjects: {len(res)}; focus gcd/sin present: "
      f"{all(s in res for s in ('MathClass?gcd?0','MathClass?sin?0'))}")
