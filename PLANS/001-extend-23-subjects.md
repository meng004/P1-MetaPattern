# PLAN-001: Extend pilot from 2 → 23 subjects (retroactive record)

**Issue**: ISSUES/001-extend-23-subjects.md
**Branch**: main (initial commit, predates rule 5)
**Drafted on**: local Claude Code (matches rule 4)

> Note: this plan is retroactive. The work was completed before the
> collab rules were established. It is recorded here so future readers
> can audit the design decisions.

## Files to add / change

| Path | Action | Rationale |
|---|---|---|
| `scripts/generate_set_n_mrs.py` | new | single source of truth: derives all 71 MRs from helpers |
| `set_n_mrs/<subject>/*.{jir,jor}.txt` | generated | 142 DSL files written by the generator |
| `scripts/run_all.sh` | new | two-stage orchestrator; runs `randoop.py` + `pitest.py` upstream then EvaluateMRs |
| `scripts/parse_results.py` | new | per-subject mutant-kill matrix → JSON |
| `scripts/aggregate_metrics.py` | new | pooled Wilson CI + McNemar across 23 subjects |
| `setup.sh` | new | apt + pip + Zenodo download + GAssert build (idempotent) |
| `.env`, `.env.example`, `.gitignore` | new | path config + ignore pattern |
| `README.md` | new | design + protocol + output schema |

## Risks / tradeoffs

| Risk | Mitigation |
|---|---|
| GAssert parser rejects Path B (jor uses only `_s` vars) for single-execution invariants | Generator emits Path B; Stage 2 logs flag rejections; follow-up issue would rewrite to Path C |
| Reproducibility of upstream Randoop seeds across JDK builds | Fix to OpenJDK 8 in `setup.sh` (matches GenMorph paper environment) |
| Sequence DSL `Sequence.fromValue(...).flip()` semantic mismatch when used on integers vs char arrays | Tested only against arrays/strings; numeric subjects use `((double) i_<arg>_{s,f})` |
| `MathClass?millerRabinPrimeTest?0` admits no useful G/O_le MRs | Recorded as a finding (3 L* fixed-point MRs only); paper notes block emptiness |

## Test gate (rule 6)

- [x] Generator round-trip: re-running `generate_set_n_mrs.py` produces 23 / 71 / 142.
- [ ] Smoke test on a fixture `mutants_killed.csv` (added in chore/establish-collab-rules branch).

## Estimated cost

| Step | Time | Where |
|---|---|---|
| Implement scripts + DSL specs | one session | local |
| Run `setup.sh` | ~10 min | cloud (rule 4 OK once plan committed) |
| Stage 1 (Randoop + PIT × 23) | ~4–7 h | **local only** (rule 8) |
| Stage 2 (EvaluateMRs × 23) | ~30 min | local or cloud |
| Aggregation | <1 sec | anywhere |

## Done when

- [x] 23 subject dirs, 142 DSL files committed
- [x] Pipeline runs end-to-end on a fresh host
- [x] README documents design + reproduction steps
- [x] Initial commit on `main`
