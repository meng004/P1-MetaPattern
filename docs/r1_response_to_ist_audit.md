# Response to internal IST-style audit, round 1

**Date**: 2026-05-09
**Audit document**: `docs/internal_review_round1_ist.md`
**Manuscript state at response time**: branch
`feat/section-7-empirical-vs-sota` head `7060ba1` (paper repo);
branch `feat/gp-30min-rerun` head `9aceb8e` (experiment repo, with
GP 30-min rerun executing on Claude Code Remote)

We thank the internal reviewer for the audit. The 5 severe items, 6
major items, and 4 minor items are addressed below in
priority-ordered sequence. Where we agree, the action and the
specific manuscript change are stated. Where we partially agree, the
caveats and the residual gap are made explicit. Where we disagree, a
technical reason is given rather than a defensive deflection.

The response follows four status types, in line with our project's
revision-tracking convention:

| Status | Meaning |
|---|---|
| `AGREED`            | Reviewer is correct; manuscript change committed |
| `PARTIAL_AGREE`     | Reviewer is partially correct; mitigation committed, residual caveat acknowledged |
| `REVIEWER_DISAGREE` | Manuscript position is correct; technical reason given |
| `IN_FLIGHT`         | Closure action already running on a separate branch; expected commit reference cited |

Sycophantic concession is anti-pattern #6 in our project's revision
guide. We have therefore chosen to push back on M2 (multiple-comparison
adjustment) where the audit's framing conflates ex-ante prediction
with post-hoc selection. The push-back is technical, not defensive.

## Quick verdict table

| ID | Severity | Status | One-line response |
|---|---|---|---|
| S1 | severe | **PARTIAL_AGREE** | Demote Hypothesis 1 language; add falsifiability paragraph; reject "more domains required" framing because the claim is conditional, not universal |
| S2 | severe | **PARTIAL_AGREE** | Deliver Set L (LLM); document structural limits on Set M and Set B for this substrate; full 4-comparator delivery is not feasible for R1 |
| S3 | severe | **IN_FLIGHT** | Issue 007 GP 30-min rerun executing on Remote; expected to retire S3 within 24 h of audit |
| S4 | severe | **PARTIAL_AGREE** | Add §5-head clarifier acknowledging codebase pilot is committed future work; cannot run pilot in R1 |
| S5 | severe | **AGREED**       | Add §4 "Practical guidance on $\mathcal{A}_P$ distillation" subsection |
| M1 | major  | **AGREED**       | Acknowledged in §7 as committed future work; no further main-text change |
| M2 | major  | **REVIEWER_DISAGREE** | $\mathcal{L}^{*}$-blindness is ex-ante prediction, not post-hoc test selection; Bonferroni/FDR is inapplicable; add explanatory footnote |
| M3 | major  | **PARTIAL_AGREE** | Demote real-bug protocol from §6.6 main text to clearly-marked future work; do not deliver pilot in R1 |
| M4 | major  | **AGREED**       | Add cost-comparison paragraph to §7.7 threats |
| M5 | major  | **AGREED**       | Move §6.7 + §6.8 to supplementary; preserve 1-paragraph stub in main §6 |
| M6 | major  | **AGREED**       | Add plain-language gloss subsection at end of §3 |
| m1 | minor  | **AGREED**       | Full sentence-case proofread on the §7 insertion |
| m2 | minor  | **AGREED**       | Audit literature search for $\rho_{\mathrm{adj}}$ and $\rho_{\mathrm{train\text{-}rev}}$ novelty claims |
| m3 | minor  | **AGREED**       | Style-audit pass on \texttt{} / \emph{} / \$\mathcal{}\$ usage |
| m4 | minor  | **AGREED**       | Standardise "$n=70$" vs "n = 70" across tables and prose |

---

## Severe items

### S1. Eight-block sufficiency hypothesis

