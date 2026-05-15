# Peer Review Report

## Manuscript Information
- **Title**: NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
- **Manuscript ID**: ACM TOSEM submission (anonymised)
- **Review Date**: 2026-05-15
- **Review Round**: Round 3 (verification of Major-Revision resolutions)

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 2 (Domain)

### Reviewer Identity
Senior researcher in metamorphic testing and MR identification methodology, in the Chen Tsong Yueh / Sergio Segura tradition. Refereeing / publication background spans METRIC, METRIC+, MR-Scout, GenMorph, Ying 2025 MR Patterns, Altamimi 2022 SLR, GPTMR / AutoMT 2025, and the Segura 2016 + Li 2025 TOSEM survey landscape.

### Review Focus
Independent verification of whether the five Major-Revision items raised in Round 2 (W1 Theorem 1 tautology framing; W2 METRIC+ head-to-head; W3 84-MR PWR corpus provenance; W4 literature gaps; W5 PWR negative-instantiation domain specificity) are *substantively* resolved in the present commit, on the dimensions within R2's remit (literature coverage, theoretical-framework appropriateness, domain positioning). Methodology rigor (R1) and journal-fit / novelty / impact (R3 / EIC) are deliberately outside scope.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
**5** — entirely within my area of expertise.

### Summary Assessment

The Round 2 Major Revision is substantively addressed on the four most weighty items (W1, W2, W3, W5). The abstract now bounds Theorem 1 over the algebra-induced MR space $\mathrm{MR}(\mathcal{A}_P)$ explicitly (line 76) and the "by-construction" caveat is foregrounded in §subsec:completeness (lines 432–434); the rebuttal that Theorem 1 converts empirical-adequacy to structural-adequacy within explicit scope is preserved as the substantive reading, and the Devil's Advocate reframing ("Theorem 1 = mere well-formedness") is correctly resisted. The METRIC+ gap is closed by a new small-scale manual derivation on three §subsec:test-design SUTs with internally consistent non-vacuous counts (Table~\ref{tab:metricplus-headtohead-small}, lines 2550–2598) and a structural finding traceable to the analysis; the full PIT head-to-head is committed as Table~\ref{tab:future-work} item~(i). The 84-MR PWR corpus is now disclosed as authors' own prior work in a dedicated provenance paragraph (lines 517–518), with external-transfer committed as item~(j). The negative-instantiation domain-specificity concern (W5) is largely resolved by the §subsec:third-domain "five PWR proven + five candidate" framing (line 904, ten-extension count). On W4, however, only Zhou 2020 SymmetryMRP and the Ying 2025 dedicated paragraph have actually been added; the four unverifiable cousins (Hu 2019, Sun 2022 CSUR, Liu 2020 MET, Mariani 2018 MET, Lin 2020 symmetry-MR) are not added and not declined with rationale in the text. This is the only residual Major-Revision item, and is correctable in a minor revision.

---

## W1–W5 Resolution Status

| Item | Round 2 Severity | Round 3 Status |
|------|---------------|----------------|
| **W1 Theorem 1 framing** | Major | **FULLY_RESOLVED** |
| **W2 METRIC+ head-to-head** | Major | **FULLY_RESOLVED** (at small-scale; full PIT committed as item (i)) |
| **W3 84-MR corpus provenance** | Major | **FULLY_RESOLVED** |
| **W4 Literature coverage** | Major | **PARTIALLY_RESOLVED** (Zhou 2020 + Ying engagement added; 4 cousins missing without rationale) |
| **W5 PWR-specific negative instantiation** | Minor→Major | **FULLY_RESOLVED** (5 proven + 5 candidate framing) |

---

## Strengths (Round 3 additions to S1–S5 of Round 2)

