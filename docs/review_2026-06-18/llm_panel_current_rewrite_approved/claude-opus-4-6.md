

```json
{
  "overall_recommendation": "Major Revision",
  "reviewer_confidence_1to5": 4,
  "scores_1to5": {
    "soundness": 2,
    "novelty": 3,
    "significance": 2,
    "presentation": 1,
    "reproducibility": 3
  },
  "summary": "The paper proposes NOETHER, a two-layer framework that derives metamorphic relation (MR) classes ('MetaPatterns') from the operator-algebraic structure of equation-governed program families. It decomposes a program-induced operator algebra into eight recurrent blocks, proves closure of the derived MR set under a Translate operator (Theorem 1), and instantiates the framework on three domains (reactor physics, equivariant ML, relational query optimizers). A negative result falsifies absolute completeness on a PWR algebra, and an Invariance-Blindness Theorem characterizes the detection kernel for two blocks.",
  "strengths": [
    "The intellectual ambition is genuine: connecting operator-algebraic structure of governing equations to systematic MR derivation is a novel angle that could advance the MR-identification bottleneck beyond purely empirical catalogues.",
    "The negative result (§3.5, Appendix C.6) is the paper's strongest theoretical contribution—falsifying Theorem 1' on A_PWR with two concrete, physically meaningful counterexamples and identifying five independent obstructions is rigorous and honest.",
    "The Invariance-Blindness Theorem (§3.3, Theorem 3) provides a non-trivial, falsifiable characterization of what algebra-derived MRs cannot detect, converting a by-construction closure into a substantive detection-limit statement.",
    "The paper is unusually transparent about its own limitations: the upstream layer is acknowledged as empirical, the circularity of 'prediction' from blocks curated from the same domain is flagged, and the scope boundary is documented in detail (Remarks 3–6).",
    "The L*-block blindness prediction (§5.2.1) is a genuinely falsifiable, ex-ante derivable prediction that is confirmed empirically, demonstrating the framework's operative-mechanism status.",
    "Artifact availability commitments are detailed and the experimental protocol includes pre-registered hypotheses with explicit falsification criteria."
  ],
  "publication_blockers": [
    {
      "section": "Throughout (§1–§6, all sections)",
      "issue": "The manuscript is approximately 3–4× the typical TOSEM page budget (~60 pages of dense content in the LaTeX source, plus extensive appendices). The extreme length makes it effectively unreviewable in its current form and violates TOSEM norms.",
      "why_fatal": "TOSEM papers typically run 40–50 pages including references. This manuscript, even accounting for the acmart manuscript format expansion, contains an enormous amount of hedging prose, repeated boundary-of-contribution boxes (at least 4 near-identical restatements), and inline protocol/future-work commitments that belong in supplementary material. The redundancy obscures rather than clarifies the contribution. A reviewer or reader cannot identify the core claims without reading 100+ paragraphs of caveats. This is a presentation-level blocker: the paper cannot be published in anything resembling its current form."
    },
    {
      "section": "§3.2 (Theorem 1, Definition 5)",
      "issue": "Theorem 1 (Algebraic Closure) is near-tautological by the authors' own admission. The MR space MR(A_P) is defined as exactly the image of Translate (Definition 5), and Theorem 1 says every element of that image is assigned to a MetaPattern. This is a restatement of the construction, not a theorem with independent content.",
      "why_fatal": "The paper's central theoretical claim (C2a) rests on Theorem 1. The authors acknowledge its by-construction status but argue it 'converts an empirical-adequacy claim into a structural-adequacy claim.' However, this conversion is vacuous: the 'structural adequacy' is over a space the framework itself defined. The only non-trivial theoretical content is the negative result (Theorem 1' falsification) and the IBT (Theorem 3). Presenting a tautology as one of five contributions (C2a) misleads about the paper's theoretical depth. The paper needs to either (a) prove something non-trivial about the Translate-defined space (e.g., that it captures a meaningful fraction of practically useful MRs, with evidence beyond the authors' own catalogues), or (b) honestly demote Theorem 1 to a well-formedness lemma and restructure contributions around the IBT and negative results."
    },
    {
      "section": "§5.1 (Table 3, case study)",
      "issue": "The primary empirical comparison (Table 3) uses a mutation set hand-constructed to have one defect category per NOETHER block, making the 'unique detection' result (H2) circular by design. The case study uses n=20 mutations on a single 5,189-parameter toy model.",
      "why_fatal": "The construct-validity caveat is acknowledged but insufficiently weighted. When the mutation set is designed so that category (iv) is detectable only by ρ_train-rev, the 5/5 unique detection is not evidence of NOETHER's value—it is evidence that the experimental design works as intended. The DeepCrime pilot (n=5, p=0.500) is explicitly underpowered. The head-to-head on Java SUTs (§5.2) shows Set N is dominated by Set G (McNemar p=0.0043 pooled). The paper therefore has no non-circular empirical evidence that NOETHER-derived MRs are practically useful for fault detection beyond what existing methods provide. For a TOSEM methods paper, some credible empirical evidence of practical value is needed."
    }
  ],
  "major_weaknesses": [
    {
      "section": "§3.1 (Hypothesis 1, eight blocks)",
      "issue": "The eight operator blocks are presented as an empirical curation but treated downstream as if they were a principled decomposition. The paper never provides evidence that these eight blocks cover a meaningful fraction of real-world MR needs beyond the authors' own catalogues.",
      "suggested_fix": "Conduct a systematic mapping study: take a published MR corpus from an independent source (e.g., Segura et al.'s survey corpus, or Ying et al.'s family trees) and classify each MR into the eight blocks. Report the fraction that maps cleanly, the fraction that is orphaned, and the inter-rater agreement with independent human raters (not LLMs sharing training data)."
    },
    {
      "section": "§5.2 (head-to-head, Table 7)",
      "issue": "The head-to-head against GenMorph shows Set N is dominated on the D1 stratum (26/52 vs 37/52, p=0.019) and the paper's reading strategy (per-block decomposition, cost-axis, D2 prediction) is post-hoc narrative construction around a negative result.",
      "suggested_fix": "Be forthright: the aggregate empirical result is that NOETHER's MRs detect fewer faults than a GP-evolved baseline on algebra-rich SUTs. The per-block decomposition is informative but should not be presented as the 'primary reading' when it was not pre-registered as such. Reframe the contribution as structural coverage + explainability, not detection competitiveness."
    },
    {
      "section": "§4 (EQ1–EQ3), §5",
      "issue": "The evaluation questions are framed as 'binary operator-block coverage' (EQ1), which is trivially satisfied by construction when NOETHER derives one MR per block. This makes EQ1 non-falsifiable for Set N.",
      "suggested_fix": "Replace binary coverage with a metric that has discriminative power: e.g., the fraction of independently-published MRs from external corpora that are algebra-induced under Definition 5, or the fraction of real faults in public bug databases that are detectable by algebra-induced MRs."
    },
    {
      "section": "§2.4, §5.4",
      "issue": "The comparison with METRIC+ is performed manually by the framework's designer on three SUTs, and the Path A head-to-head uses Java re-implementations written by the same author. This confounds framework knowledge with subject implementation.",
      "suggested_fix": "Use METRIC+'s published subjects and implementations directly, or have an independent researcher perform the METRIC+ derivation and Java re-implementation."
    },
    {
      "section": "§3.3 (IBT, Theorem 3)",
      "issue": "The Invariance-Blindness Theorem is restricted to the linear operator-implementation fault class and to the G and T* blocks. This is a narrow scope that the paper does not adequately contextualize—most real faults in software are not linear operator perturbations.",
      "suggested_fix": "Add a discussion of what fraction of real faults (e.g., from DeepCrime's taxonomy or PIT's mutation operators) fall within the linear operator-implementation class. Without this, the IBT's practical relevance is unclear."
    },
    {
      "section": "Throughout",
      "issue": "The inter-rater agreement figures (κ=0.857, κ=1.000) are from LLM panels, not independent human raters. The paper acknowledges this but still uses these figures as evidence.",
      "suggested_fix": "Either conduct a human inter-rater study or clearly label all LLM-panel agreement figures as 'LLM consistency checks' rather than 'inter-rater reliability,' and do not report Fleiss' κ values that imply independent rating."
    }
  ],
  "minor_issues": [
    "The paper's title invokes 'Noether' but the connection to Noether's theorem is explicitly acknowledged as 'methodological analogy only' (footnote 1). This is marketing, not substance.",
    "Table 1 (refinement) reports 'predicted' MetaPatterns m_adj and m_rev, but §3.4.3 extensively discusses the circularity of this 'prediction.' The table should note the circularity directly.",
    "The notation switches between A_P, A_F, A_Boltz, A_equi, A_rel, A_PWR without a consistent convention for when subscripts denote program families vs. specific algebras.",
    "The paper uses 'MetaPattern' capitalized throughout as if it were a formal term introduced here, but it appears to be used in prior work (METRIC, METRIC+) without the capitalization or the specific algebraic meaning.",
    "The cost comparison (Table 12) lists NOETHER's human effort as '~10h A_P distillation' but this is for a domain expert with operator-algebra knowledge; the actual cost for a typical software tester is likely much higher.",
    "References [cite needed] for 'Hu et al. 2019; Mariani 2018; Liu et al. 2020; Lin 2020' that 'could not be located' (§2.4) should either be found or the paragraph removed.",
    "The 'boundary of contribution' boxes appear at least 4 times with near-identical content (§1, §3.2, §5.2.4, §6). Consolidate to one.",
    "§3.5 (negative instantiation) is extremely detailed on PWR reactor physics (rod-bank worth, MTC-vs-boron curves) to a degree that exceeds the SE audience's background. The physics could be condensed significantly.",
    "The paper commits to 16 future work items (§5.2.5), which suggests the work is incomplete rather than ready for publication."
  ],
  "questions_to_authors": [
    "Can you provide a single, concrete example where NOETHER's algebraic derivation led to the discovery of an MR that was (a) not previously known in the domain literature, (b) not discoverable by prompting an LLM, and (c) detected a real fault in production software?",
    "Theorem 1 quantifies over MR(A_P) which is defined as Translate's image. What would a non-tautological version of this theorem look like? Specifically, can you state a closure property over a space defined independently of Translate?",
    "The head-to-head shows Set N losing to Set G on the aggregate D1 stratum. Under what conditions would you consider the framework empirically unsuccessful, and have those conditions been met?",
    "The eight blocks were curated by inspecting program families that include reactor physics. If you removed reactor physics from the curation set, would T* and T*_rev still appear? What is the evidence that these blocks generalize beyond physics?",
    "The IBT applies only to the linear fault class. What fraction of PIT's default mutations (which you use extensively) fall within this class?",
    "You acknowledge that the upstream distillation of A_P requires a domain expert with operator-algebra knowledge. How many such experts exist for a typical software project? Is the framework practically usable outside mathematical/scientific computing?"
  ]
}
```

