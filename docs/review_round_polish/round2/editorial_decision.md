# Editorial Decision

## Manuscript Information
- **Title**: NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
- **Manuscript ID**: ACM TOSEM (anonymised submission)
- **Decision Date**: 2026-05-15
- **Review Round**: Round 2 (polish round, post Stage 4.5 R3 integrity verification)

---

## Decision

### **Major Revision**

The decision is driven by:
1. The Devil's Advocate identifies **5 CRITICAL findings** (Theorem 1 tautology, "10 extensions" engineering, ε*-blindness post-hoc rescue, head-to-head dominance reframing, augmented-stratum circularity). Per the academic-paper-reviewer IRON RULE #4, DA CRITICAL findings **cannot be ignored by an Accept decision**.
2. Methodology reviewer (R1) detected a **publication-blocker integrity issue (W1)**: §6 case study Set L is implemented in `supplementary/S3_case_study/mr_sets/set_L_llm.py` as author-written "expected-shape placeholders" (`_placeholder_*_fn`), with the `prompt_log.md` raw GPT-4 output recorded as `[TO BE FILLED at experiment time]`. The paper text at lines 665 and 760 describes Set L as actual GPT-4 output. **The Table 4 row "Set L 2/20" is computed against author-imagined data, not against an actual LLM run.** This is a Mode 6 (methodology fabrication) failure mode that Stage 4.5 R3's integrity audit did not catch because R3's Phase B/C sampling did not extend into the `mr_sets/*.py` implementations.
3. Four of five reviewers (R1, R2, R3, plus DA) flag the **§6.6 head-to-head framing inconsistency** as a substantive concern: the §subsec:pooled-headtohead body reads "competitive parity at the published budget" while the abstract honestly states "Set N is dominated by the GP-evolved baseline"; the McNemar D1 p = 0.019 indicates Set G dominance on the algebra-disrupting stratum that Set N is designed for.
4. The decision matrix (EIC=Minor + R1=Major + R2=Major + R3=Major) maps to **Major Revision**.

---

## Reviewer Summary

| Reviewer | Role | Recommendation | Confidence | Weighted Score |
|----------|------|---------------|------------|----------------|
| EIC | ACM TOSEM AE, Testing & Analysis track | Minor Revision | 4 | 81.3 |
| R1 | Empirical SE methodologist (Wohlin/Briand) | Major Revision | 4 | 71.0 (blocked by W1) |
| R2 | MT/MR identification (Chen/Segura tradition) | Major Revision | 5 | 74.0 |
| R3 | Cross-domain V&V scholar (PWR + equi-ML + RDB) | Major Revision | 4 | 70.5 |
| DA | Devil's Advocate | — | — | 5 CRITICAL findings |

**Mean weighted score across scoring reviewers: 74.2** (Major Revision band 65-79). EIC's higher score reflects EIC-scope assessment of journal fit and overall positioning, which the other three reviewers handled at deeper detail levels where additional concrete blockers surfaced.

---

## Consensus Analysis

### Points of Agreement (Consensus)

**[CONSENSUS-5]** (All five reviewers agree, including DA):

1. **Theorem 1 is definitionally close to a tautology over `MR(A_P)` as defined by Def. `def:alg-induced`.**
   - EIC (line 110): "The 'sceptical reading might object that the by-construction status of Theorem 1 makes it near-tautological' paragraph (line 383) is the kind of self-aware caveat that makes the closure result land correctly."
   - R2 W1: "Theorem `thm:closure` reduces to: 'every MR in the image of CONSTRUCT-MP is in the image of CONSTRUCT-MP'. The 'by-construction-tautological' reading is acknowledged at line 383, and the authors offer a rebuttal that the substantive value lies in 'converting empirical-adequacy claims into structural-adequacy claims' — but this rebuttal is rhetorical, not formal."
   - R3 (S2 strengths): treats the falsification of Theorem 1' as the principal contribution rather than Theorem 1.
   - DA C1: "The proof in App. C.6.1 is two lines because `MR(A_P)` is *defined* (Def. 13) as exactly the image of `Translate`. ... The 'structural-adequacy claim' rescue in §3.3 line 383 does not restore positive content — it shifts the burden to Hypothesis 1."
   - R1 (deferred to R2 on theoretical content).

