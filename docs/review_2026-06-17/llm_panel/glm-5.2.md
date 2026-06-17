```json
{
  "overall_recommendation": "Major Revision",
  "reviewer_confidence_1to5": 4,
  "scores_1to5": {
    "soundness": 3,
    "novelty": 4,
    "significance": 3,
    "presentation": 2,
    "reproducibility": 3
  },
  "summary": "The paper proposes NOETHER, a framework that derives MetaPatterns (equivalence classes of metamorphic relations) from the operator-algebraic structure of program families. It proves an algebraic closure theorem (Theorem 1, by-construction over the Translate-reachable MR space), a polynomial-time decidability result (Theorem 2), and an Invariance-Blindness Theorem characterizing the detection kernel of symmetry/self-adjoint MRs as exactly the structure-preserving faults within the linear fault class. It falsifies a stronger absolute-completeness conjecture on the PWR core diffusion algebra via two counterexamples, and reports empirical evidence including a small-scale case study on equivariant ML, a pre-registered L*-blindness prediction on PIT mutants, and head-to-head comparisons with GenMorph and METRIC+.",
  "strengths": [
    "The Invariance-Blindness Theorem (Theorem 3) is a genuine, non-trivial limiting result: it characterizes the exact blind set of symmetry and self-adjoint MRs under a linear fault model, with faithfulness attained by a finite test (Lemma 1). The corollaries on single-block incompleteness and differential-oracle complementarity are well-motivated and useful.",
    "The falsification of Theorem 1' on A_PWR via two regulatory-essential PWR MRs (rod-bank non-additivity, MTC-vs-boron mixed derivative) is a carefully argued negative result. The five identified Translate-extension obstructions are concrete and well-localized.",
    "The L*-blindness prediction (Section 5.2) is a clean, pre-registered, ex-ante falsifiable prediction derived from public information (framework structure + PIT mutator semantics) and confirmed on 5/6 SUTs. This is the strongest empirical result in the paper.",
    "The cross-domain instantiation on three structurally distinct algebras (Boltzmann transport, equivariant ML, relational query optimisers) demonstrates the framework's skeleton-level transferability, and the relational-equivalence block extends beyond the Lie-group/self-adjoint/time-reversal core.",
    "The deflationary direction (Section 5.4) — showing that inductive catalogues may over-count patterns — is a non-circular contribution that does not depend on the potentially circular prediction of T*/T* blocks."
  ],
  "publication_blockers": [
    {
      "section": "Theorem 1 (§3.2, Definition 7)",
      "issue": "Theorem 1 (Algebraic Closure) is near-tautological. MR(A_P) is defined (Definition 7) as exactly the set of MRs reachable through Translate from a single block invariant. CONSTRUCT-MP (Steps 1-4) explicitly enumerates all blocks, extracts all invariants, applies Translate, and forms equivalence classes. Theorem 1 then asserts that every MR in this set is assigned to some MetaPattern produced by this enumeration. The authors acknowledge this ('a sceptical reading might object that the by-construction status makes it near-tautological'), but the theorem is presented as a primary contribution (C2a) and the paper's 'structural-adequacy obligation' framing does not resolve the circularity: the scope of MR(A_P) is defined to be exactly what the construction produces.",
      "why_fatal": "The paper's headline theoretical contribution is a well-formedness statement about the construction's own output space, not a guarantee about the relationship between algebra-derived MRs and the MRs practitioners need. Until Theorem 1 is either replaced by a non-circular completeness result or explicitly demoted from a primary contribution to a structural-adequacy lemma, the paper's theoretical claims are overstated relative to what is proven."
    },
    {
      "section": "§5.1 (Case Study) and §5.2 (Head-to-head)",
      "issue": "The empirical evaluation does not demonstrate that NOETHER-derived MRs provide practical advantages over existing approaches. The case study (n=20 mutations, 1 model) has its mutation set explicitly constructed to cover one defect category per non-empty block, making the 5/5 cat-(iv) unique-detection result a construct-validity exhibit rather than evidence of superiority. The head-to-head against GenMorph shows Set N is dominated by Set G on the D1 stratum (McNemar p=0.019). The DeepCrime pilot (n=5) is underpowered (McNemar p=0.500). The L*-blindness prediction, while clean, confirms a mathematical fact about homogeneity preservation rather than demonstrating testing effectiveness.",
      "why_fatal": "For a TOSEM paper claiming a framework-level contribution, the empirical evidence must show that the framework produces MRs that are useful for testing in a way that existing approaches cannot achieve. The current evaluation, while honestly reported, does not meet this bar: the strongest result (L*-blindness) is essentially a mathematical identity confirmed empirically, and the head-to-head shows the framework's MRs are dominated by a GP baseline on the algebra-disrupting stratum."
    }
  ],
  "major_weaknesses": [
    {
      "section": "§3.1 (Hypothesis 1) and §3.2",
      "issue": "The eight-block decomposition is an empirical curation ('by-inspection enumeration'), not derived from algebraic axioms. The authors acknowledge this, but it means the framework's upstream layer — the critical step where domain expertise enters — is essentially the same inductive process the paper claims to improve upon. Moving induction from 'what MetaPatterns recur?' to 'what algebraic structures recur?' does not obviously reduce the inductive burden; it may increase it by requiring operator-algebraic literacy in addition to domain knowledge.",
      "suggested_fix": "Provide concrete evidence that distilling A_P from a program family is systematically easier or more reliable than identifying MRs directly. This could be a controlled user study, or at minimum a detailed worked example showing the step-by-step extraction of A_P for a non-trivial program family, with comparison to the effort of identifying MRs without the framework."
    },
    {
      "section": "§3.3 (Invariance-Blindness Theorem)",
      "issue": "The IBT is limited to the G and T* blocks under a linear fault class. The linear operator-implementation fault model (Definition 8) is very specific: L = L* + Δ with Δ ∈ R^{N×N}. Real faults in scientific computing, ML, and database systems are rarely linear perturbations of an operator matrix. The authors note that linearity fails for O_≤, T*_rev, and L*, but the practical implications of this limitation are not adequately discussed.",
      "suggested_fix": "Either (a) extend the IBT to at least one additional block (e.g., via linearization for O_≤), or (b) provide concrete examples showing what the linear fault model covers and what it misses in practice, with quantitative estimates of coverage on a real mutation catalogue."
    },
    {
      "section": "§5.1 (Construct Validity)",
      "issue": "The METRIC+ Path A head-to-head (§5.3) uses Java re-implementations of Sun et al.'s four subjects written by the same author who designed NOETHER, creating a construct-validity confound. The LLM inter-rater agreement figures (κ=0.857, κ=1.000) are from LLM panels with shared training data, not independent human experts. These two issues together mean the paper's breadth claims rest on potentially biased evaluation.",
      "suggested_fix": "For the METRIC+ comparison, obtain independent re-implementations or use the original authors' code. For the inter-rater agreement, conduct at least a small human expert study (n≥2 independent raters) to validate the LLM-panel labels."
    },
    {
      "section": "Paper length and structure",
      "issue": "The manuscript is excessively long (estimated 60+ pages compiled) with multiple boundary-of-contribution boxes, extensive pre-emptive caveats, and forward/backward references that make it very difficult to follow. The comment in the LaTeX source ('NOT wired into NOETHER_paper_arxiv.tex yet') for the IBT section suggests incomplete preparation. The paper attempts to be both a theoretical paper (with proofs) and an empirical paper (with experiments), but does neither satisfactorily within the space.",
      "suggested_fix": "Cut the paper to roughly half its current length. Remove redundant boundary-of-contribution restatements (there are at least four). Consolidate the empirical evaluation into a focused narrative around the L*-blindness prediction and one head-to-head comparison. Move detailed proofs and supplementary material to an appendix, keeping only the IBT proof and the PWR falsification proof in the main text."
    },
    {
      "section": "§3.4 and §5.5 (Circularity of 'prediction')",
      "issue": "The authors acknowledge that the T* and T* blocks were curated from reactor-physics structures, making the 'prediction' of m_adj and m_rev on reactor physics circular. The deflationary direction is claimed to be non-circular, but it is demonstrated on only three cases (sorting, Murphy et al.'s ML categories, reactor catalogue itself). The claim that NOETHER 'predicts' MetaPatterns is therefore overstated.",
      "suggested_fix": "Drop the 'prediction' framing entirely for T* and T* blocks. Reserve the prediction language for genuinely held-out cases (the deflationary direction, and the L*-blindness prediction). Clearly label the reactor-physics re-classification as 'systematisation under a uniform algebraic structure' rather than 'prediction'."
    }
  ],
  "minor_issues": [
    "The comment '%% NOT wired into NOETHER_paper_arxiv.tex yet (no LaTeX toolchain in container; B2 integration + compile audit per CLAUDE.md §8 to be done in a LaTeX env).' in the IBT section source suggests the paper may not have been properly compiled before submission. This should be verified.",
    "Table 5 (tab:pit-block) uses '∼' for case-dependent cells without explaining how the case is resolved at deployment time. A brief note pointing to the SUT-specific overrides would help.",
    "The equivalence-relation claim for ~_s (Definition 5) is asserted by construction but the 'same constraint up to relabelling' is not formally defined. A brief formalisation would strengthen the quotient step.",
    "The Set L baseline in the case study uses a single GPT-4 sample at temperature 0, which is a weak LLM baseline. The later 2-vendor × 5-temperature ensemble (§5.2) is stronger but is not used in the case study comparison.",
    "Several references to supplementary materials (S1-S12) are not independently verifiable at review time. The SHA-256 hash is 'to be added in the camera-ready version.'",
    "The cost comparison in Table 8 (tab:gen-cost) reports '≈10h A_P distillation' for NOETHER vs 'none after harness setup' for GenMorph, but the 10h figure is for a single program family and the amortisation argument across same-algebra SUTs is not quantified.",
    "The paper cites 'four further pattern-catalogue or MR-grammar candidates raised in peer review (Hu et al. 2019; Mariani 2018; Liu et al. 2020; Lin 2020) [that] could not be located' — this is unusual in a submission and suggests incomplete literature search."
  ],
  "questions_to_authors": [
    "Can you provide a single concrete example where the algebra-induced MR space MR(A_P) includes an MR that a practitioner would not have identified without the framework, and that MR detects a real fault? The current evaluation does not clearly demonstrate this.",
    "Theorem 1 quantifies over MR(A_P) as defined by Definition 7, which is exactly the Translate-image of A_P. How is this theorem different from the statement 'CONSTRUCT-MP's output covers CONSTRUCT-MP's input space'? What would a counterexample to Theorem 1 look like?",
    "The IBT's linear fault model (Definition 8) covers L = L* + Δ. What fraction of real faults in scientific computing, ML, or database systems are accurately modelled as linear operator perturbations? Can you provide any quantitative estimate?",
    "For the L*-blindness prediction: the prediction is that homogeneity-preserving mutators are invisible to homogeneity-testing MRs. This is essentially a mathematical identity. What is the scientific value of empirically confirming it, beyond verifying that the implementation is correct?",
    "The paper claims 'structural transferability at the algebra-skeleton level.' What concrete evidence would falsify this claim? If the framework can always add a 'ninth block' for recalcitrant cases, is the claim falsifiable at all?"
  ]
}
```

