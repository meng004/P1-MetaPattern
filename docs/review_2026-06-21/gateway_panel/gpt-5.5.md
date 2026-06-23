```json
{
  "overall_recommendation": "Reject",
  "submission_maturity_0to100": 37,
  "acceptance_probability_pct": 6,
  "reviewer_confidence_1to5": 4,
  "dimension_scores_0to100": {
    "originality": 58,
    "methodology_rigor": 37,
    "evidence_sufficiency": 34,
    "argument_coherence": 31,
    "writing_presentation": 22
  },
  "persona_verdicts": {
    "EIC": {
      "recommendation": "Reject",
      "headline": "In scope and potentially interesting, but not submission-ready: extreme length, unstable contribution boundary, self-referential evidence, and theory/evidence overreach would likely trigger return-without-review or a severe reject."
    },
    "R1_methodology_theory": {
      "recommendation": "Reject",
      "headline": "Theorem 1 is largely definitional closure, Theorem 2 is not a meaningful polynomial-time input-complexity result, and the empirical/statistical claims are fragmented, underpowered, selectively framed, and often construct-validity-controlled."
    },
    "R2_domain_mt_mr": {
      "recommendation": "Reject",
      "headline": "The MT/MR novelty is overstated: many claimed patterns are known symmetry, monotonicity, convergence, reciprocity, and query-equivalence ideas repackaged under an operator-block vocabulary, with weak independent validation of MR identification payoff."
    },
    "R3_perspective_equivariance_safety": {
      "recommendation": "Reject",
      "headline": "The equivariant-ML and safety-critical legs are not yet independent validation: the ML case is a tiny constructed EGNN study, and the reactor industrial evidence is mostly monotonicity plus author-curated or inaccessible witness material."
    },
    "devils_advocate": {
      "critical_found": true,
      "strongest_counterargument": "The central claim is vulnerable to a circularity objection. NOETHER says it constructively identifies MR MetaPatterns from an operator algebra, but the hard part is precisely the human choice of the operator algebra and block decomposition. Hypothesis 1 is admitted to be an empirical curation, partly induced from the same reactor-physics material later used to show that NOETHER reproduces, refines, and predicts patterns. Theorem 1 then closes only the set of MRs defined as reachable by Translate; this is a no-drop property of the construction, not evidence that the construction discovers the MR design space. The negative PWR results are useful, but they mostly prove the authors' own Translate signature is too weak, not that the positive framework is mature. The empirical sections compound the problem: Set N is author-derived, many labels are audited by LLMs rather than independent domain experts, the equivariant-ML mutation categories are constructed so one NOETHER MR uniquely detects one category, and head-to-head results show GenMorph dominates on the D1 aggregate. Self-disclosure of these limitations does not cure them. The paper has an appealing vocabulary for organizing algebraic MRs, but the evidence does not yet establish constructive discovery, independent transfer, or practical superiority over existing MR-pattern and automated-generation methods."
    }
  },
  "publication_blockers": [
    {
      "id": "B1",
      "section": "Whole manuscript; especially Sections 1-7 and appendices",
      "issue": "Extreme length, repetition, and uncontrolled scope far beyond a TOSEM article, with multiple tcolorbox boundary restatements, long protocol/future-work digressions, and appendices still embedded despite claims of migration.",
      "why_fatal": "This is likely return-without-review under TOSEM length/structure expectations. The paper reads as several papers plus a lab notebook and supplementary manifest, not a disciplined journal article.",
      "fixable_by": "writing"
    },
    {
      "id": "B2",
      "section": "Theorem 1 / Definition 3.9 / Section 3.2.3; Appendix C.4-C.6",
      "issue": "Core theoretical result is largely by definition: MR(A_P) is defined as the Translate image, and Theorem 1 proves every Translate-reachable MR is assigned to a MetaPattern.",
      "why_fatal": "The main advertised closure contribution cannot carry the claimed foundational weight. The negative PWR counterexamples further show that the meaningful stronger completeness claim fails under the current construction.",
      "fixable_by": "either"
    },
    {
      "id": "B3",
      "section": "Hypothesis 1; Section 3.1.8; Section 3.4 Boltzmann instantiation; Section 7 threats",
      "issue": "Upstream block decomposition is author-curated and partly induced from the same domains used for validation, creating circularity in the claimed pattern prediction/refinement.",
      "why_fatal": "Without independent block extraction and held-out domain validation, the paper cannot substantiate constructive MR identification rather than post-hoc algebraic recoding.",
      "fixable_by": "experiment"
    },
    {
      "id": "B4",
      "section": "Sections 4-5, especially Table 4, Tables 8-12, H3a verdicts, and Section 7",
      "issue": "Empirical evidence is not sufficient for the central claims: small constructed studies, underpowered pilots, author-derived Set N, LLM-only or LLM-majority audits, non-independent corpora, and head-to-head aggregate domination by GenMorph.",
      "why_fatal": "The evidence supports at most feasibility and some construct-validity examples, not TOSEM-level validation of a general MR-identification framework.",
      "fixable_by": "experiment"
    },
    {
      "id": "B5",
      "section": "Data and Artifact Availability; ACM metadata; author/funding/AI disclosures",
      "issue": "Review-anonymity and artifact statements are inconsistent: the source includes full author identities, affiliations, emails, funding, Zenodo DOI, and review-stage anonymization claims simultaneously.",
      "why_fatal": "As submitted for double-blind review this is procedurally defective; even for journal review, the artifact and anonymity claims are internally inconsistent and undermine reproducibility checking.",
      "fixable_by": "writing"
    }
  ],
  "major_weaknesses": [
    {
      "section": "Theorem 2 and Table 1",
      "issue": "The polynomial-time constructibility theorem assumes termination and finite generating sets, hides invariant-extraction complexity in t_i, and treats output size/block enumeration ambiguously; it is not a strong algorithmic complexity result.",
      "suggested_fix": "Recast as an implementation-cost accounting lemma under explicit finite, bounded templates; remove headline 'polynomial-time' unless input encoding, output size, and invariant-extraction decision problems are formalized.",
      "fixable_by": "writing"
    },
    {
      "section": "Section 3.5 equivariant ML, Sections 5.2-5.4 case study",
      "issue": "Equivariant-ML validation uses a compact EGNN stand-in, an added symmetrized QK probe, constructed mutation categories, and debug-time MRs; this does not validate the claimed SE(3)-equivariant testing transfer.",
      "suggested_fix": "Run preregistered experiments on at least one real SE(3)-Transformer/e3nn/NequIP/MACE-style architecture with real or benchmarked faults, independent baselines, and CI-feasible MRs only.",
      "fixable_by": "experiment"
    },
    {
      "section": "Section 5.2 Table 4 and DeepCrime pilot Table 5",
      "issue": "Statistical testing is over-interpreted relative to design: H2 is construct-validity-controlled; n=5 DeepCrime pilot is underpowered; multiple comparisons and paired/clustered dependence are only partially handled.",
      "suggested_fix": "Demote all p-values from these studies to descriptive appendices or expand to a sufficiently powered preregistered multi-subject design with clustered analyses.",
      "fixable_by": "experiment"
    },
    {
      "section": "Section 5.6 Tables 8-12",
      "issue": "Head-to-head with GenMorph is reframed after unfavorable aggregate results; the per-block narrative is interesting but does not overcome Set G's D1 and pooled dominance.",
      "suggested_fix": "State plainly that NOETHER loses the primary fault-detection head-to-head and restrict empirical claims to cost, interpretability, and block-specific complementarity; avoid any superiority implication.",
      "fixable_by": "writing"
    },
    {
      "section": "Section 5.1 Tables 2-4",
      "issue": "Primary MR-identification evidence is too coarse: binary block coverage collapses quality, executability, novelty, and practical value into a 0/1 table, and 'Conservation' is inconsistently treated as both G-block and row.",
      "suggested_fix": "Replace binary coverage as the main empirical endpoint with independently coded MR corpora, explicit unit of analysis, execution status, novelty status, and inter-rater human coding.",
      "fixable_by": "experiment"
    },
    {
      "section": "Section 3.6 relational query optimizers",
      "issue": "Relational optimizer examples are standard query-equivalence identities; the section shows mapping to known algebra, not new MR-identification capability.",
      "suggested_fix": "Evaluate against a real query-optimizer MR/test-generation benchmark such as Segura-style query-system MRs or SQLancer/QED/SPES residues, with independent baselines and measurable gains.",
      "fixable_by": "experiment"
    },
    {
      "section": "Section 3.7 negative PWR instantiation; Appendix C.6",
      "issue": "The negative results are useful but their role is confused: they both delimit and weaken the framework; the manuscript treats them as maturity evidence while they expose missing Translate expressiveness.",
      "suggested_fix": "Make the PWR negative result a central limitation and either implement Composite-Translate or narrow all positive claims to single-block first-order MRs.",
      "fixable_by": "either"
    },
    {
      "section": "Section 7 Threats to Validity",
      "issue": "Self-disclosure is extensive but often substitutes for mitigation: LLM-only κ, same-author derivations, same-author reimplementations, and future-work commitments remain unresolved threats.",
      "suggested_fix": "Convert key threats into completed mitigations before submission: independent human coding, independent subject implementations, and externally sourced MR corpora.",
      "fixable_by": "experiment"
    },
    {
      "section": "Related Work Section 2",
      "issue": "The contrast with prior MT/MR work is sometimes straw-mannish: existing symmetry, relational-algebra, specification/model-based, and pattern-family work already provide structural grounding in narrower forms.",
      "suggested_fix": "Sharpen the delta to 'unified operator-block recoding plus explicit Translate boundary' and remove claims implying that prior work lacks any structural source.",
      "fixable_by": "writing"
    },
    {
      "section": "Conclusion and contribution list C1-C5",
      "issue": "Contributions are over-numbered and internally hedged; the reader cannot tell which claims are established, exploratory, negative, or future work.",
      "suggested_fix": "Reduce to 2-3 precise claims: framework definition, scoped closure/well-formedness, and limited empirical feasibility/complementarity; move pilots/protocols/future-work matrices to supplement.",
      "fixable_by": "writing"
    }
  ],
  "minor_issues": [
    "Title says 'discovery' in comments but 'identification' in manuscript; terminology should be consistent.",
    "Hypothesis label 'seven-blocks' is stale while the text defines eight blocks.",
    "Several tables and sections treat 'Conservation' as a separate row despite saying it is a G-block instance.",
    "The acmart metadata uses an arXiv DOI and non-anonymized author information while claiming anonymized review.",
    "Theorems, hypotheses, remarks, and boxed boundary statements are overused and dilute the actual formal contributions.",
    "Some labels contain spaces or special characters, e.g., Table label 'tab:obstruction set', which is poor LaTeX practice.",
    "The Data Availability section lists S1-S4, while the body repeatedly refers to S5-S12 and routeB; manifest is inconsistent.",
    "Several claims cite supplementary material for load-bearing evidence not present in the manuscript.",
    "The paper repeatedly says appendices are migrated but still includes long appendices and proof material.",
    "The 'Noether-style' analogy is rhetorically heavy and sometimes obscures the actual SE contribution."
  ],
  "highest_roi_fixes": [
    {
      "action": "Cut the manuscript to a single coherent TOSEM article: remove most protocols, pilots, future-work inventories, repeated boundary boxes, and non-load-bearing appendices; target one main theory claim plus one completed evaluation.",
      "expected_gain_pp": 12,
      "effort": "high",
      "fixable_by": "writing"
    },
    {
      "action": "Reframe Theorem 1 as a scoped well-formedness/closure lemma and remove any implication of completeness or discovery beyond Translate-reachable single-block MRs.",
      "expected_gain_pp": 8,
      "effort": "medium",
      "fixable_by": "writing"
    },
    {
      "action": "Run an independent MR-corpus evaluation with human domain experts: blind code MR corpora from at least two external domains into blocks, compare NOETHER-derived classes with expert and automated baselines, and report human κ.",
      "expected_gain_pp": 15,
      "effort": "high",
      "fixable_by": "experiment"
    },
    {
      "action": "Replace the constructed EGNN mutation study with a preregistered multi-architecture equivariant-ML study using real faults or standard mutation operators and CI-executable MRs.",
      "expected_gain_pp": 10,
      "effort": "high",
      "fixable_by": "experiment"
    },
    {
      "action": "Make artifact and review procedure consistent: anonymize if double-blind, provide a complete SSOT manifest for S1-S12, hashes, scripts, and exact reproduction claims.",
      "expected_gain_pp": 5,
      "effort": "medium",
      "fixable_by": "writing"
    }
  ],
  "summary": "The manuscript has a potentially useful organizing idea—operator-block grounding of MR classes—but is far below TOSEM submission maturity. The central theory is mostly definitional within a self-defined Translate image; the upstream block taxonomy is empirical and partly circular; the empirical evidence is fragmented, often constructed, underpowered, or self/LLM-audited; and the paper is massively overlong and procedurally inconsistent. A publishable version would need major narrowing, independent validation, and a much more modest claim."
}
```

