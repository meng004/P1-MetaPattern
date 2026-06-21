# NOETHER 投 TOSEM 成熟度量化考核 — 设计者×执行者×合成者（2026-06-21）

> **架构（非两个 skill 各跑一遍）**
> - **设计者** = `academic-paper-reviewer` skill：Phase 0 field-analysis 配置 5 角色（EIC + R1 理论/统计 + R2 MT/MR 领域 + R3 等变ML/安全关键 + Devil's Advocate）+ `quality_rubrics.md` 5 维加权量规 + `editorial_decision_standards.md` 决策矩阵 → 定制考卷 `task_design_personas_rubric.md`。
> - **执行者** = LLM 网关 5 模型独立冷读全文应考：`grok-4.3` · `gpt-5.5` · `claude-opus-4-7` · `qwen3-max` · `glm-5.1`（`scripts/tosem_maturity_panel.py`，网关 `https://llm-api.net`，密钥取自 `.env` 未暴露）。
> - **合成者** = 编排方（Phase 2 editorial_synthesizer + 项目 §10 ARS）：本文件。
> - 评估对象：`NOETHER_paper_arxiv.tex`（branch `codex-tosem-maturity-review-2026-06-20`，~88.6K token，82pp）。
> - 原始产物：`docs/review_2026-06-21/gateway_panel/{grok-4.3,gpt-5.5,claude-opus-4-7,qwen3-max,glm-5.1}.{md,json}` + `_panel_summary.json`。

---

## 0. 一句话结论（去偏三模型综合，primary）

**当前成熟度：Major Revision before submission（去偏三模型一致 3/3）；量化成熟度中位 58/100（均值 59.3，区间 [52,68]，SD 6.6）；原样投出接收概率中位 ≈25%。** 较 06-20 轮（52–55/100, ~22%）微升，与已落地的 A 阶段修复（Theorem 2 改名、工业整合、A6 文献）一致；但**四个结构性缺口未动**，且三模型冷读把它们逐条用 `fixable_by` 标签钉死。

> **首要裁决采用去偏三模型**（用户 2026-06-21 指示：gpt-5.5 存在偏见）。为对称去偏，同时剔除两端离群点——harsh 端 `gpt-5.5`（Reject/37，用户判定有偏）与 lenient 端 `claude-opus-4-7`（Minor/74，且与合成方同属 Claude 家族应回避），保留三家厂商各异、且全部落 Major 的中间三模型 `grok-4.3 / qwen3-max / glm-5.1`。中心估计与 5 模型中位（58）几乎不动——离群双端相互抵消，验证 Major≈58/25% 对去离群稳健。完整 5 模型数据见 §1（透明对照）。

### 0′. 去偏三模型记分卡（primary verdict）

| 模型 | 裁决 | 成熟度 | 接收概率 | DA CRITICAL |
|---|---|---:|---:|:--:|
| glm-5.1 | Major | 52 | 25% | — |
| grok-4.3 | Major | 58 | 22% | ✅ |
| qwen3-max | Major | 68 | 35% | — |
| **综合** | **Major Revision（一致 3/3）** | **中位 58 / 均 59.3 / SD 6.6 / [52,68]** | **中位 25% / 均 27.3** | **1/3** |

per-persona：EIC 3 Major · R1 3 Major · R2 3 Major · R3 2 Major+1 Minor。维度均分（3 模型）：Originality 73.7 · Coherence 70.0 · Writing 62.7 · Methodology 58.3 · **Evidence 52.3（最弱=硬墙）**。blocker fixable_by：writing 2 / experiment 2；major weakness：writing 6 / experiment 7 / either 1——**写作可修与实验硬墙仍约各半**，§4 ROI 结论不变。

---

## 1. 量化记分卡（全 5 执行模型 — 透明对照，含被去偏剔除的两端离群点）

