```json
{
  "overall_recommendation": "Major Revision",
  "reviewer_confidence_1to5": 4,
  "scores_1to5": {
    "soundness": 3,
    "novelty": 4,
    "significance": 2,
    "presentation": 2,
    "reproducibility": 3
  },
  "summary": "NOETHER proposes a two-level framework for metamorphic relation (MR) identification: an upstream layer that curates a program-family operator algebra decomposed into eight structural blocks, and a downstream layer (CONSTRUCT-MP) that mechanically derives MetaPatterns from those blocks with a closure guarantee (Theorem 1), polynomial-time decidability (Theorem 2), an Invariance-Blindness Theorem characterizing detection kernels (Theorem 3), and a falsified absolute-completeness conjecture on the PWR diffusion algebra. The framework is instantiated on three domains (Boltzmann reactor physics, equivariant ML, relational query optimisers) and evaluated on a small-scale mutation study, a head-to-head against GenMorph on 10 Java SUTs, and a DeepCrime-style pilot.",
  "strengths": [
    "The operator-algebraic framing of MR identification is genuinely novel: deriving MetaPatterns from the mathematical structure of the program family, rather than inducing them from observed MR corpora, is a principled departure from METRIC/METRIC+ and search-based methods.",
    "The Invariance-Blindness Theorem (Theorem 3, §3.4) is a substantive and non-trivial result: it characterizes the exact detection kernel of symmetry and self-adjoint block MRs as the structure-preserving faults, under a faithfulness condition that Lemma 1 shows is attainable. The corollaries on single-block incompleteness and differential-oracle complementarity are useful.",
    "The negative instantiation on the PWR core diffusion algebra (§4.6, Appendix C.6) is a genuine falsification of the stronger completeness conjecture (Theorem 1') with two well-motivated, safety-relevant counterexamples and five structurally independent obstructions in Translate's signature. This is honest and scientifically valuable.",
    "The L*-blindness prediction (§5.2) is a pre-registered, ex-ante falsifiable claim derived from public information, confirmed on 5/6 SUTs. This is the strongest empirical result in the paper.",
    "Cross-domain instantiation on three structurally distinct algebras (Boltzmann transport, equivariant ML, relational algebra) with the relational-equivalence block exercising a genuinely different algebraic skeleton is a convincing demonstration of transferability at the algebra-skeleton level."
  ],
  "publication_blockers": [
    {
      "section": "§3.2, Theorem 1 (Algebraic Closure)",
      "issue": "Theorem 1 is near-tautological. MR(A_P) is defined (Definition 12) as the Translate-image of A_P's block invariants, and CONSTRUCT-MP (Steps 1-4) enumerates all Translate-images. The theorem states that every element of this image is captured by the construction—i.e., the construction produces what it produces. The authors acknowledge this ('the closure result is by-construction within the explicit scope of Definition 12'), but the theorem is presented as the paper's central positive theoretical result (C2a) and is repeated in every Boundary-of-Contribution box.",
      "why_fatal": "A TOSEM paper's main theorem must have non-trivial content. Theorem 1 as stated adds no information beyond the definitions. The authors' defence—that it converts empirical adequacy into structural adequacy—fails because the structural adequacy is only over a space they define into existence. Either the theorem must be strengthened to cover a non-trivially larger MR space, or it must be honestly demoted from a theorem to a proposition or property, and the paper's contribution framing must be restructured around the IBT and the negative theory."
    },
    {
      "section": "§5.3, Table 9 (Head-to-head vs GenMorph)",
      "issue": "The head-to-head comparison shows NOETHER (Set N) is statistically dominated by GenMorph (Set G) on the D1 stratum (McNemar p=0.019) and pooled (p=0.0043). Set N kills 26/52 D1 mutants vs Set G's 37/52. The paper reframes this as 'per-block complementarity' and 'cost-axis advantage,' but the primary empirical finding is that algebra-derived MRs are less effective than GP-evolved MRs on this substrate. The paper's scope statement (§1) explicitly says it does not evaluate 'MR effectiveness in the sense of average fault-detection rate,' yet the head-to-head is presented as evidence.",
      "why_fatal": "The paper cannot simultaneously claim that MR effectiveness is out of scope and present head-to-head fault-detection numbers as evidence. If the comparison is retained, the dominance finding must be foregrounded honestly and the paper's claims must be reframed around what the comparison actually shows (cost-axis trade-offs and D2-stratum predictions), not around 'complementarity.' The current framing risks misleading readers about NOETHER's practical value relative to existing automated methods."
    }
  ],
  "major_weaknesses": [
    {
      "section": "§5.1, Table 4 (Case study)",
      "issue": "The case study uses 20 hand-constructed mutations on a single EGNN model (5,189 parameters). The authors acknowledge that mutations were 'constructed to cover one defect category per non-empty block,' making the 5/5 unique-detection result for cat-(iv) a construct-validity exhibit rather than evidence of effectiveness. The DeepCrime pilot (n=5) is underpowered with McNemar p=0.500.",
      "suggested_fix": "Expand the mutation set to at least 50 mutations drawn from multiple architectures (EGNN, SE(3)-Transformer, Vector Neurons) and use DeepCrime's full operator set rather than a 5-operator subset. Report detection rates with proper multiple-comparison correction. If resources do not permit this, explicitly label all empirical material as illustrative and remove any inferential claims."
    },
    {
      "section": "§3.1, Hypothesis 1 (Decomposition sufficiency)",
      "issue": "The eight-block decomposition is a by-inspection curation with no derivation from first principles. Six out-of-scope families are catalogued (Remark 3), and the authors honestly acknowledge the empirical status. However, the paper's theoretical contributions (Theorems 1-3) all depend on this decomposition, and there is no systematic method for determining when it is complete for a new program family.",
      "suggested_fix": "Develop at least one of the six candidate ninth blocks (e.g., metric-stability M_lip, which already has a Translate template in Remark 5) to full theorem-level status, demonstrating that the framework can be extended without breaking closure. Alternatively, provide a decision procedure that, given a program family, determines whether the eight blocks suffice."
    },
    {
      "section": "§4.3 (Reactor physics mapping) and §7 (Threats to validity)",
      "issue": "The 'prediction' of m_adj and m_rev is acknowledged as circular: the T* and T* blocks were partly curated from reactor-physics structures, and the derived MetaPatterns are then 'predicted' from those blocks. The deflationary direction (§5.5, PMCM worked example) is claimed to be non-circular, but it only shows that inductive catalogues over-count on simple program families (sorting, feedforward classifiers)—a result that does not require the full NOETHER apparatus.",
      "suggested_fix": "Apply NOETHER to a program family whose operator algebra was independently specified by a third party (not the authors), and show that the framework derives MetaPatterns not previously catalogued by that party. The committed external-transfer reactor-physics corpus (S4 item (j)) would address this; it should be completed before submission."
    },
    {
      "section": "§4.3 and §7 (Inter-rater reliability)",
      "issue": "The inter-rater agreement figures (κ=0.857 on the 18-MR audit, κ=1.000 on the Set N audit) are drawn entirely from LLM panels. The authors acknowledge this but still report the κ values as evidence. LLM raters share training corpora and are not independent domain experts.",
      "suggested_fix": "Conduct a human inter-rater reliability study with at least 3 domain experts (reactor physics and ML) on the MR-to-block assignments. Report human κ alongside the LLM κ. If human κ is substantially lower, revise the audit claims accordingly."
    },
    {
      "section": "Throughout (presentation)",
      "issue": "The paper is excessively long (~50 pages of LaTeX source) with extensive repetition. There are at least 4 'Boundary of contribution' tcolorboxes that repeat nearly identical information. Many paragraphs are devoted to hedging and caveat-stating that could be compressed. The 16-item committed-future-work list and multiple protocol descriptions for not-yet-executed experiments inflate the paper without adding evidence.",
      "suggested_fix": "Reduce to 35-40 pages by consolidating all boundary-of-contribution statements into a single table, moving committed-future-work items to a supplementary file, and cutting or compressing the METRIC+ manual derivation (Table 12), the PMCM worked example (§5.5), and the extensive statistical-protocol descriptions for not-yet-run experiments."
    },
    {
      "section": "§3.2, Theorem 2 (Decidability)",
      "issue": "The complexity bound O(n · max_i t_i · log n) assumes |I_s| = O(n) per block, i.e., each generator contributes O(1) invariants. This is not proven in general. For finite groups, |I_G| could be superlinear in the number of generators. The proof's Step 3 (union-find on equivalence classes) assumes the number of invariants is linear in n, which may not hold.",
      "suggested_fix": "Either prove that |I_s| = O(n) for each block under the stated assumptions, or revise the complexity bound to explicitly include |I_s| as a parameter. Clarify that the bound holds under a per-block invariant-count assumption, not just the finite-generating-set assumption."
    }
  ],
  "minor_issues": [
    "The paper references 'four further pattern-catalogue or MR-grammar candidates raised in peer review (Hu et al. 2019; Mariani 2018; Liu et al. 2020; Lin 2020) could not be located.' This is unusual in a submission and suggests the paper has been previously reviewed; the authors should either locate and cite these or remove the mention.",
    "The DeepCrime pilot (Table 3) reports Wilson 95% CIs but the sample size (n=5) makes these intervals too wide to be informative. Consider reporting only the point estimates with an explicit 'underpowered' label.",
    "Table 5 (PIT mutator × NOETHER block compatibility) uses '∼' (case-dependent) for 11 of 56 cells without specifying how the SUT-specific overrides are determined. The override files are referenced but not described.",
    "The Set L ensemble (§5.3) uses DeepSeek-V3 and ChatGPT-4o-mini, which are not the strongest available LLMs for code generation. The paper should justify this choice or note it as a limitation.",
    "The paper's title invokes Noether's theorem but the connection is explicitly disclaimed ('We do not invoke it as a theorem about programs'). Consider a less loaded title or strengthen the methodological analogy.",
    "§3.1 defines the program-induced operator algebra as (O, ∘, ∼_F) but ∼_F is never used in any proof or construction. If it is not needed, remove it; if it is, show where it enters.",
    "The canonical-block ordering (Definition 13) places B*_rel last because 'rewriting equivalences typically depend on the program family's input-perturbation, order, and method-comparison structure.' This is a heuristic justification, not a mathematical one. The ordering affects Theorem 1's uniqueness claim."
  ],
  "questions_to_authors": [
    "Can you state Theorem 1 in a form that does not quantify over a set defined as the Translate-image? For instance, can you characterize MR(A_P) independently of Translate and then prove closure?",
    "The head-to-head shows Set N is dominated by Set G on D1 (p=0.019). If the paper's contribution is not fault-detection superiority, why include the head-to-head at all? Would the paper be stronger without it?",
    "You acknowledge that the T* and T* blocks were partly curated from reactor physics. Can you identify any MetaPattern that NOETHER derives from a block NOT motivated by the domain on which it is instantiated? The equivariant-ML m_adj and m_rev are derived from blocks curated from physics, not ML.",
    "The L*-blindness prediction (§5.2) is the strongest empirical result. Could this be elevated to the paper's central empirical claim, with the head-to-head demoted to supplementary material?",
    "What is the minimum sample size needed to confirm the D2-stratum prediction (kill rate ≤ 10%) at α=0.05? The current n=5 gives a Wilson upper bound of 0.434.",
    "The Complexity bound in Theorem 2 assumes |I_s| = O(n). Is this assumption stated anywhere? If not, should the theorem's statement include it as a hypothesis?"
  ]
}
```

