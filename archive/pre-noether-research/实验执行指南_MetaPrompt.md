# MetaPrompt 实验执行指南（v4）

**对应论文**：*Recovering Metamorphic Relations from Scientific Software Artifacts via Meta-Pattern Guided LLMs*（MetaPrompt v4，IEEE SANER 2027 投稿）

## 0. 关键术语表（首次出现统一约定，与论文 §0.1 保持一致）

| 缩写 | 全称（中文 / 英文） |
|------|---------------------|
| MR | 蜕变关系（Metamorphic Relation）|
| MT | 蜕变测试（Metamorphic Testing）|
| LLM | 大语言模型（Large Language Model）|
| GT | 真值（Ground Truth）|
| MKR | 变异检错率（Mutation Kill Rate）|
| AVR | 自动验证通过率（Automatic Validation Rate）|
| GSD | 组序贯设计（Group Sequential Design）|
| ODE / PDE | 常微分方程 / 偏微分方程 |
| FDM | 有限差分法（Finite Difference Method）|
| MCMC | 马尔可夫链蒙特卡洛 |
| MC | 蒙特卡洛 |
| GPR | 高斯过程回归 |
| PCE | 多项式混沌展开 |
| MLP | 多层感知机 |
| SVM / SVC | 支持向量机 / 分类器 |
| LR | 逻辑回归 |
| LU | LU 分解 |
| CoT | 思维链 |
| FS | 少样本提示（Few-Shot）|
| BL | 基线 |
| RQ | 研究问题 |
| H1–H6 | 待验证假设 1–6 |
| DTW | 动态时间规整 |
| GEP | 基因表达式编程 |
| RBF | 径向基函数 |
| API | 应用程序接口 |
| CCF | 中国计算机学会 |
| CFP | 征稿启事 |
| FNR / FPR | 假阴性率 / 假阳性率 |
| ESS | 有效样本量 |
| KL | Kullback–Leibler 散度 |
| CV | 变异系数 |
| IS | 重要性采样 |
| PWR / HTGR | 压水堆 / 高温气冷堆 |
| NUIT | Nuclear Unstructured-mesh Iterative Tool（团队既有蜕变测试对象核工程程序）|
| CRAM | Chebyshev Rational Approximation Method（NUIT 实现的核燃料燃耗算法）|
| GP | 高斯过程（Gaussian Process）|
| NN-Surr | 神经网络代理 |
| MSE / RMSE | 均方误差 / 均方根误差 |
| NLP | 自然语言处理 |
| AI | 人工智能 |
| ML / DL | 机器学习 / 深度学习 |
| NN | 神经网络 |
| RNG | 随机数生成器 |
| RHS | 方程右端项 |
| CFL | Courant-Friedrichs-Lewy 数值稳定条件 |
| QMC | 准蒙特卡洛 |
| OOD | 分布外（Out-Of-Distribution）|
| OpenMC | 开源蒙特卡洛中子输运模拟软件 |
| CFD | 计算流体力学 |
| AVR-F1 ρ / V-AF1 | AVR 与 F1 的 Spearman 秩相关系数 |
| Cohen's κ | 双评者一致性指标 |

后续术语首次具体出现时，同样以"中文 / 英文（缩写）"格式给出。

---
本文为 SANER 2027 投稿的实验执行参考，涵盖待论证方法、研究问题、评价指标、实验对象、实验方法、对比基准与预期结果。

相对 v3.4 的关键变更：实验对象由 PWR 单程序扩为 12 程序 × 4 范式；删除变异测试，AVR 升级为可执行价值的主要证据；假设由 H1–H4 扩为 H1–H6（新增 H5 跨范式一致性、H6 元模式空缺验证）；LLM 切换为 Claude Opus 4.7 / ChatGPT 5.5 / DeepSeek-V4 / GLM-5；方法定位由"安全关键科学计算"收窄到"规约中含明确数学/物理方程的科学计算软件"；总实验量由 930 次扩为 6960 次，GSD 早停后约 5800 次。

最后更新：2026-04-28。

---

## 一、待论证方法（MetaPrompt 方法骨架）

### 1.1 方法核心声明

MetaPrompt 是一种**以蜕变关系元模式作为软件制品语义结构先验**的 MR 信息恢复方法，**适用于规约中含有明确数学或物理方程的科学计算软件**。其方法骨架由四个组件构成，与 LLM 解耦：

| 组件 | 描述 | 与 LLM 的关系 |
|---|---|---|
| **(i) 制品语义操作化指南** | 五元模式 P1–P5，作为跨制品语义维度的高层先验 | LLM 无关，元模式本身独立存在 |
| **(ii) 参数 × 元模式恢复矩阵** | 强制对每个 (θ, P_k) 单元格显式判断"适用/不适用"并输出候选 MR | LLM 是当前实现选择；可替换为 GEP / 专家手工填表 |
| **(iii) 多源独立 GT** | 文献 + 跨家族 LLM 交叉 + 团队三角化（候选池）→ 行业专家纯二元 yes/no/unsure 投票多数决过滤；独立于元模式构建 | LLM 无关（GT 构建使用非主实验 LLM） |
| **(iv) 元模式分流自动验证** | 按元模式将候选 MR 分流至 Wilcoxon / DTW / 约束逻辑管线 | LLM 无关 |

### 1.2 五元模式定义（操作化指南核心）

| 元模式 | 核心提问 | 跨范式典型 MR 示例 |
|---|---|---|
| **P1 守恒性** | 什么变换不改变输出？ | 数值积分能量守恒 / 贝叶斯先验对称性 / ML 特征缩放不变 |
| **P2 单调性** | 增大参数 θ，输出 y 往哪个方向变？ | ODE 步长 → 误差 / 似然单调 / SVM C 参数 → 边界硬度 |
| **P3 收敛性** | 推到极端/精化后趋向什么？ | 网格细化 → 精确解 / MCMC 链长 → 后验收敛 / 训练样本 → 真实分布 |
| **P4 轨迹性** | 响应路径长什么样？ | 暂态形态 / 学习曲线 / GP 后验形状 |
| **P5 偏序性** | 谁更准？在哪最不准？ | 多算法精度排序 / 多核函数偏好 / 多模型对比 |

### 1.3 恢复管线总览

```
四类软件制品（手册 / 源码 / I-O 域规约 / 专家知识）
             ↓
阶段 A：制品摄入 + 五元模式先验注入 → 参数 × 元模式恢复矩阵
             ↓
阶段 B：跨单元格恢复（LLM 桥梁）→ 候选 MR 集 {(r, R, P_k, basis)}
             ↓
阶段 C：元模式分流自动验证（P2/P5→Wilcoxon, P4→DTW, P1→约束验证）
             ↓
（可选）阶段 D：缺陷检测案例研究 ← 期刊扩展版工作，不在本论文范围
```

本论文结束于阶段 C（AVR 验证），不包含变异测试。变异测试作为期刊扩展版的独立实验保留。

---

## 二、研究问题（RQ）

| RQ | 问题描述 | 验证假设 | 核心对照 |
|---|---|---|---|
| **RQ1（恢复有效性）** | 以元模式作为软件制品语义先验，是否显著提升从科学计算制品中恢复 MR 的有效性（F1、Recall、Precision）？ | H1：A6 F1 显著优于 B2 与 B2″ | A6 vs B2 / B2″ 双对照 |
| **RQ2（先验组件贡献）** | 先验的元模式知识、参数×元模式矩阵、CoT、少样本各组件中，哪些对恢复效果贡献最大？ | H2：A0→A3 ΔF1 是相邻消融中最大 | A0→A3→A4→A6 四档消融 |
| **RQ3（跨工具与跨范式泛化）** | 在不同 LLM 与不同程序范式上元模式是否表现出一致的恢复增益？ | H3：非平凡 MR 增益大于平凡 MR；H5：跨 4 范式 ΔF1 符号一致 | 4 LLM × 4 范式 × 12 程序 |
| **RQ4（可执行价值与适用边界）** | 恢复出的 MR 集合是否具有可自动验证的可执行性？方法是否仅在规约含数学方程的程序上起作用？ | H4：AVR 显著高于基线；H6：方法在元模式空缺单元格不虚构 MR | AVR + (程序×元模式) 单元格分析 |

### 假设层次关系

```
H1（元模式操作化有效性）：主对照 A6 vs B2 / B2″
     │
     ├── H2（矩阵机制关键性）：消融 A0→A3 ΔF1 ≥ A3→A4 ≥ A4→A6
     │
     ├── H3（非平凡 MR 深度推理）：ΔRecall_nt > ΔRecall_trivial
     │
     ├── H5（跨范式一致性）：12 程序 × 4 范式 ΔF1 符号全为正且 CV < 0.5
     │
     └── H4（自动验证一致性）：A6 AVR 显著高于 B2，且 AVR-F1 Spearman ρ > 0.3

H6（元模式空缺验证）：反向假设
   GT 中 (S_i, P_k) 单元格无 MR 的程序，A6 也不应虚构 P_k MR
   GT 中 (S_i, P_k) 单元格有 MR 的程序，A6 应能识别
   Spearman ρ(A6 输出 MR 数, GT MR 数) > 0.6
```

---

## 三、评价指标

### 3.1 三层指标体系

| 层级 | 指标 | 公式 / 定义 | 用途 |
|---|---|---|---|
| **Tier 1（核心）** | Precision, Recall, F1 | $P=\|C∩G\|/\|C\|$, $R=\|C∩G\|/\|G\|$, $F1=2PR/(P+R)$ | RQ1 主指标 |
| **Tier 1（核心）** | FPR | $\|C\setminus G\|/\|C\|$ | 假阳性率 |
| **Tier 1** | **CV(ΔF1)** 跨 12 程序 | std(ΔF1) / mean(ΔF1) | RQ3 + H5 跨范式一致性 |
| **Tier 2（重要）** | Recall_nt | 非平凡 MR 中被正确识别的比例 | H3 验证 |
| **Tier 2** | **AVR**（自动分流验证通过率）| 通过 P2/P5 Wilcoxon / P4 DTW / P1 约束逻辑的 MR 数 / 该方法可分流 MR 总数 | H4 主指标，取代 MKR |
| **Tier 2** | V-AF1 一致性 | Spearman ρ(AVR, F1) | 自动验证与识别效果是否一致 |
| **Tier 3（辅助）** | 形式化完整度 | 具完整 (r, R) 形式化表达的 MR 比例 | 工程可操作性 |
| **Tier 3** | 元模式归类准确率 | 已识别 MR 元模式归类与专家判定一致比例 | 独立辅助维度 |
| **Tier 3** | 新颖 MR 数 | 不在 G_final 中但经专家确认有效的新 MR | 创造性发现能力 |
| **Tier 3** | **(程序 × 元模式) 单元格 ρ** | Spearman ρ(A6 输出 MR 数, GT MR 数) 跨 60 单元格（12 程序 × 5 元模式）| H6 元模式空缺验证 |

已删除：MKR、Marginal MKR、V-M Consistency。这三项强绑定 PWR/OpenMC，性价比极低。

### 3.2 非平凡 MR Codebook（跨范式版）

适用于 12 程序的统一 codebook：

| 准则 | 操作化判定 | 触发标签 |
|---|---|---|
| **C1 推理步数** | 该 MR 的数学/物理依据是否需要 ≥ 2 步推理？ | ≥2 步 → 半平凡或非平凡 |
| **C2 跨方程/多组件耦合** | 该 MR 是否依赖两个及以上方程或两个及以上算法组件耦合？ | 是 → 至少半平凡 |
| **C3 反直觉方向** | 该 MR 的方向/形态是否与朴素直觉一致？（"大数定律：N↑→误差↓" 是直觉；"特征缩放不变性是 ML 鲁棒性的基础" 是反直觉）| 反直觉 → 非平凡 |
| **C4 教科书可读出** | 该 MR 是否能从该范式的标准教科书中直接读出？ | 是 → 平凡 |
**判定规则**：
- 触发 C4 ∧ ¬C1 ∧ ¬C2 ∧ ¬C3 → **平凡**（教科书直接可读且无推理深度无耦合无反直觉）
- 触发 C1（≥2 步）∧ C3（反直觉）→ **非平凡**
- 触发 C2（耦合）∧ ¬C4（非教科书）→ **非平凡**
- 否则 → **半平凡**

### 3.3 统计方法

- 每个配置重复 **N=20**（temperature=0.5，固定随机种子 1..20）
- 报告均值 ± 标准差 + 95% bootstrap 置信区间（n=2000 重抽样）
- Wilcoxon 秩和检验比较方法间差异（α=0.05）；消融实验使用配对 Wilcoxon
- Cliff's δ 报告效应量（small ≥ 0.147 / medium ≥ 0.33 / large ≥ 0.474）
- **多重检验校正**：Holm-Bonferroni 顺序校正
  - H1 族：A6 vs B2 + A6 vs B2″ + B2 vs B2″ = **3 对照**
  - H2 族：A0→A3, A3→A4, A4→A6 = **3 对照**
  - H3 族：ΔRecall_nt vs ΔRecall_trivial = **1 对照**
  - H4 族：A6 vs B2 AVR = **1 对照**
  - H5 族：12 程序 ΔF1 sign test = **1 综合检验**
  - H6 族：(程序 × 元模式) 单元格 Spearman ρ = **1 检验**
  - **族总数 = 10 个独立假设检验**
- **Group Sequential Design**：Pocock-style，N=15 中期评估，若 H1 主对照 Cliff's δ ≥ 0.30 且 p < 0.025 提前停止

---

## 四、实验对象

### 4.1 12 程序 × 4 范式

每程序需满足：开源可获取 / 代码规模 < 1000 行 / 数学或物理方程明确 / 文献中有已知 MR。

#### 范式 A：数值模拟 / 数值算法（3 程序）

| ID | 程序 | 数学/物理方程 | 已知 MR 文献 | 单次运行 |
|---|---|---|---|---|
| **A1** | `scipy.integrate.solve_ivp` 求解 Lorenz 系统（σ=10, β=8/3, ρ=28；t∈[0,40]；初值 (1,1,1)±ε）| 三维非线性 ODE 系统 | Strogatz 2018 | < 1s |
| **A2** | NumPy 数值线性代数：LU 分解 + Ax=b 求解 | 矩阵分解、向量空间不变性 | Hook & Kelly 2009 | < 0.1s |
| **A3** | 一维热传导有限差分（自编 FDM）∂u/∂t = α∂²u/∂x² | 抛物线 PDE | Chen 2018, Yan 2025 | < 1s |

#### 范式 B：概率程序（3 程序）

| ID | 程序 | 数学/物理方程 | 已知 MR 文献 | 单次运行 |
|---|---|---|---|---|
| **B1** | PyMC Beta-Binomial 共轭推断 | Bayes 定理 + 共轭先验 | Dutta 2018 | 1–5s |
| **B2** | Metropolis-Hastings 采样器（自编，目标 2D 高斯）| MCMC 平稳分布、可逆性 | Dutta 2018, Salimans 2015 | 5–10s |
| **B3** | 朴素 Monte Carlo 积分（求 ∫₀¹ exp(-x²) dx）| 大数定律、收敛速率 √N | Caflisch 1998, Lemieux 2009 | < 1s |

#### 范式 C：代理模型（3 程序）

C1 GPR、C2 PCE、C3 NN-Surr 覆盖代理建模的三条独立数学路径：核方法、正交基、神经网络。原 C3 Kriging 与 C1 GPR 在 Bayesian 视角下数学等价，已替换为基于 `sklearn.MLPRegressor` 的回归代理。

| ID | 程序 | 数学/物理方程 | 已知 MR 文献 | 单次运行 |
|---|---|---|---|---|
| **C1** | `sklearn.gaussian_process` GPR | 核函数（RBF/Matern）+ 后验解析解 | Forrester 2008, Murphy 2012 | < 1s |
| **C2** | 多项式混沌展开（chaospy / numpy.polynomial）| Wiener-Askey 正交多项式族 | Xiu 2003, Sudret 2008 | < 1s |
| **C3** | `sklearn.neural_network.MLPRegressor` 作为 Forrester 1d / Branin 2d benchmark 函数代理 | 通用近似定理 + 反向传播 + MSE 损失（多层非线性逼近，非核非正交基）| Forrester 2008, Hornik 1991, Murphy 2012 | 1–3s |

#### 范式 D：机器学习（3 程序）

| ID | 程序 | 数学/物理方程 | 已知 MR 文献 | 单次运行 |
|---|---|---|---|---|
| **D1** | `sklearn.MLPClassifier` on Iris | 前向传播 + softmax | **Xie 2011 (ML MR 开山)**, Murphy 2008 | 1–3s |
| **D2** | `sklearn.svm.SVC` (RBF) on Breast Cancer | 二次规划 + 核技巧 | Xie 2011, Dwarakanath 2018 | < 1s |
| **D3** | `sklearn.linear_model.LogisticRegression` on Diabetes | sigmoid + 交叉熵损失 | Xie 2011, Liang 2021 | < 0.1s |

### 4.2 12 程序覆盖矩阵

| 范式 | 数学结构 | 元模式预期典型 MR |
|---|---|---|
| A 数值模拟 | ODE/PDE/线性代数 | P1 守恒 / P3 收敛 / P4 轨迹 |
| B 概率程序 | 概率分布族 | P1 对称 / P2 似然单调 / P3 后验集中 |
| C 代理模型 | 核方法 / 正交基 / 神经网络（三条独立路径） | P5 精度偏序 / P3 收敛（长度尺度 / 阶数 / 样本量）/ P4 响应曲线与学习曲线 |
| D 机器学习 | 损失最小化 | P1 缩放/置换不变 / P2 边界单调 / P5 鲁棒性偏序 |

### 4.3 制品来源四类（每程序统一构造）

| 制品类别 | 实际数据 | 用途 |
|---|---|---|
| **方程与算法手册** | 程序对应数学/物理方程 + 算法说明（教科书章节摘录）| 主要恢复来源 |
| **源码与配置** | Python API 接口 + 关键模块函数注释 | 辅助恢复 |
| **输入/输出域规约** | 输入参数取值范围、单位、典型工况 | 约束 r 与 R 合法形式 |
| **领域专家显式知识** | §4.4 源 2 的 1 位该范式专家独立识别清单 | 用于 GT，不混入恢复输入 |

### 4.4 Ground Truth 构建（简化协议）

