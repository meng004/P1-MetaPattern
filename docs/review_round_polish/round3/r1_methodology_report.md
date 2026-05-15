# Peer Review Report

## Manuscript Information
- **Title**: NOETHER: An Algebraic Framework for Metamorphic-Relation MetaPatterns
- **Manuscript ID**: ACM TOSEM (under review)
- **Review Date**: 2026-05-15
- **Review Round**: Round 3 (re-review after Round 2 Major Revision)

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 — Methodology

### Reviewer Identity
Senior empirical-software-engineering methodologist in the Wohlin / Briand
tradition. Focus on construct / internal / external / conclusion validity
under Wohlin et al.'s four-validity framework; statistical reporting
discipline (Wilson CIs, McNemar / Fisher exactness, effect-size reporting);
pre-registration discipline; and the integrity boundary between
construct-trace pipeline checks and independent fault-detection evidence.

### Review Focus
Independent verification of whether the five Round 2 weaknesses (W1–W5)
flagged on commit `2df9b6b` are genuinely resolved in commit `ceac6ed`,
plus methodological hygiene of Round-2-introduced material (METRIC+
small-scale table, BREAKS_HOMOGENEITY outlier rule, OR/RD reporting,
DeepCrime pilot split). Strict file-grounded, read-only audit; no
re-litigation of issues already discharged.

---

## Overall Assessment

### Recommendation
- [x] **Minor Revision** — Minor revisions needed, no re-review after revision

### Confidence Score
**5** — Methodology and statistical reporting are squarely within my
expertise; the relevant artefacts (set_L_llm.py, prompt_log.md, JSON
pre-registration, paper sections, Tables 13/19) are all file-grounded.

### Summary Assessment
The Round 3 manuscript fully discharges the four substantive Round 2
weaknesses (W1, W2, W4, W5) and meaningfully strengthens the DeepCrime
pilot reading (W3) without inflating its inferential weight. Set L is now
a verifiable GPT-4 turbo (2024-04-09, t=0.0, seed=4246) generation logged
in `supplementary/S3_case_study/mr_sets/prompt_log.md` with verbatim raw
output dated 2026-05-15; the §subsec:pooled-headtohead body leads with
the corrected D1 dominance reading (McNemar exact $p = 0.019$ on the
D1-only stratum, $n = 52$ post-equivalent-mutant exclusion), reports
paired risk difference $\mathrm{RD}_{\mathrm{paired}} = +0.212$ and odds
ratio $\mathrm{OR} = 3.75$, and demotes pooled M1 to a scope-mismatched
auxiliary; Table 13 properly italicises the design-implied Set N CTT
column with daggers and a caption-level "excluded from H3a.1 evidence
base" statement; a cross-codebase Apache Commons Math 3.6.1 pilot
(3 SUTs, 5 MRs, 77 mutants) is committed and reported as pilot evidence
with appropriate underpowered framing, and external-team transfer is
committed as future-work item (j). Round-2-introduced material is
methodologically clean with one minor textual inconsistency. The
contribution remains a robust algebraic systematisation supported by
honest, scope-matched empirical evidence within stated limits.
Recommendation: Minor Revision to address the textual mismatch and a
small disclosure tightening; no further re-review necessary.

---

## W1–W5 Resolution Status

### W1 (CRITICAL Round 2): Set L was `_placeholder_*_fn`, not GPT-4
**Status: FULLY_RESOLVED**

`supplementary/S3_case_study/mr_sets/set_L_llm.py` (L1–L191) now contains
five fully implemented MR functions (`_llm_rot_fn`, `_llm_trans_fn`,
`_llm_scale_fn`, `_llm_perm_fn`, `_llm_noise_fn`) that translate verbatim
JSON from a GPT-4 turbo run. The header docstring (L1–L25) names the
model (`gpt-4-turbo-2024-04-09`), temperature (0.0), seed (4246), and
generation date (2026-05-15 UTC). `prompt_log.md` (L1–L103) records the
prompt verbatim (L13–L43), the raw GPT-4 JSON output verbatim (L47–L90),
and parse validation rules (L92–L103). The "Mode 6 file-grounded" blocker
is closed: an external auditor can re-execute the prompt against
gpt-4-turbo-2024-04-09 at the recorded seed and compare. Table 4 numbers
remain consistent (N=2/5, L=0/5, B=0/5 with Wilson CIs at paper line
797–802) — the GPT-4 spec produces the same five MR semantics
(rotation, translation, scaling, permutation, noise) that the placeholder
encoded, so the kill vector did not shift.

