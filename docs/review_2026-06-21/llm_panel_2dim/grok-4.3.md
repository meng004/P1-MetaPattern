**JSON Block**

```json
{
  "overall_recommendation": "Major Revision",
  "reviewer_confidence_1to5": 4,
  "scores_1to5": {
    "soundness": 3,
    "novelty": 4,
    "significance": 3,
    "presentation": 4,
    "reproducibility": 4
  },
  "summary": "The manuscript presents NOETHER, a two-layer framework that derives MetaPattern equivalence classes for metamorphic relations (MRs) from the operator-algebraic structure of a program family. An upstream empirical decomposition into eight recurrent operator blocks (symmetry, order, self-adjointness, time-reversal, limits, qualitative dynamics, method comparison, relational equivalence) is fed to a downstream constructive algorithm CONSTRUCT-MP that produces a closed set of algebra-induced MR classes under Translate. The work is instantiated on Boltzmann reactor physics, equivariant ML, and relational query optimisers, reclassifies an earlier inductive PWR catalogue, falsifies a stronger absolute-completeness claim on PWR diffusion via two concrete counterexamples, and supplies an Invariance-Blindness Theorem characterizing detection kernels for the G and T* blocks within linear operator-implementation faults.",
  "strengths": [
    "The central methodological analogy to Noether's theorem (lifting induction from per-instance MRs to per-domain algebraic structure) is clearly articulated and shapes a coherent research programme (Introduction, §1).",
    "The negative result on PWR diffusion (§4.5, Appendix C.6) is technically rigorous, identifies five pairwise-independent obstructions in Translate's signature, and is supported by exhaustive per-block case analysis; this is a genuine theoretical contribution that prevents overclaiming completeness.",
    "The Invariance-Blindness Theorem (§3.4) supplies a non-tautological, falsifiable characterization of blind spots for linear faults; the finite-witness faithfulness lemma and three corollaries are cleanly proved and empirically corroborated on small linear instances (S10).",
    "Cross-domain transferability is demonstrated at the algebra-skeleton level on three structurally distinct families; the relational-equivalence block extends the framework beyond the Lie-group/self-adjoint/time-reversal core (§4.4).",
    "Reproducibility artefacts are extensive (Zenodo DOI, S1–S12, runner scripts, LRCA audit, pre-registered hypotheses); the supplementary material is unusually complete for a theory+empirical TOSEM submission."
  ],
  "publication_blockers": [
    {
      "section": "§1 (Contributions C2a–C2c), §4.5, Appendix C.6",
      "issue": "The paper repeatedly frames NOETHER as supplying a 'closure guarantee' and 'structural completeness' for MR identification, yet the negative PWR result shows that two standard safety-analysis MRs (non-additivity of rod-bank worth, second-order MTC-vs-boron dependence) lie outside MR(A_PWR) while being formulable over operators of A_PWR. The boundary between 'block sufficiency' (Hypothesis 7) and 'Translate sufficiency' is acknowledged only late and inconsistently; the abstract and introduction still imply a completeness result that the body falsifies.",
      "why_fatal": "This is a fatal soundness and significance blocker. A framework whose central claim is algebraic derivation of MetaPatterns cannot simultaneously advertise closure while exhibiting concrete, regulatorily-relevant MRs that escape the derivation. The gap between the promised 'no-drop closure invariant' (Theorem 1) and the actual Translate-bounded scope (Remark 4, Definition 5) must be stated in the abstract, introduction, and contribution list before any revision can be considered publishable."
    },
    {
      "section": "§5.2 (DeepCrime-style pilot), §6.3 (L*-blindness), Table 7",
      "issue": "The L*-block blindness prediction is presented as the 'central empirical claim' and 'falsifiable quantitative prediction', yet the pilot (n=5) and the Java head-to-head (n=62 post-exclusion) are underpowered for the statistical tests reported (McNemar exact p-values on discordant counts <25). The mutation set for the EGNN case study was explicitly constructed to cover one defect category per non-empty block, turning the 5/5 unique-detection result for ρ_train-rev into construct-validity confirmation rather than evidence of superiority. The paper acknowledges this in one paragraph but continues to cite the numbers as 'supporting the operative-mechanism reading'.",
      "why_fatal": "Empirical software engineering at TOSEM requires that pilot-scale or construct-biased experiments not be sold as primary evidence. The L*-blindness result on the six SUTs (2/44 kills, 5/6 zero) survives, but the statistical framing, p-values, and 'corroborating per-block patterns' paragraphs must be removed or rewritten as purely descriptive before the empirical sections can support the theoretical claims."
    }
  ],
  "major_weaknesses": [
    {
      "section": "§3.1–3.3 (operator algebra and Translate definitions), Remark 6",
      "issue": "The upstream empirical status of Hypothesis 7 (eight-block sufficiency) is stated clearly, yet the paper never supplies a falsification protocol or a concrete procedure by which a new program family would be shown to require a ninth block. The six out-of-scope families in Remark 9 are listed, but only metric-stability receives a Translate-template sketch; the others remain rhetorical.",
      "suggested_fix": "Add an explicit falsification procedure (e.g., 'apply the eight-block classification to the governing equations; any operator that cannot be assigned triggers a candidate-ninth-block review') and a worked example on one of the six families (e.g., label-consistency on a supervised classifier). Move the metric-stability block proposal from the appendix into the main text with its Translate template and closure proof. This turns the empirical hypothesis into a testable claim."
    },
    {
      "section": "§4.6 (Invariance-Blindness Theorem), Remark 14",
      "issue": "The theorem is proved only for linear operator-implementation faults and for the G and T* blocks; the three corollaries are stated unconditionally. The scope remark (R1–R4) appears only after the theorem and corollaries, and the empirical evidence (S10) uses N=8 linear systems. The claim that 'completeness requires oracle families with trivial joint kernel' is therefore overstated for the general nonlinear or non-G/T* case.",
      "suggested_fix": "Restrict the three corollaries to the linear fault class and the two blocks for which the theorem is proved. Add an explicit 'extension to nonlinear faults is future work' paragraph. Re-run the faithfulness check on at least one nonlinear SUT (e.g., a small neural net) to demonstrate that the sufficient direction still holds even when the necessary direction fails."
    },
    {
      "section": "§6 (Experiments), §6.4 (head-to-head), Table 8",
      "issue": "The per-block head-to-head is the correct analytical lens, yet the paper still reports an aggregate D1 McNemar p=0.019 that mixes in-scope and out-of-scope strata and overstates Set-G dominance. The cost-axis claim (H3a.3) is sound but is buried under detection-rate language. The LLM-ensemble baseline (Set L) is a 2-vendor × 5-temperature sample that subsumes only part of the cited SOTA LLM work; the third-vendor replication is 'committed as follow-up'.",
      "suggested_fix": "Remove the aggregate D1 McNemar test or label it explicitly as 'scope-mismatched auxiliary'. Promote the per-block table and the cost-axis paragraph to the primary reading. Either run the third-vendor LLM arm or drop the claim that the current ensemble subsumes Shin, Zhang, GPTMR, and AutoMT. Update the 'three-SOTA-category protocol' language to reflect what was actually executed."
    }
  ],
  "minor_issues": [
    "The title uses 'Metamorphic Pattern Identification' while the abstract and body consistently use 'MetaPattern'; standardize terminology.",
    "Figure 1's upstream layer is labelled 'empirical hypothesis' yet the downstream theorems are presented as if the hypothesis has been proved; the boundary box on p. 9 is clearer but appears too late.",
    "The LRCA multi-LLM audit (κ=0.931) is useful but the shared pre-training caveat is mentioned only once in §5.2; repeat the limitation when the κ value is first cited.",
    "Some supplementary references (S4 future_work.md item counts, S9 migrated appendices) are cited before they are defined; reorder or inline the first-use definitions.",
    "The 'no-drop closure invariant' phrasing in C2a is misleading given the later negative result; replace with 'no-drop closure over the Translate-image'.",
    "Table 5's 'unmapped' row is a lower-bound caveat on per-block denominators yet is included in the D1 aggregate row; clarify or remove from the aggregate.",
    "The abstract claims 'broader and more explainable MR class / MetaPattern design space' but the evaluation never measures explainability or maintenance cost; either drop the claim or add a qualitative readability study."
  ],
  "questions_to_authors": [
    "Given that two regulatorily-essential PWR MRs escape the Translate derivation, do the authors still claim that NOETHER supplies a 'structural source' for MetaPatterns, or only for a Translate-bounded subset? How should a practitioner decide whether a desired MR is inside or outside the framework before investing in interface instrumentation?",
    "The metric-stability block is the only ninth-block candidate given a concrete Translate template. Why was it not promoted to the canonical decomposition, and what empirical threshold would trigger its inclusion?",
    "The paper treats the upstream distillation of A_P as a permanent human task. What would a minimal viable LLM-assisted operator-extraction pipeline look like, and which of the six out-of-scope families in Remark 9 would it be most likely to mis-classify?",
    "The Invariance-Blindness Theorem is proved only for linear faults on G and T*. Can the authors supply a non-linear counter-example (e.g., a small ReLU network) that would falsify the 'structure-preserving = undetected' claim outside the linear regime?",
    "The head-to-head uses a hand-constructed mutation set biased toward one defect per block. Would the authors be willing to replace the EGNN case study with the pre-registered DeepCrime real-fault protocol (or the full 38-D4J extension) as the primary empirical evidence before acceptance?"
  ]
}
```

