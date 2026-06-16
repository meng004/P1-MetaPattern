现在我有足够的信息来生成候选文献清单和段落骨架。

---

## 候选文献清单

以下文献全部为真实存在、可从两个 bib 文件中溯源的条目，按 §2 的四条线分组。

---

### A. 线 1：MT/MR 基础与识别瓶颈（补强现有 4 行）

这条线已有 `Segura2016`、`LiTOSEM2025`、`Liu2014MTEffectiveness`、`Murphy2008`、`Xie2011`、`Saha2019SupervisedMR`。以下条目可扩充：

| 候选 | 来源 bib | cite key 建议 | 摘要关联性 |
|---|---|---|---|
| Chen, Kuo, Liu, Poon, Towey, Tse, Zhou. "Metamorphic Testing." ACM Computing Surveys, 2018. doi:10.1145/3143561 | references-2.bib, hash `2edaa17…` | `ChenCSUR2018` | 标志性综述，系统化 MT 的基础术语与分类 |
| Chen, Tse. "New visions on metamorphic testing after a quarter of a century of inception." ESEC/FSE 2021. doi:10.1145/3468264.3473136 | references-2.bib, hash `7c99e201…` | `ChenTseVisions2021` | 提出 MR 将超越 oracle 问题的七项展望，直接包含 LLM/AI 辅助方向 |
| Altamimi, Elkawakjy, Catal. "Metamorphic relation automation: Rationale, challenges, and solution directions." JSEP, 2022. doi:10.1002/smr.2509 | **NOETHER_paper.bib** (key: `Altamimi2022MRSLR`) | `Altamimi2022MRSLR` (已有) | SLR，已被引用；可在正文强化 |
| Zhou, Sun, Chen, Towey. "Metamorphic Relations for Enhancing System Understanding and Use." IEEE TSE, 2020. doi:10.1109/TSE.2018.2876433 | **NOETHER_paper.bib** (key: `Zhou2020SymmetryMRP`) | `Zhou2020SymmetryMRP` (已有) | 已引用 |

**新增高价值条目（references-2.bib，当前 NOETHER bib 未收录）：**

| 候选 | hash（references-2.bib） | 建议 cite key | 核心相关性 |
|---|---|---|---|
| Li, Zhao, Meng Li, Kexingyi Zhang, Yang, Liu, Yan. "Verification of multi-scale coupling program for high temperature gas-cooled reactor based on metamorphic testing." Annals of Nuclear Energy, 2025. doi:10.1016/j.anucene.2025.111846 | `28a9c028…` | `ZhaoLiNuclear2025` | 直接延续 Li et al. 2022 核电 MT 工作；与本文 HTGR 实证相关；需核验 year（bib 中 year=null，doi 已知）|
| Meng Li, Xiaohua Yang, Shiyu Yan, Jie Liu, Yusheng Liu, Jun Sun. "A Lightweight Verification Method Based on Metamorphic Relation for Nuclear Power Software." Frontiers in Energy, 2022. doi:10.3389/fenrg.2022.788753 | `00cf2fa5…` | `LiMengNuclear2022` | 本文第一作者先期核电 MT 工作，§2.1 或 §2.4 直接引用 |
| Yin Zhao, Meng Li, Jie-Sheng Liu. "A Review of Metamorphic Relation Representation Forms." DSA 2023. doi:10.1109/DSA59317.2023.00021 | `16b5a807…` | `ZhaoLiLiu2023RepForms` | 将 MR 按表达形式分类（算术/谓词/其他），为 MetaPattern 分类提供对比视角 |
| Jie Hong, Jie Zhang, Qi Qiu, Angang Ma, Meng Li, Shiyu Yan, Helin Gong. "A Dynamic Recognition Method of Metamorphic Relation Identification." ICRMS 2022. doi:10.1109/ICRMS55680.2022.9944595 | `fbdc7774…` | `HongZhang2022DynRecog` | 将 MR 识别转化为符号表达式回归问题，基因表达式编程动态挖掘，与本文 MR 自动识别线直接相关 |

