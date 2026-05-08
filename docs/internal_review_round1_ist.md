# Internal IST-style audit, round 1

**Date**: 2026-05-08
**Reviewer**: Internal Devil's Advocate, simulating an IST (Information
and Software Technology) external reviewer
**Manuscript state**: NOETHER_paper.tex on branch
`feat/section-7-empirical-vs-sota` head `7060ba1` (§7 v2 with
$\mathcal{L}^{*}$-block blindness as central thesis)
**Audit framing**: Reviewer 2 ARS (Adversarial Review Strengthening)
across 5 dimensions: methodological flaws, external validity,
statistical bias, benchmark fairness, Hawthorne (the latter is N/A
for this manuscript).

This audit is **not** an external R&R. It is an internal exercise to
identify items the manuscript should address before submission. The
response document `r1_response_to_ist_audit.md` is structured the
same way an external R&R response would be, so the workflow is
practiced under realistic discipline.

---

## Headline judgement

**Major Revision**. The manuscript has substantial theoretical
contribution (Theorem 1 closure under \texttt{Translate}; the
algebra-derivation of MRs) but its empirical reach is small relative
to the theoretical scope it claims. Five severe items (S1–S5) need
attention before submission; six major items (M1–M6) are revisable
during R1; four minor items (m1–m4) are cosmetic.

| IST review dimension | Score (1–5) | One-line read |
|---|---|---|
| Originality            | 5 | Algebraic-derivation route is methodologically novel in MR-testing literature |
| Significance           | 4 | Theorem 1 + $\mathcal{L}^{*}$-blindness are theoretical contributions |
| Methodology            | 3 | Pre-registration good; n=70 + 1-min Set G + single SOTA is the bottleneck |
| Presentation           | 3 | 8-block notation density high; ~13K words exceeds IST 12K cap |
| References             | 4 | 30+ citations across 4 prior-work lines; self-citation ratio audit recommended |
| Reproducibility        | 4 | Supplementary S1–S7 + test gates + pre-registered selection; Boltzmann-arm code-base testing absent |

---

## Severe items (5)

### S1. Eight-block sufficiency hypothesis is the framework basis but is not externally validated at scale