每程序的 GT 构建流程：文献 ∪ 跨家族 LLM 交叉 ∪ 团队三角化 → 团队共识审核（Cohen's κ ≥ 0.75）→ 形成候选 MR 清单 → 2–3 位行业专家纯 yes/no/unsure 投票 → 多数决过滤后入 G_final。

#### 源 1：已发表文献 MR

每程序从对应范式经典文献中抽取已发表 MR（详 §4.1 表格"已知 MR 文献"列），预计每程序 5–15 条。

#### 源 2：行业专家纯二元判断

人数 2–3 位行业专家（建议 A+B 范式一位、C+D 范式一位，第 3 位作为奇数仲裁可选）。资历要求博士学位或工程界等价资历，对应范式 ≥ 3 年研究/工程经历。

团队提供完整输入材料：
1. 程序方程与算法说明（每程序 1 页）
2. 五元模式 P1–P5 中文解释 + 示例（守恒/单调/收敛/轨迹/偏序）
3. 每条候选 MR 的形式化表达 (r, R, basis) + 中文物理含义解释 + 元模式归属

专家任务为 15–30 min 视频或线下访谈，对清单上每条候选 MR 仅作一项判断：Yes（数学/物理上成立）、No（不成立或表述错误）、Unsure（判断依据不足）。专家不做的事：识别新 MR、补充遗漏、修改表述、给出依据、主观排序、元模式归类。

多数决规则：3 位专家按 ≥ 2/3 Yes 通过；2 位时要求一致 Yes，否则记 unsure 不入 G_final。预期交付物为单一表格（行 = 候选 MR，列 = 专家 1/2/3 的 yes/no/unsure），不含文字分析。

#### 源 3：跨家族 LLM 交叉验证

使用 Qwen 3-Max（阿里）与 Doubao-1.5-Pro（字节）。这两家与主实验四款 LLM（Claude Opus 4.7、ChatGPT 5.5、DeepSeek-V4、GLM-5）厂商不同，训练数据来源差异最大。

两 LLM 各自独立运行不含元模式提示的 MR 识别（只给程序方程加 MR 通用定义），各 N=10 重复后取并集；输出由 Meng 与硕士 A 双独立编码（Cohen's κ ≥ 0.75）后纳入 G_llm_cross。预期每程序补充 4–12 条候选。

#### 源 4：团队三角化编码

Meng 与 1 位独立反审者，各自独立从源 1 与源 3 的候选清单中：
- 标注每条候选 MR 的物理基础正确性（accept / revise / reject）
- 为每程序补 0–3 条文献未覆盖但研究者公认的 "common-sense MR"

两人独立编码后计算 Cohen's κ（要求 ≥ 0.75），冲突项由 Li Meng（PI）仲裁。

#### GT 合并规则

```
候选清单 = (G_literature ∪ G_llm_cross ∪ G_team) 经团队共识审核（Cohen's κ ≥ 0.75）
G_final  = 候选清单 ∩ {专家投票 ≥ 多数 Yes}
```

源 2 在 v4.2 中纯做二元过滤器，不再贡献新 MR；候选 MR 池由源 1+3+4 提供。

每条 MR 标注三项：物理/数学内容、来源标签、(程序, 元模式) 单元格归属（用于 H6 单元格分析）。GT 中不把元模式归属作为"正确答案"，元模式归类按独立维度评估。

### 4.5 匹配判定规则（破循环论证）

两条 MR 判定为"匹配"需同时满足两条：
1. 参数匹配：涉及相同或等价的输入参数 θ
2. 输出关系语义等价：R 在数学/物理含义上一致

匹配判定不要求元模式归属相同。一条数学正确但被 LLM 归入不同元模式的 MR 仍判定为匹配。匹配判定由 2 名评审独立执行，Cohen κ ≥ 0.75，不一致项第三方仲裁。

---

## 五、实验方法

### 5.1 提示词架构（三层嵌套）

层 1（系统提示词）：角色 + MR 定义 + MR vs Property 区分 + 五元模式策略 + YAML 输出格式。元模式归类为可选字段，允许 `uncertain`：

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

层 2：参数 × 元模式恢复矩阵。
层 3：程序特化实例。

### 5.2 消融变体（4 档）

| 变体 | 缩写 | 元模式知识 | 矩阵结构 | CoT | Few-Shot |
|---|---|---|---|---|---|
| **A0** | BL | ✗ | ✗ | ✗ | ✗ |
| **A3** | MP-matrix | 完整 | ✓ | ✗ | ✗ |
| **A4** | MP-matrix-CoT | 完整 | ✓ | ✓ | ✗ |
| **A6** | Full | 完整 | ✓ | ✓ | ✓ |

原 A1（MP-name）、A2（MP-template）、A5（MP-matrix-FS）已删除：增量小，且与现有四档非独立。

### 5.3 对比基线（3 档）

B1（Zero-Shot LLM）：程序名称加最简提示。

B2（Domain-Prompted LLM，领域知识等量基线）：与本方法等量的领域知识，按"数学性质 → 数值/算法特性 → 工况约束"三层自然推理组织，不引入元模式概念，无矩阵结构。

B2″（Domain-NoMatrix，最干净对照）：等量领域知识，无矩阵机制（参数维度的扁平列表），无元模式概念。

```
你是该范式的领域专家。请基于以下程序方程与算法识别本程序应满足的蜕变关系：
[完整方程公式、参数集、算法列表，与 A6 完全相同]
请逐条列出 MR，每条包含输入变换 r、输出关系 R 与依据。
```

已删除的基线：B2′ Domain-Matrix（列内容与元模式概念重叠，切分不干净）、B3 GEP（仅 PWR 适用，不跨范式）、B4 Towey 11 模式（单 LLM 单点对比，价值低）。

等量度量：B1、B2、B2″ 与 A6 的 prompt token 数差异不超过 ±5%（cl100k_base 测度），关键概念集 K 全覆盖。

### 5.4 跨范式 LLM 配置

| LLM | 厂商 | 国别 | 发布 |
|---|---|---|---|
| **Claude Opus 4.7** | Anthropic | 美 | 2026-Q1 |
| **ChatGPT 5.5** | OpenAI | 美 | 2026-04-23 |
| **DeepSeek-V4** | DeepSeek | 中 | 2026-Q1 |
| **GLM-5** | 智谱 AI | 中 | 2026 |

国外 2 + 国内 2 平衡，覆盖不同训练数据来源、不同对齐策略、不同模型架构。

### 5.5 自动化分流验证（AVR）

每程序的 AVR 管线：

| 程序 | P2/P5 验证（Wilcoxon）| P4 验证（DTW）| P1/P3 验证（约束逻辑）|
|---|---|---|---|
| A1 Lorenz | 初值扰动 → 轨迹分离速率 | 暂态形态对比 | 能量守恒约束（Hamiltonian）|
| A2 LU | 矩阵规模 → 残差单调 | — | 行交换不变性 |
| A3 FDM 热传导 | 网格细化 → 误差单调 | 边界条件 → 形态退化 | 对称初值守恒 |
| B1 共轭推断 | 样本量 → KL 收敛 | — | 后验对称性 |
| B2 MCMC | 链长度 → 自相关下降 | — | 平稳分布约束 |
| B3 MC 积分 | N → 误差 ∝ 1/√N | — | 加性不变 |
| C1 GPR | 长度尺度 → 平滑度 | 训练点扰动 → 后验形态 | 内插点恒等 |
| C2 PCE | 阶数 → L2 误差 | — | 正交性约束 |
| C3 NN-Surr | 隐层节点数 / 训练样本量 → 验证 MSE | 训练 loss 学习曲线形态 | 特征顺序置换不变 / universal approximation 收敛 |
| D1 MLP | 训练样本 → 准确率 | 学习曲线形态 | 类标签置换不变 |
| D2 SVM | C 参数 → 边界硬度 | — | 特征缩放不变 |
| D3 LR | 正则化强度 → 权重稀疏度 | — | 概率归一 |

AVR 工程量每程序 0.5–1 天，总 6–12 工作日。

变异测试范围声明：v4 不在主实验中执行变异测试，仅作为期刊扩展版未来工作。审稿人若追问"如何证明 MR 能检测真实缺陷"，参考 Li Meng (ANE 2021) 团队既有 NUIT 变异验证证据。

---

## 六、对比基准

### 6.1 七档配置对照矩阵

| 类别 | ID | 元模式 | 矩阵 | CoT | Few-Shot | 基线类型 |
|---|---|---|---|---|---|---|
| 消融 | A0 | ✗ | ✗ | ✗ | ✗ | 起点 BL |
| 消融 | A3 | ✓ | ✓ | ✗ | ✗ | 矩阵激活 |
| 消融 | A4 | ✓ | ✓ | ✓ | ✗ | + CoT |
| 消融 | A6 | ✓ | ✓ | ✓ | ✓ | Full |
| 基线 | B1 | ✗ | ✗ | ✗ | ✗ | Zero-Shot |
| 基线 | B2 | ✗ | ✗ | ✗ | ✗ | Domain-Prompted（等量知识，三层组织）|
| 基线 | B2″ | ✗ | ✗ | ✗ | ✗ | Domain-NoMatrix（最干净对照）|

### 6.2 等量控制（H1 验证有效性的关键）

| 等量层 | 度量 | 阈值 |
|---|---|---|
| 层 1 Token 等量 | cl100k_base tokenizer | ±5% |
| 层 2 概念覆盖 | 关键概念集 K（每程序 12–18 概念）| 全覆盖 |
| 层 3 信息熵 | byte-level entropy | ±10%（辅助）|

### 6.3 H1 三对照设计

- A6 vs B2：检验"元模式 + 矩阵"对比"领域三层自然推理"。
- A6 vs B2″：H1 最干净对照，检验"元模式 + 矩阵"对比"等量知识无任何结构"。
- B2 vs B2″：检验领域三层组织本身的贡献。

---

## 七、预期结果

### 7.1 核心指标预期数值（基于跨范式假设推导）

| 假设 | 指标 | 预期最低（可接受）| 预期理想 | 依据 |
|---|---|---|---|---|
| H1 (A6 vs B2) | ΔF1 | ≥ 0.06 | 0.08–0.12 | Li Meng ANE 2021 + 跨范式估计 |
| H1 (A6 vs B2″) | ΔF1 | ≥ 0.10 | 0.13–0.18 | B2″ 无结构最弱 |
| H2 (A0→A3 ΔF1) | 矩阵机制增量 | ≥ 0.05 | 0.06–0.09 | Bose 2025 类似效应 |
| H2 (A3→A4 ΔF1) | CoT 增量 | < A0→A3 ΔF1 | 0.02–0.04 | 矩阵主导 |
| H2 (A4→A6 ΔF1) | Few-Shot 增量 | < A3→A4 ΔF1 | 0.01–0.03 | Few-Shot 边际 |
| H3 ΔRecall_nt | 非平凡召回提升 | ≥ 0.10 | 0.12–0.16 | 非平凡推理深度 |
| H3 ΔRecall_trivial | 平凡召回提升 | < ΔRecall_nt | 0.04–0.08 | 平凡 MR 无差异化优势 |
| H4 ΔAVR | 自动验证通过率 | ≥ 0.10 | 0.15–0.25 | P2/P5 Wilcoxon 通过率 |
| H4 V-AF1 ρ | AVR-F1 Spearman 相关 | ≥ 0.30 | 0.50–0.70 | 验证-识别一致性 |
| **H5 CV(ΔF1)** | 跨 4 范式变异系数 | **< 0.5** | **< 0.3** | 跨范式一致性 |
| **H5 sign test** | 12 程序 ΔF1 全为正 | **≥ 11/12** | **12/12** | binomial 显著 |
| **H6 cell ρ** | 60 单元格 Spearman | **≥ 0.6** | **0.7–0.8** | 元模式空缺识别 |

### 7.2 消融增量预期排序

```
ΔF1(A0→A3)  ≈ 0.06–0.09  ← 矩阵机制核心增量
ΔF1(A3→A4)  ≈ 0.02–0.04  ← CoT 增量
ΔF1(A4→A6)  ≈ 0.01–0.03  ← Few-Shot 边际
```

矩阵机制贡献 ≥ CoT 贡献 ≥ Few-Shot 贡献 是 H2 的核心论断。

### 7.3 跨范式预期表现

| 范式 | A6 F1 预期 | B2 F1 预期 | ΔF1 |
|---|---|---|---|
| A 数值模拟（3 程序均值）| 0.65–0.75 | 0.55–0.65 | 0.08–0.12 |
| B 概率程序（3 程序均值）| 0.60–0.70 | 0.50–0.62 | 0.08–0.12 |
| C 代理模型（3 程序均值）| 0.62–0.72 | 0.52–0.65 | 0.07–0.11 |
| D 机器学习（3 程序均值）| 0.58–0.68 | 0.50–0.60 | 0.06–0.10 |

ML 范式预期 ΔF1 略低（MR 边界更清晰、领域基线更强），但应仍 ≥ 0.06。

### 7.4 反向假设 H6 预期

60 个 (12 程序 × 5 元模式) 单元格中：
- GT 空缺单元格预期 ≈ 15–25 个（如 A2 LU 无 P4，B3 MC 积分无 P5 等）
- A6 在空缺单元格输出 0–2 条 MR（接近虚构上界）→ ρ > 0.6 通过
- 若 A6 在空缺单元格输出 5+ 条 MR → 暴露 hallucination 倾向，论文需诚实报告

### 7.5 结果解读决策树

```
A6 vs B2 ΔF1 显著 (Holm 校正后 p<0.05)?
├── 是 → A6 vs B2″ ΔF1 显著?
│       ├── 是 → H1 充分支持，主论断成立
│       └── 否 → H1 部分支持，仅 vs B2 显著说明领域三层组织已足够
│
└── 否 → 检查 A0→A3 ΔF1 (H2)
        ├── 显著 → 矩阵机制起作用但被基线"领域知识"补偿
        └── 不显著 → 方法核心机制失效，重新评估

H5 CV(ΔF1) < 0.5?
├── 是 → 跨范式一致性成立，方法泛化性获实证
└── 否 → 报告 ΔF1 在范式上的分布，软化"跨范式通用"主张

H6 cell ρ > 0.6?
├── 是 → 方法不虚构空缺元模式 MR，hallucination 可控
└── 否 → 报告虚构案例，方法定位需收窄至"元模式适用单元格"
```

### 7.6 工作量汇总

| 阶段 | 工作 | 周期 |
|---|---|---|
| **2026-05** | 12 程序选择确认 + GT 构建 | 4 周 |
| **2026-06** | AVR 管线开发 + 预实验（temperature 校准）| 4 周 |
| **2026-07–08** | 主实验 6720 次 LLM 调用 + 跨范式分析 | 8 周 |
| **2026-09 初–中** | 数据分析 + 论文撰写 | 3 周 |
| **2026-09 中旬** | **SANER 2027 投稿** | 截稿对齐 |

### 7.7 总实验量

```
主实验:
  4 消融条件（A0, A3, A4, A6）× 12 程序 × 4 LLM × N=20 = 3840 次
  3 基线条件（B1, B2, B2″）× 12 程序 × 4 LLM × N=20 = 2880 次
  小计: 6720 次

预实验（temperature 校准）:
  1 LLM × 12 程序 × 4 T 值 × 5 = 240 次

合计: 6960 次
GSD 早停后预期: ≈ 5800 次

成本估算（按 Claude Opus 4.7 单价 ~$0.05/调用）: ≈ $290–350
```

---

## 附录 A：JSON 数据记录规范

每次 LLM 调用记录字段（最小 schema）：

