# 蜕变关系元模式：近五年研究进展与实证归纳

## 摘要

蜕变测试（Metamorphic Testing, MT）通过蜕变关系（Metamorphic Relation, MR）解决软件测试中的 Oracle 问题，已成为主流测试技术之一。然而，MR 的识别长期依赖领域专家的经验直觉，制约了 MT 的工程推广。近五年来，研究者开始将 MR 从具体规则提升为可复用的抽象模式，推动了蜕变关系模式（Metamorphic Relation Pattern, MRP）理论的快速发展。但现有分类方案的元模式数量和边界缺乏实证基础，主要依赖研究者的主观判断。本文以 2020—2025 年的研究成果为主线，首先追踪 MRP 概念从萌芽到系统化的演进过程；然后采用扎根理论方法，从近 25 年文献中收集的 N 条 MR 实例出发，通过开放编码、轴向编码和选择性编码，以数据驱动的方式归纳元模式的数量和边界；最后对归纳结果进行覆盖性、不可合并性和不可拆分性验证。实证聚类的结果表明 [待补充：聚类数量和核心发现]，为蜕变关系元模式体系提供了客观的经验基础。

---

## 1 引言

蜕变测试由 Chen 等于 1998 年提出[1]，其核心思想是：当无法判断单次执行的输出是否正确时，可以通过检查多次执行之间输入-输出关系是否满足特定性质来检测缺陷。这种性质即为蜕变关系。形式化地，设 f 为被测程序，MR 是一个逻辑蕴含 R_i ⇒ R_o，其中 R_i 是关于源输入 x_s 和后续输入 x_f 的关系，R_o 是关于对应输出 f(x_s) 和 f(x_f) 的关系[2]。

Segura 等在 2016 年的综述中系统梳理了 MT 的方法论基础，指出 MR 的识别是 MT 实践中最关键也最困难的任务[3]。Chen 等在 2018 年的 ACM Computing Surveys 综述中进一步总结了 MT 面临的挑战，其中 MR 的系统化识别被列为首要问题[4]。

近五年的研究表明，绝大多数已发表的 MR 可以归入数量有限的结构模式。Zhou 等 2020 年提出了对称性和非对称性两个基础 MRP[8]，Ying 等 2025 年构建了包含十一个 MRP 的家族树[18]。然而，现有分类方案面临两个未解问题：第一，元模式的数量缺乏必要性论证——为什么是 2 个或 11 个，而不是其他数量？不同方案的抽象粒度差异巨大，但均未给出"为什么在这个粒度上划分是最合适的"的实证依据。第二，随着 LLM 测试中新型 MR 的出现，现有分类体系的覆盖完备性受到挑战——一致性检查类的 MR 是否构成独立的元模式，目前缺乏系统性分析。

本文的目标是通过实证归纳解决上述两个问题。具体贡献如下：（1）以时间线追踪 MRP 概念从萌芽到系统化的演进过程（第 2 节）；（2）提出基于扎根理论的 MR 实证归纳方法（第 3 节）；（3）以数据驱动的方式归纳元模式的数量和边界，并通过三步验证确保分类的严谨性（第 4 节）；（4）对 LLM 领域的 MR 进行专项分析，评估一致性元模式的独立性（第 5 节）；（5）给出元模式的形式化定义、派生模式族和文献示例（第 6 节）；（6）识别基础理论的研究空白并讨论局限性（第 7 节）。

---

## 2 相关工作：从具体关系到抽象模式

### 2.1 前期积累（2016—2019）：模式意识的萌芽

MR 模式化的思想并非凭空出现。早在 2007 年，Zhou 等在测试搜索引擎时就使用了"通用蜕变关系"（general metamorphic relation）这一概念，定义了一条可派生多个具体 MR 的抽象关系[5]。Segura 等在 2018 年测试 RESTful Web API 时，正式提出了"蜕变关系输出模式"（MROP）这一术语，并识别出六种 MROP：等价、相等、子集、不相交、完整和差异[6]。Murphy 等更早时在机器学习测试中引入了"蜕变性质"（metamorphic property）的概念[7]。

### 2.2 形式化奠基（2020）：对称性 MRP 的提出

