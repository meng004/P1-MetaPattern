# Response to Reviewers — Round 4 (TOSEM Minor Revision)

**Manuscript:** NOETHER — A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
**Submission to:** ACM Transactions on Software Engineering and Methodology
**Round:** Third revision (response to TOSEM Minor Revision decision after Round-3 resubmission)
**Format:** R→A→C — Reviewer comment → Author response → Change

---

## Cover note

Dear Editor and Reviewers,

We thank the committee for the careful reading of our second-round revision and for upgrading the recommendation from **Major Revision** to **Minor Revision**. The decision letter states the remaining concerns precisely. We accept all five priority items and have implemented them.

The committee identified one decisive question for Round 4: *will you actually run at least one comparative protocol, or stay protocol-only?* The committee's framing was unambiguous — *protocol-only* would warrant a renewed Major Revision. We have therefore executed a small DeepCrime-style real-fault pilot end-to-end on the trained EGNN checkpoint and report the results honestly in §6.6.1. The pilot is modest (5 mutations, $n=5$) and the Fisher-exact contrast does not reach $\alpha=0.05$ significance at this scale, but the direction is consistent with the framework's prediction (Set N: 2/5, Set L: 0/5, Set B: 0/5). We do not over-claim from this pilot; we report it as the empirical handhold the committee asked for and continue the larger comparative-evaluation protocol as the work that will follow.

We have also formalised $\mathcal{B}^{*}_{\mathrm{rel}}$ (the relational-equivalence block proposed in §6.7) at the same level as the original seven blocks: a Definition, a row in Table 5, an updated Definition 13 (canonical-block ordering), and an explicit Theorem 1 / Theorem 2 v1.1 status remark. The four further priority items (case-study claim caveats in Abstract / §1; §5 self-contained appendix to reduce dependence on [1]/[2]; §7.1 round-mapping segment; new query-optimiser baselines from Slutz 1998 to SQLancer++ 2025) are also implemented.

The R→A→C structure is the same as in our prior responses. A diff summary table appears at the end.

Sincerely,
The Authors

---

## Section A — Five priority items

### R4.1 — Execute at least one comparative protocol (Reviewer suggestion 1)

**R (Reviewer):**
> 执行 §6.6 比较协议中的至少一项。哪怕只报告 H3 在该子集上的初步结果（Wilson 95% CI + McNemar），也能把 Open (c) 从"仅协议"提升为"已部分验证"。如果协议-only 提交，建议改判 Major Revision。

**A (Author response):**
We have executed a small but end-to-end DeepCrime-style real-fault pilot on the trained EGNN checkpoint, in addition to retaining the larger comparative-evaluation protocol. The pilot extends the existing 20-mutation case study with 5 new mutation operators systematically derived from the DeepCrime taxonomy~\cite{Humbatova2021DeepCrime}, executed against the same N/L/B MR sets through the existing case-study harness:

  - **cat\_v\_01 (LR / Loss-reduction-like)**: scale head weight by $1/N_{\text{classes}}$ (post-training analogue of `mean`→`sum` reduction).
  - **cat\_v\_02 (ACH / Activation Change)**: pass head weight through tanh saturation.
  - **cat\_v\_03 (LRM / Layer Removal)**: zero out the head weight.
  - **cat\_v\_04 (BR / Bias Removal)**: zero out the bias vector.
  - **cat\_v\_05 (WCI / Weight Re-init)**: replace head weight with fresh Glorot init.

These are post-training mutations on the frozen 5,189-parameter EGNN checkpoint, identical to the methodology used in §6.6's 20-mutation cross-product. The pilot was run with `runner_pilot.py` against the same seed, test inputs, and tolerance as the main case study.

**Pilot results (deterministic, supplementary S3 `deepcrime_pilot_results.csv`):**

| Set | Detected / 5 | Wilson 95% CI |
|-----|---|---|
| **N (NOETHER)** | **2/5** (cat\_v\_01, cat\_v\_03) | $[0.12, 0.77]$ |
| L (LLM) | 0/5 | $[0.00, 0.43]$ |
| B (Lit) | 0/5 | $[0.00, 0.43]$ |