## Free-form panel report

### Overall editorial assessment

**Recommendation: Reject.** The manuscript is in TOSEM’s broad scope—software testing, metamorphic testing, oracle problems, and method foundations—but it is not a mature TOSEM submission. It is closer to a research programme dossier than a journal article. The paper contains an interesting organizing idea: map MR classes to recurring algebraic/operator structures and use that mapping to explain origin and boundary. However, the submission substantially overclaims what is established.

The most serious problems are:

1. **The formal centerpiece is too weak for the claimed role.** Theorem 1 is closure over a set defined as the image of `Translate`; that is mostly a well-formedness lemma. It does not establish completeness of MR identification in any practically relevant sense, and the manuscript’s own PWR counterexamples show the stronger claim fails.

2. **The hard upstream step is not solved.** The operator algebra and block decomposition are human-curated empirical hypotheses. The paper repeatedly admits this, but admission is not evidence. Much of the positive “prediction” evidence is circular because blocks were partly induced from the same domains used to validate them.

3. **The empirical evidence is not load-bearing enough.** Many studies are constructed sanity checks, small pilots, protocol commitments, LLM-coded audits, or author-derived comparisons. The GenMorph head-to-head actually shows aggregate dominance by GenMorph on the D1 stratum, then the manuscript reframes the result as per-block complementarity.