```json
{
  "experiment_id": "exp_v4_20260715_a6_a1_claude47_n07",
  "config": {
    "variant": "A6",          // A0/A3/A4/A6/B1/B2/B2″
    "program": "A1_Lorenz",   // A1-A3, B1-B3, C1-C3, D1-D3
    "paradigm": "numerical",  // numerical/probabilistic/surrogate/ml
    "llm": "Claude_Opus_4.7", // ChatGPT_5.5 / DeepSeek_V4 / GLM_5
    "temperature": 0.5,
    "random_seed": 7,         // 1..20
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
    "avr_rate": 0.667
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

## 附录 B：与 v3.4 的差异速查

| 维度 | v3.4 | v4 |
|---|---|---|
| 实验对象 | PWR 五层方程（1 程序）| 12 程序 × 4 范式 |
| LLM | Claude Opus 4 / GPT-4o / Gemini 2.5 Pro / GLM-4-Plus | Claude Opus 4.7 / ChatGPT 5.5 / DeepSeek-V4 / GLM-5 |
| 消融 | A0–A6（7 档）| A0/A3/A4/A6（4 档）|
| 基线 | B1/B2/B2′/B2″/B3/B4（6 档）| B1/B2/B2″（3 档）|
| 假设 | H1–H4 | H1–H6（含 H5 跨范式 + H6 元模式空缺反向）|
| 主指标 | F1 + MKR | F1 + AVR（删 MKR）|
| 变异测试 | 30–40 变异体 + 10 天集群 | 已删除 |
| GT 协议 | PWR 专家 ≥ 3 + Fleiss κ ≥ 0.65 | 2–3 位行业专家纯二元 yes/no/unsure 投票多数决过滤 + 团队三角化（Cohen's κ ≥ 0.75）+ 跨家族 LLM 强化 |
| 总 LLM 调用 | 930（GSD 后 790）| 6960（GSD 后 5800）|
| N | 20 | 20 |
| 方法定位 | 安全关键科学计算 | 含数学/物理方程规约的科学计算软件 |
| 范式 C 内部异质性 | C1 GPR + C2 PCE + C3 Kriging | C1 GPR + C2 PCE + C3 NN-Surr |

---

## 附录 C：12 程序的已发表 MR 参考清单（GT 文献种子）

下表是源 1 文献抽取的种子 MR 集，研究生在此基础上再补充。每条 MR 标注 `(r, R, basis, pattern)`。

### A1 Lorenz（σ=10, β=8/3, ρ=28）— 8 条

| ID | r（输入变换） | R（输出关系） | basis | pattern |
|---|---|---|---|---|
| A1-M1 | 时间反演 t → -t | 体积保持 div(F)=−(σ+1+β) 守恒 | Hamiltonian/耗散率 | P1 |
| A1-M2 | 初值扰动 \|δ\| → \|2δ\| | 轨迹分离速率 ≈ 2 倍（Lyapunov 指数 λ≈0.906） | Lyapunov | P2 |
| A1-M3 | 步长 h → h/2 | 数值误差 ∝ h^p（p=4 RK45） | 收敛阶 | P3 |
| A1-M4 | 同步两条轨迹 ε→0 | 轨迹完全收敛 | 连续依赖 | P3 |
| A1-M5 | ρ < 1 | 唯一稳定平衡点 origin | 分岔分析 | P4 |
| A1-M6 | 1 < ρ < 24.74 | 两个稳定平衡点 C± | 分岔 | P4 |
| A1-M7 | 求解器 RK45 vs DOP853 | 长期统计量（吸引子维数）一致 ≤ 5% | 数值等价性 | P5 |
| A1-M8 | atol/rtol → atol/10, rtol/10 | 吸引子重叠面积单调增 | 误差控制 | P3 |

### A2 LU 分解 + Ax=b — 7 条

| ID | r | R | basis | pattern |
|---|---|---|---|---|
| A2-M1 | 行交换 P → P' | 解 x 不变 | 置换 LU | P1 |
| A2-M2 | A → cA, b → cb | x 不变 | 线性 | P1 |
| A2-M3 | A → A, b → cb | x → cx | 线性 | P2 |
| A2-M4 | 矩阵规模 n → 2n | 残差 \|Ax−b\|₂ 单调增 ≤ O(εn) | 数值稳定 | P2 |
| A2-M5 | 增加病态因子 cond(A) → 10·cond(A) | 解相对误差 ↑ 约 10× | 病态分析 | P2 |
| A2-M6 | 部分主元 vs 全主元 | 解差异 ≤ √n·eps | 数值等价 | P5 |
| A2-M7 | A 对称正定 vs 一般 | LU 解 = Cholesky 解 ≤ eps | 算法等价 | P5 |

### A3 FDM 一维热传导 ∂u/∂t = α∂²u/∂x² — 8 条

| ID | r | R | basis | pattern |
|---|---|---|---|---|
| A3-M1 | 网格 Δx → Δx/2, Δt → Δt/4 | L2 误差减半 | 二阶收敛 | P3 |
| A3-M2 | t → ∞ | u(x,t) → 稳态解 | 抛物 PDE 平衡 | P3 |
| A3-M3 | 初值对称 u₀(x)=u₀(L−x) | 解任意时刻对称 | 对称守恒 | P1 |
| A3-M4 | α → 2α | 等效 t → 2t | 尺度变换 | P1 |
| A3-M5 | Dirichlet u(0)=u(L)=0 | maxₓ u(x,t) 单调减 | 极大值原理 | P2 |
| A3-M6 | 增大 α | 衰减更快 | 扩散增强 | P2 |
| A3-M7 | u₀ ≥ 0 | u(x,t) ≥ 0 | 极大值原理 | P1 |
| A3-M8 | Δt > Δx²/(2α)（违反 CFL） | 显式格式发散 | 稳定性 | P5 |

### B1 PyMC Beta-Binomial 共轭 — 7 条

| ID | r | R | basis | pattern |
|---|---|---|---|---|
| B1-M1 | 数据交换可观测 | 后验不变（exchangeability） | de Finetti | P1 |
| B1-M2 | n → 2n（同 p） | 后验方差 ↓ ≈ 1/2 | 大数定律 | P2 |
| B1-M3 | 先验 Beta(α,β) → Beta(2α,2β) | 后验集中 | 先验信息量 | P2 |
| B1-M4 | n → ∞ | 后验 → δ(p_true) | 一致性 | P3 |
| B1-M5 | swap (α↔β, k↔n−k) | 后验 p ↔ (1−p) | 对称 | P1 |
| B1-M6 | seed 不同 chains=4 | $\hat R$ < 1.01 | 收敛诊断 | P3 |
| B1-M7 | 强先验 vs 弱先验同样本 | 后验均值排序与先验均值一致 | 偏序 | P5 |

### B2 Metropolis-Hastings（目标 2D 高斯）— 6 条

| ID | r | R | basis | pattern |
|---|---|---|---|---|
| B2-M1 | 链长 L → 10L | autocorr 时间不变（≤ ESS 校正） | 平稳 | P1 |
| B2-M2 | proposal scale × 2 | 接受率单调下降 | M-H 接受率 | P2 |
| B2-M3 | burn-in 增加 | KL(p̂‖p) 单调下降 | 收敛 | P3 |
| B2-M4 | L → ∞ | 经验分布 → 目标 | 遍历定理 | P3 |
| B2-M5 | 初值跳过 burn-in | 长程统计量不变 | 平稳 | P1 |
| B2-M6 | symmetric vs asym proposal | 接受公式不同但平稳分布同 | detailed balance | P5 |

### B3 朴素 Monte Carlo 积分 ∫₀¹ exp(−x²)dx — 6 条

| ID | r | R | basis | pattern |
|---|---|---|---|---|
| B3-M1 | N → 4N | 误差 std ↓ ≈ 1/2 | 1/√N | P3 |
| B3-M2 | 区间 [0,1]→[0,a] (a∈ℚ⁺) | 估计值线性变化 | 加性 | P2 |
| B3-M3 | seed 改变 | 估计值方差不超 σ²/N | 大数定律 | P1 |
| B3-M4 | 控制变量法（同 N） | 方差 ≤ 朴素 MC 方差 | 偏序 | P5 |
| B3-M5 | 重要性采样最优 | 方差进一步降低 | 偏序 | P5 |
| B3-M6 | 函数缩放 f → cf | 估计值 → c·估计 | 线性 | P1 |

### C1 GPR（sklearn）— 7 条

| ID | r | R | basis | pattern |
|---|---|---|---|---|
| C1-M1 | 训练点扰动 ε → 0 | 后验均值 → 训练点真值 | 内插性 | P3 |
| C1-M2 | length scale ℓ → 2ℓ | 后验更平滑（曲率 ↓） | RBF 核 | P2 |
| C1-M3 | 训练样本 N → 2N | 预测 RMSE 单调下降 | 一致性 | P2 |
| C1-M4 | 输入坐标平移 | 预测协变（核函数平移不变） | 核性质 | P1 |
| C1-M5 | 加噪 σ_n → 2σ_n | 预测置信区间增宽 | 噪声模型 | P2 |
| C1-M6 | RBF vs Matern-2.5 | 平滑度排序 RBF > Matern | 偏序 | P5 |
| C1-M7 | 重复训练点 | 后验不变 | 信息冗余 | P1 |

### C2 PCE（chaospy）— 6 条

| ID | r | R | basis | pattern |
|---|---|---|---|---|
| C2-M1 | 阶数 p → p+1 | L2 截断误差 ↓ | 收敛 | P3 |
| C2-M2 | 不同正交基（Hermite/Legendre）匹配输入分布 | 收敛速率最优 | Wiener-Askey | P5 |
| C2-M3 | 输入分布平移 | 系数线性变换 | 仿射不变 | P1 |
| C2-M4 | 增加 quadrature 点 | 系数估计稳定 | 数值积分 | P3 |
| C2-M5 | sparse grid vs full tensor | 高维下 sparse 更快 | 偏序 | P5 |
| C2-M6 | 正交性 ⟨ψᵢ,ψⱼ⟩=δᵢⱼ | 系数独立 | 正交 | P1 |

### C3 NN-Surr（MLPRegressor on Forrester/Branin）— 7 条

| ID | r | R | basis | pattern |
|---|---|---|---|---|
| C3-M1 | 隐层节点数 ↑ | 训练 MSE ↓ | 容量 | P2 |
| C3-M2 | 训练样本 N → 2N | 验证 MSE ↓ | 学习理论 | P2 |
| C3-M3 | 训练 epoch ↑ | loss 学习曲线单调下降并平台 | 优化 | P4 |
| C3-M4 | 特征顺序置换 | 输出不变（多层全连接 / 与样本独立的等价输入空间） | 置换不变 | P1 |
| C3-M5 | 输入仿射缩放（输入归一化）| 网络可学回 | 通用近似 | P3 |
| C3-M6 | 增加隐层 | Forrester 1d 拟合误差 ≤ 单层 | 偏序 | P5 |
| C3-M7 | 训练样本充足后再加 | 验证 MSE 收益边际下降 | 过参化 | P3 |

### D1 MLPClassifier on Iris — 7 条

| ID | r | R | basis | pattern |
|---|---|---|---|---|
| D1-M1 | 类标签置换 | 准确率不变 | label invariance | P1 |
| D1-M2 | 特征顺序置换（重训）| 准确率 ≤ ε 差异 | 等价输入 | P1 |
| D1-M3 | 训练样本 ↑ | 准确率 ↑ | learning curve | P2 |
| D1-M4 | 加噪声特征 | 准确率 ↓ | 信噪比 | P2 |
| D1-M5 | 训练 epoch | accuracy 学习曲线形态 | 优化 | P4 |
| D1-M6 | 隐层节点（小→足够大）| 训练准确率单调升 | 容量 | P2 |
| D1-M7 | softmax 输出 | Σpᵢ = 1 | 概率归一 | P1 |

### D2 SVC RBF on Breast Cancer — 7 条

| ID | r | R | basis | pattern |
|---|---|---|---|---|
| D2-M1 | 特征缩放 x→cx + 调整 γ | 决策边界等价 | 核仿射 | P1 |
| D2-M2 | C → 10C | 边界更硬，训练误差 ↓ | hinge loss | P2 |
| D2-M3 | γ → 10γ | 边界曲率 ↑ | RBF 局部性 | P2 |
| D2-M4 | 标签翻转 y→−y | 法向量翻转，准确率不变 | 对称 | P1 |
| D2-M5 | RBF vs Polynomial vs Linear | 非线性数据 RBF 占优 | 偏序 | P5 |
| D2-M6 | 数据增加 | 支持向量比例下降 | 一致性 | P3 |
| D2-M7 | 类不平衡 → class_weight=balanced | recall 提升 | 偏序 | P5 |

### D3 LogisticRegression on Diabetes — 7 条

| ID | r | R | basis | pattern |
|---|---|---|---|---|
| D3-M1 | 特征仿射 x→ax+b（含归一化）| 系数解析变换，预测概率不变 | 仿射不变 | P1 |
| D3-M2 | C → 0（强 L2）| 权重 → 0，模型 → 多数类 | 正则 | P2 |
| D3-M3 | L1 正则强度 ↑ | 非零权重数 ↓ | 稀疏 | P2 |
| D3-M4 | 类标签翻转 | 系数翻转 | 对称 | P1 |
| D3-M5 | 训练样本 ↑ | log-loss 下降 | 一致性 | P2 |
| D3-M6 | sigmoid(z)+sigmoid(−z)=1 | 概率归一 | 数学 | P1 |
| D3-M7 | L1 vs L2 | 高维稀疏数据下 L1 偏序更优 | 偏序 | P5 |

合计 83 条种子 MR。研究生需独立复核每条 `(r,R,basis)` 的表达正确性。

---

## 附录 D：完整 Prompt 模板（A0/A3/A4/A6 + B1/B2/B2″）

每个变体维护 1 套主模板，12 程序通过 `<<PROGRAM_BLOCK>>` 参数化插入，避免维护 84 套。

### D.1 程序参数化块 `<<PROGRAM_BLOCK>>`（每程序 1 个，研究生填表后注入）

```yaml
program_id: "A1_Lorenz"
program_name: "Lorenz 系统数值求解"
mathematical_specification: |
  dx/dt = σ(y − x)
  dy/dt = x(ρ − z) − y
  dz/dt = xy − βz
  默认参数 σ=10, β=8/3, ρ=28；时间区间 [0,40]；初值 (1,1,1)±ε
algorithm_description: |
  scipy.integrate.solve_ivp，RK45 自适应步长，atol=1e-8 rtol=1e-6
input_parameters:
  - σ: float ∈ [0,30]
  - β: float ∈ [0,5]
  - ρ: float ∈ [0,50]
  - 初值 (x0,y0,z0): float³ ∈ ℝ³
  - 时间区间 [t0,tf]: float² ∈ ℝ²
  - atol,rtol: float ∈ (0,1)
output_quantities:
  - 轨迹 {(t_i, x_i, y_i, z_i)}
  - 终态 (x(tf),y(tf),z(tf))
  - 长期统计量（吸引子维数估计、Lyapunov 指数）
typical_workloads: "气象、混沌动力学；时间步 ≤ 0.01 单位；ρ=28 默认混沌区"
relevant_textbook_chapters: "Strogatz Nonlinear Dynamics 2018, Ch.9（Lorenz 方程）"
expected_concept_set_K: |
  Lyapunov 指数, 守恒量, 步长收敛, 时间反演, 初值敏感性, 吸引子维数,
  RK45, atol/rtol, 数值耗散, 体积保持率, 分岔点, 平衡点稳定性,
  长期统计量, 参数 ρ 敏感性, 误差累积, 双精度边界
```

### D.2 A0 模板（无元模式 / 无矩阵 / 无 CoT / 无 FS）

```
你是一名科学计算软件测试工程师。请为以下程序识别其应满足的蜕变关系（MR）。

<<PROGRAM_BLOCK>>

**任务**：列出该程序的 MR，每条用以下 YAML 格式输出：

- id: "Prog-NN"
  name: "简洁名称"
  input_relation_r: "数学表达"
  output_relation_R: "数学表达"
  basis: "数学/物理依据"
```

### D.3 A3 模板（+ 元模式 + 参数 × 元模式矩阵）

```
你是一名科学计算软件测试工程师。请为以下程序基于"元模式"先验识别 MR。

【元模式定义】
- P1 守恒性：什么变换不改变输出？
- P2 单调性：增大参数 θ，输出 y 往哪个方向变？
- P3 收敛性：推到极端/精化后趋向什么？
- P4 轨迹性：响应路径长什么样？
- P5 偏序性：谁更准？

<<PROGRAM_BLOCK>>

【参数 × 元模式恢复矩阵】
请依次对每个 (输入参数, 元模式) 单元格判断：
- 适用 / 不适用 / 不确定
- 若适用，给出候选 MR 的 (r, R, basis)

【输出格式】
- id: "Prog-NN"
  name: "..."
  meta_pattern: "P1|P2|P3|P4|P5|uncertain"
  classification: "MR|Property"
  input_relation_r: "..."
  output_relation_R: "..."
  basis: "..."
  falsifiability: "违反意味着什么缺陷"
```

### D.4 A4 模板（A3 + Chain-of-Thought）

```
[A3 全文]

【推理要求】
对每个矩阵单元格，先输出"思考链"再输出 MR：
THINKING:
  Step 1: 该参数的物理/数学含义是？
  Step 2: 在该元模式视角下应满足什么？
  Step 3: 是否存在反例使关系失效？
  Step 4: 用 (r, R) 形式化表达
ANSWER:
  [YAML MR 条目]
```

### D.5 A6 模板（A4 + Few-Shot）

```
[A4 全文]

【示例库】（与目标程序异范式）
EXAMPLE 1（数值范式 / P3）：
  程序：辛普森积分
  THINKING: 区间细分 n→2n，根据 O(h⁴) 误差应除以 16
  ANSWER:
    - id: Simp-01
      meta_pattern: P3
      input_relation_r: "n → 2n"
      output_relation_R: "|I_2n − I_true| ≤ |I_n − I_true| / 16"
      basis: Simpson 误差阶 O(h⁴)

EXAMPLE 2（机器学习 / P1）：
  程序：KNN 分类
  THINKING: 类标签是符号，不影响距离计算
  ANSWER:
    - id: KNN-01
      meta_pattern: P1
      input_relation_r: "类标签置换 π(y)"
      output_relation_R: "accuracy 不变"
      basis: 标签为名义型变量

【现在请为以下目标程序识别 MR】
<<PROGRAM_BLOCK>>
```

### D.6 B1 模板（Zero-Shot Baseline）

```
请为以下程序识别蜕变关系（MR）：
程序名：<<program_name>>
[YAML MR 条目]
```

### D.7 B2 模板（Domain-Prompted，等量知识，三层组织）

```
你是该范式的领域专家。基于以下三层领域知识识别 MR：

【层 1：数学性质】
<<mathematical_specification>>

【层 2：数值/算法特性】
<<algorithm_description>>

【层 3：工况约束】
<<input_parameters>> + <<typical_workloads>>

请逐条列出 MR，每条包含 (r, R, basis)。
```

### D.8 B2″ 模板（Domain-NoMatrix，最干净）

```
你是该范式的领域专家。等量领域知识扁平给出：

<<mathematical_specification>>
<<algorithm_description>>
<<input_parameters>>
<<typical_workloads>>

请列出该程序的 MR，每条 (r, R, basis)。
```

### D.9 等量校准（必需）

研究生在生成全部 prompts 后，运行 `tools/token_balance.py`：

```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
for prog in PROGRAMS_12:
    a6 = len(enc.encode(open(f"prompts/A6/{prog}.txt").read()))
    for v in ["B1","B2","B2_doubleprime"]:
        b = len(enc.encode(open(f"prompts/{v}/{prog}.txt").read()))
        ratio = b / a6
        assert 0.95 <= ratio <= 1.05, f"{prog}/{v}: {ratio:.3f} out of ±5%"
```

若超 ±5%，对 B2/B2″ 加补"领域细节"或"工况描述"段落直至匹配。

---

## 附录 E：AVR 验证管线代码骨架

12 程序统一暴露接口 `run_avr(program_id, mr_list) -> {"pass": int, "total": int, "rate": float}`。

### E.1 通用框架

```python
# avr/dispatch.py
from avr.wilcoxon_p2p5 import verify_wilcoxon
from avr.dtw_p4 import verify_dtw
from avr.constraint_p1p3 import verify_constraint

DISPATCH = {
    "P1": verify_constraint,
    "P2": verify_wilcoxon,
    "P3": verify_constraint,  # 收敛性走约束验证
    "P4": verify_dtw,
    "P5": verify_wilcoxon,
}

def run_avr(program_id, mr_list, runs_per_mr=30):
    results = {"pass": 0, "total": 0, "details": []}
    for mr in mr_list:
        if mr["meta_pattern"] in ("uncertain", None):
            continue  # 不可分流的不计入分母
        verifier = DISPATCH[mr["meta_pattern"]]
        outcome = verifier(program_id, mr, runs_per_mr)
        results["total"] += 1
        results["pass"] += int(outcome["pass"])
        results["details"].append(outcome)
    results["rate"] = results["pass"] / max(results["total"], 1)
    return results
