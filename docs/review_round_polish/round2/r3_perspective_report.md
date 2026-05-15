# Peer Review Report

## Manuscript Information
- **Title**: NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
- **Manuscript ID**: TOSEM (anonymised, double-blind)
- **Review Date**: 2026-05-15
- **Review Round**: Round 2 (polish)

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 3 (Perspective)

### Reviewer Identity
Cross-disciplinary V&V scholar. Combined background in (i) reactor physics and PWR safety analysis (transport / diffusion solvers; Bell & Glasstone, Lewis & Miller, Stacey, Lamarsh & Baratta, NRC RG 1.77, 10 CFR 50 App A); (ii) equivariant ML / geometric deep learning (Cohen–Welling, Bronstein, Thomas–Smidt TFN, Fuchs SE(3)-Transformer, Satorras EGNN, Cohen 2019 Gauge); (iii) relational database theory + idempotent semirings (Calcite rewrite rules, CockroachDB, Wang2024 QED).

### Review Focus
Cross-domain transferability of NOETHER's eight-block decomposition; physical accuracy of the PWR negative-instantiation propositions and tolerances; mathematical accuracy of the A_equi product-group and gauge-bundle counterexamples; database-theory accuracy of the A_rel survey; external validity of the §6.6 head-to-head and the §6.6.1 DeepCrime pilot beyond Java methods and the EGNN stand-in.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject

### Confidence Score
**4** (mostly within my area of expertise; high confidence on the PWR proofs and on the equivariant-ML obstructions, slightly lower confidence on the relational-algebra survey because the Calcite test names are read off file paths rather than from confirmed unverified-pair tables).