**Reviewer comment** (paraphrased): Hypothesis 1 ("the eight blocks
suffice to span the algebra-induced MR space") is the framework's
basis (Theorem 1 closure depends on it), but the empirical evidence
is 3 positive domain instantiations + 1 negative case. Four domains
is small for a structural-sufficiency claim. The DeepCrime pilot
already hints at a candidate ninth block. Recommend: demote
"the eight blocks suffice" language; add explicit
falsifiability discussion.

**Status**: PARTIAL_AGREE.

**Response**: We agree that the four-domain evidence base is small
relative to the language we use. We commit to demoting "the eight
blocks suffice" to "the eight blocks suffice on the four domains
tested; scaling validation is committed future work" wherever
that phrasing or its variants occur, and to adding a falsifiability
paragraph at §4 stating the conditions under which Hypothesis 1
would be considered falsified at scale.

We push back, however, on the implicit framing that the manuscript
needs 10+ domain instantiations before the structural-sufficiency
claim can be made. Hypothesis 1 is a **conditional** claim of the
form "if a program family's induced algebra $\mathcal{A}_P$ admits a
canonical decomposition into the eight named blocks, then
$\mathbb{M}(\mathcal{A}_P)$ closes under \texttt{Translate}". This
is not a universal claim about all program families. The negative
instantiation in §6.8 (PWR irreducibly-compositional MRs) is in
fact direct evidence of the conditional's antecedent failing on a
program family whose algebra does not admit a clean eight-block
decomposition. The conditional remains intact.

A reviewer who reads the manuscript as making a universal claim
should be redirected by §4.5 (The principal limitation), but we
acknowledge that the boundary deserves to be clearer in the
abstract and §1 framing. R1 will sharpen the abstract sentence
about Hypothesis 1's scope.

**Action**:
* §4 (after Theorem 1 statement): add a paragraph titled
  "Falsifying Hypothesis 1 at scale" that specifies the
  conditions under which the eight-block decomposition would be
  rejected (concrete: at least three program families with
  non-trivial algebras populating none of the eight blocks; or
  one program family with empirically-effective MRs not derivable
  from any of the eight). Estimated ~150 words.
* §4.5 (The principal limitation): tighten the sentence about the
  scope-boundary so it ties back to Hypothesis 1's conditional
  form.
* Abstract: replace any unconditional language about the
  eight-block decomposition with the conditional form.
* §6.8 (PWR negative): retitle the subsection so its role as
  "evidence of the conditional's antecedent failing" is more
  visible to a reviewer who does not read sequentially.

### S2. Comparator-suite completion is 1/4

**Reviewer comment** (paraphrased): §6.6 protocol commits to four
baselines (Set M, G, L, B); §7 delivers Set G alone. Recommend:
deliver at least Set L, the cheapest of the three deferrals (~1
day human cost); or demote the unfulfilled commitments.

**Status**: PARTIAL_AGREE.

**Response**: We agree that delivering Set L (LLM-prompted) is
high-value-low-cost and should be in R1. We will execute Set L on
the same 10 algebra-rich SUTs and report alongside Set G in §7.6.

We push back on the implicit assumption that all four arms of the
protocol are uniformly valuable on this substrate.
Substrate-specific limitations are:

* **Set M (MR-Scout-mined)**: MR-Scout's recall is bounded by
  relations latent in existing test suites. The 10 algebra-rich
  SUTs in this evaluation are inlined into a custom
  \texttt{MathSignalClass} (so PIT mutates the algorithm directly);
  there are no pre-existing test suites for these inlined SUTs.
  MR-Scout's reach on this substrate is therefore structurally
  zero or near-zero. We will document this in §7.7 threat (f) and
  treat Set M as not-applicable for this substrate, parallel to
  the Set G N/A cases for instance methods and boolean predicates.
* **Set B (literature MRs)**: for these specific Java mathematical
  methods (\texttt{midpoint}, \texttt{gcdSig}, \texttt{exactLog2},
  etc.), the MR-testing literature does not catalogue MRs at this
  level of granularity. The Set B arm in the EGNN case study (§6.6)
  used Segura et al. and Shin et al.; analogous coverage for
  utility-scale Java math methods is sparse to nonexistent. Set B
  for this substrate is closer to a "literature does not address"
  class than a "literature comparator is feasible" class.

R1 therefore delivers Set L and explicitly documents Set M's and
Set B's substrate-specific limitations in §7.7 threats. We do not
fabricate a Set M or Set B harvest where the substrate does not
admit one; that would be worse than acknowledging the gap.

**Action**:
* New issue/plan in experiment repo: ISSUES/008-set-l-llm-arm.md +
  PLANS/008-set-l-llm-arm.md (estimated ~1 day human + small
  compute). Branch: \texttt{feat/set-l-llm-comparator}.
* §7.6 (after Set G pooled comparison): add Set L row to
  Table~\ref{tab:algebra-rich-pooled} and the corresponding
  paragraph.
* §7.7 threats (f) (single SOTA comparator): expand to clarify
  Set M and Set B substrate-specific limitations; demote them
  from "delivered baselines" to "not-applicable on this
  substrate, with documented reason".
* §6.6 protocol paragraph (line 762–775 of NOETHER_paper.tex):
  replace "Set N alongside two independent automated pipelines"
  with "Set N alongside automated pipelines that admit the
  substrate; on Java mathematical methods this is Set G + Set L,
  with Set M and Set B substrate-N/A".

### S3. Set G 1-min vs 30-min budget asymmetry

**Reviewer comment** (paraphrased): §7.6 reports Set G at GAssert
1-min budget; GenMorph upstream's published budget is 30 min. The
asymmetry is conservative against parity but every external
reviewer will flag it. Mandatory pre-submission rerun.

**Status**: IN_FLIGHT.

**Response**: This was identified as the highest-priority closure
action in the audit and was already in execution when the audit was
recorded. Issue 007 (`ISSUES/007-gp-30min-rerun.md` and
`PLANS/007-gp-30min-rerun.md` in the experiment repository) reruns
the Set G GP harvest at GAssert 30-min on the same 10 algebra-rich
SUTs. The orchestrator (`scripts/_e3_gp_rerun_30min.sh`), the
declarative target config (`configs/gp_budget_30min.json`), the
1-min-vs-30-min comparison helper
(`scripts/_compare_gp_budgets.py`), and the test gate
(`tests/test_compare_gp_budgets.py`) are committed at experiment-repo
branch `feat/gp-30min-rerun` head `9aceb8e`. The branch is
auto-loaded into Claude Code Remote via the Active-Task section of
the experiment repo's `CLAUDE.md`.

Expected wall budget: 60–90 min for the full 8 head-to-head SUTs.
Outputs upon completion: `mrs_set_g_30min/<subject>/`,
`results/aligned_summary_30min.json`, and
`docs/e3b_gp_30min_rerun_results.md` with the per-SUT delta and the
McNemar verdict at the new budget. The §7.6 paper-text update is
local-author work (the paper repo is not on GitHub) and is
conditional on the rerun's outputs.

**Action**: post-rerun, the §7.6 paragraph is updated to report
30-min as primary and 1-min as a sensitivity row; Table~\ref{tab:future-work}
row (a) is marked "DONE"; the threat paragraph (b) on budget
asymmetry is removed or rewritten as a methodological footnote.

### S4. Boltzmann arm has no codebase empirical anchor

**Reviewer comment** (paraphrased): §5 derives 12 representative MRs
from the Boltzmann transport equation. These MRs are not tested
against any reactor-simulator codebase. §5 is therefore a
"theoretical anchor" rather than an "empirical anchor" for the
in-domain claim.

**Status**: PARTIAL_AGREE.

**Response**: We agree that §5 does not include a codebase pilot and
that the absence is a real gap relative to IST's preference for
empirical bite. We disagree with characterising §5's role as "in-domain
empirical anchor", that role is in §6 (equivariant ML EGNN case
study) and in §7 (Java mathematical methods comparison). §5's role
is to demonstrate that CONSTRUCT-MP **generates** MRs from a
non-trivial operator algebra in a domain where the algebraic
machinery is well-developed (reactor physics has been
formalised under Boltzmann transport for decades). The
"instantiation: from transport to diffusion to burnup" subtitle
refers to algebra-instantiation, not to executable-MR-testing.

