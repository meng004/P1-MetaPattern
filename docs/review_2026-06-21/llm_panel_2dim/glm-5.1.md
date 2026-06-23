```json
{
  "overall_recommendation": "Major Revision",
  "reviewer_confidence_1to5": 4,
  "scores_1to5": {
    "soundness": 3,
    "novelty": 3,
    "significance": 2,
    "presentation": 2,
    "reproducibility": 4
  },
  "summary": "The paper introduces NOETHER, a framework that derives metamorphic relation (MR) classes from the operator-algebraic structure of program families. An upstream layer curates a program family's operator algebra and decomposes it into eight empirically motivated blocks (symmetry, order, self-adjointness, time-reversal, limit, qualitative dynamics, method-comparison, relational equivalence); a downstream algorithm (CONSTRUCT-MP) mechanically derives MetaPatterns from block invariants via a Translate operator. The paper proves a closure result for the downstream construction, a polynomial-time constructibility bound, an Invariance-Blindness Theorem characterizing detection kernels for G and T* blocks under linear faults, and falsifies a stronger completeness conjecture on a PWR core diffusion algebra via two concrete counterexamples. Empirical evaluation covers three domains (Boltzmann reactor physics, equivariant ML, relational query optimisers) and a Java head-to-head against GenMorph.",
  "strengths": [
    "The operator-algebraic framing of MR identification is genuinely novel and offers a principled alternative to purely inductive or search-based MR discovery.",
    "The Invariance-Blindness Theorem (Theorem 3) is the paper's strongest theoretical contribution: it gives a non-trivial, falsifiable characterization of what symmetry/self-adjoint MRs cannot detect, with corollaries on single-block incompleteness and complementarity with differential oracles.",
    "The falsification of Theorem 1' (absolute completeness) on A_PWR via two engineering-significant counterexamples (non-additivity of rod-bank reactivity worth; mixed MTC-boron dependence) is honest, substantive, and identifies concrete extensions to Translate's signature.",
    "The L*-blindness prediction and its confirmation on 5/6 SUTs is a genuine a-priori quantitative prediction derivable from public information, providing rare falsifiability in the MR-identification literature.",
    "The paper is unusually scrupulous about scope limitations, documenting out-of-scope MR classes, candidate ninth blocks, and construct-validity caveats in dedicated boxes.",
    "Artifact availability is strong: Zenodo deposit, reproducibility manifests, and extensive supplementary materials."
  ],
  "publication_blockers": [
    {
      "section": "§3.2, Theorem 1",
      "issue": "The closure theorem is by-construction: MR(A_P) is defined as the Translate-image of A_P's block invariants, and the theorem then states that every element of this image is in the image. This is a definitional tautology dressed as a theorem.",
      "why_fatal": "A by-construction closure over a definitionally fixed space provides no information about the space's relationship to the MRs practitioners actually need. The paper positions this as contribution C2a and as the central positive theoretical result. For a TOSEM paper, a theorem that is acknowledged as 'near-tautological' cannot serve as a primary theoretical pillar without either (a) proving something non-trivial about the relationship between MR(A_P) and a richer MR space, or (b) substantially downgrading its claimed contribution."
    },
    {
      "section": "§4.2 (equivariant ML case study)",
      "issue": "The case study uses n=20 hand-constructed mutations on a single 5,189-parameter model, with mutations explicitly designed to cover one defect category per non-empty block of A_equi (including category-iv targeted at rho_train-rev). The 5/5 unique detection in cat-iv is construct-validity of that MR, not evidence of the framework's identification power.",
      "why_fatal": "The paper's only empirical demonstration that NOETHER identifies MRs missed by existing approaches rests on a construct-validity-controlled study with n=20 mutations on a toy model. No real-world fault data, no multi-architecture replication, no neutral mutation sampling. The DeepCrime pilot (n=5) is underpowered (McNemar p=0.500). Without at least one well-powered study on real faults or neutrally-sampled mutations, the practical significance of the framework is unsupported."
    }
  ],
  "major_weaknesses": [
    {
      "section": "§4.3 (Java head-to-head)",
      "issue": "Set N is dominated by Set G on the D1 stratum (McNemar p=0.019, 0.500 vs 0.712). The per-block decomposition shows G-block failure on gcdSig/lcmSig and L*-block complementarity but not dominance. The paper's contribution on this substrate is 'block-targeted precision plus complementarity with documented per-block design gaps,' which is a weaker claim than the introduction's framing suggests.",
      "suggested_fix": "Scale the evaluation to at least 30 SUTs with a wider mutation catalogue (e.g., Major's 95-operator catalogue, already partially reported). Report aggregate D1 comparisons with adequate power. Be explicit in the introduction that the framework is not claimed to outperform GP-evolved MRs on aggregate fault detection."
    },
    {
      "section": "§3.1 (Hypothesis 1)",
      "issue": "The eight-block decomposition is an empirical curation, not a theorem. The blocks were motivated by inspecting program families including reactor physics; then 'validated' by applying them back to reactor physics and to ML/DB domains. The prediction of m_adj and m_rev on A_Boltz is acknowledged as circular (the T* and T*_rev blocks were partly induced from reactor-physics structures).",
      "suggested_fix": "Add a dedicated subsection that cleanly separates which predictions are circular from which are genuinely a priori. The L*-blindness prediction is genuinely a priori (derivable from public info without data); the m_adj/m_rev 'predictions' are not. Restructure the contribution list so C3 is scoped as 're-classification under a uniform structure' rather than 'prediction.'"
    },
    {
      "section": "§3.3.4 (IBT scope)",
      "issue": "The Invariance-Blindness Theorem applies only to blocks G and T* under the linear operator-implementation fault class. For the remaining six blocks (O_<=, T*_rev, L*, D*, E*, B*_rel), only the trivial sufficient direction holds. The IBT is therefore a characterization of only 2/8 blocks.",
      "suggested_fix": "Either extend the IBT to at least one additional block (O_<= under a cone fault model would be a natural next step), or be more explicit in the abstract/introduction that the detection-kernel characterization covers only the symmetry and self-adjoint blocks."
    },
    {
      "section": "Overall paper length and presentation",
      "issue": "The manuscript is approximately 45 pages of dense, heavily cross-referenced text with 10+ tables, 3+ boundary-of-contribution boxes, 16 committed future-work items, and extensive footnotes. Key results are buried in supplementary material (Appendices A-E migrated out). The signal-to-noise ratio is very low.",
      "suggested_fix": "Cut the paper by at least 40%. Consolidate the three boundary boxes into one. Move the detailed GenMorph/PIT head-to-head tables to supplementary and keep only the per-block summary. Merge the METRIC+ subsection into Related Work. Remove the 16-item committed-future-work list and keep only the top 3."
    }
  ],
  "minor_issues": [
    "Definition 1 (program-induced operator algebra) uses a composition operator 'circ' but never specifies its properties (associativity? identity?). Is this a monoid? A category?",
    "The 'Noether-style' naming is explicitly acknowledged as methodological only, yet the paper repeatedly invokes the analogy (§3.4.4, §3.5.3) in ways that may mislead readers into expecting a variational result.",
    "Table 6: Set G (30-min) kills 40/62 mutants but the 1-min rerun kills 39/62. This near-identical result suggests the GP search converges quickly, undermining the cost-axis argument that Set N saves ~30 min per SUT.",
    "The LLM inter-rater agreement (kappa = 0.857, 0.931) uses models that share training data, so these are not independent raters. The paper acknowledges this but still reports the numbers in a way that invites over-interpretation.",
    "The equivariant ML case study's Set L uses a single GPT-4 sample at temperature 0 with a fixed seed. This is not representative of LLM MR-generation capability, yet the paper draws strong qualitative conclusions from the contrast.",
    "Remark 2 states |M(A_P)| >= number of non-empty blocks, but Remark 3 then says |M(A_P)| *equals* the number of non-empty blocks for the three instances (single-class assumption). This is a significant simplification that should be discussed more centrally.",
    "The paper cites three references (Hu et al. 2019; Mariani 2018; Liu et al. 2020) that 'could not be located.' This is unusual for a peer-reviewed submission and suggests either citation sloppiness or references to unpublished/non-existent work."
  ],
  "questions_to_authors": [
    "Theorem 1 is by-construction over MR(A_P) as defined in Definition 5. If you instead defined MR(A_P) as 'all properties of P's executions formulable over A_P's operators,' would Theorem 1 still hold? (Your Theorem 1' falsification suggests not.) If not, what is the substantive content of Theorem 1 beyond 'the construction constructs what it constructs'?",
    "How many human-hours were required to distill A_Boltz, A_equi, and A_rel respectively? This is the critical cost that Theorem 2's polynomial-time bound does not capture. Without quantifying the upstream effort, the cost comparison in Table 8 is incomplete.",
    "The L*-blindness prediction is the paper's strongest empirical result. Can you formulate analogous a-priori quantitative predictions for any other block (G, T*, O_<=) that could be tested on a different mutator set or substrate?",
    "On the PWR negative instantiation: you identify five pairwise-independent obstructions. Have you attempted even a partial Composite-Translate extension (e.g., admitting operator-spectrum outputs while keeping single-block structure) to check whether closure and poly-time constructibility survive?",
    "What happens when the eight-block decomposition is wrong for a new program family—i.e., when a user applies NOETHER to a family with an undiscovered ninth block? How would the user detect the gap? The current guidance (§5.1) says 'report as candidates for extension,' but this presupposes the user knows they missed something."
  ]
}
```

