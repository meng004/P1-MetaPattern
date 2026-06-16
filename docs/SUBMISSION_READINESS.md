# Submission-readiness assessment — NOETHER §6.6 experiment

**Date:** 2026-06-16 · **Scope:** the Set N vs Set G comparative experiment in
this repo (seed 11, 23 GenMorph subjects). **Bottom line up front:** the
*infrastructure and data are real and reproducible*, but the experiment is **not
yet ready to support a strong "NOETHER beats GenMorph" claim**. It *is* close to
ready for an honest **"deterministic, interpretable, complementary, scope-bound"**
contribution, provided the framing matches the data and 3–4 gaps are closed.

## 1. Verdict

| Aspect | State | Note |
|---|---|---|
| Pipeline correctness & reproducibility | **Ready** | thin wrapper over GenMorph's own toolchain; identical mutant sets; `bash tests/run.sh` green; resumable |
| Data (seed 11, 23 subjects) | **Ready (as a first pass)** | honest, complete except 2 subjects 0-valid under current encoding |
| Headline claim "Set N ≥ Set G" | **Not supported** | a single GP run edges Set N overall (p=0.0066); Set N wins only on Guava |
| Honest claim "complementary / scope-bound / deterministic" | **Supportable** | Guava win (p=0.027), GP seed-failures on Lang/Guava, determinism — all real |
| Fairness of the Math comparison | **At risk** | Set N's Math losses are confounded by encoding (abs tolerance, no domain guards) |
| Statistical rigor | **Needs a second test** | pooled per-mutant McNemar ignores within-subject correlation |
| External validity | **Limited** | one benchmark (GenMorph), n=23, one seed for Set N |

**Recommendation:** *Major-revision-distance* from a strong claim; *minor-to-
moderate* from an honest scoped paper. Reframe to complementarity/applicability
(as in `SECTION_6_6_RESULTS.md`), and close gaps G1–G3 below before submission.

## 2. What is solid (defensible today)

* **Same-substrate comparison.** Set N is scored through GenMorph's *own*
  `PITestGenerator` + PITest on the *identical* published mutant set (verified),
  with the identical kill definition and FP-validity rule. This is the
  experiment's core strength.
* **Guava result.** Set N significantly out-detects even GenMorph's 12-seed
  union on Guava (0.70 vs 0.54; McNemar p=0.027). Robust and notable.
* **Determinism / seed-lottery finding.** GenMorph yields **0 valid MRs** in a
  single run for 6/13 Lang+Guava subjects (and 0/12 seeds for `indexOf`,
  `sort`); Set N is deterministic and always produced valid MRs there. Strong,
  novel, and well-evidenced.
* **Honesty of accounting.** 0-valid subjects (`acos`, `pow`) are recorded as
  0 detection, not dropped; Set G reported at both single-seed and all-seeds.

## 3. Gaps that block a strong claim (ranked)

**G1 — Encoding confounds the Math comparison (highest priority).**
Set N's Math deficit is substantially an *encoding artifact*, not a method
deficit: a fixed **1e-4 absolute tolerance** fails for large-range
transcendental outputs, and missing **domain/NaN guards** make exact bounds
(e.g. `acos(x) ≤ π`) false-positive on out-of-domain inputs — excluding *all*
of `acos`/`pow`'s MRs. Until this is addressed, "Set G > Set N on Math" is not a
fair methodological statement.
*Fix:* (a) relative/ULP tolerance for floating outputs; (b) guard partial-domain
relations (`isNaN(out) || …`). Both are localized changes in
`generate_set_n_mrs.py`; the pipeline re-runs unchanged. **Est. 0.5–1 day +
~1 h compute.** Expected effect: recovers `acos`, lifts `sin/tan/sinh/pow`
validity; the Math gap should shrink materially (direction, not magnitude,
claimable a priori).

**G2 — Input-sampling fairness.**
Set N uses freshly regenerated Randoop(seed 11) inputs; Set G uses GenMorph's
published inputs (same generator/seed/config, identical mutants, but not
byte-identical). *Fix options:* (a) calibrate — regenerate Set G natively via
GAssert on our substrate (Major is installed) for a few subjects and confirm it
reproduces the published kills, demonstrating input equivalence; or (b) state
the confound explicitly and bound it. **Est. 0.5 day (b) / 1–2 days + compute (a).**

**G3 — Statistical test independence.**
Pooled per-mutant McNemar treats 562 mutants as independent, but mutants within
a subject are correlated. *Fix:* add a subject-level paired test (Wilcoxon
signed-rank on per-subject rates, or a mixed-effects model) as the primary
inferential statistic; keep McNemar as descriptive. **Est. 2–3 h** (extend
`compare_sets.py` + a test).

**G4 — Seed breadth for Set N substrate.**
The whole experiment is seed 11. Set N is deterministic, but its *inputs* and
PITest are seeded. *Fix:* re-run Set N substrate over ≥3 seeds and report
stability. **Est. ~half a day compute** (pipeline already parameterized by seed).

## 4. Smaller issues / polish

* `results/` is gitignored; the committed snapshot lives in `docs/results/`.
  Decide what the paper's artifact package ships.
* 3 Guava `flip` MRs are now implemented (array reverse); re-confirm no other MR
  is silently skipped (`setn_followups.py` logs UNSUPPORTED — currently none).
* Effective-MR-ratio / minimality (sister metric) is out of scope here but the
  reviewer may ask; note it.
* Per-subject `join` has no published Set G data (1 subject) — acknowledge.

## 5. Concrete path to "ready"

1. **G1** encoding fixes → re-run → refresh `SECTION_6_6_RESULTS.md` numbers.
2. **G3** add subject-level paired test.
3. **G2** Set-G calibration on ~3 subjects (input-equivalence evidence).
4. (Optional, strengthens) **G4** multi-seed Set N.
5. Final framing: keep the **complementarity / applicability-scope /
   determinism** thesis; do **not** claim blanket superiority.

After G1–G3 the experiment should support a credible, honestly-scoped §6.6.
Total estimated effort: **~2–3 focused days + a few hours of compute**, all on
the existing (now-working) pipeline.

## 6. One-line readiness score

**Pipeline 9/10 · Data 7/10 · Claims-as-currently-tempting 4/10 ·
Claims-if-reframed-to-complementarity 7/10 · Writing 6/10 (draft in
`SECTION_6_6_RESULTS.md`).** Net: **honest scoped submission within reach;
strong-superiority submission not supported by the current data.**
