#!/usr/bin/env python3
"""
Inter-rater kappa for the human MetaPattern/MR-family classification study.

Reads filled rater sheets from   human_kappa/ratings/rater_<name>.csv
(each row: item_id,category[,notes]; category in CATEGORIES) and reports:

  * pairwise Cohen's kappa (every rater pair)
  * Fleiss' kappa across all raters  (+ 95% bootstrap CI over items)
  * percent agreement and per-category agreement
  * the disagreement list (items the raters split on)
  * OPTIONAL human-vs-author: if _gold_author_labels.csv is present, the
    human-majority-vs-author Cohen's kappa (directly comparable to the
    LLM-majority-vs-author kappa = 0.931 reported in
    supplementary/S3_case_study/lrca_audit.md), plus each rater vs author.

Pure standard library (no numpy / sklearn needed).

USAGE
  Real run : drop rater_alice.csv, rater_bob.csv, ... into ./ratings/, then
             python3 compute_kappa.py
  Self-test: python3 compute_kappa.py --selftest
             (fabricates 3 SYNTHETIC raters to prove the pipeline; the output
              is labelled SYNTHETIC and is NOT a human result.)
"""
import csv, glob, os, sys, random, itertools, pathlib

HERE = pathlib.Path(__file__).parent
CATEGORIES = ["G", "O_le", "T_star", "T_rev", "L_star", "D_star", "E_star", "B_rel", "orphan"]

# ---------- kappa primitives ----------
def cohen_kappa(a, b):
    """a, b: dict item->label over the SAME item set."""
    items = sorted(set(a) & set(b))
    items = [i for i in items if a[i] and b[i]]
    n = len(items)
    if n == 0:
        return None, 0
    agree = sum(1 for i in items if a[i] == b[i])
    p_o = agree / n
    ca = {c: sum(1 for i in items if a[i] == c) / n for c in CATEGORIES}
    cb = {c: sum(1 for i in items if b[i] == c) / n for c in CATEGORIES}
    p_e = sum(ca[c] * cb[c] for c in CATEGORIES)
    k = 1.0 if p_e == 1 else (p_o - p_e) / (1 - p_e)
    return k, n

def fleiss_kappa(raters, items=None):
    """raters: list of dict item->label. Uses items rated by ALL raters."""
    if items is None:
        items = sorted(set.intersection(*[set(r) for r in raters]))
        items = [i for i in items if all(r.get(i) for r in raters)]
    n = len(raters)
    N = len(items)
    if N == 0 or n < 2:
        return None, N
    P = []
    cat_tot = {c: 0 for c in CATEGORIES}
    for it in items:
        counts = {c: 0 for c in CATEGORIES}
        for r in raters:
            counts[r[it]] += 1
        for c in CATEGORIES:
            cat_tot[c] += counts[c]
        Pi = (sum(v * v for v in counts.values()) - n) / (n * (n - 1))
        P.append(Pi)
    P_bar = sum(P) / N
    p = {c: cat_tot[c] / (N * n) for c in CATEGORIES}
    P_e = sum(v * v for v in p.values())
    k = 1.0 if P_e == 1 else (P_bar - P_e) / (1 - P_e)
    return k, N

def fleiss_ci(raters, B=2000, seed=0):
    items = sorted(set.intersection(*[set(r) for r in raters]))
    items = [i for i in items if all(r.get(i) for r in raters)]
    if len(items) < 3:
        return None, None
    rng = random.Random(seed)
    ks = []
    for _ in range(B):
        samp = [rng.choice(items) for _ in items]
        k, _n = fleiss_kappa(raters, items=samp)
        if k is not None:
            ks.append(k)
    ks.sort()
    lo = ks[int(0.025 * len(ks))]
    hi = ks[int(0.975 * len(ks)) - 1]
    return lo, hi

def band(k):
    if k is None: return "n/a"
    return ("poor" if k < 0 else "slight" if k < .20 else "fair" if k < .40 else
            "moderate" if k < .60 else "substantial" if k < .80 else "almost perfect")

def majority(raters, items):
    out = {}
    for it in items:
        votes = [r[it] for r in raters if r.get(it)]
        if votes:
            out[it] = max(set(votes), key=votes.count)
    return out

# ---------- IO ----------
def load_sheet(path):
    d = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            iid = (row.get("item_id") or "").strip()
            cat = (row.get("category") or "").strip()
            if iid and cat:
                if cat not in CATEGORIES:
                    print("  WARNING %s: item %s has unknown category %r (ignored)" %
                          (os.path.basename(path), iid, cat))
                    continue
                d[iid] = cat
    return d

