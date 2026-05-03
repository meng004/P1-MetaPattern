# MetaPrompt v4：基于元模式先验的蜕变关系信息恢复方法

英文标题（投稿用）：*Recovering Metamorphic Relations from Scientific Software Artifacts via Meta-Pattern Guided LLMs*

副标题候选：*A Cross-Paradigm Information Recovery Approach for Mathematical-Equation-Specified Scientific Software*

论文核心定位（SANER framing）。本论文不把蜕变关系（Metamorphic Relations, MR）识别视为"测试生成"或"提示词工程（prompt engineering）"问题，而把它视为面向已有程序与需求语义的信息恢复问题（information recovery problem），即如何从程序、输入域、输出关系与语义约束中恢复可验证的蜕变关系。元模式（meta-pattern）在本框架中扮演软件制品语义结构的高层先验（semantic prior），而非提示词技巧；大语言模型（Large Language Model, LLM）仅是中间桥梁，方法骨架（参数 × 元模式矩阵 + 多源真值 Ground Truth, GT + 分流验证）即便以基因表达式编程（Gene Expression Programming, GEP）或符号执行替代 LLM 也依然成立。

目标会议为 SANER 2027（IEEE Int'l Conf. on Software Analysis, Evolution and Reengineering，CCF B），预估截稿 2026-10。SANER 官方征稿启事（Call for Papers, CFP）关键词覆盖 *software analysis · evolution · reengineering · program comprehension · information recovery from artifacts*，与本论文"从软件手册、源码、专家知识中恢复 MR"的 framing 契合。

方法适用边界（坦诚声明）。本方法仅适用于规约中含有明确数学或物理方程的科学计算软件，包括数值模拟、概率程序、代理模型、机器学习四类范式。对于无数学方程规约的程序（如纯字符串处理、UI 交互），本方法不在其设计目标范围内。

### 0.1 关键术语表（首次出现统一在此约定）

| 缩写 | 全称（中文 / 英文） |
|------|---------------------|
| MR | 蜕变关系（Metamorphic Relation）|
| MT | 蜕变测试（Metamorphic Testing）|
| LLM | 大语言模型（Large Language Model）|
| GT | 真值（Ground Truth）|
| MKR | 变异检错率（Mutation Kill Rate）|
| AVR | 自动验证通过率（Automatic Validation Rate）|
| GSD | 组序贯设计（Group Sequential Design）|
| ODE / PDE | 常微分方程 / 偏微分方程（Ordinary / Partial Differential Equation）|
| FDM | 有限差分法（Finite Difference Method）|
| MCMC | 马尔可夫链蒙特卡洛（Markov Chain Monte Carlo）|
| MC | 蒙特卡洛（Monte Carlo）|
| GPR | 高斯过程回归（Gaussian Process Regression）|
| PCE | 多项式混沌展开（Polynomial Chaos Expansion）|
| MLP | 多层感知机（Multi-Layer Perceptron）|
| SVM / SVC | 支持向量机 / 支持向量分类器（Support Vector Machine / Classifier）|
| LR | 逻辑回归（Logistic Regression）|
| LU | LU 分解（Lower-Upper Decomposition）|
| CoT | 思维链（Chain of Thought）|
| FS / Few-Shot | 少样本提示 |
| BL | 基线（Baseline）|
| RQ | 研究问题（Research Question）|
| H1–H6 | 待验证假设 1–6（Hypothesis 1–6）|
| DTW | 动态时间规整（Dynamic Time Warping）|
| GEP | 基因表达式编程（Gene Expression Programming）|
| RBF | 径向基函数（Radial Basis Function）|
| API | 应用程序接口（Application Programming Interface）|
| CCF | 中国计算机学会（China Computer Federation）|
| CFP | 征稿启事（Call for Papers）|
| FNR / FPR | 假阴性率 / 假阳性率（False Negative / Positive Rate）|
| ESS | 有效样本量（Effective Sample Size）|
| KL | Kullback–Leibler 散度 |
| CV | 变异系数（Coefficient of Variation）|
| IS | 重要性采样（Importance Sampling）|
| IS-MR / cell ρ | 单元格 Spearman 秩相关 |
| CER | 主张-证据-推理（Claim-Evidence-Reasoning）|
| GP | 高斯过程（Gaussian Process），GPR 的简写形式 |
| NN-Surr | 神经网络代理（Neural Network Surrogate）|
| MSE | 均方误差（Mean Squared Error）|
| RMSE | 均方根误差（Root Mean Squared Error）|
| NLP | 自然语言处理（Natural Language Processing）|
| AI | 人工智能（Artificial Intelligence）|
| ML / DL | 机器学习 / 深度学习（Machine Learning / Deep Learning）|
| NN | 神经网络（Neural Network）|
| RHS | 方程右端项（Right-Hand Side）|
| RNG | 随机数生成器（Random Number Generator）|
| CFL | Courant-Friedrichs-Lewy 数值稳定条件 |
| QMC | 准蒙特卡洛（Quasi-Monte Carlo）|
| RoR / GoR | 召回率 / 增益率族缩写（如 Recall_nt = 非平凡 Recall）|
| AVR-F1 ρ / V-AF1 | AVR 与 F1 的 Spearman 秩相关系数 |
| OOD | 分布外（Out-Of-Distribution）|
| PWR | 压水堆（Pressurized Water Reactor）|
| HTGR | 高温气冷堆（High-Temperature Gas-cooled Reactor）|
| NUIT | 团队既有蜕变测试对象核工程程序（Nuclear Unstructured-mesh Iterative Tool）|
| CRAM | NUIT 程序实现的核燃料燃耗算法（Chebyshev Rational Approximation Method）|
| OpenMC | 开源蒙特卡洛中子输运模拟软件 |
| CFD | 计算流体力学（Computational Fluid Dynamics）|
| BEPU | 最佳估计加不确定度（Best Estimate Plus Uncertainty）|
| IAEA | 国际原子能机构（International Atomic Energy Agency）|

后文涉及具体程序范式与统计方法的术语（如 sklearn / scipy / numpy / chaospy / PyMC / Lorenz / Lyapunov 指数等）属于通用工具/经典名词，不再列入术语表。

相对 v3.4 的核心变更：
- 实验对象：压水堆（Pressurized Water Reactor, PWR）单程序扩为 12 程序 × 4 范式（数值模拟、概率程序、代理模型、机器学习），论证方法的跨范式通用性。
- 删除变异测试：投入产出比极低（10 天集群计算 + 数十万次 OpenMC 蒙特卡洛中子输运软件调用，仅获 1 个 MKR 指标），AVR 升级为可执行价值的主指标。
- 假设系统由 H1–H4 扩为 H1–H6，新增 H5（跨范式一致性）与 H6（元模式空缺反向验证）。H6 是反向假设，证明方法不虚构空缺元模式 MR，提供 false-when-out-of-scope 的可证伪证据。
- LLM 切换为 Claude Opus 4.7、ChatGPT 5.5、DeepSeek-V4、GLM-5（国外 2、国内 2 平衡），原 Claude Opus 4 / GPT-4o / Gemini 2.5 Pro / GLM-4-Plus 弃用。
- 基线由 B1–B4 六档裁为 B1、B2、B2″ 三档；消融由 A0–A6 七档裁为 A0、A3、A4、A6 四档。
- GT 协议二阶弱化：源 2 由"每程序 1 位独立专家"先简化为"paradigm 级顾问轻量审核+投票"，再简化为"2–3 位行业专家纯二元 yes/no/unsure 判断"。专家不做识别/补漏/修改/排序；候选 MR 池由源 1+3+4 提供，源 2 仅作为多数决过滤器。codebook 同步删除 C5 重要性准则，保留 C1–C4 客观判定。
- 总实验量由 930 次扩为 6960 次，GSD 早停后约 5800 次。

---

## 摘要

科学计算软件普遍存在测试预言（test oracle）缺失问题。蜕变测试以蜕变关系（Metamorphic Relations, MR）作为替代预言，已成为缓解该问题的核心手段。然而 MR 本身的获取迄今仍是瓶颈：高质量 MR 散落在软件手册、源码、领域专家知识与已有测试制品中。如何从这些异构软件制品中恢复一组可验证、可执行的 MR，本文称之为 MR 信息恢复问题（MR Information Recovery Problem），尚未有系统化方法。已有 LLM 辅助工作多以松散的少样本提示直接生成 MR，存在三类共性短板：恢复遗漏多于错误、推理路径未受语义先验引导、恢复结果与可执行验证之间缺乏闭环。

本文提出 MetaPrompt，一种以蜕变关系元模式作为软件制品语义结构先验的 MR 信息恢复方法，适用于规约中含明确数学或物理方程的科学计算软件。核心机制有三：（i）将五类元模式（守恒性 P1、单调性 P2、收敛性 P3、轨迹性 P4、偏序性 P5）作为软件制品的高层语义维度，构成"参数 × 元模式"恢复矩阵，强制系统性遍历恢复路径以最小化遗漏；（ii）以元模式为分流键，将候选 MR 自动路由至统计假设检验、时序形态分析、约束逻辑验证三类管线，把"恢复"与"验证"耦合为同一闭环；（iii）三源独立汇聚 Ground Truth（文献 + 领域专家 + 跨家族 LLM）破除循环论证。

我们在覆盖 4 类范式的 12 个开源科学计算程序（数值模拟、概率程序、代理模型、机器学习）上进行系统评估：4 主流 LLM（Claude Opus 4.7、ChatGPT 5.5、DeepSeek-V4、GLM-5）× 4 档消融 × 3 档基线 × N=20 次重复，共 6720 次主实验调用。论文同时提供反向验证（H6 元模式空缺假设），证明方法在元模式不适用的程序上不虚构 MR。预期结果：MetaPrompt 在 F1 上较等量知识基线提升 ΔF1 ≈ 0.08–0.12，在非平凡 MR 召回率上提升 ΔRecall_nt ≈ 0.10–0.16，跨 4 范式 ΔF1 变异系数 CV < 0.5，自动分流验证通过率 AVR 显著高于基线（数值待最终实验填入）。本文公开三源 GT、跨范式非平凡 codebook、自动化分流验证脚本与全部提示词模板，作为 MR 信息恢复方向后续研究的可复现基础设施。

---

## 一、引言与研究问题

### 1.0 引言：MR 信息恢复问题

科学计算软件（如反应堆物理、CFD、气候模拟、贝叶斯推断、机器学习模型）的测试长期受困于预言缺失问题：程序输出无法用解析解或外部参考独立验证。蜕变测试以蜕变关系（MR）作为预言的替代物，即输入变换 r 与输出关系 R 之间的可验证不变性，已成为该领域的事实标准 [Chen2018, Segura2016]。然而，MT 的工程化部署一直被同一个瓶颈所限制：MR 本身从哪里来？