| 模型 | 裁决 | 成熟度(报告) | 成熟度(按量规重算) | 接收概率 | DA CRITICAL | conf |
|---|---|---:|---:|---:|:--:|:--:|
| **gpt-5.5** | **Reject** | 37 | 37.3 | 6% | ✅ | 4 |
| glm-5.1 | Major | 52 | 51.5 | 25% | — | 4 |
| grok-4.3 | Major | 58 | 59.9 | 22% | ✅ | 4 |
| qwen3-max | Major | 68 | 75.5 | 35% | — | 4 |
| **claude-opus-4-7** | **Minor** | 74 | 73.2 | 70% | — | 5 |
| **汇总** | **Major** | **中位 58 / 均 57.8 / SD 12.9 / [37,74]** | 均 59.5 | **中位 25% / 均 31.6** | **2/5** | — |

**裁决分布**：1 Reject · 3 Major · 1 Minor → 决策矩阵落 **Major Revision**。
**DA 铁律**：2/5 模型（gpt-5.5、grok-4.3）判定 CRITICAL（curation↔validation 循环 + scope-engineering 排除目标域真正关心的 MR）→ 编辑裁决**不可为 Accept**（5 模型无一 Accept，自洽）。

### 维度均分（0-100，权重）

| 维度 (权重) | 均分 | 区间 | 读判 |
|---|---:|---|---|
| Originality (.20) | 70.8 | [58,85] | **最强项**：算子代数构造层 + IBT + 负完备证伪是真 delta |
| Methodology rigor (.25) | 56.4 | [37,70] | Theorem 1 by-construction、Theorem 2 措辞、欠功效统计拖累 |
| Evidence sufficiency (.25) | 52.2 | [34,70] | **最弱（硬墙）**：自指评估 + LLM-only κ + 构造控制 mutation |
| Argument coherence (.15) | 64.2 | [31,80] | 主线被次要材料淹没；over-claim 与自承之间张力 |
| Writing & presentation (.15) | 57.0 | [22,85] | 篇幅失控（gpt 给 22）；分歧最大维 |

---

## 2. 差距分析（distance to thresholds）

量规决策映射：≥80 Accept ｜ 65–79 Minor ｜ 50–64 Major ｜ <50 Reject。

| 目标 | 阈值 | 现状(中位58) | 缺口 | 谁已达 | 能否仅靠写作达成 |
|---|---|---|---|---|---|
| 可送审（脱离 desk-reject） | 过 LEN-01 + 格式 | 3/5 判篇幅为 blocker | 篇幅 82pp ≫ ~11k 词软上限 | — | **能（写作）** |
| Minor Revision | ≥65 | 2/5 已达(qwen68/opus74) | 低端 3 模型缺 +8~12pp | qwen, opus | **部分**（写作可推 glm/grok 上 65；gpt 不行） |
| Accept 轨道 | ≥80 | max 74 | 全员缺，最优也差 6pp | 无 | **不能（需实验硬墙）** |

**两条硬墙（experiment-fixable，作者执行，我做不到）**——5/5 模型一致：
1. **独立人类 inter-rater κ**：现 κ 是 LLM-多数 vs 作者自标（共享训练语料）；全员要求 ≥2 名独立人类盲标。
2. **一条独立/外部验证腿**：EQ1/EQ3 不能全 author-vs-author。可选 (a) 外部 reactor MR corpus（PARCS/IAEA，非作者）；(b) 真 bug 评测（e3nn/PyG，协议已写未跑）；(c) 中性（非按块构造）mutation × ≥2 架构。

---

## 3. 理由：为什么是 Major、为什么分歧这么大

### 3.1 共识缺口（被≥4/5 模型独立点名 → 不可辩驳）