Zhou、Sun、Chen 和 Towey 在 IEEE TSE 上首次给出了 MRP 的形式化定义：MRP 是"刻画一组（可能无限多个）蜕变关系的抽象"[8]。该论文明确了 MRP 的层次结构，识别出对称性 MRP 和"改变方向"MRIP，并假设对称性和非对称性是两个成对出现的基础 MRP。

### 2.3 多领域扩展（2021—2023）

MRP 的应用范围从搜索引擎扩展到自动驾驶[9][10]、NLP/LLM[11][12]、量子计算[13]、深度学习框架[14]和科学计算[30][31][32][34][35][36]。

### 2.4 自动化突破（2023—2024）

MR-Scout 从已有测试用例自动提取 MR[15]，GenMorph 通过遗传编程搜索有效 MR[16]，MARS 通过迭代精化从领域无关关系出发逐步发现领域特定 MR[19]。

### 2.5 系统化整合（2024—2025）

Li 等在 TOSEM 2025 综述中分析了 81 篇 MR 生成论文[17]；Ying 等提出十一个 MRP 和家族树[18]。

### 2.6 现有分类的不足

现有分类面临两个缺口：元模式数量的主观性（Zhou 等的 2 个 vs. Ying 等的 11 个，抽象粒度差异巨大但均未给出实证依据），以及 LLM 时代的覆盖性挑战（MetaQA[28]和 DrHall[29]中一致性类 MR 是否构成独立元模式）。

---

## 3 研究方法：基于扎根理论的 MR 实证归纳

### 3.1 方法论概述

本文采用扎根理论（grounded theory）方法，以数据驱动的方式从文献中的 MR 实例归纳元模式。选择归纳而非演绎分类的原因在于：演绎分类从预设框架出发，归纳分类让类别从数据中涌现，避免了研究者预设立场的影响。

### 3.2 数据收集

#### 3.2.1 数据来源

MR 实例从以下来源系统收集：（1）跨领域综述：Segura 等 2016[3]、Chen 等 2018[4]、Li 等 2025[17]中的 MR 实例；（2）NLP/LLM 专项：Cho 等 2025[12]中 191 条 MR；（3）科学计算专项：Li 等[31][32][35][36]和 Zhao 等[34]中的 MR；（4）其他领域代表性论文中的 MR。

#### 3.2.2 纳入与排除标准

纳入：MR 被显式定义且在实验中实际使用，来源论文经同行评审。排除：重复 MR（以最早来源为准）；纯性质（property）检查而非跨执行的蜕变关系。

#### 3.2.3 样本规模

[待补充：最终收集的 MR 总数 N，按领域分布表。]

### 3.3 编码方案

#### 3.3.1 编码维度

对每条 MR 编码四个维度：输入变换类型（置换、等价替换、几何变换、标量增减、线性代数运算、参数推极值、恒等变换、语义改写等）；输出关系类型（精确相等、近似相等、偏序、代数表达式、集合包含、分布等价、事实不矛盾、标签不变等）；应用领域；MR 来源层次。

#### 3.3.2 编码流程

双人独立编码 + 协商一致：10% 预编码计算 Cohen's kappa → 正式编码 → 一致性检查 → 差异协商。

[待补充：kappa 系数。]

### 3.4 聚类与元模式归纳

以"输入变换类型 × 输出关系类型"为结构特征，三阶段编码：

**开放编码：** 自由分组，不预设框架。

**轴向编码：** 分析类别间关系，合并推理策略相同的类别。

**选择性编码：** 提炼核心类别，确定元模式。

元模式数量由两个停止条件决定：**合并停止**（存在仅属于类别 A 且检测到类别 B 未检测缺陷的 MR 时不可合并）；**拆分停止**（类别内所有 MR 共享同一推理策略时不再拆分）。

---

## 4 聚类结果与元模式归纳

### 4.1 数据概览

[待补充：MR 总数、领域分布表、输入变换类型分布表、输出关系类型分布表。]

### 4.2 开放编码结果

[待补充：初始类别数量、每类 MR 数量和代表实例。]

### 4.3 轴向编码结果

[待补充：合并过程描述、中间层类别数量、合并理由。]

### 4.4 选择性编码结果：K 个元模式

[待补充：最终元模式数量 K。以下为预期结果的框架性描述。]

