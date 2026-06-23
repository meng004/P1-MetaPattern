```json
{
  "overall_recommendation": "Major Revision",
  "submission_maturity_0to100": 52,
  "acceptance_probability_pct": 25,
  "reviewer_confidence_1to5": 4,
  "dimension_scores_0to100": {
    "originality": 68,
    "methodology_rigor": 50,
    "evidence_sufficiency": 44,
    "argument_coherence": 58,
    "writing_presentation": 38
  },
  "persona_verdicts": {
    "EIC": {
      "recommendation": "Major Revision",
      "headline": "Novel algebraic framing for MR identification but massively over-length with self-referential evaluation; scope fit is good but the paper needs radical compression and independent validation legs"
    },
    "R1_methodology_theory": {
      "recommendation": "Major Revision",
      "headline": "Theorem 1 is near-tautological (by-construction closure over Translate-image); Theorem 2 'polynomial-time' is oversold; IBT is sound but limited to linear faults on G/T* only; all statistical tests underpowered"
    },
    "R2_domain_mt_mr": {
      "recommendation": "Major Revision",
      "headline": "Operator-algebraic framing is genuinely new for MT, but the eight blocks are empirically curated (not axiom-derived), the 'prediction' of m_adj/m_rev is circular, and Set N is empirically dominated by Set G on D1 mutants"
    },
    "R3_perspective_equivariance_safety": {
      "recommendation": "Major Revision",
      "headline": "IBT is the strongest cross-domain contribution; however, equivariant-ML instantiation is thin (tiny model, procedural data, ρ_train-rev only works with vanilla SGD), and industrial reactor witnesses validate only O_≤ block"
    },
    "devils_advocate": {
      "critical_found": false,
      "strongest_counterargument": "The paper's central claim — that NOETHER 'constructively identifies MR meta-patterns from operator algebras with completeness boundaries' — suffers from three compounding circularities. (1) Theorem 1's closure is by-construction over MR(A_P), defined as exactly the Translate-image of A_P; it is a well-formedness lemma, not a completeness result, yet is presented as the headline theoretical contribution. (2) The eight blocks were curated 'by inspection of mathematical structures that recur across the program families we have studied' (§3.2) — this is the same inductive process the paper claims to replace, merely relocated one level up. The 'prediction' of m_adj and m_rev on Boltzmann is explicitly acknowledged as circular since T* and T*_rev were partly motivated by reactor physics. (3) The equivariant-ML case study's star result (5/5 unique cat-(iv) detection) is construct-validity-controlled: the mutation set was built to cover one defect per block, and cat-(iv) was selected because ρ_train-rev targets it. The paper discloses all three circularities, but self-disclosure does not convert a weakness into evidence. The net result is a framework that replaces induction at the MR-instance level with induction at the block level, then wraps the downstream construction in a tautological closure guarantee, while the strongest empirical result (L*-blindness) confirms a negative prediction (zero kills) rather than demonstrating positive identification power. CRITICAL status is not reached because the IBT and Theorem 1' falsification are genuine, non-circular contributions; however, the gap between claimed and established contribution is substantial."
    }
  },
  "publication_blockers": [
    {
      "id": "PB-1",
      "section": "Full manuscript",
      "issue": "Manuscript length far exceeds TOSEM soft limit (~11k words); body text alone exceeds 25,000 words with extensive repetition of boundary-of-contribution boxes (three near-identical restatements)",
      "why_fatal": "TOSEM LEN-01 permits return-without-review for papers far exceeding the word limit; even if reviewed, the length overwhelms the signal-to-noise ratio",
      "fixable_by": "writing"
    }
  ],
  "major_weaknesses": [
    {
      "section": "§3.3 Theorem 1 + Definition 12",
      "issue": "Theorem 1 (closure under Translate) is near-tautological: it quantifies over MR(A_P) which is defined as the Translate-image of A_P. Of course every Translate-reachable MR is assigned to a MetaPattern — that is what CONSTRUCT-MP does by construction. Presented as the headline theoretical result, it overstates the contribution.",
      "suggested_fix": "Reframe Theorem 1 as a well-formedness/well-specifiedness guarantee (a 'no-drop' invariant), not as a closure 'theorem'. Move it from headline to supporting role. The real theoretical contributions are the IBT and the Theorem 1' falsification.",
      "fixable_by": "writing"
    },
    {
      "section": "§3.4 Theorem 2 + Table 2",
      "issue": "Theorem 2 claims 'polynomial-time constructibility' but the bound O(n·max_i t_i·log n) hides exponential quantities: |G| can be exponential in input size, and for Lie/infinite groups the bound requires truncation or finite-dimensional substitution. The 'polynomial-time' framing is misleading.",
      "suggested_fix": "Rename to 'polynomial-time under finite-generator assumption' in the theorem statement itself (not just in remarks). Add explicit input-size parameterization showing when the bound is genuine input-polynomial vs. output-polynomial.",
      "fixable_by": "writing"
    },
    {
      "section": "§5.2 Case study",
      "issue": "The equivariant-ML case study (n=20 mutations, 1 model, 5,189 parameters) is severely underpowered. The 5/5 unique cat-(iv) detection is construct-validity-controlled (mutations selected to cover one defect per block). The DeepCrime pilot (n=5, McNemar p=0.500) is uninformative.",
      "suggested_fix": "Run the committed comparative evaluation protocol (§5.2, para 'Comparative evaluation') with DeepCrime's published mutation operators on ≥2 architectures before resubmission. Report neutral-mutation results where defect categories are not selected to match blocks.",
      "fixable_by": "experiment"
    },
    {
      "section": "§4.3 Reactor mapping + §5.1 Tables 5-7",
      "issue": "EQ1/EQ3 evaluation is substantially self-referential: the reactor-physics MR catalogue is the authors' own prior work; the 18-MR audit uses LLMs (not independent humans) as raters (κ=0.857); industrial witnesses (SACOS/SPARK/LOCUST) validate primarily the O_≤ block only. The LLM-shared-training-data caveat makes κ values much weaker than human inter-rater reliability.",
      "suggested_fix": "Obtain independent human inter-rater κ for the 18-MR audit. Apply NOETHER to an external PWR MR corpus (e.g., PARCS V&V suite) authored by an independent team. Report human-κ alongside LLM-κ.",
      "fixable_by": "experiment"
    },
    {
      "section": "§5.3 Head-to-head",
      "issue": "Set N is dominated by Set G on D1 mutants (McNemar p=0.019, n=52). The paper reframes this as 'complementarity' and 'cost-axis advantage,' but the raw detection numbers favor the baseline. The per-block decomposition shows Set N has 0/7 on the G block for gcdSig/lcmSig due to input-normalization absorption — a framework boundary, not just a substrate artifact.",
      "suggested_fix": "Acknowledge the D1 dominance honestly as a current limitation. Investigate whether the G-block gap (input normalization absorbing the algebraic action) can be addressed by pre-normalization-aware MR templates or by recognizing a separate normalization-orthogonal block. Run the G-block fix on at least 3 additional Euclidean-style SUTs.",
      "fixable_by": "experiment"
    },
    {
      "section": "§3.2 Hypothesis 1 + §3.2 Remark on empirical status",
      "issue": "The eight blocks are empirically curated ('by-inspection enumeration of mathematical structures that recur across the program families we have studied'), not derived from algebraic axioms. The paper claims to 'replace inductive grounding with algebraic grounding' but only does so downstream of A_P; upstream, the block selection is itself inductive. The 'induction relocated, not eliminated' framing is honest but the paper's rhetorical structure still implies the framework is more deductive than it is.",
      "suggested_fix": "Rewrite the introduction's contribution framing to make 'induction relocated, not eliminated' the primary characterization, not a caveat. Reduce rhetoric of 'derivation' and 'constructive identification' where the upstream is inductive. Clearly separate the deductive downstream (genuine) from the inductive upstream (honest limitation).",
      "fixable_by": "writing"
    },
    {
      "section": "§4.4 ρ_train-rev",
      "issue": "ρ_train-rev (the most novel MR in the equivariant-ML instantiation) only works with vanilla SGD, which is almost never used in production (Adam/AdamW are standard). The paper labels it 'debug-time' but this severely limits practical impact. The MR 'fails by construction' on the optimizers practitioners actually use.",
      "suggested_fix": "Investigate whether a momentum-corrected or Adam-compatible time-reversal invariant exists (e.g., by linearizing the Adam update). If not, document this as a hard scope boundary with engineering guidance on when to use the debug-time fixture.",
      "fixable_by": "either"
    }
  ],
  "minor_issues": [
    "Three citations (Hu et al. 2019; Mariani 2018; Liu et al. 2020) could not be located through standard databases — the fallback to 'not cited' is acceptable but the search should be documented more transparently",
    "The 'conservation' row in Table 5 is confusing since conservation is stated to be the G-block MetaPattern m_inv (§3.2), not a separate block; the table should use consistent block nomenclature",
    "Definition 11 (alg-induced MR) uses 'equality' ρ = Translate(ι,s) but MRs are logical statements, not syntactic objects; the equality should be specified as logical equivalence or same-semantic-content",
    "The Path A METRIC+ head-to-head (§5.5) re-implements Sun 2021's subjects from prose by the same author who designed NOETHER — this confounds framework knowledge with implementation fidelity",
    "Remark on metric-stability candidate ninth block (M_lip) is developed enough to be a contribution but is relegated to an appendix remark; either promote or remove",
    "The multiple 'Boundary of contribution' tcolorboxes (§1, §3.2, §3.5, §7) are near-identical restatements; one suffices",
    "Table 6 (search-origin-boundary) is entirely qualitative prose in table format; it presents no measured comparison",
    "The Wilson 95% CI on D2 kill rate [0.000, 0.434] does not exclude the 10% ceiling claimed by the framework prediction at α=0.05; the paper should state this non-confirmation explicitly rather than 'consistent with direction'",
    "§5.3 reports McNemar p=0.0043 (pooled, n=57) but this mixes D1 (in-scope) and D2 (out-of-scope) strata; the D1-only p=0.019 is the appropriate test"
  ],
  "highest_roi_fixes": [
    {
      "action": "Radically compress the paper: remove 3 duplicate boundary boxes, merge §§4.3-4.5 into a single cross-domain section, cut PWR domain exposition by 50%, target ≤15k words body",
      "expected_gain_pp": 12,
      "effort": "medium",
      "fixable_by": "writing"
    },
    {
      "action": "Reframe Theorem 1 from 'closure theorem' to 'no-drop well-formedness guarantee'; make IBT and Theorem 1' falsification the headline theoretical results",
      "expected_gain_pp": 8,
      "effort": "low",
      "fixable_by": "writing"
    },
    {
      "action": "Run equivariant-ML case study with neutral (non-block-targeted) mutations on ≥2 architectures using DeepCrime operators at n≥30; report detection without construct-control",
      "expected_gain_pp": 10,
      "effort": "high",
      "fixable_by": "experiment"
    },
    {
      "action": "Obtain independent human inter-rater κ for 18-MR audit and Set N block labels; replace LLM-only κ with human+LLM comparison",
      "expected_gain_pp": 6,
      "effort": "medium",
      "fixable_by": "experiment"
    },
    {
      "action": "Rename Theorem 2 to explicitly state 'polynomial-time under finite-generator assumption with bounded per-generator cost'; add input-size vs output-size distinction in the theorem statement",
      "expected_gain_pp": 4,
      "effort": "low",
      "fixable_by": "writing"
    }
  ],
  "summary": "NOETHER introduces a genuinely novel operator-algebraic framing for metamorphic relation identification. The Invariance-Blindness Theorem (§3.4) and the falsification of the absolute-completeness conjecture on A_PWR (§4.6, Appendix C.6) are solid, non-circular theoretical contributions. The L*-blindness empirical confirmation (5/6 SUTs, §5.3) is a clean falsifiable prediction validated ex-ante. However, the paper suffers from four compounding problems: (1) Theorem 1's closure is near-tautological (by-construction over the Translate-image), yet presented as the headline result; (2) the evaluation is extensively self-referential (authors' own prior catalogue, LLM-based inter-raters, construct-controlled mutations); (3) Set N is empirically dominated by Set G on algebra-disrupting mutants (McNemar p=0.019 on D1), undermining the practical case; (4) the manuscript is at least 2.5× the TOSEM word limit with substantial repetition. The eight blocks are empirically curated, not axiom-derived, making the 'replace induction with algebra' claim honest only at the downstream level. A major revision must radically compress the paper, reframe Theorem 1 honestly, add independent (human, non-block-targeted) evaluation legs, and address the G-block framework boundary on normalization-absorbing SUTs."
}
```

