# 独立论文升级方案：蜕变测试应用于核反应堆PINN代理模型的物理一致性验证

## —— 从 Survey 第6.6.4节配套实验 升级为 独立可发表论文

---

> **本文档用途**：在主实验方案和补充材料的基础上，增加与原文的对比实验、系统性评价指标体系、P5偏序性覆盖、以及独立论文所需的研究问题/贡献声明/讨论框架，使实验方案达到独立论文的发表要求。

---

## P1　论文定位与研究问题

### P1.1　投稿目标期刊

| 期刊 | 理由 | 预估篇幅 |
|------|------|---------|
| **首选：Annals of Nuclear Energy (ANE)** | 作者团队已有该刊MT论文发表记录[47,50]；PINN+V&V是ANE近两年高频主题 | 12—15页 |
| 备选1：Nuclear Science and Engineering (NSE) | PINN代理模型V&V方法论正符合该刊当前关注点 | 15—18页 |
| 备选2：Nuclear Engineering and Technology (NET) | 对方法论创新的发表门槛较ANE略低，适合首次MT+ML交叉工作 | 10—14页 |

### P1.2　论文标题建议

> **Metamorphic Testing of Physics-Informed Neural Networks for Nuclear Reactor Point Kinetics: A Physical Consistency Verification Framework with Statistical Violation Analysis**

中文工作标题：基于蜕变测试的核反应堆PINN点堆动力学求解器物理一致性验证框架

### P1.3　三个研究问题（RQ）

现有实验方案回答的是"概念验证"层面的三个方法论问题。升级为独立论文后，需要重构为可证伪的研究问题：

**RQ1（迁移可行性）**：已在确定性核工程软件上建立的蜕变关系元模式（P1守恒性、P2单调性、P4轨迹性），在迁移至求解相同物理方程的PINN代理模型时，其缺陷检出能力（fault detection capability）是否保持？

- 度量指标：蜕变关系在PINN上的违反率 $\bar{V}_r$ 与在参考ODE求解器上的违反率（零基线）的差值
- 创新点：首次将MT元模式从传统核软件系统性迁移至ML代理模型

**RQ2（ML约束量化）**：PINN的训练随机性、训练域边界和连续输出容差三个ML特有因素，分别对蜕变测试的统计违反率产生多大影响？

- 度量指标：违反率的跨运行标准差 $\sigma_{V_r}$、域内/域外违反率差 $\Delta V_r = \bar{V}_r^{out} - \bar{V}_r^{in}$、容差敏感性曲线的拐点位置
- 创新点：首次提出蜕变测试在ML代理模型上的统计执行协议

**RQ3（工程诊断价值）**：蜕变测试的违反模式（哪条MR在何种条件下被违反）能否提供PINN预测可靠性退化的先兆信号，且该信号独立于参考解比对？

- 度量指标：违反模式与预测误差之间的相关性（Spearman秩相关）、蜕变测试作为域外检测器的ROC特性
- 创新点：将蜕变测试从离线V&V工具扩展为潜在的在线监控信号

### P1.4　论文贡献声明

相比Survey第6.6.4节的"概念验证"定位，独立论文的贡献需提升至以下三点：

1. **方法论贡献**：提出面向核工程PINN代理模型的蜕变测试执行框架，包括统计违反率协议、自适应容差策略和域内/域外分层诊断逻辑，并在PKE-PINN上完成首次端到端实证。
2. **实证贡献**：通过对Prantikos TL-PINN[44]的系统性蜕变测试，提供关于PINN物理一致性的定量证据——包括守恒律满足度、单调性保持范围、轨迹形态合规性——补充原论文中未涉及的V&V维度。
3. **工程贡献**：展示蜕变测试违反模式与PINN预测误差之间的相关性，论证其作为域外检测辅助信号的工程价值。

---

## P2　与 Prantikos 原文的系统性对比实验

### P2.1　对比设计的逻辑

Prantikos的两篇论文（2022 Energies版[原文A]；2023 Scientific Reports版[原文B]）报告了以下V&V内容：

