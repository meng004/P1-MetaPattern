```json
{
  "overall_recommendation": "Major Revision",
  "reviewer_confidence_1to5": 4,
  "scores_1to5": {
    "soundness": 3,
    "novelty": 4,
    "significance": 3,
    "presentation": 3,
    "reproducibility": 2
  },
  "summary": "The paper proposes NOETHER, a layered framework that derives metamorphic-test MetaPatterns from a program family’s operator algebra. Upstream, experts curate an algebra and an eight-block structural decomposition; downstream, an algorithm (CONSTRUCT-MP) generates MetaPatterns and a space of algebra-induced MRs, with a closure theorem (by-construction) and a decidability bound, and a new Invariance-Blindness Theorem characterizing blind spots for symmetry and self-adjoint blocks. The framework is instantiated on reactor physics, equivariant ML, and relational optimizers; a stronger completeness conjecture is explicitly falsified on PWR diffusion with two domain MR counterexamples.",
  "strengths": [
    "Clear, ambitious attempt to ground MR/MetaPattern discovery in operator-algebraic structure, with a coherent layered architecture (Fig. 1).",
    "Explicit scope delineation and honest treatment of limitations, including a negative result (Theorem 1' falsification on PWR) and explicit out-of-scope classes.",
    "Invariance-Blindness Theorem provides a non-tautological characterization of blind spots for symmetry/self-adjoint-based MRs under a linear-fault model.",
    "Multiple domain instantiations (reactor physics, equivariant ML, relational optimizers) that illustrate transfer at the algebra-skeleton level."
  ],
  "publication_blockers": [],
  "major_weaknesses": [
    {
      "section": "§3.2–§3.3 (Definitions 3–5, Theorem 1, Remark 3)",
      "issue": "The Algebraic Closure Theorem is essentially tautological because MR(𝒜_P) is defined as the image of Translate from a single block; closure then follows by definition rather than substantive proof.",
      "suggested_fix": "Reframe the theorem to emphasize what is nontrivial (e.g., uniqueness under canonical-block ordering) and move the core value to the Invariance-Blindness result. Alternatively, strengthen the result by proving closure for a richer class of derivations (e.g., a compositional or higher-order Translate) beyond the single-block, first-order templates."
    },
    {
      "section": "§3.2 (Definitions 3–5), Appendix A/Table of Translate templates",
      "issue": "Translate and per-block invariant extraction are under-specified at an algorithmic level (especially for infinite/Lie groups and qualitative-dynamics). Complexity claims in Table 1 rely on informal regime-dependent bounds (e.g., O(|G|^2), O(d_G^2)) without precise algorithms or termination criteria.",
      "suggested_fix": "Provide concrete, implementable procedures for each block (including tuple-generation, canonical orders, and equivalence checks), with proofs of correctness and explicit complexity analyses. For Lie groups, give a constructive basis and demonstrate how finite witness sets are constructed without sacrificing correctness."
    },
    {
      "section": "§3.4 (Invariance-Blindness Theorem) and §5.5 (E1–E3)",
      "issue": "IBT hinges on a ‘faithfulness’ condition but does not provide a constructive method to compute faithful finite witness sets in practice, nor bounds on their size beyond linear-algebra existence.",
      "suggested_fix": "Provide an explicit algorithm with complexity bounds to construct faithful witness sets for G and T* in realistic settings, and report empirical success rates and sizes across representative SUTs. Clarify robustness under floating-point tolerances."
    },
    {
      "section": "§4 and §5 (Instantiations and Empirical Evaluation)",
      "issue": "Empirical support is fragmented and underpowered: the equivariant-ML case study uses 20 hand-constructed mutations with acknowledged construct-validity bias; the DeepCrime pilot is n=5; PIT experiments mix head-to-head with multiple caveats, and deferred comparisons (MR-Scout, broader METRIC+) are not completed.",
      "suggested_fix": "Consolidate a larger, unbiased evaluation: (i) execute the pre-registered MR-Scout and METRIC+ comparisons; (ii) extend DeepCrime real-faults beyond n=5 across multiple architectures; (iii) complete a head-to-head on a broader Java benchmark with stratified D1/D2 analysis; and (iv) report effect sizes and CIs with corrected multiple testing."
    },
    {
      "section": "§4.3 (Relational optimizers)",
      "issue": "The relational instantiation is largely analytical; no executable MR derivation and evaluation is shown for an actual optimizer (e.g., Calcite) within this paper.",
      "suggested_fix": "Integrate at least one executable MR evaluation tied to a query optimizer (e.g., run your B*_rel translations with QED/SPES over a subset of TPC-H queries), and report quantitative outcomes to demonstrate practicality and transfer beyond physics/ML."
    },
    {
      "section": "§3.5 and §4.5 (Negative instantiation and obstructions)",
      "issue": "While the PWR counterexamples are compelling, the claim that no single-block Translate can derive them depends on per-block exhaustion delegated to the appendix. Readers cannot fully assess correctness without more accessible proofs.",
      "suggested_fix": "Lift the essential parts of the per-block exclusion proofs for the two PWR MRs into the main text (with clear formal assumptions) and provide a concise but rigorous justification for each obstruction O1–O5. Consider adding a minimal counterexample demo script."
    },
    {
      "section": "Global: Upstream distillation (§1 Scope, §3.1 Remarks, §6.3)",
      "issue": "The framework critically depends on humans to curate 𝒜_P and its block decomposition; guidance on how to do this reproducibly is thin. This threatens external validity and reproducibility.",
      "suggested_fix": "Provide a concrete, repeatable protocol for algebra distillation on at least one domain (e.g., a worked end-to-end extraction from an open-source SUT), and quantify inter-rater agreement (humans, not only LLMs)."
    }
  ],
  "minor_issues": [
    "Over-reliance on supplementary material (S1–S12) for core arguments, tables, and proofs; bring key proofs/definitions into the main text.",
    "Excessive length and density; repeated caveats and nested tcolorboxes impede readability. Consider streamlining and moving secondary narratives to appendices.",
    "Notation inconsistencies (e.g., switching between T* and self-adjointness, sometimes conflating operators vs. programs); ensure consistent symbols and domains.",
    "Some complexity bounds (Table 1) are heuristic; clarify assumptions and formally define parameters (e.g., K truncation, d_G).",
    "The self-adjoint attention MR (§4.2.2) seems architecture-specific and may not be generally available; clarify required hooks and whether it applies beyond specific transformers.",
    "Clarify how canonical-block ordering deals with multi-block MRs without losing essential content (Remark 3.5 vs. compositional MRs in Appendix C.5.3).",
    "Citations to several works are broad; ensure all referenced datasets, tools, and scripts are publicly accessible upon submission or clearly marked as future work."
  ],
  "questions_to_authors": [
    "Translate and invariant extraction: Can you provide precise, implementable algorithms for each block (including Lie-group cases) and an example of a full Translate pipeline for one Java SUT and one ML SUT?",
    "Faithfulness construction: How should practitioners construct faithful witness sets for G and T* in practice? What witness set sizes do you observe across domains, and how sensitive are results to floating-point tolerances?",
    "Algebra distillation: What concrete procedure should a team follow to curate 𝒜_P from a codebase? Can you report human inter-rater agreement (not just LLM panels) on a held-out system?",
    "Relational instantiation: Can you execute B*_rel-derived MRs against a real optimizer (Calcite/QED/SPES) in this paper and report detection/false-positive rates, not only analytical mappings?",
    "Compositional MRs: Do you have a concrete design for a compositional Translate that could cover your PWR counterexamples while preserving decidability? If not, what minimal extensions would you prioritize?",
    "Evaluation completeness: When will the MR-Scout and broader METRIC+ comparisons be available, and can you include at least a partial run in the current paper to strengthen the empirical case?"
  ]
}
```

