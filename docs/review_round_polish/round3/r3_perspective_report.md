# Peer Review Report — Round 3 (Perspective)

## Manuscript Information
- **Title**: NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
- **Manuscript ID**: TOSEM (anonymised, double-blind)
- **Review Date**: 2026-05-15
- **Review Round**: Round 3 (post-Major-Revision verification, commit `ceac6ed`)

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 (Perspective)

### Reviewer Identity
Cross-disciplinary V&V scholar. Combined background in (i) reactor physics and PWR safety analysis (Bell & Glasstone; Lewis & Miller; Stacey 2007; Lamarsh & Baratta; ANS 19.6.1; NRC RG 1.77; 10 CFR 50 Appendix A GDC 11); (ii) equivariant ML / geometric deep learning (Cohen–Welling; Bronstein; Thomas–Smidt TFN; Cohen et al.\ 2019 gauge-equivariant CNN; Satorras EGNN; Haan et al.\ 2020 gauge mesh CNN); (iii) relational database theory and idempotent semirings (Apache Calcite rewrite-rule corpus, Wang/Pan/Cheung 2024 QED).

### Review Focus
Independent verification — without sight of the Stage 3' re-review or Stage 4.5 R4 reports — that the five Major weaknesses I raised in Round 2 are genuinely resolved at commit `ceac6ed`, plus structural/physics/mathematical accuracy of the revisions themselves. Scope: cross-domain accuracy, external validity, structural transferability claim.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
**4** (high on PWR proofs, gauge-bundle obstruction math, Stacey §3.4 MTC decomposition, and ANS 19.6.1 / GDC 11 placement; slightly lower on the single-rater Calcite classification because I am ratifying the F3 follow-up commitment rather than re-running the QED solver myself).

### Summary Assessment
The Round 2 Major-Revision package has substantially addressed four of the five W1–W5 weaknesses I raised. The abstract and §1 contributions now explicitly qualify the three-domain claim as "structural transferability at the algebra-skeleton level rather than asserting cross-domain empirical superiority", and a dedicated `rem:domain-out-of-scope` (L345–355) catalogues web apps / RLHF / distributed consensus / compiler-internal as structurally out of scope (not candidate ninth blocks). The Wang2024QED bib entry is now correct (Wang/Pan/Cheung at `NOETHER_paper.bib` L286–292, CrossRef-verified) and `theory/rel_thm1prime_search.md` L208–211 marks F1 Resolved 2026-05-15. §subsec:reactor-mapping (L517–518) leads with a Provenance paragraph that explicitly identifies the 84-MR PWR corpus as the authors' own prior work, with the external-transfer test deferred to `tab:future-work` item (j) at L2380. §subsec:pooled-headtohead (L1601–1607) now leads with a bold sentence stating Set N is dominated by Set G with McNemar p=0.0043 pooled and p=0.019 on D1, and §9 Conclusion (L2695) explicitly notes cross-domain empirical superiority and team adoption as open follow-up. The PWR §subsec:negative-pwr / Appendix C.6 physics is intact: Stacey §3.4 three-mechanism MTC decomposition (L1010–1018), GDC 11 / 10 CFR 50 App A reference (L1027), ANS 19.6.1 reference (L1027), HFP/ARO regime distinction (L1008), the C.6.1 eight-case proof exhausts each block correctly. The gauge-bundle counterexample at §subsec:third-domain (L903–904) correctly identifies rho_gauge as requiring a bundle-section pi-template parametrised by a gauge field in C(M, H), citing Cohen 2019 and Haan 2020 appropriately.

One residual inconsistency requires Minor Revision. The §subsec:empirical-threats paragraph (c) at L2158–2162 still describes the §subsec:pooled-headtohead reading as "reframed as competitive parity rather than superiority", which now contradicts that subsection's own opening bold sentence ("Set N is dominated by Set G in the aggregate, McNemar exact two-sided p=0.0043 pooled and p=0.019 on D1 only"). This is a single-edit polish, not a structural objection.

---

## Strengths