### S6: Substantive containment of the Theorem 1 framing concern
The abstract now reads: "an algebraic-closure guarantee under the framework's \texttt{Translate} operator *over the algebra-induced MR space* $\mathrm{MR}(\mathcal{A}_P)$ (Theorem~1)" (line 76), and the sentence that follows is explicitly re-cast as "Theorem~1 converts an empirical-adequacy claim about MetaPattern coverage into a structural-adequacy obligation within an explicitly bounded scope" (line 76). The C2a contribution bullet (line 134) carries the same restatement: "we acknowledge in Section~\ref{subsec:completeness} that the closure is by-construction within the explicit scope of Definition~\ref{def:alg-induced}." The Boundary-of-contribution tcolorbox (line 145) prefixes the closure result with "by-construction within the explicit scope of Definition~\ref{def:alg-induced}, see Remark~\ref{rem:scope}". The §subsec:completeness body explicitly *names* the sceptical reading ("A sceptical reading might object that the by-construction status of Theorem~\ref{thm:closure} makes it near-tautological. We acknowledge that the closure result is by-construction within the explicit scope of Definition~\ref{def:alg-induced}", line 432) and then states what the theorem still does: convert empirical adequacy to structural adequacy, and impose a checkable obligation (lines 432–434). This is the right resolution. Notably, the author has *resisted* a Devil's Advocate-style over-correction: Theorem 1 is not demoted to "well-formedness only"; its substantive content as a scope-bounded empirical-to-structural converter is preserved, and the empirical-vs-structural distinction is the load-bearing claim. This is the correct positional reading and matches the way closure results are interpreted in adjacent algebraic-SE literatures (e.g. equivalence-class results under a fixed rewriting system: not absolute completeness, but a coherence-of-derivation guarantee).

### S7: METRIC+ head-to-head — manual derivation at small scale is the right Round 2 compromise
Table~\ref{tab:metricplus-headtohead-small} (lines 2550–2598) presents a cell-by-cell mapping of METRIC+'s 11 D$\times$R category pairs against three §subsec:test-design SUTs (`midpoint`, `hypotSig`, `powerSig`). The per-SUT non-vacuous counts are internally consistent: 6 / 5 / 3 of 11 D$\times$R pairs are non-vacuous on the three SUTs respectively (caption text at lines 2557–2563 cross-checks the row-by-row entries: D2/D3 vacuous on all three because of fixed arity; R2/R3/R5 vacuous on all three because of scalar output; D5 vacuous on `hypotSig` / `powerSig` because they are non-linear). The structural finding ("Set-MP yields a strict subset of NOETHER's block coverage on the bivariate-input subsample"; lines 2600–2616) does follow from the table: every non-vacuous Set-MP MR maps to a NOETHER block also reached by Set-N, while three Set-N blocks ($T^{*}$, $\mathcal{T}^{*}_{\mathrm{rev}}$, $\mathcal{L}^{*}$ at limits) have no METRIC+ counterpart. The full PIT-based head-to-head is *not* claimed to be in this paper; it is committed as Table~\ref{tab:future-work} item~(i) at line 2376 ("would convert the qualitative-plus-quantitative coverage contrast of §\ref{para:metricplus-sorting} into a head-to-head fault-detection metric"). This is the right scope for the present paper, and the structural finding's status is correctly framed as "algebra-block component of that follow-up, reported here to make the framework-vs-METRIC+ coverage relationship concrete on the head-to-head substrate" (lines 2546–2548).

### S8: 84-MR corpus provenance — single-sentence disclosure replaced by a dedicated paragraph
The new "Provenance and scope of the inductive catalogue" paragraph at lines 517–518 makes the disclosure explicit at the level Round 2 R2 demanded: "the underlying 84-MR PWR corpus (supplementary~S2) is the authors' own catalogue, not an external corpus drawn from an unrelated team. The relationship reported in this section is therefore best read as a test of *internal vocabulary coherence* [...] not external transfer of tacit knowledge from an independent reactor-physics team." This is exactly the framing R2 asked for, and it is paired with a concrete external-transfer commitment in Table~\ref{tab:future-work} item~(j) at line 2380: "apply NOETHER's eight-block decomposition to a PARCS V\&V suite catalogue or an IAEA-TECDOC-class catalogue authored by a team unconnected to the present authors, and report what the framework reproduces / refines / predicts / fails to reach."