#### 4.4.1 元模式 I：不变性（Invariance）

**定义。** 对输入施加属于特定变换族 T 的变换后，输出在等价意义 ≡ 下不变。

**形式化。** ∀x_s, ∀t ∈ T: f(t(x_s)) ≡ f(x_s)

**聚类来源。** [待补充：MR 数量、占比、领域分布。]

#### 4.4.2 元模式 II：单调性（Monotonicity）

**定义。** 输入沿偏序增大时，输出沿另一偏序单调变化。

**形式化。** x_s ≤_i x_f ⇒ f(x_s) ≤_o f(x_f)

**聚类来源。** [待补充。]

#### 4.4.3 元模式 III：仿射变换（Affine Transformation）

**定义。** 对输入施加参数化数学变换后，输出满足可推导的封闭代数关系。

**形式化。** f(T_θ(x_s)) = g(f(x_s), θ)

**聚类来源。** [待补充。]

**关于与元模式 I、II 的关系。** I ⊂ II ⊂ III 构成精化链（不变性是仿射变换的特例，单调性是仿射变换的弱化），但三者对应不同的推理策略。[待补充：不可合并性的实证验证结果。]

#### 4.4.4 元模式 IV：退化与收敛（Degeneration and Convergence）

**定义。** 参数推极值时程序退化为已知简化情形，或沿参数序列输出收敛。

**形式化。** lim_{θ→θ*} f(x, θ) = f*(x)；θ_1 ≺ θ_2 ≺ ... ⇒ {f(x, θ_n)} 单调收敛。

**聚类来源。** [待补充。]

#### 4.4.5 候选元模式 V：一致性（Consistency）

[是否成立取决于第 5 节专项分析。]

**定义。** 对同一输入或语义等价输入的多次独立执行，输出在事实层面应保持自洽。

**聚类来源。** [待补充。]

### 4.5 三步验证

#### 4.5.1 覆盖性验证

[待补充：是否每条 MR 都被归入某元模式。未覆盖 MR 数量及分析。]

#### 4.5.2 不可合并性验证

[待补充：每对元模式的不可合并性反例。]

#### 4.5.3 不可拆分性验证

[待补充：每个元模式内推理策略的一致性验证。]

---

## 5 LLM 领域 MR 专项分析：一致性元模式的实证检验

### 5.1 分析动机

MetaQA[28]和 DrHall[29]中的一致性 MR 是否能被元模式 I-IV 覆盖，是决定一致性是否需要独立成为第五个元模式的关键。

### 5.2 方法：穷举分类与残差分析

将 191 条 NLP/LLM MR[12]逐一对照元模式 I-IV 归类，记录完全匹配、部分匹配和不匹配三种结果。对残差（不匹配+部分匹配）MR 进行结构特征分析。

### 5.3 穷举分类结果

[待补充：分类结果表。]

### 5.4 残差 MR 的结构分析

[待补充：预期发现两类残差——类型 A（交叉推理一致性：语义保持改写 + 事实不矛盾）和类型 B（重复执行一致性：恒等变换 + 事实不矛盾）。]

### 5.5 一致性与等价替换不变性的区分

**输出关系的结构差异。** 不变性：二元等价判断 `f(t(x)) ≡ f(x)`。一致性：命题逻辑一致性检查 `¬∃p: p ∈ Fact(f(x)) ∧ ¬p ∈ Fact(f(t(x)))`。后者需要从输出中提取事实命题集合并检查逻辑相容性——这种机制在传统元模式的输出关系中无对应物。

**变换确定性的差异。** 不变性的变换是外部施加的确定性操作；一致性涉及程序内部随机性产生的输出差异。

**检错能力的不可替代性。** [待补充：MetaQA 实验数据——一致性 MR 检测到不变性 MR 无法检测的幻觉类型。]

### 5.6 关于恒等变换的合法性

**策略一（保守）：** 排除类型 B，仅保留类型 A。

**策略二（扩展）：** 视恒等变换为 MT 在非确定性程序中的推广。论据：Chen 等 2018[4]定义 MT 为"检查多次执行之间的关系"，未排除输入相同情况。

[待补充：基于实证数据选择的策略。]

### 5.7 专项分析结论

[待补充：一致性元模式是否成立的最终判断。]

---

