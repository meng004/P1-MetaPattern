```json
{
  "overall_recommendation": "Major Revision",
  "submission_maturity_0to100": 56,
  "acceptance_probability_pct": 30,
  "reviewer_confidence_1to5": 4,
  "dimension_scores_0to100": {
    "originality": 68,
    "methodology_rigor": 50,
    "evidence_sufficiency": 45,
    "argument_coherence": 60,
    "writing_presentation": 55
  },
  "persona_verdicts": {
    "EIC": {
      "recommendation": "Major Revision",
      "headline": "Novel algebraic framing of MR identification with serious scope/self-referentiality concerns and extreme length"
    },
    "R1_methodology_theory": {
      "recommendation": "Major Revision",
      "headline": "Theorem 1 is by-construction tautologous; Theorem 2 'polynomial-time' is output-polynomial not input-polynomial; statistics underpowered with uncorrected multiple comparisons"
    },
    "R2_domain_mt_mr": {
      "recommendation": "Major Revision",
      "headline": "Constructive derivation contribution is real but partially circular (blocks curated from reactor physics then 'predict' reactor physics MRs); EQ1/EQ3 self-referential"
    },
    "R3_perspective_equivariance_safety": {
      "recommendation": "Major Revision",
      "headline": "IBT is the strongest theoretical result but restricted to linear faults and exact arithmetic; industrial witness (SACOS/SPARK/LOCUST) is order-block-only, not independent multi-block validation"
    },
    "devils_advocate": {
      "critical_found": false,
      "strongest_counterargument": "The paper's central 'closure' theorem (Theorem 1) is a well-formedness statement that every element of a set defined as the Translate-image of a domain belongs to the partition of that image—it is true by construction and cannot fail, making it unfalsifiable as an empirical claim. The real scientific content is whether the algebra-induced MR space MR(𝒜_P) captures the MRs practitioners actually need, and the paper's own negative instantiation (§5.5) shows it does not on 𝒜_PWR for two regulatory-essential MRs. The eight blocks were curated by inspecting program families including reactor physics, then the Boltzmann instantiation 'predicts' m_adj and m_rev from those same blocks—this is re-projection, not prediction, as the authors honestly concede (§4.3 caveat). The LLM-panel κ=0.857 and LRCA κ=0.931 are agreement among models sharing training data, not independent verification. The head-to-head is dominated by Set G (McNemar p=0.0043), and the only quantitative falsifiable prediction (ℒ*-blindness) is a deductive consequence of PIT's mutator semantics, not a test of NOETHER's MR-identification claim. The contribution is a notational and organisational advance, not yet a method that produces MRs with demonstrated practical advantage."
    }
  },
  "publication_blockers": [
    {
      "id": "PB1",
      "section": "§3.3 Theorem 1 / §3.4 Theorem 2",
      "issue": "Theorem 1 is by-construction well-formedness (every Translate-image element lands in the Translate-image partition). Its 'closure' label overstates what is proved. Theorem 2's 'polynomial-time' claim is output-polynomial (|G| can be exponential in the input description), not input-polynomial, which the text mentions in a remark but the theorem statement does not qualify.",
      "why_fatal": "Headline theoretical claims that are near-tautological or misleadingly stated undermine the paper's formal-methods credibility at TOSEM's bar.",
      "fixable_by": "writing"
    },
    {
      "id": "PB2",
      "section": "§4.3 / §6 Table 4",
      "issue": "The equivariant-ML case study (n=20 mutations, 1 model, construct-validity-controlled design) and the PIT head-to-head (n=62, dominated by Set G) provide insufficient statistical power for any inferential claim about MR-identification superiority or even non-inferiority. The McNemar p=0.016 for N-vs-B on 20 mutations is a single comparison on a constructed mutation set; the head-to-head p=0.0043 is dominated by out-of-scope D2 stratum contribution.",
      "why_fatal": "The empirical section does not provide adequately powered evidence for the framework's practical value as an MR-identification method. Without at least one adequately powered experiment (n≥30 per stratum, independent mutation source, pre-registered analysis), the paper's empirical contribution rests on a confirmed deductive prediction (ℒ*-blindness) and descriptive case studies.",
      "fixable_by": "experiment"
    }
  ],
  "major_weaknesses": [
    {
      "section": "§4.2 / §4.3",
      "issue": "Blocks T* and 𝒯*_rev were curated partly from reactor-physics structures, then m_adj and m_rev are 'predicted' for the Boltzmann instantiation. The authors concede the circularity but the paper's framing (Table 3 column 'Predicted') still overclaims novelty.",
      "suggested_fix": "Relabel 'Predicted' as 'Re-projected' or 'Structurally separated' in Table 3; add a non-physics domain where T* and 𝒯*_rev produce genuinely novel MRs before the paper's own curation.",
      "fixable_by": "writing"
    },
    {
      "section": "§5.2 / §6 Table 4 / §6.1",
      "issue": "EQ1 and EQ3 evidence is largely author-vs-author: the expert MR sets are the authors' own PWR catalogue; the industrial corpora (SACOS/SPARK/LOCUST) cover only the O_≤ block; the LLM-panel κ is computed among models sharing training data; the cross-domain traces (Table 7) map blocks to published identities rather than testing new MRs against new programs.",
      "suggested_fix": "Add at least one external MR corpus from an independent team (e.g., PARCS V&V suite, Segura et al. IMDb MR set) evaluated by independent human raters. Replace or supplement LLM-panel κ with human inter-rater κ.",
      "fixable_by": "experiment"
    },
    {
      "section": "§5.4 IBT",
      "issue": "IBT is restricted to the linear operator-implementation fault class and exact arithmetic. The paper's empirical subjects (EGNN, Java methods) do not operate in this regime. The IBT empirical validation (E1–E3) uses N=8 linear-algebraic fault classes, not real software faults.",
      "suggested_fix": "Either (a) restrict IBT's claims explicitly to linear-algebraic programs and remove the IBT-corroboration language for non-linear subjects, or (b) add an empirical test of IBT's predictions on a non-linear PDE solver with real faults.",
      "fixable_by": "either"
    },
    {
      "section": "§6.3–6.5",
      "issue": "Multiple comparisons across per-SUT, per-block, and per-stratum analyses are reported without consistent family-wise error control. The McNemar p=0.016 for N-vs-B is one of 3 pairwise tests; the Holm-adjusted p=0.047 barely passes 0.05.",
      "suggested_fix": "Adopt a single pre-registered primary comparison (e.g., D1 stratum Set N vs Set G) and report all others as descriptive/exploratory. Ensure all p-values are Holm-Bonferroni corrected for the number of tests actually performed.",
      "fixable_by": "writing"
    },
    {
      "section": "Entire manuscript",
      "issue": "The paper is extremely long (estimated >25,000 words including appendices and inline supplementary references). TOSEM's soft limit is ~11,000 words. The excessive length includes 16 committed future-work items, multiple tcolorbox restatements of contribution boundaries, and extensive supplementary cross-references that belong in an artifact appendix.",
      "suggested_fix": "Cut the manuscript to ≤15,000 words by: (1) removing all inline future-work commitments to a separate document; (2) merging the three 'Boundary of contribution' tcolorboxes into one; (3) moving the head-to-head per-block decomposition details to an appendix; (4) eliminating the METRIC+ Path A subsection and replacing with a brief summary.",
      "fixable_by": "writing"
    },
    {
      "section": "§2 Related Work",
      "issue": "Three references (Hu et al. 2019; Mariani 2018; Liu et al. 2020) could not be located. Missing key references: Gotlieb 2003/2006 treated only briefly; no engagement with Khritankov-Iakusheva 2024's six transformation families as potential blocks; Saha-Kanewala 2019's low detection rate (14.8%) not discussed as a potential scope limitation.",
      "suggested_fix": "Locate or remove the three missing references. Add explicit comparison of the eight blocks with Khritankov-Iakusheva's six families. Discuss whether Saha-Kanewala's 14.8% detection rate on supervised classifiers reflects a scope limitation for NOETHER (most classifier MRs may be outside the eight-block frame).",
      "fixable_by": "writing"
    }
  ],
  "minor_issues": [
    "Definition 1: The equivalence relation ~_F is defined but never formally used in a proof; its role could be clarified or removed.",
    "Table 2: The 'Conservation' row in EQ1 coverage is a G-block sub-instance, not an independent block; this is noted in prose but the table structure invites misreading.",
    "Eq. (5): ρ_rot uses ‖·‖_∞ with τ=10⁻⁴; no false-positive rate is reported for this tolerance on a non-equivariant baseline.",
    "§5.5: The PWR negative instantiation is strong but the 'five pairwise-independent obstructions' claim in Table 12 should note that independence is proved only on 𝒜_PWR; the 𝒜_equi and 𝒜_rel extensions are 'asserted by inspection'.",
    "Appendix C.6 proofs: The exhaustive block-by-block exclusion for ρ_nonadd is correct but could be compressed; the proof for ρ_MTC-bor is largely redundant with the ρ_nonadd proof and should reference shared obstructions.",
    "§6.4: The 'cross-pipeline rediscovery' witness on midpoint (3 MRs converging) is anecdotal (1 SUT); framing as 'direct corroboration' is too strong.",
    "Set L ensemble (§6.5): The 43.5% block-template match rate is informative but the remaining 56.5% may contain useful out-of-block MRs; the analysis does not evaluate these.",
    "§7: The 16-item committed future-work list is unusually detailed for a paper submission and signals that much of the empirical programme is incomplete."
  ],
  "highest_roi_fixes": [
    {
      "action": "Restate Theorem 1 as a well-formedness/closure lemma (not a 'closure invariant') and Theorem 2 as 'output-polynomial constructibility'; add explicit scope qualifications to both theorem statements.",
      "expected_gain_pp": 8,
      "effort": "low",
      "fixable_by": "writing"
    },
    {
      "action": "Add one adequately powered experiment (n≥30 mutants, independent mutation source e.g. DeepCrime full taxonomy, ≥2 architectures) for a pre-registered primary comparison on the D1 stratum.",
      "expected_gain_pp": 12,
      "effort": "high",
      "fixable_by": "experiment"
    },
    {
      "action": "Relabel 'Predicted' in Table 3 as 'Structurally separated' and add a genuinely external MR corpus (not author's own PWR catalogue) for EQ1/EQ3 validation.",
      "expected_gain_pp": 7,
      "effort": "medium",
      "fixable_by": "experiment"
    },
    {
      "action": "Cut manuscript to ≤15,000 words by removing inline future-work, merging boundary boxes, and moving detailed per-block head-to-head to appendix.",
      "expected_gain_pp": 5,
      "effort": "medium",
      "fixable_by": "writing"
    },
    {
      "action": "Add Khritankov-Iakusheva 2024's six transformation families as an explicit comparison point for the eight blocks, and discuss whether they map onto or extend the current decomposition.",
      "expected_gain_pp": 4,
      "effort": "low",
      "fixable_by": "writing"
    }
  ],
  "summary": "NOETHER proposes an operator-algebraic framework for deriving metamorphic relation classes from program-family governing equations, with a by-construction closure result, an output-polynomial constructibility theorem, an Invariance-Blindness characterization for linear faults, and three domain instantiations plus a negative instantiation on PWR. The algebraic framing is genuinely novel for the MT/MR literature and the negative instantiation is a methodological strength. However, the paper has three fundamental problems. (1) The headline 'closure' theorem is by-construction well-formedness that cannot fail, while the genuinely substantive theoretical result (IBT) is restricted to linear faults and exact arithmetic—neither theorem's scope matches the empirical subjects. (2) The empirical evidence is underpowered and largely self-referential: the expert MR sets are the authors' own, the industrial corpora cover only one block, the LLM-panel agreement is among models sharing training data, and the head-to-head is dominated by GenMorph. The only falsifiable quantitative prediction (ℒ*-blindness) is a deductive consequence of PIT's mutator semantics, not an independent test of the framework. (3) The paper is far too long for TOSEM, with excessive boundary-restatement boxes and 16 committed future-work items that signal an incomplete empirical programme. A major revision that restates the theorems honestly, adds at least one adequately powered independent experiment, and cuts the manuscript length could reach TOSEM's bar; the current version does not."
}
```

