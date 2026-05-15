# Devil's Advocate Review — NOETHER (TOSEM round 3)

**Reviewer**: Devil's Advocate (independent attack, re-applied at commit `ceac6ed`)
**Paper**: `<PROJECT_ROOT>/NOETHER_paper.tex` (3348 lines, 80 pp.)
**Mandate**: re-attack the paper without softening; Attack Intensity Preservation Protocol §"Anti-Sycophancy Rules" applies. Persistent disclosure ≠ resolution.

---

## Devil's Advocate Review

### Strengths acknowledgement (1–2 sentences, mandatory for fairness)

The Round 3 revision is unusually transparent in the dimensions that matter: §6.6 (lines 1604–1607) now opens its head-to-head paragraph by declaring "Set N is dominated by Set G in the aggregate (McNemar p=0.0043 pooled, p=0.019 on D1)" before any rescue framing, and Appendix F (lines 3239, 3267–3268, 3289) carries an explicit "this table is excluded from the H3a.1 evidence base" disclaimer in bold beside the 25/25 construct-trace number. These transparency moves are not the field's norm and deserve credit. They do not, however, change the underlying substantive structure of the contribution — which is what this report attacks.

### Strongest Counter-Argument

The paper at `ceac6ed` continues to assert in its Highlights and Abstract (lines 76, 78) a "two-layer framework" whose downstream layer is "mechanical and provable: ... algebraic-closure guarantee under the framework's `Translate` operator over the algebra-induced MR space $\mathrm{MR}(\mathcal{A}_P)$ (Theorem 1)". After Round 3 the formal admission at line 432 ("the closure result is by-construction within the explicit scope of Definition 13") has been extended, but the surface contract sold to a TOSEM scanning reader remains: *Theorem 1 is the downstream theoretical contribution that distinguishes NOETHER from prior empirical MetaPattern catalogues*. The structural counter-argument is that **the only non-tautological version of the closure claim is the one this very paper falsifies on its principal domain** (Theorem 1′, §subsec:negative-pwr lines 1060–1061: false on $\mathcal{A}_{\mathrm{PWR}}$). The paper repairs this gap by introducing "ten Translate-extension dimensions" (lines 78, 152, 904) as a positive-sounding contribution. But the count is unverifiable: 5 are "proved by per-block exhaustion" on Table 6's 8 templates (which is itself a finite per-template scan, not a closure proof in the model-theoretic sense), and 5 are "asserted by inspection" (lines 152, 904). The "by inspection" half **is the same evidential mode** as Round 2 C2 charged, dressed in a new two-tier disclosure. Removing the tautology and the by-inspection half from the contribution ledger leaves: (i) an eight-block taxonomy that the authors themselves classify as empirical curation (line 317, "by-inspection enumeration of mathematical structures that recur"); (ii) Theorem 2's poly-time decidability under finite generating set; (iii) one operative falsifiable prediction (the $\mathcal{L}^*$-blindness test), whose post-data outlier-handling rule was codified on **2026-05-15 in response to Round 2 review** (line 1178–1179, paper's own admission) and is therefore not actually pre-registered against the empirical outcome it adjudicates; and (iv) a head-to-head where Set N is dominated by Set G on the in-scope D1 stratum. The Round 3 honest framing — "we propose an eight-block empirical taxonomy and observe one falsifiable prediction passes 5/6 SUTs under a post-hoc-codified outlier rule" — is materially weaker than what the abstract sells.

### Issue List

#### CRITICAL

| # | Dimension | Issue Description | Location |
|---|-----------|-------------------|----------|
| C1 | Logic-Chain / "So What?" | **Theorem 1 remains a closure-under-construction tautology.** The Round 3 rescue text at lines 432–433 ("We acknowledge that the closure result is by-construction within the explicit scope of Definition 13") is exactly what C1 charged: a disclaimer in §3.3, while the Abstract (line 76) and §1 C2a (line 134) still front-load "Algebraic Closure Theorem (Theorem 1): the constructed MetaPattern set is closed under `Translate`". The proof at §C.6.1 (referenced at line 2862 for the canonical-block ordering's uniqueness) is unchanged from R2 — definitional bookkeeping. Theorem 1′ (line 2919, conjecture* environment) remains the only non-tautological closure statement, and §subsec:negative-pwr falsifies it. Persistent disclosure ≠ relocation of substance. | Abstract line 76; §1 C2a line 134; §3.3 line 432 rescue; conjecture* line 2919 |
| C2 | Cherry-Picking / Confirmation Bias | **The "10 Translate-extension dimensions" count is preserved with a new two-tier veneer; the "by inspection" half is still C2-level engineered.** Round 3 explicitly splits 5 PWR (proven) + 5 equi/rel (by inspection) at lines 78, 135, 152, 904. But (a) the "proven" 5 are 5 obstructions extracted from 2 MRs (Table 6 lines 1043–1051; 2.5 obstructions/MR is a fine-grained split that can be re-aggregated); (b) two of the five "candidate" equi/rel dimensions are admitted to "specialise PWR-side dimensions to type-distinct algebraic primitives" (line 135 verbatim), i.e. they are not independent of the PWR five — yet they are nonetheless counted toward "ten" rather than absorbed; (c) the "per-block exhaustion" referenced at line 977, 2945 is itself a per-template scan against Table 4's `Translate` templates, not a closure proof against a general algebraic-MR space. The Round 3 disclosure ("formal per-dimension exhaustion proofs ... committed as follow-up") is a future-work IOU dressed as a present contribution. The count is engineered to round to 10. | Abstract line 78; §1 lines 135, 152; §subsec:third-domain line 904; Table 6 lines 1043–1051 |
| C3 | Cherry-Picking / Frame-Lock | **The $\mathcal{L}^*$-blindness "outlier-handling rule" admission at lines 1178–1186 strengthens, not weakens, C3.** The paper at line 1178–1179 now writes verbatim: "The rule was codified in the pre-registration config on 2026-05-15 in response to a Round 2 review observation." This is the *paper's own admission* that the rule which rescues `hypotSig` (2/4 kills, line 1427) **was written down after the kill data was observed**. The reading the authors intend ("future cross-codebase substrates inherit the rule as a written test", line 1186) is consistent with C3 (the rule survives now; the question is whether the original 5/6 verdict on the substrate that *produced* the rule is unbiased). Under standard pre-registration norms, a falsification rule codified post-data on the substrate it adjudicates is a Type-I-error inflator on that substrate, regardless of its prospective use on later substrates. The "9 grid cells under threshold sensitivity, `hypotSig` crosses every threshold" robustness check (line 1167) shows only that the *threshold* is stable; the *outlier rule itself* is the engineered piece. | §subsec:l-blindness-derivation lines 1167, 1178–1186; outlier rule footprint Table 7 line 1427 |
| C4 | Logic-Chain / Statistics-Garden | **Round 3 added OR=3.75 + RD=+0.212 to the McNemar-p=0.019 D1-only paragraph (lines 1832–1836), turning the head-to-head into a three-effect-size report. This is a *garden of statistics* expansion, not a rebuttal of C4.** The three numbers (McNemar p, paired risk difference, odds ratio) are not independent — they are three views of the same (b, c) = (15, 4) discordant cell. Reporting all three lets a reader choose the most palatable framing: OR=3.75 sounds modest in 2x2 odds-ratio register; RD=+0.212 sounds like "only a 21pp gap"; McNemar p=0.019 is the inferential verdict. The composite reads as "the gap is moderate", which softens the same data Round 2 read as "Set G dominates". The R4-flagged Mode-3 errors (powerSig count 4→3 and caption 9/8/9→6/5/3) being fixed during integrity audit is necessary but not sufficient: the substantive question — whether the head-to-head Set G dominance is the load-bearing in-scope outcome — is unchanged by adding effect sizes. The "framework's contribution is read as algebraic derivability, per-block complementarity, and an out-of-scope D2-stratum boundary" (line 1608–1614) is exactly the post-hoc reframing C4 charged. | §6.6 lines 1604–1614, 1827–1844; OR/RD addition line 1832–1836 |
| C5 | Confirmation Bias / Construct Validity | **The Round 3 boldface "This table is excluded from the H3a.1 evidence base" (Appendix F line 3267–3268, Table 12 caption) is a stronger disclosure but does not address the substantive C5 charge.** C5's core was *not* that App. F is treated as H3a.1 evidence — Round 2 already conceded that. C5's core was that the case study's H2 verdict (§subsec:case-study line 766, "cat-(iv) 5/5 unique detection") is itself construct-trace-circular by the *same* logic ("the mutation set was constructed to cover one defect category per non-empty block of $\mathcal{A}_{\mathrm{equi}}$, so cat-(iv)'s category was selected because $\rho_{\mathrm{train-rev}}$ alone covers it" — line 766 verbatim). The case study still calls H2 "the load-bearing comparative result of the case study" (line 764). H2's load-bearing 5/5 is by-construction in the exact sense Appendix F's 25/25 is by-construction. The Round 3 in-text disclaimer about H2 (lines 766, 768–769) is the *same* disclaimer that Appendix F received in bold; yet H2 is still the load-bearing case-study verdict, while App. F's 25/25 is demoted to pipeline-correctness. The asymmetric treatment is the C5 charge, untouched. | §subsec:case-study lines 764, 766, 768–769; App. F lines 3239, 3267–3268 |

#### MAJOR

| # | Dimension | Issue Description | Location |
|---|-----------|-------------------|----------|
| M1 | Frame-Lock / Logic-Chain | **New attack vector — Set-MP ⊊ NOETHER block coverage is asserted from a 3-SUT manual analysis, a construct-validity hazard analogous to C5.** §para:metricplus-headtohead-small (lines 2533–2616) introduces a manual METRIC+ derivation on midpoint, hypotSig, powerSig — chosen for "bivariate input arity" and "distinct algebraic structure" (line 2536–2538). The result (Table 11) is that every non-vacuous Set-MP MR maps to a NOETHER block already covered by Set-N (line 2603), and three Set-N MRs ($m_{\mathrm{adj}}$, $m_{\mathrm{train-rev}}$, $m_{\mathrm{conv}}$) have no Set-MP counterpart. But the analysis is *by the same authors who designed Set-N* against METRIC+'s 11 D×R categories — the authors get to decide which METRIC+ pairs are "vacuous" (fixed arity, scalar output), and a NOETHER-block-mapping by the framework's designers is not independent evidence of subsumption. The structural conclusion ("Set-MP ⊊ NOETHER block coverage", line 2600) is asserted across "the bivariate-input subsample of the §subsec:test-design substrate" (line 2602) but rests on 3 SUTs out of 10, hand-picked. The honest reading is "on three hand-picked bivariate SUTs, the framework's authors map METRIC+ pairs to NOETHER blocks and conclude inclusion." This is METRIC+ being judged by NOETHER's own classifier. | §para:metricplus-headtohead-small lines 2533–2616; Table 11 line 2574 |
| M2 | Statistics-Garden | **The Round 3 statistical apparatus now reports ~9 different p-values across §6.6 alone** (pooled M1 McNemar p=0.0043; D1 McNemar p=0.019; D2 p not significant due to n=5; per-SUT no contrast meets Holm-Bonferroni α/16≈0.003; per-block T* directional; G-block 0/7 vs 7/7; L*-blindness 5/6 vs 1/6; OR=3.75; RD=+0.212; case-study McNemar p=0.016, Fisher p=0.008; pilot p=1.00; cross-codebase commons-math 2/29=6.9%). Without a primary outcome declaration, the reader is presented with a buffet from which they can self-serve a verdict. The §6.6 paragraph (line 1986–1990) names the "Two-stratum head-to-head summary" as "Primary tabulation for H3a verdict" but the H3a verdict itself dissolves into per-block and complementarity readings. This is M8 from Round 2 with a new top layer rather than a resolution. | §6.6 lines 1604–1980, 1986–1990 |
| M3 | Cherry-Picking / Selection | **Set L is still a single GPT-4 sample at temperature 0 in §subsec:case-study (line 815, "Set L is a single GPT-4 sample at temperature 0 with a fixed seed")**, while the §subsec:pooled-headtohead Set L ensemble (line 1898, "$2$-vendor × $5$-temperature ... 100 samples, 487 proposed MRs") demonstrates that an LLM-prompted ensemble produces a *superset* of Set N's reach on the Java substrate. The asymmetric Set-L treatment — single-sample in the favorable case study, full ensemble in the substrate where the framework loses head-to-head — is the M2 charge from Round 2 unmoved. The Round 3 acknowledgment that "every Set L MR is by construction a byte-identical copy of a Set N pair, so Set L can match but not exceed Set N's per-MR kill power" (line 1918–1920) is itself the M2 finding: Set L is held to Set N's template, so the comparison is rigged at the translator. | §subsec:case-study line 815; §subsec:pooled-headtohead lines 1898, 1918–1920 |
| M4 | Construct Validity / Sample | **Inter-rater reliability for $\mathcal{A}_P$ distillation is still measured by LLM raters with shared training data**, never by independent human raters. The 18-MR audit (Fleiss' κ = 0.857, line 2924) and the LRCA κ in §7.1 remain LLM-among-LLMs. The Round 2 M4 charge ("no independent human inter-rater agreement study") is unchanged. The construct-validity threat for the framework's central operational step (distilling $\mathcal{A}_P$ from program semantics) is therefore empirically uncharacterised on human practitioners — i.e. the practitioners who would actually use the framework. | §subsec:reactor-mapping line 2924; §7.1 (LRCA κ) |
| M5 | Frame-Lock | **The "five SOTA-category baselines" framing is unchanged.** GenMorph is the only fully-executed automated baseline; MR-Scout is "adapted estimate" / not re-executed; the LLM arm is 2-of-3 vendors (Anthropic third-vendor still committed as follow-up `d.set-l-claude`, line 1927–1928). The comparative-evaluation framing is rhetorical. M7 from Round 2 unmoved. | §subsec:empirical-threats; §subsec:pooled-headtohead lines 1927–1928 |
| M6 | Logic-Chain | **The L*-blindness derivation's "homogeneity-preserving" claim for MATH-mutator-on-bivariate-inputs is still over-stated relative to the actual mutator semantics.** The derivation at lines 1058–1066 (Round 2 M6 location) and the outlier rule (line 1170–1174) jointly handle bivariate $\times \leftrightarrow \div$ as "degree-changing → homogeneity-breaking → rescued from the 5/6 verdict". But the prediction was framed as "near-zero kills on homogeneity-preserving mutators"; if half of MATH-mutators on bivariate SUTs break homogeneity by construction, then the prediction's *substrate* (the union of all PIT MATH-RETURN-VALS mutants) is not uniformly homogeneity-preserving, and the 2/44 = 4.5% pooled rate is *consistent with* this uneven substrate rather than a tight empirical test. The R3 wording "homogeneity-preserving subset of PIT's mutators" (i.e. the prediction is over a subset, not over PIT's full default set) would be more honest than "PIT's default mutator set has this property by direct calculation" (line 1082–1083). | §subsec:l-blindness-derivation lines 1058–1066, 1082–1083; outlier rule line 1170–1174 |
| M7 | Industrial Cost / Stakeholder | **The Table 8 cost matrix (≈10 h $\mathcal{A}_P$ distillation per family) is still measured under the favorable single-algebra substrate (Apache Commons Math).** The amortisation argument breaks for industrial codebases with many algebra families. M5 from Round 2 unmoved. | Table 8 (industrial cost matrix); §subsec:test-design line on single-family selection |
| M8 | Frame-Lock | **The "8-block" decomposition is still empirically curated by the authors and the curation step is repeatedly admitted (lines 317, 546) as an inductive move.** The Round 3 phrasing "Hypothesis 1, an open empirical hypothesis with six documented out-of-scope program-family classes" (line 490) and "induction has not been eliminated from MetaPattern discovery; it has been moved one level up" (line 317) are *honest about the upstream layer*, but the abstract/highlights still frame "two-layer framework: ... downstream layer is mechanical and provable". A reader processing the abstract first will under-weight the upstream inductive layer. M2 from R2 (alt path 2 "block compactness without algebra") is unmoved. | §1 line 134; §3 line 317; §3 line 490; §subsec:decomposition |

#### MINOR

| # | Dimension | Issue Description | Location |
|---|-----------|-------------------|----------|
| m1 | Overgeneralization | The Noether-analogy framing is acknowledged as "methodological only" but still drives the title, framework name, and rhetorical scaffolding. R2 m1 unmoved. | §1; title |
| m2 | Logic Chain | Remark 2 (line 289) gap between block sufficiency and Translate sufficiency persists. R2 m2 unmoved. | Remark 2 line ~289 |
| m3 | Stakeholder Blind Spot | TOSEM audience is SE practitioners, not operator-algebra specialists. R2 m3 unmoved. §7.5 engineering guidance is unchanged. | §7.5 |
| m4 | Underpowered pilot in Abstract | DeepCrime pilot ($n=5$, p=1.00) is still referenced in Abstract framing as supporting evidence even though Fisher exact is non-significant. R2 m4 unmoved. | Abstract line 78; §subsec:deepcrime-pilot |
| m5 | "So What?" | Boundary-of-contribution boxes still quantify the modest residue. R2 m5 unmoved. | Intro line 141; §3 line 440; Conclusion |
| m6 | Logic Chain — framing inversion | "Ten Translate-extension dimensions" framed as positive contribution. R2 m6 strengthened: the two-tier disclosure (5 proven + 5 by inspection) makes the framing inversion more explicit — counting unresolved obstructions as a contribution, with half of them admittedly unproven. | Abstract line 78; §subsec:third-domain line 904 |
| m7 | Pre-registration semantics | Line 1178–1179's "codified ... in response to a Round 2 review observation" is honest about timing but does not state the obvious caveat: a rule codified post-data on the substrate it adjudicates is not a pre-registration for that substrate. A footnote acknowledging this would be cleaner than the implicit framing that "future cross-codebase substrates inherit the rule". | §subsec:l-blindness-derivation line 1178–1186 |

### Round 2 Rebuttal Scoring (Anti-Sycophancy Protocol)

For each Round 2 CRITICAL finding, scored per §"Attack Intensity Preservation Protocol":

```
[DA-REBUTTAL: C1 (Theorem 1 tautology)
 | Rebuttal Score: 2/5
 | Action: Maintain (Restate)
 | Reason: Round 3 added disclosure at lines 432–433 ("by-construction within
   the explicit scope of Def 13") and rescue text "substantive value lies in
   what the theorem then enables". The abstract (line 76) and §1 C2a (line 134)
   still front-load "algebraic closure" as a positive contribution. Persistent
   disclosure is not rebuttal: it is the same admission re-disclosed.
   The proof remains 2 lines of definitional bookkeeping. Score 2 is
   "tangential or changes the subject" — the substantive content of C1 is
   unaddressed, only its visibility increased. Maintain CRITICAL.]

[DA-REBUTTAL: C2 ("10 dimensions" engineered)
 | Rebuttal Score: 3/5
 | Action: Maintain (partial response)
 | Reason: Round 3 explicitly split 5 proven + 5 by-inspection (lines 78, 135,
   152, 904) and admitted that two of the five candidate dimensions
   "specialise PWR-side dimensions to type-distinct algebraic primitives".
   This is the kind of partial concession that meets the 3/5 bar ("partially
   addresses but leaves core intact"). The core — that "ten" is a packaged
   headline rather than an independent count — is not dismantled; the
   admission that 2/5 specialise PWR dimensions actually corroborates C2's
   "5+5 with reused dimensions" charge. Maintain CRITICAL.
   Anti-sycophancy: no consecutive concession with C1 (which was Maintained,
   so the bar is unchanged at 4/5 for downgrade); 3/5 is not a downgrade.]

[DA-REBUTTAL: C3 (L*-blindness outlier rescue)
 | Rebuttal Score: 1/5
 | Action: Strengthen
 | Reason: The paper at lines 1178–1179 now contains a verbatim admission
   that the outlier-handling rule "was codified in the pre-registration
   config on 2026-05-15 in response to a Round 2 review observation." This
   admission STRENGTHENS C3: it confirms in the paper's own words that the
   rule which rescues hypotSig was codified after the kill data was observed
   on the substrate it adjudicates. A rule codified post-data is not a
   pre-registration for that substrate. Score 1 ("assertion without
   evidence") with action Strengthen — the rebuttal IS the additional
   evidence supporting the original attack. Maintain CRITICAL with reinforced
   wording.]

[DA-REBUTTAL: C4 (head-to-head Set G dominance reframing)
 | Rebuttal Score: 2/5
 | Action: Maintain
 | Reason: Round 3 added OR=3.75 + RD=+0.212 at lines 1832–1836 and reframed
   §6.6 to lead with "Set N is dominated by Set G in the aggregate"
   (line 1604–1607). The opening admission is honest but the rest of §6.6
   pivots to per-block complementarity and the out-of-scope D2 stratum
   exactly as C4 charged. Adding effect sizes does not address the
   garden-of-forking-analyses charge; it expands it. Score 2 ("tangential
   or changes the subject"). Maintain CRITICAL.]

[DA-REBUTTAL: C5 (construct-trace circularity)
 | Rebuttal Score: 3/5
 | Action: Maintain (partial response, with case-study asymmetry persisting)
 | Reason: Round 3 added Appendix F's bold disclaimer "This table is excluded
   from the H3a.1 evidence base" (line 3267–3268), which addresses the
   *augmented stratum* leg of C5. But the case-study leg — H2's 5/5 unique
   detection (line 766, "the load-bearing comparative result of the case
   study is H2") — is by-construction by the same logic, and remains
   load-bearing. Asymmetric treatment: App. F's 25/25 is demoted to
   pipeline-correctness while the case-study's 5/5 (same construct-trace
   pattern) is retained as H2 evidence. Score 3 ("partially addresses but
   leaves core intact"). Maintain CRITICAL.]
```

**Concession tracker**:
- C1: Maintain (no concession)
- C2: Maintain (no concession)
- C3: Strengthen (anti-concession)
- C4: Maintain (no concession)
- C5: Maintain (no concession)

**Concession rate: 0/5 = 0%.** Self-flag NOT triggered (the >50% threshold). Under the protocol this means the DA judged none of the Round 3 rebuttals to score ≥4/5. This is consistent with the pattern: Round 3 substantially improved *disclosure* on all five findings, but disclosure ≠ resolution of the substantive issue. The paper's responses were of the form "we now acknowledge X in §Y" rather than "X is incorrect for the following new reason"; under Anti-Sycophancy Rule "Persistent pushback ≠ valid rebuttal", these score 1–3.

### Ignored Alternative Explanations / Paths

1. **METRIC+ + 100-sample LLM ensemble alternative path** — still not seriously evaluated. The Round 2 §subsec:pooled-headtohead Set L ensemble (line 1898, $2$-vendor × $5$-temperature, 487 MRs) is the paper's own evidence that this alternative reproduces Set N's reach with $56.5\%$ extra. Round 2 alt-path 1 unmoved.

2. **Block compactness diagnostic without the algebra** — Round 2 alt-path 2 unmoved. The paper's operational utility (coverage diagnostic) does not require Theorem 1.

3. **Direct SMT-based query equivalence solvers for $\mathcal{A}_{\mathrm{rel}}$** — Round 2 alt-path 4 unmoved. The four relational MRs at §subsec:third-domain instantiate exactly the literature the algebra wraps.

4. **NEW: "Block taxonomy as a checklist, not a construction"** — A reviewer-side alternative the paper does not consider: the eight blocks operate empirically as a *checklist* (have you considered $G$, $O_{\le}$, $T^*$, $\mathcal{T}^*$, $\mathcal{L}^*$, $\mathcal{D}^*$, $\mathcal{E}^*$, $\mathcal{B}^*_{\mathrm{rel}}$ for your SUT?) — and the checklist's value is in its *completeness for a particular kind of program*, not in `Translate`'s mechanical action. Reframing NOETHER as a *practitioner checklist with three worked instantiations* would be honest and useful; the algebra-and-closure framing inflates this contribution beyond what the theorems carry.

### Missing Stakeholder Perspectives

- **Industrial Java/C++ test engineers**: Same as Round 2. The §7.5 engineering guidance has not added a protocol for "deciding whether a program admits $\mathcal{A}_P$".
- **Reproducibility-via-cross-team-agreement reviewers**: Same as Round 2. LRCA $\kappa$ is LLM-LLM only; no human inter-rater agreement.
- **TOSEM theoretical-track reviewers**: Same as Round 2. Theorem 1 (2-line bookkeeping), Theorem 2 (assumption-based bound), and a careful non-theorem (Theorem 1′ falsification). The "ten Translate-extension dimensions" framing reads as a count of open problems, not theorems.
- **NEW: Editors evaluating self-citation / circularity ratio.** The paper's 84-MR PWR corpus is the authors' own prior work (line 118); the audit raters are LLMs (shared training data with the authors' published work); the mutation set for the load-bearing case study (line 722) is hand-constructed by the authors with explicit construct-trace design; the relational MRs (line 838) wrap the cited literature's canonical identities. The "independent external validation" footprint is small. A circulation-and-confirmation editor would flag this.

### Unexamined Premise (Frame-Lock)

**The paper's central unexamined premise remains that "MR identification" is the binding constraint.**

Round 2's frame-lock analysis is unchanged. The §1 framing (lines 116–124) takes "MR identification" as the bottleneck, citing Segura 2016 and LiTOSEM 2025. The reality may be that *MR maintenance, MR reuse across SUT versions, MR adequacy assessment*, and *practitioner education in operator algebras* are the binding constraints — none of which NOETHER addresses. The framework also raises the upstream cost (10 h $\mathcal{A}_P$ distillation per family, Table 8) on the assumption that this cost is offset by downstream automation; but the downstream automation (CONSTRUCT-MP) is the part that is provably mechanical, and `Translate` was always going to be mechanical — that is what makes Theorem 1's proof two lines.

**Subsidiary unexamined premise** (also from R2): "operator-algebra-friendly" SUTs are exactly the cases where MR identification is already easiest (textbook-codified domains). The framework's three case studies — reactor physics, equivariant ML, relational query optimisers — are precisely the SUTs where decades of textbook literature has identified the canonical invariants. The "out-of-scope by construction" disclaimer at line 78 (web applications, RLHF, distributed consensus, compiler optimisations) is the field's hard problems. NOETHER systematically addresses the easy half and disclaims the hard half. This is the inverse of what a binding-constraint-relief tool should do, and the paper does not engage with this critique.

### Observations (Non-Defects)

- The negative-PWR instantiation (§subsec:negative-pwr, App. C.6.1–C.6.3) is still admirable. Picking your strongest domain and proving your strongest conjecture fails there is a contribution to disciplinary norms regardless of the DA reading of Theorem 1 as tautology.
- The Appendix F boldface "excluded from H3a.1 evidence base" disclaimer (line 3267–3268) is the right kind of transparency move and should be retained.
- The §6.6 head-to-head opening sentence (line 1604–1607) — leading with "Set N is dominated by Set G" — is honest and rare. A typical paper would bury this.
- The MR-generation cost matrix (Table 8) remains the field's first explicit cost decomposition across GP, LLM, mining, and algebraic methods; even if M5/M7 from R2 stand, the table itself is useful infrastructure.
- The 5/6 outlier rule was at least *committed to git on 2026-05-15* with a Round 2 traceable origin (line 1178–1179), not silently rewritten. This timing transparency is the right discipline; the substantive critique (rule codified post-data on its own substrate) stands separately.

### Round 3 NEW Attack Vectors

#### NEW-A: Set-MP ⊊ NOETHER block coverage from 3-SUT manual analysis (graded MAJOR, escalation candidate)

§para:metricplus-headtohead-small (lines 2533–2616) introduces a manual METRIC+ derivation on three SUTs (midpoint, hypotSig, powerSig), with Table 11 (line 2574) showing 6, 5, 3 non-vacuous Set-MP MRs respectively, all mapping to NOETHER blocks already covered by Set-N, plus three Set-N MRs without Set-MP counterpart. The structural conclusion: "Set-MP ⊊ NOETHER block coverage on the bivariate-input subsample" (line 2600–2602).

**The construct-validity hazard is analogous to C5.** The 11 D×R category framework is parametrised by the SUT (acknowledged at line 2502–2505: "operationalised here for the comparison-sort SUT ... drawing on the category families enumerated in those works rather than as a verbatim copy"). The framework's *own designers* are now applying it to METRIC+ — the "vacuous" cells in Table 11 (5/11, 6/11, 8/11 vacuous on the three SUTs) are decided by the same designers. Set-N's coverage of every non-vacuous Set-MP block is therefore tautological in the same sense Appendix F's 25/25 is tautological: each Set-MP non-vacuous MR is mapped to a NOETHER block by the NOETHER team, and Set-N has a representative in each block by construction.

This is an additional construct-trace-circular reading on top of C5, applied to the structural-subsumption claim against METRIC+. **R4's integrity audit caught the Mode-3 errors (powerSig count 4→3, caption 9/8/9→6/5/3) — but the deeper construct-validity issue is not a counting error; it is that the analysis grants the framework's designers adjudicatory power over both sides of the comparison.** Grade: MAJOR with escalation candidate status if the structural claim is repeated in headlines.

**Mitigation request**: either (i) re-execute METRIC+ on the substrate with an external METRIC+ classifier (impossible — METRIC+ is "category enumeration scaffold rather than an automated MR identification pipeline", line 2486–2487, so no executable METRIC+ exists), in which case the head-to-head is genuinely impossible and the structural claim should be downgraded to "the framework's designers' manual mapping suggests subsumption"; or (ii) frame the entire §para:metricplus-headtohead-small as "tentative manual mapping pending Future Work (i) execution" and not as a "structural finding" (which is how line 2600 labels it).

#### NEW-B: OR=3.75 + RD=+0.212 as garden-of-statistics addition (graded MAJOR)

Already incorporated into C4 reasoning above. The addition is reportable per common standards (effect size alongside p-value is good practice), but **the framing matters**: the paragraph at lines 1827–1836 now contains three effect-size readings on the same (b, c) = (15, 4) discordant cell — McNemar p=0.019, RD=+0.212, OR=3.75. Without a primary effect-size declaration, the reader is presented with three views of one dataset. The OR=3.75 in particular reads more moderately than a 21pp absolute gap on a 52-mutant denominator: 3.75x odds on 19 discordant pairs is statistically robust evidence of dominance, but presented as "OR = 3.75" alongside RD=+0.212 it dilutes. **The R3 honest framing**: declare the primary effect-size measure for the head-to-head comparison (RD is the most interpretable for clinicians reading a 2x2 paired table; McNemar p is the inferential test; OR is rare in McNemar reporting), report it, then add the others under "alternative effect-size measures". Currently all three are co-equal in the paragraph.

#### NEW-C: "5 proven + 5 by-inspection" two-tier disclosure (graded as C2-reinforcement, see C2 above)

Round 3 explicitly distinguishes "5 proven by per-block exhaustion" + "5 asserted by inspection" (lines 78, 135, 152, 904). The "proven" half is itself a per-template scan against the 8 blocks of Table 4's `Translate` template (line 977: "exhausting the eight blocks against the per-block `Translate` templates"). **This is not a formal-logic exhaustion proof in the sense of "no extension to `Translate`'s signature can absorb any two of the five obstructions"**; it is a per-template scan against the current `Translate` definition. Under a Composite-`Translate` extension (which the paper itself flags as open at line 152: "The question of whether a Composite-`Translate` extension absorbs the ten ... remains open"), some of the five obstructions could collapse pairwise. The "pairwise independence" claim is therefore *relative to the current `Translate` signature*, not absolute. The Round 3 two-tier disclosure makes the by-inspection half visible but does not address the absoluteness question on either half. C2 reinforced.

#### NEW-D: Pre-registration semantics (graded MINOR m7, but with CRITICAL implications for C3)

Line 1178–1179's "codified ... in response to a Round 2 review observation" is the paper's own admission that the falsification rule which adjudicates `hypotSig` was written after the kill data was observed. The Round 3 text frames this as "future cross-codebase substrates inherit the rule as a written test" (line 1186), implying the rule is now prospective. But the 5/6 verdict on the §subsec:test-design substrate **was decided under the rule that was codified after seeing the substrate's data**. The pre-registration is therefore prospective for *future* substrates but post-hoc for *this* substrate. The honest framing would acknowledge: "on the substrate that prompted the rule's codification, the 5/6 verdict is data-conditional and should be treated as exploratory; the prediction's falsifiability is established for future cross-codebase substrates only, and the cross-codebase commons-math pilot at line 1308–1309 (2/29 = 6.9%) is the first such substrate." Currently the paper presents the 5/6 verdict as "consistent with data" (line 78) without this caveat in the abstract.

---

## DA Summary (300 words)

**(a) Single strongest counter-argument**: Theorem 1 remains a closure-under-construction tautology in substance, with Round 3 adding the disclosure at lines 432–433 but preserving the Abstract/§1-C2a "two-layer framework: ... downstream layer mechanical and provable" framing (lines 76, 134). The only non-tautological closure statement (Theorem 1′) is falsified on $\mathcal{A}_{\mathrm{PWR}}$, repaired by the "ten Translate-extension dimensions" headline — of which 5 are "asserted by inspection" by the paper's own admission (lines 152, 904) and 2 specialise PWR-side dimensions to type-distinct primitives (line 135). Subtracting the tautology and the unproven half leaves an empirically curated eight-block taxonomy, Theorem 2's poly-time decidability under finite generating set, one falsifiable prediction whose outlier-handling rule was codified post-data on its own substrate (line 1178–1179), and a head-to-head where Set N is dominated by Set G on the in-scope D1 stratum (line 1604–1607).

**(b) C1–C5 rebuttal scores + actions**:
- C1 — Theorem 1 tautology: **2/5, Maintain** (disclosure ≠ relocation of substance).
- C2 — "10 dimensions" engineered: **3/5, Maintain** (two-tier disclosure visible but core unmoved; 2/5 specialisations confirm C2's reused-dimension charge).
- C3 — L*-blindness post-hoc rescue: **1/5, Strengthen** (paper's verbatim admission that rule codified 2026-05-15 in response to R2 confirms post-data codification on the rule's own adjudication substrate).
- C4 — Set G dominance reframing: **2/5, Maintain** (OR/RD addition is statistics-garden, not rebuttal).
- C5 — construct-trace circularity: **3/5, Maintain** (App. F demoted but case-study H2 retains same construct-trace structure as load-bearing).

**(c) Round 3 NEW CRITICAL**: None *new* at CRITICAL (the new attack vectors NEW-A through NEW-D reinforce C2/C3/C5 rather than open a new category). NEW-A (Set-MP subsumption from 3-SUT framework-designer manual analysis) is MAJOR with escalation potential.

**(d) Self-flag**: **Concession rate: 0/5 = 0% (no self-flag triggered)**. Anti-Sycophancy Protocol §"No consecutive concessions" did not engage. The DA judged that Round 3 substantially improved *disclosure* on all five findings but did not provide ≥4/5 rebuttals on any. Per protocol, this means a human reviewer should verify whether the DA is correctly resisting accommodation pressure or applying overly strict standards; the position is defensible because every Round 3 response is in the form "we now acknowledge X" rather than "X is incorrect for the following new reason", and persistent disclosure ≠ valid rebuttal.

— Devil's Advocate, independent of editorial synthesis (Round 3, commit `ceac6ed`)
