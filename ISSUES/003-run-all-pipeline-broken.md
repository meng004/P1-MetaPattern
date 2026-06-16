# ISSUE-003: scripts/run_all.sh cannot run end-to-end (interface mismatch with GenMorph upstream)

**Status**: done — pipeline rewritten + runs end-to-end; experiment executed
(seed 11, all 23 subjects). Results: `docs/SECTION_6_6_RESULTS.md`
(+ `docs/results/`). Remaining method refinements (encoding tolerance, domain
guards, subject-level stats, input-fairness calibration) are tracked in
`docs/SUBMISSION_READINESS.md`, not pipeline bugs.
**Owner**: cloud Claude Code session (rewrite authorized by repo owner — see Update)
**Branch**: claude/inspiring-pascal-1gkf8q
**Plan**: PLANS/003-run-all-pipeline-broken.md (authored this session; Rule 4's
local-only clause explicitly waived by the repo owner for this cloud rewrite, and
the GenMorph upstream sources the rule protects are present at /tmp/genmorph_pilot/).
**Opened**: 2026-06-16

## Update 2026-06-16 — environment unblocked, path chosen

Investigation since the original write-up materially changed the picture:

* **Real entry point is upstream's own orchestrator.** The faithful flow is
  `scripts/run/genmorph.py {gen,eval,all} <config…>`; `evaluation()` in
  `scripts/strategy/genmorph.py` writes `mutants_killed.csv` via PITestGenerator
  + `mvn org.pitest:pitest-maven:mutationCoverage`. The rewrite will be a thin
  orchestrator over this, not the hand-wired randoop/pitest call (the original
  defect).
* **Nothing intermediate ships.** The Zenodo package holds only MR DSL
  (`*.jir/*.jor`) + result CSVs — zero `.state.json` / `.methodinputs` /
  `.transformations.txt`. All execution state must be regenerated locally.
* **Blocker ① (Major missing) RESOLVED.** The repo owner supplied the download;
  `setup.sh` now installs **Major 2.0.0 (jre8)** — the version GenMorph's README
  pins and that produced the published results, and the JDK-8-matched build.
  Verified: the full upstream `genmorph all` now runs end-to-end on
  `MathClass?gcd?0` (EvoSuite 23 s, Major 26 s, then state-gen → GAssert →
  PITestGenerator → PIT).
* **Blocker ② (Set N has no follow-up generator).** Every upstream evaluator
  derives follow-up inputs from a constructive transformation spec, not from a
  bare `.jir` predicate. Set N (hand-authored predicates) therefore needs its
  follow-up inputs constructed from each MR's input relation.