---

## Detailed Panel Report

### EIC Perspective

**Scope fit**: The paper addresses MR identification, a core SE problem squarely within TOSEM's scope. The algebraic framing is novel for this community. **Originality**: The operator-algebraic construction is a genuine advance over inductive pattern catalogues, though the by-construction nature of Theorem 1 tempers the theoretical novelty. **Significance**: If the framework produced MRs with demonstrated practical advantages (higher coverage, better maintainability, lower cost) on adequately powered experiments, it would be highly significant; currently the practical payoff is unclear. **Length**: The manuscript is severely over-length (estimated 25,000+ words including the extensive inline apparatus). TOSEM LEN-01 advises return-without-review for manuscripts far exceeding ~11,000 words; this one merits review but the length must be cut drastically. **Desk-reject triggers**: None outright, but the length is borderline.

**EIC verdict**: Major Revision. The framing is novel but the theoretical claims are overstated and the empirical programme is incomplete.

---

### R1 (Methodology/Theory + Statistics) Perspective

**Theorem 1 (Closure)**: The theorem states that every MR in MR(𝒜_P) belongs to some m ∈ 𝕄(𝒜_P). But MR(𝒜_P) is *defined* as the Translate-image of the block decomposition (Definition 6), and 𝕄(𝒜_P) is *constructed* as the partition of that same image (Steps 2–4 of CONSTRUCT-MP). The theorem is therefore a well-formedness lemma: it says the partition covers its own generating set. This is true by construction and unfalsifiable. The authors acknowledge this (§3.3, "a sceptical reading might object that the by-construction status makes it near-tautological") but still headline it as a "no-drop closure invariant." The honest statement is: "CONSTRUCT-MP is a well-defined function from block decompositions to MetaPattern sets." The *substantive* claim—that this function is useful for MR identification—requires empirical evidence that the algebra-induced MR space captures practically important MRs, and the negative instantiation (§5.5) shows it does not for two PWR-safety MRs.