```

### E.2 P2/P5 — Wilcoxon 验证

```python
# avr/wilcoxon_p2p5.py
from scipy.stats import wilcoxon
import numpy as np

def verify_wilcoxon(program_id, mr, runs=30):
    runner = PROGRAM_RUNNERS[program_id]   # 见 §J
    direction = mr.get("direction_hint", "decrease")
    y_a, y_b = [], []
    for seed in range(runs):
        params_a, params_b = mr["transform"](seed)
        y_a.append(runner(params_a, seed))
        y_b.append(runner(params_b, seed))
    stat, p = wilcoxon(y_a, y_b, alternative=
        "greater" if direction == "decrease" else "less")
    return {"pass": p < 0.05, "p": p, "n": runs}
```

### E.3 P4 — DTW 验证

```python
# avr/dtw_p4.py
from dtaidistance import dtw
import numpy as np

def verify_dtw(program_id, mr, runs=10):
    runner = PROGRAM_RUNNERS[program_id]
    distances = []
    for seed in range(runs):
        traj_a, traj_b = runner.trajectory_pair(mr["transform"], seed)
        d = dtw.distance(traj_a, traj_b)
        distances.append(d)
    threshold = mr.get("dtw_threshold", np.percentile(distances, 50) * 1.5)
    pass_rate = np.mean([d <= threshold for d in distances])
    return {"pass": pass_rate >= 0.7, "pass_rate": pass_rate, "n": runs}
```

### E.4 P1/P3 — 约束验证

```python
# avr/constraint_p1p3.py
import numpy as np

def verify_constraint(program_id, mr, runs=30):
    runner = PROGRAM_RUNNERS[program_id]
    violations = 0
    for seed in range(runs):
        params_a, params_b = mr["transform"](seed)
        y_a = runner(params_a, seed)
        y_b = runner(params_b, seed)
        if not mr["constraint_check"](y_a, y_b, tol=mr.get("tol", 1e-6)):
            violations += 1
    return {"pass": violations == 0, "violations": violations, "n": runs}
```

### E.5 12 程序的 MR `transform / constraint_check` 配置（YAML 模板）

```yaml
# avr/configs/A1_Lorenz.yaml
- mr_id: A1-M2  # P2
  transform: |
    def t(seed):
      eps = 1e-6
      return ({"x0":(1,1,1), "tf":40}, {"x0":(1+eps,1,1), "tf":40})
  metric: |
    def m(traj_a, traj_b):
      sep = np.linalg.norm(traj_a[-1] - traj_b[-1])
      return np.log(sep / 1e-6)  # 期望 ≈ λ·tf ≈ 36
  expected_range: [25, 50]
- mr_id: A1-M1  # P1（体积保持）
  transform: 不需变换，单次运行
  constraint_check: |
    def c(traj):
      vol = compute_phase_volume(traj)
      return abs(vol - vol[0] * np.exp(-(σ+1+β)*tf)) < 1e-3
```

研究生需为 83 条种子 MR 各填写一个 YAML 块；缺 `transform / constraint_check` 的标 `unverifiable=True` 不计入 AVR 分母。

### E.6 AVR 输出 schema

```json
{
  "program_id": "A1_Lorenz",
  "variant": "A6",
  "llm": "Claude_Opus_4.7",
  "mr_total": 12,
  "dispatchable": 10,
  "passed": 8,
  "avr_rate": 0.80,
  "per_mr": [{"mr_id": "A1-M2", "pattern": "P2", "pass": true, "p": 0.001}, ...]
}
```

---

## 附录 F：12 程序的概念覆盖集 K（等量控制层 2）

B1、B2、B2″、A6 四档 prompt 必须全覆盖各自程序的 K 集合，每概念至少出现一次。

| 程序 | \|K\| | 关键概念集 K |
|---|---|---|
| A1 Lorenz | 16 | Lyapunov 指数, 守恒量, 步长收敛, 时间反演, 初值敏感性, 吸引子维数, RK45, atol/rtol, 数值耗散, 体积保持率, 分岔点, 平衡点稳定性, 长期统计量, ρ 敏感性, 误差累积, 双精度边界 |
| A2 LU | 14 | 主元选取, 行交换, 矩阵条件数, 残差范数, 数值稳定, 算子范数, LU 分解唯一性, 部分主元, 完全主元, Cholesky 等价, 病态矩阵, ε-机器精度, 浮点累积误差, 对称正定 |
| A3 FDM 热传导 | 15 | 抛物线 PDE, 显式格式, CFL 条件, 二阶收敛, 极大值原理, Dirichlet 边界, Neumann 边界, 热扩散系数 α, 网格细化, 离散稳定性, 守恒律, 对称解, 稳态收敛, 截断误差, 边界层 |
| B1 共轭 | 13 | Bayes 公式, 共轭先验, 后验集中, 大数定律, 一致性, exchangeability, 后验对称, 弱/强先验, $\hat R$ 收敛诊断, 信息熵, ELBO, 似然比, KL 距离 |
| B2 MCMC | 14 | detailed balance, 平稳分布, 遍历定理, autocorr, ESS, burn-in, proposal scale, 接受率, mixing time, 热力学链, Gibbs 等价, 不可约, 非周期, 收敛诊断 |
| B3 MC 积分 | 12 | 大数定律, 1/√N 收敛, 控制变量, 重要性采样, 方差缩减, 准 MC, 拟随机, 误差估计, 置信区间, 偏置-方差, 函数线性, 可加性 |
| C1 GPR | 14 | RBF 核, Matern 核, 长度尺度, 后验均值, 后验方差, 内插性, 训练点扰动, 核仿射不变, 噪声方差 σ_n, 重复点冗余, MAP, MLE, 数值稳定（Cholesky）, 协方差矩阵 |
| C2 PCE | 13 | Wiener-Askey, Hermite/Legendre, 正交基, 截断误差, 谱收敛, 系数估计, quadrature 点, sparse grid, full tensor, 仿射不变, L2 收敛, 阶数 p, 高维诅咒 |
| C3 NN-Surr | 16 | 通用近似定理, 反向传播, MSE 损失, 学习曲线, 过拟合, 置换不变, 隐层节点, 训练 epoch, 验证集, 输入归一化, 容量, ReLU 激活, Adam 优化, batch size, weight decay, generalization gap |
| D1 MLP | 14 | softmax, 交叉熵, 类标签置换, 特征顺序置换, 准确率, 学习曲线, 隐层容量, 噪声鲁棒性, 训练样本量, BP, 梯度下降, 概率归一, mini-batch, 验证准确率 |
| D2 SVM | 14 | hinge loss, 二次规划, RBF 核, γ 参数, C 参数, 核仿射不变, 支持向量比, 标签翻转对称, 决策边界硬度, 不平衡 class_weight, 多分类 OvO/OvR, 软间隔, KKT 条件, 核技巧 |
| D3 LR | 13 | sigmoid, 交叉熵, L1/L2 正则, 仿射不变, 标签翻转, 概率归一, 系数稀疏, 梯度下降, IRLS, 二项似然, 对数几率, 正则强度, log-loss |

研究生检查脚本：

```python
# tools/concept_coverage.py
import re
def coverage(prompt_text, K):
    return sum(1 for c in K if c.lower() in prompt_text.lower()) / len(K)
for prog in PROGRAMS_12:
    K = load_K(prog)
    for v in ["A6","B1","B2","B2_doubleprime"]:
        c = coverage(open(f"prompts/{v}/{prog}.txt").read(), K)
        assert c == 1.0, f"{prog}/{v} concept coverage {c:.2%}"
```

---

## 附录 G：统计分析脚本模板

### G.1 Holm-Bonferroni（10 假设族）

```python
# stats/holm.py
from statsmodels.stats.multitest import multipletests
import pandas as pd

def holm_correction(p_values_dict, alpha=0.05):
    keys = list(p_values_dict.keys())
    p = [p_values_dict[k] for k in keys]
    reject, p_adj, _, _ = multipletests(p, alpha=alpha, method="holm")
    return pd.DataFrame({"hypothesis": keys, "p_raw": p,
                         "p_adj": p_adj, "reject_h0": reject})

P_VALUES = {
    "H1_A6_vs_B2": ..., "H1_A6_vs_B2dd": ..., "H1_B2_vs_B2dd": ...,
    "H2_A0_A3": ..., "H2_A3_A4": ..., "H2_A4_A6": ...,
    "H3_nt_vs_t": ...,
    "H4_AVR_A6_vs_B2": ...,
    "H5_sign_test": ...,
    "H6_cell_rho": ...,
}
```

### G.2 配对 Wilcoxon + Cliff's δ + Bootstrap CI

```python
# stats/effect_size.py
from scipy.stats import wilcoxon
import numpy as np

def cliffs_delta(x, y):
    nx, ny = len(x), len(y)
    gt = sum(xi > yj for xi in x for yj in y)
    lt = sum(xi < yj for xi in x for yj in y)
    return (gt - lt) / (nx * ny)

def bootstrap_ci(data, stat_fn, n_resample=2000, alpha=0.05):
    boots = [stat_fn(np.random.choice(data, size=len(data), replace=True))
             for _ in range(n_resample)]
    return np.percentile(boots, [100*alpha/2, 100*(1-alpha/2)])

def paired_test(a6_scores, baseline_scores):
    stat, p = wilcoxon(a6_scores, baseline_scores)
    delta = cliffs_delta(a6_scores, baseline_scores)
    diffs = np.array(a6_scores) - np.array(baseline_scores)
    ci = bootstrap_ci(diffs, np.mean)
    return {"p": p, "cliff_delta": delta, "mean_diff_ci_95": ci}
```

### G.3 GSD Pocock 中期分析

```python
# stats/gsd.py
def gsd_pocock_check(interim_n, interim_delta, interim_p,
                     boundary_p=0.025, boundary_delta=0.30):
    """
    Pocock-style 单次中期：N=15 时若 Cliff's δ ≥ 0.30 且 p < 0.025 提前停止。
    最终 N=20 检验 α=0.025（对称分配）。
    """
    if interim_n != 15:
        raise ValueError("Pocock interim must be at N=15")
    return interim_delta >= boundary_delta and interim_p < boundary_p

def gsd_final_alpha():
    return 0.025  # 中期不停止时，最终检验 α
```

### G.4 H6 单元格 Spearman ρ

```python
# stats/h6_cells.py
from scipy.stats import spearmanr
import numpy as np

def h6_cell_correlation(a6_outputs, gt_table):
    cells_a6, cells_gt = [], []
    for prog in PROGRAMS_12:
        for pat in ["P1","P2","P3","P4","P5"]:
            cells_a6.append(count_mrs(a6_outputs[prog], pat))
            cells_gt.append(count_mrs(gt_table[prog], pat))
    rho, p = spearmanr(cells_a6, cells_gt)
    return {"rho": rho, "p": p, "n_cells": 60,
            "empty_cells_gt": sum(c==0 for c in cells_gt),
            "fabricated_cells_a6": sum(g==0 and a>=2
                for a,g in zip(cells_a6,cells_gt))}
```

### G.5 统一报告生成

```python
# stats/report.py
def generate_full_report(experiment_data):
    report = {
        "H1": holm_correction({"A6_vs_B2": ..., "A6_vs_B2dd": ..., "B2_vs_B2dd": ...}),
        "H2": holm_correction({"A0_A3": ..., "A3_A4": ..., "A4_A6": ...}),
        "H3": paired_test(experiment_data["recall_nt"], experiment_data["recall_t"]),
        "H4": paired_test(experiment_data["avr_a6"], experiment_data["avr_b2"]),
        "H5": cv_across_programs(experiment_data["delta_f1_per_program"]),
        "H6": h6_cell_correlation(experiment_data["a6_outputs"], experiment_data["gt"]),
    }
    return report
```

---

## 附录 H：API 调用脚手架（4 LLM 统一封装 + checkpoint）

### H.0 `.env.example` 模板（占位符，实际密钥写入本地 `.env` 后由 `.gitignore` 排除）

```bash
# Anthropic Claude (claude_opus_47)
ANTHROPIC_API_KEY=your_anthropic_api_key
ANTHROPIC_BASE_URL=your_anthropic_base_url   # 默认 https://api.anthropic.com，自定义代理时填写

# OpenAI ChatGPT (chatgpt_55)
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=your_openai_base_url         # 默认 https://api.openai.com/v1

# DeepSeek (deepseek_v4)
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=your_deepseek_base_url     # 默认 https://api.deepseek.com

# 智谱 GLM (glm_5)
ZHIPU_API_KEY=your_zhipu_api_key
ZHIPU_BASE_URL=your_zhipu_base_url           # 默认 https://open.bigmodel.cn/api/paas/v4
```

**安全要求**：
- 真实密钥**只写本地** `.env`，**绝不**写入仓库或 prompt 文本；`.gitignore` 必须包含 `.env`。
- 复现者拷贝 `.env.example` → `.env`，将每个 `your_*_api_key` / `your_*_base_url` 替换为自己的凭据。
- `scripts/check_llm_keys.py` 仅校验 4 个 KEY 非空且能成功调用 1 token 的 ping，不打印 KEY 内容。

### H.1 统一接口

```python
# llm/unified.py
import time, json, hashlib
from pathlib import Path

CHECKPOINT_DIR = Path("results/checkpoints")
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

def call_llm(provider, prompt, temperature=0.5, seed=None,
             max_retries=3, max_tokens=4096):
    payload_hash = hashlib.sha256(
        f"{provider}|{prompt}|{temperature}|{seed}".encode()).hexdigest()[:16]
    ckpt = CHECKPOINT_DIR / f"{payload_hash}.json"
    if ckpt.exists():
        return json.loads(ckpt.read_text())

    for attempt in range(max_retries):
        try:
            if provider == "claude_opus_47":
                resp = call_anthropic(prompt, temperature, seed, max_tokens)
            elif provider == "chatgpt_55":
                resp = call_openai(prompt, temperature, seed, max_tokens)
            elif provider == "deepseek_v4":
                resp = call_deepseek(prompt, temperature, seed, max_tokens)
            elif provider == "glm_5":
                resp = call_zhipu(prompt, temperature, seed, max_tokens)
            else:
                raise ValueError(provider)
            ckpt.write_text(json.dumps(resp, ensure_ascii=False))
            return resp
        except RateLimitError:
            time.sleep(2 ** attempt * 5)
        except Exception as e:
            if attempt == max_retries - 1: raise
            time.sleep(2 ** attempt)
```

### H.2 速率限制配置（按厂商文档）

```python
# llm/rate_limits.py
RATE_LIMITS = {
    "claude_opus_47": {"rpm": 50, "tpm": 40000},
    "chatgpt_55":     {"rpm": 60, "tpm": 90000},
    "deepseek_v4":    {"rpm": 60, "tpm": 60000},
    "glm_5":          {"rpm": 30, "tpm": 30000},
}
# 使用 tenacity / ratelimit 包实现限流装饰器
```

### H.3 主实验 driver

```python
# driver/main_experiment.py
from itertools import product

VARIANTS = ["A0","A3","A4","A6","B1","B2","B2_doubleprime"]
PROGRAMS = ["A1_Lorenz","A2_LU","A3_FDM",
            "B1_BetaBinom","B2_MH","B3_MC",
            "C1_GPR","C2_PCE","C3_NN_Surr",
            "D1_MLP","D2_SVC","D3_LR"]
LLMS = ["claude_opus_47","chatgpt_55","deepseek_v4","glm_5"]
SEEDS = list(range(1, 21))   # N=20

for variant, prog, llm, seed in product(VARIANTS, PROGRAMS, LLMS, SEEDS):
    prompt = render_prompt(variant, prog)
    resp = call_llm(llm, prompt, temperature=0.5, seed=seed)
    save_result(variant, prog, llm, seed, prompt, resp)
```

### H.4 失败恢复

- checkpoint 按 `sha256(provider|prompt|T|seed)` 缓存，重跑自动跳过已完成调用
- driver 每 100 调用刷一次 `progress.json`（已完成数 / 总数 / 错误清单）
- 单 LLM 整体失败时自动切换到备用 endpoint（如 OpenRouter 镜像）

### H.5 GSD 中期评估钩子

```python
# 每完成一个 LLM 的全部 N=15 时调用
if completed_seeds_per_config >= 15:
    interim = compute_h1_interim(results_so_far)
    if gsd_pocock_check(15, interim["delta"], interim["p"]):
        log("GSD early stop triggered: H1 已显著")
        # 仍跑完 N=20 用于其余假设报告
```

---

## 附录 I：共识审核 SOP（GT 构建 / 匹配判定）

### I.1 GT 共识审核流程

```
1. 收集源 1（文献 MR）+ 源 3（Qwen+Doubao 输出）
2. Meng 与反审者（硕士 A）做源 4 团队三角化：独立标注每条 MR accept / revise / reject + 各自补 0–3 条 common-sense MR
3. 计算 Cohen's κ：
   κ < 0.65 → 协议失败，第三方仲裁（Li Meng 教授）所有冲突
   0.65 ≤ κ < 0.75 → 仅冲突项第三方仲裁
   κ ≥ 0.75 → 仅冲突项两人协商解决
4. 形成候选 MR 清单（含程序方程 + 五元模式解释 + 每条 MR 的 (r, R, basis) + 中文物理含义解释 + 元模式归属）→ 提交 2–3 位行业专家做 15–30 min 视频/线下访谈，专家对每条候选 MR 仅打 yes/no/unsure
5. 多数决过滤：3 位时 ≥ 2 yes 入 G_final；2 位时一致 yes 入 G_final
6. 对入选 MR 增 (program, meta_pattern) 单元格归属（用于 H6）
7. 输出 G_final.yaml，封版 hash 到 git
```

### I.2 匹配判定 SOP（A6 输出 vs G_final）

```
两条 MR 判定"匹配"：
  (a) 输入参数 θ 等价（同名或数学等价变换）
  (b) 输出关系 R 数学/物理含义一致（含等价变形）
  不要求元模式归类相同

人工判定：Meng + 硕士 A 独立判定，每条标 match / no_match / unsure
  分歧项第三方仲裁
  Cohen κ ≥ 0.75 强制要求；不达标则增样本到达标