| V&V维度 | 原文A (Energies 2022) | 原文B (Sci. Rep. 2023) | 本论文补充 |
|---------|----------------------|----------------------|-----------|
| 训练域内精度 | ✓ 与ODE45比对，报告百分比误差 | ✓ 与ODE45比对，5个RT | ✓ 复现并独立确认 |
| 外推精度 | ✓ 5s/10s/15s时间外推 | — | ✓ 参数空间外推（MR-P2c） |
| 迁移学习效果 | — | ✓ TL-PINN vs PINN训练加速 | ✓ TL-PINN vs PINN精度偏序性（P5） |
| 物理残差 | △ 损失函数含残差项但未独立报告 | △ 同上 | ✓ 后验物理残差系统分析 |
| 守恒律满足度 | ✗ 未涉及 | ✗ 未涉及 | ✓ **本文核心贡献** |
| 单调性检验 | ✗ 未涉及 | ✗ 未涉及 | ✓ **本文核心贡献** |
| 轨迹形态检验 | △ 图形展示但无定量判据 | △ 同上 | ✓ **本文核心贡献**（定量化） |
| UQ / 训练随机性分析 | ✗ 未涉及 | ✗ 未涉及 | ✓ N=10独立训练统计 |
| 域外检测 | ✗ 未涉及 | ✗ 未涉及 | ✓ MR-P2c违反模式 |

**关键发现**：原文A和B的V&V完全停留在"与ODE45参考解的数值比对"这一单一通道上，不涉及任何独立于参考解的物理一致性验证。本论文恰好填补这一空白。

### P2.2　精度复现实验（Baseline Reproduction）

**目的**：确认本实验的PINN实现精度与Prantikos原文一致，排除实现差异对蜕变测试结果的干扰。

**复现内容**：

| 原文报告的指标 | 原文数值 | 本文复现目标 | 判定准则 |
|--------------|---------|------------|---------|
| RT-1训练时间 | ~62 s | 记录实际时间 | 同量级（30—120 s） |
| $n(t)$插值平均相对误差 | < 1% (原文B) | 复现 | ≤ 2%（允许实现差异） |
| $n(t)$ L2相对误差 | 原文A Table 4-6 | 复现 | 同量级 |
| 损失函数收敛曲线形态 | 原文A Fig 7a | 复现 | 定性一致 |

**实施方式**：

```python
# 新增评价脚本: scripts/reproduce_baseline.py

def reproduce_comparison(rt_name, n_runs=10):
    """复现Prantikos论文精度并与原文对比"""
    
    metrics = {
        'mae_percent': [],      # 平均绝对百分比误差
        'l2_relative': [],       # L2相对误差
        'max_error_percent': [], # 最大百分比误差
        'training_time_s': [],   # 训练时间
        'n_peak_error': [],      # 峰值误差
        't_peak_error': [],      # 峰值时刻误差
    }
    
    for run in range(n_runs):
        # 加载PINN预测和ODE45参考解
        pred = load_prediction(rt_name, run)
        ref = load_reference(rt_name)
        
        # 计算各指标
        rel_err = np.abs(pred['n'] - ref['n']) / (np.abs(ref['n']) + 1e-30)
        
        metrics['mae_percent'].append(np.mean(rel_err) * 100)
        metrics['l2_relative'].append(
            np.sqrt(np.sum((pred['n'] - ref['n'])**2) / np.sum(ref['n']**2))
        )
        metrics['max_error_percent'].append(np.max(rel_err) * 100)
        metrics['n_peak_error'].append(
            abs(pred['n'].max() - ref['n'].max()) / ref['n'].max() * 100
        )
        metrics['t_peak_error'].append(
            abs(pred['t'][np.argmax(pred['n'])] - ref['t'][np.argmax(ref['n'])])
        )
    
    return {k: (np.mean(v), np.std(v)) for k, v in metrics.items()}
```

### P2.3　PINN vs TL-PINN 对比实验（覆盖P5偏序性）

**核心设计**：Prantikos原文B的主要贡献是TL-PINN通过迁移学习加速训练。本论文增加一个关键问题：**TL-PINN在物理一致性方面是否优于标准PINN？**

这恰好覆盖了主实验方案附录B中标注为"未覆盖"的**P5偏序性**元模式。

**P5蜕变关系 MR-P5a（迁移学习精度偏序）**：

- 物理预期：TL-PINN经过预训练，应在目标RT上达到不低于标准PINN的精度（至少在训练域内）
- 蜕变关系：对同一RT，TL-PINN的L2相对误差 ≤ 标准PINN的L2相对误差

**P5蜕变关系 MR-P5b（迁移学习物理一致性偏序）**：

