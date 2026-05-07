# ISSUE-002: Add Effective-MR Ratio to per-subject and cross-subject metrics

**Status**: in-progress
**Owner**: local Claude Code session
**Branch**: feat/effective-mr-ratio
**Plan**: PLANS/002-effective-mr-ratio.md
**Opened**: 2026-05-07

## Why

Reviewer-style question on §6.6 metric coverage: "what fraction of each
MR set is doing useful work?" None of M1–M5 answers this directly:

* M1 (kill rate) is mutant-level and union-based — it cannot tell whether
  the union came from 3 useful MRs or 30 redundant ones.
* M2 (kills per MR) divides union kills by MR count, which conflates
  "set is dense" with "set has dead weight".

The simple MR-level efficiency indicator —

> Effective-MR Ratio = (# MRs that kill at least one mutant) / (# MRs in set)

— is a high-value, low-cost addition. Set N (algebra-derived, hand-curated)
should approach 1.0; Set G (GP-evolved, often produces redundant rules)
typically exhibits a long tail of zero-kill MRs. The ratio captures that
gap in one number.

## Scope

* `scripts/parse_results.py`: emit `n_effective_mrs` and
  `effective_mr_ratio` inside the existing `set_n` / `set_g` blocks.
* `scripts/aggregate_metrics.py`: pool `effective_mrs` and `total_mrs`
  across subjects and report a pooled `effective_mr_ratio`.
* `docs/METRICS.md`: new file, definitive reference for every metric the
  pipeline computes (formula + parameters + code location), including the
  new ratio.
* `tests/fixtures/sample_mutants_killed.csv` &
  `tests/fixtures/sample_mrs_status.csv`: add one zero-kill MR row to
  exercise the non-trivial branch (effective_mr_ratio < 1.0).
* `tests/test_parse_results.py`, `tests/test_aggregate_metrics.py`:
  assertions on the new fields (Rule 6 gate).

## Out of scope

* Per-MR redundancy analysis (which MRs are dominated by other MRs in the
  same set). Useful but a separate, larger study.
* Test-execution timing (CLAUDE.md §metrics discussion item ④); aligned
  design renders this near-identical for both sets.
* MR-generation cost (item ③); not measurable in an aligned-experiment
  layout — needs a separate informational table.

## Success criteria

- [ ] `parse_results.py` emits `n_effective_mrs` + `effective_mr_ratio`
      per set.
- [ ] `aggregate_metrics.py` emits `total_mrs`, `effective_mrs`,
      `effective_mr_ratio` per set in the cross-subject summary.
- [ ] `docs/METRICS.md` documents M1–M5, Effective-MR Ratio, pooled rate
      + Wilson CI, McNemar, and per-MR detail.
- [ ] `bash tests/run.sh` exits 0 with the new fixture row in place.

## References

* Prior conversation log establishing the metric request.
* `parse_results.py:117-140` (existing M1–M5 implementation).
* `aggregate_metrics.py:74-141` (existing cross-subject inference).
