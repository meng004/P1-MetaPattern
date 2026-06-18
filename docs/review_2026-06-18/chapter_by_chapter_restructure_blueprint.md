# NOETHER Chapter-by-Chapter Restructuring Blueprint

**Date:** 2026-06-18

**Source plan:** `docs/review_2026-06-18/research_question_and_restructure_plan.md`

**Purpose:** Provide a chapter-level restructuring blueprint for the NOETHER manuscript. Each chapter is assigned a goal, a reader-facing purpose, acceptance criteria, and planned figures/tables. The blueprint keeps the manuscript centered on MR identification, operator-block coverage, algebraic origin, and applicability boundary.

---

## 0. North Star and Reader Contract

### Final Research Question

**RQ:** How can an operator-algebraic, structured MR-identification method derive a broader and more explainable MR class / MetaPattern design space than expert-experience-based MR sets and search-based MR generation methods, by making the algebraic origin and applicability boundary of MRs explicit from the governing equations of a program family?

### Reader Contract

The paper asks the reader to judge NOETHER as an **MR identification framework**, not as an MR effectiveness benchmark. The manuscript must therefore make three claims auditable:

1. **Origin:** each claimed MR class has a governing-equation/operator source.
2. **Boundary:** each MR class has explicit assumptions and interface requirements.
3. **Coverage:** NOETHER covers operator blocks that expert sets and search-based methods do not make explicit in the same way.

### Evidence Axes

The paper should organize all evidence along three axes:

1. **Against expert MR sets:** binary operator-block coverage.
2. **Against search-based MR generation:** origin, boundary, redundancy, readability, and maintainability.
3. **Across domains:** same operator block explains MR classes in different program families or solvers.

---

## 1. Target Manuscript Structure

The current manuscript should be reorganized into the following main sections:

1. Introduction
2. Background and Positioning
3. Problem Model and Scope
4. The NOETHER Framework
5. Evidence Design and Coverage Protocol
6. Expert MR Sets vs. NOETHER: Operator-Block Coverage
7. NOETHER and Search-Based MR Generation: Complementarity
8. Cross-Domain Derivations and Boundary Cases
9. Practical Implications for Program-Family Testability
10. Threats to Validity and Limitations
11. Artefact and Supplementary Material
12. Conclusion

Appendices should hold proofs, detailed derivations, long MR catalogues, secondary mutation/effectiveness results, and extended tables that are too large for the main text.

Reason:

This structure separates theory, evidence design, expert comparison, search-method comparison, and cross-domain explanation. It prevents the current `Empirical evaluation` section from controlling the paper's perceived contribution.

---

## 2. Chapter-Level Blueprint

### Section 1. Introduction

**Goal:** Establish MR identification as the oracle-side problem and state the final RQ.

**Purpose for readers:** By the end of the introduction, readers should know that the paper is not claiming better average fault detection; it is offering a structured way to derive and classify MR classes from governing equations.

**Core messages:**

1. Metamorphic testing depends on MRs, but MR identification remains difficult.
2. Expert MR sets are useful but often encode implicit intuition, especially parameter-sensitivity intuition.
3. Search-based MR generation can produce candidates, but candidate generation alone does not explain algebraic origin or boundary.
4. Equation-governed program families provide a source of structural invariants.
5. NOETHER derives MR classes / MetaPatterns from operator-algebraic properties.
6. The paper compares design-space coverage, not fault-revealing effectiveness.

**Acceptance criteria:**

1. The RQ appears explicitly in the introduction.
2. Contributions are written as identification, origin, boundary, and coverage claims.
3. The introduction contains a scope firewall: the paper does not evaluate MR effectiveness as its central claim.
4. GenMorph is described as complementary search-based generation, not as the main opponent.
5. No sentence implies that NOETHER eliminates human expertise.

**Planned figures/tables:**

**Fig. 1 — RQ and Evidence Map**

- Type: conceptual flow diagram.
- Suggested tool: Mermaid or draw.io.
- Position: near the end of the introduction.
- Content: MR identification problem -> NOETHER operator-algebraic derivation -> three evidence axes: expert coverage, search complementarity, cross-domain derivation.
- Use: orient reviewers before technical detail.

**Table 1 — Contribution-to-Evidence Map**

- Type: compact traceability table.
- Position: after contributions.
- Columns: contribution claim, evidence section, evidence type, what is not claimed.
- Use: prevent misreading of mutation or GenMorph material as the central contribution.