- 物理预期：TL-PINN的物理约束通过预训练已部分学习，物理一致性应不劣于标准PINN
- 蜕变关系：TL-PINN的MR违反率 ≤ 标准PINN的MR违反率

**实验增量**：

| 实验 | 标准PINN | TL-PINN | 对比分析 |
|------|---------|---------|---------|
| RT-2训练 | 从零开始，N=10次 | 从RT-1预训练模型出发，N=10次 | 精度偏序 + MR违反率偏序 |
| RT-3训练 | 从零开始，N=10次 | 从RT-1预训练模型出发，N=10次 | 同上 |
| RT-4训练 | 从零开始，N=10次 | 从RT-1预训练模型出发，N=10次 | 同上 |

**额外计算成本**：~30分钟（3个RT × N=10 × ~62秒），完全可行。

### P2.4　后验物理残差分析（原文未做的独立验证通道）

原文将物理残差仅作为训练损失函数的一部分，未将其作为独立的V&V指标进行后验分析。本论文补充这一维度：

**后验物理残差定义**：在训练完成后，在密集测试网格（如5000个时间点）上重新计算PKE方程残差：

$$R_n(t) = \left|\frac{d\hat{n}}{dt} - \frac{\rho(t) - \beta}{\Lambda}\hat{n}(t) - \sum_{i=1}^{6}\lambda_i\hat{c}_i(t) - S\right|$$

$$R_{c_i}(t) = \left|\frac{d\hat{c}_i}{dt} - \frac{\beta_i}{\Lambda}\hat{n}(t) + \lambda_i\hat{c}_i(t)\right|$$

其中 $\hat{n}$, $\hat{c}_i$ 为PINN预测，$d\hat{n}/dt$通过自动微分计算。

**报告指标**：

- 后验残差的时间平均值 $\bar{R}_n$, $\bar{R}_{c_i}$
- 后验残差的最大值及其对应时刻
- 后验残差与预测误差之间的相关性（Spearman秩相关系数）

---

## P3　系统性评价指标体系

### P3.1　三层指标架构

将评价指标按"精度—物理一致性—方法论有效性"三个层次组织，每层覆盖原文对比和蜕变测试两个维度：

#### 第一层：精度指标（与参考解比对 —— 复现原文并扩展）

| 指标名 | 数学定义 | 物理含义 | 原文是否报告 |
|--------|---------|---------|:----------:|
| 平均绝对百分比误差 MAPE | $\frac{1}{T}\int_0^T \frac{|\hat{n}-n_{ref}|}{|n_{ref}|}dt \times 100\%$ | 全时域平均预测精度 | ✓ |
| L2相对误差 $\epsilon_{L2}$ | $\sqrt{\frac{\sum(\hat{n}-n_{ref})^2}{\sum n_{ref}^2}}$ | 加权整体偏差 | ✓ |
| 峰值相对误差 $\epsilon_{peak}$ | $\frac{|\hat{n}_{peak}-n_{peak}^{ref}|}{n_{peak}^{ref}} \times 100\%$ | 安全分析最关键参数的精度 | △（图形可推断） |
| 峰值时刻偏差 $\Delta t_{peak}$ | $|\hat{t}_{peak} - t_{peak}^{ref}|$ (s) | 瞬态响应的时序精度 | ✗ |
| 稳态相对误差 $\epsilon_{ss}$ | $\frac{|\hat{n}_{ss}-n_{ss}^{ref}|}{n_{ss}^{ref}} \times 100\%$ | 长期预测精度 | ✗ |
| 先驱核密度L2误差 $\epsilon_{c_i}$ | 对六组$c_i$分别计算$\epsilon_{L2}$ | 多输出通道精度 | ✗ |

#### 第二层：物理一致性指标（蜕变测试 —— 本文核心贡献）

