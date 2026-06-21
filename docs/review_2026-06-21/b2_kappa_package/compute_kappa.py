#!/usr/bin/env python3
"""compute_kappa.py — independent-human inter-rater kappa for the NOETHER
8-block MR classification (B2 leg).

Replaces the LLM-only kappa=0.931 with a genuine human inter-rater kappa, per
the pre-registered codebook (docs/review_2026-06-20/mvp_kappa_codebook.md) and
its integrity constraints (no rescue; report honestly; small-n -> Wilson CI).

Inputs (same directory unless overridden):
  author_labels.csv                 mr_id,sut_method,block   (SSOT-derived; provided)
  kappa_labels_raterA.csv           mr_id,sut_method,block,confidence,note (rater A fills)
  kappa_labels_raterB.csv           mr_id,sut_method,block,confidence,note (rater B fills)

Outputs:
  kappa_results.md                  full report (kappas + Landis-Koch bands +
                                    Wilson CIs + disagreement listing + sensitivity)

Usage:
  python3 compute_kappa.py                  # uses ./*.csv
  python3 compute_kappa.py --dir <path>     # CSVs elsewhere
Dependencies: pip install scikit-learn statsmodels pandas
"""
import argparse
import sys
from pathlib import Path

try:
    import pandas as pd
    from sklearn.metrics import cohen_kappa_score
    from statsmodels.stats.inter_rater import fleiss_kappa, aggregate_raters
    from statsmodels.stats.proportion import proportion_confint
except ImportError as e:
    sys.exit(f"ERROR: pip install scikit-learn statsmodels pandas  ({e})")

VALID = {"G", "O_le", "T_star", "T_rev", "L_star", "D_star", "E_star", "B_rel", "orphan"}


def band(k):
    if k < 0: return "poor"
    if k <= 0.20: return "slight"
    if k <= 0.40: return "fair"
    if k <= 0.60: return "moderate"
    if k <= 0.80: return "substantial"
    return "almost perfect"


def load(path, who):
    if not Path(path).is_file():
        sys.exit(f"ERROR: {path} not found. Rater {who} must fill the blank template first.")
    df = pd.read_csv(path).set_index("mr_id")
    bad = set(df["block"].dropna()) - VALID
    if bad:
        sys.exit(f"ERROR: {path} has labels outside the 9-label vocabulary: {bad}")
    if df["block"].isna().any():
        miss = list(df.index[df["block"].isna()])
        sys.exit(f"ERROR: {path} has empty block cells (fill 'orphan' if unsure): {miss}")
    return df


def kappa_pair(a, b, labels):
    return cohen_kappa_score(a, b, labels=labels)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(Path(__file__).resolve().parent))
    args = ap.parse_args()
    d = Path(args.dir)

    author = load(d / "author_labels.csv", "author")["block"]
    A = load(d / "kappa_labels_raterA.csv", "A")
    B = load(d / "kappa_labels_raterB.csv", "B")
    df = pd.concat([A["block"], B["block"], author], axis=1,
                   keys=["A", "B", "author"]).dropna()
    n = len(df)
    labels = sorted(set(df.values.ravel()))

    k_AB = kappa_pair(df.A, df.B, labels)
    k_Aauth = kappa_pair(df.A, df.author, labels)
    k_Bauth = kappa_pair(df.B, df.author, labels)
    mat, _ = aggregate_raters(df[["A", "B", "author"]].values)
    k_fleiss = fleiss_kappa(mat)

    def wilson_agreement(x, y):
        agr = int((x == y).sum())
        lo, hi = proportion_confint(agr, n, alpha=0.05, method="wilson")
        return agr, lo, hi

    agrAB, loAB, hiAB = wilson_agreement(df.A, df.B)

    dis_AB = df[df.A != df.B]
    dis_auth = df[(df.A != df.author) | (df.B != df.author)]

    # Sensitivity: drop low-confidence (conf<=2) items if confidence present
    sens = ""
    try:
        confA = A["confidence"].reindex(df.index)
        confB = B["confidence"].reindex(df.index)
        keep = (confA.fillna(5) > 2) & (confB.fillna(5) > 2)
        if keep.sum() < n:
            d2 = df[keep]
            k_AB2 = kappa_pair(d2.A, d2.B, sorted(set(d2.values.ravel())))
            sens = (f"\n## Sensitivity (drop conf<=2)\n\n"
                    f"- kept {int(keep.sum())}/{n} items; Cohen kappa(A,B) = "
                    f"**{k_AB2:.3f}** ({band(k_AB2)})\n")
    except Exception:
        pass

    out = []
    out.append("# Independent-human inter-rater kappa — NOETHER 8-block classification\n")
    out.append(f"> n = {n} items (36 cross-block MR + 5 SACOS anchors expected). "
               f"Pre-registered codebook: docs/review_2026-06-20/mvp_kappa_codebook.md\n")
    out.append("## Headline (primary result = human vs human)\n")
    out.append("| comparison | Cohen/Fleiss kappa | Landis-Koch |")
    out.append("|---|---:|---|")
    out.append(f"| **raterA vs raterB (PRIMARY, human inter-rater)** | **{k_AB:.3f}** | **{band(k_AB)}** |")
    out.append(f"| raterA vs author | {k_Aauth:.3f} | {band(k_Aauth)} |")
    out.append(f"| raterB vs author | {k_Bauth:.3f} | {band(k_Bauth)} |")
    out.append(f"| Fleiss (A,B,author) | {k_fleiss:.3f} | {band(k_fleiss)} |\n")
    out.append(f"Observed agreement A vs B: {agrAB}/{n} = {agrAB/n:.3f}, "
               f"Wilson 95% CI [{loAB:.3f}, {hiAB:.3f}].\n")
    out.append(sens)
    out.append("## Integrity reminders (codebook §6)\n")
    out.append("- If human kappa is materially below the LLM-only 0.931, REPORT IT and "
               "soften C4: present 0.931 as LLM corroborative breadth, the human kappa as "
               "the confirmatory number.\n"
               "- n is small (underpowered for a tight CI): report the Wilson CI, do NOT use "
               "'trends suggest / encouraging'.\n"
               "- Known controversy items (M08 exactLog2 L*<->T*; M16/M20 reverse+exclusion "
               "B_rel<->T_rev) must be KEPT in if they recur; no item dropping to raise kappa.\n")
    out.append(f"## Human-vs-human disagreements ({len(dis_AB)})\n")
    out.append(dis_AB.to_markdown() if len(dis_AB) else "(none)")
    out.append(f"\n## Any disagreement with author ({len(dis_auth)})\n")
    out.append(dis_auth.to_markdown() if len(dis_auth) else "(none)")

    rep = "\n".join(out) + "\n"
    (d / "kappa_results.md").write_text(rep, encoding="utf-8")
    print(f"OK: n={n}  Cohen kappa(A,B)={k_AB:.3f} ({band(k_AB)})  "
          f"Fleiss={k_fleiss:.3f}  -> {d/'kappa_results.md'}")


if __name__ == "__main__":
    main()
