# NOETHER Research Question and Restructuring Plan

**Date:** 2026-06-18

**Purpose:** Record the settled research question and use it as the control document for restructuring the NOETHER manuscript. This document deliberately separates MR identification from MR effectiveness so that the paper's argument, evidence, tables, and limitations all answer the same question.

---

## 1. Settled Research Question

### 1.1 Main Research Question

**RQ:** How can an operator-algebraic, structured MR-identification method derive a broader and more explainable MR class / MetaPattern design space than expert-experience-based MR sets and search-based MR generation methods, by making the algebraic origin and applicability boundary of MRs explicit from the governing equations of a program family?

Chinese formulation:

**本文研究问题是：如何通过程序族控制方程中方程算子的代数性质，系统化识别 MR class / MetaPattern，从而比专家经验集合和搜索式 MR 生成方法覆盖更广的 MR 设计空间，并解释每类 MR 的来源与边界？**

This is a research question about **MR identification**, not about MR fault-revealing effectiveness.

### 1.2 Scope Firewall

The manuscript must state and maintain the following scope boundary:

1. The paper evaluates whether NOETHER can identify structurally justified MR classes from governing-equation operator algebra.
2. The paper does not evaluate whether the identified MRs are more effective at revealing faults, killing mutants, or improving observed defect-detection rates.
3. Mutation results, if retained, are secondary sanity checks or historical context; they must not become the main evidence for the research question.
4. GenMorph is a complementary search-based baseline, not the central opponent. The key contrast is between unexplained/generated relations and algebraically derived MR classes with explicit origin and boundary.

Reason:

Reviewers can fairly criticize effectiveness claims if the paper appears to compete on mutant-kill rate or fault-detection superiority. The intended contribution is different: NOETHER changes the modeling of MR sources inside the oracle branch of program-family testability. The manuscript must therefore prevent theme drift.

---

## 2. Core Constructs to Define in the Paper

### 2.1 Program-Family Governing Equation

A program family is treated as an implementation family whose intended behavior is constrained by a common mathematical or physical governing equation, operator, or equation system.

Role in argument:

This construct explains why different programs, application domains, and numerical solvers can share MR classes: the shared source is not code similarity but the same kind of operator-algebraic property.

### 2.2 Operator Block

An operator block is a recurring algebraic or order-theoretic property of governing-equation operators from which one or more MR classes can be derived.

Examples of block-level categories should be taken from the manuscript's existing NOETHER taxonomy. The exact names used in the final paper must match the implemented taxonomy and tables.

Role in argument:

Operator blocks are the unit of design-space coverage. They replace vague claims such as "more MRs" with a checkable question: which independent algebraic origins are represented?

### 2.3 MR Class / MetaPattern

An MR class / MetaPattern is a reusable relation schema derived from an operator block. It describes an invariant or covariation relation that the program family ought to satisfy.

Role in argument:

This is the paper's main output level. The contribution is not just producing individual test cases; it is identifying the structural class from which executable MRs can be instantiated when interfaces permit.

### 2.4 Identified MR Class vs. Executable MR Instance

The paper must distinguish two levels:

1. **Identified MR class:** a relation schema derivable from a program family's governing-equation operator algebra.
2. **Executable MR instance:** a concrete MR that can be applied to a specific program interface, with controllable inputs and observable outputs.

Important rule:

If the equation contains a structure but the paper has not written a corresponding MR class, it does not count as coverage. If an MR class is identified but cannot be executed because the program interface lacks required control or observability, it is recorded as identified-but-not-executable, not as executable coverage.

Reason:

This two-level model prevents overclaiming. It also lets the paper explain a practical boundary of MR identification: some mathematically valid relations require testability affordances that existing programs may not expose.

### 2.5 Expert Coverage

Expert coverage is binary:

**Expert coverage = yes** if the expert MR set contains at least one MR belonging to the operator block.

**Expert coverage = no** if the expert MR set contains no MR belonging to that block.

Reason:

Binary coverage avoids turning the comparison into a count of MR instances. The comparison should be about structural design-space breadth, not about how many near-duplicate relations are listed.

### 2.6 NOETHER Coverage

NOETHER coverage is binary:

**NOETHER coverage = yes** if NOETHER derives at least one MR class from the program-family equation operator algebra in that operator block.

