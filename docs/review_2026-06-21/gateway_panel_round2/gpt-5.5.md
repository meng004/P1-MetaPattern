```json
{
  "overall_recommendation": "Reject",
  "submission_maturity_0to100": 49,
  "acceptance_probability_pct": 12,
  "reviewer_confidence_1to5": 4,
  "dimension_scores_0to100": {
    "originality": 72,
    "methodology_rigor": 45,
    "evidence_sufficiency": 42,
    "argument_coherence": 48,
    "writing_presentation": 40
  },
  "persona_verdicts": {
    "EIC": {
      "recommendation": "Reject",
      "headline": "Strong scope fit and a potentially interesting algebraic framing, but the manuscript is far beyond TOSEM length/discipline and mixes theorem, manifesto, protocols, pilots, appendices, and future-work claims into an unreviewable submission."
    },
    "R1_methodology_theory": {
      "recommendation": "Reject",
      "headline": "The main closure theorem is largely definitional, the complexity theorem is output/description-polynomial under assumed termination, and the empirical/statistical evidence is dominated by underpowered pilots, constructed denominators, post-hoc caveats, and non-independent labelling."
    },
    "R2_domain_mt_mr": {
      "recommendation": "Reject",
      "headline": "NOETHER's delta over existing MT/MR pattern, symmetry, METRIC/METRIC+, and automated MR-identification work remains over-claimed; much evaluation reclassifies the authors' own MR catalogues or author-derived MRs."
    },
    "R3_perspective_equivariance_safety": {
      "recommendation": "Major Revision",
      "headline": "The invariance-blindness idea and safety-critical reactor counterexamples are interesting, but the ML and industrial evidence do not yet provide independent validation of the claimed cross-domain transfer or practical payoff."
    },
    "devils_advocate": {
      "critical_found": true,
      "strongest_counterargument": "The central claim is that operator algebra constructively identifies MR MetaPatterns and exposes completeness boundaries. But the framework largely moves the hard identification step into the manually curated operator algebra and block decomposition, then proves closure over the image of its own Translate operator. Theorem 1 is therefore not a discovery theorem; it is a well-formedness lemma over a self-defined set. The claimed empirical support is similarly circular: reactor patterns are compared against the authors' own prior catalogue, NOETHER MRs are author-derived, coverage_N is 1.00 by construction, construct-trace mutants are deliberately targeted at Set N MRs, LLM raters are used as pseudo-independent validators, and several stronger comparative arms are protocols, follow-up, or adapted estimates rather than executed independent baselines. When a fully executable head-to-head is reported, GenMorph dominates Set N in the aggregate D1 stratum, and the manuscript reframes this as per-block complementarity and cost-axis value. The PWR negative examples honestly delimit Translate, but they also show that important safety MRs lie outside the claimed construction. Thus the paper has an interesting algebraic vocabulary, but the submitted version has not demonstrated that NOETHER independently discovers useful MR patterns beyond expert domain modelling and author-curated examples."
    }
  },
  "publication_blockers": [
    {
      "id": "B1",
      "section": "Whole manuscript; Introduction; Data and Artifact Availability; Appendices",
      "issue": "Severe length and structural noncompliance: the manuscript reads as multiple papers plus supplementary material, with many protocols, future-work items, repeated boundary boxes, and large appendices embedded in the main submission.",
      "why_fatal": "At TOSEM's bar this is likely return-without-review or reject-on-form. The central contribution cannot be evaluated reliably because claims, evidence, limitations, protocols, and appendices are interleaved across an excessive manuscript.",
      "fixable_by": "writing"
    },
    {
      "id": "B2",
      "section": "Sections 3.2, 3.4, 4.1, 4.2, 4.3; Tables 3-15; Threats to Validity",
      "issue": "Evidence base is insufficiently independent and often circular: author-derived Set N, authors' prior PWR catalogue, author re-implementations of METRIC+ subjects, LLM-only labelling, construct-targeted mutants, and coverage metrics that equal 1.00 by construction.",
      "why_fatal": "The submission's main maturity claim is empirical-methodological, but the load-bearing evaluations do not establish independent MR-identification benefit or practical payoff. This cannot be repaired by prose alone.",
      "fixable_by": "experiment"
    },
    {
      "id": "B3",
      "section": "Theorem 1; Definition 6-8; Section 3.2; Appendix C.4-C.6",
      "issue": "The main theoretical contribution is over-positioned relative to its content: closure is by construction over MR(A_P) defined as Translate's image; absolute completeness is falsified; major useful PWR MRs lie outside Translate.",
      "why_fatal": "A TOSEM theory-method paper must make clear what non-tautological theorem is established. The current manuscript repeatedly uses modest disclaimers, but still frames the theory as a foundational answer to origin-closure-transferability beyond what is proved.",
      "fixable_by": "either"
    },
    {
      "id": "B4",
      "section": "Sections 4.2-4.3; Tables 7-15; Section 5",
      "issue": "Comparative evaluation does not support the implied practical advantage over SOTA. GenMorph dominates on the aggregate D1 head-to-head; MR-Scout is not rerun; METRIC+ comparison uses re-implemented subjects and reduced enumerations; LLM comparison is template-matched to Set N.",
      "why_fatal": "The paper asks readers to prefer NOETHER as an MR-identification framework, but the executed comparisons either favor the baseline, are not independent, or measure structural coverage rather than user-visible value.",
      "fixable_by": "experiment"
    }
  ],
  "major_weaknesses": [
    {
      "section": "Introduction; Contributions C1-C5",
      "issue": "Contribution list is too broad and internally inconsistent: it simultaneously claims constructive identification, closure, negative completeness, invariance-blindness, industrial witness, cross-domain transfer, cost advantage, and empirical falsifiability.",
      "suggested_fix": "Reduce to one paper: either a theory paper on Translate/IBT plus negative PWR boundaries, or an empirical MR-identification paper with independent corpora and baselines. Remove claims not directly supported.",
      "fixable_by": "writing"
    },
    {
      "section": "Hypothesis 1; Remarks 4-8",
      "issue": "The eight-block decomposition is empirical curation but is treated throughout as if it has broad structural authority.",
      "suggested_fix": "Provide a pre-registered, independently labelled corpus of program families and candidate operators; report precision/recall of the block taxonomy and human inter-rater agreement.",
      "fixable_by": "experiment"
    },
    {
      "section": "Theorem 2; Table 1",
      "issue": "The complexity claim is weak and potentially misleading: per-generator invariant extraction is assumed to terminate; finite groups can be exponential in description; query equivalence is undecidable outside fixed-rule fragments.",
      "suggested_fix": "Rename as an output-polynomial construction bound under explicit oracle assumptions; remove any implication of input-polynomial decidability.",
      "fixable_by": "writing"
    },
    {
      "section": "Section 3.4 Invariance-Blindness Theorem",
      "issue": "IBT is interesting but narrowly scoped to linear exact-arithmetic faults for G and T*; empirical support is in supplementary material and not integrated as a primary, clean evaluation.",
      "suggested_fix": "Make IBT the paper's main theorem, give a formal statement with assumptions in the main text, and provide one concise, reproducible experiment focused on faithfulness and kernel complementarity.",
      "fixable_by": "either"
    },
    {
      "section": "Section 3.5 Reactor instantiation; Table 2; Section 4.1 Table 3",
      "issue": "Reactor evidence is heavily self-referential: the prior catalogue is by the same authors, industrial relations mostly show O_le monotonicity, and additional blocks are often latent rather than executable.",
      "suggested_fix": "Use an independently authored reactor V&V MR corpus or production test suite; require independent domain experts to classify whether NOETHER-derived MRs are valid and executable.",
      "fixable_by": "experiment"
    },
    {
      "section": "Section 3.6 Equivariant ML; Sections rho_adj and rho_train-rev",
      "issue": "Several ML MRs are debug-time or architecture-instrumented rather than natural user-level metamorphic relations; the EGNN stand-in does not instantiate the full attention/self-adjoint claims.",
      "suggested_fix": "Evaluate on actual SE(3)-Transformer/e3nn/NequIP/MACE systems with native hooks and real defects; separate CI-executable MRs from debug probes.",
      "fixable_by": "experiment"
    },
    {
      "section": "Section 4.2; Table 6",
      "issue": "The 20-mutation case study is construct-validity controlled by design, and the unique 5/5 detection cell targets an MR only Set N contains.",
      "suggested_fix": "Replace with a larger real-fault or independently generated mutant set; pre-register categories without aligning each category to Set N's blocks.",
      "fixable_by": "experiment"
    },
    {
      "section": "Section 4.3; Tables 11-14",
      "issue": "Head-to-head interpretation is over-elaborate and defensive. The aggregate result favors GenMorph, but the paper diffuses this through per-block, D2, and cost narratives.",
      "suggested_fix": "State plainly that NOETHER is not competitive on aggregate mutation detection in this substrate, then claim only complementarity/cost where measured.",
      "fixable_by": "writing"
    },
    {
      "section": "Threats to Validity",
      "issue": "LLM-based Fleiss/Cohen kappa is repeatedly used as reliability evidence despite shared pretraining and lack of domain-expert independence.",
      "suggested_fix": "Remove reliability claims based on LLM-only raters or downgrade them to debugging checks; obtain independent human expert labels.",
      "fixable_by": "experiment"
    },
    {
      "section": "Data and Artifact Availability",
      "issue": "Artifact claims are inconsistent: many sections cite S7-S12 and Zenodo DOI, but the review-stage archive list only includes S1-S4; no repository access is assumed in this review.",
      "suggested_fix": "Provide a single manifest, stable anonymized archive, exact hashes, and mapping from every table/claim to a script and raw data file.",
      "fixable_by": "writing"
    }
  ],
  "minor_issues": [
    "The manuscript is not anonymized despite saying it is: author names, emails, funding, Zenodo DOI, arXiv DOI, and institution information are present.",
    "The title alternates between 'discovery' in comments and 'identification' in the manuscript; settle the terminology.",
    "The block count is inconsistent rhetorically: 'seven blocks', 'eight blocks', conservation as not a block, and candidate ninth blocks appear in multiple places.",
    "Some table labels and references contain spaces or unusual names, e.g., Table 'obstruction set', which is poor LaTeX practice.",
    "Several claims cite supplementary files rather than presenting enough information in the main text to review them cold.",
    "Repeated tcolorbox 'Boundary of contribution' summaries clutter the narrative.",
    "The paper sometimes uses 'prediction' for reclassification of textbook-known phenomena; this invites overclaiming.",
    "The Data Availability section duplicates a later Data Availability Statement with different supplementary inventories.",
    "The abstract is more precise than the body; the body should follow the abstract's narrower MR-identification framing.",
    "Multiple future-work commitments are written as if they are evidence; they should be removed or clearly separated."
  ],
  "highest_roi_fixes": [
    {
      "action": "Split the manuscript and submit only one coherent paper: preferably the NOETHER theory plus PWR negative boundary plus one clean independent evaluation, under 11k-13k words.",
      "expected_gain_pp": 15,
      "effort": "high",
      "fixable_by": "writing"
    },
    {
      "action": "Obtain an independent MR corpus and independent human expert labelling for at least two domains, replacing author-vs-author and LLM-only kappa evidence.",
      "expected_gain_pp": 12,
      "effort": "high",
      "fixable_by": "experiment"
    },
    {
      "action": "Reframe Theorem 1 as a well-formedness lemma and make IBT or the PWR Translate-boundary result the main non-tautological theoretical contribution.",
      "expected_gain_pp": 8,
      "effort": "medium",
      "fixable_by": "writing"
    },
    {
      "action": "Run one fair, fully executed baseline comparison against GenMorph, METRIC+/manual categories, MR-Scout where applicable, and LLMs on the same subjects, with pre-registered metrics and independent equivalent-mutant adjudication.",
      "expected_gain_pp": 10,
      "effort": "high",
      "fixable_by": "experiment"
    },
    {
      "action": "Replace constructed mutation categories with real defects or independently generated mutants, and report clustered/paired analyses without treating structural coverage as empirical success.",
      "expected_gain_pp": 7,
      "effort": "high",
      "fixable_by": "experiment"
    },
    {
      "action": "Create a single artifact manifest mapping every table and statistic to scripts/data, and remove all unsupported supplementary references from the main text.",
      "expected_gain_pp": 4,
      "effort": "medium",
      "fixable_by": "writing"
    }
  ],
  "summary": "The manuscript contains a potentially publishable idea—using operator-algebraic structure to organize MR MetaPatterns and to state explicit boundaries—but the submitted version is not TOSEM-ready. It is far too long, theoretically over-positioned, empirically self-referential, and comparative evidence is either weak, constructed, future-work, or unfavorable in aggregate. A major redesign with independent evidence and a much narrower claim is required."
}
```