### Summary Assessment
NOETHER systematises MR identification by lifting induction one level: it claims a deductive downstream construction (CONSTRUCT-MP, Theorem 1 closure under Translate) from an empirically curated eight-block decomposition. The framework is instantiated on three structurally distinct algebras (Boltzmann reactor physics §5; SE(3)-equivariant ML §6; relational query optimisers §subsec:third-domain) and falsifies its own absolute-completeness conjecture (Theorem 1') on a fourth, the PWR core diffusion algebra (§subsec:negative-pwr / Appendix C.6), via two physically essential MRs (rod-bank-worth non-additivity and the MTC-vs-boron mixed derivative). On the cross-domain axis the paper is genuinely ambitious and largely succeeds at the operator-algebra level: the PWR negative instantiation is physically accurate and the tolerances are defensible against cycle-reload qualification practice; the gauge-bundle and product-group counterexamples on A_equi are mathematically correct in the sense that they identify the right algebraic primitives Cohen 2019 and Satorras 2021 invoke. The credibility issues are not in the algebra but in the empirical bridges: the equivariant-ML "cross-domain demonstration" is a 5189-parameter EGNN stand-in with construct-validity-controlled mutations; the third-domain relational survey is a single-rater LLM-pattern-matching scan against Calcite test names without verifier execution; and the §6.6 head-to-head is a pooled Set N = 26 vs Set G = 40 result on which the paper reads "competitive parity" rather than acknowledging that Set N is dominated on the aggregate substrate. External validity beyond Lie-group / self-adjoint / time-reversal program families is therefore claimed broader than the evidence supports. Major revision is required to align the abstract / contributions framing with what the three instantiations actually establish.

---

## Strengths

### S1: The PWR negative instantiation is physically accurate, regulatorily anchored, and load-bearing for the framework's honesty
§subsec:negative-pwr (lines 852–1010) and Appendix C.6 (lines 2762–2884) are the strongest part of the cross-domain story. Definition 15 (`def:rho-nonadd`, line 895) and Definition 17 (`def:rho-mtcbor`, line 930) are physically correct: the differential rod-bank worth uses the positive-convention 1/k_eff form (Definition 14, `def:drho-exact`, line 887), the adjoint perturbation reading (line 911) correctly factors d_rho through `<phi_dagger_A, delta H_B phi_A> / <phi_dagger_A, F_A phi_A>` with the configuration-indexed adjoint flux as the non-additivity root cause, and the three-mechanism MTC decomposition (lines 956–959: reduced moderation, boron poison evacuation, spectrum hardening + U-238 resonance) tracks Stacey §3.4 faithfully. The 5-pcm tolerance for `rho_nonadd` and the 0.01 pcm/°F/ppm tolerance for `rho_MTC-bor` are both defensible against cycle-reload qualification noise floors and are calibrated below the documented physical magnitudes (Stamm'ler & Abbate Ch. 6 for shadowing magnitudes 50–500 pcm adjacent / 5–20 pcm distant; Stacey §3.4 and Lamarsh & Baratta §8.3 for `partial alpha_MTC / partial C_B = 0.02-0.04` pcm/°F/ppm BOC-to-EOC). The HFP/ARO regime distinction (line 953) is correctly invoked and the HZP startup-physics-testing caveat is properly demoted as a non-power-operation regime. The GDC 11 reference (`NRC10CFR50AppA`) and ANS 19.6.1 reference (line 972) are appropriate and correctly placed. The two-regime treatment of `Delta_AB` (positive shadowing dominant 50–500 pcm; anti-shadowing secondary 5–20 pcm distant) at line 908 is calibrated to real Westinghouse 4-loop and EPR measurements. Critically, the proof in C.6.1 (lines 2767–2816) is correct: each of the eight Translate-templates is correctly enumerated against `rho_nonadd`, and the three obstructions O1–O3 (operator-spectrum output, homomorphism-failure, configuration-indexed adjoint) are genuinely independent. This negative result is the most credible cross-domain contribution because the paper exhibits its own framework boundary on its principal domain.

### S2: The Translate-extension taxonomy is well-organised and the five PWR obstructions are properly independent
Table~`tab:five-obstructions` (line 979) cleanly partitions the failure modes: (i) operator-spectrum output not in Y; (ii) homomorphism-failure pi-template; (iii) configuration-indexed adjoint structure on T*; (iv) higher-order mixed-difference pi-templates; (v) two-direction joint parametric dependence. These are not five repackagings of one obstruction. A natural sanity check is the mapping to A_equi (`theory/equi_thm1prime_search.md` §5, lines 267–284): PWR-3 (configuration-indexed adjoint) specialises to gauge-bundle section structure (E2); PWR-4 (mixed-difference) specialises to product-group orbit (E1); the other three (operator-spectrum, homomorphism-failure, joint-parametric) correctly remain inactive on A_equi. This is the kind of cross-domain dimensional analysis that would be impossible if the obstructions were collinear. The decidability and closure preservation discussion in `translate_extensions.md` (lines 27–62) is well-scoped and correctly identifies which extensions trivially preserve Theorem 1/2 (product-group with finite groups; three-valued logic semiring) versus which require non-trivial atlas-finiteness assumptions (gauge-bundle on unbounded M).

### S3: The mathematical framing of the A_equi gauge-bundle counterexample is technically correct
The `rho_gauge` write-up (`theory/equi_thm1prime_search.md` §3.2, lines 125–195) correctly distinguishes "global G-action" from "local fibre-wise H-action on tangent planes T_p M via a gauge field g in C(M, H)". The cocycle compatibility requirement and the parallel-transport transition function `g_{p -> q}` are correctly invoked. The single-block Translate cannot enumerate sections of a principal H-bundle because Definition 4 of the paper enumerates the orbit of a single g in G on a base x_0, not a function-valued parameter (`mathbf{g} in C(M, H)`). The Haan2020GaugeMesh secondary witness on general 3-D meshes correctly strengthens the case: it is not specific to the icosahedral atlas, so it is not absorbed by an "atlas is a single finite group" rejoinder. Similarly the `rho_compose` write-up correctly notes that pre-/post-fix Translate templates for `G_1 = SO(3)` and `G_2 = S_n` separately do not enforce the commutator constraint `f(R P x) = rho(R) f(x)` jointly, so a permutation-rotation interaction bug in the EGNN message-passing layer would slip past both `rho_rot` and `rho_perm` individually. This is the right argument.

### S4: The paper resists rhetorical overclaim through explicit interpretive caveats
The paragraph at line 492 ("A note on prediction (and an interpretive caveat)") is unusual in MT literature and unusually frank: it admits that T* and T_rev* blocks "were themselves curated by inspection of program families that include reactor physics" and that the m_adj / m_rev "prediction" is therefore a "uniform re-projection" rather than de novo physical discovery. The "what is and is not detected: a framework boundary, not an edge case" paragraph at line 719 similarly foregrounds the cat-(i) wrong-sign-loss invisibility as a framework-boundary missing the label-consistency block, not as an "edge case" to wave away. The construct-validity caveat at line 716 explicitly states that the 5/5 cat-(iv) unique detection "exhibits construct validity of `rho_train-rev` ... not NOETHER's superiority on a defect distribution sampled neutrally from real-world bug reports". This kind of self-disclosure is rare and is the right scholarly posture for a framework paper that has not yet been validated across teams.

### S5: The PWR proof methodology is portable: same exhaustion template can be reused for future negative instantiations
The C.6.1 proof structure (enumerate the eight blocks; instantiate the per-block Translate template from Table 2; verify by inspection that no `iota` in `I_s` yields the target MR) is exactly the right shape for falsifying Theorem 1' on any new algebra. The proofs do not depend on PWR-specific details — they depend on the Translate signature alone. This is the kind of methodological contribution that would let third parties run a Theorem-1'-falsification audit on any new program family. The audit pattern is concretely instantiated in `theory/equi_thm1prime_search.md` and `theory/rel_thm1prime_search.md`, which apply the same template across 12 equivariant-ML papers and 12 Calcite test rules respectively. The pattern works.

---

## Weaknesses

### W1: The "three structurally distinct domains" claim is asymmetric — only one is empirically tested, and that one uses a hand-controlled stand-in
**Problem.** The abstract (line 78) and the contributions block claim NOETHER is "instantiate[d] on three structurally distinct domains: a Boltzmann reactor-physics transport solver, ... equivariant machine learning, ... and relational query optimisers". In actual content the three are not comparable in evidential weight:

- §5 Boltzmann instantiation is a mapping exercise against a prior 84-MR catalogue (S2). No new program is tested; the 12-row Table~`tab:elementwise` is "structurally curated" by the paper's own protocol (line 496) and the 18-MR audit (line 498) is labelled by three LLMs that "share substantial pre-training corpora".
- §6 equivariant ML uses a 5189-parameter EGNN stand-in for SE(3)-Transformer / TFN. The paper concedes at line 659 "EGNN carries only invariant scalar and equivariant 3-vector features (type-0 + type-1 in the irrep classification), not the full type-`ell` steerable representation of an SE(3)-Transformer; the T* block instantiation in this case study is therefore an *explicitly added* symmetrised QK probe (equivariant_classifier.py: qk = nn.Parameter(torch.eye(d))) ... not a property of the EGNN architecture itself." The mutations are construct-validity-controlled: cat-(iv) was selected because it targets the T* block that `rho_train-rev` alone covers (line 717). The DeepCrime pilot (n=5) is underpowered: Fisher exact p = 1.00 for both Set N vs Set L and Set N vs Set B (line 755).
- §subsec:third-domain relational query optimisers is not a case study at all — it is a paper-internal classification of 12 Calcite test names (`theory/rel_thm1prime_search.md` §3, lines 100–124). No SQL query is executed; no MR is run on any database; the "145 unverified" Wang2024 cases are not enumerated, they are inferred from the abstract count 444 - 299 = 145 (`rel_thm1prime_search.md` line 30) without a per-case verifier trace.

**Why it matters.** The TOSEM-level claim "the framework transfers across three structurally distinct domains" is read by software-engineering V&V audiences as a multi-domain empirical validation. The actual evidence is: (i) one domain mapping exercise, (ii) one constructed mutation case-study on a stand-in architecture, and (iii) one single-rater literature scan. A reactor V&V team evaluating NOETHER for SIMULATE-3/5 or PARCS verification would conclude that the only domain with engineering-grade evidence is the negative instantiation that *fails* on the framework's intended use. A deep-learning testing team evaluating NOETHER for SE(3)-Transformer testing would not learn whether `rho_adj` (the symmetrised attention trace) or `rho_train-rev` work on a production e3nn / NequIP / MACE pipeline. A database query-optimiser team would not see any executed MR against a real Calcite or CockroachDB workload.

**Suggestion.**
1. Restructure the abstract and Section 1 contributions to read: "instantiated on **one** domain (Boltzmann), demonstrated on **one** compact stand-in (EGNN, with explicit construct-validity caveats), and surveyed on **one** further domain (relational queries, single-rater Calcite-rule classification)". The current framing oversells by a factor of three.
2. If the authors prefer to keep the "three domains" framing, move the relational query subsection to Appendix as a Theorem-1' falsification candidate (which is what `rel_thm1prime_search.md` is) and do **not** count it as a positive instantiation.
3. Commit explicitly to a follow-up that runs Set N on a real SE(3)-Transformer / TFN checkpoint (e3nn 0.5 has trained QM9 and OC20 checkpoints) before any cross-domain superiority claim.

**Severity.** Major.

---

### W2: The §subsec:third-domain Wang2024 / Calcite survey is a single-rater LLM-pattern-matching scan with structural and factual issues
**Problem.** `theory/rel_thm1prime_search.md` is the empirical backbone of the third-domain claim, but on inspection:

(a) **The bibliographic anchor is wrong.** Line 16: "The authors are Shuxian Wang, Sicheng Pan, and Alvin Cheung (*not* 'Sicheng Mao, Boyuan Tang, Junfeng Zhang, Yisu Remy Wang' as the working bib entry reads; see §5 below for a bib-correction note)". The `Wang2024QED` bib entry has wrong author names; this is a citation-integrity issue. Follow-up F1 (line 211) is open. The bib should be corrected before resubmission, not committed as future work.

(b) **The "145 unverified residue" is not enumerated.** Line 75: "A flat enumeration over the unverified 145 pairs is not provided in the QED paper or repository; the unverified set is implicitly defined as 'the 145 cases QED's decider returns inconclusive on at the cited timeout'. We classify a representative sample below based on the Calcite rule's mathematical content." So the 12 classified rules are *not confirmed* to lie in the unverified residue — they are Calcite rules from the *full* QED test directory, which includes both verified and unverified pairs. This is a sampling bias that the paper does not disclose: the 5/12 multi-block-counterexample rate is on rules that may have been *verified* by QED, in which case they are not counterexamples to Theorem 1' at all.

(c) **Single-rater classification by paper author.** No second rater, no kappa, no test-suite execution. Compare to the 18-MR audit at line 498, which at least uses three LLMs and reports Fleiss kappa = 0.857. The third-domain survey uses one rater (the author) without inter-rater agreement.

(d) **The aggregate-as-algebra "ninth block" is asserted without exhaustion proof.** The paper claims `rho_agg-proj` "requires the joint use of B*_rel and an aggregation-as-algebra ninth block not in the current decomposition" (line 849), but no proof exhausts the per-block Translate templates against `rho_agg-proj` (in the way C.6.1 exhausts them against `rho_nonadd`). Follow-up F3 (line 217) acknowledges this is open: "Confirm the formal-proof obligation that `rho_agg-proj` is not single-Translate-derivable from B*_rel alone, by exhausting the per-block templates (analogous to Appendix C.6 in the paper). *Tracked as follow-up.*"

**Why it matters.** §subsec:third-domain's open-question paragraph (line 848) is one of the load-bearing sentences in the paper: "Including the five A_PWR obstructions of Table~`tab:five-obstructions`, the three algebra-survey artefacts ... identify a total of ten pairwise-independent Translate-extension dimensions across the three algebras". The "ten" count is read by reviewers and downstream readers as a falsifiability fingerprint: ten distinct ways the framework can be falsified, surveyed empirically. The actual basis for the rel-side three (E3 aggregate-as-algebra, E4 constraint-aware, E5 three-valued logic) is one paper author classifying twelve Calcite rule names without solver execution and without a confirmed link to the unverified residue. This is weaker than the equi-side two and dramatically weaker than the PWR-side five.

**Suggestion.**
1. Fix the bib entry (Wang/Pan/Cheung) before resubmission.
2. Either (a) run the QED solver on the test suite, log the unverified subset, and re-do the classification with executable evidence; or (b) report the third-domain section as "exploratory single-rater classification" and remove the "ten pairwise-independent extensions" framing from the abstract and Section 1.
3. Provide the C.6-style block-by-block exhaustion proof for `rho_agg-proj` (or downgrade to "candidate" and mark Theorem-1' falsification as conditional on the proof).
4. Add at least one independent rater on the Calcite-rule classification.

**Severity.** Major.

---

### W3: The 84-MR PWR corpus "systematisation" is a re-projection of the same team's prior work, not an independent transfer of tacit knowledge
**Problem.** The paper claims NOETHER deductively reproduces three prior PWR MetaPatterns (P1, P2, P3), refines two (P4, P5), and predicts two (m_adj, m_rev) (Table~`tab:refinement`, line 470). The interpretive caveat at line 494 admits the circularity: "T* and T_rev* were partly induced from reactor-physics structures, and m_adj and m_rev are then derived from those blocks. The framework does not discover these MetaPatterns de novo." The 84-MR corpus itself (supplementary `S2_pwr_corpus/pwr_84mr_full.csv`) is from a prior single-team inductive work (the paper cites it as "a reactor-physics MetaPattern catalogue distilled from the standard PWR-physics literature" at line 468). Inspecting `pwr_84mr_full.csv`:

- Multiple rows are tagged "REASSIGNED from P1 to m_adj per NOETHER §5.3" (e.g. `Bol-Phy-03 Source-detector reciprocity`, `Dif-Phy-14 Diffusion adjoint-flux reciprocity`). The reassignment is from the *same* team's prior taxonomy to the *same* team's NOETHER taxonomy. This is internal re-coding, not external transfer.
- The "triviality" column has values `trivial`, `semi-trivial`, `non-trivial`. The paper does not report what fraction of the 84 MRs are trivial or semi-trivial (a sceptical reader would want to know whether NOETHER's "systematisation" is reproducing the substantive 30% of the corpus or the trivial 70%).
- The independent provenance audit in `independent_citation_provenance.md` (2.8 KB) and `mapping_protocol.md` (6.0 KB) are brief — these are not full per-MR provenance trails.

**Why it matters.** The methodological move "lift induction one level up, from per-MR-sampling to per-algebra-curation" (paper Section 1, line 139) is the central contribution. But the curation of the algebraic blocks is informed by inspection of the same program family the framework is then "applied to". The framework's predictive power on a reactor-physics MR is therefore not a transfer of tacit knowledge from PWR practitioners into a formalism; it is a re-projection of one team's PWR knowledge under a uniform algebraic interface. A PWR core-simulator V&V team would not adopt NOETHER on the strength of this evidence: they would adopt it only after seeing the framework re-derive the 84-MR catalogue from a different team's algebraic specification of MCNP / SIMULATE / PARCS / SMART (i.e., a team that had no input into the eight-block list).

**Suggestion.**
1. Commit to a follow-up where a reactor-physics V&V team independent of the authors specifies A_PWR via a written algebraic description (without seeing the eight-block list) and CONSTRUCT-MP is run on their description. This is the kind of independent-transfer test that would warrant the "systematisation" claim.
2. In the meantime, label the Boltzmann section as "self-consistency check on the upstream-layer curation" rather than as evidence of cross-domain transfer. The current label oversells.
3. Report the trivial / semi-trivial / non-trivial breakdown of the 84-MR corpus and analyse whether NOETHER's predicted MRs are concentrated in the non-trivial subset or are redistributed across all three.

**Severity.** Major.

---

### W4: §6.6 head-to-head reads "competitive parity" while the data show Set N is dominated 26 vs 40 on the pooled substrate
**Problem.** Table~`tab:algebra-rich-pooled` (line 1547) reports Set N = 26, Set G = 40 at GenMorph's published 30-min budget, n = 62, McNemar exact two-sided p = 0.0043. The text at line 1538 reads "competitive parity at the published budget, and it does not support a head-to-head superiority claim". Setting aside the per-SUT pattern (Set N wins `exactLog2` +4 and ties three others; Set G dominates `gcdSig` -5, `lcmSig` -8, `powerSig` -3, `hypotSig` -2), the *aggregate direction* is unambiguous: Set G kills 14 more PIT mutants than Set N at statistical significance, on the head-to-head substrate the authors themselves selected as "algebra-rich Java SUTs". "Competitive parity" is not a faithful reading.

**Why it matters.** The cross-domain narrative is: NOETHER is operator-algebraic and therefore systematically derivable, while GenMorph is GP-evolved and therefore opaque and expensive. The cost-axis claim (H3a.3, line 786) is well-supported: NOETHER is polynomial-time decidable per Theorem 2 while GenMorph is approximately 30-min stochastic GP search per SUT. But the detection-axis claim (H3a.1) is borderline-falsified: Set N's per-block kill rate is *competitive on at least one operative block* (the pre-registered minimum), but on the aggregate head-to-head, Set G dominates. The "competitive parity" framing in the abstract (line 78: "on the scope-matched D1 stratum, Set N is dominated by the GP-evolved baseline (a head-to-head superiority claim is not asserted)") is more honest than the §6.6 body framing, but the body needs to align with the abstract. External-validity readers will trust the body more than the abstract for engineering adoption decisions.

**Suggestion.**
1. Re-frame the §6.6 head-to-head as "GenMorph dominates aggregate kill on the head-to-head substrate; NOETHER's contribution is algebra-derived per-block precision, ex-ante derivability, and cost-axis superiority". This is the honest reading and is consistent with the abstract.
2. Report the McNemar p = 0.0043 and the 14-mutant gap prominently in the body, not just in the table caption.
3. Move "competitive parity" out of the prose at line 1538; it is not what the data say.

**Severity.** Major.

---

### W5: External validity beyond Java methods + Lie-group / self-adjoint program families is asserted broadly without test
**Problem.** The framework's stated scope (§3 introduction, line 78) is "program families that admit an explicit operator-algebraic description through mathematical or physical equations". This is a strong precondition. The case studies cover:

- Java mathematical methods (PIT-mutated, §6.4–6.7 head-to-head): in scope.
- SE(3)-equivariant point-cloud classifiers (§6.6): in scope.
- PWR diffusion solvers (§5, §subsec:negative-pwr): in scope.
- Relational query optimisers (§subsec:third-domain): in scope, but unevaluated empirically.

Out of scope but unmentioned:
- Web applications (HTTP request/response programs without operator-algebraic semantics).
- AI agents / LLM-based systems (e.g. test orchestration agents).
- General compiler-internal optimisations (loop transformations, register allocation) where the algebra is not a Lie group / self-adjoint / time-reversal.
- Distributed systems / consensus protocols where the relevant algebra is CRDT-like rather than the eight-block list.
- General-purpose AI safety testing (e.g. RLHF reward-model verification) where the relevant invariants are statistical / measure-theoretic.

**Why it matters.** TOSEM is read by SE researchers across the full spectrum of test-target program families. The paper's scope precondition correctly disclaims out-of-mathematical-scope program families, but the abstract and introduction read as if the eight-block decomposition is a candidate-universal toolkit. The 18-MR audit's Fleiss kappa = 0.857 (line 498) is on a 18-MR engineering catalogue that is *itself* from reactor physics, so it does not establish breadth across non-mathematical program families.

A PWR core-simulator V&V team: would adopt NOETHER **selectively** — they would adopt CONSTRUCT-MP for the 35-MR Boltzmann enumeration (Appendix C.7 `tab:pmcm-new7`) but would not adopt the framework's stronger Theorem-1' aspirations, which the paper itself shows to be falsified on their domain.

A deep-learning testing team: would adopt NOETHER **conditionally** — they would adopt `rho_rot`, `rho_perm`, and `rho_train` (which they likely already have in some form) but the `rho_adj` (symmetrised attention trace) and `rho_train-rev` (vanilla SGD round-trip) are not validated on production-scale e3nn / NequIP / MACE / SchNet / DimeNet checkpoints. They would not adopt the framework for testing learned reward models, safety classifiers, or LLM-based agents.

A database query-optimiser team: would not adopt NOETHER at all on the current evidence — `rho_agg-proj` is not proven non-derivable from a single block, and the four MRs listed at line 837 (`rho_join-comm`, `rho_select-push`, `rho_distinct-idem`, `rho_plan-equiv`) are already standard practice in differential-query-testing tools (SQLancer, SQLancerPP, DQP). The "complementary" framing at line 845 is correct as a position statement but is not validated.

**Suggestion.**
1. Add an explicit "Out of scope" paragraph in §3 that enumerates classes of program family the framework does **not** target: web applications, RLHF reward models, distributed-consensus protocols, compiler-internal optimisations whose algebra is not in the eight blocks. The current Remark 1 (`rem:counterex`) lists six candidate ninth blocks but does not enumerate domain-level out-of-scope.
2. Soften the abstract's "transferability" claim: "transferable across three structurally distinct *mathematical* operator-algebraic skeletons" rather than "three structurally distinct domains".
3. State explicitly in the Discussion (§9) that the framework's adoption by PWR V&V, equivariant-ML, and database query-optimiser teams is a follow-up empirical question and is not established by the current paper.

**Severity.** Major.

---

## Detailed Comments

### §5 Boltzmann instantiation
- **§5.1 (line 450)** correctly identifies A_Boltz's eight-block decomposition; the assignment B*_rel = empty is correct since transport solvers do not have idempotent-semiring rewriting on solution states.
- **§5.3 Table~`tab:refinement`** is structurally clear but is a re-coding of the same team's prior catalogue under the NOETHER taxonomy. The "REASSIGNED" annotations in `pwr_84mr_full.csv` confirm this. See W3.
- **§5.4 m_adj derivation (line 525)** is methodologically faithful to the Noether-style move (symmetry → conserved current → executable MR). The bilinear form `<phi_dagger, B phi> - <phi, B_dagger phi_dagger>` is correctly identified as the conserved current. The treatment is consistent with Bell & Glasstone §6 adjoint-perturbation theory.
- **§5.5 specialisation (line 542)** correctly contracts T_rev* on diffusion (dissipative) and correctly enriches multiple blocks on burnup (Bateman semi-group). This is technically clean.
- **Concern.** The 18-MR engineering catalogue audit at line 498 uses three LLMs that "share substantial pre-training corpora"; the Fleiss kappa = 0.857 is read by the paper as "almost-perfect" but the kappa formula assumes rater independence, which is approximately violated when raters share training data. The 94.4% subsumption Wilson CI [74.2%, 99.0%] (line 498) is wide enough that the lower bound is consistent with substantial out-of-scope MRs. Suggest reporting per-MR labelling reasoning (which the paper says is in S2 `18mr_audit/`).

### §6 Equivariant ML
- **§6.1 (line 556)** correctly identifies G = SO(3) x S_n as the relevant symmetry group; the assignment of T_att* to the attention-kernel symmetriser is principled.
- **§6.3 rho_rot (line 566)** is the standard rotation-invariance MR; the `tau = 1e-4` tolerance for fp32 is conservative but defensible.
- **§6.4 rho_adj (line 609)** introduces the "symmetrised attention trace" MR. **Verification.** The CI-time formulation (line 614) reads "for architectures whose attention layer exposes a bilinear form A(x_1, x_2) readable through a forward hook". This is correctly stated but is **not** what `equivariant_classifier.py` line 92 does: that file adds a `qk = nn.Parameter(torch.eye(d))` which is then symmetrised in `attention_trace_internal` (line 109: `m = 0.5 * (self.qk + self.qk.T)`). The CI-time MR is therefore tested on an *explicitly added* symmetric Gram-matrix probe, not on the production attention layer of SE(3)-Transformer or TFN. This is acknowledged at line 659 ("the T* block instantiation in this case study is therefore an *explicitly added* symmetrised QK probe ... not a property of the EGNN architecture itself"), but the implication is that `rho_adj` has **not been tested on a production equivariant transformer**. The CI-time-vs-debug-time distinction (line 614 vs 616) papers over this: the case study runs the debug-time variant under the CI-time label.
- **§6.5 rho_train-rev (line 628)** correctly notes that production equivariant pipelines (Allegro, NequIP, MACE, e3nn examples) use Adam / AdamW, on which `rho_train-rev` "fails by construction" (line 637). This is honest. But the framework's predicted scope on training-pipeline testing is then narrow: only vanilla-SGD fixtures, which are not the actual training step of production-grade equivariant ML.
- **§6.6 case study (line 653)** uses a 5189-parameter EGNN. The Set N vs Set L p-values (line 714) are McNemar = 0.063, Fisher = 0.13 vs Set L on detection; the construct-validity caveat (line 716) is correctly stated. The pilot at n=5 (line 736) is underpowered (Fisher exact p = 1.00 for Set N vs Set L and Set N vs Set B); the paper acknowledges this at line 755 ("We do not over-interpret this result"). Good.

### §subsec:third-domain (relational query optimisers, lines 811–850)
- **§subsec:third-domain (line 811)** correctly observes that relational algebra's skeleton is idempotent-semiring, not Lie-group / self-adjoint / time-reversal.
- **The B*_rel claim (line 828)** is appropriate: selection-pushdown, distinct-idempotence, constant-folding are genuinely idempotent-semiring properties.
- **The four MRs at line 837** (rho_join-comm, rho_select-push, rho_distinct-idem, rho_plan-equiv) are correctly identified but are already standard practice in differential SQL testing (SQLancer, SQLancerPP) and in formal query-equivalence checkers (Cosette, HoTTSQL, UDP, QED). The paper acknowledges this complementarity at line 845. **Concern.** The framing "NOETHER provides an algebraically grounded MetaPattern enumeration whose closure under Translate (Theorem 1) is a property the four lines do not establish" (line 846) is correct in principle but is not supported empirically: no experiment shows that NOETHER's MR set detects bugs the four other lines miss, or vice versa. The pre-registered protocol comparison (S6 `query_optimiser/`) is referenced but not executed.
- **The "ten pairwise-independent extensions" sentence at line 849** is the most overclaimed sentence in the cross-domain narrative; see W2. It includes "two of the equi-side dimensions specialising PWR-side dimensions to type-distinct algebraic primitives" which suggests the count is closer to 8 distinct dimensions across the three algebras (5 PWR + 3 rel + 2 equi specialisations), not 10. This is a minor but reproducible miscount.

### §subsec:negative-pwr (PWR negative instantiation, lines 852–1010)
- **The choice of PWR as the negative-instantiation domain** (line 859) is well-motivated: regulatory essentiality and engineering documentability are both correct grounds.
- **The PWR core diffusion algebra (line 862)** is correctly specified; the assignment of O_rod to G as a "commutative semigroup ... to be shown below to fail" is methodologically clean.
- **Definition 15 (line 895)** is physically correct, including the exact-form treatment that avoids first-order perturbation approximation.
- **Definition 17 (line 930)** is physically correct, including the HFP/ARO regime stipulation and the operating-envelope ranges (T_mod in [290, 320]°C, C_B in [0, 2000] ppm). The PWR engineering convention for MTC units pcm/°F is standard; the equivalence pcm/°C is correctly noted.
- **The three-mechanism MTC decomposition (lines 956–959)** is faithful to Stacey §3.4. Mechanism (b) "boron poison evacuation" correctly vanishes as C_B → 0; mechanism (c) "spectrum hardening + U-238 resonance enhancement" is correctly Doppler-weighted by fuel temperature. The competition between (a) and (b) at high C_B is the standard cycle-life MTC-trending mechanism.
- **The GDC 11 monotonicity bound** (line 953, ≤ 0 pcm/°F at HFP per 10 CFR 50 App A) is correctly attributed; the HZP regime caveat (line 953) is appropriate.
- **Tolerance defence (line 944).** `tau_MTC-bor = 0.01 pcm/°F/ppm` is between the empirical magnitude (0.02–0.04) and the simulator noise floor (≈ 0.001), which is the right placement.
- **Appendix C.6.1 proof** (line 2767): the per-block exhaustion is correct. Case s=G correctly identifies (a) operator-spectrum-output, (b) homomorphism-failure obstructions. Case s=O_le correctly identifies the four-point-rectangle obstruction. Case s=T* correctly identifies the configuration-indexed adjoint obstruction. Case s=T_rev* correctly identifies the vacuous emptiness on dissipative PWR diffusion. Cases L*, D*, E*, B*_rel are correctly excluded by template-vs-MR-structure mismatch.
- **Appendix C.6.3 proof** (line 2828): the principal obstruction is correctly localised to O_le (mixed second derivative is a four-point relation along two independent parameter directions). The other-block exclusions are correctly summarised.

### §6.8.2 anti-shadowing (line 908)
- **Anti-shadowing magnitudes 5–20 pcm distant pairs for 4-loop Westinghouse and EPR** (line 908) is calibrated against real PWR rod-worth-measurement data, not against hypothetical small-core or research-reactor regimes. The "more pronounced in small-core or strongly asymmetric insertion patterns" qualifier is correct.

### Appendix C.6 (lines 2762–2884)
- The five-obstruction summary in C.6.5 (`tab:five-obstructions` analogue) is well-organised.
- Remark on Composite Translate (line 2881) correctly states that no single uniform Composite Translate covering all five obstructions has been constructed; this is the open theoretical contribution.

---

## Questions for Authors

1. **(W1, W3 follow-up)** Can the authors arrange for an *independent* reactor-physics V&V team — preferably from a PWR-vendor or national-lab core-simulator group (PARCS at NRC/Argonne, SIMULATE-3/5 at Studsvik, ANC at Westinghouse) — to (a) read the NOETHER framework description without the eight-block list, (b) specify A_PWR for their core simulator independently, and (c) run CONSTRUCT-MP on their specification? This would convert the §5 Boltzmann section from "self-consistency check" to "external transfer test". The paper's "systematisation" claim depends on this.

2. **(W2 follow-up)** Will the authors run the QED solver on the Calcite + CockroachDB test suite, log the actually-unverified subset (i.e., 145 Calcite pairs + 308 CockroachDB pairs, per the Wang2024 abstract), and re-do the third-domain classification on that confirmed substrate, with at least one independent second rater? This would convert §subsec:third-domain from a single-author Calcite-rule classification to a verifiable empirical survey.

3. **(W4 follow-up)** Given the pooled head-to-head outcome (Set N = 26, Set G = 40, McNemar p = 0.0043) on the algebra-rich Java SUTs, is the abstract's framing "Set N is dominated by the GP-evolved baseline (a head-to-head superiority claim is not asserted)" the canonical reading the authors want to commit to? If so, will the body §6.6 (line 1538) be updated to use "Set N is dominated 26 vs 40 on the pooled head-to-head substrate; NOETHER's contribution is per-block precision, ex-ante derivability, and cost-axis superiority" rather than "competitive parity"?

4. **(W5 follow-up)** Can the authors explicitly enumerate three classes of program family the framework does **not** target (e.g. web applications without operator-algebraic semantics; RLHF reward-model verification; general distributed-consensus protocols), to delimit the scope before TOSEM readers attempt to apply NOETHER outside its mathematical operator-algebraic regime? The current scope precondition at line 78 is technically correct but is not operationally restrictive: TOSEM readers will interpret "three structurally distinct domains" as a broader transferability claim than the paper supports.

---

## Minor Issues

### Technical accuracy
- **Line 855**: "the framework's Translate operator cannot reach under any single-block derivation" — confirm "single-block" is the precise scope, not "single-block-first-order" (Definition 4's first-order pi-template is the load-bearing restriction, not just the single-block restriction). The Definition 17 mixed-derivative obstruction is *both* single-block and first-order; the precise statement is more informative.
- **Line 908**: anti-shadowing magnitude attribution: "5-20 pcm for distant bank pairs in 4-loop Westinghouse and EPR configurations" — verify against a specific NRC SER (e.g. ANC for WCAP-9272, PARCS for 50.46c). The Stamm'ler & Abbate reference is appropriate but is a 1983 textbook; modern PWR rod-worth measurements (post-2000 startup physics testing) report more refined numbers and would strengthen the citation.
- **Line 944**: "the empirical value of `partial alpha_MTC / partial C_B` in Westinghouse/Framatome PWR designs ranges over 0.02–0.04 pcm/°F/ppm at BOC-to-EOC cycle conditions" — this is correct for high-enrichment fresh fuel, but for first-cycle low-enriched UO_2 the BOC value can be closer to 0.01 pcm/°F/ppm. Suggest qualifying as "for high-enrichment cycle reloads" or report the cycle-dependent range explicitly.
- **Line 631**: "to leading order in the learning rate eta and in the absence of momentum or noise, time-reversible" — vanilla SGD with batch noise is *not* time-reversible even at leading order; the round-trip identity holds only for full-batch deterministic gradient descent, or for a fixed mini-batch sequence under exact arithmetic. The paper's `rho_train-rev` test uses "same mini-batch sequence in reversed order" (line 640) which is the correct workaround. Suggest the wording at line 631 be tightened to "deterministic full-batch GD" or "fixed mini-batch sequence".
- **Line 614**: "Mainstream equivariant transformers, including SE(3)-Transformer and the Tensor-Field-Network family, compute attention via Clebsch–Gordan tensor products of irrep features. The bilinear form A(x_1, x_2) = <Q(x_1), K(x_2)> is generically not Hermitian" — correct. But: for type-`ell` steerable Q, K features, the inner product is an SE(3)-equivariant pairing of Wigner D-matrices, and the "trace" in `Tr A` requires specifying which irrep summand contributes. The current write-up does not specify the irrep choice. Suggest adding one sentence on which irrep summand's trace is being tested; otherwise `rho_adj` is ambiguous on a TFN with more than one irrep degree.

### Citation Format
- **Line 821**: `\cite{Wang2024QED, Markl2022LearnedQO}` for query-optimiser equivalence — the Wang2024QED bib entry has wrong author list (Wang/Mao/Tang/Zhang/Wang instead of Wang/Pan/Cheung). Fix per `rel_thm1prime_search.md` line 16.
- **Line 911**: `\cite[\S6.3]{BellGlasstone1970}, \cite[\S4.4]{LewisMiller1993}` — verify Bell & Glasstone (1970) is correct edition; the canonical edition is 1970 reprint of 1958 first edition. The paper consistently uses the 1970 attribution which is the standard.
- **Line 905, 944**: tolerances `5 pcm` and `0.01 pcm/°F/ppm` — these should be referenced against ANS-19.6.1 (cited at line 972) which is the standard for cycle-reload qualification noise floors. The 1 pcm convergence tolerance for k_eff iterations is from CASMO-5 / SIMULATE-3 documentation; suggest adding a vendor manual citation.

### Layout
- **Table~`tab:five-obstructions`** (line 979) and Table~`tab:case-study` (line 691): both have the same "double-cell" structure. Consider standardising the column widths for visual consistency.

---

## Dimension Scores

Scored from the R3 cross-domain perspective only. Methodology and statistical rigour are deferred to R1; MT-literature integration is deferred to R2. The scores below weight cross-domain transferability and external validity.

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 78 | Strong | The lift-induction-one-level-up move and the Theorem-1' self-falsification on the framework's principal domain are both genuinely original methodological contributions. The eight-block decomposition itself is a curation that reasonable people could disagree with, but the *methodological pattern* of (block decomposition + Translate + closure under Translate) is novel. |
| Methodological Rigor (25%) | 68 | Adequate-to-Strong | Cross-domain methodology only. The PWR negative instantiation is rigorous (S1, S2). The equivariant-ML case study has good self-disclosure but uses a stand-in architecture with construct-validity-controlled mutations (W1). The relational survey is single-rater, single-pass, and tied to a wrong bib entry (W2). The 84-MR Boltzmann mapping is a self-consistency exercise rather than an independent transfer test (W3). |
| Evidence Sufficiency (25%) | 58 | Adequate | The PWR-side evidence is strong. The equi-side evidence is medium (5189-parameter EGNN, n=5 DeepCrime pilot underpowered, construct-validity-controlled main mutations). The rel-side evidence is weak (single-rater Calcite-rule scan without verifier execution, no MR ever run against a database). The §6.6 head-to-head shows Set N dominated 26 vs 40 (W4). |
| Argument Coherence (15%) | 76 | Strong | The framework's two-layer structure (curated upstream, deductive downstream) is consistently presented. The interpretive caveats at lines 492, 716, 719, 754, 755 are honest. The five-obstructions and ten-extensions structure is well-organised, though the "ten" count is overstated by approximately two when the equi-PWR specialisations are correctly counted (W2 detailed comment). |
| Writing Quality (15%) | 80 | Strong | The paper is unusually well-written for a 76-page TOSEM submission. The "what this subsection establishes and does not establish" pattern (e.g. line 1005) is a model of scholarly disclosure. The minor issues above are mostly editorial. |
| Significance & Impact (R3 optional) | 70 | Strong-to-Adequate | If the framework is adopted as-described, by reactor-physics V&V teams it would provide a principled re-classification (significant but methodologically incremental); by equivariant-ML testing teams it would provide `rho_adj` and `rho_train-rev` for debug-time use (interesting but not production-ready); by database query-optimiser teams it would be a position paper alongside SQLancer / QED (not adopted on current evidence). The cross-domain "lift induction one level up" methodological move is the principal contribution and is impactful at the conceptual level. The "ten pairwise-independent extensions" framing limits significance because it overclaims. |

### Weighted Average
0.20 × 78 + 0.25 × 68 + 0.25 × 58 + 0.15 × 76 + 0.15 × 80 = 15.6 + 17.0 + 14.5 + 11.4 + 12.0 = **70.5**

### Decision
**Major Revision.** The weighted average 70.5 corresponds to the "Major Revision" band in the standard rubric: substantive contribution, but evidential bridges (W1, W2, W3, W4) and external-validity scoping (W5) require restructuring before publication. The recommended revision direction is: (a) tighten the abstract's "three domains" claim to match what the evidence supports; (b) fix the Wang2024QED bib entry and either execute the QED verifier on the test suite or downgrade §subsec:third-domain to an Appendix; (c) align §6.6 head-to-head framing with the McNemar p = 0.0043 dominance; (d) add an explicit out-of-scope enumeration; (e) commit to an independent-team external-transfer test of the PWR systematisation.

---

## Closing Note

The PWR negative instantiation (§subsec:negative-pwr, Appendix C.6) is the most credible cross-domain contribution in the paper and should be defended vigorously. The same physical and mathematical care that produced the five-obstruction analysis is what the equivariant-ML and relational-query instantiations need: empirical execution rather than literature classification. The framework's "lift induction one level up" methodological move is genuinely important, but the present manuscript advertises it as a multi-domain validation when it is, on the empirical side, a one-domain mapping + one stand-in case study + one literature scan. A revision that restores honesty to the cross-domain framing will substantially strengthen the paper without weakening its theoretical contributions.