观察现实，MR 实际上散落分布在四类软件制品（software artifacts）中：
- 方程与算法手册（physical model artifact）：物理不变性、对称性、守恒律隐含其中。
- 源码与配置（implementation artifact）：边界处理、归一化、加速选项的语义可在此追溯。
- 输入/输出域规约（specification artifact）：参数取值范围、单位、单调性方向的元数据。
- 领域专家知识（tacit knowledge artifact）：未文档化的工程经验、退化工况、参考程序差异。

将"获取 MR"重新理解为"从上述异构制品中恢复一组可验证、可执行的 MR"，即本文称的 MR 信息恢复问题（MR Information Recovery Problem），是本论文的出发点。这个 framing 把 MR 工作从孤立的"测试技术"重新嵌入到 SANER 长期关注的软件分析、程序理解、信息恢复、制品逆向工程议题谱系中：与 METRIC/METRIC+（从功能规约恢复 MR）[Chen2016, Sun2018]、MeMo（从 Javadoc 恢复 MR）[Blasi2021]、MR-Scout（从测试用例恢复 MR）[Xu2024] 同属一脉，但它们各自只覆盖单一制品来源。

本论文的核心论点是：MR 信息恢复需要一个跨制品共享的语义结构先验（semantic prior）。若没有先验，LLM 等通用恢复工具会陷入两类典型失败：松散输出（recovery 路径无组织）、表层平凡 MR（被显眼路径吸引而遗漏深层不变性）。我们提出蜕变关系元模式（守恒性 P1、单调性 P2、收敛性 P3、轨迹性 P4、偏序性 P5）作为该先验。它在四类制品上具有跨范式一致性，并已在 1998–2025 年文献证据中得到归纳支撑 [Anonymous, under review]。

方法的可替代性边界（关键判别）。本方法骨架由四部分组成：(i) 制品语义操作化指南（五元模式）；(ii) 参数 × 元模式恢复矩阵；(iii) 三源独立 GT；(iv) 元模式分流自动验证。LLM 仅是 (i) 应用到 (ii) 时的中间桥梁，若以 GEP、符号执行或专家手工填表替代 LLM，方法骨架依然成立。这一可替代性证明本工作不是 prompt engineering，而是 information recovery（详 §10.5）。

方法适用边界（坦诚声明）。本方法仅声称对规约中含有明确数学或物理方程的科学计算软件有效，覆盖数值模拟、概率程序、代理模型、机器学习四类范式（共 12 个实验程序，详 §IV）。对于无数学方程规约的软件（如纯字符串处理、UI 交互、配置管理），元模式没有可挂靠的语义结构，本方法不在设计目标范围内。这一边界由 H6 反向假设实证检验（详 §1.3 与 §IV）。

### 1.1 研究问题

RQ1（恢复有效性）：以元模式作为软件制品语义先验，是否显著提升从科学计算制品中恢复 MR 的有效性（F1、Recall、Precision）？

RQ2（先验组件贡献）：先验的元模式知识、参数 × 元模式矩阵、链式推理、少样本示例等组件中，哪些对恢复效果贡献最大？

RQ3（跨工具与跨范式泛化）：在不同 LLM 与不同程序范式上，元模式先验是否表现出一致的恢复增益？

RQ4（可执行价值与适用边界）：恢复出的 MR 集合是否具有更高的自动验证通过率？方法在元模式不适用的 (程序, 元模式) 单元格上是否避免虚构 MR？

### 1.2 与并行工作的边界

本团队另有一项关于 MR 元模式理论框架的论文 [Anonymous, under review]，与本论文密切但互不重叠。在此澄清以避免审稿人对自我重复的疑虑：

| 维度 | 元模式理论论文 [under review] | 本论文（MetaPrompt v4）|
|---|---|---|
| 主要贡献 | 提出五元模式与 MR 来源层次模型；以 1998–2025 文献证据进行系统归纳 | 将元模式操作化为 LLM 可执行的结构化提示词与遍历矩阵；建立从恢复到自动验证的端到端闭环 |
| 研究方法 | 文献归纳 + 理论建构 | 实证实验（4 LLM × 4 消融 × 3 基线 × 12 程序 × N=20）|
| 实验对象 | 无（理论性） | 12 个开源程序（覆盖 4 类范式） |
| 评估指标 | 元模式覆盖率、跨程序范式迁移性 | Precision / Recall / F1 / Recall_nt / AVR / 跨范式 CV |
| 复用关系 | 提供元模式定义与归纳证据 | §II 给出最小自洽重述（一段加一表）以供本文自包含阅读，定义细节引用 [Anonymous, under review] |

理论论文回答"元模式是什么、从哪里来"，本论文回答"如何让 LLM 系统性使用元模式以高质量识别 MR、并验证识别结果的可执行性"。两文核心贡献无重叠；本文不复述理论论文的归纳证据与跨范式分析。

### 1.3 研究假设（六假设：5 正向 + 1 反向）

#### H1：元模式操作化有效性假设

> 以元模式作为软件制品语义结构的操作化指南进行 MR 恢复，其 F1 显著高于等量领域知识但无该指南的 LLM 恢复结果。

合理性推导：Li 等（TOSEM 2025）将"MR 模式方法"列为降低领域知识依赖的关键方向 [Li2024-TOSEM]；Towey 等（STVR 2025）提出 11 种 MR 模式 [Towey2025]；Luu 等（2023）证实 ChatGPT 无结构引导下 MR 大量模糊 [Luu2023]；Shin 等（CCIS 2024）证明结构化少样本可显著提升 [Shin2024]。这些证据共同指向：LLM 的瓶颈不是知识量，而是推理组织框架。

关键术语说明：本论文不声称元模式具有"先验"性质（元模式 P1–P5 来源是 1998–2025 年 40+ 篇 MT 文献的归纳产物，把归纳产物再作为先验在归纳源同类程序上验证会构成结构性循环），仅声称其作为操作化指南可显著提升 LLM 在科学计算软件上的 MR 恢复有效性。

可证伪条件：H1 通过三对照检验，即 A6 vs B2、A6 vs B2″、B2 vs B2″。若 A6 vs B2″（最干净对照，等量知识无任何结构）p ≥ 0.05，H1 被拒绝。

#### H2：矩阵结构关键性假设

> 参数 × 元模式交叉矩阵的系统性遍历是元模式方法中对识别效果贡献最大的单一组件，其消融导致的 F1 下降幅度超过其他任何单一组件。

合理性推导：Bose 等（ASE 2025 AgenticSE）发现 LLM 在 MR 识别中的核心问题是遗漏而非错误 [Bose2025]。矩阵结构通过强制对每个 (θ, P_k) 显式判断"适用/不适用"防止遗漏，思想上同源于软件工程检查表 [Fagan1976]。

可证伪条件：若消融实验中去掉矩阵结构（A0→A3）的 ΔF1 小于 A3→A4（CoT 增量）或 A4→A6（Few-Shot 增量），H2 被拒绝。

#### H3：非平凡 MR 深度推理假设

> 元模式方法相对于无元模式基线的 F1 提升，在非平凡 MR 上的幅度显著大于在平凡 MR 上的幅度。

合理性推导：Li Meng（2021）NUIT 两阶段验证已指出"高抽象层次蜕变关系识别成本高、效率低" [LiMeng2021]；Zhao 等（ANE 2026）依靠非平凡 MR 发现 HTGR 中两个传统测试无法检测的缺陷 [Zhao2026]。

可证伪条件：若元模式方法在平凡 MR 上的召回率提升 ≥ 非平凡 MR 上的提升，H3 被拒绝。

#### H4：自动验证一致性假设

> 元模式方法识别出的 MR 集合，其自动分流验证通过率（AVR）显著高于无元模式基线，且 AVR 与 F1 在 (LLM, 程序) 配对上呈中等以上正相关。

合理性推导：MR 的"识别正确"与"可执行验证"在 v3.4 之前依靠变异测试桥接，但变异测试投入产出比低且强绑定单一程序。自动分流验证（P2/P5 Wilcoxon、P4 DTW、P1 约束逻辑）提供更直接的客观证据，能直接验证"恢复 MR 真满足声明的不变性"。

可证伪条件：若 A6 与 B2 的 AVR 差异不显著（p ≥ 0.05），或 AVR-F1 Spearman ρ < 0.3，H4 被拒绝。

#### H5：跨范式一致性假设

> A6 相对 B2 的 ΔF1 在数值模拟、概率程序、代理模型、机器学习四个范式上符号一致为正，且变异系数 CV(ΔF1) < 0.5；12 程序中 ΔF1 > 0 的程序数 ≥ 11/12（sign test 显著）。

合理性推导：若元模式仅对某一范式起作用（如仅对数值模拟有效，对 ML 无效），方法的"跨范式通用性"主张就不成立。H5 是论文跨范式叙事的可证伪硬阈值。

可证伪条件：若任一范式 ΔF1 ≤ 0，或 CV(ΔF1) ≥ 0.5，或 ΔF1 > 0 的程序数 < 11/12，H5 被拒绝，方法通用性主张需软化。

#### H6：元模式空缺反向假设

> 对每个 (程序 S_i, 元模式 P_k) 单元格，A6 输出的 MR 数应与 GT 中该单元格 MR 数显著正相关（Spearman ρ > 0.6）。即：GT 中无 P_k MR 的程序，A6 也不应虚构 P_k MR；GT 中有 P_k MR 的程序，A6 应能识别。

设计目的：H6 是反向假设，证明方法不是无原则的"普适增强"。审稿人最常用的拒稿理由之一是"作者只展示方法成功的场景，无法判断方法的真实适用边界"，H6 直接消除这一风险。

合理性推导：若 A6 在所有 (S_i, P_k) 单元格上都输出大量候选 MR，则方法可能存在 hallucination 倾向，候选 MR 的高 Recall 实为"广撒网"导致的伪高召回。H6 检验方法是否具有"知道何时不适用"的能力。

可证伪条件：
- 若 A6 在 GT 空缺单元格仍输出 ≥ 5 条 MR，则方法存在 hallucination 倾向，H6 被拒绝，论文需诚实报告并将定位收窄至"元模式适用单元格"。
- 若 A6 在 GT 充实单元格大量漏报，则方法矩阵遍历不彻底，H6 被拒绝。
- 若 60 单元格 Spearman ρ < 0.6，H6 被拒绝。

---

## 二、背景与理论基础

### 2.1 蜕变测试与蜕变关系

蜕变关系 MR 是输入变换 r 与输出关系 R 之间的可验证不变性，形式 (r, R) 满足 R(f(x), f(r(x))) 对程序 f 与所有合法输入 x 恒为真 [Chen2018]。蜕变测试通过验证 MR 在源测试与衍生测试上的输出关系，绕开预言缺失。详细定义参见综述 [Chen2018, Segura2016]。