2. **§6.6 head-to-head framing is inconsistent with the data; "competitive parity" is unsupported.**
   - EIC W4: "the headline pooled number — 'Set G wins on D1, p = 0.0043' — is currently surfaced two paragraphs in, with the framing context after."
   - R1 W2: "The Abstract phrases this as 'Set N is dominated by the GP-evolved baseline' — which is honest. §subsec:pooled-headtohead and §subsec:empirical-summary lean toward 'competitive parity' and the per-block T* edge framing. The two-strands reading is internally inconsistent and selective."
   - R2 (implicit, via W1 and the absence of head-to-head against METRIC+).
   - R3 W4: "Table `tab:algebra-rich-pooled` reports Set N = 26, Set G = 40 ... McNemar exact two-sided p = 0.0043. The text at line 1538 reads 'competitive parity at the published budget' ... 'Competitive parity' is not a faithful reading."
   - DA C4: "Head-to-head Set N is dominated by Set G on D1 (p = 0.019); rescue via per-block and D2-stratum reframings is a garden-of-forking-analyses move."

**[CONSENSUS-4]** (4/5 reviewers agree):

3. **The 84-MR PWR corpus is the authors' own prior work; "systematisation" is re-binning rather than independent transfer.**
   - R2 W3, R3 W3, DA M4. EIC implicit (via S3 strengths-acknowledgement of the negative instantiation, but not direct concern with corpus provenance).

4. **External-validity claims exceed the empirical substrate.**
   - EIC W1 (length/scope), R1 W5 (single Java codebase, single architecture, single GenMorph snapshot), R3 W1 (asymmetric three domains — only one empirically tested), DA M5 (10 h cost amortisation only within Apache Commons Math family). R2's W5 also touches this (PWR negative instantiation is domain-specific physics, not generic MT scope).

**[CONSENSUS-3]** (3/5 reviewers agree):

5. **"10 pairwise-independent Translate-extension dimensions" is overcounted or engineered.**
   - R3 W2: "The 'ten pairwise-independent extensions' sentence at line 849 is the most overclaimed sentence in the cross-domain narrative ... It includes 'two of the equi-side dimensions specialising PWR-side dimensions to type-distinct algebraic primitives' which suggests the count is closer to 8 distinct dimensions across the three algebras (5 PWR + 3 rel + 2 equi specialisations), not 10."
   - DA C2: "The 'ten pairwise-independent extensions' is engineered to round to a clean number ... pairwise-independence is asserted but unproven."
   - R2 partially aligns (W2 calls for METRIC+ head-to-head, implicitly limiting the empirical confirmation of the extensions count).

6. **Wang2024QED bib entry has wrong authors.**
   - R3 W2 (specific finding): "The authors are Shuxian Wang, Sicheng Pan, and Alvin Cheung (*not* 'Sicheng Mao, Boyuan Tang, Junfeng Zhang, Yisu Remy Wang' as the working bib entry reads)."
   - Stage 4.5 R3 integrity audit covered 4 of 57 entries (the R2-fix targets) + 6 sampled core references; **Wang2024QED was not in the R3 sample**. This is a new integrity finding from Phase 1 Round 2 review.

**[CONSENSUS-2]** (2/5 reviewers agree):

7. **§6.6.1 DeepCrime pilot at n=5, Fisher p=1.00 carries inferential claims unsupported by the sample.**
   - R1 W3: "the pilot's three 'what it establishes' claims (lines 755) — (i) infrastructure runs end-to-end, (ii) L*-block prediction non-vacuous, (iii) framework boundary on cat-v-02/04/05 confirms a ninth-block candidate — each carry inferential weight beyond what n = 5 supports."
   - R3 (implicit, via Detailed Comments §6 and W1).

8. **Augmented stratum (App. F, 25 hand-crafted mutants) is construct-trace circular; the 25/25 number leaks into headline summaries.**
   - R1 W4 (cosmetic), DA C5 (substantive). R1 sees the disclosure as adequate but the visual pull as residual risk; DA sees it as construct-trace-circular yet used as headline evidence.

**[CONSENSUS-1]** (single reviewer):

9. **§6 Set L is author-written placeholders, not GPT-4 output** (R1 W1, file-level evidence in `set_L_llm.py` lines 11-15 + `prompt_log.md`). **This is the publication-blocker.**

