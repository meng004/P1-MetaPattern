# Verification Review Report (Stage 3' Re-Review)

**Manuscript**: NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
**Manuscript ID**: ACM TOSEM (anonymised submission)
**Re-review Date**: 2026-05-15
**Re-review Round**: Round 2 verification (Stage 3' of academic-pipeline state machine)
**Revised commit**: `3f47513 revise(stage-4 r2): Major→Minor Round 2 revisions; 13 Required + S1/S6/S8` on branch `feat/section-7-empirical-vs-sota`
**Base commit (pre-revision)**: `33db749 fix(stage-4.5 r2): Mode 1+3 BLOCKING fixes from FINAL INTEGRITY`
**Reviewer**: EIC (verification mode); IRON RULE — independently verify each Required item against revised manuscript, not author-stated claims alone.

---

## Decision

### **Minor Revision**

The Round 2 Major Revision decision was driven by (i) R1 W1 file-grounded Mode 6 integrity blocker (Set L placeholders), (ii) DA 5 CRITICAL findings, (iii) CONSENSUS-5 framing inconsistency between abstract and body on §6.6 head-to-head dominance, (iv) CONSENSUS-5 Theorem 1 tautology framing, and (v) the additional Required and Suggested items in the Editorial Roadmap.

Stage 4 revisions (commit `3f47513`) address all 13 Required items and 4 of 12 Suggested items. **11 of 13 Required are FULLY_ADDRESSED. 2 of 13 are PARTIALLY_ADDRESSED with NEW residual issues identified by this verification: abstract still over-asserts "ten pairwise-independent" without the body's proven/candidate distinction (NEW-1); §1 C4 (line 137) misses the abstract's "operator-algebraic" qualifier on the three-domain claim (NEW-2).** Both residual issues are framing alignment (< 1 hour text fix), not substantive content drift; the paper's arguments (Theorem 1 substantive value, §6.6 D1 dominance disclosure, Theorem 1' falsification scope, L*-blindness outlier rule pre-registration, METRIC+ structural-mapping evidence, external-validity structural transferability) are preserved without drift relative to the original paper position.

The decision is therefore **Minor Revision** rather than direct Accept because (a) the two residual framing alignments must be fixed before the manuscript reaches camera-ready, and (b) the Stage 4.5 R4 FINAL INTEGRITY check has not yet run against the revised paper (Stage 4.5 R3 was run against the pre-revision commit `33db749` and did not cover `mr_sets/*.py` or the full 57-entry bib audit).

---

## Revision Response Checklist (Schema 11: R&R Traceability Matrix)

### Priority 1 — Required Revisions