### 2.2 五元模式：最小自洽重述

> 本节仅为本文自包含阅读所需的最小重述。元模式的形式化定义、文献归纳证据与跨范式（数值模拟 / 概率程序 / ML 代理模型）通用性分析详见 [Anonymous, under review]。

五元模式（meta-patterns）是从 1998–2025 年三类目标程序的 40+ 篇 MT 文献中归纳出的、可跨程序范式迁移的高层 MR 诱导模板：

| 元模式 | 核心提问 | 跨范式典型 MR 示例 |
|---|---|---|
| **P1 守恒性** | "什么变换不改变输出？" | 数值积分能量守恒 / 贝叶斯先验对称性 / ML 特征缩放不变 / GP 内插点恒等 |
| **P2 单调性** | "增大参数 θ，输出 y 往哪个方向变？" | ODE 步长 → 误差 / 似然单调 / SVM C 参数 → 边界硬度 / 训练样本量 → 准确率 |
| **P3 收敛性** | "推到极端/精化后趋向什么？" | 网格细化 → 精确解 / MCMC 链长 → 后验收敛 / 训练样本 → 真实分布 / 多项式阶数 → L2 误差 |
| **P4 轨迹性** | "响应路径长什么样？" | 暂态形态 / 学习曲线 / GP 后验形状 / Lorenz 系统轨迹分离 |
| **P5 偏序性** | "谁更准？在哪最不准？" | 多算法精度排序 / 多核函数偏好 / 多估计器对比 |

元模式的作用是：在领域知识不足时，从"必须保持的数学/物理不变性质与结构规律"出发系统诱导出可检验的具体 MR，从而把 MR 的设计从依赖经验的手工猜测推进为可指导、可迁移、可复用的方法过程。

### 2.3 大型语言模型（沿用标准描述，从略）

---

## 三、相关工作

### 3.1 MR 信息恢复谱系（按制品来源组织）

我们把已有 MR 获取工作重组为信息恢复谱系，按所恢复的软件制品来源分类，便于审稿人定位本工作。

| 制品来源 | 代表方法 | 恢复方式 | 局限 |
|---|---|---|---|
| 功能规约 / 类别选择框架 | METRIC [Chen2016]、METRIC+ [Sun2018] | 输入域分类 + 类别选择 | 需要预先存在结构化规约 |
| API 文档 / Javadoc 注释 | MeMo [Blasi2021] | NLP 抽取等价类断言 | 高度依赖注释质量 |
| 测试用例 / 已有测试套件 | MR-Scout [Xu2024] | 从测试代码挖掘 MR | 需高质量测试套件 |
| 源码 / 控制流图 | Kanewala-Bieman [Kanewala2013, Kanewala2016]、Hardin-Kanewala [Hardin2018] | 机器学习 + 图核 | 需类似 MR 的标注训练集 |
| 输入/输出数据 / 程序行为 | AutoMR [Zhang2019]、SPSS [Wen2022]、GEP [LiMeng2020-IJPE] | 数值搜索 / 符号回归 | 仅数值可量化关系 |
| 方程与算法手册（科学计算特有）| NUIT 两阶段 [LiMeng2021] | 人工分析 + 变异验证 | 高度依赖专家 |
| 领域专家显式知识 | Luu 2022 [Luu2022], Hiremath 2021 [Hiremath2021] | 专家访谈 + 对称性枚举 | 不可规模化 |

本方法在该谱系中的位置：
- 跨制品恢复：同时利用方程手册、源码语义、I-O 域规约、专家知识四类制品。
- 跨范式先验：五元模式作为先验，对数值模拟、概率程序、代理模型、机器学习四类程序范式均有归纳证据 [Anonymous, under review]。
- 恢复-验证耦合：分流自动验证把"恢复"与"对恢复结果的验证"嵌入同一闭环。

### 3.2 LLM 辅助的 MR 工作及其与本方法的边界

| 维度 | 本方法（MetaPrompt v4）| Shin 2024 | Zhang 2025-SANER | Cho 2025 | Bose 2025 |
|---|---|---|---|---|---|
| 工作类型 | MR 信息恢复 | MR 生成 | MR 生成 | MR 应用 | MR 识别稳定性 |
| 制品来源 | 四类制品同时利用 | 单一来源 | 单一来源 | 不涉及 | 不涉及 |
| 语义先验 | 五元模式（跨范式跨制品）| 无 | 无 | 无 | 无 |
| 推理组织 | 参数 × 元模式恢复矩阵 | 少样本流程化 | 定制 GPT | 无 | 多智能体辩论 |
| 评估闭环 | 自动化分流验证 + 跨范式 CV | 问卷 | 计数 | 56 万次 MT | 稳定性度量 |
| 与 LLM 解耦度 | 方法骨架可替换 LLM | 中-高 | 高 | 高 | 高 |

### 3.3 与 Zhang et al. (SANER 2025) 的直接对照

Jiaming Zhang 等 [Zhang2025-SANER]（"Can Large Language Models Discover Metamorphic Relations? A Large-Scale Empirical Study"，SANER 2025）是与本工作同会、同档、同期、同主题的最强直接对照。SANER 评审人会立即追问本工作相对 Zhang 2025 的实质性创新：

| 维度 | Zhang et al. (SANER 2025) | 本工作（MetaPrompt v4）| 切分性质 |
|---|---|---|---|
| 核心贡献 | 评估 GPT-3.5/GPT-4 在 37 个程序上的 MR 识别能力，构建统一 prompt 框架 | 提出 MR 信息恢复问题；以五元模式作为跨制品操作化指南，建立"恢复-验证耦合"管线 | 不同贡献类型 |
| prompt 结构 | 单层统一 prompt | 三层嵌套 prompt：参数 × 元模式恢复矩阵 + 元模式分流推理模板 + 程序特化实例 | 结构不同 |
| LLM 选择 | GPT-3.5 + GPT-4（OpenAI 同家族）| Claude Opus 4.7 + ChatGPT 5.5 + DeepSeek-V4 + GLM-5（4 跨家族）| 覆盖更广 |
| 被测对象 | 37 个混合通用程序（搜索、排序、字符串、ML 等）| 12 程序 × 4 范式（数值模拟、概率程序、代理模型、机器学习）| 领域定向 |
| MR 来源 GT | 文献已发表 MR | 三源独立汇聚（文献、领域专家、跨家族 LLM）| GT 严谨性更强 |
| 评估指标 | 识别 MR 数量、新颖 MR 数量 | F1 + Recall_nt + AVR + 跨范式 CV + 单元格 ρ | 指标维度更全 |
| 可执行验证 | 无 | 自动化分流验证（P2/P5 Wilcoxon + P4 DTW + P1 约束）| 本工作独有 |
| 关键基线对照 | Zero-shot 与 Few-shot | A0/A3/A4/A6 四档消融 + B1/B2/B2″ 三档基线 | 对照设计粒度更细 |
| 反向验证 | 无 | H6 元模式空缺单元格分析（false-when-out-of-scope）| 本工作独有 |

关键边界结论：
- Zhang 2025 是本工作的精神前驱而非方法对手。本工作 §5.2 的 B2 "Domain-Prompted LLM" 基线在概念上致敬 Zhang 2025 的统一 prompt 框架。
- 本工作的非增量式创新在于：（i）从"识别 MR"到"恢复 MR"的概念升级；（ii）矩阵遍历加分流验证的方法创新；（iii）跨 4 范式 12 程序的实证厚度；（iv）H6 反向验证支撑可证伪性。

诚实声明：Zhang 2025 在通用程序规模（37 个）上仍领先本工作（12 个）。本工作不主张全面优于 Zhang 2025，优势在方法论严谨性、跨范式覆盖与反向验证设计上。

---

## 四、实验对象、制品来源与 Ground Truth 构建

### 4.0 制品来源界定

为了让本论文的"信息恢复"叙事有可审计的边界，我们显式列出实验中实际作为恢复输入的四类软件制品：

| 制品类别 | 实际数据 | 用途 |
|---|---|---|
| 方程与算法手册 | 程序对应数学/物理方程 + 算法说明（教科书章节摘录） | 主要恢复来源；构成 LLM 上下文 |
| 源码与配置 | Python API 接口签名 + 关键模块函数注释 | 辅助恢复；提供边界处理与归一化语义 |
| 输入/输出域规约 | 输入参数取值范围、单位、典型工况 | 辅助恢复；约束 r 与 R 的合法形式 |
| 领域专家显式知识 | §4.4 源 2 的 1 位该范式专家独立识别清单 | 用于 GT 构建（源 2），不混入恢复输入以防泄漏 |

严格隔离规则：用作 GT 的专家清单（源 2）不进入任何方法的恢复输入；专家在不接触元模式概念的前提下独立工作（详 §4.2）。

### 4.1 12 程序 × 4 范式

每程序需满足：开源可获取 / 代码规模 < 1000 行 / 数学或物理方程明确 / 文献中有已知 MR。

#### 范式 A：数值模拟 / 数值算法（3 程序）

| ID | 程序 | 数学/物理方程 | 已知 MR 文献 | 单次运行 |
|---|---|---|---|---|
| **A1** | `scipy.integrate.solve_ivp` 求解 Lorenz 系统（σ=10, β=8/3, ρ=28；t∈[0,40]）| 三维非线性 ODE 系统 | Strogatz 2018 | < 1s |
| **A2** | NumPy 数值线性代数：LU 分解 + Ax=b 求解 | 矩阵分解、向量空间不变性 | Hook & Kelly 2009 | < 0.1s |
| **A3** | 一维热传导有限差分（自编 FDM）∂u/∂t = α∂²u/∂x² | 抛物线 PDE | Chen 2018, Yan 2025 | < 1s |

#### 范式 B：概率程序（3 程序）

| ID | 程序 | 数学/物理方程 | 已知 MR 文献 | 单次运行 |
|---|---|---|---|---|
| **B1** | PyMC Beta-Binomial 共轭推断 | Bayes 定理 + 共轭先验 | Dutta 2018 | 1–5s |
| **B2** | Metropolis-Hastings 采样器（自编，目标 2D 高斯）| MCMC 平稳分布、可逆性 | Dutta 2018, Salimans 2015 | 5–10s |
| **B3** | 朴素 Monte Carlo 积分（求 ∫₀¹ exp(-x²) dx）| 大数定律、收敛速率 √N | Caflisch 1998, Lemieux 2009 | < 1s |

#### 范式 C：代理模型（3 程序）

范式内子方法独立性。C1 GPR（Bayesian 核方法）、C2 PCE（正交基展开）、C3 NN-Surr（多层非线性逼近）覆盖代理建模的三条独立数学路径：核方法、正交基、神经网络，避免范式内同源。原 C3 Kriging 在 Bayesian 视角下与 C1 GPR 数学等价（仅命名传统不同），已替换为基于 `sklearn.neural_network.MLPRegressor` 的回归代理，从而堵住"3 程序实质 2 证据"的潜在审稿攻击点。