## Detailed Reviewer Report

### Overview

NOETHER proposes to replace inductive MetaPattern catalogues with algebraically derived ones, using an operator-algebra decomposition of program families into eight structural blocks. The downstream construction (CONSTRUCT-MP) maps block invariants to MetaPattern equivalence classes via a Translate operator, with claimed closure (Theorem 1), polynomial-time decidability (Theorem 2), and a detection-kernel characterization (Theorem 3, Invariance-Blindness). The framework is instantiated on three domains and evaluated on a small mutation study, a head-to-head against GenMorph, and a DeepCrime-style pilot.

The paper is ambitious, addresses an important problem (MR identification), and contains genuine theoretical content. However, it has two publication-blocking issues and several major weaknesses that must be resolved before it meets TOSEM's bar.

---

### Strengths in Detail

**1. Novel framing.** The idea of deriving MRs from the operator-algebraic structure of the program family—rather than inducing MetaPatterns from observed MR corpora—is a principled and original departure from METRIC/METRIC+ (category enumeration) and search-based methods (MR-Scout, GenMorph, LLM-assisted). The three foundational questions (origin, closure, transferability) are well-motivated.

**2. The Invariance-Blindness Theorem.** Theorem 3 (§3.4) is the paper's strongest theoretical contribution. It characterizes the detection kernel of G-block and T*-block MRs as exactly the structure-preserving faults, under a faithfulness condition whose attainability Lemma 1 establishes. The corollaries (single-block incompleteness, trivial-joint-kernel requirement, differential-oracle complementarity) are non-trivial and practically useful. The restriction to the linear fault class is honestly stated (Remark 8, R1–R4).