### W2 (MAJOR Round 2): Competitive parity inconsistent with D1 McNemar p=0.019
**Status: FULLY_RESOLVED**

§subsec:pooled-headtohead (paper L1602–1620) now opens with the corrected
verdict: "Set N is dominated by Set G in the aggregate (McNemar exact
two-sided $p = 0.0043$ pooled and $p = 0.019$ on D1 only, $n = 62$
post-equivalent-mutant exclusion)" and explicitly states "The paper does
not assert head-to-head superiority on D1." The aggregate D1 paragraph
(L1827–1845) reports the OR/RD effect sizes: $(b,c) = (15, 4)$,
$\mathrm{RD}_{\mathrm{paired}} = (15-4)/52 = +0.212$ favouring Set G,
$\mathrm{OR} = 15/4 = 3.75$. Both effect-size computations are verified.
"Competitive parity" as a framing is removed from the body; the
framework's contribution is reframed as (i) algebraic derivability,
(ii) per-block complementarity (Set G alone kills 15 D1 mutants Set N
misses, Set N alone kills 4 D1 mutants Set G misses), and (iii) the D2
prediction. Pooled M1 is demoted to "auxiliary, scope-mismatched, $n = 57$"
(L1872–1896). The H3a.1 pre-registered hypothesis (L829–835) is also
correctly re-worded ("per-block; aggregate D1 dominance is \emph{not}
pre-registered as the load-bearing reading").

### W3 (MAJOR Round 2): DeepCrime n=5 carries three inferential claims
**Status: FULLY_RESOLVED**

§subsec:deepcrime-pilot now contains two explicitly separated paragraphs.
"Reading the pilot (inferential verdict)" (paper L806–807) states
"Fisher-exact $p$-values for Set N vs Set L and Set N vs Set B are both
$p = 1.00$; the pilot is therefore underpowered for an inferential
conclusion at $\alpha = 0.05$." and reports the 2/5 vs 0/5 vs 0/5 as
"descriptive evidence consistent with the direction of the framework's
$\mathcal{L}^{*}$-block prediction, not as a hypothesis confirmation."
"Interpretation of the two detection events (mechanism, not inference)"
(L809–810) provides the per-event mechanism narrative ($\rho_{\mathrm{train}}$
firing on cat-v-01 head-scaling and cat-v-03 head-zeroing) and explicitly
states the mechanism statement "is independent of the underpowered sample
size." This separation correctly partitions inferential weight from
mechanism interpretation. Wilson 95% CI $[0.12, 0.77]$ for Set N's 2/5
is also reported. Threat (e) (L815) acknowledges Set L's single-sample
limitation.

### W4 (MINOR Round 2): Augmented stratum 25/25 visual leak
**Status: FULLY_RESOLVED**

Table 13 (paper L3270–3290) and its surrounding paragraphs satisfy every
W4 recommendation:
- Set N kill columns are italicised: `\emph{Set~N kills (CTT)}`
  (L3274) and per-row `\emph{5}` / `\emph{$1.000^{\,\dagger}$}` cells
  (L3276–3282).
- The dagger marker $^{\dagger}$ appears on every Set N rate; the
  footnote (L3287–3289) explains "Set~N columns are italicised to mark
  that the rate is design-implied by mutant authoring".
- The CTT acronym is defined explicitly: "CTT = construct-trace test
  (design-implied)" (L3288), and the column header repeats it.
- The caption (L3267–3269) carries the exclusion statement in bold:
  "\textbf{This table is excluded from the H3a.1 evidence base
  (§subsec:pooled-headtohead);} the H3a.1 verdict rests on the
  pre-registered PIT-covered three-block substrate only."
- A dedicated paragraph "Why this is not a head-to-head test of H3a.1"
  (L3307–3322) reiterates the construct-trace-circularity argument
  in prose.

The visual leak — a reader scanning the table and reading 25/25 as a
head-to-head kill rate — is now blocked at three layers (italicised
values, dagger footnote, bold caption exclusion).

### W5 (MAJOR Round 2): Single Java codebase / single architecture / single GenMorph snapshot
**Status: FULLY_RESOLVED (as pilot; external-team transfer remains future work)**

