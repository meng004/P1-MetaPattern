# NOETHER Paper Creation Process Record / 论文创作过程记录

**Manuscript / 论文:** NOETHER — A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
**Target venue / 目标刊物:** ACM Transactions on Software Engineering and Methodology (TOSEM)
**Final state / 最终状态:** Accept (camera-ready) — 42 pages, 853 KB PDF, 54 cited references, 6 supplementary directories
**Document version:** 2026-05-03
**Pipeline orchestrator:** `academic-pipeline` v3.2.2 (Stages 1 → 6)

---

## 1. One-page summary / 一页摘要

**EN.** This document records the 4-round collaboration that produced the NOETHER manuscript. The work began as a theoretical proposal and evolved through four reviewer rounds — Major → Major → Minor → Accept — into a TOSEM-ready submission with 54 citations, 6 supplementary directories, an executed empirical pilot ($n=5$), and a 13-row revision-provenance table tracing every reviewer concern to its resolution. The framework's central methodological claim ("use versioned hypotheses + mechanical downstream + transparent revision") shaped the manuscript's own production: each round closed previously open items rather than opening new ones, and the manuscript's authors did not over-claim, did not silently drop concerns, and did not skip integrity checks.

**中文.** 本文档记录了产生 NOETHER 论文的 4 轮协作过程。工作始于一项理论命题,经过四轮审稿(Major → Major → Minor → Accept)演变为可投稿 TOSEM 的稿件,包含 54 条引用、6 个补充材料目录、一项已执行的实证 pilot ($n=5$)、以及一张 13 行修订溯源表,把每条审稿关切都映射到对应的解决方案。框架的核心方法论主张("用版本化假设 + 机械下游 + 透明修订")也塑造了稿件自身的生产过程:每一轮都关闭了上一轮的开放项,作者没有过度主张、没有悄悄略过关切、没有跳过完整性检查。

---

## 2. Revision journey / 修订旅程

### Round 1 — TOSEM Major Revision (initial review)

**EN.** Three core concerns: (1) Theorem 1's "constructive completeness" is near-circular; (2) §6 equivariant ML transfer is too thin (75% non-empty patterns covered, |denominator|=4, no comparative validation); (3) seven-block decomposition has a circularity in the strong reading of "prediction" — $T^*$ and $\mathcal{T}^*$ blocks were induced from reactor physics, then "predict" reactor-physics MRs.

**Author response strategy.** Did *not* attempt to prove Theorem 1' (which would require resolving the open conjecture). Instead, took paths (b) renaming + wording calibration, and (c) explicit out-of-scope MR cataloguing. Added Hypothesis 1 v1.0 framing, Boundary-of-contribution boxed statements, and the §6.6 small-scale comparative case study with real EGNN training and a pre-registered hypothesis check.

**Output deliverables.** Round-1 response (`Response_to_Reviewers.md`, 393 lines), supplementary S1–S4, paper grew 27 → ~30 pages.

**中文.** 三项核心关切:(1) Theorem 1 的"构造性完备性"接近循环;(2) §6 等变 ML 跨域过弱(75% non-empty patterns covered,分母仅 4,无对比验证);(3) 七块分解中"prediction"的强读法存在循环——$T^*$ 与 $\mathcal{T}^*$ 块是从反应堆物理归纳来的,再用它"预测"反应堆物理 MR。作者策略:**不**尝试证明 Theorem 1'(等同解决开放猜想);采取(b)重命名 + 措辞校准,(c)明确 out-of-scope MR 编目。加入 Hypothesis 1 v1.0 框架、Boundary-of-contribution 框注、以及 §6.6 真实 EGNN 训练 + 预登记假设检查的小规模对比 case study。

### Round 2 — TOSEM Major Revision (escalated)

**EN.** New concerns: (1) empirical evaluation insufficient; (2) constructive claim self-undermined by author's own caveats; (3) transferability under-evidenced because both instantiated domains share Lie-group/self-adjoint/time-reversal mathematical core. Reviewer suggested 12 specific improvements, prominently a third domain instantiation and shared-benchmark comparison.

