# NOETHER — Simulated Peer Review Reports (Stage 3)

**Manuscript:** "NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras"
**Target venue:** IEEE TSE / ACM TOSEM
**Review type:** Simulated double-blind, 5-reviewer panel + Editorial Decision + Revision Roadmap
**Pipeline stage:** academic-pipeline Stage 3 (full review mode)

> **Anti-Pattern #6 reminder applied throughout:** every weakness is recorded with concrete evidence; reviewer disagreement with the manuscript is not sycophantically softened. Disagreements between the manuscript and reviewers will be tracked through Stage 4 as `RESOLVED`, `REVIEWER_DISAGREE_DEFENDED`, or `ACKNOWLEDGED_LIMITATION`.

---

## REVIEW 1 — Reviewer #1 (Theory Lead)

**Profile:** Senior software-testing researcher with formal-methods background; prior publications on category-theoretic approaches to test oracle problems.

### Summary
The paper proposes NOETHER, a deductive framework that constructs MetaPatterns from operator-algebraic structure, with a completeness theorem (Theorem 1) and a decidability/complexity theorem (Theorem 2). The framing — Noether 1918 as analogy — is bold and the gap-statement (origin / closure / transferability) is clearly articulated. The paper is, as far as I am aware, the first to attempt an algebraic foundation for MetaPattern discovery, and on that basis the work has the potential to influence both the structured-MR-identification line (METRIC, METRIC+) and downstream automated pipelines.

### Strengths
- **S1.** The origin–closure–transferability framing is a real contribution to how the community talks about MetaPatterns, even before the technical apparatus is evaluated.
- **S2.** Definition 8 (algebra-induced MR) is the right move: bounding the completeness claim to algebra-induced MRs avoids the trivial counterexample of "any property a tester writes down".
- **S3.** §5's progression from Boltzmann through transport, diffusion, and burnup, with the explicit prediction that $m_{\mathrm{rev}}$ vanishes under dissipation, is the kind of structural prediction that an inductive framework cannot provide. This is a genuine demonstration of deductive value.

### Weaknesses

**P0 (must fix before acceptance)**

- **W1.** **Theorem 1's "unique" clause is propped up by an undefended convention.** §4.3 acknowledges that uniqueness "follows under the canonical-block convention" but does not define the convention, give examples of MRs that arise through composition of multiple blocks, or argue that the convention is the only sensible choice. As written, uniqueness is not proved; it is asserted by fiat. Either give the convention a precise definition (with worked examples of multi-block-derived MRs) or weaken the theorem to existence-only and restate accordingly.
- **W2.** **Appendix C is referenced four times but does not exist in the manuscript.** The proofs of both theorems are deferred to "Appendix C" but the appendix is absent. For a theoretical paper at TSE/TOSEM, the proofs are not optional supplementary material — they are the load-bearing artefact. This is the single largest defect.
- **W3.** **Theorem 2's complexity bound is unactionable as stated.** The bound $O(n \cdot \max_i t_i \cdot \log n)$ leaves the reader in the dark about what $t_i$ actually is for representative algebras. The text claims $n \le 12$ for Boltzmann and $n \le 8$ for equivariant ML, which is fine, but $t_i$ — the per-generator invariant-extraction cost — is precisely what determines whether the construction is practical. Provide a worked example of $t_i$ computation in at least one case.

**P1 (should fix)**

- **W4.** **§5.3 claims structural correspondence with the prior 84-MR catalogue at the "label" level only.** The five mappings ($m_{\mathrm{inv}} \leftrightarrow$ P1, etc.) are asserted by name but not verified element-wise. A small table showing which of the 84 MRs is placed into which $\mathbb{M}(\mathcal{A}_{\mathrm{Boltz}})$ MetaPattern by NOETHER's construction, contrasted with the prior catalogue's placement, would convert the claim from gestural to checkable.
- **W5.** **The identification of P4 (trajectory) with $m_{\mathrm{rev}}$ (time-reversal) is questionable.** Trajectory MRs from the prior PWR work originate, on the authors' own description in §5.1, from non-diagonal coupling in Bateman-type ODEs (e.g.\ xenon overshoot, samarium poisoning). These are dynamical-systems trajectory features, not time-reversal invariants. Conflating them risks both kinds of MR being misclassified by the framework.
- **W6.** **The identification of P5 (partial-order) with $m_{\mathrm{adj}}$ (self-adjoint duality) is similarly strained.** Partial-order MRs in the prior work concerned method-accuracy comparisons (e.g.\ CRAM vs.\ TTA), not adjoint reciprocity. The mapping is forced.