**NOETHER coverage = no** if NOETHER does not derive a written MR class for that block.

Reason:

This aligns the evidence with the research question. A block is covered only when the method makes the MR class explicit.

### 2.7 Search-Based Comparison

Search-based MR or oracle generation methods should be compared on explanatory structure rather than on fault detection:

1. Can the method state the algebraic or physical origin of the generated relation?
2. Can it state the boundary conditions under which the relation should or should not apply?
3. Does it produce relation classes that are readable and maintainable by testers?
4. Does it avoid redundant or numerically incidental relations?

Reason:

The manuscript should use existing literature on generated tests, generated oracles, readability, redundancy, and maintainability burden to motivate this comparison. The paper's own evidence should show that NOETHER gives origin/boundary explanations, not that it beats search methods in mutant killing.

---

## 3. Contribution Claims to Preserve

### C1. Theoretical Model of MR Origin

NOETHER models the source of MRs as algebraic properties of governing-equation operators. This makes explicit what domain experts often use implicitly.

Evidence required:

For each claimed operator block, the paper must show the governing-equation/operator source and the derivation route from that source to at least one MR class.

### C2. Broader Structural Coverage Than Expert MR Sets

NOETHER covers more operator blocks than the corresponding expert MR sets when evaluated as binary operator-block coverage.

Evidence required:

Use the expert-vs-NOETHER coverage table. Each yes/no cell must be traceable to a concrete MR in the expert set or a concrete NOETHER-derived MR class.

### C3. Explicit Boundary of MR Applicability

NOETHER explains where an MR class applies and where it stops applying, because the relation is tied to the assumptions of the operator block and governing equation.

Evidence required:

For each representative MR class, state the assumptions, required inputs/observables, and boundary cases. If an MR class is not executable for a program interface, record why.

### C4. Cross-Domain Sharing Through the Same Operator Block

Different application domains and different solvers can share MR classes when they instantiate the same operator block.

Evidence required:

Include at least 2-3 cross-domain examples of:

**same operator block -> different program family / solver -> corresponding MR class**

The examples should be drawn from the manuscript's existing mathematical-physics argument, not invented as new unsupported claims.

### C5. Complementarity With GenMorph

NOETHER and GenMorph answer different parts of the MR problem. GenMorph explores relations through search; NOETHER explains relation classes through operator algebra.

Evidence required:

The manuscript should use the GenMorph group only to establish complementarity and objective mismatch. It should not frame NOETHER's contribution as beating GenMorph on defect detection.

---

## 4. Required Three Tables

### Table 1. Expert vs. NOETHER Operator-Block Coverage Matrix

Purpose:

Show whether structured MR identification covers a broader MR design space than expert MR sets.

Recommended columns:

1. Program family / subject
2. Expert MR source
3. Operator block
4. Expert coverage (0/1)
5. NOETHER coverage (0/1)
6. Expert MR evidence
7. NOETHER MR-class evidence
8. Notes on interface executability, if relevant

Counting rule:

1. Expert coverage is 1 if at least one expert MR belongs to that operator block.
2. NOETHER coverage is 1 if at least one MR class has been explicitly derived for that block.
3. Equation structure alone is not coverage.
4. Identified-but-not-executable MR classes count as NOETHER identification coverage only if the MR class is explicitly derived; executability is reported separately.

Reason:

This table directly answers the expert-comparison half of the RQ. It is stronger than listing many MR instances because it measures independent structural origins.

### Table 2. Search-Based Methods vs. NOETHER Origin/Boundary Matrix

Purpose:

Show that NOETHER's advantage over search-based generation is explanation, boundary, and maintainability, not mutant killing.

Recommended columns:

1. Method type
2. Typical output
3. Origin explanation
4. Boundary explanation
5. Redundancy risk
6. Readability / maintainability burden
7. Evidence source
8. Role in this paper

Expected contrast:

1. Search-based methods may generate useful candidate relations but often require human screening, redundancy reduction, and interpretation.
2. NOETHER derives relation classes from named operator blocks, so the origin and boundary can be inspected.

Evidence rule:

Claims about search-based methods must be backed by real literature on generated tests/oracles, redundancy, readability, maintainability, and human screening burden. Do not use unsupported generalizations.

