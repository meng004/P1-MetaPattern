# Cover Letter — NOETHER submission to ACM TOSEM

**Date**: 2026-05-16
**Target venue**: ACM Transactions on Software Engineering and Methodology
**Track**: Testing & Analysis
**Submission category**: Foundational research paper
**Manuscript**: NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
**Pages**: 75 (declared, see §3)
**Companion artefacts**: supplementary S1–S9 (algorithm reference impl, PWR corpus, case-study harness, reproducibility scripts, GenMorph pilot, query-optimiser instantiation, Defects4J substrate, Sun 2021 METRIC+ subjects with PIT+Major dual-tool replication, migrated appendices)

---

Dear Editor-in-Chief and Handling Editor,

We respectfully submit *NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras* for consideration in the Testing & Analysis track of ACM TOSEM. The manuscript is original work, has not been submitted elsewhere, and is not under consideration by any other venue. The supplementary code and data are provided for review and will be released publicly upon acceptance.

## 1. What the paper does

Metamorphic Testing has matured into a standardised software-testing technique (IEEE/ISO/IEC 29119, 2022) and is increasingly recommended for AI systems. Its central limitation is **metamorphic relation (MR) identification**: the bottleneck of deciding *which* properties hold for a program under test. The literature has responded at the application and integration layers (mining, evolutionary search, LLM-prompted methods) but the **foundational layer** — what makes one MR set algebraically adequate, and how MR sets transfer between domains — has not advanced at the same pace.

NOETHER addresses this foundational layer by deriving MetaPatterns from the **operator-algebraic structure** of the program family under test. Given an operator algebra $\mathcal{A}_P$ and its eight-block decomposition (Hypothesis 1), the CONSTRUCT-MP algorithm produces a MetaPattern set $\mathbb{M}(\mathcal{A}_P)$ with two formal guarantees:

- **Theorem 1 (algebraic closure)**: $\mathbb{M}(\mathcal{A}_P)$ is closed under the framework's *Translate* operator over the algebra-induced MR space $\mathrm{MR}(\mathcal{A}_P)$.
- **Theorem 2 (polynomial-time decidability)**: CONSTRUCT-MP runs in polynomial time under a finite generating set.

The paper's central methodological contribution is therefore a **two-layer framework**: an *upstream layer* (algebra distillation and eight-block decomposition, stated as an explicit empirical hypothesis with documented out-of-scope cases) and a *downstream layer* (the construction algorithm, deductive and provable). The upstream layer is honest about its empirical grounding; the downstream layer is mechanical.

## 2. Six headline messages

1. **Two-layer framework with positive *and* negative theory.** Theorem 1 and Theorem 2 are the positive theory; Theorem $1'$ (the strictly stronger absolute-completeness conjecture, $\mathbb{M}(\mathcal{A}_P)$ closed over arbitrary properties expressible in $\mathcal{A}_P$) is **falsified** on the PWR core diffusion algebra $\mathcal{A}_{\mathrm{PWR}}$ via two pairwise-independent counterexamples (non-additivity of rod-bank reactivity worth; second-order mixed dependence of $k_{\mathrm{eff}}$ on moderator temperature and boron concentration). The five Translate-extension dimensions from this falsification, together with five candidate dimensions from companion surveys on the equivariant-ML and relational-query algebras, identify ten Translate-extension directions as the principal locus of follow-up work. The constructive negative result is part of the paper's contribution, not a limitation.

2. **Three structurally distinct instantiations.** NOETHER is instantiated on three operator-algebraic domains: Boltzmann reactor-physics transport (the framework systematises a prior inductive catalogue and re-classifies further equivalence classes); equivariant machine learning (executable MRs are derived for rotation invariance, adjoint duality, and training-trajectory reversibility); and relational query optimisers (whose idempotent-semiring algebra exercises the relational-equivalence block beyond the Lie-group / self-adjoint / time-reversal core).

3. **Honest empirical disclosure on the §6.6 head-to-head.** On the scope-matched D1 stratum at GenMorph's published 30-min GAssert budget, Set N is *dominated* by Set G in the aggregate (McNemar exact $p = 0.0043$ pooled; $p = 0.019$ on D1 only). The paper does not assert head-to-head superiority. The framework's contribution is read at three layers — algebraic derivability, per-block complementarity, and an out-of-scope D2-stratum boundary that no inductive baseline can derive *ex-ante*. The framework's central falsifiable prediction (the $\mathcal{L}^{*}$-blindness pattern on homogeneity-preserving mutators) holds 5/6 on the in-scope substrate, derivable from public information without consulting kill data.