---

### Section 2. Background and Positioning

**Goal:** Reframe related work around the paper's comparison targets.

**Purpose for readers:** Readers should see why expert MR identification and search-based generation are both relevant but incomplete for explaining MR origin and boundary.

**Core messages:**

1. MT and MR identification define the problem.
2. Expert MR identification supplies practical MRs but may leave structural source implicit.
3. METRIC/METRIC+ organize input/output relations but do not derive MR classes from governing-equation operators.
4. Search-based and generated oracle/test methods can produce candidates but raise known issues of readability, redundancy, human screening, and maintenance.
5. NOETHER occupies a theoretical-methodological position: it models the algebraic source of MR classes.

**Acceptance criteria:**

1. Related work is organized by comparison role, not by chronology.
2. Claims about generated tests/oracles are supported by real citations.
3. Search-based methods are not dismissed; they are positioned as complementary.
4. The section distinguishes `generated candidate relation` from `explained MR class`.
5. The reader can predict why the paper later uses Table 2.

**Planned figures/tables:**

**Table 2 — Positioning Matrix of MR Identification Approaches**

- Type: comparison matrix.
- Position: end of related work.
- Columns: approach family, output, required human knowledge, origin explanation, boundary explanation, maintainability concern, role in this paper.
- Use: prepare the search-vs-NOETHER comparison without turning it into a performance contest.

**No figure required unless the section becomes conceptually dense.**

Reason:

A table is better than a figure here because the comparison is categorical and citation-driven.

---

### Section 3. Problem Model and Scope

**Goal:** Define the objects the rest of the paper uses: program family, governing equation, operator block, MR class, executable MR instance, expert coverage, and NOETHER coverage.

**Purpose for readers:** Readers should know exactly what counts as coverage and why an identified MR class may be non-executable on a particular interface.

**Core messages:**

1. A program family is constrained by a governing equation/operator system.
2. Operator blocks are independent algebraic or order-theoretic origins of MR classes.
3. MR class / MetaPattern is the primary output of NOETHER.
4. Executable MR instance is a downstream realization that depends on program interface affordances.
5. Binary coverage is defined at the operator-block level.
6. Equation structure alone is not coverage unless an MR class is explicitly derived.

**Acceptance criteria:**

1. The two-level model is formalized.
2. Expert coverage and NOETHER coverage use binary definitions.
3. Identified-but-not-executable MR classes are explicitly defined.
4. The section contains no mutation-score or effectiveness criterion.
5. All later tables can cite these definitions.

**Planned figures/tables:**

**Fig. 2 — Two-Level MR Model**

- Type: conceptual pipeline diagram.
- Suggested tool: Mermaid.
- Position: after definitions.
- Content: governing equation/operator algebra -> operator block -> identified MR class -> interface gate -> executable MR instance.
- Use: visually separate theoretical identification from executable test construction.

**Table 3 — Core Definitions and Counting Rules**

- Type: terminology and rule table.
- Position: after Fig. 2.
- Columns: construct, definition, counted as coverage?, evidence required, common misreading.
- Use: gives reviewers a single source for binary coverage interpretation.

---

### Section 4. The NOETHER Framework

**Goal:** Present the method: how NOETHER derives MR classes from operator-algebraic structure.

**Purpose for readers:** Readers should understand the derivation procedure and why the framework has an upstream empirical layer and a downstream mechanical layer.

**Core messages:**

1. The upstream layer curates the operator algebra and block decomposition.
2. The downstream layer derives MR classes / MetaPatterns from the curated block structure.
3. The eight blocks are a scoped, empirically curated decomposition, not a universal axiom.
4. Each block has a derivation template and boundary assumptions.
5. The closure theorem supports the downstream derivation, but does not prove absolute completeness.

**Acceptance criteria:**

1. Upstream curation and downstream derivation are separated.
2. Each operator block is introduced with its mathematical source, derived MR class type, and boundary.
3. The method is described as reproducible enough for another researcher to audit.
4. The framework explicitly states what is out of scope.
5. Theorems are connected to MR identification, not to fault-detection claims.

**Planned figures/tables:**

**Fig. 3 — NOETHER Derivation Pipeline**