def load_gold():
    p = HERE / "_gold_author_labels.csv"
    if not p.exists():
        return None
    return {r["item_id"]: r["author_label"] for r in csv.DictReader(open(p))}

# ---------- report ----------
def report(rater_files):
    raters, names = [], []
    for fp in rater_files:
        d = load_sheet(fp)
        if d:
            raters.append(d); names.append(pathlib.Path(fp).stem.replace("rater_", ""))
    if len(raters) < 2:
        print("Need >=2 rater sheets with filled categories. Found %d." % len(raters))
        return
    print("Raters (%d): %s" % (len(raters), ", ".join(names)))
    common = sorted(set.intersection(*[set(r) for r in raters]))
    common = [i for i in common if all(r.get(i) for r in raters)]
    print("Items rated by ALL raters: %d\n" % len(common))

    print("== Pairwise Cohen's kappa ==")
    for (i, j) in itertools.combinations(range(len(raters)), 2):
        k, n = cohen_kappa(raters[i], raters[j])
        print("  %-12s vs %-12s : kappa=%s  (n=%d, %s)" %
              (names[i], names[j], "%.3f" % k if k is not None else "n/a", n, band(k)))

    print("\n== Fleiss' kappa (all raters) ==")
    k, N = fleiss_kappa(raters)
    lo, hi = fleiss_ci(raters) if k is not None else (None, None)
    ci = "" if lo is None else "  95%% CI [%.3f, %.3f]" % (lo, hi)
    print("  kappa=%s  (n=%d items, r=%d raters, c=%d categories, %s)%s" %
          ("%.3f" % k if k is not None else "n/a", N, len(raters), len(CATEGORIES), band(k), ci))

    # percent agreement
    full = sum(1 for it in common if len({r[it] for r in raters}) == 1)
    print("  unanimous items: %d/%d = %.1f%%" % (full, len(common), 100 * full / max(1, len(common))))

    gold = load_gold()
    if gold:
        print("\n== Human vs author (comparable to LLM-majority-vs-author kappa=0.931) ==")
        maj = majority(raters, common)
        k, n = cohen_kappa(maj, gold)
        print("  human-majority vs author : kappa=%s (n=%d, %s)" %
              ("%.3f" % k if k is not None else "n/a", n, band(k)))
        for nm, r in zip(names, raters):
            k, n = cohen_kappa(r, gold)
            print("  %-12s vs author : kappa=%s (n=%d, %s)" %
                  (nm, "%.3f" % k if k is not None else "n/a", n, band(k)))

    print("\n== Disagreements (items where raters split) ==")
    any_d = False
    for it in common:
        labs = {nm: r[it] for nm, r in zip(names, raters)}
        if len(set(labs.values())) > 1:
            any_d = True
            extra = ""
            if gold:
                extra = "  [author=%s]" % gold.get(it, "?")
            print("  %s: %s%s" % (it, labs, extra))
    if not any_d:
        print("  none (unanimous on all common items)")

def selftest():
    print("=" * 70)
    print("SYNTHETIC SELF-TEST -- fabricated raters, NOT human data. Proves the")
    print("pipeline runs end-to-end; the kappa below is meaningless as evidence.")
    print("=" * 70)
    gold = load_gold()
    if not gold:
        print("(_gold_author_labels.csv missing; run make_items.py first.)"); return
    rng = random.Random(42)
    ratings_dir = HERE / "ratings_selftest"
    ratings_dir.mkdir(exist_ok=True)
    # 3 synthetic raters: agree with gold ~85% of the time, else random other category
    files = []
    for nm, noise in [("synthA", 0.10), ("synthB", 0.15), ("synthC", 0.20)]:
        fp = ratings_dir / ("rater_%s.csv" % nm)
        with open(fp, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["item_id", "category", "notes"])
            for iid, g in gold.items():
                if rng.random() < noise:
                    lab = rng.choice([c for c in CATEGORIES if c != g])
                else:
                    lab = g
                w.writerow([iid, lab, "SYNTHETIC"])
        files.append(str(fp))
    report(files)
    print("\n(Delete experiment_realbug/human_kappa/ratings_selftest/ before real use.)")

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        files = sorted(glob.glob(str(HERE / "ratings" / "rater_*.csv")))
        if not files:
            print("No rater sheets in ./ratings/ . Each rater copies")
            print("rating_sheet_TEMPLATE.csv to ratings/rater_<name>.csv, fills the")
            print("'category' column (one of: %s), then run this script." % ", ".join(CATEGORIES))
            print("\nTo see the pipeline on fabricated data: python3 compute_kappa.py --selftest")
        else:
            report(files)