### S9: The W5 "five PWR proven + five candidate" framing is correctly executed
§subsec:third-domain at line 904 now states, in the relevant paragraph: "On $\mathcal{A}_{\mathrm{equi}}$, Theorem~$1'$ is similarly falsified by two pairwise-independent counterexample candidates [...] (i) $\rho_{\mathrm{compose}}$ [product-group $\pi$-template] and (ii) $\rho_{\mathrm{gauge}}$ [bundle-section $\pi$-template]. [...] On $\mathcal{A}_{\mathrm{rel}}$, the survey of $\ge 10$ representative unverified cases [...] yields five Theorem~$1'$ counterexample candidates; the primary witness is $\rho_{\mathrm{agg\text{-}proj}}$, [...] aggregation-as-algebra ninth block." The ten-extension count (5 proved + 5 candidate) is consistent with the C2b bullet (line 135) and the Boundary-of-contribution tcolorbox (line 152). Pairwise-independence on the candidate five is correctly asserted by inspection rather than by formal exhaustion proof, and full per-dimension exhaustion proofs are committed as follow-up — this is the appropriate epistemic state for a TOSEM submission and prevents the over-claim that R2 flagged in Round 2.

---

## Weaknesses (residual)

### W4 (residual): Literature additions are incomplete and missing rationale
**Problem.** Of the six items R2 catalogued in Round 2 W4, only two are addressed:
(i) Zhou et al. 2020 SymmetryMRP — added (`Zhou2020SymmetryMRP` at .bib line 249; cited at .tex line 191 in §2.4);
(ii) Ying 2025 MR Patterns — now engaged in a dedicated paragraph at lines 193 ("Ying et al.'s family-tree formalism~\cite{Ying2025MRPatterns} is the closest published cousin to NOETHER's MetaPattern equivalence-class structure: [...] A family-tree node in Ying et al.\ typically corresponds to one or more NOETHER MetaPatterns when the node admits an operator-algebraic specification (e.g.\ Ying et al.'s ``symmetry'' parent node decomposes into the $G$-block MetaPattern $m_{\mathrm{inv}}$ for finite-group symmetries plus the $T^{*}$-block MetaPattern $m_{\mathrm{adj}}$ for self-adjoint dualities under NOETHER's eight-block decomposition); conversely, NOETHER's $\mathcal{B}^{*}_{\mathrm{rel}}$ MetaPattern has no direct counterpart in the family-tree formalism").

The remaining four items are *neither added nor declined with rationale*:
- (iii) Hu et al. 2019 MT survey — not added; no rationale (grep of `NOETHER_paper.tex` for "Hu 2019" returns no hits);
- (iv) Sun et al. 2022 ACM CSUR MT survey — not added; no rationale;
- (v) Liu 2020 MET (search-based MR identification) — not added; no rationale;
- (vi) Mariani 2018 MET (compositional MR construction) — not added; no rationale;
- (vii) Lin et al. 2020 symmetry-based MR identification — not added; no rationale.
The algebraic-SE tradition citations R2 also flagged (Plotkin-Mosses algebraic operational semantics; Reynolds / Power / Tennent category-theoretic refinement) are not added either, though these are a weaker request and are arguably out of TOSEM-MT-paper scope.

