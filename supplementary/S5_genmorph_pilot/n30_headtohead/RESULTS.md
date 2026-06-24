# n>=30 commons-math head-to-head: Set N (NOETHER) vs baselines

Effectiveness evidence for the NOETHER MetaPattern framework. This expands the
S5 pilot (n=3 SUTs, ~77 PIT mutants) to **n = 36 Apache Commons Math 3.6.1
methods / 836 PIT mutants**, comparing Set N (NOETHER-derived MRs) against
generic literature and METRIC+ baselines on a shared, real mutation substrate.

All numbers below are computed from real PIT 1.15.3 runs over the actual Apache
Commons Math 3.6.1 bytecode. No baseline numbers are fabricated. Blocked
baselines (GenMorph at scale, LLM) are listed explicitly in
[Section: BLOCKED](#blocked-baselines-and-subjects).

Reproduce: `python3 run_pit.py && python3 parse_kill_matrix.py && python3 compute_stats.py`
(requires Java 21 + Maven 3.9 + commons-math3 3.6.1 from Maven Central).

---

## 1. Headline result

| Set | Detected / total | Rate | Wilson 95% CI |
|---|---|---|---|
| **Set N (NOETHER)** | **313 / 836** | **0.374** | **[0.342, 0.408]** |
| Set B (literature, generic MR) | 154 / 836 | 0.184 | [0.159, 0.212] |
| Set M (METRIC+ D×R category) | 151 / 836 | 0.181 | [0.156, 0.208] |

Set N detects roughly **twice** the mutant fraction of either baseline, with
non-overlapping Wilson 95% CIs.

### Pairwise paired tests (mutant = matched unit)

| Pair | both | N-only | other-only | neither | McNemar exact p (2-sided) | Bonferroni (α=0.025) | Risk diff (95% CI) | Paired OR (95% CI) |
|---|---|---|---|---|---|---|---|---|
| **N vs B** | 154 | **159** | **0** | 523 | 2.74e-48 | significant | +0.190 [0.164, 0.217] | 319 [19.9, 5122] |
| **N vs M** | 151 | **162** | **0** | 523 | 3.42e-49 | significant | +0.194 [0.167, 0.221] | 325 [20.2, 5218] |

- Discordant pairs b+c = 159 (N vs B) and 162 (N vs M): **the paired test is
  well-powered at α = 0.05** (not underpowered; cf. the S5 pilot whose discordant
  cells were small).
- **Set N strictly subsumes both baselines on this substrate**: there are
  **zero** mutants killed by Set B or Set M that Set N misses (other-only = 0 in
  both pairs). Every mutant a baseline kills, Set N also kills.
- Effect sizes are large and one-directional (RD ≈ +0.19; paired OR > 300), all
  CIs excluding the null (RD CI excludes 0; OR CI excludes 1).

The Bonferroni family is the 2 pre-registered pairwise tests (Set N vs each
runnable baseline), so per-test α = 0.05 / 2 = 0.025. Both p-values clear it by
~46 orders of magnitude.

---

## 2. D1 / D2 stratification (algebra-disrupting vs algebra-preserving mutators)

Mutators are partitioned by whether they disrupt the algebraic structure the MRs
constrain (explicit mapping in `parse_kill_matrix.py`):

- **D1 (algebra-disrupting)**: `MathMutator`, `ConditionalsBoundaryMutator`,
  `RemoveConditionalMutator_*`, `InvertNegsMutator`, `NegateConditionalsMutator`,
  `IncrementsMutator`, etc. -- change arithmetic / relational / branch semantics.
- **D2 (algebra-preserving)**: `*ReturnsMutator` (Primitive/Empty/Boolean/Null/
  Object), `VoidMethodCallMutator`, constructor/non-void-call mutators --
  replace the result or remove a call without rewriting the operation.

| Stratum | n mutants | Set N | Set B | Set M | N vs B McNemar p | N vs M McNemar p |
|---|---|---|---|---|---|---|
| D1 | 721 | 0.366 | 0.183 | 0.173 | 3.67e-40 (sig) | 2.87e-42 (sig) |
| D2 | 115 | 0.426 | 0.191 | 0.226 | 1.49e-08 (sig) | 2.38e-07 (sig) |

Set N dominates in **both** strata, with all four McNemar tests significant
after Bonferroni. The effect is not an artefact of one mutator family. (Exact
per-stratum p-values and effect sizes are in `results/headtohead_stats.json`.)

---

## 3. Per-SUT breakdown (36 SUTs)

Each SUT is a single commons-math method whose program-induced algebra admits at
least one non-empty NOETHER MetaPattern **beyond the plain permutation block G**
(the scope precondition; `blocks` column lists the NOETHER blocks each SUT's
Set N touches: G = permutation, L* = scaling/homomorphism, T* = translation,
I* = identity/inverse, O_le = order/monotonicity). Mutant counts are the PIT
mutations whose `mutatedMethod` + descriptor match the SUT method exactly
(sibling/helper/overload mutations filtered out at parse time).

Full machine-readable table: `results/per_sut_summary.csv`. Summary:

| SUT | method | blocks | n | cov | N | B | M |
|---|---|---|---|---|---|---|---|
| au_gcd_int | ArithmeticUtils.gcd (II)I | G,L*,O_le,I* | 25 | 18 | 8 | 5 | 6 |
| au_gcd_long | ArithmeticUtils.gcd (JJ)J | G,L*,O_le,I* | 39 | 39 | 31 | 24 | 24 |
| au_lcm_int | ArithmeticUtils.lcm (II)I | G,L*,I* | 5 | 5 | 3 | 0 | 0 |
| au_addcheck_int | ArithmeticUtils.addAndCheck | G,T*,I* | 6 | 6 | 3 | 2 | 3 |
| au_mulcheck_int | ArithmeticUtils.mulAndCheck | G,L*,I* | 6 | 6 | 3 | 2 | 2 |
| au_subcheck_int | ArithmeticUtils.subAndCheck | G,T*,I* | 6 | 6 | 3 | 2 | 2 |
| au_pow_int | ArithmeticUtils.pow (II)I | L*,I* | 10 | 7 | 6 | 4 | 2 |
| cu_binom | CombinatoricsUtils.binomialCoefficient | G,I*,O_le | 42 | 23 | 15 | 3 | 3 |
| cu_factorial | CombinatoricsUtils.factorial | L*,I*,O_le | 5 | 5 | 3 | 2 | 2 |
| au_stirling | ArithmeticUtils.stirlingS2 | I*,O_le | 1 | 1 | 1 | 1 | 1 |
| fm_hypot | FastMath.hypot | G,L*,I* | 22 | 20 | 13 | 11 | 11 |
| fm_signum_d | FastMath.signum | G,L* | 5 | 5 | 2 | 2 | 2 |
| fm_abs_d | FastMath.abs | L*,I* | 2 | 2 | 1 | 1 | 0 |
| fm_max_d | FastMath.max | G,T*,I* | 11 | 9 | 5 | 4 | 5 |
| fm_min_d | FastMath.min | G,T*,I* | 11 | 9 | 5 | 4 | 5 |
| fm_floor | FastMath.floor | T*,I*,O_le | 15 | 13 | 5 | 5 | 5 |
| fm_ceil | FastMath.ceil | T*,I*,O_le | 9 | 8 | 5 | 4 | 3 |
| fm_exp | FastMath.exp | L*,O_le | 1 | 1 | 1 | 1 | 0 |
| fm_log | FastMath.log | L*,O_le | 1 | 1 | 0 | 0 | 0 |
| fm_log10 | FastMath.log10 | L*,O_le | 15 | 14 | 11 | 4 | 9 |
| fm_log1p | FastMath.log1p | L*,O_le | 27 | 24 | 9 | 2 | 8 |
| fm_expm1 | FastMath.expm1 | L*,O_le | 1 | 1 | 1 | 0 | 1 |
| fm_sqrt | FastMath.sqrt | L*,O_le | 1 | 1 | 1 | 1 | 0 |
| fm_cbrt | FastMath.cbrt | G,L*,O_le | 82 | 76 | 51 | 5 | 5 |
| fm_sin | FastMath.sin | G,L*,O_le | 26 | 22 | 13 | 4 | 13 |
| fm_cos | FastMath.cos | G,L*,O_le | 20 | 16 | 11 | 4 | 10 |
| fm_tan | FastMath.tan | G,L*,O_le | 37 | 34 | 14 | 5 | 5 |
| fm_sinh | FastMath.sinh | G,L*,O_le | 123 | 104 | 19 | 4 | 4 |
| fm_cosh | FastMath.cosh | G,L*,O_le | 67 | 48 | 12 | 10 | 0 |
| fm_tanh | FastMath.tanh | G,L*,O_le | 109 | 106 | 27 | 11 | 4 |
| fm_atan | FastMath.atan | G,L*,O_le | 1 | 1 | 0 | 0 | 0 |
| fm_toradians | FastMath.toRadians | L*,I* | 14 | 13 | 10 | 10 | 7 |
| fm_todegrees | FastMath.toDegrees | L*,I* | 12 | 12 | 10 | 10 | 7 |
| fm_copysign | FastMath.copySign | L*,I* | 6 | 6 | 6 | 2 | 2 |
| fm_scalb | FastMath.scalb | L*,I* | 72 | 8 | 4 | 4 | 0 |
| fm_pow_di | FastMath.pow (DI)D | L*,I* | 1 | 1 | 1 | 1 | 0 |
| **TOTAL** | | | **836** | **671** | **313** | **154** | **151** |

Per-SUT, Set N is **never worse** than either baseline and strictly better on
many (e.g. `fm_cbrt` 51 vs 5; `fm_sinh` 19 vs 4; `fm_tanh` 27 vs 11; `cu_binom`
15 vs 3; `au_gcd_long` 31 vs 24). The few all-equal rows (e.g. `au_stirling`,
`fm_signum_d`) are SUTs whose only killable mutants fall to the shared generic
MR; the two 0/0/0 rows (`fm_log`, `fm_atan`) are SUTs whose single target-method
mutant is killed by no MR in any set (honestly reported, not dropped).

### Note on small per-SUT mutant counts

Several FastMath methods have a tiny target-method mutant population (e.g.
`fm_exp`, `fm_log`, `fm_sqrt`, `fm_atan` = 1) because FastMath's public method
body delegates to internal helpers / JDK intrinsics, so PIT finds few mutable
statements in the method body itself (we count only mutants inside the SUT
method's own descriptor, not its helpers -- the precise "method = SUT" scope).
Individual small-n SUTs are descriptive; the **pooled n = 836 is the inferential
basis** and is well-powered.

---

## 4. Subjects and scope precondition

- **36 SUTs**, all Apache Commons Math 3.6.1 static methods drawn from
  `org.apache.commons.math3.util.{ArithmeticUtils, CombinatoricsUtils, FastMath}`.
- Each satisfies the paper's pre-registered scope precondition (S7 SUT-selection
  rule; `protocol_path_a_headtohead.md`): the program-induced operator algebra
  admits at least one non-empty NOETHER MetaPattern **beyond block G**. Every SUT
  in the table above lists a block other than G.
- The library is mutated directly: `maven-dependency-plugin` unpacks
  commons-math3-3.6.1's `.class` files into `target/classes`, and PIT mutates the
  real Apache bytecode (not a re-implementation). This is the same substrate
  family as the S5 pilot and S7.

### MR sets

- **Set N (NOETHER)**: 2--4 MRs per SUT derived from the SUT's operator algebra
  (CONSTRUCT-MP style), spanning the SUT's non-empty blocks (G/L*/T*/I*/O_le).
  Total 120 Set N MR @Test methods across the 36 SUTs.
- **Set B (literature)**: one generic metamorphic relation per SUT, drawn from
  the standard MT catalogue (commutativity / bound / identity), matching the S5
  pilot's "single generic literature MR" baseline (Segura et al. 2016 survey
  patterns).
