# NOETHER — 投稿成熟度量化考核 + 中科院大类1区期刊定位（2026-06-21）

> 评估对象：`NOETHER_paper_arxiv.tex`（branch `codex-tosem-maturity-review-2026-06-20`，~80pp，75 refs）
> 新证据：`S5_aligned_experiment` 的 seed12/seed13 预注册 confirmatory（commit `4bc9698`，2026-06-21 完成）
> 方法：单条整合流水线（**非** academic-paper-reviewer / academic-pipeline 各跑一遍）——
> 出题人(rubric) → reviewer 角色(agent fleet 冷读双审 + 仓库内真实网关 5 厂商裁决三角印证) → 执行者(论文) → deep-research 期刊定位。
> 说明：本环境未挂外部 LLM 网关，`academic-paper-reviewer`/`academic-pipeline` 两 skill 亦未安装；其**功能**由上述 agent 编排 + 既有 `docs/` 网关产物复用实现。

---

## 0. 一句话结论

**当前成熟度（artifact-aware 双审均值）≈ 66/100；冷读 TOSEM 审稿人地板 ≈ 52–55/100；TOSEM 接收门槛 ≈ 78。**
最适合的中科院**大类1区**期刊是 **ACM TOSEM**（SE 领域大类1区仅 TOSEM 与 TSE，本文方法学/理论体裁明确归 TOSEM）。
**最高 ROI 杠杆是把我刚跑完的 seed12/seed13 预注册实验写进 §6.6**——数据已就绪、零新研究，一次性抬升 evaluation_rigor + reproducibility + honesty 三维；这是双审独立给出的共识 #1 lever。

---

## 1. 量化记分卡（9 维加权，0–10）

| 维度 | 权重 | RevA 理论/AE | RevB 实证/ARS | 旧网关 06-16 量化均值 | 合并 | 状态 |
|---|---|---|---|---|---|---|
| format_compliance | 0.05 | 8 | 8 | 8.8 | 8.3 | ✅ |
| honesty_threats | 0.10 | 9 | 8 | 7.8 | 8.3 | ✅（最强项之一）|
| scope_fit | 0.05 | 8 | 8 | 7.6 | 7.9 | ✅ |
| novelty | 0.15 | 8 | 7 | 7.4 | 7.5 | ✅ |
| technical_soundness | 0.20 | 7 | 6 | 6.8 | 6.6 | ◐ |
| reproducibility | 0.10 | 6 | 5 | 6.8 | 5.9 | ◐ |
| **evaluation_rigor** | **0.20** | 6 | 5 | 4.6 | **5.2** | 🔴（权重最高，最痛）|
| presentation_length | 0.05 | 3 | 6 | 4.4 | 4.5 | 🔴 |
| related_work | 0.10 | 8 | 8 | 3.6 | 6.5 | ◐（较 06-16 大幅回升）|

**合并加权成熟度 ≈ 65.9/100。** RevA 70.5 · RevB 64.5 · 旧网关量化均值 62 · 旧网关冷读(06-20) 52–55。
**裁决一致：Major Revision（双审 conf 4/5）。** 距门槛 ≈ 12 分（artifact-aware）/ ≈ 25 分（冷读）。

> **冷读 vs artifact-aware 的 ~13 分裂口本身是最大风险**（06-20 已记录）：真实 TOSEM 审稿人更像冷读网关（3 Reject），看到"按定义成立的定理 + 输掉的 head-to-head + 全链路自评"不会因作者自我声明就放过。提分的真功夫在**让冷读者也无法 Reject**，而非仅补可复现硬伤。

---

## 2. 双审 + 网关共识 blocker（已 grep 对抗验证）