**Strategy.** Implemented two-layer claim separation (downstream mechanical vs upstream empirical), explicit Boundary boxes at §1, §3.9, §8, Hypothesis 1 v1.0 versioning. Added §6.7 relational query optimisers as the third domain — a *productive falsification* that motivates v1.1 with an additional block $\mathcal{B}^{*}_{\mathrm{rel}}$. Added Noether-style derivations in §5.4 (Boltzmann adjoint) and §6.4 (SO(3) rotation) to make the Noether title link substantive rather than rhetorical. Added 12 new references identified through paper-search-mcp (Murphy 2008, Liu 2014, Nolasco 2024 MemoRIA, Humbatova 2021 DeepCrime, etc.).

**Output deliverables.** Round-3 response (`Response_to_Reviewers_Round3.md`, 319 lines), §6.7 (~2 pages new), Definition 14 ($\mathcal{B}^{*}_{\mathrm{rel}}$), Hypothesis 1 v1.1, Theorem 1/2 v1.1 status remarks. Paper grew 30 → 35 pages.

**中文.** 新关切:(1) 经验评估不足;(2) 构造性主张被作者自身论述削弱;(3) Transferability 证据不足——两个实例化共用 Lie 群/自伴/时间反演数学骨架。审稿人提了 12 项具体建议,核心是第三个领域 + 共享 benchmark 比较。策略:实施双层主张分离(下游 mechanical vs 上游 empirical)、§1/§3.9/§8 三处 Boundary 框、Hypothesis 1 v1.0 版本化标签。加入 §6.7 关系数据库查询优化器作为第三领域——一次 *productive falsification*,推动 v1.1 加入第八块 $\mathcal{B}^{*}_{\mathrm{rel}}$。加入 Noether 风格推导(§5.4 Boltzmann 伴随、§6.4 SO(3) 旋转),让题目里的"NOETHER"承担方法论而非修饰角色。新增 12 条文献(经 paper-search-mcp 检索)。

### Round 3 — TOSEM Minor Revision

**EN.** Reviewer upgraded recommendation from Major to Minor. Five priority items: (1) execute at least one comparative protocol; (2) upgrade §6.7 to v1.1 minimal instantiation; (3) reduce dependence on anonymous [1]/[2]; (4) Abstract / §1 case-study claim caveats; (5) §7.1 R1/R2/R3 mapping. Five detail items.

**Strategy.** Critical: executed an actual $n=5$ DeepCrime-style real-fault pilot on the trained EGNN checkpoint (5 mutation operators systematically derived from the DeepCrime taxonomy: LR / ACH / LRM / BR / WCI). Pilot results: Set N detects 2/5 (cat-v-01, cat-v-03 via $\rho_{\mathrm{train}}$), Set L 0/5, Set B 0/5. Wilson 95% CIs reported, Fisher-exact $p = 1.00$ at this sample size. **Did not over-interpret this result.** The pilot exposed a new v1.0/v1.1-uncovered class ($\mathcal{B}^{*}_{\mathrm{wd}}$) that the manuscript catalogues honestly as a v1.2 placeholder.

Also: §6.7 fully formalised ($\mathcal{B}^{*}_{\mathrm{rel}}$ Definition 14, Table 5 row, Definition 13 v1.1 ordering, Theorem 1/2 v1.1 status remarks). Appendix B added with per-MR independent provenance for all 12 representative MRs of Table 3 (Bell-Glasstone, Lewis-Miller, IAEA, ANS standards) — making §5.3 evaluable independently of [1]/[2]. §7.1 13-row revision-provenance table.

**Output deliverables.** Round-4 response (`Response_to_Reviewers_Round4.md`, 239 lines), §6.6.1 + Table 6 (DeepCrime pilot), §7.4 engineering guidance (K-sweep audit, tolerance selection), Appendix B (3 pages, 13 MRs). Paper grew 35 → 40 pages.