**Detailed Free-Form Reviewer Report**

**Summary of contribution (anchored).**  
The manuscript proposes NOETHER, a layered framework whose upstream layer curates a program-family operator algebra A_P and decomposes it into eight recurrent blocks (G, O_≤, T*, …, B*_rel). The downstream algorithm CONSTRUCT-MP extracts block invariants, translates them into MR families, quotients by structural equivalence, and returns a MetaPattern set M(A_P) that is closed under Translate over the algebra-induced MR space (Theorem 1, §3.3). Polynomial-time constructibility is proved when A_P admits a finite generating set (Theorem 2). The work is instantiated on Boltzmann reactor physics (§4.1), equivariant ML (§4.2), and relational query optimisers (§4.3); a negative PWR diffusion case (§4.5, Appendix C.6) falsifies a stronger absolute-completeness conjecture by exhibiting two standard safety-analysis MRs that escape Translate; an Invariance-Blindness Theorem (§3.4) characterises the linear-fault detection kernel for the G and T* blocks. Empirical material compares operator-block coverage against expert PWR sets, contrasts origin/boundary explanation with search-based and LLM baselines, and supplies a small EGNN case study plus a DeepCrime-style pilot.

**Strengths (concrete, section-anchored).**  
- The methodological move from inductive catalogues to algebraic derivation is cleanly motivated (Introduction, three foundational questions) and shapes every subsequent section.  
- The negative PWR result is the strongest theoretical contribution: two concrete, regulatorily-relevant MRs are proved outside MR(A_PWR) by exhaustive per-block exhaustion; the five pairwise-independent obstructions in Translate’s signature are explicitly enumerated (Table in §4.5). This prevents the paper from over-claiming completeness.  
- The Invariance-Blindness Theorem (§3.4) supplies a non-vacuous, falsifiable characterisation of blind spots for linear operator-implementation faults; the finite-witness faithfulness lemma and three corollaries are cleanly proved. The supplementary linear-algebra checks (S10) confirm that the witness sets used in the MR designs are unisolvent.  
- Cross-domain transferability is demonstrated at the algebra-skeleton level on three structurally distinct families; the relational-equivalence block exercises a part of the decomposition absent from the first two domains (§4.3).  
- Artefact quality is excellent: Zenodo DOI, full runner scripts, LRCA multi-LLM audit (κ=0.931 on Set-N block labels), pre-registered hypotheses, and per-mutant kill matrices make the empirical claims reproducible.

