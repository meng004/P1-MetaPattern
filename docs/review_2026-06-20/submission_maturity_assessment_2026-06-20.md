# NOETHER 投 TOSEM 成熟度评估 — 多厂商网关 + 多智能体复评（2026-06-20）

> 评估对象：`NOETHER_paper_arxiv.tex`（branch `main`，commit `02d8aee` 后工作树；本会话已含两处 relabel 修复，见 §10）
> 目标期刊：ACM Transactions on Software Engineering and Methodology (TOSEM)
> 标题：*NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras*
> 体量：80 页（pdfinfo 确认），acmart `manuscript` 单栏，~33–37k 词正文，21 表 / 1 图 / 77 处 S1–S12 指针
> 说明：网关使用 `.env` 的 `BASE_URL`/`API_KEY`，密钥未记录、未暴露。本文件取代同目录 workflow 子智能体中间稿 `_workflow_eic_draft.md`（后者基于 4/5 模型、未含对抗验证与精确 blocker）。

---

## 0. 一句话结论

**当前投稿成熟度：Major Revision before submission；量化成熟度 ≈ 52–55/100；如今日原样投出，预计 desk-reject 或 reproducibility-reject 概率高（接收概率 ~22%）。清完 P0+P1 后可升至 45–55%。**

理论内核（IBT + 绝对完备性证伪 + 构造性闭包）真实、且形状契合 TOSEM；拖垮成熟度的是 **篇幅/结构、可复现完整性缺陷、与最近邻文献未交锋**，几乎全部"无需新科学即可修"。

---

## 1. 评估方法与证据边界

本轮是**首次对当前 TOSEM 重写稿完成 fresh 外部多厂商复审**（06-18 那轮因执行环境拒绝外发未发表稿而未跑通；本轮用户明确授权、密钥在 `.env`，已真实跑通）。两条独立证据链：

| 证据链 | 构成 | 角色 |
|---|---|---|
| **网关 5 厂商 LLM 评审团** | gpt-5.5 · claude-opus-4-7（opus-4-8 三次 429 限流，按授权回退）· glm-5.2 · deepseek-v4-pro · qwen3-max；各读 91K-token 全文，独立结构化评审 | 模拟**冷读外部审稿人**（无仓库访问） |
| **Claude 30-agent Workflow** | 侦察 → 4 角度深度研究（paper-search）→ 5 维独立评审 → 17 项 blocker/major **对抗验证** → TOSEM 合规审计 → EIC 量化合成 | 模拟**有 artifact 访问 + 自我证伪**的尽责审稿人 |

原始产物：`docs/review_2026-06-20/llm_panel/*.json`（网关）、`docs/review_2026-06-20/workflow_result.json`（Claude）、`panel_run.log`。

---

## 2. 总量化记分卡

| 维度 | 网关均值(×20→0-100) | Claude EIC(0-100) | 合并判读 | 主因 |
|---|---:|---:|---:|---|
| Soundness | 44 | 62 | ~50 | 理论真实但 Theorem 1 by-construction、Theorem 2 poly-time 措辞过强 |
| Novelty | 64 | 68 | ~65（最高） | IBT+负完备+闭包是真 delta；但 meta-pattern 层/对称性框架本身不新 |
| Significance | 52 | 50 | ~51 | 实证多为 protocol/欠功效；GenMorph 对决被压制 |
| Reproducibility | 48 | 58 | ~52 | Set L 数据矛盾、缺 artifact、κ 误报 |
| Presentation | 40 | 38 | **~39（最低）** | 80 页、21 表、4 boundary box、主线被次要证据淹没 |
| **加权总分** | — | **55/100** | **≈ 52–55** | — |

网关五维均值（满分 5）：soundness 2.2 / novelty 3.2 / significance 2.6 / presentation 2.0 / reproducibility 2.4。两条链独立得到**同一形状**：presentation 最差、novelty 最强、其余 borderline。

---

## 3. 多 reviewer 裁决

### 3.1 网关 5 厂商（冷读，3 Reject + 2 Major）