---

## Detailed Review

### Summary of the Paper

NOETHER proposes that metamorphic relations (MRs) can be systematically derived from the operator-algebraic structure of a program family's governing equations. The framework decomposes a program-induced operator algebra $\mathcal{A}_P$ into eight empirically curated blocks, then mechanically derives MetaPattern classes from block invariants via a `Translate` operator. The main theoretical results are a closure theorem for the downstream construction, a polynomial-time constructibility bound, an Invariance-Blindness Theorem for symmetry and self-adjoint blocks under linear faults, and the falsification of a stronger completeness conjecture via two PWR reactor-physics counterexamples. The empirical evaluation spans three domains and a Java head-to-head against GenMorph's GP-evolved MRs.

### Strengths

**1. The operator-algebraic framing is genuinely original.** The insight that MRs should be traceable to invariants of a program family's mathematical structure—rather than induced from observed MR instances or mined from test suites—is novel and potentially impactful. The paper's structural decomposition provides a principled vocabulary for discussing *why* certain MRs hold and *where* they stop applying.

**2. The Invariance-Blindness Theorem is the paper's best result.** Unlike the closure theorem (which is trivial by construction), the IBT gives a non-trivial characterization of detection kernels: for G and T* blocks under linear faults, the blind spot is *exactly* the structure-preserving faults. The corollaries on single-block incompleteness and complementarity with differential oracles are clean and actionable. This is a real contribution to the theory of metamorphic testing.