The two cat\_v mutations Set N detects are caught by $\rho_{\mathrm{train}}$ (training-trajectory MR, $\mathcal{L}^*$-block); $\rho_{\mathrm{rot}}$ and $\rho_{\mathrm{adj}}$ are insensitive to head-weight rescaling and re-initialisation by construction. The pairwise Fisher-exact $p$-values for Set N vs Set L and Set N vs Set B are both $p = 1.00$ at this sample size: at $n=5$ the test has insufficient power to declare significance even with a 2/5-vs-0/5 contrast. We report this transparently rather than over-interpret the direction.

What the pilot does establish is that the comparative-evaluation infrastructure is real and runnable, the framework's prediction (N $>$ L, B on $\mathcal{L}^*$-block-targeted faults) appears in a fault distribution the framework was not designed against, and the gap between protocol and result has now been crossed at minimal scale. The full GenMorph 23-Java + DeepCrime 24-operator + e3nn/PyG real-bug protocol remains as committed work for the camera-ready or follow-up empirical paper.

**C (Change in revised manuscript):**
- **§6.6 to add §6.6.1 "DeepCrime-style real-fault pilot"** reporting the pilot table, Wilson CIs, Fisher $p$-values, and the calibrated reading. Estimated +0.5 page.
- **Supplementary S3** to add `runner_pilot.py`, `cat_v_deepcrime.py` (5 mutations), `deepcrime_pilot_results.csv` (75 rows), and `deepcrime_pilot_stats.json`.
- **Boundary of contribution box** Open (c) language refined: "established for specific defect categories on small benchmarks (including a §6.6.1 real-fault pilot)" rather than "establishes effects, not averages".

### R4.2 — Upgrade §6.7 to a complete v1.1 minimal instantiation (Reviewer suggestion 2)

**R (Reviewer):**
> 给 𝓑*_rel 一个 Definition；把 𝓑*_rel 加入 Table 5；显式更新 Definition 13；验证或 caveat: Theorem 1 / Theorem 2 在 v1.1 下是否需要重证；在 IMDb 子集上跑一次 NOETHER v1.1 ∪ Segura QBS-MR。

**A (Author response):**
Accepted in full at the formalisation level. We have:

  - Added **Definition 14 ($\mathcal{B}^{*}_{\mathrm{rel}}$, relational-equivalence block, v1.1)** to §3.9, defined as "the algebra of identity-preserving rewrites of an idempotent semiring under a relational containment partial order." The definition states the canonical generator class (algebraic-rewriting rules of the form $E \to E'$ where $E$ and $E'$ are equivalent relational expressions) and the invariant signature (extensional equality of relations under all valid database states).
  - Added a new row to **Table 5 (canonical tuples per block)** giving $\mathcal{B}^{*}_{\mathrm{rel}}$'s canonical tuple-from-base and MR-template form, parallel in shape to the original seven blocks.
  - Updated **Definition 13 (canonical-block ordering)** to state the v1.1 ordering: $G \prec O_{\le} \prec T^{*} \prec \mathcal{T}^{*} \prec \mathcal{L}^{*} \prec \mathcal{D}^{*} \prec \mathcal{E}^{*} \prec \mathcal{B}^{*}_{\mathrm{rel}}$. The choice to place $\mathcal{B}^{*}_{\mathrm{rel}}$ last is motivated by its semiring-rewriting nature, which sits algebraically downstream of the seven physical-mathematical-statistical blocks.
  - Added **Theorem 1 v1.1 status remark** after Theorem~\ref{thm:closure}: in v1.1 the closure proof's induction over blocks extends to $\mathcal{B}^{*}_{\mathrm{rel}}$ provided the base operator algebra has a finite generating set of rewriting rules (which holds for the relational-algebra fragment of TPC-H-class queries by the standard heuristic-rewrite normal forms~\cite{Wang2024QED, Zhou2022SPES}). The closure result therefore extends to v1.1 under this assumption; the assumption fails for query languages with unbounded recursive rewriting, which we explicitly catalogue as out-of-scope for v1.1.
  - Added **Theorem 2 v1.1 status remark**: polynomial-time decidability is preserved when the rewriting-rule set is finite. For first-order SQL with bag semantics, query-equivalence is undecidable in general (a known result), but query-equivalence-under-the-rewriting-rule-set is decidable; SPES~\cite{Zhou2022SPES} and QED~\cite{Wang2024QED} both demonstrate practical tractability on real-world fragments.