- **Set M (METRIC+)**: the METRIC+ D×R category scaffold (Sun et al. 2021),
  instantiated per SUT as the applicable category pairs (perm-invariant /
  additive-invariant / scale-homogeneous / sign-invariant / sign-flip). This is
  the same scaffold used in `experiment_realbug/mr_sets/set_M_metric.py` and
  `S8`, ported to commons-math granularity.

All 120 Set N + 36 Set B + 52 Set M MR test methods **pass on the unmutated
Apache Commons Math 3.6.1** (208 baseline tests, 0 failures) -- i.e. no MR is a
false positive on correct code. Validated before mutation analysis.

---

## 5. Honest caveat: baseline subsumption is structural, by construction

Set N kills a strict superset of Set B and Set M (other-only = 0). This is
**not** an accident of tuning: Set B and Set M are deliberately the *generic*
relations (commutativity, sign, bounds, additive/scale invariance) that the
literature and METRIC+ catalogues supply without an operator-algebra analysis,
and these generic relations are a **subset** of the per-SUT relations NOETHER
derives. The result therefore measures exactly the paper's claim -- that an
algebra-driven derivation surfaces MRs (homomorphisms, Euclid invariance,
refinement orders, period/phase relations) that generic catalogues miss -- and
quantifies the gap as a +19 percentage-point kill-rate difference on a real
mutation substrate.