Detailed reviewer report

This is a highly ambitious and thoughtful paper that seeks to re-ground metamorphic testing in operator-algebraic structure. The idea of treating MetaPatterns as equivalence classes derived from algebraic invariants is original and potentially impactful, and the paper is unusually candid about scope and limitations. The negative result on PWR diffusion (falsifying a stronger completeness conjecture) and the Invariance-Blindness Theorem are valuable contributions that, if packaged more crisply and supported by stronger evidence, could help anchor a foundational thread in metamorphic testing.

That said, in its current form the submission overreaches in some areas and under-delivers in others. The formal core beyond definitions and design choices is limited: the closure theorem is essentially tautological given the definition of MR(𝒜_P) as the image of Translate; the decidability theorem is a lightweight complexity statement with informal per-block costs; and the Invariance-Blindness Theorem, while an interesting characterization, remains restricted to linear operator-implementation faults and relies on a non-constructive “faithfulness” assumption without a practical recipe. Empirical support is fragmented and often underpowered, with several promised comparisons deferred to supplementary materials or future work.

Below I expand on strengths, weaknesses, threats to validity, and concrete revision requirements.

Strengths

- Conceptual grounding: The layered decomposition (upstream block curation, downstream mechanical construction) is a compelling way to move MR design upstream. Figure 1 and §3 present a consistent architecture. The eight-block decomposition is plausible and covers a productive portion of algebraic structure encountered in numerics/ML/relational settings.