| 模型 | 裁决 | conf | sound/novel/signif/present/reprod | 头条致命点 |
|---|---|---|---|---|
| **gpt-5.5** | **Reject** | 5 | 1/2/2/1/1 | Theorem 1 同义反复；Theorem 2 不可判定；八块自相矛盾(7/8/Conservation)；实证非验证 |
| **deepseek-v4-pro** | **Reject** | 4 | 2/3/2/2/2 | EQ1 工业列仅单块 O≤，"更广设计空间"被自证据反驳；GenMorph 压制 |
| **claude-opus-4-7** | **Reject** | 4 | 2/3/2/2/3 | 净贡献仅 IBT+L\*-blindness+PWR 负结果+同义反复定理，不撑 TOSEM 长文 |
| qwen3-max | Major Revision | 5 | 3/4/4/3/3 | 欠功效 pilot 报 p 值/CI；IBT 线性-精确算术假设 vs 浮点实证 |
| glm-5.2 | Major Revision | 4 | 3/4/3/2/3 | 全链路自评（自导 MR/自重实现/LLM-only κ）；篇幅 |

> opus-4-8 三次 429（"上游负载饱和"），按用户授权回退 opus-4-7 成功。

### 3.2 Claude EIC 综合裁决

**Major Revision · 55/100 · 接收概率 22%（清完 P0/P1→45-55%）**。比网关温和，因对抗验证推翻 9/17 误读、并采信论文自界定。**分歧本身是最重要的发现（见 §9）。**

---

## 4. 学术水平评估（深度研究 / paper-search，4 角度）

| 角度 | venue-fit | 真正新颖 | 不新颖 / 已有先例 |
|---|---:|---|---|
| MT meta-patterns / MR 分类 | 4/5 | 算子代数**构造性推导** + 闭包/可判定 | "meta-pattern 抽象层"框架：Ying 2025(STVR)、Segura 2019、Zhou 2020、Murphy 2008、Khritankov-Iakusheva 2024 已有 |
| oracle 问题 / 对称性框架 | 4/5 | origin-closure-transferability + IBT 不可能性 | 对称性 oracle：**Gotlieb Symmetric Testing (ISSRE 2003/2006)**、Patel-Hierons 2018 已命名 |
| MR 质量度量 / 选择 / 最小化 | 3/5 | （此角度非强项） | AutoMR 2019、MemoRIA 2024、MUT 2024、Qiu 2022 MR-composition 已覆盖 |
| 等变 ML / 不变性测试 | 4/5 | IBT（检测核=结构保持故障的 commutant）无 MT 先例 | 等变实例本身增量；Gruver 2023、Kaba-Ravanbakhsh 2023、Saha-Kanewala 2019 未引 |

**结论**：净理论 delta = **IBT + 绝对完备性证伪 + 构造性闭包/可判定**，在 MT 领域无清晰先例（4 角度独立判 venue-fit 3–4）。但论文把"发明抽象层 / 对称性直觉"也当新颖点，会被最近邻文献证伪——须把 delta 收紧为"construction+proof over the layer"，而非"inventing the layer"。

---

## 5. 对抗验证：17 项 blocker/major → 仅 8 项证实为真

Claude workflow 把 5 维评审去重出的 17 项 blocker/major 逐条对照**活文件**核验，**9 项被推翻**（误读 / 论文已自界定）：

- **被推翻（保护作者，勿返工）**：Theorem 1 "致命同义反复"（论文已明写 by-construction，定位为 well-formedness）、GenMorph 输了"掩盖 effectiveness"（已重定位为 cost/coverage 互补 + 二级 sanity-check）、IBT 近循环（已被 Reachability Lemma 限定）、reactor 自目录循环（已自承 re-projection not discovery）、EGNN 玩具/构造性 5/5（已自承 construct-validity）、**time-reversal 记号"不一致"——验证为 false（本会话已修）**。
- **证实为真的 8 项 → 见 §6。**

这解释了网关（无验证）3 Reject 与 Claude（有验证）Major 的差距：约一半"致命"在对照原文后站不住。

---

## 6. 存活致命问题（8 项证实为真；其中 1 项本会话已修）