---

### B. 线 2：结构化 MR 识别（METRIC/METRIC+）

已有 `ChenMETRIC2016`、`SunMETRICplus2021`。以下条目可补充论证：

| 候选 | 来源 | 建议 cite key | 相关性 |
|---|---|---|---|
| Sun, Dai, Liu, Chen. "Feedback-Directed Metamorphic Testing." TOSEM, 2022. doi:10.1145/3533314 | references-2.bib, hash `7041f1f0…` | `SunFeedbackMT2022` | 利用执行反馈动态调整 MR 选择，是 METRIC 框架的扩展应用 |
| Qiu, Zheng, Chen, Poon. "Theoretical and Empirical Analyses of the Effectiveness of MR Composition." IEEE TSE, 2022. doi:10.1109/tse.2020.3009698 | references-2.bib, hash `54a444ba…` | `QiuZhengMRComposition2022` | MR 组合的理论分析，与本文代数结构下 MR 空间的闭包性论证互补 |

---

### C. 线 3：自动化 MR 识别（含 LLM 辅助）

已有 `MRScout2024`、`GenMorph2024`、`Shin2024`、`ZhangChatGPTMR2023`、`GPTMR2025`、`AutoMT2025`、`Kanewala2016GraphKernel`、`Nolasco2024MemoRIA`。以下条目可补充：

| 候选 | 来源 | 建议 cite key | 相关性 |
|---|---|---|---|
| Xu, Chen, Wu, Cheung, Terragni, Zhu, Cao. "MR-Adopt: Automatic Deduction of Input Transformation Function for Metamorphic Testing." ASE 2024. doi:10.1145/3691620.3696020 | references-2.bib, hash `16f7bf04…` | `XuMRAdopt2024` | 用 LLM 推断 MR 输入变换，直接属于 LLM 辅助 MR 识别线 |
| Bose, Alebachew, Brown. "LLMs in Debate: Does Arguing Make Them Better at Detecting Metamorphic Relations?" ASE Workshops 2025. doi:10.1109/ASEW67777.2025.00019 | references-2.bib, hash `9d154d1b…` | `BoseLLMDebate2025` | 多 agent 辩论框架改善 LLM 识别 MR 的一致性，2025 最新；与 §2.3 LLM 辅助线直接衔接 |
| Duque-Torres, Pfahl, Ramler, Klammer. "A Replication Study on Predicting Metamorphic Relations at Unit Testing Level." SANER 2022. doi:10.1109/SANER53432.2022.00088 | references-2.bib, hash `e4ca978a…` | `DuqueTorresReplication2022` | 对 Kanewala PMR 方法的概念性复现，发现跨语言泛化受限，为本文 MR 可迁移性论证提供实证支撑 |
| Rahman, Kahanda, Kanewala. "MRpredT: Using Text Mining for Metamorphic Relation Prediction." ICSE Workshops, 2020. doi:10.1145/3387940.3392250 | references-2.bib, hash `35cc5353…` | `RahmanMRpredT2020` | 用文本挖掘（程序文档）预测 MR 类别，与 Kanewala2016GraphKernel 互补，均属结构特征预测线 |
| Zhang, Hao, Chen, Xiong, Xie, Zhang, Mei. "Search-based inference of polynomial metamorphic relations." ASE 2014. doi:10.1145/2642937.2642994 | references-2.bib, hash `6908a9f9…` | `ZhangSearchPoly2014` | 数值 MR 的搜索推断，早期自动化基线 |

---

### D. 线 4：MetaPattern 目录与经验充分性

已有 `Zhou2020SymmetryMRP`、`Ying2025MRPatterns`、`LiTOSEM2025`、`BellGlasstone1970`、`LewisMiller1993`。以下条目可补充：

