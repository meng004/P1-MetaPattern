# NOETHER 投稿成熟度更新评估（证据约束版）

> 日期：2026-06-18  
> 评估对象：`NOETHER_paper_arxiv.tex` 最新提交后状态  
> 目标期刊：ACM TOSEM  
> 结论口径：所有结论均绑定证据编号；无证据则不作强结论。

## 0. 结论

**投稿成熟度：Major revision before submission。量化成熟度：71/100。**

该稿已具备明确的 TOSEM 潜力：理论问题重要，贡献边界比上一轮更诚实，参考文献真实性审计通过，且昨日最高优先级的 ISS-7 记号冲突已在最新稿件中修复为 `G_{\mathrm{tr}}` translation sub-class 表述（E7, E8, E17）。但当前仍不建议直接投稿 TOSEM：初投稿模板不符合 ACM journals 的单栏 `manuscript` 要求（E1, E5），PDF 仍为 77 页且存在冗余/排版警告（E10, E11），实证证据仍是“小样本、理论优先、非平均优越”的形态（E8, E9, E12），artifact/Zenodo 仍未到可公开复核状态（E14, E15），且今天无法在不外传未发表全文的情况下重新跑 full gateway panel（E18）。

## 1. 证据登记表

| ID | 证据 | 来源 |
|---|---|---|
| E1 | ACM journals 要求接受稿件使用 ACM authoring template；初投稿 LaTeX 应使用 Primary Article Template 2.16（2025-08-28）和 `\documentclass[manuscript]{acmart}` 单栏格式。 | ACM Author Gateway, “Submitting Articles to ACM Journals”, accessed 2026-06-18: https://authors.acm.org/journals/submission-process |
| E2 | ACM journals 页面说明 ACM journals 发表高质量 peer-reviewed computing research，且 ACM 作为 COPE 成员强调 plagiarism、falsification 等零容忍。 | ACM Journals overview, accessed 2026-06-18: https://authors.acm.org/journals/overview |
| E3 | ACM TAPS workflow 要求源文件可被 TAPS 处理；常见错误包括缺失图、非法包、模板错误等。 | ACM TAPS workflow, accessed 2026-06-18: https://authors.acm.org/proceedings/production-information/taps-production-workflow |
| E4 | ACM submission page 要求 CCS Concepts/keywords；ACM reference format 对超过一页文章必需。 | ACM Author Gateway, lines on CCS/reference format: https://authors.acm.org/journals/submission-process |
| E5 | 当前稿件使用 `\documentclass[acmsmall, screen]{acmart}`，并标记 `\acmJournal{TOSEM}`。 | `NOETHER_paper_arxiv.tex`:10-12 |
| E6 | 当前稿件已有 CCSXML、`\ccsdesc`、`\keywords`。 | `NOETHER_paper_arxiv.tex`:132-156 |
| E7 | 贡献边界明确声明：不建立 arbitrary-property absolute completeness、不主张平均优越、不消除 induction。 | `NOETHER_paper_arxiv.tex`:257-275 |
| E8 | 最新稿件已将 translation per-block 结果表述为 `G_{\mathrm{tr}}`，并明确 Set N 在 D1 aggregate 上被 Set G 支配。 | `NOETHER_paper_arxiv.tex`:1696-1703, 1767-1818 |
| E9 | 稿件明确承认 $n=70$ across 10 SUTs underpowered，且 Set G 只做 single seed，multi-seed follow-up。 | `NOETHER_paper_arxiv.tex`:2128-2138 |
| E10 | 最新编译日志显示 PDF 77 页。 | `NOETHER_paper_arxiv.log`:2192 |
| E11 | 编译日志仍有 ACM reference format mandatory、possible images without descriptions、字体替换、overfull/underfull 等警告。 | `NOETHER_paper_arxiv.log`:1751-2159 |
| E12 | Threats 中承认 Set N 的 30 MRs 由单作者推导，LLM kappa 不能等同独立人类专家一致性，Path A subject reimplementation 由同一作者完成。 | `NOETHER_paper_arxiv.tex`:2608-2618 |
| E13 | Invariance-Blindness empirical evidence 有更强量化支撑：三 SUT、104 real mutants，union 89/104，paired McNemar p=3.85e-5。 | `NOETHER_paper_arxiv.tex`:2568-2593 |
| E14 | Review-stage artifact 计划是 anonymised supplementary archive；acceptance-stage 才 Zenodo DOI。 | `NOETHER_paper_arxiv.tex`:2631-2644 |
| E15 | Data Availability Statement 仍写 repository 和 Zenodo DOI to be added in camera-ready。 | `NOETHER_paper_arxiv.tex`:2900-2912 |
| E16 | 参考文献真实性校验：58 条，53 条完全匹配，5 条小差异，0 条虚构/严重不符，hard-block 解除。 | `docs/review_2026-06-17/reference_verification_2026-06-17.md` |
| E17 | 2026-06-17 五模型网关 panel 原始结果：1 Reject + 4 Major Revision；平均 soundness 2.4、novelty 3.2、significance 2.8、presentation 2.4、reproducibility 2.6。 | `docs/review_2026-06-17/llm_panel/*.json`; synthesized in `docs/review_2026-06-17/submission_maturity_assessment_2026-06-17.md` |
| E18 | 2026-06-18 full gateway rerun在沙箱内 5/5 APIConnectionError；非沙箱 rerun 被权限审查拒绝，原因是会把完整未发表稿件发送到外部 LLM gateway。 | `docs/review_2026-06-18/llm_panel/_panel_summary.json`; tool denial log |
| E19 | 集成的 IBT 文件仍含 3 个 `% TODO-ref` 与顶部“cross-refs to be resolved”注释。 | `theory/ibt_section_3_4.tex`:6,124,127,164 |