| ID | 程序 | 数学/物理方程 | 已知 MR 文献 | 单次运行 |
|---|---|---|---|---|
| **C1** | `sklearn.gaussian_process` GPR | 核函数（RBF/Matern）+ 后验解析解 | Forrester 2008, Murphy 2012 | < 1s |
| **C2** | 多项式混沌展开（chaospy / numpy.polynomial）| Wiener-Askey 正交多项式族 | Xiu 2003, Sudret 2008 | < 1s |
| **C3** | `sklearn.neural_network.MLPRegressor` 作为 Forrester 1d / Branin 2d benchmark 函数的回归代理 | 通用近似定理 + 反向传播 + MSE 损失（多层非线性逼近，非核非正交基）| Forrester 2008, Hornik 1991, Murphy 2012 | 1–3s |

#### 范式 D：机器学习（3 程序）

| ID | 程序 | 数学/物理方程 | 已知 MR 文献 | 单次运行 |
|---|---|---|---|---|
| **D1** | `sklearn.MLPClassifier` on Iris | 前向传播 + softmax | Xie 2011（ML MR 开山）、Murphy 2008 | 1–3s |
| **D2** | `sklearn.svm.SVC` (RBF) on Breast Cancer | 二次规划 + 核技巧 | Xie 2011, Dwarakanath 2018 | < 1s |
| **D3** | `sklearn.linear_model.LogisticRegression` on Diabetes | sigmoid + 交叉熵损失 | Xie 2011, Liang 2021 | < 0.1s |

### 4.2 12 程序 × 5 元模式覆盖矩阵（H6 反向验证基础）

下表给出预期的 (程序 × 元模式) 单元格 GT MR 数量分布，作为 H6 单元格 Spearman ρ 分析的基础：

| 程序 | P1 守恒 | P2 单调 | P3 收敛 | P4 轨迹 | P5 偏序 |
|---|---|---|---|---|---|
| A1 Lorenz | ●● | ● | ●● | ●●● | ● |
| A2 LU | ●●● | ● | ● | **○** | ● |
| A3 FDM | ●● | ●● | ●●● | ●● | ● |
| B1 Beta-Binomial | ●●● | ●● | ●● | **○** | ● |
| B2 MCMC | ●● | ● | ●●● | ●● | ● |
| B3 MC 积分 | ● | ● | ●●● | **○** | **○** |
| C1 GPR | ● | ●● | ●● | ●● | ●●● |
| C2 PCE | ●● | ● | ●●● | **○** | ●● |
| C3 NN-Surr | ●● | ●●● | ●● | ●● | ●● |
| D1 MLP | ●●● | ●● | ●● | ●● | ●● |
| D2 SVM | ●● | ●●● | ● | ● | ●● |
| D3 LR | ●● | ●● | ●● | **○** | ● |

图例：●●● ≥ 3 条 / ●● 1–2 条 / ● 仅 1 条 / **○** 预期 0 条（元模式空缺单元格）

H6 验证基础。60 个单元格中预期 6 个空缺（○）：5 个集中在 P4 轨迹性维度（A2 LU、B1 Beta-Binomial、B3 MC 积分、C2 PCE、D3 LR），另 1 个在 B3 MC 积分的 P5 偏序性。A6 在这些单元格上若仍输出 ≥ 5 条候选 MR，则暴露 hallucination 倾向；若输出 0–2 条，则方法具有"知道何时不适用"的能力。

### 4.3 Ground Truth 构建：三源独立汇聚法

核心原则：Ground Truth 必须独立于元模式理论构建，避免循环论证。

#### 源 1：已发表文献 MR

每程序从对应范式经典文献（Xie 2011、Forrester 2008、Dutta 2018、Strogatz 2018、Yan 2025 等，详 §4.1 表）抽取已发表 MR，预计每程序 5–15 条。

#### 源 2：行业专家纯二元判断

人数 2–3 位行业专家，覆盖四类范式（建议 A 数值模拟 + B 概率程序为 1 位、C 代理模型 + D 机器学习为 1 位，第 3 位作为奇数仲裁可选）。资历要求博士学位或工程界等价资历，对应范式 ≥ 3 年研究/工程经历。

团队提供完整输入材料：
1. 程序方程与算法说明（每程序 1 页）。
2. 五元模式 P1–P5 的中文解释（守恒、单调、收敛、轨迹、偏序，含示例）。
3. 每条候选 MR 的形式化表达 (r, R, basis) + 中文物理含义解释 + 元模式归属。

专家任务为 15–30 min 视频或线下访谈。对清单上每条候选 MR 仅做一项判断：Yes（数学/物理上成立，可作为该程序的有效蜕变关系）、No（不成立或表述错误）、Unsure（判断依据不足）。专家不做的事：识别新 MR、补充遗漏、修改表述、给出依据、主观排序、元模式归类。

一致性度量：3 位专家按多数决（≥ 2/3 Yes 通过）；2 位时要求一致 Yes，冲突项整体记 unsure 不计入 G_final。预期产出为单一表格，记录每条候选 MR 一组 (yes/no/unsure)×N_experts 投票。

#### 源 3：跨家族 LLM 交叉验证

使用 Qwen 3-Max（阿里）与 Doubao-1.5-Pro（字节）作为 GT 交叉源。这两家与主实验四款 LLM（Claude Opus 4.7、ChatGPT 5.5、DeepSeek-V4、GLM-5）厂商不同。

两 LLM 各自独立运行不含元模式提示的 MR 识别（仅给程序方程加 MR 通用定义），各 N=10 重复后取并集；输出经 Meng 与硕士 A 双独立编码（Cohen's κ ≥ 0.75）后纳入 G_llm_cross。预期每程序补充 4–12 条候选。

#### 源 4：团队三角化编码

源 4 用于补偿源 2 弱化带来的人工独立维度损失。Meng 与 1 位独立反审者各自独立从源 1 + 源 3 候选清单中：
- 标注每条候选 MR 的物理基础正确性（accept / revise / reject）。
- 为每程序补 0–3 条文献未覆盖但研究者公认的 "common-sense MR"（如 D1 MLP 的"softmax 输出归一"等显然条目）。

两人独立编码后计算 Cohen's κ，要求 ≥ 0.75；冲突项由 Li Meng（PI）仲裁。

#### Ground Truth 合并规则

```
候选清单 = (G_literature ∪ G_llm_cross ∪ G_team) 经团队共识审核（Cohen's κ ≥ 0.75）
G_final = 候选清单 ∩ {专家投票 ≥ 多数 Yes 的 MR}
```

源 2 扮演纯二元过滤器，不贡献新 MR。源 1（文献）、源 3（跨家族 LLM）、源 4（团队三角化）共同构成候选 MR 池，源 2（行业专家）做最终验证。

每条 MR 标注三项：数学/物理内容、来源标签、(程序, 元模式) 单元格归属（用于 H6 单元格分析）。GT 中不把元模式归属作为"正确答案"，元模式归类按独立维度评估。

### 4.4 匹配判定规则（破循环论证）

两条 MR 判定为"匹配"需同时满足两条：
1. 参数匹配：涉及相同或等价的输入参数 θ。
2. 输出关系语义等价：R 在数学/物理含义上一致。

匹配判定不要求元模式归属相同。一条数学正确但被 LLM 归入不同元模式的 MR 仍判定为匹配。匹配判定由 2 名评审独立执行，报告 Cohen's κ，要求 κ > 0.75，不一致项第三方仲裁。

### 4.5 跨范式非平凡 MR Codebook

适用于 12 程序的统一 codebook，按四条客观准则确定每条 MR 的标签：

| 准则 | 操作化判定 | 触发标签 |
|---|---|---|
| **C1 推理步数** | 该 MR 的数学/物理依据是否需要 ≥ 2 步推理？ | ≥2 步 → 半平凡或非平凡 |
| **C2 跨方程/多组件耦合** | 该 MR 是否依赖两个及以上方程或两个及以上算法组件耦合？ | 是 → 至少半平凡 |
| **C3 反直觉方向** | 该 MR 的方向/形态是否与朴素直觉一致？ | 反直觉 → 非平凡 |
| **C4 教科书可读出** | 该 MR 是否能从该范式的标准教科书中直接读出？ | 是 → 平凡 |

判定规则：
- 触发 C4 ∧ ¬C1 ∧ ¬C2 ∧ ¬C3：平凡（教科书直接可读且无推理深度无耦合无反直觉）。
- 触发 C1 ∧ C3：非平凡（多步推理加反直觉）。
- 触发 C2 ∧ ¬C4：非平凡（多组件耦合且非教科书）。
- 其他情形：半平凡。

12 程序预期标签分布（codebook 校准用）：平凡 ≈ 35 / 半平凡 ≈ 60 / 非平凡 ≈ 50（合计约 145 条 GT MR）。

---

## 五、恢复管线：从制品到可验证 MR

### 5.0 管线总览

```
┌─────────────────────────────────────────────────────────────────┐
│              MR Information Recovery Pipeline (v4)              │
│                                                                 │
│  四类软件制品（§4.0）                                            │
│  ┌─手册 ─┬─源码 ─┬─I-O 域 ─┬─专家知识*┐                          │
│  └────────┴────────┴───────────┴──────────┘                     │
│                       ↓                                         │
│  ╔═══════════════════════════════════════╗                      │
│  ║  阶段 A: 制品摄入 + 五元模式先验注入   ║                      │
│  ║  → 参数 × 元模式恢复矩阵 (Sec 5.1)    ║                      │
│  ╚═══════════════════════════════════════╝                      │
│                       ↓                                         │
│  ╔═══════════════════════════════════════╗                      │
│  ║  阶段 B: 跨单元格恢复 (LLM 桥梁)      ║                      │
│  ║  → 候选 MR 集 {(r, R, P_k, basis)}   ║                      │
│  ╚═══════════════════════════════════════╝                      │
│                       ↓                                         │
│  ╔═══════════════════════════════════════╗                      │
│  ║  阶段 C: 元模式分流自动验证 (Sec 6.3)  ║                      │
│  ║  P2/P5→Wilcoxon, P4→DTW              ║                      │
│  ║  P1→约束验证                          ║                      │
│  ╚═══════════════════════════════════════╝                      │
│                                                                 │
│  *专家知识仅用于 GT，不进入恢复输入                              │
└─────────────────────────────────────────────────────────────────┘
```

阶段 B 当前以 LLM 实现，但管线骨架对 LLM 不依赖：阶段 A 的恢复矩阵也可由 GEP、符号执行或专家手工填表填充；阶段 C 与 LLM 完全无关。这是本方法属于 information recovery 范式的结构性证据。

本论文管线结束于阶段 C（AVR 验证），不包含变异测试。变异测试作为期刊扩展版的独立实验保留。