4. **The manuscript is far too long and structurally undisciplined.** It contains repeated boundary boxes, extensive future-work inventories, protocols, appendices, and supplementary references. This alone is a likely TOSEM return-without-review risk.

5. **Review/anonymity/artifact handling is inconsistent.** The LaTeX source includes authors, emails, funding, AI disclosure, Zenodo DOI, and claims about anonymized archives. This is not procedurally clean.

The current paper could eventually become publishable if radically narrowed and supported by independent validation. It is not fixable by copy-editing alone.

---

## Persona-specific findings

### 1. EIC perspective

**Verdict: Reject / likely return-without-review risk.**

#### Scope fit

The topic is in scope for TOSEM: MR identification, test-oracle problems, structured test design, and empirical SE evaluation. The paper is not “pure math” because it explicitly targets MR design and testing workflows. However, the paper repeatedly drifts into:

- abstract algebraic formalization,
- reactor physics exposition,
- equivariant ML architectural discussion,
- query-optimizer equivalence,
- mutation-testing lab reports,
- future-work manifesting.

This scope sprawl makes it hard to identify one coherent TOSEM contribution.

#### Originality and significance

The claimed delta should be narrowed. The manuscript often implies that prior work lacks structural grounding. That is too strong. Prior work already includes:

- symmetry-based testing and symmetric oracles,
- METRIC/METRIC+ category scaffolds,
- relational-algebra MR patterns for query systems,
- specification/model/documentation-based MR derivation,
- equivariance/invariance testing in ML.

