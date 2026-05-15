# Peer Review Report

## Manuscript Information
- **Title**: NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
- **Manuscript ID**: TOSEM (anonymised; commit 33db749, branch `feat/section-7-empirical-vs-sota`)
- **Review Date**: 2026-05-15
- **Review Round**: Round 2 polish (post Stage 4.5 integrity verification)

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief (EIC).

### Reviewer Identity
ACM TOSEM Associate Editor on the "Testing & Analysis" track, with prior AE experience handling submissions of the GenMorph (TSE 2024), MR-Scout (TOSEM 2024), and METRIC+ (TSE 2021) family.

### Review Focus
Journal fit for ACM TOSEM; originality and significance relative to METRIC/METRIC+, MR-Scout, GenMorph, GPTMR, and AutoMT; scope, length, and writing at a high level; and whether the contribution is a single coherent paper or should be split. Methodological depth and literature granularity are deferred to R1/R2/R3.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision**
- [ ] Major Revision
- [ ] Reject

### Confidence Score
4 (mostly within my area of expertise; the operator-algebra formalism and Lie-group treatment in §3 and §6.2 sit at the edge of my track and I defer detail-level methodology checks to R1).

### Summary Assessment
NOETHER proposes a two-layer constructive framework that derives MetaPatterns from program-induced operator algebras: a mechanical CONSTRUCT-MP downstream procedure with an algebraic-closure theorem under the `Translate` operator (Theorem 1) and a polynomial-time decidability bound (Theorem 2), paired with an upstream eight-block decomposition stated explicitly as Hypothesis 1. The contribution is instantiated on three structurally distinct domains (Boltzmann reactor-physics transport, equivariant ML, relational query optimisers) and includes a falsifiable $\mathcal{L}^{*}$-blindness prediction tested head-to-head against GenMorph at the published 30-min GAssert budget (§7), plus a negative instantiation on PWR core diffusion that falsifies the stronger Theorem 1' conjecture via two literature-grounded counterexamples (§6.8, Appendix C.6). The paper's foundational ambition, the explicit boundary-of-contribution discipline, and the rare combination of constructive theory with falsification on its own conjecture make it a strong fit for TOSEM's "Methodology" remit. The principal weaknesses are length (76 pages stretches even TOSEM's generous envelope; some material would land better as a companion technical report), and the gap between the framework's stated ambition and its head-to-head evidence (Set N is dominated by Set G on D1 at $p = 0.0043$; the paper now correctly does not assert superiority, but the abstract still has to do a lot of work to keep that boundary visible). I recommend Minor Revision: the contribution is publishable in its current shape with edits to length, abstract, and a handful of high-level positioning issues.

---

## Strengths

### S1: Re-frames a foundational SE problem with rare conceptual clarity
The paper reorganises MR identification around three crisp questions (*Origin*, *Closure*, *Transferability*; §1 lines 120-124) and answers them within a stated scope. This is the kind of programmatic re-grounding that a Methodology track expects but rarely sees. The Noether analogy in §1 line 114 is used carefully and explicitly disclaimed as methodological-only in the same footnote, rather than as a load-bearing technical claim, which is the right move and an unusually disciplined one. METRIC/METRIC+ established the categorical scaffold; the present submission is the first I have seen that asks what would *ground* such a scaffold.

### S2: Boundary-of-contribution discipline is exceptional
Two tcolorbox "Boundary of contribution" panels (§1 lines 141-156, §3 lines 440-442) and a third in the Conclusion (lines 2522-2526) explicitly enumerate what is and is not established. The non-establishment items are non-trivial: (a) absolute completeness, (b) sufficiency of the eight-block list, (c) superiority over SOTA on average, (d) elimination of induction. This is the kind of writing that lets an AE close a file without litigation in revision, and it is rare. The C2 contribution paragraph (§1 line 134) names the five Translate-extension dimensions explicitly, which converts an "open problem" gesture into a concrete agenda.

### S3: The negative instantiation is the paper's strongest move
§6.8 (lines 853-1011) and Appendix C.6 (line 2762 onward) actively falsify the framework's most ambitious stated claim (Theorem 1', absolute completeness) on the framework's principal application domain, using two MRs that are *regulatory-essential* on PWR core simulators (10 CFR 50, NRC RG 1.77; lines 859-860). The five-row obstruction table (Table at line 980) translates the falsification into five pairwise-independent Translate-extension targets. Self-falsifying the strongest stated conjecture, in the same paper, on the framework's home turf, is unusual and increases the work's credibility considerably. Most foundational-frameworks papers in our area do not do this.