| 指标名 | 数学定义 | 物理含义 |
|--------|---------|---------|
| 统计违反率 $\bar{V}_r \pm \sigma_{V_r}$ | 见主方案4.1.2节 | MR被PINN违反的概率 |
| 域内违反率 $\bar{V}_r^{in}$ | 仅在训练域内RT参数范围统计 | 模型架构/训练的本质缺陷指标 |
| 域外违反率 $\bar{V}_r^{out}$ | 仅在训练域外Δρ方案统计 | 训练覆盖不足指标 |
| 域内外违反率差 $\Delta V_r$ | $\bar{V}_r^{out} - \bar{V}_r^{in}$ | 域外泛化退化的物理约束信号强度 |
| 闭合残差 $R_{closure}$ | 见主方案MR-P1a | 守恒律满足度的定量指标 |
| 有效β偏差 $\delta_{\beta}$ | $|\hat{\beta}_{eff} - \beta| / \beta$ | 缓发中子守恒精度 |
| 单调性违反对数 $N_{mono}$ | 违反排序的RT配对数 | 物理方向性约束的合规度 |
| 形态违反项数 $N_{shape}$ | P4a中4项检验的违反计数 | 轨迹定性合规度 |
| 衰减时间常数偏差 $\delta_{\tau}$ | $|\hat{\tau} - 1/\lambda_6| / (1/\lambda_6)$ | 瞬态衰减物理合理性 |

#### 第三层：方法论有效性指标（蜕变测试作为V&V工具的质量）

| 指标名 | 数学定义 | 含义 |
|--------|---------|------|
| 假阳性率 FPR | ODE45参考解上的MR违反率（应为零） | MR设计正确性验证 |
| 容差敏感性拐点 $\alpha^*$ | $V_r(\alpha)$曲线斜率变化最大处的$\alpha$值 | 逼近误差与物理违反的可分离性 |
| 违反-误差相关系数 $\rho_s$ | MR违反率与$\epsilon_{L2}$的Spearman秩相关 | 蜕变测试的工程诊断价值 |
| 域外检测ROC-AUC | 以MR违反模式为检测器、以域外标签为真值 | 蜕变测试作为域外检测器的性能 |
| P5偏序一致率 | TL-PINN优于PINN的指标占比 | 偏序蜕变关系的物理合理性 |
| 统计收敛性 $N^*$ | $\sigma_{V_r}$降至$0.01$以下所需的最小$N$ | 多运行协议的实用性指导 |

### P3.2　指标汇总表模板（论文核心表格）

**表1：PINN精度复现与原文对比**

| RT方案 | 原文MAPE (%) | 本文MAPE (%) [$\bar{x}\pm\sigma$, N=10] | 原文$\epsilon_{L2}$ | 本文$\epsilon_{L2}$ [$\bar{x}\pm\sigma$] | $\epsilon_{peak}$ (%) | $\Delta t_{peak}$ (s) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| RT-1 | < 1 | — | — | — | — | — |
| RT-2 | < 1 | — | — | — | — | — |
| RT-3 | — | — | — | — | — | — |
| RT-4 | — | — | — | — | — | — |
| RT-5 | — | — | — | — | — | — |

**表2：蜕变关系违反率综合结果**（论文核心结果表，升级版）

| MR | 元模式 | 测试用例对数 | $\bar{V}_r^{in}\pm\sigma$ | $\bar{V}_r^{out}\pm\sigma$ | $\Delta V_r$ | FPR | $\rho_s$ | 判定 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| MR-P1a | P1 | 5×10 | — | — | — | 0 | — | — |
| MR-P1b | P1 | 5×10 | — | — | — | 0 | — | — |
| MR-P2a | P2 | C(5,2)×10 | — | — | — | 0 | — | — |
| MR-P2b | P2 | C(5,2)×10 | — | — | — | 0 | — | — |
| MR-P2c | P2 | 4(Δρ)×10 | — | — | — | 0 | — | — |
| MR-P4a | P4 | 5×10×4 | — | — | — | 0 | — | — |
| MR-P4b | P4 | 5×10 | — | — | — | 0 | — | — |
| MR-P5a | P5 | 3(RT)×10 | — | N/A | N/A | 0 | — | — |
| MR-P5b | P5 | 3(RT)×7(MR)×10 | — | N/A | N/A | 0 | — | — |

**表3：PINN vs TL-PINN 偏序性对比**

| 指标 | RT-2 PINN | RT-2 TL-PINN | RT-3 PINN | RT-3 TL-PINN | RT-4 PINN | RT-4 TL-PINN | P5一致? |
|------|:---------:|:------------:|:---------:|:------------:|:---------:|:------------:|:-------:|
| MAPE (%) | — | — | — | — | — | — | — |
| $\epsilon_{L2}$ | — | — | — | — | — | — | — |
| $R_{closure}$ | — | — | — | — | — | — | — |
| $\bar{V}_r$ (P1-P4均值) | — | — | — | — | — | — | — |
| 训练迭代次数 | 65k | — | 65k | — | — | — | N/A |