4. **METRIC+ comparison on Sun's own published corpus (Path A).** We pre-registered a head-to-head protocol against the most directly comparable inductive prior art, METRIC+ (Sun et al., 2021), using Sun et al.'s own 4 published subjects (SPHONE / SBAGGAGE / SEXPENSE / SMEAL) and executed it at three layers: a Python reduced-scale ($n = 219$ mutants), a Java + PIT 1.7.4 substrate ($n = 120$ mutants; same tool as the body paper's §6.6), and a **Major + JDK 11 cross-tool replication** ($n = 555$ mutants; independent operator catalogue $4.6\times$ larger than PIT). Both tools deliver the same qualitative verdict at $\alpha = 0.05$ (pooled McNemar exact $p = 0.625$ for PIT, $p = 0.211$ for Major; both NS), and Major's larger pool exposes *bidirectional* per-subject reach asymmetries (Set MP exclusive reach on SPhone; Set N exclusive reach on SBaggage) that *cancel pooled* — the strongest possible empirical evidence for the framework's "complementary not competitive" reading. The pre-registered $H_{\mathrm{MP1}}$ (subsumption either direction) is falsified in *both* directions per-subject, which is論點-strengthening rather than論點-weakening.

5. **Methodological transparency at four explicit layers.** (a) Pre-registration: the $\mathcal{L}^{*}$-blindness prediction and its outlier-handling rule, the SUT-selection criterion, and the Path A protocol are all committed to git before the corresponding data was collected. (b) Failure-mode audit: Stage 4.5 Round 5 caught and corrected a Mode 1 + Mode 3 finding (Fisher exact $p = 1.0$ was a column-degenerate misuse of `scipy.stats.fisher_exact`; corrected to McNemar exact $p = 0.500$). (c) Construct-trace circularity acknowledged: the §6.x case study's H2 verdict is by-construction within case-study scope; the Appendix-E (now supplementary S9) construct-trace check is design-implied and not used as independent fault-detection evidence. (d) Scope-precondition discipline: the framework's scope is explicitly programs admitting an operator-algebraic description; four classes (web applications, RLHF reward models, distributed-consensus protocols, compiler-internal optimisations) are stated out-of-scope by construction.

6. **Reproducibility.** All claims map to scripts in supplementary S1–S9. The dual-tool METRIC+ replication completes in ≈ 5 seconds wall-time (Major) plus ≈ 5 minutes (PIT 1.7.4) on a stock Java 8 + Maven + JDK 11 toolchain — reviewers can replicate the head-to-head end-to-end. The 84-MR PWR corpus, the 18-MR audit's Fleiss $\kappa = 0.857$ inputs, the Apache Commons Math pilot's per-mutant kill matrix, and all per-subject category-choice specifications used in the Path A enumeration are committed to the experiment repository.

## 3. Length declaration

The manuscript is 75 pages in `acmart` manuscript single-column mode, which exceeds the TOSEM 30–50 page recommendation. We respectfully ask the EIC to consider this submission under the foundational-paper category, where the length is justified by the following structural breakdown:

| Section | Pages | Why load-bearing |
|---|---|---|
| §1–§4 framework + formal preliminaries | ~16 | Theorems 1, 2 and the construction algorithm |
| §5–§6 three instantiations (Boltzmann, equi-ML, RDB) | ~24 | Each tests a distinct algebraic skeleton; deletion would forfeit C4 transferability |
| §7 empirical $\mathcal{L}^{*}$-blindness test + head-to-head | ~22 | Pre-registered prediction + per-block + cost-axis + D2-prediction layers; tables are the load-bearing evidence base for H3 |
| §8 discussion + METRIC+ comparison + scope | ~7 | METRIC+ comparison is the most-requested reviewer item (Path A) |
| §9 + Appendix C proofs (C.1–C.6) | ~6 | Theorem 1' falsification's five-extension per-block exhaustion proof — load-bearing for the negative theory |

Six illustrative appendices (A, B, C-worked, C.7, D, E) totaling ~10 pp. have already been migrated to supplementary S9 to compress; the remaining 75 pp. is what each section requires to support its specific contribution. We are happy to discuss further reductions with the EIC if needed.

## 4. Differentiation from related prior art

NOETHER's positioning relative to four closest references:

| Prior art | Relationship |
|---|---|
| **METRIC+ (Sun et al., 2021)** | Inductive 11-pair D×R category catalogue; NOETHER provides the algebraic-warrant downstream layer to METRIC+'s inductive upstream layer; complementarity quantified at instance level via Path A Tier 3+/3++ (supplementary S8) |
| **Zhou et al., 2020 (TSE 46:10) SymmetryMRP** | Single-pattern instance of NOETHER's $G$-block; NOETHER subsumes via uniform 8-block decomposition |
| **Ying et al., 2025 family-tree formalism** | Inductive pattern hierarchy; NOETHER provides the algebraic warrant for each family-tree node admitting an operator-algebraic specification (§2.4) |
| **GenMorph (2024)** | GP-evolved MRs at GAssert's published budget; NOETHER offers polynomial-time deterministic derivation in place of stochastic search; complementary on the per-block reading (§6.6 + Table tab:per-block-headtohead) |

## 5. Suggested handling editor and reviewers

The track's existing handling editors with theory-of-testing or metamorphic-testing background would be the natural fit. We have no conflicts of interest to declare; should the EIC identify potential COIs with our affiliations, we are happy to provide our institutional disclosure separately.

## 6. Closing

We acknowledge that NOETHER's contribution is **systematisation**, not deduction from first principles — induction is *relocated* from MR-instance level to algebra-block level rather than eliminated. We believe this re-grounding is a productive direction for the metamorphic-testing community, and we have prepared the submission with four rounds of self-review (5-reviewer panel + Devil's Advocate + Stage 4.5 integrity audit + cross-tool replication) and explicit transparency on every methodological choice.

We thank you for considering this work, and we look forward to your editorial decision.

Sincerely,
[Author list to be inserted per double-blind policy at submission time]

---

## Appendix to Cover Letter — Highlights (≤ 85 chars per bullet, in case the venue accepts the IST-style summary)

1. NOETHER derives MetaPatterns from operator-algebraic structure of program families.
2. Theorem 1: algebraic closure of the MetaPattern set under Translate; poly-time decidable.
3. Theorem 1' (absolute completeness) falsified on PWR core diffusion algebra.
4. Three instantiations: Boltzmann reactor physics, equivariant ML, relational queries.
5. METRIC+ head-to-head on Sun 2021's corpus with PIT+Major dual-tool concordance.

(Each line is ≤ 85 characters; verified by `awk '{ print length, $0 }' highlights.md`.)