## Panel report

### Overall decision

**Reject.** The paper has a real idea, but the submitted manuscript is not mature enough for TOSEM. The strongest path to publication is not incremental editing; it requires substantial narrowing, new independent evidence, and a reframing of the theory away from “foundational closure” toward a more modest and defensible contribution.

The maturity score is **49/100**, computed from:

\[
72(0.20)+45(0.25)+42(0.25)+48(0.15)+40(0.15)=49.35.
\]

Rounded: **49**.

This is just below the Major Revision band under the supplied rubric, but the combination of form/length, circular evaluation, and overclaimed theory makes **Reject** the appropriate TOSEM recommendation.

---

## 1. EIC lens: scope, significance, TOSEM fit, desk-reject risk

### Verdict: Reject

The topic is in scope for TOSEM: MR identification, test-oracle problems, metamorphic testing, and structural testing methods are central software-engineering topics. The operator-algebraic framing is also potentially valuable if disciplined.

However, the current manuscript is likely to fail editorial triage.

### 1.1 Severe length and structure problem

**Whole manuscript; Introduction; Sections 3–5; Appendices; Data Availability.**

The paper reads like several manuscripts combined:

1. A theory paper on operator-algebraic MR construction.
2. A negative-completeness paper on PWR counterexamples.
3. An invariance-blindness theorem paper.
4. A Java/GenMorph empirical comparison paper.
5. A METRIC+/NOETHER comparison paper.
6. An equivariant-ML MR case study.
7. A reactor-industrial witness report.
8. A supplementary artifact manifesto.