**Publication blockers (fatal).**  
1. **Over-claiming of closure and completeness (Introduction, C2a–C2c, §4.5, Abstract).**  
   The abstract promises a “broader and more explainable MR class / MetaPattern design space” and the contribution list advertises a “no-drop closure invariant”. Yet the negative PWR instantiation proves that two standard safety-analysis MRs (non-additivity of rod-bank reactivity worth, second-order MTC-vs-boron dependence of k_eff) lie outside MR(A_PWR) while being formulable over operators of A_PWR. The boundary between “block sufficiency” (Hypothesis 7) and “Translate sufficiency” is acknowledged only late (§4.5, Remark 6, Appendix C.6) and is never reflected in the abstract or contribution list. A framework whose central claim is algebraic derivation of MetaPatterns cannot simultaneously advertise closure while exhibiting concrete, regulatorily-relevant MRs that escape the derivation. This is a fatal soundness and significance blocker. The gap must be stated in the abstract, introduction, and contribution list before any revision can be considered publishable.

2. **Statistical over-interpretation of underpowered or construct-biased pilots (§6.2 case study, §6.3 L*-blindness, Table 7, DeepCrime pilot).**  
   The EGNN mutation set was explicitly constructed to cover one defect category per non-empty block of A_equi; the 5/5 unique-detection result for ρ_train-rev therefore exhibits construct validity rather than superiority. The L*-block blindness prediction is presented as the “central empirical claim”, yet the pilot (n=5) and the Java head-to-head (n=62 post-exclusion) are underpowered for the McNemar p-values reported. The paper acknowledges the bias in one paragraph but continues to cite the numbers as “supporting the operative-mechanism reading”. Empirical software engineering at TOSEM cannot treat pilot-scale or construct-biased experiments as primary evidence. The L*-blindness result on the six SUTs (2/44 kills, 5/6 zero) survives, but the statistical framing, p-values, and “corroborating per-block patterns” paragraphs must be removed or rewritten as purely descriptive.

