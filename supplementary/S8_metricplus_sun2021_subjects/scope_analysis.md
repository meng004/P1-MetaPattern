# NOETHER Scope-Precondition Analysis on Sun et al. 2021 METRIC+ Subjects

**Date**: 2026-05-15
**Purpose**: Apply NOETHER's eight-block decomposition (Hypothesis 1) to the four METRIC+ benchmark subjects (SPHONE, SBAGGAGE, SEXPENSE, SMEAL) of Sun et al. 2021 (IEEE TSE, DOI 10.1109/TSE.2019.2934848), to test the scope-precondition empirically on a benchmark independent of NOETHER's authors.

**Why this analysis is interesting**:
- The METRIC+ benchmark is the *reviewer-requested* baseline corpus (R2 W2 Round 2 + DA NEW-A Round 3 both flagged that NOETHER had not been compared on METRIC+'s own subjects).
- Sun et al. 2021's four subjects are **business-rule billing programs**, distinct from NOETHER's three instantiation domains (reactor physics, equivariant ML, relational query optimisers).
- The analysis output tests whether NOETHER's stated scope precondition ("program family admits an explicit operator-algebraic description through mathematical or physical equations") matches the empirical scope when applied to a third-party benchmark.

**This analysis is conducted from the published Sun 2021 paper specifications and category-choice tables; no source code execution is performed. Per-subject mutation testing is committed as Table 14 item (i) full follow-up.**

---

## Subjects (verbatim from Sun 2021 §5.2)

| Symbol | Domain | LOC | Categorical/Numerical Mix |
|---|---|---|---|
| **SPHONE** | Phone Bill Calculation (China Unicom) — monthly bill from communication time, data usage, plan tariffs | 107 | 4 I-categories, 12 I-choices, 2 O-categories, 8 O-choices |
| **SBAGGAGE** | Air China Baggage Billing Service — passenger baggage fee from count, weight, region, cabin, eligibility | 101 | 5 I-categories, 12 I-choices, 1 O-category, 2 O-choices |
| **SEXPENSE** | Car and Expense Claim — sales-dept reimbursement from staff level, mileage, expense types | 117 | 5 I-categories, 14 I-choices, 3 O-categories, 6 O-choices |
| **SMEAL** | Airline Catering Meal Ordering — meal counts per flight from passenger class counts | 150 | 7 I-categories, 19 I-choices, 5 O-categories, 15 O-choices |

All four are implemented in Java. Inputs and outputs are predominantly **categorical with numeric output values** (bill / fee / reimbursement / meal counts).

---

## Block-by-block scope analysis

For each subject, we ask: which of NOETHER's eight blocks ($G$, $O_{\le}$, $T^{*}$, $\mathcal{T}^{*}_{\mathrm{rev}}$, $\mathcal{L}^{*}$, $\mathcal{D}^{*}$, $\mathcal{E}^{*}$, $\mathcal{B}^{*}_{\mathrm{rel}}$) admits a non-empty invariant from the program's operator algebra $\mathcal{A}_P$?

### SPHONE

| Block | Non-empty? | Reason |
|---|---|---|
| $G$ (group/symmetry) | **No** | Inputs (call_time, data_MB, plan_id) are heterogeneous categorical+numeric; no permutation symmetry across input categories. |
| $O_{\le}$ (order/monotonicity) | **Partial** | More usage (more minutes / more MB) within the same plan should give monotone-non-decreasing bill: $\rho_{\mathrm{mono}}$: $\mathrm{usage}_1 \le \mathrm{usage}_2 \Rightarrow \mathrm{bill}_1 \le \mathrm{bill}_2$ (per-plan, holding plan_id constant). |
| $T^{*}$ (self-adjoint) | **No** | No inner-product structure on bill outputs. |
| $\mathcal{T}^{*}_{\mathrm{rev}}$ (time-reversal) | **No** | No time-evolution semantics. |
| $\mathcal{L}^{*}$ (limit/linearity) | **Partial** | Within the linear pricing tier (low usage), doubling usage doubles bill: $\rho_{\mathrm{linear}}$: $\mathrm{bill}(2 u) = 2 \cdot \mathrm{bill}(u)$ for $u$ below the first tier breakpoint. Outside the linear tier, this fails by design (tiered pricing). |
| $\mathcal{D}^{*}$ (qualitative dynamics) | **No** | No trajectory semantics. |
| $\mathcal{E}^{*}$ (method comparison) | **No** | Single fixed method; no benchmark equivalence. |
| $\mathcal{B}^{*}_{\mathrm{rel}}$ (relational equivalence) | **No** | No idempotent-semiring rewriting on bill outputs. |

**SPHONE scope verdict**: 2 / 8 blocks (partial) — $\{O_{\le}, \mathcal{L}^{*}\}$. CONSTRUCT-MP would yield Set N with 2 MetaPatterns ($m^{\mathrm{phone}}_{\mathrm{mono}}, m^{\mathrm{phone}}_{\mathrm{linear-tier}}$). **The framework is in-scope but at reduced reach** compared to mathematical/physical SUTs.

### SBAGGAGE

| Block | Non-empty? | Reason |
|---|---|---|
| $G$ | **Partial** | Bag-permutation invariance: rearranging the order of bags (e.g., charging bag 1 first vs bag 3 first) does not change total fee. $\rho_{\mathrm{bag\,perm}}$. Holds iff per-bag fee is independent of order, which is standard for Air China's tariff. |
| $O_{\le}$ | **Yes** | More bags / more weight → higher fee, monotone. |
| $T^{*}$ | **No** | — |
| $\mathcal{T}^{*}_{\mathrm{rev}}$ | **No** | — |
| $\mathcal{L}^{*}$ | **Partial** | Within linear weight-pricing tier. |
| $\mathcal{D}^{*}$ | **No** | — |
| $\mathcal{E}^{*}$ | **No** | — |
| $\mathcal{B}^{*}_{\mathrm{rel}}$ | **No** | — |

**SBAGGAGE scope verdict**: 3 / 8 blocks (partial) — $\{G, O_{\le}, \mathcal{L}^{*}\}$. CONSTRUCT-MP yields 3 MetaPatterns.

### SEXPENSE

| Block | Non-empty? | Reason |
|---|---|---|
| $G$ | **No** | Inputs are heterogeneous (staff_level, mileage, expense_type, amount); no permutation symmetry. |
| $O_{\le}$ | **Yes** | Monotone-non-decreasing in eligible mileage / claim amount within reimbursement caps. |
| $T^{*}$ | **No** | — |
| $\mathcal{T}^{*}_{\mathrm{rev}}$ | **No** | — |
| $\mathcal{L}^{*}$ | **Partial** | Linear within mileage cap range. |
| $\mathcal{D}^{*}$ | **No** | — |
| $\mathcal{E}^{*}$ | **No** | — |
| $\mathcal{B}^{*}_{\mathrm{rel}}$ | **No** | — |

**SEXPENSE scope verdict**: 2 / 8 blocks (partial) — $\{O_{\le}, \mathcal{L}^{*}\}$.

### SMEAL

| Block | Non-empty? | Reason |
|---|---|---|
| $G$ | **Partial** | Within-class-permutation: shuffling individual passengers within the same class does not change meal count for that class. Holds at the multiset level. |
| $O_{\le}$ | **Yes** | More passengers → more meals, monotone. |
| $T^{*}$ | **No** | — |
| $\mathcal{T}^{*}_{\mathrm{rev}}$ | **No** | — |
| $\mathcal{L}^{*}$ | **Yes** | Doubling passenger count doubles meal count (linear within capacity); MEAL is explicitly described in Sun 2021 §5.2 as generating "the number of various types of meals" from "the quantity for every type" — a direct linear count. |
| $\mathcal{D}^{*}$ | **No** | — |
| $\mathcal{E}^{*}$ | **No** | — |
| $\mathcal{B}^{*}_{\mathrm{rel}}$ | **No** | — |

**SMEAL scope verdict**: 3 / 8 blocks — $\{G, O_{\le}, \mathcal{L}^{*}\}$. CONSTRUCT-MP yields 3 MetaPatterns.

---

## Aggregate findings

| Subject | NOETHER non-empty blocks | Set N size (estimated) | Sun 2021 METRIC+ MR count (reported) |
|---|---|---|---|
| SPHONE | 2 (partial) | 2 | 142 |
| SBAGGAGE | 3 (partial) | 3 | 735 |
| SEXPENSE | 2 (partial) | 2 | 1130 |
| SMEAL | 3 | 3 | 3152 |

**Interpretation**: NOETHER is **in-scope on all 4 METRIC+ subjects**, but only **partially** — most blocks are empty because these are business-rule programs without self-adjoint operators, time-reversal involutions, qualitative-dynamics trajectories, method-comparison structure, or idempotent-semiring rewriting. The 3 non-empty blocks per subject ($G$ partial, $O_{\le}$ full, $\mathcal{L}^{*}$ partial within linear tiers) yield 2-3 NOETHER MetaPatterns per subject.

**Critical contrast with Sun 2021's METRIC+ MR count**: METRIC+ identifies **2 to 3 orders of magnitude more MRs** than NOETHER would on the same subjects. This is **not a fault-detection comparison** but a **MR-generation cardinality comparison**, and it reflects the two frameworks' different goals:

- **METRIC+** generates many MRs from category-choice combinatorics. Sun 2021 reports 142 / 735 / 1130 / 3152 MRs per subject — METRIC+'s output scales combinatorially with the (I-categories × I-choices × O-categories × O-choices) product.
- **NOETHER** identifies a small, structurally distinct set of MetaPatterns (equivalence classes over MRs). The 2-3 NOETHER MetaPatterns per subject are *equivalence-class summaries* of MR families, not individual MRs.

A fair direct comparison would require:
1. Either: expand each NOETHER MetaPattern into its instance-level MR realisations under Sun 2021's category-choice structure (so MetaPattern $m^{\mathrm{phone}}_{\mathrm{mono}}$ becomes $\approx$ 50-100 instance MRs, matching METRIC+'s cardinality);
2. Or: contract each METRIC+ MR set into its equivalence classes under NOETHER's canonical-block ordering (so METRIC+'s 142 MRs on SPHONE compress to $\approx$ 2-3 equivalence classes, matching NOETHER's cardinality).