Reason:

This table prevents a false competition. The point is not that search is useless; the point is that search does not by itself provide the theoretical account of MR origin and boundary that NOETHER contributes.

### Table 3. NOETHER Derivation Trace Table

Purpose:

Make every NOETHER coverage claim auditable.

Recommended columns:

1. Program family / subject
2. Governing equation or operator
3. Independent mathematical / physical source
4. Operator block
5. Derived MR class / MetaPattern
6. Required assumptions
7. Required program-interface affordances
8. Executable instance available (0/1)
9. If not executable, reason
10. Manuscript or supplement evidence location

Reason:

This table is the anti-circularity mechanism. It shows that blocks are grounded in independent mathematical or physical sources and that NOETHER did not merely re-label existing expert MRs.

---

## 5. Manuscript Restructuring Plan

### 5.1 Abstract

Revise the abstract to state:

1. The problem is MR identification for program families with governing equations.
2. Existing expert MR sets can be narrow because they reflect implicit expert heuristics.
3. Search-based methods can generate candidates but do not necessarily explain MR origin or boundary.
4. NOETHER derives MR classes from operator-algebraic properties of equations.
5. Evidence is reported as operator-block coverage, derivation traces, and cross-domain sharing examples.

Remove or demote:

1. Any wording that suggests the central result is higher fault-detection rate.
2. Any wording that suggests NOETHER eliminates domain expertise.

Reason:

The abstract is where reviewers form the evaluation frame. It must tell them to judge the paper as an MR-identification theory and method paper.

### 5.2 Introduction

Rebuild the introduction around the following progression:

1. Metamorphic testing needs MRs, but MR identification remains a central oracle-side problem.
2. Expert experience can identify useful MRs, but it often leaves the source and boundary of MR classes implicit.
3. Search-based generation can discover candidates, but candidates may be redundant, difficult to interpret, or hard to maintain without a structural explanation.
4. For equation-governed program families, many MRs originate from operator-algebraic properties of the equations.
5. NOETHER makes these origins explicit and uses them to identify MR classes / MetaPatterns.
6. The paper asks whether this structured approach covers a broader MR design space than expert sets and explains origin/boundary better than search-based generation.

Reason:

This progression leads naturally to the real contribution and avoids opening a competition about fault-detection effectiveness.

### 5.3 Research Questions / Claims Section

Add or rewrite a compact RQ section:

**RQ1:** Can operator-algebraic analysis derive MR classes / MetaPatterns from governing-equation structures that are absent from expert MR sets?

**RQ2:** Can these derived MR classes be organized by explicit operator blocks, so that their algebraic origin and applicability boundary are inspectable?

**RQ3:** Do the same operator blocks explain shared MR classes across different domains, program families, or solvers?

**RQ4:** How does this structured identification model complement search-based MR generation with respect to explanation, redundancy control, readability, and maintenance?

Reason:

These RQs are directly answerable by the three tables and the existing mathematical-physics derivations. None requires proving superior mutant-kill rate.

### 5.4 Related Work

Reorganize related work into three tracks:

1. Expert MR identification and domain-knowledge-based MR design.
2. Search-based or generated MR/oracle/test methods.
3. Program-family testability and oracle modeling for metamorphic testing.

Required adjustment:

The generated-test/search literature should be used to support claims about readability, redundancy, maintainability, and human screening burden. Do not claim search methods are inferior unless the cited source supports the exact statement.

Reason:

This makes the literature review serve the RQ instead of becoming a loose catalog of MT work.

### 5.5 Theory / Method Section

Reframe the method section around derivation:

1. Define program family, governing equation, operator block, MR class, and executable MR instance.
2. State the derivation procedure from equation/operator assumptions to MR class.
3. State the classification rule for assigning MR classes to operator blocks.
4. State the coverage rule used in Table 1.
5. State the boundary rule: assumptions and interface affordances determine whether an identified class can become an executable MR.

Reason:

This section is the theoretical core. It should make the MR source explicit enough that a reviewer can audit whether a claimed MR class really follows from the operator block.

### 5.6 Evaluation / Evidence Section

Split the evaluation into three evidence groups:

**Group A: Expert-set coverage comparison**

Use Table 1 to compare expert MR sets with NOETHER by binary operator-block coverage.

