# PLAN-003: rewrite run_all.sh as a faithful orchestrator over GenMorph + a Set N follow-up emitter

**Issue**: ISSUES/003-run-all-pipeline-broken.md
**Branch**: claude/inspiring-pascal-1gkf8q
**Drafted on**: cloud Claude Code — Rule 4's local-only clause **explicitly waived by
the repo owner** for this cloud rewrite; the upstream sources the rule protects are
present at `/tmp/genmorph_pilot/`, and the full flow has been empirically validated
here (see "Validated facts").

## Validated facts (empirical, this session)

* Real entry point: `scripts/run/genmorph.py {gen,eval,all} <cfg…>`; `evaluation()`
  in `scripts/strategy/genmorph.py` writes `pitest_seed{seed}/<subject>/mutants_killed.csv`
  via PITestGenerator + `mvn org.pitest:pitest-maven:mutationCoverage`.
* With Major 2.0.0 (jre8) installed, `genmorph all` runs end-to-end on
  `MathClass?gcd?0` (exit 0) and the produced `mutants_killed.csv` has **25 mutants
  `M1..M25` — identical to the published seed-11 gcd CSV**. FP-filter + MS columns
  behave exactly as upstream (`mrs_status.csv`).
* Nothing intermediate ships in the Zenodo package; substrate is regenerated.
* **MR→follow-up pairing is by transformation name** (PITestGenerator.java:176-202):
  the `.jor` is read from `mrs/<exp>/<sut>/<sut>@<transform>.jor.txt`; follow-up
  inputs are `<sut>@<testid>@<transform>.methodinputs`, paired by matching
  `<transform>`; a `<sut>@<transform>.cmrip` marker enumerates the MR. The
  published Set G MRs are renamed `MR0..MRn` (no transform), so they are **not**
  directly evaluable by the native flow without the (unshipped) mrinfo mapping.
  → Set N slots straight in: construct its follow-ups under its own transform
  name and run the upstream emitter + PIT unchanged.
* Box: 4 cores / 15 GB / no swap; `GASSERT_HEAP=16g`.

## Architecture of the rewrite

`run_all.sh` becomes a thin orchestrator (no hand-wired randoop/pitest flags):

1. **Per-subject substrate** (cached, reused by both MR sets): drive upstream to
   produce build + source test inputs + states + `*.transformations.txt` + sampled
   transformations + PIT mutant set. Skip GAssert MR-*learning* on the main path
   (we use published Set G MRs, not newly-learned ones) — the dominant cost and the
   16 GB OOM hazard.
2. **Set G**: the canonical result is the upstream-published
   `pitest_seed11/<subject>/mutants_killed.csv` (mutant set verified identical to ours).
   Published MRs (`MR0..`) can't be re-run natively (rename strips the transform), so
   we **calibrate** instead: on a few subjects, regenerate Set G natively via
   `genmorph all` (full GAssert) and confirm it reproduces the published kills — this
   validates that our regenerated seed-11 substrate (source inputs in particular)
   matches upstream's, which is what makes the Set N comparison fair.
3. **Set N**: construct follow-up `.methodinputs` from each Set N MR's input relation
   (`*.jir`), named `<sut>@<testid>@<setN-transform>`, drop the `<sut>@<setN-transform>.cmrip`
   marker + `.jor.txt`, and run the **upstream PITestGenerator + PIT unchanged** so Set N
   is scored on the **same `M1..M25`** with the **same kill definition** (`genmorph.py:345`)
   and the **same source inputs** as the calibration.
4. **Compare**: pooled kills + Wilson CI + paired McNemar (Set N vs Set G) on the
   shared mutant set, per subject and across all 23.

`--jobs N` runs independent subjects concurrently (default 2; RAM-bound, cap 3).

## Files to add / change

| Path | Action | Rationale |
|---|---|---|
| `scripts/run_all.sh` | rewrite | orchestrate the validated flow; `--subject`, `--jobs N`, `--stage` |
| `scripts/setn_followups.py` | new | construct Set N follow-up `.methodinputs` from `*.jir` input relations |
| `scripts/gen_subject_config.py` | new | emit per-subject GenMorph configs (gcd-style) for `--subject`/parallel runs |
| `scripts/compare_sets.py` | new | Set N vs Set G on shared mutants: pooled rate, Wilson CI, McNemar |
| `scripts/parse_results.py` | adjust | read the real `pitest_seed*/<subj>/mutants_killed.csv` schema (per-MR × mutant) |
| `tests/test_setn_followups.py` | new | rule 6: `.jir` → follow-up inputs for known transforms (perm/scale/…) |
| `tests/test_compare_sets.py` | new | rule 6: synthetic kill matrices → correct McNemar / CI |
| `tests/run.sh` | extend | add a guarded single-subject end-to-end smoke (skips if toolchain absent) |

## Risks / tradeoffs

* **Set G calibration drift.** Regenerated transformations/test-inputs may not bit-match
  the published run (stochastic generators, seed sensitivity). Detect: diff our Set G
  `mutants_killed.csv` vs `setg_baseline/`. Mitigate: report both; the *comparison* only
  needs Set N and Set G scored by the **same** harness on the **same** mutants.
* **Set N → follow-up fidelity.** Input-relation construction must match each `*.jir`'s
  intent. Detect: assert generated follow-ups satisfy the `.jir` predicate (compile a
  check); spot-check per transform family.
* **Compute time.** ~40–50 min/subject at full budgets (GAssert skipped); ~6–8 h for 23
  at `--jobs 2-3`. Resumable (per-subject caching). Reduced budgets for iteration.
* **OOM.** Never run GAssert in parallel; cap `--jobs`; watch PIT/EvoSuite JVM heaps.

## Test gate (rule 6)

- [ ] `tests/test_setn_followups.py` + `tests/test_compare_sets.py` cover new code
- [ ] single-subject end-to-end smoke produces a real `mutants_killed.csv` (25 cols for gcd)
- [ ] `bash tests/run.sh` exits 0

## Estimated cost

| Step | Time | Where |
|---|---|---|
| Implement + unit tests | ~half day | cloud |
| Single-subject smoke | ~15–20 min | cloud |
| Full 23-subject run (`--jobs 2-3`, GAssert skipped) | ~6–8 h | cloud (nohup, resumable) |
| compare_sets.py | <1 sec | anywhere |

## Done when

- [ ] `bash scripts/run_all.sh --subject 'MathClass?gcd?0'` produces a real
      `results/seed11/MathClass?gcd?0/mutants_killed.csv` for **both** sets + comparison.
- [ ] Set-G calibration vs `setg_baseline/` recorded (exact-or-explained).
- [ ] Full run yields `results/aligned_summary.json` with measured Set N & Set G kills,
      Wilson CIs, paired McNemar across the 23 subjects.
- [ ] `bash tests/run.sh` exits 0.