## Detailed Reviewer Report

### Overview

This paper attempts something ambitious: grounding metamorphic relation identification in operator algebra rather than empirical cataloguing. The intellectual direction is sound and potentially valuable. However, the manuscript suffers from three interrelated problems that collectively prevent publication in its current form: (1) the central theorem is tautological, (2) the empirical evaluation does not demonstrate practical value, and (3) the presentation is so bloated that the genuine contributions are buried.

### Strengths in Detail

**The negative result is genuinely strong.** The falsification of Theorem 1' on A_PWR (§3.5) via two physically meaningful counterexamples—non-additivity of rod-bank reactivity worth and MTC-vs-boron mixed dependence—is the paper's best theoretical work. The identification of five pairwise-independent obstructions in Translate's signature is rigorous, well-motivated by engineering practice, and provides concrete direction for future theoretical development. This is publishable-quality theoretical contribution.

**The Invariance-Blindness Theorem provides real insight.** Theorem 3's characterization that the detection kernel equals the structure-preserving faults (under linearity and faithfulness conditions) is a non-trivial result that converts the framework's by-construction closure into a falsifiable, non-tautological detection-limit statement. The three corollaries (single-block incompleteness, trivial-joint-kernel completeness requirement, differential-oracle complementarity) are actionable for test design.

