# Peer Review Report

## Manuscript Information
- **Title**: NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
- **Manuscript ID**: ACM TOSEM (anonymised submission)
- **Review Date**: 2026-05-15
- **Review Round**: Round 2 (polish round)

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 (Methodology)

### Reviewer Identity
Senior empirical software engineering methodologist in the Wohlin / Briand tradition. Domain expertise: experimental design for software-testing studies, PIT mutator semantics, Wilson confidence intervals and McNemar paired testing, threats-to-validity taxonomies (Wohlin 2012), statistical reporting standards for ICSE / TSE / TOSEM, and reproducibility audits.

### Review Focus
Experimental design rigour across the three empirical components (re-classification of the 84-MR PWR corpus, the SE(3)-equivariant ML case study, and the head-to-head PIT-mutated Java methods); sample sizes and statistical power; correctness of Wilson CIs, McNemar p-values and effect-size reporting; construct, internal and external validity; reproducibility of the supplementary scripts. Journal-fit and literature-coverage commentary deferred to R2/R3 / EIC.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision** — substantial revisions needed, re-review required after revision
- [ ] Reject

### Confidence Score
**4** — Mostly within my area of expertise. The operator-algebra layer (Sections 3–4) is outside my primary expertise and I defer the algebraic-closure / decidability theorems to R2 / R3; my assessment is focused on the empirical sections §§5–7 and the supplementary materials.