| # | 严重度 | 问题 | 位置 | 工作量 |
|---|---|---|---|---|
| B1 | **reproducibility / blocker** | **Set L 结构覆盖 0.40 vs SSOT 0.20**：`table4.json`=0.2、`analysis.py` 重算=0.20，论文 3 处写 0.40；"reaches G **and L\***"被数据反驳（Set L 实际只达 G）。已传播进投稿 tex(`manuscript_singleblind` L1073/2127、`anonymized` L1051/2144) | arxiv L1266/1277/2325 +2 投稿文件 | 低 ~30min |
| B2 | **presentation / blocker** | **80 页 ≈ TOSEM 软上限(~11k 词)3 倍**，LEN-01 触发"return without review"；Results 70% 篇幅是论文自称"secondary"材料，主线 EQ1-EQ3 仅占 ~7% | 全文 / Results L1084-2756 | 高 1-2 周 |
| B3 | reproducibility / major | **两处被引 artifact 路径不存在**：`S3 (lrca_audit.md)`、`S2 (18mr_audit/)`；κ=0.857 原始逐评者标注仓库中无 | L720/2767/2971/Data Avail. | 低-中 数小时 |
| B4 | reproducibility / major | **κ 误报**：正文只报 LLM-vs-LLM Fleiss=1.000（共享语料，近乎无意义），隐去 majority-vs-author **Cohen's κ=0.931**（n=36，记于 `lrca_kappa.json`）及 2 处分歧；n 漂移 33/34/35/36 | §8 L2767 | 低 1-2h |
| B5 | soundness / major | **Theorem 2 "polynomial-time" 措辞过强**：证得 O(n·maxᵢtᵢ·log n)，但有限群 tᵢ=O(\|G\|²)，\|G\| 可随生成元指数增长（(Z₂)ᵏ→2ᵏ）；是 output/group-size 多项式，非 input 多项式。术语扩散到 abstract/贡献表/conclusion | §3.3.3 + 多处 | 低 15min |
| B6 | novelty / major | **最近邻文献未引/未交锋**：Khritankov-Iakusheva 2024(CrossRef 已验)、Gotlieb Symmetric Testing 2003/2006、Patel-Hierons 2018、Gruver 2023、Kaba-Ravanbakhsh 2023、Saha-Kanewala 2019、MemoRIA 2024、MUT 2024 | Related Work §2.4 | 中 2-4 天 |
| B7 | compliance / major | **TOSEM 格式/流程**(合规 72%)：`documentclass` 缺 `acmsmall,review`；双盲/OpenReview/conference 残留语言（TOSEM 单盲）；无 GenAI 披露（ACM 政策，论文重度用 LLM）；arXiv 预印本未披露；Zenodo 非匿名 | L19/25/26/2868 等 | 低 2-3h |
| ~~B8~~ | ~~presentation / major~~ | ~~EQ1/EQ3/held-out 段引入未定义第九块 "Conservation"~~ → **本会话已修**（§3.1 L469 加定义句调和到 G 块） | — | ✅ 已修 |

> 另：EIC 单列的"过程叙事残留"（pre-register ~16 次、"committed as follow-up" 19 次、"subsequent revisions of this paper" 活文档措辞 L1357）违反终稿去过程化（§6.5 C1），并入 B2/P3 处理。

---

## 7. TOSEM 合规审计（72%）

| 项 | 状态 | 要点 |
|---|---|---|
| LEN-01 篇幅软上限 | **FAIL** | >~11k 词可 return without review（唯一硬 FAIL） |
| FMT-01 文档类 | partial | 应 `\documentclass[acmsmall,review,manuscript,screen]{acmart}` |
| FMT-03 desk-reject 触发 | partial | 超长 + 格式不完整 |
| BLIND-01 单盲 | partial | 双盲残留语言与单盲自相矛盾 |
| ETHICS-02 GenAI 披露 | partial | ACM 政策必需 |
| NOV-01 / ORIG-01 | partial | 缺 originality/not-under-consideration 声明 + arXiv 未披露 |
| REPRO-01 RCR | partial | 可选；建议补 FAIR 链接 + artifact DOI |

---

## 8. 提高接收率路线图（按 ROI 排序，预期增益为 EIC 估计）