10. **Literature gaps (R2 W4)**: Hu 2019 MT survey, Sun 2022 MR-derivation survey, MET workshop proceedings (Liu 2020, Mariani 2018), Lin 2020 symmetry-MR, deeper Ying 2025 engagement, algebraic-SE tradition (Plotkin-Mosses, Hoare-He). R3 does not duplicate this; the gap is R2's domain reading.

11. **METRIC+ head-to-head is described but never run** (R2 W2). The §para:metricplus-sorting is a category-mapping exercise, not a fault-detection comparison. The §6.6 head-to-head against GenMorph does not substitute (GenMorph is GP-evolved, not category-scaffolded).

12. **ε*-blindness "5/6 SUTs" outlier (`hypotSig`) rescued by post-hoc inspection rule not pre-registered** (DA C3). R1 and R3 considered the rescue methodologically clean; DA sees it as falsifiability-illusory.

### Points of Disagreement

**Disagreement 1: Severity of Theorem 1's tautological character**
- **EIC view**: Self-aware caveat at line 383 is "the kind of disclosure that makes the closure result land correctly" — i.e., adequate disclosure mitigates the issue.
- **R2/DA view**: The line-383 rebuttal is "rhetorical, not formal"; the substantive theoretical content is in Theorem 1''s falsification + the ten extensions, not in Theorem 1. The abstract still over-frames closure.
- **Disagreement type**: Severity disagreement (Minor vs Major).
- **Editor's Resolution**: Adopt R2/DA reading. The abstract's "algebraic-closure guarantee" framing without scope-qualifying clause leaves the reader expecting more than the theorem delivers; this is editorial under-disclosure that requires correction. The §3.3 self-aware paragraph at line 383 helps the careful reader but does not solve the abstract-level over-framing.
- **Resolution Rationale**: When 2/5 reviewers (R2 + DA) independently and with high confidence flag the same load-bearing claim as definitionally close to vacuous, with consistent file-level citations (Def. `def:alg-induced` defines `MR(A_P)` as the Translate-image; Theorem 1 then quantifies over this image; proof is 2 lines), the EIC-level acknowledgement-only response is insufficient. R1 and R3 deferred this to R2; their non-objection is not concurrence.

**Disagreement 2: ε*-blindness `hypotSig` outlier handling**
- **R1 view (S1)**: The outlier rescue is methodologically clean: the two killed mutants both genuinely break degree-1 homogeneity by the predicted exception clause. The threshold sensitivity grid is well done.
- **DA view (C3)**: The exception-handling rule is *not* pre-registered (pre-registration covers the prediction threshold, not the outlier-handling rule); the prediction is unfalsifiable in practice because any future SUT crossing the threshold can be re-classified as "homogeneity-breaking-mutator-acting-as-predicted".
- **Disagreement type**: Existence disagreement (is the prediction falsifiable in practice?).
- **Editor's Resolution**: Adopt DA's reading with R1's mitigation. The authors must commit the **outlier-handling rule** (inspect killed mutants and classify each as "homogeneity-breaking" vs "homogeneity-preserving"; outlier SUT is rescued only if all killed mutants are homogeneity-breaking) to a pre-registered protocol before any further empirical extension. R1's observation that the 2 `hypotSig` killed mutants both break homogeneity remains correct; DA's concern is about the falsifiability boundary, not the specific instance.
- **Resolution Rationale**: DA's frame-lock detection identified a real generalisability concern. The rescue rule must be made explicit and pre-registered for the prediction to remain genuinely falsifiable on future SUTs.

