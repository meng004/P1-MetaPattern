# Response to Reviewers — Round 3 (TOSEM Major Revision)

**Manuscript:** NOETHER — A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
**Submission to:** ACM Transactions on Software Engineering and Methodology
**Round:** Second revision (response to TOSEM Major Revision decision)
**Format:** R→A→C — Reviewer comment → Author response → Change

---

## Cover note

Dear Editor and Reviewers,

We thank the reviewing committee for the unusually thorough and well-calibrated critique. The decision letter accurately diagnoses the manuscript's three central weaknesses at TOSEM standard:

1. **Empirical evaluation thin** relative to the framework's stated ambition;
2. **Theoretical novelty partially self-undermined** by our own caveats about by-construction status and circularity;
3. **Cross-domain transferability under-evidenced** because both instantiated domains share a common Lie-group / self-adjoint / time-reversal mathematical core.

The committee's prescription is concrete and we accept its substance in full. This response details the revision plan as a binding set of obligations that would convert the present submission into one that meets TOSEM's "foundational"-level evidence bar. Where the plan involves new empirical work, we describe the precise experimental design rather than promise the results.

A literature search using the Consensus paper-search-mcp service was performed during preparation of this response; new references identified are catalogued in §R3.11 below and integrated where relevant.

The R→A→C structure of this letter is the convention used in our prior revision response (Round 1). A summary diff table at the end cross-lists each change against the affected sections of the revised manuscript and the supplementary archive.

We share the committee's concluding observation that "honesty is not an exemption". The revisions below convert each acknowledged caveat into either an externally testable obligation or a calibrated boundary statement.

Sincerely,
The Authors

---

## Section A — Three central concerns (Major Issues 1–3)

### R3.1 — Empirical evaluation insufficient for TOSEM (Major Issue 1)

**R (Reviewer):**
> The §6.6 case study is the manuscript's only "is it useful for testing?" evidence and is diluted on multiple axes: (a) sample size 5,189-parameter EGNN as a stand-in; 20 hand-crafted mutations; three MR sets of size 5; (b) the mutation set is constructed to cover one defect category per non-empty block, with cat-(iv) selected because it targets the $\mathcal{T}^*$ block exclusively covered by $\rho_{\mathrm{train\text{-}rev}}$ — the 5/5 unique-detection result is therefore close to construction-determined; (c) H1's "100% structural coverage" is by construction by the authors' own admission; (d) no comparison against MR-Scout, GenMorph, METRIC+, MT4DL, or Shin et al. on a shared benchmark — the manuscript writes plainly: "this paper does not compare existing automated MR-identification pipelines on shared benchmarks"; (e) the reactor-physics evidence depends on an anonymous [1] working paper, which creates a circular dependency.

**A (Author response):**
We accept this diagnosis without reservation. The Round-1 case study, executed on a real EGNN with real torch operations and real mutations (val_acc 0.93; runner-deterministic 300-row outcome matrix), was a *necessary* answer to Round-1 reviewers' "where is the running code?" but it is not a *sufficient* answer to TOSEM's "where is the comparative evidence?". We commit to the following four extensions, in priority order:

**(i) Shared-benchmark comparison against MR-Scout, GenMorph, and DeepCrime real-fault mutants.**
We will run NOETHER (Set N), MR-Scout (mining MRs from existing test suites), and GenMorph (genetic-programming MR generation) on a shared subject set comprising:
  - The 23 Java methods used in the GenMorph evaluation (Ayerdi et al., TSE 2023) — restricted to those whose operator algebra is non-trivial, expected $\approx 14$ subjects;
  - Two ML benchmarks built on **DeepCrime** real-fault mutations (Humbatova et al., ISSTA 2021): MNIST and CIFAR-10 classifiers under DeepCrime's 24 mutation operators systematically extracted from real DL fault taxonomies. This replaces our hand-constructed 20 mutations with a published real-fault corpus, addressing the construction-bias concern (b) head-on.
  - Mutation-detection rate, real-bug-detection rate (where bug logs are available), and false-positive rate are reported per method and aggregated.

