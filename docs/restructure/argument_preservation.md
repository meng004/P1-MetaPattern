# 论点-论据保鲜文件

**目的**：在 IMRaD 重构前固化 7 个核心论点与其支撑证据；重构后逐条核查"论点不漂移"。

**重构原则**（用户明示）：本文的论点不应随着修订出现漂移。

---

## 论点 C1：两层框架（two-layer framework）

**论点表述**：NOETHER 是一个两层框架——upstream 层（algebra distillation + 8-block decomposition，empirical hypothesis）+ downstream 层（CONSTRUCT-MP algorithm，deductive 可证）。Upstream 层 honest about empirical grounding；downstream 层 mechanical。

**当前位置**：§3 (operator-algebraic prelim) + §4 (NOETHER framework) 散落

**重构后位置**：新 §3.1-§3.4 集中

**支撑证据**：
- Hypothesis 1 (7-block plus 1 relational equivalence block): NOETHER_paper.tex L394 `\label{hyp:seven-blocks}`
- 8 block definitions: L319, L327, L335, L339, L345, L353, L361, L367, L375, L386
- CONSTRUCT-MP algorithm: L469 `\subsection{Construction of the MetaPattern set}`
- Figure 1 (architecture): L139-200 `fig:noether-arch`

**不漂移检查**：重构后 §3 必须显式陈述"two-layer"措辞，且 Figure 1 留 §1。

---

## 论点 C2a：Theorem 1（algebraic closure）+ Theorem 2（poly-time decidability）

**论点表述**：
- Th 1: $\mathbb{M}(\mathcal{A}_P)$ 在 *Translate* 操作下闭合（over algebra-induced MR space $\mathrm{MR}(\mathcal{A}_P)$）
- Th 2: CONSTRUCT-MP 在 finite generating set 下运行时间多项式

**当前位置**：§4.2 + §4.3 + Appendix C.3, C.4

**重构后位置**：新 §3.3 + §3.4 + Appendix C 不动

**支撑证据**：
- Theorem 1 statement: L490 `\begin{theorem}[Algebraic Closure under \texttt{Translate}]`
- Theorem 2 statement: L518 `\begin{theorem}[Decidability]`
- tab:complexity: §4 内
- Appendix C.3 Th1 full proof: L2669
- Appendix C.2 per-block Translate instantiations: L2641
- Appendix C.1 well-foundedness lemma: L2630

**不漂移检查**：Theorem 1, 2 statements 文字必须**逐字保留**；tab:complexity 必须出现在新 §3.4 内。

---

## 论点 C2b：Theorem 1' 绝对完备性 **被证伪**（negative theory）

**论点表述**：Theorem 1'（绝对完备性猜想：$\mathbb{M}(\mathcal{A}_P)$ 在 $\mathcal{A}_P$ 中 expressible 的任意 property 上闭合）在 PWR core diffusion algebra $\mathcal{A}_{\mathrm{PWR}}$ 上**通过两个 pairwise-independent counterexamples 被证伪**：
1. Non-additivity of rod-bank reactivity worth
2. Second-order mixed dependence of $k_{\mathrm{eff}}$ on moderator temperature and boron concentration

5 个 Translate-extension dimensions 是 follow-up work 的 principal locus。

**当前位置**：§6.8 (L999) + Appendix C.4 (L2691) + Appendix C.6 (L2718)

**重构后位置**：新 §3.6 (theory 章末，与 positive theory 对偶呈现) + Appendix C 不动

**支撑证据**：
- Negative instantiation 主文: §subsec:negative-pwr L999
- Proposition: Non-additivity is not Translate-reachable: L1064
- Proposition: MTC-vs-boron mixed dependence is not Translate-reachable: L1111
- tab:five-obstructions: §6 内（PIT-unexercised 5 blocks）
- Appendix C.4: An open problem absolute completeness L2691
- Appendix C.5: Out-of-scope MRs three concrete classes L2702
- Appendix C.6: Proofs for negative instantiation on A_PWR L2718

**不漂移检查**：两个 propositions 必须保留；tab:five-obstructions 必须迁至新 §3.6；5 Translate-extension dimensions 必须显式列出。**关键短语保留**："Theorem 1' is falsified ... via two pairwise-independent counterexamples"。

---

## 论点 C3：Systematisation（归纳重组为 deductive）