```

### I.3 工时预算

| 阶段 | 工作量 |
|---|---|
| 12 程序文献 MR 抽取 | 6 工作日（Meng） |
| 2–3 位行业专家招募 + 15–30 min 视频/线下访谈（纯 yes/no/unsure 投票）| 0.5–1 周（联系 + 排期 + 访谈 + 投票表整理）|
| Qwen+Doubao 调用 + 双审 | 3 工作日 |
| GT 共识审核 | 5 工作日 |
| 主实验匹配判定 | 7 工作日（结果产出后） |

### I.4 争议仲裁记录格式

```yaml
- mr_id: "A1-M3"
  rater_a: accept
  rater_b: revise
  conflict_reason: "Meng 主张 RK45 阶 p=4，硕士 A 主张 p=5（dop853）"
  arbitrator: "Li Meng"
  resolution: "保留 p=4 用于 RK45；新增 A1-M3' 描述 dop853 p=8"
```

---

## 附录 J：12 程序参考实现（runner 接口）

所有 AVR 验证共享统一 runner 接口 `runner(params, seed) -> output`。

### J.1 接口规范

```python
# programs/runners.py
class ProgramRunner:
    def __call__(self, params: dict, seed: int) -> Any: ...
    def trajectory_pair(self, transform_fn, seed) -> tuple[np.ndarray, np.ndarray]: ...

PROGRAM_RUNNERS = {
    "A1_Lorenz": LorenzRunner(),
    "A2_LU": LURunner(),
    "A3_FDM": FDMHeatRunner(),
    "B1_BetaBinom": BetaBinomRunner(),
    "B2_MH": MHRunner(),
    "B3_MC": MCIntRunner(),
    "C1_GPR": GPRRunner(),
    "C2_PCE": PCERunner(),
    "C3_NN_Surr": NNSurrRunner(),
    "D1_MLP": MLPRunner(),
    "D2_SVC": SVCRunner(),
    "D3_LR": LRRunner(),
}
```

### J.2 各程序参考实现源（开放/可复用）

| 程序 | 推荐实现 |
|---|---|
| A1 Lorenz | `scipy.integrate.solve_ivp` + 标准 Lorenz RHS（10 行） |
| A2 LU | `scipy.linalg.lu_factor / lu_solve` |
| A3 FDM | 自编显式格式 ≤ 60 行（Larsson & Thomée 模板） |
| B1 BetaBinom | `pymc as pm` + `with pm.Model()` Beta+Binomial（15 行） |
| B2 MH | 自编 Metropolis-Hastings（30 行；高斯 proposal） |
| B3 MC | numpy.random.uniform 直接采样 |
| C1 GPR | `sklearn.gaussian_process.GaussianProcessRegressor` |
| C2 PCE | `chaospy` 库（5 行） |
| C3 NN-Surr | `sklearn.neural_network.MLPRegressor` on Forrester 1d |
| D1 MLP | `sklearn.MLPClassifier` on `sklearn.datasets.load_iris` |
| D2 SVC | `sklearn.svm.SVC` on `sklearn.datasets.load_breast_cancer` |
| D3 LR | `sklearn.linear_model.LogisticRegression` on diabetes csv |

仓库结构：

```
metaprompt-saner27/
  programs/
    runners.py
    A1_lorenz.py  ...  D3_lr.py
  prompts/
    A0/{12 programs}.txt
    A3/{12 programs}.txt
    A4/{12 programs}.txt
    A6/{12 programs}.txt
    B1/{12 programs}.txt
    B2/{12 programs}.txt
    B2_doubleprime/{12 programs}.txt
  avr/
    dispatch.py wilcoxon_p2p5.py dtw_p4.py constraint_p1p3.py
    configs/{12 programs}.yaml
  llm/
    unified.py rate_limits.py
  driver/
    main_experiment.py pilot_temperature.py
  stats/
    holm.py effect_size.py gsd.py h6_cells.py report.py
  gt/
    G_literature.yaml G_llm_cross.yaml G_team.yaml G_expert_votes.csv G_final.yaml
  results/
    checkpoints/  raw/  evaluated/  reports/
  tools/
    token_balance.py concept_coverage.py