NOETHER’s plausible novelty is not “deriving MRs from structure” in general. A more defensible novelty is:

> a unified operator-block vocabulary for classifying algebraically grounded MR classes, with an explicit `Translate` boundary and examples across several algebraic program families.

That is potentially useful, but not yet supported at TOSEM level.

#### Desk-reject triggers

- **Length and structure:** severe. This is far beyond a standard TOSEM article. The source reads like a monograph plus supplementary material.
- **Anonymity inconsistency:** the manuscript claims anonymization but includes full identities and funding.
- **Artifact inconsistency:** body refers to S1-S12, routeB, future_work.md, many scripts, while Data Availability lists only S1-S4 in one place and later lists many more.

These are not small polish issues.

---

### 2. R1: methodology / theory + statistics

**Verdict: Reject.**

#### Theorem 1: closure under `Translate`

Anchors: Section 3.2.3, Definition `Algebra-induced MR`, Theorem 1, Appendix C.4-C.6.

Theorem 1 states that every MR in `MR(A_P)` belongs to a MetaPattern. But `MR(A_P)` is defined as the set of MRs obtained by `Translate` from block invariants. Then `CONSTRUCT-MP` forms MetaPatterns from those same invariants. The proof is therefore mostly:

> if an MR is produced by the construction, then the construction assigns it to a constructed class.