---

## Detailed Reviewer Report

### Summary

This paper proposes NOETHER, a framework that derives MetaPatterns from the operator-algebraic structure of program families. The framework has two layers: an upstream empirical layer where a domain expert curates an operator algebra A_P and its decomposition into eight structural blocks, and a downstream mechanical layer (CONSTRUCT-MP) that derives a MetaPattern set with closure and decidability guarantees. The paper's substantive theoretical contributions are the Invariance-Blindness Theorem (characterizing the detection kernel of symmetry/self-adjoint MRs) and the falsification of an absolute-completeness conjecture on the PWR core diffusion algebra. The empirical evaluation includes a small-scale case study, a pre-registered L*-blindness prediction, head-to-head comparisons with GenMorph and METRIC+, and several pilots.

### Strengths

**1. The Invariance-Blindness Theorem is the paper's strongest contribution.** It provides a precise characterization of what algebra-derived MRs cannot detect, converting the by-construction closure of Theorem 1 into a falsifiable, non-tautological statement. The proof structure is clean: the sufficient direction (⊇) is by definition, the necessary direction (⊆) uses faithfulness, and the Reachability Lemma ensures faithful witnesses exist under finite fault-dimensionality. The corollaries on single-block incompleteness and differential-oracle complementarity are practically useful and well-derived. This theorem is what lifts the framework from a taxonomic exercise to a theory with predictive content.