**Theorem 2 (Polynomial-time)**: The theorem states O(n · max_i t_i · log n) where n = |gen(𝒜_P)|. For finite groups, t_i = O(|G|²), and |G| can be exponential in the description length of the algebra (e.g., a permutation group on k elements has |G| ≤ k! but is described by O(k²) generators). The remark in §3.4 acknowledges this ("output-polynomial, not input-polynomial") but the theorem statement itself says "polynomial-time constructibility" without qualification. This must be corrected in the theorem statement itself, not buried in a remark.

**Statistics**: The case study (Table 4) reports McNemar exact p=0.016 (Holm-adjusted p=0.047) for N-vs-B on n=20 mutations. This is one of three pairwise tests; with only 20 mutations the test is fragile (a single mutation flip changes the verdict). The head-to-head (Table 9) reports McNemar p=0.0043 pooled, but this is contaminated by the out-of-scope D2 stratum (3/5 Set G kills inflate the gap). On D1 only, p=0.019 with discordant pairs (15,4)—still significant but the effect size (RD=0.212) favours Set G, not Set N. The DeepCrime pilot (n=5) is explicitly underpowered (p=0.500). No power analysis is reported for any experiment.

**HARKing concerns**: The mutation set in §6.1 was "constructed to cover one defect category per non-empty block" with cat-(iv) selected to target ρ_train-rev. This is construct-validity-controlled design, not hypothesis-testing against a neutral defect distribution. The authors disclose this, but the paper still reports the 5/5 unique detection as if it were evidence.