That is a valid well-formedness property but not a strong theory of MR identification. The paper itself acknowledges the by-construction nature, but then repeatedly uses the result rhetorically as “closure,” “structural adequacy,” and “foundational.”

A mature revision must demote this theorem. It should be described as a **scoped no-drop invariant** of a particular construction, not as a core completeness result.

#### Theorem 2: complexity

Anchors: Theorem 2, Table 1, Appendix proof.

Theorem 2 assumes a finite generating set and assumes each invariant computation terminates in time `t_i`. That hides the hard part in `t_i`. For relational query equivalence, the manuscript admits undecidability outside fixed-rule fragments. For groups, it requires finite or finite-dimensional Lie representations or truncation. The claimed `O(n * max t_i * log n)` is therefore a bookkeeping bound over already-solved extraction tasks, not a meaningful general polynomial-time result.

The term “polynomial-time constructibility” should be used only with a formal input encoding, output-size bound, and precisely decidable invariant-extraction procedures. Otherwise it should be reframed as implementation cost under finite templates.

#### Invariance-Blindness Theorem

Anchors: Section 3.3.

This is one of the stronger formal parts. The kernel characterization for linear faults under faithful finite witness sets is plausible. However, its scope is narrow:

- linear operator-implementation faults,
- exact arithmetic,
- G and T* blocks only,
- faithfulness assumed or rank-checked in small finite settings.

The manuscript sometimes uses IBT to make broader claims about blind spots and complementarity. The formal result does not justify broad extrapolation to nonlinear ML faults, production reactor simulators, or general MR batteries.

#### Statistics and empirical methodology

Problems recur:

- **Constructed mutations:** In Section 5.2, category (iv) is selected so that the NOETHER time-reversal MR uniquely detects it. The paper admits this. It remains non-independent evidence.
- **Underpowered pilots:** The DeepCrime-style pilot has `n=5`; the paper reports it descriptively, but it still appears in the evidence chain.
- **Multiple comparisons:** Many McNemar/Fisher tests appear across sections and tables. Some corrections are mentioned, but the overall empirical narrative is not controlled as one analysis family.
- **Pooled vs clustered:** Many mutants are nested within SUTs and MRs; simple pooled counts ignore clustering.
- **LLM raters:** LLM-majority κ is not a substitute for independent human coding.

A TOSEM revision would need one clean, preregistered empirical design with an appropriate unit of analysis, clustering, and independently sourced subjects.

---

### 3. R2: MT / MR domain expert

**Verdict: Reject.**

#### Literature positioning

The related work section is broad and includes many appropriate references: Chen, Segura, METRIC/METRIC+, GenMorph, MR-Scout, Gotlieb symmetric testing, query-based MR patterns, MemoRIA, etc. However, the argumentative contrast is too sweeping.

The manuscript’s operator blocks often correspond to familiar MR families:

- symmetry / permutation / invariance,
- monotonicity,
- convergence,
- reciprocity / adjoint relations,
- method comparison,
- relational equivalence.

The paper’s contribution is not that these sources were unknown. It is the proposed unifying vocabulary and `Translate` construction. The manuscript should stop describing existing pattern catalogues as if they are mere empirical lists with no structural basis. Query-based MR work, specification-based MR work, and symmetry testing already use structural reasoning.

#### MR identification vs recoding

Anchors: Section 3.4 Boltzmann instantiation, Table 2, Table 3.

The reactor-physics evidence is explicitly an internal vocabulary-coherence test using the authors’ own prior PWR MR catalogue. The paper says so. That makes it weak evidence for “constructive identification.” Reproducing or refining the authors’ own previous taxonomy does not demonstrate independent discovery.

The two “predicted” patterns, adjoint reciprocity and time reversal, are textbook physics. The manuscript admits they are not de novo discoveries and that the blocks were partly motivated by reactor physics. That should end the strong predictive claim.

#### Binary block coverage

