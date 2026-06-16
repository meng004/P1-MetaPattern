# Set G detection baseline (GenMorph, seed 11) — interim, read-only

> **This is NOT the §6.6 aligned comparison.** It is the **Set G half only**,
> adopted from GenMorph upstream's *already published* numbers. **Set N is not
> evaluated** here — see the gap statement below and
> [`ISSUES/003-run-all-pipeline-broken.md`](../ISSUES/003-run-all-pipeline-broken.md).

## Why this exists

A cloud run of the full sequence reached `run_all.sh` and found it
**non-functional** (its CLI/data-flow contract does not match the GenMorph
upstream toolchain; empirically reproduced — ISSUE-003). The full Set N vs
Set G comparison cannot be produced in this environment because evaluating
Set N needs per-execution `states`/`classifications` that only a working
Stage 1 can generate, and the Zenodo package ships none.

Rather than fabricate or emit an empty `aligned_summary.json`, this delivers
the part that *is* trustworthy: Set G's detection on the 23-subject benchmark,
taken verbatim from upstream `evaluation/pitest_seed11/<subject>/mutants_killed.csv`.

## Result (Set G, seed 11)

| | value |
|---|---|
| Subjects in benchmark | 23 |
| Subjects with Set G seed11 data | **22** (`GuavaClass?join?0` missing upstream) |
| Total mutants (22 subjects) | **557** |
| **Set G kills** | **204** |
| **Set G kill rate** | **0.3662** |
| **Wilson 95% CI** | **[0.3273, 0.4070]** |
| Effective Set G MRs (kill ≥1) / total DSL MRs | 38 / 83 = 0.530 |
| Set N | **not evaluated** (placeholder) |
| Paired McNemar (N vs G) | **n/a** (needs Set N) |

### Per-subject (Set G, seed 11)

| Subject | n_mut | kills | kill_rate | effMR/total | note |
|---|--:|--:|--:|--:|---|
| MathClass?acos?0 | 76 | 0 | 0.000 | 0/4 | no valid Set G MR @seed11 |
| MathClass?gcd?0 | 25 | 11 | 0.440 | 2/4 | |
| MathClass?log10?0 | 15 | 8 | 0.533 | 1/4 | |
| MathClass?millerRabinPrimeTest?0 | 25 | 0 | 0.000 | 0/4 | no valid Set G MR @seed11 |
| MathClass?nextPrime?0 | 20 | 15 | 0.750 | 2/4 | |
| MathClass?pow?0 | 10 | 7 | 0.700 | 3/4 | |
| MathClass?sin?0 | 26 | 16 | 0.615 | 3/4 | |
| MathClass?sinh?0 | 123 | 36 | 0.293 | 2/4 | |
| MathClass?stirlingS2?0 | 46 | 17 | 0.370 | 3/4 | |
| MathClass?tan?0 | 37 | 16 | 0.432 | 3/4 | |
| LangClass?abbreviate?0 | 39 | 18 | 0.462 | 2/4 | |
| LangClass?capitalize?0 | 10 | 0 | 0.000 | 0/3 | no valid Set G MR @seed11 |
| LangClass?center?0 | 12 | 8 | 0.667 | 2/4 | |
| LangClass?difference?0 | 6 | 0 | 0.000 | 0/4 | MRs present but 0-kill |
| LangClass?isSorted?0 | 11 | 9 | 0.818 | 2/3 | |
| GuavaClass?indexOf?0 | 12 | 0 | 0.000 | 0/4 | MRs present but 0-kill |
| GuavaClass?join?0 | — | — | — | 0/4 | **MISSING upstream (seed11)** |
| GuavaClass?meanOf?0 | 12 | 10 | 0.833 | 3/3 | |
| GuavaClass?min?0 | 9 | 5 | 0.556 | 2/3 | |
| GuavaClass?padStart?0 | 7 | 6 | 0.857 | 3/4 | |
| GuavaClass?repeat?0 | 18 | 16 | 0.889 | 3/4 | |
| GuavaClass?sort?0 | 8 | 0 | 0.000 | 0/4 | MRs present but 0-kill |
| GuavaClass?truncate?0 | 10 | 6 | 0.600 | 2/3 | |

Per-block (NOETHER 8-block) decomposition is a **Set N** property and is
therefore **not reportable here** (Set N unevaluated). Set G is GP-evolved and
has no block structure.

## Honesty / provenance

- **As-published, not re-aligned.** Set G numbers are taken directly from
  upstream `evaluation/pitest_seed11/<subject>/mutants_killed.csv`, rows where
  `EXPERIMENT == assertions_seed11` and `MR != '*'`. They are **not** locally
  recomputed — the task's alignment check (re-run EvaluateMRs vs published CSV)
  needs the same broken pipeline (ISSUE-003), so it could not be performed.
- **Self-consistency check (passed).** For every subject with data, the union
  recomputed over its `assertions_seed11` MR rows equals upstream's
  pre-aggregated `assertions_seed11,*` row. The extractor hard-aborts on any
  mismatch; none occurred.
- **`set_n` / McNemar are absent, not zero.** Every `set_n_*` field in the
  per-subject `aligned_metrics.json` is a structural placeholder produced by
  feeding an empty Set-N directory to `parse_results.py`; it is **not** a
  measured Set N result.

### Underpowered / honest gaps

- `GuavaClass?join?0`: upstream produced no `mutants_killed.csv` for seed11
  (only `mrs_status.csv`); join is largely empty across seeds. Excluded from
  the pooled denominator, reported as missing.
- `acos`, `capitalize`, `millerRabinPrimeTest`: zero Set G MRs survive
  upstream's FP filter at seed11 → kills = 0 is a **real upstream outcome**.
- `difference`, `indexOf`, `sort`: Set G MRs exist for seed11 but kill 0
  mutants (kill_rate 0.000, effMR 0).
- Pooling treats each mutant as an independent Bernoulli trial; this
  underestimates variance (intra-subject mutants share SUT/inputs/mutator).

## Reproduce

```bash
bash setup.sh                       # populates /tmp/genmorph_pilot (Zenodo)
python3 setg_baseline/extract_setg_baseline.py
cat setg_baseline/setg_baseline_summary.json
```

## Files

```
setg_baseline/
├── extract_setg_baseline.py        # read-only extractor (self-consistency check inside)
├── setg_baseline_summary.json      # pooled Set G + per-subject + caveats
├── README.md                       # this file
└── seed11/<subject>/
    ├── mutants_killed.csv           # upstream seed11 Set G rows (filtered)
    ├── mrs_status.csv               # upstream FP/MS status (copied)
    └── aligned_metrics.json         # via scripts/parse_results.py (set_n = placeholder)
```