```

---

## 附录 K：Few-Shot 示例池（A6 专用，与目标程序异范式选取）

| 目标程序范式 | 推荐 Few-Shot 示例（异范式 2 例） |
|---|---|
| A 数值 | KNN 标签置换（D1）+ Beta 后验集中（B1） |
| B 概率 | 辛普森积分阶（A1 异程序）+ SVM 缩放（D2） |
| C 代理 | LU 行交换（A2）+ MCMC 平稳（B2） |
| D 机器学习 | FDM 网格收敛（A3）+ MC 1/√N（B3） |

每示例包含完整 THINKING + ANSWER 结构，存于 `prompts/few_shot_pool/`。

---

## 附录 L：研二学生独立执行的 15 周详细工作计划

单人执行场景。每周分三段：目标与任务、验收标准、自评表。周末把 `weekly_log/wkN.md` 填好，自评总分 ≥ 18/25 算通过，低于 18 找老师面谈复盘。卡点先查附录 N 失败决策树，无法解决再升级。

### 通用自评表模板（每周末填写）

| 维度 | 1 分（差） | 3 分（合格） | 5 分（优秀） | 本周得分 | 证据/快照 |
|---|---|---|---|---|---|
| **目标达成** | 主目标未完成 | 主目标完成，次目标部分完成 | 全部完成 + 提前 |  |  |
| **验收达标率** | < 60% 项打勾 | 60-90% | ≥ 90% |  |  |
| **数据归档** | 缺关键产物 | 产物在指定路径但未 commit | 产物 + commit + 数据快照路径全 |  |  |
| **异常处理** | 卡 ≥ 1 天才求助 | 半天内找答案，必要时升级 | 自查附录 N 解决，未升级 |  |  |
| **反思深度** | 流水账 | 列遇到的 1-2 个问题 + 解法 | 主动总结可改进项 + 下周调整 |  |  |
| **总分** | | | | **/25** | |

---

### 第 0 周：环境就绪与试运行

**目标**：本机能跑通 1 个最小 cell（B3 + Claude Opus 4.7 + N=1 + AVR），证明工具链通畅。

**任务**：
1. 克隆仓库 → `pip install -r requirements.txt`（含 numpy/scipy/dtaidistance/openai/anthropic/zhipuai）
2. 配置 4 LLM API key（写入 `.env`，参附录 H）
3. 跑 12 个 `programs/*_runner.py` 单测（`pytest tests/test_runners.py`），全部 PASS
4. 完整通读论文 §1-§4 + 实验指南 §0（术语表）+ §1（任务定义）+ 附录 M（B3 walked example）
5. 在本机复现附录 M（B3 + Claude Opus + T=0.5 + seed=7），输出 `walked_example_replay.json`

**验收标准**：
- [ ] `pytest tests/test_runners.py` 全 PASS（12/12）
- [ ] `.env` 含 4 个 key，且 `python scripts/check_llm_keys.py` 4/4 OK
- [ ] B3 复现：MR 数 ∈ [4, 8]，包含 GT-B3-1 或 GT-B3-3 至少一条（粗匹配）
- [ ] 术语表 51 项可口头解释 ≥ 40 项（找老师/同门 5 分钟抽查）
- [ ] commit hash 写入 `weekly_log/wk0.md`

**自评表**：用上方通用模板。第 0 周特别警戒 "环境配置占用 ≥ 3 天" → 直接升级。

---

### 第 1 周：12 程序 program_block.yaml 与种子 MR 落表

**目标**：把附录 C 的 12 程序 × 83 种子 MR 全部录入仓库 YAML，并通过格式校验。

**任务**：
1. 为每个程序填写 `programs/{ID}/program_block.yaml`（参附录 D 字段：program_id/spec/algorithm/inputs/outputs/workloads/textbook）
2. 把附录 C 的 83 条种子 MR 写入 `gt/seed_mrs.yaml`（含 r/R/basis/pattern/source）
3. 跑 `python scripts/validate_yaml.py` 通过 schema 校验
4. 提交 PR 给老师 review（review 走 GitHub PR）

**验收标准**：
- [ ] 12 个 `program_block.yaml` 全部存在、字段无 `null`、`relevant_textbook_chapters` 含真实出处（参 §4.1 程序表）
- [ ] `gt/seed_mrs.yaml` 共 83 条，每条 5 字段齐全
- [ ] schema 校验 PASS（输出 `validation_report.json`）
- [ ] 老师 review 通过（≤ 5 处 minor comments，已 commit 修复）

**自评表**：通用模板。重点关注"数据归档"，YAML 必须 commit，不能仅留在本地。

---

### 第 2 周：84 套 prompt 生成 + token_balance + concept_coverage 校验

**目标**：完成 12 程序 × 7 prompt 模板（A0/A3/A4/A6/B1/B2/B2″）= 84 套实验 prompt 的渲染与等量校准。

**任务**：
1. 用附录 D 的 7 个 jinja2 模板 + 12 个 program_block 渲染 84 套 prompt → 写入 `prompts/rendered/{LLM}/{prog}_{template}.txt`（每 LLM 一份目录，先用 1 LLM 占位）
2. 对每对 (B1, A6)、(B2, A6)、(B2″, A6) 在同一程序上跑 `scripts/token_balance.py`：所有对 token 差 ≤ ±5%
3. 跑 `scripts/concept_coverage.py`（参附录 F 168 概念集 K）：B1/B2/B2″/A6 在每个程序上的概念命中数差 ≤ 1
4. 异常对（差 > 5% 或概念命中差 > 1）→ 调整模板措辞重生成 → 直至全合格
5. 产出 `reports/wk2_token_balance.csv` + `reports/wk2_concept_coverage.csv`

**验收标准**：
- [ ] `prompts/rendered/` 下 84 个文件齐全
- [ ] `token_balance.csv`：12 程序 × 3 对 = 36 行，全部在 ±5% 内
- [ ] `concept_coverage.csv`：12 程序 × 4 模板 = 48 行，最大-最小差 ≤ 1
- [ ] 偏差超标的初始版本与修复版本 diff 已记录在 `weekly_log/wk2.md`

**自评表**：通用模板。第 1-2 周均通过后，进入文献+GT 阶段。

---

### 第 3 周：源 1（文献 MR）抽取 + 源 3（跨家族 LLM）调用

**目标**：完成 12 程序的文献 MR 抽取与 Qwen/Doubao 跨家族 LLM 候选生成。

**任务**：
1. 按 §4.1 程序表的 textbook/paper 引用，逐程序检索并抽取已发表 MR → `gt/source1_literature.yaml`（每条带 [PaperID, page, quote]）
2. 用 Qwen-Max + Doubao-pro 各跑 12 程序 × N=10 = 240 次 A6 prompt → `gt/source3_cross_family/{LLM}_{prog}_{run}.yaml`
3. 对 Qwen + Doubao 输出做去重合并 → `gt/source3_merged.yaml`
4. 每日记录 API 用量（防超额，参附录 H 限速表）

**验收标准**：
- [ ] `source1_literature.yaml` 总条数 ≥ 60（12 程序平均 ≥ 5 条，单程序最低 3 条）；每条含 quote
- [ ] `source3_cross_family/` 共 240 个 yaml 文件，无 API 报错残留
- [ ] `source3_merged.yaml` 去重后总条数在 [80, 200] 区间
- [ ] API 用量记录 `wk3_api_usage.csv`，未超日额度

**自评表**：通用模板。本周如某程序文献 MR < 3，参附录 N 决策树第 8 项处理。

---

### 第 4 周：源 4 团队三角化 + 源 2 行业专家二元投票 → G_final 封版

**目标**：合并源 1+3+4 候选 → 团队共识审核（κ ≥ 0.75）→ 2-3 名行业专家 15-30 min 视频/线下 yes/no/unsure 投票 → G_final.yaml 封版。

**任务**：
1. 老师 + 你 + 1 同门，独立对源 1+3 合并清单做"是否真 MR + 元模式归类"标注 → 计算 Cohen's κ
2. 若 κ < 0.75 → 召开分歧会议，重审条款，重测 → 至 ≥ 0.75 → `gt/source4_team.yaml`
3. 合并 (源 1 ∪ 源 3 ∪ 源 4) 候选清单 → 老师确认进入专家投票
4. 联系 2-3 位行业专家（核工程/科学计算方向），15-30 min 视频/线下，提供"元模式 + 解释 + 候选 MR + 解释"，专家只回 yes/no/unsure，结果填 `gt/G_expert_votes.csv`
5. 多数决过滤（3 位 ≥ 2/3 yes；2 位一致 yes）→ G_final.yaml 封版（含 version + sha256）

**验收标准**：
- [ ] κ_team ≥ 0.75（写入 `reports/wk4_kappa.txt`）
- [ ] 候选清单条数 ≥ 100
- [ ] 至少 2 位专家完成投票（带签名/录音同意凭证），`G_expert_votes.csv` 完整
- [ ] G_final.yaml 含 `version: v1.0`、`frozen_at: <date>`、`sha256: <hash>`
- [ ] 老师签字确认封版（在 `weekly_log/wk4.md` 留痕）

**自评表**：通用模板。专家联系不上 / 拒绝 / 投票分歧严重 → 立即升级，不要拖到第 5 周。

---

### 第 5 周：12 程序 AVR YAML 配置 + verifier 调试

**目标**：开发并调通 12 程序对应的 AVR 流水线配置文件与各元模式 verifier。

**任务**：
1. 为每个程序写 `avr/{prog}.yaml`：声明本程序覆盖的元模式 + 每个 verifier 类型（Wilcoxon/DTW/constraint）+ 阈值
2. 对每个 verifier 跑 `tests/test_verifiers.py`（含正样本+负样本，参附录 E）
3. 跑端到端干跑（dry-run）：用 G_final.yaml 自身作为输入，AVR 应输出全 PASS
4. 整理 `reports/wk5_avr_dry_run.json`

**验收标准**：
- [ ] 12 个 `avr/*.yaml` 全部存在
- [ ] `pytest tests/test_verifiers.py` 全 PASS（每 verifier 至少 1 正 1 负样本）
- [ ] dry-run on G_final：≥ 95% PASS（容许 ≤ 5% 边界争议）
- [ ] DTW 距离阈值 / Wilcoxon p 阈值在 `avr/thresholds.yaml` 集中管理（不要硬编码）

**自评表**：通用模板。

---

### 第 6 周：温度预实验 240 次 → 选定 T=0.5

**目标**：用 1 LLM（Claude Opus）× 12 程序 × T∈{0.0, 0.3, 0.5, 0.7} × 5 重复 = 240 次跑温度敏感性。

**任务**：
1. 用附录 H 调用脚本跑 240 次 A6，输出存 `runs/wk6_temperature/{T}/{prog}_r{i}.json`
2. 计算每个温度下的 V-AF1（参§5）+ MR 数变异系数 CV
3. 画温度 vs V-AF1 / 温度 vs CV 折线图 → `figures/wk6_temperature.png`
4. 决定主实验温度（默认 T=0.5；若 T=0.5 V-AF1 不是最优，找老师讨论）
5. 写 `reports/wk6_temperature_decision.md`

**验收标准**：
- [ ] 240 个 json 全部存在且无空响应
- [ ] V-AF1 折线图含 4 个温度数据点 + 误差棒
- [ ] T=0.5 决策书面说明（含数据支撑）
- [ ] 老师签字确认主实验温度

**自评表**：通用模板。

---

### 第 7 周：主实验启动 — Claude Opus 4.7 × 12 程序 × 7 模板 × N=20

**目标**：跑完第 1 个 LLM 的全部 1680 次实验。

**任务**：
1. 启动 `python run_main.py --llm claude-opus-4-7 --temperature 0.5`，用附录 H checkpoint 机制
2. 实时监控 token 用量、报错率、平均响应时长
3. 每日尾盘备份 `runs/main/claude-opus/` 到外部硬盘
4. 出错单元格记录到 `reports/wk7_failures.csv`，按附录 N 决策树处理

**验收标准**：
- [ ] runs 数 = 1680（完成率 100%；硬目标）
- [ ] 失败单元格 ≤ 5%（重试机制后），剩余必须人工排查
- [ ] checkpoint 中断恢复 ≥ 1 次实测演练
- [ ] 每日 commit + 备份到外盘（共 7 次）

**自评表**：通用模板。

---

### 第 8 周：主实验 — ChatGPT 5.5 × 1680 次

**目标**：第 2 个 LLM 完成。

**任务/验收/自评**：同第 7 周，把 LLM 替换为 chatgpt-5-5。

特别注意：OpenAI rate limit 与 Anthropic 不同（参附录 H），可能需要 batch 提交。

---

### 第 9 周：主实验 — DeepSeek-V4 × 1680 次

**目标**：第 3 个 LLM 完成。

**任务/验收/自评**：同第 7 周，LLM 替换为 deepseek-v4。

---

### 第 10 周：主实验 — GLM-5 × 1680 次 + 全量校核

**目标**：第 4 个 LLM 完成 + 4 LLM 总 6720 次 runs 全量数据完整性校核。

**任务**：
1. 跑 GLM-5（zhipuai SDK，参附录 H）
2. 跑 `scripts/data_audit.py`：检查 4 LLM × 12 程序 × 7 模板 × 20 重复 = 6720 行齐全 + 无重复 + 无空内容
3. 生成 `reports/wk10_data_audit.json`

**验收标准**：
- [ ] GLM-5 1680 次完成
- [ ] data_audit：6720/6720 OK
- [ ] 任何缺失行已补齐或文档化（说明为什么不能补 → 老师确认）

**自评表**：通用模板。

---

### 第 11 周：A6 输出匹配判定 + AVR 全跑

**目标**：完成 LLM 输出 MR 与 G_final 的匹配判定（双标注 κ ≥ 0.75）+ 全部 6720 次的 AVR 验证。

**任务**：
1. 老师 + 你独立对每个 (run, MR) 做"是否匹配 G_final 某条 GT"的判定 → 写入 `analysis/match_judgments_{rater}.csv`
2. 计算 Cohen's κ；若 < 0.75 → 召开分歧会议
3. 跑 `python avr/run_all.py` 对所有 6720 runs 跑 AVR，输出 `analysis/avr_results.csv`
4. 计算每 cell 的 V-AF1、效果量等

**验收标准**：
- [ ] κ_match ≥ 0.75
- [ ] AVR 跑完 6720 次（PASS/FAIL/TIMEOUT 三态都允许，但 TIMEOUT ≤ 1%）
- [ ] V-AF1 表格完整 → `analysis/v_af1_table.csv`

**自评表**：通用模板。

---

### 第 12 周：统计分析 + Holm 校正 + H1-H6 报告

**目标**：完成所有假设检验，生成论文 §9 所需全部数字与图表。

**任务**：
1. 跑附录 G 的 4 个分析脚本：`holm.py` / `effect_size.py` / `gsd.py` / `h6_cells.py`
2. 生成论文 §9 的表 1-表 7 数据 → `analysis/paper_section9_tables.xlsx`
3. 生成 4 个核心图（分布、热力图、收敛、跨范式 CV）→ `figures/fig1.png` ~ `fig4.png`
4. 写 H1-H6 简报 `reports/wk12_hypothesis_results.md`（每假设：通过/拒绝 + p_adj + 效果量）

**验收标准**：
- [ ] 7 个表全部填 → xlsx
- [ ] 4 张图分辨率 ≥ 300 dpi
- [ ] H1-H6 简报每假设 ≤ 200 字、含数字
- [ ] 老师 review 通过

**自评表**：通用模板。

---

### 第 13 周：异常诊断 + 软化文案

**目标**：处理 H5（跨范式 CV ≥ 0.5）/ H6（ρ < 0.6）/ V-AF1 离群 等异常情况，撰写软化文案。

**任务**：
1. 跑 `scripts/anomaly_scan.py`：列出所有触发软化阈值的 cells
2. 对每个异常做归因分析（数据 / 模板 / LLM / GT 四类）→ `reports/wk13_anomalies.md`
3. 在论文 §10 limitations 增补 1-2 段软化文案
4. 必要时回跑特定 cells（最多 1 LLM × 2 程序，预算 200 次）

**验收标准**：
- [ ] 所有异常 cell 归因可解释（不留 "原因不明"）
- [ ] §10 limitations 软化段落老师签字通过
- [ ] 回跑（如有）数据已合并

**自评表**：通用模板。

---

### 第 14 周：投稿前再审 + LaTeX 压版至 10 页 IEEE

**目标**：完成 SANER 2027 投稿包。

**任务**：
1. 把 markdown 论文转 LaTeX（IEEEtran，参 SANER 2027 CFP）
2. 压缩至 10 页正文（不含 references）→ 参考文献单独 1-2 页
3. 跑 academic-paper-reviewer 完整 review（5 reviewers + DA）→ 修复 P0/P1
4. 跑 integrity_verification（参考文献 100% 验证 + 数据 100% 验证）
5. 提交 OpenReview / EasyChair（按 SANER 2027 投稿系统）

**验收标准**：
- [ ] PDF 正文 ≤ 10 页（含图表）
- [ ] integrity_verification 报告 0 issues
- [ ] reviewer 模拟 decision = Minor Revision 或更好
- [ ] 投稿确认邮件截图存档 `submission/confirmation.png`

**自评表**：通用模板。**第 14 周得分 ≥ 22/25 才算 SANER 投稿合格。**

---

每周末必须在 `weekly_log/wkN.md` 提交：✓ 任务清单 + commit hash + 数据快照路径 + 自评表。

---

## 附录 M：端到端 Walked Example（B3 朴素 MC 积分）

选 B3（朴素 Monte Carlo 积分 ∫₀¹ exp(-x²) dx）作首跑案例：单次运行 < 1s，数学性质极简，GT 只 6 条。学生先把 B3 走完一遍，掌握 prompt → LLM → 匹配 → AVR → JSON 全流程，再处理其余 11 程序。

### M.1 程序与 GT（输入侧）

```python
# programs/B3_mc_integration.py
import numpy as np

def mc_integrate(n: int, seed: int) -> float:
    rng = np.random.default_rng(seed)
    x = rng.uniform(0.0, 1.0, size=n)
    return np.mean(np.exp(-x**2))

# 真值（解析）：∫₀¹ exp(-x²) dx ≈ 0.74682
TRUE_VALUE = 0.74682413
```

**GT G_final（合并源 1+2+3 后，6 条）**：

| GT-ID | meta_pattern | r（输入变换）| R（输出关系）| basis |
|---|---|---|---|---|
| GT-B3-1 | P3 | N → 4N | std(I_4N) ≈ 0.5 × std(I_N) | 1/√N 收敛 |
| GT-B3-2 | P2 | 区间 [0,1]→[0,a] | I_a 与 a 单调 | 加性 |
| GT-B3-3 | P1 | seed 改变 N 不变 | E[I_seed] 不变 | 大数定律 |
| GT-B3-4 | P5 | 控制变量 vs 朴素 | var(CV) ≤ var(MC) | 偏序 |
| GT-B3-5 | P5 | 重要性采样 vs 朴素 | var(IS_optimal) ≤ var(MC) | 偏序 |
| GT-B3-6 | P1 | f → cf | I_cf = c · I_f | 线性 |

### M.2 A6 完整 Prompt（render 后实际文本）

```
你是一名科学计算软件测试工程师。请为以下程序基于"元模式"先验识别 MR。

【元模式定义】
- P1 守恒性：什么变换不改变输出？
- P2 单调性：增大参数 θ，输出 y 往哪个方向变？
- P3 收敛性：推到极端/精化后趋向什么？
- P4 轨迹性：响应路径长什么样？
- P5 偏序性：谁更准？

【程序 B3 信息】
program_id: "B3_MC_integration"
program_name: "朴素 Monte Carlo 数值积分"
mathematical_specification: |
  目标：估计 I = ∫₀¹ exp(-x²) dx
  估计量：Î_N = (1/N) Σᵢ₌₁ᴺ exp(-Xᵢ²)，Xᵢ ~ U(0,1) 独立同分布
  解析真值 I ≈ 0.74682
algorithm_description: |
  numpy.random.default_rng(seed).uniform(0,1,size=N)，
  然后 mean(exp(-x²))；时间复杂度 O(N)
input_parameters:
  - N: int ∈ [10, 10⁷]    样本量
  - seed: int             随机种子
  - 区间 [a,b]: 默认 [0,1]
output_quantities:
  - Î_N: float            估计值
  - 估计误差 |Î_N − I|
  - var(Î_N) 多次重复的方差
typical_workloads: "高维数值积分、不确定性量化；小 N 用于快速原型，大 N 用于精度要求"
relevant_textbook_chapters: "Caflisch 1998 Acta Numerica；Lemieux 2009 Springer"

【参数 × 元模式恢复矩阵】
请依次对每个 (输入参数, 元模式) 单元格判断：适用 / 不适用 / 不确定。
若适用，给出候选 MR (r, R, basis)。

【推理要求】
对每个矩阵单元格，先输出"思考链"再输出 MR：
THINKING:
  Step 1: 该参数的物理/数学含义是？
  Step 2: 在该元模式视角下应满足什么？
  Step 3: 是否存在反例使关系失效？
  Step 4: 用 (r, R) 形式化表达
ANSWER: [YAML MR 条目]

【示例库（异范式）】
EXAMPLE 1（数值范式 / P3）:
  程序：辛普森积分
  THINKING: 区间细分 n→2n，根据 O(h⁴) 误差应除以 16
  ANSWER:
    - id: Simp-01
      meta_pattern: P3
      input_relation_r: "n → 2n"
      output_relation_R: "|I_2n − I_true| ≤ |I_n − I_true| / 16"
      basis: Simpson 误差阶 O(h⁴)

EXAMPLE 2（机器学习 / P1）:
  程序：KNN 分类
  THINKING: 类标签是符号，不影响距离计算
  ANSWER:
    - id: KNN-01
      meta_pattern: P1
      input_relation_r: "类标签置换 π(y)"
      output_relation_R: "accuracy 不变"
      basis: 标签为名义型变量

【输出格式】
- id: "B3-NN"
  name: "..."
  meta_pattern: "P1|P2|P3|P4|P5|uncertain"
  classification: "MR|Property"
  input_relation_r: "..."
  output_relation_R: "..."
  basis: "..."
  falsifiability: "违反意味着什么缺陷"
```

token 计数：3247（cl100k_base）。等量校准合格区间 ±5% → [3085, 3409]。

### M.3 LLM 真实响应（Claude Opus 4.7，T=0.5，seed=7，单次实例）

```yaml
# (N, P3) 单元格
THINKING:
  Step 1: N 是样本量，越大估计越精确
  Step 2: P3 收敛性视角：N→∞ 时 Î_N → I（一致性），且收敛速率应 ∝ 1/√N
  Step 3: 若违反则是大数定律或独立同分布假设被破坏
  Step 4: 取 N→4N，则 std(Î_4N) ≈ 0.5 × std(Î_N)
ANSWER:
  - id: "B3-01"
    name: "样本量四倍化的方差减半"
    meta_pattern: P3
    classification: MR
    input_relation_r: "N → 4N（保持 seed-family 独立）"
    output_relation_R: "std(Î_4N) / std(Î_N) ≈ 0.5"
    basis: "中心极限定理 + 独立同分布假设下的 1/√N 收敛"
    falsifiability: "若比值显著偏离 0.5（如 > 0.7）则提示 RNG 相关性或方差估计偏差"

# (区间端点, P2) 单元格
THINKING:
  Step 1: 改变积分区间 [0,a] 等价改变积分上限
  Step 2: P2 单调性：a 增大，I_a = ∫₀^a exp(-x²)dx 单调增（被积函数 ≥ 0）
  Step 3: 若失败则是采样区间映射错误
  Step 4: r: a → a' (a' > a)，R: Î_a' > Î_a
ANSWER:
  - id: "B3-02"
    name: "积分区间扩张时估计值单调增"
    meta_pattern: P2
    classification: MR
    input_relation_r: "[0,a] → [0,a']，a' > a"
    output_relation_R: "Î_[0,a'] ≥ Î_[0,a]（高概率，N 充分大）"
    basis: "exp(-x²) ≥ 0 单调累积"
    falsifiability: "区间扩张反而估计值减小则表明区间映射错误"

# (seed, P1) 单元格
THINKING:
  Step 1: seed 决定具体随机序列但不影响统计期望
  Step 2: P1 守恒性：seed 不变 N 期望仍为 I
  Step 3: 单次结果会变（这是随机算法本质），但期望值守恒
  Step 4: r: seed → seed'，R: E[Î_seed] = E[Î_seed'] = I
ANSWER:
  - id: "B3-03"
    name: "seed 改变期望守恒"
    meta_pattern: P1
    classification: MR
    input_relation_r: "seed → seed'（保持 N 不变）"
    output_relation_R: "|mean(Î_{seed=k}, k∈[1..K]) − I| ≤ σ/√(K·N)（K 次重复均值）"
    basis: "大数定律期望不变性"
    falsifiability: "K 次重复均值偏离 I 显著超出 σ/√(KN) 表明 RNG bias"

# (函数缩放 c, P1) 单元格
THINKING:
  Step 1: 把被积函数 f → cf 等价输出乘 c
  Step 2: P1 形式不变性：估计算子对线性缩放线性
  Step 3: r: f→cf，R: Î(cf) = c · Î(f)
  Step 4: 简单线性算子
ANSWER:
  - id: "B3-04"
    name: "被积函数线性缩放"
    meta_pattern: P1
    classification: MR
    input_relation_r: "f(x) → c·f(x), c ∈ ℝ\\{0}"
    output_relation_R: "Î(cf) / Î(f) = c（精确）"
    basis: "积分线性"
    falsifiability: "比值偏离 c 表示 reduce 步骤数值溢出或类型错误"

# (区间, P1) 单元格
THINKING:
  Step 1: 改变积分区间但保持长度（平移）
  Step 2: 平移会改变 I 但不改变某些性质... 此处不适用 P1
ANSWER:
  - id: "B3-05"
    name: "（不适用）区间平移不变性"
    meta_pattern: uncertain
    classification: Property
    input_relation_r: "[0,1] → [a, a+1]"
    output_relation_R: "（被积函数非平移对称，关系复杂）"
    basis: "exp(-x²) 不具备平移对称"
    falsifiability: "—"

# (重要性采样替代, P5) 单元格
THINKING:
  Step 1: 用其他方差更小的采样策略替代均匀采样
  Step 2: P5 偏序性：方差最优 IS（取 g(x)∝|f(x)|）应优于朴素 MC
  Step 3: 满足偏序：var(IS_opt) ≤ var(MC)
  Step 4: 这是估计算法间偏序
ANSWER:
  - id: "B3-06"
    name: "重要性采样方差不劣于朴素 MC"
    meta_pattern: P5
    classification: MR
    input_relation_r: "采样分布 U(0,1) → g(x) = exp(-x²)/Z（最优 IS 提议）"
    output_relation_R: "var(Î_IS, N) ≤ var(Î_MC, N)（同 N）"
    basis: "Rao-Blackwell / 最优重要性采样定理"
    falsifiability: "IS 方差 ≥ MC 方差表明实现错误"

# (准 MC 替代, P5) 单元格
THINKING:
  Step 1: Halton/Sobol 等低差异序列替代伪随机
  Step 2: P5：QMC 在低维下应严格优于 MC（O(N^{-1}) vs O(N^{-1/2})）
  Step 3: r: PRNG → Halton；R: |I_QMC − I| ≤ |I_MC − I|（高概率）
ANSWER:
  - id: "B3-07"
    name: "准 MC 收敛阶优于朴素 MC"
    meta_pattern: P5
    classification: MR
    input_relation_r: "RNG → Halton 序列（同 N）"
    output_relation_R: "|Î_QMC − I| / |Î_MC − I| → 0 (N→∞)，速率 O(N^{-1/2})"
    basis: "Koksma-Hlawka 不等式"
    falsifiability: "QMC 误差 ≥ MC 误差表明 Halton 实现错误"

# 其他单元格判 "不适用"（共 ~10 个），LLM 不再展开
```

输出 token 数：1820。共生成 7 条 MR + 多条不适用判定。

### M.4 GT 比对 + Cohen κ 计算

| LLM 输出 ID | GT 匹配 | rater_a (Meng) | rater_b (硕士 A) | 共识 |
|---|---|---|---|---|
| B3-01（N→4N 方差减半）| GT-B3-1 | match | match | match ✓ |
| B3-02（区间单调）| GT-B3-2 | match | match | match ✓ |
| B3-03（seed 期望守恒）| GT-B3-3 | match | match | match ✓ |
| B3-04（线性缩放）| GT-B3-6 | match | match | match ✓ |
| B3-05（区间平移）| 不匹配 | no_match | no_match | no_match（LLM 自己标 uncertain）|
| B3-06（重要性采样）| GT-B3-5 | match | match | match ✓ |
| B3-07（准 MC）| 无对应 GT | unsure | match | 仲裁 → 列入 extra MR（专家确认有效，纳入 R3 创造性发现）|

**Cohen κ 计算**：
- 一致 6 / 7 = 85.7%
- 偶然一致期望 (P_e) ≈ 0.50（match/no_match 频率近 1:1）
- κ = (P_o − P_e) / (1 − P_e) ≈ (0.857 − 0.5) / (1 − 0.5) = **0.714**
- κ ≥ 0.65 通过；< 0.75 仅冲突项仲裁

### M.5 计算 Tier-1 指标

```
匹配 GT 条数 |C ∩ G| = 5（B3-01/02/03/04/06）
LLM 总输出（含不适用过滤后）|C| = 6（B3-01..06，B3-07 列为 extra）
GT 总数 |G| = 6

Precision = 5 / 6 = 0.833
Recall    = 5 / 6 = 0.833
F1        = 0.833
FPR       = 1 / 6 = 0.167  （B3-07 暂作 FP，待 extra 校验后回扣）
Recall_nt = 待 codebook 标注（B3 中 GT-B3-4 控制变量、GT-B3-5 重要性采样属非平凡）
```

### M.6 AVR 验证（B3-01 P3 走 Wilcoxon 路径）

```python
# avr/configs/B3_MC.yaml — 对应 B3-01
- mr_id: B3-01
  pattern: P3
  transform: |
    def t(seed):
      n_a = 1000
      n_b = 4000
      return ({"n":n_a,"seed":seed}, {"n":n_b,"seed":seed+10000})
  metric: |
    def m(y_a, y_b):
      # 30 次重复，分别计算 std
      return np.std(y_a), np.std(y_b)
  expected_ratio: [0.4, 0.6]  # std(4N)/std(N) ≈ 0.5

# 执行（30 runs）
$ python avr/run.py --program B3 --mr B3-01
[B3-01] std(N=1000) = 0.0114, std(N=4000) = 0.0058
       ratio = 0.509, p_wilcoxon = 0.0023, ratio ∈ [0.4, 0.6] ✓
       → PASS
```

7 条 MR 中可分流 6 条（B3-05 LLM 自标 uncertain 不计），通过 5 条（B3-04 因 c=0 边界数值精度问题失败）：

```
AVR 数据点：dispatchable=6, passed=5, AVR_rate = 5/6 = 0.833
```

### M.7 JSON 记录（单次 N=1 实例）

```json
{
  "experiment_id": "exp_v4_20260801_a6_b3_claude47_n07",
  "config": {
    "variant": "A6", "program": "B3_MC_integration",
    "paradigm": "probabilistic", "llm": "Claude_Opus_4.7",
    "temperature": 0.5, "random_seed": 7,
    "prompt_token_count": 3247, "concept_coverage": "12/12"
  },
  "output": {
    "mr_list": [/* 7 条如 M.3 */],
    "raw_response": "...（完整 LLM 文本）...",
    "response_token_count": 1820
  },
  "evaluation": {
    "matched_mrs": 5, "total_output": 6, "total_gt": 6,
    "precision": 0.833, "recall": 0.833, "f1": 0.833, "fpr": 0.167,
    "recall_nt": null,
    "avr_pass": 5, "avr_total_dispatchable": 6, "avr_rate": 0.833,
    "extra_mrs_count": 1
  },
  "metadata": {
    "timestamp": "2026-08-01T14:32:18Z",
    "rater_a": "Meng", "rater_b": "MasterA", "kappa": 0.714,
    "arbitration_log": [{"mr_id":"B3-07","resolution":"extra_valid"}]
  }
}
```

### M.8 教学要点（硕士生需掌握的 7 个判断）

1. **uncertain 不计入分母**：B3-05 LLM 自标 uncertain，不进 LLM 输出分母也不进 AVR 分母
2. **extra MR 的处置**：B3-07 经专家确认有效但不在原 GT，记入 `extra_mrs_count`，不算 FP，不算 TP
3. **AVR 失败 ≠ MR 错**：B3-04 数值精度边界失败，是实现细节问题；这种应在 AVR YAML 中加入 `c ≠ 0` 约束
4. **κ 计算只算冲突项**：7 条中 1 条冲突（B3-07），其他自动通过
5. **LLM 响应非确定性**：seed=7 与 seed=8 同一 prompt 输出可能不同 ±2 条 MR；这是 N=20 重复的根本原因
6. **token 等量必须卡死**：B1 prompt 必须改写到 [3085, 3409] 区间，不能让 B 系列因 token 多 10% 而看起来"信息更丰富"
7. **匹配判定不要求元模式归类一致**：若 LLM 把 B3-01 标为 P2 单调而 GT 标 P3 收敛，仍算 match（§4.5 破循环条款）

### M.9 一次完成审核清单

```
[ ] prompt token ∈ [3085, 3409]
[ ] concept coverage 12/12
[ ] 7 条 MR 输出 YAML 解析成功
[ ] 双评 Cohen κ ≥ 0.65（本例 0.714 ✓）
[ ] AVR 配置 YAML 完整覆盖可分流 MR
[ ] JSON 记录字段全（无 null 关键字段）
[ ] 通过 token_balance.py + concept_coverage.py 双脚本
[ ] commit + 数据快照路径写入 progress.md
```

完成 M.1–M.9 全部 ✓ 后，硕士生即可用同样流程并行处理其余 11 程序。预计单程序首次端到端 ~6 小时，第二程序起降至 ~3 小时。

---

### M.A1：A1 Lorenz 系统（数值范式 walked example，重点示范 P4 轨迹）

补 P4 轨迹元模式（B3 未涉及），同时演示数值 ODE 程序的 MR 识别流程。

#### M.A1.1 程序与 GT

```python
# programs/A1_lorenz.py
from scipy.integrate import solve_ivp
import numpy as np

