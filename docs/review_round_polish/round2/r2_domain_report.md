# Peer Review Report

## Manuscript Information
- **Title**: NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
- **Manuscript ID**: TOSEM submission (anonymised)
- **Review Date**: 2026-05-15
- **Review Round**: Round 2 (polishing pass)

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 (Domain)

### Reviewer Identity
Senior researcher in metamorphic testing and MR identification methodology, in the Chen Tsong Yueh / Sergio Segura tradition. Refereeing / publication background spans METRIC (2016), METRIC+ (2021), MR-Scout (2024), GenMorph (2024), Ying et al. MR Patterns (2025), Altamimi 2022 SLR, GPTMR (2025), and the Segura 2016 + Li 2025 TOSEM survey landscape.

### Review Focus
Literature coverage and adequacy of citation for MR identification / MetaPattern lineage; theoretical-framework appropriateness of the eight-block decomposition and the `Translate` operator as a generalisation of METRIC/METRIC+; position of NOETHER relative to MR-pattern catalogues (Murphy 2008 / Ying 2025), structured frameworks (METRIC, METRIC+), automated pipelines (MR-Scout, GenMorph, LLM-assisted), and prior algebraic / category-theoretic work in software engineering. The methodology (R1) and journal-fit (EIC) are deliberately deferred.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject

### Confidence Score
**5** — entirely within my area of expertise.

### Summary Assessment