Anchors: Section 5.1, Table 2.

Binary block coverage is too crude. A block is counted covered if at least one MR belongs to it. This ignores:

- number of useful MRs,
- executable vs latent MRs,
- fault-revealing potential,
- redundancy,
- novelty,
- maintenance cost,
- human interpretability.

It is acceptable as a diagnostic, but not as primary evidence of a superior MR-identification method.

#### Comparison with automated MR methods

Anchors: Section 5.6, Tables 8-12.

The GenMorph comparison is not favorable to NOETHER in aggregate. The manuscript’s per-block reframing is not invalid, but it cannot be sold as competitive superiority. The proper claim is:

> NOETHER produces some complementary, interpretable MRs at lower derivation cost, but does not outperform GenMorph in aggregate mutation detection on the reported D1 stratum.

That is a much narrower contribution.

---

### 4. R3: equivariant ML + safety-critical V&V perspective

**Verdict: Reject.**

#### Equivariant ML leg

Anchors: Section 3.5, Section 5.2, Table 4.

The equivariant-ML examples are conceptually plausible but empirically weak.

Problems:

- The study uses a small EGNN, not a full SE(3)-Transformer or production equivariant architecture.
- The T* attention probe is added/instrumented rather than intrinsic to the EGNN.
- Some MRs are debug-time rather than CI-time.
- The mutation set is constructed around the block taxonomy.
- Real-fault evidence is a tiny `n=5` pilot.

This is not enough to establish cross-domain transfer beyond illustrative feasibility.

#### Safety-critical / reactor evidence

The reactor sections contain extensive domain detail, but independent validation is limited. The industrial SACOS/SPARK/LOCUST evidence is largely summarized via supplementary material and appears dominated by order/monotonicity relations. The important PWR negative examples actually show that real safety-critical MR needs exceed the current `Translate` signature.

The safety-critical implication should therefore be conservative:

> NOETHER may help organize some algebraic MR classes in reactor codes, but the current framework misses important regulatory-relevant PWR relations unless extended.

That is not a small limitation.

#### IBT and fault detection

The IBT exact-arithmetic, linear-fault setting is far removed from floating-point, nonlinear, stochastic, and high-dimensional ML systems. The manuscript acknowledges this, but the broader interpretive language risks overreach. The finite-tolerance regime is not solved.

---

### 5. Devil’s Advocate findings

**Critical found: yes.**

#### Circular argument

The paper’s construction depends on the authors selecting a decomposition of operator structures. The “discovery” of MetaPatterns follows mechanically after that. The framework relocates induction to the upstream algebra/block level, but does not solve it. Positive examples are often drawn from domains that informed the block list.

#### Selection-on-the-response

Many empirical components are selected or reframed after seeing fit:

- The equivariant-ML mutation category that NOETHER uniquely detects is constructed for the NOETHER MR.
- Head-to-head aggregate loss to GenMorph is reframed as per-block complementarity.
- Future-work commitments are interleaved with results, blurring completed evidence and planned evidence.

#### Self-disclosure as shield

The manuscript repeatedly discloses limitations. That is good practice, but the paper then still uses the limited evidence rhetorically. Self-disclosure does not make LLM κ equivalent to human reliability, nor constructed mutations equivalent to real defect distributions.

#### Overgeneralization

The framework is valid only for program families with explicit operator-algebraic structure and only for the current `Translate`-reachable MR space. The conclusion and abstract should be far narrower.

---

## Publication blockers vs fixability

### Blocker B1: Length and article discipline

**Fixable by writing only, but high effort.**

The paper must be reduced drastically. A TOSEM article should not include:

- multiple large protocols not executed,
- 16-item future-work programmes,
- long appendix proofs plus claims of migration,
- repeated boxed boundary statements,
- extensive supplementary manifest details,
- multiple domains evaluated at different depths without a single clean evaluation story.

A possible structure:

1. Problem and scoped claim.
2. Formal framework.
3. One strong formal result, honestly scoped.
4. One completed empirical evaluation.
5. Threats and limitations.

Everything else should go to supplementary material or a separate paper.

### Blocker B2: Theory overclaim

**Fixable by either writing or new theory.**

If the authors keep the current theory, the claim must be narrowed:

