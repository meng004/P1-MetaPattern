# Multiseed Set-G (GenMorph) effectiveness — published 12-seed replication

> Source: GenMorph replication package (Zenodo 10067096) `evaluation.zip`, `pitest_seed{11,12,13,21,22,23,31,32,33,41,42,43}/<subject>/mutants_killed.csv`.
> Metric: matched (gen seed == PIT seed) union-kill of all FP-valid GenMorph MRs (the `assertions_seed{S},*` summary row). No recomputation.


## Focus subjects (where NOETHER Set N comparison applies)

### MathClass?gcd?0
- mutants=25, killable-by-any-GenMorph-seed=21
- per-seed Set G union kills: s11=11, s12=17, s13=18, s21=17, s22=12, s23=10, s31=17, s32=18, s33=18, s41=18, s42=14, s43=10
- mean=15, sd=3.21, min=10, max=18, spread=8, CV=0.214
- **seed11=11 → rank 3/12 (low→high), 61% of best-seed**

### MathClass?sin?0
- mutants=26, killable-by-any-GenMorph-seed=17
- per-seed Set G union kills: s11=16, s12=16, s13=16, s21=13, s22=16, s23=15, s31=13, s32=17, s33=13, s41=17, s42=15, s43=17
- mean=15.33, sd=1.49, min=13, max=17, spread=4, CV=0.097
- **seed11=16 → rank 6/12 (low→high), 94% of best-seed**


## All 23 subjects — is seed=11 representative for Set G?

| subject | s11 | mean | min | max | spread | rank(low→high) |
|---|--:|--:|--:|--:|--:|--:|
| GuavaClass?indexOf?0 | 0 | 6.2 | 0 | 11 | 11 | 1/5 |
| GuavaClass?join?0 | None | 4 | 4 | 4 | 0 | None/1 |
| GuavaClass?meanOf?0 | 10 | 10 | 10 | 10 | 0 | 1/12 |
| GuavaClass?min?0 | 5 | 5.75 | 5 | 6 | 1 | 1/12 |
| GuavaClass?padStart?0 | 6 | 6 | 6 | 6 | 0 | 1/10 |
| GuavaClass?repeat?0 | 16 | 15.58 | 13 | 16 | 3 | 3/12 |
| GuavaClass?sort?0 | 0 | 4.67 | 0 | 6 | 6 | 1/12 |
| GuavaClass?truncate?0 | 6 | 5.57 | 4 | 7 | 3 | 4/7 |
| LangClass?abbreviate?0 | 18 | 17.91 | 14 | 23 | 9 | 5/11 |
| LangClass?capitalize?0 | None | 7.5 | 7 | 9 | 2 | None/4 |
| LangClass?center?0 | 8 | 7.64 | 5 | 10 | 5 | 4/11 |
| LangClass?difference?0 | 0 | 2.33 | 0 | 4 | 4 | 1/9 |
| LangClass?isSorted?0 | 9 | 9.5 | 8 | 11 | 3 | 2/4 |
| MathClass?acos?0 | None | 32.5 | 31 | 35 | 4 | None/4 |
| MathClass?gcd?0 | 11 | 15 | 10 | 18 | 8 | 3/12 |
| MathClass?log10?0 | 8 | 7.33 | 7 | 8 | 1 | 3/3 |
| MathClass?millerRabinPrimeTest?0 | None | 9.78 | 8 | 17 | 9 | None/9 |
| MathClass?nextPrime?0 | 15 | 15.58 | 13 | 16 | 3 | 2/12 |
| MathClass?pow?0 | 7 | 6.83 | 6 | 7 | 1 | 3/12 |
| MathClass?sin?0 | 16 | 15.33 | 13 | 17 | 4 | 6/12 |
| MathClass?sinh?0 | 36 | 42.45 | 31 | 56 | 25 | 2/11 |
| MathClass?stirlingS2?0 | 17 | 15.83 | 9 | 20 | 11 | 8/12 |
| MathClass?tan?0 | 16 | 14 | 12 | 20 | 8 | 11/12 |

**seed=11 lands in the bottom third of seeds for 11/19 subjects and the top third for only 2/19** (Set G union-kill). The single-seed head-to-head therefore did not use a seed favourable to Set G; if anything seed=11 understates Set G, so the disclosed 'Set N dominated by Set G' result is robust to (or strengthened by) seed choice rather than a selection-bias artefact.
