# NOETHER 投稿成熟度复评：当前 TOSEM 重构稿

> 日期：2026-06-18  
> 评估对象：`NOETHER_paper_arxiv.tex`，branch `codex-noether-tosem-rewrite`，commit `7aae838` 后当前工作树  
> 目标期刊：ACM Transactions on Software Engineering and Methodology (TOSEM)  
> 证据边界：本轮尝试 fresh 外部 LLM 网关复评，但运行环境安全审查拒绝将未发表稿件重新发送至外部网关。因此，本报告使用：(i) 当前源码/PDF/日志，(ii) 本地补充材料，(iii) 已存在的 2026-06-18 授权外部 LLM panel 原始报告，(iv) ACM Author Gateway 官方投稿规范。不能把本报告解释为“当前重构稿已完成 fresh 外部多模型复审”。

## 1. 总裁决

**当前学术水平：TOSEM-relevant, theory-methodology contribution with clear potential.**  
**当前投稿成熟度：Major Revision before submission。量化成熟度：76/100。**

相对于上一版 `submission_maturity_assessment_2026-06-18-approved-rerun.md` 的 74/100，本轮重构真实改善了两个关键风险：

1. 论文主线已明显回到 **MR identification**，而不是 fault-detection / mutant-kill effectiveness。证据：Introduction 的 C5 和 Scope 明确写明 mutation、GenMorph、DeepCrime-style results 只是 secondary executability checks，不作为 average fault-detection superiority 证据；Experiments 开头定义 EQ1/EQ2/EQ3，且说明实验不估计 average fault-detection superiority。
2. ACM review 版模板的一个硬伤已修复。证据：当前源码为 `\documentclass[manuscript]{acmart}`，并含 `\setcopyright{none}`。

但当前仍不建议立即投 TOSEM，原因是：主文仍过长且图表未约简；Theorem 1 的 by-construction 风险仍会被强 reviewer 抓住；上游 algebra/block distillation 的人类依赖仍缺可复核 protocol；二级 mutation/head-to-head 段落仍占据大量篇幅，容易把 reviewer 拉回 effectiveness 评价框架；ACM 格式仍有 reference style、figure description、ACM reference format 等警告。

## 2. 证据使用说明

### 2.1 本轮 fresh LLM 网关状态

已按用户授权尝试执行：

```bash
rtk .venv-noether/bin/python scripts/llm_reviewer_panel.py --manuscript NOETHER_paper_arxiv.tex --out docs/review_2026-06-18/llm_panel_current_rewrite_approved
```

结果：执行层拒绝，理由是外部披露未发表稿件风险。因此，本报告不声称当前稿已完成 fresh external panel。

### 2.2 可用外部 panel 证据

可用外部 panel 是此前已存在的 2026-06-18 授权重跑结果：

- `docs/review_2026-06-18/llm_panel_rerun_approved/*.json`
- `docs/review_2026-06-18/llm_panel_rerun_approved_kimi_retry/kimi-k2-instruct.md`

该 panel 的共同裁决是 **Major Revision**。结构化 4 模型加 Kimi 手工读取后，主要风险集中于：

- Theorem 1 near-tautological / by-construction；
- EGNN / DeepCrime / mutation evidence underpowered or construct-biased；
- GenMorph D1 aggregate dominance；
- upstream algebra distillation reproducibility；
- presentation length and density。

当前重构已经处理了其中一部分 framing 问题，但没有完成图表压缩、human validation、larger empirical study 或 theorem reframing。

## 3. 目标期刊与投稿规范对照

官方 ACM Author Gateway 证据：

- ACM journals 要求 manuscript 使用 ACM authoring template；LaTeX 初投稿使用 `\documentclass[manuscript]{acmart}` 的单栏格式。来源：ACM Author Gateway, “Submitting Articles to ACM Journals,” https://authors.acm.org/journals/submission-process
- ACM LaTeX 指南要求 review/submission 版使用 `manuscript` 参数，并建议 `\setcopyright{none}`。来源：https://authors.acm.org/proceedings/production-information/preparing-your-article-with-latex
- ACM 指南说明所有 figures 需要 `\Description{}`，CCS concepts / keywords 对超过两页文章是 required，bibliography 应使用 `ACM-Reference-Format`。来源同上。