TOSEM can handle long method papers, but this is not just long; it is structurally uncontrolled. The repeated “Boundary of contribution” boxes, future-work inventories, supplementary cross-references, and multiple overlapping evaluation sections prevent a reviewer from identifying the load-bearing contribution.

**Fixability:** writing, but high effort. The paper should be split or radically compressed. A plausible TOSEM submission would have one central contribution, one or two evaluations, and the rest moved to supplementary material or future work.

### 1.2 Contribution overbreadth

**Introduction, C1–C5.**

The paper claims:

- constructive MR-class identification;
- closure;
- polynomial-time constructibility;
- negative theory;
- invariance-blindness;
- reactor instantiation;
- equivariant-ML transfer;
- relational optimizer transfer;
- GenMorph comparison;
- LLM comparison;
- METRIC+ comparison;
- industrial evidence;
- PMCM reformulation;
- cost advantage.

No single submission can convincingly establish all of these at TOSEM’s bar, especially when many are only partially executed or self-referential.

### 1.3 Anonymity and artifact inconsistency

**Author block; Acknowledgements; Data and Artifact Availability.**

The manuscript says “Anonymised for review” but includes:

- author names;
- emails;
- ORCIDs;
- institutions;
- funding;
- industry grant;
- Zenodo DOI;
- arXiv DOI.

