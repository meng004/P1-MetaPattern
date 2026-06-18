```json
{
  "overall_recommendation": "Major Revision",
  "reviewer_confidence_1to5": 4,
  "scores_1to5": {
    "soundness": 3,
    "novelty": 4,
    "significance": 3,
    "presentation": 2,
    "reproducibility": 2
  },
  "summary": "The paper proposes NOETHER, a theory-guided framework to identify metamorphic-relation (MR) classes (MetaPatterns) from an operator-algebraic view of a program family. It defines eight upstream operator blocks (symmetry, order, self-adjointness, time reversal, limits, qualitative dynamics, method comparison, relational equivalence) and a downstream CONSTRUCT-MP procedure producing MetaPatterns with a by-construction closure theorem. It also contributes an Invariance-Blindness Theorem for two blocks, three domain instantiations, and a negative PWR case falsifying a stronger completeness claim.",
  "strengths": [
    "Ambitious, well-motivated attempt to formalize MR identification around an operator-algebraic scaffold and to articulate origin–closure–transferability explicitly (Section 1).",
    "Clear scoping of claims, including a candid negative result falsifying a stronger completeness claim on PWR diffusion and enumerating Translate obstructions (Section 3.7, Appendix C.6).",
    "Invariance-Blindness Theorem provides a non-tautological detection-kernel characterization for symmetry/self-adjoint blocks under linear assumptions (Section 3.3).",
    "Cross-domain instantiations (reactor physics, equivariant ML, relational optimizers) show the idea’s reach beyond a single domain (Sections 4, 5, 6)."
  ],
  "publication_blockers": [
    {
      "section": "Section 3.2 (Decidability Theorem, Theorem 2) and Table 1; Definitions 3.1–3.4",
      "issue": "The Decidability/complexity claim for CONSTRUCT-MP is under-specified and likely incorrect; Step 1 \"invariant extraction\" is left abstract, yet the theorem claims O(n · max t_i · log n) without a precise, executable algorithm or bounds on the size/structure of invariants, even for nontrivial algebras (e.g., Lie groups, PDE operators).",
      "why_fatal": "A core claimed contribution is algorithmic decidability/complexity. As stated, the theorem’s premises hide the hard part (computing invariants) inside opaque t_i and assume finite, tractable sets without proof. For several blocks, invariant computation is nontrivial or undecidable in general. Without a rigorous, per-block algorithm and complexity analysis (or a greatly narrowed scope), the complexity theorem is misleading and unsound."
    },
    {
      "section": "Definitions 3.2–3.4; Table A.1 (Translate templates) and Theorem 1",
      "issue": "Translate and the invariant/equivalence machinery are not formally specified to a level that supports the closure theorem beyond a by-construction tautology. Phrases like “canonical order specified by s” and “constraint equality up to relabelling” are not defined precisely per block, and equivalence classes are not given an effective decision procedure.",
      "why_fatal": "The claimed closure result hinges on a well-defined Translate and a computable equivalence on invariants. As written, these notions are partly informal and leave ambiguity (e.g., what canonical order means per block, which constraints are admitted). This undermines the theorem’s substance and reproducibility; minimal formalization is needed to make the result rigorous and evaluable."
    }
  ],
  "major_weaknesses": [
    {
      "section": "Sections 5–7 (empirical evaluations: ML case study, PIT/GenMorph head-to-head, METRIC+ comparisons)",
      "issue": "The empirical evidence is sprawling but underpowered and selection-biased: small N in the ML case (n=20 constructed mutants), multiple claims depend on author re-implementations of baselines (or omissions), use of LLM raters as “independent audit,” and heavy reliance on supplementary artifacts not provided.",
      "suggested_fix": "Provide a consolidated, preregistered evaluation on public subjects with publicly available code and data; avoid LLM raters as validators; add stronger and fair baselines (e.g., MR-Scout, METRIC+ realizations) or clearly separate them as out-of-scope; release the complete artifact to enable replication."
    },
    {
      "section": "Section 3.1 (Block decomposition hypothesis) and throughout",
      "issue": "Upstream modeling is an empirical hypothesis with no methodology for consistent, reproducible distillation of A_P; risks of subjectivity and poor inter-rater reliability are unaddressed (LLM ‘agreement’ is not a valid substitute for human inter-rater reliability).",
      "suggested_fix": "Define and evaluate a concrete, auditable protocol for distilling A_P (coding guide, training, examples), and report human inter-rater agreement on multiple domains; include failure cases and decision logs."
    },
    {
      "section": "Sections 4–6 (instantiations) and 7.4 (Path A)",
      "issue": "Several comparisons rely on author-constructed SUTs or re-implementations (e.g., METRIC+ benchmark programs) and ‘pre-registered’ configs stored in a private supplement; this weakens external validity.",
      "suggested_fix": "Use original benchmark implementations where possible; if re-implementation is unavoidable, have an independent team supply them; host prereg and all scripts in an accessible artifact for review."
    },
    {
      "section": "Section 3.2 and Theorem statements",
      "issue": "Theorems (closure, decidability) conflate definitional closure with meaningful completeness, and complexity is presented without acknowledging known hardness for some operator classes (e.g., symbolic invariants, relational equivalence generality).",
      "suggested_fix": "Recast Theorem 1 explicitly as a definitional closure lemma, and either (i) drop Theorem 2 or (ii) scope it to a narrowly defined class with a fully specified algorithm and proven bounds; add counterexamples and limits where invariant extraction is intractable."
    },
    {
      "section": "Presentation throughout",
      "issue": "The paper is overlong and hard to follow (many detours, footnotes, sidebars, future-work placeholders); core technical definitions are scattered; results depend heavily on out-of-band supplements.",
      "suggested_fix": "Substantially streamline: concentrate core definitions and theorems; move long empirical discursions to an artifact or appendix; present one focused, well-powered evaluation."
    }
  ],
  "minor_issues": [
    "Overuse of rhetorical caveats (“pre-registered,” “committed as follow-up”) in a journal article; focus on completed, verifiable results.",
    "Some references look uncertain or uncheckable in context (e.g., regulatory guide numbering); verify all citations.",
    "Inconsistent naming (Theorem 1′ is called a conjecture then a theorem; clarify).",
    "Canonical-block ordering rationale is weak; justify or treat it as a tie-breaker convention explicitly.",
    "Several per-block Translate templates remain informal; provide precise signatures and examples, or collapse into a minimal core.",
    "Tables/figures frequently refer to supplements; ensure all essential material is in the paper or an accessible artifact."
  ],
  "questions_to_authors": [
    "Provide a precise, per-block formal definition of Translate, including how input tuples are generated, what constraints π may express, and a decision procedure for the equivalence ~s. Can this be machine-checked on your artifacts?",
    "Give a concrete algorithm for Step 1 (invariant extraction) per block with complexity analysis; show it on at least one nontrivial algebra (e.g., SO(3) for equivariance) without handwaving t_i.",
    "Release the full artifact (code, data, preregistration documents) used for all empirical results so reviewers can verify claims and reproduce numbers.",
    "Demonstrate inter-rater reliability for human experts in distilling A_P on at least two domains; avoid LLM raters as proxies for independent human judgment.",
    "For METRIC+ and MR-Scout comparisons: provide fair, executed baselines or move these to future work; alternatively, narrow the claims to structural mapping and remove any performance implications.",
    "Clarify the scope of the Decidability theorem: for which classes of algebras and invariant schemas is it actually computable in polynomial time? If this is not defensible, remove or restate as an assumption."
  ]
}
```