| # | Blocker | 严重度 | 类型 | 验证 |
|---|---|---|---|---|
| **B-NEW** | **seed12/seed13 预注册多 seed confirmatory 不在论文里**——论文 §6.6 仍是旧 `seed=11` 单 seed + routeB gcd/sin；新 23-subject、substrate-locked、cluster-bootstrap+Wilcoxon 数据只在 S5 repo | 🔴 blocker | **纯文本（数据已就绪）** | ✅ grep 证实：`seed12/seed13/cluster-bootstrap/Wilcoxon` 对 .tex 零命中 |
| G1 | head-to-head 聚合败局：Set N 被 Set G 主导（旧 p=0.0043；新 seed12/13 p=0.0018/0.0007 复现），Math 被 robustly 压制（b=56 vs c=8）；主结果靠 per-block/cost-axis/D2 切片承接 | 🔴 | 部分需研究 | ✅ 新数据复现，未翻盘 |
| G5 | κ=0.931/0.857 全部来自 **LLM 评分团**（DeepSeek/ChatGPT/Claude），作者自承不能等同独立 human inter-rater；human κ 仅 committed | 🔴 | **需真做（≥2 名独立人类 rater）** | ✅ L2629 |
| 自评混淆 | Path-A 四个 Java subject 由框架作者本人重实现（L2629）；case study 5/5 是 construct-validity-controlled；5 个 block 是 hand-crafted probe（自承非独立证据）→ 真正独立的 fault-detection 证据很薄 | 🟠 | 需研究（第三方实现/中立 mutation）| ✅ L2629/L1287/L1957 |
| G3 | 理论核 load-bearing 偏弱：Thm 1 closure = by-construction 近同义反复（L603 自承）；最强 Thm 1′（绝对完备）**被自证伪**；真正非平凡的 IBT 局限于 {G,T*}、线性故障、τ→0 | 🟠 | 文本可缓（IBT 领头重构）| ✅ |
| B2 | 篇幅 ~80pp ≫ TOSEM 30–50pp / ~11k 词软上限；4 个重复 boundary-box、remark 叠 remark | 🟠 | 文本（大工作量）| ✅ L267/660/1833/2707 |
| B6 | 与最近邻文献（Gotlieb Symmetric Testing 2003/06、Khritankov 2024、Gruver 2023、Kaba-Ravanbakhsh 2023、MemoRIA/MUT 2024）未尖锐交锋 | 🟠 | 文本 | ✅ |
| B1/B3/B4/B5/B7 | 可复现 P0 簇：Set L 覆盖 0.40 vs SSOT 0.20（3处）、两条 artifact 路径不存在、κ n 漂移、Theorem 2 "poly-time" 措辞过强、TOSEM 格式/GenAI 披露/双盲残留 | 🟠 | **纯文本/数据，半天可清** | 06-20 已定位 |
| Salami(T2) | 与 NP-hard minimum-MR-subset 姊妹稿 venue-overlap | 🟢 已缓解 | — | L330–344 已显式划界、cover letter 披露 |

> **被对抗验证推翻/降级**（保护作者勿返工）：RevA 称"IBT \input 未 wire in"——实际 L665 `\input{theory/ibt_section_3_4}` 已挂载（仅 compile-audit 待核，降为 minor）。06-20 另有 9/17 误读已推翻（Thm 1 已自承 by-construction、GenMorph 已重定位为互补、EGNN 已自承 construct-validity 等）。

---

## 3. Deep-research：中科院大类1区期刊定位

| 期刊 | 中科院大类 | 小类(软件工程) | TOP | IF/JCR | 大类1区? |
|---|---|---|---|---|---|
| **ACM TOSEM** | 计算机科学 **1区** | 1区 | 是 | 6.2/Q1 | ✅ **推荐** |
| IEEE TSE | 计算机科学 **1区** | 1区 | 是 | 5.6/Q1 | ✅（次优）|
| EMSE | 工程3区 | 2区 | — | 3.5/Q2 | ❌ |
| IST / JSS | 计算机 **2区** | 2区 | — | 3.8 / 3.7 | ❌（大类2区回退）|

> 中科院分区**已官方停更**，上表为最新一版口径。SE 领域真正大类1区**仅 TOSEM 与 TSE**。

**推荐 ACM TOSEM，理由（双审独立同口径）：**
1. **体裁契合**——本文重心是 method/foundations（算子代数构造性推导 + closure/IBT 两定理 + PWR 负实例），经验明确从属（abstract/§1/§6 反复声明 "secondary executability checks, not fault-detection superiority"）。TOSEM 长期接纳"框架+形式保证+适度经验"的方法学论文（METRIC/METRIC+ 即出 TOSEM 谱系），且论文 L12 `\acmJournal{TOSEM}` 即原始 target。
2. **价值命题与 venue 取向匹配**——本文显式**不主张**故障检测优越（seed12/13 已确认聚合败、Math 被压制）。TSE 评审更强调 head-to-head 击败 SOTA，聚合败局在 TSE 会被放大为致命弱点；TOSEM 容许"identification ≠ effectiveness"的范围切割。
3. **理论形状契合**——IBT 不可能性 + 构造性闭包 + 可证伪负实例，是 TOSEM 偏好的贡献形态。