### S4: Three structurally distinct domain instantiations, not three relabellings
The three instantiations (Boltzmann §5, equivariant ML §6, relational query §6.7) probe genuinely different algebraic skeletons: Lie-group + self-adjoint + time-reversal for Boltzmann; Lie-group + scaling + training-trajectory for equivariant ML; idempotent-semiring rewriting for relational query. The relational-query block ($\mathcal{B}^{*}_{\mathrm{rel}}$, §6.7 line 812) sits algebraically downstream of the seven physical/mathematical blocks and tests the framework outside its core, which is the right structural stress test. This is materially stronger than a "three case studies in the same algebraic family" composition.

### S5: Falsifiable, pre-registered, *and confirmed* central prediction
§7 (lines 1013-1112) frames an ex-ante $\mathcal{L}^{*}$-blindness prediction derivable from public information (PIT mutator semantics + CONSTRUCT-MP's Translate template) and reports its outcome (5/6 SUTs, robust across a 3 × 3 threshold grid; line 1109). This is the structure-of-science move that most "framework" submissions in our area substitute with a fitted-coverage figure. The threshold and "more-than-one-SUT" quantifier were committed to git *before* the per-MR kill counts (line 1105). A predictor track-record this clean is rare.

---

## Weaknesses

### W1: 76 pages is too long, even for a TOSEM foundational paper
**Problem**: At 3,157 lines of LaTeX source / 76 pages, the manuscript exceeds TOSEM's target range (30-50 pp.) and sits at the upper end of what the journal occasionally accepts for foundational work (~70 pp.). The appendices (C.6 alone runs to ~120 lines of formal proofs, Appendix B is per-MR provenance for 12 representative MRs, Appendix E reports a construct-trace consistency check on hand-crafted mutants) together account for roughly a third of the page budget. The §7 head-to-head + §6.6 case study + DeepCrime pilot + Apache Commons Math pilot also stack four empirical strata into one section, with stratum-specific verdicts that the abstract has to carry simultaneously.
**Why it matters**: For a single paper, the reader has to hold (i) the abstract framework, (ii) three domain instantiations, (iii) a negative instantiation with five Translate-extension obstructions, (iv) a head-to-head SOTA comparison with D1/D2 strata, (v) an LRCA multi-LLM κ check, (vi) a DeepCrime pilot, and (vii) a Commons Math replication pilot. The cognitive load risks burying the foundational contribution under empirical pilots that, individually, are appropriately scoped but collectively read as a separate companion paper.
**Suggestion**: Either (a) move §7's per-block head-to-head (lines 1527-1655) plus the Commons Math pilot (line 2361, External Validity para) to a companion empirical paper, leaving §7 as the $\mathcal{L}^{*}$-blindness test + a one-paragraph reference to the companion; (b) move Appendix B (per-MR provenance) and Appendix E (construct-trace consistency check) to an online artefact and leave a single-page summary in the main file; or (c) accept the 76-page envelope but request that the editor confirm with TOSEM's EiC during the AE handle, which I would not block. My preference is (a) + (b).
**Severity**: Major.

### W2: The abstract is asked to carry too much, including conditional verdicts
**Problem**: The abstract (lines 73-79) runs ~430 words and packs in: the two-layer framing, three domains, the $\mathcal{L}^{*}$-blindness prediction's 5-of-6 outcome, the scope-matched D1 head-to-head verdict ("Set N is dominated by the GP-evolved baseline; a head-to-head superiority claim is not asserted"), the negative instantiation with five Translate-extension obstructions, and the ten-extension cross-algebra count. A reader has to track that Set N is *dominated* on D1, *the framework's contribution is read as algebraic derivability + per-block complementarity + a D2-stratum boundary*, *the central prediction is observed on 5/6 SUTs*, and *Theorem 1' is falsified on PWR*. That is four distinct, partially conditional verdicts in one abstract.
**Why it matters**: Readers will either (a) skim the conditional verdicts and walk away thinking NOETHER does not beat GenMorph (true on D1, misleading without the per-block / D2 / derivability framing), or (b) skim the positive cells and miss the dominance result. Either way the abstract under-protects the paper's actual contribution surface. The project's CLAUDE.md §1.1 explicitly forbids internal `\ref{}` in abstracts and the present abstract does not violate that, but the prose does require the reader to mentally cross-reference §6.6, §7.6, and §6.8 to interpret what is being claimed.
**Suggestion**: Restructure the abstract as Context / Objective / Method / Results / Conclusion (IST/TOSEM-standard structured format), and lead Results with the *one-line headline* that NOETHER's contribution is derivability + closure + falsifiable prediction *confirmed* + Theorem 1' *falsified*, then state in two sentences that the head-to-head against GenMorph is on D1 only (Set N dominated) with per-block complementarity and a D2-stratum framework prediction. Move the ten-extension count into the body; the abstract does not need it.
**Severity**: Major.

### W3: The relationship to METRIC+ and to LLM-prompted baselines could be sharper at the framing level
**Problem**: §2.2 (lines 174-178) correctly identifies that METRIC/METRIC+ leave Origin and Closure unanswered and that Transferability rests on an unstated universality assumption. §6.6 (Case study; lines 653-810) compares against an LLM-prompt baseline (Set L) and a literature baseline (Set B), and §7.6 (head-to-head at GenMorph's budget) compares against the GP-evolved Set G. But a reader unfamiliar with our subfield's history will not immediately see *why* the comparison against GenMorph is the right comparison: GenMorph is GP-evolved, MR-Scout mines from existing tests, AutoMT is multi-agent LLM-RAG, and METRIC+ is a category enumeration scaffold. The four are not commensurable, and §6.6 / §7.6 each pick a different one without an explicit "comparator-selection rationale" paragraph in §2 or §6.
**Why it matters**: An EiC handling this paper has to defend, in the cover letter or decision letter, why GenMorph is the SOTA representative for the D1 head-to-head and why MR-Scout's absence is acceptable. The paper does carry the answer (MR-Scout requires a pre-existing test corpus; GenMorph operates over PIT mutants on Java methods; the D1 stratum is GenMorph's published 23-method benchmark), but the answer is dispersed.
**Suggestion**: Add a short "Comparators and why" paragraph at the top of §6.6 or in §2.4, stating: (i) METRIC+ as the category-scaffold predecessor, mapped in §8.2 (Table at line 2400); (ii) GenMorph as the GP-evolved SOTA, head-to-head in §7.6; (iii) MR-Scout omitted because its mining input (existing test suite) is structurally absent on the framework's scope precondition; (iv) AutoMT / GPTMR omitted because they target safety-critical / traffic-rule domains rather than the operator-algebraic substrate. One paragraph; closes the gap.
**Severity**: Minor (positional, not substantive).

### W4: The framework's "Set N dominated by Set G on D1 pooled" needs an even more visible head-to-head paragraph
**Problem**: §7.6 Table at line 1547 reports pooled D1 Set N = 26, Set G = 40, McNemar exact two-sided $p = 0.0043$ ($n = 62$), and the prose at lines 1538-1546 correctly notes this is "competitive parity at the published budget" and "does not support a head-to-head superiority claim". The framework's contribution is then re-read as algebraic derivability + per-block complementarity (Table at line 1631) + D2-stratum boundary prediction. The reading is defensible, but the headline pooled number — "Set G wins on D1, $p = 0.0043$" — is currently surfaced two paragraphs in, with the framing context after.
**Why it matters**: A skeptical AE or external reviewer will read the table number first and the framing second. The paper's actual claim — that head-to-head on D1 is *the wrong comparison* for an algebra-grounded framework, because the framework's contribution is per-block reach + D2 prediction — needs to land in the lead sentence of §7.6, not three paragraphs in.
**Suggestion**: Rewrite §7.6's lead paragraph (lines 1527-1546) to put the framing first: "On the scope-matched D1 stratum at GenMorph's published 30-min budget, Set N is pooled-dominated by Set G (McNemar exact $p = 0.0043$, $n = 62$); the paper does not assert head-to-head superiority on D1. The framework's contribution is read as (i) algebraic derivability, (ii) per-block complementarity (Set G alone kills 15 D1 mutants Set N misses, Set N alone kills 4 D1 mutants Set G misses), and (iii) a D2-stratum framework prediction (kill rate $\le 10\%$) that no inductive baseline can derive ex-ante. The D1 pooled comparison is reported for protocol-completeness rather than as the framework's verdict." This lifts the framing above the number and makes the abstract's "Set N is dominated by the GP-evolved baseline (a head-to-head superiority claim is not asserted)" sentence easier to land.
**Severity**: Minor.

### W5: §6.8 (negative instantiation) is structurally upstream of §7 (empirical test) but appears after it in the reading order
**Problem**: The negative instantiation (§6.8, lines 853-1011) falsifies Theorem 1' on the PWR core diffusion algebra and identifies five Translate-extension dimensions; §7 (lines 1013-2349) tests the eight-block decomposition empirically via the $\mathcal{L}^{*}$-blindness prediction. Logically, §6.8 is the *upstream* result (it bounds the framework's reach in principle) and §7 is the *downstream* result (it tests the framework's predictions on a particular substrate). The current ordering — §6 instantiations → §6.7 third domain → §6.8 negative → §7 empirical — interleaves three structurally distinct kinds of result (positive instantiations; cross-domain extension; negative instantiation; empirical test) under the §6 header in a way that makes §7's relation to §6.8 hard to read.
**Why it matters**: A first-time reader has to keep track of which sections are establishing closure (§6.1-6.6), which are testing reach (§6.7), which are bounding the framework (§6.8), and which are testing predictions (§7). At 76 pages, the cognitive load of inferring section function from section header is non-trivial.
**Suggestion**: Either (a) renumber §6.8 to §7 and the current §7 to §8 (so the order is: instantiations; cross-domain; negative; empirical), or (b) add a one-paragraph "Roadmap of empirical evidence" panel at the start of §6.6 / §6.7 / §6.8 / §7 stating which kind of result each section establishes. Either fix is light-touch and pre-publication.
**Severity**: Minor.

---

## Detailed Comments

### Title & Abstract
- Title is precise and informative; "Constructive Framework" and "Operator Algebras" together signal the contribution shape correctly. The use of an all-caps acronym (NOETHER) is conventional in TOSEM. No change needed.
- Abstract is too dense; see W2. Specific issues: (i) the sentence "Within this scope, we instantiate NOETHER on three structurally distinct domains..." (line 78) lists three domains in succession without verdict markers, making it hard to read at a glance; (ii) "on the scope-matched D1 stratum, Set N is dominated by the GP-evolved baseline (a head-to-head superiority claim is not asserted), and the framework's contribution is read as algebraic derivability, per-block complementarity, and an out-of-scope D2-stratum boundary that no inductive baseline can derive ex-ante" is the longest sentence in the abstract and carries the most conditional reasoning; this should be broken into two or three sentences, ideally with a Results-block-first structure.
- The abstract correctly avoids internal `\ref{}`; the keyword set (line 105) is appropriate for TOSEM.

### Introduction
- The Origin / Closure / Transferability framing (lines 120-124) is the single best framing in this paper; do not change it. The "we move induction one level up" sentence (line 139) is the most quotable line in the introduction.
- The "Scope of contribution" paragraph (lines 139-156) is the right move for a foundational paper and explicitly disclaims (a)-(d). I would suggest expanding (c) "Superiority over existing automated MR-identification pipelines on average" with one additional sentence noting that the §7.6 D1 head-to-head pooled result is consistent with this non-claim (Set N dominated), so the reader who reaches §7.6's pooled number is not surprised.
- The C1-C4 contribution list (lines 132-137) is well-structured. C2 packs a lot into one bullet (Theorem 1, Theorem 2, Theorem 1' falsification, ten extensions); consider splitting into C2a (positive theory: closure + decidability) and C2b (negative theory: Theorem 1' falsification + ten extensions). At 76 pages, that small structural concession to the reader is worth the four extra lines.

### Literature Review / Theoretical Framework
- §2.4 (lines 188-197) frames the convergent diagnosis correctly: unbounded MR emergence + poor reusability, both following from inductive grounding. The four-line treatment is appropriately compact for a foundational paper whose own contribution is the framework, not the literature audit. I would defer detail-level coverage assessment to R2.
- The omission of MR-Scout from the §7.6 head-to-head (with Set N + Set G only) is noted in §2.3 (line 180), but the reasoning is implicit. See W3 for the suggestion.

### Methodology / Research Design
- High-level only (R1's domain): §3 is the framework's load-bearing section, Theorems 1 and 2 are stated with the right scope (Theorem 1 = closure under Translate over algebra-induced MRs; Theorem 2 = polynomial-time decidability under finite generating set). The "sceptical reading might object that the by-construction status of Theorem 1 makes it near-tautological" paragraph (line 383) is the kind of self-aware caveat that makes the closure result land correctly. R1 will check the per-block instantiations of Translate (Appendix C, line 2685) at detail.
- The Hypothesis 1 / Theorem 1' / Conjecture / Falsification chain is unusual in our literature and is handled responsibly: Hypothesis 1 is empirical, Theorem 1 is proved within its scope, Theorem 1' is conjectured and *falsified* in the same paper (§6.8). I defer the proof correctness to R1.

### Results / Findings
- §6.6 (case study) reports 7/20, 2/20, 0/20 with Wilson 95% CIs that overlap for Set N vs Set L but not for Set N vs Set B (McNemar exact $p = 0.016$, Fisher $p = 0.008$ for N vs B; line 714). The construct-validity-control framing (lines 716-720) is correct: the mutation set was constructed to cover one defect category per non-empty block, so the 5/5 cat-(iv) detection is construct-validity-controlled, not averaged superiority. This framing is honest and the abstract preserves it. R1/R3 will check the statistics; the framing at the §6.6 level is defensible.
- §7 (empirical test) is the cleanest part of the empirical work: 5/6 SUTs confirm $\mathcal{L}^{*}$-blindness, threshold robust across a 3 × 3 grid, prediction committed to git ex-ante. This is the most replicable falsifiable test of the framework's structural claim and earns the section its scaffolding.
- The DeepCrime pilot (§6.6.1, line 733) is correctly framed as $n = 5$ underpowered for $\alpha = 0.05$; the Apache Commons Math pilot (§Discussion External Validity, line 2361) is correctly framed as 3-SUT replication, descriptive only. Both follow CLAUDE.md §1's "C6 small-sample pilot honesty" rule. No issue at the EIC level.

### Discussion
- §8 (Discussion, lines 2350-2511) is well-structured around Wohlin's four-validity framework (line 2355). The LRCA multi-LLM κ result (Cohen's κ 0.927-0.929, Fleiss' κ 1.000 on $n = 33$; line 2359) is reported with the LLM-shared-pre-training caveat. Honest framing.
- §8.2 (METRIC+ relationship, line 2365) is the right placement and the §8.2 sorting-library Table at line 2400 is the most concrete pedagogical exhibit in the discussion. Keep it.
- §8.3 (PMCM coverage reassessment, line 2439) is conceptually important — the 11-to-2 block compression for sorting, and the under-count for Boltzmann — but is buried in the discussion. Consider promoting the §8.3 "deflationary direction" paragraph (line 2442) to a paragraph in §1.

### Conclusion
- §9 (lines 2513-2526) is appropriately concise. The Conclusion's Boundary-of-contribution tcolorbox is a third restatement of the same boundary; consider trimming one of the three (intro, §3, conclusion) to a one-line reference to the others.
- The "most important follow-up work is therefore upstream" sentence (line 2520) is the right closing claim and aligns with the C4 contribution boundary.

### References
- Reference list integrity to be verified by R2 / the project's CLAUDE.md §2 paper-search-MCP audit (per `docs/review_round_polish/round{N}/reference_verification_round{N}.md`). At the EIC level the cited works that anchor the framework (METRIC/METRIC+, MR-Scout, GenMorph, Murphy 2008, Xie 2011, Saha 2019, Shin 2024, Coles 2016 PIT, Humbatova 2021 DeepCrime, Bell & Glasstone 1970, Lewis & Miller 1993, Stamm'ler & Abbate 1983, NRC RG 1.77, 10 CFR 50) all look appropriate. No anonymous companion entries observed in the source I sampled.

### Scope, length, and "single paper or split"
- My assessment: the contribution is a single coherent paper conceptually (the framework + the falsification of its strongest conjecture + the falsifiable empirical prediction are inseparable as a foundational result). The empirical envelope is what stretches the page count. See W1: I recommend moving §7.6's per-block head-to-head + the Commons Math pilot to a companion empirical paper or to extended online material, and trimming Appendices B and E. The framework + Boltzmann + equivariant ML + relational query + PWR negative + $\mathcal{L}^{*}$-blindness test should fit in ~50-55 pages and read as a tighter foundational paper.

---

## Questions for Authors

1. **Length decision.** Would you accept moving §7.6 (per-block head-to-head + Commons Math pilot at the External Validity para of §8.1) to a companion empirical paper, leaving §7 as the $\mathcal{L}^{*}$-blindness test only? If yes, the page count drops to ~50-55 pp. and the foundational contribution lands without the empirical envelope competing for attention. If no, what is the argument for retaining all four empirical strata in one paper?

2. **Abstract restructure.** Are you willing to restructure the abstract along Context / Objective / Method / Results / Conclusion lines, with the headline Result being "framework's central falsifiable prediction confirmed on 5/6 SUTs; framework's strongest conjecture (Theorem 1') self-falsified on PWR" and the D1 pooled head-to-head appearing in a single conditional sentence?

3. **Negative-instantiation placement.** §6.8 (negative on PWR) is logically upstream of §7 (empirical test of eight-block decomposition). Would renumbering — §6.8 → §7, §7 → §8 — clarify the reading order, or do you have a reason for the current sequence I am missing?

4. **MR-Scout / AutoMT comparator absence.** Can you add a one-paragraph "Comparators and why" passage in §2.4 or at the top of §6.6 stating *explicitly* why MR-Scout (mining-based, requires pre-existing test corpus) and AutoMT (multi-agent LLM-RAG, traffic-rule domain) are not in the head-to-head, and why GenMorph is the GP-evolved SOTA representative for the D1 stratum?

---

## Minor Issues

### Language / Grammar
- §1 line 78 (abstract): the sentence beginning "on the scope-matched D1 stratum, Set N is dominated by the GP-evolved baseline..." is the longest in the abstract and the most conditionally structured. Break into two sentences.
- §1 line 134 (C2 contribution): packs four distinct sub-claims (Theorem 1 closure; Theorem 2 decidability; Theorem 1' falsification; ten extensions). Consider C2a / C2b split.
- §6.6 line 720 (framework boundary paragraph): "We do not absorb this case into 'out-of-scope for MR testing' in some over-broad sense; the original motivation..." reads slightly tortured. Consider: "We do not classify this case as out-of-scope for MR testing in general: the original motivation for MR testing is the absence of an oracle, so a label-consistency MR block is a candidate ninth block (Remark on out-of-scope program-family classes), not a domain exclusion."

### Citation Format
- TOSEM uses `acmsmall` natbib style; the source declares `\acmJournal{TOSEM}` correctly. No issues observed at the EIC sample.
- Anonymisation (line 18 `\setcopyright{none}`, line 64 `\author{[Anonymised for Review]}`) is set up correctly for double-blind submission.

### Figures and Tables
- Table 5 (per-block head-to-head, line 1631) carries the load-bearing per-block kill counts; ensure column header "rate (95% CI)" is the Wilson interval (it is per the prose) and add a footnote stating "Wilson 95% intervals" in the caption itself for self-contained readability.
- Table at line 980 (five obstructions) is a clear and well-designed exhibit; do not change.

### Layout
- The Boundary-of-contribution tcolorbox panels (§1 line 141, §3 line 440, §9 line 2522) are three near-identical restatements; consider keeping the §1 and §9 panels and replacing the §3 panel with a one-line "see §1 box and §9 box" reference, to save vertical space without losing the boundary-discipline benefit.
- §7 (lines 1013-2349) is by far the longest section at ~1,337 lines of source / ~32 pp. Consider sub-numbering to ease navigation: 7.1 prediction, 7.2 PIT–block matrix, 7.3 test design, 7.4 central result, 7.5 per-block corroboration, 7.6 head-to-head, 7.7 threats, 7.8 cost, 7.9 evidence summary. The current subsections are largely in this order but the numbering is not strict.

---

## Dimension Scores

Scoring relative to TOSEM "Methodology" track standards (foundational frameworks with empirical confirmation).

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 86 | Strong | Re-grounds MetaPattern discovery in operator algebra, answers Origin/Closure/Transferability questions left open by METRIC+/MR-Scout/GenMorph; the negative-instantiation move (self-falsifying Theorem 1' on the framework's home domain) is original in our literature. Not "Exceptional" only because the upstream layer (eight-block list) remains empirical and the framework explicitly does not eliminate induction, only relocates it. |
| Methodological Rigor (25%) | 80 | Strong | Theorem 1 and Theorem 2 stated with explicit scope; closure-under-Translate not claimed as absolute completeness; falsification of Theorem 1' is methodologically clean (two literature-grounded counterexamples, exhaustion-of-blocks proof). §7's $\mathcal{L}^{*}$-blindness test is ex-ante and threshold-robust. R1 will verify proof detail. Not 90+ because the upstream eight-block list remains Hypothesis 1 (an open empirical hypothesis) rather than a derived structure, and the Translate signature's five-obstruction limitation means closure is provably partial. |
| Evidence Sufficiency (25%) | 78 | Strong | Three structurally distinct domain instantiations, $n = 62$ pooled D1 head-to-head, 5-of-6 $\mathcal{L}^{*}$-blindness confirmation, multi-LLM LRCA κ check (Cohen κ ≈ 0.93, Fleiss κ = 1.000), DeepCrime pilot ($n = 5$, honestly underpowered), Commons Math replication pilot (3 SUTs, descriptive only). Reference set covers the four prior lines and standard PWR safety-analysis literature. Not 85+ because the head-to-head against GenMorph is on a single Java-method benchmark family (D1 = 8 SUTs, $n = 62$ post-equivalent-mutant exclusion), MR-Scout and AutoMT are not in the head-to-head, and the framework's transfer claim across program-family algebras is supported by three instances, not a population. |
| Argument Coherence (15%) | 84 | Strong | The Origin/Closure/Transferability framing carries the paper end to end; Boundary-of-contribution panels enforce coherence between contribution and evidence. Two minor incoherences: (i) §6.8 (negative) appears after §6.7 (third domain) but is logically upstream of §7 (empirical test); (ii) the abstract has to do conditional verdict-bookkeeping that the body handles in dedicated sections. Both are positional, not substantive. |
| Writing Quality (15%) | 80 | Strong | Precise terminology, careful disclaimer of the Noether analogy as methodological, disciplined use of "we do not claim" language. The 76-page envelope strains paragraph-level pacing in §7 (a 32-page subsection competes with the framework section for the reader's attention). Per CLAUDE.md §1.7, no em-dash; spelling consistency British throughout; sentence case in titles (sampled). Not 85+ because of length-induced pacing issues in §7 and the abstract density (W2). |
| Literature Integration (optional, R2 focus) | 78 | — | Defers to R2. |
| Significance & Impact (optional, R3 focus) | 85 | — | Defers to R3. The foundational re-grounding has clear potential to influence subsequent MetaPattern catalogue work, METRIC-style scaffolding, and LLM-assisted MR generation (recast as algebra-conditioned generation per §9). |
| **Weighted Average** | **81.2** | **Accept** (boundary) | $(86 \times 0.20) + (80 \times 0.25) + (78 \times 0.25) + (84 \times 0.15) + (80 \times 0.15) = 17.2 + 20.0 + 19.5 + 12.6 + 12.0 = 81.3$. |

The weighted average (81.3) lands in the Accept band ($\ge 80$). I nonetheless recommend **Minor Revision** rather than direct Accept, because (i) the length issue (W1) and the abstract density (W2) materially affect the paper's readability and reception at TOSEM's target page range, and (ii) the head-to-head framing (W4) and the negative-instantiation placement (W5) are pre-publication light-touch edits that improve the paper's defensibility. None of the weaknesses rise to Major Revision: the contribution, its scope discipline, its evidence base, and its self-falsification on Theorem 1' are all already in place. The Minor Revision changes are editorial (length, abstract, ordering, one new "Comparators and why" paragraph) rather than substantive.

---

## EIC Summary Statement

NOETHER is the most ambitious foundational paper on metamorphic-relation identification I have handled in two cycles. It does what METRIC+/MR-Scout/GenMorph collectively do not: it re-grounds MetaPattern discovery in an algebraic structure, proves closure within an explicit scope, *self-falsifies* its strongest stated conjecture on its principal application domain, and reports a falsifiable empirical prediction that is confirmed on 5/6 SUTs. The recommendation is Minor Revision, with attention to length (W1), abstract restructure (W2), head-to-head framing (W4), and negative-instantiation placement (W5). The contribution is a clean fit for the TOSEM "Methodology" remit.