Detailed reviewer report

Summary and contributions
The paper tackles a foundational problem in metamorphic testing (MT): how to identify metamorphic relations (MRs) systematically, beyond ad hoc or search-based approaches. It proposes NOETHER, a two-layer framework: an upstream, empirically curated decomposition of a program family’s operator algebra into eight “blocks,” and a downstream, constructive procedure (CONSTRUCT-MP) deriving MetaPatterns/MR classes from these blocks. The paper claims: (i) a closure theorem for the algebra-induced MR space under a Translate operator, (ii) a decidability theorem for the construction given a finite generating set, (iii) an Invariance-Blindness Theorem characterizing detection kernels for symmetry and self-adjoint blocks, (iv) cross-domain instantiations (reactor physics, equivariant ML, relational optimizers), and (v) a negative instantiation falsifying a stronger “absolute completeness” claim on a PWR diffusion algebra.

Novelty and significance
Conceptually, this is a creative and ambitious effort to ground MR identification in the mathematical structure of a program family. The articulation of the origin–closure–transferability gap is compelling. The Invariance-Blindness Theorem, while scoped to linear faults and two blocks, is a meaningful characterization that can inform practitioners about blind spots. The negative completeness result and isolation of Translate obstructions are refreshingly candid.

However, the practical significance is not yet demonstrated. The empirical sections remain sprawling and heavily caveated; they do not convincingly show that NOETHER substantially changes practice or outperforms strong baselines. The reliance on an upstream human-curated algebra and the lack of a clear, reproducible method to extract it across teams limit immediate impact.

Technical soundness
Positives:
- The closure result, presented as “by-construction,” is consistent once “algebra-induced MR space” is defined via Translate. This is honest about scope.
- The Invariance-Blindness Theorem is plausible and supported for linear faults, with a faithfulness condition; the finite-witness existence lemma is standard linear algebra.