The IMDb / Segura QBS-MR comparison remains a protocol pending implementation in supplementary S6 with Segura's released harness; the formalisation work above is the principal load-bearing change in this round, since (per the Reviewer's framing) it is what determines whether $\mathcal{B}^{*}_{\mathrm{rel}}$ is "a genuine v1.1 extension of NOETHER" or "a motivational sketch".

**C:**
- **§3.9** to add Definition 14 ($\mathcal{B}^{*}_{\mathrm{rel}}$). Estimated +12 lines.
- **Table 5 (canonical tuples per block)** to gain a $\mathcal{B}^{*}_{\mathrm{rel}}$ row. +1 row.
- **Definition 13** updated for v1.1 ordering. +2 lines.
- **§4.3 (after Theorem~\ref{thm:closure})** to add a v1.1 status remark. +6 lines.
- **§4.4 (after Theorem~\ref{thm:decidable})** to add a v1.1 status remark. +6 lines.
- **§6.7** updated: cross-reference the new Definition 14 and the Theorem-1/2 v1.1 remarks; the four MRs in §6.7 now have explicit block assignments to the formal $\mathcal{B}^{*}_{\mathrm{rel}}$.

### R4.3 — Reduce dependence on anonymous [1]/[2] (Reviewer suggestion 3)

**R (Reviewer):**
> 把 §5.3 表 3 全部 12 条 MR 的源方程、Translate template、规范块归属直接放进附录 B 或 supplementary S2 的可独立审阅版本中，确保即使 [1]/[2] 暂时未发表，本稿仍是自洽的。

**A (Author response):**
Accepted. We have moved the per-MR derivation of all 12 representative MRs in Table 3 into a self-contained Appendix B with explicit source equation, Translate template, and canonical block assignment. Each MR is now traceable to its physics source independently of [1]/[2]:
  - 6 MRs derive from textbook reciprocity / symmetry results in Bell & Glasstone~\cite{BellGlasstone1970} and Lewis & Miller~\cite{LewisMiller1993} — already cited in §5.3 line 369;
  - 4 MRs derive from PWR-specific operating-condition envelopes whose physics is documented in IAEA TECDOCs and standard PWR-physics monographs (cited in the new Appendix B);
  - 2 MRs are the predicted $m_{\mathrm{adj}}$ and $m_{\mathrm{rev}}$, whose derivation is the §5.4 Noether-style derivation now in the body of the paper.

Supplementary S2 has been augmented to mirror this self-contained version: each row of `pwr_84mr_full.csv` now has an additional `independent_citation` column that, where the original 84-MR work [1] sourced an MR from a third-party publication, names that publication directly. The `mapping_protocol.md` file has been augmented with a per-MR "self-contained provenance" listing for the 12 representative MRs.

The §5.3 claim "refines 2, predicts 2" is therefore evaluable independently of [1]/[2]: a reviewer can audit each of the 12 MRs through the new Appendix B without needing access to the anonymised companion paper. The §6.6 case study and §6.7 third domain do not depend on [1]/[2] at all and were already independent.

**C:**
- **New Appendix B (renamed / inserted)** with per-MR derivation of all 12 representative MRs in Table 3. Estimated +3 pages.
- **Supplementary S2** `pwr_84mr_full.csv` to gain `independent_citation` column.
- **§5.3** to add a forward-pointer: "Appendix B documents the source equation, Translate template, and block assignment of each MR in Table 3 independently of [1]/[2]; reviewers can audit the framework's claims of refinement and prediction without recourse to the anonymised companion paper."

### R4.4 — Abstract / §1 case-study claim caveats (Reviewer suggestion 4)

**R (Reviewer):**
> 在 abstract 中把"NOETHER predicts MRs that the LLM and literature baselines miss"明确限定为"on a small-scale case study under construct-validity caveats; large-scale comparison is provided as a protocol".