* Theorem 1 closure depends on Hypothesis 1 ("the eight blocks suffice
  to span the algebra-induced MR space")
* Current evidence: 3 domain instantiations (Boltzmann + equivariant
  ML + relational query optim) plus 1 negative case (PWR
  irreducibly-compositional MRs)
* DeepCrime pilot already hints at a candidate ninth block
  (label-consistency or weight-distribution)
* N=4 domains is small for a structural-sufficiency claim
* **Pre-submission ask**: in §4 add an explicit "How would
  Hypothesis 1 be falsified at scale?" paragraph, demote
  "the eight blocks suffice" to "the eight blocks suffice on the
  four domains tested; scaling validation is committed future work"

### S2. Comparator-suite completion is 1/4

* §6.6 protocol commits to four baselines: Set M (MR-Scout),
  Set G (GenMorph), Set L (LLM), Set B (literature)
* §7 delivers Set G alone
* IST reviewer position: "the paper commits to a 4-baseline
  comparison protocol but delivers only one. Either complete the
  protocol or remove the commitment."
* **Pre-submission ask**: at minimum deliver Set L (LLM-prompted),
  the cheapest of the three deferrals (~1 day human cost); or
  demote the Set M / Set L / Set B promises in §6.6 protocol to
  explicit future-work, removing the implicit promise

### S3. Set G 1-min vs published 30-min budget asymmetry

* §7.6 acknowledges 1-min Set G handicaps the comparator
  conservatively but the asymmetry will be flagged by every
  external reviewer
* Closure action 1 (issue 007 in the experiment repo) re-runs
  Set G at 30-min; orchestrator already committed at branch
  `feat/gp-30min-rerun`, executing on a Claude Code Remote
  host as of this audit
* **Pre-submission ask**: complete the 30-min rerun and update
  §7.6 to report the 30-min number as primary; demote 1-min to
  sensitivity; this is a hard gate

### S4. Boltzmann arm (§5) has no codebase empirical anchor

* §5 derives 12 representative MRs from the Boltzmann transport
  equation (full per-MR provenance in Appendix B)
* These MRs are not tested against any reactor-simulator codebase
  (OpenMC / MCNP / DRAGON)
* §5 is therefore a "theoretical anchor" rather than an "empirical
  anchor" for the in-domain claim
* **Pre-submission ask**: either (a) run a 3-MR pilot against a
  reactor-simulator codebase, or (b) add explicit text at §5 head
  acknowledging that the empirical test of these MRs against a
  reactor-simulator codebase is committed future work and is not
  the present paper's deliverable

### S5. $\mathcal{A}_P$ distillation lacks practical adoption guidance

* §4.5 The principal limitation acknowledges "domain experts must
  still distil $\mathcal{A}_P$ from program semantics"
* The framework's outputs depend on this human-distilled input
  but the manuscript does not provide a step-by-step procedure
  for it
* For an IST audience (oriented to practitioner adoption) this is
  a usability gap
* **Pre-submission ask**: add a "Practical guidance on
  $\mathcal{A}_P$ distillation" subsection to §4 with a 3–5 step
  workflow and one worked example (lighter than §5/§6's full case
  studies)

---

## Major items (6, revisable during R1)

### M1. Sample sizes are uniformly small

* EGNN n=20, DeepCrime n=5, algebra-rich n=70
* For a framework-level IST paper, n=200 (full 38-SUT in-scope
  set) is recommended; closure action 2 in supplementary S7
* Honest-disclosure language already present (3× "underpowered for
  α=0.05") so this is acknowledged but not fixed

### M2. No multiple-comparison adjustment

* §7 reports per-block patterns ($T^{*}$, $G$, $\mathcal{L}^{*}$,
  $\mathcal{I}^{*}$)
* If treated as 4 independent hypothesis tests, Bonferroni / FDR
  adjustment may be required
* The $\mathcal{L}^{*}$-blindness result is ex-ante prediction
  (not post-hoc selection) and is arguably exempt from
  multiple-comparison correction; this distinction should be
  made explicit

### M3. Real-bug evaluation is committed-but-not-delivered

* §6.6 "Real-bug evaluation (protocol)" paragraph commits to
  e3nn / PyTorch Geometric bug-mining
* Not delivered
* IST reviewer position: "delivered protocol or removed promise"

### M4. No runtime / cost comparison

* GenMorph GP runs at 30-min wall per SUT; NOETHER's manual
  $\mathcal{A}_P$ distillation costs ~10h human + ~30min compute
  for 38 SUTs
* Cost-effectiveness comparison is absent from the manuscript
* IST reviewer would ask: "Is your method cheaper or more
  expensive than GenMorph in practice?"

### M5. Length exceeds IST cap

* Current ~13K+ words; IST cap 12K
* §6.7 (relational query optim) and §6.8 (PWR negative case) are
  candidate downscope-to-supplementary

### M6. Notation density

* 8-block names ($G$, $O_{\le}$, $\mathcal{L}^{*}$, $T^{*}$,
  $T^{*}_{2}$, $\mathcal{D}^{*}$, $\mathcal{E}^{*}$,
  $\mathcal{I}^{*}$) introduced in dense sequence at §3
* IST reader is not necessarily formal-methods background

---

## Minor items (4, cosmetic)

### m1. Section-title sentence-case consistency
After §7 insertion, do a one-pass proofread for sentence-case
across the new section.

### m2. "To the best of our knowledge" claims about novel MRs
$\rho_{\mathrm{adj}}$ and $\rho_{\mathrm{train\text{-}rev}}$ are
self-described as "not catalogued in the literature we surveyed";
ensure literature search is comprehensive enough to support this.

### m3. Style audit: \texttt{} / \emph{} / $\mathcal{}$ usage
Cross-check usage consistency across §3, §4, §6, §7.

### m4. Table caption style
Sentence-case caption titles, consistent abbreviation conventions
(e.g., "n=70" vs "$n=70$" vs "n = 70").

---

## Acceptance probability estimates (per IST review type)

| State | accept-after-major | reject-or-die-in-revision | reject |
|---|---|---|---|
| Current (with §7 v2) | 55% | 35% | 10% |
| After S2 + S3 + S4 fixed | 70% | 25% | 5% |
| After all S1–S5 fixed | 80% | 15% | 5% |

---

## Reviewer-recommended revision sequence (priority-ordered)

1. (S3) GP 30-min rerun [in flight, issue 007]
2. (S2) Set L LLM-prompted comparator [~1 day]
3. (S4) §5 head text update OR 3-MR reactor pilot [text update is cheap]
4. (S5) §4 practical guidance subsection on $\mathcal{A}_P$
5. (S1) Hypothesis 1 demote + falsifiability paragraph
6. (M1) algebra-rich n>200 extension [longer-horizon]
7. (M2, M4) statistical-method + cost-comparison clarifications
8. (M3) demote real-bug protocol or deliver pilot
9. (M5) length trim via §6.7/§6.8 supplementary demotion
10. (M6) §3 plain-language gloss
11. (m1–m4) full proofread + style audit
