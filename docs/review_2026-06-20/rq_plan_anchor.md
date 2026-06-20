# NOETHER 研究问题计划锚点（反主题漂移基准）

> 用途：修订—审稿闭环中，**每一轮修订后**逐条对照本锚点，确认无主题漂移。
> 来源：`NOETHER_paper_arxiv.tex` Abstract（L123-133）、Introduction（L165-285）。
> 建立日期：2026-06-20。本锚点是论文当前真实主张的固化，**不是新设计**——修订不得偏离它，若需改动锚点本身须显式标注并说明理由。

---

## 1. 核心 Objective（论文要回答的问题）

> "whether a structured, operator-algebraic method can derive a **broader and more explainable** MR class / MetaPattern design space than expert MR sets and search-based MR generation, by making the **algebraic origin and applicability boundary** of MRs explicit from program-family governing equations."（Abstract L126）

**定位（不可漂移的硬约束）**：本文研究 **MR identification**，**不研究** MR fault-revealing effectiveness（Abstract L126、Scope L265）。任何把论文重新包装成"故障检测优越性"的修订都是主题漂移。

## 2. 三个基础问题 — origin–closure–transferability gap（Intro L174-180）

- **RQ-Origin**：为什么是这些 MetaPattern 而非其他？MP 的结构源（区别于语料里的经验规律）是什么？
- **RQ-Closure**：在什么数学条件下，已发现的 MP set 在给定推导算子（`Translate`）下**闭合**（不漏掉算子可达的 pattern）？绝对完备是更强的要求，一般情形仍 open。
- **RQ-Transferability**：程序族改变时 MP set 如何变化？能否**不重跑**整套经验归纳即得到新集合？

## 3. 三个评估问题 EQ1–EQ3（Abstract L130 + C5 L262）

- **EQ1**：expert MR sets vs NOETHER 的 **binary operator-block coverage**。
- **EQ2**：NOETHER vs search-based MR generation 在 **origin / boundary / redundancy / readability / maintenance** 五维比较。
- **EQ3**：**cross-domain derivation traces**——同一 operator block 跨程序族/求解器解释 MR class。
- **二级证据（非主张）**：mutation / head-to-head / DeepCrime —— 仅作 secondary executability & sanity-check，**不**作平均故障检测优越性证据（C5 L262、Scope L280(c)）。

## 4. 贡献结构 C1–C5（L253-263）

- **C1**：NOETHER 两层框架（upstream 经验 + downstream 算法）。
- **C2a（正向理论）**：Theorem 1 — no-drop closure invariant（**intentionally modest**，well-formedness，非故障检测优越）；Theorem 2 — 有限生成集下 poly-time 可判定。
- **C2b（负向理论）**：Theorem 1′（绝对完备猜想）在 𝒜_PWR 上**被证伪**（两反例 + 五结构障碍）。
- **C2c（极限理论）**：Invariance-Blindness Theorem（IBT）—— G/T\* 块的检测核 = 结构保持故障（faithfulness-tight，线性故障类内）。
- **C3**：在真实程序族上**系统化/再分类**先验目录（再现 3、refine 2、去重 2）；非 de novo 发现。
- **C4**：算法骨架层的 **structural transferability**（**非**跨域经验优越），三结构相异域实例化。
- **C5**：MR identification 证据协议（EQ1-EQ3）。

## 5. Scope（in / out，L265-283）

| in scope | out of scope |
|---|---|
| MR identification（derive 结构化 MR class） | MR effectiveness（平均故障检测率/mutation score/优越性） |
| downstream 层算法化+可证 | upstream 层（仍经验+人工，未消除归纳） |
| Translate 下的 closure（C2a） | 任意属性的绝对完备（C2b 已证伪） |
| 三域 structural transferability（骨架层） | 跨域经验优越性 |

---

## 6. 每轮反漂移 checklist（修订后逐条核对）

- [ ] **D1 定位不变**：论文仍是 MR identification 论文，未被改写成 fault-detection effectiveness 论文。
- [ ] **D2 RQ 不变**：仍回答 origin–closure–transferability gap；未新增 RQ 之外的主张，未删回答 EQ1-EQ3 必需的证据。
- [ ] **D3 headline 一致**：理论 headline（C2a→C2c 调整）仍在 closure RQ 内（IBT=closure 盲点刻画，Thm1′=closure 边界），非新主题。
- [ ] **D4 二级证据未上位**：mutation/head-to-head/DeepCrime 未被改写为主张性优越证据；GenMorph 败局（McNemar p=0.0043）未被隐藏或粉饰。
- [ ] **D5 scope 边界完整**：四条 "does not establish"（L276-283）与 IBT/Thm1′ scope 限定未在压缩中丢失。
- [ ] **D6 数字诚实**：effect size / κ / p / n 逐字来自数据源；underpowered 标注（§6.9）保留。
- [ ] **D7 无新术语**：未引入原文不存在的数字前缀术语（§4.2）或新概念。

> 任一项不通过 → 该轮修订有漂移，回退并仅保留 RQ 内的改动。