| # | Original Review Comment | Author's Claim (commit 3f47513) | Response Status | Revision Location | Verified? | Quality Assessment |
|---|---|---|---|---|---|---|
| R1 | Set L is implemented as `_placeholder_*_fn` in `supplementary/S3_case_study/mr_sets/set_L_llm.py` but paper claims actual GPT-4 output — Mode 6 (methodology fabrication) blocker | Ran actual prompt against `gpt-4-turbo-2024-04-09` (temp=0, seed=4246) via bltcy.ai proxy; replaced 5 callables; reran runner.py; Set N 7/20, Set L 2/20 unchanged; supplementary/README/dataset_versions synced | **FULLY_ADDRESSED** | `set_L_llm.py`, `prompt_log.md`, `S3 README.md`, `S4 dataset_versions.txt`, paper §subsec:case-study | ✅ Yes | `grep "placeholder" set_L_llm.py = 0`; `prompt_log.md` Date generated: 2026-05-15 (UTC); `table4.json` shows Set N=7, Set L=2, McNemar p=0.0625, Fisher p=0.1274; integrity blocker resolved without claim drift |
| R2 | Theorem 1 framing: scope qualifier missing; "algebraic-closure guarantee" reads as absolute closure | Abstract restored author position ("Theorem 1 converts empirical-adequacy to structural-adequacy obligation within explicitly bounded scope"); §1 C2 split to C2a positive + C2b negative; §3.3 substantive-content discussion restored "converts empirical to structural adequacy" + acknowledged by-construction within scope; Lemma C.1 labelled `lem:canonical-order` | **FULLY_ADDRESSED** | Abstract L76; §1 C2a/C2b L134-135; §1 Boundary box item 1 L145 + item (a) L152; §3.3 L432; App. C Lemma C.1 | ✅ Yes | Author position preserved (substantive value of conversion); scope qualifier added (Definition `def:alg-induced` fixes MR(A_P) as Translate-image); DA C1 reframing rejected per drift-free discipline; all four locations consistent |
| R3 | §6.6 body says "competitive parity" while abstract says "Set N is dominated by Set G" — internal inconsistency, CONSENSUS-5 | §subsec:pooled-headtohead title renamed to "per-block decomposition of an aggregate Set G dominance"; lead paragraph leads with McNemar p=0.0043 + p=0.019 D1 dominance fact; framework contribution (derivability + per-block complementarity + D2 prediction) demoted to secondary; "competitive parity" removed throughout | **FULLY_ADDRESSED** | §subsec:pooled-headtohead title L1601, lead paragraph L1604-1619, cost-axis paragraph L2261 | ✅ Yes | `grep "competitive parity" = 0`; lead paragraph leads with **bold dominance fact**; per-block T* edge framed as "directional finding consistent with the framework's design prediction on that block; does not overturn Set G's aggregate dominance" |
| R4 | `Wang2024QED` bib has wrong authors (Sicheng Mao, Boyuan Tang, Junfeng Zhang, Yisu Remy Wang) — R3 W2 | Verified bib already correct (Wang/Pan/Cheung) matching CrossRef DOI 10.14778/3681954.3682024; cleaned 3 obsolete notes in `theory/rel_thm1prime_search.md` line 16, 191-196, 210-212 marking F1 follow-up as resolved | **FULLY_ADDRESSED** | NOETHER_paper.bib `Wang2024QED`, theory/rel_thm1prime_search.md | ✅ Yes | CrossRef DOI lookup confirms author list Shuxian Wang; Sicheng Pan; Alvin Cheung; R3 W2 was reviewer misreading of obsolete companion-doc comment, not actual bib error |
| R5 | "10 pairwise-independent Translate-extension dimensions" is engineered count; pairwise-independence claim unproven on equi/rel side — DA C2 | Preserved ten-dimension count; distinguished proven (5 PWR-side, per-block exhaustion in App. C.6) from candidate (5 equi/rel-side, asserted by inspection); committed formal exhaustion proofs on A_equi/A_rel as follow-up | **PARTIALLY_ADDRESSED** | §1 C2b L135 ✓; §1 Boundary box (a) L152 ✓; **Abstract L78 ✗ (still over-asserts)**; **§subsec:third-domain L904 ✗ (still over-asserts)** | ⚠️ Partial | Body locations carry the proven/candidate distinction correctly. Abstract and §subsec:third-domain still claim "ten pairwise-independent Translate-extension dimensions across the three algebras" as if all ten are formally proven; reader of abstract alone receives the original (uncorrected) over-claim. **Residual issue NEW-1.** |
| R6 | L*-blindness "5/6 SUTs" outlier-handling rule was post-hoc; pre-registration covers threshold but not outlier rule — DA C3 (falsifiability illusory) | Added `l_blindness_prediction` section to `noether-s5-experiment/configs/d4j_algebra_rich_criterion.json` with rule registered 2026-05-15 UTC + rationale explicit; paper §subsec:l-blindness-derivation added disclosure paragraph; hypotSig retained as worked example; under codified rule both killed mutants classify as homogeneity-breaking; 5/6 verdict stands | **FULLY_ADDRESSED** | `configs/d4j_algebra_rich_criterion.json` `l_blindness_prediction.outlier_handling_rule`; paper §subsec:l-blindness-derivation L1167-1185 | ✅ Yes | JSON validates with new `outlier_rule_registered_at_utc: 2026-05-15T00:00:00Z`; paper disclosure explicit on post-codification timing; hypotSig classification matches the codified rule's BREAKS_HOMOGENEITY taxonomy; DA C3 attack on falsifiability illusory is resolved by codification |
| R7 | DeepCrime pilot at n=5, Fisher p=1.00 has 3 inferential claims unsupported by sample size — R1 W3 | Split §subsec:deepcrime-pilot Reading paragraph into (i) inferential verdict (n=5/p=1.00 underpowered; descriptive evidence only; load-bearing claim is only that infrastructure runs end-to-end) and (ii) mechanism interpretation (independent of sample size) | **FULLY_ADDRESSED** | §subsec:deepcrime-pilot L806-815 | ✅ Yes | Two paragraphs cleanly separated; inferential verdict opens with "At n=5 the Fisher-exact p-values...are both p=1.00; pilot is therefore underpowered for an inferential conclusion at α=0.05"; mechanism paragraph labelled "(mechanism, not inference)"; passes CLAUDE.md C6 rule |
| R8 | 84-MR PWR corpus is the authors' own prior work; "systematisation" is re-binning not external transfer — R2 W3 + R3 W3 + DA M4 | Added `\paragraph{Provenance and scope of the inductive catalogue.}` at start of §subsec:reactor-mapping; explicitly states corpus is authors' own; comparison tests internal vocabulary coherence not external transfer; commits Table 14 item (j) for external-team corpus follow-up (PARCS V&V / IAEA-TECDOC) | **FULLY_ADDRESSED** | §subsec:reactor-mapping L517-518; Table 14 item (j) | ✅ Yes | Provenance disclosure leads §subsec:reactor-mapping; internal/external transfer distinction made explicit; commons-math pilot cited as the Java-side analogue at n=3 SUTs; future-work item (j) committed |
| R9 | METRIC+ head-to-head described but never run — R2 W2 | Added §para:metricplus-headtohead-small + Table `tab:metricplus-headtohead-small` applying METRIC+'s 11 D×R framework manually to 3 §6.6 SUTs (midpoint, hypotSig, powerSig); structural finding documented; full PIT head-to-head committed as Table 14 item (i) | **FULLY_ADDRESSED** | §subsec:relationship-with-METRIC `\paragraph{Small-scale manual METRIC+ derivation...}` L2533; Table `tab:metricplus-headtohead-small` L2571 | ✅ Yes | 3-SUT manual derivation present; per-pair non-vacuous count + algebra-block mapping + Set-N coverage of those blocks reported; structural finding "Set-MP ⊊ NOETHER block coverage on this substrate" honestly stated; full PIT head-to-head appropriately deferred to Table 14 (i) |
| R10 | Supplementary code must match paper text (was inconsistent due to R1) | Consequent on R1; set_L_llm.py 5 callables, prompt_log.md filled, S3 README.md "Replacing Set L placeholders" rewritten as "Regenerating Set L from the GPT-4 prompt", S4 dataset_versions.txt LLM-baseline section updated | **FULLY_ADDRESSED** | `supplementary/S3_case_study/{set_L_llm.py, prompt_log.md, README.md}`, `supplementary/S4_reproducibility/dataset_versions.txt` | ✅ Yes | Three files updated consistently; README.md now describes regeneration procedure (not placeholder replacement); dataset_versions.txt status field reflects 2026-05-15 generation |
| R11 | Literature gaps: Hu 2019, Sun 2022 CSUR, Liu 2020 MET, Mariani 2018 MET, Lin 2020 symmetry-MR, Ying 2025 deeper engagement, algebraic-SE traditions — R2 W4 | Added Zhou 2020 SymmetryMRP (CrossRef-verified DOI 10.1109/TSE.2018.2876433); §2.4 deeper engagement with Ying 2025 family-tree formalism (NOETHER block ↔ family-tree node mapping); Sun 2022 ACM CSUR survey is Li 2025 TOSEM (LiTOSEM2025) already in bib; 4 unverifiable references (Hu 2019, Liu 2020 MET, Mariani 2018 MET, Lin 2020 symmetry-MR) declined per CLAUDE.md §3 step 2c hard-block (paper-search-mcp CrossRef + DBLP + Semantic Scholar returned no matches) | **FULLY_ADDRESSED** | §2.4 L191-193 (Zhou 2020 + Ying engagement); `NOETHER_paper.bib` Zhou2020SymmetryMRP | ✅ Yes | Real citation added (Zhou 2020 CrossRef DOI confirmed); Ying 2025 dedicated engagement paragraph adds Ying family-tree ↔ NOETHER block mapping; decline-rationale honest (paper-search-mcp triple-tier failure, integrity > reviewer satisfaction) |
| R12 | Augmented stratum table 13: 25/25 number leaks into headline despite design-implied caveat — R1 W4 + DA C5 | Table 13 caption: bold "Set N's column is design-implied"; bold "This table is excluded from the H3a.1 evidence base"; CTT (construct-trace test) prefix abbreviation in column headers; Set N rate column italic + dagger marker; CTT footnote explicit "Do not compare 1.000^dagger against Set G's 0.480 as if they were commensurable"; Table 14 item (g) design-implied caveat italicised; §app:augmented-stratum's "Why this is not a head-to-head test" paragraph labelled `para:construct-trace-not-headtohead` | **FULLY_ADDRESSED** | Table `tab:augmented-stratum` L3271-3281; Table 14 item (g); §app:augmented-stratum `\paragraph{Why this is not a head-to-head test of H3a.1.}` | ✅ Yes | Visual marking present in every Set N column entry (italic + dagger); footnote calls out incommensurability of 1.000^dagger vs 0.480; caption explicit exclusion from H3a.1 evidence base; DA C5 attack on construct-trace-circular-as-headline is resolved by visual + textual disclosure |
| R13 | External-validity claims exceed empirical substrate — EIC W1 + R3 W1+W5 + DA M5 | Abstract scope sentence enumerates 4 out-of-scope program-family classes (web apps / RLHF / distributed consensus / compiler internal); abstract three-domains qualifier added "operator-algebraic" + "structural transferability rather than cross-domain empirical superiority"; §3 added Remark `rem:domain-out-of-scope` (4 domain-level out-of-scope classes distinguished from candidate-ninth-block in Remark 4); §9 Conclusion: team adoption is open follow-up | **PARTIALLY_ADDRESSED** | Abstract L78 ✓; §3 `\begin{remark}[Domain-level out-of-scope]` L345-346 ✓; §9 Conclusion Transferability L2692 ✓; **§1 C4 L137 ✗ (missing qualifier)** | ⚠️ Partial | Abstract / §3 / §9 all carry the structural-transferability qualifier and out-of-scope enumeration. **§1 C4 (L137) still says "three structurally distinct domains" without the abstract's "operator-algebraic" qualifier**, so the §1 contribution list misaligns with abstract framing. **Residual issue NEW-2.** |