- Type: method flowchart.
- Suggested tool: Mermaid.
- Position: early in the framework section.
- Content: distil program-family operator algebra -> decompose into blocks -> extract invariants -> translate into MR classes -> check interface executability.
- Use: make the method procedural.

**Table 4 — Operator Blocks and Derivation Templates**

- Type: taxonomy table.
- Position: after block definitions.
- Columns: block, operator source, derived MR class form, assumptions, boundary, example program family.
- Use: central taxonomy for the rest of the paper.

**Table 5 — Per-Block Derivation Cost**

- Type: revised version of the existing per-generator cost table.
- Position: later in the framework section or appendix.
- Use: keep algorithmic detail available without making cost the main claim.

---

### Section 5. Evidence Design and Coverage Protocol

**Goal:** Define how the paper evaluates the research question before presenting results.

**Purpose for readers:** Readers should understand that the evidence protocol measures MR design-space coverage and explanation, not observed fault-revealing effectiveness.

**Core messages:**

1. Expert comparison uses binary operator-block coverage.
2. Search comparison uses origin/boundary/readability/maintenance criteria.
3. Cross-domain evidence uses derivation traces across program families.
4. Evidence must be traceable to textual, mathematical, comparative, literature, or boundary evidence.
5. Mutation/effectiveness material is secondary and does not decide the RQ.

**Acceptance criteria:**

1. The three evidence axes are explicitly mapped to RQ subquestions.
2. The coverage counting rule is stated before any result table.
3. The paper explains why counts of individual MRs are not the main metric.
4. The protocol states how identified-but-not-executable classes are reported.
5. The section contains an evidence-to-claim traceability table.

**Planned figures/tables:**

**Table 6 — Evidence-to-RQ Traceability Matrix**

- Type: claim-evidence map.
- Position: end of evidence design.
- Columns: RQ subquestion, evidence axis, main table, required evidence, exclusion rule.
- Use: makes the evaluation auditable.

**Fig. 4 — Evidence Architecture**

- Type: three-lane diagram.
- Suggested tool: Mermaid.
- Position: optional; include if Section 5 feels abstract.
- Content: expert sets lane, search methods lane, cross-domain derivation lane, all feeding the same RQ.
- Use: help readers see why the later sections are complementary rather than redundant.

---

### Section 6. Expert MR Sets vs. NOETHER: Operator-Block Coverage

**Goal:** Show that NOETHER covers a broader operator-block design space than expert MR sets under the binary coverage definition.

**Purpose for readers:** Readers should see that expert sets often emphasize certain intuitive relation types, while NOETHER makes additional operator-block origins explicit.

**Core messages:**

1. Expert coverage is yes/no per operator block.
2. NOETHER coverage is yes/no per explicitly derived MR class.
3. SACOS/SPARK/LOCUST are central evidence for expert-set comparison.
4. PWR and other existing corpora can provide additional corroboration if their expert-source status is clear.
5. Interface limitations are recorded rather than hidden.

**Acceptance criteria:**

1. The main table uses binary coverage only.
2. Every expert yes-cell cites a concrete expert MR.
3. Every NOETHER yes-cell cites a derived MR class and source equation/operator.
4. Equation structure without derived MR class is not counted.
5. The text does not claim higher fault detection from this table.

**Planned figures/tables:**

**Table 7 — Expert vs. NOETHER Operator-Block Coverage Matrix**

- Type: required main result table.
- Position: early in Section 6.
- Columns: program family, expert MR source, operator block, expert coverage 0/1, NOETHER coverage 0/1, expert MR evidence, NOETHER MR-class evidence, executability note.
- Use: primary evidence against expert MR sets.

**Table 8 — Added NOETHER MR Classes Beyond Expert Sets**

- Type: derivation-summary table.
- Position: after Table 7.
- Columns: program family, added MR class, operator block, governing-equation source, duplicate of expert MR? yes/no, executable? yes/no.
- Use: prove that added classes are not merely parameter variants of expert MRs.

**Fig. 5 — Operator-Block Coverage Heatmap**

- Type: binary heatmap.
- Suggested tool: seaborn/matplotlib if values are finalized; otherwise LaTeX table may suffice.
- Position: after Table 7 or in summary paragraph.
- Data source: Table 7 only.
- Use: visual summary of expert-vs-NOETHER coverage breadth.

Important:

Do not generate Fig. 5 until Table 7 values are finalized from real evidence.

---

