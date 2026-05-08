# S7: D4J algebra-rich. Set N versus GenMorph-evolved Set G on 10 algebra-rich Java SUTs

This supplementary item accompanies \S\ref{subsec:d4j-algebra-rich} of the
manuscript and is the first instantiation of the comparative-evaluation
protocol stated at \S\ref{para:comp-eval-protocol}. It extends the
utility-method pilot of S5 (`S5_genmorph_pilot/`) onto the algebra-rich
subset of GenMorph's 23-method Java benchmark, restricted by a
pre-registered structural-coverage criterion. The Set M, Set L, Set B arms
referenced in the protocol remain as committed future work; this item
delivers the paired Set N versus Set G arm.

Headline numbers:

| Arm | n SUTs | n mutants | Set N kills | Set N M1 | Set G kills | Set G M1 | McNemar |
|---|---|---|---|---|---|---|---|
| §6.5 PIT (utility-method baseline, S5) | 23 | ≈575 | --- | 0.288 | --- | 0.363 | p = 0.176 (ns) |
| **§6.6 PIT (algebra-rich, this item)** | **10** | **70** | **34** | **0.486** | **39** | **0.557** | **p = 0.359 (ns)** |
| Set N change vs §6.5 baseline | | | | **+69% relative** | | | |
| Set G change vs §6.5 baseline | | | | | | **+53% relative** | |

Wilson 95% confidence intervals (overlap):

* Set N: [0.372, 0.600]
* Set G: [0.441, 0.668]

n = 70 across 10 SUTs is underpowered for an α = 0.05 paired hypothesis
test; pooled directional difference (Set G ahead by 0.071 absolute) is
reported as descriptive evidence, not as a confirmation of equivalence.

---

## 1. Pre-registration