This is a formal problem if submitted to a double-blind track. Even if TOSEM’s exact review model permits identities, the manuscript is internally inconsistent.

The artifact section also lists only S1–S4 in the review-stage archive, while the body relies on S7–S12 for many claims.

---

## 2. R1 methodology/theory/statistics lens

### Verdict: Reject

### 2.1 Theorem 1 is essentially definitional

**Definitions 6–8; Theorem 1; Appendix C.**

Theorem 1 states that every MR in \(\mathrm{MR}(\mathcal{A}_P)\) belongs to a MetaPattern. But \(\mathrm{MR}(\mathcal{A}_P)\) is defined as the image of `Translate` from block invariants, and CONSTRUCT-MP constructs MetaPatterns from those same block invariants.

Thus the theorem is a no-drop/well-formedness lemma, not a substantive completeness theorem. The manuscript often acknowledges this, but the paper’s framing still uses “closure”, “structural adequacy”, and “foundational answer” language that gives the theorem more importance than it has.

**Fixability:** partly writing. If Theorem 1 is retained, it should be called something like “well-formedness of the quotient construction.” The main theory should instead be the PWR negative result or the Invariance-Blindness Theorem.

### 2.2 Theorem 2 is weak and should not be sold as polynomial-time in the usual sense

**Theorem 2; Table 1; Section 3.2.3.**

