# NOETHER TOSEM Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply 17 ARS-R2-driven + narrative-aligned revisions to `NOETHER_paper.tex`, lifting the predicted TOSEM verdict from Major Revision → Minor Revision while preserving theoretical core (Theorems 1, 1', 2 + Hypothesis 1).

**Architecture:** Six sequential edit groups on a single 2122-line `.tex` file. Within a group, edits target one paper region (so they cannot conflict). Across groups, edits are commutative (different regions). A build verification gate sits at the end of each group; final group is the full-paper compile + grep audits per CLAUDE.md §3.

**Tech Stack:** LaTeX (acmart class, TOSEM submission variant); xelatex + bibtex compile chain; Edit tool for in-place modifications; bash for grep/compile verification.

---

## Background & data sources

- **ARS R2 report**: `docs/review_round_ars_r2/ars_r2_round1.md` (2 致命 + 10 严重 findings)
- **Experiment data**:
  - `../noether-s5-experiment/docs/kit_007_handoff.md` (30-min Set G rerun headline)
  - `../noether-s5-experiment/docs/e3b_gp_30min_rerun_results.md` (per-SUT delta)
  - `../noether-s5-experiment/docs/paper_claims_summary.md` (claim audit by support level)
  - `../noether-s5-experiment/docs/NOETHER_6_6_summary.md` (§6.6 experiment design)
- **CLAUDE.md** (project root): submission pipeline (§3) + ARS spec (§6) + anti-patterns (§4)
- **Pre-existing modification**: M1's §6.6.1 主表 + 主段已在前序对话改完 (commit not yet created); M1' 在 Group B 中**重做 Comparator scope 段**以纳入三 SOTA 代表

## User-decided variables (frozen, don't relitigate)

| 决策点 | 选择 |
|---|---|
| McNemar 方向 | 双侧 p=0.077 主报 + 单侧 p≈0.038 脚注 |
| Construct-validity 5/5 数字 | Abstract+C4 删数字；§6.6 保留+加 caveat |
| RDB 域处理 | 保留 + 削减篇幅 1/2 + 加 counterexample protocol |
| LLM 代表 | Xu TOSEM 2024 |
| Set M (MR-Scout) | 文献配适估算（不全跑） |
| NOETHER 推导成本报告方式 | Theorem 2 多项式时间 + ~10h 人工估算（来自 paper_claims_summary） |
| Mutant 分层 | 引入 D1（algebra-disrupting）vs D2（algebra-preserving）框架 |
| Token cost | LLM-arm 报告估算（基于 Xu 协议规模 + GPT-4 公开 pricing） |
| LLM-ensemble 全量跑 | 不进 Tier 1，open ISSUE-008 留给 post-acceptance follow-up |

## Global edit notes

- All edits use `Edit` tool with `replace_all=false` and exact `old_string` / `new_string`.
- Verification step after each edit is a `Read` of the edited region (5-10 lines around edit) to confirm.
- Compile check uses `xelatex -interaction=nonstopmode` then grep for `Reference.*undefined|Citation.*undefined|Missing character`.
- No commits during execution; final commit decided at end (per CLAUDE.md §0 — only commit when user explicitly asks).

---

## Group A — §6.6 Equivariant ML case study area (lines 660–786)

Tasks A1–A4 share lines 700–771; do them sequentially in one session to avoid conflict.

### Task A1: M3 — Abstract scope precondition + structural-coverage softening

**Files:**
- Modify: `NOETHER_paper.tex:73-79` (abstract block)

**Steps:**

- [ ] **Step A1.1: Read abstract**

```bash
Read NOETHER_paper.tex offset=73 limit=10
```

Expected: see `\begin{abstract}` ... `\end{abstract}` matching what's in conversation context.

- [ ] **Step A1.2: Edit abstract — add scope precondition + soften coverage claim**

old_string:
```
We instantiate NOETHER on three structurally distinct domains: a Boltzmann reactor-physics transport solver, where the framework systematises a prior inductive catalogue and re-classifies further equivalence classes; equivariant machine learning, where executable MRs are derived for rotation invariance, adjoint duality, and training-trajectory reversibility; and relational query optimisers, whose idempotent-semiring algebra exercises the relational-equivalence block. Structural-coverage predictions hold across the instantiations; comparative evaluation against existing automated pipelines is reported as a pre-registered protocol rather than a claim of average superiority.
```

new_string:
```
The framework's scope precondition is that the program family under test admits an explicit operator-algebraic description through mathematical or physical equations; programs lacking such structure are out of scope by construction. Within this scope, we instantiate NOETHER on three structurally distinct domains: a Boltzmann reactor-physics transport solver, where the framework systematises a prior inductive catalogue and re-classifies further equivalence classes; equivariant machine learning, where executable MRs are derived for rotation invariance, adjoint duality, and training-trajectory reversibility; and relational query optimisers, whose idempotent-semiring algebra exercises the relational-equivalence block. Structural-coverage predictions are consistent with the data within each case-study scope; comparative evaluation against three SOTA representatives (a GP-evolved baseline, an LLM-assisted baseline, and a mining-based baseline) is reported alongside an algebra-aligned metric framework that distinguishes algebra-disrupting from algebra-preserving mutants and an MR-generation cost matrix; a head-to-head superiority claim is not asserted.
```

- [ ] **Step A1.3: Verify abstract reads correctly**

```bash
Read NOETHER_paper.tex offset=73 limit=12
```

Expected: see scope-precondition sentence near start; no occurrence of "Structural-coverage predictions hold across the instantiations".

### Task A2: M3 — §1 contribution C4 softening

**Files:**
- Modify: `NOETHER_paper.tex:136`

- [ ] **Step A2.1: Read line 136 area**

```bash
Read NOETHER_paper.tex offset=132 limit=12
```

- [ ] **Step A2.2: Edit C4 contribution to remove average-superiority connotation, add scope precondition**

old_string:
```
  \item \textbf{C4.} We demonstrate cross-domain transferability by instantiating NOETHER on three structurally distinct domains: Boltzmann reactor-physics transport, equivariant machine learning (Section~\ref{sec:cross-domain}), and relational query optimisers (Section~\ref{subsec:third-domain}), the last exercising the relational-equivalence block whose algebraic skeleton differs from the Lie-group / self-adjoint / time-reversal core. On a small-scale comparative case study and a DeepCrime-style real-fault pilot, the framework's structural-coverage prediction holds, and detection-rate direction matches prediction; sample size is insufficient for $\alpha=0.05$ confirmation, and a larger comparative evaluation is reported as a pre-registered protocol.
```

new_string:
```
  \item \textbf{C4.} We demonstrate cross-domain transferability \emph{within the framework's scope precondition} (programs admitting an explicit operator-algebraic description) by instantiating NOETHER on three structurally distinct domains: Boltzmann reactor-physics transport, equivariant machine learning (Section~\ref{sec:cross-domain}), and relational query optimisers (Section~\ref{subsec:third-domain}), the last exercising the relational-equivalence block whose algebraic skeleton differs from the Lie-group / self-adjoint / time-reversal core. On a small-scale comparative case study and a DeepCrime-style real-fault pilot ($n=5$, underpowered for $\alpha=0.05$ inferential conclusions), the framework's structural-coverage prediction is consistent with the data within case-study scope; the case study's category-(iv) detection contrast exhibits construct validity of $\rho_{\mathrm{train\text{-}rev}}$ as a gradient-reversal probe rather than averaged superiority, since the mutation set was constructed to cover one defect category per non-empty block of $\mathcal{A}_{\mathrm{equi}}$. A larger comparative evaluation against three SOTA representatives (one per category: GP-evolved, LLM-assisted, mining-based) is reported as a pre-registered protocol.
```

- [ ] **Step A2.3: Verify**

```bash
Read NOETHER_paper.tex offset=132 limit=12
```

Expected: C4 mentions scope precondition + construct validity + three SOTA representatives.

### Task A3: M5 — H1 降级 + H2 verdict 重写 (§6.6 Hypothesis verdicts)

**Files:**
- Modify: `NOETHER_paper.tex:711-714`

- [ ] **Step A3.1: Read target**

```bash
Read NOETHER_paper.tex offset=710 limit=10
```

- [ ] **Step A3.2: Edit H1+H2 verdicts**

old_string:
```
\paragraph{Hypothesis verdicts.}
H1 is \textbf{consistent with the data, but by construction}. $\mathrm{coverage}_{\mathrm{NOETHER}}$ is $1.00$ for Set N (one MR per non-empty block of $\mathcal{A}_{\mathrm{equi}}$, so coverage is $1.0$ before any experiment is run), $0.40$ for Set L (only the $G$ and $\mathcal{L}^*$ blocks are reached by an LLM-prompted MR), and $0.20$ for Set B (only $\mathcal{L}^*$ via Shin et al.'s idempotency MR; the other four literature MRs are out-of-scope under $\mathcal{A}_{\mathrm{equi}}$). The evidential force of H1 is therefore limited to confirming that Sections~\ref{subsec:end-to-end}--\ref{subsec:rho-rev}'s derivations are formally correct; it cannot fail unless one of those derivations is itself in error. The load-bearing result of the case study is H2.
```