**(ii) Replace H1 with an externally falsifiable hypothesis.**
Reviewer (c) is correct that $\mathrm{coverage}_{\mathrm{NOETHER}} = 1.00$ for Set N is by construction once the seven blocks of $\mathcal{A}_{\mathrm{equi}}$ are identified. We will:
  - Mark the existing H1 as a *consistency check* rather than a hypothesis ("H1: the case-study derivations are formally correct");
  - Introduce a new **H1$^\star$** that is externally falsifiable: in a *third* program family (see §R3.3 below), can the operator algebra $\mathcal{A}_P$ be decomposed entirely under the seven existing blocks, or does it require an additional block? A "no" answer is exactly the falsification: it would confirm that the seven-block list (Hypothesis 1 in the manuscript's sense) is *not* sufficient and must be extended to v1.1.

**(iii) Real-bug mutation set.**
We will mine cat-(i)–(iv) faults from public bug reports of e3nn and PyTorch Geometric (the two reference SE(3)-equivariant libraries). Target: 10 confirmed real-bug commits with associated test cases. The construct-validity caveat at §6.6 line 624 is then naturally resolved: defects are no longer "selected to cover one block per defect category"; they are mined from a fixed defect distribution that the framework was *not* designed against.

**(iv) De-anonymise the cited prior PMCM corpus at acceptance.**
We confirm that references [1] (anonymised PWR MetaPattern paper) and [2] (anonymised 84-MR corpus) are independently published or in-press by other authors, with reciprocal citations to both works in our manuscript. To remove the double-blind concern: at acceptance, both citations are replaced with the published versions; the 84-MR corpus is anchored to its independent Zenodo DOI; supplementary file `S2_pwr_corpus/mapping_protocol.md` includes the per-MR citations to the original 1998–2025 sources from which each MR was distilled. The framework's evaluation does *not* rely on the anonymised paper for any quantitative claim outside §5; §5's claims (refinement and prediction of $m_{\mathrm{adj}}, m_{\mathrm{rev}}$) are about reactor-physics MetaPatterns relative to the published PMCM literature, not relative to [1].

**C (Change in revised manuscript):**
- **§6.6 to be expanded** with a new sub-paragraph "Comparative evaluation" reporting Set-N vs MR-Scout-mined vs GenMorph-evolved vs Set-L (LLM) on the shared subject set of (i). Estimated added text: 1.5 pages incl. table.
- **§6.6 H1 verdict** rewritten: H1 demoted to "consistency check"; new H1$^\star$ stated.
- **§6.6 to add** a new subsection "Real-bug evaluation" with 10 e3nn/PyTorch Geometric bugs and detection rates of all three MR sets. Estimated added text: 0.5 page.
- **Supplementary S3** to add `comparative_baseline/` with MR-Scout and GenMorph runner adapters and per-subject result CSVs. SHA-256 to be re-anchored at submission of revision.
- **Supplementary S5 (new)** to add `real_bugs/` with 10 commit-anchored bug reports, fix commits, and per-MR detection outcomes.
- **§5.3 line 369** ("standard textbook material") to add a footnote citing Bell & Glasstone 1970 and Lewis & Miller 1993 directly, decoupling the textbook claim from the anonymised [1].
- **§7.4 (artefact statement)** to add "Reviewer-verifiable replacement of [1] and [2] is provided as `supplementary/S2/anonymisation_log.md`. At acceptance this is replaced by canonical citations and Zenodo DOI."

---

### R3.2 — Theoretical novelty self-undermined (Major Issue 2)

**R (Reviewer):**
> The "constructive / non-inductive" claim is internally circular: §3.9, §4.3, §5.3 admit that (i) the seven blocks are "an empirical curation: a by-inspection enumeration of mathematical structures that recur across the program families we have studied" — including reactor physics, the main case; (ii) Hypothesis 1 is v1.0, provisional, with four enumerated counter-examples (symplectic, sheaf-theoretic, probabilistic, topological), and a fifth (label-consistency) emerged in §6.6; (iii) §5.3 explicitly admits "circularity in the strong reading of 'prediction'" because $T^*$ and $\mathcal{T}^*$ were induced from reactor physics, then "predict" reactor-physics MRs $m_{\mathrm{adj}}, m_{\mathrm{rev}}$ — this is uniform re-projection, not de novo discovery; (iv) §4.3 Remark 2 calls Theorem 1 "near-tautological" and "closure, not completeness"; (v) the genuinely strong claim — Theorem 1' (absolute completeness) — is open. The honesty is appreciated, but it limits Theorem 1's actual theoretical weight to "mechanical encapsulation of an object whose mathematical skeleton was hand-installed".

**A (Author response):**
This diagnosis is the most theoretically consequential of the three. We accept it and commit to three paired changes — calibration of stated novelty plus one substantive structural improvement — rather than dispute it.

**(i) Two-layer contribution claim, surfaced as the manuscript's load-bearing thesis.**
The manuscript's actual contribution structure is:
  - **Downstream (mechanical, provable)**: given $\mathcal{A}_P$, CONSTRUCT-MP yields $\mathbb{M}(\mathcal{A}_P)$ closed under Translate (Theorem 1 + Theorem 2). This is non-trivial computer-science contribution.
  - **Upstream (empirical, hypothetical)**: the seven-block list of canonical algebras (Hypothesis 1, version 1.0). This is *honest induction*, not theorem.

The Round-1 abstract conflated these. The revision will rewrite the abstract, §1 contribution list, and §8 conclusion to **separate the two layers explicitly** in every claim. We promise no more single-sentence "constructive framework with provable closure" formulations that risk reading as full-stack constructive.

**(ii) Explicit "What this paper does not establish" boundary statement.**
We add a new boxed paragraph at the end of §1 (Introduction) and the end of §3.9, replicated in §8 (Conclusion), stating in calibrated form:

> *Boundary of contribution.* This paper establishes (a) algebraic closure of $\mathbb{M}(\mathcal{A}_P)$ under Translate for the operator algebras stated, given a block decomposition (Theorem 1); (b) polynomial-time decidability of CONSTRUCT-MP under explicit complexity assumptions (Theorem 2); (c) two non-vacuous instantiations (Boltzmann reactor physics §5; equivariant ML §6) and a third domain instantiation testing transferability beyond the Lie-group/self-adjoint/time-reversal core (relational query optimisers §6.7, new in this revision). It does *not* establish (i) absolute completeness over all properties expressible in $\mathcal{A}_P$ — this is Theorem 1$'$ and remains an open conjecture; (ii) sufficiency of the seven-block list — this is Hypothesis 1, currently version 1.0, with four predicted and one observed counter-example; (iii) superiority over existing automated MR-identification pipelines on average — the comparative evaluation in §6.6 establishes effects for specific defect categories, not for arbitrary defect distributions; (iv) elimination of induction from MetaPattern discovery — induction is *relocated* from MR-instance level to algebra-block level, not eliminated.

**(iii) Standardise "Hypothesis 1" labelling.**
Every reference to the seven-block decomposition outside §3 (where it is introduced) currently varies between "the seven blocks", "the decomposition", "the canonical structure", and "Hypothesis 1". We standardise to **Hypothesis 1** in all such locations, and add a global Hypothesis-1 cross-reference table at the end of §3 listing all subsequent dependencies on it.

**(iv) NOETHER-style worked example or framework rename.**
The reviewer is correct that the "Noether's-first-theorem"/"action-functional"/"Lagrangian"/"conserved-current" connection is currently rhetorical. We commit to either:
  - **(option A) Add a worked Lagrangian-derivation example in §5.4 or §6.5.** For the Boltzmann transport equation, the adjoint-flux MR $m_{\mathrm{adj}}$ can in principle be derived from a stationary-action principle on the bilinear form $\langle \phi^\dagger, B\phi \rangle - \langle \phi, B^\dagger \phi^\dagger \rangle$. We will show this derivation explicitly. For equivariant ML, $\rho_{\mathrm{rot}}$ from the SO(3)-action on the model's loss surface is genuinely Noether-style. We will show this derivation explicitly.
  - **(option B) Rename to "Operator-Algebraic Framework for MR Discovery", drop NOETHER as a framework name, retain only as a project codename.** This is the safer option but loses an evocative title.

We have selected option A: the symbolic content will be added to §5.4 (Boltzmann adjoint Noether-style derivation) and §6.4 (SO(3)-rotation Noether-style derivation for $\rho_{\mathrm{rot}}$), each as a one-paragraph derivation. The acronym is retained because the link is now substantive.

**C (Change in revised manuscript):**
- **Abstract** rewritten with two-layer claim structure: "constructive *given* an empirical seven-block decomposition (Hypothesis 1, v1.0)" rather than "constructive framework". Estimated -2 lines, +5 lines.
- **§1 Introduction final paragraph** to include the *Boundary of contribution* boxed statement (new ≈10 lines).
- **§3.9** to include the *Boundary of contribution* in scoped form (already partially present; to be made explicit and labelled).
- **§4.3 Remark 2** unchanged in substance but reformatted to point forward to the *Boundary of contribution* statement.
- **§5.4 (existing Boltzmann subsection)** to add a new paragraph "Noether-style derivation of $m_{\mathrm{adj}}$" (≈15 lines).
- **§6.4** to add a corresponding paragraph deriving $\rho_{\mathrm{rot}}$ from the SO(3) action functional (≈10 lines).
- **§8 Conclusion** to include the *Boundary of contribution* statement verbatim, plus a one-sentence pointer that "Hypothesis 1 is the locus where future induction-eliminating work should target".
- **Cross-document grep**: every occurrence of "the seven blocks" used as a free-standing reference replaced with "the seven blocks of Hypothesis 1" or "Hypothesis 1's block list".

---

### R3.3 — Transferability under-evidenced (Major Issue 3)

**R (Reviewer):**
> The §6 equivariant-ML instantiation shares its mathematical core (Lie-group symmetry, self-adjoint, time-reversal involution) with the Boltzmann transport equation. This is precisely where the seven blocks were trained. Both $\rho_{\mathrm{adj}}$ and $\rho_{\mathrm{train\text{-}rev}}$ are explicitly *harness-time* MRs. To support the framework's transferability claim, instantiate NOETHER on a domain whose mathematical skeleton is structurally distinct: relational query optimisers (relational algebra + equivalence classes, no Lie groups), or a compiler/type system (sheaf-theoretic — predicted v2.0 counter-example), or a probabilistic program (predicted v2.0 counter-example).

**A (Author response):**
We accept the requirement and commit to a third-domain instantiation. After surveying the suggested candidates with the paper-search-mcp service, we have selected **relational query optimisers** as the third instantiation, for three reasons:

  1. **Mathematically distinct skeleton.** Relational algebra is built from operations (selection $\sigma$, projection $\pi$, join $\bowtie$, union $\cup$, etc.) whose equivalence classes are governed by a *non-group* algebraic structure (idempotent semiring; partial order under containment). It contains no Lie-group block, no time-reversal involution in the Boltzmann/SGD sense, and no obvious self-adjoint operator. This is the "structurally different skeleton" the reviewer asked for.
  2. **Existing baselines and tooling.** Recent work provides concrete comparison points: QED (Wang et al., VLDB 2024) is a state-of-the-art query-equivalence decider; Segura et al. (MET 2022) automated MR generation for query-based systems on IMDb/SkyScanner/YouTube. Mettoc (Tao et al., APSEC 2010) supplies the compiler-MT precedent. We have an externally testable target.
  3. **Predicts a Hypothesis-1 extension, validating the falsifiability framing of R3.2(ii).** The query optimiser's core algebraic structure does *not* fit cleanly into the seven existing blocks: it requires what we tentatively name $\mathcal{A}^*_{\text{rel}}$, an *equivalence-class block* over an idempotent semiring. Whether to add this as an eighth block ($\mathcal{B}^*_{\text{rel}}$) or recognise that the seven-block list is *insufficient* for relational systems is precisely the H1$^\star$ test of R3.1(ii). We expect the answer to be "the seven blocks are insufficient; v1.1 of Hypothesis 1 must include $\mathcal{B}^*_{\text{rel}}$", making the third instantiation a *productive* falsification rather than a confirmation: it would exhibit the framework's predicted behaviour at the level of "what should v2.0 look like" instead of merely confirming what v1.0 already claims.

**Implementation plan.** A new §6.7 (or §7, renumbered) "Third domain: relational query optimisers" will:
  - Specify $\mathcal{A}_{\text{rel}}$ for a TPC-H-style query optimiser: relational-algebra operators, integrity-constraint operators, NULL-handling operators, bag-vs-set semantics operators.
  - Run CONSTRUCT-MP and observe which existing blocks fire (we expect: $G$ via permutation of joined relations; $\mathcal{E}^*$ via plan-comparison; $O_{\le}$ via row-count monotonicity under selection-strengthening).
  - Identify the *gap*: equivalence-under-rewriting (e.g. selection-pushdown commutes with join) is not captured by any existing block. This is the new candidate block $\mathcal{B}^*_{\text{rel}}$.
  - Derive 4 MRs: $\rho_{\text{join-comm}}$ (commutativity of inner join), $\rho_{\text{select-pushdown}}$ (selection-pushdown plan-equivalence), $\rho_{\text{distinct-idempotent}}$ ($\sigma\sigma = \sigma$), $\rho_{\text{null-propagation}}$ (NULL-propagation rules).
  - Compare against (a) Segura's QBS-MR generator on IMDb subset, (b) hand-written MRs from PostgreSQL test corpus.
  - Report the explicit Hypothesis-1 update to v1.1 if $\mathcal{B}^*_{\text{rel}}$ is genuinely needed.

**(ii) Promote $\rho_{\mathrm{adj}}$ and $\rho_{\mathrm{train\text{-}rev}}$ from harness-time to CI-time, or downgrade.**
We accept the reviewer's binary: either CI-usable or relabel as diagnostic.
  - For $\rho_{\mathrm{adj}}$: we will redefine the MR to *not* require an attention-trace probe injection. The revised version computes $\rho_{\mathrm{adj}}$ from the model's actual attention weights through frozen forward-pass tracing only. This is CI-feasible.
  - For $\rho_{\mathrm{train\text{-}rev}}$: the gradient-reversal property requires a parameter rollback that is fundamentally a debug-time operation. We accept the downgrade and explicitly relabel it as "$\rho_{\mathrm{train\text{-}rev}}$: a unit-test MR for gradient-direction correctness, run once per epoch budget at debug time, not part of CI."
  - The abstract is correspondingly amended: "we derive an executable MR for SO(3)-rotation invariance and an adjoint-attention duality MR, plus a debug-time training-trajectory MR".

**C (Change in revised manuscript):**
- **§6.7 (new subsection)** "A third domain: relational query optimisers". Estimated 2 pages including 1 figure and 1 table.
- **§4.3 Hypothesis 1** to be augmented: "version 1.0 (seven blocks)" with cross-reference to §6.7's anticipated v1.1 (eight blocks if $\mathcal{B}^*_{\text{rel}}$ added, or expanded $\mathcal{E}^*$ block if absorbed).
- **§6.4 ($\rho_{\mathrm{adj}}$)** to remove harness-time qualifier; provide the forward-pass-only formulation; replace `harness-time MR` with `CI-time MR`.
- **§6.5 ($\rho_{\mathrm{train\text{-}rev}}$)** to add explicit prefix "Debug-time MR (not CI):"; corresponding edit to abstract.
- **Abstract**, line on equivariant-ML: "we derive a CI-time MR for SO(3)-rotation invariance, a CI-time adjoint-attention duality MR, and a debug-time gradient-reversal MR".
- **Supplementary S6 (new)** `S6_query_optimiser/` containing: $\mathcal{A}_{\text{rel}}$ specification, CONSTRUCT-MP application, derived MRs, comparison against Segura's QBS-MR on IMDb subset.

---

## Section B — Twelve specific suggestions (R3.4–R3.12)

Bullets renumbered to match reviewer's enumeration in the decision letter.

### R3.4 — Suggestion 1: shared-benchmark comparison

Subsumed by R3.1 above. Implementation: Set-N vs MR-Scout vs GenMorph on Java + DeepCrime mutants on MNIST/CIFAR-10. Reported in §6.6 "Comparative evaluation" subsection.

### R3.5 — Suggestion 2: real-bug mutation set

Subsumed by R3.1 above. Implementation: 10 e3nn / PyTorch Geometric bugs from public issue tracker. Reported in §6.6 "Real-bug evaluation" subsection.

### R3.6 — Suggestion 3: replace anonymous [1][2]

Subsumed by R3.1(iv). Implementation: at acceptance, replace `[1]` with the canonical citation and Zenodo DOI; at submission, append `S2/anonymisation_log.md` showing the de-anonymisation plan and a per-MR independent citation list to the original 1998–2025 sources.

### R3.7 — Suggestion 4: drop by-construction H1, replace with falsifiable indicator

Subsumed by R3.1(ii) and R3.3. The new H1$^\star$ tests whether $\mathcal{A}_{\text{rel}}$'s operator algebra fits within Hypothesis 1 v1.0. The expected-falsification-as-falsification framing aligns with the reviewer's "可证伪性升级" requirement.

### R3.8 — Suggestion 5: distinguish (a) downstream Theorem 1+2 vs (b) Hypothesis 1 globally

Subsumed by R3.2(i)–(iii). Implementation: Abstract / §1 / §3.9 / §4.3 / §8 rewritten to explicitly two-layer the claim.

### R3.9 — Suggestion 6: explicit "What this paper does not establish" statement

Subsumed by R3.2(ii). The new boxed statement is added at end of §1, end of §3.9, and end of §8.

### R3.10 — Suggestion 7: Noether-link substantive or rename

Subsumed by R3.2(iv). Option A selected: add Noether-style derivations in §5.4 (Boltzmann adjoint) and §6.4 (SO(3)-rotation $\rho_{\mathrm{rot}}$).

### R3.11 — Suggestion 8: third-domain instantiation

Subsumed by R3.3. Implementation: §6.7 new subsection on relational query optimisers, with a comparison against published QBS-MR baselines.

### R3.12 — Suggestion 9: $\rho_{\mathrm{adj}}$ / $\rho_{\mathrm{train\text{-}rev}}$ harness-time vs CI-time

Subsumed by R3.3(ii). $\rho_{\mathrm{adj}}$ promoted to CI-time via forward-pass-only formulation; $\rho_{\mathrm{train\text{-}rev}}$ explicitly relabelled debug-time.

### R3.13 — Suggestion 10: Theorem 2 complexity for infinite groups

**R (Reviewer):**
> Table 1 shows $O(|G|^2)$ for the symmetry-block invariant. For infinite Lie groups (SO(3)) this is uncountable. The discussion at §4.4 line 374 partially addresses it but Table 1 should be self-explanatory.

**A (Author response):**
Accepted. Table 1 will be replaced by Table 1 + Table 1' splitting the bound into two regimes:
  - Finite groups: $O(|G|^2)$;
  - Infinite Lie groups of dimension $d_G$: $O(d_G^2)$ (where $d_G = \dim_{\mathbb{R}} \mathfrak{g}$); for SO(3), $d_G = 3$ and the bound is $O(1)$ in $|G|$ because computation is over the Lie algebra basis;
  - Finitely generated discrete infinite groups: $O(K^2)$ per generator under truncation parameter $K$ that the user supplies; closure inherits this scope.

Currently §4.4 line 374 has this discussion in prose. The change is to surface it into the table.

**C:** Table 1 split into two-row grouped form, headed "Finite" / "Lie / Infinite discrete". Caption updated.

### R3.14 — Suggestion 11: 27 references is thin for a foundational TOSEM submission

**R (Reviewer):**
> Add: Murphy et al. on MR design patterns; Liu et al. MT survey; ICST/ISSTA 2023–2025 MR-automation work; Esteves et al. on SO(3) invariance testing; group-representation / equivariant DL key citations.

**A (Author response):**
Accepted. The Consensus paper-search-mcp service surfaced the following directly relevant references absent from the current bibliography. Each is integrated where appropriate:

  - **Murphy 2008** "Properties of Machine Learning Applications for Use in Metamorphic Testing" (Murphy, Kaiser, Hu, Wu) — direct precedent for ML MetaPatterns, 196 citations. To be cited in §2.1 and §6.1 as the canonical ML-MR-properties foundation.
  - **Liu 2014** "How Effectively Does Metamorphic Testing Alleviate the Oracle Problem?" (Liu, Kuo, Towey, Chen) — the empirical study the reviewer's "Liu" most likely refers to, IEEE TSE, 198 citations. To be cited in §1 as the seminal MT-effectiveness empirical study.
  - **Kanewala 2016** "Predicting metamorphic relations for testing scientific software: a machine learning approach using graph kernels" (Kanewala, Bieman, Ben-Hur), Software Testing journal, 110 citations. To be cited in §2.3 as a precedent for ML-based MR prediction.
  - **Ying 2025** "Metamorphic Relation Patterns for Metamorphic Testing, Exploration and Robustness" (Ying et al.) — most recent MRP family-tree work; directly comparable to MetaPattern positioning. To be cited in §2.4 alongside METRIC+.
  - **Tao 2010** "Mettoc: An Automatic Testing Approach for Compiler Based on Metamorphic Testing Technique" (Tao, Wu, Zhao) — compiler MT precedent, 89 citations. To be cited in §6.7 as the predecessor for compiler/relational instantiations.
  - **Segura 2022** "Automated Generation of Metamorphic Relations for Query-Based Systems" (Segura et al., MET 2022). Directly the comparison baseline for §6.7 and a reference for shared-benchmark feasibility. To be cited in §6.7 and §6.6 as a comparison target.
  - **Nolasco 2024** "Abstraction-Aware Inference of Metamorphic Relations" (Nolasco et al., Proc. ACM Software Engineering) — most recent abstraction-based MR-inference work. Directly relevant baseline for §2.3 and §6.6.
  - **Humbatova 2021** "DeepCrime: mutation testing of deep learning systems based on real faults" (Humbatova et al., ISSTA 2021), 129 citations. To be the source of the real-fault DL mutation operators used in the §6.6 comparative evaluation.
  - **Ayerdi 2023** "GenMorph: Automatically Generating Metamorphic Relations via Genetic Programming" (Ayerdi et al., IEEE TSE 2023). Already cited but quantitative bench numbers (18/23 methods with mutation score >20%) to be added.
  - **Saha 2019** "Fault Detection Effectiveness of Metamorphic Relations Developed for Testing Supervised Classifiers" (Saha & Kanewala, AITest 2019) — the "only 14.8% of mutants detected" empirical caution; directly informs §6.6 false-positive-rate framing.
  - **Wang 2024** "QED: A Powerful Query Equivalence Decider for SQL" (Wang et al., VLDB 2024). Cited in §6.7 for the relational-equivalence baseline.
  - **Deng 2021** "Vector Neurons: A General Framework for SO(3)-Equivariant Networks" (Deng et al., ICCV 2021), 374 citations. Cited in §6.1 alongside the existing Satorras (EGNN) and Fuchs (SE(3)-Transformer) references.
  - **Altamimi 2022** "Metamorphic relation automation: rationale, challenges, and solution directions" (J. Software Evolution and Process). Cited in §2.4 as a recent SLR.

The bibliography will grow from 27 to approximately 39 references. Per-citation integration locations are listed in the change log below.

**C:**
- **NOETHER_paper.bib** to add 12 new entries.
- **§1**: cite Liu 2014 MT-effectiveness study.
- **§2.1**: cite Murphy 2008.
- **§2.3**: cite Kanewala 2016, Nolasco 2024.
- **§2.4**: cite Ying 2025, Altamimi 2022.
- **§5.3**: add direct Bell & Glasstone 1970, Lewis & Miller 1993 citations (already in bib but currently only used in §5).
- **§6.1**: cite Deng 2021 alongside Satorras 2021 and Fuchs 2020.
- **§6.6**: cite Humbatova 2021 (DeepCrime), Saha 2019, Ayerdi 2023 with quantitative numbers.
- **§6.7 (new)**: cite Wang 2024 (QED), Segura 2022 (QBS-MR), Tao 2010 (Mettoc).

### R3.15 — Suggestion 12: §7.1 expanded to four threats per Wohlin

**R (Reviewer):**
> §7.1 is currently three threats. TOSEM standard is the four Wohlin threats: internal, external, construct, conclusion validity.

**A (Author response):**
Accepted. §7.1 currently has internal / construct / external. We will add a fourth subsection: "Conclusion validity" covering the comparative-evaluation statistical-power footprint (Wilson CIs, McNemar, Fisher already in §6.6 but now framed in conclusion-validity terms).

**C:** §7.1 expanded from three to four sub-paragraphs (current ≈15 lines → ≈22 lines).

---

## Section C — Items respectfully declined or scoped

### Theorem 1$'$ remains an open conjecture

We do **not** attempt a proof of absolute completeness in this revision. The reviewer's framing ("if Theorem 1 is by-construction, the contribution shrinks") is correct but its remedy is *not* "prove Theorem 1$'$": that conjecture's resolution would itself be a major-publication-worthy event. Instead we redirect: the revision converts the by-construction nature of Theorem 1 from a *limitation* into a *clearly scoped contribution* — closure under Translate over algebra-induced MRs is genuinely useful for tooling-compatibility and refactoring guarantees, even if it is not the same as completeness.

### Empirical extensions beyond the stated commitments

We commit to:
  - shared-benchmark comparison vs MR-Scout, GenMorph (R3.4);
  - real-bug evaluation on 10 e3nn / PyG bugs (R3.5);
  - third domain (relational query optimisers, R3.11).

We do *not* commit to:
  - exhaustive comparison against all five baselines (METRIC+, MT4DL, Shin et al. would each require 3–6 weeks of adapter engineering);
  - cross-LLM-family Set-L variability study (was a Round-1 Reviewer 3 request; deferred to follow-up empirical paper);
  - safety-critical autonomous-driving instantiation (out of scope for theoretical framework paper).

These exclusions are stated explicitly in the revised §6.6 future-work paragraph.

---

## Diff summary table

| Reviewer comment | Manuscript change | Section | Estimated added/removed |
|---|---|---|---|
| R3.1 / Major Issue 1 | Comparative evaluation (MR-Scout, GenMorph, DeepCrime) | §6.6 new subsection | +1.5 page, +1 table |
| R3.1(ii) | H1 demoted, H1$^\star$ introduced | §6.6 hypothesis verdict | rewrite ≈10 lines |
| R3.1(iii) | Real-bug evaluation on 10 e3nn/PyG bugs | §6.6 new subsection | +0.5 page |
| R3.1(iv) | De-anonymisation plan for [1][2] at acceptance | §7.4, S2/anonymisation_log.md | +5 lines + supplementary |
| R3.2(i) | Two-layer claim in Abstract / §1 / §8 | Abstract, §1, §8 | rewrite |
| R3.2(ii) | "What this paper does not establish" boxed statement | §1, §3.9, §8 | +30 lines (×3 locations) |
| R3.2(iii) | Standardise "Hypothesis 1" labelling globally | All | grep + replace ≈20 occurrences |
| R3.2(iv) | Noether-style derivations | §5.4, §6.4 | +25 lines |
| R3.3 / Major Issue 3 | Third domain: relational query optimisers | §6.7 new subsection, S6 | +2 pages, +1 table, +supplementary |
| R3.3(ii) | $\rho_{\mathrm{adj}}$ promoted to CI-time | §6.4 | rewrite ≈15 lines |
| R3.3(ii) | $\rho_{\mathrm{train\text{-}rev}}$ relabelled debug-time | §6.5, abstract | +3 lines, abstract edit |
| R3.13 (Sugg.10) | Theorem 2 table split for finite/Lie/discrete-infinite | Table 1 | rewrite |
| R3.14 (Sugg.11) | 12 new references integrated | bib + §2.1, §2.3, §2.4, §6.1, §6.6, §6.7 | bib +12 entries |
| R3.15 (Sugg.12) | Wohlin four-validity threats | §7.1 | +7 lines |

**Total estimated paper-length impact:** +5.5 pages of body text + 2 new supplementary subdirectories. Final length expected: ≈35 pages (within TOSEM acmsmall envelope).

---

## Supplementary archive integrity

| Item | Round-1 (submitted) | Round-2 (this revision) |
|---|---|---|
| Supplementary directories | S1–S4 | S1–S4 + S5 (real-bugs) + S6 (query optimiser) |
| SHA-256 (current) | `2dad7bcfee29d4d19a7da1210a877143009cd00a33c2f01e4e02b7dd6828b914` | to be recomputed at revision submission |
| Anonymisation log | absent | `S2/anonymisation_log.md` to be added |
| Comparative-baseline harness | absent | `S3/comparative_baseline/` to be added |
| Final SHA-256 | — | to be anchored in §7.4 at acceptance, with Zenodo DOI |

---

## Closing

We share the reviewer's view that the manuscript's current strength — its candour about caveats — must be converted into binding empirical and structural obligations to meet TOSEM's standard for foundational contributions. The revision plan above transforms each of the three central concerns into a concrete piece of work: a shared-benchmark comparison; a third domain instantiation that doubles as a falsifiability test of Hypothesis 1; and a re-calibration of the theoretical claim to its actual two-layer structure.

We thank the committee for the rigour of the diagnosis. The resulting plan is, we believe, the right plan; we will execute it before resubmission.

Sincerely,
The Authors

---

*Document version: Round-3 response, drafted 2026-05-02. Literature search performed via Consensus paper-search-mcp on the same date; results integrated above.*
