# NOETHER 投稿成熟度复评（外部 LLM 网关授权重跑版）

> 日期：2026-06-18  
> 评估对象：`NOETHER_paper_arxiv.tex` 最新稿  
> 目标期刊：ACM TOSEM  
> 网关状态：用户已明确批准发送完整未发表稿件至外部 LLM 网关；本报告基于授权后的 fresh panel。

## 0. 总裁决

**投稿成熟度：Major revision before submission。量化成熟度：74/100。**

授权重跑显著改善了昨日 panel 的信号：`gpt-5` 从昨日的 **Reject** 变为 **Major Revision**；5 个 reviewer（4 个结构化 JSON + Kimi 手工解析）全部给 **Major Revision**。这说明 ISS-7 记号冲突修复后，稿件已从“可能被一名强 reviewer 直接拒稿”推进到“有明确 TOSEM 讨论资格，但仍需重大修改”的状态。

但结论仍不是“现在可投”。当前真正风险集中在五处：Theorem 1 的贡献定位仍容易被判为 near-tautological；实证部分仍不能支撑平均 fault-detection superiority；GenMorph 在 D1 aggregate 上显著支配 Set N；upstream algebra/block distillation 的可复现性不足；ACM 投稿模板、长度、artifact 和 TODO-ref 仍未达到投稿成熟状态。

## 1. 授权重跑记录

命令：

```bash
rtk .venv-noether/bin/python scripts/llm_reviewer_panel.py --manuscript NOETHER_paper_arxiv.tex --out docs/review_2026-06-18/llm_panel_rerun_approved
```

结果：4/5 结构化成功；`Kimi-K2-Instruct` 首轮 429，上游饱和。随后小写模型名单独补跑：

```bash
rtk .venv-noether/bin/python scripts/llm_reviewer_panel.py --manuscript NOETHER_paper_arxiv.tex --out docs/review_2026-06-18/llm_panel_rerun_approved_kimi_retry --models kimi-k2-instruct
```

Kimi 补跑成功，但其 JSON 因字符串转义问题未被脚本自动解析；报告正文中包含完整 fenced JSON，可手工读取。

输出位置：

- 结构化 4 模型：`docs/review_2026-06-18/llm_panel_rerun_approved/`
- Kimi retry：`docs/review_2026-06-18/llm_panel_rerun_approved_kimi_retry/`

## 2. Panel 原始裁决

| 模型 | 裁决 | conf | soundness | novelty | significance | presentation | reproducibility | raw blockers | major |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| claude-opus-4-6 | Major Revision | 4 | 2 | 3 | 2 | 2 | 3 | 2 | 6 |
| deepseek-r1 | Major Revision | 4 | 4 | 5 | 5 | 4 | 5 | 0 | 2 |
| glm-5.2 | Major Revision | 4 | 3 | 4 | 3 | 2 | 3 | 2 | 6 |
| gpt-5 | Major Revision | 4 | 3 | 4 | 3 | 3 | 2 | 0 | 7 |
| kimi-k2-instruct | Major Revision | 3 | 3 | 3 | 3 | 2 | 3 | 1 | 3 |
| **均值** | — | — | **3.0** | **3.8** | **3.2** | **2.6** | **3.2** | — | — |

对比昨日：昨日是 1 Reject + 4 Major，均值 soundness 2.4、presentation 2.4、reproducibility 2.6。今日授权重跑后为 5 Major，soundness 3.0、novelty 3.8、significance 3.2、presentation 2.6、reproducibility 3.2。**改善最大的是 soundness/reproducibility 风险，但 presentation 仍是最弱维度。**

## 3. Blocker 对抗验证

Panel raw blockers 共 5 个，但不宜机械等同于真实 publication blocker。逐条核验如下。

| Raw blocker | 来源 | 核验结论 | 处理 |
|---|---|---|---|
| Theorem 1 near-tautological，closure over framework-defined space | Claude | **真实问题，但非 soundness fatal。** 稿件已承认 by-construction scope；问题在贡献架构仍把 Theorem 1 放得太重。 | Major-fixable：把 Theorem 1 降格为 well-formedness / framework invariant，把 IBT + negative result 前置为理论主贡献。 |
| EGNN n=20 case study 构造性偏置；cat-(iv) 去掉后 Set N 与 Set L 同为 2/15 | Claude | **真实问题。** 当前 case study 只能证明 construct validity，不能证明平均优越。 | Major-fixable：重写为 construct-validity demonstration；若要保留 utility claim，需补 real-fault / larger randomized evaluation。 |
| Case study + DeepCrime pilot underpowered，缺 adequately powered real-fault evaluation | GLM | **真实问题。** 稿件自己承认 n=5 pilot underpowered。 | Major：不必补到“平均优越”，但必须进一步收紧 claims，或执行至少一个已承诺协议。 |
| GenMorph 在 D1 / pooled 上支配 Set N，per-block edge underpowered | GLM | **真实问题。** 稿件已诚实披露 McNemar p=0.019 / 0.0043。 | Major venue-fit risk：可通过 theory-first framing + cost-axis + structural prediction 保住贡献，但不能包装成 fault-detection superiority。 |
| PWR negative-result proof relies on inspection / not fully formalized | Kimi | **部分成立。** Kimi JSON 未自动解析且该 critique 与稿件中“per-block exhaustion”表述存在冲突；但 reviewer 可见性不足是真的。 | Major-fixable：把 PWR counterexample 的关键 impossibility proof 从 appendix 抬到主文，给形式化假设和最小证明骨架。 |