### S1: W1 (three-domain asymmetry) is now correctly qualified at every load-bearing site
The new abstract sentence at L78 reads "we instantiate NOETHER on three structurally distinct *operator-algebraic* domains, testing transferability at the algebra-skeleton level rather than asserting cross-domain empirical superiority". §1 contribution C4 at L137 contains the same qualification verbatim and adds the "within the framework's scope precondition" guard. §3 Remark `rem:domain-out-of-scope` at L345–355 enumerates the four structurally absent domains (web apps, RLHF reward models, distributed-consensus protocols, compiler-internal optimisations) explicitly as out-of-scope-by-construction, distinct from the candidate-ninth-block families of `rem:counterex`. §9 Conclusion at L2695 closes the loop: "Cross-domain empirical superiority and team adoption by PWR-simulator V&V groups, equivariant-ML testing teams, or database-optimiser test groups are open follow-up questions; the present paper establishes the structural transferability of the construction mechanism, not adoption outcomes on each domain." This is the exact framing I called for in Round 2 W1. The "three structurally distinct domains" language survives but is now unambiguously algebra-skeleton-level, not multi-domain empirical superiority.

### S2: W2 (Wang2024QED bib + A_rel survey) is structurally resolved on the bib side and properly bounded on the survey side
The `Wang2024QED` bib entry (`NOETHER_paper.bib` L286–292) correctly reads `Wang, Shuxian and Pan, Sicheng and Cheung, Alvin`, with DOI `10.14778/3681954.3682024`. `theory/rel_thm1prime_search.md` L15–16 confirms the match to CrossRef-verified author order, and L191–194 explicitly states "no correction required (resolved 2026-05-15)". Follow-up F1 at L208–211 is marked Resolved. The survey itself remains a single-rater proposed classification on 12 Calcite test names rather than a QED-solver-executed audit, but this limitation is explicitly disclosed at L173–190 of `rel_thm1prime_search.md` and at L904 of the paper's §subsec:third-domain ("pairwise independence is asserted by inspection rather than by formal exhaustion proof, and full per-dimension exhaustion proofs are committed as follow-up"); the survey's claim level is now "candidate dimensions" rather than "confirmed extensions". F3 (the formal block-by-block exhaustion proof for rho_agg-proj) remains tracked as follow-up. This is the correct epistemic posture for an exploratory single-rater survey.

### S3: W3 (84-MR PWR corpus provenance) is now front-loaded and the external-transfer commitment is concrete
§subsec:reactor-mapping at L517–518 opens with a Provenance paragraph that states verbatim: "The reactor-physics MetaPattern catalogue compared against here was distilled by the present authors from the standard PWR-physics literature as their own prior inductive work; the underlying 84-MR PWR corpus (supplementary S2) is the authors' own catalogue, not an external corpus drawn from an unrelated team. The relationship reported in this section is therefore best read as a test of *internal vocabulary coherence*." This is the disclosure I asked for in Round 2 W3. `tab:future-work` item (j) at L2380 commits to "External-transfer test on an independently-authored reactor-physics MR corpus: apply NOETHER's eight-block decomposition to a PARCS V&V suite catalogue or an IAEA-TECDOC-class catalogue authored by a team unconnected to the present authors". The parallel commons-math cross-codebase pilot (b.cm) at L2368 is concretely reported with n=3 SUTs, 5 Set N MRs, 77 mutants, Wilson 95% CI on G-block kill rate [13.8%, 50.0%], and D2 stratum kill rate 2/29=6.9%, with explicit underpowered disclosure.

### S4: W4 (pooled-headtohead inconsistency with McNemar) is now D1-dominance-led
§subsec:pooled-headtohead at L1601–1619 now opens with a bold sentence: "**On the algebra-disrupting D1 stratum at GenMorph's published 30-min GAssert budget, Set~N is dominated by Set~G in the aggregate (McNemar exact two-sided $p = 0.0043$ pooled and $p = 0.019$ on D1 only, $n = 62$ post-equivalent-mutant exclusion).**" The follow-on sentence reads "The paper does not assert head-to-head superiority on D1". This is the alignment I asked for in Round 2 W4: the §6.6 head-to-head body now reflects the statistical reality of McNemar p=0.0043. The framework's contribution on D1 is correctly re-framed as (i) algebraic derivability, (ii) per-block complementarity (Set G alone kills 15 D1 mutants Set N misses, Set N alone kills 4 D1 mutants Set G misses), and (iii) an out-of-scope D2-stratum framework prediction that no inductive baseline can derive ex-ante. The Round 2 "competitive parity" framing of the head-to-head body is gone.