## 6 元模式体系：定义、派生模式与示例

### 6.1 元模式与派生模式族的关系

约束特化关系：元模式定义最一般结构，派生模式施加额外约束。若元模式 M 的参数空间为 (T, ≡)，派生模式 D 施加约束后 MR(D) ⊂ MR(M)。

### 6.2 元模式 I 的派生模式族

#### 6.2.1 置换不变性

**示例 1：** 搜索引擎查询词序[5]。**示例 2：** 代码生成 LLM 提示顺序[20]。**示例 3：** 燃耗矩阵核素排列不变性[35]。

#### 6.2.2 等价替换不变性

**示例 1：** 机器翻译指称透明性[21]。**示例 2：** 量子电路门集等价变换[13]。

#### 6.2.3 几何对称不变性

**示例 1：** 自动驾驶图像翻转[22]。**示例 2：** ADS 仿真器场景对称性[10]。

### 6.3 元模式 II 的派生模式族

#### 6.3.1 标量单调性

**示例 1：** ML 分类器置信度单调性[23]。**示例 2：** Web 安全严重性排序[24]。**示例 3：** HTGR 功率-温度单调性[34]。**示例 4：** HTGR 流量-温度反向单调性[34]。

#### 6.3.2 集合包含单调性

**示例 1：** 搜索引擎查询放宽[5]。**示例 2：** RESTful Web API 子集模式[6]。

### 6.4 元模式 III 的派生模式族

#### 6.4.1 加法平移

**示例 1：** 统计软件标准差不变性[1]。**示例 2：** 科学计算能量平移[19]。

#### 6.4.2 乘法缩放

**示例 1：** DL 算子参数缩放[14]。**示例 2：** 图像亮度缩放[22]。

#### 6.4.3 否定与反转

**示例 1：** 情感分析否定翻转[12]。**示例 2：** 排序算法反序[3]。

#### 6.4.4 守恒律约束

**关于 MR 与性质的边界。** 守恒律在分类上存在张力：单次执行中可验证（接近 property），但用于跨执行比较时具备 MR 结构[34]。

**示例 1：** 衰变链质量守恒[36]。**示例 2：** 燃耗步时间守恒[32]。

### 6.5 元模式 IV 的派生模式族

#### 6.5.1 参数退化

**示例 1：** 正则化回归退化[7]。**示例 2：** 量子化学库单原子退化[19]。**示例 3：** 耦合程序初始温度无关性[34]。

#### 6.5.2 离散化收敛

**示例 1：** 有限元网格收敛[25]。**示例 2：** CRAM 阶数收敛[35][36]。**示例 3：** 燃耗步数精度收敛[32]。**示例 4：** DL 训练损失收敛[14]。

### 6.6 元模式 V 的派生模式族（若第 5 节确认成立）

#### 6.6.1 交叉推理一致性

**示例 1：** 自一致性推理[27]。**示例 2：** 多轮对话一致性[12]。

#### 6.6.2 重复执行一致性（若采用策略二）

**示例 1：** MetaQA 幻觉检测[28]。**示例 2：** DrHall 幻觉检测[29]。

---

## 7 讨论

### 7.1 与现有分类的关系

[待补充：实证归纳的 K 个元模式与 Zhou 等二分法[8]、Ying 等十一类[18]、Segura 等六种 MROP[6] 的对比。]

### 7.2 关于组合性

组合是元模式间的运算而非模式本身。Qiu 等对 MR 组合有效性已有初步分析[26]。

### 7.3 MR 基础理论的研究空白

**空白一：MR 充分性理论。** [17]中的优先方向。实证归纳为充分性度量提供候选框架。

**空白二：MR 与程序语义的关系。** Chen 等 semi-proving[37]和 Gotlieb 等自动化 MT[38]是早期探索，但未被充分继承。

**空白三：元模式的公理化基础。** 实证归纳提供经验基础，但严格证明需公理化框架。

**空白四：领域特定的 MR 拓扑结构与 MR 库。** Yang 等层次分类模型[30]、Li 等 MR 生成框架[31]和两阶段验证方法[33]、Zhao 等 HTGR 耦合程序验证[34]构成科学计算领域的完整案例链条。

### 7.4 局限性

