# NOETHER TOSEM 投稿成熟度量化评估

> 日期：2026-06-20  
> 评估对象：`NOETHER_paper_arxiv.tex` / `NOETHER_paper_arxiv.pdf`  
> 目标期刊：ACM Transactions on Software Engineering and Methodology (TOSEM)  
> 方法：deep-research review mode + academic-pipeline mid-entry Stage 2.5/3 + academic-paper-reviewer full-review synthesis。网关面板使用 `.env` 中 `BASE_URL` / `API_KEY`，未记录或暴露密钥。

## 0. 执行边界

已可用的 2026-06-20 网关 panel 结果位于 `docs/review_2026-06-20/llm_panel/`：

| 模型 | 映射 reviewer 视角 | 状态 | 裁决 | 主要关注 |
|---|---|---:|---|---|
| gpt-5.5 | EIC / theory-skeptic | ok | Reject | Theorem 1/2 平凡化、taxonomy 不稳、artifact 不足 |
| deepseek-v4-pro | empirical / reproducibility | ok | Reject | 工业覆盖表解释、GenMorph head-to-head、实证支撑不足 |
| glm-5.2 | formal-methods + balanced TOSEM reviewer | ok | Major Revision | Theorem 1 tautological、自评偏倚、经验研究分散 |
| qwen3-max | domain / constructive reviewer | ok | Major Revision | underpowered pilots、IBT exact-vs-floating gap、算法细节不足 |
| claude-opus-4-8 | planned independent reviewer | failed | not available | 首次为上游 429/model_not_found；本会话重试因连接失败且外部发送整稿被安全策略拦截 |

因此，本报告不是 5/5 完整模型面板，而是 **4 个成功模型 + 1 个失败席位的投稿前成熟度综合**。Claude 缺席不改变主要结论，因为四个成功模型已经形成 Major/Reject 共识。

## 1. 目标期刊与模板对照

ACM Author Gateway 要求 ACM 期刊稿件使用 ACM authoring template，并接受 LaTeX 或 Word；LaTeX 初投稿应使用 `\documentclass[manuscript]{acmart}` 的单栏格式。ACM 同页还要求作者协助提供 figure descriptions 以满足 accessibility。ACM artifact badging 对 artifact functional 层级强调 documented、consistent、complete、exercisable；Artifacts Available 要求公共归档库有 DOI 或唯一标识符；Results Validated 需要作者之外团队获得主结果。参考：

- https://www.acm.org/publications/authors/submissions
- https://www.acm.org/publications/policies/artifact-review-badging
- https://www.acm.org/publications/authors/information-for-authors

当前稿件硬事实：

| 项目 | 当前状态 | 评价 |
|---|---|---|
| ACM class | `\documentclass[manuscript]{acmart}` | 通过 |
| Journal code / refs | `acmsmall,screen`, `ACM-Reference-Format`, `printacmref=true` | 基本通过 |
| CCS / keywords | 已有 `\ccsdesc` 与 `\keywords` | 通过 |
| Figure description | 1 个 figure，1 个 `\Description{}` | 通过 |
| PDF length | `pdfinfo` 显示 80 页 | TOSEM 送审风险高 |
| 表格密度 | 21 个 table，1 个 figure | 过载，presentation risk |
| 编译日志 | 无 fatal error；有 postal-address warnings、float/underfull warnings | 非阻塞，但投稿前应清理 |
| 匿名性 | 源码写有 “Anonymised”，但仍含作者、邮箱、funding、CRediT | 若走 double-blind 或匿名外审，当前不合格 |

## 2. 总裁决

**学术潜力：76/100。**  
NOETHER 的 operator-algebraic MR identification framing、origin/boundary/transferability 问题意识、IBT、PWR negative result 都有 TOSEM 相关性。这个 idea 不是普通 incremental work。

**当前投稿成熟度：58/100。**  
四个成功 LLM reviewer 给出 2 Reject + 2 Major Revision。Reject 不是因为题目无价值，而是因为当前稿件把“方法论 framing、形式理论、实证验证、artifact 可信度、长篇边界声明”同时推到主文里，导致 TOSEM reviewer 很容易抓住任一弱环节判 Major/Reject。

**当前建议：不要直接投 TOSEM。先做 Major Revision。**  
若现在投稿，较可能得到 desk-send 后外审 Major/Reject，或直接因 presentation / empirical sufficiency / theory framing 被强 reviewer 拉低。

## 3. 量化评分

| 维度 | 权重 | 分数/10 | 判断 |
|---|---:|---:|---|
| Journal fit | 0.05 | 8.0 | TOSEM 范围匹配：software testing、MR identification、formal+empirical SE |
| Novelty | 0.15 | 7.4 | 概念有新意，但需更公平地区分 METRIC/METRIC+/GenMorph/MR-Scout/LLM-MR |
| Technical soundness | 0.20 | 5.0 | IBT 与 negative result 强；Theorem 1/2 仍被多 reviewer 判为 by-construction / bookkeeping |
| Evaluation rigor | 0.20 | 3.8 | 最大短板：自评语料、LLM-only rater、underpowered pilots、head-to-head aggregate 落败 |
| Reproducibility | 0.10 | 5.8 | 代码和补充材料多，但 artifact hash、独立复核、完整可执行路径仍需更硬 |
| Presentation | 0.05 | 3.5 | 80 页、21 表、论点分散；强 reviewer 会先疲劳再挑刺 |
| Related work / positioning | 0.10 | 5.4 | 已补很多，但仍需 “双向能力矩阵” 而非叙述性比较 |
| Template / submission compliance | 0.05 | 8.2 | ACM 格式大体过关；匿名性与 postal warnings 需按投稿系统处理 |
| Honesty / threat disclosure | 0.10 | 8.0 | 边界披露很诚实，但披露不能替代解决 |