**Disagreement 3: Set L in §6 case study — placeholder integrity issue**
- **R1 view (W1, Critical)**: Publication-blocker; `set_L_llm.py` explicitly labels its five MRs as `_placeholder_*_fn` "expected-shape placeholders"; `prompt_log.md` records the raw GPT-4 output as `[TO BE FILLED at experiment time]`. The Table 4 row "Set L 2/20" is computed against author-imagined data. Affects H2 verdict on cat-(iv) detection and the §6.6.1 DeepCrime pilot.
- **EIC / R2 / R3 view**: Not flagged (sampling of supplementary code did not reach this file).
- **Disagreement type**: Detection disagreement (only one reviewer found this, but the finding is concrete and file-verifiable).
- **Editor's Resolution**: Adopt R1's finding as the **principal publication-blocker**. The discrepancy between paper text (lines 665, 760) and supplementary code (`set_L_llm.py` lines 11-15, `prompt_log.md`) is verifiable and must be resolved before publication. Three options per R1: (i) run the actual GPT-4 prompt and update Table 4; (ii) demote Set L from "LLM baseline" to "author-constructed plausible-tester baseline"; (iii) drop §6 Set L row in favour of §6.6 Set L_ensemble.
- **Resolution Rationale**: R1's finding is file-grounded and independently verifiable by inspection of `set_L_llm.py` lines 11-15 + `prompt_log.md`. Other reviewers' non-detection reflects sampling scope, not disagreement. The finding aligns with Stage 4.5 Mode 6 (methodology fabrication), which the failure-mode checklist requires be CLEAR before pipeline advance.

**Disagreement 4: Length and structure (76 pp.)**
- **EIC view (W1)**: 76 pp. exceeds TOSEM target (30-50 pp.); recommend moving §7.6 per-block head-to-head + Commons Math pilot to a companion empirical paper, leaving §7 as L*-blindness test only.
- **R2 view**: Length not flagged; the empirical density is the right level for a foundational paper.
- **R1 view**: Length not flagged directly; suggests an empirical-overview table at top of §6 to ease navigation.
- **R3 view**: Not flagged; the cross-domain instantiations are the load-bearing evidence and need their current depth.
- **Disagreement type**: Structural preference (split paper vs. single paper).
- **Editor's Resolution**: Defer to author's choice between EIC's option (a) split, option (b) trim appendices, option (c) accept current length pending TOSEM EiC consultation. The other reviewers' non-objection to length suggests the current envelope is defensible if accompanied by EIC's other framing-level fixes.
- **Resolution Rationale**: 4/5 reviewers consider the empirical density appropriate or necessary; length is an EIC-only concern at this reading.

---

## Decision Rationale

The paper has substantive intellectual content: it re-grounds MetaPattern discovery in operator-algebra structure, instantiates the framework on three structurally distinct domains, self-falsifies its strongest conjecture (Theorem 1') on its principal application domain via two regulatory-essential PWR counterexamples, and reports a falsifiable L*-blindness prediction confirmed on 5/6 SUTs. The negative instantiation (§subsec:negative-pwr + Appendix C.6) is among the most credibility-enhancing moves in recent MT-identification literature. The pre-registration of the L*-blindness threshold via git timestamp, the LRCA multi-LLM κ check, the Wohlin-compliant threats-to-validity organisation, and the Boundary-of-contribution tcolorboxes collectively place the paper above the median TOSEM submission for methodological discipline (R1 S1-S5; R2 S1-S5; R3 S1-S5; DA observations).

However, four pivots are required before publication:

1. **Set L placeholder integrity (R1 W1, principal blocker)**: The §6 case study's Set L baseline is implemented as author-written placeholders. The Table 4 "Set L 2/20" row, the H2 cat-(iv) verdict's framing of Set L as an independent LLM-prompted tester, and the §6.6.1 DeepCrime pilot's Set L 0/5 result are all conditional on the actual GPT-4 output, which has not been generated at submission time. This is a verifiable integrity discrepancy (file-level evidence at `set_L_llm.py` lines 11-15 + `prompt_log.md`'s `[TO BE FILLED at experiment time]`). Three resolution paths are available; whichever is taken, the paper text must match the supplementary code.