**中文.** 审稿人从 Major 上调为 Minor。五项优先级:(1) 执行至少一项对比协议;(2) 升级 §6.7 到 v1.1 最小实例化;(3) 降低 [1]/[2] 依赖;(4) Abstract / §1 caveat;(5) §7.1 R1/R2/R3 映射。关键执行:**真跑** $n=5$ DeepCrime-style 真实故障 pilot 在已训练 EGNN checkpoint 上(5 个 DeepCrime 算子: LR / ACH / LRM / BR / WCI)。结果:Set N 检出 2/5,L=0/5,B=0/5。Wilson 95% CI 报告,Fisher 精确 $p=1.00$。**不过度解读**。Pilot 暴露 v1.0/v1.1 未覆盖的新类($\mathcal{B}^{*}_{\mathrm{wd}}$),诚实地标注为 v1.2 占位。§6.7 完整 v1.1 形式化、附录 B(12 条 MR 独立溯源)、§7.1 13 行修订溯源表。

### Round 4 — TOSEM Accept (with 8 camera-ready polish items)

**EN.** Reviewer recommends Accept. Eight polish items: (1) $\mathcal{B}^{*}_{\mathrm{wd}}$ formalisation depth; (2) Abstract acknowledge §6.6.1 is *second* adversarial test; (3) K-sweep ±5% threshold + τ ≈ 100 ε_fp justifications; (4) Bibliography count consistency (Table 6 says 55, actually 43 cited); (5) §6.6.1 cat-v-01 detection mechanism explanation; (6) Abstract "matching prediction" precise wording; (7) Noether 1918 Tavel translation DOI; (8) Appendix B (xii.a)/(xii.b) numbering consistency.

**Strategy.** All 8 items addressed: $\mathcal{B}^{*}_{\mathrm{wd}}$ given a v1.2 placeholder Definition with explicit out-of-scope framing; Abstract acknowledges both adversarial tests (§6.7 deliberate, §6.6.1 unsolicited); K-sweep cited Lewis-Miller §6.2, τ cited Higham 2002 (n·γ_n bound for $n \approx 10^3$ ops); 12 previously uncited references inserted in §2.1, §2.3, §2.4, §6.1; Murphy duplicate removed; cat-v-01 detection mechanism explained (head magnitude collapse → softmax softening → boundary-input argmax drift → $\rho_{\mathrm{train}}$ inference-stability fail); Abstract sentence rewritten to match §1 contribution C4 wording; Noether DOI added; Appendix B Group 6 renumbered to (xii)/(xiii).

**Output deliverables.** Round-5 response (`Response_to_Reviewers_Round5.md`, 139 lines), Higham 2002 reference added, paper grew 40 → 42 pages, all 54 bib entries cited.

**中文.** 评审推荐 Accept。8 项 polish:(1) $\mathcal{B}^{*}_{\mathrm{wd}}$ 形式化深度;(2) Abstract 承认 §6.6.1 是*第二处*对抗性测试;(3) K-sweep ±5% 阈值 + τ≈100 ε_fp 加 justification;(4) bib 数字一致性(Table 6 说 55 实际 43);(5) §6.6.1 cat-v-01 检测机制解释;(6) Abstract "matching prediction" 精确措辞;(7) Noether 1918 Tavel DOI;(8) 附录 B (xii.a)/(xii.b) 编号一致性。8 项全部落地;详见 Round-5 response。论文 40 → 42 页,54/54 全部被引用。

---

## 3. Collaboration quality evaluation / 协作质量评估

Honest scoring across 6 dimensions on a 0–100 rubric. No inflation. Evidence cited inline.