**论点表述**：NOETHER 把现有的 inductive MR catalogues（PWR 84-MR / METRIC+ 11-pair D×R / Sun 2021 等）**重组**为 deductive output。Induction is *relocated* from MR-instance level to algebra-block level rather than eliminated.

**当前位置**：§5 Boltzmann (refinement) + §8.3 PMCM worked example

**重构后位置**：新 §3.5.1 (theory worked example via tab:refinement) + 新 §4.2 (RQ1 empirical: 84/84 mapped) + 新 §4.6 (RQ5 METRIC+ PMCM)

**支撑证据**：
- §5 refinement subsec: L588 `\subsection{Relationship to the prior inductive catalogue: refinement plus prediction}`
- tab:refinement (核心 mapping 表，**必留 body**)
- tab:elementwise (12 MRs，**方案 A: 压缩为 4 MRs；完整 12 → Supp S1**)
- §5.4 Noether-style derivation of $m_{\mathrm{adj}}$: L651
- §8.3 PMCM worked example + tab:metricplus-sorting: L2530
- 84-MR full enumeration: 已在 Supp S1 (reproducibility)

**不漂移检查**：tab:refinement 必须留 body；"84/84 mapped to 5 of 8 blocks" 必须有句陈述；PMCM coverage claim 必须保留。

---

## 论点 C4：三个 structurally distinct instantiations

**论点表述**：NOETHER 实例化于三个 operator-algebraic domains：
1. Boltzmann reactor-physics transport（systematises prior inductive catalogue）
2. Equivariant machine learning（executable MRs for rotation invariance, adjoint duality, training-trajectory reversibility）
3. Relational query optimisers（idempotent-semiring algebra exercises relational-equivalence block beyond Lie-group / self-adjoint / time-reversal core）

**当前位置**：§5 (Boltzmann) + §6.1-§6.5 (equi-ML theory) + §6.6 (equi-ML case study) + §6.7 (RDB)

**重构后位置**：新 §3.5.1 + §3.5.2 + §3.5.3 (theory consolidation) + 新 §4.3 (RQ2 cross-domain executability)

**支撑证据**：
- $\mathcal{A}_{\mathrm{Boltz}}$ section: L568
- $\mathcal{A}_{\mathrm{equi}}$ section: L679-998 (excluding negative PWR)
- SE(3) end-to-end derivation: L695
- Adjoint-attention duality MR: L738
- Training-trajectory time-reversal MR: L757
- Small-scale case study: L782 (含 tab:case-study)
- $\mathcal{A}_{\mathrm{rel}}$ third domain: L970
- algebra_breakdown.md: supplementary/S6_query_optimiser/algebra_breakdown.md

**不漂移检查**：三个 algebras 必须均出现在 §3.5；三者**结构性不同**的论点必须保留（Boltzmann 用 D, L, T*, T_rev；equi-ML 用 G, T*; RDB 用 B*_rel）。

---

## 论点 H L*：L*-blindness 5/6 falsifiable prediction（pre-registered）

**论点表述**：NOETHER 的中心 falsifiable prediction：homogeneity-preserving mutators 对 L*-block MRs 系统性盲。预测 5/6 在 in-scope substrate 上通过。

**当前位置**：§7 整章 (L1160-2177)

**重构后位置**：新 §4.4 (RQ3) + §4.5 (RQ4 head-to-head)

**支撑证据**：
- Prediction statement: L1187 `\subsection{The prediction: L*-block blindness}`
- PIT × 8-block compatibility: L1292 + tab:pit-block
- Test design: L1355
- Central result 5/6: L1417 + tab:l-blindness
- Per-block patterns: L1498 (Witness 1 + tab:rediscovery)
- Witnesses: L1564 (Witness 2)
- Head-to-head: L1601 + tab:algebra-rich-pooled + tab:per-block-headtohead + tab:two-stratum
- Cost analysis: L2042 + tab:gen-cost
- Summary: L2120

**不漂移检查**：
- 5/6 数字必须**逐字保留**
- Pre-registered 措辞必须保留（"committed to git before data collected"）
- McNemar exact $p = 0.0043$ pooled / $p = 0.019$ on D1 必须保留
- "Set N is dominated by Set G in the aggregate" (RuleS 9 honest disclosure) 必须保留
- 三层 reading：algebraic derivability + per-block complementarity + D2 boundary

---

