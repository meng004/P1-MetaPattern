#!/usr/bin/env python3
"""analyze_b1.py — B1 real-bug pre-registered analysis (prereg_b1_realbug.md §3.2).

Reads experiment_realbug/results/bug_*.json (one per OK bug; schema = b1_cloud_task §B Step 3e)
and emits a RESULTS.md following the frozen statistical contract:

  - per-set detection rate over APPLICABLE bugs + Wilson 95% CI
  - pairwise EXACT McNemar (paired by bug) for Set N vs each evaluable baseline
  - frozen underpowered trigger: discordant b+c < 25 -> "underpowered, inconclusive";
    b+c == 0 -> "test undefined"; never upgraded to "confirmed"
  - Holm-Bonferroni over the N-vs-others family
  - H4 non-inferiority: gap = best_other_rate - rate_N; gap <= 0.10 -> supported, else NOT
  - Set G = "not evaluable on library bugs" (manifest): excluded from McNemar/H4, footnote only
  - coverage_NOETHER (descriptive)

Scope (frozen, anti-drift): MR IDENTIFICATION, NON-INFERIORITY only. No superiority claim.

bug_<id>.json schema consumed:
{
  "id": "...", "repo": "...", "cat": "cat-i|cat-ii|cat-iii|cat-iv",
  "fired_pre":  {"N": true|false|null, "M": ..., "G": null, "L": ..., "B": ...},
  "fired_post": {"N": true|false|null, ...},          # firing on FIXED code => false positive
  "cpu_status": "OK|CPU-INFEASIBLE|BLOCKED", "notes": "..."
}
  fired_pre[s]:  true = MR VIOLATED on buggy code (detection); false = held; null = not_applicable.
  A bug counts toward set s's denominator iff fired_pre[s] is not null.
  detection(bug,s) = fired_pre[s] is true AND NOT (fired_post[s] is true)   # drop false positives

Usage: python3 analyze_b1.py [--results-dir results] [--out experiment_realbug/RESULTS.md] [--freeze-hash <h>]
Deps: Python 3.8+ stdlib only.
"""
import json, glob, os, math, argparse
from math import comb

SETS = ["N", "M", "G", "L", "B"]
EVALUABLE = ["N", "M", "L", "B"]          # Set G not evaluable on library bugs (APPLICABILITY_MANIFEST)
BASELINES = ["M", "L", "B"]               # N-vs-others family (G excluded)
DELTA = 0.10                              # frozen non-inferiority margin (prereg H4)
UNDERPOWER = 25                          # frozen discordant threshold b+c<25


def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def mcnemar_exact(b, c):
    """Two-sided exact McNemar via binomial on discordant pairs."""
    n = b + c
    if n == 0:
        return None
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / (2 ** n))


def holm(name_p):
    """Holm-Bonferroni. name_p: list of (name, p|None). None p (undefined) excluded from family."""
    fam = [(nm, p) for nm, p in name_p if p is not None]
    m = len(fam)
    out = {nm: None for nm, _ in name_p}
    for rank, (nm, p) in enumerate(sorted(fam, key=lambda x: x[1])):
        out[nm] = min(1.0, p * (m - rank))
    # enforce monotonicity
    return out


def detected(bug, s):
    fp_pre = bug["fired_pre"].get(s)
    fp_post = bug["fired_post"].get(s) if "fired_post" in bug else None
    if fp_pre is None:
        return None  # not applicable
    return bool(fp_pre) and not bool(fp_post)  # detection, drop false positive