That distinction said, an external IST reviewer will not read the
section title with the algebra-vs-implementation distinction in
mind, and will read absent codebase testing as a weakness. We
therefore commit to two text-level changes that resolve the framing
without changing the deliverable:

* §5 head paragraph: add explicit "the empirical test of these MRs
  against a reactor-simulator codebase is committed future work and
  is not the present paper's deliverable" sentence.
* §1 "organised as follows" paragraph: clarify that §5 demonstrates
  algebra-derivation in the Boltzmann domain; empirical anchoring is
  in §6 (EGNN) and §7 (Java).

A 3-MR pilot against an open-source reactor simulator (OpenMC,
DRAGON, or PyNE) is technically feasible but would require ~3–5
days of work for a non-trivial test (build, integrate Set N MRs as
runtime invariants, evaluate detection on injected mutants). This is
out of scope for R1 but is committed future work; we note it
explicitly in the §7.7 future-work table as item (e), parallel to
the Set L delivery and the 38-SUT extension.

**Action**:
* §5 head: add 1-sentence committed-future-work clarifier.
* §1 organised-as-follows: clarify §5 vs §6/§7 roles.
* §7.7 Table~\ref{tab:future-work}: add row (e) "Reactor-simulator
  3-MR pilot against an open-source codebase (OpenMC / DRAGON /
  PyNE)", cost ~3–5 days, expected effect "executable empirical
  anchor for the §5 derivation".