2. **Theorem 1 framing (CONSENSUS-5)**: The abstract's "algebraic-closure guarantee under the framework's Translate operator" reads as a closure result on the substantive sense (closure within the broader space of all MRs formulable in `A_P`). The proof is, however, two lines because `MR(A_P)` is defined as the Translate-image. The substantive theoretical content is in (a) Theorem 1''s falsification, (b) the ten Translate-extension dimensions across the three algebras, and (c) Theorem 2's polynomial-time decidability. The abstract and Section 1 contribution C2 need to reflect this. Recommended: rewrite the abstract sentence on Theorem 1 to read "an algebraic-closure guarantee over the Translate-image of `A_P` (Theorem 1), with the strictly stronger absolute-completeness conjecture (Theorem 1') falsified on the PWR core diffusion algebra".

3. **§6.6 head-to-head framing (CONSENSUS-5)**: The body's "competitive parity at the published budget" framing is inconsistent with the abstract's honest "Set N is dominated by the GP-evolved baseline" disclosure. The McNemar p = 0.0043 pooled and p = 0.019 D1-only indicate Set G dominance on the algebra-disrupting stratum that Set N is designed for. The §subsec:pooled-headtohead lead paragraph and §subsec:empirical-summary need to be rewritten to put the dominance result first and the per-block / D2-stratum / cost-axis reframings second.

4. **"10 pairwise-independent extensions" claim (CONSENSUS-3)**: The count of 10 is engineered from 5 (PWR) + 2 (equi) + 3 (rel) with two equi-side dimensions explicitly "specialising PWR-side dimensions" (paper line 849). The pairwise-independence claim is asserted but not proven across the ten. Recommended: either (a) prove pairwise-independence formally across the three algebras, or (b) state the count as "up to ten candidate Translate-extension dimensions, of which two equi-side dimensions specialise PWR-side dimensions to type-distinct algebraic primitives, and the relational-side dimensions are surveyed at a single-rater Calcite-rule classification level".

These four pivots, plus the further consensus items (provenance disclosure, METRIC+ head-to-head or contribution rescoping, literature gaps, DeepCrime pilot reading, Wang2024QED bib correction, augmented-stratum visual presentation, ε*-blindness outlier-handling rule pre-registration) are fixable in 6-8 weeks of revision and do not require fundamental redesign. The framework's foundational contribution, its scope discipline, its evidence base, and its self-falsification on Theorem 1' are all already in place.

---

## Required Revisions (Must Fix)

| # | Revision Item | Source Reviewer | Severity | Section | Estimated Effort |
|---|---------------|-----------------|----------|---------|-------------------|
| R1 | **Resolve Set L placeholder/text discrepancy in §6 case study.** Either (i) run the actual GPT-4 prompt, paste the raw output into `prompt_log.md`, regenerate Set L from the JSON, re-run `runner.py`, and update Table 4 numbers; or (ii) demote Set L's framing from "LLM-prompt baseline" to "author-constructed plausible-tester baseline" and remove the GPT-4 framing entirely; or (iii) drop §6 Set L row and rely on §6.6 Set L_ensemble. | R1 W1 | §6.6 case study; Table 4; `set_L_llm.py`; `prompt_log.md` | 2-5 days |
| R2 | **Rewrite Theorem 1's abstract framing and §3.3 substantive-content discussion.** Abstract sentence: "algebraic-closure guarantee over the Translate-image of `A_P` (Theorem 1), with the strictly stronger absolute-completeness conjecture (Theorem 1') falsified on the PWR core diffusion algebra". §3.3 substantive-content discussion: demote Theorem 1's content from "closure" to "well-formedness and uniqueness of canonical assignment under the strict total order"; concentrate theoretical novelty on Theorem 1''s falsification, ten extensions, and Theorem 2's complexity bound. | R2 W1, DA C1 | Abstract, §1 C2, §3.3, Remark `rem:scope` | 1-2 days |
| R3 | **Rewrite §6.6 head-to-head body framing to match abstract's honest "Set N is dominated on D1" disclosure.** Lead paragraph of §subsec:pooled-headtohead must put the McNemar p = 0.0043 pooled and p = 0.019 D1-only result first, with the per-block decomposition / D2-stratum / cost-axis reframings second. Remove "competitive parity" from the prose at line 1538 and elsewhere. | EIC W4, R1 W2, R3 W4, DA C4 | §subsec:pooled-headtohead lead paragraph; §subsec:empirical-summary | 1-2 days |
| R4 | **Fix `Wang2024QED` bib entry: change author list from "Sicheng Mao, Boyuan Tang, Junfeng Zhang, Yisu Remy Wang" to "Shuxian Wang, Sicheng Pan, Alvin Cheung" per the published QED paper.** Re-verify via CrossRef DOI. | R3 W2 | `NOETHER_paper.bib` | 30 min |
| R5 | **Tighten "ten pairwise-independent extensions" claim.** Either (a) prove pairwise-independence formally across A_PWR (5) + A_equi (2) + A_rel (3-5) with a C.6-style block-by-block exhaustion, or (b) restate as "up to ten candidate dimensions, of which two equi-side dimensions specialise PWR-side dimensions, and the relational-side dimensions are surveyed at a single-rater Calcite-rule classification level". Drop "pairwise-independent" if (a) cannot be delivered. | R3 W2, DA C2 | Abstract, §1 C2, §subsec:third-domain line 849, `theory/translate_extensions.md` | 3-5 days |
| R6 | **Pre-register the ε*-blindness outlier-handling rule.** Commit to a written rule: "an outlier SUT is rescued only if all killed mutants are independently classified as homogeneity-breaking by the framework's mutator-semantics taxonomy". Add this rule to `configs/d4j_algebra_rich_criterion.json` (with git timestamp) before any further empirical extension. | DA C3 | `configs/d4j_algebra_rich_criterion.json`; §subsec:l-blindness-derivation; §subsec:l-blindness-confirmed | 1 day |
| R7 | **Tighten §6.6.1 DeepCrime pilot reading.** Replace the three "what the pilot establishes" claims with a single sentence: "At n = 5, p = 1.00, the pilot infrastructure is end-to-end functional; no inferential conclusion is supported at α = 0.05; the 2/5 detection events are reported as descriptive context consistent with the direction of the framework's L*-block prediction, not as a hypothesis confirmation." Move mechanism explanation to a separately labelled paragraph. | R1 W3 | §subsec:deepcrime-pilot, abstract | 1 day |
| R8 | **Disclose 84-MR PWR corpus provenance more explicitly in §subsec:reactor-mapping.** Either (a) extend the §subsec:reactor-mapping line 492-494 caveat with a paragraph stating that the 84-MR corpus is the authors' own prior inductive output and re-classification within it tests internal vocabulary coherence not external transfer; or (b) commit to a follow-up applying NOETHER to an external reactor-physics MR corpus (PARCS V&V suite, IAEA TECDOC) before camera-ready. | R2 W3, R3 W3, DA M4 | §subsec:reactor-mapping; §1 C1; supplementary S2 README | 2-3 days |
| R9 | **METRIC+ contribution claim must match evidence.** Either (a) run a minimal METRIC+ vs NOETHER head-to-head on 3-5 SUTs by manual application of METRIC+'s 9-category catalogue and report Set-MP vs Set-N kill rates plus algebra-block / category-pair mapping; or (b) restate the contribution claim as "block-compressed and algebra-warranted version of METRIC+'s catalogue, without claiming superior fault detection". | R2 W2 | §2.2, §subsec:metricplus-sorting (Discussion), §1 C2/C3 contributions | 3-7 days |
| R10 | **§6.6 Set L in §subsec:case-study supplementary trace must match paper text.** If R1 option (i) (run actual GPT-4) is taken: update `set_L_llm.py` to remove `_placeholder_*` labels, fill `prompt_log.md` with raw output and date. If option (ii) (demote framing) is taken: update paper text at lines 665, 760, 717 to remove GPT-4 framing entirely. | R1 W1 | `supplementary/S3_case_study/mr_sets/set_L_llm.py`; `prompt_log.md`; §subsec:case-study lines 665, 717, 760 | 1-2 days |
| R11 | **Add literature coverage for the six missing items (R2 W4).** Add 1-2 sentence positioning for each in §2.4 or new §2.5 ("Algebraic and category-theoretic precedents in SE"): Hu 2019 MT survey, Sun 2022 MR-derivation survey, Liu 2020 MET search-based, Mariani 2018 MET compositional, Lin 2020 symmetry-MR, Plotkin-Mosses / Hoare-He / Power-Tennent algebraic-SE tradition. Ying 2025 MR Patterns deserves a dedicated paragraph contrasting NOETHER's algebra-block equivalence with Ying's family-tree specialisation relation. | R2 W4 | §2.4 (or new §2.5), §subsec:pmcm-worked | 3-5 days |
| R12 | **Augmented-stratum 25/25 table visual presentation.** Either (a) collapse Table 13 to a single aggregate row + footnote rather than per-block 2-set comparison; or (b) keep Table 13 but add a header column "Construct-trace check (design-implied)" with visual marker (italics) on the Set N rate column. | R1 W4, DA C5 | Appendix F (Table 13); Table 14 item (g) | 1 day |
| R13 | **External-validity claim alignment.** Soften abstract's "transferable across three structurally distinct domains" to "transferable across three structurally distinct *mathematical* operator-algebraic skeletons". Add explicit "Out of scope" paragraph in §3 enumerating program-family classes not targeted: web apps, RLHF reward models, distributed-consensus protocols, compiler-internal optimisations. State explicitly in §9 that the framework's adoption by PWR V&V / equi-ML / database query-optimiser teams is an open follow-up. | EIC W1, R3 W1, R3 W5, DA M5 | Abstract; §3 line 78; §9 (Conclusion) | 2-3 days |