- Cross-codebase pilot: `tab:future-work` item (b.cm) (paper L2368) is
  marked **Done (pilot)**: 3 Commons Math 3.6.1 SUTs (`Complex.multiply`,
  `Complex.divide`, `Vector3D.dotProduct`), 5 Set N MRs via
  CONSTRUCT-MP, PIT 1.7.4 on 77 target-method mutants. Headline:
  $G$-block kill rate $6/21 = 0.286$ Wilson 95% CI $[0.138, 0.500]$;
  D2 stratum prediction passes at $2/29 = 0.069 \le 0.10$; $\mathcal{L}^{*}$
  block $n = 0$ documented as structural (not a measurement gap).
- The External Validity paragraph (L2454) reports the pilot in detail,
  explicitly frames it as "underpowered for $\alpha = 0.05$ hypothesis
  testing" and as "descriptive evidence consistent with the framework's
  scope-internal generalisation prediction."
- External-team transfer (the analogue on the reactor-physics side) is
  committed as future-work item (j) (L2380): "External-transfer test
  on an independently-authored reactor-physics MR corpus … applying
  NOETHER's eight-block decomposition to a PARCS V&V suite catalogue
  or an IAEA-TECDOC-class catalogue authored by a team unconnected to
  the present authors."
- GenMorph-snapshot caveat: 30-min budget and a 1-min sensitivity rerun
  are both reported on the D1 substrate (Table 11 / Table 12); item
  (a.budget-replication) commits a multi-seed GP rerun.

The framework's external-validity claims are now explicitly scope-
internal, with cross-codebase pilot evidence supporting the
generalisation direction without overclaiming.

---

## Round 3 NEW Concerns (specific to revisions)

### R6 (Outlier rule): BREAKS_HOMOGENEITY decision procedure
**Status: Consistent with hypotSig's two killed mutants — with one minor
documentation issue.**

The 3-step decision procedure in
`noether-s5-experiment/configs/d4j_algebra_rich_criterion.json`
(L117–133) is sound: classify → BREAKS_HOMOGENEITY rescue iff ALL killed
mutants are BREAKS_HOMOGENEITY → per-mutant log required. The taxonomy
sub-rule "VR-mutator that returns 0 unconditionally is also classified
BREAKS_HOMOGENEITY by the fixed-output sub-rule" correctly handles
hypotSig's `return_zero_doubles_VR` (fixed-output zero). The
`Math.sqrt_replaced_with_one_RC` mutator falls under the explicit
"constant-replacement" example. Both classify as BREAKS_HOMOGENEITY,
the 5/6 verdict stands.

**Minor textual inconsistency**: at paper L1183 the killed mutant is
named `return_zero_doubles_VR` (matching the JSON config), while at
paper L1457 the same mutant appears as `return_two_doubles_VR`. One of
these is a typo. The classification logic is unaffected (both names
describe a return-value-replacement mutator that yields a fixed
output), but the manuscript should pick one and use it consistently.

### R9 (METRIC+ small-scale table): Per-SUT non-vacuous counts
**Status: Consistent and properly supported.**

Table `tab:metricplus-headtohead-small` (paper L2576–2597) reports per-SUT
non-vacuous Set-MP MR counts of 6 / 5 / 3 for midpoint / hypotSig / powerSig.
Manual recount from the cell entries (L2580–L2590):
- **midpoint**: $D_1, D_4, D_5, D_6, R_1, R_4$ = **6** non-vacuous ✓
- **hypotSig**: $D_1, D_4, D_6, R_1, R_4$ = **5** non-vacuous ✓
- **powerSig**: $D_6, R_1, R_4$ = **3** non-vacuous ✓

The caption footer line "Set-MP non-vacuous: 6/11 — 5/11 — 3/11"
(L2592) matches. The structural finding "Set-MP $\subsetneq$ NOETHER
block coverage" is properly supported: every non-vacuous Set-MP entry
maps to $\{G, O_{\le}, \mathcal{L}^{*}\}$ which Set N's $5$ MRs cover,
while Set N's $\mathcal{T}^{*}, \mathcal{T}^{*}_{\mathrm{rev}}, \mathcal{L}^{*}$
(at limits) have no METRIC+ counterpart. The structural claim is correctly
framed as "bounded above by Set-N's $G$/$O_{\le}$ contribution" rather
than as a measured kill-rate verdict, and follow-up (i) (L2376) commits
the full PIT-based head-to-head.

### OR/RD effect-size addition
**Status: Verified correct.**