### S5. $\mathcal{A}_P$ distillation lacks practical adoption guidance

**Reviewer comment** (paraphrased): §4.5 admits that $\mathcal{A}_P$
distillation requires human domain expertise. The framework's
output therefore depends on a human-distilled input that the
manuscript does not show how to produce. For an IST audience this
is a usability gap.

**Status**: AGREED.

**Response**: This is a real gap and we are surprised the original
draft did not address it. We commit to adding a "Practical guidance
on $\mathcal{A}_P$ distillation" subsection at the end of §4 (after
§4.5 The principal limitation, before §5). The subsection will give:

1. A 3–5 step workflow for distilling $\mathcal{A}_P$ from a
   program family's documented mathematical structure.
2. A worked example lighter than §5/§6's full case studies, we
   propose using one of the §7 algebra-rich SUTs (e.g.,
   \texttt{midpoint}) where the distillation is short enough to fit
   in 1 page but non-trivial.
3. A short discussion of failure modes (when distillation fails —
   the §6.8 PWR case is one — and what a practitioner does when
   that happens).

The audience for this subsection is IST's practitioner-oriented
reader. We expect this subsection to be one of the most-cited parts
of the paper if it lands well, because it is the first time the
framework's adoption procedure is laid out concretely.

**Action**:
* New subsection in §4: "Practical guidance on $\mathcal{A}_P$
  distillation". Estimated ~600–800 words plus a short worked
  example using \texttt{midpoint}.
* Abstract: add a half-sentence pointing at the practical guidance
  as a contribution alongside the algebraic-derivation thesis.
* §1: brief mention in the paper-organisation paragraph.

---

## Major items

### M1. Sample sizes are uniformly small

**Status**: AGREED. Already acknowledged in §7's "underpowered for
$\alpha = 0.05$" disclosures (3 occurrences, per the manuscript's C6
small-sample-pilot honesty rule). The 38-SUT extension is committed
future work in §7.7 Table~\ref{tab:future-work} row (b). No further
main-text change is required for R1.

### M2. No multiple-comparison adjustment

**Status**: REVIEWER_DISAGREE.

**Response**: The audit conflates two distinct statistical roles
the per-block patterns play in §7. The
$\mathcal{L}^{*}$-block-blindness result (§7.3) is an **ex-ante
prediction** derivable from the framework's algebraic structure
and PIT's public mutator specification, with falsifiability
criterion stated in advance ("$\le 1/3$ kill rate on at least 5 of
6 SUTs"). The other per-block patterns ($T^{*}$ high, $G$
moderate-correlated-with-symmetry, $\mathcal{I}^{*}$ low under the
paired-MR DSL) in §7.4 are **corroborating qualitative
observations**, not independent hypothesis tests with effect-size
thresholds.

Bonferroni or FDR correction is the appropriate adjustment when a
study performs multiple independent statistical tests with risk of
false-positive inflation under the multiple-testing Family-Wise
Error Rate. This is **not** the situation in §7. The
$\mathcal{L}^{*}$-blindness test is one prediction with one
falsifiability criterion; multiplicity-correction does not apply.
The other per-block patterns do not have associated hypothesis
tests; they are qualitative descriptions of the data.

We will therefore **not** apply Bonferroni or FDR correction. We
will, however, add an explanatory footnote to §7.3 explicitly
distinguishing the ex-ante role of the $\mathcal{L}^{*}$ test from
the corroborative role of the §7.4 patterns, so a reviewer who
expects multiplicity correction sees why it is not appropriate
here. The footnote will cite Hochberg & Tamhane on the conceptual
distinction between ex-ante and post-hoc multiple comparisons.

**Action**: footnote on §7.3 (~80 words) explaining the ex-ante /
corroborative distinction. No change to test reporting or to claim
strength.