### Summary Assessment
NOETHER proposes a two-layer framework for MetaPattern discovery: an algebraic downstream layer (CONSTRUCT-MP) with closure and decidability theorems, and an empirical eight-block upstream layer that is honestly framed as a hypothesis. Three empirical components are reported: (i) re-classification of an 84-MR PWR corpus into the eight blocks (§5, Table 3, with an 18-MR LRCA audit at Fleiss' κ = 0.857); (ii) a 20-mutation hand-constructed SE(3)-equivariant ML case study (Set N 7/20, Set L 2/20, Set B 0/20; §6.6); (iii) a head-to-head against GenMorph on 10 Java SUTs with n = 57 paired PIT mutants (D1 n = 52, D2 n = 5; McNemar p = 0.0043 pooled, p = 0.019 D1-only; §subsec:pooled-headtohead), plus an L*-blindness falsifiability test passing on 5/6 SUTs. From a methodology lens, the statistical machinery is competent (all Wilson CIs and McNemar p-values I spot-checked replicate exactly) and the disclosure of underpowered strata is mostly honest. However, **three issues are load-bearing and require resolution before acceptance**: (a) the §6 Set L baseline is implemented in `supplementary/S3_case_study/mr_sets/set_L_llm.py` as author-written "expected-shape placeholders" rather than as the GPT-4 output the paper text claims; (b) the head-to-head superiority framing on D1 has been retreated from in commit 6f3407f but the prose still oscillates between "competitive parity" and "Set N is dominated"; (c) the construct-validity of the §6 case study is acknowledged but the cat-(iv) 5/5 result still leaks into the abstract's hypothesis-confirmation language. The empirical scaffold is fundamentally rescuable; the path is disclosure-and-rework, not redesign.

---

## Strengths

### S1: Honest pre-registration of falsifiability and the L*-blindness derivation
The §subsec:l-blindness-derivation prediction is genuinely derivable ex-ante from the framework (CONSTRUCT-MP's `Translate` template) and PIT 1.7.4's public mutator specification. The prediction is sharp: "one third or more on more than one SUT" is the falsification threshold, with the 1/3 threshold and "more than one SUT" quantifier committed to git in `configs/d4j_algebra_rich_criterion.json` ahead of per-MR kill counts. The observation (5/6 SUTs at zero kills; hypotSig at 2/4 with the two killed mutants both genuinely homogeneity-breaking by the predicted exception clause) is the kind of quantitative falsifiable test the operative-mechanism reading of the eight-block decomposition warrants. The threshold sensitivity grid (lines 1107–1112) is well done; the verdict is robust to plausible threshold variation. This is the methodologically strongest single element of the paper.

### S2: Statistical computations are correct
I re-computed every Wilson 95% CI and McNemar p-value reported in §6.6 and Tables 7, 8, 9, 11 against the underlying counts. All match. Specifically: Set N 7/20 → [0.181, 0.567] ✓; Set L 2/20 → [0.028, 0.301] ✓; Set N 26/52 D1 → [0.369, 0.631] ✓; Set G 37/52 D1 → [0.577, 0.817] ✓; T* Set N 10/17 → [0.360, 0.784] ✓; T* Set G 8/17 → [0.262, 0.690] ✓; G-block N 2/11 → [0.051, 0.477] ✓; pooled N 26/57 → [0.334, 0.584] ✓; McNemar pooled (b,c) = (18,4) → p = 0.00434 ✓; D1-only (b,c) = (15,4) → p = 0.0192 ✓; D2 (3,0) → p = 0.25 ✓; case-study N-vs-L (5,0) → p = 0.0625 ✓; N-vs-B (7,0) → p = 0.0156 ✓. Holm–Bonferroni correction for the 16 per-SUT comparisons is correctly applied (α/16 ≈ 0.003, no per-SUT contrast meets the threshold; the paper correctly labels per-SUT Δ as "directional descriptors only", line 1542). This level of statistical care is above the median TOSEM submission.

### S3: Threats-to-validity organisation is comprehensive and Wohlin-compliant
§subsec:empirical-threats (lines 2044–2160) covers (a) prediction commitment, (b) Set G budget asymmetry, (c) sample size, (d) Set G structural absence as upstream-snapshot-relative, (e) substrate selection, (f) three SOTA-category coverage with baseline-strength caveats. §7.1 (§subsec:four-threats, lines 2353–2363) explicitly invokes Wohlin's four-validity framework (internal / external / construct / conclusion) with substantive content under each heading. The construct-validity treatment of the cat-(iv) 5/5 result in Table 4 — that the mutation set was *constructed* to cover one defect category per non-empty block, so the result exhibits construct validity of ρ_train-rev rather than averaged superiority — is honest and appears repeatedly (lines 693, 717, 760, 2359). The framework-boundary discussion at §para:g-block-euclidean-boundary (lines 1431–1455) is methodologically exemplary: the 0/7 Set N kill rate on gcdSig + lcmSig is read as the framework-correct verdict under the scope precondition rather than as MR-design failure, and the reasoning (the SUT's `a < 0 ? -a : a` prologue absorbs the G-action) is concrete and inspectable.

### S4: D1 / D2 stratification operationalises the framework's scope claim
The §subsec:pit-block-matrix Table 5 mapping of PIT mutator categories × NOETHER blocks (with ○ = preserves invariant / × = breaks / ∼ = case-dependent), combined with the per-mutant D1 / D2 classification (52 D1 / 5 D2 / 0 ambiguous after equivalent-mutant exclusion), provides a principled basis for the framework's "Set N is by construction silent on algebra-preserving mutants" claim. The D2 prediction (≤ 10%) is consistent with the observed 0/5 on D2 (Wilson upper bound 0.434 correctly does *not* exclude the ceiling at n = 5, and the paper says so, lines 1768–1776); the cross-codebase commons-math pilot at 2/29 = 6.9% (Wilson [0.012, 0.221]) corroborates the direction at slightly larger n. This is the right way to operationalise a scope claim in an empirical context.

### S5: LRCA multi-LLM second-rater protocol on Set N derivation
§subsec:four-threats (lines 2359) reports Cohen's κ = 0.927–0.929 between the author and each of three LLM raters on the 36-MR Set N catalogue, with Fleiss' κ = 1.000 across the three LLMs on n = 33 parseable items and majority-vote κ = 0.931 on n = 36. The 18-MR engineering-catalogue audit at Fleiss' κ = 0.857 (line 498) is a separate broader breadth check. The LLM-shared-training-data caveat is explicitly stated and a human-pair κ replication is committed for industrial-port follow-up. Within the constraint of the single-author Set N derivation, this is a reasonable construct-validity check.

---

## Weaknesses

### W1: Set L in the §6 equivariant-ML case study is author-written "placeholders", not GPT-4 output, despite paper claim to the contrary
**Problem**: The paper at line 665 describes Set L as "five MRs generated by prompting GPT-4 with the task description 'produce five metamorphic relations for testing an SE(3)-equivariant point-cloud classifier'", and line 760 states "Set L is a single GPT-4 sample at temperature 0 with a fixed seed (the prompt and raw output are recorded in supplementary S3 `prompt_log.md`)". However, the actual file `supplementary/S3_case_study/mr_sets/prompt_log.md` records the prompt and then states under "Raw GPT-4 output (verbatim)": `[TO BE FILLED at experiment time]`, and under "Date generated": `[TO BE FILLED at experiment time]`. The actual `set_L_llm.py` source code (line 11) explicitly labels its five functions as `PLACEHOLDER STATUS: the five entries below are *expected-shape* placeholders. Replace each _placeholder_*_fn with the actual MR translated from prompt_log.md::Raw GPT-4 output once the LLM run has been executed.` (lines 11–15). Each MR is named `_placeholder_rot_fn`, `_placeholder_perturb_fn`, `_placeholder_prob_valid_fn`, `_placeholder_scale_fn`, `_placeholder_determ_fn` (lines 37–123). The dataset_versions.txt file (lines 44–47) further confirms: "at submission time, Set L is implemented as the five expected-shape placeholders documented in mr_sets/set_L_llm.py; the full GPT-4 output is to be filed in prompt_log.md before camera-ready". The Table 4 row "Set L (LLM) 2/20" is therefore generated against an author-imagined LLM output, not against an actual LLM output.

**Why it matters**: This is the single most load-bearing case-study comparison in §6. The H2 verdict ("Set N uniquely detects all five category-(iv) mutations; Sets L and B detect zero cat-(iv) mutations") presupposes that Set L is an independent representative of what an LLM-prompted tester would obtain. If Set L is in fact an author-constructed strawman whose detection profile is necessarily a strict subset of what the authors anticipated, then (a) the construct-validity caveat the paper *does* state (5/5 was construct-engineered) understates the problem — the L row is also construct-engineered, in the opposite direction; (b) the McNemar / Fisher significance claims for N vs L (p = 0.063 / p = 0.13, lines 714) are computed against author-imagined data; (c) the §6.6.1 DeepCrime pilot also runs Set L = the same placeholders. This is a publication-blocker in its current form: the paper text and the supplementary code disagree on what the Set L baseline actually is.

**Suggestion**: Three options, in increasing order of effort. (i) Run the actual GPT-4 prompt, paste the raw output into `prompt_log.md`, regenerate Set L from the JSON, re-run runner.py, and update Table 4 numbers accordingly; if Set L's detection rate changes the H2 verdict the paper must accept that. (ii) If (i) is not feasible by camera-ready, demote Set L in §6 case study from "LLM-prompt baseline" to "author-constructed plausible-tester baseline" and remove the GPT-4 framing entirely. (iii) Drop Set L from §6 and rely on the §6.6 Set L_ensemble (the 2-vendor × 5-temperature 487-MR harvest), which is an actual multi-LLM run on the Java substrate — that arm appears genuine and is the stronger baseline. Whichever option, the discrepancy between paper text and supplementary code must be resolved before publication.

**Severity**: **Critical** (publication blocker; honesty-integrity issue).

### W2: The "head-to-head superiority claim is not asserted" framing is a partial retreat; prose still oscillates
**Problem**: The Abstract (line 78) states "on the scope-matched D1 stratum, Set~N is dominated by the GP-evolved baseline (a head-to-head superiority claim is not asserted)". Section §subsec:pooled-headtohead's headline (lines 1538–1546) frames the reading as "competitive parity at the published budget" and says "it does not support a head-to-head superiority claim". Yet within the same subsection: (i) the per-block H3a.1 verdict is "mixed" with Set N's T* edge at 10/17 vs 8/17 described as "directional edge consistent with the algebra-induced prediction" (lines 1933–1934); (ii) §subsec:empirical-summary (lines 2306–2340) lists the head-to-head as one of four "corroborating" pieces of evidence, with per-block readings emphasised over the aggregate; (iii) Table 11 (two-stratum head-to-head, lines 1905–1923) reports the *pooled* McNemar p = 0.0043 *and* the D1-only McNemar p = 0.019 — both formally indicate Set G dominance, with the pooled value strengthened by Set G's incidental D2 kills (lines 1796–1801 acknowledge this). The reader is left with the conclusion that the pooled comparison favours Set G, the D1-only comparison also favours Set G (though less strongly), and the framework's contribution must be read at the per-block / cost-axis / D2-prediction level — but the abstract's "competitive parity" framing and §6.6.6's "approximate per-block detection parity on T*" prose come close to selective emphasis on the one block where Set N edges (T* 10/17 vs 8/17), an edge that is itself underpowered (overlapping Wilson intervals, n = 17, the paper acknowledges this at lines 1700–1705).

**Why it matters**: The abstract's "Set N is dominated" disclosure is honest. The §subsec:pooled-headtohead "competitive parity" header is not consistent with that disclosure. A reader skimming for the bottom line will receive different messages from the abstract, from the section headings, and from the H3a verdict paragraph. Methodologically, the correct reading is: on the algebra-disrupting (D1) stratum where Set N is by design competitive, Set G outperforms Set N at McNemar p = 0.019; on the algebra-preserving (D2) stratum Set N is silent by construction (a feature, not a bug, but at n = 5 the Wilson upper bound 0.434 does not confirm the ≤ 10% prediction). Calling this "competitive parity" overstates the head-to-head reading.

**Suggestion**: Rename §subsec:pooled-headtohead from "Head-to-head at GenMorph's published budget: per-block precision, complementarity, and framework D2 prediction" to something like "Head-to-head at GenMorph's published budget: per-block decomposition of an aggregate Set G dominance". State at the top of the subsection (one sentence): "On the algebra-disrupting D1 stratum (Set N's design target), Set G's aggregate kill rate exceeds Set N's at McNemar p = 0.019; the per-block decomposition below shows that the gap is concentrated on G + L* with Set N edging on T*; on the algebra-preserving D2 stratum Set N's silence is by design (≤ 10% prediction, n = 5 underpowered for confirmation)." That is the honest summary; the per-block exposition that follows is unchanged.

**Severity**: **Major** (selective emphasis / inconsistency between abstract and section, fixable in prose).

### W3: §6.6.1 DeepCrime pilot — n = 5, Fisher p = 1.00, but the section header and prose lean confirmatory
**Problem**: §subsec:deepcrime-pilot (lines 733–757) reports Set N 2/5, Set L 0/5, Set B 0/5 with Wilson CIs [0.12, 0.77], [0.00, 0.43], [0.00, 0.43] and Fisher exact p = 1.00 for both N-vs-L and N-vs-B contrasts. The paper *does* state "$n=5$, underpowered for $\alpha=0.05$ inferential conclusions" (line 136 in Abstract; line 755 in §6.6.1: "the Fisher-exact p-values for Set N vs Set L and Set N vs Set B are both p = 1.00: the test has insufficient power to declare significance even with a 2/5-vs-0/5 contrast. *We do not over-interpret this result.*"). This is correct per CLAUDE.md C6 rule. However: (a) the same paragraph (line 755) lists three things "the pilot establishes": (i) comparative-evaluation infrastructure runs end-to-end, (ii) the framework's L*-block prediction is non-vacuous on a fault distribution it was not designed against, (iii) the framework boundary on cat-v-02/04/05 confirms the empirical-parameter-distribution out-of-scope class — *all three are inferential conclusions* about the framework. (b) Line 755 says "*directional* finding" but the directional finding (2/5 vs 0/5) at n = 5 with p = 1.00 is exactly the kind of "trends suggest" / "directional evidence" the CLAUDE.md C6 rule prohibits in unqualified form. (c) The paragraph then mixes the underpowered finding with a substantive mechanism claim ("ρ_train tests training-size limit invariance: ... softens the softmax and changes the argmax on inputs near classification boundaries", lines 754–755) that does not depend on n at all but is presented inside the pilot's verdict envelope.

**Why it matters**: The honest reading at n = 5, p = 1.00 is: "the pilot infrastructure works; no inferential conclusion is supported". Anything beyond that ("non-vacuous on a fault distribution it was not designed against", "framework boundary on cat-v-02/04/05 confirms an out-of-scope class") is over-claim at this n. The mechanism explanation is interesting but should be moved out of the pilot's results paragraph into a separate "interpretation of the 2/5 detection event" paragraph clearly bounded by sample-size caveat.

**Suggestion**: Tighten §subsec:deepcrime-pilot's reading paragraph to one sentence: "At n = 5, p = 1.00, the pilot is underpowered for an inferential conclusion at α = 0.05; the 2/5 vs 0/5 difference is reported as descriptive context consistent with the direction of the framework's L*-block prediction, not as a hypothesis confirmation." Move the mechanism explanation to a separate paragraph clearly labelled "Interpretation of the two detection events" so it is not entangled with the inferential verdict. Drop the three "what the pilot establishes" claims (i)–(iii) or qualify each as "candidate evidence requiring a larger n".

**Severity**: **Major** (C6 rule compliance, fixable in prose).

### W4: The augmented stratum (5 hand-crafted mutants per uncovered block = 25 total) is design-implied; disclosure is adequate but the 25/25 number is repeated outside Appendix F where the caveat is buried
**Problem**: Appendix F (§app:augmented-stratum, lines 3001–3132) is admirably clear: each of the 25 hand-crafted mutants was constructed to violate the targeted invariant of a specific known Set N MR, the 25/25 Set N detection is design-implied, and the construct-trace check is run only for pipeline-correctness verification, not as independent fault-detection evidence. The text at lines 3117–3131 ("Why this is not a head-to-head test of H3a.1") explicitly states "the construct-trace check is reported here for transparency and to verify the pipeline's end-to-end correctness on the previously uncovered blocks; the H3a.1 verdict reported in §subsec:pooled-headtohead rests on the pre-registered PIT-covered three-block substrate only". This is exemplary disclosure. However, the 25/25 number leaks into the main-text discussion: (a) Table 14 (tab:future-work, line 2282) item (g) reports "25/25 Set~N detection is design-implied by mutant authoring … and is therefore not used as independent fault-detection evidence for H3a.1" — that caveat is in the cell text but a hasty reader will see "25/25" and infer effectiveness; (b) the main §subsec:pooled-headtohead text at lines 1708–1724 ("Coverage of the remaining five operative blocks") gives a forward pointer to Appendix F and reiterates the construct-trace circularity caveat, but the same paragraph then discusses 25 hand-crafted mutants without quantifying that 5 of the 5 blocks are "all Set N kills" by construction. Set G's 12/25 = 0.480 incidental reach in Appendix F is reported as informative, and indeed it is — but if a reader stops at Table 13 (tab:augmented-stratum, lines 3075–3100) and sees Set N's "1.000" rates and Set G's "0.480", the comparative reading "Set N strongly outperforms Set G" is the natural inference and is precisely the construct-trace circularity the appendix warns against.

**Why it matters**: This is design-implied evidence presented in a 2 × 5-block comparative table. Even with the disclosure paragraph, the visual pull of Table 13 is toward the comparison itself, which is exactly what the construct-trace check is supposed to prohibit. The H3a.1 verdict in §subsec:pooled-headtohead does correctly exclude Appendix F's numbers from the H3a.1 evidence base.

**Suggestion**: Either (a) collapse Table 13 to a single aggregate row + footnote rather than a per-block 2-set comparison table (the 2 × 5-block format invites the comparison Appendix F warns against), or (b) keep Table 13 as-is but add a header column "Construct-trace check (design-implied)" with a clear visual marker (italics, "(construct-trace)") on the Set N rate column. Option (a) is preferred; option (b) is the lower-effort fix.

**Severity**: **Minor** (disclosure is present; the cosmetic / visual reading is the residual risk).

### W5: External validity — single Java codebase (MathSignalClass + ComplexSignal), single architecture (compact EGNN, not a full SE(3)-Transformer), single GenMorph snapshot
**Problem**: The Java head-to-head substrate is concentrated on a single codebase per §subsec:test-design line 2361: "the 10 SUTs of §subsec:test-design are concentrated on a single codebase (MathSignalClass + ComplexSignal) selected by the pre-registered scope criterion". The cross-codebase commons-math pilot at follow-up (b.cm) reports 3 SUTs, 5 MRs, 77 mutants — too small for inferential generalisation, and the paper acknowledges this (lines 2361, 1234–1237: "the cross-codebase commons-math pilot corroborates the direction at 2/29 = 6.9% … and inferential confirmation of the ≤ 10% ceiling requires a pooled sample of n ≥ 30"). The equivariant-ML case study uses a compact EGNN (5,189 parameters, 2 layers, hidden dim 16) as a "deliberately compact minimal stand-in for a full SE(3)-Transformer", per line 659. The transfer claim is at the operator-algebra level, but the empirical numbers (7/20, 2/20, 0/20) are architecture-specific. GenMorph is run at a single random seed (seed = 11 per §subsec:test-design line 1311) at the published 30-min budget, with follow-up (a.budget-replication) committing 5-seed replication as future work.

**Why it matters**: For a paper whose contribution claim is partly transferability ("the framework's mechanism applies unchanged once a new program family's algebra has been specified", line 2516), the empirical substrate is narrow. The cross-codebase Apache Commons Math pilot is the right move; at n = 77 it is the lower-bound test, and the L*-blindness direction does corroborate, but the paper would be substantially strengthened by either (a) running the full follow-up (b) on the 38 in-scope D4J subjects before camera-ready, or (b) recasting the cross-codebase generalisation claim explicitly as "tested on a single algebra-rich codebase with cross-codebase corroboration at small n; broader generalisation is open" — which the paper *does* say at line 2361 ("the SUTs satisfy the framework's scope precondition (each admits at least one non-empty NOETHER block beyond G), so the substrate confirms applicability within scope rather than tests the framework outside its design intent"), but the framing in the Conclusion (lines 2516–2520) is still general.

**Suggestion**: Tighten the Conclusion's transferability claim to mirror line 2361's careful phrasing: "transferability tested within the framework's scope precondition on a single algebra-rich codebase, with cross-codebase corroboration at small n committed as follow-up (b)". The GenMorph single-seed limitation (item (a.budget-replication) in Table 14) is acknowledged but should be lifted into the §subsec:empirical-threats prose as a named threat to conclusion validity rather than left in the future-work table.

**Severity**: **Major** (scope of generalisation claim; partially fixable in prose, partially requires follow-up (b)).

---

## Detailed Comments

### Title & Abstract
The title is precise and informative. The abstract structure is unconventional but defensible for a methods paper. Two abstract-level concerns:

- The empirical numbers in the abstract (line 78: "five of six SUTs admitting an L_scale MR on the comparative substrate", "scope-matched D1 stratum, Set N is dominated by the GP-evolved baseline", "out-of-scope D2-stratum boundary") are mostly correctly hedged. The phrase "head-to-head superiority claim is not asserted" is welcome and consistent with the McNemar p = 0.019 D1 reading.
- Per the project-level CLAUDE.md (lines 31–36, the "Abstract" section), specific Wilson CIs, p-values, percentages, and Wilson-interval numbers should be downstream of the Abstract. The current Abstract contains "five of six SUTs" (a percentage in disguise) and the structural-coverage numbers (1.00 vs 0.40 vs 0.20). These are arguably structural rather than empirical, but I would recommend the authors audit per CLAUDE.md.

### Methodology / Research Design
The three empirical components (PWR re-classification §5, equivariant-ML §6, head-to-head §6.6) are individually well-designed but are not cohesive as a single empirical chapter. They address different RQs:
- §5 tests systematisation-by-re-classification on an existing corpus (no new MR identification).
- §6 case study tests generative transferability + cat-(iv) construct validity on a synthetic mutation set, n = 20.
- §6.6.1 DeepCrime pilot tests on n = 5 real-fault-style mutations.
- §6.6 head-to-head tests against GenMorph on n = 57 PIT mutants.

The paper would benefit from a methodology-overview table at the top of §6 (or as Table 0) listing the four empirical sub-studies × {n, mutation source, comparator, hypothesis tested, falsification criterion, verdict}, so the reader can see at a glance how the four contribute differently to the framework's empirical defence. Currently the reader assembles this mental model section-by-section.

**Sampling strategy** is the framework's design (pre-registered SUT criterion in `configs/d4j_algebra_rich_criterion.json`, line 1283), which is internally sound. The selection is committed before evaluation data exists, the criterion contains no kill-rate references and cannot be tuned by outcomes, and the git timestamp chain is the auditable proof. This is exemplary pre-registration for a software-testing study.

**Data collection** for the head-to-head is through PIT 1.7.4 with the default mutator configuration, JUnit codegen, 2-pass surefire green-suite filter, and per-mutant kill vector parsing. This is reproducible at the protocol level; the supplementary S7 (`d4j/`) contains the per-MR kill counts, the prediction's git timestamp, and the test-gate harness (`tests/run.sh`), per lines 2342–2347. I did not run the harness end-to-end (out of review scope), but the file inventory is consistent with reproducibility expectations.

**Analysis methods** are correct (Wilson CIs, exact McNemar, Fisher exact, Holm–Bonferroni correction for 16 per-SUT comparisons, equivalent-mutant exclusion via 2-of-3 LLM vote with third-voter tiebreaker, 1.000 Fleiss' κ on the 33 parseable items). Two concerns:
- The 2-of-3 LLM equivalent-mutant exclusion (lines 1846–1881) is the right idea but the human-pair κ replication is committed only for "industrial-port follow-up". For the n = 18 both-miss mutants subjected to the LLM vote, a single-author manual re-classification audit on a subsample would substantially strengthen the analysis at low cost.
- The construct-trace consistency check (Appendix F) is correctly excluded from H3a.1's evidence base. See W4.

### Results / Findings
Tables 4 (case study), 7 (L*-blindness), 8 (algebra-rich pooled head-to-head), 9 (per-block head-to-head), 11 (two-stratum), and 13 (augmented stratum) are dense but readable. Table quality notes:

- Table 4 (line 691): "Construct-validity-controlled" label is appropriate; the cat-(iv) row 5/5 vs 0/5 vs 0/5 is correctly framed in the caption. The detection-rate row of 7/20 vs 2/20 vs 0/20 should be read in conjunction with W1 above (Set L is placeholders).
- Table 7 (L*-blindness, line 1331): the per-SUT verdict column is informative; "hypotSig 2/4 Outlier; explained below" is honest and the explanation (return_zero_doubles_VR and Math.sqrt_replaced_with_one_RC both violate degree-1 homogeneity directly, lines 1380–1389) is methodologically clean.
- Table 8 (algebra-rich pooled, line 1547): caption correctly says "n = 62 is underpowered for a paired hypothesis test at α = 0.05 in two-sided form". The per-SUT Δ column is "directional only" with Holm–Bonferroni properly applied (no per-SUT contrast meets α/16 ≈ 0.003).
- Table 9 (per-block, line 1631): the {both / N-only / G-only / neither} complementarity partition is a nice addition. The "unmapped (lower-bound caveat)" row at n = 25 is correctly bracketed as not a fourth block.
- Table 11 (two-stratum, line 1913): the row formatting is correct; D1 McNemar p = 0.019, D2 p = 0.25, pooled p = 0.0043 are all consistent with my recomputation.
- Table 13 (augmented stratum, line 3087): see W4.

### Discussion / Limitations
§7 (lines 2350–2520) is well-structured. The Wohlin four-validity organisation is followed. The construct-validity discussion of the §6 case study (line 2359) is concrete and honest *with the caveat* that the underlying Set L data is placeholder (see W1). The external-validity discussion at line 2361 is the most thorough threats section I've reviewed at TOSEM in recent memory and includes the cross-codebase commons-math pilot's actual numbers. The conclusion-validity discussion (line 2363) correctly notes that 20 mutations on one EGNN is insufficient to characterise the framework's performance distribution across architectures.

The §subsec:engineering-guidance practical recommendations (lines 2481–2491) — K-sweep audit at three truncation levels, ±5% mesh-convergence threshold citing Lewis & Miller §6.2, tolerance selection τ ≈ 10² ε_fp citing Higham 2002 §γ_n bound — read as carefully sourced and are above the median empirical-paper concern for actionable practitioner advice.

### Conclusion
The conclusion's "Established / Open" boundary box (lines 2522–2526) is the kind of disclosure I want to see more of in software-testing papers. Items (a)–(e) under "Open" are appropriately scoped. The transferability claim in the body (lines 2516, "the framework's mechanism applies unchanged once a new program family's algebra has been specified") is broader than the §subsec:empirical-threats commitments; see W5.

---

## Questions for Authors

1. **The §6 Set L baseline (W1).** The supplementary code `set_L_llm.py` explicitly states the five MRs are placeholders, and `prompt_log.md` records the Raw GPT-4 output as `[TO BE FILLED at experiment time]`. The paper text at line 665 and line 760 describes Set L as actual GPT-4 output. (a) Has the GPT-4 prompt been run? (b) If yes, where are the raw output and the actual translated MRs? (c) If no, why does the paper text describe placeholder code as a GPT-4 output, and how does this affect the H2 verdict (which depends on Set L's detection profile being independent of the authors' anticipation)? A point-by-point response is requested.

2. **D1-only McNemar p = 0.019 and the "competitive parity" framing (W2).** The D1-only McNemar p = 0.019 with discordant pairs (b, c) = (15, 4) and the aggregate D1 rates 26/52 vs 37/52 indicate Set G dominance on the algebra-disrupting stratum that Set N is designed for. The Abstract phrases this as "Set N is dominated by the GP-evolved baseline (a head-to-head superiority claim is not asserted)" — which is honest. §subsec:pooled-headtohead and §subsec:empirical-summary lean toward "competitive parity" and the per-block T* edge (10/17 vs 8/17, n = 17, underpowered). Can the authors commit to a single consistent framing across abstract, section headings, and summary paragraphs? Specifically: on the D1 stratum, is the bottom line "Set G dominates, with per-block complementarity and Set N's T* edge underpowered" or "competitive parity, with Set G stronger on G + L* and Set N stronger on T*"?

3. **Cross-codebase generalisation (W5) and follow-up (b) timeline.** The 10-SUT head-to-head is on a single codebase; the commons-math pilot is at n = 77 across 3 SUTs. Follow-up (b) (extending to all 38 in-scope D4J subjects) is committed at ≈ 10 h human + ≈ 30 min compute and would yield n > 200. Given the modest cost, can the authors commit to delivering follow-up (b) before camera-ready, or commit to a tighter framing of generalisation in the Conclusion if the larger study cannot be done in revision time?

4. **§6.6.1 DeepCrime pilot reading at n = 5, p = 1.00 (W3).** The pilot's three "what it establishes" claims (lines 755) — (i) infrastructure runs end-to-end, (ii) L*-block prediction non-vacuous, (iii) framework boundary on cat-v-02/04/05 confirms a ninth-block candidate — each carry inferential weight beyond what n = 5 supports. Will the authors tighten the reading to "the pilot infrastructure is end-to-end functional; no inferential conclusion supported at this n; the 2/5 detection events are reported with mechanism in a separately labelled paragraph"?

---

## Minor Issues

### Language / Grammar
- Lines 1538, 2306–2340: "competitive parity" phrase is contested by the McNemar numbers; see W2.
- Line 78: "ten pairwise-independent extensions across the three algebras" is a numerical claim that depends on the companion artefacts (`theory/equi_thm1prime_search.md`, `theory/rel_thm1prime_search.md`, `theory/translate_extensions.md`); verify the count is consistent with those files (out of R1 scope to audit).
- Line 1538: "We nonetheless report a pooled comparison against GenMorph's GP-evolved Set~G" — the phrasing "we nonetheless report" sounds defensive. Suggest: "We additionally report a pooled comparison …".
- Line 2516: "the framework's mechanism applies unchanged once a new program family's algebra has been specified" — too strong given §subsec:empirical-threats. Suggest mirroring line 2361's careful phrasing.

### Citation Format
- I did not audit citations end-to-end; this is R2 scope. The two citations I checked (Wohlin 2012EmpiricalSE at line 2355; Higham 2002Accuracy at line 2490) are appropriately invoked.

### Figures and Tables
- Table 4 caption (line 693): the "Detection numbers for ρ_adj in Set~N use the CI-time forward-pass-only formulation" disclosure is appropriately bold-faced; consider doing the same for "Set L is currently implemented as expected-shape placeholders pending GPT-4 run; numbers may revise on actual run" if W1 is resolved by option (ii) (demotion).
- Table 13 (line 3087): see W4 for visual-marker suggestion.
- Table 14 (Future Work, line 2269): item (g) cell text says "25/25 Set~N detection is design-implied by mutant authoring … and is therefore not used as independent fault-detection evidence for H3a.1." — italicise the construct-trace caveat for visual prominence.

### Layout
- The paper is 76 pages with 14 tables in the empirical sections. A "Roadmap of empirical sections" table at the start of §6 (n / mutation source / comparator / hypothesis / verdict per sub-study) would help the reader.
- §subsec:pooled-headtohead is dense (lines 1527–2042); breaking it into separate subsections for (a) the aggregate D1 / D2 result, (b) the per-block complementarity, (c) the Set L_ensemble comparison, and (d) the equivalent-mutant exclusion methodology would improve readability without changing content.

### Statistical reporting against the APA 7 / EQUATOR checklist
- Wilson CIs: complete and correctly computed ✓
- McNemar exact p-values: complete and correctly computed ✓
- Effect sizes for paired binary outcomes: kill-count differences and (b, c) discordant counts are reported throughout — the natural effect size for paired binary McNemar is the odds ratio (b/c) or the risk difference (b – c)/n; the paper reports counts but not the OR. Consider adding OR or RD with CI for the D1 and pooled McNemar.
- Multiple comparisons: Holm–Bonferroni correctly applied to the 16 per-SUT × 2-budget comparisons (α/16 ≈ 0.003, line 1543). The 10 pairwise tests across 5 sets noted in the protocol (line 770) are also Bonferroni-committed but the head-to-head ultimately runs only 1 paired comparison (Set N vs Set G) at α = 0.05, which is correct.
- A priori power analysis: not reported (typical for software-testing exploratory studies; the §subsec:empirical-threats item (c) does acknowledge underpoweredness for several strata). Recommend adding a minimum-detectable-effect-size note for the D1 McNemar at n = 52 (the post-hoc sensitivity analysis is informative even if a priori power was not computed).

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 80 | Strong | Methodological originality on the algebraic-derivation side is genuine and the L*-blindness falsifiable prediction is a real methodological contribution; the upstream eight-block decomposition is honestly framed as a hypothesis. R2 / R3 assess theoretical originality more carefully. |
| Methodological Rigor (25%) | 68 | Adequate | Strong on statistical computation correctness (S2), pre-registration (S1, S4), threats-to-validity organisation (S3), and LRCA construct-validity check (S5). Weakened by W1 (Set L placeholder discrepancy is publication-blocker), W2 ("competitive parity" inconsistency), W3 (DeepCrime pilot over-reading at n = 5), and W4 (augmented-stratum table visual pull). Most issues are fixable in prose; W1 is the load-bearing item. |
| Evidence Sufficiency (25%) | 62 | Adequate | The L*-blindness test on n = 44 across 6 SUTs is the strongest single piece of empirical evidence and passes its pre-registered falsification criterion on 5/6 SUTs with one SUT explainable by the prediction's quantitative tail. The head-to-head at n = 57 is appropriately framed as scope-mismatched and per-block. The DeepCrime pilot at n = 5 is correctly underpowered. The §6 case study at n = 20 has the W1 Set L integrity issue. The cross-codebase commons-math pilot at n = 77 corroborates. Cumulatively the evidence base is sufficient for a methods-paper claim but does not characterise the framework's performance distribution; the paper is honest about this. |
| Argument Coherence (15%) | 72 | Adequate-to-Strong | The two-layer (upstream-empirical / downstream-mechanical) framing is coherent and the C1–C4 contribution structure (line 132) is followed. The Conclusion's Established / Open boundary box is exemplary. Coherence is degraded by W2 (abstract vs subsection vs summary inconsistency on the head-to-head reading) and the lack of an empirical-roadmap table (Detailed Comments §Methodology). |
| Writing Quality (15%) | 78 | Strong | The prose is precise and the §subsec:empirical-threats / §7 threats-to-validity sections are above the median TOSEM submission for honesty and concreteness. The construct-validity disclosures are repeated where they need to be repeated. The 76-page length is justified by the framework's scope; the empirical sections are dense but readable. CLAUDE.md hygiene (em-dash, AI-vocabulary, hedging stacking) was not the focus of this review. |
| **Weighted Average** | **70.4** | **Minor-to-Major Revision (boundary)** | (80×0.20)+(68×0.25)+(62×0.25)+(72×0.15)+(78×0.15) = 16+17+15.5+10.8+11.7 = 71.0. Decision-mapping: 65–79 = Minor Revision; the weighted score lands in Minor Revision territory but the W1 issue is a publication-blocker that mechanically forces Major Revision. |

**Decision: Major Revision.** The weighted dimension-score average (71.0) would map to Minor Revision under the standard rubric, but W1 (the Set L placeholder discrepancy in §6 case study) is an integrity issue that must be resolved before publication and constitutes a "Required Revision" per the template severity scale. The other issues (W2–W5) are all fixable in prose or with a single delivered follow-up (b). I recommend a Round 3 with explicit response to W1's three options and a final pass at framing consistency for W2.

---

## 200-word summary for the parent agent

**Recommendation**: Major Revision. Weighted score 71.0 (Minor-Revision range), but the W1 publication-blocker forces Major Revision.

**Scores**: Originality 80 / Methodological Rigor 68 / Evidence Sufficiency 62 / Argument Coherence 72 / Writing Quality 78. Weighted average 71.0.

**Top 3 methodological concerns**:

1. **W1 (Critical): Set L in §6 case study is author-written placeholders, not GPT-4 output.** Paper text at lines 665 and 760 describes Set L as GPT-4-generated; supplementary `set_L_llm.py` lines 11–15 explicitly label its five MRs as "expected-shape placeholders" and `prompt_log.md` records the raw output as `[TO BE FILLED]`. This affects Table 4's H2 verdict on cat-(iv) detection and the §6.6.1 DeepCrime pilot. Must be resolved: either run the actual GPT-4 prompt, demote Set L's framing, or drop the §6 Set L row in favour of the §6.6 Set L_ensemble (which is genuine).

2. **W2 (Major): "Competitive parity" framing inconsistent with D1 McNemar p = 0.019.** Abstract honestly states Set N is dominated on D1; §subsec:pooled-headtohead heading and §subsec:empirical-summary lean toward "competitive parity" / per-block T* edge framing. The two-strands reading is internally inconsistent and selective.

3. **W3 (Major): §6.6.1 DeepCrime pilot at n = 5, Fisher p = 1.00 carries three inferential claims that the sample does not support** (infrastructure, L*-non-vacuous, ninth-block candidate). Per CLAUDE.md C6 rule, tighten to "infrastructure functional; no inferential conclusion at α = 0.05; 2/5 events reported with mechanism separately".

Wilson CIs and McNemar p-values are all correctly computed (spot-checked exhaustively); pre-registration is exemplary; threats-to-validity organisation is above median TOSEM. The methodology core is sound; the issues are integrity-and-framing, fixable in revision.