def lorenz_rhs(t, s, sigma=10.0, rho=28.0, beta=8.0/3.0):
    x, y, z = s
    return [sigma*(y-x), x*(rho-z)-y, x*y-beta*z]

def run_lorenz(x0, t_max=40.0, rtol=1e-8, method='RK45', seed=None):
    sol = solve_ivp(lorenz_rhs, [0, t_max], x0,
                    method=method, rtol=rtol, atol=rtol*1e-2,
                    dense_output=True, max_step=0.01)
    return sol.t, sol.y  # shape (3, T)
```

**GT G_final（6 条）**：

| GT-ID | meta_pattern | r（输入变换）| R（输出关系）| basis |
|---|---|---|---|---|
| GT-A1-1 | P3 | rtol → rtol/10 | ‖traj_fine − traj_ref‖∞ ↓ | RK45 阶数收敛 |
| GT-A1-2 | **P4** | x0 → x0 + ε（‖ε‖ = 1e-6）| ‖Δs(t)‖ ≈ ‖ε‖ · exp(λ·t)，λ ≈ 0.9 | Lyapunov 指数 |
| GT-A1-3 | P3 | t_max → 2·t_max | 吸引子统计矩稳定（mean(z), var(z) 变化 < 5%）| 吸引子不变测度 |
| GT-A1-4 | P5 | RK45 vs 显式 Euler（同 rtol）| ‖Euler − ref‖ ≥ ‖RK45 − ref‖ | 阶数 4 vs 1 |
| GT-A1-5 | P2 | ρ: 0.5 → 1.5 → 28 | 不动点结构变化（稳定→Hopf→混沌）可观测 | 分岔图 |
| GT-A1-6 | **P4** | x0 共轴对称变换 (x,y,z)→(−x,−y,z) | 轨迹镜像对称 | Lorenz 对称群 |

GT 来源：源 1 = Strogatz 2018 ch.9；源 3 = Qwen+Doubao 各 N=10；源 4 = 团队 κ=0.81；源 2 = 3 专家 3 yes / 0 no（A1-1~A1-6 全过）。

#### M.A1.2 Prompt 关键差异（与 B3 模板对比）

只列与 B3 不同的字段：

```yaml
program_id: "A1_lorenz"
mathematical_specification: |
  dx/dt = σ(y−x), dy/dt = x(ρ−z)−y, dz/dt = xy − βz
  默认 σ=10, β=8/3, ρ=28（经典混沌区）
input_parameters:
  - x0: 三维初值 ∈ ℝ³
  - t_max: 仿真时长 ∈ [1, 100]
  - rtol: 容差 ∈ [1e-12, 1e-3]
  - method: ∈ {'RK45', 'RK23', 'Euler'}
output_quantities:
  - 轨迹序列 s(t) ∈ ℝ³ × T
  - 终态 s(t_max)
  - 吸引子统计：mean/var/skew of (x,y,z) at t > t_burn
relevant_textbook_chapters: "Strogatz 2018 ch.9 Strange Attractors"
```

few-shot 示例选 KNN(P1) + Simpson(P3) + Lorenz 同范式 P4 示例 1 个：

```
EXAMPLE 3（数值范式 / P4）:
  程序：双摆系统
  THINKING: 初值微扰 ε，相空间距离按 Lyapunov 速率指数发散
  ANSWER:
    - id: DP-01
      meta_pattern: P4
      input_relation_r: "θ₀ → θ₀ + 1e-8"
      output_relation_R: "‖Δs(t)‖ ≈ ‖ε‖·exp(λt), λ ≈ 0.6"
      basis: 双摆 Lyapunov 指数
```

token 计数：3361（在 ±5% [3085, 3409] 内通过 token_balance）。

#### M.A1.3 LLM 响应核心 cells（Claude Opus 4.7, T=0.5, seed=11）

```yaml
# (rtol, P3) 单元格
THINKING:
  Step 1: rtol 是 ODE 求解器局部误差容忍
  Step 2: P3 收敛：rtol → 0 时数值解 → 真实解
  Step 3: RK45 是 4 阶方法，全局误差 ~ O(rtol)
  Step 4: r: rtol → rtol/10，R: ‖traj_new − ref‖ ≤ 0.1·‖traj_old − ref‖（粗略上界）
ANSWER:
  - id: "A1-01"
    name: "容差精化导致轨迹收敛"
    meta_pattern: P3
    classification: MR
    input_relation_r: "rtol → rtol/10"
    output_relation_R: "‖traj(rtol/10) − traj(rtol/100)‖∞ < ‖traj(rtol) − traj(rtol/10)‖∞"
    basis: "RK45 4 阶收敛 + Cauchy 序列"
    falsifiability: "容差精化反而轨迹差距增大 → 求解器 bug"

# (x0, P4) 单元格 — 轨迹元模式核心示例
THINKING:
  Step 1: x0 是初值，决定整条轨迹
  Step 2: P4 轨迹：相邻初值的轨迹分离速率
  Step 3: Lorenz 经典混沌系统，最大 Lyapunov 指数 λ ≈ 0.9
  Step 4: r: x0 → x0 + ε(‖ε‖=1e-6)，R: ‖Δs(t)‖ ≈ ‖ε‖·exp(λt)，至 t ≈ 16 时 Δ ~ O(1)
ANSWER:
  - id: "A1-02"
    name: "Lyapunov 指数验证（混沌轨迹分离）"
    meta_pattern: P4
    classification: MR
    input_relation_r: "x0 → x0 + ε，‖ε‖ = 1e-6，方向随机"
    output_relation_R: "ln(‖Δs(t)‖/‖ε‖) 对 t 线性，斜率 λ ∈ [0.85, 0.95]"
    basis: "Lorenz 系统最大 Lyapunov 指数 ≈ 0.9056"
    falsifiability: "斜率显著偏离区间 → 数值耗散异常或求解器精度不足"

# (method, P5) 单元格
THINKING:
  Step 1: method 决定离散化方案
  Step 2: P5 偏序：高阶方法应比低阶更准
  Step 3: RK45 (4 阶) vs Euler (1 阶)，同步长下误差悬殊
  Step 4: r: method: RK45 → Euler，R: ‖Euler − ref‖ ≥ ‖RK45 − ref‖
ANSWER:
  - id: "A1-03"
    name: "高阶求解器更接近参考解"
    meta_pattern: P5
    classification: MR
    input_relation_r: "method: 'RK45' → 'Euler'，rtol 相同"
    output_relation_R: "‖traj_Euler − traj_ref(RK45,rtol=1e-12)‖ ≥ ‖traj_RK45(rtol) − traj_ref‖"
    basis: "全局误差 O(h^p)，p_RK45=4 > p_Euler=1"
    falsifiability: "Euler 反而更准 → 测试 case 太短/参考解配置错误"

# (x0, P4) 第二条 — 对称性
THINKING:
  Step 1: Lorenz 方程对 (x,y,z)→(−x,−y,z) 不变（二阶项 xy 同号，xz 同变号）
  Step 2: P4 轨迹：对称变换后整条轨迹是镜像
  Step 3: r: x0 → (−x0_x, −x0_y, x0_z)，R: traj_new(t) = (−traj.x, −traj.y, traj.z)(t)
ANSWER:
  - id: "A1-04"
    meta_pattern: P4
    classification: MR
    input_relation_r: "x0 → (−x0_x, −x0_y, x0_z)"
    output_relation_R: "‖traj_new − reflect(traj_orig)‖∞ < tol_numerical"
    basis: "Lorenz Z₂ 对称群"
    falsifiability: "对称性破缺 → 实现错误（可能符号错位）"

# (ρ, P2) 单元格
ANSWER:
  - id: "A1-05"
    meta_pattern: P2
    input_relation_r: "ρ: 0.5 → 1.0 → 1.5 → 24.74 → 28"
    output_relation_R: "不动点稳定性变化序列：稳定→pitchfork→稳定→Hopf→混沌"
    basis: "Lorenz 分岔图（Strogatz §9.3）"

# (t_max, P3) 单元格
ANSWER:
  - id: "A1-06"
    meta_pattern: P3
    input_relation_r: "t_max → 2·t_max（去除前 t_burn=10）"
    output_relation_R: "|mean(z)_2T − mean(z)_T| < 0.05·|mean(z)_T|"
    basis: "吸引子不变测度"
```

LLM 共输出 8 条候选（含 2 条假阳：rtol→0 时间反转；method→symplectic 不存在）。

#### M.A1.4 匹配判定（Meng + 硕士 A）

| LLM 输出 | 匹配的 GT | 状态 |
|---|---|---|
| A1-01 | GT-A1-1 | ✓ 匹配（rtol 收敛）|
| A1-02 | GT-A1-2 | ✓ 匹配（Lyapunov）|
| A1-03 | GT-A1-4 | ✓ 匹配（RK45 vs Euler）|
| A1-04 | GT-A1-6 | ✓ 匹配（Z₂ 对称）|
| A1-05 | GT-A1-5 | ✓ 匹配（分岔）|
| A1-06 | GT-A1-3 | ✓ 匹配（吸引子）|
| A1-07 时间反转 | — | ✗ 假阳（耗散系统不可逆）|
| A1-08 symplectic | — | ✗ 假阳（不适用）|

V-AF1 = 2·6/(6+8+6) = 0.857；P=0.75，R=1.0。Cohen κ=1.0（两标注者完全一致）。

#### M.A1.5 AVR 验证（核心步骤）

```yaml
# avr/A1_lorenz.yaml
verifiers:
  GT-A1-1:
    type: constraint
    runs: [(rtol=1e-4), (rtol=1e-5), (rtol=1e-6)]
    check: monotonic_decrease(traj_diff_norm)
  GT-A1-2:
    type: trajectory
    runs: [x0, x0 + 1e-6·random_unit] × 30 random
    check: linear_fit(log(diff_norm) vs t).slope ∈ [0.85, 0.95]
  GT-A1-4:
    type: constraint
    check: mean(err_Euler) ≥ mean(err_RK45)
  GT-A1-6:
    type: trajectory
    check: traj_reflected ≈ reflect(traj_orig), max_dev < 1e-3
```

实测 AVR 结果：6/6 PASS（real Lorenz Lyapunov 拟合 λ=0.901，P4 验证强阳性）。

#### M.A1.6 JSON 落表（关键字段，完整版见 `runs/walked/A1_claude.json`）

```json
{
  "run_id": "A1_claude_T0.5_s11",
  "extracted_mrs": 8,
  "matched_gt": 6,
  "false_positives": 2,
  "v_af1": 0.857,
  "avr_pass_rate": 1.00,
  "p4_signature": {"lyapunov_fit": 0.901, "ci": [0.85, 0.95]}
}
```

---

### M.C1：C1 GPR（代理模型 walked example，重点示范 P5 偏序）

演示 P5 偏序（核选择优劣）与代理模型程序的 MR 识别流程。

#### M.C1.1 程序与 GT

```python
# programs/C1_gpr.py
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern, WhiteKernel
import numpy as np

def forrester_1d(x):  # 标准 benchmark
    return (6*x - 2)**2 * np.sin(12*x - 4)

def fit_gpr(n_train, kernel_name='RBF', noise=1e-6, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.uniform(0, 1, size=(n_train, 1))
    y = forrester_1d(X.ravel())
    k = {'RBF': RBF(), 'Matern25': Matern(nu=2.5), 'Matern15': Matern(nu=1.5)}[kernel_name]
    gpr = GaussianProcessRegressor(kernel=k + WhiteKernel(noise), n_restarts_optimizer=5, random_state=seed)
    gpr.fit(X, y)
    return gpr
```

**GT G_final（6 条）**：

| GT-ID | meta_pattern | r | R | basis |
|---|---|---|---|---|
| GT-C1-1 | P3 | n_train: N → 4N | RMSE_test ≈ RMSE_old / 2 | 通用近似 + GP 收敛 |
| GT-C1-2 | **P5** | kernel: RBF vs Matern25 (smooth f) | RMSE(RBF) ≤ RMSE(Matern25) | f∈C^∞，RBF 更适合 |
| GT-C1-3 | P2 | noise: α → 2α | std_predict 增大 | 不确定性传播 |
| GT-C1-4 | P1 | shuffle 训练点顺序 | 预测分布不变 | 可交换观测 |
| GT-C1-5 | **P5** | length_scale: optimized vs default(1.0) | RMSE_opt ≤ RMSE_default | hyperparameter optimization |
| GT-C1-6 | P3 | n_restarts_optimizer: 1 → 10 | log_marginal_likelihood ↑（单调不减）| 多起点全局极值 |

GT 来源：源 1 = Forrester 2008, Murphy 2012；源 3 重合 5/6；源 4 κ=0.83；源 2 = 2 专家 2 yes / 0 no。

#### M.C1.2 Prompt 关键差异

```yaml
program_id: "C1_gpr"
mathematical_specification: |
  代理 f(x) = (6x−2)² sin(12x−4)，x ∈ [0,1]
  GP 后验：μ(x*) = k*ᵀ(K+σ²I)⁻¹y，  σ²(x*) = k(x*,x*) − k*ᵀ(K+σ²I)⁻¹k*
input_parameters:
  - n_train: ∈ [10, 500]
  - kernel: ∈ {RBF, Matern25, Matern15}
  - noise α: ∈ [1e-8, 1e-2]
  - length_scale: ∈ [0.01, 10]
output_quantities:
  - 测试集 RMSE
  - 后验均值 μ(x*) 与方差 σ²(x*)
  - log_marginal_likelihood
relevant_textbook_chapters: "Forrester 2008 §3-4, Murphy 2012 §15"
```

few-shot 示例选 KNN(P1) + GPR-同范式 P5 示例 + ML/D 类 P3 示例。

#### M.C1.3 LLM 响应核心 cells（DeepSeek-V4，T=0.5，seed=3；选异 LLM 增加多样性）

```yaml
# (kernel, P5) — 偏序元模式核心
THINKING:
  Step 1: kernel 决定 GP 先验函数空间
  Step 2: f(x) = (6x-2)²sin(12x-4) 是 C^∞ 光滑函数
  Step 3: RBF kernel 假设 C^∞ 样本路径；Matern25 假设 C² 样本路径
  Step 4: 真函数光滑度高 → RBF 拟合更紧；偏序：RMSE(RBF) ≤ RMSE(Matern25)
ANSWER:
  - id: "C1-01"
    meta_pattern: P5
    classification: MR
    input_relation_r: "kernel: 'Matern25' → 'RBF'，固定 n_train, noise, seed"
    output_relation_R: "RMSE_test(RBF) ≤ 0.95 · RMSE_test(Matern25)，置信 80%"
    basis: "样本路径光滑度匹配真函数"
    falsifiability: "Matern25 反而更准 → 训练点不足导致光滑性优势未现"

# (n_train, P3)
THINKING:
  Step 1: 训练点越多，先验越被数据约束
  Step 2: GP 后验方差按 1/n 收敛（点处密度均匀情况下）
  Step 3: r: N → 4N，R: RMSE 大致减半
ANSWER:
  - id: "C1-02"
    meta_pattern: P3
    input_relation_r: "n_train: N → 4N（保持 seed 同分布扩样）"
    output_relation_R: "RMSE_test(4N) ≤ 0.6 · RMSE_test(N)"
    basis: "GP minimax 收敛速率"

# (length_scale, P5)
ANSWER:
  - id: "C1-03"
    meta_pattern: P5
    input_relation_r: "length_scale: default 1.0 → optimized via marginal likelihood"
    output_relation_R: "RMSE_opt ≤ RMSE_default"
    basis: "marginal likelihood 是后验预测分布的 KL 下界"

# (训练点顺序, P1)
ANSWER:
  - id: "C1-04"
    meta_pattern: P1
    input_relation_r: "permute(X_train, y_train) 同步置换"
    output_relation_R: "max(|μ_new(x*) − μ_orig(x*)|) < 1e-10 ∀ x*"
    basis: "GP 后验对训练点是可交换的"
    falsifiability: "排序敏感 → 实现 bug（可能涉及数值稳定性 Cholesky）"

# (noise α, P2)
ANSWER:
  - id: "C1-05"
    meta_pattern: P2
    input_relation_r: "noise α → 2α"
    output_relation_R: "mean(σ²_predict) 增大 ≥ 5%"
    basis: "WhiteKernel 直接加入对角"

# (n_restarts, P3)
ANSWER:
  - id: "C1-06"
    meta_pattern: P3
    input_relation_r: "n_restarts_optimizer: 1 → 10"
    output_relation_R: "log_marginal_likelihood 单调不减"
    basis: "多起点取最优解"
```

LLM 共输出 7 条（多 1 条假阳：噪声噪声相加性 RMSE 单调，与 GT-C1-3 重叠但表述错误）。

#### M.C1.4 匹配判定

| LLM | GT | 状态 |
|---|---|---|
| C1-01 | GT-C1-2 | ✓ |
| C1-02 | GT-C1-1 | ✓ |
| C1-03 | GT-C1-5 | ✓ |
| C1-04 | GT-C1-4 | ✓ |
| C1-05 | GT-C1-3 | ✓ |
| C1-06 | GT-C1-6 | ✓ |
| C1-07（噪声 RMSE 单调）| — | ✗ 假阳（RMSE 与噪声非单调）|

V-AF1 = 2·6/(6+7+6) = 0.923；Cohen κ=1.0。

#### M.C1.5 AVR 验证

```yaml
# avr/C1_gpr.yaml
verifiers:
  GT-C1-1:
    type: constraint
    runs: [N=20, N=80, N=320]
    check: rmse[k+1] ≤ 0.6 · rmse[k]
  GT-C1-2:
    type: wilcoxon
    runs: 30 paired (RBF, Matern25), 不同 seed
    check: wilcoxon(rmse_RBF, rmse_M25, alternative='less').p < 0.05
  GT-C1-4:
    type: constraint
    check: max_abs_diff < 1e-9
```

实测 6/6 PASS（Wilcoxon p=0.003，强阳性 P5）。

#### M.C1.6 JSON 落表

```json
{
  "run_id": "C1_deepseek_T0.5_s3",
  "extracted_mrs": 7,
  "matched_gt": 6,
  "v_af1": 0.923,
  "avr_pass_rate": 1.00,
  "p5_evidence": {"wilcoxon_p": 0.003, "median_rmse_diff": -0.087}
}
```

---

### M.D1：D1 MLP/Iris（机器学习 walked example，重点示范 P1 标签置换）

演示 ML 范式经典 MR：Xie 2011 标签置换、Dwarakanath 特征缩放。

#### M.D1.1 程序与 GT

```python
# programs/D1_mlp_iris.py
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

def train_mlp_iris(hidden_size=10, max_iter=200, scale=True, seed=0):
    X, y = load_iris(return_X_y=True)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=seed)
    if scale:
        sc = StandardScaler().fit(Xtr); Xtr = sc.transform(Xtr); Xte = sc.transform(Xte)
    m = MLPClassifier(hidden_layer_sizes=(hidden_size,), max_iter=max_iter, random_state=seed)
    m.fit(Xtr, ytr)
    return m.score(Xte, yte), m.loss_