**Group B: Search-based comparison**

Use Table 2 to contrast search-based methods and NOETHER on origin, boundary, redundancy, readability, and maintainability. Keep GenMorph as a complementary example rather than the main opponent.

**Group C: Derivation and cross-domain sharing**

Use Table 3 and 2-3 cross-domain examples to show that the same operator block can explain MR classes across different programs, domains, or solvers.

Reason:

This structure aligns each evidence group with a part of the RQ. It prevents the evaluation section from being judged as an effectiveness benchmark.

### 5.7 SACOS / SPARK / LOCUST Positioning

Use SACOS, SPARK, and LOCUST as evidence for expert-vs-NOETHER structural coverage if the paper can show:

1. The expert MR sets cover only a subset of operator blocks.
2. NOETHER derives additional MR classes from operator algebra.
3. The added classes are not merely duplicates or parameter variants of expert MRs.
4. Each added class has a clear governing-equation/operator source.
5. Interface limitations are explicitly marked where they prevent executable instances.

Reason:

These subjects are valuable because they show MR identification in realistic scientific/engineering programs. Their role is not to prove stronger bug-finding but to show broader structured MR design-space coverage.

### 5.8 GenMorph Positioning

Move GenMorph-related material into a complementarity subsection:

1. GenMorph represents search-based MR generation.
2. It can be useful for discovering candidates.
3. Its output needs interpretation, redundancy control, and maintainability assessment.
4. NOETHER supplies algebraic origin and boundary explanations.
5. Any head-to-head numeric result should be described as secondary and not load-bearing.

Reason:

This defuses the strongest reviewer objection: if the paper looks like an effectiveness contest, mixed quantitative results weaken the contribution. If the paper is framed as identification theory, GenMorph becomes useful context rather than a threat.

### 5.9 Threats to Validity / Limitations

Add limitations that match the RQ:

1. Operator-block coverage is binary and measures design-space breadth, not relation quality or fault-revealing strength.
2. Some identified MR classes may not be executable without suitable program interfaces.
3. The operator-block taxonomy must be traceable to independent mathematical or physical sources to avoid circular classification.
4. Expert MR sets may be incomplete records of expert knowledge.
5. Search-based method comparison relies on literature and conceptual contrast unless the paper runs a dedicated search-method study.
6. Design-for-testability is a future-work implication: programs may expose interfaces that make algebraically valid MR classes executable.

Reason:

These limitations make the paper more credible. They concede the right boundaries without weakening the core contribution.

### 5.10 Conclusion

Conclude with:

1. NOETHER provides a theory-guided method for MR identification.
2. It explains MR origin and boundary through governing-equation operator algebra.
3. It broadens expert MR design-space coverage at the operator-block level.
4. It complements search-based generation by improving interpretability and maintainability of MR classes.
5. It suggests design-for-testability as future work for making more identified MR classes executable.

Avoid:

1. Claims of general superiority in fault detection.
2. Claims that NOETHER replaces experts.
3. Claims that search-based methods are unnecessary.

Reason:

The conclusion should leave reviewers with the theoretical contribution, not a disputed effectiveness claim.

---

## 6. Evidence Discipline Rules

Every conclusion in the revised manuscript should satisfy one of these evidence routes:

1. **Textual evidence:** explicit line, table, or supplement entry showing an MR belongs to an operator block.
2. **Mathematical evidence:** derivation from a named governing equation/operator property.
3. **Comparative evidence:** binary coverage matrix cell backed by an expert MR or NOETHER-derived class.
4. **Literature evidence:** real cited source for generated-test/oracle readability, redundancy, maintainability, or human-screening claims.
5. **Boundary evidence:** explicit statement of assumptions and interface affordances required for execution.

Do not allow unsupported claims of:

1. Higher fault-detection effectiveness.
2. Better mutant-kill performance.
3. Full completeness of MR identification.
4. Elimination of human expertise.
5. Universal applicability across all scientific programs.

Reason:

This rule operationalizes "事实求是". It forces each claim to carry auditable evidence and keeps the paper within a defendable scope.

---

## 7. Concrete Rewrite Tasks

### Task 1. Insert the Final RQ and Scope Firewall