## 2. 评分

| 维度 | 分数 | 判定 | 证据 |
|---|---:|---|---|
| 理论原创性与学术价值 | 80 | 强理论型贡献；origin/closure/transferability 问题有清晰定位，IBT 是最有发表价值的核心。 | E7, E13, E17 |
| 技术 soundness | 74 | 无已证实 publication blocker；ISS-7 已修，但 Theorem 2/CONSTRUCT-MP 的算法实质仍会被追问。 | E7, E8, E17 |
| 实证充分性 | 60 | 能支持“理论一致/可实例化”，不足以支持平均效用优越；作者已有诚实降级。 | E8, E9, E12, E13 |
| 目标期刊 fit | 70 | TOSEM fit 成立，但更像 theory + rigorous artifact paper，不应包装成 broad empirical superiority。 | E2, E7-E13 |
| 投稿模板与形式成熟度 | 54 | 当前 arXiv/production 风格不满足 ACM 初投稿单栏 `manuscript` 要求；PDF 仍长。 | E1, E3-E6, E10, E11 |
| 可复现性与 artifact | 68 | 目录内 artifact 丰富，但投稿可审查包、匿名 hash、永久 DOI 尚未完成。 | E14, E15 |
| 引文/事实完整性 | 86 | 参考文献 hard-block 已解除；剩余是少量元数据润色级问题。 | E16 |
| Reviewer 风险 | 62 | 存档五模型 panel 仍是 1 Reject + 4 Major；ISS-7 修复会降低 blocker 风险，但没有新的 external panel 证据确认。 | E17, E18 |

**综合分：71/100。**  
解释：这是“可进入 TOSEM 大修轨道”的分数，不是“可直接投”的分数。若完成模板切换、压缩、artifact 包、TODO-ref 清理、multi-seed/LLM-human validation 或更强限制性措辞，预期可提升到 78-82。

## 3. Reviewer Panel 复核

2026-06-17 已保存的真实网关 panel 使用 5 个模型：`gpt-5`、`claude-opus-4-6`、`deepseek-r1`、`glm-5.2`、`kimi-k2-instruct`。原始裁决是：