### S5: W5 (external validity beyond Java methods / Lie-group families) is correctly bounded at the Conclusion
§9 Conclusion at L2695 reads: "the framework's mechanism applies unchanged once a new program family's algebra has been specified, tested within the framework's scope precondition on three structurally distinct operator-algebraic skeletons (Boltzmann reactor physics, equivariant ML, relational query optimisers). Cross-domain empirical superiority and team adoption by PWR-simulator V&V groups, equivariant-ML testing teams, or database-optimiser test groups are open follow-up questions; the present paper establishes the structural transferability of the construction mechanism, not adoption outcomes on each domain." The §subsec:empirical-threats External validity paragraph at L2454 likewise scopes external validity to (i) algebraic reach and (ii) substrate generalisation, with the commons-math pilot reported as scope-internal generalisation and explicit underpowered framing.

### S6: PWR physics in §subsec:negative-pwr / Appendix C.6 is intact and remains a load-bearing strength
I re-verified the six PWR-physics items I checked in Round 2:
- Definition `def:drho-exact` at L941–948 uses the positive-convention 1/k_eff form correctly.
- The three-mechanism MTC decomposition at L1010–1018 tracks Stacey §3.4 verbatim: (a) reduced moderation (negative), (b) boron poison evacuation (positive, proportional to C_B, vanishes as C_B → 0), (c) spectrum hardening + U-238 resonance enhancement (negative, Doppler-weighted, significant for MOX / high-enrichment).
- GDC 11 / 10 CFR 50 Appendix A reference at L1027 is correctly cited via `NRC10CFR50AppA`.
- ANS 19.6.1 reference at L1027 is correctly placed in the engineering-significance paragraph for the MTC-vs-boron curve.
- HFP / ARO regime distinction at L1008 is correctly carried; the HZP startup-physics-testing caveat is correctly demoted as a non-power-operation regime.
- The two-regime treatment of Delta_AB at L963 (positive shadowing 50–500 pcm adjacent; anti-shadowing 5–20 pcm distant) is calibrated to real Westinghouse 4-loop and EPR measurements.
- The 5-pcm tolerance for rho_nonadd and the 0.01 pcm/°F/ppm tolerance for rho_MTC-bor remain physically defensible against cycle-reload qualification noise floors.
- The C.6.1 eight-block proof (L2947–2996) cleanly exhausts $\mathcal{D}(\mathcal{A}_{\mathrm{PWR}})$; the three obstructions O1–O3 (operator-spectrum output not in Y; homomorphism-failure of d_rho; configuration-indexed adjoint structure on T*) are correctly identified and pairwise distinct.

No physics errors were introduced in the Round 2 revisions.

### S7: A_equi gauge-bundle counterexample remains mathematically correct
§subsec:third-domain at L903–904 and `theory/equi_thm1prime_search.md` §3.2 (L125–195) correctly distinguish "global G-action" from "local fibre-wise H-action on tangent planes T_p M via a gauge field g in C(M, H)". The cocycle compatibility requirement and the parallel-transport transition function g_{p→q} are correctly invoked. The single-block Translate cannot enumerate sections of a principal H-bundle because Definition 4 enumerates the orbit of a single g in G on a base x_0, not a function-valued parameter. Cohen 2019 (icosahedral CNN) and Haan 2020 (general 3-D mesh) are cited correctly, and the icosahedral case is correctly described as "a restricted but still bundle-non-trivial instance" while the general 3-D mesh case is identified as irreducible to single-group orbits — which is the right mathematical reading. The product-group counterexample rho_compose (Satorras 2021 EGNN) is correctly distinguished as a different obstruction (SO(3) × S_n joint action) that the gauge-bundle pi-template does not absorb, and vice versa. The pairwise-independence claim across the two equi-side dimensions is sound at the inspection level the paper asserts.

---

## Weaknesses

### W1' (residual): "competitive parity" survives at §subsec:empirical-threats paragraph (c) and contradicts the §subsec:pooled-headtohead opening
**Problem.** L2158–2162 (§subsec:empirical-threats paragraph (c) "Sample size") reads:

> n = 70 across 10 SUTs is underpowered for a paired head-to-head verdict at α = 0.05; the §subsec:pooled-headtohead reading is **reframed as competitive parity rather than superiority**. The L*-blindness test is on n = 44 across 6 SUTs admitting an L_scale MR ...

But §subsec:pooled-headtohead (L1601–1607) now opens with:

> On the algebra-disrupting D1 stratum at GenMorph's published 30-min GAssert budget, **Set N is dominated by Set G in the aggregate** (McNemar exact two-sided p = 0.0043 pooled and p = 0.019 on D1 only, n = 62 post-equivalent-mutant exclusion).

"Set N is dominated by Set G with McNemar p = 0.0043" and "competitive parity" are logically incompatible. A careful reviewer of an industrial V&V audit would catch this in 30 seconds: it is the exact rhetorical move my Round 2 W4 flagged as the headline problem. The body of §subsec:pooled-headtohead has been correctly revised, but L2161–2162 was not synchronised, presumably because the revision touched §subsec:pooled-headtohead directly without grep-checking downstream cross-references to that reading.

**Why it matters.** The Threats-to-validity section is read by reviewers and downstream readers as the authors' self-assessment of evidence quality. When the threats section says "the reading is competitive parity" while the body says "Set N is dominated", a reader who only reads the threats section comes away with a misleading impression. In a real submission cycle, a careful AE re-read of §subsec:empirical-threats would mark this as a contradiction; if the contradiction reaches the final published version, a citing author quoting "competitive parity" from §subsec:empirical-threats could be accused of misrepresenting the head-to-head finding. This is a credibility hygiene issue, not a structural one.

**Suggestion.** One-line edit at L2161–2162: replace "the §subsec:pooled-headtohead reading is reframed as competitive parity rather than superiority" with something like "the §subsec:pooled-headtohead reading is reframed as Set G's aggregate D1 dominance (McNemar p = 0.0043) rather than a competitive-parity claim" or, more conservatively, "the §subsec:pooled-headtohead body acknowledges Set G's aggregate D1 dominance (McNemar p = 0.0043 pooled, p = 0.019 on D1); the framework's substantive contribution on the head-to-head substrate is read as per-block complementarity and out-of-scope D2-stratum prediction, not as superiority on the aggregate kill rate." Either phrasing eliminates the contradiction without changing the substantive verdict.

**Severity.** Minor.

### W2' (residual): the §subsec:case-study "Approximate-parity-at-lower-cost" paragraph (L2322) uses "parity" in a non-contradicting but adjacent sense — flag-only
The paragraph at L2322–2354 reads "Approximate-parity-at-lower-cost reading (H3a.3 verdict)" and concludes "comparable within-scope per-block detection at lower amortised generation cost". This use of "parity" is on the per-block T* and L* axes (not on the aggregate D1) and explicitly defers to Set G's aggregate D1 dominance at L2347–2349 ("does not overturn Set G's aggregate dominance on the D1 stratum, which is acknowledged at the head of §subsec:pooled-headtohead"). The qualifier is correct and the claim is bounded, so this is not contradictory in the same sense as W1'. I flag it only because the word "parity" appears in two different scopes (aggregate-D1 parity, which is now contradicted by McNemar p=0.0043, and per-block T*/L* parity, which is the cost-axis H3a.3 verdict) — readers may not always carry the scope qualifier across the two paragraphs. A defensive edit at L2322 could replace "Approximate-parity-at-lower-cost" with "Per-block-complementarity-at-lower-cost", which has the same content without re-using the now-loaded "parity" vocabulary. **Not blocking**; severity Minor.

### W3' (residual, post-Round-2 follow-up): the F3 formal proof (rho_agg-proj not single-Translate-derivable from B*_rel) remains tracked but unexecuted
`theory/rel_thm1prime_search.md` F3 at L215–219 is correctly tracked as follow-up. The §subsec:third-domain text at L904 is now appropriately worded ("pairwise independence is asserted by inspection rather than by formal exhaustion proof, and full per-dimension exhaustion proofs are committed as follow-up"). My Round 2 W2 third bullet (provide the C.6-style block-by-block exhaustion proof for rho_agg-proj) is therefore acknowledged as follow-up rather than executed in-paper. This is acceptable for the present submission given the proof obligation is honestly declared, but it does mean that the rel-side "ten Translate-extension dimensions" count rests on three rel-side dimensions whose Theorem-1' falsification status is candidate-level rather than proved. The paper handles this honestly; readers who care about formal-proof status get the right signal.