The theorem assumes:

- finite generating set;
- per-generator invariant extraction terminates in time \(t_i\);
- finite or truncated groups;
- fixed-rule-set relational equivalence;
- no general query-equivalence decidability.

The manuscript eventually says “description/output polynomial, not input polynomial.” That is good, but the title “Complexity and decidability” and the repeated “polynomial-time constructibility” phrasing remain stronger than the result.

**Fixability:** writing. Rename and narrow the theorem.

### 2.3 Invariance-Blindness Theorem is more promising but too isolated

**Section 3.4; Section 4.7.**

The IBT is the most interesting formal result. It states a kernel characterization for \(G\) and \(T^*\) blocks under:

- linear operator-implementation fault class;
- exact arithmetic;
- faithful finite witness set;
- linear \(E_s\).

This is nontrivial enough to build a paper around, but here it is buried among many other claims. The empirical evidence in Section 4.7 is partly summarized but heavily dependent on supplementary S10.

**Fixability:** either. The theorem could be made central by rewriting. But if it is to support practical claims, a cleaner in-paper experiment is needed.

### 2.4 Statistical evidence is often underpowered or misaligned

Examples:

- **Table 6 / Section 4.2:** 20 mutations, one small EGNN, constructed categories, 5/5 unique detections by the MR designed for that category.
- **Table 7:** DeepCrime-style pilot \(n=5\), explicitly underpowered.
- **D2 stratum:** \(0/5\), Wilson upper bound 0.434; cannot confirm a \(\le 10\%\) claim.
- **Table 13 / D1 head-to-head:** Set G dominates Set N on D1, McNemar \(p=0.019\).
- **LLM Set L:** deterministic template matching against Set N makes Set L a subset of Set N; this is not a fair independent LLM baseline for fault detection.

The manuscript often reports proper caveats, but then still uses the same material as support for the broader framework.

### 2.5 Non-independent reliability evidence

**Threats to Validity; Reactor audit; LRCA audit.**

The paper reports Fleiss/Cohen kappa based on LLM raters. This is not equivalent to independent human expert labelling. Shared pretraining, similar prompt interpretation, and lack of domain accountability make these weak reliability checks.

**Fixability:** experiment. Need independent human raters.

---

## 3. R2 MT/MR domain lens

### Verdict: Reject

### 3.1 Literature coverage is broad but the delta remains unclear

The related work section covers many relevant works: Chen, Segura, METRIC/METRIC+, MR-Scout, GenMorph, LLM MR generation, Gotlieb symmetric testing, MemoRIA, Patel-Hierons, Khritankov-Iakusheva, etc.

However, breadth is not the same as a sharp delta. The paper’s real contribution seems to be:

> Given a manually curated operator-block decomposition, define a quotient over block-derived MR templates and use it to classify MR MetaPatterns.

That is more modest than “constructive pattern identification from operator algebras.”

### 3.2 “Prediction” is mostly reclassification

**Section 3.5; Table 2.**

For reactor physics, the paper says NOETHER “predicts” \(m_{\mathrm{adj}}\) and \(m_{\mathrm{rev}}\). But it also admits:

- the prior PWR catalogue is by the same authors;
- \(T^*\) and time-reversal blocks were partly curated from reactor physics;
- adjoint reciprocity and time reversal are textbook phenomena.

This is not strong external prediction. It is a re-projection of known physics into the NOETHER vocabulary.

The manuscript eventually says this, but the claims remain too rhetorically ambitious.

### 3.3 Self-referential MR identification

Sections 3.5, 4.1, 4.2, 4.3, and 5 repeatedly rely on author-derived:

- operator decompositions;
- Set N MRs;
- PWR catalogues;
- Java SUTs or re-implementations;
- block labels;
- construct-targeted mutants.

For an MR-identification method paper, this is a central problem. The main evaluation must show that the framework helps identify valid, useful, non-obvious MRs beyond the authors’ own modelling choices.

### 3.4 METRIC+ comparison is not yet strong

**Section 4.6; Path A.**

The METRIC+ comparison is interesting but problematic:

- Java subjects are reimplemented from Sun 2021’s prose specification by the framework authors.
- MR enumeration is below Sun’s full cardinality.
- Equivalent-mutant vote not fully run.
- The result is parity/complementarity, not superiority.
- The manuscript treats compression as a benefit, but does not show that the compressed representation helps testers in practice.

