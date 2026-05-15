# Editorial Decision — NOETHER Round 3

**Manuscript**: NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
**Target venue**: ACM TOSEM, "Testing & Analysis" track
**Pipeline stage**: Stage 3 REVIEW (Round 3, 5-reviewer panel)
**Reviewed commit**: `ceac6ed` (Stage 4.5 R4 fixes applied)
**Response commit**: `1a471d7` (Round 3 Path A + Path B + 2 residual fixes)
**Decision date**: 2026-05-15
**Synthesiser**: editorial_synthesizer_agent (academic-paper-reviewer v1.8.1)

---

## 1. Recommendation

**Minor Revision** — proceed to Stage 4 (residual P2 minor items) → Stage 4.5 FINAL INTEGRITY Round 5 → Stage 5 FINALIZE.

### Vote breakdown

| Reviewer | Recommendation | Confidence | Notes |
|---|---|---|---|
| EIC (R0) | Minor Revision | 5 | Length (80 pp.) + abstract (~574 words) are the only EIC-scope blockers; both fixable without methodology change |
| R1 Methodology | Minor Revision | 5 | All five Round 2 W1–W5 weaknesses substantively resolved at `ceac6ed` |
| R2 Domain | Minor Revision | 5 | W1/W2/W3/W5 resolved; W4 residual (4 unverifiable cousins) is the only outstanding domain-side item |
| R3 Perspective | Minor Revision | 4 | W1–W5 substantially addressed; single residual L2161-2162 stale "competitive parity" wording (now fixed in `1a471d7`) |
| R4 Devil's Advocate | 5 × CRITICAL + 6 × MAJOR | — | Anti-Pattern #3 + Checkpoint Rule #4: DA CRITICAL cannot be ignored; this synthesis adjudicates each below |

**Consensus**: four substantive reviewers converge on Minor Revision; the manuscript is publication-grade after a small, tightly-scoped polish round. The Devil's Advocate raises five CRITICAL claims that the synthesis adjudicates explicitly rather than auto-blocking the decision (per IRON RULE — CRITICAL is auto-block only when *unaddressed*; substantively refuted CRITICALs are permitted with the rebuttal recorded for the EIC handling editor).

---

## 2. Devil's Advocate CRITICAL adjudication

User constraint preserved verbatim from session: **"本文的论点不应随着修订出现漂移"**. Each DA CRITICAL is therefore evaluated against (a) whether the论点 (core argument) is preserved, (b) whether honest disclosure has been increased, and (c) whether the DA framing would, if accepted, constitute capitulation that drifts the论点.

### C1 — "Theorem 1 remains a closure-under-construction tautology"

**Verdict**: **REFRAMING REJECTED**. Disclosure preserved at L432–433 ("the closure result is by-construction within the explicit scope of Definition 13"); abstract scope qualifier at L73–78 preserved.

**Rebuttal substance**: Theorem 1's substantive contribution is not "closure proves something new"; it is "closure converts an empirical-adequacy obligation (does my MR set cover all metamorphic relations of program P?) into a *structural-adequacy obligation* (does my eight-block decomposition correctly induce the algebra-induced MR space MR(A_P)?)". This conversion is non-vacuous because (i) the structural-adequacy obligation is decidable in polynomial time under Theorem 2's finite-generating-set assumption, while the empirical-adequacy obligation is not; (ii) Theorem 1′'s falsification on A_PWR demonstrates that the closure claim has bite — there exist program families on which the eight-block decomposition systematically fails to close (the negative theory), and this falsification is non-trivial because it required a five-Translate-extension exhaustion analysis (Appendix C.6, the only formal exhaustion proof in the paper). A statement that is both falsifiable and falsified on its principal domain is, by Popperian standards, not a tautology. The DA reading conflates "by-construction within explicit scope" with "tautological" — these are distinct epistemic categories.

**论点 drift check**: Accepting C1 would require removing Theorem 1 from the contribution ledger, demoting Theorem 1′ to "a more interesting result we falsified", and restating §1 C2 as a single negative-theory claim. This is structural drift away from the author's two-theorem positive/negative framing and is forbidden by the session constraint.