A fully *independent* baseline (one that could kill mutants Set N misses) would
require either GenMorph's GP-evolved MRs or an LLM-prompted set; both are blocked
in this environment (next section). Where GenMorph's evolved MRs **do** exist
(the gcd/sin pilot SUTs), Set G is genuinely complementary (gcd: Set G 17/25 vs
Set N 5/25 in the pilot; sin: the reverse, Set N 11/26 vs Set G 2/26), which is
why GenMorph remains the most informative comparator and is recorded as the
priority blocked item rather than dropped.

---

## 6. BLOCKED baselines and subjects

Recorded honestly per CLAUDE.md (诚实优先于救援, C6). No blocked-baseline numbers
are fabricated. Machine-readable: `results/setG_status.json`.

| Item | Status | Exact blocker |
|---|---|---|
| **Set G (GenMorph)** -- 34 of 36 new SUTs | **BLOCKED** | GenMorph ships no fixed MR catalogue; its MRs are GP-evolved per SUT with PIT-kill fitness, needing the GAssert + Randoop + pitest-wrapper-1.7.4 toolchain and a multi-minute GP search per SUT. Published evolved MRs exist only for the 2 pilot SUTs (`MathClass?gcd?0`, `MathClass?sin?0`). The S7 README documents two structural failures that block re-evolution at scale: a race on the shared `target/classes/<SUT>.class` during Major/PIT compile, and degenerate GP grammar for boolean-predicate-output SUTs. |
| **Set G (GenMorph)** -- gcd, sin | **AVAILABLE (real, separate)** | Real GenMorph-evolved Set G from the S5 pilot: gcd 17/25 (68%), sin 2/26 (7.7%) -- PIT **1.7.4**, GenMorph Randoop seed-11 inputs. **Not pooled** with the n30 Set N/B/M numbers because the n30 runs use PIT **1.15.3** and a different (deterministic, boundary-seeded) input distribution; cross-tool/cross-distribution pooling would be invalid. Reported as a separate anchor in `results/setG_status.json`. |
| **Set L (LLM-prompted)** | **BLOCKED** | No LLM API key reachable in this environment (`ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `DEEPSEEK_API_KEY` / `ZHIPU_API_KEY` / `MOONSHOT_API_KEY` / `GEMINI_API_KEY` / `DASHSCOPE_API_KEY` all unset; no `.env`). An LLM-prompted MR set cannot be generated without a model endpoint. |
| Subjects (n>=30) | **ACHIEVED (n=36)** | Maven Central reachable; commons-math3 3.6.1 + PIT 1.15.3 resolved. 36 >= 30 target met. |
| Defects4J algebra-rich (S7) subjects | **NOT RUN here** | The S7 subjects (`MathSignalClass`, `ComplexSignal`) are an inlined re-implementation curated for the GenMorph DSL; resolving them adds no new in-scope algebra beyond the 36 live commons-math methods above and would re-introduce the GenMorph toolchain dependency. The n>=30 target is met with live commons-math methods directly, so D4J was not needed. |

---

## 7. Power statement (honest)

The pooled paired comparison is **well-powered at α = 0.05**: discordant pair
counts are 159 (N vs B) and 162 (N vs M), far above the ~5 needed for an exact
McNemar test to be able to reach significance, and both strata (D1: 721 mutants;
D2: 115 mutants) independently clear Bonferroni. This is the positive
effectiveness evidence the body paper deferred, and it is **not underpowered** --
in contrast to the small-n pilots elsewhere in the supplement which are flagged
descriptive. The only honesty qualifier is the structural one in Section 5
(baselines are generic subsets of Set N), and the blocked independent comparators
(GenMorph at scale, LLM) in Section 6.

---

## 8. Files

| File | Contents |
|---|---|
| `sut_registry.py` | Single source of truth: 36-SUT roster + per-SUT Set N/B/M MRs + PIT scope |
| `gen_tests.py` | Emits one JUnit-4 test class per SUT (Set N + B + M) from the registry |
| `run_pit.py` | Per-SUT PIT 1.15.3 driver (mutationCoverage, fullMutationMatrix) |
| `parse_kill_matrix.py` | mutations.xml -> kill matrix CSV (descriptor-filtered, D1/D2 tagged) |
| `compute_stats.py` | Wilson CI + McNemar exact + risk difference + paired OR + Bonferroni + strata |
| `harness/pom.xml`, `harness/src/test/java/headtohead/T_*.java` | Maven project + generated test classes |
| `results/kill_matrix.csv` | One row per (SUT, mutant): set_n/set_b/set_m + per-MR + mutator + stratum + status |
| `results/per_sut_summary.csv` | Per-SUT detection counts + rates + D1/D2 split |
| `results/headtohead_stats.json` | Full stats (pooled, pairwise, stratified, per-SUT) |
| `results/setG_status.json` | Set G / Set L blocked-status + real gcd/sin Set G anchor |
| `pit_reports/<sut>/mutations.xml` | Raw PIT output per SUT |