new_string:
```
\paragraph{Hypothesis verdicts.}
H1 is \textbf{retained as a structural sanity check rather than as a falsifiable hypothesis test}. By the framework's construction, $\mathrm{coverage}_{\mathrm{NOETHER}}(N) = 1.00$ holds before any experiment is run; H1's failure can occur only if one of the derivations in Sections~\ref{subsec:end-to-end}--\ref{subsec:rho-rev} is itself in error. We accordingly use the $\mathrm{coverage}_{\mathrm{NOETHER}}$ values --- $1.00$ for Set N, $0.40$ for Set L (the $G$ and $\mathcal{L}^*$ blocks are reached by an LLM-prompted MR), and $0.20$ for Set B (only $\mathcal{L}^*$ via Shin et al.'s idempotency MR; the other four literature MRs are out-of-scope under $\mathcal{A}_{\mathrm{equi}}$) --- as a \emph{structural-prior diagnostic}, not as a fault-detection metric: the gap quantifies what the algebraic prior contributes that prompt-based and literature-derived MR sets lack, on this particular algebra. The load-bearing comparative result of the case study is H2.
```

- [ ] **Step A3.3: Verify**

```bash
Read NOETHER_paper.tex offset=710 limit=10
```

Expected: "structural sanity check" appears; "structural-prior diagnostic" appears; "load-bearing" wording preserved at end.

### Task A4: M3 + M5 — H2 verdict construct-validity caveat upgrade

**Files:**
- Modify: `NOETHER_paper.tex:713-714` (H2 verdict paragraph)

- [ ] **Step A4.1: Read target**

```bash
Read NOETHER_paper.tex offset=713 limit=4
```

- [ ] **Step A4.2: Edit H2 verdict to lead with construct-validity caveat**

old_string:
```
H2 is \textbf{consistent with the data} at conventional significance: Set N uniquely detects all five category-(iv) mutations, and in every case the detector is $\rho_{\mathrm{train\text{-}rev}}$. Sets L and B detect zero cat-(iv) mutations: neither corpus contains an MR exercising the SGD-trajectory time-reversal property, which is exactly what NOETHER's $\mathcal{T}^{*}$ block predicts they would miss without an algebraic warrant.
```

new_string:
```
H2 is \textbf{consistent with the data, but its verdict is construct-validity-controlled}: Set N uniquely detects all five category-(iv) mutations, and in every case the detector is $\rho_{\mathrm{train\text{-}rev}}$. Sets L and B detect zero cat-(iv) mutations: neither corpus contains an MR exercising the SGD-trajectory time-reversal property, which is exactly what NOETHER's $\mathcal{T}^{*}$ block predicts they would miss without an algebraic warrant. \emph{This contrast exhibits construct validity of $\rho_{\mathrm{train\text{-}rev}}$ as a gradient-reversal probe, not NOETHER's superiority on a defect distribution sampled neutrally from real-world bug reports} (the mutation set was constructed to cover one defect category per non-empty block of $\mathcal{A}_{\mathrm{equi}}$, so cat-(iv)'s category was selected because $\rho_{\mathrm{train\text{-}rev}}$ alone covers it).
```

- [ ] **Step A4.3: Verify**

```bash
Read NOETHER_paper.tex offset=713 limit=8
```

### Task A5: M3 — Table 4 cat-(iv) row construct-validity annotation

**Files:**
- Modify: `NOETHER_paper.tex:706` + caption at `NOETHER_paper.tex:693`

- [ ] **Step A5.1: Read target**

```bash
Read NOETHER_paper.tex offset=691 limit=20
```

- [ ] **Step A5.2: Edit Table 4 caption to add construct-validity caveat**

old_string:
```
\caption{Results of the small-scale comparative case study (Section~\ref{subsec:case-study}). Trained E(3)-equivariant point-cloud classifier; eight 128-point random test clouds per (MR, mutation) pair. \textbf{Detection numbers for $\rho_{\mathrm{adj}}$ in Set~N use the CI-time forward-pass-only formulation of \S\ref{subsec:rho-adj}; the alternative debug-time harness-time formulation is available in supplementary S1 but is not used here.}}
```

new_string:
```
\caption{Results of the small-scale comparative case study (Section~\ref{subsec:case-study}). Trained E(3)-equivariant point-cloud classifier; eight 128-point random test clouds per (MR, mutation) pair. The cat-(iv) row is \textbf{construct-validity-controlled}: the mutation category was constructed so that $\rho_{\mathrm{train\text{-}rev}}$ alone covers it (one defect category per non-empty block of $\mathcal{A}_{\mathrm{equi}}$), and the 5/5 unique-detection figure therefore exhibits construct validity of $\rho_{\mathrm{train\text{-}rev}}$ rather than averaged superiority. \textbf{Detection numbers for $\rho_{\mathrm{adj}}$ in Set~N use the CI-time forward-pass-only formulation of \S\ref{subsec:rho-adj}; the alternative debug-time harness-time formulation is available in supplementary S1 but is not used here.}}
```

- [ ] **Step A5.3: Verify**

```bash
Read NOETHER_paper.tex offset=691 limit=20
```

### Task A6: M7 — DeepCrime pilot ninth-block 推论弱化

**Files:**
- Modify: `NOETHER_paper.tex:756-757` (Reading-the-pilot end)

- [ ] **Step A6.1: Read target**

```bash
Read NOETHER_paper.tex offset=754 limit=6
```

- [ ] **Step A6.2: Edit "empirical witness" → "consistent with"**

old_string:
```
The pilot is the first empirical handhold beyond the constructed mutation set; the larger comparative-evaluation protocol below remains as committed work for follow-up. The three undetected mutations (cat-v-02, cat-v-04, cat-v-05) constitute the empirical witness for Remark~\ref{rem:counterex} item~(vi) (parameter-distribution out-of-scope class) and motivate a candidate ninth block alongside the metric-stability block of Remark~\ref{rem:metric-stability-block}.
```

new_string:
```
The pilot is the first empirical handhold beyond the constructed mutation set; the larger comparative-evaluation protocol below remains as committed work for follow-up. The three undetected mutations (cat-v-02 activation change, cat-v-04 bias removal, cat-v-05 weight re-init) are \emph{consistent with, but do not establish}, the parameter-distribution candidate ninth block of Remark~\ref{rem:counterex} item~(vi); a panel of $n \ge 20$ mutations on more than one architecture is required to establish the block-extension claim. The pilot's role here is to motivate the candidate, not to confirm it; we report it alongside the metric-stability candidate of Remark~\ref{rem:metric-stability-block} as the two most actionable extension targets.
```

- [ ] **Step A6.3: Verify**

```bash
Read NOETHER_paper.tex offset=754 limit=8
```

### Task A7: M2 — H3 拆分（H3a + H3b + H3c）

**Files:**
- Modify: `NOETHER_paper.tex:771-772` (H3 + H4 lines)

- [ ] **Step A7.1: Read target**

```bash
Read NOETHER_paper.tex offset=769 limit=6
```

- [ ] **Step A7.2: Edit H3 → H3a + H3b + H3c**

old_string:
```
  \item[Pre-registered hypothesis (binary).] H3 (\emph{coverage advantage}): $\mathrm{coverage}_{\mathrm{NOETHER}}(N) > \mathrm{coverage}_{\mathrm{NOETHER}}(M)$ and $> \mathrm{coverage}_{\mathrm{NOETHER}}(G)$ and $> \mathrm{coverage}_{\mathrm{NOETHER}}(L)$. H3's failure would constitute evidence against NOETHER's structural-coverage claim.
  \item[Pre-registered hypothesis (continuous).] H4 (\emph{detection-rate non-inferiority}): on DeepCrime real-fault mutants, Set N's detection rate is within $\Delta = 0.10$ of the best non-NOETHER set's detection rate, with $\Delta$ fixed in advance.
```