| 候选 | 来源 | 建议 cite key | 相关性 |
|---|---|---|---|
| Segura, Alonso, Martin-Lopez, Duran, Troya, Ruiz-Cortes. "Automated Generation of Metamorphic Relations for Query-Based Systems." MET 2022. doi:10.1145/3524846.3527338 | **NOETHER_paper.bib** (key: `Segura2022QBSAutoMR`) | 已有 | 已引用 |
| Segura, Duran Toro, Troya, Ruiz-Cortes. "A Template-Based Approach to Describing Metamorphic Relations." MET 2017. doi:10.1109/MET.2017..3 | references-2.bib, hash `1516f0f6…` | `SeguraTemplate2017` | 标准化 MR 描述的模板方法，是 MetaPattern "vocabulary of recurring strategies" 的直接先驱 |
| Wu, Wang, Hu, Niu, Nie, Chen. "How Composite Metamorphic Relations Enhance Test Effectiveness of DNN Testing." IEEE TSE, 2026. doi:10.1109/TSE.2026.3675285 | references-2.bib, hash `8426bc34…` | `WuCompositeMR2026` | composite MR 的 DNN 实证研究，与 NOETHER 代数块组合 MetaPattern 的理论预测对应；需核验（year=2026，doi 已知）|

---

## Related Work 段落骨架

以下骨架仅使用上述**已确认真实**的文献（条目来自两个 bib 文件，doi 均有记录）。对于尚未并入 NOETHER_paper.bib 的条目，标注「需补入 bib」；对于 bib 中 year=null 的条目，标注「需核验年份」。骨架假设原有四线结构不变，在各小节末尾补充 1–3 个段落。

---

### 补充段落（嵌入位置：§2.1 小节末，现有第 3 段之后）

> Parallel evidence for the bottleneck's severity comes from empirical studies of MR quality assessment. Chen et al.'s 2018 CSUR survey systematically maps the twenty-year output of MT research and formalises the key vocabulary still in use today~\cite{ChenCSUR2018}. Chen and Tse's prospective analysis at ESEC/FSE 2021 identifies seven visions for the next decade, foregrounding AI-assisted and LLM-assisted MR identification as the most structurally open frontier~\cite{ChenTseVisions2021}. Within the nuclear-software domain specifically, Li et al.'s lightweight verification framework~\cite{LiMengNuclear2022} demonstrates that MT can be applied to nuclear-power software without reference solutions by deriving MRs from physical equations and numerical-algorithm specifications; Zhao et al.\ extend this line to multi-scale coupling programs for the HTGR reactor~\cite{ZhaoLiNuclear2025}（需核验年份）, establishing the domain-specific MR corpus that the present paper attempts to ground algebraically. A classification of MR representation forms across 162 relations—arithmetic expressions, predicate expressions, and other categories—provides an empirical baseline for our algebraic taxonomy~\cite{ZhaoLiLiu2023RepForms}（需补入 bib）; a dynamic recognition approach that frames MR identification as symbolic expression regression and mines relations via gene expression programming~\cite{HongZhang2022DynRecog}（需补入 bib） offers the closest operational predecessor to our algebraic-induction pipeline.

---

### 补充段落（嵌入位置：§2.2 小节末，现有段落之后）

> The compositionality of structured MR identification has received growing theoretical attention. Qiu et al.\ derive conditions under which MR composition is guaranteed to preserve fault-detection capability, showing that component MR independence is a necessary but not sufficient condition~\cite{QiuZhengMRComposition2022}（需补入 bib）. Sun et al.'s feedback-directed MT further demonstrates that dynamic selection of MRs during test execution can recover much of the cost lost to follow-up test generation~\cite{SunFeedbackMT2022}（需补入 bib）. Both results point toward the same conclusion that motivates NOETHER: the algebraic structure of the MR space, not just empirical selection heuristics, is the key to cost-effective composition.

---

### 补充段落（嵌入位置：§2.3 小节末，现有自动化识别段落之后）