**Fixability:** experiment. Use original artifacts or independent reimplementation; compare human effort and MR quality under matched protocols.

---

## 4. R3 equivariant-ML / safety-critical V&V lens

### Verdict: Major Revision leaning Reject

R3 sees more promise than the other lenses, especially in:

- PWR negative counterexamples;
- explicit boundary of Translate;
- IBT kernel characterization;
- cross-domain ambition.

But the evidence remains immature.

### 4.1 PWR negative result is valuable

**Section 3.8; Appendix C.6; Table obstruction set.**

The negative PWR instantiation is one of the most convincing parts of the paper. The two MRs:

1. non-additivity of rod-bank reactivity worth;
2. mixed \(T_{\mathrm{mod}}\)-vs-\(C_B\) dependence of \(k_{\mathrm{eff}}\);

are plausible, domain-important examples that the current Translate signature cannot express.

This is a genuine contribution because it shows where the proposed construction fails and identifies missing expressivity dimensions.

However, this result undercuts any strong completeness rhetoric. It should be central to a more honest paper:

> NOETHER provides a disciplined, block-based MR-class construction and exposes precise expressivity gaps.

That would be a more credible contribution.

### 4.2 Equivariant ML claims are not adequately validated

**Section 3.6; Section 4.2.**

The paper derives several MRs for equivariant ML:

- rotation invariance;
- permutation invariance;
- training-size/stability;
- adjoint-attention duality;
- training-trajectory reversal.

Problems:

- \(\rho_{\mathrm{rot}}\) is already obvious and widely used.
- \(\rho_{\mathrm{adj}}\) requires forward hooks or symmetrized probes; in the EGNN case, the self-adjoint probe is explicitly added, not native.
- \(\rho_{\mathrm{train\text{-}rev}}\) is debug-time, vanilla-SGD-specific, and fails by construction on Adam/AdamW pipelines.
- The evaluation uses a compact EGNN stand-in, not the SE(3)-Transformer attention structure used to motivate \(T^*\).

This does not yet establish practical transfer to equivariant-ML testing teams.

### 4.3 Industrial evidence is mostly monotonicity

**Section 5, out-of-construction transferability.**

The industrial SACOS/SPARK/LOCUST evidence mainly shows that many expert-approved relations fall into \(O_{\le}\). That supports monotonicity as a common expert MR pattern, but does not validate the full eight-block decomposition.

The paper is honest that this corroborates \(O_{\le}\), not the full decomposition, but the broader transferability claim still leans on it.

---

## 5. Devil’s Advocate: strongest challenge

The strongest challenge is that NOETHER’s core “constructive discovery” claim is substantially circular.

The hard work in MR identification is knowing what structure matters. NOETHER places that work in the upstream human curation of \(\mathcal{A}_P\) and \(\mathcal{D}(\mathcal{A}_P)\). Once those blocks and invariants are manually supplied, CONSTRUCT-MP mechanically emits MR classes and Theorem 1 proves that the emitted classes cover the emitted classes. That is not false, but it is much weaker than the paper’s ambition.

The empirical evaluation follows the same pattern: author-derived MRs are checked against author-derived mutants or author-labelled corpora, then structural coverage is reported as 1.00 by construction. When outside baselines are executed, the strongest result is not superiority but complementarity or aggregate underperformance. The manuscript frequently discloses these limitations, but disclosure does not convert them into evidence.

This is a **critical** issue because it affects the central claim, not a peripheral experiment.

---

## Publication blockers in detail

### Blocker B1: Length and structure

**Sections:** whole manuscript.

This must be fixed before any serious review. The paper should be reduced by at least 50–70%. Move most of:

- detailed GenMorph tables;
- METRIC+ replication;
- Java SUT details;
- future-work tables;
- artifact manifest detail;
- repeated boundary boxes;
- appendices;

to supplementary material.

### Blocker B2: Lack of independent evidence

**Sections:** 3.5, 4.1–4.6, 5.

A TOSEM-ready version needs at least one independent, load-bearing evaluation. Examples:

- independent domain experts derive \(\mathcal{A}_P\) and MRs using NOETHER;
- independent MR corpus classified blind by human raters;
- external production test suite where NOETHER predicts MRs not in the expert set and engineers validate executability/usefulness;
- fair baseline comparison on the same subject/mutant/test corpus.