**综合 blocker 判定：0 个不可修复 soundness blocker；4-5 个 major-fixable submission blockers。**  
也就是说，稿件不是“学术水平不够”，而是“当前论证/实证/呈现还不够稳，直接投会被 Major 或 Reject 的 reviewer 拖住”。

## 4. 学术水平评估

| 维度 | 分数 | 判断 |
|---|---:|---|
| 理论原创性 | 84 | panel novelty 均值 3.8/5；IBT 与 PWR 反例是最强贡献。 |
| 技术 soundness | 76 | 2/5 reviewer 无 raw blocker；raw blockers 多集中在定位与实证，不是明显数学错误。 |
| 贡献重要性 | 76 | significance 均值 3.2；有 TOSEM 价值，但必须从“效用优越”回到“理论框架 + 边界定理 + falsifiable prediction”。 |
| 实证支撑 | 62 | L*-blindness 与 IBT empirical thread 较强；fault-detection superiority 不足。 |
| 可复现性 | 70 | panel reproducibility 均值从 2.6 升至 3.2；但 review-time artifact/匿名包/DOI 仍未完全到位。 |
| 表达与投稿成熟度 | 58 | presentation 均值 2.6；长度、重复 caveat、ACM `manuscript` 模板、TODO-ref 仍是硬伤。 |
| 目标期刊 fit | 74 | TOSEM 可投，但要以 theory / methodology contribution 投稿；若按 empirical superiority 投稿，风险高。 |

## 5. 与 ACM TOSEM 投稿要求对照

沿用 2026-06-18 已核对的 ACM Author Gateway 官方要求：ACM journals 初投稿 LaTeX 应使用最新 Primary Article Template 2.16 与 `\documentclass[manuscript]{acmart}` 单栏；需要 CCS Concepts、keywords、ACM reference format；TAPS/production 需要源文件可处理、图像与字体等合规。

当前稿件状态：

- 不合规：`NOETHER_paper_arxiv.tex` 仍是 `\documentclass[acmsmall, screen]{acmart}`，不是 `manuscript`。
- 已具备：CCSXML、`\ccsdesc`、keywords 已存在。
- 风险：编译日志显示 77 页；仍有 image description、ACM reference format mandatory、字体替换、overfull/underfull 等警告。
- 风险：`theory/ibt_section_3_4.tex` 仍有 `% TODO-ref`。
- 风险：Data Availability 仍写 repository 和 Zenodo DOI camera-ready 后补；TOSEM review 阶段应提供匿名 artifact archive/hash。

## 6. 投稿前修订路线

### P0：投稿阻塞项

1. 生成 TOSEM review 版：`\documentclass[manuscript]{acmart}`，不要用 `acmsmall, screen` 作为投稿主版本。
2. 清理 `theory/ibt_section_3_4.tex` 的所有 `% TODO-ref` 与集成注释。
3. 准备匿名 artifact 包：archive、SHA-256、README、运行脚本、关键结果再现路径；正文从“camera-ready 后补 DOI”改为“review-stage anonymized archive available”。
4. 重构贡献叙事：Theorem 1 降格，IBT / negative result / L*-blindness prediction 前置。

### P1：Reviewer-2 会抓的核心项

1. 把 EGNN n=20 case study 改写为 construct-validity demonstration，不再作为比较优越证据。
2. 对 GenMorph D1 aggregate 明确承认“fault-detection aggregate 输给 Set G”；将 NOETHER 的优势限定为 algebraic derivability、cost-axis、structural coverage / falsifiable blind-spot prediction。
3. 将 PWR negative-result 的关键 impossibility proof 抬到主文，减少“inspection only”的阅读风险。
4. 若时间允许，执行一个最小但可信的补强实验：multi-seed GenMorph 或 human validation 小样本混淆矩阵。二选一也比纯承诺强。

### P2：提升接收概率项

1. 压缩主文，从 77 页优先降到 45-55 页。
2. 合并重复 Boundary boxes 与 threats，减少“防御性写作”的视觉负担。
3. 把 algebra distillation 做成可复现 protocol：给一个 held-out SUT 的端到端 extraction trace。

## 7. 最终建议

**建议：不要今天直接投；完成 P0 + P1 后投 TOSEM。**

授权重跑后的结论比上一版乐观：已经不是 Reject-risk dominant，而是清晰的 **Major Revision** 档。论文的学术水平足以支撑 TOSEM 投稿尝试，尤其是 IBT、PWR 反例和 theory-driven prediction。但现在直接投会把 reviewer 注意力引向“同义反复定理”“小样本实证”“GenMorph aggregate 失败”“模板/长度/artifact 未成熟”这些可避免问题。把这四类问题先处理掉，稿件会更像一篇强 theory-methodology TOSEM paper，而不是一篇被实证包装拖累的理论稿。