- Honest scoping and negative result: The paper explicitly distinguishes a tractable closure (over Translate-reachable, single-block MRs) from a false absolute-completeness claim (Theorem 1′). The PWR diffusion counterexamples (non-additive rod-bank worth and MTC-vs-boron mixed derivative) and the identification of five structural obstructions add substantive value by delineating limits.

- Invariance-Blindness Theorem (IBT): For G and T*, the tight kernel characterization under a linear-fault model and faithfulness is a useful, non-tautological result that turns closure into a practical statement about blind spots. The faithfulness rank checks (E1) and the MR-vs-differential complementarity (E2) are aligned with the theorem’s spirit.

- Cross-domain instantiation: Even if primarily analytical, the application to equivariant ML and relational optimizers indicates the generality of the approach beyond the authors’ native domain (reactor physics).

Major concerns and requested changes

1) Closure theorem as a near-tautology; Translate underspecified.

- As stated (Definition 5 and Theorem 1), MR(𝒜_P) is defined as Translate’s image from a single block invariant. Closure is then immediate. This is not, per se, a fault, but the result’s value lies in the rest of the framework (Translate design, canonical ordering, invariant extraction). Those parts are currently insufficiently specified.

Required: Either (a) reframe Theorem 1 more modestly and move the weight to IBT and the negative result, or (b) strengthen the result by extending Translate beyond first-order/single-block templates and proving a nontrivial closure. In either case, provide precise per-block Translate algorithms and correctness/complexity analyses.

2) IBT practicality hinges on faithfulness; provide constructive procedures.

- The existence proof via linear algebra is fine, but practitioners need a construction. Currently, §3.4 defines faithfulness and proves existence, and §5.5 (E1) shows a small-rank check. This is not enough to operationalize IBT or to claim its broader utility.

Required: Provide a concrete procedure to construct faithful witness sets for G and T* in practice, with complexity and observed sizes on representative systems. Discuss tolerance selection and robustness in floating-point arithmetic. Show IBT’s tight-kernel behavior in at least one substantive case study beyond toy matrices.

3) Translate and invariant-extraction algorithms need to be explicit.

- Table 1 gives time bounds but no algorithms. For Lie groups, the paper references O(d_G^2) on Lie-algebra bases; for infinite groups, a truncation K. Without precise algorithms, it is unclear how to implement Translate, ensure correctness, and interpret decidability claims.

Required: For each block, specify (i) how invariants are extracted from 𝒜_P, (ii) the canonical tuple generation, (iii) equivalence checks (~_s), and (iv) the practical algorithms (pseudocode or precise descriptions). For Lie groups, show how infinitesimal generators translate to finite tests; for qualitative-dynamics, define robust shape invariants and their extraction.

4) Empirical evaluation is incomplete and tailored.

- The equivariant-ML case study (20 hand-constructed mutants) and the DeepCrime pilot (n=5) are underpowered; you repeatedly acknowledge construct-validity design (e.g., cat-(iv) selected to showcase 𝒯*). The Java PIT head-to-head is more substantive but still limited and shows GP-based GenMorph outperforming overall (which you acknowledge). Several promised comparisons (MR-Scout, broader METRIC+) are absent or in supplementary materials.

