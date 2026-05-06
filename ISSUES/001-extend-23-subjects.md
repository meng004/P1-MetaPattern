# ISSUE-001: Extend pilot from 2 → 23 subjects with aligned pipeline

**Status**: done
**Owner**: local Claude Code session
**Branch**: main (initial commit, predates rule 5)
**Plan**: PLANS/001-extend-23-subjects.md
**Opened**: 2026-05-06
**Closed**: 2026-05-06 (commit f9f6071)

## Why

NOETHER paper §6.6 protocol calls for the full 23-subject GenMorph
benchmark, single-variable design (only the MR set varies). The earlier
pilot covered 2 subjects (gcd, sin) on a parallel JUnit pipeline that left
five confounders uncontrolled (PIT version, test inputs, evaluator, mutator
scope, mutant byte-code). To support publication-grade comparison Set N
vs Set G, we must:

1. Cover all 23 GenMorph subjects.
2. Run on upstream's exact PIT 1.7.4 + Randoop seed=11 + EvoSuite + GAssert
   substrate so only the MR set varies.

## Scope

* 71 NOETHER-derived MRs across 23 subjects encoded in GenMorph (jir, jor)
  DSL under `set_n_mrs/<subject>/`.
* Source-of-truth generator at `scripts/generate_set_n_mrs.py`.
* Two-stage orchestrator at `scripts/run_all.sh` (Stage 1 reproduce upstream;
  Stage 2 inject Set N + re-run EvaluateMRs).
* Per-subject `parse_results.py` and cross-subject `aggregate_metrics.py`.
* `setup.sh` for one-shot Ubuntu provisioning.

## Out of scope

* Real-bug evaluation (paper §6.6 \texttt{S5 real\_bugs/} — separate issue).
* DeepCrime ML-fault evaluation (separate supplementary, not S5).
* Per-MR FP-rate reduction (treated downstream by GAssert's rejection).
* Path C fallback for Set N MRs that GAssert may reject — deferred to a
  follow-up issue if Stage 2 surfaces parser failures.

## Success criteria

- [x] 23 subject directories under `set_n_mrs/`.
- [x] 142 DSL files (71 MRs × 2 files).
- [x] Pipeline orchestrator runs end-to-end on a fresh Ubuntu host given
      `setup.sh` + `run_all.sh`.
- [x] Block coverage breakdown (G / O_le / L*) committed in `README.md`.
- [x] Initial commit on `main` (f9f6071).

## References

* Paper §6.6 protocol description (`../MR元模式/NOETHER_paper.tex` lines 762–775).
* GenMorph 2023/2024 (Ayerdi et al., Zenodo 10067096).
* Earlier pilot at `../MR元模式/supplementary/S5_genmorph_pilot/aligned/`.
