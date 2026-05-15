# Peer Review Report

## Manuscript Information
- **Title**: NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
- **Manuscript ID**: TOSEM submission (commit `ceac6ed`)
- **Review Date**: 2026-05-15
- **Review Round**: Round 3 (EIC, post Stage 4 + Stage 3' + Stage 4.5)

---

## Reviewer Information

### Reviewer Role
Editor-in-Chief Associate Editor, ACM TOSEM "Testing & Analysis" track

### Reviewer Identity
TOSEM EIC handling editor. Twenty-plus years of editorial experience on
software-testing track manuscripts; routinely arbitrates length / scope /
positioning decisions for foundational submissions; not a domain specialist
in operator algebras, reactor physics, or equivariant ML (defers methodology /
domain depth to R1, R2, R3). Focused on journal fit, gate-keeping, and
whether the manuscript is ready for production handling.

### Review Focus
Five EIC-scope questions: (1) Is 80 pp. defensible against TOSEM's 30-50 pp.
target, or must the manuscript split? (2) Is the ~574-word abstract
publishable, or should it be tightened / IST-restructured? (3) Does the
foundational positioning (Theorem 1 + Theorem 2 + Theorem 1' falsification +
three instantiations + L*-blindness 5/6) read as one coherent paper or as
two stapled papers? (4) After two rounds of revisions, do abstract / §1 / §4 /
§subsec:third-domain / §6.6 carry consistent framing? (5) What three to five
messages should the cover letter highlight for EIC handling?

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [x] **Minor Revision** — Length and abstract are the only EIC-scope blockers; both are fixable without methodology changes.
- [ ] Major Revision
- [ ] Reject

### Confidence Score
**4 / 5** — EIC-scope decisions on length / abstract / positioning are
squarely within editorial purview; methodology and domain claims are
deferred to R1-R3. I am confident on (1)-(2)-(4)-(5) and moderately
confident on (3).

### Summary Assessment
The paper introduces NOETHER, a two-layer framework that derives MetaPatterns
from a program's operator algebra: an upstream eight-block decomposition
(Hypothesis 1) plus a downstream constructive algorithm with a
provable algebraic-closure theorem (Theorem 1) over the algebra-induced MR
space and polynomial-time decidability (Theorem 2). A strictly stronger
absolute-completeness claim (Theorem 1') is falsified on the PWR core
diffusion algebra by two independent counterexamples that identify five
pairwise-independent extensions of `Translate`, with five further candidate
extensions surveyed on the equivariant-ML and relational-query algebras,
totalling ten Translate-extension dimensions as the principal open
problem. Three instantiations (Boltzmann reactor physics, equivariant ML,
relational query optimisers) and a falsifiable L*-blindness prediction
confirmed on five of six SUTs anchor the empirical layer. The Round 2
issues raised by the prior cycle (C1 tautology, C2 engineered-extension,
C3 post-hoc rescue, C4 D1 re-framing, C5 augmented-stratum circularity)
have been substantively addressed at the level of framing, scope, and
disclosure; the central remaining EIC-scope concerns are length (80 pp.
versus TOSEM's 30-50 pp. target) and abstract density (~574 words versus
the 250-400 sweet spot), neither of which threatens the science but both
of which threaten production handling. My recommendation is **Minor
Revision** conditional on a structured abstract rewrite and a length plan
that the authors choose between two clean options.

---

## Strengths

### S1: Foundational positioning is now coherent rather than stapled
After Round 2's framing revisions, the C1-C4 contributions list (L132-138)
plus the Boundary-of-contribution box (L142-156) plus the Conclusion
restatement box (L2701-2705) form a single argumentative arc: Theorem 1
(scoped closure) + Theorem 2 (decidability) + Theorem 1' (falsified on
PWR) + three instantiations + L*-blindness prediction (confirmed 5/6).
The paper reads as one foundational claim with multiple supporting
instantiations, not as four loosely coupled papers. Internal cross-references
between abstract claims, §1 contributions, §3.3 Theorem 1 substantive
content (L432), §subsec:third-domain Theorem 1' verdict (L903-904), and
§9 Conclusion are now traceable and consistent.

### S2: Round 2 critical findings are addressed at the framing level
Round 2 DA's five CRITICAL findings have visible resolutions in the
current draft. C1 (Theorem 1 tautology): explicitly acknowledged at L432
("A sceptical reading might object that the by-construction status... we
acknowledge that the closure result is by-construction within the explicit
scope of Definition `def:alg-induced`") and converted to a structural-
adequacy obligation rather than oversold. C2 (engineered "10 extensions"):
five PWR-side dimensions are proven by per-block exhaustion; five candidate
dimensions on equi / rel algebras are explicitly labelled as
"asserted by inspection rather than by formal exhaustion proof, full
per-dimension exhaustion proofs are committed as follow-up" (L135 and
L152). The "10" total is now a properly distinguished 5-proven plus
5-candidate count rather than a uniform claim. C3 (L*-blindness post-hoc
rescue): subsec:l-blindness-derivation now states the prediction
ex-ante from algebra + PIT mutator specification (L1095+), git-commits
the prediction (L2134-2146), and the 5/6 verdict (L1440-1471) follows
the pre-stated falsification criterion. C4 (D1 dominated): abstract
(L78) and §6.6 (L1604-1619) lead with "Set N is dominated by Set G on D1"
without re-asserting superiority. C5 (augmented-stratum circular):
explicitly demoted in L1700-1711 and L2041-2048 as "construct-trace
consistency check ... not used as independent fault-detection evidence
in this section's H3a verdicts".

### S3: Honesty in disclosure exceeds journal norms
The Boundary-of-contribution boxes (§1 L142-156, §4 L489-491, §9
L2701-2705) state both what is established and what is not. The
"deflationary direction" case in subsec:reactor-mapping L546 explicitly
flags the prediction-circularity caveat ("There is therefore a
circularity in the strong reading of `prediction'... we acknowledge..."),
and the over-counted-undercounted distinction is documented in
subsec:pmcm-worked (L2618). Pilot sample-size disclosures
("n=5 underpowered for α=0.05", "n=3 SUTs", "n=17 underpowered for
α=0.05 inferential test") are stated throughout rather than hidden
in footnotes. For a journal that frequently sees over-claimed
foundational papers, this disclosure quality is a positive signal.

### S4: Falsifiable prediction is genuine and well-tested
The L*-blindness result is the paper's strongest empirical chapter: a
quantitative prediction (kill rate near zero on homogeneity-preserving
mutators, falsifiable if a single MR kills ≥ 1/3 mutants on more than
one SUT, L1465-1471) was derivable ex-ante from the algebra plus the PIT
mutator specification, the falsification criterion was stated before the
data, and the observed result (5/6 SUTs confirm at the strongest reading,
1 outlier on a SUT containing two documented homogeneity-breaking
mutators) is consistent with the prediction including its quantitative
tail. This is the clearest piece of foundational-paper evidence in the
manuscript and would survive aggressive Reviewer 2 scrutiny.

### S5: Negative instantiation is structurally rather than rhetorically deployed
§subsec:negative-pwr (L907+) uses NOETHER's principal application domain
(reactor physics) to falsify the framework's most ambitious claim
(absolute completeness), and the choice is justified on regulatory
essentiality and engineering documentability grounds (L915). Two
counterexamples ($\rho_{\mathrm{nonadd}}$ for rod-bank reactivity worth,
$\rho_{\mathrm{MTC\text{-}bor}}$ for second-order mixed dependence) are
proved not Translate-reachable, the obstructions are localised to five
pairwise-independent dimensions in `Translate`'s signature
(Table 9 L1034-1067), and pairwise independence is established by
per-block exhaustion (Appendix C.6). This converts an open conjecture
into a falsified statement with structurally informative
follow-up direction, which is rare and valuable for a foundational paper.

---

## Weaknesses

### W1: Length materially exceeds TOSEM's target band, and the natural split point is not exploited
**Problem**: 80 PDF pages (3348 LaTeX lines, 603 KB). Main body runs
pages 1-62; appendices A-E run pages 62-75; References ~75-80. TOSEM's
target is 30-50 pp.; up to ~70 pp. is occasionally accepted for
foundational work. 80 pp. is in the territory where the AE typically
either (a) requests a split before sending out for review or (b) asks for
a defended length-reduction plan. The §6.6 head-to-head occupies
roughly L1601-2386 (~785 lines, ~16-18 PDF pages by itself) and
constitutes a self-contained empirical chapter with its own threats
section, cost matrix, per-block decomposition, LLM-ensemble baseline,
DeepCrime real-fault pilot pointer, and Apache Commons Math
cross-codebase pilot. It is logically severable from the foundational
theorems and the three instantiations.

**Why it matters**: At 80 pp. the manuscript will (1) draw automatic
length pushback from production handling, (2) burden Reviewer 1
(methodology) and Reviewer 2 (domain) with a substantially larger reading
load than they expect, and (3) dilute the foundational message (Theorem 1
+ Theorem 2 + Theorem 1' + three instantiations + L*-blindness) under
the weight of an empirical chapter that is, by the author's own
admission (abstract L78 "Set~N is dominated by the GP-evolved baseline"),
not a head-to-head superiority claim. Foundational papers benefit from
being read as foundational; empirical heft beyond what is needed to
support the theorems is a liability.

**Suggestion**: Two clean options the cover letter can offer.
*Option A (preferred)*: Split into a foundational main paper (~55 pp.)
+ a companion empirical paper. The main paper retains §1-§5 (Boltzmann),
§6.1-§6.5 (equivariant-ML, third domain, negative-PWR), §7
(L*-blindness, the falsifiable prediction confirmed 5/6), §8-§9. The
companion takes §6.6 head-to-head + §6.6.1 DeepCrime pilot + Apache
Commons Math cross-codebase pilot + §7.7 MR-generation cost matrix. The
foundational paper then runs ~55 pp. (within TOSEM tolerance), and the
companion stands as ~25 pp. empirical study suitable for TOSEM short
paper or for ICSE/ISSTA. The cross-references can be maintained as
forward references to the companion paper, which is standard practice.
*Option B*: Retain a single paper but compress §6.6 to ~6 pages by
demoting the LLM-ensemble baseline tabulations, the MR-generation cost
matrix sub-sub-paragraphs, and the Apache Commons Math pilot to the
supplementary; keep only the per-block head-to-head table and the H3a
verdict split in the main body. With aggressive compression and
appendix consolidation, the paper can plausibly reach 65-70 pp.

The author's choice between A and B should be defended in the cover
letter. My editorial preference is A; the foundational story is
strong enough to stand on its own without the empirical chapter.

**Severity**: Major (EIC-scope; not a methodology defect, but a
production-handling blocker at the current page count).

### W2: Abstract density is publishable but lossy; structured reformatting recommended
**Problem**: Abstract (L73-78) is ~574 words by rough count (TOSEM
abstracts more commonly run 200-350 words; the journal does not
formally enforce a cap, but the median is ~300). The current abstract
carries: (1) the field framing (MT / MR identification bottleneck), (2)
the three foundational gaps (origin / closure / transferability), (3)
the framework description (two layers, CONSTRUCT-MP), (4) Theorem 1
scoped statement, (5) Theorem 2 decidability, (6) the scope
precondition with four out-of-scope program-family examples, (7) the
three operator-algebraic instantiations, (8) the L*-blindness 5/6
verdict, (9) the head-to-head verdict ("Set~N is dominated by Set~G on
D1"), (10) the per-block-complementarity framing, (11) the D2 boundary
prediction, (12) the negative instantiation on PWR with five proven
obstructions, (13) the five candidate dimensions on equi / rel, (14)
the ten Translate-extension dimensions total, (15) the
relocation-not-elimination thesis. Even a charitable reader reaches
fatigue around item (9). For an EIC who triages dozens of TOSEM
submissions, the abstract should be a 250-350-word executive summary,
not a contributions list.

**Why it matters**: TOSEM's gate-keeping increasingly relies on abstract
readability for first-pass screening. A 574-word abstract is *not* a
formal violation but signals "this paper has a length problem
upstream", which compounds the W1 length issue. An EIC scanning for
journal fit will read the abstract twice, the §1 contributions list
once, and decide; if the abstract has not delivered a clean executive
summary by the third sentence, the paper starts behind.

**Suggestion**: Move to a structured abstract (IST-style)
in five tagged segments, ~70 words each:

- *Context*: MT, MR identification bottleneck, three foundational gaps
  origin / closure / transferability.
- *Objective*: Replace inductive grounding of MetaPatterns with
  operator-algebraic grounding.
- *Method*: Two-layer NOETHER framework, CONSTRUCT-MP algorithm,
  algebraic-closure Theorem 1 within explicit scope, decidability
  Theorem 2, eight-block decomposition as upstream empirical hypothesis.
- *Results*: Three operator-algebraic instantiations (reactor,
  equivariant ML, relational queries); L*-blindness prediction
  confirmed on 5/6 SUTs; Theorem 1' falsified on PWR via two
  counterexamples identifying five proven plus five candidate
  Translate-extension dimensions; on the scope-matched D1 stratum
  Set~N is dominated by the GP-evolved baseline, contribution is
  read as algebraic derivability plus per-block complementarity plus
  D2-stratum boundary.
- *Conclusion*: NOETHER lifts induction from per-program MR sampling
  to per-domain algebraic layer; downstream from $\mathcal{A}_P$ is
  deductive and mechanical; upstream distillation of $\mathcal{A}_P$
  remains human.

Target ~350 words total. The Boundary-of-contribution box in §1
(L142-156) already provides a clean factual decomposition that the
restructured abstract can mirror.

**Severity**: Minor (structural / readability; the abstract is
publishable as-is but cannot land cleanly with EIC handling at this
density).

### W3: One residual framing seam between §6.6 main body and the §1 abstract framing
**Problem**: Abstract (L78) and §1 C4 (L137) frame the comparative
evaluation as "structural transferability not empirical superiority"
and "Set~N is dominated... a head-to-head superiority claim is not
asserted". §6.6 opening (L1604-1619) carries this framing correctly.
However, the §6.6.1 head-to-head subsection then proceeds to a full
McNemar table with directional p-values, Wilson 95% CIs, per-block
decomposition, complementarity partition, LLM-ensemble extension, and
multiple paragraphs of paired-test interpretation. While each of these
is individually disclaimed ("underpowered for an inferential test at
α=0.05", "directional descriptors only", "the per-block table makes
visible..."), the *cumulative* density of statistical machinery in §6.6
implicitly signals "head-to-head" without explicitly asserting
superiority, which may read as hedge-after-hedge to a hostile
reviewer.

**Why it matters**: The framing "structural transferability not
empirical superiority" is the load-bearing positioning for the entire
empirical chapter. If §6.6's body lets that framing slip even slightly
(by spending too much space on aggregate-D1 paired tests and
Holm-Bonferroni-style multiple-comparison analyses), Reviewer 2 may ask
"if this is not a superiority claim, why is the chapter laid out like
one?" and the paper will need to defend at re-review.

**Suggestion**: Open §6.6 with a single boxed restatement (one
paragraph) of what the chapter does and does not claim, mirroring
the §1 Boundary-of-contribution box. The opening should land
something like: "This section does *not* claim head-to-head
superiority of Set~N over Set~G on D1. It establishes three things:
(i) Set~N's per-block reach is targeted by construction and the
$\mathcal{L}^{*}$-blindness prediction (§7) is the chapter's primary
empirical claim; (ii) Set~N and Set~G complement each other per block;
(iii) Set~G's D1 advantage in the aggregate is concentrated on the
$G$-block on two Euclidean-style SUTs and the $\mathcal{L}^{*}$-block
on six SUTs, and is partially offset by Set~N's $\mathcal{T}^{*}$
edge. The D2-stratum prediction is the framework's own falsifiability
commitment and is a Set~N-specific scope boundary." Place this box
at L1601 before any per-SUT table. The cost is one paragraph; the
benefit is foreclosing the framing-slip critique. (Option B from W1
would naturally trim §6.6's body anyway; this suggestion holds even
under Option A's untouched §6.6.)

**Severity**: Minor (already mostly addressed; one
prophylactic measure recommended).

### W4: Appendix C and Appendix E are heavy and could be tightened
**Problem**: Appendix C (Proofs) runs ~80 lines of LaTeX preamble
(L2851+) including a 76-line worked CONSTRUCT-MP enumeration in C.7
(L3066+); Appendix E (Construct-trace consistency check, L3181+)
runs ~145 lines and is explicitly disclaimed as "not used as
independent evidence". An EIC scanning for production handling will
flag both: C.7's worked enumeration is illustrative rather than
load-bearing for the proofs of Theorems 1, 2, 1' (L2893, L2901,
C.6); E is by the authors' own statement not independent evidence
and could live as supplementary material.

**Why it matters**: Length pressure (W1) cascades. Cutting 4-5 pages
from appendices is the cheapest path to bringing the paper to
≤ 70 pp. without touching the body.

**Suggestion**: Move Appendix C.7 (worked CONSTRUCT-MP enumeration on
the Boltzmann algebra) and Appendix E (Construct-trace consistency
check) to a single supplementary PDF or to the supplementary S3
artefact bundle. Retain in the main body only proofs of Theorems 1, 2,
and the Proposition 1 / 2 / 3' counterexamples (C.1-C.6). This
should release 4-6 pages.

**Severity**: Minor (cosmetic; the proofs themselves are fine).

### W5: Cover letter targeting requires more decisive editorial guidance than the manuscript currently signals
**Problem**: The author's revisions have left a small number of EIC-
scope questions implicit rather than explicit, which the cover letter
should resolve up front rather than burying. Examples: (1) Is this a
foundational paper or an empirical paper? Both are arguably defended
in the manuscript, and the framing differs. (2) Why TOSEM rather than
TSE or ISSTA? The methodological-framework + theorems angle suits
TOSEM well, but the empirical chapter would also suit TSE or ISSTA.
(3) What does the author want the reviewer pool to look like (theory-
heavy + one applications reviewer; or applications-heavy + one
theory reviewer)? This guides EIC assignment.

**Why it matters**: A clean cover letter saves the EIC ~30 minutes of
upstream reading and reduces the chance of reviewer-mismatch
re-assignment.

**Suggestion**: The cover letter should foreground five messages:

1. *Foundational positioning*. The paper is a foundational-theory
   submission. Theorem 1 + Theorem 2 + Theorem 1' + the constructive
   algorithm are the central artefacts; the three instantiations and
   the L*-blindness empirical chapter are supporting evidence, not
   the contribution itself.
2. *What the paper does not claim*. No head-to-head superiority
   claim over GenMorph / Shin et al. / MR-Scout. Set~N is dominated
   by Set~G on the scope-matched D1 stratum at the GenMorph budget;
   the contribution on the empirical side is algebraic derivability
   plus per-block complementarity plus an out-of-scope D2 boundary
   that no inductive baseline can derive ex-ante.
3. *Falsifiable prediction*. The L*-blindness prediction is ex-ante
   derivable from the algebra plus the PIT mutator specification,
   was committed to git before the empirical work, and is confirmed
   on 5/6 SUTs at the strongest reading.
4. *Honest negative instantiation*. The framework's strongest claim
   (absolute completeness) is falsified by the authors themselves on
   their principal application domain (PWR core diffusion); five
   pairwise-independent proven obstructions, plus five candidate
   obstructions on the other two algebras, are the principal open
   problem.
5. *Length decision the EIC should arbitrate*. Either Option A (split
   §6.6 into a companion empirical paper, main paper ~55 pp.) or
   Option B (compress §6.6 in-place, demote supplementary
   appendices). The author's preference is stated, but the EIC's
   decision is binding.

**Severity**: Minor (cover-letter editorial; non-publication-blocking
but materially affects handling efficiency).

---

## Detailed Comments

### Title & Abstract
- Title is appropriate and informative for an EIC reader: identifies
  the artefact (NOETHER), the contribution type (Constructive
  Framework), the artefact's object (Metamorphic Pattern Discovery),
  and the source theory (Operator Algebras). No revision suggested.
- Abstract: see W2. The content is correct; the format is too dense.

### Introduction
- §1 (L111-159) establishes the origin-closure-transferability gap
  cleanly. The Noether-theorem methodological analogy (L114) is
  appropriately tempered ("The analogy is methodological only").
  Contributions C1-C4 (L132-138) are well-tagged and individually
  scoped. The Boundary-of-contribution box (L142-156) is the
  cleanest single piece of editorial work in the manuscript; it lets
  an EIC understand the scope precondition in one page.
- One micro-suggestion: at L130, "We make four contributions" is
  followed by five bullets (C1, C2a, C2b, C3, C4). Renumber as
  "five contributions" or fold C2a + C2b into a single C2.

### Theorem 1 substantive content (§3.3, L432)
- The acknowledgement of the by-construction status of Theorem 1
  (L432, "A sceptical reading might object... we acknowledge...") is
  exactly the right move. The conversion from empirical-adequacy
  claim to structural-adequacy obligation (L432-434) carries the
  argumentative weight that Theorem 1 needs to bear, and the
  Remark `rem:scope` (L421-430) plus Remark `rem:closure-brel`
  (L436-440) cleanly bound the scope.

### §6.6 head-to-head body (L1601+)
- See W3 for the framing-seam observation. The substantive content
  is fine; the per-block decomposition (Table 11 / `tab:per-block-headtohead`
  at L1716) is the right unit of analysis. The aggregate D1 paragraph
  (L1827+) is correctly demoted as secondary.
- L1604-1619 (the chapter's opening framing paragraph) is bold-faced
  and reads well, but it should be elevated to a `tcolorbox` rather
  than left as a bold-italic prose paragraph; this aligns visually
  with the §1 and §9 Boundary boxes and gives the framing the
  weight it deserves.

### §subsec:third-domain (L850-905)
- The third domain (relational query optimisers) is the strongest
  test of cross-Lie-group-/-self-adjoint-/-time-reversal-core
  transferability. The Theorem 1' verdict paragraph (L903-904)
  correctly identifies the five candidate dimensions on
  equi / rel algebras and labels their pairwise independence as
  "asserted by inspection rather than by formal exhaustion proof".
  This is exactly the right honesty.

### §subsec:negative-pwr + Appendix C.6
- Strongest piece of editorial work in the manuscript. The two
  counterexamples are framed as "regulatory essential, engineering
  documentable" (L915), the proofs (Appendix C.6) are explicit, and
  the five-obstruction table (Table 9, L1034) cleanly localises the
  required `Translate` extensions. The choice to use the framework's
  principal application domain (reactor physics) as the falsification
  testbed is editorially courageous and methodologically appropriate.

### §9 Conclusion (L2691-2705)
- Open / Established split in the Boundary box (L2701-2705) is well
  done. One micro-suggestion: at L2702, the "Established" item (iv)
  introduces a level of detail (two specific PWR MRs, five
  obstructions, etc.) that does not match items (i)-(iii)'s
  abstraction level. Compress (iv) to "(iv) a negative instantiation
  on $\mathcal{A}_{\mathrm{PWR}}$ that falsifies Theorem 1' and
  identifies five pairwise-independent `Translate`-extension
  dimensions as the principal locus of follow-up". Move the
  specifics to the body.

### References
- Not reviewed at the per-citation level (defer to reference-
  verification audit). The bibliography style (acmart with
  `printacmref=false` per L19) is appropriate for review submission;
  switch to printacmref=true at final acceptance.

---

## Questions for Authors

1. **Length plan**: Which of W1 Option A (split) or Option B
   (in-place compression) do you prefer, and why? If Option A, are you
   prepared to spin §6.6 + §6.6.1 + Apache Commons Math pilot into a
   ~25-page companion empirical paper, and where would you submit it
   (TOSEM short paper, TSE, ICSE)? If Option B, can you commit to a
   ≤ 70-page main body with §6.6 compressed to ~6 pages, the
   LLM-ensemble baseline demoted to supplementary S4, and Appendices
   C.7 / E demoted to supplementary?

2. **Abstract restructuring**: Are you willing to move to a
   structured (Context / Objective / Method / Results / Conclusion)
   abstract at ~350 words, or do you defend the current ~574-word
   prose-paragraph format? If the latter, please justify against
   TOSEM's typical 250-400-word range.

3. **Cover-letter targeting**: Confirm the five-message cover letter
   layout in W5. Specifically, please commit to (a) foundational
   positioning, (b) explicit non-claim of head-to-head superiority,
   (c) ex-ante status of the L*-blindness prediction with git-
   timestamp evidence, (d) honesty of the negative instantiation,
   (e) length decision the EIC should arbitrate.

4. **Reviewer-pool guidance**: For the EIC's reviewer-assignment
   purposes, do you recommend a theory-heavy pool (one operator-algebra
   / categorical-semantics reviewer, one MT-pattern-catalogue
   reviewer, one statistical-methodology reviewer) or an
   applications-heavy pool (one reactor-physics V&V reviewer, one
   equivariant-ML testing reviewer, one DB-optimiser-testing
   reviewer)? My editorial preference is theory-heavy with one
   applications reviewer, on the grounds that the contribution is
   foundational; please confirm or push back.

---

## Minor Issues

### Language / Grammar
- L130: "We make four contributions" followed by five bullets. Re-number.
- L2702: "Established" item (iv) over-detailed relative to (i)-(iii).

### Citation Format
- `printacmref=false` (L19) and `\setcopyright{none}` (L18) are
  anonymisation settings; remember to flip at acceptance.

### Figures and Tables
- Table 9 (`tab:five-obstructions`, L1034-1067): the column headers
  ("Failure mode", "Required extension to `Translate`") are clear.
  Suggest adding a "Proven / Candidate" status column at submission
  time, mirroring the L78 / L135 distinction between PWR-side proven
  and equi/rel-side candidate dimensions; this makes the table
  stand-alone interpretable.

### Layout
- The Boundary-of-contribution boxes (§1, §4, §9) are visually
  distinct and editorially valuable. Adding a fourth Boundary box at
  the start of §6.6 (per W3) would round out the pattern.

---

## Dimension Scores

Scores reflect quality relative to TOSEM's foundational-paper standard,
not against a generalist software-engineering venue. Calibration: my
prior TOSEM foundational-paper acceptances cluster around 75-85
weighted average; this paper sits firmly in that band.

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 86 | Strong | Operator-algebraic grounding of MetaPatterns is a genuinely novel framing; the three-instantiations + falsification structure goes beyond incremental extension. The "Noether-style derivation of $m_{\mathrm{adj}}$" (§5.4, L577) is a piece of foundational craftsmanship rarely seen in software-testing papers. |
| Methodological Rigor (25%) | 78 | Strong | Two theorems (closure, decidability) proved within explicit scope; Theorem 1' falsified with per-block exhaustion proofs; L*-blindness prediction ex-ante derived and committed to git; pilot sample-size disclosure is exemplary. Minor gaps: five-candidate-dimension pairwise independence on equi/rel is "asserted by inspection", committed as follow-up rather than proved; this is honestly disclosed but counts as a methodology-rigor caveat. |
| Evidence Sufficiency (25%) | 76 | Strong | 80 pp. of detailed instantiations + appendices; three operator-algebraic domains exercised; PIT mutation evidence for L*-blindness on 6 SUTs; comparative case study against three SOTA categories; Apache Commons Math cross-codebase pilot. Empirical evidence is sufficient for a foundational paper at TOSEM; not over-engineered. |
| Argument Coherence (15%) | 82 | Strong | After Round 2 framing revisions, abstract / §1 / §3.3 / §6.6 / §9 carry consistent framing ("structural transferability not empirical superiority"; "Set N dominated on D1"; "5 PWR proven + 5 candidate"; ten Translate-extensions). Boundary-of-contribution boxes are coherent across §1 / §4 / §9. One residual seam (W3) on §6.6 framing-density. |
| Writing Quality (15%) | 81 | Strong | Professional academic prose throughout; precise terminology; appropriate hedging on pilot sample sizes; honest disclosure of scope. Minor stylistic note: abstract is too dense (W2). No grammatical errors detected at the read-through level. |
| Literature Integration (optional) | 80 | Strong | METRIC / METRIC+ / MR-Scout / GenMorph / Shin et al. / Murphy et al. / Ying et al. / Saha-Kanewala all positioned. Ying et al.'s family-tree formalism is given a one-paragraph comparative treatment (L193). Deferred to R2 for completeness. |
| Significance & Impact (optional) | 78 | Strong | Theorem 1' falsification with five proven plus five candidate Translate-extensions is a genuinely informative negative result for the MT-foundations community. Deferred to R3 for practitioner-impact assessment. |
| **Weighted Average** | **79.9** | **Minor Revision (borderline-Accept)** | Weighted = (0.20 × 86) + (0.25 × 78) + (0.25 × 76) + (0.15 × 82) + (0.15 × 81) = 17.2 + 19.5 + 19.0 + 12.3 + 12.15 = 80.15. The decision band crossing (≥ 80 = Accept; 65-79 = Minor Revision) is within rounding tolerance; I land on **Minor Revision** because the length and abstract issues, while EIC-scope-fixable, do require an iteration. |

---

## EIC Synthesis (Round 3 specific)

**Round 2 inheritance**: 13 Required + 12 Suggested issues, 13 Required +
4 Suggested addressed, 8 Suggested declined with documented rationale.
Round 2 DA's five CRITICAL findings (C1-C5) substantively addressed at
the level of framing, scope, and disclosure (see S2). I do not re-litigate
Round 2 issues.

**Round 3 EIC-scope verdict**: The paper is publication-ready on
substance and would survive aggressive R1-R2-R3 review with the framing
already in place. The two EIC-scope blockers are:

1. **Length** (80 pp. exceeds TOSEM target band; W1). Resolvable by
   either Option A (split) or Option B (in-place compression), but the
   resolution must be made before re-review goes out.
2. **Abstract density** (~574 words exceeds 250-400 sweet spot; W2).
   Resolvable by structured (IST-style) reformatting at ~350 words.

The remaining items (W3 §6.6 framing-seam, W4 appendix tightening, W5
cover-letter targeting) are minor and can be handled at copy-edit /
production stage.

**Recommended Round 3 disposition**: **Minor Revision**. Two-month
revision window. After revision, the paper does not require a fresh
Round 4 full review; an EIC desk-check on (1) length compliance + (2)
abstract restructure + (3) cover letter is sufficient. The science is
done; what remains is editorial production handling.

---

*End of Round 3 EIC Report.*