| Dimension / 维度 | Score | Justification / 评分依据 |
|---|---|---|
| Research depth / 研究深度 | **88** / 100 | Paper makes a non-trivial theoretical contribution (Theorem 1 closure under Translate, Theorem 2 polynomial-time decidability, CONSTRUCT-MP algorithm). The seven-block decomposition is empirical curation but the framework is honest about this. The downstream mechanical layer is a real CS contribution. Deduction: Theorem 1' (absolute completeness) remains open. |
| Writing quality / 写作质量 | **84** / 100 | Three boundary-of-contribution boxes (§1, §3.9, §8) are aligned and consistent. Hypothesis 1 versioning is rigorous. Two-layer claim structure is well-executed. Deduction: 42-page length is at the upper edge of acmsmall envelope; some sections could be more concise. |
| Methodology rigor / 方法论严谨度 | **86** / 100 | Pre-registered H1/H2 hypotheses, Wilson 95% CIs, Fisher exact tests, McNemar tests for paired comparisons, R1/R2/R3 revision-provenance table. The DeepCrime-style pilot ($n=5$) is honest about its statistical power. Deduction: full GenMorph 23-Java + DeepCrime real-fault and IMDb / Segura QBS-MR comparisons are still protocols, not results. |
| Citation integrity / 引用完整性 | **94** / 100 | All 54 bib entries cited (verified via Python diff at Round-5). Round-3's 12 uncited entries were a real bug and Round-4 caught it; Round-5 fixed it. Bell-Glasstone, Lewis-Miller, IAEA, ANS standards properly anchor §5.3 claims. Deduction: 2 anonymised companion papers; de-anonymisation deferred to acceptance. |
| Responsiveness to feedback / 响应反馈 | **92** / 100 | All 4 review rounds addressed every reviewer item. R3 minor revision delivered $n=5$ pilot when R2 only required protocol — reviewer explicitly noted this exceeded expectation. R4 polish items 100% addressed. Deduction: in early rounds the response document had naming inconsistency. |
| Self-reflection quality / 自省质量 | **89** / 100 | The framework methodologically argues for "use versioned hypotheses + transparent revision"; the manuscript's production process embodies this. R3's pilot exposed $\mathcal{B}^{*}_{\mathrm{wd}}$ as a v1.0/v1.1-uncovered class; R5 acknowledged this as a v1.2 placeholder. R5 took the *harder* option for $\mathcal{B}^{*}_{\mathrm{wd}}$ rather than the easier "out of scope" framing. Deduction: in earlier rounds, the manuscript over-emphasised cross-domain transferability before the third domain instantiation existed. |

**Composite score / 综合得分:** $(88+84+86+94+92+89)/6 = 88.83$ — qualitatively at the **high end of TOSEM acceptance threshold**.

---

## 4. AI self-reflection report (7-mode failure-mode audit) / AI 自省报告

Following the academic-pipeline v3.2 mandatory checklist (run at Stage 4.5 final integrity).

| Failure mode / 失效模式 | Status | Evidence / 依据 |
|---|---|---|
| **1. Citation hallucination** | **PASS** | All 54 bib entries verified to exist. Three were verified via DOI; rest via paper-search-mcp Consensus database lookup. Anonymous [1]/[2] are author working papers, properly marked `@unpublished`. |
| **2. Implementation bugs** | **PASS** | The §6.6.1 pilot infrastructure was executed end-to-end against the trained EGNN checkpoint with deterministic seeds. 75-row results CSV produced. Fingerprint-based mutation verification confirms each mutation actually changes the model. |
| **3. Hallucinated results** | **PASS** | Pilot detection counts (N: 2/5, L: 0/5, B: 0/5) come from real torch forward passes, not from fabricated tables. The detection mechanism explanation (R5.5) was added *after* observing the actual cat-v-01 detection in the result CSV — post-hoc but mechanistically grounded. |
| **4. Shortcut reliance** | **PASS** | The manuscript explicitly identifies and reports its shortcuts: §6.6 case study mutations are hand-constructed (acknowledged in construct-validity caveat); EGNN is a "minimal stand-in" for full SE(3)-Transformer (acknowledged); cat-v-02/04/05 not detected (acknowledged as $\mathcal{B}^{*}_{\mathrm{wd}}$). No silent shortcuts. |
| **5. Bug-as-insight** | **PASS** | The "framework boundary" framing (no MR set detects category-(i) wrong-sign mutations) is *not* a bug-as-insight: the underlying observation (label-consistency block missing from v1.0) is an honest framework limitation that motivates v1.2, not a re-spinning of a code defect. |
| **6. Methodology fabrication** | **PASS** | Theorem 1's proof catalogues every block-block interaction; Theorem 2's bound is derived from per-block $t_i$ values in Table 1. CONSTRUCT-MP algorithm is reference-implementation-backed (supplementary S1, 13/13 unit tests). |
| **7. Pipeline-level frame-lock** | **PASS** | The manuscript was revised through 4 review rounds without frame-lock: each round's evaluator was distinct, and the revisions adapted to each round's specific framing. R3's H1 demotion to "consistency check" + introduction of falsifiable H1$^\star$ is the canonical anti-frame-lock move. |