[待补充：编码主观性、样本代表性、聚类方法选择敏感性、一致性元模式的理论成熟度等。]

---

## 8 结论

[待补充：核心主张为"通过对近 25 年文献中 N 条 MR 的实证归纳，本文发现 MR 的结构自然聚成 K 个元模式"——实证发现而非预设提出。]

---

## 参考文献

[1] CHEN T Y, CHEUNG S C, YIU S M. Metamorphic testing: a new approach for generating next test cases[R]. HKUST-CS98-01. Hong Kong: Department of Computer Science, Hong Kong University of Science and Technology, 1998.

[2] BARR E T, HARMAN M, MCMINN P, et al. The oracle problem in software testing: a survey[J]. IEEE Transactions on Software Engineering, 2015, 41(5): 507-525.

[3] SEGURA S, FRASER G, SÁNCHEZ A B, et al. A survey on metamorphic testing[J]. IEEE Transactions on Software Engineering, 2016, 42(9): 805-824.

[4] CHEN T Y, KUO F C, LIU H, et al. Metamorphic testing: a review of challenges and opportunities[J]. ACM Computing Surveys, 2018, 51(1): 4:1-4:27.

[5] ZHOU Z Q, TSE T H, KUO F C, et al. Automated functional testing of web search engines in the absence of an oracle[R]. TR-2007-06. Hong Kong: Department of Computer Science, The University of Hong Kong, 2007.

[6] SEGURA S, PAREJO J A, TROYA J, et al. Metamorphic testing of RESTful web APIs[J]. IEEE Transactions on Software Engineering, 2018, 44(11): 1083-1099.

[7] MURPHY C, KAISER G, HU L, et al. Properties of machine learning applications for use in metamorphic testing[C]//Proceedings of the 20th International Conference on Software Engineering and Knowledge Engineering. Redwood City: KSI, 2008: 867-872.

[8] ZHOU Z Q, SUN L, CHEN T Y, et al. Metamorphic relations for enhancing system understanding and use[J]. IEEE Transactions on Software Engineering, 2020, 46(10): 1120-1154.

[9] ZHOU Z Q, SUN L. Metamorphic testing of driverless cars[J]. Communications of the ACM, 2019, 62(3): 61-67.

[10] ZHANG Y, TOWEY D, PIKE M, et al. Scenario-driven metamorphic testing for autonomous driving simulators[J]. Software Testing, Verification and Reliability, 2024, 34(7): e1892.

[11] WANG W, HUANG J T, WU W, et al. MTTM: metamorphic testing for textual content moderation software[C]//Proceedings of the 45th International Conference on Software Engineering. Melbourne: IEEE/ACM, 2023: 2387-2399.

[12] CHO H, TERRAGNI V, JOHNSON B, et al. Metamorphic testing of large language models for natural language processing[C]//Proceedings of the 41st IEEE International Conference on Software Maintenance and Evolution. Montréal: IEEE, 2025.

[13] PALTENGHI M, PRADEL M. MorphQ: metamorphic testing of the Qiskit quantum computing platform[C]//Proceedings of the 45th International Conference on Software Engineering. Melbourne: IEEE/ACM, 2023: 2413-2424.

[14] CHEN J, JIA C, YAN Y, et al. A miss is as good as a mile: metamorphic testing for deep learning operators[J]. Proceedings of the ACM on Software Engineering, 2024, 1(FSE): 2005-2027.

[15] XU C, TERRAGNI V, ZHU H, et al. MR-Scout: automated synthesis of metamorphic relations from existing test cases[J]. ACM Transactions on Software Engineering and Methodology, 2024, 33(6): 1-26.

[16] AYERDI J, TERRAGNI V, JAHANGIROVA G, et al. GenMorph: automatically generating metamorphic relations via genetic programming[J]. IEEE Transactions on Software Engineering, 2024, 50(7): 1888-1900.

[17] LI R, LIU H, POON P L, et al. Metamorphic relation generation: state of the art and visions for future research[J]. ACM Transactions on Software Engineering and Methodology, 2025, 34(5).

[18] YING Z, TOWEY D, BELLOTTI A G, et al. Metamorphic relation patterns for metamorphic testing, exploration and robustness[J]. Software Testing, Verification and Reliability, 2025, 35(2): e70003.

