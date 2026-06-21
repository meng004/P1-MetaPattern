# NOETHER — 两维深审（evaluation_rigor + presentation_length）+ 修复方案（2026-06-21）

> 对象：`NOETHER_paper_arxiv.tex`（codex 分支，post-T2/B5，commit `9beff90`）
> 方法：真实 5 厂商网关评审（`scripts/llm_reviewer_panel.py`，`.env` 网关，密钥仅本地 gitignored、未提交）
> 聚焦：得分最低 × 接收率影响最大的 2 维 = **evaluation_rigor**（权重 0.20）与 **presentation_length**（desk-reject 硬闸）
> 原始产物：`docs/review_2026-06-21/llm_panel_2dim/{grok-4.3,gpt-5.5,claude-opus-4-7,qwen3-max,glm-5.1}.{md,json}`

---

## 1. 真实 5 厂商裁决（当前论文）

模型：grok-4.3 / gpt-5.5 / claude-opus-4-7 / qwen3-max / glm-5.1。

| 模型 | 裁决 | significance（≈评估）| presentation（篇幅）| soundness | reproducibility |
|---|---|---|---|---|---|
| grok-4.3 | Major | 3 | 4 | 3 | 4 |
| gpt-5.5 | **Reject** | 2 | **1** | 1 | 2 |
| claude-opus-4-7 | Major | 4 | 4 | 4 | 4 |
| qwen3-max | Major | 4 | 3 | 4 | 4 |
| glm-5.1 | Major | 2 | **2** | 3 | 4 |
| **均值/5** | **4 Major + 1 Reject** | **3.0 → 6.0/10** | **2.8 → 5.6/10** | 3.0 | 3.6 |

**对比 2026-06-20 panel（3 Reject + 2 Major；significance 3.0、presentation 2.4）**：裁决改善（related work + 人类导向 κ + GenAI 披露 + T2 已见效），presentation 微升 2.4→2.8，但**两维仍是全 panel 最弱**，presentation 出现最大分裂（冷读 gpt=1/glm=2 仍判 desk-reject；artifact 友好 opus/grok=4）。

## 2. 两维综合评估（共识根因，逐字取自本轮 panel）

### evaluation_rigor / significance（3.0，相对 06-20 纹丝不动）
- **gpt-5.5**：「empirical evidence is **not a valid test** of the main claims, heavily **contaminated by constructed tasks, author-designed subjects, post-hoc** inter-rater agreement」
- **qwen3-max**：「underpowered pilots (**n=20** §5.2, **n=5** §5.2.1) and **hand-constructed mutation sets designed to validate specific blocks**」
- **glm-5.1**：「**n=20 hand-constructed mutations** on a single 5,189-parameter model, mutations **explicitly designed to cover one defect category per non-empty block**」
- **grok-4.3**：「L\*-blindness presented as 'central empirical claim' yet the pilot (**n=5**) and the Java head-to-head…」

→ 诊断：seed12/13（T2）抬升了**方法学严谨**（预注册、多 seed、中立 substrate、cluster-bootstrap），但 panel 判定**实证内核**仍薄：① 构造式 mutation（按块设计=循环论证）② 自实现 subject ③ 欠功效 pilot。这三项 T2 **未触及**。

### presentation_length（2.8，最低且一票否决）
- gpt-5.5 / glm-5.1 仍把 ~80pp 判为 `LEN-01`（return without review）触发；4 个 boundary-box、主线被自称 "secondary" 的材料淹没（Results ~70% 篇幅）未改。

## 3. 差距 → 修复方案 → 理由