### 5.1 提示词架构（三层嵌套）

层 1 系统提示词：角色 + MR 定义 + MR vs Property 区分 + 五元模式策略 + YAML 输出格式：

```yaml
- id: "Prog-NN"
  name: "简洁名称"
  source_artifact: "方程 / 源码 / I-O 域 / 专家"
  meta_pattern: "P1|P2|P3|P4|P5|uncertain"
  classification: "MR|Property"
  input_relation_r: "数学表达"
  output_relation_R: "数学表达"
  basis: "数学/物理依据"
  falsifiability: "违反意味着什么缺陷"
```

层 2 元模式推理模板（参数 × 元模式矩阵）。
层 3 程序特化实例。

### 5.2 消融变体（4 档）

| 变体 | 缩写 | 元模式知识 | 矩阵结构 | CoT | Few-Shot | 验证假设 |
|---|---|---|---|---|---|---|
| **A0** | BL | ✗ | ✗ | ✗ | ✗ | 起点纯 LLM 基线 |
| **A3** | MP-matrix | 完整 | ✓ | ✗ | ✗ | H2 矩阵机制激活 |
| **A4** | MP-matrix-CoT | 完整 | ✓ | ✓ | ✗ | H3 CoT 增量 |
| **A6** | Full | 完整 | ✓ | ✓ | ✓ | 完整方法 |

原 A1（MP-name）、A2（MP-template）、A5（MP-matrix-FS）已删除：增量小，且与现有 4 档非独立。

### 5.3 对比基线（3 档）

B1（Zero-Shot LLM）：程序名称加最简提示。

B2（Domain-Prompted LLM，领域知识等量基线）：与本方法等量的领域知识，按"数学性质 → 数值/算法特性 → 工况约束"三层自然推理组织，不引入元模式概念，无矩阵结构。

B2″（Domain-NoMatrix，最干净对照）：等量领域知识，无矩阵机制（参数维度的扁平列表），无元模式概念。

```
你是该范式的领域专家。请基于以下程序方程与算法识别本程序应满足的蜕变关系：
[完整方程公式、参数集、算法列表，与 A6 完全相同]
请逐条列出 MR，每条包含输入变换 r、输出关系 R 与依据。
```

已删除的基线：B2′（Domain-Matrix，列内容与元模式概念重叠不干净）、B3（GEP，仅 PWR 适用）、B4（Towey 11 模式，单点对比价值低）。

### 5.4 等量度量（H1 验证有效性的关键）

| 等量层 | 度量 | 阈值 |
|---|---|---|
| 层 1 Token 等量 | cl100k_base tokenizer | ±5% |
| 层 2 概念覆盖 | 关键概念集 K（每程序 12–18 概念）| 全覆盖 |
| 层 3 信息熵 | byte-level entropy | ±10%（辅助）|

### 5.5 H1 三对照设计

- A6 vs B2：检验"元模式 + 矩阵"对比"领域三层自然推理"的总体差异。
- A6 vs B2″：H1 最干净对照，检验"元模式 + 矩阵"对比"等量知识无任何结构"。
- B2 vs B2″：检验领域三层组织本身的贡献。

MR-Scout 与 MARS 不作为基线的理由：
- MR-Scout 依赖已有测试套件中 MR 编码用例，需先存在 MR 才能发现 MR。本论文 12 个开源程序的测试套件无显式 MR 编码用例，MR-Scout 无法启动。
- MARS 依赖清晰函数签名加类型系统进行符号分析。本论文程序多以 numpy/sklearn/pymc 高层 API 组织，符号边界不满足 MARS 前置条件。

---

## 六、评估指标体系

### 6.1 第一层指标：识别效果

| 指标 | 公式 | 说明 |
|---|---|---|
| Precision | $P = \|C \cap G\| / \|C\|$ | 正确率 |
| Recall | $R = \|C \cap G\| / \|G\|$ | 召回率 |
| F1 | $2PR/(P+R)$ | 综合分数 |
| FPR | $\|C \setminus G\| / \|C\|$ | 假阳性率 |
| CV(ΔF1) 跨 12 程序 | std(ΔF1) / mean(ΔF1) | H5 跨范式一致性核心指标 |

### 6.2 第二层指标：分层质量指标

| 指标 | 定义 | 目的 |
|---|---|---|
| 非平凡 MR 召回率 | 非平凡 MR 中被正确识别的比例（按 §4.5 codebook）| 验证 H3 |
| AVR（自动分流验证通过率）| 通过 P2/P5 Wilcoxon / P4 DTW / P1 约束逻辑的 MR 数 / 该方法可分流 MR 总数 | H4 主指标，取代 MKR |
| V-AF1 一致性 | Spearman ρ(AVR, F1) | H4 验证-识别一致性 |
| MR/Property 区分准确率 | 正确区分 MR 与属性的比例 | 概念理解深度 |
| 形式化完整度 | 具完整 (r, R) 形式化表达的 MR 比例 | 工程可操作性 |
| 元模式归类准确率 | 已识别 MR 元模式归类与专家判定一致比例 | 独立辅助指标 |
| 新颖 MR 数 | 不在 G_final 中但经专家确认有效的新 MR | 创造性发现能力 |

### 6.3 第三层指标：H6 元模式空缺单元格 ρ

对 60 个 (12 程序 × 5 元模式) 单元格，计算 A6 输出 MR 数与 GT MR 数的 Spearman 相关系数。

判定：
- ρ ≥ 0.6：H6 通过，方法具有"知道何时不适用"的能力。
- ρ < 0.6：H6 不通过，需报告虚构案例与漏报案例。

### 6.4 自动化分流验证（AVR）协议

每程序的 AVR 管线设计：

| 程序 | P2/P5 验证（Wilcoxon）| P4 验证（DTW）| P1/P3 验证（约束逻辑）|
|---|---|---|---|
| A1 Lorenz | 初值扰动 → 轨迹 Lyapunov | 暂态形态对比 | 能量守恒约束 |
| A2 LU | 矩阵规模 → 残差单调 | — | 行交换不变性 |
| A3 FDM | 网格细化 → 误差单调 | 边界条件 → 形态退化 | 对称初值守恒 |
| B1 Beta-Binomial | 样本量 → KL 收敛 | — | 后验对称性 |
| B2 MCMC | 链长度 → 自相关 | — | 平稳分布约束 |
| B3 MC 积分 | N → 误差 √N | — | 加性不变 |
| C1 GPR | 长度尺度 → 平滑度 | 训练点扰动 → 后验形态 | 内插点恒等 |
| C2 PCE | 阶数 → L2 误差 | — | 正交性约束 |
| C3 NN-Surr | 隐层节点数 / 训练样本量 → 验证 MSE | 训练 loss 学习曲线形态 | 特征顺序置换不变 / universal approximation 收敛 |
| D1 MLP | 训练样本 → 准确率 | 学习曲线形态 | 类标签置换 |
| D2 SVM | C 参数 → 边界硬度 | — | 特征缩放不变 |
| D3 LR | 正则化 → 权重稀疏 | — | 概率归一 |

判据：P2/P5 通过条件为 Wilcoxon p < 0.01 且 Cliff's δ > 0.33；P4 通过条件为 DTW 归一距离 < 0.2；P1 通过条件为约束通过率 ≥ 95%。

变异测试不在 v4 论文范围内：投入产出比极低（10 天集群加数十万次调用，仅获 1 个 MKR 指标），且强绑定单一程序。变异测试作为期刊扩展版独立实验保留。

### 6.5 统计方法

- 每个配置重复 N=20（temperature=0.5，固定随机种子 1..20）。
- 报告均值 ± 标准差，加 95% bootstrap 置信区间（n=2000 重抽样）。
- 用 Wilcoxon 秩和检验比较方法间差异（α=0.05），消融实验使用配对 Wilcoxon。
- Cliff's δ 报告效应量（small ≥ 0.147、medium ≥ 0.33、large ≥ 0.474）。
- 多重检验校正使用 Holm-Bonferroni 顺序校正：
  - H1 族（A6 vs B2 + A6 vs B2″ + B2 vs B2″ = 3 对照）。
  - H2 族（A0→A3、A3→A4、A4→A6 = 3 对照）。
  - H3 族（ΔRecall_nt vs ΔRecall_trivial = 1 对照）。
  - H4 族（A6 vs B2 AVR = 1 对照）。
  - H5 族（12 程序 ΔF1 sign test = 1 综合检验）。
  - H6 族（60 单元格 Spearman ρ = 1 检验）。
  - 族总数为 10 个独立假设检验。
  - 报告校正后 p 值与原始 p 值并排。

### 6.6 样本量与功效分析

| 假设 | 期望效应量 | 所需 N | N=20 实际功效 |
|---|---|---|---|
| H1（A6 vs B2 ΔF1）| Cliff's δ ≈ 0.45 (large) | 16 | ~85% |
| H1（A6 vs B2″ ΔF1）| Cliff's δ ≈ 0.50 (large) | 14 | ~88% |
| H2（A0→A3 ΔF1）| Cliff's δ ≈ 0.40 (medium-large)| 18 | ~80% |
| H3（ΔRecall_nt vs ΔRecall_trivial）| Cliff's δ ≈ 0.50 (large) | 14 | ~88% |
| H4（A6 vs B2 AVR）| Cohen's h ≈ 0.40 (medium) | 30 | 跨 12 程序汇总 N=240 远超阈值 |
| H5（12 程序 sign test）| binomial(12, 0.5) | 12 | 11/12 → p=0.003 |
| H6（60 单元格 Spearman ρ）| ρ_target = 0.6 | 60 | 直接达到 |

Group Sequential Design 采用 Pocock 风格，在 N=15 时做中期评估：若 H1 主对照（A6 vs B2）Cliff's δ ≥ 0.30 且 p < 0.025（O'Brien-Fleming 调整后），提前停止该配置实验。早停可减少约 25% 工作量。

### 6.7 Inter-Rater Agreement 度量

- 二分类数据（"匹配 / 不匹配"，§4.4 GT 匹配判定）：Cohen κ ≥ 0.75。
- 有序三分类数据（"平凡 / 半平凡 / 非平凡"，§4.5 codebook 标注）：Weighted Cohen κ（quadratic weights）≥ 0.65 或 Krippendorff α ≥ 0.67。

---

## 七、消融实验设计

### 7.1 消融矩阵（4 档）

| 实验 | 元模式知识 | 矩阵结构 | CoT | Few-Shot | 验证假设 |
|---|---|---|---|---|---|
| A0-BL | ✗ | ✗ | ✗ | ✗ | 纯 LLM 能力基线 |
| A3-MP-matrix | 完整 | ✓ | ✗ | ✗ | H2 矩阵结构增量 |
| A4-MP-matrix-CoT | 完整 | ✓ | ✓ | ✗ | H3 CoT 对非平凡 MR |
| A6-Full | 完整 | ✓ | ✓ | ✓ | 完整方法 |