当前稿状态：

| 项 | 当前证据 | 评估 |
|---|---|---|
| `manuscript` class | `NOETHER_paper_arxiv.tex:10` 为 `\documentclass[manuscript]{acmart}` | 通过 |
| review copyright | `NOETHER_paper_arxiv.tex:18` 为 `\setcopyright{none}` | 通过 |
| ACM reference format | `\settopmatter{printacmref=false...}`，编译日志有 “ACM reference format is mandatory”；bibliography style 为 `unsrtnat` | 不通过 / 投稿前修 |
| Figure descriptions | 源码未发现 `\Description`；日志有 “Some images may lack descriptions” | 不通过 / 投稿前修 |
| 编译 | `pdflatex -interaction=nonstopmode -halt-on-error NOETHER_paper_arxiv.tex` 生成 78 页 PDF；无 fatal / undefined / rerun 错误 | 技术通过，但警告需清理 |
| 主文图表 | 1 图，18 表；计划目标为 3 图 + 6 表 | 未达计划，presentation 风险高 |
| TODO | `theory/ibt_section_3_4.tex` 仍有 4 处 TODO-ref / integration 注释 | 投稿阻塞 |

## 4. 当前稿的学术贡献评估

| 维度 | 分数 | 证据与理由 |
|---|---:|---|
| Originality / novelty | 84 | operator-algebraic MR identification、IBT、PWR negative result 仍是强原创点；上一轮外部 panel 的 novelty 均值约 3.8/5。 |
| Theoretical soundness | 76 | IBT 与 negative result 是强项；但 Theorem 1 仍容易被判为 by-construction invariant 而非深理论贡献。 |
| Research-question fit | 82 | 当前 Introduction / Experiments / Threats 已明确回到 MR identification、operator-block coverage、origin/boundary。 |
| Evidence sufficiency | 70 | S11 显示 SACOS/SPARK/LOCUST expert MR sets 为 110/110 `O<=` 单块覆盖；S12 显示 numpy.linalg / numpy.fft 可执行地覆盖 6 个 blocks。但专家-vs-NOETHER 二值 coverage matrix 尚未在主文中压缩成核心表。 |
| Reproducibility | 72 | 有补充材料、代码、结果文件和编译通过证据；但匿名 artifact hash、human validation、algebra distillation protocol 尚不足。 |
| Presentation | 61 | 78 页、18 表、重复 boundary/caveat、kill-rate 语汇残留，仍是最大投稿风险。 |
| TOSEM template compliance | 74 | `manuscript` 已修，但 `ACM-Reference-Format`、`\Description{}`、ACM reference format warning、TODO-ref 未清。 |

**加权总分：76/100。**

## 5. 多 reviewer 模拟裁决

| 角色 | 裁决 | 成熟度 | 核心判断 |
|---|---|---:|---|
| EIC / TOSEM fit | Major Revision | 77 | 主题和期刊匹配：software testing、MR identification、test oracle problem、formal/empirical SE 都在 TOSEM 读者范围内。但当前稿仍不像可直接送审的 clean submission。 |
| R1 Theory / formal methods | Major Revision | 78 | IBT 与 PWR counterexample 有价值；Theorem 1 必须降格为 pipeline invariant；operator algebra 定义和 Translate 模板需更可执行。 |
| R2 Empirical SE / reproducibility | Major Revision | 68 | 现在已经不再 overclaim effectiveness，但主文仍保留太多 underpowered mutation/head-to-head 材料；artifact/hash/human-rater protocol 不够成熟。 |
| R3 MT domain reviewer | Minor-to-Major Revision | 80 | MR identification positioning合理，GenMorph互补叙事正确；需要把 expert coverage matrix 和 search-origin/boundary matrix 做成主文核心证据。 |
| Devil's Advocate | Major Revision, reject risk if uncompressed | 64 | 读者仍可能看到 78 页和大量 kill-rate 段落后，以为论文在回避 GenMorph dominance；必须用 3 表/6 表策略强制重排证据。 |