| 模型 | 裁决 | soundness | novelty | significance | presentation | reproducibility | blocker/major/minor |
|---|---|---:|---:|---:|---:|---:|---:|
| gpt-5 | Reject | 2 | 3 | 2 | 2 | 2 | 3/5/5 |
| claude-opus-4-6 | Major Revision | 3 | 3 | 3 | 2 | 3 | 2/6/9 |
| deepseek-r1 | Major Revision | 2 | 3 | 3 | 4 | 3 | 2/2/2 |
| glm-5.2 | Major Revision | 3 | 4 | 3 | 2 | 3 | 2/5/7 |
| kimi-k2-instruct | Major Revision | 2 | 3 | 3 | 2 | 2 | 1/1/4 |

这组 panel 的核心负面项中，最高优先的“`T*`/translation/idempotence 记号冲突”已经被最新稿件实质修复：translation 行现在标为 `G_{\mathrm{tr}}`，per-block 表也把 translation 作为 `G` 的 sub-class，而非自相矛盾地归入 `T*` 或 `\mathcal{T}*`（E8）。因此，**不应继续把 ISS-7 作为当前 blocker**。但是，今天无法重新把完整未发表稿件发送到外部 gateway 获得新 panel 确认（E18），所以该降级判断只是“本地证据支持”，不是“新多模型 panel 共识”。

## 4. 对照目标期刊与作者指南

**不合规或未成熟项：**

1. 初投稿格式：ACM journals 当前要求 review submission 用单栏 `manuscript` 格式；稿件仍是 `acmsmall, screen`（E1, E5）。这是投稿前必须修的形式项。
2. 长度：77 页对 TOSEM 理论长文不是绝对不可投，但对 reviewer 负担明显偏高；昨日 panel presentation 均值仅 2.4/5，与长度/重复问题一致（E10, E17）。
3. TAPS/可访问性：日志提示 image description、ACM reference format、字体替换等问题；这些不一定阻断初审，但会在 production/TAPS 前变成硬性整理项（E3, E11）。
4. Artifact：当前承诺 review-stage anonymised archive 和 acceptance-stage DOI，但正文仍是“to be added in camera-ready”。TOSEM 审稿人会要求 review-time 可访问匿名 artifact，而不是只承诺 acceptance release（E14, E15）。

**已满足或接近满足项：**

1. CCS Concepts 和 keywords 已具备（E4, E6）。
2. 参考文献真实性已通过 hard-block（E16）。
3. COPE/科研诚信角度，稿件对 limitation、负结果、aggregate dominated by GenMorph 等不利证据有明示披露，优于“只报正结果”的稿件（E2, E7-E9, E12）。

## 5. 投稿前必须完成的修订

1. **切换投稿模板**：生成 TOSEM review submission 版本，使用 `\documentclass[manuscript]{acmart}`；保留 `\acmJournal{TOSEM}`、CCS、keywords、ACM reference format。
2. **压缩主文**：目标先从 77 页压到约 45-55 页；把重复 Boundary box、worked examples、per-MR provenance、过长 threat 细节迁到 supplement。
3. **清理 IBT TODO-ref**：`theory/ibt_section_3_4.tex` 的 3 个 `% TODO-ref` 不能进入投稿版。
4. **artifact 包审查化**：准备匿名 archive、SHA-256、README、run instructions；正文不要只写 DOI camera-ready 后补。
5. **实证措辞继续收紧**：摘要和 C4 中保持“theory-first / structural transferability / not average superiority”；不要把 home-field 多块 gain 或 cost-axis advantage 写成 broad empirical superiority。
6. **补强 Reviewer-2 杠杆点**：最优先是 LLM 判等/second-rater 的 human validation 小样本混淆矩阵，以及 GenMorph multi-seed sensitivity。若无法补实验，必须把这些明示为 resubmission/follow-up limitation，而非支撑性证据。

## 6. 最终裁决

**不建议今天直接投 TOSEM。建议完成一轮 major revision 后投稿。**

当前稿件的学术水平不是“低”，而是“强理论稿件但投稿成熟度不够均衡”：理论贡献和诚实边界已经有 TOSEM 讨论资格，参考文献真实性没有硬伤；主要风险集中在 presentation/template、empirical framing、review-time artifact、以及 reviewer 对算法实质和小样本证据的信任。ISS-7 修复后，已知 blocker 风险显著下降；但在没有新 external full panel 的情况下，最保守、事实求是的裁决仍是 **Major revision before submission**。