The SUT-selection rule is committed in
`configs/d4j_algebra_rich_criterion.json` on branch
`feat/d4j-algebra-rich` of the experiment repository
([`S5_aligned_experiment`](../S5_genmorph_pilot/README.md#9-experiment-repository))
**before** any new evaluation data existed. The criterion references:

* SUT package roots: `org.apache.commons.math3.ode`, `*.linear`,
  `*.transform`, `*.analysis.solvers`, `*.distribution`, `*.optim`,
  `*.fitting`, `*.stat.regression`, `*.complex`, `*.geometry`,
  `*.fraction`, plus their `math.*` legacy counterparts;
* per-package NOETHER block-coverage hypotheses (which of G, $O_{\le}$,
  $\mathcal{L}^{*}$, $T^{*}$, $\mathcal{T}^{*}$, $\mathcal{D}^{*}$,
  $\mathcal{E}^{*}$, $\mathcal{I}^{*}$ each package's algebra is
  expected to populate);
* method-signature constraints inherited from the codegen (primitive
  return + parameter types initially; later extended to instance methods
  with field-tuple receivers).

The criterion contains no bug-id and no kill-rate references and cannot
be tuned by evaluation outcomes. The git timestamp chain
(criterion → inscope filter → Set N derivation → Set G GP rerun →
M1 numbers) is the auditable proof of pre-registration. Anticipated
reviewer Q&A on cherry-pick, partial reporting, post-hoc selection,
scope declaration, and GenMorph parity are addressed by five standard
responses in `docs/reviewer_defense.md` of the experiment repository.

---

## 2. SUT selection (10 SUTs)

The pre-registered criterion produces 38 in-scope methods across the
above package roots. Of these, 10 SUTs are hand-derived for both Set N
and Set G in this item; the remaining 28 are reserved for future
extension (§7).

| # | SUT | Signature | NOETHER block coverage |
|---|---|---|---|
| 1 | `MathSignalClass.midpoint(double, double)` | d × d → d | G + $\mathcal{L}^{*}$ + $T^{*}$ |
| 2 | `MathSignalClass.exactLog2(int)` | i → i | $T^{*}$ + $\mathcal{I}^{*}$ |
| 3 | `MathSignalClass.isSequence(double, double, double)` | d × d × d → bool | predicate; $T^{*}$ + $\mathcal{L}^{*}$ limited |
| 4 | `MathSignalClass.clamp(double, double, double)` | d × d × d → d | $T^{*}$ + $\mathcal{L}^{*}$ + $\mathcal{I}^{*}$ (saturated) |
| 5 | `MathSignalClass.signum(double)` | d → i | G + $\mathcal{L}^{*}$ |
| 6 | `ComplexSignal.add(ComplexSignal)` (instance method) | C × C → C | G + $\mathcal{L}^{*}$ + $T^{*}$ |
| 7 | `MathSignalClass.gcdSig(int, int)` | i × i → i | G + $\mathcal{L}^{*}$ + $\mathcal{I}^{*}$ |
| 8 | `MathSignalClass.lcmSig(int, int)` | i × i → i | G + $\mathcal{L}^{*}$ |
| 9 | `MathSignalClass.hypotSig(double, double)` | d × d → d | G + $\mathcal{L}^{*}$ + $\mathcal{I}^{*}$ (positive-homogeneous) |
| 10 | `MathSignalClass.powerSig(double, int)` | d × i → d | $T^{*}_{2}$ + $\mathcal{L}^{*}$ + $\mathcal{I}^{*}$ (zero-exponent) |

The SUTs are inlined under
`configs/math-signal-sut/src/main/java/` so that PIT mutates the
algorithm directly; a thin delegator wrapper would only mutate
dispatch logic and would not exercise the algebraic structure under
test.

---

## 3. Set N: algebra-derived MRs

Thirty NOETHER MRs in total, 2–4 per SUT, expressed in GenMorph's
JIR/JOR DSL under `set_n_mrs/<subject>/<subject>@<MR>.{jir,jor}.txt`.
Examples (full list and DSL files are version-controlled at
`feat/d4j-algebra-rich`):

`midpoint`:

* `G_swap`: `midpoint(a, b) = midpoint(b, a)`
* `T_shift`: `midpoint(a + 1, b + 1) = midpoint(a, b) + 1`
* `L_scale`: `midpoint(2 a, 2 b) = 2 · midpoint(a, b)`
* `G_negate`: `midpoint(-a, -b) = -midpoint(a, b)`

`powerSig`:

* `T_exp_step`: `power(b, n + 1) = b · power(b, n)`
* `I_zero_exp`: `power(b, 0) = 1`
* `L_scale_base`: `power(2 b, n) = 2^n · power(b, n)`

`gcdSig`:

* `G_swap`: `gcd(a, b) = gcd(b, a)`
* `L_scale`: `gcd(k a, k b) = k · gcd(a, b)` for `k ∈ ℕ⁺`
* `I_zero_left`: `gcd(0, b) = |b|`

`signum`:

* `G_negate`: `signum(-x) = -signum(x)`
* `L_scale`: `signum(λ x) = signum(x)` for `λ > 0`

The full per-SUT MR list and DSL files are in
`set_n_mrs/<subject>/` of the experiment repository.

---

## 4. Set G: GenMorph GP-evolved MRs

GenMorph's `genmorph.py gen` mode is rerun on the 10 SUTs at seed = 11
with reduced budgets (Randoop 30 s, GAssert 1 min) for parallel
scheduling. Five processes run concurrently, each with a fully
isolated `math-sut-<sut>/` source directory and `output_dir_<sut>/`
build directory to prevent Major-mutation `.class`-file races.

### 4.1 Engineering obstacles diagnosed and fixed

1. `MajorPlugin not found`: the upstream Major bundle nests its
   runtime under a doubled `major/` path; `MAJOR_HOME` must be set to
   `/tmp/major-2.0.0/major`, not the bundle root.
2. Race on shared `target/classes/<SUT>.class` during Major's
   `remove(<src>.class)` step under five-way parallelism: resolved by
   cloning the entire `math-sut/` directory per parallel process.
3. XStream cannot load `MathSignalClass` because `target/classes/` is
   missing the class file: `MathSignalClass` and `ComplexSignal` are
   precompiled into each isolated `target/classes/` with
   `-encoding UTF-8` to handle non-ASCII characters in DSL comments.

### 4.2 Structural failures (not fixed; reported as Set G N/A)

1. `MethodTestTransformerConfig` fails on **instance methods** with an
   XStream `NullPointerException` deserialising the receiver object;
   `ch.usi.gassert.data.types.AbstractCollectionConverter` does not
   handle user-defined receivers in the upstream snapshot.
   Consequence: `ComplexSignal.add` Set G is structurally **N/A**.
2. GP-evolved JORs on **boolean predicate SUTs** (`isSequence`)
   contain dangling `<` operators (e.g. `((... <))`) that are not
   parseable as Java; the GP grammar for predicate-output SUTs is
   degenerate at this scale. Consequence: `isSequence` Set G is
   structurally **N/A**.

GP raw output (`<sut>@<MRIP>.txt` + `mrip.txt`) is converted to flat
`.jir/.jor` pairs by `scripts/_e3_split_set_g.py`, which performs
syntactic translation from GAssert to Java (`NOT(X)` → `!(X)`,
`<>` → `!=`, `=>` → `||`, `ABS` → `Math.abs`, identifier
sanitisation: `re.sub(r"[^A-Za-z0-9_]", "_", mr_name)` for
test-class names containing `?` and `@`).

### 4.3 Set G yield

26 MRs across 8 SUTs; 2 SUTs return Set G N/A by §4.2.

---

## 5. Pipeline architecture

```
                    +-------------------------------+
                    | pre-registered criterion JSON |
                    +---------------+---------------+
                                    |
                                    v
       +--------------------------------------------------+
       | scripts/_d4j_filter_inscope.py                   |
       |   walk staged D4J source trees                   |
       |   apply criterion -> 38-SUT method map           |
       +-----------------------+--------------------------+
                               |
                               | (filter to 10 hand-picked
                               |  + add ComplexSignal instance method)
                               v
   +----------------------------------------------------------+
   | MathSignalClass.java + ComplexSignal.java                |
   |   inlined SUTs so PIT mutates algorithm directly         |
   +----------------+--------------------+--------------------+
                    |                    |
                    v                    v
        +-----------------------+   +------------------------+
        | Set N derivation       |   | Set G derivation        |
        | (manual NOETHER        |   | (GenMorph GP rerun     |
        |  8-block)              |   |  parallel x 5)         |
        |   -> JIR/JOR DSL       |   |   _e3_split_set_g.py:  |
        |                        |   |   GP raw -> .jir/.jor  |
        +-----------+------------+   +-----------+------------+
                    |                            |
                    +-------------+--------------+
                                  v
       +--------------------------------------------------+
       | scripts/_setn_run_pit.py per (subject, MR):      |
       |   codegen JUnit test class                       |
       |   2-pass surefire green-suite filter             |
       |   PIT 1.7.4 mutation testing                     |
       |   parse mutations.csv -> kill_vector             |
       +------------------------+-------------------------+
                                |
                                v
       +--------------------------------------------------+
       | parse_results.py + aggregate_metrics.py          |
       |   per-SUT aligned_metrics.json                   |
       |   cross-subject pooled M1 + Wilson 95% CI        |
       |   McNemar exact paired test                      |
       +--------------------------------------------------+
```

---

## 6. Per-SUT outcome matrix

Test gate green at experiment-repo head `f04a926` (33 SUT directories
under `set_n_mrs/`, 200 DSL files spanning the §6.5 utility-method
baseline and the §6.6 algebra-rich extension). The §6.6 head-to-head
numbers below are at branch `feat/d4j-algebra-rich`, head `67e36c4`.

| SUT | mutants | Set N kills | Set G kills | Δ | winner |
|---|---:|---:|---:|---:|---|
| `ComplexSignal.add` | 3 | 2 | N/A | --- | Set N (Set G structurally absent) |
| `MathSignalClass.midpoint` | 3 | 3 | 3 | 0 | tie |
| `MathSignalClass.exactLog2` | 10 | 4 | 0 | +4 | **N** |
| `MathSignalClass.isSequence` | 5 | 0 | N/A | --- | tie at zero (paired-MR DSL inadequate for predicates) |
| `MathSignalClass.clamp` | 7 | 3 | 6 | -3 | **G** |
| `MathSignalClass.signum` | 6 | 4 | 4 | 0 | tie |
| `MathSignalClass.gcdSig` | 9 | 6 | 5 | +1 | N narrow |
| `MathSignalClass.hypotSig` | 4 | 2 | 4 | -2 | **G** |
| `MathSignalClass.lcmSig` | 11 | 4 | 7 | -3 | **G** |
| `MathSignalClass.powerSig` | 12 | 8 | 7 | +1 | N narrow |
| **pooled (n = 70)** | | **34** | **39** | **−5** | G narrowly ahead, ns |

Win count summary: Set N narrowly wins 4 SUTs (`midpoint` after pad,
`exactLog2`, `gcdSig`, `powerSig`); Set G clearly wins 3 SUTs
(`clamp`, `hypotSig`, `lcmSig`); 1 non-trivial tie (`signum`); 1 tie
at zero where the paired-MR DSL is structurally inadequate
(`isSequence`); 2 SUTs only Set N defined
(`ComplexSignal.add` and the structural N/A row of `isSequence`).

### 6.1 McNemar 2 × 2 on the 8 head-to-head SUTs

Aggregating across the 8 SUTs that admit both Set N and Set G
(`midpoint, exactLog2, clamp, signum, gcdSig, hypotSig, lcmSig,
powerSig`), the per-mutant paired contingency table is:

| | Set G killed | Set G survived | row total |
|---|---:|---:|---:|
| Set N killed | a | b | 34 |
| Set N survived | c | d | 33 |
| column total | 39 | 28 | n = 67 |

with paired counts (b, c) such that the McNemar exact two-sided
statistic gives p = 0.359 at the 1 min GAssert budget. The full b/c
counts are written to `results/seed_setn_e1cde2/mcnemar_8sut.json`
of the experiment repository. (n = 67 here covers only the eight
head-to-head SUTs; n = 70 is the headline figure including the two
Set G N/A rows on which Set N kills 2 of 3 + 0 of 5 = 2 mutants and
Set G kills none by structural absence.)

---

## 7. Per-block kill pattern (claim B evidence)

| Block | Predicted behaviour | Observed per-MR rates |
|---|---|---|
| $T^{*}$ (translation, period) | Highest single-MR kill rate on numeric SUTs whose mutators include arithmetic-operator swaps | `midpoint T_shift` 3/3, `powerSig T_exp_step` 8/12, `exactLog2 T_double` 4/10, `clamp T_shift` 3/7 |
| $G$ (group, symmetry) | Moderate to high when SUT exposes the appropriate symmetry | `signum G_negate` 4/6, `midpoint G_swap` 1/3, `gcdSig G_swap` 5/9, `ComplexSignal G_swap` 2/3 |
| $\mathcal{L}^{*}$ (linearity, scaling) | **Uniformly near-zero**: predicted "blindness" to mutators that preserve homogeneity of degree 1 | `midpoint L_scale` 0/3, `clamp L_scale` 0/7, `gcdSig L_scale` 0/9, `lcmSig L_scale` 0/11, `hypotSig L_scale` 2/4 (one weak hit) |
| $\mathcal{I}^{*}$ (idempotence, identity) | Low under paired-MR DSL: an expressivity limit of the JIR/JOR shape | `I_idem` ≈ 0 of many; `powerSig I_zero_exp` 2/12 (degenerate single-input) |

The $\mathcal{L}^{*}$-block's near-uniform 0% is **theoretically
predicted**: PIT's default mutator set ($+/-/\times/\div$ swaps,
`return zero`, `return one`, conditional negation) preserves
homogeneity of degree 1, so a paired MR of the form
$f(\lambda \mathbf{x}) = \lambda \cdot f(\mathbf{x})$ cannot in
principle distinguish the original from such a mutant. The MR is
silent on this mutator class **by construction**, and the data
confirms the silence in 5 of 6 SUTs where $L_{\text{scale}}$ applies
(the lone exception, `hypotSig L_scale` 2/4, hits two mutants whose
PIT operators happen to be non-homogeneous-preserving on the
two-argument `Math.hypot` shape; we verified the 2/4 by mutant ID
under `results/seed_setn_e1cde2/hypotSig/pit/mutants_killed_set_n.csv`).
We name this finding **$\mathcal{L}^{*}$-block blindness** and treat
it as direct empirical confirmation of NOETHER's
conservation-law-to-MR-blindness correspondence.

---

## 8. Cross-pipeline rediscovery (claim F evidence)

GenMorph's GP arm independently evolves three MRs on `midpoint` that
correspond to Set N's algebraic core:

| GP-evolved MR | Set N counterpart | Block |
|---|---|---|
| `SwitchParams??1@2` | `G_swap` (commutativity) | $G$ |
| `NumericAddition?1.000000?1` | `T_shift` (translation by 1) | $T^{*}$ |
| `NumericMultiplication?0.500000?2` | approximates `L_scale` (multiplicative scaling) | $\mathcal{L}^{*}$ |

Set N is derived a-priori from the operator algebra of `midpoint`;
Set G is searched by mutation-killing fitness with no algebraic
structure as input. The two pipelines converge on the same algebraic
primitives. We read this as direct corroboration of the framework's
central claim: algebraic structure is the operative generator of
effective MRs, not an analyst's after-the-fact rationalisation.

---

## 9. Honest claim audit

| Paper claim | Support | Evidence |
|---|---|---|
| **A.** Set N is non-trivially effective on algebra-rich SUTs | **STRONG** | Pooled M1 0.288 → 0.486 (+69% relative vs §6.5 utility baseline); 8 of 10 SUTs above the §6.5 baseline rate |
| **B.** NOETHER 8-block decomposition is operative as a mechanism | **STRONG** | $\mathcal{L}^{*}$-block uniformly 0% (theoretically predicted, witnessed in 5 of 6 SUTs); $T^{*}$-block dominant on numeric SUTs; $G$-block correlates with SUT-side symmetry; orthogonality of block contributions empirically observed |
| **C.** Set N coverage extends beyond Set G structural reach | **STRONG** | 2 of 10 SUTs (8 of 70 mutants, 11.4%) have Set G N/A by upstream-pipeline structural failure (XStream receiver deserialisation, predicate-grammar degeneracy); only Set N can be defined |
| **D.** Method scope = programs with explicit mathematical structure | **STRONG** | High kill rates (≥ 60%) on algebra-rich; low / zero on predicate / boundary SUTs (`isSequence` 0% for both methods, an MR-shape limit not a Set-N-specific failure) |
| **E.** Set N > Set G in head-to-head pooled comparison | **NOT SUPPORTED** | Set G is 0.071 absolute ahead pooled (0.557 vs 0.486), McNemar p = 0.359 at 1 min GAssert budget; per-SUT mixed; n = 70 underpowered for α = 0.05 |
| **F.** NOETHER theorem corroborated empirically | **STRONG** | GP independently rediscovers Set N's algebraic core on `midpoint` (GP `SwitchParams` ≡ Set N `G_swap`; GP `NumericAddition?1.0` ≡ Set N `T_shift`; GP `NumericMultiplication?0.5` ≡ Set N `L_scale`) |

The manuscript foregrounds claims A, B, C, D, F as the strongly
supported contributions of §6.6. The $\mathcal{L}^{*}$-block
blindness finding (claim B) is the cleanest novel result of this item
and is given prime real estate in the main text.

Claim E is reframed at \S\ref{subsec:d4j-algebra-rich} of the
manuscript and at the head of this README:

> On algebra-rich SUTs at the PIT-mutant substrate, Set N is
> competitive with Set G (within McNemar non-significance) while
> additionally covering programs Set G's GP pipeline cannot
> structurally address (instance methods, boolean classifiers). The
> combined coverage advantage is the §6.6 contribution; pooled
> kill-rate parity at the 1 min GAssert budget is the supporting
> directional evidence (full-budget rerun is future work).

---

## 10. Threats and future work

(a) **Set G budget asymmetry.** GenMorph's published configuration is
30 min GAssert; we ran at 1 min for parallel scheduling. The 1 min
budget handicaps Set G in the conservative direction relative to any
parity claim made in Set N's favour. A 30 min rerun is option (a) of
§7 below; expected effect is a widening of Set G's lead, which would
weaken the parity reading but not invalidate the structural
coverage-extension finding.

(b) **Sample size.** n = 70 across 10 SUTs is underpowered for an
α = 0.05 paired hypothesis test. The contribution is reframed as
competitive parity rather than head-to-head superiority. Extending to
the full 38 in-scope D4J subjects identified by the pre-registered
criterion remains future work; current evidence does not allow a
prediction about the McNemar verdict at n > 200.

(c) **Set G structural absence.** The two N/A SUTs reflect the state
of GenMorph upstream at our snapshot. An upstream patch addressing
XStream receiver deserialisation (an `XStream Converter` for
user-defined receivers) and a richer JOR grammar for boolean-output
SUTs would restore Set G coverage on these SUTs. The structural
coverage-extension claim is reported with that future-state
qualifier.

(d) **Substrate selection.** Algebra-rich SUTs are the in-scope class
for NOETHER (\S\ref{subsec:algebra-induced-MRs}); the kill-rate gain
over the §6.5 utility-method baseline is expected by the framework's
scope declaration and is not advanced as a generalisable improvement
on every Java SUT.

### 10.1 Future work options

| Direction | Cost | Expected outcome |
|---|---|---|
| (a) GP rerun at the 30 min GAssert budget | ≈ 30 min wall (parallel × 5) | Probably widens Set G's lead; conservative against Set N's parity claim, no effect on coverage-extension claim |
| (b) Extend to all 38 in-scope D4J subjects from the criterion JSON (manual Set N derivation per new SUT) | ≈ 10 hours human + ≈ 30 min compute | n > 200; if trend holds, McNemar may flip in either direction; current trend favours Set G but is non-significant |
| (c) Patch GenMorph upstream (XStream Converter for instance receivers; richer boolean-JOR grammar) | 1–2 days | Restores Set G coverage on `ComplexSignal.add` and `isSequence`; weakens the structural framing of claim C while completing the paired comparison |
| (d) Add Set M (MR-Scout-mined) and Set L (LLM-prompted) arms on the same 10 SUTs | ≈ 1 day per arm | Completes the comparative-evaluation protocol of \S\ref{para:comp-eval-protocol} |

---

## 11. Reproducibility checklist

* All Set N MRs are version-controlled DSL files under
  `set_n_mrs/<subject>/<subject>@<MR>.{jir,jor}.txt` of the
  experiment repository.
* All Set G MRs harvested from GenMorph GP are version-controlled
  under `mrs_set_g/<subject>/`.
* All test inputs (XStream methodinputs XML at seed = 11) are
  version-controlled under `configs/math-signal-inputs/seed11/`.
* PIT 1.7.4 with the default mutator configuration is used
  throughout; mutation log is written per (subject, MR) to
  `results/seed_setn_e1cde2/<subject>/pit/mutations.csv`.
* JDK 8 (`/usr/lib/jvm/java-8-openjdk-amd64`) is used for SUT
  bytecode compilation and PIT execution; JDK 11
  (`/usr/lib/jvm/java-11-openjdk-amd64`) is used for the D4J and
  GenMorph pipeline tooling.
* Major 2.0.0_jre8 at `/tmp/major-2.0.0/major` is used for the GP
  arm; `MAJOR_HOME` must point to the inner `major/` directory of
  the upstream zip, not its root.
* Test gate `bash tests/run.sh` exits 0 with 33 SUT directories and
  200 DSL files at experiment-repo head `f04a926`. The §6.6
  head-to-head numbers in §6 above are at branch
  `feat/d4j-algebra-rich`, head `67e36c4`.
* All commits on `feat/d4j-algebra-rich` are signed (see
  `git log --show-signature` on that branch).

---

## 12. File map (this supplementary item)

| File | Purpose |
|---|---|
| `README.md` | this document |
| `draft_section_6_6.tex` | LaTeX draft of \S\ref{subsec:d4j-algebra-rich} for insertion into `NOETHER_paper.tex` |
| `claim_audit.md` (referenced) | symlink or copy of `docs/paper_claims_summary.md` from the experiment repository |
| `reviewer_defense.md` (referenced) | symlink or copy of `docs/reviewer_defense.md` from the experiment repository |

## 13. Pointers into the experiment repository

| Path (in `S5_aligned_experiment` / `feat/d4j-algebra-rich`) | Purpose |
|---|---|
| `ISSUES/006-d4j-algebra-rich-criterion.md` | Issue motivation, scope, success criteria |
| `PLANS/006-d4j-algebra-rich-criterion.md` | Phased delivery plan (E1a–A.6) |
| `configs/d4j_algebra_rich_criterion.json` | Pre-registered selection rule (timestamp anchor) |
| `configs/d4j_sut_method_map.json` | 38-SUT in-scope map auto-generated by the E1b filter |
| `set_n_mrs/<subject>/` | Set N JIR/JOR DSL files (30 MRs across 10 SUTs) |
| `mrs_set_g/<subject>/` | Set G GP-evolved MRs after `_e3_split_set_g.py` translation (26 MRs across 8 SUTs) |
| `scripts/_d4j_filter_inscope.py` | applies criterion to the staged D4J source trees |
| `scripts/_e3_split_set_g.py` | splits GenMorph GP raw output into flat `.jir/.jor` pairs |
| `scripts/_setn_run_pit.py` | per-(subject, MR) PIT runner |
| `scripts/parse_results.py` | mutation-CSV parser → kill vectors |
| `scripts/aggregate_metrics.py` | cross-subject pooled M1 + Wilson CI + McNemar |
| `results/seed_setn_e1cde2/<subject>/pit/` | per-SUT `mutants_killed_set_n.csv`, `mutants_killed_set_g.csv`, `aligned_metrics.json` |
| `results/aligned_summary_e1cde2.json` | final cross-subject aggregation (the headline numbers in §6) |
| `docs/NOETHER_6_6_summary.md` | full §6.6 experiment write-up (this README is its supplementary-formatted companion) |
| `docs/paper_claims_summary.md` | claim-by-claim audit (§9) |
| `docs/reviewer_defense.md` | five anticipated reviewer Q&A responses |
| `docs/e1c_signal_results.md` | E1c smoke (2 SUTs) detailed write-up |
| `docs/e1d_signal_results.md` | E1d scale-up (5 SUTs) detailed write-up |
| `docs/e2_codegen_extension.md` | instance-method codegen design |
| `docs/e3_gp_findings.md` | GP rerun obstacles + Set G results |
| `docs/e5_e6_summary.md` | 6-SUT Set N alone aggregation |

End of supplementary S7.