**The L*-block blindness prediction is a model for framework validation.** The ex-ante derivable, falsifiable prediction that scaling MRs kill near-zero PIT mutants on homogeneity-preserving programs (§5.2.1), confirmed on 5/6 SUTs, demonstrates that the structural decomposition has operative-mechanism status. This is exactly the kind of evidence a framework paper should provide.

### Publication Blockers in Detail

**1. Manuscript length and redundancy.** The paper is approximately 25,000+ words of body text plus extensive appendices. For comparison, a typical TOSEM paper runs 12,000–15,000 words. The "boundary of contribution" box appears in near-identical form in §1, §3.2, §5.2.4, and §6. The threats-to-validity section (§6) repeats caveats already stated inline throughout §5. Future work commitments (16 items!) are scattered across the paper. The result is a manuscript that is physically impossible to review carefully in a single sitting. **A revision must cut the paper by at least 40%, consolidating the contribution statement to one location and moving all protocol commitments, future work items, and worked examples to supplementary material.**

**2. Theorem 1 is tautological.** Definition 5 defines MR(A_P) as the image of Translate. Theorem 1 says every element of MR(A_P) is assigned to a MetaPattern by CONSTRUCT-MP. This is equivalent to saying "the construction constructs what it constructs." The authors acknowledge this ("a sceptical reading might object that the by-construction status makes it near-tautological") but then spend several paragraphs arguing the tautology has value. It does not have the value claimed. The paper lists this as contribution C2a, one of five contributions. **A revision must either (a) prove a non-trivial theorem about the relationship between MR(A_P) and some independently-defined MR space, or (b) demote Theorem 1 to a well-formedness lemma and restructure the contribution list around the IBT and negative results.**