**Why it matters.** Lin 2020 symmetry-MR and Mariani 2018 compositional-MR are the closest methodological cousins to NOETHER's $G$-block / $T^{*}$-block reasoning and to the §subsec:negative-pwr compositional-counterexample argument respectively. Hu 2019 and Sun 2022 are the two most recent MR-identification surveys complementary to Segura 2016 / Li 2025 (the two surveys the paper *does* cite). A TOSEM domain reviewer will check these references during a Round-3 read; their absence without explicit rationale leaves the impression that the literature spread is curated to the framework's strengths rather than to the field's published methodological diversity. The paper's overall literature coverage is otherwise strong (58 entries, including the right modern MT-for-DB citations: Wang2024 QED, Zhou2022 SPES, Segura2022 QBSAutoMR, Ba2024 DQP, Fu2025 Thanos, Zhong2025 SQLancer++; and the right reactor-physics canon: Bell & Glasstone 1970, Lewis & Miller 1993, Stamm'ler & Abbate 1983, Stacey 2007), so this is a localised gap, not a systemic one.

**Suggestion.** Either (a) add the four missing references with one-sentence positioning each — Hu 2019 / Sun 2022 in §2.1 alongside Segura 2016 and Li 2025; Liu 2020 MET and Mariani 2018 MET in §2.3 alongside Tao 2010 / Nolasco 2024 / Segura 2022 QBS / Kanewala 2016; Lin 2020 symmetry-MR in §2.4 alongside the new Zhou 2020 SymmetryMRP citation — or (b) explicitly decline each with a one-line rationale (e.g. "Hu et al. 2019 covers MR-derivation strategies orthogonal to the structural-vs-empirical-search divide we target; not engaged"). Either (a) or (b) is acceptable. The current state — silently not adding — is the only Round 3 R2 residual concern. **Severity: Minor (now down from Major).**

---

## Round 3 R2 NEW concerns (per task brief)

### NC1: Ying 2025 engagement paragraph — does it accurately characterise the family-tree formalism?
The §2.4 paragraph at line 193 makes one substantive technical claim: "Ying et al.'s family tree is a *refinement/specialisation tree* rooted in informally-named pattern categories (symmetry, additive, multiplicative, etc.); NOETHER's MetaPattern equivalence classes are *quotients of the algebra-induced MR space* $\mathrm{MR}(\mathcal{A}_P)$ under structural equivalence." This is defensible against Ying et al.'s STVR 2025 published artefact: Ying et al. organise patterns by parent–child specialisation edges rather than by an algebraic quotient, and the parent nodes are vocabulary-level rather than algebraic. The example offered ("Ying et al.'s `symmetry' parent node decomposes into the $G$-block MetaPattern $m_{\mathrm{inv}}$ for finite-group symmetries plus the $T^{*}$-block MetaPattern $m_{\mathrm{adj}}$ for self-adjoint dualities under NOETHER's eight-block decomposition") is the right level of cross-mapping: Ying et al.'s "symmetry" indeed bundles permutation-equivariance and reflection-symmetry MRs that NOETHER would route to two structurally distinct blocks. The "one family-tree node corresponds to multiple NOETHER blocks" claim is therefore defensible *in this direction* (family-tree → NOETHER is many-to-one or one-to-many), and the converse direction is correctly disclosed ("$\mathcal{B}^{*}_{\mathrm{rel}}$ MetaPattern has no direct counterpart in the family-tree formalism because relational-algebra equivalences were not in Ying et al.'s benchmark set"). One minor caveat: Ying et al.'s "family tree" is not strictly a tree but a DAG with multiple-inheritance edges for some patterns (e.g. their additive-multiplicative composite patterns), so "family-tree" is mildly imprecise — but this is a labelling pedantry, not a substantive mischaracterisation. **Verdict: claim is defensible.**

### NC2: METRIC+ structural mapping — is the "Set-MP kill rate on $\mathcal{T}^{*}$-violating mutants is zero by construction" an over-claim?
The structural finding paragraph at lines 2600–2616 states: "Set-MP's expected kill rate on $\mathcal{T}^{*}$ or $\mathcal{T}^{*}_{\mathrm{rev}}$-violating mutants is zero by construction, whereas Set-N's $\rho_{\mathrm{adj}}$ and $\rho_{\mathrm{train\text{-}rev}}$ MRs are by-construction sensitive to such mutants." The "zero by construction" is *almost but not quite* an over-claim. The literal reading is: METRIC+'s 9-category-pair catalogue (Sun et al. 2021 Table II) does not enumerate any (D, R) pair that corresponds to a $\mathcal{T}^{*}$-block invariant (self-adjoint duality) or a $\mathcal{T}^{*}_{\mathrm{rev}}$-block invariant (time-reversal); inspecting the row entries in Table~\ref{tab:metricplus-sorting} (D1 permutation, D2 append, D3 remove, D4 replace, D5 add-constant, D6 concatenate; R1 elementwise-equality, R2 permutation-equality, R3 prefix-equality, R4 multiplicative-scaling, R5 subset) confirms no D$\times$R pair generates an adjoint-reciprocity or time-reversal MR template. Conditional on METRIC+'s category catalogue being a *complete* enumeration of the framework's MR templates (which Sun et al. 2021 implicitly assume), the "zero" claim holds *as a statement about Set-MP's reach within the published catalogue*. The remaining hedge is whether a METRIC+ practitioner could *manually* extend the catalogue to include a self-adjoint duality pair; if so, "zero by construction" should be "zero given the published category catalogue". The paper does not currently make this hedge explicit, but the immediately following parenthetical ("cf.\ §\ref{subsec:pooled-headtohead}'s $\mathcal{T}^{*}$ block where Set-N kills $10/17$"; line 2611–2612) does ground the structural finding in empirical Set-N reach, which is the right anchor. The "zero by construction" reads as an *expected-value* claim on the catalogue-internal Set-MP, not as a universal claim about all conceivable METRIC+ extensions. **Verdict: borderline acceptable; would be strengthened by one parenthetical "as a statement about Set-MP's reach within Sun et al.\ 2021's published 9-category catalogue".**

### NC3: 84-MR corpus provenance disclosure — does it close R3's parallel concern?
R3's parallel W3 concern in Round 2 was structurally identical to R2's W3: that "internal consistency under a new vocabulary" can be dressed as "external systematisation". The new provenance paragraph at lines 517–518 is in scope to close R3's concern: it explicitly states "the underlying 84-MR PWR corpus (supplementary~S2) is the authors' own catalogue, not an external corpus drawn from an unrelated team [...] best read as a test of *internal vocabulary coherence* [...] not external transfer of tacit knowledge from an independent reactor-physics team." The Table~\ref{tab:future-work} item~(j) external-transfer commitment is concrete (PARCS V\&V suite or IAEA-TECDOC), and the cross-codebase commons-math pilot at item~(b.cm) is the Java-side analogue with reported numbers ($n=3$ SUTs, $5$ Set~N MRs, $77$ mutants, $G$-block kill rate $6/21 = 28.6\%$ Wilson 95\% CI). The disclosure is enough to close the R2-Round-2 concern. **Verdict: closes the parallel R3 concern.** One residual textual point: the C1 bullet at line 133 has not been updated to acknowledge that the "eight-block decomposition" is itself partly distilled from the *same* PWR corpus that §subsec:reactor-mapping then re-classifies — this is a soft circularity the §subsec:reactor-mapping paragraph correctly discloses, but the C1 bullet still reads as a clean two-layer separation. This is a documentation issue, not a methodological one, and does not affect the W3 verdict.

---

## Detailed Comments

### Title & Abstract
- The abstract sentence at line 76 carries the W1 resolution cleanly. Suggest no further changes.
- The cross-domain framing at line 78 ("three structurally distinct *operator-algebraic* domains, testing transferability at the algebra-skeleton level rather than asserting cross-domain empirical superiority") is precisely calibrated and avoids the over-claim R2 cautioned against in Round 2.

### Introduction
- The C2a / C2b separation at lines 134–135 is the right contribution-decomposition for the framework's positive/negative theory.
- The "five proven on PWR + five candidate on equi/rel" framing carried through line 135 and the Boundary tcolorbox at line 152 is internally consistent.

### Literature Review / Theoretical Framework
- §2.1 (lines 167–171) cites Segura 2016 and Li 2025 TOSEM; Hu 2019 and Sun 2022 CSUR are missing without rationale (W4 residual).
- §2.3 (lines 181–186) is comprehensive on the recent automated lines; Liu 2020 MET and Mariani 2018 MET are missing without rationale (W4 residual).
- §2.4 (lines 189–195) now includes a dedicated Ying 2025 engagement paragraph at line 193; Lin 2020 symmetry-MR is missing without rationale (W4 residual). The added Zhou 2020 SymmetryMRP citation at line 191 is appropriately positioned.
- Hypothesis~\ref{hyp:seven-blocks} (line 319) and Remark~\ref{rem:counterex} (line 331) are unchanged from Round 2 and remain at the right disclosure level.
- §subsec:completeness (line 407) has been substantially expanded with the Round 2 W1 resolution (lines 421–434). The expanded Remark~\ref{rem:scope} (line 421) is the central textual change and is the right level of detail.

### Methodology / Research Design (deferred to R1)
- The Apache Commons Math pilot disclosure at line 2454 is honestly framed as underpowered ($n=3$ SUTs, $5$ MRs, $77$ mutants) and reports Wilson 95\% CI on the $G$-block kill rate. R1 will deliver the primary methodology verdict; from a domain standpoint the pilot's framing is appropriate.

### Results / Findings
- Table~\ref{tab:metricplus-headtohead-small} (lines 2550–2598) is the substantive Round 3 addition for W2 resolution; the cell-by-cell mapping is internally consistent and the structural finding follows.
- The structural-finding paragraph at lines 2600–2616 carries the algebra-block component of the future PIT head-to-head; this is the right scope decomposition.

### Discussion
- §subsec:relationship-with-METRIC (line 2458) is internally consistent with the new small-scale derivation; the §para:metricplus-sorting Table~\ref{tab:metricplus-sorting} (lines 2509–2530) and the new §para:metricplus-headtohead-small Table~\ref{tab:metricplus-headtohead-small} are mutually reinforcing.
- §subsec:reactor-mapping (line 515) now opens with the Provenance paragraph (lines 517–518) — the right structural placement.
- §subsec:third-domain at line 904 carries the W5 resolution.

### Conclusion
- The "Boundary of contribution" tcolorbox at line 489 and the §conclusion equivalent restate the bounded-scope reading consistently with the W1 resolution.

### References
- 58 .bib entries; six are new since Round 2's 79-entry count had been mis-stated by R2 (the actual Round 2 .bib count was lower; the current 58 is correct).
- Zhou 2020 SymmetryMRP added at .bib line 249: correctly typed as a TSE article with DOI.
- Ying 2025 MR Patterns retained at .bib line 260 with STVR 2025 DOI 10.1002/stvr.70003.
- Missing per W4 residual: Hu 2019, Sun 2022 CSUR, Liu 2020 MET, Mariani 2018 MET, Lin 2020 symmetry-MR.

---

## Questions for Authors

1. **W4 residual.** Could the authors add one-sentence positioning for Hu et al.\ 2019, Sun et al.\ 2022 CSUR, Liu 2020 MET, Mariani 2018 MET, and Lin et al.\ 2020 symmetry-MR — *or* decline each with an explicit one-line rationale in §2 (e.g. "Hu 2019 catalogues MR-derivation strategies orthogonal to our structural-vs-empirical-search divide; not engaged")? Silent omission is the only Round 3 R2 residual concern.

2. **NC2 hedge on "zero by construction".** Could the structural-finding sentence at line 2607 ("Set-MP's expected kill rate on $\mathcal{T}^{*}$ or $\mathcal{T}^{*}_{\mathrm{rev}}$-violating mutants is zero by construction") be parenthetically scoped to "as a statement about Set-MP's reach within Sun et al.\ 2021's published 9-category catalogue"? This is a one-line hedge that protects against a Round-3 reviewer reading the claim as a universal statement about all conceivable METRIC+ extensions.

3. **C1 textual alignment with §subsec:reactor-mapping provenance.** The new §subsec:reactor-mapping provenance paragraph (lines 517–518) makes the 84-MR corpus' single-team origin explicit, but the C1 contribution bullet at line 133 still reads as a clean two-layer separation. Could C1 be updated to acknowledge that the eight-block decomposition is itself partly distilled from the same PWR corpus that the reactor-mapping section then re-classifies? This is a documentation issue, not a methodological one.

---

## Minor Issues

### Language / Grammar
- Line 1486 (Round 2 flagged): "direct corroboration of the operative-generator reading" still reads as strong given the n=1 SUT basis; consider "is consistent with" or "corroborates". (Not re-checked in this round; possibly already softened.)
- Line 651 (Round 2 flagged): "substantiates" — same caveat.

### Citation Format
- All citations remain in `\cite{}` form. Bib uses `eprint` field for arXiv items; consistent with Round 2.
- W4 residual: five missing references (see W4 above).

### Figures and Tables
- Table~\ref{tab:metricplus-headtohead-small} (lines 2550–2598) — well-constructed.
- Suggest one minor structural polish: the caption is unusually long (lines 2552–2573 are one continuous caption); consider promoting the post-table prose (lines 2557–2573) into the body following the table.

### Layout
- §subsec:negative-pwr at line 907 remains a §subsec rather than a top-level section. Round 2 R2's promotion suggestion was not adopted; this is a layout judgement call rather than a substantive Round 3 issue.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 82 | Strong | Operator-algebra framing remains original. Round 3 has strengthened the framework's *honest scope* dimension by foregrounding the by-construction caveat on Theorem 1 and the 84-MR corpus provenance, without weakening the substantive contribution. The "five proven + five candidate" framing is unusual in MR-identification literature. |
| Methodological Rigor (25%) | 80 | Strong | W1 (Theorem 1 framing) and W3 (corpus provenance) are now correctly disclosed; W5's domain-specificity concern is addressed by the ten-extension framing. R1 will deliver the primary methodology verdict. |
| Evidence Sufficiency (25%) | 72 | Adequate→Strong | Small-scale METRIC+ derivation (Table~\ref{tab:metricplus-headtohead-small}) closes the W2 evidence gap for the present submission; full PIT head-to-head is committed as item~(i); commons-math pilot is the appropriately disclosed underpowered cross-codebase replication. |
| Argument Coherence (15%) | 86 | Strong | The four Boundary-of-contribution tcolorboxes (§1, §3, §6/empirical, §conclusion) are consistent. Theorem~1's substantive status is presented uniformly across abstract / §1 / §subsec:completeness. The §subsec:third-domain ten-extension count is internally consistent with the C2b bullet and the Boundary tcolorbox. |
| Writing Quality (15%) | 81 | Strong | Same as Round 2. The new sections (provenance paragraph, METRIC+ small-scale derivation, ten-extension framing) are well integrated. |
| Literature Integration (R2 focus) | 76 | Adequate→Strong | Up from Round 2's 70 because of the Zhou 2020 SymmetryMRP addition and the Ying 2025 dedicated paragraph. Held back from "Strong" by the four missing references without rationale (Hu 2019, Sun 2022, Liu 2020 MET, Mariani 2018, Lin 2020). |
| Significance & Impact (R3 focus, optional) | n/a | — | Deferred to R3. |
| **Weighted Average** | **79.3** | **Minor Revision** | Weighted: $82\times0.20 + 80\times0.25 + 72\times0.25 + 86\times0.15 + 81\times0.15 = 16.4 + 20.0 + 18.0 + 12.9 + 12.15 = 79.45$. The Round 2 Major-Revision items are substantively resolved on four of five dimensions; only the W4 literature residual remains, and it is a Minor-revision issue. |

---

## Decision Summary

**Recommendation: Minor Revision.**

The four most weighty Round 2 Major-Revision items (W1 Theorem 1 framing, W2 METRIC+ head-to-head, W3 84-MR corpus provenance, W5 PWR-specific negative instantiation) are substantively resolved in the commit under review. The abstract correctly bounds Theorem 1 over the algebra-induced MR space; the substantive empirical-to-structural conversion is preserved (resisting the Devil's Advocate over-correction); the METRIC+ small-scale manual derivation closes the structural-mapping gap (with full PIT head-to-head committed as item~(i)); the 84-MR PWR corpus is disclosed as the authors' own prior work with external-transfer committed as item~(j); the W5 PWR-specificity concern is addressed by the §subsec:third-domain "five PWR proven + five candidate" framing, yielding a ten-extension count that converts the negative instantiation from a domain witness into a framework-level falsification claim.

The only residual concern is W4: four of the six literature items Round 2 R2 catalogued (Hu 2019, Sun 2022 CSUR, Liu 2020 MET, Mariani 2018 MET, Lin 2020 symmetry-MR) are neither added nor declined with rationale. This is a Minor-revision item: a one-paragraph addition in §2.1 / §2.3 / §2.4 or an explicit decline-with-rationale paragraph suffices.

The framework's positional claim against METRIC+, the operator-algebra framing, and the falsification-with-extension methodology are now correctly scoped. The paper has matured from Round 2's Major-Revision profile to a Minor-Revision profile within the R2 (literature / theoretical framework / domain) review remit. The work is on track for acceptance after the W4 residual is closed.

---

## R2 Domain — Round 3 250-word summary

**Decision**: Minor Revision. **Weighted score**: 79.3.

**Round 3 W1–W5 resolution status**: W1 FULLY_RESOLVED (abstract / §subsec:completeness / Boundary tcolorbox correctly bound Theorem 1 over $\mathrm{MR}(\mathcal{A}_P)$ with explicit by-construction caveat; Devil's Advocate over-correction correctly resisted; substantive empirical-to-structural conversion preserved). W2 FULLY_RESOLVED at small scale (new Table~\ref{tab:metricplus-headtohead-small} on three §subsec:test-design SUTs is internally consistent: 6/5/3 of 11 D$\times$R pairs non-vacuous; structural finding "Set-MP $\subsetneq$ NOETHER block coverage on bivariate-input SUTs" follows; full PIT head-to-head committed as item~(i)). W3 FULLY_RESOLVED (new Provenance paragraph at §subsec:reactor-mapping lines 517–518 explicitly states 84-MR PWR corpus is authors' own prior work and frames the comparison as internal vocabulary coherence not external transfer; PARCS / IAEA-TECDOC external-transfer follow-up committed as item~(j)). W4 PARTIALLY_RESOLVED (Zhou 2020 SymmetryMRP added; Ying 2025 dedicated engagement paragraph at line 193 with defensible family-tree-vs-NOETHER-block mapping; but Hu 2019, Sun 2022 CSUR, Liu 2020 MET, Mariani 2018 MET, Lin 2020 symmetry-MR neither added nor declined with rationale). W5 FULLY_RESOLVED (§subsec:third-domain "five PWR proven + five candidate" framing yields ten-extension count; PWR-specificity concern correctly addressed).

**Round 3 R2 new concerns**: NC1 Ying 2025 family-tree characterisation is defensible. NC2 "zero by construction" wording is borderline; suggest one-line scope hedge. NC3 84-MR provenance disclosure adequately closes R3's parallel concern; one residual C1-bullet textual alignment suggested.

**Recommendation**: Minor Revision pending the W4 literature additions (or explicit declines with rationale).
