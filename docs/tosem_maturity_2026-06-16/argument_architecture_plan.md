# NOETHER 论证方案与材料组织（argument architecture plan）

> 产出日期：2026-06-17
> 范围：论证设计 + 材料分工，不改 `NOETHER_paper_arxiv.tex` 正文，不跑新实验。
> 依据：作者指令"**核心贡献 = 从数学物理方程算子的代数结构导出 MR；其他皆辅助**"
> + 前序指令"进攻性、探究深层原理、有被质疑的勇气"。
> 标注 **[需作者数学判断]** 的条目 agent 不可代证。

---

## 0. 一句话核心（sharpened thesis）

> 数学物理程序所容许的 MR 集合，**不是**一个需要归纳采样的开放设计空间，而是其
> **算子代数的可计算函数**。我们给出该推导过程，证明其良构，并证明该推导的
> **预测力可证伪、且跨域成立**：算子代数在看任何 MR 语料之前，就决定了哪些 MR
> 存在、哪些 block 被占据、derived MR 对哪类故障**结构性致盲**。

设计约束（三条，全程不可违背）：

1. **数据诚实，论点进攻**：n / CI / 检出率照实（CLAUDE.md C6 硬规），但论点由
   **跨域结构律**承担，小样本点估计退为完整性附录，不作头条。
2. **核心唯一**：算子代数 → MR 推导 是唯一核心；定理、3 域、负实例、S10、12-PUT、
   METRIC 对比 全部是**服务核心的证据**，不与核心争头条。
3. **边界即力量**：推导的失败边界（Thm 1′ 证伪、5 维 Translate 扩展、检出下限）
   是"推导有力量"的反向证据，公开陈列，邀人攻击。

---

## 1. 诊断：现稿为何被判"理论平凡 / 只研不究"

| 现稿症状（行号） | 病因 | 后果 |
|---|---|---|
| L256「contribution is systematisation rather than deduction」 | 自我降格为"整理" | 评审判 "not novel" |
| Thm 1（closure）作头条；L574 自认 "by-construction … near-tautological" | 把**良构性**当**贡献** | "理论内核平凡" |
| Thm 1′（absolute completeness）被自家 PWR 反例证伪 | 最强断言自证伪 | 读作"框架不完备"而非"边界清晰" |
| 唯一 ex-ante 预测只有 L\*-blindness | 推导的"预测力"证据单薄 | 无法支撑"推导有力量" |
| head-to-head vs GenMorph（n=5 underpowered）作卖点 | 用弱统计争"优越性" | 被 Reviewer 2 攻欠功效 |
| CONSTRUCT-MP Step 3/4 per-block vs per-class 歧义（protocol_theory T1） | 定义级 bug | 推导过程本身不严谨 |

**根因**：现稿把"closure（by-construction）"误当核心 → 必然平凡；把"优越性
（underpowered）"当卖点 → 必然防御。**核心选错了。** 真正非平凡、可证伪、可进攻的，
是**推导的预测力与其代数刻画的边界**。

---

## 2. 非平凡化策略（三招，按重要性）

### 招 1（关键）：把 P2「不变性致盲」形式化为新定理 —— 非 by-construction 的理论内核

S10 已实测出（paired McNemar，同 29 真故障）：algebra-MR battery 与中立微分 oracle
**互补不冗余**（MR-only=6、diff-only=5），且 diff-only 全部是 advection-speed /
wavenumber-sign 故障 —— 即 MR battery 因 **平移/Galilean 不变性**对"沿该不变性轨道
的故障"结构性致盲。把它升为定理：

> **Invariance-Blindness Theorem（拟）**：设 ρ = Translate(ι, s) 为从 block s 的
> 不变量 ι 导出的 algebra-induced MR，其有效性依赖 P 在变换群 T_s 下的不变性。则
> ρ 的"检出核"（kernel）包含一切只在 T_s 轨道方向上作用的故障 δ：对此类 δ，
> ρ(mutant) 恒 hold。**推论**：任何单-block battery 不完备；完备性要求一族 block，
> 其联合 stabilizer 平凡。

- **为什么非平凡**：它不是 by-construction —— 它陈述了 derived MR 的**固有极限**，
  是关于"代数推导能力上界"的真命题，可证伪（造一个 Galilean-不变却能抓 speed 误差
  的 MR 即推翻）。