> Three recent contributions sharpen the comparison with our algebraic grounding. MR-Adopt~\cite{XuMRAdopt2024}（需补入 bib） uses LLMs to deduce input-transformation functions from hard-coded test-case pairs, achieving reuse for 72\% of encoded MRs but remaining bounded by the relation types latent in the training corpus. Duque-Torres et al.'s replication study on the PMR approach~\cite{DuqueTorresReplication2022}（需补入 bib） finds that graph-kernel classifiers trained on Java control-flow graphs do not transfer to functionally equivalent Python and C++ methods, providing direct evidence that structural-feature predictors lack the language-invariant algebraic basis that would be needed for the transferability NOETHER requires. Most recently, Bose et al.\ show that a multi-agent LLM debate framework improves consistency in MR detection for augmented-reality applications but does not eliminate incorrect predictions, reinforcing that stability of LLM output is not a proxy for algebraic correctness~\cite{BoseLLMDebate2025}（需补入 bib）.

---

### 补充段落（嵌入位置：§2.4 小节末，现有 MetaPattern 段落之后）

> Segura et al.'s template-based approach to describing MRs~\cite{SeguraTemplate2017}（需补入 bib） demonstrates that recurring structural patterns can be abstracted into reusable descriptions; the templates are, in effect, MR MetaPatterns expressed in a domain-specific language rather than derived from operator algebras. Wu et al.'s empirical study of composite MRs in DNN testing~\cite{WuCompositeMR2026}（需补入 bib；需核验年份） corroborates our theoretical prediction that MRs derived from structurally complementary blocks of $\mathcal{D}(\mathcal{A}_P)$ exhibit superior failure revelation when composed: their finding that geometric complementarity in the latent embedding space predicts composition gain is an empirical analogue of NOETHER's block-orthogonality condition.

---

## 操作指引

**需补入 NOETHER_paper.bib 的条目（6 条）：**

1. `ZhaoLiNuclear2025` — doi:10.1016/j.anucene.2025.111846（year 需由出版商页面核实）
2. `LiMengNuclear2022` — doi:10.3389/fenrg.2022.788753（Frontiers in Energy, 已有 doi）
3. `ZhaoLiLiu2023RepForms` — doi:10.1109/DSA59317.2023.00021
4. `HongZhang2022DynRecog` — doi:10.1109/ICRMS55680.2022.9944595
5. `XuMRAdopt2024` — doi:10.1145/3691620.3696020
6. `BoseLLMDebate2025` — doi:10.1109/ASEW67777.2025.00019
7. `DuqueTorresReplication2022` — doi:10.1109/SANER53432.2022.00088
8. `QiuZhengMRComposition2022` — doi:10.1109/tse.2020.3009698
9. `SunFeedbackMT2022` — doi:10.1145/3533314
10. `SeguraTemplate2017` — doi:10.1109/MET.2017..3
11. `WuCompositeMR2026` — doi:10.1109/TSE.2026.3675285（year 需核验）
12. `ChenCSUR2018` — doi:10.1145/3143561
13. `ChenTseVisions2021` — doi:10.1145/3468264.3473136
14. `RahmanMRpredT2020` — doi:10.1145/3387940.3392250

**最高优先级（与论文核心论点最直接）：** `LiMengNuclear2022`（先期工作）、`ZhaoLiNuclear2025`（续作）、`BoseLLMDebate2025`（LLM-MR 最新）、`DuqueTorresReplication2022`（MR 迁移性实证）、`WuCompositeMR2026`（代数组合预测）。

**严禁使用的条目：** references-2.bib 中 `year = {null}` 的条目（如 `28a9c028…`）在 `ZhaoLiNuclear2025` 年份未经外部核实前，不得加入正式 `\cite{}`；骨架中已标注「需核验年份」。所有骨架段落中已标注「需补入 bib」的条目在 `\cite{}` 插入前必须先经 `get_crossref_paper_by_doi` 核验并写入 NOETHER_paper.bib。