---

## Detailed Panel Report

### EIC Assessment

**Scope fit** is strong: MR identification is a core TOSEM topic, and the algebraic/formal-methods angle is appropriate. **Originality** is genuine at the conceptual level — no prior work derives MR patterns from operator algebras with explicit closure and boundary characterization. **Significance** is tempered by the evaluation: the framework identifies MR classes but the identified classes detect fewer mutants than GP-evolved baselines on the tested substrate. The practical payoff (auditability, maintainability, cost) is claimed but not measured empirically.

**Length is a potential desk-reject trigger.** The body text exceeds 25,000 words with three near-identical "Boundary of contribution" tcolorboxes, extensive PWR physics exposition that belongs in a domain-specific journal, and a case-study section that repeatedly caveats itself. A 40% cut is feasible without losing content.

### R1: Methodology/Theory + Statistics

**Theorem 1 (Closure):** Formally, the theorem states: for every ρ ∈ MR(A_P) (defined as Translate-reachable from A_P), there exists a unique m ∈ M(A_P) containing ρ. This is correct but near-tautological: MR(A_P) is defined as the Translate-image, and CONSTRUCT-MP is defined to produce M(A_P) from that image. The "uniqueness" comes from the canonical ordering (Lemma C.1), which is trivially well-founded on a finite set. The paper acknowledges the by-construction status (§3.3, Remark 3) but still labels it "Theorem 1" and gives it top billing. The substantive value the paper claims — converting empirical adequacy to structural adequacy — only holds within the Translate-reachable space, which the Theorem 1' falsification shows is a proper subset of practically relevant MRs.