**R1 verdict**: Major Revision. Theorems must be restated with honest scope qualifications. At least one adequately powered experiment with an independent mutation source is needed.

---

### R2 (MT/MR Domain) Perspective

**Literature coverage**: The paper cites Segura 2016, Zhou 2020, Chen METRIC 2016, Sun METRIC+ 2021, Ying 2025, and the 2024 Li TOSEM survey. Missing or under-engaged: Gotlieb's symmetric testing (ISSRE 2003/2006) is mentioned but not confronted—Gotlieb's permutation-based oracle is arguably a G-block instance, and the paper should explicitly map it. Khritankov-Iakusheva 2024's six transformation families are cited but not compared block-by-block. Saha-Kanewala 2019's 14.8% detection rate on 709 mutants for supervised classifiers is cited but its implications for NOETHER's scope (most classifier MRs may lie outside the eight-block frame) are not discussed.

**Self-referentiality**: The prior inductive catalogue (P1–P5) is the authors' own. The "prediction" of m_adj and m_rev from T* and 𝒯*_rev blocks that were "themselves curated by inspection of program families that include reactor physics" (§4.3 caveat) is circular in the strong reading. The authors' concession is honest but insufficient: the paper should relabel Table 3's "Predicted" column as "Structurally separated" or "Re-projected," and should demonstrate prediction on a domain where the blocks were not curated from that domain's structures.

**MR contribution**: The constructive derivation over the operator-block layer is a real contribution—it provides an algebraic warrant for pattern existence and a mechanism for de-duplication (the deflationary direction in §6.7). But this is a vocabulary and organisational contribution, not yet demonstrated to produce MRs with higher fault-revealing power, better maintainability, or lower identification cost in practice.

**R2 verdict**: Major Revision. The algebraic construction is novel for MT but the evaluation is self-referential and underpowered. An external MR corpus and independent human raters are needed.

---

### R3 (Equivariant ML + Safety-Critical V&V) Perspective

**IBT**: The Invariance-Blindness Theorem (§5.4) is the paper's strongest theoretical result. It characterises the detection kernel of G-block and T*-block MRs as exactly the structure-preserving faults, within the linear fault class and under exact arithmetic. This is non-tautological (it requires the Faithfulness Lemma) and has clear practical implications (single-block batteries are incomplete; differential oracles are complementary). However: (1) The restriction to linear faults excludes the nonlinear PDE solvers that are the paper's primary motivating domain. (2) The exact-arithmetic assumption (Remark 8, R2) means that finite-tolerance MRs have strictly larger kernels; the theorem's tightness does not transfer to the executable regime. (3) The empirical validation (E1–E3) uses N=8 linear-algebraic fault classes, not real software faults.

