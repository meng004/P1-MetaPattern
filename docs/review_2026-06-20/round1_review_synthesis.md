# 第 1 轮基线审稿综合（2026-06-20）

> 方法：5 个互相隔离的独立 reviewer（EIC + 3 peer + DA）冷读当前稿（含 A14/A6/ca3f333 修复）。
> 判据（用户设定）：除 DA 外 4 个 reviewer 全部 minor revision 才可投稿。
> 原始数据：workflow `wf_7e1d144f-32b`。

## 1. 裁决汇总

| Reviewer | Verdict | 达 minor 是否需新实验 |
|---|---|---|
| EIC | **major revision** | 部分（P0 identification payoff = either；construct-validity = experiment） |
| R1 形式方法/理论 | **major revision**（近 minor 边界） | **否**——"None of these requires new experiments" |
| R2 实证/可复现 | **major revision** | **是（硬墙）**——"cannot exceed major regardless of writing quality" without external-corpus + human-rater data |
| R3 MT/MR 领域 | **major revision** | **是（硬墙）**——需 external/independent validation leg |
| DA（不计入门槛） | major revision | 是 |

**当前 4 个非 DA reviewer 全是 major。距"4 minor"目标差距大，且部分是真实验硬墙。**

## 2. 维度均分（非 DA 4 人粗汇）

| 维度 | 分 | 趋势 |
|---|---|---|
| Novelty / 概念贡献 | ~7.5–8 | 最强项，A6 后站得住 |
| Honesty / 诚信 | ~9 | 全员盛赞，须保持 |
| Theory（IBT + 1′ 证伪） | ~6.5–7.5 | 真 delta，但 headline 错配（Theorem 1/2 被高估） |
| Scope-venue fit | ~7 | identification 定位可辩护，但"effectiveness 退避"易被读作逃避 |
| **Evaluation rigor** | **~4–4.5** | **最弱，硬墙所在** |
| **Presentation** | **~3–4** | **全员要求压缩到 ~40–45 页** |

## 3. 硬墙 vs 写作可解（决定性分类）

### 🔴 硬墙（fixable_by = experiment，我做不到，需作者执行；3 个非 DA reviewer 要求）
- **独立人类 inter-rater κ**（block-label 信度）：现 κ=0.931 是 LLM-多数 vs 作者自标，非独立人类。R2/R3/EIC 都要求 ≥2 名独立人类 rater 盲标一组 MR。
- **至少一条独立/外部验证腿**：R2/R3 要求 EQ1/EQ3 不能全是 author-vs-author——需 (a) 外部团队 reactor MR corpus（非作者自有），或 (b) 独立重实现 Path-A subjects，或 (c) 中立 real-bug 证据（e3nn/PyG 协议已写未跑）。
- **identification payoff 具体化**（EIC P0，either 但倾向需实测）：auditability/maintainability/reuse 的可测优势，或 end-to-end cost 量化——否则 GenMorph 落败下"为何用 NOETHER"无答案。

> R2 原话："honest disclosure of a weakness does not convert it into evidence... the paper cannot exceed major revision regardless of writing quality, because the core empirical claims remain self-referential."

### 🟢 写作可解（fixable_by = writing，我能做；做完可让 R1 达 minor + 清掉全员 writing 类 blocking）
1. **A9 压缩到 ~40–45 页**（全员 P1，presentation 3–4 分）：L\* battery 精简但核心留主文、二级表/DeepCrime/METRIC+ 详节入 supplement、合并 4 个 boundary box、清"committed-as-follow-up"协议堆。
2. **理论 headline 重定位**（EIC/R1/R3）：Theorem 1 显式降为 well-formedness lemma；IBT + Theorem 1′ 证伪 carry 理论主张；Abstract/contributions 重新加权。
3. **Theorem 2 改名**（R1）：从 "Decidability" → "Complexity of CONSTRUCT-MP (under finite generating set + per-block extraction oracle)"。
4. **EQ1 reframe**（EIC/R2/R3）：明确标为 definitional/structural 主张，非 evidential 比较（或换一个可能不利的比较）。
5. **平衡 contributions**（R3）：非循环结果（PMCM over-count、Murphy-2008 Case A-bis、IBT）carry novelty；循环的 m_adj/m_rev "prediction" 从 headline 降为 systematisation note。
6. **title "discovery" → "systematisation/identification"**（R1）：消题文不符。
7. **"ten dimensions" 去 headline 或补证明**（R1，either）：5 proved + 5 conjectured 全文一致，不可读作 10 proved。
8. **Zhou2020 引用核查**（R3）：symmetry-MRP 归属是否与 TSE2020 标题混淆。
9. **预注册完整性**（DA P2）：L\*-blindness outlier rule 的事后写入须如实说明。

## 4. 关键结论

- **仅靠写作不可能达到"4 reviewer minor"**。写作上限 ≈ R1 达 minor + 其余 reviewer 的 writing 类 blocking 清空，但 R2/R3/EIC 的 experiment 硬墙仍在 → 仍 major。
- **达 4-minor 的唯一路径 = 全部写作修复 + 作者补实验**（至少：独立人类 κ + 一条外部/独立验证腿）。
- 写作修复无论走哪条路都该做（对任何 venue 都有益、且让论文显著更强）。实验是作者决策（需招人类 rater / 跑外部 corpus / 重实现 subjects）。

## 5. 下一步建议

1. 我继续推进**全部写作修复**（第 2 轮：A9 压缩 + headline 重定位 + EQ1 reframe + Theorem 2 改名 + 平衡 contributions + title + Zhou cite），把论文推到 writing 上限。
2. 我同时准备**实验协议 + 脚手架**（独立人类 κ 评分表/盲标协议；外部 corpus 对照模板；real-bug 协议已在 S5）。
3. 作者决策是否执行实验——这是能否达成"4 minor"的 gating 决定。