### 7.2 消融分析框架

对每对相邻消融 (A_k, A_{k+1}) 计算：ΔF1、ΔRecall_nontrivial、Wilcoxon p 值、Cliff's δ。

预期分析模式：
- H2 预期：ΔF1(A0→A3) > ΔF1(A3→A4) > ΔF1(A4→A6)。
- H3 预期：ΔRecall_nt(A3→A4) / ΔRecall_trivial(A3→A4) > 1。

---

## 八、多模型对比与总实验规模

### 8.1 模型选择

| 模型 | 提供商 | 国别 | 发布 | 选择理由 |
|---|---|---|---|---|
| Claude Opus 4.7 | Anthropic | 美 | 2026-Q1 | 最强推理加长上下文 |
| ChatGPT 5.5 | OpenAI | 美 | 2026-04-23 | 行业最广旗舰 |
| DeepSeek-V4 | DeepSeek | 中 | 2026-Q1 | 国产强推理加 MoE 架构 |
| GLM-5 | 智谱 AI | 中 | 2026 | 国产旗舰加中文优势 |

国外 2、国内 2 平衡，覆盖不同训练数据来源、不同对齐策略、不同模型架构（含 DeepSeek 的 MoE）。所有模型使用完全相同的最佳提示词（A6-Full）与领域知识输入，各运行 N=20 次。

### 8.2 对比基线汇总

| 基线 | 类型 | 是否实际运行 | 控制变量 |
|---|---|---|---|
| B1-Zero-Shot | LLM 直接提问 | ✓ 4 模型 × 12 程序 × N=20 | 无领域知识，无元模式 |
| B2-Domain-Prompted | 领域知识等量 + 三层组织 | ✓ 4 模型 × 12 程序 × N=20 | 等量领域知识，无矩阵 |
| B2″-Domain-NoMatrix | 领域知识等量，无矩阵无元模式 | ✓ 4 模型 × 12 程序 × N=20 | H1 最干净对照 |

### 8.3 总实验运行次数

```
主实验:
  4 消融条件（A0, A3, A4, A6）× 12 程序 × 4 LLM × N=20 = 3840
  3 基线条件（B1, B2, B2″）× 12 程序 × 4 LLM × N=20    = 2880
  小计: 6720

预实验（temperature 校准）:
  1 LLM × 12 程序 × 4 T 值 × 5 = 240

合计: 6960 次 LLM 调用
GSD 早停后预期: ≈ 5800 次

成本估算（按 Claude Opus 4.7 单价 ~$0.05/调用）: ≈ $290–350
```

---

## 九、实验结果（待填）

### 9.1 RQ1：元模式引导有效性

#### 表 1：A6 vs B2 vs B2″（按程序汇总，4 LLM 平均）

| 程序 | A6 F1 | B2 F1 | B2″ F1 | ΔF1(A6-B2) | ΔF1(A6-B2″) | p_holm |
|---|---|---|---|---|---|---|
| A1 Lorenz |  |  |  |  |  |  |
| A2 LU |  |  |  |  |  |  |
| A3 FDM |  |  |  |  |  |  |
| B1 Beta-Binomial |  |  |  |  |  |  |
| B2 MCMC |  |  |  |  |  |  |
| B3 MC 积分 |  |  |  |  |  |  |
| C1 GPR |  |  |  |  |  |  |
| C2 PCE |  |  |  |  |  |  |
| C3 NN-Surr |  |  |  |  |  |  |
| D1 MLP |  |  |  |  |  |  |
| D2 SVM |  |  |  |  |  |  |
| D3 LR |  |  |  |  |  |  |
| **范式 A 均值** |  |  |  |  |  |  |
| **范式 B 均值** |  |  |  |  |  |  |
| **范式 C 均值** |  |  |  |  |  |  |
| **范式 D 均值** |  |  |  |  |  |  |

### 9.2 RQ2：消融实验结果

#### 表 2：4 档消融指标（4 LLM × 12 程序均值 ± 标准差）

| 配置 | Precision | Recall | F1 | Recall_nt | ΔF1 | p_holm | Cliff's δ |
|---|---|---|---|---|---|---|---|
| A0-BL |  |  |  |  | — | — | — |
| A3-MP-matrix |  |  |  |  |  |  |  |
| A4-MP-matrix-CoT |  |  |  |  |  |  |  |
| A6-Full |  |  |  |  |  |  |  |

### 9.3 RQ3：跨工具与跨范式泛化

#### 表 3：4 LLM 在 A6-Full 配置下的性能（12 程序均值）

| 模型 | Precision | Recall | F1 | Recall_nt | AVR |
|---|---|---|---|---|---|
| Claude Opus 4.7 |  |  |  |  |  |
| ChatGPT 5.5 |  |  |  |  |  |
| DeepSeek-V4 |  |  |  |  |  |
| GLM-5 |  |  |  |  |  |

#### 表 4：H5 跨范式一致性

| 范式 | A6 F1 均值 | B2 F1 均值 | ΔF1 | sign |
|---|---|---|---|---|
| A 数值模拟 |  |  |  |  |
| B 概率程序 |  |  |  |  |
| C 代理模型 |  |  |  |  |
| D 机器学习 |  |  |  |  |
| **CV(ΔF1)** | — | — |  | — |
| **sign test (12 程序)** | — | — |  | binomial p |

### 9.4 RQ4：可执行价值与适用边界

#### 表 5：自动化分流验证 AVR 结果

| 方法 | P2 通过率 | P5 通过率 | P4 通过率 | P1 通过率 | 综合 AVR | V-AF1 ρ |
|---|---|---|---|---|---|---|
| A6-Full |  |  |  |  |  |  |
| B2-Domain |  |  |  |  |  |  |
| B2″-Domain-NoMatrix |  |  |  |  |  |  |

#### 表 6：H6 元模式空缺单元格分析（60 单元格）

| 单元格类型 | 数量 | A6 平均输出 MR 数 | GT 平均 MR 数 | 单元格 Spearman ρ |
|---|---|---|---|---|
| 空缺单元格（GT=0）|  |  |  | — |
| 稀疏单元格（GT=1）|  |  |  | — |
| 中等单元格（GT=2）|  |  |  | — |
| 充实单元格（GT≥3）|  |  |  | — |
| **全部 60 单元格** | 60 |  |  | (target ≥ 0.6) |

#### 表 7：12 程序 × 4 LLM 单元格 F1（A6-Full，48 cells，H5 跨工具一致性证据）

| 程序＼LLM | Claude Opus 4.7 | ChatGPT 5.5 | DeepSeek-V4 | GLM-5 | 行均值 ± SD |
|---|---|---|---|---|---|
| A1 Lorenz |  |  |  |  |  |
| A2 LU |  |  |  |  |  |
| A3 FDM |  |  |  |  |  |
| B1 Beta-Binomial |  |  |  |  |  |
| B2 MCMC |  |  |  |  |  |
| B3 MC 积分 |  |  |  |  |  |
| C1 GPR |  |  |  |  |  |
| C2 PCE |  |  |  |  |  |
| C3 NN-Surr |  |  |  |  |  |
| D1 MLP |  |  |  |  |  |
| D2 SVM |  |  |  |  |  |
| D3 LR |  |  |  |  |  |
| **列均值 ± SD** |  |  |  |  | (LLM 间 CV) |

### 9.5 图表规范（4 figures）

Fig 1（H1 主对照箱线图）：A6 vs B2 vs B2″，12 程序合并 × 4 LLM × N=20 = 960 数据点。
- x 轴：3 个组（A6、B2、B2″）。
- y 轴：F1 ∈ [0, 1]。
- 元素：箱线加散点 jitter；标注 Holm 校正后 p 值与 Cliff's δ。
- 期望形态：A6 中位数显著高于 B2 与 B2″，B2 略高于 B2″。

Fig 2（H2 消融累积增益曲线）：A0 → A3 → A4 → A6 单调上升。
- x 轴：4 档配置序号。
- y 轴：F1（误差棒为 95% bootstrap CI）。
- 期望形态：A0→A3 跳跃最大（矩阵机制），A3→A4 中等增量（CoT），A4→A6 边际增量（Few-Shot）。
- 决策提示：若 A0→A3 ≤ A3→A4 且 ≤ A4→A6，需重写 §10.1 主论断。

Fig 3（H5 跨范式森林图）：12 程序 ΔF1 95% CI。
- y 轴：12 程序按范式聚类（A1–A3、B1–B3、C1–C3、D1–D3）。
- x 轴：ΔF1 = F1(A6) − F1(B2)，零线参考。
- 每条 95% bootstrap CI；标注 sign test 结果（k/12 程序为正）。
- 期望：≥ 11/12 程序 ΔF1 > 0，CV(ΔF1) < 0.5。

Fig 4（H6 元模式空缺热力图）：12 程序 × 5 元模式 = 60 单元格。
- 双图并列：左为 GT 单元格 MR 数（参考），右为 A6 输出 MR 数。
- 颜色映射：0–8 渐变。
- 关键观测：左图深色处右图也应深色；左图为零（白色）处右图应保持低（≤ 2）。
- 决策提示：若右图在 GT 空缺单元格出现 ≥ 5 个 MR，说明 hallucination 严重，论文需软化主张。

### 9.6 表格回填规范（执行注意事项）

1. 数值精度：比例（F1/P/R/AVR）保留 3 位小数；ΔF1 与 ρ 保留 3 位；p 值保留 4 位（含科学计数 e-04）。
2. 统计量呈现：表中数字一律 `mean ± std`；若需 95% CI 则单独脚注列出。
3. 多重检验标识：`p_holm < 0.05` 加 *，`< 0.01` 加 **，`< 0.001` 加 ***。
4. 缺失数据：API 失败导致的缺失用 "—" 标注，并在 §9.0 脚注汇总缺失单元格数。
5. 预期值越界处理：若实测 ΔF1 < 期望最低（§7.1），文案改用 §7.5 决策树的"软化分支"，不得直接掩盖。
6. 早停说明：若 GSD N=15 提前停止，N=15 与 N=20 同时报告（一份正文一份附录），不得只报有利数据。

---

## 十、讨论与分析

### 10.1 H1 预期讨论

预期一：A6 vs B2 ΔF1 ≈ 0.06–0.10（p<0.05），证明元模式加矩阵优于领域三层自然推理。
预期二：A6 vs B2″ ΔF1 ≈ 0.10–0.15（p<0.05），此为 H1 最干净对照（B2″ 等量知识无任何结构）。
预期三：B2 vs B2″ ΔF1 ≈ 0.04–0.06，证明领域三层组织本身有部分贡献，但矩阵加元模式仍有独立增益。

