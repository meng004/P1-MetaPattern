# Pre-Registered Protocol — METRIC$+$ vs NOETHER Instance-Level Head-to-Head on Sun et al. 2021 Subjects (Path A)

**Status**: Pre-registered protocol (Path A response to Round 3 reviewer question Q2)
**Date registered**: 2026-05-16
**Pre-registration commit**: this file's first git commit; do not modify after data collection begins.
**Linked future-work item**: Table `tab:future-work` item (i) in `NOETHER_paper.tex`.
**Linked scope analysis**: `scope_analysis.md` in this same directory (Sun 2021 4 subjects scoped under NOETHER's 8 blocks).

---

## 1. Motivation

The body paper (`NOETHER_paper.tex` §subsec:relationship-with-METRIC) contains two METRIC$+$ comparisons:

1. **`tab:metricplus-headtohead-small`** — a manual analysis on 3 SUTs from the paper's own algebra-rich substrate (`midpoint`, `hypotSig`, `powerSig`). This is methodologically light: the framework's authors hand-classify which METRIC$+$ category pairs are vacuous, on substrate the framework's authors curated.

2. **`tab:metricplus-sun2021-scope`** (the Path B scope analysis) — NOETHER's 8-block decomposition applied to Sun et al.'s published 4 subjects (SPHONE, SBAGGAGE, SEXPENSE, SMEAL). Finds NOETHER in-scope on all 4 subjects but at narrower reach (2--3 of 8 blocks). Cardinality contrast: NOETHER 2--3 MetaPatterns vs METRIC$+$ 142--3152 instance MRs.

What remains as committed follow-up (per `tab:future-work` item (i)) is the **fair instance-level head-to-head**:

- METRIC$+$ side: re-implement Sun 2021's 11-pair input--output category enumeration as an automated identifier.
- NOETHER side: expand $\mathbb{M}(\mathcal{A}_P)$ to instance MRs at matched cardinality (via the category-choice enumeration).
- Mutation substrate: shared across both sets.
- Goal: convert the qualitative coverage contrast into a measured kill-rate difference, on Sun 2021's published subjects, with both methods exercised at instance-MR granularity.

This protocol pre-registers that experiment. Pre-registration discipline: the hypotheses, metrics, statistical analysis plan, mutation operators, and translation procedure below are all committed before data collection begins; deviations from this protocol during execution must be recorded as protocol deviations in the post-experiment write-up.

---

## 2. Subjects (Sun 2021's published corpus)

All four subjects from Sun, Fu, Poon, Xie, Liu, Chen (2021), "METRIC$+$: A Metamorphic Relation Identification Technique Based on Input Plus Output Domains" (IEEE TSE, DOI 10.1109/TSE.2019.2934848):

| Subject | Domain | LOC | I-cats / I-choices | O-cats / O-choices |
|---|---|---|---|---|
| `SPHONE`    | China Unicom phone-bill calculator                        | 107 | 4 / 12 | 2 / 8 |
| `SBAGGAGE`  | Air China baggage-billing service                         | 101 | 5 / 12 | 1 / 2 |
| `SEXPENSE`  | Sales-department expense reimbursement                    | 117 | 5 / 14 | 3 / 6 |
| `SMEAL`     | Airline catering meal-ordering service                    | 150 | 7 / 19 | 5 / 15 |

Numbers from Sun 2021 Table 17. Subjects are business-rule billing programs whose semantics are categorical+numeric rather than mathematical/physical; this is exactly the substrate the present paper's `§subsec:relationship-with-METRIC` scope analysis classified as "in-scope but narrower reach".

**Acquisition path**: contact Sun et al. for the original Java implementations; if no response within 30 days, re-implement from Sun 2021's prose specification (Tables 7, 9, 11, 13, 15 contain the per-subject behaviour rules sufficient for re-implementation).

---

## 3. Pre-registered hypotheses

The following three hypotheses are pre-registered before data collection. The numbering is fixed; deviations or revisions to hypothesis text after pre-registration must be flagged explicitly and reported alongside the original.

### H$_{\mathrm{MP1}}$ — Coverage subsumption at matched cardinality

**Statement**. When NOETHER's MetaPattern set $\mathbb{M}(\mathcal{A}_P)$ on each Sun 2021 subject is expanded to instance MRs via the category-choice enumeration, and METRIC$+$'s 11-pair D$\times$R catalogue is enumerated to instance MRs by the same procedure, the NOETHER-induced MR set on each subject is a structural superset of the METRIC$+$-induced MR set at the per-D$\times$R-pair granularity. Equivalently: every non-vacuous METRIC$+$ category pair on each subject maps to a non-empty NOETHER block, and there exist NOETHER blocks not exercised by any METRIC$+$ category pair on the same subject.

**Falsification criterion**. H$_{\mathrm{MP1}}$ is falsified if there exists a Sun 2021 subject and a non-vacuous METRIC$+$ category pair on that subject whose MR template does not map to any NOETHER block under the framework's 8-block decomposition.

### H$_{\mathrm{MP2}}$ — Kill-rate parity within scope

**Statement**. On a shared PIT-1.7.4 mutation substrate over Sun 2021's 4 subjects, instance-level Set N (NOETHER-expanded) and Set MP (METRIC$+$-enumerated) achieve statistically indistinguishable pooled kill rates at $\alpha = 0.05$, with overlapping Wilson 95\% CIs.

**Falsification criterion**. H$_{\mathrm{MP2}}$ is falsified if pooled-kill-rate McNemar exact two-sided $p < 0.05$ in either direction (either set dominates the other) with non-overlapping Wilson 95\% CIs.

**Sample-size note**. Sun 2021 reports 4 subjects with category-enumeration cardinalities $\{142, 735, 1130, 3152\}$ instance MRs (total $\approx 5159$). After Sun 2021's vacuous-pair filter (typically 60--80\% reduction), the executable instance-MR substrate is expected at $\approx 1000$--$2000$ per subject, sufficient for $\alpha = 0.05$ inferential testing.

### H$_{\mathrm{MP3}}$ — Cost-axis asymmetry

**Statement**. NOETHER's MR-generation cost on each Sun 2021 subject is asymptotically lower than METRIC$+$'s on the same subject. Specifically: NOETHER's per-subject derivation cost is polynomial in the algebra's generating-set size (Theorem 2, $\approx$ minutes wall-time after $\mathcal{A}_P$ distillation); METRIC$+$'s per-subject cost is at least $|D| \times |R| \times \prod_i |c_i|$ where $c_i$ ranges over the category-choice product (the 142--3152 instance MR counts are the empirical witness of this combinatorial blow-up).

**Falsification criterion**. H$_{\mathrm{MP3}}$ is falsified if on any Sun 2021 subject NOETHER's measured wall-time + human-effort cost exceeds METRIC$+$'s on the same subject.

---

## 4. Methods

### 4.1 NOETHER side (Set N expansion)

For each Sun 2021 subject $S$:

1. **Algebra distillation** (one-time per subject; uses CONSTRUCT-MP Step 1). Identify the program-induced operator algebra $\mathcal{A}_S$. The `scope_analysis.md` in this directory already records the 8-block scope verdict (which blocks are non-empty on each subject).
2. **MetaPattern derivation** (CONSTRUCT-MP Steps 2--4). Run CONSTRUCT-MP on the non-empty blocks of $\mathcal{A}_S$. Yields 2--3 MetaPatterns per subject (matching the cardinalities in `tab:metricplus-sun2021-scope`).
3. **Instance MR expansion**. For each MetaPattern $m$, enumerate concrete MR instances by binding $m$'s parameter slots to the subject's input domain values. Translate's parameter-slot enumeration is documented in §subsec:translate-templates.
4. **Pre-execution filter**. Discard any instance whose `jor` predicate is out-of-domain on the subject (e.g.~negative weight when the subject's input domain excludes negatives). This is the same filter applied to the existing `§subsec:test-design` substrate.
5. **Output**: Set N for subject $S$ as a flat list of executable instance MRs with one MetaPattern parent each.

### 4.2 METRIC$+$ side (Set MP automated identifier)

For each Sun 2021 subject $S$:

1. **Input-domain category extraction**. Re-implement Sun 2021's "input domain partitioning by category-choice" step as an automated identifier reading the subject's input-domain specification (Sun 2021 Tables 7, 9, 11, 13 give the spec for SPHONE, SBAGGAGE, SEXPENSE, SMEAL respectively).
2. **Output-domain category extraction**. Same for output domain (Sun 2021 Tables 8, 10, 12, 14).
3. **D$\times$R category-pair enumeration**. Enumerate all 11 input-domain $\times$ output-domain category pairs $(d_i, r_j)$. The 11 pairs are Sun 2021's R1--R5 output relations $\times$ a partition of input-domain pair types.
4. **Per-pair MR-template synthesis**. For each non-vacuous pair, instantiate the MR template by binding category choices. Sun 2021's prose specification §IV gives the algorithm.
5. **Pre-execution filter** (same as 4.1.4).
6. **Output**: Set MP for subject $S$ as a flat list of executable instance MRs.

### 4.3 Mutation substrate

PIT 1.7.4 with the stock mutator catalogue, applied to each Sun 2021 subject's Java source. Mutator overrides for business-rule subjects (no `MATH` or `RETURN_VALS` overrides needed; subjects do not contain operator-algebra-rich code) follow PIT defaults.

### 4.4 Translation step (matched cardinality)

Two parallel readings are reported:

**Reading A** — NOETHER expanded to instance granularity, METRIC$+$ at its native granularity.
- Direct head-to-head at the per-(SUT, mutator) cell.

**Reading B** — METRIC$+$ contracted to equivalence classes at the algebra-block level, NOETHER at its native MetaPattern granularity.
- For each METRIC$+$ category pair $(d_i, r_j)$, identify the NOETHER block that subsumes it (per the `scope_analysis.md` mapping table).
- Aggregate METRIC$+$ kills by NOETHER block.
- Compare block-level kill rates.

Both readings are pre-registered; both are reported in the result table.

### 4.5 Equivalent-mutant exclusion

Same two-stage filter as §subsec:pooled-headtohead (the existing equivalent-mutant protocol). Stage 1: kill-vector auto-classify the $|\text{Set N} \cap \text{Set MP killed}|$ mutants as non-equivalent. Stage 2: progressive multi-LLM vote (DeepSeek + ChatGPT + Anthropic tiebreaker) on the both-miss mutants.

---

## 5. Metrics (pre-registered)

| # | Metric | Formula |
|---|---|---|
| M1 | Per-subject Set N kill rate | $\frac{\text{Set N kills}}{n_{\text{mutants}}}$, Wilson 95\% CI |
| M2 | Per-subject Set MP kill rate | $\frac{\text{Set MP kills}}{n_{\text{mutants}}}$, Wilson 95\% CI |
| M3 | Pooled cross-subject kill rate (each set) | $\frac{\sum \text{Set X kills}}{\sum n_{\text{mutants}}}$, Wilson 95\% CI |
| M4 | Paired McNemar exact $p$ (Set N vs Set MP) | discordant cells $(b, c)$; binomial exact two-sided |
| M5 | Per-NOETHER-block kill rate, both sets | partition kills into 8 blocks (5 vacuous on Sun corpus) |
| M6 | Per-METRIC$+$-pair kill rate, both sets | partition kills into 11 D$\times$R pairs |
| M7 | Complementarity 4-tuple per subject | (both / N-only / MP-only / neither) |
| M8 | Generation-time wall-clock per subject (NOETHER side) | CONSTRUCT-MP + Translate + instance enumeration |
| M9 | Generation-time wall-clock per subject (METRIC$+$ side) | category extraction + D$\times$R enumeration + MR synthesis |
| M10 | Human-effort estimate per subject (both sides) | based on operator-algebra distillation vs category-spec authoring |

---

## 6. Statistical analysis plan (pre-registered)

1. **Primary test for H$_{\mathrm{MP2}}$**: pooled McNemar exact two-sided $p$ across all 4 subjects. Reject H$_{\mathrm{MP2}}$ at $\alpha = 0.05$.
2. **Per-subject secondary tests**: McNemar exact per subject. Bonferroni correction at $\alpha_{\mathrm{Bonf}} = 0.05/4 = 0.0125$.
3. **Effect-size reporting**: odds ratio (OR) and risk difference (RD) on the $(b, c)$ discordant cells, with bootstrap 95\% CIs.
4. **Wilson 95\% CIs**: reported alongside every kill-rate point estimate.
5. **Multiple-comparison guard**: the 8 NOETHER-block per-block rates and the 11 METRIC$+$-pair per-pair rates are descriptive secondary readings; per-block / per-pair $p$-values are not reported as inferential.
6. **Negative direction**: if Set MP dominates Set N at McNemar $p < 0.05$, this is reported as a substantive finding (the framework's coverage advantage is not converting to kill-rate advantage at instance granularity), not as a null result.

---

## 7. Risks and protocol deviations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Sun 2021 source unavailable | Medium | Re-implement from Tables 7--14 of Sun 2021 |
| METRIC$+$ category-extraction automation hits ambiguous-spec cases | Medium--High | Document each ambiguous case + adjudicate against Sun 2021's published Table 17 totals; flag deviations |
| Mutation-substrate is too small ($n < 300$) for $\alpha = 0.05$ inference | Low (Sun's $\approx 1000-2000$ executable instances per subject) | Pre-register subject pooling as the primary test if any single subject falls below $n = 100$ |
| Equivalent-mutant exclusion changes the 2x2 cells substantially | Medium | Report both pre- and post-exclusion numbers; the post-exclusion is the inferential basis |
| Wilson CI overlap interpretation conflated with non-inferiority | Low | The protocol's H$_{\mathrm{MP2}}$ is two-sided; non-inferiority would require a separate pre-registered margin |

Any deviation from this protocol during execution must be:
1. Time-stamped in `protocol_path_a_deviations.md` (to be created in this directory at first deviation).
2. Reported alongside the original protocol text in the post-experiment write-up.
3. Flagged as either "data-blind" (decided before any data was seen) or "data-informed" (decided after partial data); the latter inflates Type I error and must be reported.

---

## 8. Timeline and resources

| Step | Estimated effort |
|---|---|
| Sun 2021 source acquisition | 1 week (correspondence + license) |
| METRIC$+$ automated identifier implementation | 1 week (4 subjects $\times$ category-extraction + D$\times$R enumeration + MR synthesis) |
| NOETHER side: CONSTRUCT-MP + instance enumeration on 4 subjects | 3 days (per-subject CONSTRUCT-MP is $\le 1$\,h after $\mathcal{A}_S$ distilled; enumeration is automated) |
| PIT 1.7.4 mutation runs (4 subjects) | 4 hours wall, parallel-4 |
| Equivalent-mutant exclusion (multi-LLM vote) | 2 days |
| Statistical analysis + write-up | 3 days |
| **Total** | **$\approx 2$ weeks engineering + $\approx 30$ min compute**, matching `tab:future-work` item (i)'s estimate |

---

## 9. Pre-registration artifacts

| Artifact | Path | Purpose |
|---|---|---|
| This protocol | `supplementary/S8_metricplus_sun2021_subjects/protocol_path_a_headtohead.md` | Pre-registered hypotheses, metrics, plan |
| Scope analysis | `supplementary/S8_metricplus_sun2021_subjects/scope_analysis.md` | NOETHER 8-block verdict on each Sun 2021 subject (Path B; complementary to this Path A protocol) |
| Deviation log | `supplementary/S8_metricplus_sun2021_subjects/protocol_path_a_deviations.md` | To be created at first protocol deviation |
| Post-experiment write-up | `supplementary/S8_metricplus_sun2021_subjects/results_path_a.md` | Created after data collection completes |

Pre-registration timestamp: this file's first git commit. Any modification to §§2--6 after that commit must be flagged as a protocol deviation.

---

## 10. Relationship to the body paper

This protocol is the **engineering plan** for `tab:future-work` item (i) ("METRIC$+$ head-to-head: re-implement category enumeration as automated identifier"). When the experiment completes, the body paper's METRIC$+$ comparison subsection (`§subsec:relationship-with-METRIC`) will be revised post-acceptance to add a third METRIC$+$ table reporting the instance-level head-to-head results on Sun 2021's corpus, alongside the existing `tab:metricplus-headtohead-small` (3 hand-picked SUTs from the present paper's substrate) and `tab:metricplus-sun2021-scope` (NOETHER block coverage on Sun 2021's 4 subjects).

The three METRIC$+$ tables will then provide a complete coverage of the Round 3 reviewer-requested comparison:

1. **Small-scale manual** (`tab:metricplus-headtohead-small`): the framework's authors hand-classify 3 SUTs from their own substrate (currently in body; methodologically lightest but most accessible).
2. **Scope verdict on independent corpus** (`tab:metricplus-sun2021-scope`): the framework's authors apply NOETHER's 8-block test to Sun 2021's 4 published subjects (currently in body; addresses the "framework authors adjudicate both sides" concern at the block-coverage layer).
3. **Instance-level head-to-head on independent corpus** (this protocol's output; deferred to post-acceptance): the framework's authors run both methods on Sun 2021's published subjects with shared mutation substrate and pre-registered hypotheses (the gold-standard fair comparison).

The three tables stack from cheapest-but-weakest to most-expensive-but-strongest. The body paper currently reports tables 1 and 2; this protocol is the registered design for table 3.