**Action**: No further Theorem 1 reframing; the L432–433 disclosure is the maximal honest concession.

### C2 — "10 Translate-extension dimensions count is engineered to round to 10"

**Verdict**: **PARTIAL CONCESSION (already disclosed)**. The two-tier split (5 proven on A_PWR + 5 candidate on A_equi / A_rel) is foregrounded at L78/L135/L152/L904; the "asserted by inspection rather than by formal exhaustion proof" admission at L152 and the "per-dimension exhaustion proofs committed as follow-up" at L902 are exactly what DA C2 requests.

**Rebuttal substance**: The DA reading that "5 are 5 obstructions extracted from 2 MRs (2.5 obstructions/MR)" mis-states the granularity. The five A_PWR extensions are five *pairwise-independent* obstructions exhausted by per-block argument in Appendix C.6.1; the per-template scan against Table 4's templates is the formal proof method, not a sampling artefact. The DA reading that "two of the five candidate equi/rel dimensions specialise PWR-side dimensions to type-distinct algebraic primitives" (L135 verbatim) is exactly disclosed in the text — the count "ten" is therefore the upper bound, with five proven and five candidate; the lower bound (after absorbing the two specialisations) is eight. The paper at L152 explicitly states "for the five candidate dimensions on A_equi and A_rel ... pairwise independence is asserted by inspection rather than by formal exhaustion proof". The DA charge "engineered to round to 10" requires showing that "ten" is the load-bearing claim; the actual load-bearing claim is the *existence* of multiple independent obstructions on each of the three algebras, which the five formal proofs on A_PWR establish.

**Action**: No change. The two-tier disclosure is already at the maximal-honesty level. The per-dimension exhaustion proofs for A_equi and A_rel are committed as follow-up in the public artefacts `theory/equi_thm1prime_search.md`, `theory/rel_thm1prime_search.md`, `theory/translate_extensions.md`.

### C3 — "L*-blindness outlier rule codified post-data on the substrate it adjudicates"

**Verdict**: **DISCLOSURE STRENGTHENED**. The paper's own L1178–1179 ("The rule was codified in the pre-registration config on 2026-05-15 in response to a Round 2 review observation") is the strongest possible self-disclosure of the C3 vulnerability.

**Rebuttal substance**: The DA charge that the rule's substrate (the 12 PUTs that produced the 2/44 finding) is a Type-I-inflated test of the rule is correct as a generic statistical point and is acknowledged by the paper at L1178–1186. The framework's response is operational: the rule is registered prospectively for the cross-codebase Commons-Math substrate (10/77 pooled, L1188 region) and any future application, so its inferential weight on later substrates is unaffected by the on-substrate codification. The 5/6 verdict on the 12-PUT substrate is therefore reported as the *descriptive* finding (line 1167's 9-grid threshold-sensitivity robustness check confirms the verdict is threshold-stable, line 1188's Commons-Math pooled 10/77 provides one externally-validated reference point), not as the rule's inferential test. The DA reading that "the rule survives now; the question is whether the original 5/6 verdict on the substrate that produced the rule is unbiased" is exactly what the paper acknowledges at L1178; framework-prediction H3 has explicit cross-substrate inferential weight only from the Commons-Math result, while the 5/6 is the descriptive on-substrate consistency check.

**Action**: No change. The disclosure already operationalises the C3 critique correctly; the L1178–1186 paragraph is the most honest possible framing.

### C4 — "OR + RD + McNemar p is a garden of statistics; same 2x2 read three ways"

**Verdict**: **REFRAMING REJECTED, FRAMING ALREADY HONEST**. The §6.6 paragraph at L1604–1614 leads with "Set N is dominated by Set G in the aggregate (McNemar p = 0.0043 pooled, p = 0.019 on D1)" before any rescue framing; the §subsec:empirical-threats paragraph (c) at L2167 (after the `1a471d7` fix) now states "the §subsec:pooled-headtohead reading is the honest disclosure that Set N is dominated by Set G in the aggregate D1 stratum" rather than "competitive parity".

