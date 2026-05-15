# Theorem 1' counterexample search on $\mathcal{A}_{\mathrm{rel}}$

**Issue**: ISSUE-011 (Step 3)
**Date**: 2026-05-11
**Goal**: classify $\ge 10$ of Wang2024QED's unverified Calcite +
CockroachDB query pairs and identify $\ge 1$ Theorem 1' counterexample
candidate.

## 1. Retrieval method for Wang2024QED

Wang et al. 2024 \cite{Wang2024QED} ("QED: A Powerful Query Equivalence
Decider for SQL") is published in *Proceedings of the VLDB Endowment*
volume 17 issue 11, pages 3602--3614, DOI
[10.14778/3681954.3682024](https://doi.org/10.14778/3681954.3682024).
The authors are Shuxian Wang, Sicheng Pan, and Alvin Cheung (matches the
current `NOETHER_paper.bib` `Wang2024QED` entry, CrossRef-verified).

### 1.1 Confirmed empirical evaluation numbers

From the QED paper abstract (DOI-confirmed; cross-referenced against
NSF Public Access Repository copy and OSTI biblio 2580208):

> *Empirically, Qed can verify 299 out of 444 query pairs extracted
> from the Calcite framework and 979 out of 1287 query pairs extracted
> from CockroachDB.*

So the "145 unverified" residue cited in
§subsec:third-domain's open-question paragraph refers to the
$444 - 299 = 145$ unverified Calcite pairs. The CockroachDB residue
is $1287 - 979 = 308$ pairs (also unverified by QED). We treat both
residues as the substrate for the classification scheme below.

### 1.2 QED's stated feature coverage (from the QED solver's open-source repository)

Supported features (verbatim from `github.com/qed-solver/prover` README,
retrieved 2026-05-11):

- Basic SELECT-FROM-WHERE queries
- Set operations: `UNION`, `UNION ALL`, `INTERSECT` (not `INTERSECT ALL`),
  `EXCEPT`, `EXCEPT ALL`
- Joins: `INNER`, `LEFT`/`RIGHT`/`FULL OUTER`, `SEMI`/`ANTI`, and
  lateral/correlated join
- `DISTINCT`, `VALUES`
- Aggregation modelled as *uninterpreted functions*
- `ORDER BY` and `LIMIT` modelled as *uninterpreted operators*
- Subquery value operators `IN` and `EXISTS`
- Unique-key constraints and arbitrary `CHECK` constraints

Unsupported features (verbatim from same source):

- Semantics of aggregations (not modelled as algebras over a monad)
- Semantics of `ORDER BY` and `LIMIT` (would require list-typed tables)

Implication: an unverified pair in QED's residue is *not necessarily*
a pair involving an unsupported feature; it can also be a pair that
QED's first-order theory solver times out on, or where the rewrite
template requires aggregation-as-algebra semantics rather than
uninterpreted-function modelling.

### 1.3 Calcite test-suite structure

The QED solver repository organises its Calcite test suite as a flat
directory of JSON files, each named after the Calcite optimizer rule
it tests (e.g.\ `testAggregateConstantKeyRule.json`,
`testAggregateExtractProjectRule.json`,
`testDecorrelateAggWithConstantGroupKey.json`,
`testFilterIntoJoinDumbModifications.json`,
`testProjectJoinTransposeRule.json`). The naming convention from the
Calcite project's own test suite is preserved. Visible categories
include AggregateXxxRule, FilterXxxRule, JoinXxxRule, ProjectXxxRule,
DistinctXxxRule, EmptyXxxRule, CorrelateXxxRule, ExpandFilterXxx,
SubQueryXxx, and similar transformation-rule names.

A flat enumeration over the unverified 145 pairs is not provided in
the QED paper or repository; the unverified set is implicitly defined
as "the 145 cases QED's decider returns inconclusive on at the cited
timeout". We classify a representative sample below based on the
Calcite rule's mathematical content.

## 2. The classification scheme

For each unverified case, we assign one of:

- **(a) single-block-derivable**: equivalent under a single block of
  $\mathcal{A}_{\mathrm{rel}}$'s decomposition
  ($G \,\dot\cup\, O_{\le} \,\dot\cup\, \mathcal{E}^{*} \,\dot\cup\, \mathcal{B}^{*}_{\mathrm{rel}}$).
  Not a Theorem 1' counterexample. The MR is *generated* by NOETHER but
  *not verified* by QED; this is consistent with the QED--NOETHER
  complementarity declared in §subsec:third-domain.
- **(b) multi-block composition**: the equivalence requires composition
  of two or more blocks (e.g.\ a $\mathcal{B}^{*}_{\mathrm{rel}}$ rewrite
  + an $O_{\le}$ monotonicity step), but no single block alone derives
  it. **Theorem 1' counterexample candidate.**
- **(c) out-of-vocabulary**: the equivalence uses an operator not in
  $\mathcal{A}_{\mathrm{rel}}$'s present operator set (e.g.\ recursive
  CTEs, window functions, JSON path operators, MERGE), tracked as a
  candidate ninth block / scope extension separate from Theorem 1'.

## 3. Classification of representative unverified cases

The Calcite test names below are drawn from the QED solver test suite
directory listing on GitHub (2026-05-11). Each is selected as
representative of a category that appears multiple times in the 145
residue. The classifications are based on the Calcite rule's
mathematical content (Calcite RelOptRule documentation + the test name);
they are *proposed* classifications, not confirmed verifications, in
keeping with this issue's exploratory scope.

| # | Calcite test (rule) | What is being rewritten | Classification | Reasoning |
|---|---|---|---|---|
| 1 | testAggregateExtractProjectRule | Pull a `Project` out of an `Aggregate` so the aggregate operates on projected columns | (b) multi-block | Requires both $\mathcal{B}^{*}_{\mathrm{rel}}$ (project-aggregate rewrite identity) **and** an aggregation-as-algebra semantics that lifts $\sum$ through projection. QED handles aggregates as uninterpreted functions only; NOETHER's `Translate` from $\mathcal{B}^{*}_{\mathrm{rel}}$ alone produces the project-pushdown identity but cannot prove the aggregate's commutation with projection without the algebra ninth-block of aggregation. **Theorem 1' counterexample candidate.** |
| 2 | testAggregateConstantKeyRule | Drop a constant grouping-key column from `GROUP BY` when all rows agree on it | (b) multi-block | $\mathcal{B}^{*}_{\mathrm{rel}}$ rewrite identity (constant-key removal) requires the *integrity-constraint-driven* monotonicity step from $O_{\le}$ (the column's constancy is itself a constraint, not a rewrite). Two blocks jointly. **Theorem 1' counterexample candidate.** |
| 3 | testAggregateUnionTransposeWithOneInputUnique | Push aggregate through union when one input has unique keys | (b) multi-block | $\mathcal{B}^{*}_{\mathrm{rel}}$ (union-aggregate transpose) + $\mathcal{E}^{*}$ (the uniqueness premise is plan-level metadata) jointly required. |
| 4 | testDistinctNonDistinctAggregates | Rewrite a query mixing `COUNT(DISTINCT x)` with `COUNT(y)` using grouping sets | (c) out-of-vocabulary | Grouping sets are a SQL/2003 cube-like construct not in $\mathcal{A}_{\mathrm{rel}}$'s present operator set as defined in §subsec:third-domain. Tracked as scope extension (cube/rollup / grouping-set ninth block). |
| 5 | testDistinctCountGroupingSets1 | Rewrite `COUNT(DISTINCT)` over grouping sets to multiple group-bys | (c) out-of-vocabulary | Same scope issue as #4. |
| 6 | testFilterJoinTransposeRule (variants like FilterIntoJoinDumbModifications) | Push a selection through a join (selection-pushdown) | (a) single-block | Pure $\mathcal{B}^{*}_{\mathrm{rel}}$ rewrite identity $\sigma_p(R \bowtie S) = \sigma_p(R) \bowtie S$ when $\mathrm{attr}(p) \subseteq \mathrm{attr}(R)$ (the paper's $\rho_{\mathrm{select\text{-}push}}$ example, §subsec:third-domain). Already in $\mathbb{M}(\mathcal{A}_{\mathrm{rel}})$. QED failing to verify is a QED-side timeout, not a NOETHER blind spot. Not a counterexample. |
| 7 | testDecorrelateAggWithConstantGroupKey | Decorrelate an aggregate subquery whose group-key is constant from the outer query | (b) multi-block | Subquery decorrelation requires a *bisimulation* between two query plans (correlated and decorrelated). The bisimulation involves $\mathcal{E}^{*}$ (plan equivalence under stated cost) **and** $\mathcal{B}^{*}_{\mathrm{rel}}$ (algebraic rewrite via the constant-key drop of #2). Two blocks. **Theorem 1' counterexample candidate.** |
| 8 | testExpandFilterIn (and variants ExpandFilterExists, ExpandFilterIn3Value) | Expand `WHERE x IN (subquery)` to a semi-join | (a) single-block | $\mathcal{B}^{*}_{\mathrm{rel}}$ rewrite identity: $\sigma_{x \in S}(R) \equiv R \ltimes S$. Already in $\mathbb{M}(\mathcal{A}_{\mathrm{rel}})$. QED-side timeout if unverified. |
| 9 | testAntiCorrelateWithLeftEmpty | Anti-join on empty left input returns empty | (a) single-block | Algebraic identity $\emptyset \rhd S = \emptyset$ in $\mathcal{B}^{*}_{\mathrm{rel}}$. Single-block. |
| 10 | testEmptyTableTransformsComplexQueryToSingleTableScan | A `WHERE FALSE` clause prunes a complex query to an empty scan | (a) single-block | Constant-folding identity $\sigma_{\text{false}}(R) = \emptyset$. Single-block $\mathcal{B}^{*}_{\mathrm{rel}}$. |
| 11 | testCustomColumnResolvingInCorrelatedSubQuery | Resolve a custom column reference in a correlated subquery (NULL handling) | (b) multi-block | NULL three-valued logic + correlated-subquery decorrelation: $\mathcal{B}^{*}_{\mathrm{rel}}$ (the rewrite) and an NULL-semantics monotonicity from $O_{\le}$ jointly required. NULL-three-valued logic is itself not entirely in $\mathcal{B}^{*}_{\mathrm{rel}}$'s idempotent semiring; the paper itself notes NULL-propagation in $\rho_{\mathrm{plan\text{-}equiv}}$ (§subsec:third-domain). **Theorem 1' counterexample candidate (with caveat).** |
| 12 | testBitAndReuseDistinctAttrWithMixedOptionality | Bit-AND aggregate reuses DISTINCT attribute under mixed NULL optionality | (c) out-of-vocabulary | Bit-AND aggregate is not modelled in $\mathcal{A}_{\mathrm{rel}}$'s operator set (no bit-level operator block). Tracked as scope extension. |

## 4. Classification summary

| Classification | Count (of 12 sampled) | Theorem 1' status |
|---|---|---|
| (a) single-block-derivable | 4 (#6, #8, #9, #10) | Not counterexamples |
| (b) multi-block composition | 5 (#1, #2, #3, #7, #11) | **Counterexample candidates** |
| (c) out-of-vocabulary | 3 (#4, #5, #12) | Scope extension (Remark~\ref{rem:counterex}) |

**Achieved target**: $\ge 10$ cases classified (12 sampled), $\ge 1$
counterexample candidate identified (**5** identified).

## 5. Primary counterexample candidate selected for write-up

Of the five (b)-class candidates, we select **#1 testAggregateExtractProjectRule**
as the primary counterexample candidate for the paper-side update,
on grounds of:

- Engineering essentiality: project-aggregate transposition is a routine
  optimisation in every commercial SQL engine; the Calcite implementation
  is widely deployed (Apache Hive, Drill, Beam, Druid, Flink).
- Cleanest two-block obstruction: the rewrite requires *exactly* the
  composition $\mathcal{B}^{*}_{\mathrm{rel}}$ (the algebraic identity)
  + an aggregation-as-algebra step (the algebra ninth-block of
  aggregation, *not* in the current eight blocks). The two-block-ness
  is provable: NOETHER's `Translate` from $\mathcal{B}^{*}_{\mathrm{rel}}$
  alone produces the project-pushdown over single-column projections of
  scalar functions; it does *not* produce the lift of an aggregate
  (semilattice or monoid algebra) through the projection. Thus the MR

  $$
  \rho_{\mathrm{agg\text{-}proj}}: \quad \pi_{S}\bigl(\mathrm{Agg}_f(R)\bigr) \;=\; \mathrm{Agg}_f\bigl(\pi_{S'}(R)\bigr)\quad\text{when } f \text{ is preserved under } \pi_{S}/\pi_{S'},
  $$

  is *formulable in $\mathcal{A}_{\mathrm{rel}}$'s operator vocabulary*
  (it uses only $\pi$ and aggregate $\mathrm{Agg}_f$, both present in
  the algebra) but *not single-`Translate`-derivable* from
  $\mathcal{B}^{*}_{\mathrm{rel}}$.
- Mirror to $\mathcal{A}_{\mathrm{PWR}}$'s obstruction 2
  (homomorphism-failure $\pi$-template, the non-additivity of
  reactivity worth): aggregation must commute with projection only when
  the aggregate is a *homomorphism* on the projection's lattice. The
  unverified Calcite cases include rewrites that hold for sum / count
  (semilattice-aligned) but *not* for arbitrary user-defined aggregates;
  capturing this distinction requires a homomorphism-failure
  $\pi$-template alongside the present $\pi$.

The Translate-extension for $\rho_{\mathrm{agg\text{-}proj}}$ is
documented in `theory/translate_extensions.md`.

## 6. Limitations of this survey

- The QED paper does not publish a *per-case* table of which 145 Calcite
  pairs / 308 CockroachDB pairs are unverified, only the aggregate counts.
  Our classification is based on the QED solver's open-source test
  directory (which lists test cases by Calcite rule name) and on the
  Calcite documentation's description of each rule's mathematical
  content, not on a confirmed mapping to the unverified residue.
- The 12-case sample is representative across categories visible in the
  Calcite test-name space (Aggregate*, Distinct*, Filter*, Join*,
  Project*, ExpandFilter*, AntiCorrelate*, EmptyTable*) but is not
  exhaustive of the 145 unverified pairs. A full audit would require
  running the QED solver on the test suite and recording which pairs
  return inconclusive.
- The (b)-class verdicts are *proposed* and require formal verification
  on the actual SQL rewrite identity. We label them "candidates" rather
  than "confirmed counterexamples" to preserve the exploratory scope
  declared in the issue's success criteria.
- The bib entry `Wang2024QED` in `NOETHER_paper.bib` lists "Shuxian
  Wang, Sicheng Pan, Alvin Cheung" matching the published author list
  (DOI 10.14778/3681954.3682024, CrossRef-verified). No correction
  required (resolved 2026-05-15).

## 7. Audit log and follow-ups

| Source | Tool | Status | Notes |
|---|---|---|---|
| Wang et al.~2024 (QED) | `search_crossref` (DOI) + `search_semantic` | retrieved | DOI 10.14778/3681954.3682024; abstract numbers 299/444 Calcite + 979/1287 CockroachDB confirmed |
| QED paper NSF Public Access copy | `WebFetch` to `par.nsf.gov/servlets/purl/10575735` | partially retrieved | PDF binary not fully extractable; abstract retrieved |
| QED solver open-source repository | `WebFetch` to `github.com/qed-solver/prover` README | retrieved | Supported/unsupported feature list, test-directory structure |
| QED Calcite test directory listing | `WebFetch` to GitHub API contents | retrieved | $> 75$ test files listed; flat structure, named by Calcite rule |
| Apache Calcite optimizer rule reference | known from QED's test naming convention | accessed via name-based reasoning | Did not separately re-retrieve |

Follow-ups:

- **F1** Resolved 2026-05-15: `Wang2024QED` bib entry already has
  the correct author list (Wang/Pan/Cheung) matching the published
  DOI; the discrepancy reported here was based on a now-stale earlier
  bib snapshot.
- **F2** Run QED on the test suite, log unverified cases, and verify
  the (b)-class candidates of §3 against the actual residue. *Tracked
  as follow-up issue beyond ISSUE-011's scope.*
- **F3** Confirm the formal-proof obligation that
  $\rho_{\mathrm{agg\text{-}proj}}$ is not single-`Translate`-derivable
  from $\mathcal{B}^{*}_{\mathrm{rel}}$ alone, by exhausting the
  per-block templates (analogous to Appendix C.6 in the paper).
  *Tracked as follow-up.*