---

## Suggested Revisions (Should Fix)

| # | Revision Item | Source Reviewer | Priority | Section | Expected Improvement |
|---|---------------|-----------------|----------|---------|-----------------------|
| S1 | Add "Comparators and why" paragraph at top of §6.6 or in §2.4 stating: (i) METRIC+ as category-scaffold predecessor; (ii) GenMorph as GP-evolved SOTA representative; (iii) MR-Scout omitted because mining input absent; (iv) AutoMT/GPTMR omitted because safety-critical domains. | EIC W3 | §2.4 or top of §6.6 | Improves comparator-selection defensibility |
| S2 | Add methodology-overview table at top of §6 listing (n / mutation source / comparator / hypothesis / falsification criterion / verdict) for the four empirical sub-studies. | R1 Detailed | §6 (new Table 0 / roadmap) | Improves reader navigation |
| S3 | Renumber §6.8 (negative instantiation) to §7 and shift §7 to §8; OR add a "Roadmap of empirical evidence" panel at the start of §6.6 / §6.7 / §6.8 / §7 stating which kind of result each establishes. | EIC W5 | Sectioning | Improves reading order |
| S4 | Drop one of the three Boundary-of-contribution tcolorbox panels (Intro / §3 / Conclusion); keep §1 and §9 panels, replace §3 panel with one-line reference. | EIC Minor | §3 line 440 | Saves vertical space |
| S5 | Promote §subsec:third-domain or §subsec:negative-pwr to top-level §6 (consistent with R2 W5's depth-warrant note). | R2 Layout | Sectioning | Increases visibility of load-bearing results |
| S6 | Add OR / RD with CI as effect size for paired binary McNemar outcomes (Table 11, pooled and D1). | R1 Stat Reporting | §6.6 statistical reporting | Improves effect-size reporting per APA 7 / EQUATOR |
| S7 | Single-author re-classification audit on the n = 18 both-miss mutants subjected to the LLM equivalent-mutant vote. | R1 Detailed | §subsec:pooled-headtohead equivalent-mutant exclusion | Strengthens LLM-vote construct validity |
| S8 | Update `Bronstein2021GDL` from arXiv preprint to MIT Press book (2024) if available. | R2 Minor | NOETHER_paper.bib | Citation currency |
| S9 | Trivial/semi-trivial/non-trivial breakdown of the 84-MR corpus in §subsec:reactor-mapping. | R3 W3, R2 implicit | §subsec:reactor-mapping; supplementary S2 | Improves provenance reading |
| S10 | Add per-MR labelling reasoning for the 18-MR audit (currently said to be in S2 `18mr_audit/` but not surfaced). | R3 Detailed | Supplementary S2 README | Improves audit transparency |
| S11 | Drop §6.6.1 DeepCrime pilot from abstract entirely; confine to §6.6.1 as future-work seed. | DA m4 | Abstract | Avoids n=5 inferential leak into abstract |
| S12 | C2 contribution split into C2a (positive: Theorem 1 + Theorem 2) and C2b (negative: Theorem 1' falsification + ten extensions). | EIC Minor | §1 line 134 | Improves contribution-list readability |

---

## Revision Roadmap

### Priority 1 — Integrity and Critical Issues (Estimated total effort: 7-12 days)
- [ ] **R1**: Resolve Set L placeholder/text discrepancy (R1 W1 critical blocker)
- [ ] **R10**: Update supplementary code/log to match paper text (consequent on R1)
- [ ] **R4**: Fix Wang2024QED bib entry (30 min)

### Priority 2 — Structural Revisions (Estimated total effort: 7-12 days)
- [ ] **R2**: Rewrite Theorem 1 abstract framing and §3.3 substantive-content discussion
- [ ] **R3**: Rewrite §6.6 head-to-head body to match abstract's "Set N is dominated" disclosure
- [ ] **R5**: Tighten "ten pairwise-independent extensions" claim (prove or restate)
- [ ] **R6**: Pre-register ε*-blindness outlier-handling rule
- [ ] **R13**: External-validity claim alignment (scope + out-of-scope enumeration)

### Priority 3 — Content Supplementation (Estimated total effort: 6-12 days)
- [ ] **R7**: Tighten §6.6.1 DeepCrime pilot reading
- [ ] **R8**: 84-MR PWR corpus provenance disclosure
- [ ] **R9**: METRIC+ contribution claim must match evidence (head-to-head OR rescope)
- [ ] **R11**: Add six missing literature items
- [ ] **R12**: Augmented-stratum table visual marker

### Priority 4 — Should Fix (Estimated total effort: 5-8 days)
- [ ] S1-S12 from Suggested Revisions

### Total Estimated Effort
- **Major Revision**: **6-8 weeks** (industry-standard envelope; the Set L resolution path determines the lower bound)

---

## Revision Deadline

- **Recommended deadline**: 2026-07-10 (8 weeks from decision)
- **Basis**: Major Revision standard envelope; R1, R5, R8, R9, R11 require concrete new work (running GPT-4 prompt, formal proofs, external corpus application, METRIC+ comparison, literature additions) that exceed 4-week Minor envelope.
- **Extension policy**: If R5 (formal pairwise-independence proof) cannot be delivered within 8 weeks, the alternative (restate as "candidate dimensions") is available with no further extension.

---

## Response Letter Instructions

Please use the format in `~/.claude/skills/academic-paper-reviewer/templates/revision_response_template.md` to respond to every reviewer comment item by item. Required content:

1. Response and revision description for each of R1-R13 (Required Revisions)
2. Response for each of S1-S12 (Suggested Revisions; adopted or reason for not adopting)
3. R&R Traceability Matrix per Schema 11 (cross-skill data contract)
4. Change markup in the revised manuscript (color coding or LaTeX `\todo{}` macros for material changes)
5. Cross-reference table of new line numbers / paragraph numbers per change

The DA's CRITICAL findings C1-C5 must be specifically addressed in the response letter:
- **C1 (Theorem 1 tautology)**: handled via R2 above
- **C2 (10 extensions engineered)**: handled via R5 above
- **C3 (ε*-blindness rescue)**: handled via R6 above
- **C4 (D1 dominated, garden of forking)**: handled via R3 above
- **C5 (augmented stratum circular)**: handled via R12 above + explicit acknowledgement that augmented stratum is excluded from H3a.1 evidence base (currently §subsec:pooled-headtohead does this; verify after revision)

The DA's Unexamined Premise (MR identification as the binding constraint) and DA M2 (LLM ensemble subsumes Set N at lower cost) deserve a direct response in the §9 (Discussion) section, even if the framework's position is to retain MR identification as a central concern.

---

## Closing

We encourage the authors to carefully consider the reviewers' comments and submit a substantially revised manuscript. Please note that the revised manuscript will undergo another round of review (Stage 3' verification review in the academic-pipeline state machine). Given the foundational nature of the contribution and the rare combination of constructive theory with self-falsification on the framework's strongest conjecture, the path to acceptance is clear; the four pivots in the Decision Rationale and the 13 Required Revisions provide a concrete agenda.

The Stage 4.5 R3 integrity report's PASS verdict remains valid for the items it audited; the W1 Set L placeholder discrepancy is a Mode 6 (methodology fabrication) finding that R3 did not surface because its Phase B/C sampling did not extend into the `mr_sets/*.py` implementations. After Stage 4 R3 revisions land, Stage 4.5 R4 must independently verify (i) the Set L resolution path was correctly executed, (ii) the head-to-head body framing matches the abstract, and (iii) the bib `Wang2024QED` author list matches the CrossRef DOI source.

---

## Appendix: Full Reviewer Reports

- [EIC Report](r0_eic_report.md)
- [R1 Methodology Report](r1_methodology_report.md)
- [R2 Domain Report](r2_domain_report.md)
- [R3 Perspective Report](r3_perspective_report.md)
- [DA Devil's Advocate Report](r4_devils_advocate_report.md)