[19] COHEN M B, WANG Y, ROTHERMEL G, et al. Model assisted refinement of metamorphic relations for scientific software[C]//Proceedings of the 47th International Conference on Software Engineering: New Ideas and Emerging Results. Ottawa: IEEE/ACM, 2025.

[20] VINCENZI A M R, DUQUE-TORRES A, PFAHL D, et al. Effectiveness of symmetric metamorphic relations on validating the stability of code generation LLM[J]. Journal of Systems and Software, 2025, 222: 112323.

[21] HE P, MEISTER C, SU Z. Testing machine translation via referential transparency[C]//Proceedings of the 43rd International Conference on Software Engineering. Madrid: IEEE/ACM, 2021: 410-422.

[22] TIAN Y, PEI K, JANA S, et al. DeepTest: automated testing of deep-neural-network-driven autonomous cars[C]//Proceedings of the 40th International Conference on Software Engineering. Gothenburg: ACM, 2018: 303-314.

[23] XIE X, HO J W K, MURPHY C, et al. Testing and validating machine learning classifiers by metamorphic testing[J]. Journal of Systems and Software, 2011, 84(4): 544-558.

[24] CHALESHTARI N B, PASTORE F, GOKNIL A, et al. Metamorphic testing for web system security[J]. IEEE Transactions on Software Engineering, 2023, 49(6): 3430-3471.

[25] KANEWALA U, BIEMAN J M. Testing scientific software: a systematic literature review[J]. Information and Software Technology, 2014, 56(10): 1219-1232.

[26] QIU K, ZHENG Z, CHEN T Y, et al. Theoretical and empirical analyses of the effectiveness of metamorphic relation composition[J]. IEEE Transactions on Software Engineering, 2022, 48(5): 1584-1600.

[27] WANG X, WEI J, SCHUURMANS D, et al. Self-consistency improves chain of thought reasoning in language models[C]//Proceedings of the 11th International Conference on Learning Representations. Kigali: ICLR, 2023.

[28] YANG B, AL MAMUN M A, ZHANG J M, et al. Hallucination detection in large language models with metamorphic relations[J]. Proceedings of the ACM on Software Engineering, 2025, 2(FSE): FSE020.

[29] WU W, CAO Y, YI N, et al. Detecting and reducing the factual hallucinations of large language models with metamorphic testing[J]. Proceedings of the ACM on Software Engineering, 2025, 2(FSE).

[30] YANG X H, YAN S Y, LIU J, et al. Hierarchical classification model for metamorphic relations of scientific computing programs[J]. Computer Science, 2020, 47(S2): 557-561.

[31] LI M, WANG L J, YAN S Y, et al. Metamorphic relation generation for physics burnup program testing[J]. International Journal of Performability Engineering, 2020, 16(2): 297-306.

[32] LI M, WANG L J, YUE W, et al. Metamorphic testing of the NUIT code based on burnup time[J]. Annals of Nuclear Energy, 2021, 153: 108027.

[33] LI M. Research on two-stage verification method based on metamorphic relation[D]. Hengyang: University of South China, 2021.

[34] ZHAO Y, LI M, ZHANG K, et al. Verification of multi-scale coupling program for high temperature gas-cooled reactor based on metamorphic testing[J]. Annals of Nuclear Energy, 2026, 226: 111846.

[35] LI M, YAN S Y, YANG X H, et al. Metamorphic testing on nuclide inventory tool[C]//Proceedings of the 2020 International Conference on Nuclear Engineering. Virtual: ASME, 2020: V003T14A001.

[36] LI M, WANG L J, YAN S Y, et al. Metamorphic relations identification on Chebyshev rational approximation method in the nuclide depletion calculation program[C]//Proceedings of the 2020 IEEE 20th International Conference on Software Quality, Reliability and Security Companion. Macau: IEEE, 2020: 1-6.

[37] CHEN T Y, TSE T H, ZHOU Z Q. Semi-proving: an integrated method for program proving, testing, and debugging[J]. IEEE Transactions on Software Engineering, 2011, 37(1): 109-125.

[38] GOTLIEB A, BOTELLA B. Automated metamorphic testing[C]//Proceedings of the 27th Annual International Computer Software and Applications Conference. Dallas: IEEE, 2003: 34-40.