综合：**Major Revision before submission**。不是因为贡献不够，而是因为当前稿件包装、证据层级和格式成熟度还没有到 TOSEM 直接投稿的稳定状态。

## 6. 关键证据核验

### 6.1 Expert MR sets vs NOETHER coverage

S11 industrial evidence 显示：

- SPARK: 36 expert MRs, covered 36/36, blocks = [`O<=`], new = 6
- LOCUST: 28 expert MRs, covered 28/28, blocks = [`O<=`], new = 6
- SACOS: 46 expert MRs, covered 46/46, blocks = [`O<=`], new = 6
- total: 110/110 = 1.000, Wilson95 [0.966, 1.000], orphans = 0, newly discovered / implicit = 18

这强力支持一个窄而真实的结论：**专家 MR 集高度集中在 order / monotone block，NOETHER 能把这种专家隐性知识显性化，并发现额外 implicit MRs。**

但 S11 自身也写明：该 corpus 是 single-block `O<=`，它不证明 G/T*/L*/E*/Conservation 等全 block transfer。因此主文如果声称“专家集 vs NOETHER across all blocks”必须给出 NOETHER-derived block occupancy matrix，不能只凭方程中存在结构就算 coverage。

### 6.2 Cross-domain operator-block evidence

S12 cross-domain evidence 较强：

- `numpy.linalg`: populated blocks = `G`, `T*`, `O<=`, `L*`, `E*`, `Conservation`；block count = 6；executable-hold = True for listed MRs。
- `numpy.fft`: populated blocks = `G`, `T*`, `Conservation`, `L*`, `O<=`, `E*`；block count = 6；executable-hold = True。

这支持“同一 operator block 可跨不同程序族 / 求解算法导出 MR class”的论证。它应进入主文核心表，而不是散落在 threats 或补充材料。

### 6.3 Search-based comparison

上一轮 panel 对 GenMorph 的共识是：不能把 NOETHER 写成 effectiveness winner。当前稿已经在 Scope、Experiments、Results reading guide 中改正方向。但正文仍有大量 `kill-rate`、`mutation score`、GenMorph D1 dominance 段落。它们可以保留为 secondary sanity-check，但主文占比过高，仍会诱导 reviewer 用 effectiveness 标尺打分。

## 7. 三个最重要的 P0 修复

1. **清理投稿格式阻塞。**  
   删除 `TODO-ref`，补所有 `\Description{}`，把 bibliography style 改为 ACM 要求的 `ACM-Reference-Format`，处理 `printacmref=false` 与 ACM mandatory warning 的冲突，去掉 postal-address warnings。

2. **表格约简到计划目标。**  
   主文保留 6 表：Definitions/counting rules；operator blocks/templates；experimental design matrix；expert vs NOETHER binary coverage；search vs NOETHER origin/boundary；cross-domain shared blocks + derivation trace。其余 mutation/head-to-head 表移 appendix/supplement。

3. **把 Theorem 1 降格，前置 IBT / boundary / coverage evidence。**  
   Theorem 1 用作 “no-drop / well-formedness invariant”；理论贡献 headline 放到 IBT、PWR negative result、MR origin/boundary taxonomy。

## 8. 最终建议

**不建议今天直接投。建议完成 P0 后再做一轮 fresh review。**

如果只能做一个短周期修订，优先顺序是：格式阻塞清理 → 主文表格约简 → Results 重排为 EQ1/EQ2/EQ3 → Theorem 1 降格 → Conclusion 压缩。完成后，预计成熟度可从 76/100 提升到 82-84/100，达到 TOSEM “可送审但大修概率仍高”的状态。