### Section 7. NOETHER and Search-Based MR Generation: Complementarity

**Goal:** Contrast NOETHER with search-based generation on explanation and maintenance dimensions.

**Purpose for readers:** Readers should understand that search can discover candidate relations, while NOETHER explains relation classes and boundaries.

**Core messages:**

1. Search-based generation and NOETHER answer different questions.
2. Generated candidates may need screening, deduplication, interpretation, and maintenance.
3. NOETHER derives named classes from operator blocks, making origin and boundary inspectable.
4. GenMorph should be treated as a representative complementary method, not an opponent to defeat.
5. Any existing head-to-head results should be demoted to context or appendix unless needed for a narrow complementarity point.

**Acceptance criteria:**

1. Claims about search-method readability, redundancy, maintainability, or screening burden cite real literature.
2. GenMorph comparison is not framed as the central contribution.
3. The section contains no unsupported superiority claim.
4. The section explains what search does well.
5. The reader can see why NOETHER and GenMorph are complementary.

**Planned figures/tables:**

**Table 9 — Search-Based Methods vs. NOETHER Origin/Boundary Matrix**

- Type: required comparison table.
- Position: main body.
- Columns: method type, output, origin explanation, boundary explanation, redundancy risk, readability/maintainability burden, evidence source, role in this paper.
- Use: primary evidence against search-based generation.

**Fig. 6 — Candidate Generation vs. Class Derivation**

- Type: conceptual contrast diagram.
- Suggested tool: Mermaid.
- Position: optional, after Table 9.
- Content: search path produces candidate relations needing interpretation; NOETHER path starts from operator algebra and produces named MR classes with assumptions.
- Use: clarify complementarity visually.

**Appendix table — Demoted Head-to-Head Results**

- Type: appendix-only numeric table, if retained.
- Use: preserve reproducibility without allowing effectiveness numbers to drive the paper.

---

### Section 8. Cross-Domain Derivations and Boundary Cases

**Goal:** Show that the same operator block can explain MR classes across different domains, and that NOETHER can also state boundaries where its current signature does not apply.

**Purpose for readers:** Readers should see generality as structural transfer, not as performance generalization.

**Core messages:**

1. Shared MR classes arise from shared operator-block origins.
2. Different domains and solvers can instantiate the same block.
3. Cross-domain examples should be independent of expert MR labels.
4. Negative instantiations are valuable because they define framework boundaries.
5. Boundary cases support honesty rather than weaken the theory.

**Acceptance criteria:**

1. Include at least 2-3 cross-domain examples in the form: same operator block -> different program family/solver -> MR class.
2. Each example cites an existing manuscript derivation or supplement source.
3. Each example states assumptions and interface affordances.
4. Negative PWR/compositional cases are framed as boundary clarification.
5. No cross-domain claim is presented without a governing-equation/operator source.

**Planned figures/tables:**

**Table 10 — Cross-Domain Shared Operator-Block Examples**

- Type: required cross-domain table.
- Position: beginning or middle of Section 8.
- Columns: operator block, mathematical source, program family A, MR class A, program family B, MR class B, optional program family C, boundary note.
- Use: prove that NOETHER identifies structural origins rather than memorizing domain examples.

**Table 11 — NOETHER Derivation Trace Table**

- Type: required audit table.
- Position: main text in compact form; full version in appendix.
- Columns: program family, governing equation/operator, independent source, operator block, derived MR class, assumptions, interface affordances, executable 0/1, reason if not executable, evidence location.
- Use: anti-circularity mechanism.

**Fig. 7 — Shared Operator Block Across Domains**

- Type: hub-and-spoke conceptual diagram.
- Suggested tool: draw.io or Mermaid.
- Position: after Table 10.
- Content: one operator block at center, arrows to several program families and MR classes.
- Use: make cross-domain transfer intuitive.

**Table 12 — Boundary and Out-of-Scope Cases**

- Type: limitations-in-theory table.
- Position: end of Section 8 or Threats.
- Columns: case, why not covered by current Translate signature, needed extension, status.
- Use: turn negative instantiations into theoretical boundary evidence.

---

### Section 9. Practical Implications for Program-Family Testability

**Goal:** Explain what the theory means for testers and software designers without turning implications into the main contribution.

**Purpose for readers:** Readers should understand that NOETHER suggests design-for-testability affordances: programs can expose controls/observables that make algebraically valid MR classes executable.