**Theorem 2 (Polynomial-time):** The bound O(n · max_i t_i · log n) is genuine polynomial time *in the number of generators and their per-generator costs*, but |G|² in Table 2's first row is not polynomial in the *input size* of the program. For a group specified by generators and relations, |G| can be exponential in the description length. The "polynomial-time" label without qualification is misleading. The paper partially addresses this in §3.5 ("On infinite groups") but the theorem statement itself should carry the qualification.

**IBT (§3.4):** This is the strongest theoretical contribution. The proof is correct: faithfulness (finite-dimensional linear system + rank condition) ensures the detection kernel equals exactly the structure-preserving faults. The three corollaries (single-block incompleteness, trivial joint kernel requirement, differential oracle complementarity) follow cleanly. The scope limitations are honestly stated (linear faults only, G and T* blocks only, exact arithmetic). The empirical validation (E1–E3 in §5.7) is consistent but narrow (N=8, three SUTs).

**Statistical validity:**
- Case study (n=20, 1 model): Wilson CIs are reported but the denominator is too small for reliable inference. The McNemar p=0.016 for N vs B is the only significant pairwise result; N vs L is borderline (p=0.063).
- DeepCrime pilot (n=5): McNemar p=0.500 — completely uninformative. Reporting this as "descriptive evidence consistent with the direction" is honest but the pilot adds essentially no inferential value.
- Head-to-head (n=52 D1, n=57 pooled): The D1 McNemar p=0.019 is the only adequately powered test, and it *favors Set G*. The paper's reframing as "complementarity" is a fair reading but does not overcome the dominance finding.
- L*-blindness: This is the cleanest test — a falsifiable quantitative prediction confirmed on 5/6 SUTs. However, it confirms a *negative* prediction (near-zero kills), which is less impactful than confirming positive identification power.
- LLM-based κ values (0.857, 0.931): These reflect consistency among similarly-trained models, not independent verification. The paper discloses this but the κ values are presented in a way that invites over-interpretation.