| # | 缺口 | 谁点名 | fixable_by | 理由 |
|---|---|---|---|---|
| G1 | **Theorem 1 by-construction 被当 headline** | 5/5 | writing | MR(A_P) 定义为 Translate-image，Theorem 1 证"每个 Translate-可达 MR 都被分类"= 良构性，非完备性。降为 lemma，IBT + Theorem 1′ 证伪上位。 |
| G2 | **Theorem 2 "polynomial-time" 过强** | 5/5 | writing | |G| 可指数（(Z₂)ᵏ→2ᵏ）→ output/group-size 多项式非 input 多项式。须在**定理陈述本体**加 finite-generator 限定。 |
| G3 | **评估自指** | 5/5 | experiment(κ+外腿) / writing(诚实框定) | 块从同一 reactor 语料 curation 后又用它"验证 prediction"；LLM-only κ；construct-controlled mutation。 |
| G4 | **上游块归纳而非公理推导** | 4/5 | writing | "induction relocated, not eliminated" 应做**主characterization**而非脚注 caveat。 |
| G5 | **篇幅/结构失控** | 4/5（3 判 blocker） | writing | 82pp ≈ TOSEM 软上限 ~3×；LEN-01 触发 return-without-review；4 个重复 boundary box。 |
| G6 | **统计欠严谨** | 4/5 | writing(校正)/experiment(功效) | 无多重比较校正（Bonferroni/Holm）；欠功效 pilot 报 p/CI；pooled 混 D1/D2 忽略 within-subject 相关。 |
| G7 | **novelty over-claim / 未尖锐交锋最近邻** | 4/5 | writing | 收紧为"constructive operator-block layer + closure/complexity within Translate scope"；与 Gotlieb/Segura/Zhou/Khritankov 正面对照。 |
| G8 | **GenMorph head-to-head 落败被重框** | 3/5 | writing(直说)/experiment(修G块) | Set N 在 D1 被 Set G 压制（McNemar p=0.019）；"complementarity/cost-axis"易被读作逃避。 |

### 3.2 分歧的根因（最重要发现）= **如何对待 self-disclosure**

成熟度从 37(gpt) 到 74(opus) 跨 37 分，SD 12.9。分裂轴**不是**对事实的认定（5 模型对 G1–G8 的事实判断高度一致），而是**对论文"已自承缺陷"是否免责**：

- **宽松端**（opus-4-7 Minor/74、qwen Major/68）：采信论文诚实自披露循环性/欠功效 → 当作"已知限制 + roadmap"，DA 不判 CRITICAL。
- **严苛端**（gpt-5.5 Reject/37、grok-4.3 Major+CRITICAL/58）：**拒绝让 self-disclosure 充当 mitigation**——"honest disclosure does not convert a weakness into evidence"（gpt）、"self-disclosure used as a shield"（grok）→ 判 CRITICAL。

**这复刻了 06-20 轮的核心洞察并强化之**：真实 TOSEM 审稿人行为更接近**严苛冷读端**。因此提接收率的真功夫不止"修可复现硬伤"，而在**重构叙事让冷读者也无法 Reject** + **补一条独立证据腿把自指洗掉**。把希望寄托在"我都自承了"上 = 把命运交给抽到 opus 型而非 gpt 型审稿人，期望值 ≈ 25%。

---

## 4. 最具 ROI 的任务（按"单位工作量增益 × 风险 × 可执行性"排序）

聚合 5 模型 `highest_roi_fixes`（21 条）后分两档。blocker fixable_by 计数：writing=4 / experiment=4 / either=1；major weakness：writing=14 / experiment=12 / either=3——**约一半写作可修（我能做），一半实验硬墙（作者做）**。

### 档 A — 写作可修（我现在就能做，零科学风险，应无条件先做）

| 排名 | 任务 | 聚合增益 | 工作量 | 依据 |
|:--:|---|---:|---|---|
| **A1 🥇** | **Theorem 1 降为 well-formedness lemma；IBT + Theorem 1′ 证伪上位为理论 headline** | +8pp | **低** | **5/5 共识 + 最佳增益/工作量比**；glm/gpt 各列 +8 |
| **A2 🥇** | **篇幅压缩到 ≤~40-45pp / ≤15k 词**（删 3 重复 boundary box、合并跨域节、PWR 阐述砍半、二级表入 supplement） | +8~12pp | 中-高 | 移除**唯一硬 desk-reject 触发器**（LEN-01）；glm+12/gpt+12/grok+8 |
| A3 | **收紧 novelty + 与最近邻文献尖锐对照**（"operator-block 构造层 + closure/complexity，限定 Translate scope"） | +12pp(grok) | 中 | 4/5；正中 R2 "overstated" |
| A4 | **统计卫生**：Bonferroni/Holm 校正 + 欠功效 pilot p 值降为 descriptive | +8pp(qwen) | **低** | 4/5；低成本高确定 |
| A5 | **Theorem 2 改名 + finite-generator 限定写进陈述本体** | +4~7pp | **低** | 5/5；qwen+7/glm+4 |
| A6 | **诚实框定**：GenMorph 落败直说（不暗示 superiority）+ "induction relocated" 作主characterization | — | 低-中 | 3-4/5；防 §6.4 visibility-laundering |
| A7 | **合规/artifact 一致性**：清双盲↔作者实名矛盾、SSOT S1-S12 manifest、GenAI 披露、acmsmall,review | +5pp | 中 | gpt B5 + 06-20 B7 |