**2. The PWR negative result is carefully argued.** The two counterexamples (ρ_nonadd and ρ_MTC-bor) are regulatory-essential MRs, not contrived edge cases. The proof by block exhaustion is thorough, and the five identified structural obstructions in Translate's signature are concrete and actionable. This is one of the more honest negative results I have seen in a software-testing paper — the authors identify precisely where their framework fails and why.

**3. The L*-blindness prediction is a model of pre-registered falsifiability.** The prediction is derived ex-ante from public information (the framework's structure + PIT's published mutator semantics), committed to git before the data was inspected, and confirmed on 5/6 SUTs. The outlier (hypotSig) is explained by homogeneity-breaking mutators. While the prediction is essentially a mathematical identity, the discipline of pre-registration and honest reporting is commendable.

**4. The deflationary direction (§5.4) is a non-circular contribution.** Showing that inductive catalogues may over-count patterns (e.g., the sorting library where 5 inductive patterns compress to 2 algebraic ones) does not depend on the potentially circular curation of T* and T* blocks from reactor physics. This is the framework's most practically relevant contribution.

### Publication Blockers

**Blocker 1: Theorem 1 is near-tautological and presented as a primary contribution.**

Theorem 1 states that every ρ ∈ MR(A_P) is assigned to some m ∈ M(A_P). But MR(A_P) is defined (Definition 7) as exactly the set of MRs reachable through Translate from a single block invariant, and CONSTRUCT-MP explicitly enumerates all blocks and all invariants. The theorem is therefore a well-formedness statement about the construction's own output space. The authors acknowledge this in a candid passage, but Theorem 1 is still listed as contribution C2a, framed as converting "an empirical-adequacy claim into a structural-adequacy obligation," and used to justify the framework's downstream layer.