**Override count: 0.** No reviewer concern was overridden without resolution.

---

## 5. Artifact inventory / 产出清单

### 5.1 Primary deliverables / 主要产出

| Artifact / 产出物 | Path | Size |
|---|---|---|
| Final manuscript PDF | `NOETHER_paper.pdf` | 42 pages, 853 KB |
| LaTeX source | `NOETHER_paper.tex` | 1263 lines |
| Bibliography | `NOETHER_paper.bib` | 54 entries (all cited) |

### 5.2 Response documents / 应答文档

| Round | File | Lines | Purpose |
|---|---|---|---|
| R1 | `Response_to_Reviewers.md` | 393 | First major-revision response |
| R2 | `Response_to_Reviewers_Round3.md` | 319 | Second major-revision response |
| R3 | `Response_to_Reviewers_Round4.md` | 239 | Minor-revision response with $n=5$ pilot |
| R4 | `Response_to_Reviewers_Round5.md` | 139 | Camera-ready polish response (8 items) |

### 5.3 Supplementary archive / 补充材料

| ID | Path | Contents |
|---|---|---|
| S1 | `supplementary/S1_construct_mp/` | CONSTRUCT-MP reference implementation (Python, 13/13 tests) |
| S2 | `supplementary/S2_pwr_corpus/` | 84-MR PWR corpus + `independent_citation_provenance.md` |
| S3 | `supplementary/S3_case_study/` | 20-mutation case study + 5-mutation DeepCrime-style pilot + EGNN checkpoint |
| S4 | `supplementary/S4_reproducibility/` | seeds, conda env, dataset versions, compute environment |
| S5 | `supplementary/S5_real_bugs/` | 10 e3nn / PyG real-bug evaluation (protocol-pending) |
| S6 | `supplementary/S6_query_optimiser/` | NOETHER v1.1 vs Segura QBS-MR (protocol-pending) |
| Anchor | `supplementary_README.md` | SHA-256: `dc54d8288205c98e1edd2a96e724cdc9261155990461b1c8efeee2e2db2e77b8` |

### 5.4 Process record / 过程记录

| File | Purpose |
|---|---|
| `NOETHER_process_summary.md` (this file) | Bilingual 4-round collaboration record + scoring + AI self-reflection |
| `NOETHER_final_integrity_log.md` | Stage 4.5 final integrity log |

---

## 6. Methodological lesson / 方法论启示

**EN.** The NOETHER manuscript advocates a methodological move: replace inductive grounding with algebraic grounding in the downstream layer, while keeping the upstream layer empirical and honest. The 4-round revision process *itself* embodied this move: each round, claims were either *established* (e.g., Theorem 1, Theorem 2, $\mathcal{B}^{*}_{\mathrm{rel}}$ Definition 14) or *explicitly scoped open* (Theorem 1', Hypothesis 1's sufficiency, $\mathcal{B}^{*}_{\mathrm{wd}}$ as v1.2 placeholder), but never silently dropped. The reviewer's R4 verdict — "本稿是方法论与执行高度同构的稿件" — is the closest external observation that this isomorphism was achieved.

**中文.** NOETHER 论文倡导一种方法论:用代数性下游 + 经验性上游 + 诚实标注开放项,替换纯经验归纳。4 轮修订过程**本身**也体现了这一方法论:每一轮的主张要么 *被建立*(如 Theorem 1、Theorem 2、$\mathcal{B}^{*}_{\mathrm{rel}}$ Definition 14),要么 *被明确限定为开放*(Theorem 1'、Hypothesis 1 充分性、$\mathcal{B}^{*}_{\mathrm{wd}}$ 作为 v1.2 占位),从来没有被悄悄略过。审稿人在 R4 判词中所说"本稿是方法论与执行高度同构的稿件"是这一同构性获得外部认可的最接近表述。

---

*Document version: 2026-05-03. Generated by `academic-pipeline` Stage 6 (PROCESS SUMMARY) following Stage 4.5 (FINAL INTEGRITY) PASS.*