### M3. Real-bug evaluation is committed-but-not-delivered

**Status**: PARTIAL_AGREE.

**Response**: Agreed that the §6.6 "Real-bug evaluation (protocol)"
paragraph commits to e3nn / PyTorch Geometric mining and that no
delivery follows. We have two viable paths:

(a) demote the real-bug protocol from §6.6 main text into §7.7
future-work table (parallel to the cost of Set M / L / B
delivery), removing the implicit promise from main text.

(b) deliver a small (n=5–8) real-bug pilot from e3nn / PyG bug
trackers in R1.

Path (b) is technically feasible but takes ~1 week; combined with
the other R1 items it would push the R1 wall-time to multiple
weeks. We choose path (a) for R1 and commit (b) as future work.
The honest framing matches our C6 pilot-disclosure rule and avoids
overcommitment.

**Action**: rewrite §6.6 "Real-bug evaluation (protocol)" paragraph
as a 2–3 sentence stub pointing to §7.7 Table~\ref{tab:future-work}
row (f) "Real-bug evaluation pilot on e3nn / PyG, n≥10, 1-week
cost".

### M4. No runtime / cost comparison

**Status**: AGREED.

**Response**: A runtime/cost comparison between NOETHER's manual
$\mathcal{A}_P$ distillation and GenMorph's GP search is a fair
question and the manuscript does not currently address it. The
honest numbers, with appropriate caveats:

* GenMorph GP at upstream 30-min budget: 30 min wall × 10 SUTs ≈
  5 h compute (parallelisable to ~1 h wall at 5-process). Per-SUT
  human cost: zero after the SUT is wired into upstream. Wiring
  cost (per §6.6 GP rerun): ~half a day per SUT class (instance
  methods, boolean predicates, etc.).
* NOETHER manual derivation per §7.4: ~1 hour per SUT for a
  trained derivation analyst, assuming the SUT's algebra is
  documented. Translation to JIR/JOR DSL: ~30 min per MR. Per-SUT
  total for 3 MRs: ~3 h human.
* For 38 algebra-rich SUTs: GP costs ~5 h compute (parallelised),
  zero human; NOETHER costs ~110 h human + zero search compute.

The comparison does not have a single dominant winner. GP wins on
human-cost; NOETHER wins on closure guarantee (Theorem 1) and on
covering programs GP's pipeline cannot address (instance methods,
boolean predicates). For the R1 manuscript, the honest framing is
"different cost profiles for different value propositions"; we do
not claim cost-superiority.

**Action**: §7.7 threats add new paragraph (g) "Runtime and human
cost", ~100 words, stating the numbers above with explicit
"different cost profiles" framing.

### M5. Length exceeds IST cap

**Status**: AGREED.

**Response**: Current ~13K+ words; IST cap 12K. Move §6.7 (relational
query optimisers) and §6.8 (PWR negative instantiation) to
supplementary; preserve a 1-paragraph stub in §6 pointing to each.
Estimated saving: ~1.5K–2K words from main text. Trim §3 plain-language
gloss (M6 below) compensates with ~200–300 words added; net saving
~1.2K–1.7K, bringing main text to ~11.5K-12K, within IST cap.

**Action**:
* Move §6.7 to supplementary S6 (extending current
  `supplementary/S6_query_optimiser/`); leave 1-paragraph stub at
  §6 between current §6.6 and §6.8 (which becomes §6.7-stub-on-PWR).
* Move §6.8 to supplementary as S8 (new directory:
  `supplementary/S8_pwr_negative/`); leave 1-paragraph stub.
* Cross-references throughout main text updated via
  `\ref{}` to the supplementary anchors.

### M6. Notation density

**Status**: AGREED.

**Response**: The eight-block names ($G$, $O_{\le}$,
$\mathcal{L}^{*}$, $T^{*}$, $T^{*}_{2}$, $\mathcal{D}^{*}$,
$\mathcal{E}^{*}$, $\mathcal{I}^{*}$) are introduced in §3 in a
dense sequence. We will add a "Plain-language gloss for the eight
blocks" subsection at the end of §3, with one sentence per block in
non-formal language. Examples:

* $G$ (group / symmetry): "the input transformations that the
  function commutes with, e.g., swap-arguments for commutative
  binary operations"
