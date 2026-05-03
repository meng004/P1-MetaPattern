# MR 层次与元模式归类

##### [**Undermind**](https://undermind.ai)

---


## Table of Contents

- [MR 层次与元模式归类](#mr-层次与元模式归类)
- [表 1 清理后 MR 层次分类模型归类表](#表-1-清理后-mr-层次分类模型归类表)
- [表 2 清理后 MR 元模式归类表](#表-2-清理后-mr-元模式归类表)
- [表 3 程序类型 论文 MR 数量表](#表-3-程序类型-论文-mr-数量表)
- [创新点表述](#创新点表述)
  - [创新点 1 MR 层次分类模型](#创新点-1-mr-层次分类模型)
  - [创新点 2 MR 元模式框架](#创新点-2-mr-元模式框架)
  - [创新点 3 三类程序共享的统一验证主张](#创新点-3-三类程序共享的统一验证主张)
  - [一句话概括](#一句话概括)
- [本文贡献](#本文贡献)
  - [1 提出三类程序共享的统一验证观点](#提出三类程序共享的统一验证观点)
  - [2 提出 MR 层次分类模型](#提出-mr-层次分类模型)
  - [3 提出五类 MR 元模式](#提出五类-mr-元模式)
  - [4 基于文献证据对层次模型与元模式进行系统归纳](#基于文献证据对层次模型与元模式进行系统归纳)
  - [5 澄清现有研究中的空缺与本文的位置](#澄清现有研究中的空缺与本文的位置)
- [表格解释与理论主张](#表格解释与理论主张)
- [References](#references)

## MR 层次与元模式归类

这版是在原始整理基础上做的清理版。

清理规则如下：

- 去除综述论文
- 去除不适用论文
- 去除通用软件论文
- 保留三类目标程序论文，即科学计算、概率程序、ML 代理模型
- 保留疑惑项，格式统一为 `疑惑：...`

行单位仍然是论文，不是单条 MR。若论文给出明确编号，则保留编号。若未统一编号，则提取 MR 描述中的关键词。对于不是标准 MT 论文、但能直接支撑“物理不变性质或结构性约束可作为验证证据”的论文，保留其可对应的 invariant 或 relation 关键词。

## 表 1 清理后 MR 层次分类模型归类表

| 论文 | MR 编号或关键词 | 程序类型 | 所属层次 | 备注 |
|:---|:---|:---|:---|:---|
| (Lin, Simon, & Niu, 2018) | hierarchical MRs | 科学计算 | 疑惑：数学物理层 / 运行行为层 | 强调增量式层次开发 |
| (Olsen & Raunak, 2019) | parameters and behaviors within simulation model | 科学计算 | 运行行为层 | 模型验证导向 |
| (Raunak & Olsen, 2021) | simulation verification and validation MRs | 科学计算 | 运行行为层 | 仿真行为与参数关系 |
| (Yan & Zhu, 2024) | elliptic PDE numerical-model-derived MRs | 科学计算 | 数学物理层 | 明确由微分方程数值模型导出 |
| (Li et al., 2022) | physical model MR, computational model MR, code model MR, likely MR | 科学计算 | 跨层 | 最直接支撑层次分类模型 |
| (T. Chen et al., 2002) | PDE case-study MR | 科学计算 | 疑惑：数学物理层 / 计算方法层 | 方程性质与网格细化并存 |
| (Lin et al., 2021) | nominal, ordinal, functional hierarchy | 科学计算 | 运行行为层 | 主要从输出视角分类 |
| (Luu et al., 2022) | periodic tide property MRs | 科学计算 | 数学物理层 | 来源于天文潮周期性质 |
| (Li et al., 2021) | burnup time based MRs | 科学计算 | 疑惑：数学物理层 / 计算方法层 | 数学方程与数值算法同时出现 |
| (Li et al., 2020) | physics burnup MR generation | 科学计算 | 疑惑：数学物理层 / 计算方法层 | 面向燃耗程序 |
| (Raunak & Olsen, 2015) | metamorphic validation for simulation | 科学计算 | 运行行为层 | 仿真验证框架 |
| (T. Y. Chen et al., 2011) | grid refinement related MR | 科学计算 | 疑惑：数学物理层 / 计算方法层 | PDE 数值程序案例 |
| (Olsen & Raunak, 2016) | metamorphic validation for ABM | 科学计算 | 运行行为层 | 代理式仿真模型 |
| (Ding et al., 2019) | invariant relations for light scattering | 科学计算 | 数学物理层 | 基于领域不变量迭代细化 |
| (Farhan et al., 2021) | hybrid simulation validation MRs | 科学计算 | 运行行为层 | 混合仿真模型 |
| (Lin, Simon, Niu, Carver, et al., 2018) | exploratory MT | 科学计算 | 运行行为层 | 连续仿真结果模式探索 |
| (Zhang et al., 2019) | numerical MR discovery and cleansing | 科学计算 | 跨层 | 自动发现数值程序 MR |
| (Chan et al., 1998) | numerical analysis MR | 科学计算 | 计算方法层 | 数值分析程序早期案例 |
| (T. Chen et al., 2009) | bioinformatics domain-specific MRs | 科学计算 | 运行行为层 | 以生物信息软件行为性质为主 |
| (Hiremath et al., 2021) | ocean system symmetries | 科学计算 | 数学物理层 | 物理对称性已知 |
| (Hiremath et al., 2020) | ocean-modeling identity-map based MR search | 科学计算 | 数学物理层 | 从物理对称性出发自动识别 |
| (Contrastin et al., 2016) | units of measure, stencil specifications | 科学计算 | 代码实现层 | 轻量规格作为关系来源旁证 |
| (Guderlei & Mayer, 2007) | statistical metamorphic relations | 概率程序 | 运行行为层 | 统计假设检验驱动 |
| (Yoo, 2010) | stochastic optimisation MRs | 概率程序 | 运行行为层 | 面向随机优化行为 |
| (Ding et al., 2011) | Monte Carlo modeling MRs | 概率程序 | 计算方法层 | 从随机采样模型分析 MR |
| (Spieker et al., 2024) | mirroring, rescaling, trajectory invariants | 概率程序 | 运行行为层 | 预测轨迹的统计判据 |
| (Ding & Hu, 2016) | Monte Carlo simulation MRs | 概率程序 | 计算方法层 | 同时讨论 adequacy 监测 |
| (Rounds & Kanewala, 2018) | GA statistical MRs | 概率程序 | 运行行为层 | 遗传算法随机行为 |
| (Y. Chen et al., 2023) | random sampling model based MRs | 概率程序 | 计算方法层 | 蒙特卡洛数值计算程序 |
| (Barthe et al., 2016) | probabilistic invariants and martingales | 概率程序 | 计算方法层 | 期望不变量 |
| (Bartocci et al., 2019) | moment-based invariants | 概率程序 | 计算方法层 | higher moments 作为性质 |
| (Wang et al., 2019) | expected sensitivity | 概率程序 | 计算方法层 | 概率程序灵敏度性质 |
| (Moosbrugger et al., 2022) | higher moments for probabilistic loops | 概率程序 | 计算方法层 | 统计性质计算 |
| (Murphy et al., 2008) | ML property catalog | ML代理模型 | 跨层 | 机器学习应用性质分类 |
| (Xie et al., 2011) | MR-0 至 MR-5.2 | ML代理模型 | 计算方法层 | 分类器算法性质导出 |
| (Yang & Chui, 2021) | rainfall to runoff consistency MRs | ML代理模型 | 数学物理层 | 来源于被建模水文系统性质 |
| (Dwarakanath et al., 2018) | image transformation MRs | ML代理模型 | 运行行为层 | 关注实现 bug 暴露 |
| (Xie et al., 2009) | MR-0 至 MR-5.2 | ML代理模型 | 计算方法层 | 监督分类器算法性质 |
| (Luu et al., 2021) | MR 1.1 至 MR 6 | ML代理模型 | 计算方法层 | 多元线性回归数学性质 |
| (Liu et al., 2022) | momentum conservation, translation and rotation invariance | ML代理模型 | 数学物理层 | 物理约束内生到 neural operator |
| (Prantl et al., 2022) | momentum conservation hard constraint | ML代理模型 | 数学物理层 | 粒子流体动力学守恒 |
| (Bhattoo et al., 2021) | translational and rotational symmetries, energy and momentum conservation | ML代理模型 | 数学物理层 | 关系性归纳偏置 |

## 表 2 清理后 MR 元模式归类表

| 论文 | MR 编号或关键词 | 程序类型 | 元模式 | 备注 |
|:---|:---|:---|:---|:---|
| (Lin, Simon, & Niu, 2018) | hierarchical MRs | 科学计算 | 跨元模式 | 重在层次开发，不限单一模式 |
| (Olsen & Raunak, 2019) | simulation behavior relations | 科学计算 | P4 轨迹性 | 重点是参数与行为轨迹之间关系 |
| (Raunak & Olsen, 2021) | simulation V and V continuum | 科学计算 | P4 轨迹性 | 仿真行为约束 |
| (Yan & Zhu, 2024) | PDE numerical model MRs | 科学计算 | 疑惑：P1 / P3 | 方程不变性与网格精化都出现 |
| (Li et al., 2022) | physical, computational, code, likely MRs | 科学计算 | 跨元模式 | 文中示例同时包含单调、平滑与不变性 |
| (T. Chen et al., 2002) | PDE case-study MR | 科学计算 | P3 收敛性 | 经典网格精化与更好近似 |
| (Lin et al., 2021) | nominal, ordinal, functional hierarchy | 科学计算 | 跨元模式 | 输出视角分类，不限单一模式 |
| (Luu et al., 2022) | periodic tide property | 科学计算 | P1 守恒性 | 周期与相位不变性质 |
| (Li et al., 2021) | burnup time based MRs | 科学计算 | 疑惑：P2 / P4 | 时间演化中有单调与轨迹性质 |
| (Li et al., 2020) | physics burnup MR generation | 科学计算 | 跨元模式 | 面向燃耗程序的 MR 生成 |
| (Raunak & Olsen, 2015) | metamorphic validation for simulation | 科学计算 | P4 轨迹性 | 面向仿真行为有效性 |
| (T. Y. Chen et al., 2011) | grid refinement related MR | 科学计算 | P3 收敛性 | 明确更细网格更好近似 |
| (Olsen & Raunak, 2016) | agent-based simulation validation | 科学计算 | P4 轨迹性 | 模型行为轨迹验证 |
| (Ding et al., 2019) | invariant relations for light scattering | 科学计算 | P1 守恒性 | 直接以 invariant relations 命名 |
| (Farhan et al., 2021) | hybrid simulation validation | 科学计算 | P4 轨迹性 | 混合仿真行为模式 |
| (Lin, Simon, Niu, Carver, et al., 2018) | exploratory MT | 科学计算 | P4 轨迹性 | 连续仿真中的 testing-result patterns |
| (Zhang et al., 2019) | equality and inequality numerical MRs | 科学计算 | 跨元模式 | 自动发现等式和不等式关系 |
| (Chan et al., 1998) | numerical analysis MR | 科学计算 | 疑惑：P1 / P3 | 数值分析早期案例，可能同时含不变与收敛 |
| (T. Chen et al., 2009) | bioinformatics domain-specific MRs | 科学计算 | 跨元模式，以 P1 为主 | 领域性质为主，具体模式不止一类 |
| (Hiremath et al., 2021) | symmetries of simulated physical systems | 科学计算 | P1 守恒性 | 物理对称性最直接 |
| (Hiremath et al., 2020) | identity map and orthogonal MRs | 科学计算 | P1 守恒性 | 从海洋系统对称性出发 |
| (Contrastin et al., 2016) | units of measure, stencil specifications | 科学计算 | P1 守恒性 | 物理量纲与访问模式保持 |
| (Guderlei & Mayer, 2007) | statistical metamorphic testing | 概率程序 | 疑惑：P1 / P3 | 既有统计不变性，也有样本量相关收敛 |
| (Yoo, 2010) | stochastic optimisation MRs | 概率程序 | 疑惑：P3 / P5 | 常涉及迭代改进与结果排序 |
| (Ding et al., 2011) | Monte Carlo modeling MRs | 概率程序 | 疑惑：P1 / P3 | 采样一致性与统计收敛并存 |
| (Spieker et al., 2024) | trajectory mirroring, rescaling | 概率程序 | P4 轨迹性 | 直接针对轨迹预测 |
| (Ding & Hu, 2016) | Monte Carlo adequacy monitored MRs | 概率程序 | 疑惑：P1 / P3 | 统计 MT 与 adequacy 结合 |
| (Rounds & Kanewala, 2018) | GA statistical MRs | 概率程序 | 疑惑：P1 / P3 | 既看统计稳定性，也看迭代改进 |
| (Y. Chen et al., 2023) | Monte Carlo numerical calculation MRs | 概率程序 | 疑惑：P1 / P3 | 从随机抽样模型导出 |
| (Barthe et al., 2016) | martingale invariants | 概率程序 | P1 守恒性 | 期望保持不变 |
| (Bartocci et al., 2019) | moment-based invariants | 概率程序 | P1 守恒性 | 高阶矩不变量 |
| (Wang et al., 2019) | expected sensitivity | 概率程序 | P2 单调性 | 输入变化引起输出按界变化 |
| (Moosbrugger et al., 2022) | higher moments for probabilistic loops | 概率程序 | P1 守恒性 | 统计矩性质 |
| (Murphy et al., 2008) | ML property catalog | ML代理模型 | 跨元模式，以 P1 为主 | 排列、标签置换、加噪等性质并存 |
| (Xie et al., 2011) | MR-0 至 MR-5.2 | ML代理模型 | P1 守恒性 | 主要是预测结果不变或等价变换 |
| (Yang & Chui, 2021) | rainfall magnitude to runoff increase | ML代理模型 | P2 单调性 | 典型输入输出协变方向 |
| (Dwarakanath et al., 2018) | image transformation MRs | ML代理模型 | P1 守恒性 | 目标是对标签保持变换不变 |
| (Xie et al., 2009) | MR-0 至 MR-5.2 | ML代理模型 | P1 守恒性 | 以等价保持为主 |
| (Luu et al., 2021) | MR 1.1 至 MR 6 | ML代理模型 | 跨元模式，以 P1 为主 | 不变、缩放、平移、置换、旋转并存 |
| (Liu et al., 2022) | momentum conservation, translation and rotation invariance | ML代理模型 | P1 守恒性 | 守恒与对称直接内嵌模型 |
| (Prantl et al., 2022) | momentum conservation hard constraint | ML代理模型 | P1 守恒性 | 硬约束守恒 |
| (Bhattoo et al., 2021) | differentiable symmetries, energy and momentum conservation | ML代理模型 | P1 守恒性 | 对称与守恒是核心 |

## 表 3 程序类型 论文 MR 数量表

说明：

- 对明确给出 MR 编号的论文，直接按编号计数
- 对非标准 MT 论文，若文中直接给出可对应的 invariant 或 relation 关键词，则按关键词粗计，并在备注说明
- 无法从现有材料中稳定确定数量时，记为“未说明”

| 程序类型 | 论文 | MR 数量 | 备注 |
|:---|:---|---:|:---|
| 科学计算 | (Lin, Simon, & Niu, 2018) | 未说明 | hierarchical MRs |
| 科学计算 | (Olsen & Raunak, 2019) | 未说明 | simulation model relations |
| 科学计算 | (Raunak & Olsen, 2021) | 未说明 | simulation V and V relations |
| 科学计算 | (Yan & Zhu, 2024) | 未说明 | PDE numerical-model-derived MRs |
| 科学计算 | (Li et al., 2022) | 未说明 | 明确给出 4 类来源，但不是 4 条 MR |
| 科学计算 | (T. Chen et al., 2002) | 1 | 摘要明确为 identify a metamorphic relation |
| 科学计算 | (Lin et al., 2021) | 未说明 | nominal ordinal functional hierarchy |
| 科学计算 | (Luu et al., 2022) | 未说明 | tide periodicity related MRs |
| 科学计算 | (Li et al., 2021) | 未说明 | burnup time based MRs |
| 科学计算 | (Li et al., 2020) | 未说明 | physics burnup MR generation |
| 科学计算 | (Raunak & Olsen, 2015) | 未说明 | simulation validation MRs |
| 科学计算 | (T. Y. Chen et al., 2011) | 1 | 摘要明确为 identify a metamorphic relation |
| 科学计算 | (Olsen & Raunak, 2016) | 未说明 | ABM validation relations |
| 科学计算 | (Ding et al., 2019) | 未说明 | invariant relations |
| 科学计算 | (Farhan et al., 2021) | 未说明 | hybrid simulation relations |
| 科学计算 | (Lin, Simon, Niu, Carver, et al., 2018) | 未说明 | exploratory MT |
| 科学计算 | (Zhang et al., 2019) | 未说明 | 自动发现并清洗多条 numerical MRs |
| 科学计算 | (Chan et al., 1998) | 未说明 | numerical analysis MR |
| 科学计算 | (T. Chen et al., 2009) | 未说明 | bioinformatics domain-specific MRs |
| 科学计算 | (Hiremath et al., 2021) | 未说明 | ocean system symmetry based MRs |
| 科学计算 | (Hiremath et al., 2020) | 未说明 | automated MR scenario identification |
| 科学计算 | (Contrastin et al., 2016) | 2 | units of measure, stencil specifications |
| 概率程序 | (Guderlei & Mayer, 2007) | 未说明 | statistical metamorphic relations |
| 概率程序 | (Yoo, 2010) | 未说明 | stochastic optimisation MRs |
| 概率程序 | (Ding et al., 2011) | 未说明 | Monte Carlo modeling program MRs |
| 概率程序 | (Spieker et al., 2024) | 未说明 | trajectory prediction MRs |
| 概率程序 | (Ding & Hu, 2016) | 未说明 | Monte Carlo simulation MRs |
| 概率程序 | (Rounds & Kanewala, 2018) | 17 | 文中明确 identified 17 metamorphic relations |
| 概率程序 | (Y. Chen et al., 2023) | 未说明 | Monte Carlo numerical calculation MRs |
| 概率程序 | (Barthe et al., 2016) | 未说明 | probabilistic invariants, martingales |
| 概率程序 | (Bartocci et al., 2019) | 未说明 | moment-based invariants |
| 概率程序 | (Wang et al., 2019) | 1 | expected sensitivity |
| 概率程序 | (Moosbrugger et al., 2022) | 未说明 | higher moments |
| ML代理模型 | (Murphy et al., 2008) | 6 | 6 类通用性质类别，不是具体实例化 MR |
| ML代理模型 | (Xie et al., 2011) | 11 | MR-0 至 MR-5.2 |
| ML代理模型 | (Yang & Chui, 2021) | 未说明 | hydrological consistency MRs |
| ML代理模型 | (Dwarakanath et al., 2018) | 未说明 | image classifier MRs |
| ML代理模型 | (Xie et al., 2009) | 11 | MR-0 至 MR-5.2 |
| ML代理模型 | (Luu et al., 2021) | 11 | Table 1 明确列出 MR 1.1 至 MR 6 |
| ML代理模型 | (Liu et al., 2022) | 3 | momentum conservation, translation invariance, rotation invariance |
| ML代理模型 | (Prantl et al., 2022) | 1 | momentum conservation |
| ML代理模型 | (Bhattoo et al., 2021) | 4 | translational symmetry, rotational symmetry, energy conservation, momentum conservation |

## 创新点表述

本文的创新不在于再罗列若干零散的蜕变关系，而在于围绕三类目标程序，即传统科学计算程序、概率程序和 ML 代理模型程序，提出一个更高层的统一验证框架，并分别回答两个更基础的问题：蜕变关系从哪里来，以及在领域知识不足时蜕变关系如何从 0 到 1 被诱导出来。

### 创新点 1 MR 层次分类模型

本文提出一个按来源组织的蜕变关系层次分类模型，将蜕变关系系统划分为数学物理模型层、计算方法层、代码实现层和运行行为层。该模型的创新在于，它不再按应用领域、表示形式或自动化方式理解蜕变关系，而是从关系来源出发，系统回答“MR 从哪里来”这一长期缺少统一框架的问题。现有文献中虽然已经零散出现了来自物理方程、数值算法、程序规格、执行行为等不同来源的关系，但尚未形成一个可同时覆盖三类程序的稳定层次模型。本文的层次分类模型正是对这些分散来源的统一组织，因此其创新性质主要属于理论创新。

### 创新点 2 MR 元模式框架

本文进一步提出五类蜕变关系元模式，即 P1 守恒性、P2 单调性、P3 收敛性、P4 轨迹性和 P5 偏序性。它们不是具体 MR 的简单汇总，而是可跨程序范式迁移的高层诱导模板。其作用是，当测试人员并非领域专家、缺乏足够先验知识时，能够借助元模式，从程序应保持的物理不变性质与结构规律出发，系统诱导出可检验的具体 MR。换言之，这一框架试图把 MR 的设计从依赖经验的手工猜测，推进为可指导、可迁移、可复用的方法过程。因此，元模式框架的创新性质主要属于方法创新。

### 创新点 3 三类程序共享的统一验证主张

本文不再把传统科学计算程序、概率程序和 ML 代理模型程序视为彼此割裂的测试对象，而是提出如下统一主张：三类程序虽然分别表现为真值缺失、随机性掩蔽和分布外失效，但其共同的验证基础并不是对点值真解的恢复，而是检验程序是否保持了其必须保持的物理不变性质及其派生结构规律。由此，本文将三类程序中的关系证据、统计证据和可信性证据统一理解为同一判定基础在不同程序范式中的展开形式。这一主张使蜕变测试不再只是具体技术，而成为连接三类程序验证问题的一条共同理论主线。

### 一句话概括

本文的核心创新在于，把蜕变测试从“为具体程序寻找若干关系”推进为“以物理不变性质为根、以层次模型组织来源、以元模式指导诱导”的统一验证框架。

## 本文贡献

本文围绕传统科学计算程序、概率程序和机器学习代理模型程序三类对象，试图回答一个共同问题：在点值预言缺失的条件下，如何建立统一而可操作的验证准则。围绕这一目标，本文的主要贡献如下。

### 1 提出三类程序共享的统一验证观点

本文提出，对三类目标程序而言，其测试困难虽然分别表现为真值缺失、随机性掩蔽和分布外失效，但其共同的判定基础不是恢复不可得的点值真解，而是检验程序是否保持了其必须保持的物理不变性质及其派生结构规律。基于这一观点，本文将三类程序中的关系证据、统计证据和可信性证据统一理解为同一验证基础在不同程序范式中的展开形式。

### 2 提出 MR 层次分类模型

本文从关系来源出发，提出一个按来源组织的蜕变关系层次分类模型，将蜕变关系划分为数学物理模型层、计算方法层、代码实现层和运行行为层。该模型旨在系统回答“MR 从哪里来”的问题，并将已有文献中分散出现的关系来源组织成一个可同时覆盖三类程序的统一结构。

### 3 提出五类 MR 元模式

本文提出五类可跨程序范式迁移的蜕变关系元模式，即守恒性、单调性、收敛性、轨迹性和偏序性。该框架旨在回答“在领域知识不足时，如何从 0 到 1 诱导 MR”的问题。与将 MR 视为个案经验不同，本文将元模式理解为面向关系构造的高层模板，用于指导测试人员从物理不变性质与结构规律出发构造具体 MR。

### 4 基于文献证据对层次模型与元模式进行系统归纳

本文通过对相关代表论文的系统梳理，建立三张归纳表：MR 层次分类模型归类表、MR 元模式归类表，以及程序类型、论文与 MR 数量统计表。这些表格一方面为本文提出的层次模型与元模式框架提供文献支撑，另一方面也揭示了现有研究的证据分布：P1 守恒性最强，P2 单调性与 P3 收敛性已有较稳定支撑，P4 轨迹性主要集中在仿真与时间演化程序中，而 P5 偏序性目前仍相对薄弱。

### 5 澄清现有研究中的空缺与本文的位置

本文指出，现有研究虽然已经在局部上展示了 MR 可以来自物理方程、数值算法、程序规格、运行行为以及统计性质，但尚未形成一个统一的来源层次模型；同时，现有研究虽已零散呈现出守恒、单调、收敛、轨迹和偏序等跨问题可迁移的关系雏形，但尚未被系统提升为元模式框架。本文因此将自身定位为一项连接已有局部方法与统一验证理论的工作：层次分类模型回答来源问题，元模式回答诱导问题，而统一验证主张回答三类程序为何能够被放在同一理论框架下理解。

## 表格解释与理论主张

清理后的三张表把证据集中到了真正与三类目标程序相关的论文上，结论比原始表更清楚。

首先，从表 1 看，现有文献已经明显支持“MR 可以按来源分层组织”这一判断，但支持方式是分散的，而不是现成统一的。科学计算程序中，(Li et al., 2022) 最直接，因为它明确区分了 physical model、computational model 和 code model 三类 MR，并额外提出 likely MR，已经很接近本文要主张的层次分类模型。与此同时，(Yan & Zhu, 2024)、(T. Chen et al., 2002)、(Li et al., 2021)、(Li et al., 2020) 把 MR 直接系到方程、燃耗方程或离散算法上，(Contrastin et al., 2016) 则从量纲和 stencil specification 这类轻量规格给出代码实现层的旁证，(Olsen & Raunak, 2019)、(Raunak & Olsen, 2021)、(Olsen & Raunak, 2016)、(Farhan et al., 2021)、(Lin, Simon, Niu, Carver, et al., 2018) 则把仿真模型行为与演化轨迹组织成运行行为层。概率程序中的证据更集中在计算方法层与运行行为层，如 (Ding et al., 2011)、(Ding & Hu, 2016)、(Y. Chen et al., 2023) 依托随机采样模型，(Barthe et al., 2016)、(Bartocci et al., 2019)、(Wang et al., 2019)、(Moosbrugger et al., 2022) 依托概率不变量、矩和灵敏度性质。ML 代理模型则在两端展开：一端是 (Xie et al., 2009)、(Xie et al., 2011)、(Luu et al., 2021) 这类算法性质驱动的计算方法层，另一端是 (Yang & Chui, 2021)、(Liu et al., 2022)、(Prantl et al., 2022)、(Bhattoo et al., 2021) 这类由物理系统性质直接导出的数学物理层。换句话说，文献并不缺“来源导向”的局部证据，真正缺的是把这些局部来源统一组织成一个稳定的四层模型。这正是层次分类模型的理论空间。

其次，从表 2 看，五类元模式并不是均匀分布的。P1 守恒性最强，几乎是三类程序共同的硬核证据。科学计算中，潮汐周期性、光散射不变量、海洋系统对称性都可直接落到 P1。(Ding et al., 2019; Hiremath et al., 2021; Luu et al., 2022) 概率程序中，martingale invariants、moment-based invariants 和更一般的统计不变量也都落到 P1。(Barthe et al., 2016; Bartocci et al., 2019; Moosbrugger et al., 2022) ML 代理模型中，动量守恒、平移旋转不变性更是直接把 P1 内嵌进模型结构。(Bhattoo et al., 2021; Liu et al., 2022; Prantl et al., 2022) P2 单调性也有支撑，但更偏局部，如 (Yang & Chui, 2021) 的降雨到径流方向性，以及 (Wang et al., 2019) 的 expected sensitivity。P3 收敛性在传统科学计算和概率程序中都很自然，典型如 (T. Chen et al., 2002)、(T. Y. Chen et al., 2011) 以及若干 Monte Carlo 论文，因此它很适合作为第二强元模式。P4 轨迹性主要集中在仿真与时间演化程序，如 (Olsen & Raunak, 2019)、(Raunak & Olsen, 2021)、(Li et al., 2021)、(Spieker et al., 2024)。P5 偏序性在清理后样本中最弱，这不是坏事，反而提示它更可能是你框架里“理论上必要、经验上尚待补强”的一类，而不是一个已经被文献充分证明的共识模式。

再次，从表 3 看，现有文献并不总是显式报告 MR 数量。真正给出系统编号并可直接统计的，主要集中在 (Xie et al., 2009)、(Xie et al., 2011)、(Luu et al., 2021) 和 (Rounds & Kanewala, 2018) 这类经典案例。大量科学计算与概率程序论文虽然明确使用了 MR 或 invariant，但更关注关系来源、验证逻辑与故障检测，而不是把 MR 编号标准化。这一点对本文有两层意义：一方面，说明 MR 的“来源组织”和“元模式组织”本身比单纯计数更接近理论问题；另一方面，也说明你提出元模式作为“0 到 1 诱导框架”是有现实必要性的，因为大量论文虽然能提出有效 MR，但并没有给测试人员留下一个可复用的诱导模板。

据此，本文可以更稳地提出如下理论主张：

> 对三类目标程序，即传统科学计算程序、概率程序和 ML 代理模型程序，MR 的共同根源不是某种孤立的测试技巧，而是程序必须保持的物理不变性质及其派生结构规律。现有文献已经在局部上分别展示了这种来源可以来自数学物理模型、计算方法、代码实现和运行行为，但尚未形成统一的来源层次模型；同时，现有文献也已零散显示出守恒、单调、收敛、轨迹和偏序等可跨问题迁移的关系雏形，却尚未被系统提升为元模式框架。由此，本文所主张的 MR 层次分类模型是对“MR 从哪里来”的理论组织，而 MR 元模式则是对“在领域知识不足时如何从 0 到 1 诱导 MR”的方法回应。

如果把这个主张再压缩一句，就是：

> 层次分类模型回答 MR 的来源问题，元模式回答 MR 的诱导问题，而三类程序共享的判定基础则是物理不变性质及其派生结构规律。

---

## References

Barthe, G., Espitau, T., Fioriti, L. M. F., & Hsu, J. (2016). Synthesizing Probabilistic Invariants via Doob’s Decomposition. *ArXiv*, *abs/1605.02765*. <https://doi.org/10.1007/978-3-319-41528-4_3>

Bartocci, E., Kovács, L., & Stankovič, M. (2019). Automatic Generation of Moment-Based Invariants for Prob-Solvable Loops. *ArXiv*, *abs/1905.02835*. <https://doi.org/10.1007/978-3-030-31784-3_15>

Bhattoo, R., Ranu, S., & Krishnan, N. (2021). Lagrangian Neural Network with Differentiable Symmetries and Relational Inductive Bias. *ArXiv*, *abs/2110.03266*.

Chan, F. T., Chen, T., Cheung, S., Lau, M., & Yiu, S. (1998). Application of metamorphic testing in numerical analysis. In *International Conference on Software Engineering*.

Chen, T. Y., Feng, J., & Tse, T. H. (2011). *Title Metamorphic testing of programs on partial differentialequations : a case study*.

Chen, T., Feng, J., & Tse, T. H. (2002). Metamorphic testing of programs on partial differential equations: a case study. *Proceedings 26th Annual International Computer Software and Applications*, 327–333. <https://doi.org/10.1109/CMPSAC.2002.1045022>

Chen, T., Ho, J., Liu, H., & Xie, X. (2009). An innovative approach for testing bioinformatics programs using metamorphic testing. *BMC Bioinformatics*, *10*, 24–24. <https://doi.org/10.1186/1471-2105-10-24>

Chen, Y., Yan, S., & Yang, X. (2023). A Case Study of Metamorphic Test for Monte Carlo Numerical Calculation Programs. *2023 International Conference on Applied Physics and Computing (ICAPC)*, 69–73. <https://doi.org/10.1109/ICAPC61546.2023.00019>

Contrastin, M., Danish, M., Rice, A., & Orchard, D. A. (2016). *Supporting Software Sustainability with Lightweight Specifications*.

Ding, J., & Hu, X.-H. (2016). Application of metamorphic testing monitored by test adequacy in a Monte Carlo simulation program. *Software Quality Journal*, *25*, 841–869. <https://doi.org/10.1007/s11219-016-9337-3>

Ding, J., Li, X., & Hu, X.-H. (2019). Testing Scientific Software with Invariant Relations: A Case Study. *2019 IEEE 19th International Conference on Software Quality, Reliability and Security (QRS)*, 406–417. <https://doi.org/10.1109/QRS.2019.00057>

Ding, J., Wu, T., Xu, D., Lu, J. Q., & Hu, X.-H. (2011). Metamorphic testing of a Monte Carlo modeling program. *International Conference/Workshop on Automation of Software Test*, 1–7. <https://doi.org/10.1145/1982595.1982597>

Dwarakanath, A., Ahuja, M., Sikand, S., Rao, R. M., Bose, J. C. J. C., Dubash, N., & Podder, S. (2018). Identifying implementation bugs in machine learning based image classifiers using metamorphic testing. In *Proceedings of the 27th ACM SIGSOFT International Symposium on Software Testing and Analysis*. <https://doi.org/10.1145/3213846.3213858>

Farhan, M., Krejci, C. C., Olsen, M. M., & Raunak, M. (2021). Metamorphic Testing for Hybrid Simulation Validation. *2021 Annual Modeling and Simulation Conference (ANNSIM)*, 1–12. <https://doi.org/10.23919/ANNSIM52504.2021.9552058>

Guderlei, R., & Mayer, J. (2007). Statistical Metamorphic Testing Testing Programs with Random Output by Means of Statistical Hypothesis Tests and Metamorphic Testing. *Seventh International Conference on Quality Software (QSIC 2007)*, 404–409. <https://doi.org/10.1109/QSIC.2007.54>

Hiremath, D. J., Claus, M., Hasselbring, W., & Rath, W. (2020). Automated identification of metamorphic test scenarios for an ocean-modeling application. *2020 IEEE International Conference On Artificial Intelligence Testing (AITest)*, 62–63. <https://doi.org/10.1109/AITEST49225.2020.00016>

Hiremath, D. J., Claus, M., Hasselbring, W., & Rath, W. (2021). Towards Automated Metamorphic Test Identification for Ocean System Models. *2021 IEEE/ACM 6th International Workshop on Metamorphic Testing (MET)*, 42–46. <https://doi.org/10.1109/MET52542.2021.00014>

Li, M., Wang, L., Yan, S., & Yang, X. (2020). Metamorphic Relation Generation for Physics Burnup Program Testing. *Int. J. Perform. Eng.*, *16*, 297–306. <https://doi.org/10.23940/IJPE.20.02.P12.297306>

Li, M., Wang, L., Yue, W., Liu, B., Liu, J., Liu, Z.-H., Yan, S., & Yang, X. (2021). Metamorphic testing of the NUIT code based on burnup time. In *Annals of Nuclear Energy* (Vol. 153, p. 108027). <https://doi.org/10.1016/j.anucene.2020.108027>

Li, M., Yang, X., Yan, S., Liu, J., Liu, Y., & Sun, J. (2022). A Lightweight Verification Method Based on Metamorphic Relation for Nuclear Power Software. In *Frontiers in Energy Research* (Vol. 10). <https://doi.org/10.3389/fenrg.2022.788753>

Lin, X., Simon, M., & Niu, N. (2018). Hierarchical Metamorphic Relations for Testing Scientific Software. In *2018 IEEE/ACM 13th International Workshop on Software Engineering for Science (SE4Science)* (pp. 1–8). <https://doi.org/10.1145/3194747.3194750>

Lin, X., Simon, M., Niu, N., Carver, J. C., & Rouson, D. (2018). Exploratory Metamorphic Testing for Scientific Software. *Computing in Science & Engineering*, *22*, 78–87. <https://doi.org/10.1109/MCSE.2018.2880577>

Lin, X., Simon, M., Peng, Z., Niu, N., Carver, J. C., & Morris, K. (2021). Discovering Metamorphic Relations for Scientific Software From User Forums. *Computing in Science & Engineering*, *23*, 65–72. <https://doi.org/10.1109/MCSE.2020.3046973>

Liu, N., Yu, Y., You, H., & Tatikola, N. (2022). INO: Invariant Neural Operators for Learning Complex Physical Systems with Momentum Conservation. *International Conference on Artificial Intelligence and Statistics*, 6822–6838. <https://doi.org/10.48550/arXiv.2212.14365>

Luu, Q.-H., Lau, M., Ng, S., & Chen, T. (2021). Testing Multiple Linear Regression Systems with Metamorphic Testing. *ArXiv*, *abs/2108.07584*. <https://doi.org/10.1016/j.jss.2021.111062>

Luu, Q.-H., Liu, H., Chen, T., & Vu, H. L. (2022). Testing Ocean Software with Metamorphic Testing. In *2022 IEEE/ACM 7th International Workshop on Metamorphic Testing (MET)* (pp. 23–30). <https://doi.org/10.1145/3524846.3527341>

Moosbrugger, M., Stankovivc, M., Bartocci, E., & Kov’acs, L. (2022). This is the moment for probabilistic loops. *Proceedings of the ACM on Programming Languages*, *6*, 1497–1525. <https://doi.org/10.1145/3563341>

Murphy, C., Kaiser, G. E., Hu, L., & Wu, L. L. (2008). Properties of Machine Learning Applications for Use in Metamorphic Testing. *International Conference on Software Engineering and Knowledge Engineering*, 867–872. <https://doi.org/10.7916/D8XK8PFD>

Olsen, M. M., & Raunak, M. (2016). Metamorphic validation for agent-based simulation models. *Summer Simulation Multiconference*, 33. <https://doi.org/10.22360/summersim.2016.scsc.041>

Olsen, M. M., & Raunak, M. (2019). Increasing Validity of Simulation Models Through Metamorphic Testing. *IEEE Transactions on Reliability*, *68*, 91–108. <https://doi.org/10.1109/TR.2018.2850315>

Prantl, L., Ummenhofer, B., Koltun, V., & Thuerey, N. (2022). Guaranteed Conservation of Momentum for Learning Particle-based Fluid Dynamics. *ArXiv*, *abs/2210.06036*. <https://doi.org/10.48550/arXiv.2210.06036>

Raunak, M., & Olsen, M. M. (2015). Simulation validation using metamorphic testing (WIP). *Summer Simulation Multiconference*, 69:1–69:6.

Raunak, M., & Olsen, M. M. (2021). Metamorphic Testing on the Continuum of Verification and Validation of Simulation Models. *2021 IEEE/ACM 6th International Workshop on Metamorphic Testing (MET)*, 47–52. <https://doi.org/10.1109/MET52542.2021.00015>

Rounds, J., & Kanewala, U. (2018). Systematic Testing of Genetic Algorithms: A Metamorphic Testing based Approach. *ArXiv*, *abs/1808.01033*.

Spieker, H., Belmecheri, N., Gotlieb, A., & Lazaar, N. (2024). Evaluating Human Trajectory Prediction with Metamorphic Testing. *Proceedings of the 9th ACM International Workshop on Metamorphic Testing*. <https://doi.org/10.1145/3679006.3685071>

Wang, P., Fu, H., Chatterjee, K., Deng, Y., & Xu, M. (2019). Proving expected sensitivity of probabilistic programs with randomized variable-dependent termination time. *Proceedings of the ACM on Programming Languages*, *4*, 1–30. <https://doi.org/10.1145/3371093>

Xie, X., Ho, J., Murphy, C., Kaiser, G. E., Xu, B., & Chen, T. (2009). Application of Metamorphic Testing to Supervised Classifiers. *2009 Ninth International Conference on Quality Software*, 135–144. <https://doi.org/10.1109/QSIC.2009.26>

Xie, X., Ho, J., Murphy, C., Kaiser, G. E., Xu, B., & Chen, T. (2011). Testing and validating machine learning classifiers by metamorphic testing. *The Journal of Systems and Software*, *84 4*, 544–558. <https://doi.org/10.1016/J.JSS.2010.11.920>

Yan, S., & Zhu, H. (2024). Metamorphic Testing on Scientific Programs for Solving Second‐Order Elliptic Differential Equations. *Software Testing*, *35*. <https://doi.org/10.1002/stvr.1912>

Yang, Y., & Chui, T. M. (2021). Reliability Assessment of Machine Learning Models in Hydrological Predictions Through Metamorphic Testing. In *Water Resources Research* (Vol. 57). <https://doi.org/10.1029/2020WR029471>

Yoo, S. (2010). Metamorphic Testing of Stochastic Optimisation. *2010 Third International Conference on Software Testing, Verification, and Validation Workshops*, 192–201. <https://doi.org/10.1109/ICSTW.2010.26>

Zhang, B., Zhang, H., Chen, J., Hao, D., & Moscato, P. (2019). Automatic Discovery and Cleansing of Numerical Metamorphic Relations. *2019 IEEE International Conference on Software Maintenance and Evolution (ICSME)*, 235–245. <https://doi.org/10.1109/ICSME.2019.00035>
