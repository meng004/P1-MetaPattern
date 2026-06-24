# Cover Letter — ACM TOSEM submission

**To:** Prof. Mauro Pezzè, Editor-in-Chief, *ACM Transactions on Software Engineering and Methodology (TOSEM)*

**Manuscript:** *NOETHER: Constructive Metamorphic Pattern Identification from Operator Algebras and a Falsifiable Invariance-Blindness Theorem*

**Submission track:** Regular paper.

**Authors:** Meng Li (corresponding, mlemon@usc.edu.cn), Jie Liu, Shiyu Yan, Xiaohua Yang — School of Computing, University of South China; Hunan Engineering Research Center of Software Evaluation and Testing for Intellectual Equipment; CNNC Key Laboratory on High Trusted Computing. Hengyang 421001, China.

---

Dear Professor Pezzè and the editorial board,

We submit *NOETHER* for consideration as a regular paper in TOSEM. The manuscript addresses the long-standing **metamorphic-relation (MR) identification bottleneck** in metamorphic testing: MR sets are still assembled by induction over observed examples, with no account of *where a relation comes from*, *where it stops applying*, or *whether the catalogue is complete*. NOETHER reframes MR identification as a derivation from a program family's governing-equation operator algebra, and makes the origin and applicability boundary of each MR class auditable.

**Principal contributions.**

1. A two-layer framework: an upstream, empirically curated structural decomposition of a program-induced operator algebra, and a downstream constructive algorithm (`CONSTRUCT-MP`) that mechanically derives MR classes / MetaPatterns from it.
2. A positive theory (closure invariant; polynomial-time constructibility under a finite generating set) and, in the same paper, a **negative result**: the strictly stronger absolute-completeness conjecture is *falsified* on a PWR core-diffusion algebra by two relations from the safety-analysis literature — bounding the method's reach rather than overclaiming it.
3. An **Invariance-Blindness Theorem** that characterises exactly which implementation faults an algebra-derived MR can and cannot detect, converting the closure result into a falsifiable, non-tautological prediction, confirmed on a held-out instance.
4. Instantiation across three structurally distinct domains (Boltzmann reactor-physics transport, equivariant ML, relational query optimisers), demonstrating structural transferability at the algebra-skeleton level.

**Scope, stated plainly.** The paper evaluates MR *identification*, not average fault-detection *effectiveness*; mutation/head-to-head results are reported as secondary executability checks. We have tried to be explicit about every boundary, including a documented out-of-scope catalogue and a falsified completeness conjecture.

**Length.** At its current length the paper carries the formal development (definitions, theorems, proofs), three-domain instantiation, and the empirical protocol together, because the contribution is precisely the *link* between the algebraic derivation and the resulting MR classes; separating them would break the argument. We submit under the regular track, which has no hard page limit, and are happy to migrate self-contained material to the online appendix per the journal's appendix policy.

**Prior dissemination (ACM policy disclosure).** A preprint of this manuscript is posted on arXiv (arXiv:2605.17390). No part of this work has been published in or is under review at any peer-reviewed venue.

**Relationship to a companion submission (salami disclosure).** A separate manuscript by an overlapping author group studies the *complementary* problem of selecting a minimum detecting MR subset (under review at *IEEE TSE*). The two papers share the two-layer MetaPattern / MR-family vocabulary (a single canonical definition is reused by citation) but make disjoint contributions: the present paper is about *deriving and bounding* the MR design space; the companion is about *selecting* within a given set. Neither paper's results depend on the other's.

**Generative-AI use.** Disclosed in full in the manuscript per the ACM Policy on Authorship: large language models appear both as instruments of the study (an evaluated baseline; a second-rater labelling protocol; mutant-equivalence adjudication) and as authoring assistance (code scaffolding, reference formatting, language editing). All research design, theorems, proofs, procedures, numerical results, and claims were produced and verified by the authors, who take full responsibility for the content.

We believe NOETHER fits TOSEM's interest in the methodological foundations of software testing, and we thank you for considering it.

Sincerely,
Meng Li, on behalf of all authors