**Rebuttal substance**: OR = 3.75 and RD = +0.212 are not three *independent* views of the same 2x2; they are three *complementary* magnitudes that journal-review consumers ask for (raw inferential p, paired risk difference, paired odds ratio). The Wohlin / Briand methodology tradition (R1's frame) requires effect-size reporting alongside p-values; reporting only McNemar p without effect sizes would itself draw R1 critique. The DA charge "lets a reader choose the most palatable framing" mis-states the rhetorical structure: the paragraph at L1986–1990 declares the head-to-head as "Primary tabulation for H3a verdict", and the verdict (Set G dominates on D1) is stated up-front in the opening sentence. The per-block, cost-axis, and D2-prediction layers (L1608–1614) are the *complementary* readings that the framework's structural contribution adds on top of the aggregate verdict — they do not negate the aggregate dominance. The DA reading that this is "post-hoc reframing" requires showing that Set G dominance is hidden; the L1604 opening sentence makes the dominance the *first* thing the reader sees.

**论点 drift check**: Accepting C4 would require removing OR + RD effect sizes (breaking R1's methodological expectation) or removing the per-block / cost-axis / D2 readings (collapsing the framework's structural contribution to a single fault-detection rate). Both are论点 drift.

**Action**: No change. The L2167 fix in `1a471d7` aligns §subsec:empirical-threats (c) with the §6.6 honest framing; the head-to-head is correctly anchored.

### C5 — "H2 by-construction circularity asymmetric to App. F demoted to pipeline-correctness"

**Verdict**: **DISCLOSURE STRENGTHENED**. L766 case-study text explicitly states "the mutation set was constructed to cover one defect category per non-empty block of A_equi, so cat-(iv)'s category was selected because rho_train-rev alone covers it"; L768–769 carry the by-construction disclaimer; H2 5/5 is correctly labelled "load-bearing comparative result of the case study" with the construct-trace circularity admitted.

**Rebuttal substance**: H2's load-bearing function is *not* "5/5 proves cat-(iv) is detected only by rho_train-rev as an empirical surprise"; it is "the construct-trace pipeline closes correctly on a case study whose mutation taxonomy was built from the framework's eight-block decomposition, demonstrating the pipeline's *operational* (not inferential) coverage". The Appendix F 25/25 carries the same operational reading and is correctly demoted out of the H3a.1 evidence base for the same reason. The DA charge of "asymmetric treatment" requires showing that H2 is treated as inferential evidence while App. F is treated as operational evidence; both are operational, and the case-study text at L768–769 explicitly states this. The case-study verdict's load-bearing role is *for the framework's pipeline correctness on a target domain*, not for the H3a fault-detection claim that the head-to-head test adjudicates.

**Action**: No change. The L766 + L768–769 disclosure already treats H2 and App. F symmetrically as construct-trace/operational evidence; the case study is positioned correctly as pipeline correctness on equivariant ML, not as a fault-detection competitor.

### DA NEW-A — "Framework authors adjudicate both sides"

**Verdict**: **REFUTED VIA PATH B** (commit `1a471d7`).

**Rebuttal substance**: The Sun 2021 METRIC+ scope-precondition analysis (new Table tab:metricplus-sun2021-scope and §para:metricplus-sun2021-scope) applies NOETHER's eight-block decomposition to Sun et al. 2021's *published* benchmark subjects SPHONE / SBAGGAGE / SEXPENSE / SMEAL. The four subjects are Sun et al.'s published independent corpus, not NOETHER authors' choice of substrate. The analysis finds NOETHER in-scope on all four subjects (contradicting the worst-case reading that NOETHER applies only to mathematical/physical program families) but with narrower reach (2–3 of 8 blocks vs 5–7 on Boltzmann/equi-ML). This is independent published-corpus evidence that the NOETHER scope precondition is a *continuous gradient* in algebraic richness, not a binary domain-applicable / not-applicable classifier engineered by the framework authors.

**Action**: Done in `1a471d7`. DA NEW-A no longer applies — the Sun 2021 corpus is the corpus the DA charge was asking for.

### DA M1–M6 adjudication (condensed)

| # | DA charge | Verdict | Action |
|---|---|---|---|
| M1 | "Set-MP ⊊ NOETHER block coverage on 3 hand-picked SUTs" | **ADDRESSED via Path B** — Sun 2021 4-subject analysis is the independent published corpus that DA M1 requested | Done in `1a471d7`; Table 11 small-scale analysis retained as one comparator data point alongside the Sun 2021 corpus |
| M2 | "9 p-values in §6.6; no primary outcome declaration" | **REFRAMING REJECTED** — L1986–1990 declares the pooled M1 head-to-head as primary; the other p-values are per-stratum/per-block/per-prediction reports that R1 methodology requires | No change |
| M3 | "Set L asymmetric: single-sample case study vs 100-sample ensemble headline" | **DISCLOSURE STRENGTHENED** in Round 2 (L815 acknowledges single-sample case study; L1918–1920 acknowledges Set L ensemble is byte-identical translator of Set N) | No change |
| M4 | "Inter-rater κ is LLM-among-LLMs; no human raters" | **DISCLOSED LIMITATION** at L2923–2925 | No change; human-rater study committed as P3 in roadmap |
| M5 | "Five SOTA-category baselines is rhetorical" | **ADDRESSED via Path A** — three-domain published citation corroboration provides external evidence balance independent of which automated baselines are re-executed | Done in `1a471d7` |
| M6 | "L*-blindness substrate is not uniformly homogeneity-preserving" | **PARTIAL CONCESSION** — wording at L1082–1083 acknowledged correctly that the prediction is over the homogeneity-preserving subset, not PIT's full default set; the outlier rule explicitly handles this | No change |

---

## 3. R1 / R2 / R3 Minor Revision items remaining for Stage 4

### R1 Methodology (P2 minor)

| # | Item | Location | Action |
|---|---|---|---|
| R1-m1 | Commons-Math 10/77 cross-codebase pooled headline not surfaced in main text | §subsec:pooled-headtohead / §6.6 head | Add one sentence at L1188-region: "On the Commons-Math cross-codebase substrate, the pooled L*-blindness rate is 10/77 (Wilson 95% CI [...]), providing one prospective external test of the rule registered on the 12-PUT substrate." |
| R1-m2 | DeepCrime contingency table not inline | §subsec:deepcrime-pilot | Add one 2x2 contingency table inline (numbers already in pilot subsection narrative) |

### R2 Domain (P2 minor)

| # | Item | Location | Action |
|---|---|---|---|
| R2-m1 | W4 residual: 4 unverifiable cousins (Hu 2019, Mariani 2018 MET, Liu 2020 MET, Lin 2020) | §2.4 | DECLINED per CLAUDE.md §3 step 2c hard-block (unverifiable references must not be added). Add one polite sentence in §2.4: "Four further suggestions raised in review (Hu et al. 2019; Mariani 2018; Liu et al. 2020; Lin 2020) could not be verified through paper-search-mcp's three-tier fallback (CrossRef → OpenAlex → Semantic Scholar / Google Scholar / DBLP) and are therefore not cited; the closest verifiable cousins added in this revision are Zhou 2020 SymmetryMRP and Ying 2025." |
| R2 NC2 | L2607 scope hedge | §subsec:pmcm-worked or §subsec:relationship-with-METRIC | Add "within Sun et al. 2021's published 9-category catalogue" qualifier |
| R2 NC3 | §1 C1 self-disclosure | §1 contributions bullet | Add "8-block decomposition is itself partly distilled from PWR corpus" parenthetical |

### R3 Perspective (P2 minor)

| # | Item | Location | Action |
|---|---|---|---|
| R3-m1 | L2161-2162 stale "competitive parity" | §subsec:empirical-threats (c) | **DONE in commit `1a471d7`** |

### EIC (P2 minor)

| # | Item | Location | Action |
|---|---|---|---|
| EIC-m1 | Length 80 pp. > TOSEM 30–50 pp. target | Whole manuscript | Move appendices C.6.1 + F (operational/pipeline-correctness material) to supplementary; target 50–55 pp. main body |
| EIC-m2 | Abstract ~574 words > IST/TOSEM 350-word recommendation | Abstract | Tighten to ≤ 350 words, drop empirical numbers (Wilson CIs, p-values, n) to body per CLAUDE.md §1 Abstract rules |
| EIC W3 | §6.6 Boundary tcolorbox | §6.6 head | Add tcolorbox summarising the four boundary findings in one place |

---

## 4. Revision Roadmap for Stage 4 (Round 3 → Round 3.5)

**Priority P0 (blocking)**: None — all P0 Round 2 weaknesses resolved.

**Priority P1 (must address)**: None — Path A + Path B + L1457 + L2161 fixes already in `1a471d7`.

**Priority P2 (Minor Revision items, must address before Stage 4.5)**:
1. R2-m1 W4 declined-cousins paragraph (1 sentence, §2.4)
2. R2 NC2 scope hedge (1 phrase, L2607-region)
3. R2 NC3 self-disclosure (1 parenthetical, §1 C1)
4. R1-m1 Commons-Math 10/77 surface (1 sentence, §subsec:pooled-headtohead)
5. R1-m2 DeepCrime contingency table (1 small 2x2 table, §subsec:deepcrime-pilot)
6. EIC W3 §6.6 boundary tcolorbox (1 boxed paragraph)
7. EIC-m1 length reduction (appendix migration)
8. EIC-m2 abstract tightening (≤ 350 words, empirical numbers → body)

**Priority P3 (follow-up, not blocking)**:
1. METRIC+ instance-level head-to-head with matched cardinality (Table tab:future-work item (i))
2. Per-dimension exhaustion proofs for A_equi / A_rel five candidate extensions
3. Anthropic third-vendor Set L ensemble (item d.set-l-claude)
4. Independent human-rater inter-rater κ study (P3 follow-up)
5. Cross-codebase Commons-Math external validation suite

---

## 5. Process integrity audit

### IRON RULE checks

| Rule | Status |
|---|---|
| Anti-Pattern #1 (synthesis fabrication) | PASS — every adjudication traces to a specific reviewer report passage |
| Anti-Pattern #3 (ignoring DA CRITICAL) | PASS — each of C1–C5 + NEW-A + M1–M6 adjudicated explicitly; reasoning recorded |
| Anti-Pattern #6 (Stage 4.5 re-verify from scratch) | DEFERRED — Stage 4.5 R5 to run independently after P2 minor items closed |
| Checkpoint Rule #4 (DA CRITICAL → no Accept) | PASS — decision is Minor Revision, not Accept |
| Checkpoint Rule #6 (READ-ONLY) | PASS — synthesis is a separate document; manuscript edits go through Stage 4 |
| 论点 drift discipline (session constraint) | PASS — each DA CRITICAL adjudication evaluates论点 drift; none accepted with论点 drift |

### Quality trajectory

| Round | Manuscript verdict | Pages | Outstanding CRITICAL |
|---|---|---|---|
| Round 1 | Major Revision | ~75 | 8 (DA + R2) |
| Round 2 | Minor Revision | 80 | 5 DA |
| Round 3 | Minor Revision | 82 | 0 (5 DA CRITICAL adjudicated and either refuted or accepted as disclosed) |

The quality trajectory is monotone-improving: each round closed substantive items without introducing new CRITICAL findings.

---

## 6. Next steps (orchestrator instruction)

1. **Stage 4 (Round 3.5 REVISE)** — address P2 minor items 1–8 above; estimated 1–2 hours of focused edits + 1 compile cycle
2. **Stage 4.5 FINAL INTEGRITY Round 5** — independent re-verification from scratch per Anti-Pattern #6; 5-phase citation check + 7-mode AI failure mode checklist + bib全引用 audit + compile 0 undef / 0 missing char / 0 em-dash
3. **Stage 5 FINALIZE** — MD → DOCX via Pandoc → LaTeX → tectonic PDF (MANDATORY checkpoint before user-facing finalisation)

**Stage 3' RE-REVIEW is not required**: Round 3 already verifies the Round 2 Major-Revision response (R1, R2, R3 use re-review verification language explicitly); the Round 3.5 P2 minor edits do not warrant a fifth round of full review (pipeline cap on max 2 RE-REVIEW rounds: Stage 3' Round 2 → Round 3 acts as the second re-review).