| 优先级 | 动作 | 预期增益 | 工作量 |
|---|---|---|---|
| **P0** | B1：5 处改 0.40→0.20 + 删假 "L\*" 声明，重跑 `analysis.py` 确认 Table 4 重生 | +5-8pp | 30min |
| **P0** | B3：补/改 `lrca_audit.md`、`18mr_audit/` 至真实路径，全仓库跑 supplementary 指针存在性检查 | +3-5pp | 数小时 |
| **P0** | B4：正文补 Cohen's κ=0.931 + 2 处分歧，调和 n，**以人评 κ 领头**而非 LLM-LLM | +2-4pp | 1-2h |
| **P1** | B2：压到 ≤45 页：L\*/IBT 电池、DeepCrime pilot、METRIC+ 对决、LLM-ensemble 各降为 1 表（全表入 S9），EQ1-EQ3 提为独立主证据节，合并重复叙述 | **+8-12pp（最大单项天花板）** | 1-2 周 |
| **P1** | B6：补并**尖锐对照**最近邻文献，把 delta 定位为"construction+proof"而非"发明抽象层/对称性直觉" | +4-6pp | 2-4 天 |
| **P2** | B5：Theorem 2 加一句限定（\|G\| 可指数→output-polynomial）；abstract/intro 同步 | +1-3pp | 15min |
| **P2** | B7：切 `acmsmall,review`；清双盲残留；加 GenAI 披露；披露 arXiv | +2-3pp | 2-3h |
| **P3** | git 时间戳/SHA / 21 处 "committed as follow-up" 移到 artifact 附录/Future Work；删活文档措辞 | +1-2pp | 数小时 |

**总判读**：P0（半天内全部可清）即可把"近 desk-reject"拉回"可送审"；P0+P1（约 2-3 周）后接收概率从 ~22% 升至 ~45-55%。**没有任何一条需要补新实验**——这正是 Major 而非 Reject 的依据。

---

## 9. 关键洞察：冷读 vs 验证的分歧 = 真实风险

- **网关 5 厂商（冷读，无仓库）→ 3 Reject + 2 Major**；**Claude（有 artifact + 对抗验证）→ Major / 55 / 22%**。
- 差距全在"论文自界定能否免责"：Claude 采信"by-construction Theorem 1 已自承""GenMorph 已重定位为互补""EGNN 已自承 construct-validity"，故推翻 9/17；网关把这些当**致命**——冷读审稿人看到"按定义成立的定理 + 输掉的 head-to-head + 全链路自评"，**不会因为你自己声明了就放过**。
- **真实 TOSEM 审稿人更像网关冷读模型**。因此提接收率的真功夫不止"修可复现硬伤"，更在 **重构叙事让冷读者也无法 Reject**：
  1. 把 Theorem 1 显式降格为 well-formedness lemma（已部分做），理论 headline 让给 IBT + PWR 负结果；
  2. 把输掉的 GenMorph 对决移出 load-bearing 位置；
  3. 欠功效 pilot 全部移补充材料，正文只留 5/6 L\*-blindness 这一条干净预注册结果；
  4. 引入并交锋最近邻文献，使"scoped novelty"站得住。

---

## 10. 本会话已完成的修复（用户指派的两处 relabel）

1. **time-reversal 记号归一**：`\mathcal{T}^{*}` / `\mathcal{T}^{*}_{\mathrm{rev}}` / `\mathcal{T}_{\mathrm{rev}}^{*}` / `\mathcal{T}^*` → 统一 `\mathcal{T}^{*}_{\mathrm{rev}}`（33 处转换，最终 44 处规范，0 残留；self-adjoint `T^{*}` 与算子 `\mathcal{T}`/`\mathcal{T}_{\mathrm{seq}}` 不动）。→ 对抗验证已确认此"不一致"现为 **false**。
2. **Conservation 第九标签调和**：§3.1 L469 加一句，定义 conservation/invariance 为 G 块 m_inv 实例（Noether 对称-守恒对应），EQ1/EQ3/held-out 段不再引入未定义第九块。数值未动、em-dash=0。→ EIC 已记录"now reconciled at L469"。

> 残留报备：B2 篇幅压缩时，建议一并收紧 §2773 "Expert monotonicity bias" 段把 conservation 与 symmetry 并列称 blocks 的措辞；以及决定 EQ1 后续正文/held-out 段的"six blocks"是否改为"six coverage rows / five canonical blocks"（属论断层面，需作者拍板）。

---

*评估者：网关 5 厂商 LLM 评审团 + Claude 30-agent 对抗验证 Workflow + EIC 合成。原始数据见同目录 `llm_panel/`、`workflow_result.json`、`panel_run.log`；workflow 中间稿见 `_workflow_eic_draft.md`。*