### R2: Domain MT/MR Expert

**Literature coverage** is adequate for the core MT literature (Chen 1998, Segura 2016, Zhou 2020, METRIC/METRIC+, GenMorph, MR-Scout). Gotlieb's symmetric testing is cited but the relationship is only sketched — the paper says NOETHER "does not invent the symmetry layer" but provides "a constructive derivation over the operator-block layer," which is the right framing but needs sharper articulation of what the construction adds beyond Gotlieb's per-program insight. Khritankov-Iakusheva 2024's six input-transformation families are cited but not mapped onto the eight blocks. Patel-Hierons 2018 is cited in passing. MemoRIA 2024 is cited but not structurally compared.

**Core novelty question:** Is "constructive identification" genuinely new, or is it repackaging of existing symmetry/monotonicity/convergence intuition? The paper's honest answer (§3.2, "empirical curation") suggests the latter for the block level, but the downstream construction (Translate + canonical ordering + quotient) is genuinely new formalization. The IBT's kernel characterization is new. The Theorem 1' falsification with concrete PWR counterexamples is new and valuable.

**Self-referential evaluation:** The reactor-physics mapping (§4.3) compares NOETHER against the authors' own prior inductive catalogue. The "prediction" of m_adj and m_rev is acknowledged as circular (§4.3, "A note on prediction"). The 18-MR audit uses LLMs, not humans. The industrial witnesses (SACOS/SPARK/LOCUST) are the strongest external validation but almost entirely validate the O_≤ block — the other six blocks have no independent industrial confirmation.