- **直接回应**评审"理论平凡"：这是 Thm 1（平凡）之外一条**有内容**的定理。
- **证据已就绪**：S10 paired McNemar + diff-only 故障分类即其实证确认。
- **[需作者数学判断]**：T_s「轨道方向故障」的精确形式化（fault 作为 A_P 上的扰动
  算子 δ，"沿轨道"= δ 与 T_s 表示可交换？）；kernel 非空性的一般性证明 vs 仅在
  本文 block 族成立。protocol_theory 的 T2（Composite-Translate）与此互补。

### 招 2：把 Theorem 1 从"贡献"降为"良构引理"，把"推导有预测力"升为头条

- Thm 1（closure）+ Thm 2（poly-time）合并表述为 **Well-formedness Lemma**：
  "CONSTRUCT-MP 不会漏掉任何 Translate-可达 MR，且多项式可判定" —— 诚实承认
  by-construction，定位为"推导过程**自洽**的保证"（必要管道），**不再是 novelty**。
- 头条改为 **Derivation-Force claims（可证伪预测族）**：从 A_P 单独、在看任何 MR
  语料之前可推出并已确认的预测：
  - **L1 Block 占据律**（= S10 P1 + 现稿 L\*-blindness 的推广）：哪些 block 被占据，
    由 PDE 类**先验可测**；9/9 home-field SUT 零例外（唯一可逆 wave 占 T_rev\*+
    Conservation，耗散 SUT 的 T_rev\* 恒空）。
  - **L2 不变性致盲律**（= 招 1）。
  - **L3 离散可检出下限**（= S10 P3）：跨实现微分检出有硬下限 δ。
- 修订 L256：删"systematisation rather than deduction"的自我降格，改为"derivation
  with falsifiable predictive force, whose downstream step is mechanical and whose
  empirical force is established by three predictions confirmed across N domains"。

### 招 3：负实例 + 检出下限 = "推导有边界、边界可代数刻画" 的勇气陈列

- PWR Thm 1′ 证伪（2 反例 → 5 维 Translate 扩展，pairwise-independent on A_PWR）
  从"尴尬的自证伪"重构为 **Boundary Theorem 候选**："derived MR 空间的边界本身被
  代数刻画为 5 个独立扩展维"。
- 每条 detectability law 附**一行反驳条件**（已在 `supplementary/S10.../ANALYSIS.md`）。
- 明确写"我们邀请以下攻击"（block 是 battery 的产物 / 更巧的单 oracle 完备 / 更巧的
  容差破下限），各给一行 refutation。

---

## 3. 论证主链（spine：claim → support，7 步）

| # | 主张 | 支撑材料 | 角色 |
|---|---|---|---|
| S1 | MR 识别受困于归纳（origin/closure/transferability gap） | 现稿 §1 + §2 related work；12-PUT/5-MP 旧归纳目录 | 问题设定 |
| S2 | 用"从算子代数推导"替代归纳（Noether 类比，方法论而非定理） | 现稿 §1 Noether 脚注 | 立论 |
| S3 | 推导机制：A_P → 8-block 分解 → CONSTRUCT-MP → M(A_P) | 现稿 §3.1–§3.2（修 Step3/4 bug, T1） | **核心机制** |
| S4 | 推导良构：不漏 Translate-可达 MR + 多项式可判定（诚实 by-construction） | Thm 1 + Thm 2 → 合为 Well-formedness Lemma | 辅助（管道） |
| S5 | **推导有预测力（offensive 头条）**：A_P 先验预测 block 占据 / 致盲 / 检出下限，且确认 | **L1**=S10 9-SUT + 现 L\*-blindness；**L2**=S10 paired McNemar；**L3**=S10 微分 oracle δ | **核心力量** |
| S6 | 推导有可代数刻画的边界 | PWR 负实例（5 维）；ANALYSIS.md 三条 law 的反驳条件 | 边界（勇气） |
| S7 | 推导跨域稳定 | 3 域（Boltzmann/ML/relational）+ 9 PDE home-field 同 8-block | 迁移性 |

主链一句话：**S3 给推导，S4 证良构，S5 证推导有力量（可证伪预测），S6 标边界，
S7 证跨域** —— S5 是新的重心。

---

## 4. 材料组织（role table：每份资产 → 角色）