**3. The negative instantiation.** §4.6 and Appendix C.6 falsify the stronger completeness conjecture (Theorem 1') on the PWR core diffusion algebra using two safety-relevant MRs (non-additivity of rod-bank reactivity worth, second-order mixed k_eff dependence on T_mod and C_B). The five structural obstructions in Translate's signature are well-identified and the per-block exhaustion proofs are thorough.

**4. The L*-blindness prediction.** §5.2 derives a quantitative, falsifiable prediction from public information (NOETHER's framework + PIT's mutator specification) and confirms it on 5/6 SUTs. The pre-registration in git and the ex-ante derivability argument are commendable. This is the paper's strongest empirical result.

---

### Publication Blockers

**PB1: Theorem 1 is near-tautological.**

Theorem 1 (Algebraic Closure under Translate) states that for every ρ ∈ MR(A_P) (Definition 12: the set of MRs reachable as Translate(ι, s) for some block s and invariant ι), there exists a unique m ∈ M(A_P) such that ρ ∈ m. But M(A_P) is constructed by CONSTRUCT-MP, which (Step 2) forms R(ι) = {ρ : ρ = Translate(ι', s), ι' ∼_s ι} and (Step 3) sets m_{s,[ι]} = R(ι). So the theorem says: every MR produced by Translate is in the MetaPattern that CONSTRUCT-MP constructs from Translate's output. This is true by construction.

The authors acknowledge this in the text following Remark 4 ("A sceptical reading might object that the by-construction status of Theorem 1 makes it near-tautological"). Their defence is that the theorem "converts an empirical-adequacy claim into a structural-adequacy obligation." But the structural adequacy is only over MR(A_P), which is defined as the Translate-image. The theorem provides no information about whether MR(A_P) is a meaningful or interesting space—it could be empty, or it could be a tiny subset of all relevant MRs. Indeed, §4.6 shows that two important PWR safety MRs are outside this space.

**What a revision must do:** Either (a) redefine MR(A_P) independently of Translate (e.g., as all MRs formulable as first-order properties over A_P's operators) and prove that Translate reaches all of them, or (b) demote Theorem 1 to a Proposition/Property and restructure the paper's contribution claims around the IBT (Theorem 3) and the negative theory (§4.6). Option (b) is more feasible and would result in a more honest paper.

**PB2: The head-to-head shows NOETHER is dominated by GenMorph, but the paper frames this as evidence.**

Table 9 (§5.3) reports Set N (NOETHER) kills 26/52 D1 mutants vs Set G (GenMorph) kills 37/52, with McNemar p = 0.019. Pooled over D1∪D2, Set N kills 26/57 vs Set G's 40/57 (p = 0.0043). NOETHER is statistically dominated.

The paper's scope statement (§1) says: "It does not evaluate MR effectiveness in the sense of average fault-detection rate, mutation score, or general defect-revealing superiority." Yet §5.3 presents fault-detection numbers as evidence, reframing the dominance as "per-block complementarity" and "cost-axis advantage."

This is internally contradictory. If fault-detection is out of scope, the head-to-head should not be presented as evidence. If it is in scope, the dominance finding must be foregrounded, not buried under per-block decomposition and cost-axis reframing.

**What a revision must do:** Choose one framing and stick with it. If the paper is about MR identification (not effectiveness), remove the head-to-head from the main text and relegate it to supplementary material, or present it as a pure cost-axis comparison without detection-rate claims. If fault-detection is part of the evaluation, the dominance finding must be the headline result, not "complementarity."

---

### Major Weaknesses in Detail

**MW1: Underpowered and construct-biased empirical evaluation.**

The main case study (§5.1, Table 4) uses 20 hand-constructed mutations on a single 5,189-parameter EGNN model. The authors acknowledge that mutations were "constructed to cover one defect category per non-empty block of A_equi," making the cat-(iv) 5/5 unique-detection result a construct-validity exhibit. The DeepCrime pilot (n=5, Table 3) has McNemar p = 0.500 and is acknowledged as "underpowered for an inferential conclusion." The cross-codebase commons-math pilot (n=77 mutants, 3 SUTs) is described as "underpowered for α=0.05 hypothesis testing."

The paper's empirical evidence thus consists of: one constructed mutation set (biased by design), one pilot (n=5, non-inferential), one L*-blindness test (n=44, the strongest result), one head-to-head (n=57, shows NOETHER is dominated), and one cross-codebase pilot (n=77, underpowered). This is insufficient for a TOSEM methods paper claiming a framework-level contribution.

**MW2: Circularity in "prediction" claims.**

The authors acknowledge (§4.3, "A note on prediction") that the T* and T* blocks were "partly induced from reactor-physics structures" and that m_adj and m_rev are then "predicted" from those blocks. The deflationary direction (§5.5) is claimed to be non-circular, but it only shows that simple program families (sorting, feedforward classifiers) have fewer non-empty blocks than the reactor-physics catalogue has rows—a result that follows from basic algebraic inspection without needing the full NOETHER apparatus.

**MW3: LLM-based inter-rater reliability.**

The κ = 0.857 (18-MR audit) and κ = 1.000 (Set N audit) are from LLM panels (DeepSeek, ChatGPT, Anthropic Claude). These models share substantial pre-training corpora and are not independent domain experts. The authors acknowledge this, but the κ values are still presented in the text as if they carry evidential weight. A human inter-rater study is "committed as follow-up" but is essential for the construct validity of the audit claims.

**MW4: Theorem 2's complexity bound has a hidden assumption.**

The proof of Theorem 2 assumes that the number of invariants |I_s| is O(n) (one per generator), but this is not stated as a hypothesis. For finite groups, the number of distinct invariants could be superlinear in the number of generators (e.g., if each pair of generators produces a distinct joint invariant). The complexity bound should either include |I_s| as a parameter or prove that |I_s| = O(n) under the stated assumptions.

**MW5: Excessive length and repetition.**

The paper is approximately 50 pages of LaTeX source with at least four "Boundary of contribution" tcolorboxes repeating nearly identical information. Multiple paragraphs are devoted to describing protocols for not-yet-executed experiments. The 16-item committed-future-work list and the extensive METRIC+ manual derivation (Table 12) inflate the paper without adding evidence. A TOSEM paper should be self-contained; protocols for future work belong in a supplementary file.

---

### Threats to Validity

**Construct validity.** The mutation set in the main case study is designed to favor NOETHER (one defect category per block). The LLM-based κ values are not equivalent to human inter-rater reliability. The four Java subjects in the Path A comparison are re-implementations by the NOETHER framework's own author.

**Internal validity.** Theorem 1's uniqueness depends on the canonical-block ordering, whose justification is heuristic ("rewriting equivalences sit algebraically downstream"). The L*-blindness prediction's outlier-handling rule was "codified in the pre-registration config on 2026-05-15"—after the hypotSig analysis had "relied in implicit rather than written form" on it, which weakens the pre-registration claim.

**External validity.** The 10 SUTs are from a single codebase (MathSignalClass + ComplexSignal). The reactor-physics corpus is the authors' own. The equivariant-ML case study uses a compact EGNN stand-in, not a production architecture. Six program-family classes are catalogued as out-of-scope, but there is no systematic method for determining scope membership.

**Conclusion validity.** The denominators (n=20, n=5, n=57, n=77) are below the thresholds needed for the claimed inferences. The Wilson CIs are wide and overlapping in most comparisons. The L*-blindness test (n=44) is the only adequately powered result, and it confirms a prediction rather than testing effectiveness.

---

### What a Revision Must Do

1. **Resolve PB1.** Demote Theorem 1 to a Proposition or Property; restructure the paper's contribution claims around the IBT (Theorem 3) and the negative theory (§4.6). If Theorem 1 is retained as a theorem, redefine MR(A_P) independently of Translate and prove a non-trivial closure result.

2. **Resolve PB2.** Choose a consistent framing: either remove fault-detection numbers from the main text (if effectiveness is out of scope) or foreground the GenMorph dominance finding honestly (if it is in scope).

3. **Expand the empirical evaluation.** The L*-blindness prediction is the strongest result; elevate it to the central empirical claim. Add at least one more pre-registered, falsifiable prediction at similar power. Expand the mutation set to ≥50 mutations across ≥2 architectures. Complete the DeepCrime evaluation at n ≥ 20.

4. **Conduct human inter-rater reliability.** Replace or supplement the LLM-based κ values with at least 3 human domain experts.

5. **Complete at least one external-transfer test.** Apply NOETHER to a program family whose operator algebra was independently specified, and show derivation of MetaPatterns not previously catalogued by that party.

6. **Cut the paper to 35-40 pages.** Consolidate all boundary-of-contribution statements into one table. Move committed-future-work items and unexecuted protocols to a supplementary file. Compress the METRIC+ manual derivation and the PMCM worked example.

7. **Fix Theorem 2's complexity statement.** Either prove |I_s| = O(n) or include it as a hypothesis.

8. **Address the circularity in prediction claims.** Either complete an independent transfer test or remove the "prediction" framing and use "re-classification" throughout.