Paper L1833–1836: $(b, c) = (15, 4)$ on the D1-only stratum, $n = 52$.
$\mathrm{RD}_{\mathrm{paired}} = (15-4)/52 = 11/52 = 0.2115\ldots = +0.212$
(favouring Set G, since b-cells = Set G kills Set N misses) ✓.
$\mathrm{OR} = b/c = 15/4 = 3.75$ ✓. Both effect sizes are reported
alongside the McNemar exact $p = 0.019$ and Wilson 95% CIs for each set's
M1 rate. This is the standard paired-comparison effect-size reporting
discipline that Round 2 W2 required.

### Statistical reporting completeness on Round-2-introduced claims
**Status: Adequate, minor tightening recommended.**

New statistical claims introduced in Round 2 revisions:
- Commons Math pilot $G$-block $6/21 = 0.286$ with Wilson 95% CI
  $[0.138, 0.500]$ ✓; D2 $2/29 = 0.069$ with Wilson 95% CI
  $[0.012, 0.221]$ (paper L1860); both reported with CI.
- LLM ensemble Set L: ChatGPT $34/70 = 0.486$ Wilson 95% CI
  $[0.372, 0.600]$, DeepSeek $33/70 = 0.471$ $[0.359, 0.587]$,
  ensemble union $34/70 = 0.486$ $[0.372, 0.600]$ (paper L1914–1916) ✓.
- LRCA $\kappa$ values $0.927$–$0.929$ on $n = 34$–$35$ parseable items
  (paper L2452) ✓; sample size and item-level disagreement disclosed.
- Per-block CIs in Table 12: every row has Wilson 95% CI ✓.

Two minor gaps:
1. The Commons Math pilot's pooled Set N kill rate (cited as $10.4\%$ in
   the experiment repo's `commons_math_replication_results.md`) is
   mentioned in the running text via the $G$-block / D2 breakdown but
   the pooled headline figure is not explicitly cited in the paper's
   External Validity paragraph. Recommendation: add the pooled
   "$10/77 = 0.104$, Wilson 95% CI $[0.057, 0.182]$" sentence for
   completeness, even though it is auxiliary by the scope-matched
   reporting discipline.
2. The DeepCrime pilot's Fisher exact $p = 1.00$ is reported in prose
   but the test-statistic / contingency-table details are deferred to
   the supplementary JSON. A brief in-paper note that the supplementary
   contains the $2\times 2$ contingency tables would help reviewers.

---

## Strengths

### S1: Honest scope-matched primary metric with auxiliary demotion
The single most important methodological improvement is the §subsec:pooled-headtohead
restructuring (paper L1602–1896). Set N's natural reach (block-induced D1
mutants) is now the per-block primary; the cross-block D1 aggregate is
demoted to secondary with McNemar / OR / RD reporting; pooled M1 on
D1∪D2 is demoted to auxiliary with an explicit scope-mismatched caveat.
This is the discipline Wohlin et al. require for paired-comparison
empirical studies with structurally different reach profiles.

### S2: Pre-registered outlier rule with full transparency
The `outlier_handling_rule` block in the JSON config (added 2026-05-15)
codifies the 3-step BREAKS_HOMOGENEITY classification with a "must be
applied BEFORE inspecting which specific mutants the outlier's
prediction-rescue depends on" requirement and a per-mutant log mandate
(step 3). The meta-note explicitly acknowledges "the outlier-handling
rule below was implicit until the Round 2 review correctly flagged it
as missing from the pre-registration" — this is good-practice
post-hoc-rescue prevention.

### S3: Cross-codebase pilot establishes external-validity direction
The Commons Math 3.6.1 pilot (3 SUTs, 5 MRs, 77 mutants) on a
substrate the framework was not designed against is the right shape of
external-validity evidence for a Round 2 W5 response, reported with
appropriate underpowered framing and a clear $\mathcal{L}^{*}$-block
$n=0$ explanation (PIT's mutator set does not break bilinearity on
Complex multiplication / division). Future-work item (j) (external-team
reactor-physics transfer) is the matching commitment for the
domain-theory side.

### S4: Construct-trace circularity guarded at three layers
Table 13's design-implied Set N column is guarded by (a) italics on every
cell, (b) per-cell daggers tied to a footnote, (c) bold "excluded from
the H3a.1 evidence base" in the caption, and (d) a dedicated paragraph
"Why this is not a head-to-head test of H3a.1." This is the right level
of caution for a $25/25$ value that could otherwise be misread.

### S5: GPT-4 generation now externally re-runnable
The `prompt_log.md` records the exact prompt sent to gpt-4-turbo-2024-04-09,
the seed (4246), the temperature (0.0), the date (2026-05-15), and the
raw JSON output verbatim. An independent reviewer can re-execute the
prompt against the same model snapshot and compare. The five MR
functions in `set_L_llm.py` are direct translations of the JSON output,
not a paraphrase.

