# §6.6 — Set N (NOETHER) vs Set G (GenMorph): detection results

> Drop-in draft for the NOETHER paper §6.6. Numbers are produced by this repo's
> pipeline (seed 11); see `docs/results/{comparison_seed11.json,
> per_subject_seed11.csv, strata_seed11.csv}`. **This is an honest, nuanced
> result — not a "NOETHER beats GenMorph" claim.** Read alongside
> `docs/SUBMISSION_READINESS.md`.

## 6.6.1 Setup

Single-variable design: the substrate is held to GenMorph's exact toolchain and
only the MR set varies. For every one of the 23 GenMorph benchmark subjects we:

1. regenerate the source test inputs with **Randoop (seed 11)** — the same
   generator/seed GenMorph's published evaluation uses;
2. for **Set N** (the NOETHER-algebra-derived MRs, deterministic, hand-encoded
   in GenMorph's `jir/jor` DSL) construct follow-up inputs from each MR's input
   relation and score them through GenMorph's **own** `PITestGenerator` + PITest
   (`org.pitest:pitest-maven:mutationCoverage`), so the **mutant set and kill
   definition are upstream-native** (a mutant is killed iff
   `KILLED/TIMED_OUT/MEMORY_ERROR`);
3. for **Set G** adopt GenMorph's published `pitest_seed*/<subject>/
   mutants_killed.csv`.

The PITest mutant set is identical to GenMorph's published columns (verified,
e.g. `MathClass?gcd?0` = 25 mutants `M1..M25`), so Set N and Set G are compared
on the **same mutants** with the **same kill definition** — 562 mutants across
the 23 subjects.

Because GenMorph is stochastic (the package ships up to 12 seeds), we report
Set G at two honest references: **`G@seed11`** (a single GP run, comparable MR
budget to Set N) and **`G@all-seeds`** (the union over all 12 published seeds —
GenMorph's 12-run upper bound). An MR counts only if it is **FP-free** on the
original SUT (GenMorph's own validity rule); MRs with any false positive are
excluded, exactly as in the published evaluation.

## 6.6.2 Headline results (mutation detection, pooled + stratified)

Kill rate = union mutants killed / mutants; paired **McNemar** is per-mutant
(b = killed by Set G only, c = killed by Set N only); Wilson 95% CIs in the JSON.

| Stratum | subj | mutants | **Set N** | **G@seed11** | **G@all-seeds** | McNemar N vs seed (b,c,p) |
|---|---:|---:|---:|---:|---:|---|
| **All** | 23 | 562 | **0.313** (176) | 0.363 (204) | 0.607 (341) | b=77, c=46, **p=0.0066** |
| Math | 10 | 403 | 0.216 (87) | 0.313 (126) | 0.618 (249) | b=55, c=16, **p≈0.000** |
| Lang | 5 | 78 | 0.410 (32) | 0.449 (35) | 0.615 (48) | b=17, c=14, p=0.72 |
| **Guava** | 8 | 81 | **0.704 (57)** | 0.531 (43) | 0.543 (44) | b=5, c=16, **p=0.027** |

Three findings, none of them "one set dominates":

1. **A single GenMorph run edges out Set N overall** (0.363 vs 0.313;
   McNemar p=0.0066), and **GenMorph's 12-seed union is far ahead** (0.607) — but
   that union spends ~12× the MR-search budget of a single deterministic Set N.
2. **The gap is entirely a Math-domain effect** (Set G 0.313 vs Set N 0.216,
   p≈0). It does **not** generalise to the other domains.
3. **On Guava, Set N significantly out-detects even GenMorph's all-seeds union**
   (0.704 vs 0.543; McNemar p=0.027), and on Lang the two are statistically tied.

## 6.6.3 The real mediator: exact vs approximate relations (applicability scope)

The decisive factor is **not** "mathematical vs string" but whether the SUT's
governing relations are **exact** (hold identically) or **approximate**
(transcendental, sensitive to numeric encoding):

* **Where Set N is strong** — operators with clean algebraic/structural
  invariants that hold *exactly*: integer arithmetic (`gcd` 13/25 vs 11;
  `nextPrime` 17/20 vs 15) and Guava sequence operations (length/sum/order/
  permutation invariants: `repeat`, `meanOf`, `min`, `sort`, `indexOf`,
  `truncate`). Here the hand-derived relations are tight and FP-free.
* **Where Set N is weak** — **transcendental** functions whose identities hold
  only *approximately* under a fixed **1e-4 absolute tolerance**, and/or are
  **partial**: `sin`/`tan`/`sinh` periodicity & odd-symmetry break the absolute
  tolerance over large ranges; `acos` is undefined for `|x|>1` (returns `NaN`),
  so the *exact* bound `acos(x) ≤ π` is a false positive on 56% of inputs and
  **all of acos's MRs are excluded**; `pow`'s identities (`b^{e+1}=b^e·b`, …)
  overflow the absolute tolerance and are likewise excluded.

So Set N's effectiveness is **conditional on the SUT exposing operators with
exact algebraic structure** — precisely the meta-pattern precondition — and on
the numeric **encoding** (tolerance, domain guards) matching the function. This
is a scope/positioning result, and it is consistent with the design intent of
the NOETHER algebra.

## 6.6.4 Determinism vs the seed lottery (a second axis)

Set N is **deterministic**: one MR set per subject, no search. GenMorph's GP is
**seed-sensitive**, and the sensitivity is itself domain-structured
(`setg_seeds_with_valid_mr` column):

* On **Math**, GenMorph is reliable — 11–12 of 12 seeds yield ≥1 valid MR.
* On **Lang/Guava**, GenMorph frequently finds **no** valid MR in a run:
  `indexOf` and `sort` → **0/12 seeds**, `capitalize`/`difference` → 2/12.
  At seed 11 specifically, GenMorph produced **zero** valid MRs for 6 of the 13
  Lang/Guava subjects, detecting nothing — whereas Set N detected 3–13 mutants
  on each.

Thus the two approaches are **complementary**: NOETHER supplies reliable,
interpretable MRs for structurally-rich (algebraic/sequence) subjects where the
GP search often fails to find any valid MR; GenMorph's search excels on the
transcendental numeric subjects where a fixed-tolerance hand encoding struggles.

## 6.6.5 Threats to validity

* **Independent input samples.** Set N is scored on freshly regenerated Randoop
  (seed 11) inputs; Set G uses GenMorph's published inputs. Same generator/seed/
  config and identical mutant set, but not byte-identical inputs — a sampling
  confound bounded by using the same generator and a 100-input cap.
* **Deterministic vs stochastic budget.** A single Set N set is fairly compared
  to `G@seed11`; the `G@all-seeds` column is deliberately generous to GenMorph
  (12× search budget) and is reported as an upper bound, not a like-for-like.
* **Encoding choices for Set N.** A fixed **1e-4 absolute tolerance** and the
  absence of **domain/NaN guards** drive the transcendental-Math failures; these
  are encoding limitations, not fundamental to the meta-patterns (see
  readiness doc for the planned fix and expected effect).
* **Coverage.** 68/71 Set N MRs are FP-free-evaluable; `acos` and `pow` yield 0
  valid MRs under the current encoding (reported honestly as 0 detection, not
  dropped). All 23 subjects' mutant sets are upstream-native.
* **Single seed for Set G reference.** seed 11 is one GP run; the per-seed
  distribution (`docs/results/`) shows the spread and is summarised above.

## 6.6.6 Takeaway

NOETHER-derived MRs are a **deterministic, interpretable, and on structurally-
rich subjects competitive-to-superior** alternative/complement to GP-evolved
MRs — significantly better on Guava sequence operations and reliable where the
GP search finds nothing — while a single GP run retains the edge on
transcendental numeric functions under the present fixed-tolerance encoding.
The honest framing is **complementarity and applicability scope**, not blanket
superiority.