### Blocker B3: Theoretical overpositioning

**Sections:** Theorem 1, Theorem 2, Appendix C.

The paper should stop treating Theorem 1 as a central completeness/closure result in a substantive sense. It is a construction invariant. The PWR negative result and IBT are stronger candidates for the central theory.

### Blocker B4: Comparative evaluation mismatch

**Sections:** 4.2–4.6.

The paper must clearly distinguish:

- structural classification;
- MR generation cost;
- mutation detection;
- real-fault detection;
- human usability;
- maintainability.

Currently these are mixed together, and when one metric is weak, another is invoked.

---

## Dimension-by-dimension scoring rationale

### Originality: 72/100

The operator-algebraic framing and explicit Translate-boundary analysis are original enough to be interesting. The PWR negative examples and IBT kernel framing are potentially publishable.

The score is not higher because much of the substantive MR content is known under other names: symmetry testing, adjoint reciprocity, monotonicity, convergence, relational rewrite equivalence, and method comparison. The paper’s novelty is mostly organizational/formal, not empirical discovery.

### Methodology rigor: 45/100

Strengths:

- explicit definitions;
- candid limitations;
- paired tests where applicable;
- some Wilson intervals and McNemar tests;
- negative examples instead of only positive evidence.

Weaknesses:

- circular definitions;
- self-generated MR sets;
- author-derived baselines;
- underpowered pilots;
- LLM-only reliability;
- constructed mutants;
- protocols presented alongside results;
- uneven baseline execution.

### Evidence sufficiency: 42/100

The evidence is abundant in volume but insufficient in independence and alignment. The paper provides many signals, but few are decisive. The strongest independent-looking head-to-head favors GenMorph on aggregate D1.

### Argument coherence: 48/100

The paper repeatedly narrows claims, then expands them again. It is internally aware of its weaknesses but does not restructure around them. The reader is left with an unstable claim boundary.

### Writing & presentation: 40/100

The prose is polished sentence by sentence, but the manuscript is not presentationally acceptable. It is far too long, repetitive, and overburdened with tables, caveats, and supplementary references.

---

## Required revision path for TOSEM acceptability

A viable revision should do the following.

### 1. Choose one main paper

Recommended version:

> **A theory-method paper on algebra-induced MR classes, with a precise well-formedness construction, an Invariance-Blindness theorem, and PWR counterexamples showing Translate’s expressivity boundary.**

Then include only one concise empirical demonstration.

Alternative version:

> **An empirical MR-identification paper comparing NOETHER against METRIC+/GenMorph/MR-Scout/LLM baselines on independent corpora.**

Do not try to publish both in one manuscript.

### 2. Reframe the theory

- Rename Theorem 1 as a construction/well-formedness theorem.
- Stop implying absolute or practical completeness.
- Make the PWR negative result a first-class contribution.
- Clarify that \(\mathcal{A}_P\) distillation is the hard human step.
- Make Hypothesis 1 an empirical taxonomy, not a quasi-axiom.

### 3. Provide independent validation

At minimum:

- independent human raters for block labels;
- independent MR corpus not authored by the paper’s authors;
- independent subject implementations for METRIC+ comparison;
- real or independently generated defects not constructed to match Set N blocks.

### 4. Clean up statistics

- Treat coverage_N = 1.00 as a design property, not an empirical result.
- Do not use underpowered \(n=5\) pilots as evidence beyond feasibility.
- Use clustered/paired analyses where multiple mutants are nested within SUTs.
- Report effect sizes and confidence intervals without rhetorical overinterpretation.
- Remove or demote LLM-only kappa.

### 5. Fix presentation

- Target TOSEM length.
- Remove repeated caveat boxes.
- Move appendices and detailed experiment logs to supplementary material.
- Provide a single artifact manifest.
- Ensure anonymization policy is followed.
- Use consistent terminology: “identification” vs “discovery,” “block” vs “MetaPattern,” “coverage” vs “fault detection.”

---

## Bottom line

The manuscript is not ready for TOSEM. It contains ingredients of a strong paper, especially the PWR boundary analysis and the invariance-blindness theorem, but the current submission overclaims, overextends, and relies too heavily on self-generated evidence. A focused, shorter, independently validated revision could become competitive; this version should be rejected.