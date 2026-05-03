"""
analysis.py — produce Table 4 (§6.6) numbers from results.csv.

Inputs:
  - results.csv from runner.py (one row per (set, mr, mutation))

Outputs:
  - table4.json — machine-readable Table 4 entries
  - table4.tex  — LaTeX table fragment matching the manuscript schema
  - hypothesis_check.json — H1/H2 verdict with supporting numbers

H1 (pre-registered):
  coverage_NOETHER(N) == 1.0,
  coverage_NOETHER(L) <  1.0,
  coverage_NOETHER(B) <  1.0.

H2 (pre-registered):
  Set N has at least one cat-iv mutation it uniquely detects (no other
  set detects it), and that detection is via rho_train_rev.

H1 falsifies if NOETHER's derivation is incorrect.
H2 falsifies if L or B independently produces a gradient-reversal probe.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

# Non-empty NOETHER blocks for A_equi (manuscript §6.1)
NON_EMPTY_BLOCKS = ("G", "O_le", "T*", "T_rev*", "L*")
# Note: "(out)" is the placeholder block for set L / set B MRs that do
# not correspond to any NOETHER block (e.g., scaling robustness, axis
# permutation). These do not count towards coverage_NOETHER.


def load_results(path: str) -> list[dict]:
    with open(path) as f:
        return list(csv.DictReader(f))


def coverage_noether(rows_for_set: list[dict]) -> float:
    """coverage_NOETHER = |non-empty blocks covered by at least one MR|
    / |non-empty NOETHER blocks for A_equi|.
    """
    blocks_covered = {r["block"] for r in rows_for_set if r["block"] in NON_EMPTY_BLOCKS}
    return len(blocks_covered) / len(NON_EMPTY_BLOCKS)


def detection_rate(rows_for_set: list[dict]) -> tuple[int, int]:
    """Number of mutations detected by *any* MR in the set, out of total."""
    by_mut = defaultdict(list)
    for r in rows_for_set:
        by_mut[r["mutation_id"]].append(r["detected"] == "True")
    detected = sum(1 for v in by_mut.values() if any(v))
    return detected, len(by_mut)


def per_category_detection(rows_for_set: list[dict]) -> dict[str, tuple[int, int]]:
    by_cat: dict[str, dict[str, list[bool]]] = defaultdict(lambda: defaultdict(list))
    for r in rows_for_set:
        by_cat[r["mutation_category"]][r["mutation_id"]].append(r["detected"] == "True")
    out = {}
    for cat, mut_dict in by_cat.items():
        detected = sum(1 for v in mut_dict.values() if any(v))
        out[cat] = (detected, len(mut_dict))
    return out


def unique_detections(rows: list[dict]) -> dict[str, dict[str, list[str]]]:
    """For each set, list mutations detected ONLY by that set
    (no other set detects them). Returns {set: {mutation_id: [mr_names]}}.
    """
    set_detected: dict[str, set[str]] = defaultdict(set)
    set_mr_for_mut: dict[tuple[str, str], list[str]] = defaultdict(list)
    for r in rows:
        if r["detected"] == "True":
            set_detected[r["set"]].add(r["mutation_id"])
            set_mr_for_mut[(r["set"], r["mutation_id"])].append(r["mr"])
    out: dict[str, dict[str, list[str]]] = {}
    for s, muts in set_detected.items():
        unique = {}
        for mut in muts:
            others = [other for other in set_detected if other != s]
            if not any(mut in set_detected[o] for o in others):
                unique[mut] = set_mr_for_mut[(s, mut)]
        out[s] = unique
    return out


def wilson_interval(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval (95% by default) for a binomial proportion."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, centre - half), min(1.0, centre + half))


def fisher_exact_2x2(a: int, b: int, c: int, d: int) -> float:
    """Two-sided Fisher exact test p-value for the 2x2 table
    [[a, b], [c, d]] using exact hypergeometric tail summation.

    Returns p-value in [0, 1]. No external dependency.
    """
    n = a + b + c + d
    r1 = a + b
    c1 = a + c
    if r1 == 0 or n - r1 == 0 or c1 == 0 or n - c1 == 0:
        return 1.0
    obs = math.comb(r1, a) * math.comb(n - r1, c1 - a)
    p_obs = obs / math.comb(n, c1)
    p_total = 0.0
    a_min = max(0, c1 - (n - r1))
    a_max = min(r1, c1)
    for a_alt in range(a_min, a_max + 1):
        c_alt = c1 - a_alt
        p_alt = (math.comb(r1, a_alt) * math.comb(n - r1, c_alt)) / math.comb(n, c1)
        if p_alt <= p_obs + 1e-15:
            p_total += p_alt
    return min(1.0, p_total)


def mcnemar_exact(b: int, c: int) -> float:
    """Exact two-sided McNemar test on paired counts.

    b = number of mutations detected by A but not B; c = vice versa.
    Returns p-value (binomial test on b ~ Binomial(b+c, 0.5)).
    """
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n)
    return min(1.0, 2 * p)


def paired_detection_stats(rows: list[dict], set_a: str, set_b: str) -> dict:
    """For two sets, count agreements and disagreements per mutation.

    Returns: detected_a, detected_b, both, only_a, only_b, neither, p_mcnemar,
    p_fisher (treating mutations as independent, less strict than McNemar).
    """
    by_mut: dict[str, dict[str, list[bool]]] = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r["set"] in (set_a, set_b):
            by_mut[r["mutation_id"]][r["set"]].append(r["detected"] == "True")
    only_a = only_b = both = neither = 0
    for mut, m_dict in by_mut.items():
        det_a = any(m_dict.get(set_a, [False]))
        det_b = any(m_dict.get(set_b, [False]))
        if det_a and det_b:
            both += 1
        elif det_a and not det_b:
            only_a += 1
        elif det_b and not det_a:
            only_b += 1
        else:
            neither += 1
    detected_a = both + only_a
    detected_b = both + only_b
    n = detected_a + detected_b + neither - both  # = total mutations
    n = both + only_a + only_b + neither
    p_mcnemar = mcnemar_exact(only_a, only_b)
    # Fisher exact treating each mutation as a sample (paired structure ignored)
    p_fisher = fisher_exact_2x2(detected_a, n - detected_a,
                                  detected_b, n - detected_b)
    return {
        "set_a": set_a, "set_b": set_b,
        "detected_a": detected_a, "detected_b": detected_b,
        "both": both, "only_a": only_a, "only_b": only_b,
        "neither": neither, "n_mutations": n,
        "p_mcnemar_two_sided": p_mcnemar,
        "p_fisher_two_sided": p_fisher,
    }


def render_table4(table: dict) -> str:
    """LaTeX fragment matching the schema in §6.6 Table 4."""
    lines = [
        r"\begin{tabular}{lccc}",
        r"\toprule",
        r"& Set N (NOETHER) & Set L (LLM) & Set B (Lit.) \\",
        r"\midrule",
    ]
    n, l, b = table["sets"]["N"], table["sets"]["L"], table["sets"]["B"]
    nm = n["mutations_total"]
    lines.append(
        f"Detection rate & {n['detected']}/{nm} & {l['detected']}/{nm} & {b['detected']}/{nm} \\\\"
    )
    lines.append(
        f"Structural coverage & {n['coverage_noether']:.2f} & {l['coverage_noether']:.2f} & {b['coverage_noether']:.2f} \\\\"
    )
    lines.append(
        f"Unique detections & {n['unique']} & {l['unique']} & {b['unique']} \\\\"
    )
    for cat in ("i", "ii", "iii", "iv"):
        cat_label = {"i": "wrong-sign loss", "ii": "equivariance break",
                     "iii": "precision degradation",
                     "iv": "gradient-reversal sign"}[cat]
        nc = n["per_cat"].get(cat, [0, 5])
        lc = l["per_cat"].get(cat, [0, 5])
        bc = b["per_cat"].get(cat, [0, 5])
        lines.append(
            f"Detected cat. {cat} {cat_label} & "
            f"{nc[0]}/{nc[1]} & {lc[0]}/{lc[1]} & {bc[0]}/{bc[1]} \\\\"
        )
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    return "\n".join(lines)


def main(results_path: str, *, output_dir: str = ".") -> None:
    rows = load_results(results_path)
    if not rows:
        raise SystemExit(f"No rows in {results_path}")

    by_set = defaultdict(list)
    for r in rows:
        by_set[r["set"]].append(r)

    table: dict = {"sets": {}}
    for s in ("N", "L", "B"):
        rs = by_set.get(s, [])
        det, total = detection_rate(rs)
        cov = coverage_noether(rs)
        per_cat = per_category_detection(rs)
        table["sets"][s] = {
            "detected": det,
            "mutations_total": total,
            "coverage_noether": cov,
            "per_cat": {k: list(v) for k, v in per_cat.items()},
        }

    uniq = unique_detections(rows)
    for s in ("N", "L", "B"):
        table["sets"][s]["unique"] = len(uniq.get(s, {}))
        table["sets"][s]["unique_details"] = uniq.get(s, {})

    # Hypothesis verdicts
    h1 = {
        "noether_coverage_eq_1": abs(table["sets"]["N"]["coverage_noether"] - 1.0) < 1e-9,
        "llm_coverage_lt_1": table["sets"]["L"]["coverage_noether"] < 1.0,
        "literature_coverage_lt_1": table["sets"]["B"]["coverage_noether"] < 1.0,
    }
    h1["holds"] = all(h1.values())

    cat_iv_unique_to_n = [
        mut for mut in table["sets"]["N"]["unique_details"]
        if any(r for r in by_set["N"]
               if r["mutation_id"] == mut and r["mutation_category"] == "iv")
    ]
    rho_train_rev_detections = [
        r for r in by_set["N"]
        if r["mr"] == "rho_train_rev"
        and r["detected"] == "True"
        and r["mutation_category"] == "iv"
    ]
    h2 = {
        "n_has_unique_cat_iv": len(cat_iv_unique_to_n) > 0,
        "via_rho_train_rev": len(rho_train_rev_detections) > 0,
        "cat_iv_uniquely_detected": cat_iv_unique_to_n,
        "rho_train_rev_detected_count": len(rho_train_rev_detections),
    }
    h2["holds"] = h2["n_has_unique_cat_iv"] and h2["via_rho_train_rev"]

    # Per-set Wilson 95% CI on detection rate
    for s in ("N", "L", "B"):
        det = table["sets"][s]["detected"]
        n = table["sets"][s]["mutations_total"]
        lo, hi = wilson_interval(det, n)
        table["sets"][s]["wilson_ci_95"] = [round(lo, 3), round(hi, 3)]

    # Pairwise statistical comparisons
    table["pairwise_stats"] = {
        "N_vs_L": paired_detection_stats(rows, "N", "L"),
        "N_vs_B": paired_detection_stats(rows, "N", "B"),
        "L_vs_B": paired_detection_stats(rows, "L", "B"),
    }

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "table4.json").write_text(json.dumps(table, indent=2))
    (out_dir / "table4.tex").write_text(render_table4(table))
    (out_dir / "hypothesis_check.json").write_text(
        json.dumps({"H1": h1, "H2": h2}, indent=2)
    )

    # Print pairwise stats summary
    print("\nPairwise statistical comparisons (paired McNemar + Fisher exact):")
    for pair_name, p in table["pairwise_stats"].items():
        print(f"  {pair_name}: detect {p['detected_a']}/{p['n_mutations']} vs "
              f"{p['detected_b']}/{p['n_mutations']}, "
              f"only_a={p['only_a']} only_b={p['only_b']} both={p['both']}, "
              f"p_mcnemar={p['p_mcnemar_two_sided']:.4f}, p_fisher={p['p_fisher_two_sided']:.4f}")
    print("\nWilson 95% CI on detection rate:")
    for s in ("N", "L", "B"):
        det = table["sets"][s]["detected"]
        n = table["sets"][s]["mutations_total"]
        lo, hi = table["sets"][s]["wilson_ci_95"]
        print(f"  Set {s}: {det}/{n} = {det/n:.2f} (95% CI [{lo:.2f}, {hi:.2f}])")

    print("=" * 70)
    print("Table 4 (text):")
    print("=" * 70)
    print(render_table4(table))
    print("\nH1 verdict:", "HOLDS" if h1["holds"] else "FAILS", h1)
    print("H2 verdict:", "HOLDS" if h2["holds"] else "FAILS", h2)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("results", help="results.csv from runner.py")
    ap.add_argument("--output-dir", default=".",
                    help="directory for table4.json/.tex/hypothesis_check.json")
    args = ap.parse_args()
    main(args.results, output_dir=args.output_dir)