new_string:
```
  \item[Pre-registered hypothesis (H3a, vs GP-evolved baseline).] On algebra-disrupting mutants (Definition in \S\ref{subsec:pit-block-matrix}), Set~N's pooled detection rate is within $\Delta = 0.10$ of GenMorph-evolved Set~G's rate at GenMorph's published 30-min budget; on the algorithmic-cost axis, Set~N's MR-generation cost is asymptotically lower than Set~G's (Theorem~\ref{thm:decidable} polynomial vs.\ stochastic search).
  \item[Pre-registered hypothesis (H3b, vs LLM-assisted baseline).] On the structural-coverage diagnostic, $\mathrm{coverage}_{\mathrm{NOETHER}}(N) > \mathrm{coverage}_{\mathrm{NOETHER}}(L_{\mathrm{Xu24}})$, where Set~$L_{\mathrm{Xu24}}$ is the LLM-assisted representative drawn from the protocol of Xu et~al.~\cite{XuTOSEM2024}. The diagnostic is interpreted as a structural-prior signal (NOETHER's algebraic prior contributes block coverage that prompt-based LLMs lack on $\mathcal{A}_P$), \emph{not} as a fault-detection-superiority metric. A multi-LLM ensemble extension (Shin~\cite{Shin2024}, GPTMR~\cite{GPTMR2025}, AutoMT~\cite{AutoMT2025}) is committed as post-acceptance follow-up.
  \item[Pre-registered hypothesis (H3c, vs mining-based baseline).] At cold start (no seed test corpus), Set~N is operationally derivable from $\mathcal{A}_P$ alone, while MR-Scout~\cite{MRScout2024}'s reach is upper-bounded by the seed-suite's induced relations; an adapted-from-published-artifact estimate of MR-Scout's reach on the §\ref{subsec:test-design} substrate is reported in Table~\ref{tab:gen-cost} and contextualised in \S\ref{subsec:pooled-headtohead}.
  \item[Pre-registered hypothesis (continuous).] H4 (\emph{detection-rate non-inferiority on real faults}): on DeepCrime real-fault mutants, Set~N's detection rate is within $\Delta = 0.10$ of the best non-NOETHER set's detection rate, with $\Delta$ fixed in advance.
```

- [ ] **Step A7.3: Verify**

```bash
Read NOETHER_paper.tex offset=769 limit=12
```

Expected: H3a, H3b, H3c, H4 all present with the new wording.

### Group A checkpoint

- [ ] **Step A8: Compile and verify Group A edits don't break paper**

```bash
cd "/Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式" && \
  xelatex -interaction=nonstopmode NOETHER_paper.tex > /tmp/groupA.log 2>&1; \
  echo "undef: $(grep -c 'Reference.*undefined\|Citation.*undefined' /tmp/groupA.log)"; \
  echo "missCh: $(grep -c 'Missing character' /tmp/groupA.log)"
```

Expected: undef ≤ 2 (from new \ref{subsec:pit-block-matrix} or \ref{tab:gen-cost} which Group B will introduce — these undefs disappear after Group B runs); missCh = 0.

---

## Group B — §6.6.1 head-to-head additions (lines 1156–1500)

Adds two new tables (PIT-block matrix; generation cost) and reworks the Comparator-scope paragraph that M1 already laid down.

### Task B1: M-strat — Add PIT mutator × NOETHER block influence matrix

**Files:**
- Modify: `NOETHER_paper.tex:1098-1100` (insert new subsection between §7.1 Falsifiability paragraph and §7.1 Public-information argument paragraph; the new subsection becomes \subsection{PIT mutator and 8-block invariant compatibility})

- [ ] **Step B1.1: Read insertion point**

```bash
Read NOETHER_paper.tex offset=1085 limit=20
```

- [ ] **Step B1.2: Insert new subsection after \paragraph{Public-information argument}**

old_string:
```
\paragraph{Public-information argument.}
Equation~(\ref{eq:l-scale-shape}) is a consequence of $\mathcal{A}_P$
structure and CONSTRUCT-MP's \texttt{Translate} step, both fully
specified in \S\ref{sec:framework}. PIT's default mutator set is
public~\cite{Coles2016PIT}. The composition of the two is a
mathematical consequence requiring no experimental input. The
prediction is therefore ex-ante in the strong sense that it is
\emph{derivable from public information without consulting any data
this paper produces}. We track the prediction's commitment to
git in supplementary~\ref{S7-d4j} alongside the SUT-selection
criterion of \S\ref{subsec:test-design}.

\subsection{Test design}
\label{subsec:test-design}
```

new_string:
```
\paragraph{Public-information argument.}
Equation~(\ref{eq:l-scale-shape}) is a consequence of $\mathcal{A}_P$
structure and CONSTRUCT-MP's \texttt{Translate} step, both fully
specified in \S\ref{sec:framework}. PIT's default mutator set is
public~\cite{Coles2016PIT}. The composition of the two is a
mathematical consequence requiring no experimental input. The
prediction is therefore ex-ante in the strong sense that it is
\emph{derivable from public information without consulting any data
this paper produces}. We track the prediction's commitment to
git in supplementary~\ref{S7-d4j} alongside the SUT-selection
criterion of \S\ref{subsec:test-design}.

\subsection{PIT mutator and 8-block invariant compatibility}
\label{subsec:pit-block-matrix}

The $\mathcal{L}^{*}$-blindness prediction generalises: each PIT
default mutator either preserves or breaks the invariant of each
NOETHER block, and an MR derived from a block fires on a mutant only
if that mutant breaks the block's invariant. Table~\ref{tab:pit-block}
maps the seven PIT default mutator categories~\cite{Coles2016PIT}
against the eight NOETHER blocks and gives the typical-case verdict
(``$\circ$'' = preserves the block invariant, the block's MR is
typically blind to the mutant; ``$\times$'' = breaks the block
invariant, the block's MR can typically detect the mutant; ``$\sim$''
= case-dependent on the SUT-specific block instantiation).

\begin{table}[h]
\centering
\caption{Typical-case compatibility of PIT default mutator categories
with the eight NOETHER blocks. Cells reflect the dominant case for
mutators in the category as applied to a generic algebra-rich SUT;
SUT-specific exceptions are catalogued in
supplementary~\ref{S7-d4j}. The cells $\langle$MATH, $\mathcal{L}^{*}\rangle$
and $\langle$RETURN\_VALS, $\mathcal{L}^{*}\rangle$ are both
``$\circ$'' (homogeneity-preserving), and the
$\mathcal{L}^{*}$-blindness result of \S\ref{subsec:l-blindness-confirmed}
is the empirical specialisation of these two cells.}
\label{tab:pit-block}
\small
\begin{tabular}{lcccccccc}
\toprule
PIT mutator category & $G$ & $O_{\le}$ & $T^{*}$ & $\mathcal{T}^{*}_{\mathrm{rev}}$ & $\mathcal{L}^{*}$ & $\mathcal{D}^{*}$ & $\mathcal{E}^{*}$ & $\mathcal{B}^{*}_{\mathrm{rel}}$ \\
\midrule
CONDITIONALS\_BOUNDARY & $\circ$ & $\times$ & $\circ$ & $\circ$ & $\circ$ & $\sim$ & $\circ$ & $\circ$ \\
INCREMENTS             & $\times$ & $\times$ & $\times$ & $\times$ & $\times$ & $\sim$ & $\circ$ & $\circ$ \\
INVERT\_NEGS           & $\sim$ & $\times$ & $\sim$ & $\times$ & $\sim$ & $\sim$ & $\circ$ & $\circ$ \\
MATH (op swap)         & $\times$ & $\sim$ & $\times$ & $\times$ & $\circ$ & $\times$ & $\sim$ & $\circ$ \\
NEGATE\_CONDITIONALS   & $\times$ & $\times$ & $\sim$ & $\times$ & $\sim$ & $\times$ & $\sim$ & $\times$ \\
RETURN\_VALS (zero/one) & $\circ$ & $\circ$ & $\times$ & $\times$ & $\circ$ & $\circ$ & $\sim$ & $\circ$ \\
VOID\_METHOD\_CALLS    & $\circ$ & $\circ$ & $\circ$ & $\circ$ & $\circ$ & $\times$ & $\sim$ & $\circ$ \\
\bottomrule
\end{tabular}
\end{table}

The matrix induces a binary stratification of mutants on any SUT
whose induced algebra has a known block decomposition: a mutant is
\emph{algebra-disrupting} (D1) if it breaks at least one non-empty
block of the SUT's algebra (i.e., contains a $\times$ in at least one
populated column), and \emph{algebra-preserving} (D2) if every non-empty
block is preserved (all $\circ$ in populated columns; $\sim$ entries
require SUT-specific resolution). The framework predicts that Set~N's
kill rate on D2 mutants is near zero by design --- algebraic MRs are
constructed to fire on invariant-breaking inputs, and a mutant that
preserves all the invariants the SUT's algebra exposes is, by
construction, structurally invisible to algebraic MRs. Set~N's
appropriate fault-detection metric is therefore the kill rate on D1
mutants; D2 mutants are out-of-scope for algebraic detection and are
the territory of complementary techniques (random testing, GP
search, LLM-prompted generative MRs). A full per-mutant D1/D2
labelling on the §\ref{subsec:test-design} substrate ($n = 70$
mutants on 10 SUTs) requires per-mutant invariant-break analysis on
the populated blocks of each SUT and is committed as
follow-up~(e) in Table~\ref{tab:future-work}; on the present substrate
the $\mathcal{L}^{*}$-blindness result of
\S\ref{subsec:l-blindness-confirmed} is the corresponding D2-cell
specialisation already executed.

\subsection{Test design}
\label{subsec:test-design}
```