Concerns:
- Decidability/complexity (Theorem 2) is not substantiated. Step 1 “invariant extraction” is precisely the hard part and is left as a black box with cost t_i; the theorem then bounds the total as O(n · max t_i · log n). For several blocks, invariant computation is not trivial, may depend on symbolic reasoning, or can be undecidable in general (e.g., general relational equivalence; even with a finite rule set, checking invariance across nontrivial algebras is not naively poly-time). As written, the theorem risks misleading readers about algorithmic guarantees.
- Translate and invariant equivalence lack formal precision. Statements like “canonical order specified by s” and equivalence up to “constraint relabeling” need formal definitions and examples for each block. Without a precise definition of the constraints π, and an effective equivalence test, Theorem 1 (closure) is little more than a definitional restatement.
- The operator-algebra upstream hypothesis is left as an empirical curation. This is acknowledged, but the absence of a protocol (and demonstrated inter-rater agreement by human experts) is problematic for a method that aspires to be foundational.

Empirical evaluation
The empirical story attempts many things at once (LLM case study, mutation tests on Java SUTs with PIT and GenMorph, METRIC+ mappings, MR-Scout positioning, DeepCrime pilot). Unfortunately:
- The ML case study is small (n=20 artificial mutations) and construct-biased (fault classes chosen per block); unique detections for the time-reversal MR then reflect construct validity, not generality.
- The Java head-to-head shows Set N is dominated in aggregate by GenMorph; the authors pivot to per-block interpretation and complementarity. This is fine as a qualitative insight, but it is not evidence of practical superiority.
- Several comparisons rely on author-built SUTs, private preregistration configs, and LLM raters for “audits,” which is not acceptable evidence for TOSEM-level empirical claims.
- Many claimed results and protocols defer to supplementary artifacts that are not accessible in review.

Presentation
The paper is dense and overly expansive. It contains many sidebars, caveats, and forward references to future work. Core definitions and theorems are diluted by rhetorical asides. The result is hard to follow and evaluate. A much shorter, tighter paper focusing on the formal core (definitions, theorems, one clean instantiation) plus a single, well-powered empirical evaluation would be far clearer.

Reproducibility
At review time, reproducibility is low. Critical definitions are informal, and empirical claims depend on an unavailable artifact and author re-implementations. The paper promises an artifact upon acceptance, but review decisions at TOSEM must be based on assessable material.

Publication blockers
1) Decidability/complexity theorem (Theorem 2) as stated is under-specified and likely incorrect. Step 1 (invariant extraction) subsumes the hard problems, yet is assumed tractable per generator. For nontrivial algebras and blocks, this is not substantiated. This is a central claimed contribution and must be corrected, sharply scoped, or removed.

2) The Translate operator and equivalence relation are not precisely and formally defined per block, beyond informal text and a brief template table. Without a rigorous per-block signature, tuple-generation rule, and equivalence decision procedure, the closure theorem is not meaningful beyond a tautology. The lack of formalization also harms reproducibility.

Recommendations for a major revision
- Formalization: Provide precise, per-block definition of Translate (domain, codomain, admissible π constraints), the canonical tuple-generation procedure, and the equivalence ~s with an effective test. Include at least one fully worked, machine-checkable example for each non-empty block you use in experiments.
- Complexity: Either remove Theorem 2 or limit it to a narrowly defined class with a fully specified invariant-extraction algorithm and proof of complexity. Acknowledge known hardness for general relational equivalence and for invariant synthesis in symbolic domains; align claims accordingly.
- Upstream algebra protocol: Define and evaluate a concrete protocol for distilling A_P (with a manual and examples) and report human inter-rater reliability on at least two domains. Do not use LLM raters as a substitute for human experts.
- Evaluation: Consolidate to one main empirical evaluation that is adequately powered, fair, and reproducible. Prefer public subjects and public implementations; eliminate self-authored SUTs where possible. Execute strong baselines (e.g., MR-Scout where appropriate, a METRIC+ realization if feasible) or clearly narrow claims to structural mapping only. Provide the full replication package in the submission.
- Scope and claims: Recast the closure statement explicitly as a definitional closure under a precisely defined Translate. Treat the canonical-block ordering as a convention rather than a theorem-enabler. Keep the Invariance-Blindness Theorem and negative completeness result—they are the best founded parts.

Minor editorial fixes
- Reduce rhetorical pre-registration/future-work language; present verified results only.
- Tighten references and ensure all are checkable.
- Clarify the “Theorem 1′/Conjecture” naming and final status.
- Justify or downplay the canonical-block ordering; it is a tie-breaking convention.

Bottom line
The paper contains an interesting and potentially influential line of thought, especially the formal framing of algebra-induced MR classes and the Invariance-Blindness result. However, the current version overclaims on algorithmic decidability/complexity, lacks formal precision in key definitions, and relies on underpowered or non-independent empirical material. A substantial revision is needed to make the theoretical core rigorous, the claims properly scoped, and the evaluation convincing and reproducible.