---

## P4　新增实验维度

### P4.1　实验E1：违反率-误差相关性分析

**目的**：回答RQ3——蜕变测试的违反模式是否与预测误差相关？

**方法**：

1. 对每个训练运行$s$（$s=1,\ldots,N$），计算该运行的精度指标（$\epsilon_{L2}^{(s)}$）和每条MR的违反情况（通过=0/违反=1）
2. 对每条MR，计算其违反与$\epsilon_{L2}$之间的逐点二列相关系数（point-biserial correlation），或将全部MR的违反计数求和得到"违反严重度评分"$S_{viol}^{(s)} = \sum_{m} \mathbb{1}[\text{MR}_m \text{ violated in run } s]$
3. 计算$S_{viol}$与$\epsilon_{L2}$之间的Spearman秩相关系数$\rho_s$

**实现**：

```python
from scipy.stats import spearmanr, pointbiserialr

def violation_error_correlation(violations_per_run, l2_errors):
    """
    violations_per_run: shape (N_runs,), 每次运行的总违反MR数
    l2_errors: shape (N_runs,), 每次运行的L2相对误差
    """
    rho, p_value = spearmanr(violations_per_run, l2_errors)
    return rho, p_value
```

**预期结果与解读**：

- $\rho_s > 0.5$, $p < 0.05$：强正相关，说明MR违反是预测质量退化的有效指示器
- $\rho_s \approx 0$：无相关性，说明MR违反捕获的是与精度不同维度的问题（物理结构错误 vs 数值逼近不足）
- $\rho_s < 0$：负相关，异常情况，需检查实验设计

两种结果均有论文价值——前者证明蜕变测试的工程诊断能力，后者揭示蜕变测试与精度比对的互补性。

### P4.2　实验E2：蜕变测试作为域外检测器的ROC分析

**目的**：量化蜕变测试在域外检测中的潜在价值。

**方法**：

1. 将MR-P2c的全部测试用例按域内/域外标注真值标签（域内=RT-1至RT-5的参数范围内；域外=超出该范围的$\Delta\rho$方案）
2. 对每个测试用例，计算其"蜕变违反度"（violation score）：一种简单做法是以$R_{closure}$（MR-P1a）或单调性违反的二值指示器作为检测分数
3. 以违反度为阈值扫描变量，以域外标签为正类，绘制ROC曲线并计算AUC

**关键约束**：样本量有限（~9个工况 × 10次运行），ROC分析的统计功效需要在论文中坦诚声明。这是概念验证性质的ROC分析，目的是展示潜在价值，而非给出精确的检测性能估计。

### P4.3　实验E3：统计收敛性分析

**目的**：为"$N$取多少次够用"提供实证数据，指导后续研究和工程实践。

**方法**：

1. 对RT-1方案额外训练至$N=30$次（追加20次，计算量~20分钟）
2. 对$N = 3, 5, 7, 10, 15, 20, 25, 30$，分别计算$\bar{V}_r$和$\sigma_{V_r}$
3. 绘制$\sigma_{V_r}$随$N$的衰减曲线
4. 确定$N^*$（$\sigma_{V_r}$降至$0.01$以下的最小$N$）

**对Survey的价值**：Survey第7.1节建议许可证级应用$N \geq 10$，本实验为这一建议提供实证依据。

### P4.4　实验E4：后验物理残差的空间-时间分布

**目的**：补充原文未做的独立验证通道，建立"训练残差vs后验残差"的比较。

**方法**：

1. 在训练完成后，在5000个均匀时间点上计算后验物理残差$R_n(t)$和$R_{c_i}(t)$
2. 对$N=10$次运行，统计后验残差的均值和标准差随时间的分布
3. 识别后验残差峰值的时间位置——通常对应瞬态的快变区（如反应性翻转点附近）
4. 将后验残差峰值与蜕变测试违反点进行时间位置对比

**实现**：

