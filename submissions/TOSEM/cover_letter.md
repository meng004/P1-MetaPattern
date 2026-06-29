# Cover Letter — Submission to ACM TOSEM (Fast Impact track)

**Date:** 30 June 2026

**To:** Prof. Mauro Pezzè, Editor-in-Chief
ACM Transactions on Software Engineering and Methodology (TOSEM)

Dear Professor Pezzè,

We are pleased to submit our manuscript **"NOETHER: Constructive Metamorphic Pattern
Identification from Operator Algebras and a Falsifiable Invariance-Blindness Theorem"**
for consideration in ACM TOSEM under the **Fast Impact** track.

## Scope, novelty, and contribution

The paper targets a software-testing problem that directly concerns the TOSEM readership:
metamorphic testing is valuable when test oracles are unavailable, but metamorphic-relation
(MR) identification remains largely experience- or search-driven. Existing approaches offer
limited structural explanation of *where* MR patterns (MetaPatterns) come from, *when* a
pattern catalogue is closed, or *how* it transfers across program families. NOETHER addresses
this origin–closure–transferability gap by turning MR identification into an auditable
construction over a program family's operator-algebraic structure.

The manuscript makes five contributions to software-engineering methods and foundations:

1. **A layered, constructive framework (NOETHER).** MetaPatterns are derived from the
   operator-algebraic structure of a program family by a mechanical algorithm
   (CONSTRUCT-MP), separating an empirical upstream layer (curating the algebra) from a
   provable downstream layer.
2. **Positive theory.** A no-drop closure invariant (Theorem 1) and polynomial-time
   constructibility under a finite generating set (Theorem 2) over the algebra-induced MR
   space.
3. **A falsifiable Invariance-Blindness Theorem.** For the symmetry and self-adjoint
   MetaPatterns, an algebra-derived MR's detection kernel equals *exactly* the
   structure-preserving faults: a non-tautological, testable characterisation of what such
   MRs can and cannot detect, confirmed on a held-out evaluation.
4. **A negative instantiation.** Absolute completeness is proved *false* on a PWR
   reactor-physics algebra via two counterexamples from the standard safety-analysis
   literature, identifying five independent obstructions and delimiting the theory's reach.
5. **Structural transferability and an evidence protocol.** The construction is instantiated on
   three structurally distinct operator-algebraic domains (Boltzmann reactor physics,
   equivariant machine learning, and relational query optimisers), under an MR-identification
   evidence protocol that treats mutation/head-to-head results as secondary executability
   checks rather than average-superiority claims.

## Validation and reproducibility

The evidence combines analytical and experimental validation paradigms. The closure and
constructibility claims are supported by formal derivations; the blindness theorem is stated as
a falsifiable prediction about detectable and undetectable fault classes; the PWR instantiation
deliberately reports a negative result to delimit the theory; and the three-domain protocol
checks whether the construction transfers beyond a single case.

The submitted data and artifact availability statement identifies the replication package,
supplementary material (S1–S12), prompts, raw outputs, mapping files, and scripts needed to
inspect or rerun the reported checks.

## Submission track and length

We request the **Fast Impact** track. The manuscript has been shortened so that the
main paper body fits the TOSEM Fast Impact 45-page limit in the official
`acmsmall,screen,review` format; references and online-only appendix / supplementary material
are kept outside the main-body count. Self-contained implementation details, detailed
derivation traces, and secondary tables have been migrated to appendices and supplementary
material.

## arXiv disclosure

A preprint of this work is available on arXiv (**arXiv:2605.17390**,
<https://arxiv.org/abs/2605.17390>). TOSEM is a single-blind journal, so the submitted
manuscript lists all authors and affiliations on the first page; this cover letter discloses
the related preprint for editorial transparency.

## Related / companion work (overlap disclosure)

A separate line of work by a subset of the authors addresses the **orthogonal** problem of
*selecting* a minimum complete subset from a *given* MR pool. That work takes an MR set as input
and minimises its cardinality under a fixed fault model; the present paper concerns the upstream
question of where MRs and MetaPatterns *come from*: their constructive derivation from a
program-induced operator algebra and algebraic closure under the `Translate` operator. The two
share no theorem or empirical claim.

## Generative-AI disclosure

In line with ACM's Policy on Authorship, large language models appear in this work in two roles.
As instruments of the study, they are part of the reported LLM baseline, LRCA second-rater
protocol, and mutant-equivalence adjudication; the prompts and raw outputs are released with the
replication package. As authoring assistance, the authors used a large-language-model assistant
for code scaffolding, reference formatting, and language editing. All research design, theorems,
proofs, experimental procedures, numerical results, and claims were produced and verified by the
authors, who take full responsibility for the manuscript.

## Competing interests

The authors declare no competing interests.

Sincerely,

**Meng Li** (corresponding author), on behalf of Xiaohua Yang, Jie Liu, and Shiyu Yan
School of Computing, University of South China, Hengyang 421001, China
mlemon@usc.edu.cn