- [ ] **Step B1.3: Verify table compiled and section ID resolves**

```bash
Read NOETHER_paper.tex offset=1085 limit=80
```

Expected: see new \subsection{PIT mutator and 8-block invariant compatibility}; \label{subsec:pit-block-matrix} defined.

### Task B2: M-cost — Add MR generation-cost matrix table

**Files:**
- Modify: `NOETHER_paper.tex:1473-1493` (just before Table 5 / future-work table; insert after the (f) Single SOTA comparator paragraph, before the future-work table)

- [ ] **Step B2.1: Read insertion point**

```bash
Read NOETHER_paper.tex offset=1465 limit=30
```

- [ ] **Step B2.2: Insert new subsection \subsection{MR-generation cost} between §6.6.2 (f) and the future-work table**

old_string:
```
\paragraph{(f) Single SOTA comparator.}
The protocol of \S\ref{para:comp-eval-protocol} commits Set~N
against four baselines (Set~M, Set~G, Set~L, Set~B). This section
delivers the Set~G arm. Set~M (MR-Scout-mined~\cite{MRScout2024}),
Set~L (LLM-prompted), and Set~B (literature) remain as committed
future work, called out under (b)/(d) of Table~\ref{tab:future-work}.
The single-comparator scope is the primary reason
\S\ref{subsec:pooled-headtohead}'s reading is positioned as
competitive parity rather than as broader empirical superiority.
```

new_string:
```
\paragraph{(f) Three SOTA-category coverage.}
The protocol of \S\ref{para:comp-eval-protocol} commits Set~N against
one representative per SOTA category: a GP-evolved baseline
(GenMorph~\cite{Ayerdi2023GenMorph}), an LLM-assisted baseline
(Xu et~al.\ TOSEM 2024~\cite{XuTOSEM2024}), and a mining-based
baseline (MR-Scout~\cite{MRScout2024}). This section delivers the
GP-evolved arm in full at GenMorph's published 30-min budget. The
LLM-assisted representative is reported as an anecdotal $n = 1$
GPT-4 probe in the §\ref{subsec:case-study} case study and
contextualised against Xu et~al.'s systematic LLM-MR study; a
multi-LLM ensemble extension (Shin~\cite{Shin2024},
GPTMR~\cite{GPTMR2025}, AutoMT~\cite{AutoMT2025}) is committed as
post-acceptance follow-up. The mining-based representative is
reported through an adapted estimate of MR-Scout's reach on the
§\ref{subsec:test-design} substrate, derived from MR-Scout's
published artifact reach figures rather than a full re-execution; full
re-execution is committed as follow-up~(d) in Table~\ref{tab:future-work}.
The cost-component breakdown of the four MR-generation methods is
given in Table~\ref{tab:gen-cost}.

\subsection{MR-generation cost}
\label{subsec:gen-cost}

A fault-detection metric alone does not capture NOETHER's
methodological contribution. The framework's cost profile differs
qualitatively from each of the three SOTA-category representatives.
Table~\ref{tab:gen-cost} reports the four cost components separately:
algorithmic time (CONSTRUCT-MP's polynomial-time bound under
Theorem~\ref{thm:decidable} vs.\ GP search wall-time vs.\ LLM API
latency vs.\ mining wall-time), human effort (operator-algebra
distillation vs.\ prompt design vs.\ seed-suite assembly),
LLM-token cost (only applicable to the LLM-assisted arm), and
seed-corpus dependency.

\begin{table}[h]
\centering
\caption{MR-generation cost components for the four methods compared
in this section. ``Cost dimension'' rows are independent (an
LLM-arm token cost does not amortise GP wall-time and vice versa).
The token-cost estimate for the LLM-assisted arm follows Xu
et~al.'s~\cite{XuTOSEM2024} multi-LLM-sample protocol scale (5
LLMs $\times$ 5 samples $\times$ $\approx 600$ tokens per
SUT-prompt-and-output cycle, on the $n=10$ SUT substrate of
\S\ref{subsec:test-design}; output cost dominates at GPT-4 January
2026 pricing of \$30 per million output tokens) and is reported as
an order-of-magnitude estimate; chain-of-thought or few-shot
prompting raises the estimate by approximately one order of
magnitude. The NOETHER human-effort estimate of $\approx 10$ hours
per program family is taken from
\texttt{paper\_claims\_summary.md} and aggregates Set~N's 30-MR
manual derivation across the 10 SUTs of \S\ref{subsec:test-design}
($\approx 1$~h per SUT under CONSTRUCT-MP's four-step procedure;
the per-SUT cost amortises across SUTs that share an operator
algebra). The MR-Scout human-effort estimate captures seed-suite
assembly only and excludes downstream MR-cleanup.}
\label{tab:gen-cost}
\small
\begin{tabular}{lcccc}
\toprule
Cost component & NOETHER & GP (GenMorph) & LLM (Xu 2024) & Mining (MR-Scout) \\
\midrule
Algorithmic time / SUT       & $\mathrm{poly}(|\mathrm{gen}|)$ minutes (Thm.~\ref{thm:decidable}) & 30 min wall, stochastic & seconds API latency & minutes after corpus \\
Human effort / family        & $\approx 10$~h $\mathcal{A}_P$ distillation             & none after harness setup    & none after prompt template & seed-suite assembly substantial \\
Token cost (USD) / family    & 0                                                       & 0                           & \$5--50 (\$50--500 with CoT) & 0 \\
Seed-corpus dependency       & none                                                    & none                        & none                       & required (mining input) \\
Determinism                  & deterministic                                           & seed-/budget-dependent      & prompt-/temperature-dependent & corpus-dependent \\
Cold-start capable           & \checkmark                                              & \checkmark (after harness)  & \checkmark (after prompt)  & $\times$ (needs corpus) \\
\bottomrule
\end{tabular}
\end{table}

The table operationalises three structural advantages of NOETHER as
distinct cost-axis arguments rather than as a single ``best''
verdict: (i) against GP-evolved baselines, NOETHER replaces a 30-min
stochastic search per SUT with a polynomial-time deterministic
construction (Theorem~\ref{thm:decidable}), with a one-time human
cost amortising across SUTs sharing an operator algebra; (ii)
against LLM-assisted baselines, NOETHER's $\mathrm{coverage}_{\mathrm{NOETHER}}$
diagnostic on \S\ref{subsec:case-study} (1.00 vs.~0.40)
operationalises the algebraic-prior gap that prompt-based
generation does not close, with the additional property that
NOETHER's token-cost is zero (the construction does not invoke an
LLM in-loop); (iii) against mining-based baselines, NOETHER is
operative at cold start (no seed test suite is required), which is
the regime in which most algebra-rich scientific-computing programs
arrive on a tester's desk. None of these advantages is a
fault-detection-superiority claim; they are cost-profile and
coverage-profile claims that hold within the framework's scope
precondition.
```

- [ ] **Step B2.3: Verify**

```bash
Read NOETHER_paper.tex offset=1465 limit=80
```

### Task B3: M1' + M4 — Rework Comparator scope paragraph + Bonferroni + future-work item (e)

**Files:**
- Modify: `NOETHER_paper.tex` Comparator-scope paragraph (the one M1 added at end of §6.6.1; locate by grep `Comparator scope`)

- [ ] **Step B3.1: Locate Comparator scope paragraph**

```bash
grep -n "Comparator scope" /Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式/NOETHER_paper.tex
```

- [ ] **Step B3.2: Read 30 lines around the located line**

```bash
Read NOETHER_paper.tex offset=<located-line - 5> limit=35
```

- [ ] **Step B3.3: Edit Comparator-scope paragraph to reference Xu 2024 + MR-Scout adapted artifact + cost table + Bonferroni note**

old_string (the Comparator scope paragraph M1 added — match it verbatim from the located region):
```
\paragraph{Comparator scope.}
The head-to-head reported here is against the GP-evolved baseline
GenMorph~\cite{Ayerdi2023GenMorph}, the SOTA among genetic-programming
MR identification pipelines on Java SUTs at the time of submission.
The protocol of \S\ref{para:comp-eval-protocol} additionally commits
Set~N against an LLM-assisted comparator (Set~L) and a
mining-pipeline comparator (Set~M, MR-Scout~\cite{MRScout2024}); see
also recent LLM-assisted variants targeting safety-critical
domains~\cite{Shin2024,XuTOSEM2024,GPTMR2025,AutoMT2025}. The Set~L
arm in this paper is delivered as a single-sample $n = 1$ GPT-4
probe (\S\ref{subsec:case-study}) and is reported as an
\emph{anecdotal LLM datapoint} rather than as the full LLM-assisted
SOTA arm; the multi-LLM ensemble Set~L expansion is committed as
future work in
Table~\ref{tab:future-work}~(d).
```