```python
def compute_posterior_residual(model, params, rho_func, t_eval):
    """计算后验物理残差"""
    import tensorflow as tf
    
    t_tensor = tf.constant(t_eval.reshape(-1, 1), dtype=tf.float32)
    
    with tf.GradientTape(persistent=True) as tape:
        tape.watch(t_tensor)
        y_pred = model.predict(t_tensor)  # shape (N, 7)
    
    # 自动微分求时间导数
    dy_dt = tape.gradient(y_pred, t_tensor)  # shape (N, 7)
    
    n = y_pred[:, 0]
    c = y_pred[:, 1:7]
    dn_dt = dy_dt[:, 0]
    dc_dt = dy_dt[:, 1:7]
    
    # PKE方程1残差
    rho = np.array([rho_func(t) for t in t_eval])
    R_n = np.abs(dn_dt.numpy() - (rho - params['beta_total'])/params['Lambda']*n.numpy()
                 - np.sum(params['lam'] * c.numpy(), axis=1) - params['S'])
    
    # PKE方程2-7残差
    R_c = np.abs(dc_dt.numpy() - params['beta']/params['Lambda']*n.numpy().reshape(-1,1)
                 + params['lam']*c.numpy())
    
    return R_n, R_c
```

---

## P5　论文图表清单

### P5.1　完整图表列表（按出现顺序）

| 编号 | 内容 | 类型 | 回答的RQ | 新增/复用 |
|------|------|------|---------|-----------|
| Fig.1 | PKE-PINN网络架构示意图 + 蜕变测试工作流 | 框架图 | 总览 | 新增 |
| Fig.2 | RT-1至RT-5反应性方案与对应的$n(t)$参考解 | 双子图 | 背景 | 复用（与原文对比呈现） |
| Fig.3 | PINN预测 vs ODE45参考解（N=10均值±σ带） | 对比曲线+误差带 | RQ1前提 | 新增 |
| Fig.4 | 精度复现对比：本文MAPE vs 原文MAPE | 柱状图 | 复现验证 | 新增 |
| Fig.5 | MR-P1a闭合残差$R_{closure}$箱线图 | 箱线图（5组×10点） | RQ1 | 原方案图2 |
| Fig.6 | MR-P1b有效$\hat{\beta}_{eff}(t)$时间演化 | 时间序列+参考线 | RQ1 | 新增 |
| Fig.7 | MR-P2c单调性图：$\hat{n}_{peak}$ vs $\Delta\rho$ | 散点+趋势线+违反标注 | RQ1+RQ2 | 原方案图3（增强） |
| Fig.8 | 容差敏感性曲线$V_r(\alpha)$ | 多曲线图+拐点标注 | RQ2 | 原方案图4 |
| Fig.9 | 域内/域外违反率对比柱状图 | 分组柱状图 | RQ2 | 新增 |
| Fig.10 | 违反度-误差相关性散点图 + Spearman $\rho_s$ | 散点+回归线 | RQ3 | 新增（实验E1） |
| Fig.11 | 蜕变测试域外检测ROC曲线 | ROC曲线+AUC值 | RQ3 | 新增（实验E2） |
| Fig.12 | 统计收敛性：$\sigma_{V_r}$ vs $N$ | 衰减曲线+$N^*$标注 | RQ2 | 新增（实验E3） |
| Fig.13 | 后验物理残差时空分布 | 热力图或带状图 | RQ1补充 | 新增（实验E4） |
| Fig.14 | PINN vs TL-PINN偏序性雷达图 | 雷达图（多指标对比） | RQ1(P5) | 新增 |
| Fig.15 | MR-P4a形态检验示例（通过 vs 违反） | 对比曲线 | RQ1 | 原方案图5 |

| 编号 | 内容 | 回答的RQ |
|------|------|---------|
| Table 1 | PINN精度复现与原文对比 | 复现 |
| Table 2 | 蜕变关系违反率综合结果 | RQ1+RQ2 |
| Table 3 | PINN vs TL-PINN偏序性对比 | RQ1(P5) |
| Table 4 | 容差敏感性拐点汇总 | RQ2 |
| Table 5 | MR设计摘要（蜕变关系×元模式×物理来源） | 方法论 |

---

## P6　论文结构与篇幅规划

### P6.1　建议论文结构（ANE格式，约12—15页）