**P2 (nitpicks / suggestions)**

- **W7.** §3.6 promises that "an operator may participate in several blocks" but the later quotient construction in §4.2 step 3 acts within a single block. Clarify how multi-block membership is reconciled.
- **W8.** The Noether 1918 framing is rhetorically powerful but, taken literally, is overstated: Noether's theorem requires a Lagrangian and a continuous symmetry of the *action*, neither of which has a clean software-engineering analogue. Tone the analogy down in §1 paragraph 1 to a structural homage rather than a mathematical extension.

### Recommendation: **Major Revision.** The framework is publishable in principle, but Theorem 1's uniqueness claim and the absent Appendix C must be addressed before any further evaluation. With those fixed, plus the §5.3 element-wise table and the P4/P5 reclassifications, this is acceptable.

---

## REVIEW 2 — Reviewer #2 (Methodology / Comparative Lead)

**Profile:** Software-testing researcher specialising in automated MR generation and empirical-evaluation methodology.

### Summary
The paper positions itself against a respectable cross-section of the MR-identification literature (Chen 1998, Segura 2016, Li 2025, MR-Scout, GenMorph, METRIC, METRIC+, LLM-assisted methods including Shin et al.) and credibly argues that no prior work answers the origin/closure/transferability questions. The deductive construction is correct in spirit but the comparative analysis is asymmetric: prior work is described, criticised, and shelved, but never directly contested with NOETHER on the same evaluation terms.

### Strengths
- **S1.** §2's four-storyline structure — fundamentals, structured (METRIC/METRIC+), automated, catalogues — is the cleanest taxonomy of the MR-identification field I have seen.
- **S2.** The honest acknowledgement (§4.5, §7.4) that NOETHER does not automate $\mathcal{A}_P$ distillation is rare in this literature and substantially improves the paper's credibility.
- **S3.** The Shin-QUATIC2024 reference replacing the earlier draft's MARS citation is correctly handled (acknowledged via the audit log). The paper's integrity-checking process is itself something the field could learn from.

### Weaknesses

**P0**

- **W9.** **No empirical validation accompanies the theoretical claims.** A constructive framework with a completeness theorem ought to be testable against existing automated pipelines on at least one shared benchmark: take Apache Commons Math (used by GenMorph, MR-Scout, MARS-equivalents in the literature), distil $\mathcal{A}_P$, run NOETHER, and report which MRs the framework places into which MetaPatterns versus what MR-Scout / GenMorph / Shin-style LLM pipelines produce. Without this, the §6 cross-domain claim ("the framework transports") is asserted but not demonstrated to actually compete with anything. For TSE/TOSEM, a pure-theory paper is acceptable, but it must defend the absence of empirical work, not silently proceed without it.

**P1**

- **W10.** **The §6 ML instantiation produces a MetaPattern set but never derives concrete MRs from it.** The promise in §6.4 ("NOETHER provides a deductive starting point") is not redeemed: no example MR for, say, an SE(3)-equivariant point-cloud classifier is written down in the paper. Without an end-to-end worked example, the cross-domain transferability claim is taken on faith.
- **W11.** **The relationship to METRIC and METRIC+ is described in §7.2 but never operationalised.** If NOETHER's MetaPatterns "supply *why* the categories are these", it should be possible to map METRIC's category templates onto $\mathbb{M}(\mathcal{A}_P)$ blocks for at least one program family. Such a mapping would be the most valuable practical contribution to the structured-MR-identification community.
- **W12.** **The claim that NOETHER "re-grounds" PMCM (§7.3) is asserted without a worked example.** Take a PMCM grid from a published evaluation, demonstrate which cells correspond to $\mathbb{M}(\mathcal{A}_P)$ entries, and show what an algebraically-warranted PMCM coverage report would look like.

**P2**