The problem is that the "structural-adequacy obligation" is vacuous: it says "every Translate-reachable MR is assigned to a MetaPattern," which is true by construction. The obligation would be substantive only if MR(A_P) were defined independently of Translate — for example, as "every MR that a domain expert would recognize as algebraically grounded." The paper's Theorem 1' (absolute completeness over arbitrary A_P properties) would be such a non-circular statement, but it is falsified.

**What a revision must do:** Either (a) demote Theorem 1 from a primary contribution to a structural-adequacy lemma and reframe the paper's theoretical contribution around the IBT and the negative result, or (b) define MR(A_P) in a way that is independent of Translate and prove closure against that independent definition. Option (a) is more realistic and would result in a stronger, more honest paper.

**Blocker 2: The empirical evaluation does not demonstrate practical utility.**

The evaluation has three arms, each with a critical weakness:

- **Case study (n=20, 1 model):** The mutation set is constructed to cover one defect category per non-empty block, so the 5/5 unique-detection result for cat-(iv) is construct-validity-controlled by design. The authors are transparent about this, but it means the result demonstrates that ρ_train-rev detects gradient-reversal faults (which it was designed to detect) rather than that NOETHER-derived MRs are superior to alternatives.

- **Head-to-head vs GenMorph:** Set N is dominated by Set G on the D1 stratum (26/52 vs 37/52, McNemar p=0.019). The authors reframe this as "per-block complementarity," but the aggregate verdict is clear: on the algebra-disrupting stratum where Set N should have an advantage, it is outperformed by a GP baseline.

- **METRIC+ comparison:** The Path A results show near-parity (McNemar p=0.625), but the Java subjects are re-implementations by the same author who designed NOETHER, creating a construct-validity confound. The Major cross-tool replication (p=0.211) is more convincing but shows bidirectional per-subject asymmetries rather than NOETHER superiority.

The L*-blindness prediction, while methodologically excellent, confirms a mathematical fact: homogeneity-preserving mutators are invisible to homogeneity-testing MRs. This is a consistency check, not evidence of testing effectiveness.

**What a revision must do:** Provide at least one empirical result where NOETHER-derived MRs detect real faults that existing approaches miss, on a substrate not constructed to favor the framework. The real-bug evaluation protocol (§5.1, currently a protocol only) would be the natural source of such evidence. Alternatively, demonstrate that the framework's MRs provide equivalent fault detection at substantially lower cost (human effort, computation, or both) on a substrate large enough for statistical inference.

### Major Weaknesses (Fixable)