* **Chosen path (repo owner's decision): custom/hybrid detection harness.**
  Substrate + a faithful Set G come from the upstream native flow (Set G
  calibrated against the published seed-11 `mutants_killed.csv`); Set N
  follow-ups are constructed from input relations and scored on the **same PIT
  mutant set** with the **same kill definition** (`genmorph.py:345`) so the
  Set N vs Set G comparison is apples-to-apples on identical mutants.
* **Speed levers (4 cores / 15 GB, no swap).** The main path skips GAssert
  (`-Xmx16g`, ~30 min×4/subject) *and* gen's per-mutant state loop — both exist
  only for MR *learning*, which we don't do (we use published Set G MRs).
  Remaining cost is PIT (one `mvn pitest` per MR); parallelize at the subject
  level (`--jobs`, cap 2–3, RAM-bound). Subagents do NOT add compute
  parallelism (shared cores/RAM) and risk OOM — not used.

Next: author `PLANS/003`, rewrite `scripts/run_all.sh` over `genmorph.py` with a
Set N follow-up emitter + `--jobs N`, add a real single-subject end-to-end test
(Rule 6).

## Why

A cloud run of the full sequence (`tests/run.sh` → `setup.sh` → `run_all.sh`)
was attempted. `tests/run.sh` passed and `setup.sh` succeeded (JDK8/11, Python
deps, Zenodo package ~80 MB downloaded — egress to zenodo.org is *not* blocked —
GAssert jar present). Before launching the advertised "4–7 h" Stage 1, the
orchestrator was audited and **empirically tested on one subject**. It is
**non-functional**: it cannot produce `states`, `mutants_killed.csv`, the
alignment check, or any Set N detection. A blind `nohup run_all.sh` would not
burn 4–7 h — Stage 1 fails immediately per subject, Stage 2 then SKIPs/errors,
and the run produces an **empty** `aligned_summary.json`. Reporting that as a
result would violate the experiment's honesty constraints, so the run was
stopped here.

## Findings (evidence)

**① Stage-1 CLI interface mismatch (empirically reproduced).**
`run_all.sh:123-127,136-140` calls
`python3 scripts/run/{randoop,pitest}.py --config <c> --seed <s> --subject <subj>`.
But upstream `scripts/tools/randoop.py:main` takes **positional** args
(`sys.argv[1]=classpath`, `sys.argv[2:]=randoop_args`) and `tools/pitest.py:main`
takes a single positional `workdir`. Actual output when invoked the way
run_all.sh invokes them:

```
randoop → "Unrecognized command: configs/evaluation-config-math.json."   (no states produced)
pitest  → FileNotFoundError: [Errno 2] No such file or directory: '--config'
          (tools/pitest.py:267  Popen(cwd='--config', ...))
```

→ `output_dir_{math,lang,guava}/states_seed11/...` and `.../pitest_seed11/...`
are never created. Every subject's Stage-1 cache check misses; nothing is built.

**② Stage-2 produces the wrong filename + needs inputs that never exist.**
`EvaluateMRs.java` writes per-MR `*.results.csv` (`RESULTS_EXTENSION=".results.csv"`,
a TP/FP/TN/FN matrix), **not** `mutants_killed.csv`. But `run_all.sh:207`
gates `parse_results.py` on `[[ -f "$OUT_DIR/mutants_killed.csv" ]]` — a file
EvaluateMRs never writes — so `parse_results.py` never runs and no
`aligned_metrics.json` is produced. (The real producer of `mutants_killed.csv`
is the full `tools/pitest.py` flow.) Furthermore `EvaluateMRs` requires
per-execution `states` (`*.state.json`) + `classifications`; the Zenodo package
ships **zero** `.state.json` files and no classification dirs, and Stage 1
(finding ①) cannot generate them → `EvaluateMRs` would throw
`sourceStates has no systemIds`.

**③ Set G MRs are never staged into the path Stage 2 reads.**
`run_all.sh:163` reads MRs from `$GENMORPH/output_dir_${lib}/assertions_seed11/<subj>`,
but upstream Set G MRs live at `/tmp/genmorph_pilot/mrs/assertions_seed11/<subj>`.
No copy step bridges the two.

**④ No alignment-validation step exists.**
The task requires re-running EvaluateMRs on Set G alone and diffing it against
upstream's published `mutants_killed.csv`. `run_all.sh` contains no such diff,
and (per ②) the published CSV is a pitest-flow artifact, not an EvaluateMRs one.

**Root cause.** `run_all.sh` is a re-written, simplified orchestrator whose
contract with the GenMorph upstream toolchain was never validated end-to-end.
`tests/run.sh` only `bash -n` syntax-checks it and unit-tests
`parse/aggregate/generate` against synthetic fixtures; nothing exercises the
real upstream call path.

## Scope (of the fix — for the LOCAL plan)

- `scripts/run_all.sh`: drive the **real** GenMorph evaluation flow. Likely
  reuse upstream top-level entry points (e.g. `scripts/run/genmorph.py`,
  `evaluate_*.py`, `gen_run_scripts.py`) rather than hand-wiring randoop/pitest
  flags; correct Stage-1 invocation; stage Set G MRs + inject Set N; generate
  `states`/`classifications`; produce `mutants_killed.csv` via the pitest flow.
- New explicit **alignment-validation** step: Set-G-only re-run vs upstream
  `evaluation/pitest_seed11/<subj>/mutants_killed.csv`; abort if mismatch.
- `tests/`: an end-to-end smoke on ≥1 subject that asserts a real
  `mutants_killed.csv` is produced and parsed (Rule 6).

## Out of scope

- Set N MR semantics / DSL (unchanged; `set_n_mrs/` already validated by
  `tests/test_generate_mrs.py`).
- k* / minimal-subset analysis (sister paper T2 — this is a detection-only
  experiment).
- The interim **Set G baseline** delivered alongside this issue
  (`setg_baseline/`) — that is a read-only adoption of upstream-published
  numbers and does not touch the pipeline.

## Success criteria

- [ ] `bash scripts/run_all.sh --subject 'MathClass?gcd?0'` produces a real
      `results/seed11/MathClass?gcd?0/mutants_killed.csv` + `aligned_metrics.json`.
- [ ] Set-G-only alignment check reproduces upstream
      `pitest_seed11/<subj>/mutants_killed.csv` exactly (else hard-abort).
- [ ] Full run yields `results/aligned_summary.json` with **measured** Set N
      and Set G kills, Wilson CIs, and paired McNemar across the 23 subjects.
- [ ] `bash tests/run.sh` (incl. the new end-to-end smoke) exits 0.

## References

- Upstream sources: `/tmp/genmorph_pilot/genmorph_full/genmorph/`
  (`scripts/tools/{randoop,pitest}.py`, `src/main/java/ch/usi/gassert/EvaluateMRs.java`),
  configs `configs/evaluation-config-{math,lang,guava}.json`.
- Upstream published Set G results: `evaluation/pitest_seed11/<subj>/mutants_killed.csv`.
- Upstream Set G MR DSL: `mrs/assertions_seed11/<subj>/`.
- Interim Set G baseline: `setg_baseline/` (this commit).
- Offending lines: `run_all.sh:123-140` (Stage1 flags), `:196-213` (Stage2
  EvaluateMRs + mutants_killed.csv gate), `:163` (MR dir).