**3. The negative instantiation is honest and substantive.** Falsifying Theorem 1' on $\mathcal{A}_{\text{PWR}}$ with two engineering-significant MRs (non-additivity of rod-bank reactivity worth; MTC-vs-boron mixed dependence) that are *regulatory-essential* for PWR core simulators is a strong result. It identifies five pairwise-independent obstructions in Translate's signature, giving a precise roadmap for future work.

**4. The L*-blindness prediction and confirmation.** The prediction that $L_{\text{scale}}$ MRs kill near-zero PIT mutants on homogeneity-preserving substrates is derivable from public information without consulting any data, and it is confirmed on 5/6 SUTs. This is rare in the MR-identification literature and provides genuine falsifiability.

**5. Exceptional honesty about scope.** The boundary-of-contribution boxes, the explicit catalogue of out-of-scope MR classes, the construct-validity caveats, and the honest reporting of Set G's dominance in the head-to-head are commendable.

### Fatal and Major Weaknesses

**PUBLICATION BLOCKER 1: The closure theorem is by-construction.** Theorem 1 states that every MR in $\text{MR}(\mathcal{A}_P)$ (defined as the Translate-image of block invariants) is assigned to a MetaPattern in $\mathbb{M}(\mathcal{A}_P)$ (constructed to contain all such MRs). This is a definitional tautology. The authors acknowledge this (§3.3, "A sceptical reading might object that the by-construction status of Theorem 1 makes it near-tautological"), but the paper still positions it as contribution C2a and as a "no-drop closure invariant." The paragraph attempting to justify the theorem's value—converting "empirical-adequacy claim" into "structural-adequacy claim"—is rhetorical rather than mathematical: the structural adequacy is over a space that was defined to make the theorem true. The real content is in the IBT and the negative instantiation, not in Theorem 1.

*What a revision must do:* Either (a) prove something non-trivial relating $\text{MR}(\mathcal{A}_P)$ to a richer MR space (e.g., an approximation ratio or a sandwich bound), or (b) substantially downgrade Theorem 1's claimed contribution to a well-formedness property and recenter the paper's theoretical contribution on the IBT and the negative result.