**Core messages:**

1. MR identification can reveal missing interface affordances.
2. Identified-but-not-executable MRs motivate design-for-testability decisions.
3. Program families with shared governing equations can reuse MR classes.
4. Tooling can partially automate downstream derivation once the operator algebra is curated.
5. The remaining human role is to distil the program-family algebra and judge domain assumptions.

**Acceptance criteria:**

1. Design-for-testability appears as implication/future work, not a main contribution.
2. Practical guidance is tied to the two-level model.
3. The section does not promise automated end-to-end MR discovery.
4. Interface affordances are named concretely.
5. The text is useful to practitioners without overclaiming deployment readiness.

**Planned figures/tables:**

**Table 13 — Interface Affordance Checklist**

- Type: practitioner checklist.
- Position: Section 9.
- Columns: MR class need, required controllable input, required observable output, common missing interface, design-for-testability action.
- Use: translate theory into actionable software-engineering guidance.

**No new data figure recommended.**

Reason:

This section is interpretive. A checklist carries the practical message more cleanly than a chart.

---

### Section 10. Threats to Validity and Limitations

**Goal:** State the limits that match the real RQ.

**Purpose for readers:** Readers should trust the paper because it concedes the right things: binary coverage is not effectiveness, expert sets may be incomplete, and operator-block taxonomy is curated.

**Core messages:**

1. Binary operator-block coverage measures design-space breadth, not MR quality or observed fault-revealing strength.
2. Expert MR sets may under-record expert tacit knowledge.
3. Search-method comparison depends on cited literature unless a direct study is conducted.
4. Operator-block taxonomy is empirically curated and may need extension.
5. LLM-assisted labels are not equivalent to independent human expert agreement.
6. Some MR classes are identified but not executable under current interfaces.

**Acceptance criteria:**

1. Threats align with the RQ and evidence design.
2. Mutant-kill and effectiveness limitations are explicitly scoped as secondary.
3. Claims from LLM panels are treated as corroborative, not confirmatory.
4. Future work separates theory extension, human validation, search-method empirical study, and executable validation on production codes.
5. No limitation accidentally expands the paper's main claim.

**Planned figures/tables:**

**Table 14 — Threats Mapped to Evidence Claims**

- Type: threat traceability table.
- Position: Section 10.
- Columns: claim, threat, possible bias direction, mitigation in manuscript, future work.
- Use: show reviewers that each evidence limit is understood.

---

### Section 11. Artefact and Supplementary Material

**Goal:** Make evidence auditable and reproducible.

**Purpose for readers:** Readers should know where to find coverage matrices, derivation traces, expert MR corpora, search-method comparison sources, and secondary results.

**Core messages:**

1. Main-text tables are summaries; full evidence lives in supplementary material.
2. Every coverage cell should be traceable.
3. Every derived MR class should have a derivation source.
4. Secondary mutation/effectiveness results, if retained, belong in clearly marked supplementary locations.
5. Artifact availability should satisfy ACM expectations.

**Acceptance criteria:**

1. Supplementary mapping is complete and named consistently.
2. Main-text evidence points to exact files/sections.
3. Artifact statement avoids promising unavailable DOIs during review.
4. Review-stage and acceptance-stage availability are clearly separated.
5. No important coverage claim lacks an evidence pointer.

**Planned figures/tables:**

**Table 15 — Artifact Evidence Index**

- Type: artifact map.
- Position: Section 11.
- Columns: evidence item, main-text use, supplementary file/path, reproducibility status, review-stage availability.
- Use: gives reviewers an audit trail.

---

### Section 12. Conclusion

**Goal:** Close with the theoretical contribution and its limits.

**Purpose for readers:** Readers should remember NOETHER as a framework that explains where MR classes come from and where they apply.

**Core messages:**

1. NOETHER derives MR classes / MetaPatterns from governing-equation operator algebra.
2. It makes MR origin and boundary explicit.
3. It broadens expert MR design-space coverage at the operator-block level.
4. It complements search-based generation by adding explanation and maintainability.
5. It points toward design-for-testability for making more identified classes executable.

**Acceptance criteria:**

1. Conclusion does not claim general fault-detection superiority.
2. Conclusion does not claim NOETHER replaces experts.
3. Conclusion does not claim search-based methods are unnecessary.
4. The final paragraph returns to program-family testability and oracle modeling.
5. The conclusion mirrors the RQ and evidence axes.

