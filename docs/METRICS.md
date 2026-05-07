# Metrics Reference — S5 Aligned Experiment

Single-source-of-truth specification for every metric the pipeline
computes when comparing **Set N** (NOETHER algebraic MRs) against
**Set G** (GenMorph GP-evolved MRs) on the 23-subject GenMorph benchmark.

For each metric: **purpose**, **formula**, **parameter meaning**, and
the **code location** where it is computed.

---

## Notation

For a single subject:

| Symbol | Meaning |
|---|---|
| `M` | Number of mutants for this subject (PIT-generated, fixed). |
| `𝓝`, `𝓖` | Set N (NOETHER) and Set G (GenMorph) MR sets. |
| `\|𝓝\|`, `\|𝓖\|` | Number of MRs in each set. |
| `kills(m)` | For MR `m`, the set of mutant indices it kills (one CSV row in `mutants_killed.csv`). |
| `𝓚(S)` | `⋃_{m∈S} kills(m)` — mutants killed by **any** MR in set `S` (the union, not the sum). |

For 23 subjects pooled:

| Symbol | Meaning |
|---|---|
| `M_total` | `Σ_i M_i` over the 23 subjects. |
| `K_S` | `Σ_i \|𝓚_i(S)\|` — pooled mutant-kill count for set `S`. |

---

## Per-subject metrics

Computed in `scripts/parse_results.py`. Output to
`results/seed11/<subject>/aligned_metrics.json`.

### M1 — Mutation Score (Kill Rate)

**Purpose**: classic mutation-testing effectiveness — what proportion of
injected faults each set detects. Direct counterpart to GenMorph's
upstream MS metric.

**Formula**:

```
M1_N = |𝓚(𝓝)| / M
M1_G = |𝓚(𝓖)| / M
```

**Parameters**:
- numerator is the **union** (a mutant killed by 5 different MRs counts once)
- denominator is total mutants `M` for the subject

**Code**: `parse_results.py:130-131` (`m_metrics()`), helper at `:104-110` (`union_kills`).

---

### M2 — Kills per MR

**Purpose**: set-level density / efficiency. With M1 fixed, lower `|S|`
gives higher M2 → "achieve same coverage with fewer rules". Useful for
arguing **compactness** of Set N versus Set G.

**Formula**:

```
M2_N = |𝓚(𝓝)| / |𝓝|
M2_G = |𝓚(𝓖)| / |𝓖|
```