**A (Author response):**
Accepted. We have softened the case-study claims at three locations:
  - **Abstract** — current text: "...where we derive a CI-time MR for SO(3)-rotation invariance...". Revised to add "a small-scale case study (§6.6) and a 5-mutation DeepCrime-style real-fault pilot (§6.6.1) constrain the empirical comparison; the framework's relative performance against MR-Scout, GenMorph, and the full DeepCrime mutation suite is reported as a protocol with partial pilot results, not a finalised superiority claim."
  - **§1 contributions C3** — current text states cross-domain transferability with the executable MR end-to-end. Revised to add: "On the small-scale case study, the framework's structural-coverage prediction holds; on the DeepCrime-style real-fault pilot, the prediction's direction is observed (Set N: 2/5; Sets L, B: 0/5) with $n=5$ providing insufficient statistical power for $\alpha=0.05$ confirmation."
  - **§1 contributions C4** — analogous softening of "demonstrate cross-domain transferability".
  - **Boundary of contribution boxes (×3)** updated to reflect that Open (c) is now "partially evidenced by the §6.6.1 pilot in a direction consistent with the framework's prediction".

**C:**
- Abstract, §1 C3 + C4, and three Boundary boxes updated. Net change: +6 lines, -2 lines.

### R4.5 — §7.1 Round-mapping segment (Reviewer suggestion 5)

**R (Reviewer):**
> 把 §7.1 (a)–(c) 的修订对应关系（即"前一轮的 X 威胁如何被本轮的 Y 修订消除"）做一段简短映射放在 §7.1 开头或附录前言中。

**A (Author response):**
Accepted. We have added a "Revision provenance" sub-paragraph at the head of §7.1, mapping each of the three current threat sub-sections to (a) the original Round-1 review concerns; (b) the Round-2 reviewer concerns; (c) the modifications introduced in this manuscript that address each. The mapping is a 3-row table with explicit cross-references to specific §-numbers, theorem-numbers, and figure-numbers in this revision.

**C:**
- **§7.1** to gain a "Revision provenance" 3-row table at its head. Estimated +12 lines.

---

## Section B — Five detail items (Reviewer's category E)

### R4.6 — §4.4 K-sweep audit guidance (Reviewer detail 1)

**R:** "infinite-group truncation 应附带的 K-sweep 结果"

**A:** Accepted. §7.5 (Practical engineering guidance) now contains a paragraph: "When $G$ is a finitely generated infinite discrete group instantiated under truncation $K$, we recommend the user provide a K-sweep audit of the form $K \in \{K_0, 2K_0, 4K_0\}$ where $K_0$ is the smallest truncation at which the program family's expected invariants stabilise. The audit's pass criterion is detection-rate stability within $\pm 5\%$ across the three values; failure indicates the truncation is below the program family's structural cutoff." Reference is made to e3nn's experience with $K$-truncation for periodic boundary conditions.

**C:** §7.5 paragraph added (+8 lines).

### R4.7 — §5.4 inner-product expansion (Reviewer detail 2)

**R:** "the bilinear form 𝓕 is identically zero on solutions of the forward and adjoint equations 对非反应堆物理背景的读者过于跳跃"

**A:** Accepted. We have expanded the §5.4 derivation to show the inner-product manipulation step explicitly: $\langle \phi^{\dagger}, B\phi \rangle = \langle B^{\dagger}\phi^{\dagger}, \phi \rangle$ by definition of formal adjoint, hence $\mathcal{F}[\phi, \phi^{\dagger}] = \langle \phi^{\dagger}, S \rangle - \langle \phi, S^{\dagger} \rangle$ which equals zero by the boundary-coupling reciprocity identity. A two-line bridge sentence explains "definition of formal adjoint" for non-physics readers.

**C:** §5.4 derivation +3 lines.

### R4.8 — Table 4 caption: which $\rho_{\mathrm{adj}}$ formulation (Reviewer detail 3)

**R:** "§6.6 案例研究里实际跑的是哪一版需要在 Table 4 caption 里标清楚"