Modify the introduction and contribution section so that the RQ is stated as MR identification over operator-algebraic MR class / MetaPattern space.

Acceptance check:

The introduction contains the main RQ, the two comparison targets, and an explicit statement that the paper does not evaluate MR effectiveness.

### Task 2. Define the Two-Level MR Model

Add definitions for identified MR class and executable MR instance.

Acceptance check:

The paper explains how an MR can be derivable but not executable because of program-interface constraints.

### Task 3. Build Table 1

Create the expert-vs-NOETHER binary operator-block coverage matrix.

Acceptance check:

Every yes/no cell is backed by a concrete expert MR or NOETHER-derived MR class. Equation structure without a written MR class is not counted.

### Task 4. Build Table 2

Create the search-based-vs-NOETHER origin/boundary matrix.

Acceptance check:

Every claim about search-based methods is supported by real literature or removed.

### Task 5. Build Table 3

Create the NOETHER derivation trace table.

Acceptance check:

Every NOETHER coverage claim traces to a governing equation/operator, operator block, MR class, assumptions, and executability status.

### Task 6. Reposition SACOS / SPARK / LOCUST

Rewrite these subjects as evidence for structured MR identification breadth.

Acceptance check:

The section explains broader operator-block coverage and potential testability implications without claiming superior fault detection.

### Task 7. Reposition GenMorph

Rewrite GenMorph as a complementary search-based method.

Acceptance check:

The section contrasts search and structure on origin, boundary, redundancy, readability, and maintenance. Quantitative head-to-head results are secondary.

### Task 8. Add Cross-Domain Operator-Block Examples

Select 2-3 existing examples from the manuscript where the same operator block yields MR classes in different program families, domains, or solvers.

Acceptance check:

Each example has the form:

**operator block -> program family / solver A -> MR class A; program family / solver B -> MR class B**

### Task 9. Revise Threats and Future Work

Add limitations about binary coverage, expert-set incompleteness, identified-but-not-executable MRs, operator-block taxonomy, and search-method comparison.

Acceptance check:

Design-for-testability appears only as an implication or future-work point, not as the main contribution.

### Task 10. Final Consistency Audit

Search the revised manuscript for terms and claims that imply effectiveness competition.

Acceptance check:

Any use of fault detection, mutant killing, bug finding, or effectiveness is either removed, explicitly scoped as secondary, or placed in limitations/context.

---

## 8. Rationale for the Restructuring

### 8.1 It Aligns Evidence With the Actual Contribution

The strongest contribution is not that NOETHER kills more mutants. The contribution is that NOETHER identifies MR classes from operator algebra and explains their origin and boundary. The restructuring makes the evidence answer that contribution directly.

### 8.2 It Makes the Paper More Suitable for TOSEM

A TOSEM-level contribution should be a generalizable software engineering idea, not only a case-specific benchmark result. Framing NOETHER as a program-family testability and oracle-modeling contribution gives the paper a clearer theoretical software-engineering core.

### 8.3 It Reduces Reviewer Attack Surface

If the paper claims effectiveness, reviewers can focus on sample size, single seeds, mixed GenMorph results, and mutation adequacy. If the paper claims structured MR identification, the decisive evidence becomes derivation traceability, operator-block coverage, and boundary explanation.

### 8.4 It Preserves Complementarity

GenMorph and NOETHER can both be valuable. Search can discover candidate relations; operator algebra can explain why relation classes should exist and when they apply. This framing is more defensible than treating the two methods as substitutes.

### 8.5 It Gives SACOS / SPARK / LOCUST a Stronger Role

These programs are strongest as evidence that expert MR sets can be structurally narrow and that NOETHER can reveal additional operator-block-based MR classes. Their main value is identification breadth, not measured fault-revealing superiority.

### 8.6 It Handles the Interface Problem Honestly

The two-level model lets the paper acknowledge that some valid MR classes cannot be executed without suitable program interfaces. This is not a failure of MR identification; it is a boundary between theory, program observability, and design-for-testability.

---

## 9. One-Sentence North Star

**NOETHER contributes a theory-guided MR-identification framework: it derives MR classes / MetaPatterns from governing-equation operator algebra, thereby making MR origin, boundary, and structural coverage explicit beyond what expert MR sets or search-based generation alone usually provide.**
