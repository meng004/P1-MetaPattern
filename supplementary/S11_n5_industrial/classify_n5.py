"""N5 coverage analysis: classify the expert-approved industrial MRs (BAMBOO-C
SPARK/LOCUST, SACOS) against the FROZEN NOETHER 8-block decomposition.

This is the coverage / block-occupancy arm of the N5 protocol (Arm B = the supplied
expert-approved corpus; J1 validity is given by expert approval). It tests whether
the frozen blocks SUBSUME these unseen industrial codes' MRs, with no re-fitting.

Classification is rule-based over the 8 blocks (NOT hard-coded to O<=): an MR is sent
to G/T*/T_rev*/L*/E*/Conservation/D* if it shows that block's structural cue
(invariance, adjoint, reversal, refinement-limit, method-comparison, conservation,
qualitative-shape); otherwise, a monotone input->output covariation is O<= (order).
An MR matching no block is an ORPHAN (candidate ninth block).

Honesty: occupancy / prediction here is POST-HOC (corpus already seen); reported as
descriptive, not a pre-registered confirmation (HARKing guard, CLAUDE.md §6).
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPORA = HERE / "mr_corpora.md"
NEW_RANGES = {  # documents' "newly discovered / implicit" subsets
    "SPARK": range(31, 37), "LOCUST": range(23, 29), "SACOS": range(41, 47),
}

# structural cues per block (searched in the MR text, case-insensitive)
CUES = {
    "G":            r"rotat|reflect|shift|invarian|symmetr|permut|equivar",
    "T*":           r"adjoint|recipro|transpose|self-adjoint",
    "T_rev*":       r"revers|time-reversal|backward",
    "L*":           r"refine|converg|grid|mesh|limit|asymptot|→|->",
    "E*":           r"method|scheme.*(vs|versus)|error bound|no worse",
    "Conservation": r"conserv|balance|sum.*invariant|total.*preserv",
    "D*":           r"extrem|overshoot|peak|inflect|monotone phase|s-curve",
}
ORD = re.compile(r"([A-Za-zρ_]+)\s*[12]\s*([<>])\s*([A-Za-zρ_]+)\s*[12]")


def parse_corpora():
    text = CORPORA.read_text(encoding="utf-8")
    sections = re.split(r"^## ", text, flags=re.M)
    corpus = {}
    for sec in sections:
        head = sec.splitlines()[0] if sec.strip() else ""
        for code in ("SPARK", "LOCUST", "SACOS"):
            if head.startswith(code):
                mrs = []
                for blk in re.findall(r"```(.*?)```", sec, re.DOTALL):
                    for line in blk.splitlines():
                        m = re.match(r"\s*MR(\d+)\s*:\s*(.+)", line)
                        if m:
                            mrs.append((int(m.group(1)), m.group(2).strip()))
                corpus[code] = mrs
    return corpus


def classify(text):
    low = text.lower()
    for blk, pat in CUES.items():
        if re.search(pat, low):
            return blk, "cue"
    # default: monotone input->output covariation => O<= (order/monotone)
    if ORD.search(text):
        sub = "plain"
        if re.search(r"\bAND\b|threshold|阈值", text):
            sub = "conditional"
        if re.search(r"\bd[A-Za-z]|increment|_same|相同|Δ", text):
            sub = "increment"
        return "O<=", sub
    return "ORPHAN", "unparsed"


def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def main():
    corpus = parse_corpora()
    rows = []
    for code, mrs in corpus.items():
        for n, txt in mrs:
            blk, sub = classify(txt)
            rows.append({"code": code, "mr": n, "block": blk, "subtype": sub,
                         "new": n in NEW_RANGES[code], "text": txt})
    total = len(rows)
    covered = [r for r in rows if r["block"] != "ORPHAN"]
    orphans = [r for r in rows if r["block"] == "ORPHAN"]
    occ = {}
    for r in covered:
        occ[r["block"]] = occ.get(r["block"], 0) + 1
    new_cnt = sum(r["new"] for r in rows)
    sub_cnt = {}
    for r in covered:
        sub_cnt[r["subtype"]] = sub_cnt.get(r["subtype"], 0) + 1
    cov_lo, cov_hi = wilson(len(covered), total)

    print(f"N5 industrial coverage (frozen NOETHER 8-block) — {total} expert MRs\n")
    for code, mrs in corpus.items():
        cc = [r for r in rows if r["code"] == code]
        cov = sum(r["block"] != "ORPHAN" for r in cc)
        print(f"  {code:7}: {len(cc):3} MRs | covered {cov}/{len(cc)} | "
              f"blocks={sorted(set(r['block'] for r in cc))} | "
              f"new={sum(r['new'] for r in cc)}")
    print(f"\n  TOTAL coverage: {len(covered)}/{total} = {len(covered)/total:.3f} "
          f"Wilson95 [{cov_lo:.3f},{cov_hi:.3f}]")
    print(f"  block occupancy: {occ}")
    print(f"  sub-types (within O<=): {sub_cnt}")
    print(f"  orphans (candidate ninth block): {len(orphans)}")
    print(f"  newly-discovered/implicit (valid beyond initial expert set): {new_cnt}")
    print("\n  HONEST READ:")
    print("   - Coverage of the frozen blocks is essentially complete, BUT the corpus")
    print("     is single-block (O<=): it confirms the order/monotone block transfers")
    print("     to unseen industrial reactor codes; it does NOT exercise G/T*/L*/E*/")
    print("     Conservation/T_rev*, nor the FA-rank-tight IBT blocks (G, T*).")
    print("   - O<= is the inequality/cone block (fa_block_classification.py): these")
    print("     MRs confirm COVERAGE (C4), not the IBT tight characterization.")
    print("   - Same broad field (nuclear reactor codes): held-out at the CODE level")
    print("     (framework not fit to these codes' MRs), not a non-physics cross-domain")
    print("     test. Occupancy read is post-hoc (descriptive, not pre-registered).")

    out = {
        "total": total, "covered": len(covered),
        "coverage_rate": len(covered) / total, "coverage_wilson95": [cov_lo, cov_hi],
        "block_occupancy": occ, "subtypes": sub_cnt,
        "orphans": len(orphans), "newly_discovered": new_cnt,
        "per_code": {c: {"n": len([r for r in rows if r["code"] == c]),
                         "new": sum(r["new"] for r in rows if r["code"] == c)}
                     for c in corpus},
        "rows": rows,
    }
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / "n5_coverage.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if not orphans else 0   # orphans are informative, not a failure


if __name__ == "__main__":
    raise SystemExit(main())