**PUBLICATION BLOCKER 2: The empirical evaluation is underpowered and construct-biased.** The equivariant ML case study—the only empirical demonstration that NOETHER identifies MRs missed by existing approaches—uses n=20 mutations on a single 5,189-parameter model, with mutations *explicitly designed* to cover one defect category per block. The 5/5 unique detection in category (iv) exhibits construct validity of $\rho_{\text{train-rev}}$, not the framework's identification power. The DeepCrime pilot (n=5) is underpowered (McNemar p=0.500). The Java head-to-head shows Set N *dominated* by Set G on D1 mutants (0.500 vs 0.712, McNemar p=0.019). The cross-codebase pilot (n=77 mutants) gives Set N only 13.0% kill rate. None of these individually or collectively provides adequate evidence that the framework's algebraic grounding leads to MRs with practical testing value.

*What a revision must do:* Conduct at least one well-powered study (≥50 real or neutrally-sampled mutations, ≥3 architectures or codebases) where NOETHER-derived MRs demonstrate non-trivial fault detection that is not an artifact of mutation construction. The real-bug evaluation protocol (§4.2, mining from e3nn/PyG bug reports) would be ideal if actually executed.

**MAJOR WEAKNESS 1: The eight-block taxonomy is empirical and partially circular.** Hypothesis 1 is an "empirical hypothesis open to refutation." The T* and T*_rev blocks were partly induced from reactor-physics structures; applying them back to reactor physics and "predicting" $m_{\text{adj}}$ and $m_{\text{rev}}$ is therefore circular. The authors acknowledge this ("The framework does not discover these MetaPatterns de novo. What it does is closer to a uniform re-projection"), but the paper still labels these as "predicted" in Table 3. This misrepresents the nature of the result.

**MAJOR WEAKNESS 2: The upstream bottleneck.** The entire framework depends on distilling $\mathcal{A}_P$ from program semantics, which is acknowledged as a "human task" and the "principal limitation." This means the framework automates only the easier, downstream step. The cost comparison in Table 8 lists NOETHER's human effort as ≈10 hours for $\mathcal{A}_P$ distillation per family, but this is the bottleneck cost that determines whether the framework is practically usable. If distillation requires deep domain expertise and hours of manual work, the framework's advantage over simply asking a domain expert to list MRs is unclear.

**MAJOR WEAKNESS 3: The IBT covers only 2/8 blocks.** For the six blocks where the sufficient direction is trivial and the necessary direction fails (O_≤, T*_rev, L*, D*, E*, B*_rel), the IBT provides no detection-kernel characterization. The paper's title and abstract imply a general framework, but the deepest theoretical result applies to a quarter of the blocks.

**MAJOR WEAKNESS 4: Excessive length and poor signal-to-noise ratio.** The manuscript is approximately 45 pages of dense text with 10+ tables, 3 boundary boxes, and 16 committed future-work items. Key results (Appendices A-E) are migrated to supplementary. The METRIC+ comparison (§4.4) and PMCM worked example (§4.5) could be substantially compressed. The paper would be significantly stronger at 25 pages with the same content.

### Threats to Validity

**Internal:** The construct validity of the equivariant ML case study is the most material threat. The mutation set was hand-constructed to map one-to-one onto A_equi's non-empty blocks, making the unique-detection result a tautology of the construction rather than an empirical finding. The LLM-based inter-rater agreement (κ=0.857, 0.931) uses models sharing training data and is not equivalent to independent human expert evaluation.

**External:** The framework is evaluated only on programs with explicit mathematical governing equations (reactor physics, equivariant ML, query optimisers, numerical libraries). The six out-of-scope program-family classes in Remark 4 include most general software engineering domains. The paper's applicability is therefore narrow, and the generalizability claim should be scoped accordingly.

**Conclusion:** The case study's denominator (20 mutations, one model, one architecture) is insufficient to characterize the framework's performance distribution. The Java head-to-head's Set G dominance on D1 mutants is honestly reported but undermines the practical significance claim.

### What a Revision Must Do

1. **Downgrade Theorem 1's contribution** to a well-formedness property and recenter the theoretical contribution on the IBT and the negative instantiation.

2. **Conduct at least one adequately powered empirical study** with real faults or neutrally-sampled mutations on ≥3 subjects, ideally using the proposed real-bug evaluation protocol.

3. **Resolve the circularity in the "prediction" claims** by cleanly separating re-classification results from genuinely a priori predictions (only the L*-blindness prediction qualifies).

4. **Cut the paper by at least 40%**, consolidating boundary boxes, compressing the METRIC+ and PMCM sections, and moving detailed head-to-head tables to supplementary.

5. **Extend the IBT** to at least one additional block (O_≤ under a cone fault model is the natural candidate) or be explicit in the abstract that the detection-kernel characterization covers only symmetry and self-adjoint blocks.

6. **Quantify the upstream distillation cost** concretely (hours per algebra, expertise required) so readers can assess the framework's practical usability.