**3. The empirical evaluation is insufficient.** The case study (§5.1) uses 20 hand-constructed mutations on a toy EGNN model. The mutation set is designed with one category per NOETHER block, making H2's "unique detection" result circular. The DeepCrime pilot (n=5) is underpowered (p=0.500). The Java head-to-head (§5.2) shows Set N losing to Set G (McNemar p=0.0043 pooled, p=0.019 on D1). The METRIC+ comparison (§5.4) uses Java re-implementations written by the framework's designer. **A revision must provide at least one evaluation on an independently-authored corpus with real faults, or clearly reposition the paper as a purely theoretical contribution and remove all claims about practical testing utility.**

### Major Weaknesses in Detail

**The eight-block decomposition lacks independent validation.** Hypothesis 1 lists eight blocks curated "by inspecting mathematical structures that recur across the program families we have studied." The only validation is against the authors' own reactor-physics catalogue, an LLM-panel audit (which the authors correctly note has shared-training-data limitations), and the three instantiations the authors themselves performed. No independent researcher has applied the decomposition to a program family outside the authors' domain expertise. The claim that these eight blocks are "sufficient" for equation-governed programs is a strong empirical hypothesis with no independent corroboration.

**The head-to-head narrative is post-hoc.** The pre-registered hypothesis H3a has three sub-claims. H3a.1 (per-block detection) gets a "mixed" verdict; H3a.2 (complementarity) is "supported" but asymmetrically (Set G has 4× more exclusive kills); H3a.3 (cost-axis) is "supported" but is an apples-to-oranges comparison (human algebra distillation vs. automated GP search). The paper then presents the per-block decomposition as the "primary reading" and the aggregate D1 result as "secondary"—but the aggregate result is the only one with sufficient statistical power. The narrative structure gives the impression of choosing the reading that makes the framework look best.

**Scope is narrower than presentation suggests.** Remark 5 explicitly lists web applications, RLHF reward models, distributed-consensus protocols, and compiler optimizations as out of scope. This means NOETHER applies only to programs with explicit mathematical governing equations—a small fraction of the software testing landscape. The paper's abstract and introduction do not adequately convey this restriction; a reader must reach §3.1, Remark 5 to discover it.

### Threats to Validity Not Adequately Addressed

- **Selection bias in SUT choice.** The 10 Java SUTs are from a single class (MathSignalClass + ComplexSignal) pre-selected by the framework's designer to satisfy the scope precondition. The Commons-Math pilot (n=3 SUTs, n=77 mutants) is acknowledged as underpowered.
- **LLM-as-rater validity.** All inter-rater agreement figures use LLM panels. The paper acknowledges shared training data but still reports Fleiss' κ values, which readers will interpret as standard inter-rater reliability.
- **Single-author derivation.** All 30 Set N MRs were derived by a single author. The LRCA audit uses LLMs, not independent human experts.

### What a Revision Must Do

1. **Cut length by 40%+.** One boundary-of-contribution box. Move all protocols, future work, and worked examples to supplements.
2. **Restructure contributions around the IBT and negative results.** Demote Theorem 1 to a lemma. Make the IBT and the Theorem 1' falsification the central theoretical contributions.
3. **Provide credible empirical evidence.** Either (a) run the pre-registered DeepCrime protocol at adequate sample size (n≥50) on independently-authored subjects, or (b) reposition as a purely theoretical paper and remove all claims about practical testing utility.
4. **Validate the eight-block decomposition independently.** Map an external MR corpus (not authored by the paper's team) onto the blocks with independent human raters.
5. **Be honest about the head-to-head.** The aggregate result is that NOETHER loses to GenMorph on fault detection. Present this clearly and argue for the framework's value on other axes (explainability, structural coverage, cost) without burying the detection result in per-block decompositions.