若 A6 vs B2″ 不显著但 A6 vs B2 显著，意味着方法的真正有效成分是"任何系统化结构都比无结构好"，元模式与领域语言效用相当。此时本论文需诚实调整核心创新表述为"系统化遍历是关键，元模式是其有效列填充之一"。

### 10.2 H2 预期讨论

预期：ΔF1(A0→A3) ≈ 0.06–0.09（矩阵机制核心增量），ΔF1(A3→A4) ≈ 0.02–0.04（CoT 增量），ΔF1(A4→A6) ≈ 0.01–0.03（Few-Shot 边际增量）。三档单调递减证明矩阵机制是元模式方法的最大单一杠杆。

### 10.3 H3 预期讨论

预期：CoT（A3→A4）对非平凡 MR 召回率的提升（ΔRecall_nt ≈ 0.10–0.15）显著大于平凡 MR（ΔRecall_trivial ≈ 0.02–0.05）。CoT 为 LLM 展开"截断误差结构""方程对称性""跨方程耦合"等多步推理提供空间，恰好作用于非平凡 MR 所需的超越直觉的数学分析。

### 10.4 H4 预期讨论

预期：A6 AVR ≈ 0.70–0.85，B2 AVR ≈ 0.55–0.70（ΔAVR ≈ 0.10–0.20，p<0.05）。AVR 与 F1 在 (LLM, 程序) 配对上 Spearman ρ ≈ 0.5–0.7，验证"自动验证通过的 MR 是真正高质量 MR"，构成对"低质量 MR 凭运气通过"质疑的客观反驳。

### 10.5 H5 预期讨论（跨范式一致性）

预期：4 范式均值 ΔF1 全为正（数值 ≈ 0.08–0.12，概率 ≈ 0.08–0.12，代理 ≈ 0.07–0.11，ML ≈ 0.06–0.10），CV(ΔF1) ≈ 0.20–0.40 < 0.5，12 程序 sign test 12/12，binomial p < 0.001。

ML 范式 ΔF1 略低（MR 边界更清晰，领域基线更强），但仍 ≥ 0.06。若任一范式 ΔF1 ≤ 0，本论文需诚实将"跨 4 范式通用"主张降级为"跨 3 范式通用，第 4 范式（具体指出哪个）需要专门方法"。

### 10.6 H6 预期讨论（元模式空缺反向验证）

预期：A6 在 GT 空缺的 (S_i, P_k) 单元格上输出 0–2 条 MR（接近虚构上界）；60 单元格 Spearman ρ ≈ 0.65–0.80。

若 H6 不通过：A6 在 GT 空缺单元格输出 ≥ 5 条 MR，暴露 hallucination 倾向。诚实处理三步：（i）报告虚构案例的具体内容；（ii）将方法定位收窄至"对元模式适用单元格有效，对空缺单元格 hallucinate"；（iii）讨论矩阵机制加元模式归类是否需要增加"该单元格不适用"的明确豁免选项。

### 10.7 方法局限性

1. GT 不完备性与专家维度弱化：源汇聚不保证完备，所有方法的 Recall 可能被低估。源 2 收敛为"2–3 位行业专家做纯二元 yes/no/unsure 判断"（不识别、不补漏、不分析），目的是把专家任务降到最低认知负荷与最低任务解释成本，使招募现实可行。代价是丧失"专家独立识别"带来的发现性维度，专家信号仅起多数决过滤器作用。源 3 强化（双跨家族 LLM 各 N=10 重复）与源 4（团队三角化 Cohen's κ ≥ 0.75）补偿候选 MR 的多样性。新颖 MR 由源 3 与源 4 提供，由专家二元投票通过率决定是否纳入 G_final。
2. 方法适用边界：仅适用于规约中含明确数学/物理方程的科学计算软件。对纯字符串处理、UI 交互等无方程程序，本方法不适用，这是设计目标范围限制，不是失效。H6 反向验证从 12 程序内部检验该边界。
3. 元模式作为先验对比操作化指南的 construct validity 局限：五元模式 P1–P5 来源于团队基于 1998–2025 年文献的归纳 [Anonymous, under review]。本论文不声称元模式具有"先验"性质，仅声称其作为操作化指南有效。
4. LLM 幻觉：Cho 等（ICSME 2025）报告平均假阳性率 38% [Cho2025]。本方法假阳性控制依赖输出 `physics_basis` 与 `falsifiability` 字段，加 §6.4 自动化分流验证作客观二次过滤。
5. 变异测试缺位：v4 不含变异测试，"恢复 MR 能检测真实缺陷"的端到端因果链需期刊扩展版工作填补。当前以 AVR 加 Li Meng (ANE 2021) 团队既有 NUIT 变异验证证据作为间接支撑。
6. 自动化分流验证范围：v4 落地 P2/P5/P4 与 P1 约束验证（部分），P3 GEP 符号回归留为未来工作。

### 10.8 为什么这是 Information Recovery 而非 Prompt Engineering

本工作属于 information recovery 范式而非 prompt engineering，依据是四点结构性证据：
- 方法骨架与 LLM 解耦：(i) 元模式、(iii) 三源 GT、(iv) 分流验证三组件与 LLM 完全无关，仅 (ii) 矩阵填充阶段使用 LLM；团队 [MLD-v2] 内部技术报告已实施 GEP 替代 LLM 实例（NUIT 程序上 17 条 P1 MR、9 条 P3 MR）。
- 输入是软件制品，输出是测试规约：四类制品输入到形式化 MR 输出，LLM 既不是输入也不是输出的所有者。
- 评估指标围绕恢复质量：Recall（GT 完备度）、AVR（恢复 MR 的可执行性）、单元格 ρ（恢复的语义边界）等指标全部度量"被恢复信息的保真度与可用性"，而非 prompt engineering 的典型指标（生成多样性、token 效率）。
- 贡献对 LLM 升级具有内禀稳定性：矩阵遍历机制加按元模式分流的验证管线对底层 LLM 升级稳定。基础模型变强只会降低 LLM 桥梁失败率，不会废止矩阵或分流验证的必要性。

诚实声明：上述论断不主张元模式本身具有跨范式先验性。元模式作为"先验"对比"操作化指南"的差异详 §1.3 H1 与 §10.7 局限性 3。

---

## 十一、实验执行计划

### 11.1 阶段规划

| 阶段 | 任务 | 时间 | 交付物 |
|---|---|---|---|
| P0a | 12 程序选择确认 + 制品摄入接口开发 | 2 周 | 12 程序运行环境 |
| P0b | 三源 GT 构建（12 程序）| 4 周 | 标注完整的 G_final |
| P0c | 跨范式非平凡 codebook 校准 | 1 周 | codebook 定稿 + κ ≥ 0.75 报告 |
| P1 | 提示词开发（4 消融 + 3 基线）+ 预实验 temperature 校准 | 2 周 | 提示词模板 + T=0.5 校准报告 |
| P2 | 主实验（6720 次主调用）| 8 周 | A0/A3/A4/A6 + B1/B2/B2″ 完整数据 |
| P3 | AVR 自动验证管线开发 + 执行 | 2 周 | AVR 管线 + 表 5 数据 |
| P4 | H6 元模式空缺单元格分析 | 1 周 | 表 6 数据 |
| P5 | 综合分析 + 论文写作 | 3 周 | 实验结果 + 论文初稿 |
| P6 | 投稿前合规审查 | 0.5 周 | 投稿包 |

总周期约 18 周（合 4–5 个月）。关键里程碑：
- 2026-06 底完成 P0–P1（GT、codebook、提示词）。
- 2026-09 中完成 P2–P5（主实验、AVR、H6、论文初稿）。
- 2026-09 中下旬提交 SANER 2027。

### 11.2 数据记录规范

每次 LLM 调用记录 JSON 格式数据包：

```json
{
  "experiment_id": "exp_v4_20260715_a6_a1_claude47_n07",
  "config": {
    "variant": "A6",
    "program": "A1_Lorenz",
    "paradigm": "numerical",
    "llm": "Claude_Opus_4.7",
    "temperature": 0.5,
    "random_seed": 7,
    "prompt_token_count": 3247,
    "concept_coverage": "18/18"
  },
  "output": {
    "mr_list": [...],
    "raw_response": "...",
    "response_token_count": 1820
  },
  "evaluation": {
    "matched_mrs": 12,
    "total_output": 18,
    "total_gt": 22,
    "precision": 0.667,
    "recall": 0.545,
    "f1": 0.600,
    "fpr": 0.333,
    "recall_nt": 0.500,
    "recall_trivial": 0.700,
    "avr_pass": 8,
    "avr_total_dispatchable": 12,
    "avr_rate": 0.667,
    "cell_distribution": {"P1": 5, "P2": 4, "P3": 3, "P4": 2, "P5": 4}
  },
  "metadata": {
    "timestamp": "2026-07-15T14:32:18Z",
    "rater_a": "Meng",
    "rater_b": "MasterA",
    "kappa": 0.81
  }
}
```

---

## 十二、预期贡献

1. 概念贡献：首次将"MR 获取"重新形式化为 MR 信息恢复问题（MR Information Recovery Problem），即从方程手册、源码、I-O 域规约、专家知识四类软件制品中恢复可验证 MR，并把它嵌入 SANER 的 program comprehension 与 information recovery 议题谱系。

2. 方法贡献：提出以蜕变关系元模式作为跨制品语义先验的恢复方法 MetaPrompt，包含三部分：(i) 参数 × 元模式恢复矩阵的强制遍历机制；(ii) 按元模式分流到 Wilcoxon、DTW、约束验证的自动化恢复-验证耦合；(iii) 与 LLM 解耦的方法骨架。

3. 实验设计贡献：
   - 三源独立汇聚 GT 构建方法，破循环论证。
   - 跨 4 范式 12 程序的实验设计，论证方法的跨范式通用性（H5）。
   - H6 反向假设的元模式空缺单元格分析，提供 false-when-out-of-scope 的可证伪证据。
   - 跨范式非平凡 MR 评审 codebook，提供可复现标注准则。

4. 闭环验证贡献：建立从软件制品到 MR 恢复再到自动化分流验证的端到端管线，把 MR 评估从"恢复多少条"提升到"客观可验证"。

5. 实证贡献：在 12 个开源科学计算程序（覆盖数值模拟、概率程序、代理模型、机器学习 4 范式）上的大规模实验：4 主流 LLM（国外 2、国内 2）× 4 消融 × 3 基线 × N=20，共 6720 次主实验调用，加 240 次预实验（GSD 早停后实测约 5800 次）。

6. 可复现基础设施：公开提示词模板、四类制品摄入接口、12 程序 GT 数据集、跨范式非平凡 codebook、自动化分流验证脚本，作为 SANER 社区 MR 信息恢复方向的可复用基础设施。

---

## 参考文献