- Theorem 1 = no-drop assignment for `Translate`-reachable MRs.
- Theorem 2 = finite-template construction cost.
- Negative PWR examples = current expressiveness boundary.

If the authors want the stronger claim, they need a real Composite-Translate theory and demonstrate closure/complexity under it. That requires new theoretical work.

### Blocker B3: Circularity of block decomposition

**Requires new experiments / independent validation.**

The authors need an independent block-extraction protocol:

- external domain experts identify governing equations and operators,
- independent human raters classify blocks,
- authors’ NOETHER derivations are compared against independently authored MR corpora,
- held-out domains are selected before block revision.

LLM raters are not enough.

### Blocker B4: Evidence insufficiency

**Requires new experiments.**

A publishable evaluation should include at least:

- independent MR corpora from multiple domains,
- executable comparison with one or two strong baselines,
- powered and clustered statistical analysis,
- human-coded novelty/interpretability/maintenance outcomes if those are claimed,
- clear separation of confirmatory vs exploratory results.

### Blocker B5: Procedural/artifact inconsistency

**Fixable by writing and artifact cleanup.**

The manuscript must be internally consistent about:

- anonymized vs non-anonymized review,
- artifact DOI,
- supplementary file manifest,
- exact scripts and hashes,
- what evidence is in the manuscript vs supplement.

---

## Threats to validity not adequately mitigated

### Construct validity

- Set N is author-derived.
- Block labels are partly LLM-audited.
- Some subjects are same-author reimplementations.
- Mutation categories are constructed around block coverage.
- Binary coverage does not measure MR usefulness.

### Internal validity

- The `Translate` templates may not faithfully capture all intended block invariants.
- Canonical-block ordering is arbitrary and may hide compositional MRs.
- Equivalent-mutant filtering uses LLM voting, not formal or human adjudication.

### External validity

- Strongest evidence is concentrated in algebra-rich/math-heavy domains.
- General SE systems without clean operator algebras are out of scope.
- Industrial reactor evidence is not sufficiently transparent in the manuscript.
- Equivariant ML evaluation does not use production-scale architectures.

### Conclusion validity

- Many claims are supported by small counts.
- Multiple testing and clustering are not consistently handled.
- Some results are descriptive but narratively elevated.
- Head-to-head comparisons do not support superiority.

---

## What a revision must do to be acceptable at TOSEM

A viable TOSEM revision should not try to preserve the current scope. It should choose one of two paths.

### Path A: Theory/method paper

Required changes:

1. **Narrow the claim.**
   - Present NOETHER as a scoped classification and construction framework for single-block algebra-induced MRs.
   - Drop broad “discovery” and “completeness” language.

2. **Demote Theorem 1 and Theorem 2.**
   - Theorem 1 becomes a well-formedness theorem.
   - Theorem 2 becomes a finite-template construction-cost proposition.

3. **Make the negative PWR result central.**
   - Explain exactly what current `Translate` cannot express.
   - Do not treat this as a minor limitation.

4. **Provide one independent validation of block decomposition.**
   - Human expert block coding over an external MR corpus.
   - Report κ from independent human raters, not LLMs.

5. **Cut empirical mutation-testing sprawl.**
   - Keep one concise feasibility study or move all mutation details to supplement.

### Path B: Empirical SE paper

Required changes:

1. **Define measurable MR-identification outcomes.**
   Examples:
   - independent expert-rated validity,
   - executable MR yield,
   - novelty against existing corpora,
   - time/cost to identify,
   - maintenance/readability ratings,
   - mutation/real-fault detection as secondary.

2. **Run a powered multi-subject study.**
   - At least two domains not used to design the block taxonomy.
   - Independent baselines: METRIC+/category method, GenMorph/MR-Scout/LLM.
   - Human raters.

3. **Use proper statistics.**
   - Clustered by SUT and MR.
   - Correct multiple comparisons.
   - Predefine primary endpoint.

4. **Report unfavorable results plainly.**
   - If GenMorph wins on detection, state that.
   - Claim complementarity/cost only if measured.

5. **Separate exploratory findings from confirmatory claims.**

---

## Bottom-line maturity

The manuscript has conceptual potential but is not close to TOSEM acceptance. The current maturity score is **37/100**. The most plausible path to publication is not a “major revision” of this manuscript as-is, but a substantial reconception into a shorter, scoped, independently validated paper.