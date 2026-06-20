# SACOS 工业实例缺口诊断（2026-06-20）

> 触发：用户质疑"有了 SACOS 等工业实例，为何还需补实验？真实缺口在哪？"
> 方法：3-agent workflow（事实核查 + 对抗验证 + 缺口/最小实验）`wf_ebb3549a-4d2`，全部基于论文原文行号。

## 1. SACOS 的三重不足（均为论文自承）

| 维度 | 事实 | 论文出处 |
|---|---|---|
| **来源非中立** | SACOS/SPARK/LOCUST 属作者所在核工业生态，非独立第三方；论文把整个 reactor 侧定性为 "the authors' own catalogue, not an external corpus ... internal vocabulary coherence, not external transfer" | L692 |
| **只覆盖 1/6 块** | 110 条 expert MR **全部**落在 order 块 O_le（单调）；其余 5 块（G/T\*/L\*/E\*/Conservation）在 expert-industrial 与 NOETHER-industrial 两列均为 0 | L2775(i), L2777, 覆盖表 L1121-1126 |
| **subsumption 非可执行** | 工业侧是"110 条 expert MR 能否被 O_le 归类"的分析；非-order 块只在纸面从方程 derive，从未在 SACOS 上可执行验证（自承 future work） | L2775(i), L2777, L2790 |

## 2. 核心结论：缺口是证据的"自指性"，不是证据的量

reviewer（R2/R3/EIC）的硬墙不是"SACOS 不够多"，而是**每条验证腿都是 author-vs-author、每个 block 标签都是作者/LLM 标的**。SACOS 再多也只把 O_le 那一格做厚，填不上独立性。对抗验证判定 `sacos-insufficient`，且击败"SACOS 已足够"的证据正是论文自己写下的诚实段落（L692/L2771/L2775）——作者无法在 rebuttal 里绕过自己的自陈。R2 原话封死该路径："honest disclosure of a weakness does not convert it into evidence."

NOETHER 的核心卖点是"覆盖 expert 系统性漏掉的 5 块"——而这 5 块在工业代码上**既无 expert MR 对照、又无可执行验证**，故 SACOS 恰恰证不到最关键的差异化主张。

## 3. 真实缺口（4 条，全部无法用现有数据填）

| # | 缺口 | SACOS 为何填不上 | 最小实验 | 成本 |
|---|---|---|---|---|
| ① | **独立人类 κ**（block-label 信度）| SACOS 语料无"独立人类对 block 归属"的标注；现 κ=0.931 是 LLM-多数 vs 作者自标 | 2 名独立 rater 盲标 ~40-50 条 MR（SACOS 110 + Set N 30 抽样）的 block，算 Cohen κ。**纯标注、无需跑代码** | 最低（半天-1 天）|
| ② | **多块外部可执行验证** | SACOS 只 1 块；其余 5 块只在作者自选的 numpy 上跑过 | SACOS 上 1 个非-order 块可执行验证（L2790 已 committed 未跑），或中立外部库多块 | 中 |
| ③ | **独立重实现 Path-A** | SACOS 非 Path-A subject，解不开"设计者=实现者"耦合（L2771）| 1 名独立工程师按 Sun 2021 prose 重实现 1 个 Java subject，重跑 head-to-head | 中-高 |
| ④ | **中立 real-bug** | SACOS 无真实 bug ground truth；现稿是作者自造 mutation（每块一类，L2771）| 真实 bug（e3nn/PyG）上验 NOETHER MR | 高 |

## 4. 最小路径（关键：比想象小）

满足 3 个非 DA reviewer 的硬墙，**不必四条全做**。最小组合：

> **① 独立人类 κ（纯标注，最高 ROI、3 reviewer 都点名）＋ 一条非自指验证腿（②/③/④ 任选一条，破"验证腿自指"）**

用户已选 ③ real-bug + 独立重实现；加上 ① 独立人类 κ，即构成最小硬墙组合。

## 5. 写作能填的部分（让 R1 达 minor，但不够 R2/R3/EIC）

把 EQ1 明确 reframe 为 **definitional/structural** 覆盖主张（不声称 evidential），SACOS 限定为"O_le 单块 in-domain breadth"。这是 R1 路径（仅 writing 可达 minor）；但 R2/R3/EIC 的独立性硬墙仍需 ①＋一条腿。