> **档 A 净效果（诚实估计）**：中位 58 → ~68-70，清空全部 writing-class blocker + 过 LEN-01。可让 glm/grok/qwen/opus 落 Minor，但 **gpt 型冷读仍 Major/Reject**——因 G3 自指是 experiment 硬墙，写作触不到。**写作天花板 ≈ 跨 Minor 但非全员、非 Accept 轨道。**

### 档 B — 实验硬墙（作者执行；天花板最高、是真正的 binding constraint）

| 排名 | 任务 | 聚合增益 | 工作量 | 状态 |
|:--:|---|---:|---|---|
| **B1 🏆最高天花板** | **一条独立/外部验证腿**（外部 MR corpus 非作者 / 真 bug e3nn-PyG / 中性 mutation×≥2 架构） | +10~18pp | 高 | grok+18/gpt+15/qwen+12/glm+10；**seed12/13 confirmatory 已 prereg(`f2a5980`)、云任务已就绪** |
| B2 | **独立人类 inter-rater κ**（替换 LLM-only κ） | +6~15pp | 中 | 5/5；**κ codebook 已起草**（`mvp_kappa_codebook.md`），需 2 名非作者 rater |

> 档 B 是把接收概率从 ~25% 推过 ~45-55% 的**唯一**路径，也是让 gpt/grok 型冷读不再 Reject 的唯一办法。两件执行物均已在 NEXT_STEPS 搭好脚手架，缺的是算力/云主机 + 2 名独立 rater（作者侧资源）。

---

## 5. 建议执行序（最大化期望接收概率/单位投入）

1. **立刻做 A1 + A5 + A4**（全低工作量、5/5 或 4/5 共识、合计 ~+16~19pp、零风险）——半天到一天。
2. **再做 A2 压缩 + A3 novelty + A6 框定 + A7 合规**（中工作量、清空写作 blocker、过 LEN-01）——~1-2 周。做完写作天花板触顶（~68-70，多数模型 Minor）。
3. **B1 + B2 实验腿**（作者 gating 决策）：这是把 gpt/grok 型冷读从 Reject/CRITICAL 拉过线、把接收概率推过 45% 的 binding constraint。prereg + κ codebook 已就绪，只待资源到位即可云端执行。

**ROI 一句话**：*A1（Theorem 1 降格，低成本+8pp+5/5 共识）是单项 ROI 之王，必须最先做；但 B1（独立外部验证腿）是天花板的唯一钥匙——写作能让你"可送审 + 抽到宽松审稿人时 Minor"，只有 B1+B2 能让你"抽到严苛审稿人时也不被 Reject"。*

---

## 6. Reviewer 2 视角（项目 §10 ARS 必跑）

5 模型冷读 + 2 个 DA CRITICAL 已构成最严苛 Reviewer-2 扫描，致命三条：
1. **curation↔validation 循环 + scope-engineering**（gpt/grok CRITICAL）：块从 reactor 语料归纳后又用它证 prediction；Translate 故意排除目标域真正在测的 MR（非加性、混合二阶导）。→ 需 B1 外部腿，非脚注 disclaim。
2. **核心定理 by-construction**（5/5）：headline 理论主张其实是定义闭包。→ A1。
3. **主证据自指 + 欠功效**（5/5）：EQ1 二元块覆盖把质量/可执行/新颖压成 0/1；κ 为 LLM-only。→ A4/A6（写作）+ B1/B2（硬墙）。

无新增 publication blocker 超出上述 G1–G8 范围。

---

*执行者：网关 5 模型（grok-4.3/gpt-5.5/claude-opus-4-7/qwen3-max/glm-5.1）独立冷读。设计者：academic-paper-reviewer skill。原始数据见 `gateway_panel/`。grok-4.3 原始 JSON 有单个多余闭合括号已精准修复（不改任何评分/内容），详见恢复记录。*