```
1  Introduction (1.5页)
   1.1  PINN在核工程中的应用与V&V缺口
   1.2  蜕变测试：从传统核软件到ML代理模型
   1.3  本文贡献与结构

2  Background (2页)
   2.1  点堆动力学方程与Prantikos PKE-PINN
   2.2  蜕变测试与蜕变关系元模式
   2.3  ML代理模型蜕变测试的三个特有约束

3  Methodology (3页)
   3.1  蜕变关系设计 (MR-P1a/b, MR-P2a/b/c, MR-P4a/b, MR-P5a/b)
   3.2  统计执行协议 (多运行、违反率定义、容差策略)
   3.3  评价指标体系 (三层指标)
   3.4  实验设置 (DeepXDE配置、计算环境)

4  Results (3—4页)
   4.1  精度复现与原文对比 (Table 1, Fig.3-4)
   4.2  蜕变关系违反率结果 (Table 2, Fig.5-7)
   4.3  ML特有约束的量化影响 (Fig.8-9, Fig.12)
   4.4  PINN vs TL-PINN偏序性 (Table 3, Fig.14)
   4.5  工程诊断价值 (Fig.10-11)
   4.6  后验物理残差分析 (Fig.13)

5  Discussion (2页)
   5.1  RQ1—RQ3回答汇总
   5.2  蜕变测试与传统V&V手段的互补性
   5.3  向其他核工程PINN的推广路径
   5.4  局限性与威胁

6  Conclusion (0.5页)

Appendix A: PUR-1参数完整表
Appendix B: 代码可用性声明
```

### P6.2　与Survey的分工

| 内容 | Survey 6.6.4节 | 独立论文 |
|------|---------------|---------|
| 方法论框架（元模式→MR映射） | 简要引用Survey 6.6.1 | 完整展开Section 3 |
| 实验结果 | 摘要表+1-2幅关键图 | 完整表1—5 + 15幅图 |
| 与原文对比 | 不涉及 | 完整的Table 1 + Fig.3-4 |
| P5偏序性 | 标注为"未覆盖" | 完整实验+Table 3 |
| ROC分析/相关性分析 | 不涉及 | 实验E1+E2 |
| 讨论/局限性 | 2-3句 | 完整Section 5 |

---

## P7　Discussion 框架

### P7.1　五个必须讨论的议题

**议题1：蜕变测试的"无预言机"价值——在哪些场景下优于参考解比对？**

- 当精度比对的参考解不可得时（如新型反应堆设计、超设计基准事故），蜕变测试是唯一可用的V&V手段
- 本实验中，MR-P2c的域外违反率数据正是"无参考解可用的参数区域"中的唯一物理一致性信号
- 对接Survey 6.4节"数据稀缺悖论"

**议题2：容差敏感性拐点的方法论含义**

- 若存在清晰拐点：说明PINN的逼近误差和物理结构违反是可分离的，蜕变测试在该分离点以下具有高特异性
- 若不存在拐点：说明两者耦合，蜕变测试需要与其他V&V手段联合使用
- 讨论$\alpha = 3$的$3\sigma$类比是否在核工程语境下足够保守

**议题3：违反率-误差相关性的工程意义**

- 正相关→蜕变测试可作为模型质量的低成本预筛工具（不需要参考解）
- 不相关→蜕变测试捕获的是"物理结构正确性"这一独立于"数值精度"的V&V维度，两者互补
- 连接到Survey表5（V&V缺口映射表）

**议题4：从PKE-PINN到其他核工程PINN的推广路径**

- P1守恒性→任何基于守恒方程的PINN（中子扩散、热工水力能量守恒）
- P2单调性→任何具有已知参数-输出方向性的核工程问题（吸收截面↑→k_eff↓、流量↑→CHF↑）
- P4轨迹性→任何瞬态PINN（LOHS事故[25]、启停堆瞬态）
- P5偏序性→任何多模型比较场景（PINN vs DeepONet vs FNO）
- 讨论推广中的额外挑战：空间依赖PINN的P3收敛性、高维输入的MR-P2c参数扫描成本

**议题5：局限性（Threats to Validity）**

- **内部有效性**：PKE是简化模型（忽略空间依赖），结论对空间依赖PINN的可转移性未验证；PUR-1参数来自论文而非实验直接测量；反应性方案从图形数字化读取可能引入偏差
- **外部有效性**：仅在一个SUT（PKE-PINN）上的单案例研究，推广到其他PINN架构（CNN-PINN、NA-PINN）和其他物理方程需要更多实证
- **构建有效性**：$\epsilon_{MR}$阈值为经验性设定，缺乏理论推导；容差敏感性分析的拐点识别依赖主观判断
- **统计有效性**：$N=10$的统计功效有限；ROC分析的样本量受限于RT方案数