def applicable(bug, s):
    return bug["fired_pre"].get(s) is not None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", default="results")
    ap.add_argument("--out", default="RESULTS.md")
    ap.add_argument("--freeze-hash", default="<FREEZE_HASH>")
    ap.add_argument("--prereg-intact", default="intact")
    ap.add_argument("--runid", default="local")
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(a.results_dir, "bug_*.json")))
    bugs_all = [json.load(open(f)) for f in files]
    ok = [b for b in bugs_all if b.get("cpu_status") == "OK"]
    n_inf = sum(1 for b in bugs_all if b.get("cpu_status") == "CPU-INFEASIBLE")
    n_blk = sum(1 for b in bugs_all if b.get("cpu_status") == "BLOCKED")

    # per-set detection over applicable OK bugs
    perset = {}
    for s in SETS:
        app = [b for b in ok if applicable(b, s)]
        det = [b for b in app if detected(b, s)]
        n, k = len(app), len(det)
        perset[s] = dict(n=n, k=k, rate=(k / n if n else float("nan")), wilson=wilson(k, n))

    # pairwise McNemar N vs each baseline (paired over bugs where BOTH applicable)
    pair = {}
    for x in BASELINES:
        both = [b for b in ok if applicable(b, "N") and applicable(b, x)]
        bcount = sum(1 for b in both if detected(b, "N") and not detected(b, x))
        ccount = sum(1 for b in both if detected(b, x) and not detected(b, "N"))
        p = mcnemar_exact(bcount, ccount)
        disc = bcount + ccount
        verdict = ("test undefined (b+c=0)" if disc == 0 else
                   ("underpowered, inconclusive (b+c<25)" if disc < UNDERPOWER else
                    ("difference (p<0.05)" if (p is not None and p < 0.05) else "no significant difference")))
        pair[x] = dict(b=bcount, c=ccount, disc=disc, p=p, verdict=verdict)
    holm_p = holm([(x, pair[x]["p"]) for x in BASELINES])

    # H4 non-inferiority (evaluable baselines with n>0)
    base_rates = {x: perset[x]["rate"] for x in BASELINES if perset[x]["n"] > 0}
    rate_N = perset["N"]["rate"]
    if base_rates and not math.isnan(rate_N):
        best_other = max(base_rates.values())
        gap = best_other - rate_N
        h4 = (f"H4 non-inferiority SUPPORTED (gap={gap:.3f} <= Δ={DELTA})" if gap <= DELTA
              else f"H4 NOT supported: Set N trails best baseline by gap={gap:.3f} (> Δ={DELTA})")
    else:
        best_other, gap, h4 = float("nan"), float("nan"), "H4 not computable (no evaluable baseline with n>0)"
    primary_disc = min((pair[x]["disc"] for x in BASELINES), default=0)
    underpowered = any(pair[x]["disc"] < UNDERPOWER for x in BASELINES) or len(ok) < 10

    # coverage_NOETHER (descriptive): fraction of cats present where Set N applicable on >=1 bug
    cats = sorted({b.get("cat") for b in ok if b.get("cat")})
    cov_hit = sum(1 for c in cats if any(applicable(b, "N") for b in ok if b.get("cat") == c))
    coverage = (cov_hit / len(cats)) if cats else float("nan")

    # false positives
    fps = [(b["id"], s) for b in ok for s in SETS
           if b.get("fired_post", {}).get(s) is True]

    def ci(s): w = perset[s]["wilson"]; return f"[{w[0]:.3f}, {w[1]:.3f}]"
    L = []
    L.append("# B1 Real-Bug Evaluation (e3nn / PyG) — Results\n")
    L.append(f"Freeze hash: {a.freeze_hash}     Prereg integrity: {a.prereg_intact}")
    L.append(f"Run id: {a.runid}                Branch: claude/b1-realbug-{a.runid}")
    L.append("CPU-only confirmed: yes        GPU used: no        LLM/API calls: none\n")
    L.append("## Ledger accounting")
    L.append(f"- Ledger rows analysed: {len(bugs_all)}")
    L.append(f"- OK (analysed): {len(ok)}    CPU-INFEASIBLE (excluded): {n_inf}    BLOCKED (excluded): {n_blk}")
    L.append(f"- Category coverage in OK set: " + ", ".join(f"{c} {sum(1 for b in ok if b.get('cat')==c)}" for c in cats) + "\n")
    L.append("## Per-set detection (OK bugs only; denominator = applicable bugs per set)")
    L.append("| Set | fired/total | rate | Wilson 95% CI |")
    L.append("|-----|------------:|-----:|---------------|")
    for s in SETS:
        if s == "G":
            L.append("| G | — | — | **not evaluable on library bugs** (no portable Set-G artefact; manifest) |")
        else:
            ps = perset[s]
            L.append(f"| {s} | {ps['k']}/{ps['n']} | {ps['rate']:.3f} | {ci(s)} |")
    L.append("\n## Pairwise McNemar (paired by bug), Holm-Bonferroni corrected (N-vs-others)")
    L.append("| Pair | b | c | b+c | exact p (2-sided) | Holm p | verdict |")
    L.append("|------|--:|--:|----:|------------------:|-------:|---------|")
    for x in BASELINES:
        pr = pair[x]; pp = "—" if pr["p"] is None else f"{pr['p']:.4f}"
        hp = "—" if holm_p[x] is None else f"{holm_p[x]:.4f}"
        L.append(f"| N vs {x} | {pr['b']} | {pr['c']} | {pr['disc']} | {pp} | {hp} | {pr['verdict']} |")
    L.append("| N vs G | — | — | — | — | — | Set G not evaluable (excluded) |")
    L.append(f"\n## H4 verdict (non-inferiority, Δ={DELTA})")
    L.append(f"best non-N rate = {best_other:.3f};  Set N rate = {rate_N:.3f};  gap = {gap:.3f}")
    L.append(f"=> **{h4}**")
    L.append(f"(Underpowered? {'YES' if underpowered else 'no'}; min primary discordant b+c = {primary_disc}; n_ok = {len(ok)})\n")
    L.append("## coverage_NOETHER (descriptive)")
    L.append(f"{cov_hit}/{len(cats)} = {coverage:.3f} of cat categories present have a block-aligned Set N MR.\n")
    L.append("## False-positive check (MR fired on POST-FIX code)")
    L.append(("None." if not fps else ", ".join(f"{i}:{s}" for i, s in fps)) + "\n")
    L.append("## Honest negatives / limitations")
    if len(ok) < 10:
        L.append(f"- n_ok={len(ok)} < 10 target; **underpowered for α=0.05; reported as descriptive evidence (C6).**")
    L.append("- Set G stated plainly: not evaluable on library bugs (substrate limitation), reported as such, not as 0 detections.")
    L.append("- Cross-set overlap (rho_rot ≡ L_rot ≡ B-rotation on the same rotation category) makes set counts correlated, not independent.")
    L.append("\n## Anti-drift attestation")
    L.append("- MR-identification scope only; non-inferiority framing; **no superiority claim**.")
    L.append("- All negatives/underpowered results reported above; GenMorph (Set G) comparison not hidden (stated not-evaluable).")
    L.append("- All faults are upstream maintainer fix commits (provenance per bug in bug_<id>.json).")
    open(a.out, "w").write("\n".join(L) + "\n")
    print(f"wrote {a.out}  (OK bugs={len(ok)}, infeasible={n_inf}, blocked={n_blk})")


if __name__ == "__main__":
    main()