**回退**：若大类1区补差后仍不可达，现实回退为大类2区 IST/JSS（本就有 IST 就绪线）。

---

## 4. 差距 → 修复方案（分级）

**P0 文本/数据（半天–2 天，立即可执行，移除 desk-reject 触发）**
- 集成 seed12/13 进 §6.6（B-NEW）；Set L 0.40→0.20 + 删假 "reaches L\*"（B1）；修两条 artifact 路径（B3）；正文以 human Cohen κ 领头、调和 n（B4）；Theorem 2 加 output-polynomial 限定句（B5）；切 `acmsmall,review` + 补 GenAI 披露 + 清双盲残留（B7）。

**P1 文本（2 天–2 周，最大单项天花板）**
- 压至 ≤45–50pp：L\*/IBT 电池、DeepCrime pilot、METRIC+ 对决、LLM-κ 各降 1 表入附录；EQ1–EQ3 提为独立主证据节；合并 4 个 boundary-box（B2，+8–12pp 天花板）。
- IBT 领头重构理论层级，closure 显式降格为 well-formedness lemma（G3）。
- 补并尖锐交锋最近邻文献，delta 收紧为 "construction+proof over the layer" 而非 "发明抽象层"（B6）。

**P2 需真实研究（1–2 周+，拆冷读硬伤）**
- ≥2 名独立**人类** rater 做 block 标注 Cohen/Fleiss κ（G5）——construct validity 的根。
- Path-A 四 subject 第三方独立重实现 / 换中立 mutation 源（自评混淆）——seed12/13 的中立 substrate 已部分替代，但人评腿仍需人。

---

## 5. 最高 ROI 任务排序（增益/工作量）

| 排序 | 任务 | 工作量 | 类型 | 预估增益 | 备注 |
|---|---|---|---|---|---|
| **T1** | **可复现 P0 簇**（B1/B3/B4/B5/B7）| ~0.5 天 | 文本/数据 | **+5–8pp** | 最便宜，"近 desk-reject"→"可送审" |
| **T2** | **集成 seed12/13 进 §6.6**（B-NEW）| 1–2 天 | 文本（数据已就绪）| **+3–4pp** | 数据已花成本跑完；一举抬 rigor+reproducibility+honesty；**单位成本最高** |
| **T3** | 压篇幅 ≤45–50pp + IBT 领头重构 + 合并 boundary-box（B2/G3）| 1–2 周 | 文本 | +8–12pp（最大天花板）| 工作量大但纯文本 |
| **T4** | 最近邻文献尖锐交锋 + scope-novelty 收紧（B6）| 2–4 天 | 文本 | +4–6pp | — |
| **T5** | 独立**人类** κ（≥2 rater）（G5）| 1–2 周 | **研究** | +2–4pp | 拆冷读 blocker，construct validity 根 |
| **T6** | Path-A 第三方重实现 / 中立 mutation（自评混淆）| 数周 | 研究 | +2–4pp | seed12/13 已部分替代 |

**轨迹估计**：T1+T2（≈3 天，全部数据已就绪）→ 66 → ~70，且把已花成本的数据变现；叠加 T3+T4（文本，~3–4 周）→ ~76–78，逼近门槛；T5+T6（研究）→ 越过门槛并抵御冷读 Reject。
**硬结论**：T1+T2+T3+T4 全为文本/已有数据，**无需新实验**即可把 artifact-aware 成熟度推到门槛附近——这正是 Major 而非 Reject 的依据；但要让**冷读** TOSEM 审稿人也无法 Reject，T5（人类 κ）与 G1 的诚实重构是不可绕过的最后一公里。

---

*评估者：出题人 rubric（9 维加权，TOSEM 口径）+ 双 agent 冷读审稿（理论/AE 70.5 · 实证/ARS 64.5，均 Major/conf4）+ 仓库内真实网关 5 厂商裁决（3 Reject + 2 Major）三角印证 + deep-research 期刊定位（多源核证）。原始：`docs/review_2026-06-20/llm_panel/`、`docs/tosem_maturity_2026-06-16/gateway_quant_raw.json`、本文件。*