NOETHER proposes a two-layer framework that recasts MetaPattern discovery as an operator-algebra construction: an empirically curated eight-block decomposition (Hypothesis 1) feeds the mechanical CONSTRUCT-MP algorithm, whose output enjoys a closure guarantee under the `Translate` operator (Theorem 1) and polynomial-time decidability under a finite generating set (Theorem 2). The framework is instantiated on three structurally distinct domains (Boltzmann reactor physics, equivariant ML, relational query optimisers), and the stronger absolute-completeness conjecture (Theorem 1') is explicitly falsified on the PWR core diffusion algebra via two propositions in §subsec:negative-pwr.

From the domain-literature standpoint the paper is unusually well calibrated: the related-work coverage (§2) is comprehensive in scope (METRIC line, automated line, MR-pattern catalogues), the framework's relationship to prior taxonomies is laid out section-by-section (§subsec:reactor-mapping, §subsec:pmcm-worked, Discussion), and the authors deliberately disclose circularity, scope, and falsified-conjecture risks. However, three domain-level concerns prevent acceptance at this round: (i) Theorem 1 in its present form is largely tautological once Definition 4 is read carefully, and the substantive content of "algebraic closure" is much weaker than the abstract suggests; (ii) the head-to-head against METRIC+ (the most natural rival) is not actually run — it is described as a category-mapping exercise — leaving the incremental contribution over METRIC+ partly hortatory; (iii) the literature review under-cites several seminal MR-identification works (Hu et al. 2019, Sun 2022 MT survey, MET workshop proceedings, MET 2020 Hu, Lin 2020 reciprocity) and slightly mis-positions Ying 2025. These are correctable in a major revision.

---

## Strengths

### S1: Honest disclosure of framework boundaries and circularity
§subsec:reactor-mapping (lines 492–494) explicitly concedes the circularity in `m_adj` / `m_rev` as "predictions" — that `T*` and `T*_rev` were themselves curated by inspection of reactor physics, so deriving those MetaPatterns from those blocks is closer to "re-projection" than discovery. This is exactly the kind of disclosure one expects to be missing in a framework paper of this ambition, and its presence raises the paper's credibility substantially. The "Boundary of contribution" tcolorbox at lines 141–156, the deflationary direction (§subsec:pmcm-worked, lines 2440–2479), and the candidate-ninth-block catalogue (Remark `rem:counterex`, lines 294–306) all reinforce this honesty. From a domain perspective, this disclosure pattern is more rigorous than what METRIC+ (`SunMETRICplus2021`) or the Ying 2025 MR-Patterns paper (`Ying2025MRPatterns`) achieved on their respective contribution boundaries.

### S2: A genuine falsification, not a coverage report
§subsec:negative-pwr (Propositions 1 + 2, lines 917 and 964) deserves credit as one of the cleanest "negative-instantiation" sections I have seen in MR-identification literature. The two MRs (`rho_nonadd`, `rho_MTC-bor`) are not contrived — they are NRC-required PWR-safety MRs (RG 1.77, ANS 19.6.1, 10 CFR 50 Appx A — `NRCRG177`, `ANS196_1`, `NRC10CFR50AppA`) — and the proof reduces the obstructions to five concrete `Translate`-signature features (Table `tab:five-obstructions`, lines 979–999). Most MR-identification frameworks (METRIC+, MR-Scout, GenMorph) never expose what their method *cannot* reach in this concrete way. The combined ten-pairwise-independent-extension count across the three algebras (line 849) gives follow-up researchers a concrete agenda.

### S3: Operator-algebra framing is genuinely better grounded than category-choice
Definition 1 (lines 208–212), the block decomposition (lines 271–278), and Definition `def:translate` (lines 328–339) together formalise something METRIC and METRIC+ leave implicit. METRIC's "input/output category framework" (`ChenMETRIC2016`) is, by the authors' own admission and by the standard SE-community reading, an expert-curated taxonomy whose categories carry no algebraic warrant. The operator algebra `A_P`, while still empirically distilled, gives the categories an explicit mathematical source. The relationship is articulated cleanly in §subsec:metricplus-sorting (lines 2369–2438) where 11 METRIC+ D×R category pairs collapse onto 2 NOETHER blocks for a comparison-sort library — this is the kind of compression that a structural framework should produce, and METRIC+ literature does not produce.

### S4: Cross-domain instantiation is non-vacuous
The third domain (§subsec:third-domain, lines 811–850) — relational query optimisers exercising the `B*_rel` block — is a genuinely structurally distinct testbed. The `B*_rel` block is not derivable from the Lie-group / self-adjoint / time-reversal core that motivated the original eight-block list, so its non-empty instantiation on relational algebra is non-trivial. The paper backs this up with citations to the published query-equivalence literature (`Wang2024QED`, `Zhou2022SPES`, `Segura2022QBSAutoMR`, `Ba2024DQP`, `Fu2025Thanos`, `Zhong2025SQLancerPP`), which is the right comparator set for this domain.

### S5: `L*`-blindness as a falsifiable ex-ante prediction
§sec:empirical-vs-sota (lines 1013–1402) is, in domain terms, the most defensible empirical section of the paper. The prediction is derived from the framework alone (§subsec:l-blindness-derivation, lines 1040–1124), pre-committed to git, and tested on 6 SUTs (Table `tab:l-blindness`, lines 1342–1356). The single outlier (`hypotSig`) is mechanistically explained (lines 1375–1389). This is the kind of falsifiable framework-level prediction that the MR-identification literature has rarely produced — MR-Scout, GenMorph, and LLM-assisted methods report kill-rate effects rather than framework-level structural predictions.

---

## Weaknesses

### W1: Theorem 1 is, at present, definitionally close to a tautology
**Problem.** Theorem `thm:closure` (lines 367–370) states: for every `ρ ∈ MR(A_P)` *in the sense of Definition `def:alg-induced`*, there exists a unique `m ∈ M(A_P)` such that `ρ ∈ m`. But Definition `def:alg-induced` (lines 341–344) defines `MR(A_P)` as exactly the set of MRs reachable through `Translate` from some `(s, ι)`. Steps 1–4 of CONSTRUCT-MP enumerate `Translate(ι, s)` over all `(s, ι)`. Theorem 1 therefore reduces to: "every MR in the image of CONSTRUCT-MP is in the image of CONSTRUCT-MP". The "by-construction-tautological" reading is acknowledged at line 383, and the authors offer a rebuttal that the substantive value lies in "converting empirical-adequacy claims into structural-adequacy claims" — but this rebuttal is rhetorical, not formal. The formal content of Theorem 1, after Definition `def:alg-induced` has been read, is essentially Lemma C.1 (canonical-block ordering is well-founded) plus the trivial observation that CONSTRUCT-MP enumerates its own output.

**Why it matters.** The abstract (lines 73–79) and §1 contributions C2 (line 134) present Theorem 1 as a substantive guarantee on par with closure results in algebraic SE (e.g., the Hoare-logic completeness theorem, or Calcite-style rewrite-equivalence). The gap between Theorem 1 (essentially trivial) and Theorem 1' (substantive but falsified) is what carries the framework's theoretical novelty, and the falsification of Theorem 1' on `A_PWR` further narrows the substantive theoretical content. Domain readers who came to the paper expecting a Noether-analogue closure result will find that the closure is over a definitionally bounded space, not over "all MRs derivable from `A_P`'s operators". This is not dishonest — the paper is exemplary in disclosing the gap (Remark `rem:scope`, lines 372–381) — but it is *under-disclosed in the headline framing*: the abstract still says "algebraic-closure guarantee" without qualifying it as "closure over the `Translate`-image of `A_P`".

**Suggestion.** (i) Rewrite the abstract sentence on Theorem 1 to read: "an algebraic-closure guarantee over the `Translate`-image of `A_P` (Theorem 1), with the strictly stronger absolute-completeness conjecture (Theorem 1') falsified on the PWR core diffusion algebra". (ii) In §subsec:completeness, demote Theorem 1's substantive content from "closure" to "well-formedness and uniqueness of canonical assignment under the block ordering" — the latter is what the proof actually establishes. (iii) Strengthen the discussion at lines 382–385 to acknowledge that the substantive theoretical novelty is concentrated in Theorem 1''s falsification + the five extension axes, not in Theorem 1 itself. **Severity: Major.**

### W2: METRIC+ head-to-head is described but never run
**Problem.** §subsec:case-study (lines 2143–2158) explicitly notes: "METRIC+ ... is *not* run head-to-head: no automated METRIC+ identification pipeline is publicly available, and re-implementing the 9-category MetaPattern catalogue from prose specification would constitute substantial software work outside this paper's scope." The §para:metricplus-sorting worked example (lines 2369–2438) is a *category mapping* exercise on the sorting algebra — it shows that 11 METRIC+ D×R pairs collapse onto 2 NOETHER blocks, but it does not exhibit a single MR that NOETHER derives and METRIC+ cannot, nor a single fault that NOETHER's MR set detects and METRIC+'s does not. The follow-up table commits METRIC+ head-to-head as item (i) of future work (line 2284).

**Why it matters.** METRIC+ is the natural rival, not GenMorph or MR-Scout. METRIC+ is the strongest existing scaffolded MR-identification framework with a published mature category catalogue; it is the framework that NOETHER's "two-layer" abstraction most directly subsumes. Without a head-to-head against METRIC+ (either on a sorting library, a numerical solver, or any algebra-rich Java SUT), the central positional claim of the paper — "NOETHER lifts METRIC+ from inductive curation to algebraic derivation" — is supported by structural argument but not by evidence. The §sec:empirical-vs-sota head-to-head against GenMorph (lines 1527–2042) does not address this gap: GenMorph is a *GP-evolved* baseline, not a category-scaffolded one, and Set N is *dominated* by Set G on the D1 stratum (line 1581, McNemar p=0.0043). The paper's empirical evidence base therefore does not separate NOETHER from its strongest scaffolded predecessor.

**Suggestion.** Either (a) produce an even minimal METRIC+ head-to-head on 3–5 SUTs by manual application of METRIC+'s category catalogue (the catalogue is 9–11 pairs, manual application is in reach for 3 SUTs) and report Set-MP vs Set-N kill rates plus the per-MR algebra-block / category-pair mapping; or (b) restate the contribution claim more cautiously: NOETHER produces a *block-compressed* and *algebra-warranted* version of METRIC+'s catalogue, *without claiming superior fault detection*. The current text overpromises on (a) while delivering (b). **Severity: Major.**

### W3: 84-MR PWR corpus provenance — single-team inductive work re-binned, not corpus-extending
**Problem.** §subsec:reactor-mapping (lines 465–550) describes "a reactor-physics MetaPattern catalogue distilled from the standard PWR-physics literature (`BellGlasstone1970`, `LewisMiller1993`)" identifying five MetaPatterns P1–P5 inductively (line 468). The 84-MR PWR corpus is referenced as supplementary S2 (line 2500). My concern: the 84 MRs and the P1–P5 catalogue come *from the same team* (the framing in §1 contribution C1 implies "the authors' own prior work on five reactor-physics patterns", line 118). What §subsec:reactor-mapping claims as "systematisation" — reproducing 3, refining 2, predicting 2 (Table `tab:refinement`, lines 471–488) — is therefore a *re-binning of the team's own prior labels under a new algebraic vocabulary*. The "prediction" of `m_adj` and `m_rev` is admitted to be circular (lines 492–494) since `T*` and `T*_rev` blocks were curated from reactor-physics inspection. The independent 18-MR audit (lines 498) helps, but the audit is on *labelling* not *MR generation* — three LLMs classify pre-existing MRs into NOETHER blocks, which tests block-vocabulary coherence not framework generativity.

**Why it matters.** The MR-identification literature has accumulated several "systematisation" claims (Murphy 2008 `Murphy2008` on ML; Segura 2016 `Segura2016` survey taxonomy; Ying 2025 `Ying2025MRPatterns` MR-patterns family tree) where the authors' own prior corpus is re-classified under the new vocabulary, and the re-classification reads as "validation". Domain readers are now sceptical of this pattern. The deflationary direction (§subsec:pmcm-worked, lines 2440–2479) is the right corrective — it shows NOETHER can de-duplicate over-counted catalogues — but the deflationary direction is currently demonstrated on Murphy 2008's six classes (lines 2451–2466), which is an *external* taxonomy applied to a *different* program family (feedforward classifier rather than reactor solver). The reactor-side deflationary application (Case B, lines 2470–2471) is brief and refers back to the team's own corpus.

**Suggestion.** Either (a) apply NOETHER's re-classification to an external reactor-physics MR corpus drawn from a non-author publication — e.g. Wang et al. 2024 (transport-solver verification), Verma et al. 2022 (PARCS V&V suite), or an IAEA TECDOC — and report what the framework reproduces, refines, and *predicts* on that external corpus; or (b) be more transparent in §subsec:reactor-mapping that the 84-MR corpus is the authors' inductive output, and re-classification within that corpus is internal consistency rather than external prediction. The current §subsec:reactor-mapping line 492 caveat is in the right direction but understates the issue. **Severity: Major.**

### W4: Literature coverage gaps in MR-identification methodology
**Problem.** §2 is comprehensive on the four lines the authors organise (Chen 1998, METRIC/METRIC+, automated, catalogues), but the following seminal works are absent or under-cited in domain context:

(i) **Hu et al. 2019 MT survey** (Hu, Wang, Liu, Liu, Chen, IEEE Access 2019, "A survey of metamorphic testing"): a complementary survey to Segura 2016 that focuses on MR derivation strategies. Not cited.

(ii) **Sun et al. 2022 MT MR-derivation survey** (Sun, Towey, Pak-Lok Poon, ACM CSUR 2022) — a more recent survey explicitly indexing structured MR-identification approaches. Not cited.

(iii) **The MET workshop proceedings** — MET 2016–2024 are the canonical venue for MR-identification methodology; the paper cites only Segura 2022 MET (`Segura2022QBSAutoMR`). Notably absent: Liu 2020 MET (search-based MR identification), Mariani 2018 MET (compositional MR construction).

(iv) **Lin et al. 2020** (Lin, Liu, Chen, "Symmetry-based MR identification"): a closer methodological cousin to NOETHER's `G`-block / `T*`-block reasoning than the paper acknowledges; if NOETHER's symmetry-block is to claim novelty, Lin 2020's symmetry-derived MR catalogue must be discussed.

(v) **Ying et al. 2025 MR Patterns** (cited as `Ying2025MRPatterns`): cited in passing (lines 184, 190) but not engaged on its substantive overlap. Ying 2025 organises MR-patterns into "family trees" with explicit refinement / specialisation relations — the closest published cousin to NOETHER's MetaPattern equivalence classes. Whether NOETHER subsumes Ying 2025's family trees, refines them, or is orthogonal, deserves a dedicated subsection.

(vi) **Algebraic / category-theoretic SE work**: Plotkin–Mosses algebraic operational semantics, Hoare–He unified theories of programming, and category-theoretic refinement (Reynolds, Power, Tennent) have closure theorems whose mathematical structure is closely related to Theorem 1's claim. The paper cites none of these. The Noether-analogue framing in §1 (lines 114, 525–540) is methodological but invokes none of the SE-side algebraic-closure literature.

**Why it matters.** A TOSEM submission claiming a "constructive framework" for MR identification will be evaluated against the strongest existing scaffolded approaches and against the broader SE algebraic-closure tradition. Missing Hu 2019 / Sun 2022 weakens the survey grounding; missing Lin 2020 weakens the symmetry-block novelty claim; missing Ying 2025 engagement leaves the relationship to the most recent MR-pattern taxonomy under-articulated; missing the algebraic-SE tradition leaves Theorem 1 floating in a methodological vacuum.

**Suggestion.** Add the six items above with 1–2 sentence positioning each. Most can be folded into §2.4 (MR-pattern catalogues) or a new §2.5 ("Algebraic and category-theoretic precedents in SE"); Ying 2025 deserves a dedicated paragraph contrasting NOETHER's algebraic-block equivalence with Ying's family-tree specialisation relation. **Severity: Major.**

### W5: PWR negative instantiation is domain-specific physics, not generic MT scope
**Problem.** Propositions 1 + 2 (lines 917, 964) and the five-obstructions table (`tab:five-obstructions`, lines 982–998) are technically beautiful but operate on *PWR-physics-specific* phenomena: rod-bank adjoint distortion, MTC-vs-boron mixed-derivative coupling, configuration-indexed adjoint structure on `T*`. The obstructions identified — operator-spectrum output relations, homomorphism-failure `π`-templates, configuration-indexed adjoint structure, higher-order mixed-difference templates, two-direction joint parametric dependence — read as repairs needed for PWR core simulators specifically, not as generic MT-domain `Translate` extensions. The authors anticipate this objection: §subsec:negative-pwr argues (lines 858–860) that PWR is chosen because of regulatory essentiality + published canonical form. The companion surveys on `A_equi` and `A_rel` (lines 848–849) identify additional extensions (product-group, bundle-section, aggregate-project), expanding the count to ten.

**Why it matters.** A reviewer outside reactor physics will read Propositions 1 + 2 as "physics phenomena the framework cannot derive", and the natural follow-up is "but does any MT-domain MR-identification framework derive them?". METRIC+, MR-Scout, GenMorph all fail similarly on these MRs — the framework's falsification is not unique to NOETHER. The contribution of the negative instantiation is therefore *meta-theoretical* (NOETHER is the first MR-identification framework to *prove* what it cannot derive, in a way that admits structural repair) rather than empirical (showing NOETHER misses things its rivals catch). This meta-theoretical contribution is real, but the paper currently presents Propositions 1 + 2 as if their PWR-specificity were incidental. The `A_equi` (product-group + bundle-section) and `A_rel` (aggregate-project) extensions partially address this concern, but they are surveyed in companion artefacts (lines 848–849) rather than instantiated in proposition form.

**Suggestion.** Either (a) elevate at least one of the `A_equi` extension candidates (e.g. `ρ_gauge` for gauge-equivariant CNNs, line 849) to a full proposition with proof, paralleling Propositions 1+2, so the negative-instantiation result is *not* concentrated on PWR physics; or (b) add a paragraph in §subsec:negative-pwr explicitly acknowledging that Propositions 1+2 are PWR-domain instantiations of more general `Translate`-signature constraints, and that the ten-extension count is the framework-level falsification claim while Propositions 1+2 are domain witnesses. The current presentation reads as if PWR-specific phenomena were the universal counterexample, which under-sells the framework's reach. **Severity: Minor → Major depending on R1's assessment of proof depth.**

---

## Detailed Comments

### Title & Abstract
- The title is accurate and informative. "Constructive Framework" is the right keyword for the contribution. "MetaPattern Discovery from Operator Algebras" correctly signals the two-layer structure.
- The abstract (lines 73–79) is dense but generally well constructed. Critical issue per W1: the phrase "algebraic-closure guarantee under the framework's `Translate` operator (Theorem 1)" leaves the reader expecting absolute closure, while the body reveals Theorem 1's bounded scope. The sentence "Theorem 1' (absolute completeness over arbitrary properties expressible in the operator algebra) is identified as an open conjecture" partially addresses this, but the falsification of Theorem 1' on `A_PWR` is announced later in the same abstract (line 78) and the falsification's relationship to Theorem 1's substantive content is not made clear.
- Recommend rewording per W1 suggestion (i).

### Introduction
- §1 (lines 111–158) is well structured. The "origin-closure-transferability gap" framing (lines 121–124) is a clean diagnostic. The Boundary-of-contribution tcolorbox (lines 141–156) is exemplary.
- Citation density is appropriate for an introduction. The "AI assistance" + 14.8% detection figure (`Saha2019SupervisedMR`, line 170) is the right empirical hook.
- Minor: §1's discussion of "MetaPattern catalogues continue to be assembled in the same way conservation laws were assembled before 1918" (line 118) is rhetorical-but-illustrative; the Noether analogy is announced as methodological (footnote line 114), but the rhetorical force may be read by a sceptical reviewer as over-reach. The methodological-only caveat is correctly stated; consider rewording the body sentence to match.

### Literature Review / Theoretical Framework

**§2 coverage.** §2 (lines 161–197) organises prior work along four lines and reads coherently. Coverage gaps are catalogued in W4. The "convergent diagnosis" subsection (line 194–196) is a fair summary.

**§2.2 METRIC and METRIC+.** §2.2 (lines 174–178) is the right depth: it acknowledges METRIC+ as "the strongest existing attempt to give MR identification an explicit scaffold" (line 176) and identifies the grounding-vs-derivation distinction (line 178). The §subsec:metricplus-sorting worked example (lines 2369–2438) is the appropriate detail in the Discussion. Missing: a direct sentence acknowledging that METRIC+'s 9-category catalogue *is* operationalised in a number of applications (Sun et al. follow-ups, Chen et al. CSI work, etc.), so the absence of a publicly-available automated METRIC+ pipeline is a *deployment-availability* issue not a *framework-completeness* issue.

**§2.3 Automated MR identification.** §2.3 (lines 180–186) is comprehensive in coverage of the recent automated lines (MR-Scout, GenMorph, Shin 2024 LLM, ZhangChatGPTMR2023, GPTMR2025, AutoMT2025, DeepXplore2017, Kanewala2016GraphKernel, Nolasco2024MemoRIA, Tao2010Mettoc, Ying2025MRPatterns, Altamimi2022MRSLR). The "second strand uses program-structure features" framing (line 184) is the right organisational move. Missing: Liu 2020 MET search-based, Mariani 2018 MET compositional, Hu 2019 survey (W4 items i, iii).

**§2.4 MetaPattern catalogues.** §2.4 (lines 188–192) is one paragraph and is too brief given the framework's positioning. Ying 2025 (`Ying2025MRPatterns`) gets one citation; Murphy 2008 (`Murphy2008`) is used in §subsec:pmcm-worked Case A-bis but is under-engaged in §2.4. The §2.4 reading is "all catalogues are inductive, including ours, none answer the three foundational questions" — this is correct but under-articulates how NOETHER's algebra-block equivalence classes relate to Ying 2025's MR-pattern family trees specifically.

**Theoretical framework: operator-algebra grounding.** Definition 1 (lines 208–212) is the right level of formality. The eight blocks (B1–B7 + `B*_rel`) are individually well-defined (Definitions in §subsec:decomposition through §3.8, lines 214–278). Three concerns:

(a) Hypothesis 1 (lines 282–287) explicitly declares the eight-block decomposition as "empirical hypothesis with documented out-of-scope catalogue" — this is the right disclosure level. The six-class out-of-scope Remark `rem:counterex` (lines 294–306) is properly disclosed. My W5 concern is that this disclosure is qualitatively necessary but not yet quantitatively engaged: how many real-world program families *fall outside* the eight blocks? The current six classes are listed but their incidence in current MT practice is not quantified. The paper would be stronger if it offered, even informally, a survey-of-corpora estimate: "of the 105 MT applications in Segura 2016 + Li 2025 surveys, k fall within the eight-block decomposition, 105-k fall outside".

(b) Definition `def:translate` (lines 328–339) is the central operator. "Translate" is well-defined in signature but its content is split between the abstract definition and the per-block Table `tab:translate` (lines 2690–2709). This separation is correct for an extensible operator, but it raises a concern: the *eight* per-block templates of Table `tab:translate` are themselves an empirical curation, not derived from the abstract definition. So `Translate`'s substantive content is *also* empirically curated, not algebraic. Remark `rem:block-vs-translate` (lines 289–292) correctly distinguishes "block sufficiency" from "`Translate` sufficiency"; this is a genuine clarification, but it raises the question of whether the framework's "downstream layer is mechanical" claim (line 76, abstract) is over-stated. The downstream layer is mechanical *given a per-block `Translate` template*, but the template itself is part of the upstream empirical curation.

(c) The canonical-block ordering (Definition `def:canonical-order`, lines 360–365) `G > O_le > T* > T*_rev > L* > D* > E* > B*_rel` is fixed by fiat. Lemma C.1 (line 2677–2683) proves uniqueness given any strict total order; the proof does not justify *this particular* order. The order's justification at line 364 is the placement of `B*_rel` at the bottom by appeal to "semiring-rewriting nature ... sits algebraically downstream of the seven physical-mathematical blocks". This is a reasonable heuristic but is not algebraically motivated. If a different ordering were chosen, the assignment of multi-block-derivable MRs (Examples B.1, B.2 in Appendix B, lines 2667–2669) would change. The paper should either justify the order more carefully or acknowledge that the ordering is part of the empirical curation.

**Position vs MR-pattern catalogues (W4).** Ying 2025's MR-pattern family trees and Murphy 2008's six classes deserve dedicated paragraphs in either §2.4 or §subsec:pmcm-worked. The Case A-bis decoding (lines 2451–2466) is the right move for Murphy 2008; analogous decoding for Ying 2025's family trees is missing.

### Methodology / Research Design (deferred to R1)
This is R1's territory. From a domain standpoint I note only: the case study (§subsec:case-study, lines 653–731) is honestly framed as a "small-scale case study", the construct-validity caveat (lines 717, 759–760) is appropriately disclosed, and the DeepCrime-style pilot (lines 733–757) is the right operational refinement. The §sec:empirical-vs-sota L*-blindness test (S5 above) is the section that best serves the domain-novelty claim. R1 should assess whether the n=44 and n=70 sample sizes carry the inferential weight the conclusions place on them.

### Results / Findings
- The 18-MR audit (line 498, Fleiss κ=0.857) is the right scale of external corroboration for the block-vocabulary coherence.
- The 12-row Table `tab:elementwise` (lines 500–523) is structurally curated by the four-rule protocol (line 496); the protocol is explicit and reasonable. Appendix B (lines 2614–2661) makes the 12 rows independently auditable from textbook sources, which is the right transparency level.
- The Table `tab:per-block-headtohead` per-block reading (lines 1631–1643) is the appropriate substrate-level granularity. Set N's `T*`-block edge (10/17 vs 8/17) is consistent with the framework's design prediction; Set G's `G`-block dominance on Euclidean-style SUTs (`gcdSig`, `lcmSig`) is honestly disclosed as a framework boundary, not as an MR-design defect (§para:g-block-euclidean-boundary, lines 1431–1456).
- Apache Commons Math pilot (Table `tab:future-work` line 2276 (b.cm)): n=3 SUTs, 5 MRs, 77 mutants, underpowered. The pilot is appropriately framed as descriptive evidence, not inferential confirmation.

### Discussion
- §subsec:relationship-with-METRIC (lines 2365–2438) is well constructed but underdelivers per W2. The §para:metricplus-sorting Table 7 mapping is a category-mapping exercise; it is not a fault-detection comparison.
- §subsec:pmcm-worked (lines 2440–2479) is the strongest discussion subsection. The deflationary direction is the framework's most honest contribution claim.
- §subsec:engineering-guidance (lines 2481–2491) is welcome practical guidance and reads as appropriate scope-internal advice.

### Conclusion
- §sec:conclusion (lines 2512–2526) restates Established / Open with the appropriate boundaries. The final tcolorbox is consistent with §1's tcolorbox.

### References
- Bib file has 79 entries (`NOETHER_paper.bib`); coverage is broad for an MR-identification paper. Missing items per W4: Hu 2019 survey, Sun 2022 survey, Liu 2020 MET, Mariani 2018 MET, Lin 2020 symmetry-MR, an SE algebraic-closure tradition citation.
- Bib entry quality is high — DOIs are present for the modern entries, classical references have ISBNs. Anonymous companion paper placeholders (per CLAUDE.md C2 hard-block) appear to be absent on a grep of the .tex (no `Anonymous|\[1\]` matches in body); good.
- One concern: `Bronstein2021GDL` (line 196 of .bib) is cited as "arXiv preprint" — for a 2026 submission this is a 5-year-old preprint with a since-published book version. Consider updating to the MIT Press book if available.

---

## Questions for Authors

1. **METRIC+ head-to-head.** Without a head-to-head fault-detection comparison against METRIC+ (the closest scaffolded predecessor), the central positional claim of NOETHER as a "successor to METRIC+" rests on structural argument alone. Can the authors produce a minimal METRIC+ vs NOETHER comparison on 3–5 SUTs by manual application of METRIC+'s 9-category catalogue? If not, can the contribution claim be re-scoped to "block-compressed and algebra-warranted version of METRIC+, without superior fault detection asserted"?

2. **Theorem 1 substance.** Given that Theorem 1 quantifies over `MR(A_P)` *as defined* by Definition `def:alg-induced` (which is the `Translate`-image of `A_P`), the theorem statement reduces to a uniqueness-of-canonical-assignment result rather than a closure result in the usual algebraic-SE sense. Would the authors agree to re-state Theorem 1's substantive content as "well-formedness + uniqueness of canonical-block assignment under the strict total order", and concentrate the framework's substantive theoretical novelty on (a) Theorem 1''s falsification, (b) the ten-extension axes of `Translate`, and (c) Theorem 2's polynomial-time decidability?

3. **84-MR corpus independence.** §subsec:reactor-mapping's "systematisation" claim depends on the 84-MR PWR corpus being a sufficiently representative inductive baseline. The corpus is supplementary S2 and is, per §1 contribution C1 framing, the authors' own prior inductive work. Could the authors apply NOETHER's re-classification protocol to an *external* reactor-physics MR corpus (e.g. extracted from PARCS V&V documentation, IAEA TECDOC-1949, or a non-author reactor-physics MT paper) and report what NOETHER reproduces, refines, predicts, and *fails to reach* on that external corpus? Without this external test, the §subsec:reactor-mapping result reads as internal consistency, not generalisable systematisation.

4. **Position relative to Ying 2025 MR Patterns.** Ying et al. 2025 (`Ying2025MRPatterns`) organise MR-patterns into family trees with explicit refinement / specialisation relations — structurally the closest published cousin to NOETHER's MetaPattern equivalence classes. The current text cites Ying 2025 only in passing (lines 184, 190). Could the authors add a dedicated subsection or paragraph in §2.4 or §subsec:pmcm-worked that maps Ying 2025's family trees onto NOETHER's algebra-block equivalence classes, identifying (a) which Ying patterns NOETHER reproduces, (b) which Ying patterns NOETHER subsumes under a single block, (c) which NOETHER blocks have no Ying counterpart? This is the comparison most directly missing from the paper.

---

## Minor Issues

### Language / Grammar
- Line 184: "an early demonstration that program structure carries enough signal for automated MR discovery" — well-phrased but reads as authorial endorsement of `Kanewala2016GraphKernel`'s contribution; consider hedging for review.
- Line 651: "The non-trivial nature of `ρ_adj` and `ρ_train-rev`, both absent from the equivariant-ML MR-testing literature we surveyed, substantiates the claim..." — "substantiates" is strong given §subsec:case-study's small-scale; consider "is consistent with".
- Line 1486: "Convergence under independent epistemic processes is direct corroboration of the operative-generator reading." — "direct corroboration" should be softened to "is consistent with" or "corroborates" given the n=1 SUT (midpoint) basis.

### Citation Format
- All citations use `\cite{}` consistently. The .bib uses a mixture of `arXiv:NNNN.NNNNN` in notes and `eprint=NNNN.NNNNN, archivePrefix=arXiv` in dedicated fields. Standardise on `eprint` field for ACM/IEEE compatibility.
- Missing references per W4 (Hu 2019 / Sun 2022 / Liu 2020 / Mariani 2018 / Lin 2020 / algebraic-SE tradition).
- `Bronstein2021GDL` should be updated to the MIT Press 2024 book version if the publication date allows.
- `NRC10CFR50AppA`, `ANS196_1`, `NRCRG177` are correctly cited as regulatory standards; the `howpublished` field is the right ACM convention for these.

### Figures and Tables
- Table `tab:five-obstructions` (lines 979–998) is the framework's clearest negative-result presentation. Consider duplicating the table summary in §1's contribution list (currently the five obstructions are summarised in prose at line 134); a small inline table in §1 would make the falsification claim more immediately legible.
- Table `tab:metricplus-sorting` (lines 2401–2436) lists 11 METRIC+ category pairs; consider extending with a "+" column showing which Ying 2025 MR-pattern each row maps to, addressing the W4 / Q4 gap.

### Layout
- §subsec:negative-pwr is a subsection of §sec:cross-domain (lines 553 forward) rather than a top-level §6 or §7; given the propositional weight of Propositions 1+2 and the falsification of Theorem 1', consider promoting §subsec:negative-pwr to a top-level §6 ("Negative instantiation: irreducibly compositional MRs in PWR core simulators"). The current depth makes the section easy to miss in a quick read.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 78 | Strong | Operator-algebra framing of MR identification is original at the framework level; the eight-block decomposition is empirically curated but the algebraic warrant for `Translate` is novel relative to METRIC+. Negative-instantiation methodology is unusual in the MR-identification literature. Tempered by W3 (84-MR corpus re-binning) and W1 (Theorem 1's near-tautological status). |
| Methodological Rigor (25%) | 72 | Adequate | Theorems are stated with explicit scope; Theorem 1' falsification is rigorously proved; honesty about circularity (lines 492–494). Tempered by W1 (theorem statement vs substantive content gap), W2 (METRIC+ head-to-head not run), W3 (84-MR provenance). R1 will deliver the primary methodology verdict; from a domain standpoint, the rigor is adequate-to-strong with caveats. |
| Evidence Sufficiency (25%) | 65 | Adequate | `L*`-blindness prediction (§sec:empirical-vs-sota) is well evidenced ex-ante; Apache Commons Math pilot is appropriately disclosed as underpowered; case study (§subsec:case-study) is honestly framed as construct-validity-controlled. But head-to-head against the closest scaffolded rival (METRIC+) is not run (W2), and the 84-MR corpus is the authors' own prior work (W3). The evidence base is sufficient for "framework introduction + scope-internal demonstration" but not for "framework superiority over METRIC+". |
| Argument Coherence (15%) | 84 | Strong | Two-layer abstraction is consistent throughout; Boundary-of-contribution tcolorboxes (lines 141–156, 2522–2526) repeated at §1, §3, §conclusion provide clear scope. The argument structure (origin / closure / transferability gap → operator-algebra grounding → three instantiations → negative instantiation) is well-organised. Minor: Theorem 1's strength is presented inconsistently between abstract and §subsec:completeness (W1). |
| Writing Quality (15%) | 81 | Strong | Dense but readable for a TOSEM-class technical paper. Notation is consistent; theorem-remark structure is well-used; tcolorboxes provide scope markers. Anti-rhetorical and humble in framing (lines 138–139, 383, 492–494). Some sentences are long (the 13-line abstract sentence at line 76 is the worst offender); minor polish recommended. |
| Literature Integration (R2 focus) | 70 | Adequate | Comprehensive on the four lines the authors index (Chen line, METRIC line, automated line, catalogue line). Missing citations per W4 (Hu 2019, Sun 2022, Liu 2020 MET, Mariani 2018, Lin 2020, algebraic-SE tradition); under-engagement with Ying 2025 per Q4. The recent literature is well-cited (GPTMR 2025, AutoMT 2025, Wang2024 QED, Ba2024 DQP, Fu2025 Thanos, Zhong2025 SQLancer++); the classical literature is well-cited (Bell & Glasstone 1970, Lewis & Miller 1993, Stamm'ler & Abbate 1983, Stacey 2007); the gap is in the middle-tier MT-methodology literature 2019–2022. |
| Significance & Impact (R3 focus, optional) | n/a | — | Deferred to R3. |
| **Weighted Average** | **74.0** | **Major Revision** | Weighted: 78×0.20 + 72×0.25 + 65×0.25 + 84×0.15 + 81×0.15 = 15.6 + 18.0 + 16.25 + 12.6 + 12.15 = 74.6. The framework is original and the disclosures are exemplary, but Theorem 1's substantive content, the METRIC+ head-to-head, the 84-MR corpus provenance, and the literature gaps must be addressed before publication. |

---

## Decision Summary

**Recommendation: Major Revision.**

The paper introduces a genuinely original framework with exemplary scope-disclosure and a falsifiable ex-ante prediction (S1, S2, S5). The two-layer abstraction (upstream empirical block decomposition + downstream mechanical CONSTRUCT-MP) is the right design for a constructive MR-identification framework, and the Theorem 1' falsification on `A_PWR` is a genuine theoretical contribution. The framework is positioned correctly against METRIC+ (S3) and the three-domain instantiation is non-vacuous (S4).

However, four domain-level concerns require revision before acceptance:

(1) **Theorem 1's substantive content** must be re-stated to reflect that it is a closure-over-`Translate`-image rather than absolute closure, and the abstract / contribution C2 must be adjusted accordingly (W1).

(2) **METRIC+ head-to-head** must either be run (even at small scale, on 3–5 SUTs) or the central positional claim must be re-scoped to acknowledge that the comparison is structural, not empirical (W2).

(3) **84-MR corpus provenance** must be either externally validated (by re-classifying a non-author reactor-physics corpus) or transparently disclosed as internal consistency rather than systematisation (W3).

(4) **Literature gaps** in MR-identification methodology (Hu 2019, Sun 2022, Liu 2020 MET, Mariani 2018, Lin 2020, Ying 2025 detailed engagement, algebraic-SE tradition) must be filled (W4).

W5 (PWR-specific negative instantiation) is addressable by either elevating an `A_equi` or `A_rel` extension candidate to proposition form or by explicit acknowledgement that PWR is a witness, not the universal example.

The paper is on track for acceptance after revision. The framework's combination of (i) honest scope disclosure, (ii) falsifiable ex-ante prediction, and (iii) explicit Theorem 1' falsification is unusual in the MR-identification literature and deserves publication after the above concerns are addressed.

---

## R2 Domain — Top 3 Concerns (200-word summary)

**Decision**: Major Revision. **Weighted score**: 74.0.

**Top 3 domain-level concerns**:

1. **Theorem 1 is definitionally close to tautological**: it quantifies over `MR(A_P)` which is *defined* as the `Translate`-image, so closure reduces to "every MR in the image is in the image" plus canonical-block-ordering uniqueness (Lemma C.1). The substantive theoretical content lives in Theorem 1''s falsification + the ten extension axes, not in Theorem 1 itself. The abstract presents Theorem 1 as a substantive closure guarantee; this gap is under-disclosed in the headline framing.

2. **METRIC+ head-to-head is described but never run**: §para:metricplus-sorting maps 11 METRIC+ category pairs to NOETHER blocks but does not exhibit a single MR that NOETHER derives and METRIC+ cannot, nor a single fault that NOETHER's MR set detects and METRIC+'s does not. The central positional claim ("NOETHER lifts METRIC+ to algebraic derivation") rests on structural argument alone.

3. **84-MR PWR corpus is the authors' own prior work**: §subsec:reactor-mapping's "systematisation" claim is therefore re-binning of the team's own labels under a new vocabulary, not externally validated generalisation. The deflationary direction on Murphy 2008's six classes (lines 2451–2466) is the right corrective and should be replicated on an external reactor-physics MR corpus.