## 论点 H_MP：METRIC+ subsumption $H_{\mathrm{MP1}}$ 被证伪（互补 not 竞争）

**论点表述**：在 Sun 2021 自有 4 subjects (SPHONE / SBAGGAGE / SEXPENSE / SMEAL) 上 pre-registered 头对头协议；Python (n=219) + Java/PIT (n=120) + Major/JDK11 (n=555) 三层执行。两个 tool 在 α=0.05 下定性一致 (McNemar p=0.625 PIT; p=0.211 Major; 均 NS)。Major 更大 pool 暴露 *bidirectional* per-subject reach asymmetries (Set MP exclusive on SPhone; Set N exclusive on SBaggage) cancel pooled。$H_{\mathrm{MP1}}$ pre-registered subsumption 在**双向**上 falsified per-subject——**论点-strengthening**。

**当前位置**：§8.2 (L2193) + Supp S8 (Path A protocol + results_path_a.md + results_path_a_full.md + results_path_a_major_crosstool.md)

**重构后位置**：新 §4.6 (RQ5) + Supp S8 不动

**支撑证据**：
- Relationship with METRIC and METRIC+: §subsec:relationship-metric-plus L2193
- tab:metricplus-headtohead-small (Tier 1 manual 3 SUTs)
- tab:metricplus-sun2021-scope (Tier 2 scope analysis)
- Supp S8: protocol_path_a_headtohead.md (pre-registered protocol)
- Supp S8: results_path_a.md (Tier 3 Python)
- Supp S8: results_path_a_full.md (Tier 3+ Java/PIT)
- Supp S8: results_path_a_major_crosstool.md (Tier 3++ Major cross-tool)

**不漂移检查**：
- 三层 n 数字必须保留：n=219 (Python) / n=120 (Java/PIT) / n=555 (Major)
- McNemar p 值必须保留：p=0.625 (PIT pooled) / p=0.211 (Major pooled)
- "bidirectional per-subject reach asymmetries cancel pooled" 必须保留
- "H_MP1 falsified bidirectionally → 论点-strengthening rather than论点-weakening" 必须保留

---

## 重构后论点核查清单

重构完成后逐条核查（每条必须 ✓）：

- [ ] C1: "two-layer framework" 措辞在新 §3 出现
- [ ] C2a: Theorem 1, 2 statements 逐字保留；tab:complexity 在新 §3 内
- [ ] C2b: "Theorem 1' falsified via two pairwise-independent counterexamples" 措辞保留；tab:five-obstructions 在新 §3.6 内
- [ ] C3: tab:refinement 在新 §3.5.1 (body)；84/84 mapped 陈述保留
- [ ] C4: 三 algebras ($\mathcal{A}_{\mathrm{Boltz}}$ / $\mathcal{A}_{\mathrm{equi}}$ / $\mathcal{A}_{\mathrm{rel}}$) 均在新 §3.5
- [ ] H L*: 5/6 数字 + McNemar p 值 + "Set N dominated by Set G aggregate" + 三层 reading
- [ ] H_MP: n=219/120/555 + McNemar p=0.625/0.211 + bidirectional cancellation + 论点-strengthening
- [ ] Cover letter 6 headline messages 全部仍被新结构支撑

## 措辞保留清单（重构中**不得改写**）

以下短语在 cover letter 中明示，必须**完整保留**：

1. "two-layer framework with positive *and* negative theory"
2. "Theorem 1' (absolute completeness) falsified on PWR core diffusion algebra"
3. "two pairwise-independent counterexamples"
4. "Three structurally distinct instantiations"
5. "Set N is *dominated* by Set G in the aggregate (McNemar exact $p = 0.0043$ pooled; $p = 0.019$ on D1 only)"
6. "The framework's contribution is read at three layers — algebraic derivability, per-block complementarity, and an out-of-scope D2-stratum boundary"
7. "$\mathcal{L}^{*}$-blindness pattern on homogeneity-preserving mutators ... 5/6 on the in-scope substrate"
8. "bidirectional per-subject reach asymmetries ... cancel pooled — the strongest possible empirical evidence for the framework's 'complementary not competitive' reading"
9. "$H_{\mathrm{MP1}}$ ... falsified in *both* directions per-subject, which is论点-strengthening rather than论点-weakening"
10. "Induction is *relocated* from MR-instance level to algebra-block level rather than eliminated"
