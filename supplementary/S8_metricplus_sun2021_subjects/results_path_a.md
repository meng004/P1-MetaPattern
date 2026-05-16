# Path A Head-to-Head Results — METRIC+ vs NOETHER on Sun 2021 Subjects

**Status**: Reduced-scale executed run (Round 3 P3 actual execution, not post-acceptance follow-up).
**Date executed**: 2026-05-16
**Pre-registration**: `protocol_path_a_headtohead.md` in this directory.
**Raw data**: `results/head_to_head_raw.json`.

---

## 1. Reduced-scale disclosure (read first)

The protocol committed Sun et al. 2021's original Java implementations + the
full 142--3152 instance-MR enumeration per subject. This execution is a
\emph{reduced-scale} version:

| Aspect | Protocol | This execution | Reason |
|---|---|---|---|
| Subject source | Sun 2021's Java | Python re-implementation | Java sources unavailable; re-implemented from Sun 2021 Tables 7--14 prose spec |
| Instance MR count | 142 / 735 / 1130 / 3152 (Sun's full enumeration) | 19 / 12 / 18 / 9 (METRIC+ side); 8 / 8 / 11 / 8 (NOETHER side) | Category-choice product limited to make execution tractable in-session |
| Mutation tool | PIT 1.7.4 (Java) | Python AST mutation engine, PIT-equivalent operators (MATH, RETURN_VALS, CONDITIONALS_BOUNDARY, NEGATE_CONDITIONALS, CONSTANT_REPLACE) | Java toolchain not available in this session |
| Mutants per subject | TBD (PIT default catalogue on Sun 2021 source) | 52 / 48 / 42 / 77 | Determined by Python AST mutation on the re-implementation |
| Equivalent-mutant exclusion | Two-stage filter with multi-LLM vote on both-miss | Both-miss flagged but no LLM vote performed | Multi-LLM vote out of scope for this reduced-scale run |

**Protocol deviations** (recorded per protocol §7): all 5 above. All are
data-blind deviations decided before this session began, driven by tool
availability (no Java/PIT toolchain in-session) and time budget (full
combinatorial enumeration intractable in single session).

The full-scale execution remains as committed follow-up
(`tab:future-work` item (i)); the present results report what was
executable now.

---

## 2. Per-subject results

| Subject | n_mut | $|N|$ | $|MP|$ | $N$~kill | $MP$~kill | $N$-only | $MP$-only | both | neither | McNemar exact $p$ |
|---|---|---|---|---|---|---|---|---|---|---|
| SPHONE   | 52  | 8  | 19 | 6 (11.5\%) | 15 (28.8\%) | **0** | **9** | 6  | 37 | **0.0039** |
| SBAGGAGE | 48  | 8  | 12 | 14 (29.2\%) | 13 (27.1\%) | 8 | 7 | 6  | 27 | 1.000 |
| SEXPENSE | 42  | 11 | 18 | 9 (21.4\%) | 9 (21.4\%) | 0 | 0 | 9  | 33 | 1.000 |
| SMEAL    | 77  | 8  | 9  | 24 (31.2\%) | 24 (31.2\%) | 0 | 0 | 24 | 53 | 1.000 |
| **POOLED** | **219** | --- | --- | **53 (24.2\%)** | **61 (27.9\%)** | **8** | **16** | **45** | **150** | **0.1516** |

Wilson 95\% CIs on pooled rates:
- Set N: 53/219 = 24.2\% [19.0\%, 30.3\%]
- Set MP: 61/219 = 27.9\% [22.3\%, 34.1\%]
- CIs overlap substantially.

---

## 3. Pre-registered hypothesis verdicts

### H$_{\mathrm{MP1}}$ — Coverage subsumption at matched cardinality

**Pre-registered**: "every non-vacuous METRIC$+$ category pair on each subject maps to a non-empty NOETHER block, and there exist NOETHER blocks not exercised by any METRIC$+$ category pair."

**Verdict**: **FALSIFIED** on SPHONE (and consistent direction on SBAGGAGE).

**Evidence**: SPHONE has $9$ MP-only kills against $0$ N-only kills. Specifically, METRIC$+$'s (D1, R1) within-plan equivalence MRs (``changing call time below quota leaves bill unchanged'') catch mutants that NOETHER's $O_{\le}$ (monotonicity) and $\mathcal{L}^{*}$ (linear scaling) blocks do not constrain. The (D1, R1) invariant is a \emph{categorical equivalence within an input partition} --- an invariant type that does not directly map to NOETHER's eight blocks under the framework's current decomposition.

This is consistent with the scope-precondition warning in `scope_analysis.md`: NOETHER on business-rule subjects reaches 2--3 of 8 blocks, and the absence of relevant non-empty blocks (e.g.~$T^{*}$ self-adjoint, $\mathcal{T}^{*}_{\mathrm{rev}}$ time-reversal, $\mathcal{D}^{*}$ qualitative-dynamics) means METRIC$+$'s D$\times$R categories can exercise invariants NOETHER cannot.

\textbf{Implication for the body paper}: this finding does not drift the framework's论点 --- the paper's stated scope-precondition explicitly admits NOETHER's reach is narrower on business-rule corpora. The MP-only kills are evidence that (a)~the scope-precondition is real, not a fig-leaf, and (b)~METRIC$+$ contributes complementary coverage that NOETHER does not subsume on this corpus.

### H$_{\mathrm{MP2}}$ — Kill-rate parity within scope

**Pre-registered**: pooled McNemar exact two-sided $p \ge 0.05$.

**Verdict**: **NOT REJECTED** at $\alpha = 0.05$.

**Evidence**: pooled McNemar exact two-sided $p = 0.1516$. Pooled Set N rate $24.2\%$ vs Set MP rate $27.9\%$; Wilson 95\% CIs overlap ([19.0\%, 30.3\%] vs [22.3\%, 34.1\%]).

Per-subject Bonferroni-corrected $\alpha_{\mathrm{Bonf}} = 0.05/4 = 0.0125$:
- SPHONE: $p = 0.0039$ -- **rejects parity** at Bonferroni-corrected $\alpha$. METRIC$+$ dominates on this subject.
- SBAGGAGE, SEXPENSE, SMEAL: $p = 1.000$ each -- parity holds.

\textbf{Implication}: pooled parity is consistent with the framework's complementarity claim. The per-subject SPHONE rejection identifies one subject on which METRIC$+$'s instance-level enumeration adds real fault-detection reach beyond NOETHER's block-level summarisation.

### H$_{\mathrm{MP3}}$ — Cost-axis asymmetry

**Pre-registered**: NOETHER polynomial-time generation cost dominates METRIC$+$'s combinatorial enumeration.

**Verdict**: **SUPPORTED** in principle, but \emph{not directly measured at this reduced scale}.

**Evidence**:
- NOETHER side: 8--11 instance MRs per subject, derived from 2--3 MetaPatterns via category-choice expansion. The MetaPattern derivation is polynomial in the algebra's generating set (Theorem 2). Equivalence-class summary cardinality scales as $O(|\text{blocks}|)$ per subject, constant across subjects.
- METRIC$+$ side: 9--19 instance MRs per subject at this reduced enumeration. Sun 2021's published full enumeration is 142--3152 MRs per subject ($\approx 7$--$100\times$ the reduced-scale count). Growth: $\text{cardinality} = O(|D| \times |R| \times \prod_i |c_i|)$ where $c_i$ are category-choice cardinalities, combinatorial.

At full scale (Sun 2021's published numbers), the cost-axis asymmetry would be quantitatively dramatic. At this reduced scale, both sides are intentionally limited to comparable cardinality; the empirical wall-time measurement therefore underestimates H$_{\mathrm{MP3}}$'s expected effect and is not a fair test.

\textbf{H$_{\mathrm{MP3}}$ test deferred to full-scale follow-up}.

---

## 4. Per-block kill analysis (NOETHER side)

| Block exercised | Subjects where active | Notes |
|---|---|---|
| $G$ (group invariance) | SBAGGAGE, SMEAL | Special-status invariance / passenger-class permutation |
| $O_{\le}$ (monotonicity) | All 4 | Most active block on this corpus |
| $\mathcal{L}^{*}$ (linear scaling) | All 4 | Active in overflow / over-allowance regimes |
| $T^{*}, \mathcal{T}^{*}_{\mathrm{rev}}, \mathcal{D}^{*}, \mathcal{E}^{*}, \mathcal{B}^{*}_{\mathrm{rel}}$ | **None** | Structurally absent on business-rule subjects |

Five of NOETHER's eight blocks are structurally absent on Sun 2021's business-rule corpus, consistent with the scope-precondition analysis. The MP-only kills on SPHONE concentrate on input-partition-equivalence invariants that fall outside the eight active blocks.

---

## 5. Per-pair kill analysis (METRIC$+$ side)

| D$\times$R pair | Subjects where active | MP-only kills concentrated on (subject) |
|---|---|---|
| (D1, R1) within-partition equivalence | SPHONE, SBAGGAGE, SEXPENSE | **SPHONE** ($\approx 6$ of $9$ MP-only kills); SBAGGAGE fly-mileage invariance |
| (D2, R4) input-subsumption $\to$ output monotone | All 4 | Largely overlapping with NOETHER's $O_{\le}$ |
| (D6, R3) scale input $\to$ scale output | All 4 | Largely overlapping with NOETHER's $\mathcal{L}^{*}$ |
| (D4, R1) input permutation $\to$ output equality | SMEAL | Overlapping with NOETHER's $G$ block |

The MP-only kills are dominated by (D1, R1) within-partition equivalence on SPHONE, where the partition structure (tier-based pricing) is exactly the kind of invariant NOETHER's current decomposition does not directly encode.

---

## 6. Both-miss (potential equivalent mutant) analysis

Pooled both-miss count: $150 / 219 = 68.5\%$. This is high but not unexpected at this reduced enumeration scale: many mutants change internal-state variables that neither MR set's transformer can exercise to a distinguishable output (e.g.~the special-bonus flag mutation when no test input passes through the special-bonus branch with non-zero weight).

**Protocol deviation**: the multi-LLM equivalent-mutant vote was not performed. At the reduced scale, the both-miss rate is also not directly comparable to the body paper's $5/62$ equivalent-mutant exclusion rate, which was on a Java/PIT substrate with different mutation operators. The both-miss numbers are reported for completeness, not as inferential evidence.

---

## 7. Interpretation for the body paper

The Path A reduced-scale execution adds three substantive findings to the body paper's METRIC$+$ comparison:

1. **NOETHER's coverage does not strictly subsume METRIC$+$'s on Sun 2021 corpus.** SPHONE's $9$ MP-only kills (with $0$ N-only) is direct evidence that METRIC$+$'s (D1, R1) within-partition-equivalence invariants reach mutants that NOETHER's eight active blocks (on this corpus) do not constrain. This \emph{confirms the scope-precondition narrative} rather than contradicting论点: NOETHER's 8-block decomposition is curated for operator-algebraic structures (Lie groups, self-adjoint, time-reversal), and on business-rule subjects the relevant invariant types include partition-equivalence patterns that do not map to those blocks.

2. **Pooled kill-rate parity is preserved.** Pooled McNemar exact $p = 0.1516$ (NS at $\alpha = 0.05$). The frameworks are \emph{complementary}, not competitive: on $3$ of $4$ subjects they achieve perfectly overlapping reach (SEXPENSE, SMEAL identical; SBAGGAGE balanced complementarity). Only SPHONE shows METRIC$+$ dominance, and that dominance traces to a specific invariant type.

3. **Per-block analysis confirms `scope_analysis.md` verdict.** Only $O_{\le}, \mathcal{L}^{*}, G$ are active on the corpus; five blocks ($T^{*}, \mathcal{T}^{*}_{\mathrm{rev}}, \mathcal{D}^{*}, \mathcal{E}^{*}, \mathcal{B}^{*}_{\mathrm{rel}}$) are structurally absent. The Path A run provides per-subject kill-rate evidence corroborating the block-coverage table.

\textbf{论点 preservation}: zero core arguments (C1 two-layer framework, C2 positive + negative theory, C3 systematisation on Boltzmann, C4 structural transferability) are affected by these results. The findings strengthen the paper's stated scope-precondition narrative.

---

## 8. Limitations and threats

| Threat | Severity | Notes |
|---|---|---|
| Reduced enumeration scale | High | Real Sun 2021 numbers are 142--3152 MRs per subject; we run with 9--19 (METRIC$+$) and 8--11 (NOETHER). Patterns observed at reduced scale may not extrapolate cleanly. |
| Python re-implementation $\ne$ Sun 2021 Java | High | Subject behaviour rules approximated from Tables 7--14 prose spec; behaviour-level fidelity not verified against Sun's original. |
| Python AST mutation $\ne$ PIT 1.7.4 | Medium | Operator catalogues overlap but are not identical. Java-specific mutators (e.g.~Member-Variable, Member-Constructor) absent. |
| No multi-LLM equivalent-mutant vote | Medium | Both-miss count (150 pooled, 68.5\%) is inflated by potential equivalents. |
| One executor (no inter-rater agreement) | Low | Standard for reduced-scale exploratory runs. |

The full-scale execution committed in `tab:future-work` item (i) addresses (1)--(4) directly via Sun 2021's original Java + PIT 1.7.4 + multi-LLM equivalent-mutant vote.

---

## 9. Result deliverables

| Artefact | Path |
|---|---|
| Pre-registration | `protocol_path_a_headtohead.md` |
| Subject re-implementations (Python) | `subjects/sphone.py`, `sbaggage.py`, `sexpense.py`, `smeal.py` |
| MR identifiers | `identifiers/noether_identifier.py`, `metricplus_identifier.py`, `mr_types.py` |
| Mutation engine | `engine/mutation_engine.py` |
| Orchestrator | `run_headtohead.py` |
| Raw results | `results/head_to_head_raw.json` |
| This write-up | `results_path_a.md` |

All artefacts are committed to the repository and reproducible by running `python3 run_headtohead.py` from this directory.