- **W13.** §1's "27 years" framing of the MR-identification bottleneck would benefit from a one-paragraph quantitative pulse: how many surveys, how many open methods, how many MRs catalogued? Current §1 is impressionistic on this point.
- **W14.** §7.4's three automation directions for $\mathcal{A}_P$ distillation are sketched plausibly but no preliminary feasibility evidence is offered. This is acceptable for a future-work paragraph; flag if the authors choose not to expand.

### Recommendation: **Major Revision.** The theoretical contribution is sufficient for the venue but the paper currently reads as Half a Paper — the algebraic framework is well-built, but the comparative posture against existing tooling has not been operationalised. At minimum, supply (a) one shared-benchmark comparison with an existing automated pipeline (W9), (b) an end-to-end MR derivation in the ML domain (W10), and (c) a worked METRIC-to-NOETHER mapping (W11).

---

## REVIEW 3 — Reviewer #3 (Reproducibility / Empirical Standards Lead)

**Profile:** Software-engineering researcher with an artifact-evaluation track-record and emphasis on open-science standards.

### Summary
This is a theoretical paper, but TSE/TOSEM has tightened reproducibility expectations even for theoretical contributions. Definitions, theorems, and constructions in such papers must be independently re-derivable from publicly accessible source material. NOETHER currently fails this expectation in three specific ways.

### Strengths
- **S1.** The Stage 2.5 audit log appended to the manuscript is exemplary integrity practice. It should be retained (or summarised in a "data and integrity availability statement") in the submitted version.
- **S2.** All external citations are now verified with DOIs or arXiv IDs. This is the basic standard but rarely actually met.

### Weaknesses

**P0**

- **W15.** **Two key references are unpublished author working papers** ([PWR-MetaPattern-Report] and [PMCM-Adequacy]). The 84-MR corpus relied upon in §5.3 is unavailable to reviewers without supplementary material. Either (a) attach the full PWR analysis report as a non-archival appendix or supplementary file with arXiv-archived contents, or (b) replace the dependence on the unpublished corpus with a publicly-available MR corpus from Segura 2016 or LiTOSEM2025.
- **W16.** **CONSTRUCT-MP is presented as an algorithm but never as runnable code.** A theoretical paper does not require a polished implementation, but a Python sketch (50–80 lines) demonstrating the four steps on a toy algebra would substantially strengthen Theorem 2's "computable" claim and would let independent readers verify the construction.

**P1**

- **W17.** **§3 introduces five operator-algebra building blocks (B1–B5) but does not justify the choice of five.** Why not four (collapsing self-adjoint into symmetry)? Why not seven (adding spectral structure as a sixth, as the prior PWR report explored)? §7.1's "external validity" paragraph hand-waves at this question. A more direct treatment is needed: either the five are necessary and sufficient (give the argument) or the five are *currently* sufficient for the worked instantiations (state this explicitly).
- **W18.** **No artifact evaluation track is mentioned.** TSE/TOSEM increasingly include badging for available/functional/reusable artifacts. State the authors' artifact-availability intent explicitly; this is a submission-readiness item, not strictly a content defect, but expected.

**P2**

- **W19.** Some symbols are introduced informally before formal definition (e.g.\ $\rho$ for the output representation, used in §1 paragraph 5 before §3.2 defines it). Add forward-references or restate.
- **W20.** §A.4's discussion of self-shielding non-monotonicity ("non-monotone in absolute terms but monotone in normalised terms") is interesting but unsourced; cite a representative reactor-physics text or worked numerical example.

### Recommendation: **Major Revision.** The theoretical content is strong; the reproducibility gap is fixable but currently substantial. W15 (unpublished-corpus dependency) and W16 (no runnable artefact) are blocking issues for the venue's current standards. With a 2-page Appendix sketch of CONSTRUCT-MP in code and a public-corpus replacement for the PWR dependency, the paper meets reproducibility expectations.

---

## REVIEW 4 — Devil's Advocate (Adversarial Sceptic)

**Profile:** Pre-assigned to find the strongest possible case *against* publication. Conversational, not collegial. The reader who would tank the paper at a programme committee meeting if the case is not airtight.

### The case against publication

**The paper is not what it claims to be.** It claims to provide MetaPattern discovery with its first deductive foundation. What it actually provides is a *recoding* of an existing inductive catalogue into the language of operator algebra, with a theorem (Theorem 1) whose strength exactly matches that recoding and not one inch more. Look closely:

1. **The five MetaPatterns ($m_{\mathrm{inv}}$, $m_{\mathrm{mono}}$, $m_{\mathrm{adj}}$, $m_{\mathrm{rev}}$, $m_{\mathrm{conv}}$) coincide one-for-one with the prior catalogue's P1–P5.** §5.3 calls this a "consequence of structural fact"; I call it the giveaway. If the algebra were doing the work, the algebraic decomposition would have generated *some* MetaPattern not present in the inductive catalogue, or refused to generate one of P1–P5 due to algebraic incompatibility. Neither happens. The framework reproduces what was already known.

2. **The completeness theorem (Theorem 1) is true *because* of how Definition 8 (algebra-induced MR) is set up.** The definition restricts the universe to MRs that arise via $\mathrm{Translate}(\iota, s)$ — the same translation that CONSTRUCT-MP uses. Every algebra-induced MR is, by definition, traceable back to an invariant within a block; CONSTRUCT-MP collects all blocks; therefore every algebra-induced MR is collected. This is not a mathematical achievement; it is a tautology disguised as a theorem.

3. **The transferability claim (§6) is not a transferability *demonstration*.** The paper specifies $\mathcal{A}_{\mathrm{equi}}$, runs CONSTRUCT-MP, and reports a list of label names ($m^{\mathrm{eq}}_{\mathrm{inv}}$, $m^{\mathrm{eq}}_{\mathrm{mono}}$, ...). Nothing else happens. No actual MR is derived. No actual ML system is tested. No comparison is performed. "Transferability" is, in §6, the property that a procedure can be re-run; that is true of any mechanical procedure, not a substantive achievement.

4. **The "principal limitation" (§4.5) is not a limitation; it is the entire upstream problem.** The paper concedes that distilling $\mathcal{A}_P$ from program semantics is human labour and is not automated. That concession alone subsumes the "MR identification bottleneck" the paper is supposed to solve. If a domain expert can already write down $\mathcal{A}_P$, can they not also write down the MRs directly? The paper does not seriously engage this objection.

### What would have to change for me to retract the case

**(a) The framework would have to make a structural prediction the inductive catalogue does not.** §5.4's prediction that diffusion-equation solvers cannot exhibit $m_{\mathrm{rev}}$ MRs is a step in this direction but is too small a yield: every reactor-physics practitioner knows diffusion is dissipative. Show me one MetaPattern *omission* the algebra demands but which the inductive catalogue erroneously included; or show me one MetaPattern the algebra demands which the inductive catalogue missed. Either would convert the result from re-coding to discovery.

**(b) Theorem 1 would have to be statable without Definition 8's restriction.** Restate completeness over an MR space that is *not* the trivial pre-image of CONSTRUCT-MP, e.g.\ "every MR a tester can articulate as a property over the operator algebra, regardless of whether it arises from a single invariant". Then prove that statement, or prove its falsehood.

**(c) §6 would have to derive at least one ML MR end-to-end and test it on at least one ML system.** A worked example, however small, demonstrating that the deductive MetaPattern set yields a non-obvious testing artefact for a non-physics program.

### Recommendation: **Reject in current form**, with explicit reservation that (a)–(c) above could change my position to Accept on resubmission.

---

## REVIEW 5 — Editor-in-Chief (EIC) Synthesis

### Summary across all four reviewers
The technical reviewers (R1, R2, R3) converge on **Major Revision**. The Devil's Advocate (R4) recommends **Reject** but identifies three concrete pivots ((a)–(c) in R4's "what would have to change") that, if executed, would convert their position. The reviewers' weaknesses cluster into four themes:

1. **Theory completeness gaps** (R1's W1–W3): Theorem 1's uniqueness convention is undefined; Appendix C is missing; Theorem 2's complexity bound lacks a worked $t_i$ example. **Severity: P0.**
2. **Empirical / comparative absence** (R2's W9–W12, R4's pivot (c)): no shared-benchmark comparison; no end-to-end MR derivation in §6; no operationalised METRIC-to-NOETHER mapping; no PMCM worked example. **Severity: P0 to P1.**
3. **Conceptual mappings strained** (R1's W5–W6, R4's structural-prediction critique): the P4↔$m_{\mathrm{rev}}$ and P5↔$m_{\mathrm{adj}}$ correspondences are forced; the framework currently reproduces, rather than refines or extends, the inductive catalogue. **Severity: P0** (this is the crux of the paper's contribution claim).
4. **Reproducibility and corpus access** (R3's W15–W16): two key dependencies ([PWR-MetaPattern-Report], [PMCM-Adequacy]) are unpublished; no runnable artefact accompanies CONSTRUCT-MP. **Severity: P0** for current TSE/TOSEM standards.

### Editorial decision

**Decision:** **MAJOR REVISION**, with explicit conditional path to acceptance.

The paper is publishable in principle — the framing is novel, the theorem statements are non-trivial, and the integrity discipline (Stage 2.5 log) is exemplary. However, in current form, the Devil's Advocate's central objection is sound: the paper recodes rather than discovers, and the conceptual mappings P4↔$m_{\mathrm{rev}}$ and P5↔$m_{\mathrm{adj}}$ are not defensible. Without addressing this, the paper's central contribution claim is structurally undermined.

Authors are invited to submit a revised version addressing the Major-Revision items below, with attention to the Crux Items (CR-1 to CR-3) that, if addressed, would resolve the Devil's Advocate's reservation. Failure to address Crux Items will result in a recommendation toward Reject on the second pass.

---

## REVISION ROADMAP (Schema 11 / R&R Traceability format)

This roadmap is structured to feed academic-paper revision mode in Stage 4. Each row carries a unique ID, the originating reviewer, the priority, the required change, the location in the manuscript, and a status field that Stage 4 will populate.

| ID | Reviewer | Priority | Crux? | Required change | Location | Stage 4 status |
|----|----------|----------|-------|------------------|----------|------------------|
| R1-W1 | R1 | P0 | yes | Define the canonical-block convention precisely (with at least 2 worked examples of multi-block-derived MRs) OR weaken Theorem 1 to existence-only and revise downstream claims. | §4.3 + Appendix C | pending |
| R1-W2 | R1 | P0 | yes | Write Appendix C: full proofs of Theorem 1 and Theorem 2, with case analysis for multi-block compositions. | new Appendix C | pending |
| R1-W3 | R1 | P0 | no | Provide a worked example of $t_i$ computation for at least one block in $\mathcal{A}_{\mathrm{Boltz}}$ (e.g.\ symmetry block: $t_i$ = group-action fixed-point computation). | §4.4 | pending |
| R1-W4 | R1 | P1 | yes | Add element-wise correspondence table in §5.3: for at least 10 representative MRs from the 84-corpus, show their NOETHER placement vs prior catalogue placement. | §5.3 | pending |
| R1-W5 | R1 | P0 | yes | Re-examine the P4 (trajectory) ↔ $m_{\mathrm{rev}}$ (time-reversal) mapping. Either (a) reclassify trajectory MRs into a new block (e.g.\ "qualitative-dynamics block") or (b) defend why trajectory phenomena are mathematically subsumed by time-reversal compatibility, with explicit Bateman-coupling examples. | §3.4, §5.2, §5.3 | pending |
| R1-W6 | R1 | P0 | yes | Re-examine the P5 (partial-order) ↔ $m_{\mathrm{adj}}$ (self-adjoint duality) mapping. Most likely a sixth block (method-comparison / error-estimation block) is required; this also addresses R3-W17. | §3.4, §3.6, §5.2 | pending |
| R1-W7 | R1 | P2 | no | Clarify multi-block membership reconciliation in §3.6. | §3.6 | pending |
| R1-W8 | R1 | P2 | no | Soften Noether 1918 framing in §1 paragraph 1 to "structural homage" rather than "extension". | §1 | pending |
| R2-W9 | R2 | P0 | yes (R4-c) | Add an empirical comparison: take Apache Commons Math (or another shared benchmark from MR-Scout / GenMorph / Shin), distil $\mathcal{A}_P$, run NOETHER, report MR placement; OR explicitly defend the absence of empirical work with a "scope of the contribution" paragraph in §1. | §6 or §7 | pending |
| R2-W10 | R2 | P1 | yes (R4-c) | Derive at least one concrete MR end-to-end in §6 for an SE(3)-equivariant point-cloud classifier; show the MR's executable form. | §6.4 | pending |
| R2-W11 | R2 | P1 | no | Map METRIC's category templates onto $\mathbb{M}(\mathcal{A}_P)$ blocks for one program family. | §7.2 | pending |
| R2-W12 | R2 | P1 | no | Worked PMCM-to-$\mathbb{M}(\mathcal{A}_P)$ example: take a published PMCM grid, show algebraic warrant. | §7.3 | pending |
| R2-W13 | R2 | P2 | no | Quantify "27 years" framing with one paragraph of pulse statistics. | §1 | pending |
| R2-W14 | R2 | P2 | no | Optional: add preliminary feasibility evidence for $\mathcal{A}_P$ automation directions. | §7.4 | optional |
| R3-W15 | R3 | P0 | no | Resolve unpublished-corpus dependency: archive [PWR-MetaPattern-Report] as supplementary material with hash, or replace with public-corpus citation (e.g.\ Segura 2016). | §5.3, References | pending |
| R3-W16 | R3 | P0 | no | Add a 50–80-line Python sketch of CONSTRUCT-MP applied to a toy algebra (e.g.\ $\mathbb{Z}/2\mathbb{Z}$ symmetric input transformation). Include in supplementary material. | new Appendix D / supplementary | pending |
| R3-W17 | R3 | P1 | yes | Justify the five-block decomposition explicitly: state whether B1–B5 are necessary and sufficient (with argument) or *currently sufficient for the instantiations attempted* (with explicit acknowledgement). This dovetails with R1-W6. | §3.6, §7.1 | pending |
| R3-W18 | R3 | P2 | no | State artefact-availability intent. | manuscript metadata / acknowledgements | pending |
| R3-W19 | R3 | P2 | no | Add forward-references for symbols introduced informally before formal definition. | §1 | pending |
| R3-W20 | R3 | P2 | no | Source the self-shielding non-monotonicity claim. | §A.4 | pending |
| R4-CR-a | R4 | P0 | yes | **Crux item.** Identify at least one MetaPattern that the algebraic decomposition demands but the prior inductive catalogue missed, OR one the catalogue erroneously included that the algebra rules out. Without this, the contribution claim ("deductive foundation, not re-coding") is not defensible. | §5.4–§5.5 | pending |
| R4-CR-b | R4 | P0 | yes | **Crux item.** Restate Theorem 1 over a non-trivial MR space (one that is not the pre-image of CONSTRUCT-MP by construction), and prove it OR honestly weaken Theorem 1 to "completeness over the algebra-induced MR space, by construction" with explicit acknowledgement. | §4.1, §4.3 | pending |
| R4-CR-c | R4 | P0 | yes | **Crux item.** End-to-end ML demonstration: derive at least one concrete MR for a real ML system, run it, report whether it detects faults. Combines with R2-W10. | §6.4 | pending |

### Crux items summary

The three items marked "Crux" determine whether the paper's central contribution claim is defensible:

- **CR-a** (structural-prediction yield): Address by either finding a concrete prediction the algebra makes which contradicts or refines the inductive catalogue, or honestly stating that the framework currently re-grounds rather than refines.
- **CR-b** (Theorem 1 strength): Address by either lifting the theorem to a non-trivial MR space, or weakening it to a constructive completeness statement.
- **CR-c** (transferability empirical yield): Address by deriving and running at least one ML MR end-to-end, even if small.

Resolving the three crux items resolves the Devil's Advocate's structural objection. Failing to resolve them risks the paper's contribution claim being reduced to "re-coding" — publishable as such but not at the strength currently advertised.

### Convergence-aware stopping notice (per academic-pipeline v3.2)

If, in Stage 4 revision, the manuscript addresses all P0 items (W1, W2, W3, W5, W6, W9, W15, W16, W17, CR-a, CR-b, CR-c) AND the R&R deltas to subsequent re-review (Stage 3') yield <3 points improvement on a 100-point rubric, Stage 4' (second revision loop) is convergence-stopped per pipeline policy.

---

## End of Stage 3 review reports.

**Files produced:**
- This file: `NOETHER_review_reports.md` — 5 reviewer reports + EIC synthesis + Revision Roadmap.
- Manuscript (unchanged at this stage): `NOETHER_paper_draft.md`.

**Next pipeline stage:** Stage 4 REVISE (academic-paper revision mode), driven by the Revision Roadmap above.