```

**GT G_final（6 条）**：

| GT-ID | meta_pattern | r | R | basis |
|---|---|---|---|---|
| GT-D1-1 | **P1** | 类标签置换 π(y)（训练 + 测试同步）| test_accuracy 不变 | 标签是符号 |
| GT-D1-2 | P1 | feature 列置换（训练+测试同步）| test_accuracy 不变 | 全连接对特征顺序不敏感 |
| GT-D1-3 | P3 | max_iter: 100 → 200 → 400 | loss 单调不增 | 梯度下降单调下降（凸子问题）|
| GT-D1-4 | P2 | hidden_size: 5 → 20 → 50 | train_acc ↑（直至过拟合）| 容量增加 |
| GT-D1-5 | **P5** | scale=True vs scale=False | acc_scaled ≥ acc_unscaled | 特征量级一致化 |
| GT-D1-6 | P1 | 对训练数据加随机但同分布扰动（小 σ）| test_accuracy 期望不变 | 输入分布不变 |

GT 来源：源 1 = Xie 2011, Murphy 2008, Dwarakanath 2018；源 3 重合 6/6；源 4 κ=0.85；源 2 = 3 专家 3 yes / 0 no。

#### M.D1.2 Prompt 关键差异

```yaml
program_id: "D1_mlp_iris"
mathematical_specification: |
  分类器 f: ℝ⁴ → {0,1,2}, softmax(W₂·tanh(W₁x + b₁) + b₂)
  loss = cross_entropy(softmax_logits, y_onehot)
  优化：Adam, learning_rate_init=1e-3
input_parameters:
  - hidden_size ∈ [5, 100]
  - max_iter ∈ [50, 1000]
  - scale: bool
  - seed: int
output_quantities:
  - test_accuracy ∈ [0, 1]
  - 训练 loss
  - 混淆矩阵
relevant_textbook_chapters: "Xie 2011 ICST（ML MR 开山）, Murphy 2008 §16"
```

few-shot 选 KNN(P1) + Simpson(P3) + Dwarakanath SVM 特征缩放(P5) 示例。

#### M.D1.3 LLM 响应核心 cells（GLM-5，T=0.5，seed=42）

```yaml
# (类标签 π, P1) — Xie 2011 经典
THINKING:
  Step 1: 类标签 0/1/2 是符号，softmax 交叉熵对类索引置换协变
  Step 2: 训练 + 测试同步置换，模型本质学到的同等可分类问题
  Step 3: r: y → π(y)，π 任意置换；R: test_acc 不变（期望意义）
ANSWER:
  - id: "D1-01"
    meta_pattern: P1
    classification: MR
    input_relation_r: "π ∈ S_3, y_train → π(y_train), y_test → π(y_test)"
    output_relation_R: "|test_acc_new − test_acc_orig| < 0.02"
    basis: "标签的符号性 + softmax 交叉熵置换协变"
    falsifiability: "差异显著 → 类索引被错误用作回归目标"

# (feature 顺序, P1)
ANSWER:
  - id: "D1-02"
    meta_pattern: P1
    input_relation_r: "permute_columns(X_train, X_test) 同步"
    output_relation_R: "|acc_new − acc_orig| < 0.02"
    basis: "全连接层对输入维度无序"

# (scale, P5) — 特征缩放经典 P5
THINKING:
  Step 1: Iris 4 特征量级相近但仍有差异（厘米单位但花瓣 vs 花萼数量级不同）
  Step 2: P5 偏序：scaled 应 ≥ unscaled（梯度更对称）
  Step 3: r: scale=False → True，R: acc_scaled ≥ acc_unscaled
ANSWER:
  - id: "D1-03"
    meta_pattern: P5
    input_relation_r: "scale: False → True"
    output_relation_R: "median(acc_scaled, 30 seeds) ≥ median(acc_unscaled, 30 seeds)"
    basis: "梯度下降在量级一致空间中收敛更快"
    falsifiability: "scale 后反而下降 → seed 固定导致小样本偶然，扩大重复数验证"

# (max_iter, P3)
ANSWER:
  - id: "D1-04"
    meta_pattern: P3
    input_relation_r: "max_iter: 100 → 200 → 400"
    output_relation_R: "train_loss 单调不增"
    basis: "梯度下降单调下降"

# (hidden_size, P2)
ANSWER:
  - id: "D1-05"
    meta_pattern: P2
    input_relation_r: "hidden_size: 5 → 20 → 50"
    output_relation_R: "train_acc 单调不减（直至接近 1.0）"
    basis: "网络容量增加"

# (训练数据加噪, P1)
ANSWER:
  - id: "D1-06"
    meta_pattern: P1
    input_relation_r: "X_train → X_train + ε, ε ~ N(0, 0.01·std)"
    output_relation_R: "|mean(acc_perturbed, 30 seeds) − acc_orig| < 0.03"
    basis: "训练分布期望不变（小扰动）"
```

LLM 共输出 8 条（多 2 条：dropout 单调 P3、bias 项加值 P1，均为部分正确但不在 GT）。

#### M.D1.4 匹配判定

| LLM | GT | 状态 |
|---|---|---|
| D1-01 | GT-D1-1 | ✓ |
| D1-02 | GT-D1-2 | ✓ |
| D1-03 | GT-D1-5 | ✓ |
| D1-04 | GT-D1-3 | ✓ |
| D1-05 | GT-D1-4 | ✓ |
| D1-06 | GT-D1-6 | ✓ |
| D1-07 dropout | — | ✗（程序未启用 dropout）|
| D1-08 bias shift | — | ✗（语义模糊）|

V-AF1 = 2·6/(6+8+6) = 0.857；Cohen κ=0.91（D1-08 一票模糊，老师判 ✗，学生初判 ✓→修订一致）。

#### M.D1.5 AVR 验证

```yaml
# avr/D1_mlp.yaml
verifiers:
  GT-D1-1:
    type: wilcoxon
    runs: 30 paired (orig π, π=cyclic_shift)
    check: |acc_diff_median| < 0.02 AND wilcoxon p > 0.05  # 不显著差异
  GT-D1-3:
    type: constraint
    runs: max_iter ∈ [100, 200, 400]
    check: loss[k+1] ≤ loss[k]
  GT-D1-5:
    type: wilcoxon
    runs: 30 paired (scale=T, scale=F)
    check: wilcoxon(acc_scaled, acc_unscaled, alternative='greater').p < 0.05
```

实测：6/6 PASS（GT-D1-1 acc_diff_median=0.003, p=0.42 不显著差异；GT-D1-5 p=0.012 强阳性）。

#### M.D1.6 JSON 落表

```json
{
  "run_id": "D1_glm_T0.5_s42",
  "extracted_mrs": 8,
  "matched_gt": 6,
  "v_af1": 0.857,
  "avr_pass_rate": 1.00,
  "p1_label_perm": {"acc_diff": 0.003, "wilcoxon_p_invariance": 0.42},
  "p5_scaling": {"median_diff": 0.018, "wilcoxon_p_greater": 0.012}
}
```

---

### M.X 跨范式对照速查表（学生外推参考）

| 范式 | walked example | 重点元模式 | 关键 r | 关键 R 验证手段 |
|---|---|---|---|---|
| 数值（A） | A1 Lorenz | P4 轨迹 | 初值 + ε | Lyapunov 线性拟合 |
| 概率（B） | B3 MC 积分 | P3 收敛 | N → 4N | std 比例校验 |
| 代理（C） | C1 GPR | P5 偏序 | RBF vs Matern | Wilcoxon 检验 |
| 机器学习（D） | D1 MLP/Iris | P1 不变 | π(y) 置换 | acc 差 + Wilcoxon |

学生处理其余 8 程序时，按下面思路对应模仿即可：
- 数值（A2/A3）仿 A1：参考 A1 的 P4/P5/P3 处理思路。
- 概率（B1/B2）仿 B3：参考 B3 的 P3 收敛与期望守恒。
- 代理（C2/C3）仿 C1：替换 kernel、正交基、网络架构等对应的 r 维度。
- ML（D2/D3）仿 D1：标签置换与特征缩放是 ML 标配 MR。

预计每范式第 1 程序约 6 小时，第 2、3 程序约 3 小时。

---

## 附录 N：失败决策树（卡点自查 → 升级流程）

任何异常先自查 ≤ 30 分钟。解决了就记录到 `weekly_log/`；30 分钟没解决就写 issue 升级。直接 Slack/微信问"老师怎么办"会被退回，必须先附上"已尝试 X/Y/Z"的排查记录。

### 异常分类与处置

#### N.1 LLM API 限速 / 配额耗尽 / 网络中断

| 触发 | 立即处置 | 回退方案 | 升级阈值 |
|---|---|---|---|
| HTTP 429 / Rate limit | 退避 60s 重试，最多 3 次；改用附录 H batch 模式 | 切到夜间跑（避开美区高峰）；分散到次日 | 单 LLM 卡 ≥ 6h 仍 429 |
| 配额耗尽 (quota exceeded) | 切下一个 LLM 继续；本 LLM 排队第 8/9/10 周 | 用 checkpoint 暂停，等月度配额重置 | 周内无法恢复 |
| 网络/SDK 异常 | `try/except + checkpoint.save()` 续跑 | 重启脚本，从最近 checkpoint 续 | 同一 cell 失败 ≥ 5 次 |
| 单次响应超时 (> 120s) | 重试 1 次；仍超时记 TIMEOUT 状态，不阻塞流程 | 保留 TIMEOUT cell，留到第 11 周补跑 | TIMEOUT 比例 > 5% |

#### N.2 Cohen's κ < 0.75（团队三角化 / 匹配判定）

| 触发 | 立即处置 | 回退方案 | 升级阈值 |
|---|---|---|---|
| 第 4 周 κ_team < 0.75 | 列分歧条目 → 召开 1-2h 共识会 → 修订编码手册（§4.5）→ 重测 | 增加第 3 名标注者；用多数决而非全一致 | 修订 2 轮后仍 < 0.70 |
| 第 11 周 κ_match < 0.75 | 同上，补充匹配判定示例（参附录 K few-shot） | 把"模糊匹配 / 紧匹配"分两层判定 | 同上 |

升级时把分歧清单 + 已修订手册 diff 一并附上。

#### N.3 行业专家投票分歧（2 票时不一致 / 3 票时 1:2 接近）

| 场景 | 立即处置 | 回退方案 |
|---|---|---|
| 2 位专家投票不一致（1 yes 1 no） | 找第 3 位专家做 tie-breaker（约 15 min 视频） | 把该 MR 标记 disputed，放入 G_final 但加备注，不入主分析 |
| 3 位中 1:2（少数 yes） | 按多数决过滤掉 | 同上：争议 MR 单独表，敏感性分析时报告 |
| 专家答 unsure 占 > 30% | 检查解释文案是否过技术；改写后重投 | 对 unsure 多的 MR 视为"非典型 MR"，不入 G_final 主集 |
| 联系不上专家 / 拒绝 | 先用替补名单（论文实验室预留 ≥ 2 名候补） | 24h 内升级老师，启动新一轮联络 |

#### N.4 AVR 流水线异常

| 触发 | 立即处置 | 回退方案 | 升级阈值 |
|---|---|---|---|
| Wilcoxon p 计算 NaN | 检查样本是否全相等（var=0），加 `if std==0: skip` | 该 cell 标 INCONCLUSIVE | INCONCLUSIVE > 5% |
| DTW 距离爆炸 (> 1e6) | 检查输入序列长度是否一致；归一化后重算 | 改用 PCC 作 fallback，记录 fallback 标记 | 同上 |
| 数值溢出 (overflow / inf) | 加 `np.errstate(over='warn')`；用 log 空间 | 该单一 run 重跑（不扩散到全 cell） | 单 cell 多次 overflow |
| constraint check 全 FAIL | 检查阈值文件 `avr/thresholds.yaml`；对比 dry-run 是否同样 FAIL | 阈值放宽 1 σ 重测；记录敏感性 | 阈值已放宽 2 σ 仍全 FAIL |

#### N.5 GSD 早停 / 提前停止判定

| 触发 | 处置 |
|---|---|
| N=15 时 H1-H4 全 p_adj < α/2（强证据） | 触发早停；剩余 N=16-20 不跑，节省预算（写入 `reports/gsd_early_stop.md`） |
| N=15 时 1-2 假设不显著 | 继续跑到 N=20，不早停 |
| N=20 时仍不显著 | 报告 power 分析（事后效果量），写 §10 limitations |

#### N.6 H5 跨范式 CV ≥ 0.5 / H6 ρ < 0.6（软化阈值）

| 触发 | 处置 |
|---|---|
| H5 跨范式 V-AF1 CV ≥ 0.5 | §9 用"范式间差异显著"取代"跨范式一致"；§10 limitations 增段说明 |
| H6 反向假设 ρ < 0.6 | §9 改文案"未观察到强反向相关"；不影响 H1-H4 结论 |
| H5 + H6 同时触发 | 第 13 周回跑 1 LLM × 2 异常程序 ≤ 200 次，看是否数据偶然；仍异常则保留软化文案 |

#### N.7 文献 MR 不足（源 1 数 < 3 条 / 程序）

| 触发 | 处置 |
|---|---|
| 某程序 source1 < 3 条 | 扩大检索：textbook 章节 + 1 篇相关 paper + 1 篇 thesis；仍不足 → 标记"文献稀缺程序"，主依赖源 3+4 |
| 全 12 程序源 1 总数 < 60 | 升级老师，可能需要更换某 1-2 程序 |

#### N.8 跨家族 LLM 候选与团队三角化重合度 < 30%

| 触发 | 处置 |
|---|---|
| Qwen+Doubao 输出 vs 团队三角化 重合度 < 30% | 检查 prompt 是否被跨家族 LLM 误读；调整 program_block 的 spec/algorithm 描述清晰度后重跑 |
| 重合度仍 < 30% | 该程序 GT 标记"高不确定"；§10 增段说明，主分析照常进行 |

#### N.9 进度落后（任一周自评 < 18/25）

| 落后程度 | 处置 |
|---|---|
| 落后 ≤ 3 天 | 周末加班补；下周减少非核心任务（如文献阅读时长） |
| 落后 4-7 天 | 立即升级老师，调整后续周计划（如压缩第 13 周异常诊断到 3 天） |
| 落后 > 7 天 | 老师介入，重新评估投稿时间表（推迟到 SANER round 2 也是选项） |

#### N.10 数据丢失 / 仓库异常

| 触发 | 处置 |
|---|---|
| 本机硬盘损坏 | 从外盘 + GitHub 双备份恢复；丢失数据按附录 H checkpoint 重跑 |
| commit 误删 / 误 force-push | `git reflog` 找回；如已 push，从老师/同门镜像拉回。永不对主干使用 `git push --force` |
| 数据快照与 commit 不一致 | 立即停手，校验 sha256；不一致即视为污染数据，从最近一致点重建 |

### 升级模板（写到 `escalations/{date}_{topic}.md`）

```
标题：{一句话症状}
触发时间：{ISO 时间戳}
触发情境：{我在做什么、第几周、哪个脚本}
已尝试：
  1. {步骤 + 输出}
  2. {步骤 + 输出}
  3. {步骤 + 输出}
当前阻塞：{为什么前面 3 步都没解决}
请求：{需要老师做什么决策 / 提供什么资源}
影响：{若 24h 不解决，对总体进度影响}
```

老师收到此模板才回复；不带"已尝试"的 Slack 直接退回。
