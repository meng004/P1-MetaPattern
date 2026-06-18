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
  "summary": "The paper proposes NOETHER, a two-layer framework that derives metamorphic pattern (MetaPattern) sets from the operator-algebraic structure of program families: an upstream empirical layer curates an eight-block decomposition of the program-induced operator algebra, and a downstream mechanical layer (CONSTRUCT-MP) constructs MetaPatterns via a Translate operator. The paper proves an algebraic closure theorem (Theorem 1, acknowledged as by-construction), a polynomial-time decidability result (Theorem 2), and an Invariance-Blindness Theorem characterising the detection kernel of symmetry/self-adjoint MRs as exactly structure-preserving faults under a faithfulness condition. It falsifies a stronger absolute-completeness conjecture (Theorem 1') on the PWR core diffusion algebra with two concrete counterexamples, and reports empirical evidence from a small equivariant-ML case study, an L*-blindness prediction test on PIT mutants, and head-to-head comparisons against GenMorph and METRIC+.",
  "strengths": [
    "The Invariance-Blindness Theorem (§3.4) is a genuinely novel and non-trivial characterisation: it formalises the intuition that structural MRs are blind to structure-preserving faults, proves a finite faithful witness set exists (Lemma 1), and derives three informative corollaries (single-block incompleteness, trivial-joint-kernel requirement for completeness, differential-oracle complementarity).",
    "The falsification of Theorem 1' on A_PWR (§3.6, Appendix C.6) with two regulatory-essential PWR safety MRs is a well-motivated negative result. The per-block exhaustion proofs are detailed and the five identified Translate-extension dimensions are structurally informative.",
    "The L*-blindness prediction (§4.2) is a pre-registered, ex-ante falsifiable quantitative prediction derived from public information. Its confirmation on 5/6 SUTs with a mechanistic explanation for the outlier is the strongest piece of empirical evidence in the paper.",
    "The METRIC+ Path A comparison (§4.3, Table on Sun 2021 corpus, n=120 PIT mutants) reports a clean null result (McNemar p=0.625, 92.6% both-kill) that is honestly interpreted as complementarity rather than superiority.",
    "The framework's structural approach to MetaPattern derivation is novel relative to METRIC/METRIC+ (expert-curated categories) and automated pipelines (empirical search), and the three instantiations on structurally distinct algebras (Lie-group/physical, equivariant-ML, idempotent-semiring/relational) test the transfer claim at the algebra-skeleton level."
  ],
  "publication_blockers": [
    {
      "section": "§4.1 (Case study) and §4.1.1 (DeepCrime pilot)",
      "issue": "The primary empirical evidence for cross-domain utility is a case study with n=20 hand-constructed mutations on a single compact EGNN model (5,189 parameters), where the mutation set was explicitly constructed to cover one defect category per non-empty block of A_equi, and the headline 5/5 unique-detection result for cat-(iv) is acknowledged by the authors as exhibiting construct validity of ρ_train-rev rather than NOETHER's superiority. The DeepCrime pilot (n=5) is explicitly underpowered (McNemar p=0.500). No adequately powered real-fault evaluation has been executed; only a protocol is described.",
      "why_fatal": "For TOSEM, the empirical evaluation must provide at least one adequately powered comparative study on real or realistically-sourced faults that is not compromised by construct-validity bias. The case study's design circularity (mutations selected to match blocks, then blocks shown to detect them) and the pilot's acknowledged underpowering mean the paper's central utility claim— that NOETHER-derived MRs are useful for testing relative to alternatives—rests on structural-coverage diagnostics and the L*-blindness prediction alone, neither of which is a fault-detection efficacy claim. The committed-but-unexecuted protocols (§4.1 comparative evaluation, real-bug mining) are the studies that would address this, and their absence leaves the empirical contribution below TOSEM's bar."
    },
    {
      "section": "§4.2.6 (Head-to-head against GenMorph)",
      "issue": "Set N is dominated by Set G on the D1 stratum (McNemar p=0.019, n=52) and pooled (p=0.0043, n=57). The paper reframes this as 'per-block complementarity' and 'cost-axis advantage,' which is honest but means the framework's algebra-derived MRs detect fewer algebra-disrupting mutants than GP-evolved MRs on the only adequately sized head-to-head substrate. The per-block edge on G_tr (10/17 vs 8/17) is directional only with overlapping Wilson intervals. The n=57 denominator (reduced from 62 by LLM-judged equivalent-mutant exclusion) is underpowered for the fine-grained per-block claims made.",
      "why_fatal": "The head-to-head result, taken at face value, shows NOETHER's MRs are less effective at fault detection than the strongest baseline on the substrate where the framework should have an advantage (algebra-rich SUTs). The paper's reframing (per-block, cost-axis, D2-prediction) is legitimate but the aggregate dominance by Set G, combined with the underpowered per-block sub-samples, means the empirical case for NOETHER's practical utility over existing automated pipelines is not established. TOSEM requires that a framework claiming to systematise MR identification demonstrate, at minimum, non-inferiority on a powered substrate or a clearly bounded regime where it is superior; neither is convincingly shown here."
    }
  ],
  "major_weaknesses": [
    {
      "section": "§3.2 (Theorem 1 / Algebraic Closure)",
      "issue": "Theorem 1 is by-construction near-tautological: MR(A_P) is defined as the Translate-image of block invariants (Definition 7), CONSTRUCT-MP constructs all of them (Steps 1-4), and the theorem asserts every element of MR(A_P) is in some MetaPattern. The paper acknowledges this ('a sceptical reading might object that the by-construction status makes it near-tautological') but still lists it as contribution C2a. The theorem converts an empirical-adequacy claim into a structural-adequacy obligation, which is useful as a framework property but carries limited standalone theoretical weight.",
      "suggested_fix": "Demote Theorem 1 to a Proposition or Well-Formedness Property, and reframe C2a around the IBT and the negative instantiation as the substantive theoretical contributions. Acknowledge explicitly that the theorem's value is as a framework invariant (no Translate-reachable MR is dropped) rather than as a deep algebraic result."
    },
    {
      "section": "§3.1 (Hypothesis 1 / Eight-block decomposition)",
      "issue": "The eight blocks are empirically curated by inspection of program families the authors have studied, not derived from algebraic axioms. The paper is honest about this ('we do not claim that the eight blocks are necessary in an absolute sense'), but it means the 'origin' question from §1 is only partially answered: the structural source of MetaPatterns is the blocks, but the structural source of the blocks is empirical curation. The circularity is partially acknowledged for T* and T*_rev (blocks curated from reactor physics, then used to 'predict' reactor-physics MetaPatterns).",
      "suggested_fix": "Strengthen the non-circular evidence: the deflationary direction (§4.4, Cases A and A-bis) and the L*-blindness prediction (which does not depend on the block curation provenance) are the strongest non-circular results. Feature these more prominently as the primary validation of the framework, and downgrade the reactor-physics 'prediction' of m_adj and m_rev to internal-consistency evidence."
    },
    {
      "section": "§4.3 (METRIC+ Path A, construct validity)",
      "issue": "The four Java subjects (SPHONE, SBAGGAGE, SEXPENSE, SMEAL) are re-implementations written from Sun 2021's prose specification by the same author who designed NOETHER and CONSTRUCT-MP. This confounds framework-design knowledge with subject-implementation fidelity. The paper acknowledges this threat but does not resolve it.",
      "suggested_fix": "Have an independent contributor (or an LLM with no NOETHER knowledge) produce the Java re-implementations, or use Sun et al.'s original Java artefacts if available. At minimum, report the level of divergence between the re-implementation and the original specification."
    },
    {
      "section": "§3.4 (IBT scope)",
      "issue": "The IBT is proved only for the G and T* blocks under the linear operator-implementation fault class. The paper notes that linearity of E_s fails for O_≤ (cone, not subspace), T*_rev (matrix inverse), and L* (norm ratio), so only the sufficient direction holds for those blocks. Since O_≤ and L* are among the most practically populated blocks in the instantiations, the IBT's coverage of the framework's own blocks is limited to 2 of 8.",
      "suggested_fix": "Either develop a linearised-subclass version of the IBT for O_≤ and L* (as hinted in Remark 9, R3), or explicitly state that the IBT's practical scope is the symmetry and self-adjoint blocks and that extension to the remaining blocks is the primary theoretical follow-up. Consider whether the IBT's corollaries (single-block incompleteness, differential-oracle complementarity) can be established under weaker assumptions that cover more blocks."
    },
    {
      "section": "Overall paper length and structure",
      "issue": "The paper is excessively long (estimated 40+ pages in this format) with at least four repeated 'Boundary of contribution' boxes, extensive self-qualification, numerous forward references to supplementary material, and many paragraphs explaining what the paper does NOT claim. This makes the paper very difficult to read and dilutes the genuine contributions.",
      "suggested_fix": "Reduce length by 30-40%. Consolidate all boundary-of-contribution statements into one box in §1 and one in §6. Move the extensive qualifications into a single threats-to-validity section. Eliminate redundant restatements of scope. The core paper should be: framework (§3), IBT (§3.4), negative instantiation (§3.6), empirical evaluation (§4), with supplementary material carrying the rest."
    },
    {
      "section": "§4.1 (Inter-rater agreement)",
      "issue": "The κ values (0.857 for the 18-MR audit, 1.000 for the LRCA Set N audit) are from LLM panels (DeepSeek, ChatGPT, Anthropic Claude) that share substantial pre-training corpora. The paper acknowledges this but the κ values are still presented in the body text as if they carry corroborative weight, which they do not in the standard inter-rater-reliability sense.",
      "suggested_fix": "Remove the κ values from the body text or clearly label them as 'LLM-consistency diagnostics' rather than 'inter-rater agreement.' A human inter-rater κ study should be executed before these numbers carry evidential weight."
    }
  ],
  "minor_issues": [
    "Table 1 caption refers to 'seven-block' decomposition but the paper has eight blocks; the hypothesis label is 'hyp:seven-blocks' despite eight blocks (B1-B8). This is confusing and should be renamed.",
    "The paper cites 'LiTOSEM2025' for a 2024 survey on MR generation but the citation key suggests a 2025 TOSEM paper; verify this is published or forthcoming.",
    "The Set L ensemble (§4.2.6) uses DeepSeek-V3 and ChatGPT-4o-mini, not the strongest available LLM; the paper acknowledges a third-vendor (Claude) extension is 'committed' but the current LLM baseline may be weaker than SOTA.",
    "The cost table (Table 8) estimates '≈10h A_P distillation' for NOETHER's human effort but does not justify this estimate with a timing study.",
    "The paper references 'TODO-ref' comments in the IBT section (§3.4) that appear to be unfixed integration artefacts (e.g., '% TODO-ref empirical sec' in Remark 8).",
    "Definition 4 (Block invariant) uses k≥1 for arity but the per-block Translate templates in Table 9 show varying arities (2 for O_≤, |G| for G, etc.) without a formal arity-binding mechanism.",
    "The 'home-field benchmark' mentioned in the abstract is not clearly defined as a named artefact in the body; the thermal/fluid/reactor SUTs in §4.4 (E1-E3) appear to constitute it but are only briefly described."
  ],
  "questions_to_authors": [
    "Can you execute at least one of the committed protocols (real-bug mining from e3nn/PyG, or the full DeepCrime n≥20 panel) and report results in the revision? This would address the primary publication blocker.",
    "Given that Set G dominates Set N on D1 (p=0.019), can you identify a specific, well-bounded regime (fault class, SUT family, block type) where Set N is non-inferior or superior with adequate power, rather than reporting directional per-block edges on underpowered sub-samples?",
    "Is the eight-block decomposition's empirical curation reproducible by an independent expert? Can you report whether a second analyst, given the same program families, would derive the same eight blocks?",
    "For the IBT, can you establish the corollaries (single-block incompleteness, differential-oracle complementarity) under assumptions weaker than linearity of E_s, to cover at least O_≤ and L*?",
    "What is the actual wall-clock time for A_P distillation on the three instantiated domains? The '≈10h' estimate in Table 8 is unsubstantiated."
  ]
}
```

## Detailed Reviewer Report

### Overview

This is an ambitious paper that proposes a structural, operator-algebraic grounding for metamorphic pattern (MetaPattern) discovery, motivated by an analogy to Noether's methodological move from catalogued conservation laws to symmetry-derived invariants. The framework (NOETHER) has two layers: an upstream empirical layer that curates an eight-block decomposition of a program family's operator algebra, and a downstream mechanical layer (CONSTRUCT-MP) that derives MetaPatterns via a Translate operator. The paper's substantive theoretical contributions are (i) the Invariance-Blindness Theorem (IBT), which characterises the detection kernel of symmetry and self-adjoint MRs as exactly the structure-preserving faults under a faithfulness condition; (ii) the falsification of a stronger absolute-completeness conjecture on the PWR core diffusion algebra with two safety-critical counterexamples; and (iii) a pre-registered, ex-ante L*-blindness prediction confirmed on PIT mutants. The empirical evaluation includes a small equivariant-ML case study, a head-to-head against GenMorph, and a METRIC+ comparison on Sun et al.'s benchmark corpus.

The paper is remarkably self-aware about its limitations—perhaps to a fault, as the excessive self-qualification significantly impairs readability. The core ideas are interesting and the IBT is a genuine contribution to the metamorphic testing literature. However, the empirical evaluation does not meet TOSEM's bar: the primary case study has acknowledged construct-validity bias, the DeepCrime pilot is underpowered, the head-to-head shows Set N dominated by Set G, and the most informative comparison (METRIC+ Path A) has a same-author-reimplementation confound. The committed-but-unexecuted protocols are exactly the studies that would address these gaps.

### Strengths

**S1. The Invariance-Blindness Theorem (§3.4) is the paper's strongest contribution.** The formalisation of "structure-preserving faults are invisible to structural MRs" is non-trivial: the faithfulness condition (Definition 6) and the Reachability Lemma (Lemma 1) establish that a finite executable MR can pin the exact blind set, which is not tautological but follows from finite fault-dimensionality. The three corollaries—single-block incompleteness, trivial-joint-kernel requirement, differential-oracle complementarity—are informative and have practical implications for MR battery design. The empirical support (E1-E3 in §4.4) is consistent with the theorem, though the fault class is restricted to linear operator-implementation faults on N=8.

**S2. The negative instantiation on A_PWR (§3.6, Appendix C.6) is well-executed.** The two counterexamples (non-additivity of rod-bank reactivity worth; mixed T_mod × C_B second derivative of k_eff) are regulatory-essential PWR safety MRs, not contrived edge cases. The per-block exhaustion proofs are detailed and identify five structurally independent obstructions in Translate's signature. This is a valuable negative result that honestly bounds the framework's reach.

**S3. The L*-blindness prediction (§4.2) is the strongest empirical evidence.** The prediction is derived ex-ante from public information (the framework's Translate template for the L* block + PIT's published mutator semantics), pre-registered in git, and confirmed on 5/6 SUTs with a mechanistic explanation for the outlier (two homogeneity-breaking mutators). This is falsifiable science done properly.

**S4. The METRIC+ Path A comparison (§4.3) provides the most informative head-to-head.** On n=120 PIT mutants across four Java subjects, Set N and Set MP achieve comparable detection (42.5% vs 44.2%, McNemar p=0.625) with 92.6% both-kill rate. The Major cross-tool replication (n=555) confirms pooled parity while revealing bidirectional per-subject asymmetries. This is the clearest evidence that NOETHER's algebra-derived MRs reach comparable fault-detection power to a structured-identification scaffold.

### Publication Blockers

**PB1. No adequately powered, construct-validity-clean comparative fault-detection study has been executed.**

The case study (§4.1) has n=20 hand-constructed mutations on a single compact model, with mutations explicitly designed to cover one defect category per non-empty block. The authors themselves state: "The 5/5 unique-detection result therefore exhibits construct validity of ρ_train-rev as a gradient-reversal probe rather than NOETHER's superiority on a defect distribution sampled neutrally from real-world bug reports." The DeepCrime pilot (n=5) yields McNemar p=0.500. The real-bug mining protocol (§4.1, targeting e3nn/PyG bug reports) and the full DeepCrime panel (n≥20) are described as protocols only.

For TOSEM, at least one comparative study must (a) use real or realistically-sourced faults (not hand-constructed to match blocks), (b) have adequate power for inferential statistics, and (c) not be compromised by same-author subject implementation. The METRIC+ Path A comparison comes closest but has the reimplementation confound. The revision must execute at least one of the committed protocols and report results.

**PB2. The head-to-head against GenMorph shows Set N dominated by Set G.**

On the D1 stratum (n=52, the within-scope comparison), Set N achieves 26/52 (50.0%) vs Set G's 37/52 (71.2%), McNemar p=0.019. The paper reframes this as per-block complementarity and cost-axis advantage, which is honest but means the framework's MRs detect fewer algebra-disrupting mutants than GP-evolved MRs on the substrate where NOETHER should have a structural advantage. The per-block sub-samples (G: n=11; L*: n=24; G_tr: n=17) are underpowered, and the only directional edge (G_tr, 10/17 vs 8/17) has substantially overlapping Wilson intervals.

The paper needs either (a) a larger head-to-head substrate where per-block claims can be powered, or (b) a clearly bounded regime (specific fault class, SUT family, block type) where Set N demonstrates non-inferiority or superiority with adequate power, or (c) a frank acknowledgment that NOETHER's contribution is structural coverage and cost-axis, not fault-detection efficacy, with the empirical evaluation restructured accordingly.

### Major Weaknesses (Fixable)

**MW1. Theorem 1 is by-construction near-tautological.** The paper acknowledges this but still presents it as contribution C2a. The theorem's value is as a framework invariant (no Translate-reachable MR is dropped), not as a deep algebraic result. The revision should demote it to a Proposition or Well-Formedness Property and reframe the theoretical contribution around the IBT and the negative instantiation.

**MW2. The eight-block decomposition is empirically curated, not derived.** Hypothesis 1 is an empirical hypothesis, and the paper is honest about this. But the "origin" question from §1 is only partially answered: the structural source of MetaPatterns is the blocks, but the structural source of the blocks is by-inspection curation of program families the authors have studied. The circularity for T* and T*_rev (curated from reactor physics, then used to "predict" reactor-physics MetaPatterns) is acknowledged. The non-circular evidence (deflationary direction in §4.4, L*-blindness prediction) should be featured more prominently.

**MW3. The IBT covers only 2 of 8 blocks.** Linearity of E_s holds for G and T* but fails for O_≤ (inequality/cone), T*_rev (matrix inverse), and L* (norm ratio). Since O_≤ and L* are among the most practically populated blocks, the IBT's coverage of the framework's own blocks is limited. The revision should either develop linearised-subclass versions for additional blocks or explicitly state the IBT's practical scope and prioritise extension as the primary theoretical follow-up.

**MW4. Construct-validity threats in the METRIC+ comparison.** The four Java subjects are re-implementations by the same author who designed NOETHER. An independent re-implementation or use of original artefacts would resolve this confound.

**MW5. LLM-based inter-rater agreement.** The κ values from LLM panels that share training data cannot be interpreted as independent inter-rater reliability. These should be clearly labelled as LLM-consistency diagnostics, not inter-rater agreement, and a human κ study should be executed.

**MW6. Excessive length and self-qualification.** The paper has at least four repeated "Boundary of contribution" boxes, extensive qualification paragraphs, and numerous forward references to supplementary material. A 30-40% reduction would significantly improve readability without losing content. Consolidate boundary statements, move qualifications to §5, and eliminate redundant scope restatements.

### Threats to Validity

*Internal:* The canonical-block ordering (Definition 8) determines Theorem 1's uniqueness but is asserted by inspection, not derived. The per-block exhaustion proofs for the negative instantiation depend on the completeness of Table 9's Translate templates.

*Construct:* The case study's mutation construction bias is the most material threat. The same-author reimplementation of METRIC+ subjects is a second construct threat. The LLM-based κ values are a third.

*External:* The 10 SUTs in the head-to-head are from a single codebase (MathSignalClass + ComplexSignal). The cross-codebase Commons-Math pilot (n=3 SUTs, 77 mutants) is underpowered. The three primary instantiations are all domains where the authors have prior expertise.

*Conclusion:* The statistical inferences rest on small denominators (n=20, n=5, n=57) with wide confidence intervals. The L*-blindness prediction (n=44 across 6 SUTs) is the only adequately powered test, and it tests a narrow prediction.

### What a Revision Must Do

1. **Execute at least one committed protocol** (real-bug mining or full DeepCrime panel) and report results. This is the primary blocker.
2. **Either power the head-to-head** (larger substrate, more SUTs) or **restructure the empirical claims** to explicitly privilege structural coverage, cost-axis, and the L*-blindness prediction over fault-detection efficacy.
3. **Demote Theorem 1** and reframe the theoretical contribution around the IBT and the negative instantiation.
4. **Reduce paper length by 30-40%**: consolidate boundary boxes, move qualifications to §5, eliminate redundant scope restatements.
5. **Address the construct-validity confounds**: independent reimplementation of METRIC+ subjects, human inter-rater κ, or clear labelling of LLM-based diagnostics.
6. **Fix the integration artefacts** (TODO-ref comments in §3.4) and verify all cross-references resolve.