---

## P8　增量工作量评估

在已有主实验方案 + 补充材料的基础上，升级为独立论文需要的额外工作：

| 新增项 | 额外计算量 | 额外编程量 | 额外写作量 |
|--------|-----------|-----------|-----------|
| P2.2 精度复现对比 | 无（复用已有训练） | ~50行（指标计算脚本） | 0.5页 |
| P2.3 TL-PINN实验（P5） | ~30分钟训练 | ~100行（TL-PINN流程） | 1页 |
| P2.4 后验物理残差 | ~5分钟计算 | ~80行 | 0.5页 |
| P4.1 违反-误差相关性 | 无（复用已有数据） | ~30行 | 0.5页 |
| P4.2 ROC分析 | 无 | ~50行 | 0.5页 |
| P4.3 统计收敛性（N=30） | ~20分钟训练 | ~30行 | 0.5页 |
| 论文写作（引言/背景/方法/讨论） | — | — | 6—8页 |
| 图表制作（15图+5表） | ~3小时 | ~200行可视化 | — |
| **总计** | **~1小时计算** | **~540行代码** | **~10页+图表** |

### 总工时估计（在已有实验基础上）

| 阶段 | 工时 |
|------|------|
| TL-PINN实验 + 统计收敛性追加训练 | 1天 |
| 新增评价指标实现 + 后验残差 | 1天 |
| 相关性分析 + ROC分析 | 0.5天 |
| 全部图表制作 | 2天 |
| 论文写作（英文） | 5—7天 |
| 修改/润色 | 2—3天 |
| **总计** | **约12—14天（在实验完成后）** |

含主实验方案的执行时间（14天），**从零到论文投稿的总工时约4—5周**。

---

## P9　代码开源与可复现性声明

### P9.1　代码仓库结构（升级版）

```
pke-mt-verification/
├── README.md                    # 项目说明 + 快速开始
├── requirements.txt             # 版本锁定的依赖
├── LICENSE                      # MIT License
├── config/
│   ├── pur1_params.yaml
│   ├── rt_schedules.yaml
│   └── experiment_config.yaml
├── src/
│   ├── pke_ode.py               # ODE参考解求解器
│   ├── pke_pinn.py              # DeepXDE PINN实现
│   ├── pke_tl_pinn.py           # TL-PINN实现 [新增]
│   ├── reactivity.py            # 反应性方案加载
│   ├── mr_p1_conservation.py
│   ├── mr_p2_monotonicity.py
│   ├── mr_p4_trajectory.py
│   ├── mr_p5_partial_order.py   # P5偏序性检验 [新增]
│   ├── posterior_residual.py    # 后验物理残差 [新增]
│   ├── correlation_analysis.py  # 违反-误差相关性 [新增]
│   ├── roc_analysis.py          # 域外检测ROC [新增]
│   ├── tolerance_analysis.py
│   └── utils.py
├── scripts/
│   ├── run_all.sh               # 一键运行全部实验
│   ├── run_reference.py
│   ├── run_training.py
│   ├── run_tl_training.py       # TL-PINN训练 [新增]
│   ├── run_mt.py
│   ├── run_analysis.py
│   └── generate_figures.py      # 论文图表生成 [新增]
├── results/                     # .gitignore中排除大文件
└── paper/
    ├── figures/                  # 论文用图（PDF/SVG格式）
    └── tables/                  # 论文用表（LaTeX格式）
```

### P9.2　论文中的可复现性声明

> All code, configuration files, and data analysis scripts used in this study are publicly available at [GitHub URL]. The experimental results can be reproduced using the one-click script `scripts/run_all.sh` on a standard desktop computer (no GPU required) in approximately 4 hours. Random seeds for all training runs are recorded in `experiment_config.yaml` to ensure exact reproducibility.

### P9.3　审稿人友好设计

- **一键复现**：`bash scripts/run_all.sh` 从环境检查到论文图表生成，全自动
- **中间结果检查点**：每个阶段完成后自动输出摘要统计，审稿人可在任意阶段中断检查
- **图表自动生成**：`python scripts/generate_figures.py` 直接生成论文用PDF矢量图
- **预期运行时间标注**：每个脚本开头注释预期耗时