* $\mathcal{L}^{*}$ (linearity / scaling): "the function's behaviour
  under positive rescaling of all numeric inputs"
* $T^{*}$ (translation / period): "the function's behaviour under
  additive shift of inputs"
* etc.

This is a presentation patch, not a content change.

**Action**: new §3 subsection ~250–300 words. Abstract gains a
short pointer to the gloss subsection.

---

## Minor items

### m1. Section-title sentence-case consistency

**Status**: AGREED. After the §7 v2 insertion, run a one-pass
proofread for sentence-case across the new section. No content
change.

### m2. "Best of our knowledge" claims about novel MRs

**Status**: AGREED. Re-audit the literature search for
$\rho_{\mathrm{adj}}$ (adjoint-attention duality MR for equivariant
attention) and $\rho_{\mathrm{train\text{-}rev}}$ (training-trajectory
time-reversal MR). Add 2–3 additional citations if recent
equivariant-ML or autodiff-testing literature contains analogous
constructs.

### m3. Style audit: \texttt{} / \emph{} / $\mathcal{}$ usage

**Status**: AGREED. Run a single-pass audit across §3, §4, §6, §7
for consistent use of code-identifier formatting, mathematical
emphasis, and operator-block notation. Apply the project's existing
style audit (`style_audit/` directory in the repo).

### m4. Table caption style

**Status**: AGREED. Standardise "$n=70$" / "n = 70" / "n=70" usage
across all tables and prose; sentence-case all caption titles;
consistent abbreviation conventions.

---

## Convergence and next-round expectations

### What this round (R1) delivers

The R1 deliverable will be a manuscript at branch
`feat/section-7-empirical-vs-sota` with the following changes
relative to the audit-time head `7060ba1`:

* **§7.6 update with 30-min Set G as primary** (S3 closure;
  conditional on issue 007 completion)
* **Set L LLM-prompted comparator added to §7.6 + §7.7** (S2
  partial closure via new issue 008)
* **§5 head clarifier on the algebra-vs-implementation
  distinction** (S4 partial closure)
* **§4 new subsection "Practical guidance on $\mathcal{A}_P$
  distillation"** (S5 closure)
* **§4 new paragraph "Falsifying Hypothesis 1 at scale"; abstract
  + §6.8 conditional-claim language tightening** (S1 closure)
* **§6.6 protocol paragraph rewritten** (M3 closure on real-bug
  protocol; S2 closure on Set M / B substrate-N/A documentation)
* **§7.3 footnote on ex-ante vs corroborative statistical role**
  (M2 explanatory closure)
* **§7.7 threats expanded with runtime/cost paragraph** (M4
  closure)
* **§6.7 / §6.8 demoted to supplementary, stubs preserved in
  §6** (M5 closure)
* **§3 plain-language gloss subsection added** (M6 closure)
* **m1–m4 cosmetic proofread**

### What R1 does not deliver

* (S4 alternative path) reactor-simulator 3-MR pilot — committed
  future work, ~3-5 days
* (M1) full 38-SUT algebra-rich extension — committed future work,
  ~10 days human + 30 min compute
* (M3 alternative path) real-bug evaluation pilot — committed future
  work, ~1 week
* (S2 alternatives) Set M (MR-Scout) — substrate-N/A on inlined
  utility methods; Set B (literature) — substrate-N/A given absent
  literature MRs at this granularity

### Estimated R1 wall-time

* IN_FLIGHT items (S3): ~24 h (Remote rerun + local §7.6 update)
* Set L delivery (S2 partial): ~1 day
* Manuscript text edits (S1, S4, S5, M2, M3, M4, M5, M6, m1–m4):
  ~3 days

Total R1 wall-time after Remote completes: ~5–6 days.

### Acceptance probability re-estimate after R1

| State | accept-after-major | reject-or-die-in-revision | reject |
|---|---|---|---|
| At audit time (head `7060ba1`) | 55% | 35% | 10% |
| Post-R1 (this response delivered) | 75% | 20% | 5% |

This re-estimate is conservative against R1 because Set M and Set B
remain undelivered (with technical justification), and the §5
codebase pilot is deferred. An R1 reviewer who insists on Set M / B
delivery or §5 codebase pilot will move to "die-in-revision". An
R1 reviewer who accepts the substrate-N/A and committed-future-work
framings will move to "accept-after-major". Both outcomes are
plausible.

---

End of response.