- [Anonymous, under review] 团队元模式理论论文（暂以匿名/审稿中形式占位）
- [Li2024-TOSEM] Li R, Liu H, Poon PL, et al. *Metamorphic Relation Generation: State of the Art and Research Directions.* ACM Transactions on Software Engineering and Methodology, 2025. doi:10.1145/3708521.
- [Towey2025] Ying L, Towey D, et al. *Metamorphic Relation Patterns for Metamorphic Testing, Exploration and Robustness.* Software Testing, Verification and Reliability, 2025. doi:10.1002/stvr.70003.
- [Luu2023] Luu QH, Liu H, Chen TY. *Can ChatGPT advance software testing intelligence?* arXiv:2310.19204, 2023.
- [Shin2024] Shin SY, Pastore F, Bianculli D, et al. *Towards Generating Executable Metamorphic Relations Using Large Language Models.* In: Quality of Information and Communications Technology (QUATIC 2024), Springer CCIS vol. 2178, 2024. doi:10.1007/978-3-031-70245-7_9.
- [Bose2025] Bose DB, et al. *LLMs in Debate: Does Arguing Make Them Better at Detecting Metamorphic Relations?* In: Proc. 1st Int'l Workshop on Agentic Software Engineering (AgenticSE) co-located with ASE 2025. IEEE Xplore document 11334553.
- [Zhang2025-SANER] Zhang J, Sun C-A, Liu H, Dong S. *Can Large Language Models Discover Metamorphic Relations? A Large-Scale Empirical Study.* In: Proc. IEEE Int'l Conf. on Software Analysis, Evolution and Reengineering (SANER), 2025, pp. 24–35. doi:10.1109/SANER64311.2025.00011.
- [Segura2016] Segura S, Fraser G, Sanchez AB, Ruiz-Cortés A. *A Survey on Metamorphic Testing.* IEEE TSE, 2016.
- [Chen2018] Chen TY, et al. *Metamorphic Testing: A Review of Challenges and Opportunities.* ACM Comp. Surveys, 2018.
- [Cho2025] Cho S, Ruberto S, Terragni V. *Metamorphic Testing of Large Language Models for Natural Language Processing.* In: Proc. IEEE Int'l Conf. on Software Maintenance and Evolution (ICSME), 2025. IEEE Xplore document 11185922.
- [Chen2016] Chen TY, et al. *METRIC: METamorphic Relation Identification based on the Category-choice framework.* JSS, 2016.
- [Sun2018] Sun C-A, Fu A, Poon P-L, Xie X, Liu H, Chen TY. *METRIC+: A Metamorphic Relation Identification Technique Based on Input Plus Output Domains.* IEEE Transactions on Software Engineering, 2021, 47(9): 1764–1785. doi:10.1109/TSE.2019.2934848.
- [Blasi2021] Blasi A, et al. *MeMo: Automatically Identifying Metamorphic Relations in Javadoc Comments for Test Automation.* JSS, 2021.
- [Xu2024] Xu C, et al. *MR-Scout: Automated Synthesis of Metamorphic Relations from Existing Test Cases.* TOSEM, 2024.
- [Kanewala2013] Kanewala U, Bieman JM. *Using machine learning techniques to detect metamorphic relations for programs without test oracles.* ISSRE 2013.
- [Hardin2018] Hardin B, Kanewala U. *Using semi-supervised learning for predicting metamorphic relations.* MET 2018.
- [Zhang2019] Zhang B, et al. *AutoMR: Automatic Discovery of Metamorphic Relations.* ICSE 2019.
- [Wen2022] Wen X, et al. *SPSS: A Statistical Pattern-based Search System for Discovering Metamorphic Relations.* 2022.
- [Xie2011] Xie X, Ho J, Murphy C, et al. *Testing and validating machine learning classifiers by metamorphic testing.* Journal of Systems and Software, 2011, 84(4): 544–558.
- [Strogatz2018] Strogatz SH. *Nonlinear Dynamics and Chaos: With Applications to Physics, Biology, Chemistry, and Engineering.* 2nd ed. CRC Press, 2018.
- [Yan2025-STVR] Yan L, Zhu H, et al. *Metamorphic Testing on Scientific Programs for Solving Second-Order Elliptic Differential Equations.* Software Testing, Verification and Reliability, 2025. doi:10.1002/stvr.1912.
- [Dutta2018] Dutta S, et al. *Testing probabilistic programming systems.* In: Proc. ESEC/FSE 2018.
- [Forrester2008] Forrester A, Sóbester A, Keane A. *Engineering Design via Surrogate Modelling: A Practical Guide.* Wiley, 2008.
- [Murphy2008] Murphy C, et al. *Properties of machine learning applications for use in metamorphic testing.* SEKE 2008.
- [Murphy2012] Murphy KP. *Machine Learning: A Probabilistic Perspective.* MIT Press, 2012.
- [Caflisch1998] Caflisch RE. *Monte Carlo and quasi-Monte Carlo methods.* Acta Numerica, 1998.
- [Lemieux2009] Lemieux C. *Monte Carlo and Quasi-Monte Carlo Sampling.* Springer, 2009.
- [Salimans2015] Salimans T, Kingma DP, Welling M. *Markov Chain Monte Carlo and Variational Inference: Bridging the Gap.* In: Proc. ICML 2015.
- [Xiu2003] Xiu D, Karniadakis GE. *Wiener-Askey polynomial chaos for stochastic differential equations.* SIAM J. Sci. Comput., 2003.
- [Sudret2008] Sudret B. *Global sensitivity analysis using polynomial chaos expansions.* RESS, 2008.
- [Hornik1991] Hornik K. *Approximation capabilities of multilayer feedforward networks.* Neural Networks, 4(2):251–257, 1991.
- [HookKelly2009] Hook D, Kelly D. *Testing for trustworthiness in scientific software.* In: Proc. ICSE Workshop on Software Engineering for Computational Science and Engineering (SECSE), 2009, pp. 59–64. IEEE Xplore document 5069163.
- [Dwarakanath2018] Dwarakanath A, et al. *Identifying implementation bugs in machine learning based image classifiers using metamorphic testing.* In: Proc. ISSTA 2018.
- [Liang2021] Liang Z, Jiang B, Chan WK. *Towards effective metamorphic testing by algorithm stability for linear classification programs.* Journal of Systems and Software, 2021, 178: 110980. doi:10.1016/j.jss.2021.110980.
- [Hiremath2021] Hiremath DJ, Claus M, Hasselbring W, Rath W. *Towards Automated Metamorphic Test Identification for Ocean System Models.* In: Proc. IEEE/ACM 6th Int'l Workshop on Metamorphic Testing (MET), 2021. IEEE Xplore document 9477689 / arXiv:2103.09782.
- [Luu2022] Luu Q-H, Liu H, Chen TY, Vu HL. *Testing Ocean Software with Metamorphic Testing.* In: Proc. 7th Int'l Workshop on Metamorphic Testing (MET 2022), 2022. doi:10.1145/3524846.3527341.
- [LiMeng2021] Li M. *基于蜕变关系的两阶段验证方法研究.* 南华大学博士论文, 2021.
- [LiMeng2021-ANE] Li M, Wang L, Yue W, et al. *Metamorphic testing of the NUIT code based on burnup time.* Annals of Nuclear Energy, 2021, 153: 108027.
- [LiMeng2020-IJPE] Li M, Wang L, Yan S, et al. *Metamorphic relation generation for physics burnup program testing.* International Journal of Performability Engineering, 2020, 16(2): 297–306. doi:10.23940/ijpe.20.02.p12.297306.
- [Zhao2026] Zhao Y, Li M, Zhang K, et al. *Verification of multi-scale coupling program for high temperature gas-cooled reactor based on metamorphic testing.* Annals of Nuclear Energy, 2026, 226: 111846. doi:10.1016/j.anucene.2025.111846.
- [LiMeng2022-FER] Li M, Yang X, Yan S, et al. *A lightweight verification method based on metamorphic relation for nuclear power software.* Frontiers in Energy Research, 2022, 10: 788753. doi:10.3389/fenrg.2022.788753.
- [Fagan1976] Fagan ME. *Design and code inspections to reduce errors in program development.* IBM Systems Journal, 1976.
- [Kanewala2016] Kanewala U, Bieman JM, Ben-Hur A. *Predicting metamorphic relations for testing scientific software: a machine learning approach using graph kernels.* STVR, 2016.
- [MLD-v2] 团队内部技术报告：MetaPattern-LLM-DataDriven Framework v2，2026.

---

## 附录 A：v3.4 → v4 修订对照表

| 维度 | v3.4 | v4 | 变更原因 |
|---|---|---|---|
| 实验对象 | PWR 五层方程（1 程序）| 12 程序 × 4 范式 | 论证方法跨范式通用性 |
| LLM | Claude Opus 4 / GPT-4o / Gemini 2.5 Pro / GLM-4-Plus | Claude Opus 4.7 / ChatGPT 5.5 / DeepSeek-V4 / GLM-5 | 模型升级 + 国外 2 + 国内 2 平衡 |
| 消融 | A0–A6（7 档）| A0/A3/A4/A6（4 档）| 增量小档非独立 |
| 基线 | B1/B2/B2′/B2″/B3/B4（6 档）| B1/B2/B2″（3 档）| B2′ 切分不干净；B3 PWR-only；B4 单点价值低 |
| 假设 | H1–H4 | H1–H6（含 H5 跨范式 + H6 元模式空缺反向）| 增加跨范式与反向证伪证据 |
| 主指标 | F1 + MKR | F1 + AVR（删 MKR）| 变异测试投入产出比极低 |
| 变异测试 | 30–40 变异体 + 10 天集群 | 已删除 | 强绑定单一程序，与跨范式策略冲突 |
| GT 协议 | PWR 专家 ≥ 3 + Fleiss κ ≥ 0.65 + 复杂 pre-screening | 2–3 位行业专家纯二元 yes/no/unsure 判断 + 团队三角化（Cohen's κ ≥ 0.75）+ 跨家族 LLM 强化 | 通用程序 MR 边界更清晰，简化协议足够 |
| 总 LLM 调用 | 930（GSD 后 790）| 6960（GSD 后 5800）| 12 倍程序数 + 跨范式扩展 |
| N | 20 | 20 | 不变 |
| 方法定位 | 安全关键科学计算 | 含数学/物理方程规约的科学计算软件 | 坦诚承认适用边界 |
| 范式 C 内部异质性 | C1 GPR + C2 PCE + C3 Kriging（C1/C3 在 Bayesian 视角下数学等价）| C1 GPR + C2 PCE + C3 NN-Surr | 增强范式内子方法独立性，覆盖核方法、正交基、神经网络三条独立路径，堵审稿人"3 程序实质 2 证据"攻击点 |
| 投稿目标 | SANER 主推 / FSE 备选 | SANER 主推 | 篇幅压缩匹配 SANER 10 页 |
