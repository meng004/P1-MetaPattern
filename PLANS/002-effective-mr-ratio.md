# PLAN-002: Add Effective-MR Ratio + metrics doc

**Issue**: ISSUES/002-effective-mr-ratio.md
**Branch**: feat/effective-mr-ratio
**Drafted on**: local Claude Code (matches Rule 4)

## Files to add / change

| Path | Action | Rationale |
|---|---|---|
| `docs/METRICS.md` | new | single-source reference for every metric (formula + code line) |
| `scripts/parse_results.py` | modify | add `n_effective_mrs` + `effective_mr_ratio` to `set_n` / `set_g` blocks |
| `scripts/aggregate_metrics.py` | modify | pool `total_mrs` and `effective_mrs` across subjects |
| `tests/fixtures/sample_mutants_killed.csv` | modify | add one zero-kill MR row (MR4) so the ratio is < 1.0 in the test fixture |
| `tests/fixtures/sample_mrs_status.csv` | modify | corresponding MR4 row |
| `tests/test_parse_results.py` | modify | update `n_total_mrs` / `set_g.n_mrs` assertions + new ratio assertions |
| `tests/test_aggregate_metrics.py` | modify | extend synthetic JSONs with the new fields + pooled-ratio assertion |

## Risks / tradeoffs

| Risk | Mitigation |
|---|---|
| Older `aligned_metrics.json` files lacking the new field break `aggregate_metrics.py` | Use `.get(..., 0)` fallbacks when summing. New runs always emit the fields. |
| Set with `n_mrs == 0` (no MRs of that flavour for a subject) → division-by-zero in ratio | `max(1, n_mrs)` guard, mirroring the existing M1/M2 pattern. |
| Doc rot — `parse_results.py` line numbers in `docs/METRICS.md` drift after future edits | Use stable section anchors (function names) plus line numbers; reviewer only needs the function to find the math. |

## Test gate (Rule 6)

- [ ] `tests/test_parse_results.py` asserts `n_effective_mrs` and
      `effective_mr_ratio` for both Set N and Set G with the < 1.0 case
      surfaced via the fixture's new zero-kill MR4 row.
- [ ] `tests/test_aggregate_metrics.py` asserts pooled
      `effective_mr_ratio` matches the synthetic ground truth.
- [ ] `bash tests/run.sh` exits 0.
- [ ] `bash -n` syntax checks unchanged (no shell scripts touched).

## Estimated cost

| Step | Time | Where |
|---|---|---|
| Implement | 15 min | local |
| Run tests | <2 sec | anywhere |
| Pipeline re-run (Stage 2 only) | ~30 min | local or remote (Rule 8 already relaxed) |

## Done when

- [ ] Issue 002 success criteria all checked.
- [ ] Branch fast-forward merged to `main`.
- [ ] Tests green on `main`.