**The Set N vs Set G gap** is the most damaging empirical finding. On D1 mutants (the in-scope stratum), Set G kills 37/52 vs Set N's 26/52 (p=0.019). The per-block decomposition shows this is driven by the G-block gap on gcdSig/lcmSig (0/7 for Set N). The paper argues this is a "framework boundary" (input normalization absorbs the G-action), which is theoretically coherent but practically problematic — normalization prologues are extremely common in real code.

### R3: Equivariant ML + Safety-Critical

**IBT significance for equivariant ML:** The kernel characterization (symmetry MRs are blind to symmetry-preserving faults) is directly actionable for equivariant-ML testing. A tester who only uses rotation-invariance MRs will miss any fault that preserves rotation equivariance — this is now formally characterized, not just intuitively understood.

**Equivariant-ML instantiation weaknesses:**
- The EGNN model (5,189 parameters, procedural dataset) is a toy. Production equivariant models (NequIP, MACE, Allegro) have 10⁵–10⁶ parameters and operate on real molecular datasets.
- ρ_adj requires exposing the attention bilinear form through a forward hook — architecture-specific and not always available.
- ρ_train-rev only works with vanilla SGD, which is almost never used in production. Calling it "debug-time" is honest but severely limits practical value.
- The case study's detection advantage (7/20 vs 2/20 vs 0/20) is construct-controlled and underpowered.

**Industrial reactor witness:** The SACOS/SPARK/LOCUST evidence validates primarily the monotonicity (O_≤) block. The LOCUST MTC-vs-boron relation independently corroborates the Theorem 1' obstruction, which is valuable. But the full 8-block framework has no independent industrial validation for G, T*, T*_rev, L*, D*, E*, or B*_rel blocks on production codes.

**"So what" for equivariant ML practitioners:** The paper's cost-axis argument (polynomial-time derivation vs. 30-min GP search) is real but the human effort for A_P distillation (~10h per family) is substantial. The auditability advantage (each MR tied to an algebraic source) is genuine but unmeasured. No equivariant-ML team has adopted NOETHER; adoption outcomes are "open follow-up questions."

### Devil's Advocate: Strongest Counterargument

(Provided in the JSON above.) Summary: Three compounding circularities — (1) Theorem 1 is by-construction over the Translate-image; (2) the eight blocks are inductively curated; (3) the star empirical result (5/5 cat-(iv)) is construct-controlled. Self-disclosure does not convert weaknesses into evidence. The IBT and Theorem 1' falsification are genuine non-circular contributions, but they establish *limitations* of the framework (what it cannot do) more strongly than they establish its positive identification power.

### Threats to Validity Summary

1. **Internal:** Construct-controlled mutations in the equivariant-ML case study; LLM-based inter-rater reliability not equivalent to human reliability.
2. **External:** 10 SUTs from a single codebase; equivariant-ML validation on one tiny model; no independent reactor-physics MR corpus.
3. **Construct:** Theorem 1's scope (Translate-reachable MRs) is a proper subset of practically relevant MRs, as shown by the Theorem 1' falsification.
4. **Conclusion:** The paper's strongest empirical result (L*-blindness) confirms a negative prediction; the positive identification case rests on underpowered, self-referential evidence.

### What a Revision Must Do

1. **Compress to ≤15,000 words body.** Remove duplicate boundary boxes, merge cross-domain sections, cut PWR physics exposition. This alone would improve writing score by ~12pp.
2. **Reframe Theorem 1** as a well-formedness guarantee, not a headline closure result. Promote IBT and Theorem 1' falsification to headline status.
3. **Add independent evaluation legs:** (a) Human inter-rater κ for the 18-MR audit and Set N labels; (b) neutral (non-block-targeted) mutation study on ≥2 equivariant architectures with n≥30; (c) application to an external PWR MR corpus.
4. **Address the G-block boundary** on normalization-absorbing SUTs — either develop pre-normalization-aware MR templates or document this as a hard scope boundary with engineering guidance.
5. **Qualify Theorem 2's "polynomial-time"** claim explicitly in the theorem statement, distinguishing input-polynomial from output-polynomial.
6. **Measure the auditability/maintainability advantage** that the paper claims but does not quantify — e.g., time-to-understand for NOETHER-derived vs. search-generated MRs.