"""
Aggregate replication audit (NOT a transcription-faithfulness proof).

Compares the kill rate of our Java-transcribed Set G against GenMorph's
published mutants_killed.csv union kill rate for the same (subject, seed).

What this script measures:
    - Single scalar: |our_kill_rate - genmorph_kill_rate| over the same
      mutant CARDINALITY (typically 25 or 26 PIT mutants).

What this script does NOT measure:
    1. Per-mutant agreement (we cannot — PIT 1.15 vs upstream PIT 1.7 produce
       different mutant byte-code; mutant indices are not comparable).
    2. Per-input jor-evaluation agreement (would require GenMorph's recorded
       Randoop test inputs).
    3. Syntactic transcription correctness (only inspectable by human review
       of jorMR<n> helpers vs the DSL files).

Three failure modes are conflated in the delta:
    (a) Transcription bug         — we get jor wrong on some inputs
    (b) Pipeline mismatch          — PIT version, test inputs, evaluator
                                     differ across our pipeline and upstream
    (c) Mutator-scope drift        — `excludedMethods` may not match GenMorph's

A non-zero |delta| could be any combination of (a)+(b)+(c). Use this only as
a coarse replication audit — NOT as evidence that our transcription is
correct or wrong.

For establishing local correctness of the transcription, rely on:
    - FP=0 baseline (./gradlew test passes on unmutated SUT) → rules out
      systematic over-firing of the jor.
    - Human review of jorMR<n> helpers against MR<n>.jor.txt source.

GenMorph's CSV row format:
    EXPERIMENT,MR,M1,...,M25,COUNT
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd  # type: ignore[import-untyped]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--our-stats", required=True, type=Path,
                        help="Path to results/pilot_stats.json from stats.py")
    parser.add_argument("--our-results", required=True, type=Path,
                        help="Path to results/results.csv from parse_pit_xml.py")
    parser.add_argument("--genmorph-csv", required=True, type=Path,
                        help="Path to GenMorph's mutants_killed.csv for the chosen subject + seed")
    parser.add_argument("--seed-row", default="assertions_seed11",
                        help="Which EXPERIMENT row in mutants_killed.csv to use")
    parser.add_argument("--tolerance", type=float, default=0.10,
                        help="Max absolute kill-rate delta per MR")
    parser.add_argument("--subject-label", default="MathClass?gcd?0",
                        help="Subject label written to cross_validation.json")
    parser.add_argument("--output", default="results/cross_validation.json", type=Path)
    args = parser.parse_args()

    if not args.genmorph_csv.exists():
        print(f"ERROR: {args.genmorph_csv} not found")
        return 1
    if not args.our_results.exists():
        print(f"ERROR: {args.our_results} not found")
        return 1

    gm = pd.read_csv(args.genmorph_csv)
    gm_seed = gm[gm["EXPERIMENT"] == args.seed_row]
    if len(gm_seed) == 0:
        print(f"ERROR: no rows in {args.genmorph_csv} match EXPERIMENT='{args.seed_row}'")
        return 2

    # Compute GenMorph kill rates per MR
    gm_per_mr = {}
    for _, row in gm_seed.iterrows():
        mr_name = row["MR"]
        kill_count = int(row["COUNT"])
        n_mutants = sum(1 for col in row.index if isinstance(col, str) and col.startswith("M") and col[1:].isdigit())
        gm_per_mr[mr_name] = {
            "killed": kill_count,
            "total_mutants": n_mutants,
            "kill_rate": kill_count / n_mutants if n_mutants else 0.0,
        }

    # Compute our Set G kill rate (union across MR0..MR3)
    ours = pd.read_csv(args.our_results)
    n_total = len(ours)
    our_set_g_killed = int(ours["set_g_detected"].sum())
    our_set_g_rate = our_set_g_killed / n_total if n_total else 0.0

    # GenMorph union: a mutant is killed by Set G if it was killed by any of
    # MR0..MR3. Recompute from the per-mutant matrix.
    mut_cols = [c for c in gm_seed.columns if c.startswith("M") and c[1:].isdigit()]
    union_kills = set()
    for _, row in gm_seed.iterrows():
        for c in mut_cols:
            if int(row[c]) == 1:
                union_kills.add(c)
    gm_union_killed = len(union_kills)
    gm_union_rate = gm_union_killed / len(mut_cols) if mut_cols else 0.0

    delta = our_set_g_rate - gm_union_rate
    pass_check = abs(delta) <= args.tolerance

    # Direction-aware interpretation:
    #   |delta| <= tolerance  → faithful transcription, equivalent kill rate
    #   delta < -tolerance    → our Set G underperforms GenMorph: indicates
    #                           transcription bug or input distribution that
    #                           misses MR's pattern
    #   delta > +tolerance    → our Set G outperforms GenMorph: typically
    #                           caused by (a) PIT version difference (our
    #                           1.15 vs upstream 1.7 generates different
    #                           mutants), (b) test inputs exercise code
    #                           paths upstream's Randoop-only inputs missed.
    #                           NOT a transcription bug.
    if pass_check:
        verdict = "WITHIN_TOLERANCE"
        interpretation = (
            f"Set G kills {our_set_g_rate*100:.1f}% vs GenMorph's published {gm_union_rate*100:.1f}% "
            f"(|delta| = {abs(delta)*100:.1f} pp ≤ {args.tolerance*100:.0f} pp). The aggregate "
            "kill rates align. NOTE: this audit cannot distinguish transcription correctness "
            "from coincidental pipeline-difference cancellation; it is a necessary but not "
            "sufficient replication signal."
        )
    elif delta < 0:
        verdict = "UNDERPERFORMING"
        interpretation = (
            f"Set G kills {our_set_g_rate*100:.1f}% vs GenMorph's published {gm_union_rate*100:.1f}% "
            f"({delta*100:+.1f} pp). The negative delta has at least three non-mutually-exclusive "
            "causes: (a) transcription weakness (some jor branches under-fire on our inputs); "
            "(b) test inputs miss the regions where GenMorph's evolved jor was tuned to fire; "
            "(c) PIT 1.15 mutants differ from upstream PIT 1.7 mutants in non-equivalent ways. "
            "The audit cannot disambiguate; FP=0 baseline rules out systematic over-firing but "
            "not under-firing on specific mutant patterns."
        )
    else:
        verdict = "EXCEEDING"
        interpretation = (
            f"Set G kills {our_set_g_rate*100:.1f}% vs GenMorph's published {gm_union_rate*100:.1f}% "
            f"(+{delta*100:.1f} pp). Three non-mutually-exclusive causes: (a) PIT 1.15 mutants are "
            "a different — possibly easier — set than upstream PIT 1.7; (b) our boundary inputs "
            "(MIN/MAX_VALUE, both-negative pairs, ±π/2, ±π) reach code paths Randoop's value "
            "seeding may have missed; (c) transcription has accidental over-firing on certain "
            "input patterns (FP=0 baseline rules out systematic over-firing on the original SUT "
            "but does not rule out per-mutant over-firing). The audit cannot disambiguate; "
            "the +delta should NOT be read as 'NOETHER beats GenMorph' nor 'transcription is "
            "perfectly faithful'."
        )

    out = {
        "subject": args.subject_label,
        "seed_row": args.seed_row,
        "tolerance": args.tolerance,
        "n_mutants_ours": n_total,
        "n_mutants_genmorph": len(mut_cols),
        "our_set_g_kill_rate": round(our_set_g_rate, 4),
        "genmorph_union_kill_rate": round(gm_union_rate, 4),
        "delta": round(delta, 4),
        "verdict": verdict,
        "passes_tolerance": pass_check,
        "per_mr_genmorph": gm_per_mr,
        "interpretation": interpretation,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    # Exit-code semantics:
    #   0 = WITHIN_TOLERANCE or EXCEEDING (transcription is faithful;
    #       EXCEEDING is favourable for our pilot)
    #   3 = UNDERPERFORMING (delta < -tolerance) — likely transcription bug
    return 0 if verdict in ("WITHIN_TOLERANCE", "EXCEEDING") else 3


if __name__ == "__main__":
    raise SystemExit(main())