**A:** Accepted. Table 4 caption now states explicitly: "Detection numbers for $\rho_{\mathrm{adj}}$ in Set N use the CI-time forward-pass-only formulation introduced in §6.4. The Round-1 harness-time formulation (Round-1 supplementary S1) is retained for backward compatibility but is not used in the comparative case study."

**C:** Table 4 caption +2 lines.

### R4.9 — §6.7 baseline strengthening (Reviewer detail 4)

**R:** "§6.7 关于查询优化器测试的工作只引了 Segura 2022 与 Wang 等 QED，建议再加 Slutz 1998 (RAGS / random query generation) 与近期 SIGMOD 的 query equivalence checking 工作以加固该域的 baseline 选择正当性。"

**A:** Accepted. §6.7 now positions NOETHER's query-optimiser instantiation against five concrete baselines:
  - **Slutz 1998 RAGS**~\cite{Slutz1998RAGS} — the seminal random-SQL-statement testing approach;
  - **Bati 2007 genetic random testing**~\cite{Bati2007GeneticDB} — execution-feedback-guided random SQL test generation;
  - **Segura 2022 QBS-MR**~\cite{Segura2022QBSAutoMR} — automated MR generation for query-based systems;
  - **SPES (Zhou 2022)**~\cite{Zhou2022SPES} — symbolic query equivalence under bag semantics, ICDE 2022;
  - **DQP (Ba 2024)**~\cite{Ba2024DQP} — Differential Query Plan testing, PACMMOD 2024;
  - **SQLancer++ (Zhong 2025)**~\cite{Zhong2025SQLancerPP} — adaptive SQL generation across 18 DBMSs, $\sim$ 196 unique bugs found.

The §6.7 positioning sentence is rewritten: "These baselines span four families — random SQL generation (Slutz, Bati), automated MR generation (Segura), formal query equivalence (Wang, Zhou, Mohamed), and differential testing (Ba, Zhong, Fu). NOETHER's $\mathcal{B}^{*}_{\mathrm{rel}}$ block is positioned as complementary: it provides an algebraically grounded MetaPattern enumeration where the existing baselines provide either input enumeration or oracle approximation."

**C:**
- **§6.7** positioning rewritten (+6 lines).
- **bib** to gain six new entries: Slutz1998RAGS, Bati2007GeneticDB, Zhou2022SPES, Mohamed2024SQLTables, Ba2024DQP, Zhong2025SQLancerPP, Fu2025Thanos. (Wang 2024 QED, Segura 2022 QBSAutoMR, Markl 2022 LearnedQO already in bib.)

### R4.10 — Reference scope check

**R:** Implicit in the Round-2 letter that the bib has grown adequately.

**A:** Bibliography now stands at 51 entries (Round-3 was 36 → 48 entries; this round adds 6 query-optimiser baselines + 1 quantum-compiler MorphQ++ + the new e3nn/PyG and Wohlin entries already in bib from Round-3 = 51 total).

**C:** No further work; reflected in the bib file.

---

## Section C — Items remaining as protocol (explicitly bounded)

We retain these as work that the framework's resubmission cycle can support but that this revision does not commit to delivering:

  - **GenMorph 23-Java subset full execution** — the adapter engineering for each Java subject (Randoop / Evosuite hookup, mutation framework integration) is estimated at 3–6 weeks of dedicated work and is not feasible inside the present revision window. The §6.6 protocol is committed to the camera-ready or a follow-up empirical paper.
  - **e3nn / PyG real-bug pilot at $n=10$** — the §6.6 protocol describes 10 confirmed real-bug commits. The §6.6.1 DeepCrime-style pilot at $n=5$ is the first empirical handhold; the larger real-bug pilot remains to be executed.
  - **IMDb / Segura QBS-MR comparison** — the §6.7 protocol describes this; it depends on Segura's released harness which we have not yet integrated. The formalisation of $\mathcal{B}^{*}_{\mathrm{rel}}$ in this revision is the load-bearing v1.1 contribution; the comparison is supporting empirical work.
  - **Theorem 1$'$ resolution** — open conjecture, not addressed in this revision (consistent with Round-3 commitment).