**Severity.** Acknowledged-follow-up rather than weakness. No action required.

---

## W1–W5 Resolution Status

| Weakness | Round 2 Severity | Resolution at `ceac6ed` | Status |
|---|---|---|---|
| W1: Three-domain claim asymmetric (only 1 empirically tested) | Major | Abstract + §1 C4 qualified as "structural transferability at algebra-skeleton level not cross-domain empirical superiority"; §3 `rem:domain-out-of-scope` added (L345–355); §9 Conclusion (L2695) closes the loop | **FULLY_RESOLVED** |
| W2: Wang2024QED bib + single-rater A_rel survey | Major | Bib corrected to Wang/Pan/Cheung (`NOETHER_paper.bib` L286–292); F1 resolved 2026-05-15 in `rel_thm1prime_search.md` L208–211; survey scope explicitly disclosed; F3 formal-proof obligation tracked | **FULLY_RESOLVED** (bib + scope) / **PARTIALLY_RESOLVED** (single-rater survey remains, F3 deferred) |
| W3: 84-MR PWR corpus is authors' own prior work | Major | §subsec:reactor-mapping L517–518 leads with Provenance paragraph identifying corpus as authors' own; `tab:future-work` (j) at L2380 commits external-transfer test on PARCS V&V / IAEA-TECDOC | **FULLY_RESOLVED** |
| W4: §6.6 head-to-head "competitive parity" vs McNemar p=0.0043 | Major | §subsec:pooled-headtohead opening bold sentence (L1604–1607) leads with Set N is dominated, McNemar p=0.0043 pooled + p=0.019 D1; framework contribution re-framed as algebraic derivability + per-block complementarity + D2 boundary | **FULLY_RESOLVED** in body / **PARTIALLY_RESOLVED** at §subsec:empirical-threats (c) L2161–2162 where residual "competitive parity" wording survives — see W1' above |
| W5: External validity beyond Java methods / Lie-group / self-adjoint / time-reversal families | Major | §3 `rem:domain-out-of-scope` enumerates web apps / RLHF / distributed consensus / compiler-internal; §9 Conclusion (L2695) notes team adoption as open follow-up | **FULLY_RESOLVED** |

---

## Round 3 R3 New Concerns (post-Round-2 revisions)

### N1: PWR physics accuracy in §subsec:negative-pwr / Appendix C.6
**Verdict: No errors introduced.** Stacey §3.4 three-mechanism MTC decomposition is preserved verbatim at L1010–1018. GDC 11 / 10 CFR 50 App A is correctly cited at L1027. ANS 19.6.1 is correctly placed at L1027 for the MTC-vs-boron curve. HFP/ARO regime distinction at L1008 is intact. The 5-pcm and 0.01 pcm/°F/ppm tolerances remain calibrated to cycle-reload qualification noise floors. The C.6.1 eight-block proof exhausts $\mathcal{D}(\mathcal{A}_{\mathrm{PWR}})$ correctly and the O1–O5 obstructions are pairwise distinct. The two-regime treatment of Delta_AB (positive shadowing 50–500 pcm adjacent; anti-shadowing 5–20 pcm distant) is correctly bounded by Stamm'ler & Abbate Ch. 6 magnitudes.

### N2: A_equi gauge-bundle counterexample (rho_gauge with bundle-section, Cohen 2019)
**Verdict: Mathematically correct.** The §subsec:third-domain description at L903–904 and `theory/equi_thm1prime_search.md` §3.2 correctly identify the bundle-section pi-template parametrised by a gauge field $\mathbf{g} \in \mathcal{C}(M, H)$ as the structural obstruction, distinguish it from a global G-action, invoke the cocycle compatibility / transition function $g_{p \to q}$ correctly, and cite Haan 2020 as the secondary witness on general 3-D meshes. The pairwise independence of rho_gauge and rho_compose (product-group SO(3) × S_n) is correctly asserted by inspection: a product-group pi does not absorb a gauge-bundle section and vice versa. No mathematical errors.