**加权总分：58/100。**

门槛解释：TOSEM 可送审状态约 75/100；较稳 R&R 状态约 82/100。当前差距约 17 分。

## 4. 多 reviewer 共识问题

### P0：理论贡献包装仍会被攻击

gpt-5.5 与 glm-5.2 都把 Theorem 1 判为 near-tautological：如果 `MR(A_P)` 已定义为 Translate image，则 closure 只是在说生成物属于生成空间。Theorem 2 也容易被看成对未定义 invariant extraction black boxes 的复杂度包装。

修复方向：

1. 不再把 Theorem 1/2 作为 headline contribution。
2. 把 headline 转到 IBT、Theorem 1' falsification、operator-block taxonomy 的可证边界。
3. 若要保留 formal contribution，补一个非循环命题：例如对一个明确有限语言/代数片段，证明某类 independently defined MRs 可归约到 Translate-normal form。

### P0：实证设计仍不足以支撑 TOSEM 方法论文

四个模型都指出 empirical weakness。问题不是“没有实验”，而是实验太多、每个都带边界：作者自有 PWR catalogue、自实现 Java subjects、LLM-only second raters、n=5 pilot、n=20 constructed mutants、GenMorph aggregate D1 落败后再转为 complementarity 叙事。

修复方向：

1. 主文聚焦 2-3 个最硬结果：L*-blindness、独立 MR corpus coverage、人类/第三方 rater 复核。
2. 把 DeepCrime pilot、部分 GenMorph sensitivity、protocol-only 内容移 appendix/supplement。
3. 至少补一个独立人类复核：block assignment / orphan decision / equivalent-mutant filtering 三者任选其一，但最好覆盖前两者。

### P0：主文过载，削弱接收率

80 页和 21 张表使 reviewer 更容易把论文读成“多篇稿件拼接”。当前文本诚实披露很多边界，但边界声明过多会反过来强化“不成熟”的印象。

修复方向：

1. 主文压到 45-55 页以内。
2. 主文表格控制在 6-8 张：taxonomy、CONSTRUCT-MP summary、EQ design、expert coverage、L*-blindness、head-to-head/complementarity、artifact matrix。
3. 只保留一个 contribution-boundary box，其余并入 Threats。

### P1：artifact 与匿名投稿还有可见风险

ACM artifact badge 语义强调 documented、consistent、complete、exercisable，以及 DOI/unique identifier。当前稿中 Zenodo DOI 和 hash 叙述看起来偏“最终会报告”，reviewer 会担心可复现材料是否稳定。另一个明显问题是：稿件写着 anonymised，但作者姓名、邮箱、funding、CRediT 都在源码中。

修复方向：

1. 提供匿名 review artifact 包：固定 SHA-256、inventory、one-command reproduction、expected outputs。
2. 把 Data Availability 写成“review package currently available”，不要只写 final manuscript。
3. 若 TOSEM 系统要求双盲，生成 blind variant；若单盲，删除 “Anonymised for double-blind review” 这种自相矛盾措辞。

## 5. 接收率提升路线

| 动作 | 类型 | 预估增益 |
|---|---|---:|
| 降格 Theorem 1/2，把 IBT + falsified completeness + boundary taxonomy 作为理论主线 | 写作+理论 | +4 |
| 补独立人类 rater 或独立 corpus validation | 研究 | +6 |
| 主文压缩到 45-55 页、21 表减到 6-8 表 | 写作 | +5 |
| 将 GenMorph/DeepCrime 从“竞争性胜负”改为“secondary sanity/complementarity”，减少 kill-rate 叙事 | 写作+论证 | +3 |
| Artifact hash / anonymized package / reproduction checklist 落地 | 工程+材料 | +3 |
| Related work 做双向能力矩阵：NOETHER vs METRIC+ vs GenMorph vs MR-Scout vs LLM-MR vs specification-based MR | 写作 | +3 |

完成文本压缩和理论重定位后，成熟度可到约 66-68。再完成独立人类/独立 corpus validation 与 artifact hardening，成熟度可到约 75-78，进入“值得投、但大修概率仍高”的区间。

## 6. 结论

**当前学术水平不是低，而是“高潜力、低成熟度”。**  
它有足够的概念原创性进入 TOSEM 视野，但当前形态还没有把最强贡献压成一个 reviewer 能快速相信的核心论证。接收率的关键不在继续增加材料，而在做减法：把稿件从“全景式研究档案”改成“一个主张、三条硬证据、一个可复核 artifact”的 TOSEM 方法论文。