**Planned figures/tables:**

No new figure or table.

Reason:

The conclusion should synthesize, not introduce new visual evidence.

---

## 3. Figure Plan Summary

This is a planning list only. Do not generate figures until table values and section wording are stable.

| Figure | Title | Section | Type | Tool | Necessity | Purpose |
|---|---|---:|---|---|---|---|
| Fig. 1 | RQ and Evidence Map | 1 | Conceptual flow | Mermaid/draw.io | High | Tell readers how to evaluate the paper |
| Fig. 2 | Two-Level MR Model | 3 | Pipeline | Mermaid | High | Separate identified MR class from executable MR instance |
| Fig. 3 | NOETHER Derivation Pipeline | 4 | Method flowchart | Mermaid | High | Make the method procedural |
| Fig. 4 | Evidence Architecture | 5 | Three-lane diagram | Mermaid | Medium | Show how evidence axes answer the RQ |
| Fig. 5 | Operator-Block Coverage Heatmap | 6 | Binary heatmap | seaborn/matplotlib | Medium | Visualize Table 7 after evidence is finalized |
| Fig. 6 | Candidate Generation vs. Class Derivation | 7 | Conceptual contrast | Mermaid | Medium | Explain complementarity with search |
| Fig. 7 | Shared Operator Block Across Domains | 8 | Hub-and-spoke | draw.io/Mermaid | High | Make cross-domain structural sharing visible |

Figure selection rule:

Include Fig. 1, Fig. 2, Fig. 3, and Fig. 7 unless page pressure is severe. Fig. 4, Fig. 5, and Fig. 6 are optional and should be included only if they remove substantial textual explanation.

---

## 4. Table Plan Summary

| Table | Title | Section | Necessity | Purpose |
|---|---|---:|---|---|
| Table 1 | Contribution-to-Evidence Map | 1 | High | Prevent misreading of the paper as an effectiveness benchmark |
| Table 2 | Positioning Matrix of MR Identification Approaches | 2 | High | Frame expert/search comparisons |
| Table 3 | Core Definitions and Counting Rules | 3 | High | Define coverage and the two-level MR model |
| Table 4 | Operator Blocks and Derivation Templates | 4 | High | Present the NOETHER taxonomy |
| Table 5 | Per-Block Derivation Cost | 4 / Appendix | Low-Medium | Preserve algorithmic cost detail |
| Table 6 | Evidence-to-RQ Traceability Matrix | 5 | High | Connect evidence design to RQ |
| Table 7 | Expert vs. NOETHER Operator-Block Coverage Matrix | 6 | Critical | Primary expert-set comparison |
| Table 8 | Added NOETHER MR Classes Beyond Expert Sets | 6 | High | Show added classes are not duplicates |
| Table 9 | Search-Based Methods vs. NOETHER Origin/Boundary Matrix | 7 | Critical | Primary search-method comparison |
| Table 10 | Cross-Domain Shared Operator-Block Examples | 8 | Critical | Show structural sharing across domains |
| Table 11 | NOETHER Derivation Trace Table | 8 / Appendix | Critical | Audit every NOETHER coverage claim |
| Table 12 | Boundary and Out-of-Scope Cases | 8 / 10 | High | Explain framework limits |
| Table 13 | Interface Affordance Checklist | 9 | Medium | Translate theory into design-for-testability guidance |
| Table 14 | Threats Mapped to Evidence Claims | 10 | High | Align limitations with claims |
| Table 15 | Artifact Evidence Index | 11 | High | Help reviewers audit evidence |

Table reduction rule:

If page pressure is high, keep Tables 3, 4, 7, 9, 10, 11, and 14 in the main text; move Tables 1, 2, 5, 8, 13, and 15 to appendix or supplementary material.

---

## 5. Handling Existing Sections and Tables

### Current Introduction

Keep:

1. Motivation around MR identification.
2. Existing scope-of-contribution language if revised to the new RQ.

Change:

1. Move effectiveness or engineering-payoff language out of the opening frame.
2. State binary operator-block coverage and origin/boundary explanation earlier.

### Current Background and Related Work

Keep:

1. MT identification bottleneck.
2. METRIC/METRIC+ and automated MR identification comparisons.

Change:

1. Reorder around expert/search/framework categories.
2. Add literature-backed discussion of generated tests/oracles readability and maintainability.