**Industrial witness**: SACOS, SPARK, and LOCUST are independently developed production codes, which is a strength. However, the 110 expert-approved relations are overwhelmingly order-block (O_≤) relations. This confirms transferability of one block, not of the full decomposition. The LOCUST MTC-vs-boron relation is an independent witness for the §5.5 obstruction, which is valuable, but it also confirms that production MR sets contain MRs outside NOETHER's Translate-reachable space.

**Equivariant ML instantiation**: The five MetaPatterns derived for 𝒜_equi are cross-corroborated by the published literature (Cohen & Welling, SE(3)-Transformer, etc.), but this is citation-based corroboration of the *existence* of the invariants, not of the *testing value* of the derived MRs. The case study's cat-(iv) result (5/5 unique detection for ρ_train-rev) is construct-validity-controlled and the DeepCrime pilot is underpowered.

**R3 verdict**: Major Revision. IBT is valuable but its scope must be honestly delimited. The industrial and equivariant-ML evidence needs at least one adequately powered experiment with real faults.

---

### Devil's Advocate Perspective

**Strongest counterargument**: The paper's central "closure" theorem is unfalsifiable by construction. The real question is whether MR(𝒜_P) captures the MRs practitioners need, and the paper's own negative instantiation shows it does not for two regulatory-essential PWR MRs. The eight blocks were curated from (inter alia) reactor physics, then the Boltzmann instantiation "predicts" MRs from those same blocks—this is re-projection, not prediction. The LLM-panel κ values are inflated by shared training data. The head-to-head is dominated by Set G. The only falsifiable quantitative prediction (ℒ*-blindness) is a deductive consequence of PIT's mutator design, not a test of NOETHER's MR-identification claim. The contribution is organisational and notational: it provides a uniform algebraic vocabulary for classifying MRs that already exist and a mechanism for de-duplicating pattern catalogues. This is useful but not yet demonstrated to be practically superior to existing methods for *identifying* new MRs.

**No CRITICAL found**: The paper is honest about its limitations (multiple boundary boxes, explicit scope statements). The circularity in the Boltzmann "prediction" is disclosed. The negative instantiation is a genuine strength. These prevent a fatal flaw but do not resolve the major weaknesses.

---

### Threats to Validity Summary

1. **Construct**: Mutation sets are hand-constructed to target specific blocks (§6.1); LLM-panel κ is not equivalent to human inter-rater reliability; Path A Java re-implementations are by the framework's author.
2. **Internal**: The canonical-block ordering is arbitrary and affects which block "owns" a multi-derivable MR; no sensitivity analysis is reported.
3. **External**: All empirical subjects are from two codebases (MathSignalClass + Commons Math for Java; EGNN for ML); no cross-codebase replication at powered scale. The eight blocks may not transfer to program families outside the construction set.
4. **Conclusion**: The ℒ*-blindness prediction is confirmed but is a deductive consequence, not an inductive test. The head-to-head D1 result favours Set G. The paper's claims about MR-identification value are not adequately supported by the current empirical programme.

---

### What a Revision Must Do

1. **Restate theorems honestly**: Theorem 1 becomes a well-formedness lemma; Theorem 2 becomes "output-polynomial constructibility under finite generating set with per-generator cost t_i." Move the overstatement corrections from remarks into the theorem statements.
2. **Add one powered experiment**: Minimum n=30 mutants per stratum, independent mutation source (DeepCrime full taxonomy or real bug commits), ≥2 architectures or codebases, single pre-registered primary comparison (D1 stratum, Set N vs best baseline).
3. **External MR corpus**: Evaluate against at least one MR set from an independent team (PARCS V&V, Segura QBS MR set, or similar) with independent human raters.
4. **Cut length to ≤15,000 words**: Remove inline future-work (16 items → supplementary document), merge three boundary boxes into one, move per-block head-to-head details to appendix, compress the METRIC+ subsection.
5. **Correct Table 3 labelling**: Change "Predicted" to "Structurally separated" and add a genuinely external prediction (e.g., a domain whose blocks were not curated from that domain).
6. **Add Khritankov-Iakusheva comparison**: Map their six transformation families against the eight blocks explicitly.
7. **Delimit IBT scope**: Add explicit statement that IBT does not apply to nonlinear programs or finite-tolerance MRs; remove or qualify IBT-corroboration language for non-linear subjects.