| 资产 | 现位置 | 新角色 | 处理 |
|---|---|---|---|
| A_P + 8-block + CONSTRUCT-MP | §3.1–3.2 | **CORE 机制** | 保留；修 Step3/4 歧义（T1 选项 A/B/C 需作者定） |
| Invariance-Blindness（招1） | 新增（源自 S10 P2） | **CORE 定理** | 新写 §3 一条 Theorem + 证明草图 |
| S10 home-field 9 SUT（P1 block 占据） | `supplementary/S10` | **PRIMARY 证据**（L1） | 升为 §5 主实验之一 |
| S10 paired MR-vs-differential（P2） | `S10/results/.../paired_vs_mr.json` | **PRIMARY 证据**（L2/招1 实证） | 升为 §5 |
| S10 微分 oracle + δ 敏感度（P3） | `S10/.../advdiff-xeval-diff` | **PRIMARY 证据**（L3） | 升为 §5 |
| 现 L\*-blindness 预测 | §5.2（L1232+） | PRIMARY（并入 L1 family） | 保留，归并叙述 |
| Theorem 1 closure | §3 头条 | **辅助：良构引理** | 降级、并入 Lemma |
| Theorem 2 poly-time | §3 | 辅助：良构引理 | 并入 |
| PWR 负实例 + 5 维 | §3.6 | **BOUNDARY（勇气）** | 保留、重构为 Boundary 叙事 |
| 3 域（Boltzmann/ML/relational） | §3.3–3.5 | **TRANSFER 证据** | 保留；ML/relational 压缩 |
| head-to-head vs GenMorph（n=5） | §5 | 辅助：construct-validity，**非优越性** | 降级；用 L2 解释"互补" |
| METRIC/METRIC+ 对比 | §5.5 | 辅助：定位 | 保留、压缩 |
| 12-PUT / 5-MP 旧目录 | S2 corpus | 辅助：被替代的归纳基线 | 引为对照 |
| DeepCrime n=5 / Apache n=3 pilot | §5 | 辅助：underpowered，诚实标注 | 降为附录 |
| 版本史 / process notes / response letters | archive/ | **CUT**（不进正文） | 不动，留档 |

**"其他皆辅助"的精确化**：辅助分两类 ——
(a) **载重辅助**（不可删）：Well-formedness Lemma（挡"你的过程不良构"攻击）、
PWR 负实例（提供可证伪性）、3 域（提供迁移性）。
(b) **装饰辅助**（可压缩/下放）：优越性叙事、underpowered pilot、METRIC 细节、版本史。

---

## 5. 目标章节结构（map 到现 tex：keep / promote / demote / add / cut）

```
§1 Introduction
   - keep：origin/closure/transferability gap + Noether 类比
   - REWRITE L256：删 "systematisation rather than deduction"；改为 derivation-force 表述
   - REWRITE Boundary box：把 "establishes closure" 降为 lemma；把三条 law 升为 establishes
§2 Related work — keep，压缩
§3 The NOETHER framework（CORE）
   §3.1 preliminaries + 8-block — keep（修 Step3/4）
   §3.2 CONSTRUCT-MP — keep
   §3.3 Well-formedness Lemma（= 旧 Thm1+Thm2，DEMOTE 合并）
   §3.4 [ADD] Invariance-Blindness Theorem（招1，新核心定理 + 证明草图）
   §3.5 Boundary：PWR 负实例 + 5 维（PROMOTE 为"边界定理候选"叙事）
§4 Instantiations（TRANSFER，压缩）
   Boltzmann（keep）/ equivariant ML（压缩）/ relational（压缩）
§5 Empirical force of the derivation（PROMOTE 为重心）
   §5.1 L1 Block-occupancy law：home-field 9 SUT + 旧 L\*-blindness（PRIMARY）
   §5.2 L2 Invariance-blindness：paired MR-vs-differential（PRIMARY，实证招1）
   §5.3 L3 Detectability floor：微分 oracle δ + 敏感度（PRIMARY）
   §5.4 [DEMOTE] case study / METRIC / pilots → construct-validity + 附录
§6 Threats & limitations — keep；underpowered 诚实留此
§7 Conclusion — REWRITE：核心 = derivation-with-force，三条 law + 一条边界定理
Appendices：proofs（含招1 证明）、out-of-scope、S10 复现
```

---