Required: Consolidate a more substantial empirical section. At minimum: (i) complete at least one MR-Scout and one broader METRIC+ comparison; (ii) increase the DeepCrime real-fault sample size across multiple architectures; (iii) extend the Java benchmark and report D1/D2 stratified outcomes with proper multiple-testing correction. Clarify how many of the conclusions are pre-registered versus exploratory.

5) Relational instantiation lacks executable evidence.

- §4.3 maps to published equivalences but does not show an executable MR run against a real optimizer.

Required: Integrate an executable evaluation (e.g., construct MRs from B*_rel and test them with QED/SPES against a subset of TPC-H/Calcite), reporting detection and false-positive rates. This greatly strengthens the cross-domain transfer claim.

6) PWR counterexample proofs: move essential arguments into the main text.

- The negative result is central and good; however, the per-block exclusion is deferred to the appendix. Readers need to see the essence of why the two MRs cannot be obtained under single-block Translate, including the precise nature of obstructions O1–O5.

Required: Summarize the per-block exclusions concisely in the main text (one paragraph per obstruction) and provide a more accessible proof sketch. If possible, include a minimal executable script (or a pointer to one in the supplementary materials) that demonstrates the mismatched structure.

7) Upstream algebra distillation reproducibility.

- The framework’s main bottleneck is human curation of 𝒜_P. You suggest LLMs and informal procedures, but do not provide a replicable path.

Required: Provide a concrete, repeatable protocol for 𝒜_P extraction for at least one open-source SUT (e.g., a Java class from Commons Math), with annotation guidelines and (ideally) human IRR statistics (not only LLM panels). This is crucial for reproducibility and for readers to assess the cost of adopting NOETHER.

Minor issues

- Reduce dependence on supplementary materials for critical definitions, tables, and proofs. Ensure the main text is self-contained enough for a TOSEM audience to evaluate the core contributions without chasing multiple appendices.

- Streamline the narrative. Several tcolorboxes and reiterations of scope break flow and add length. Consider moving extended related-work contrasts and procedural caveats to appendices.

- Clarify notation: keep consistent use of T* for self-adjoint operators, G for symmetries, and avoid conflating operator algebra elements with program functions P.

- The self-adjoint attention MR (§4.2.2) seems strongly architecture-specific and to require probes/hooks; clarify generality and whether this is broadly applicable beyond particular transformer implementations.

- Canonical-block ordering: make explicit how assigning a multi-block MR to the highest-priority block preserves essential content and does not erase mixed-structure properties (you note this limitation; emphasize its consequences).

- Ensure all cited tools/datasets/scripts will be publicly available at review/acceptance time; currently many are promised but not verifiable.

Threats to validity

You devote significant space to threats, which is commendable. The most serious ones that currently weaken the case are:

- Construct validity: The small, tailored mutant sets and reliance on architecture-specific probes; LLM rater panels are not equivalent to human IRR.

- External validity: Heavy reliance on the authors’ own reactor-physics catalogues and self-authored Java SUTs; cross-team or independent corpora are largely absent.

- Conclusion validity: Underpowered pilots and multiple comparisons without corrected inferences in parts of the empirical sections.

What a revision must do

- Tighten and clarify the theoretical core: specify Translate algorithms and invariant extraction; reframe the closure theorem; provide constructive procedures for faithfulness; move key parts of the PWR counterexample proofs into the main text.

- Strengthen empirical evidence: complete at least one automated comparator (MR-Scout or broader METRIC+), expand DeepCrime real-faults, and include an executable relational evaluation. Report effect sizes and confidence intervals; correct for multiple comparisons where appropriate.

- Improve reproducibility: add a concrete, repeatable protocol for 𝒜_P distillation and demonstrate it on an independent open-source SUT; provide human IRR on algebra extraction.

- Streamline presentation and reduce over-dependence on supplementary materials for critical arguments.

Recommendation

Overall, I see a valuable, novel direction here, with several strong ideas (operator-algebraic grounding, IBT characterization, and explicit negative results). However, the current package mixes definitional theorems, incomplete empirical evidence, and underspecified algorithms. I recommend Major Revision. With tighter theory, practical algorithms, and stronger, more complete empirical support, this could become a high-impact TOSEM contribution.