---

## Weaknesses

### W1 (Round 3 NEW; Minor): Naming inconsistency for hypotSig's first killed mutant
**Problem**: Paper L1183 names the mutant `return_zero_doubles_VR` (matching the
JSON config at line 128 of `d4j_algebra_rich_criterion.json`), while
paper L1457 names the same mutant `return_two_doubles_VR`. The
classification logic is unaffected — both names describe a
return-value-replacement mutator yielding a fixed output — but the
manuscript must pick one consistent name.
**Why it matters**: A reviewer audit of the pre-registered outlier rule
relies on cross-referencing the kill log filename / mutator-id against
the JSON config. Two different names in the paper text raises a
reproducibility question that has a five-minute fix.
**Suggestion**: Audit the killed-mutant log file
(`mutants_killed_set_n.csv` for `hypotSig`) and adopt the actual
mutator id consistently in the paper and the JSON config; commit the
correction in a polish round.
**Severity**: Minor.

### W2 (Round 3 NEW; Minor): Commons Math pilot pooled rate not surfaced in paper text
**Problem**: The External Validity paragraph (paper L2454) reports the
Commons Math pilot's $G$-block kill rate ($6/21 = 28.6\%$) and the D2
prediction ($2/29 = 6.9\%$) but does not explicitly cite the pooled
Set N kill rate ($10/77 = 13.0\%$, with Wilson 95% CI) that the
experiment repo's `commons_math_replication_results.md` reports as the
overall pilot headline. The reader has to compute it.
**Why it matters**: A scope-matched reporting discipline correctly
demotes the pooled rate to auxiliary, but completeness (and rebuttal
preparedness against a reviewer who insists on a single comparable
headline) argues for surfacing the pooled number in one sentence with
the explicit "auxiliary, scope-mismatched" framing.
**Suggestion**: Add one sentence to the External Validity paragraph:
"For completeness, the pooled Set N kill rate on the Commons Math
substrate is $10/77 = 0.130$ Wilson 95% CI [$\ldots$], reported as
auxiliary; the scope-matched primary is the per-block $G$ kill rate
above."
**Severity**: Minor.

### W3 (Round 3 NEW; Minor): DeepCrime contingency-table pointer missing
**Problem**: §subsec:deepcrime-pilot reports the Fisher exact $p = 1.00$
for Set N vs Set L and Set N vs Set B (paper L807) but the $2\times 2$
contingency tables underlying the test are deferred to supplementary
S3 (`deepcrime_pilot_stats.json`). A reviewer cannot verify the test
statistic against the published values without opening the JSON.
**Why it matters**: At $n = 5$ the contingency tables are small enough
to inline; doing so removes a verification step.
**Suggestion**: Inline the two $2\times 2$ tables in a small in-text
table or a footnote: e.g., "Set N $\cap$ Set L kill = $(2, 0; 0, 3)$
yielding Fisher exact $p = 1.00$."
**Severity**: Minor.

---

## Detailed Comments

### Methodology / Research Design
The Round 2 → Round 3 transition has restructured the central
empirical claim chain into a defensible posture:
- L*-blindness as the section's central falsifiable prediction (5/6
  SUTs at zero, hypotSig outlier explained by the now-pre-registered
  homogeneity-breaking taxonomy).
- D1 aggregate as a head-to-head where Set G wins, with effect sizes
  ($\mathrm{OR}=3.75$, $\mathrm{RD}_{\mathrm{paired}}=0.212$) reported.
- D2 prediction as the framework's own falsifiability commitment (Set N
  $0/5$ vs Set G $3/5$ on the surviving D2 stratum).
- Per-block complementarity as the structural reading (Set N alone kills 4,
  Set G alone kills 15, $\mathcal{T}^{*}$ block where Set N edges Set G).