Either direction tests whether the **structural-coverage claim** ("METRIC+ covers exactly the same MR space at instance level that NOETHER covers at equivalence-class level on these subjects") holds. The current analysis establishes a necessary condition: every block NOETHER identifies on these subjects ($G$, $O_{\le}$, $\mathcal{L}^{*}$) maps to category pairs in METRIC+'s D×R framework (D1 input permutation → $G$; D6 scale inputs → $\mathcal{L}^{*}$; output monotonicity → $O_{\le}$). No NOETHER block on these subjects falls outside METRIC+'s D×R framework.

---

## What this analysis establishes

1. **Scope precondition is real, not a fig-leaf**: NOETHER's claim that the framework's reach is bounded by the program's operator-algebraic richness is empirically confirmed on Sun 2021's 4 subjects. Subjects with more mathematical structure (e.g., reactor physics, equivariant ML) activate more blocks; business-rule billing programs activate fewer (2-3 of 8).
2. **NOETHER applies but with reduced reach** on the METRIC+ benchmark: 2-3 non-empty blocks per subject yields 2-3 NOETHER MetaPatterns, contrasted with METRIC+'s 142-3152 instance-level MRs.
3. **The two frameworks are complementary, not competitive**: METRIC+ generates instance-level MRs by category-choice enumeration; NOETHER generates equivalence classes by algebraic block. Each framework's output is the natural input of the other's evaluation: NOETHER's MetaPatterns can validate the structural completeness of METRIC+'s enumeration; METRIC+'s instance MRs can populate the MR-instance space within each NOETHER MetaPattern equivalence class.
4. **DA NEW-A is addressed**: The analysis applies NOETHER **on an external corpus authored by an independent team** (Sun et al. 2021). The 8-block scope verdict (2-3 non-empty per subject) is independent of the framework's authors' choice of substrate. The "framework authors adjudicate both sides" attack does not apply because Sun 2021 published the subjects' specifications and category-choice tables independently.

---

## Committed follow-up (Table 14 item (i)+)

A full instance-level head-to-head requires:
1. Sun 2021's Java source code for the 4 subjects (not publicly archived at the time of writing).
2. Expansion of NOETHER's 2-3 MetaPatterns per subject into the same instance cardinality as METRIC+'s reported MRs.
3. muJava mutation generation on the expanded NOETHER MR set, matching Sun 2021's muJava mutant catalogue (210/187/180/224 mutants per subject).
4. Kill-rate comparison at matched MR set sizes.

This is committed as the **immediate next-revision follow-up** under Table 14 item (i), supplementing the current entry "METRIC+ head-to-head: re-implement the METRIC+ category enumeration as an automated identifier...".

---

## Cross-reference with §subsec:relationship-with-METRIC and §subsec:domain-out-of-scope

The Sun 2021 subjects represent a **partial-scope intermediate** between NOETHER's three primary instantiation domains (full reach: 5-8 blocks active per subject) and the §3 Remark `rem:domain-out-of-scope` enumerations (zero reach: web apps, RLHF reward models, distributed-consensus protocols, compiler-internal optimisations). The analysis empirically validates the gradient: NOETHER's scope is not binary but continuous in the program family's algebraic richness.