### N3: A_rel survey — five candidate dimensions vs Calcite/CockroachDB rewrite-rule literature
**Verdict: Correctly identified, single-rater scope honestly disclosed.** `theory/rel_thm1prime_search.md` §3 (L99–123) classifies 12 representative Calcite test names into (a) single-block-derivable / (b) multi-block / (c) out-of-vocabulary. The (b)-class candidates (rho_agg-proj, constant-key, decorrelate, NULL three-valued logic, project-aggregate transposition) correctly identify three net rel-side dimensions (aggregate-as-algebra, constraint-aware equivalence, three-valued logic). Aggregate-as-algebra is consistent with what monad-based aggregation semantics would require (QED's "uninterpreted-function" treatment vs. a monoid/semilattice algebra is a real semantic gap that the Calcite literature has discussed). Constraint-aware equivalence is consistent with Calcite's integrity-constraint-driven rewrites (Decorrelate, AggregateConstantKey). NULL three-valued logic is consistent with Codd's SQL three-valued semantics and Calcite's NULL-propagation rules. None of these classifications is unreasonable; the limitation (single rater, no QED execution, no inter-rater agreement) is now explicitly disclosed at L173–190 of `rel_thm1prime_search.md` and at §subsec:third-domain L904. F3 formal exhaustion proof remains tracked as follow-up.

### N4: Cross-codebase Apache Commons Math pilot (n=3 SUTs, 77 mutants, D2 prediction 2/29=6.9%)
**Verdict: Reported with proper underpowered caveats.** `tab:future-work` item (b.cm) at L2368 reports n=3 SUTs, 5 Set N MRs, 77 mutants, G-block kill rate 6/21=28.6% Wilson 95% CI [13.8%, 50.0%], D2 stratum 2/29=6.9% Wilson 95% CI [0.012, 0.221], with explicit "underpowered for α = 0.05 hypothesis testing" disclosure. §subsec:empirical-threats External validity at L2454 reports the L*=0 finding correctly as a framework structural prediction rather than a measurement gap, with the bilinearity-symmetric-propagation argument correctly explained. Set G is correctly reported as structurally N/A on Maven-resolved substrates (head-to-head against GenMorph deferred to (b) as a harness-extension task). The replication is correctly framed as descriptive evidence consistent with the framework's scope-internal generalisation prediction, not as inferential confirmation. This is CLAUDE.md C6 compliant.

---

## Detailed Suggestions for Authors

### Required (Minor)
1. **L2161–2162**: replace "the §subsec:pooled-headtohead reading is reframed as competitive parity rather than superiority" with wording that does not contradict §subsec:pooled-headtohead's opening bold sentence (McNemar p = 0.0043 D1 dominance). Suggested: "the §subsec:pooled-headtohead body acknowledges Set G's aggregate D1 dominance (McNemar p = 0.0043 pooled, p = 0.019 on D1); the framework's substantive contribution on the head-to-head substrate is read as per-block complementarity and out-of-scope D2-stratum prediction, not as superiority on the aggregate kill rate."

### Recommended (Polish, not blocking)
2. **L2322** (paragraph title "Approximate-parity-at-lower-cost reading"): consider renaming to "Per-block-complementarity-at-lower-cost reading" or "Per-block-T*-edge-at-lower-cost reading" to avoid re-using the "parity" vocabulary that is now contradicted at the aggregate-D1 scope by §subsec:pooled-headtohead's opening. The paragraph's content is correct; only the section heading carries the word that may confuse a fast reader.
3. **`tab:future-work` (j)** (L2380, external-transfer test on PARCS V&V / IAEA-TECDOC): consider adding an explicit "≥ N MR corpus required for the external Fleiss-κ replication to reach decisive evidence" target, so the follow-up is operationalisable rather than open-ended. (Round 2 W3 suggested this as well; the present formulation says "≈ 1 month corpus-access + classification" but does not commit to a minimum N for the κ measurement.)
4. **F3 follow-up** (`theory/rel_thm1prime_search.md` L215–219): the formal block-by-block exhaustion proof for rho_agg-proj — analogous to Appendix C.6 — would close the only remaining structural-completeness gap on the rel side. The current "asserted by inspection" status is honest but downgrades the "ten Translate-extension dimensions" count from "ten with five proved + five candidate" to "ten with five proved + five inspection-only". A 1–2 page formal proof in a future supplementary would lift the candidate-level rel-side three to proved-level.

### Optional
5. The §subsec:third-domain "the three algebra-survey artefacts ... identify a total of ten Translate-extension dimensions across the three algebras" framing at L904 is correctly bounded by the inspection-vs-formal-proof split, but a reader who quotes "ten dimensions" without the qualifier may overclaim. Consider adding "(five proved, five candidate at inspection level)" inline at L904 to make the qualifier travel with the count.

---

## 250-Word Round 3 Decision Summary

**Decision: Minor Revision.**

The Round 2 Major-Revision package addresses W1–W5 substantively. **W1 FULLY_RESOLVED**: abstract + §1 C4 now qualify three-domain claim as algebra-skeleton-level structural transferability, not cross-domain empirical superiority; §3 `rem:domain-out-of-scope` (L345) enumerates web apps / RLHF / distributed consensus / compiler-internal as structurally absent; §9 Conclusion (L2695) notes team adoption as open follow-up. **W2 RESOLVED on bib, SCOPE-BOUNDED on survey**: `Wang2024QED` correctly Wang/Pan/Cheung (bib L286, CrossRef-verified), F1 resolved 2026-05-15; single-rater Calcite survey limitation now explicitly disclosed, F3 formal-proof tracked as follow-up. **W3 FULLY_RESOLVED**: §subsec:reactor-mapping L517 Provenance paragraph identifies 84-MR corpus as authors' own; `tab:future-work` (j) commits external-transfer test on PARCS V&V / IAEA-TECDOC. **W4 BODY RESOLVED, RESIDUAL at L2161**: §subsec:pooled-headtohead opens with bold "Set N is dominated, McNemar p=0.0043 pooled, p=0.019 D1"; but §subsec:empirical-threats (c) L2161–2162 still says "competitive parity", contradicting the body. One-line edit needed. **W5 FULLY_RESOLVED**: external validity correctly scoped to (i) algebraic reach + (ii) substrate generalisation.

**New concerns: none structural.** PWR physics in §subsec:negative-pwr / Appendix C.6 intact (Stacey §3.4, GDC 11, ANS 19.6.1, HFP/ARO regime); gauge-bundle counterexample mathematically correct (Cohen 2019, Haan 2020); A_rel five dimensions correctly identified; commons-math pilot honestly underpowered (CLAUDE.md C6 compliant).

**Score: 82/100.** One required Minor edit at L2161–2162; three optional polish items. The framework's structural-transferability claim and PWR negative instantiation are now well-bounded and load-bearing. Ready for Minor Revision and re-review.

---

## IRON RULES Compliance
- READ-ONLY: confirmed; no edits to `NOETHER_paper.tex`, `NOETHER_paper.bib`, or `theory/*.md`.
- Specific citations: §3 `rem:domain-out-of-scope` L345; abstract L78; §1 C4 L137; §subsec:reactor-mapping L517; `tab:future-work` (j) L2380, (b.cm) L2368; §subsec:pooled-headtohead L1601–1619; §subsec:empirical-threats (c) L2161–2162; §9 Conclusion L2695; Appendix C.6.1 L2947–2996; `NOETHER_paper.bib` L286–292; `theory/rel_thm1prime_search.md` L15–16, L191–194, L208–211; `theory/equi_thm1prime_search.md` §3.2 L125–195.
- Physics references: Stacey 2007 §3.4 at L991, L1010; Lamarsh & Baratta §8.3 at L999; Bell & Glasstone §6.1, §6.3, §10.4 at L930, L966, L980; Lewis & Miller §4.2, §4.4 at L930, L966, L980; Stamm'ler & Abbate at L960, L963, L980; NRC RG 1.77 at L915, L980; 10 CFR 50 App A GDC 11 at L1008, L1027; ANS 19.6.1 at L1027. All correctly placed.
- Honest scoring: revision effort substantial but not rewarded if residual inconsistencies remain; W1' at L2161–2162 is the only required edit, downgraded to Minor not Major because it is a one-line synchronisation rather than a structural defect.
- R3 scope: cross-domain accuracy (PWR + equi + rel), external validity (scope precondition + commons-math), structural transferability claim (abstract + §1 + §9).