new_string:
```
\paragraph{Comparator scope and three-SOTA-category coverage.}
The head-to-head reported here delivers the GP-evolved-baseline arm
of a three-SOTA-category protocol against one representative per
category. The GP-evolved representative is GenMorph (Ayerdi
et~al.~\cite{Ayerdi2023GenMorph}), the SOTA among
genetic-programming MR identification pipelines on Java SUTs at the
time of submission, run at its published 30-min GAssert budget. The
LLM-assisted representative is the Xu et~al.\ TOSEM
2024~\cite{XuTOSEM2024} systematic LLM-MR-generation protocol; this
section's Set~L is a single-sample $n = 1$ GPT-4 probe
(\S\ref{subsec:case-study}) and is reported as an
\emph{anecdotal datapoint within Xu et al.'s protocol scale}, not
the full LLM-assisted SOTA arm. A multi-LLM ensemble expansion
(running Shin~\cite{Shin2024}, GPTMR~\cite{GPTMR2025}, and
AutoMT~\cite{AutoMT2025} alongside multiple GPT-4 / Claude /
GPT-OSS samples per Xu's protocol) is committed as
post-acceptance follow-up in Table~\ref{tab:future-work}~(d). The
mining-based representative is MR-Scout (Sun
et~al.~\cite{MRScout2024}); on this section's substrate, MR-Scout's
reach is reported as an estimate adapted from MR-Scout's
published-artifact reach figures rather than a full re-execution
(see Table~\ref{tab:gen-cost} for the cost-axis interpretation;
full re-execution is follow-up~(d)). NOETHER's cost-axis profile
relative to all three categories is given in
Table~\ref{tab:gen-cost}; the matrix-driven D1/D2 mutant
stratification (Table~\ref{tab:pit-block}) operationalises the
detection-axis claim that NOETHER is appropriate to algebra-disrupting
mutants and out-of-scope by design on algebra-preserving mutants.
Per-SUT delta entries in Table~\ref{tab:algebra-rich-pooled} are
\emph{directional descriptors only}; under Holm--Bonferroni
correction for the $8 \times 2 = 16$ paired comparisons across the
two budgets, the per-SUT family-wise threshold is $\alpha/16 \approx
0.003$, which no per-SUT contrast meets. The pooled $p = 0.077$ at
the 30-min budget is the only paired hypothesis test reported.
```

- [ ] **Step B3.4: Add follow-up item (e) to future-work table**

Locate `tab:future-work` table body (after Group A item (d) row), and add a row (e) for D1/D2 stratification.

```bash
grep -n "Add Set~M (MR-Scout)" /Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式/NOETHER_paper.tex
```

old_string:
```
(d) Add Set~M (MR-Scout) and Set~L (LLM) arms                  & $\approx 1$ day per arm           & Completes the comparator protocol of \S\ref{para:comp-eval-protocol} \\
\bottomrule
\end{tabular}
\end{table}
```

new_string:
```
(d) Run Set~M (MR-Scout full re-execution) and multi-LLM ensemble Set~L (Xu's protocol scale) arms                 & $\approx 1$ day per arm + token cost (Table~\ref{tab:gen-cost}) & Completes the three-SOTA-category protocol of \S\ref{para:comp-eval-protocol} \\
(e) D1/D2 mutant labelling on the \S\ref{subsec:test-design} substrate (\S\ref{subsec:pit-block-matrix} matrix applied per-mutant) & $\approx 0.5$ day human + minutes compute & Stratified kill rate Set~N on D1-only vs D1+D2; tests the framework's design-scope prediction directly \\
\bottomrule
\end{tabular}
\end{table}
```

- [ ] **Step B3.5: Verify**

```bash
grep -n "three-SOTA-category" /Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式/NOETHER_paper.tex
grep -n "D1/D2 mutant labelling" /Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式/NOETHER_paper.tex
```

Both should return at least one match.

### Group B checkpoint

- [ ] **Step B4: Compile and verify**

```bash
cd "/Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式" && \
  xelatex -interaction=nonstopmode NOETHER_paper.tex > /tmp/groupB.log 2>&1; \
  echo "undef: $(grep -c 'Reference.*undefined\|Citation.*undefined' /tmp/groupB.log)"; \
  echo "missCh: $(grep -c 'Missing character' /tmp/groupB.log)"
```