## 6. 审稿攻击 → 防御映射

| 预期攻击 | 防御（用哪份材料） |
|---|---|
| "Thm1 平凡 by-construction" | 承认并降为 Lemma；**招1 新定理**承担非平凡性 |
| "只是 systematisation" | L256 重写；L1/L2/L3 是**可证伪预测**，非整理 |
| "n=5 欠功效，结论不可信" | 撤优越性叙事；论点由**跨 9 SUT 结构律 + paired McNemar**（非单点率）承担 |
| "shared-corpus LLM 循环自证" | L1/L3 由**纯 numpy 自包含 SUT（无 LLM、无 T2）**产出（heat/wave/poisson）；招1 由中立微分 oracle 确认，不依赖 LLM 语料 |
| "Thm1′ 自证伪 = 框架坏了" | 重构为 Boundary：边界被**代数刻画为 5 维**，附反驳条件 |
| "8-block 是你拼凑的" | Hypothesis 1 显式经验假设 + 6 类 out-of-scope；L1 跨 9 SUT 零例外是其**可证伪确认** |

**关键防御资产**：heat/wave/poisson 三个**自包含、无 LLM、无 T2 依赖**的 SUT —— 它们
让 L1/L3 的证据**独立于"shared-corpus"质疑**，是回应评审 Blocker #4 的硬通货。

---

## 7. 诚实 × 进攻 的边界（操作定义）

- **进攻**（鼓励）：thesis、定理陈述、law 的预测、"我们邀请攻击"。
- **诚实**（硬约束）：每个数字标 n + CI；underpowered 标注不删（C6）；by-construction
  照认；reused-committed vs executed-here 区分；self-consistent 故障漏检照报。
- **红线**：不得用小样本率"假装"强结论（HARKing）；强结论只能由**跨域定性结构律 +
  形式化定理**承担。即：**point estimate 弱没关系，structural law 必须硬。**

---

## 8. 落地动作清单（agent 可起草 vs 需作者判断）+ 优先级

| 优先 | 动作 | 谁 | 阻塞项 |
|---|---|---|---|
| P0 | 招1 Invariance-Blindness 的精确陈述 + 证明草图 | **作者**（agent 起草命题形式） | fault 沿轨道的形式化 [需作者数学判断] |
| P0 | 修 CONSTRUCT-MP Step3/4 歧义（A/B/C） | **作者**选 + agent 落文本 | 每 block ∼_s 等价类数 [需作者数学判断] |
| P1 | §1 L256 + Boundary box 重写（降 Thm1、升 law） | agent 起草 | 作者 review 语气 |
| P1 | §5 重组为"derivation force"三小节（L1/L2/L3） | agent | S10 数据已就绪 |
| P2 | head-to-head 优越性叙事 → 互补（用 L2 解释） | agent | — |
| P2 | PWR 负实例重构为 Boundary 定理候选 | agent 起草 | 5 维独立性形式证明（部分 [需作者]） |
| P3 | L1 扩到 radxfer/grayscott 双实现（招1 推广，需真跑微分 oracle） | agent | 运行时（可做） |
| P3 | 独立人类 κ（回应 shared-corpus Blocker） | **作者** + 第二评分者 | 人力（protocol_humanKappa.md） |

**建议执行序**：P0（作者数学判断两项）→ P1（agent 重写 §1 + §5）→ P2（降优越性、
重构边界）→ P3（扩实验 + κ）。**P0 不决，P1 之后的正文重写不应动笔**（避免重写后又
因定理形式变更返工）。

---

## 9. 不做 / 待决（需作者拍板）

1. **招1 是否立为正式定理**？这是把论文从"systematisation（防御）"翻为"constructive
   theory with a limiting theorem（进攻）"的枢纽。立 → 需作者完成形式化；不立 → 退回
   选项 II re-grounding（protocol_theory §3.3），进攻性受限。**[需作者决定]**
2. **投稿目标**：TOSEM（要非平凡定理 → 必须招1）vs IST/TSE（systematisation 可接受）。
3. **是否扩 N≥30** 让 paired McNemar 自身达显著（现 p=1.0 因 b/c 接近 + 样本小）；
   或维持"定性互补 + 跨域律"为主、McNemar 仅作完整性。
4. 本 plan 仅规划；**正文重写需另一轮明确授权**（改动大、半不可逆）。