| 维度 | 差距(现→标) | 修复（按 ROI 排） | 类型 | 理由 |
|---|---|---|---|---|
| **evaluation_rigor** | 6.0 → 7.5 | E1 人类 κ（≥2 独立专家标 30 个 block）| **需真人** | gpt 的"post-hoc / author-designed"指控只有**独立人验证**能拆；LLM-κ 共享语料、冷读判无效 |
| | | E2 构造式 mutation 换中立缺陷集（DeepCrime/Defects4J 真缺陷，非按块设计）| **需研究** | qwen/glm/gpt 一致咬"designed per block"=循环论证；中立缺陷集才是有效检验 |
| | | E3 Path-A 4 subject 第三方独立重实现 | **需研究** | 拆"author-designed subjects"；seed12/13 中立 substrate 已部分替代 |
| | | E4 n=5/n=20 pilot 合并入单一 Sensitivity 段、撤出 summary-of-evidence | **可代做** | 守 C6；停止把欠功效当 load-bearing |
| **presentation_length** | 5.6 → 7.5 | P1 压至 ≤45–50pp（大表入附录/补充、主线提级）| **可代做（内容保全=迁移非删）** | gpt presentation=1 直接致 Reject；唯一硬 FAIL |
| | | P2 4 个 boundary-box 合 1 | 可代做 | 同一 caveat 三处重述，删冗余 |
| | | P3 IBT 领头、Theorem 1 显式降 well-formedness lemma | 可代做 | 理论 headline 错配；present+soundness 双收益 |

**核心理由**：significance 权重 0.20 是离接收线最近的内容杠杆，但其拆解项（E1/E2/E3）**全需真实研究、agent 无法代做**；presentation 权重仅 0.05 却是**冷读 Reject 的直接触发器**（gpt-5.5 因 presentation=1 判 Reject），且**纯文本可代做、ROI 最高**。**能立刻把 1 张 Reject 票翻成 Major 的最快动作是 P1 压篇幅**；要让 significance 真正过线则绕不开 E1/E2/E3。

## 4. 压篇幅 cut-list（P1 操作清单，内容保全=迁移优先于删除）

> 原则：**先迁移（全表入补充、正文留 1 摘要行），后删冗余（重复 box）**，不删任何论点。每项标当前位置、动作、估省页、风险。执行需逐项确认（flagship 投稿，§0.5 禁止自发删除）。

| # | 项 | 当前位置 | 动作 | 估省 | 风险 |
|---|---|---|---|---|---|
| C1 | per-SUT head-to-head 表 `tab:algebra-rich-pooled` | §6.6 L1863 | 全表入补充 S8，正文留 pooled 1 行 | ~1pp | 低 |
| C2 | per-block 表 `tab:per-block-headtohead` | §6.6 L1907 | 全表入补充，正文留 3 行摘要 | ~1pp | 低 |
| C3 | LLM-ensemble(Set L) 487-MR 明细 + κ 表 | §6.4/§7 | 入附录，正文留 κ=0.931 + 43.5% 两数 | ~2pp | 低 |
| C4 | DeepCrime n=5 + D2 n=5 pilot | §6.x | 合并入单一 Sensitivity 段（=E4）| ~2pp | 中 |
| C5 | 4 个 "Boundary of contribution" box | L267/660/1833/2707 | 合 1（保留 §6.6 那个；其余删冗余）| ~3pp | 中 |
| C6 | remark 叠 remark（rem:counterex/domain-out/metric-stability）| §3.x | 合并相邻 remark | ~1pp | 中 |
| C7 | 迁移附录证明明细（App C 密集证明）| App C | 留定理陈述 + 证明骨架，细节入补充 | ~4–6pp | 高（需作者核证明完整性）|

**估计**：C1–C5（低-中风险，可代做）≈ 省 9pp（80→71）；叠加 C6+C7（需作者核）≈ 至 ~55–60pp。要稳到 ≤50pp 需 C7 + 正文叙述去重（一次过 humanizer + 去 hedging 堆叠）。

## 5. 分工

- **可代做（我，待你逐项确认 cut-list）**：E4 + P1(C1–C6) + P2(C5) + P3。
- **需你侧真人/研究**：E1 人类 κ、E2 中立缺陷集、E3 第三方重实现、C7 证明迁移核对。

---

*产物：`docs/review_2026-06-21/llm_panel_2dim/`（5 厂商原始评审）+ 本文件。凭据仅存 gitignored `.env`，未提交、未回显。*