**Major weaknesses (fixable).**  
- The upstream empirical status of Hypothesis 7 is stated but never operationalised as a falsification protocol. The six out-of-scope families in Remark 9 are listed; only metric-stability receives a Translate-template sketch. A concrete procedure (“apply the eight-block classification; any unassigned operator triggers a ninth-block review”) plus one worked example on, say, label-consistency for a supervised classifier is required.  
- The Invariance-Blindness Theorem and its corollaries are stated unconditionally, yet the proof and empirical evidence cover only linear faults on G and T*. The scope remark appears after the corollaries. Restrict the corollaries to the linear class or supply a nonlinear counter-example.  
- The head-to-head (§6.4) mixes in-scope and out-of-scope strata in the aggregate D1 McNemar test and buries the cost-axis claim. The LLM baseline is a 2-vendor × 5-temperature sample that does not fully subsume the cited SOTA LLM pipelines. Either run the third vendor or qualify the claim; promote the per-block table and cost-axis paragraph to the primary reading.  
- The LRCA multi-LLM audit (κ=0.931) and the supplementary-MR audit (κ=0.857) rely on LLM raters that share pre-training corpora. The limitation is mentioned once; it must be repeated whenever the κ values are cited, and a human inter-rater study should be committed.

**Minor issues.**  
- Terminology oscillation between “Metamorphic Pattern” (title) and “MetaPattern” (body).  
- Figure 1’s upstream layer is labelled “empirical hypothesis” while the downstream theorems are presented as proved; the boundary box on p. 9 is clearer but appears too late.  
- Some supplementary citations (S4 future_work.md item counts, S9 migrated appendices) are used before they are defined.  
- The “no-drop closure invariant” phrasing in C2a is misleading given the later negative result; replace with “no-drop closure over the Translate-image”.

**Recommendation and revision roadmap.**  
**Major Revision.** The theoretical core (operator-algebraic derivation, closure proof, negative PWR result, Invariance-Blindness Theorem) is sound and novel. The fatal blockers are (1) inconsistent framing of closure/completeness and (2) statistical over-interpretation of underpowered/construct-biased empirical material. A revision that (a) rewrites the abstract, introduction, and contribution list to reflect the Translate-bounded scope, (b) removes or re-labels all inferential statistics from the EGNN and DeepCrime pilots, (c) supplies an explicit falsification protocol for Hypothesis 7 plus one worked ninth-block example, and (d) promotes the per-block and cost-axis readings while qualifying the LLM baseline will bring the manuscript to TOSEM’s bar. The supplementary material is already of exceptional quality; the main text must be made consistent with it.

I am happy to re-review a revised version that addresses the two fatal blockers and the three major weaknesses listed above.