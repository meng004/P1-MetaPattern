#!/usr/bin/env python3
"""scripts/aggregate_maturity_panel.py — Synthesize the 5-model maturity panel.

Reads every per-model *.json produced by tosem_maturity_panel.py and emits a
compact synthesis: maturity distribution, per-dimension means, recommendation
tally, persona-verdict tally, blocker counts split by writing-vs-experiment
fixability, and a flat dump of every highest_roi_fix for ROI ranking.

Usage: python3 scripts/aggregate_maturity_panel.py docs/review_2026-06-21/gateway_panel
"""
import json
import sys
from pathlib import Path
from statistics import mean, median, pstdev

REC_ORDER = {"Reject": 0, "Major Revision": 1, "Minor Revision": 2, "Accept": 3}
DIMS = ["originality", "methodology_rigor", "evidence_sufficiency",
        "argument_coherence", "writing_presentation"]
WEIGHTS = {"originality": .20, "methodology_rigor": .25, "evidence_sufficiency": .25,
           "argument_coherence": .15, "writing_presentation": .15}


def norm_rec(r):
    r = (r or "").strip().lower()
    for k in REC_ORDER:
        if k.lower() in r:
            return k
    return r or "?"


def main():
    d = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/review_2026-06-21/gateway_panel")
    only = set(sys.argv[2:])  # optional stem allowlist, e.g. grok-4.3 qwen3-max glm-5.1
    files = sorted(p for p in d.glob("*.json") if not p.name.startswith("_")
                   and (not only or p.stem in only))
    if not files:
        sys.exit(f"No per-model JSON in {d}")
    if only:
        print(f"[subset] including only: {', '.join(sorted(only))}\n")

    rows = []
    for f in files:
        try:
            j = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"!! {f.name}: parse fail {e}")
            continue
        rows.append((f.stem, j))

    print(f"=== {len(rows)} models: {', '.join(r[0] for r in rows)} ===\n")

    # Maturity + recommendation
    mats, accs = [], []
    print("model               | rec            | maturity | recomputed | accept% | conf")
    print("-" * 84)
    for name, j in rows:
        rec = norm_rec(j.get("overall_recommendation"))
        mat = j.get("submission_maturity_0to100")
        acc = j.get("acceptance_probability_pct")
        conf = j.get("reviewer_confidence_1to5")
        ds = j.get("dimension_scores_0to100", {}) or {}
        recomp = round(sum(WEIGHTS[k] * ds.get(k, 0) for k in DIMS), 1) if ds else None
        if isinstance(mat, (int, float)):
            mats.append(mat)
        if isinstance(acc, (int, float)):
            accs.append(acc)
        print(f"{name:19s} | {rec:14s} | {str(mat):8s} | {str(recomp):10s} | "
              f"{str(acc):7s} | {conf}")

    if mats:
        print(f"\nMaturity: mean={mean(mats):.1f}  median={median(mats):.1f}  "
              f"min={min(mats)}  max={max(mats)}  "
              f"sd={pstdev(mats):.1f}" + (f"  (n={len(mats)})"))
    if accs:
        print(f"Accept%:  mean={mean(accs):.1f}  median={median(accs):.1f}  "
              f"min={min(accs)}  max={max(accs)}")

    # Recommendation tally
    tally = {}
    for _, j in rows:
        r = norm_rec(j.get("overall_recommendation"))
        tally[r] = tally.get(r, 0) + 1
    print("\nRecommendation tally:", "  ".join(f"{k}={v}" for k, v in
          sorted(tally.items(), key=lambda kv: -REC_ORDER.get(kv[0], 9))))

    # Per-dimension means
    print("\nPer-dimension (0-100) mean [min-max]:")
    for k in DIMS:
        vals = [j.get("dimension_scores_0to100", {}).get(k) for _, j in rows]
        vals = [v for v in vals if isinstance(v, (int, float))]
        if vals:
            print(f"  {k:22s} {mean(vals):5.1f}  [{min(vals)}-{max(vals)}]  (w={WEIGHTS[k]})")

    # Persona verdict tally
    print("\nPer-persona recommendation tally:")
    personas = ["EIC", "R1_methodology_theory", "R2_domain_mt_mr",
                "R3_perspective_equivariance_safety"]
    for p in personas:
        t = {}
        for _, j in rows:
            pv = (j.get("persona_verdicts", {}) or {}).get(p, {}) or {}
            r = norm_rec(pv.get("recommendation"))
            if r and r != "?":
                t[r] = t.get(r, 0) + 1
        print(f"  {p:36s}", "  ".join(f"{k}={v}" for k, v in
              sorted(t.items(), key=lambda kv: -REC_ORDER.get(kv[0], 9))) or "(none)")
    da_crit = sum(1 for _, j in rows
                  if (j.get("persona_verdicts", {}) or {}).get("devils_advocate", {}).get("critical_found"))
    print(f"  Devil's Advocate CRITICAL found: {da_crit}/{len(rows)}")

    # Blockers split by fixability
    print("\nPublication blockers (per model count, by fixable_by):")
    fixcat = {"writing": 0, "experiment": 0, "either": 0, "?": 0}
    nb = []
    for name, j in rows:
        bl = j.get("publication_blockers", []) or []
        nb.append((name, len(bl)))
        for b in bl:
            fb = (b.get("fixable_by") or "?").strip().lower()
            fixcat[fb if fb in fixcat else "?"] += 1
    for name, n in nb:
        print(f"  {name:19s} {n} blocker(s)")
    print("  blocker fixable_by totals:", "  ".join(f"{k}={v}" for k, v in fixcat.items()))

    # Major weaknesses fixability
    mwfix = {"writing": 0, "experiment": 0, "either": 0, "?": 0}
    for _, j in rows:
        for w in j.get("major_weaknesses", []) or []:
            fb = (w.get("fixable_by") or "?").strip().lower()
            mwfix[fb if fb in mwfix else "?"] += 1
    print("  major_weakness fixable_by totals:", "  ".join(f"{k}={v}" for k, v in mwfix.items()))

    # Flat ROI dump
    print("\n=== ALL highest_roi_fixes (flat, for ROI ranking) ===")
    for name, j in rows:
        for fx in j.get("highest_roi_fixes", []) or []:
            print(f"  [{name}] +{fx.get('expected_gain_pp','?')}pp "
                  f"({fx.get('effort','?')}/{fx.get('fixable_by','?')}): {fx.get('action','')}")


if __name__ == "__main__":
    main()