**1. The upstream layer is unautomated and may not reduce the inductive burden.** The framework requires a domain expert to distill A_P from program semantics — a task that requires both domain knowledge and operator-algebraic literacy. The paper does not provide evidence that this is easier or more reliable than identifying MRs directly. A controlled study or even a detailed worked example comparing the two processes would address this.

**2. The IBT's scope is narrow.** The theorem covers only G and T* blocks under a linear fault model. Real faults in scientific computing (e.g., wrong boundary conditions, incorrect material properties), ML (e.g., architecture bugs, training-loop errors), and database systems (e.g., incorrect query rewriting, wrong join ordering) are rarely linear operator perturbations. The paper should either extend the IBT to additional blocks via linearization or other techniques, or provide quantitative evidence that the linear fault model covers a meaningful fraction of real faults.

**3. Circularity in "prediction" claims.** The T* and T* blocks were curated from reactor physics, so "predicting" m_adj and m_rev on reactor physics is circular. The authors acknowledge this candidly, but the abstract and contributions list still use "prediction" language. The deflationary direction is genuinely non-circular but is demonstrated on only three cases.

**4. Excessive length and defensive framing.** The paper contains at least four "boundary of contribution" boxes, extensive pre-emptive caveats, and repeated restatements of scope. This makes the paper difficult to read and suggests insecurity about the claims. A TOSEM paper should state its contributions confidently and let the evidence speak; the current defensive posture undermines the real contributions (IBT, negative result, L*-blindness prediction).

**5. Inter-rater agreement relies on LLMs.** The κ values (0.857 for the supplementary-MR audit, 1.000 for the Set N audit) are from LLM panels (DeepSeek, ChatGPT, Claude) with shared training data. The authors acknowledge this, but the breadth claims (94.4% subsumption, etc.) rest on these potentially inflated agreement figures. At least a small human expert validation would strengthen these claims substantially.

### Threats to Validity

**Construct validity:** The case-study mutation set is constructed to favor the framework. The METRIC+ Java subjects are re-implementations by the framework's designer. The inter-rater labels are from LLMs with shared training data. These three construct-validity threats compound: the breadth, depth, and comparative claims all rest on evaluation instruments that may be biased in the framework's favor.

**Internal validity:** The L*-blindness prediction's outlier-handling rule was "codified in the pre-registration config on 2026-05-15" but the analysis "had relied in implicit rather than written form." This is a minor but real concern about post-hoc rationalization of the outlier. The authors' transparency is appreciated, but the rule should have been explicit before the analysis.

**External validity:** The framework applies only to programs with explicit operator-algebraic structure, which excludes large classes of software (web applications, distributed systems, RLHF reward models, etc.). The 10-SUT substrate is concentrated on a single codebase. The cross-codebase pilot (n=3 SUTs, 77 mutants) is too small for generalization.

**Conclusion validity:** The case study's denominator (20 mutations, 1 model) is too small to characterize performance distributions. The head-to-head (n=62) is underpowered for the per-SUT comparisons claimed. The DeepCrime pilot (n=5) is underpowered for any inferential conclusion.

### What a Revision Must Do

1. **Demote Theorem 1** from a primary contribution to a structural-adequacy lemma. Reframe the paper's theoretical contribution around the IBT and the PWR negative result, which are genuine and non-circular.

2. **Provide one strong empirical result** demonstrating practical utility: either (a) NOETHER-derived MRs detecting real faults that existing approaches miss, on a non-constructed substrate, or (b) equivalent fault detection at substantially lower cost, with sufficient sample size for statistical inference.

3. **Cut the paper to roughly half its length.** Remove redundant boundary-of-contribution boxes, consolidate the empirical narrative, and move detailed proofs to an appendix. The IBT proof and the PWR falsification proof can remain; the rest should be streamlined.

4. **Drop "prediction" language** for T* and T* blocks on reactor physics. Reserve it for genuinely held-out cases.

5. **Address the upstream automation question.** Provide at least a worked example showing the step-by-step extraction of A_P, with comparison to the effort of identifying MRs directly.

6. **Validate at least one breadth claim with human experts**, not just LLM panels.

The core ideas — algebraic grounding of MetaPatterns, the IBT, the PWR negative result, the L*-blindness prediction — are interesting and worthy of publication. But the current manuscript overstates what Theorem 1 proves, understates how much the framework depends on unautomated expert input, and does not yet demonstrate practical advantages. A substantial revision addressing these issues could result in a strong TOSEM paper.