### Current NOETHER Framework

Keep:

1. Operator-algebraic preliminaries.
2. Block definitions.
3. Construct-MP / Translate logic.
4. Closure theorem and principal limitation.

Change:

1. Insert two-level MR model before derivation details.
2. Make every block table row include origin, boundary, and interface affordance.
3. Move excessive instantiation detail to later evidence sections or appendix.

### Current Boltzmann, Equivariant ML, Relational Optimizer, and Negative PWR Sections

Keep:

1. Derivation examples.
2. Cross-domain material.
3. Negative instantiation as boundary evidence.

Change:

1. Reframe as cross-domain derivation evidence.
2. Extract at least 2-3 shared-operator-block examples for Table 10.
3. Move long derivations to appendix if they interrupt the main RQ flow.

### Current Empirical Evaluation

Keep:

1. Material that helps explain complementarity, boundary, or structural coverage.
2. Cost material if it supports practical adoption.
3. GenMorph protocol details only if they clarify search complementarity.

Move/Demote:

1. Mutation kill-rate tables.
2. DeepCrime-style pilot.
3. Head-to-head statistical tests.
4. H3a effectiveness verdict language.

New placement:

Secondary appendix or supplementary section titled "Secondary Executability and Sanity-Check Evidence."

Reason:

These results are not wrong, but they currently create the wrong reading frame.

### Current Threats and Limitations

Keep:

1. Upstream curation limitation.
2. LLM-rater caveat.
3. Human role and partial automation discussion.
4. Artifact availability.

Change:

1. Make threats correspond to the new evidence axes.
2. Add expert-set incompleteness and identified-but-not-executable limitations.
3. Move design-for-testability into implication/future work.

---

## 6. Cross-Section Acceptance Checklist

Before editing is considered complete, the revised manuscript must pass these checks:

1. The abstract, introduction, and conclusion all state the same RQ.
2. The words "fault detection", "kill", "mutant", and "effectiveness" appear only in scoped secondary contexts, limitations, or appendices.
3. The main evaluation/evidence sections are ordered as expert coverage, search complementarity, and cross-domain derivation.
4. Every operator-block coverage claim is backed by a concrete expert MR or NOETHER-derived MR class.
5. Every search-method claim about readability/redundancy/maintenance is backed by literature.
6. Every cross-domain example has a governing-equation/operator source.
7. Identified-but-not-executable MRs are reported honestly.
8. GenMorph is consistently framed as complementary.
9. SACOS/SPARK/LOCUST are used as MR-identification breadth evidence, not as effectiveness evidence.
10. The paper ends with MR origin, boundary, and program-family testability, not mutation superiority.

---

## 7. Recommended Rewrite Order

1. Rewrite Introduction and Contributions.
2. Add Problem Model and Scope section with the two-level MR model.
3. Rebuild NOETHER Framework tables around operator origin and boundary.
4. Draft Evidence Design and Coverage Protocol.
5. Build Table 7 from SACOS/SPARK/LOCUST and other expert corpora.
6. Build Table 9 using cited generated-test/search literature.
7. Extract cross-domain examples and build Tables 10-11.
8. Move secondary effectiveness material to appendix.
9. Rewrite Threats and Conclusion.
10. Conduct final consistency audit against the RQ.

Reason:

This order fixes the reader frame before touching evidence-heavy sections. Once the RQ and definitions are stable, the coverage tables can be filled without ambiguity.

---

## 8. Minimal Main-Text Visual Set

If the manuscript must be kept lean, use this minimal set:

1. **Fig. 1:** RQ and Evidence Map.
2. **Fig. 2:** Two-Level MR Model.
3. **Fig. 3:** NOETHER Derivation Pipeline.
4. **Fig. 7:** Shared Operator Block Across Domains.
5. **Table 3:** Core Definitions and Counting Rules.
6. **Table 4:** Operator Blocks and Derivation Templates.
7. **Table 7:** Expert vs. NOETHER Coverage Matrix.
8. **Table 9:** Search vs. NOETHER Origin/Boundary Matrix.
9. **Table 10:** Cross-Domain Shared Operator-Block Examples.
10. **Table 11:** NOETHER Derivation Trace Table.
11. **Table 14:** Threats Mapped to Evidence Claims.

This is the smallest set that still lets the paper carry the RQ honestly.