### Priority 2 — Suggested Revisions

| # | Original Review Comment | Response Status | Notes |
|---|---|---|---|
| S1 | Add "Comparators and why" paragraph at top of §6.6 or §2.4 — EIC W3 | **FULLY_ADDRESSED** | Added as `\paragraph{Comparators in the head-to-head: what is compared and why.}` at §2.5 end L209-235; explains rationale for each of 4 SOTA categories (Set G executed; METRIC+ scaffold + Table 14 item (i); MR-Scout structurally absent; AutoMT/GPTMR domain mismatch; Set L ensemble in-scope LLM-assisted) |
| S2 | §6 empirical-overview table summarising 4 sub-studies (n / mutation source / comparator / hypothesis / verdict) — R1 Detailed | **NOT_ADDRESSED** | Declined: large structural addition, risk of framing drift; sub-study descriptions already distributed across §6.6 / §6.6.1 / §subsec:case-study with explicit per-section headers |
| S3 | §6.8 negative → §7; §7 → §8 renumbering — EIC W5 | **NOT_ADDRESSED** | Declined: large structural change with broad cross-reference impact; risk of `\ref` breakage and unstable section ordering across the paper |
| S4 | Drop one of three Boundary-of-contribution boxes — EIC Minor | **NOT_ADDRESSED** | Declined: triple-box discipline is deliberate anti-overclaim signal; removing weakens reader-facing scope discipline |
| S5 | Promote §subsec:third-domain or §subsec:negative-pwr to top-level §6 — R2 Layout | **NOT_ADDRESSED** | Declined: changes section-weight balance; risk of framing drift on what counts as "first-class instantiation" vs "negative instantiation" |
| S6 | Add OR / RD effect size for paired McNemar — R1 Stat reporting | **FULLY_ADDRESSED** | Added to §subsec:pooled-headtohead D1 aggregate paragraph: "paired risk difference RD_paired = (b - c)/n = (15 - 4)/52 = +0.212 favouring Set G, and odds ratio OR = b/c = 15/4 = 3.75" |
| S7 | Single-author re-classification audit on n=18 both-miss mutants — R1 Detailed | **NOT_ADDRESSED** | Declined: requires new empirical work; LLM-2-of-3 vote with κ=1.000 on parseable items reported as construct-validity check |
| S8 | Update `Bronstein2021GDL` to MIT Press 2024 book version if available — R2 Minor | **PARTIALLY_ADDRESSED** | MIT Press 2024 book version not found via CrossRef; instead changed bib type from `@book` (which had malformed `publisher = {arXiv preprint arXiv:2104.13478}`) to `@misc` with proper `eprint = 2104.13478, archivePrefix = arXiv, primaryClass = cs.LG`. Reviewer's specific suggestion (MIT Press version) couldn't be verified; bib hygiene improvement made |
| S9 | Trivial/semi-trivial/non-trivial breakdown of 84-MR corpus — R3 W3 | **NOT_ADDRESSED** | Declined: requires new categorisation work; supplementary S2 contains the raw corpus for reviewer audit |
| S10 | Per-MR labelling reasoning for 18-MR audit — R3 Detailed | **NOT_ADDRESSED** | Declined: supplementary S2 18mr_audit/ contains raw labels; deep traceability is supplementary domain |
| S11 | Drop §6.6.1 DeepCrime pilot from abstract — DA M4 | **NOT_ADDRESSED** | Declined: abstract already qualifies as "n=5, underpowered for α=0.05 inferential conclusions"; removing entirely would be reviewer-pleasing over-correction without论点 necessity; honest disclosure is the right framing |
| S12 | C2 contribution split into C2a (positive) + C2b (negative) — EIC Minor | **FULLY_ADDRESSED** | Completed jointly with R2 Theorem 1 framing; §1 C2 now reads as C2a positive theory (Theorem 1 + Theorem 2) + C2b negative theory (Theorem 1' falsification + 10 extensions) |

---

## New Issues (Discovered During Revision)

| # | Type | Severity | Location | Description | Suggested Fix |
|---|------|---------|----------|-------------|---------------|
| **NEW-1** | Framing inconsistency | Minor | Abstract L78 + §subsec:third-domain L904 | Abstract and §subsec:third-domain still write "ten pairwise-independent extensions across the three algebras" while §1 C2b (L135) and §1 Boundary box item (a) (L152) correctly distinguish proven (PWR-5) from candidate (equi/rel-5 asserted by inspection). Reader of abstract alone receives the original (uncorrected) over-claim that all 10 are formally proven pairwise-independent. | Replace "ten pairwise-independent extensions" in Abstract L78 with "five pairwise-independent extensions on the PWR core diffusion algebra plus five candidate extensions on the equivariant-ML and relational-query algebras, totalling ten Translate-extension dimensions (pairwise independence proven on the PWR-side five and asserted by inspection on the candidate five)". Apply equivalent wording to §subsec:third-domain L904. |
| **NEW-2** | Framing inconsistency | Minor | §1 C4 L137 | §1 C4 says "we demonstrate cross-domain transferability ... by instantiating NOETHER on three structurally distinct domains: Boltzmann reactor-physics transport, equivariant machine learning, and relational query optimisers" without the abstract's added qualifier "operator-algebraic" or the "structural transferability rather than cross-domain empirical superiority" caveat. Reader of §1 alone receives the original (uncorrected) over-claim. | Insert "structurally distinct **operator-algebraic**" and append a clause "; the demonstration is of structural transferability at the algebra-skeleton level, not cross-domain empirical superiority". |

Both NEW issues are framing-alignment residuals (abstract / §1 contributions list / §subsec:third-domain do not consistently apply the body's nuance). Neither is substantive content drift; the paper's论点 (Theorem 1 substantive value, §6.6 dominance disclosure, Theorem 1' falsification scope, L*-blindness pre-registration, METRIC+ structural mapping, external-validity structural transferability) is preserved correctly in the body sections.

---

## Decision Rationale

The Round 2 review identified 13 Required + 12 Suggested revisions plus 5 DA CRITICAL findings. Stage 4 (commit 3f47513) addresses all Required items at the body level and 4 of 12 Suggested items (S1 / S6 / S8 / S12) with explicit decline rationale for the remaining 8 Suggested (per drift-discipline: declined items are large structural changes or new empirical work; their absence does not affect论点).

**Verification independence**: Each Required item was checked by reading the actual revised .tex (not relying on author's commit-message claim). The two PARTIALLY_ADDRESSED items (R5, R13) are caught by this independent verification: the author's claim that the count was "tightened" or the qualifier was "added" is true at most body locations but missed the abstract and §1 contribution list, creating internal inconsistency.

**DA Attack Intensity Preservation** (per protocol §"Anti-Sycophancy Rules"): All 5 DA CRITICAL findings from Round 2 are substantively addressed —
- C1 (Theorem 1 tautology): rejected via drift-free framing (Theorem 1 substantive value preserved + scope qualifier added; DA's reframing to "well-formedness only" was not accepted).
- C2 (10 extensions engineered): body distinguishes proven/candidate; **abstract still over-asserts (NEW-1)** — DA C2 is not fully resolved at the abstract level.
- C3 (L*-blindness rescue post-hoc): codification of outlier rule in pre-registration config + paper disclosure; falsifiability now operational.
- C4 (D1 dominated, garden of forking): §subsec:pooled-headtohead now leads with dominance fact; framework contributions demoted to secondary.
- C5 (augmented stratum circular): table visual marking (italic + dagger + CTT prefix) + caption "excluded from H3a.1 evidence base" + footnote on incommensurability.

The two PARTIALLY_ADDRESSED items are easy to fix and do not warrant another full Major Revision cycle. Accordingly:
- **Decision**: Minor Revision (rather than Accept)
- **Conditions**: Fix NEW-1 and NEW-2 (1 hour); proceed to Stage 4.5 R4 FINAL INTEGRITY (independent from-scratch verification including `mr_sets/*.py` and the full 57-entry bib, which Stage 4.5 R3 did not cover).

---

## Residual Issues (List for Author Action)

| # | Issue | Action | Estimated Effort |
|---|---|---|---|
| 1 | NEW-1 abstract / §subsec:third-domain "ten pairwise-independent" | Apply proven/candidate distinction at abstract L78 and §subsec:third-domain L904 to match §1 C2b L135 and Boundary box (a) L152 | 30 min |
| 2 | NEW-2 §1 C4 missing "operator-algebraic" qualifier and "structural transferability" caveat | Insert qualifier and caveat at L137 to match abstract L78 | 15 min |
| 3 | Stage 4.5 R4 FINAL INTEGRITY (per pipeline state machine, mandatory after Stage 3' before Stage 5) | Independent from-scratch verification: scan `supplementary/S3_case_study/mr_sets/*.py` (R3 missed), audit full 57-entry bib via CrossRef/DOI (R3 sampled 10/57), run 7-mode AI Failure Mode Checklist on revised paper | 1-2 hours |

Once NEW-1 + NEW-2 are fixed and Stage 4.5 R4 passes, the paper is ready for Stage 5 FINALIZE (format conversion + camera-ready PDF).

---

## Recommendation to Pipeline Orchestrator

- **Decision**: Minor Revision
- **Next step in state machine**: Author addresses NEW-1 + NEW-2 (Stage 4'), then directly proceed to Stage 4.5 R4 (no second Stage 3'' re-review needed because the two residuals are framing alignment, not substantive content)
- **Stage 5 FINALIZE readiness**: blocked on (1) NEW-1 + NEW-2 fixes, (2) Stage 4.5 R4 PASS

---

## Appendix: Verification Sources

| File | Source verified |
|---|---|
| `NOETHER_paper.tex` | Direct read of L76 (abstract), L134-135 (C2a/C2b), L137 (C4), L145+152 (Boundary box), L191-193 (§2.4 Ying), L209-235 (§2.5 Comparators), L345-346 (Remark domain-out-of-scope), L432 (§3.3 substantive content), L517 (Provenance), L806-815 (DeepCrime split), L904 (third-domain ten extensions), L1167-1185 (outlier rule disclosure), L1601-1619 (§6.6 lead), L2533-2604 (METRIC+ small-scale), L2692 (§9 Conclusion), L3271-3281 (augmented stratum table) |
| `NOETHER_paper.bib` | `Wang2024QED`, `Zhou2020SymmetryMRP` (new), `Bronstein2021GDL` (@book → @misc) — all CrossRef-verified |
| `supplementary/S3_case_study/mr_sets/set_L_llm.py` | `grep "_placeholder_" = 0`; 5 callables named `_llm_rot_fn`, `_llm_trans_fn`, `_llm_scale_fn`, `_llm_perm_fn`, `_llm_noise_fn` |
| `supplementary/S3_case_study/mr_sets/prompt_log.md` | Date generated: 2026-05-15 (UTC); Raw GPT-4 output filled (5 JSON MR specs) |
| `supplementary/S3_case_study/table4.json` | Set N=7, Set L=2, Set B=0; McNemar p=0.0625; Fisher p=0.1274 |
| `supplementary/S4_reproducibility/dataset_versions.txt` | LLM-baseline section reflects 2026-05-15 execution + seed 4246 |
| `noether-s5-experiment/configs/d4j_algebra_rich_criterion.json` | `l_blindness_prediction.outlier_handling_rule` present with registered_at_utc 2026-05-15 |
| `theory/rel_thm1prime_search.md` | F1 follow-up marked resolved 2026-05-15 |
| Compile output | 80 pages / 602,080 B / 0 undef / 0 missing char / 58 cited = 58 defined / 0 em-dash |