**Parameters**:
- numerator: union kills (same as M1's numerator)
- denominator: MR count (not mutant count)

**Code**: `parse_results.py:132-133`.

**Note**: M2 is **not** the same as Effective-MR Ratio (see below). M2
divides *mutants killed* by *MRs*; Effective-MR Ratio divides
*MRs that fired* by *MRs available*.

---

### M3 — Differential / Unique Kills

**Purpose**: the headline §6.6 evidence. If `M3_N-only > 0` for many
subjects, Set N catches faults that Set G misses, supporting NOETHER's
claim of complementary coverage.

**Formula**:

```
M3_N-only = |𝓚(𝓝) \ 𝓚(𝓖)|
M3_G-only = |𝓚(𝓖) \ 𝓚(𝓝)|
M3_overlap = |𝓚(𝓝) ∩ 𝓚(𝓖)|
```

The three quantities sum to `|𝓚(𝓝) ∪ 𝓚(𝓖)|`.

**Code**: `parse_results.py:134-136`.

---

### M4 — Jaccard Similarity

**Purpose**: quantify how much the two sets overlap *in their detection
fingerprint*. `M4 ≈ 1` → sets catch the same mutants (one is redundant);
`M4 ≈ 0` → sets are disjoint detectors (strong complementarity).

**Formula**:

```
M4 = |𝓚(𝓝) ∩ 𝓚(𝓖)| / |𝓚(𝓝) ∪ 𝓚(𝓖)|
```

**Parameters**: both numerator and denominator are mutant-level set sizes.
**Not** an MR-level similarity (which would require comparing MR semantics
or kill matrices and is not implemented here).

**Code**: `parse_results.py:137`.

---

### M5 — Complementarity Lift

**Purpose**: "How much extra coverage does combining the two sets give
over using only the better single set?" If `M5 > 0`, deploying both Set N
and Set G together is *strictly* better than picking one — evidence for
practical hybrid use.

**Formula**:

```
M5 = |𝓚(𝓝) ∪ 𝓚(𝓖)| / M  −  max(|𝓚(𝓝)|, |𝓚(𝓖)|) / M
```

**Parameters**:
- first term: union kill rate
- second term: kill rate of whichever set is stronger alone
- `M5 ∈ [0, min(M1_N, M1_G)]` in theory; non-negative because the union
  can never beat itself

**Code**: `parse_results.py:138-139`.

---

### Effective-MR Ratio (ER)

**Purpose**: MR-level *efficiency* — what fraction of the MRs in each set
actually fire on at least one mutant. Set N (algebraic, hand-curated)
should approach 1.0; Set G (GP-evolved, often produces redundant rules)
typically exhibits a tail of zero-kill MRs.

This **complements M2**: two sets can have identical M2 values yet very
different ER values if Set G's union kills come from a small subset of
its MRs while the rest do nothing.

**Formula**:

```
ER_N = |{ m ∈ 𝓝 : kills(m) ≠ ∅ }| / |𝓝|
ER_G = |{ m ∈ 𝓖 : kills(m) ≠ ∅ }| / |𝓖|
```

**Parameters**:
- numerator: count of MRs that kill **at least one** mutant
- denominator: total MRs in the set

**Interpretation**:
- `ER = 1.0` → every MR in the set is contributing
- `ER < 1.0` → the set carries dead weight; `1 − ER` is the prunable fraction
- `ER` and M1 together sketch the Pareto frontier: high M1 / high ER is the design goal

**Code**: `parse_results.py` (`set_n.n_effective_mrs`, `set_n.effective_mr_ratio`, mirror for `set_g`).

---

### Per-MR detail (`per_mr` array)

**Purpose**: enables drill-down — for any mutant, "which MR caught it?";
for any MR, "what did it catch?". Drives heat-maps and per-MR FP/MS
audits in the paper appendix.

**Schema** (each row in the `per_mr` JSON array):

| Field | Meaning |
|---|---|
| `experiment` | EvaluateMRs experiment tag (e.g. `assertions_seed11`) |
| `mr` | MR identifier as it appears in `mutants_killed.csv` |
| `set` | `"N"` or `"G"` |
| `fp` | False-positive rate from `mrs_status.csv` (float in [0, 1] or `null`) |
| `n_killed` | Count of mutants this MR kills |
| `killed_indices` | Sorted list of mutant indices (0-based) it kills |

**Code**: `parse_results.py:155-166`.

---

## Cross-subject metrics

Computed in `scripts/aggregate_metrics.py`. Output to
`results/aligned_summary.json` after Stage 2 finishes.

### Pooled Kill Rate + Wilson 95% CI

**Purpose**: collapse 23 subject-level kill rates into a single
publication-ready number with a defensible uncertainty bracket. Wilson CI
is preferred over the Wald CI because it does not break at extreme
proportions.

**Formula**:

```
p̂_S = K_S / M_total                    (point estimate)

Wilson 95% CI:
  centre = (p̂ + z²/2n) / (1 + z²/n)
  half   = (z · √(p̂(1−p̂)/n + z²/4n²)) / (1 + z²/n)
  CI     = [centre − half, centre + half]

with z = 1.96 (two-sided 95%) and n = M_total.
```

**Parameters**:
- `S ∈ {𝓝, 𝓖}`: which set's rate is being estimated
- `K_S = Σ_i K_{S,i}`: subject-summed kills for set `S`
- `M_total = Σ_i M_i`: subject-summed mutants

**Caveat**: pooling treats every mutant as an independent Bernoulli trial;
this **underestimates variance** because mutants within a subject are not
independent (they share SUT, test inputs, and mutator). The paper should
caveat this; a cluster bootstrap is the principled fix and lives in a
follow-up issue.

**Code**: `aggregate_metrics.py:26-34` (`wilson_ci`), used at `:115, :120`.

---

### McNemar Exact Paired Test

**Purpose**: principled significance test for "Set N vs Set G". Each
mutant is evaluated by both sets, so observations are paired; an exact
McNemar test on the discordant pairs answers whether `P(N kills, G doesn't)`
differs from `P(G kills, N doesn't)`.

**Formula**:

```
For all subjects, all mutants:
  b = #{ mutants : N kills, G doesn't }
  c = #{ mutants : G kills, N doesn't }

H₀: b = c

Two-sided p-value (exact binomial, scipy.stats.binomtest fallback to
manual sum):

  p = 2 · P(X ≤ min(b, c) | X ~ Binomial(b + c, 0.5))
```

**Why exact rather than χ²**: per-subject `M3_N-only` or `M3_G-only` are
often small (<5), and the χ² approximation is unsafe in that regime.

**Interpretation**:
- `b > c` and `p < α` → Set N significantly stronger
- `c > b` and `p < α` → Set G significantly stronger
- otherwise → equivalent at level `α`

**Code**: `aggregate_metrics.py:37-54` (`mcnemar_exact`), used at `:124-126`.

---

### Pooled Effective-MR Ratio

**Purpose**: cross-subject summary of MR utilization (counterpart to the
per-subject Effective-MR Ratio).

**Formula**:

```
ER_pooled_S = (Σ_i n_effective_mrs_{S,i}) / (Σ_i |S_i|)
```

**Parameters**:
- numerator: subject-summed effective-MR counts for set `S`
- denominator: subject-summed total MR counts for set `S`

**Code**: `aggregate_metrics.py` (`set_n.total_mrs`, `set_n.effective_mrs`,
`set_n.effective_mr_ratio`, mirror for `set_g`).

---

### Per-Subject Delta

**Purpose**: forest-plot input — for each of the 23 subjects, how much
better/worse is Set N versus Set G in raw kill rate? Lets the paper show
a sign test or per-subject distribution alongside the pooled estimate.

**Formula**:

```
Δ_i = M1_{N,i} − M1_{G,i}     for i = 1..23
```

**Code**: `aggregate_metrics.py:95-107`.

---

### M1–M5 Cross-Subject Means

**Purpose**: a quick at-a-glance summary of each per-subject metric
averaged across 23 subjects. Reported in tables alongside the pooled
estimates; useful for sanity-checking that no one subject dominates.

**Formula** (for each metric `m`):

```
mean_m = (1/23) · Σ_i m_i
```

Plain arithmetic mean — no weighting by subject mutant count.

**Code**: `aggregate_metrics.py:128-131`.

---

## Metrics not measured here (and why)

### MR-generation cost

Set N is generated deterministically by
`scripts/generate_set_n_mrs.py` in <1 s. Set G's GP runtime is whatever
GenMorph upstream reported (~hours per subject), not re-measured here.

**Why excluded**: the aligned-experiment design (CLAUDE.md §"Project
context") deliberately holds substrate constant and varies only the MR
set. Folding generation cost into the comparison would mix two
incommensurable measurements (one-shot algebraic derivation vs an entire
GP search). If the paper needs a generation-cost statement, it should
appear as an **informational table** citing GenMorph's reported runtime,
not as an experimental measurement.

### Test-execution performance

Stage 2 invokes a single `EvaluateMRs` JVM call per subject that
processes both Set N's and Set G's MRs together (`run_all.sh:172-179`).
The per-MR runtime difference is sub-millisecond and dwarfed by JVM
startup, so the metric is uninformative under the aligned design.

**If needed**: per-subject `EvaluateMRs` wall-clock can be reconstructed
from `results/seed11/_logs/stage2_evaluate_<subject>.log` timestamps to
±1 s precision. Adding explicit timing to `aligned_metrics.json` is a
2-line follow-up that has been deferred until reviewers ask.

---

## Where each metric lives in code

| Metric | Layer | File | Anchor |
|---|---|---|---|
| M1 kill rate | per-subject | `scripts/parse_results.py` | `m_metrics()`, lines 130–131 |
| M2 kills/MR | per-subject | `scripts/parse_results.py` | `m_metrics()`, lines 132–133 |
| M3 unique/overlap | per-subject | `scripts/parse_results.py` | `m_metrics()`, lines 134–136 |
| M4 Jaccard | per-subject | `scripts/parse_results.py` | `m_metrics()`, line 137 |
| M5 complementarity lift | per-subject | `scripts/parse_results.py` | `m_metrics()`, lines 138–139 |
| Effective-MR Ratio | per-subject | `scripts/parse_results.py` | `set_n` / `set_g` blocks in `main()` |
| Per-MR detail | per-subject | `scripts/parse_results.py` | `per_mr` block, lines 155–166 |
| Pooled kill rate + Wilson CI | cross-subject | `scripts/aggregate_metrics.py` | `wilson_ci()` and `summary["set_n"]` block |
| McNemar exact paired p | cross-subject | `scripts/aggregate_metrics.py` | `mcnemar_exact()`, used at `paired_mcnemar` block |
| Pooled Effective-MR Ratio | cross-subject | `scripts/aggregate_metrics.py` | `summary["set_n"]` / `["set_g"]` blocks |
| Per-subject delta | cross-subject | `scripts/aggregate_metrics.py` | `deltas` list, lines 95–107 |
| M1–M5 means | cross-subject | `scripts/aggregate_metrics.py` | `m_metrics_means` block, lines 128–131 |

Line numbers are accurate as of the commit that introduced this file;
search by function name if the file has drifted.