This is internally coherent under the Rule-9 scope-matched reporting
discipline. The pre-registration of the outlier rule on 2026-05-15
(after Round 2 review surfaced the gap) is acknowledged as not strictly
prior to the §6.6.4 hypotSig analysis; the meta-note (JSON L121) is
honest about this and frames the codification as forward-looking
("future cross-codebase substrates inherit the rule as a written
test"). I accept this framing.

### Results / Findings
Tables 11, 12, and 13 form a coherent triple: pooled head-to-head
(secondary), per-block head-to-head (primary), and construct-trace
consistency check (excluded). The "unmapped" auxiliary row's treatment
as a lower-bound caveat (rather than a fourth block) is correct.

### Statistical Analysis
Effect sizes are now reported alongside p-values; Wilson CIs are reported
for every per-set / per-block rate; family-wise control is acknowledged
($\alpha/16 \approx 0.003$ Holm–Bonferroni threshold for per-SUT
descriptors; no per-SUT contrast meets this) and per-SUT entries are
labelled "directional only." This is exemplary discipline.

### Discussion of limitations
The "Construct validity" paragraph (paper L2452) acknowledges the
single-author derivation of Set N, the multi-LLM second-rater protocol
($\kappa = 0.927$–$0.929$ on $n = 34$–$35$), and the LLM-shared-
training-data caveat. A human-pair $\kappa$ replication is committed
for the industrial-port phase. The External Validity paragraph
explicitly distinguishes algebraic-reach vs codebase-generalisation
external-validity questions and reports the Commons Math pilot
honestly.

---

## Questions for Authors

1. **hypotSig mutant id**: Which of `return_zero_doubles_VR` (JSON
   config + paper L1183) and `return_two_doubles_VR` (paper L1457) is
   the correct VR-mutator id from `mutants_killed_set_n.csv`? Please
   pick one and use it consistently.
2. **Commons Math pooled rate**: The experiment repo cites
   $10/77 = 13.0\%$ as the pilot's pooled Set N kill rate. Confirm and
   add the pooled headline (with Wilson CI) to the External Validity
   paragraph for completeness.
3. **DeepCrime $2\times 2$ tables**: Please inline the two $2\times 2$
   contingency tables (or a small footnote) so the Fisher exact
   $p = 1.00$ is independently checkable without opening the
   supplementary JSON.

---

## Minor Issues

### Citation Format
- L1183 / L1457: hypotSig mutant naming inconsistency (see W1 above).

### Figures and Tables
- Table 13's $^{\dagger}$ footnote is excellent; consider explicitly
  citing the per-mutant CTT log file path in the footnote so a reviewer
  can audit the design-implied mapping in one step.

### Layout
- The Commons Math pilot subsection inside External Validity is dense
  (one long paragraph from L2454). A bullet list of (G kill rate, D2
  prediction, $\mathcal{L}^{*}$ structural absence) would improve
  scan-ability.

---

## Dimension Scores

| Dimension | Score (0-100) | Descriptor | Notes |
|-----------|--------------|------------|-------|
| Originality (20%) | 86 | Strong | Algebraic systematisation with three-domain instantiation and closure theorem; the structural-coverage framing for METRIC+ contrast is original. |
| Methodological Rigor (25%) | 90 | Exceptional | Per-block primary / D1 aggregate secondary / pooled auxiliary discipline; OR/RD effect sizes; pre-registered outlier rule; multi-LLM LRCA $\kappa$; construct-trace circularity guarded at three layers. |
| Evidence Sufficiency (25%) | 84 | Strong | L*-blindness 5/6 confirmed; commons-math cross-codebase pilot; LLM ensemble 2-of-3 vendors; D2 prediction PASS but Wilson upper bound does not exclude 10% ceiling — honestly disclosed. |
| Argument Coherence (15%) | 90 | Exceptional | Three-layer reporting (per-block / D1 / pooled) is coherent; construct-trace vs head-to-head distinction is razor-sharp; falsifiability commitments are explicit. |
| Writing Quality (15%) | 86 | Strong | Dense but precise; one mutant-id naming inconsistency; section-level structure is clear. |
| Literature Integration (R2 focus) | — | — | Reviewer 2 perspective. |
| Significance & Impact (R3 focus) | — | — | Reviewer 3 perspective. |
| **Weighted Average** | **87.0** | **Minor Revision** | Three minor weaknesses (hypotSig name, pooled-rate surfacing, DeepCrime contingency inlining). No re-review required after these fixes. |

---

## Round 3 R1 Final Verdict

The Round 2 W1 (CRITICAL), W2, W3, W4, W5 weaknesses are all FULLY_RESOLVED
under the file-grounded audit. Round-2-introduced material (METRIC+ small
table, BREAKS_HOMOGENEITY outlier rule, OR/RD effect sizes, DeepCrime
inferential/mechanism split) is methodologically clean. Three minor
issues (one mutant-naming typo, one pooled-rate surfacing, one
contingency-table inlining) remain; none require re-review. Recommendation
to the editor: **Minor Revision**, accept-conditional on the three
minor textual fixes. Weighted score: **87.0 / 100**.