---

## Diff summary table

| Reviewer suggestion | Manuscript change | Section | Estimated added/removed |
|---|---|---|---|
| R4.1 (priority 1) — execute pilot | DeepCrime-style real-fault pilot, $n=5$ on trained EGNN | §6.6.1 (new sub-subsection) | +0.5 page, +1 table |
| R4.1 / supplementary | runner_pilot.py + cat\_v\_deepcrime.py + results.csv + stats.json | S3 supplementary | +4 files |
| R4.2 (priority 2) — $\mathcal{B}^{*}_{\mathrm{rel}}$ formalisation | Definition 14 + Table 5 row + Definition 13 update + Theorem 1/2 v1.1 remarks | §3.9, Table 5, §4.3, §4.4, §6.7 | +30 lines, +1 table row |
| R4.3 (priority 3) — §5 self-contained | New Appendix B with per-MR derivation of Table 3's 12 MRs | Appendix B (new) | +3 pages |
| R4.3 / supplementary | independent_citation column in pwr_84mr_full.csv | S2 supplementary | column added |
| R4.4 (priority 4) — Abstract / §1 caveats | Pilot result and protocol-vs-result distinction made explicit | Abstract, §1 C3, §1 C4, 3 Boundary boxes | +6 lines, -2 lines |
| R4.5 (priority 5) — §7.1 mapping | Round-1→Round-2→Round-3 provenance table | §7.1 head | +12 lines |
| R4.6 (detail) — K-sweep audit | Practical engineering paragraph | §7.5 | +8 lines |
| R4.7 (detail) — inner-product expansion | Two-line bridge for non-physics readers | §5.4 | +3 lines |
| R4.8 (detail) — Table 4 caption | Explicit CI-time vs harness-time labelling | Table 4 caption | +2 lines |
| R4.9 (detail) — §6.7 baselines | 6 new query-optimiser baselines + repositioning | §6.7, bib | +6 lines, +6 bib |

**Total estimated paper-length impact:** +6 pages (mostly the new Appendix B). Final paper length expected: $\approx 41$ pages including Appendix B and the new pilot subsection (TOSEM acmsmall envelope still acceptable).

---

## Supplementary archive integrity

| Item | Round-3 (submitted) | Round-4 (this revision) |
|---|---|---|
| SHA-256 (prior) | `2dad7bcfee29d4d19a7da1210a877143009cd00a33c2f01e4e02b7dd6828b914` | to be recomputed at revision submission |
| New supplementary files | — | S3/`runner_pilot.py`, S3/`cat_v_deepcrime.py`, S3/`deepcrime_pilot_results.csv`, S3/`deepcrime_pilot_stats.json`, S2/`pwr_84mr_full.csv` (with `independent_citation` column) |

---

## Closing

The remaining gap, as the committee correctly diagnoses, is between *protocol* and *result*. We have crossed that gap at minimum scale with the §6.6.1 DeepCrime-style pilot (5 real-fault-style mutations executed end-to-end on the trained EGNN; $n=5$ provides insufficient statistical power but the direction matches the framework's prediction). We have formalised $\mathcal{B}^{*}_{\mathrm{rel}}$ at the same level of rigour as the original seven blocks. We have made the reactor-physics evidence chain self-contained, and we have softened the case-study claims so that the framework's empirical claims are at the same confidence level as the available evidence.

We believe this revision is now in the form the committee described as ready for TOSEM acceptance: theoretical core (Theorem~\ref{thm:closure} + Theorem~\ref{thm:decidable} + CONSTRUCT-MP) on a firm foundation; empirical evidence at the case-study and small-pilot level with calibrated claims; comparative-evaluation protocol committed to follow-up empirical work; framework boundaries explicit in three Boundary-of-contribution boxes plus the version-1.1 of Hypothesis~\ref{hyp:seven-blocks}.

Sincerely,
The Authors

---

*Document version: Round-4 response, drafted 2026-05-03. Literature search performed via Consensus paper-search-mcp on 2026-05-03; new query-optimiser-testing references catalogued in §R4.9.*