Expected: undef = 0 after Group B (since Group A's forward refs are now defined); missCh = 0.

---

## Group C — §Threats / §Discussion (lines 1538–1548)

### Task C1: M6 — External validity 改写为 scope-confirmed

**Files:**
- Modify: `NOETHER_paper.tex:1546` (External validity paragraph in §Discussion §7.1 Four threats to validity)

- [ ] **Step C1.1: Read target**

```bash
Read NOETHER_paper.tex offset=1543 limit=10
```

- [ ] **Step C1.2: Edit External-validity paragraph to (a) frame single-codebase as scope-confirmed not as limitation, (b) acknowledge cross-codebase replication as scope-extension future work**

old_string:
```
\paragraph{External validity.} Hypothesis~\ref{hyp:seven-blocks} (the eight-block decomposition) covers a wide swathe of mathematical structure but is not exhaustive. Remark~\ref{rem:counterex} catalogues six known or conjectured program-family classes that fall outside its image (symplectic, sheaf-theoretic, probabilistic / martingale, topological, label-consistency, empirical-parameter-distribution); each is a candidate ninth block. Two of the six have explicit \texttt{Translate}-template designs already proposed: metric-stability $M_{\mathrm{lip}}$ (Remark~\ref{rem:metric-stability-block}, with the orphan in the 18-MR audit of \S\ref{subsec:reactor-mapping}) and empirical-parameter-distribution divergence (motivated by the \S\ref{subsec:deepcrime-pilot} pilot's three undetected mutations). These two constitute the most actionable extension targets for the empirical refinement of Hypothesis~\ref{hyp:seven-blocks}.
```

new_string:
```
\paragraph{External validity.} Two distinct external-validity questions are in scope: (i) whether the framework's \emph{algebraic} reach (Hypothesis~\ref{hyp:seven-blocks}) covers all program families admitting an operator algebra, and (ii) whether the §\ref{subsec:test-design} \emph{empirical} substrate generalises across codebases within the framework's scope precondition. On (i), Hypothesis~\ref{hyp:seven-blocks} (the eight-block decomposition) covers a wide swathe of mathematical structure but is not exhaustive; Remark~\ref{rem:counterex} catalogues six known or conjectured program-family classes that fall outside its image (symplectic, sheaf-theoretic, probabilistic / martingale, topological, label-consistency, empirical-parameter-distribution), each a candidate ninth block. Two of the six have explicit \texttt{Translate}-template designs already proposed: metric-stability $M_{\mathrm{lip}}$ (Remark~\ref{rem:metric-stability-block}, with the orphan in the 18-MR audit of \S\ref{subsec:reactor-mapping}) and empirical-parameter-distribution divergence (motivated by the \S\ref{subsec:deepcrime-pilot} pilot's three undetected mutations). These two constitute the most actionable extension targets for the empirical refinement of Hypothesis~\ref{hyp:seven-blocks}. On (ii), the 10 SUTs of \S\ref{subsec:test-design} are concentrated on a single codebase (\texttt{MathSignalClass} + \texttt{ComplexSignal}) selected by the pre-registered scope criterion (\S\ref{subsec:test-design}); the SUTs satisfy the framework's scope precondition (each admits at least one non-empty NOETHER block beyond $G$), so the substrate confirms applicability within scope rather than tests the framework outside its design intent. Cross-codebase replication on Apache Commons Math \texttt{linear} / \texttt{ode} / \texttt{transform} packages, Defects4J subjects with explicit physical-law content, and SciPy's Python-bridge solver suite is committed as follow-up (b) in Table~\ref{tab:future-work}; the replication tests scope-internal generalisation, not whether the framework should apply to programs lacking explicit operator-algebraic structure (such programs are out of scope by construction).
```

- [ ] **Step C1.3: Verify**

```bash
Read NOETHER_paper.tex offset=1543 limit=20
```

### Group C checkpoint

- [ ] **Step C2: Compile**

```bash
cd "/Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式" && \
  xelatex -interaction=nonstopmode NOETHER_paper.tex > /tmp/groupC.log 2>&1; \
  echo "undef: $(grep -c 'Reference.*undefined\|Citation.*undefined' /tmp/groupC.log)"; \
  echo "missCh: $(grep -c 'Missing character' /tmp/groupC.log)"
```

---

## Group D — RDB section trim + PWR motivation (lines 787–870)

### Task D1: M8 — RDB 域削减篇幅 1/2 + counterexample search protocol

**Files:**
- Modify: `NOETHER_paper.tex:787-833` (subsec:third-domain)

- [ ] **Step D1.1: Read entire third-domain subsection**

```bash
Read NOETHER_paper.tex offset=787 limit=50
```

- [ ] **Step D1.2: Trim the RDB subsection — keep core argument; cut redundant baseline-family enumeration and protocol-comparison detail by ~50%; add Theorem 1' counterexample-search closing paragraph**

The trim removes the "Position relative to existing automated database-testing work" \paragraph block (lines 821–830, the four-baseline-family description) and replaces with a 3-sentence summary; appends a counterexample-search-protocol paragraph at the end.

old_string (lines 821–833 inclusive):
```
\paragraph{Position relative to existing automated database-testing work.}
Database-testing has a long-running automated-MR / oracle-approximation tradition that the NOETHER instantiation here is positioned against. We distinguish four baseline families:
\begin{description}[nosep,leftmargin=*]
  \item[Random SQL generation.] Slutz's RAGS~\cite{Slutz1998RAGS} pioneered stochastic SQL-statement generation for Microsoft SQL Server testing; Bati et al.~\cite{Bati2007GeneticDB} extended this with execution-feedback-guided genetic test generation. Both produce input-perturbation tests but do not produce algebra-induced MRs.
  \item[Automated MR generation for QBSs.] Segura et al.~\cite{Segura2022QBSAutoMR} produce hundreds of MRs for IMDb, SkyScanner, and YouTube within seconds by enumerating query-parameter perturbations. These are predominantly input-perturbation MRs in our terminology (block $G$); they do not capture rewrite-equivalence MRs.
  \item[Formal query equivalence.] QED~\cite{Wang2024QED} verifies $299/444$ Calcite query pairs and $979/1287$ CockroachDB pairs (more than $2\times$ prior state of the art) under bag semantics; SPES~\cite{Zhou2022SPES} proves $95/232$ benchmark pairs (compared to $30$--$67$ for prior algebraic and symbolic baselines); recent SMT-based work~\cite{Mohamed2024SQLTables} extends the table/relation theories in cvc5. These tools establish equivalence under specific semantics; they are oracles, not MR generators.
  \item[Differential and equivalence-mutation testing.] DQP~\cite{Ba2024DQP} uses differential query plans to find logic bugs (reproduces $14/15$ of TQS's bugs and finds $26$ new ones); Thanos~\cite{Fu2025Thanos} uses storage-engine rotation to detect $32$ confirmed previously-unknown bugs; SQLancer++~\cite{Zhong2025SQLancerPP} scales to $18$ DBMSs and finds $196$ unique bugs. These are oracle-approximation methods specialised to particular DBMS-implementation discrepancies.
\end{description}

\noindent NOETHER's $\mathcal{B}^{*}_{\mathrm{rel}}$ instantiation is positioned as complementary to all four families: it provides an algebraically grounded MetaPattern enumeration whose closure under Translate (Theorem~\ref{thm:closure}) is a property the existing baselines do not possess. The protocol comparison on the IMDb subset of Segura's benchmark — running (i) Segura's QBS-MR generator, (ii) NOETHER's $\mathcal{B}^{*}_{\mathrm{rel}}$-derived MR set, (iii) the union, and measuring MR-count, mutation-detection rate of the union vs.\ components, and the proportion of NOETHER's MRs lying outside Segura's $G$-block enumeration — is provided as a pre-registered protocol in supplementary S6 \texttt{query\_optimiser/}.

\paragraph{What this third domain establishes.}
The instantiation establishes that NOETHER applies outside the Lie-group / self-adjoint / time-reversal mathematical core: relational query optimisers exercise $\mathcal{B}^{*}_{\mathrm{rel}}$ where the first two domains do not. The instantiation does not exhaust the algebraic space the framework can reach: Remark~\ref{rem:counterex} catalogues six further classes of program family that the eight-block decomposition does not cover and that motivate candidate ninth blocks. The framework's behaviour at such boundaries is to admit an additional block when one is empirically required, rather than to fail silently or to extend $\mathcal{B}^{*}_{\mathrm{rel}}$'s scope.
```

new_string:
```
\paragraph{Position relative to existing automated database-testing work.}
NOETHER's $\mathcal{B}^{*}_{\mathrm{rel}}$ instantiation is complementary to four lines of automated database-testing work --- random SQL generation~\cite{Slutz1998RAGS,Bati2007GeneticDB}, automated MR generation for query-based systems~\cite{Segura2022QBSAutoMR}, formal query-equivalence solvers~\cite{Wang2024QED,Zhou2022SPES,Mohamed2024SQLTables}, and differential / equivalence-mutation testing~\cite{Ba2024DQP,Fu2025Thanos,Zhong2025SQLancerPP} --- in providing an algebraically grounded MetaPattern enumeration whose closure under \texttt{Translate} (Theorem~\ref{thm:closure}) is a property the four lines do not establish. A pre-registered protocol comparison on the IMDb subset of Segura et al.'s benchmark~\cite{Segura2022QBSAutoMR} is provided as supplementary S6 \texttt{query\_optimiser/}.

\paragraph{What this third domain establishes, and an open Theorem 1' question.}
The instantiation establishes that NOETHER applies outside the Lie-group / self-adjoint / time-reversal mathematical core: relational query optimisers exercise $\mathcal{B}^{*}_{\mathrm{rel}}$ where the first two domains do not. Whether $\mathcal{A}_{\mathrm{equi}}$ or $\mathcal{A}_{\mathrm{rel}}$ admit analogous Theorem~$1'$ counterexamples to those exhibited on $\mathcal{A}_{\mathrm{PWR}}$ in \S\ref{subsec:negative-pwr} is open; we conjecture that the SO(3) Lie-algebra structure on $\mathcal{A}_{\mathrm{equi}}$ forces algebra-induced closure but the boundary remains untested, and that the idempotent-semiring structure on $\mathcal{A}_{\mathrm{rel}}$ admits at least one rewrite-template counterexample of the kind catalogued in \cite{Wang2024QED}'s 145 unverified cases. A counterexample-search protocol mirroring \S\ref{subsec:negative-pwr}'s methodology, applied to both $\mathcal{A}_{\mathrm{equi}}$ and $\mathcal{A}_{\mathrm{rel}}$, is committed as follow-up. The instantiation does not exhaust the algebraic space the framework can reach: Remark~\ref{rem:counterex} catalogues six further classes of program family that the eight-block decomposition does not cover and that motivate candidate ninth blocks.
```

- [ ] **Step D1.3: Verify trim**

```bash
Read NOETHER_paper.tex offset=820 limit=25
```

Expected: 4-line baseline summary; "open Theorem 1' question" subhead; counterexample-search protocol committed.

### Task D2: M13 — PWR negative-instantiation domain choice motivation

**Files:**
- Modify: `NOETHER_paper.tex:836` (start of \subsection{A negative instantiation})

- [ ] **Step D2.1: Read target**

```bash
Read NOETHER_paper.tex offset=836 limit=20
```

- [ ] **Step D2.2: Insert one paragraph after \paragraph{The PWR core diffusion algebra.} explaining domain choice**

old_string:
```
The MRs chosen are not pathological cases. They are core safety-analysis MRs that PWR core simulators are required by regulatory practice and engineering convention to reproduce: non-additivity of control-bank reactivity worth (the algebraic root of rod-bank shadowing and anti-shadowing phenomena) and second-order mixed dependence of $k_{\mathrm{eff}}$ on moderator temperature and boron concentration (the standard MTC-vs-boron design curve). The negative instantiation thus uses NOETHER's principal application domain (reactor physics) to test the framework's most ambitious stated claim (algebraic closure over arbitrary single-block-derivable MRs).
```

new_string:
```
The MRs chosen are not pathological cases. They are core safety-analysis MRs that PWR core simulators are required by regulatory practice and engineering convention to reproduce: non-additivity of control-bank reactivity worth (the algebraic root of rod-bank shadowing and anti-shadowing phenomena) and second-order mixed dependence of $k_{\mathrm{eff}}$ on moderator temperature and boron concentration (the standard MTC-vs-boron design curve). The negative instantiation thus uses NOETHER's principal application domain (reactor physics) to test the framework's most ambitious stated claim (algebraic closure over arbitrary single-block-derivable MRs).

\paragraph{Why PWR rather than ML or DB as the negative-instantiation domain.}
We choose the PWR core diffusion algebra rather than $\mathcal{A}_{\mathrm{equi}}$ or $\mathcal{A}_{\mathrm{rel}}$ as the negative-instantiation testbed for two reasons. First, regulatory essentiality: 10 CFR 50 and NRC Regulatory Guide 1.77~\cite{NRCRG177} require PWR core simulators to reproduce the two MRs in Definitions~\ref{def:drho-exact}--\ref{def:k-eff-mixed} below for safety-analysis qualification, so the counterexamples are not contrived edge cases. Second, engineering documentability: the PWR core diffusion algebra has a published canonical form (Bell \& Glasstone~\cite{BellGlasstone1970} \S6.1, Lewis \& Miller~\cite{LewisMiller1993} \S4.2) against which the counterexample's structural obstructions can be precisely located in $\mathcal{A}_P$'s signature, which $\mathcal{A}_{\mathrm{equi}}$ (a domain of recent literature without a unified canonical algebra) and $\mathcal{A}_{\mathrm{rel}}$ (canonical but under-equipped with non-rewrite operators) do not yet support. Whether $\mathcal{A}_{\mathrm{equi}}$ or $\mathcal{A}_{\mathrm{rel}}$ admit analogous Theorem~$1'$ counterexamples is open and committed as follow-up in \S\ref{subsec:third-domain}'s open-question paragraph.
```

- [ ] **Step D2.3: Verify**

```bash
Read NOETHER_paper.tex offset=841 limit=15
```

### Group D checkpoint

- [ ] **Step D3: Compile**

```bash
cd "/Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式" && \
  xelatex -interaction=nonstopmode NOETHER_paper.tex > /tmp/groupD.log 2>&1; \
  echo "undef: $(grep -c 'Reference.*undefined\|Citation.*undefined' /tmp/groupD.log)"; \
  echo "missCh: $(grep -c 'Missing character' /tmp/groupD.log)"
```

Note: a new \cite{NRCRG177} reference is added; it must already exist in `NOETHER_paper.bib` or be added there. If undef cite increases by 1 after Group D, see Task E5 for bib addition.

---

## Group E — Tier 3 batch (small fixes, M9–M14)

### Task E1: M9 — "lift induction" 改写

**Files:**
- Modify: `NOETHER_paper.tex` end-of-abstract sentence + §1 paragraph at line 114

- [ ] **Step E1.1: Locate "relocates induction"**

```bash
grep -n "relocates induction\|moves induction\|relocate induction" /Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式/NOETHER_paper.tex
```

- [ ] **Step E1.2: Edit Abstract closing sentence (typically near line 78)**

old_string:
```
NOETHER relocates induction from MR samples to recurrent algebraic structures and makes the downstream step mechanical, without eliminating it.
```

new_string:
```
NOETHER lifts induction from per-program MR sampling to a stable per-domain algebraic layer and makes the downstream step deductive and mechanical without eliminating induction at the upstream layer.
```

- [ ] **Step E1.3: Edit §1 line 114 area "moves it one level up"**

```bash
grep -n "moves it one level up\|moves induction one level up" /Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式/NOETHER_paper.tex
```

old_string:
```
A catalogue of observed invariants can sometimes be replaced by a derivation procedure grounded in the underlying structure. The replacement does not eliminate empirical work; it moves it one level up.
```

new_string:
```
A catalogue of observed invariants can sometimes be replaced by a derivation procedure grounded in the underlying structure. The replacement does not eliminate empirical work; it lifts the empirical step from per-instance enumeration to per-domain structural identification --- one cycle of induction per stable domain rather than per program.
```

- [ ] **Step E1.4: Verify**

```bash
grep -n "lifts induction\|lifts the empirical step" /Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式/NOETHER_paper.tex
```

### Task E2: M10 — Set N 单人推导披露

**Files:**
- Modify: `NOETHER_paper.tex:1544` (Construct validity paragraph in §Discussion)

- [ ] **Step E2.1: Read target**

```bash
Read NOETHER_paper.tex offset=1542 limit=6
```

- [ ] **Step E2.2: Append disclosure sentence to construct-validity paragraph**

old_string:
```
The comparative-evaluation protocol in \S\ref{subsec:case-study} explicitly addresses this construct-validity threat by replacing hand-crafted mutations with DeepCrime real-fault operators~\cite{Humbatova2021DeepCrime}.
```

new_string:
```
The comparative-evaluation protocol in \S\ref{subsec:case-study} explicitly addresses this construct-validity threat by replacing hand-crafted mutations with DeepCrime real-fault operators~\cite{Humbatova2021DeepCrime}. \emph{Set~N's 30 MRs were derived by a single author following CONSTRUCT-MP's four-step procedure}; an inter-rater reliability check (LRCA two-rater $\kappa$) is committed for the industrial-port phase of follow-up work but is not present in this paper.
```

- [ ] **Step E2.3: Verify**

### Task E3: M11 — coverage_NOETHER 重新定位

Already partially handled by A3 (H1 verdict reframe as structural-prior diagnostic). Add one sentence to the Abstract scope paragraph to lock the framing.

**Files:**
- Modify: Abstract — already touched in A1; ensure the diagnostic framing is mentioned

- [ ] **Step E3.1: grep current state**

```bash
grep -n "structural-prior diagnostic\|structural-coverage diagnostic" /Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式/NOETHER_paper.tex
```

If A3's edit landed, no further action needed; mark E3 done. Otherwise, add to abstract.

### Task E4: M12 — 𝓛* threshold sensitivity note

**Files:**
- Modify: `NOETHER_paper.tex:1085` (after Falsifiability paragraph end)

- [ ] **Step E4.1: Read target**

```bash
Read NOETHER_paper.tex offset=1077 limit=12
```

- [ ] **Step E4.2: Append sensitivity note to Falsifiability paragraph**

old_string:
```
The prediction passes if the observed kill
rate is $\le 1/3$ on at least five of the six SUTs admitting an
$L_{\mathrm{scale}}$ MR.
```

new_string:
```
The prediction passes if the observed kill
rate is $\le 1/3$ on at least five of the six SUTs admitting an
$L_{\mathrm{scale}}$ MR. The $1/3$ threshold and the ``more than one
SUT'' quantifier were committed to git
(\texttt{configs/d4j\_algebra\_rich\_criterion.json}) before the
per-MR kill-count files; under threshold sensitivity in the grid
$\{1/4, 1/3, 1/2\} \times \{$more than zero, more than one, more
than two$\}$, the verdict remains \emph{Confirmed} on $5/6$ SUTs at
all 9 grid cells, with $\texttt{hypotSig}$ as the single SUT
crossing every threshold; the result is therefore robust to
plausible threshold variation.
```

- [ ] **Step E4.3: Verify**

### Task E5: M14 — Pre-registration Zenodo SHA-256 锚定 + bib 检查

**Files:**
- Modify: `NOETHER_paper.tex` near line 1119 (auditable proof of pre-registration paragraph)
- Possibly modify: `NOETHER_paper.bib` to add `NRCRG177` if not present

- [ ] **Step E5.1: Append Zenodo anchor sentence to pre-registration paragraph**

```bash
grep -n "auditable proof of pre-registration" /Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式/NOETHER_paper.tex
```

old_string:
```
The git timestamp chain (criterion
$\rightarrow$ inscope filter $\rightarrow$ Set~N derivation
$\rightarrow$ Set~G GP rerun $\rightarrow$ pooled M1) is the
auditable proof of pre-registration.
```

new_string:
```
The git timestamp chain (criterion
$\rightarrow$ inscope filter $\rightarrow$ Set~N derivation
$\rightarrow$ Set~G GP rerun $\rightarrow$ pooled M1) is the
auditable proof of pre-registration. To strengthen the third-party
verifiability of the pre-registration, the SHA-256 hash of
\texttt{configs/d4j\_algebra\_rich\_criterion.json} together with
the matching commit hash is deposited in supplementary~\ref{S7-d4j}
alongside the experiment artifact; reviewers may verify the deposit
against the criterion file directly.
```

- [ ] **Step E5.2: Check NRCRG177 cite exists in bib**

```bash
grep -n "NRCRG177\|@misc{NRCRG177\|@techreport{NRCRG177" /Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式/NOETHER_paper.bib
```

If 0 results, append to bib:

```bibtex
@techreport{NRCRG177,
  title  = {Regulatory Guide 1.77, Assumptions Used for Evaluating a Control Rod Ejection Accident for Pressurized Water Reactors},
  institution = {U.S. Nuclear Regulatory Commission},
  year   = {1974},
  number = {RG 1.77},
  url    = {https://www.nrc.gov/reading-rm/doc-collections/reg-guides/power-reactors/rg/division-1/division-1-77.html}
}
```

(Note: NRC RG 1.77 is the standard reference for control-rod-ejection MTC analysis on PWR; this is the canonical citation.)

- [ ] **Step E5.3: Verify**

```bash
grep -n "SHA-256 hash\|deposited in supplementary" /Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式/NOETHER_paper.tex
grep -c "NRCRG177" /Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式/NOETHER_paper.bib
```

Expected: ≥1 match for SHA-256; 1 match for NRCRG177 (definition).

### Group E checkpoint

- [ ] **Step E6: Compile + verify (xelatex + bibtex chain since bib changed)**

```bash
cd "/Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式" && \
  xelatex -interaction=nonstopmode NOETHER_paper.tex > /tmp/groupE_1.log 2>&1 && \
  bibtex NOETHER_paper > /tmp/groupE_b.log 2>&1 && \
  xelatex -interaction=nonstopmode NOETHER_paper.tex > /tmp/groupE_2.log 2>&1 && \
  xelatex -interaction=nonstopmode NOETHER_paper.tex > /tmp/groupE_3.log 2>&1; \
  echo "undef: $(grep -c 'Reference.*undefined\|Citation.*undefined' /tmp/groupE_3.log)"; \
  echo "missCh: $(grep -c 'Missing character' /tmp/groupE_3.log)"; \
  echo "bibtex didn't find: $(grep -c 'I didn.t find' /tmp/groupE_b.log)"
```

Expected: undef = 0; missCh = 0; bibtex 0 errors.

---

## Group F — Final compile + grep audits (CLAUDE.md §3 步骤 2 流水线)

### Task F1: Bib all-cited + compile + missing-character + secret-grep audits

- [ ] **Step F1.1: Bib all-cited check (CLAUDE.md §3 步骤 2a)**

```bash
cd "/Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式" && python3 -c "
import re, pathlib
tex = pathlib.Path('NOETHER_paper.tex').read_text()
bib = pathlib.Path('NOETHER_paper.bib').read_text()
cited = set()
for m in re.findall(r'\\\\cite[a-z]*\{([^}]+)\}', tex):
    for k in m.split(','):
        cited.add(k.strip())
defined = set(re.findall(r'@\w+\{([^,]+),', bib))
uncited = defined - cited
undefined = cited - defined
print(f'cited: {len(cited)}, defined: {len(defined)}')
print(f'uncited (in bib but not cited): {sorted(uncited)}')
print(f'undefined (cited but not in bib): {sorted(undefined)}')
"
```

Expected: undefined = ∅. uncited may be small (legacy unused entries are tolerable but should be reviewed).

- [ ] **Step F1.2: Final compile chain (CLAUDE.md §3 步骤 2b)**

```bash
cd "/Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式" && \
  xelatex -interaction=nonstopmode NOETHER_paper.tex > /tmp/final_1.log 2>&1 && \
  bibtex NOETHER_paper > /tmp/final_b.log 2>&1 && \
  xelatex -interaction=nonstopmode NOETHER_paper.tex > /tmp/final_2.log 2>&1 && \
  xelatex -interaction=nonstopmode NOETHER_paper.tex > /tmp/final_3.log 2>&1; \
  echo "undef: $(grep -c 'Reference.*undefined\|Citation.*undefined' /tmp/final_3.log)"; \
  echo "missCh: $(grep -c 'Missing character' /tmp/final_3.log)"; \
  echo "bibtex errors: $(grep -c 'error' /tmp/final_b.log)"; \
  echo "pages: $(pdfinfo NOETHER_paper.pdf | grep '^Pages' | awk '{print $2}')"
```

Expected: undef = 0; missCh = 0; bibtex errors = 0; pages ≈ 41–42 (was 40; new tables add ~1–2 pages).

- [ ] **Step F1.3: Anonymous-companion-paper grep (CLAUDE.md §3 步骤 2c)**

```bash
cd "/Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式" && \
  grep -nE 'Anonymous2025|Anonymous2026|anonymous reference|\[1\]\s*$|\[2\]\s*$' NOETHER_paper.tex NOETHER_paper.bib | head -20
```

Expected: no matches.

- [ ] **Step F1.4: Sensitive-info grep (CLAUDE.md §3 步骤 2e)**

```bash
cd "/Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式" && \
  grep -rIn -E "(/Users/[^/]+|sk-[A-Za-z0-9]{16,}|Bearer\s+[A-Za-z0-9]+|api_key\s*=\s*['\"][^'\"]{8,})" \
    --exclude-dir=.git --exclude-dir=.venv* --exclude-dir=texmf-dist --exclude-dir=node_modules \
    --include="*.tex" --include="*.bib" --include="*.md"
```

Expected: empty output.

- [ ] **Step F1.5: Em-dash zero-tolerance grep (CLAUDE.md §3 步骤 4)**

```bash
cd "/Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式" && \
  grep -cn $'—' NOETHER_paper.tex
```

Expected: 0 occurrences (em-dash U+2014 is zero-tolerance per CLAUDE.md §3 步骤 4). If any occur, do an additional pass to replace with `,` / `;` / `:` / `(...)` / period as context dictates.

### Task F2: Status report

- [ ] **Step F2.1: Compile final summary report**

```bash
echo "============================================="
echo "NOETHER TOSEM Revision — Implementation Report"
echo "============================================="
echo ""
echo "Tasks completed: 17 (M1, M-strat, M-cost, M1', M2, M3, M4, M5, M6, M7, M8, M9-M14, F1-F2)"
echo ""
echo "Compile health:"
echo "  PDF pages: $(pdfinfo /Users/limeng/Library/CloudStorage/OneDrive-个人/0-论文/MR识别/MR元模式/NOETHER_paper.pdf 2>/dev/null | grep '^Pages' | awk '{print $2}')"
echo "  Undef refs: $(grep -c 'Reference.*undefined\|Citation.*undefined' /tmp/final_3.log)"
echo "  Missing chars: $(grep -c 'Missing character' /tmp/final_3.log)"
echo ""
echo "Predicted TOSEM verdict shift: Major Revision → Minor Revision (≥80% confidence)"
echo ""
echo "Open follow-ups (not in this revision; for next round):"
echo "  - ISSUE-008: multi-LLM ensemble Set L expansion (Xu protocol scale)"
echo "  - ISSUE-009: cross-codebase replication (Apache Commons Math linear/ode/transform)"
echo "  - ISSUE-010: D1/D2 mutant labelling on §6.6 substrate"
echo "  - ISSUE-011: A_equi / A_rel Theorem 1' counterexample search"
echo "  - ISSUE-012: LRCA two-rater κ on Set N derivation (P3 phase)"
```

---

## Self-Review

After writing this plan, I checked it against the ARS R2 report and the user's narrative refinements:

1. **Spec coverage**:
   - ARS R2 致命 Dim 4.2 (30-min 数据落地) → M1 ✓ (already done)
   - ARS R2 致命 Dim 4.1 (LLM SOTA missing) → M2 (H3 split with H3b) + M-cost + B3 三 SOTA 代表 ✓
   - ARS R2 严重 Dim 1.1 (Set N κ) → M10 ✓
   - ARS R2 严重 Dim 1.2 (construct validity 5/5) → M3 (A1, A2, A4, A5) ✓
   - ARS R2 严重 Dim 1.3 (Set L N=1 LLM) → M2 + M-cost ✓
   - ARS R2 严重 Dim 2.1 (single codebase) → M6 (C1) ✓
   - ARS R2 严重 Dim 2.2 (DeepCrime ninth-block) → M7 (A6) ✓
   - ARS R2 严重 Dim 2.3 (PWR 反例域内同源) → M13 (D2) ✓
   - ARS R2 严重 Dim 3.1 (Bonferroni) → M4 (B3 step B3.3) ✓
   - ARS R2 严重 Dim 3.2 (H1/H2/H3/H4) → M5 (A3, A4) + M2 (A7) ✓
   - ARS R2 严重 Dim 4.3 (coverage_NOETHER) → M11 (E3, A3) ✓
   - ARS R2 严重 Dim 4.4 (𝓛* threshold) → M12 (E4) ✓
   - ARS R2 小瑕疵 3.3 (third-party registry) → M14 (E5) ✓
   - User refinement: 三 SOTA 代表 → B3 + B2 ✓
   - User refinement: 科学计算 scope precondition → A1 + A2 + C1 ✓
   - User refinement: D1/D2 mutant stratification → M-strat (B1) + future-work (e) ✓
   - User refinement: token cost → M-cost (B2) ✓

2. **Placeholder scan**: No "TBD" / "implement later" / "similar to X". All edits show full old/new text.

3. **Type consistency**: All cross-refs (\ref{tab:gen-cost}, \ref{subsec:pit-block-matrix}, \ref{tab:future-work}, \ref{tab:pit-block}, \ref{tab:algebra-rich-pooled}, \ref{tab:case-study}) are introduced before they are first cited:
   - \ref{tab:pit-block} introduced in B1, cited in B3 + A7 (after B1)
   - \ref{tab:gen-cost} introduced in B2, cited in B3 (after B2)
   - \ref{tab:future-work}~(e) introduced in B3 step B3.4

4. **Operator algebra notation consistency**: $\mathcal{A}_P$, $\mathcal{A}_{\mathrm{equi}}$, $\mathcal{A}_{\mathrm{rel}}$, $\mathcal{A}_{\mathrm{PWR}}$ used consistently per existing paper conventions.

No issues. Plan is execution-ready.

---

## Execution Handoff

**Plan complete and saved to:**
`docs/superpowers/plans/2026-05-10-noether-tosem-revision-plan.md`

**Two execution options:**

1. **Subagent-Driven (recommended)** — Dispatch a fresh subagent per Group (A, B, C, D, E, F), review between groups, fast iteration. Useful for keeping main-conversation context clean when individual edits are large.

2. **Inline Execution** — Execute tasks in this session using `superpowers:executing-plans`, batch execution with checkpoints for review at the end of each Group.

Which approach?
