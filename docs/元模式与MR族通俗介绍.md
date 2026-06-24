# 元模式与 MR 族通俗介绍

> **本文档目的**：用读者无需阅读 NOETHER 论文也能看懂的方式，把 NOETHER 框架的两层结构讲清楚——上层"元模式"（L1）是什么、下层"MR 族"（L2）是什么、两者怎么由最小代数基派生而来，以及拿到一段程序时该怎么用它来判定正确性。
>
> **形式化定义来源**：[`P1-MetaPattern/shared/two_layer_canon.tex`](../../最小完备MR子集/manuscript/shared/two_layer_canon.tex)（canonical SSOT，跨 P-series 共享）。
> **示例参考**：[`docs/historical_notes/MR_MetaPattern_Survey.md`](historical_notes/MR_MetaPattern_Survey.md) §4.4 + §6；实证 MR 数据 [`supplementary/S2_pwr_corpus/pwr_84mr_full.csv`](../supplementary/S2_pwr_corpus/pwr_84mr_full.csv)（PWR 84 条 MR 全量）。
>
> **本文档不引入新结论**，只把已发表/在审的两层结构与 84-MR 实证库整理为入门读物。

---

## §1 元模式的目的：为什么提出，能做什么，意义在哪里

### 1.1 软件测试的"预言机问题"

测试一段计算程序最朴素的做法是：给它一组输入，**事先算出正确答案**，再比对程序输出。能"事先算出正确答案"的那个工具，软件工程界叫**预言机（test oracle）**。

可是反应堆中子输运、机器学习模型、数据库查询优化器——这些程序的预言机往往**根本不存在**：

- 中子分布要解六维 Boltzmann 方程，唯一的"准确解"也是别的程序算出来的
- 神经网络在新输入上"应该"输出什么，没人能闭着眼睛写下来
- SQL 查询优化器对一条 1 000 行的查询"应该"用哪种连接顺序，也没有正确答案

这就是 **oracle problem**。

### 1.2 蜕变测试：用关系替代预言机

蜕变测试（Metamorphic Testing, MT）换了思路：

> 不去问"输入 $x$ 的正确输出是什么"，而是去问"如果把输入做某种改动 $T$，输出**应该**怎么对应改变"。

举个最浅显的例子。`sin(x)` 函数：

- 不知道 `sin(1.2345)` 的正确值是多少？没关系。
- 但你**知道** `sin(x + 2π) = sin(x)`——这是 sin 的周期性。
- 程序如果跑出 `sin(1.2345) ≠ sin(1.2345 + 2π)`，**不管这两个数具体是什么**，程序就一定错了。

这种"对输入做变换 $T$ → 对输出可以预测变化 $T'$"的二元关系，就是**蜕变关系（Metamorphic Relation, MR）**。

### 1.3 但 MR 哪里来？元模式的提出

MT 的瓶颈一直在于：**MR 从哪里来？**——挖一条 MR 需要懂程序所属领域的知识（物理、数学、语言学），还要能把这种直觉写成可执行断言。已有方法多半：

- **人工挖**——依靠资深专家直觉，覆盖窄、不可复现
- **搜索/进化挖**——靠基因编程在表达式空间里乱试，找到的关系往往零碎、没有结构解释
- **LLM 提示挖**——用大模型生成候选，质量受 prompt 工程影响，且无可证伪边界

这些方法的共同短板：**找到的 MR 是"孤儿"**——不知道它属于哪一族、覆盖完没、新程序能不能照猫画虎复用。

NOETHER 框架（即"P1-MetaPattern"项目）的核心主张是：

> **可以从程序所属的方程家族（"算子代数"）出发，演绎地推导出该家族应有的所有 MR；每条具体 MR 都来自少数几条"元模式"。**

这就好比化学：单看上千万个有机分子是杂乱的，但只要回到 C/H/O/N 几个元素 + 几条化学键规则，所有分子就成了"基本元素的组合"。NOETHER 想做的是：把 MR 也分解到这种"元素 + 规则"层级。

### 1.4 能做什么，意义在哪里

提出元模式（L1）+ MR 族（L2）两层结构带来的直接好处：

1. **可枚举的覆盖**：一旦把算子代数分解成最小代数基（5 块），就可逐块检查"这个程序在这块上有没有 MR"——遗漏可见。
2. **可解释的来源**：每条 MR 都能回答"它从哪条代数性质来"，而不是"专家说它对"。
3. **可迁移**：两个程序如果共享同一种代数结构（例如都来自 Boltzmann 输运方程），它们的 MR 族就有共同骨架——一个程序的测试经验可移植到另一个。
4. **可预测**：框架能**预言**前人未挖到的 MR——NOETHER 论文中两条 PWR 预言（伴随互易性 $m_{\mathrm{adj}}$ 与时间反演 $m_{\mathrm{rev}}$）就是用这种方式从代数推导出来的。
5. **可证伪**：若算子代数无某一块结构，元模式空缺成为一条具体的"out-of-scope"主张，可被反例驳斥。

意义可以一句话总结：**把"挖 MR 的工艺"升级为"推导 MR 的理论"**。

---

## §2 最小代数基、L1、L2 的形式化定义与关系

> 本节定义逐字来自 canonical SSOT [`two_layer_canon.tex`](../../最小完备MR子集/manuscript/shared/two_layer_canon.tex)。本文不引入新符号。

### 2.1 最小代数基（program-induced operator algebra）

每一段程序 $P$ 都对应一个**程序诱导算子代数**：

$$
\mathcal{A}_P = (\mathcal{O}, \circ, \sim_{\mathcal{F}})
$$

其中 $\mathcal{O}$ 是程序"可观测"的算子集合（如解算子、迭代算子、估计器算子），$\circ$ 是它们的复合运算，$\sim_{\mathcal{F}}$ 是程序家族 $\mathcal{F}$ 共享的等价关系。

$\mathcal{A}_P$ 的**结构分解**：

$$
\mathcal{D}(\mathcal{A}_P)
$$

是把 $\mathcal{A}_P$ 沿最小代数结构（群作用、偏序、自伴算子等）切分成的**块**集合。这就是"最小代数基"——五类基本块：

| 块符号 | 数学含义 | 直观例子 |
|---|---|---|
| $G$ | 群作用 | 几何对称、坐标置换、能群置换 |
| $O_{\le}$ | 偏序 | 参数→输出的单调依赖、误差界 |
| $T^{*}$ | 自伴算子 | 反应堆的伴随通量、电路的对偶 |
| $\mathcal{T}^{*}_{\mathrm{rev}}$ | 时间反演对合 | 无碰撞情形中子轨迹可倒放 |
| $\mathcal{L}^{*}$ | 参数化极限 | 网格细化→收敛、阶数↑→精度↑ |

这五块就是用户问的"**最小代数基**"。

### 2.2 Layer 1: 元模式（MetaPattern）

> 形式化（[`two_layer_canon.tex`](../../最小完备MR子集/manuscript/shared/two_layer_canon.tex) L40–L46）：
> 元模式是 CONSTRUCT-MP 通过 Translate 从 $\mathcal{A}_P$ 的**一个最小代数结构（生成基）**派生出的所有代数诱导 MR 的**等价类**。

通俗讲：**一个最小代数基对应一个元模式**。五个最小代数基对应五个元模式：

| 元模式符号 | 英文名 | 中文名 | 由哪块代数生成 |
|---|---|---|---|
| $m_{\mathrm{inv}}$ | Invariance | 不变 | 群作用 $G$ |
| $m_{\mathrm{mono}}$ | Monotonicity | 单调 | 偏序 $O_{\le}$ |
| $m_{\mathrm{adj}}$ | Adjoint | 伴随 | 自伴算子 $T^{*}$ |
| $m_{\mathrm{rev}}$ | Reversal | 反演 | 时间反演对合 $\mathcal{T}^{*}_{\mathrm{rev}}$ |
| $m_{\mathrm{conv}}$ | Convergence | 收敛 | 参数化极限 $\mathcal{L}^{*}$ |

整个元模式集合记 $\mathbb{M}(\mathcal{A}_P) = \{m_{\mathrm{inv}}, m_{\mathrm{mono}}, m_{\mathrm{adj}}, m_{\mathrm{rev}}, m_{\mathrm{conv}}\}$。

> $m_{\mathrm{adj}}$ 取名 **Adjoint/伴随**（属概念），**不叫**"自伴"——"自伴"是它的子族（见 §2.3 的 $\mathsf{f}_{\mathrm{adj}.\mathrm{self}}$），父名若同名会和子撞。

### 2.3 Layer 2: MR 族（MR family）

> 形式化（[`two_layer_canon.tex`](../../最小完备MR子集/manuscript/shared/two_layer_canon.tex) L47–L55）：
> MR 族是一个元模式 $m \in \mathbb{M}$ 在**固定 π-template + MR mode（Mode-I 输入轨道 / Mode-M 实现轨道）**下，通过 Translate 实例化得到的**可执行 MR 集合**：$\textsc{Translate}(\iota, s)$，其中 $\iota = (\Phi, \pi)$ 是组件不变式。

通俗讲：**元模式（L1）是抽象骨架，MR 族（L2）是骨架在不同"姿势"下展开的可执行 MR 集**。一个元模式可以展开成多个族（**一对多映射**），每个族再展开成若干条具体 MR。

**MR 族的符号**：无衬线 $\mathsf{f}$ + 点号双段下标 $\mathsf{f}_{\mathrm{父}.\mathrm{子}}$——点前是父元模式的词干（inv/mono/adj/rev/conv），点后是该族的机制标签。看一眼下标点号前就知道它属于哪个元模式。

canonical 文档给出的 L1→L2 映射（10 个族）：

| L1 元模式 | L2 MR 族（符号 · 中文名） |
|---|---|
| $G \to m_{\mathrm{inv}}$ | $\mathsf{f}_{\mathrm{inv}.\mathrm{eqv}}$ 等变(a) · $\mathsf{f}_{\mathrm{inv}.\mathrm{con}}$ 守恒(b) |
| $T^{*} \to m_{\mathrm{adj}}$ | $\mathsf{f}_{\mathrm{adj}.\mathrm{self}}$ 自伴对称(c) · $\mathsf{f}_{\mathrm{adj}.\mathrm{dual}}$ 伴随对偶(d) |
| $\mathcal{T}^{*}_{\mathrm{rev}} \to m_{\mathrm{rev}}$ | $\mathsf{f}_{\mathrm{rev}.\mathrm{traj}}$ 轨迹反演(e) |
| $O_{\le} \to m_{\mathrm{mono}}$ | $\mathsf{f}_{\mathrm{mono}.\mathrm{stat}}$ 静态序(f) · $\mathsf{f}_{\mathrm{mono}.\mathrm{shape}}$ 动态形态(g) |
| $\mathcal{L}^{*} \to m_{\mathrm{conv}}$ | $\mathsf{f}_{\mathrm{conv}.\mathrm{lim}}$ 收敛(h) · $\mathsf{f}_{\mathrm{conv}.\mathrm{rate}}$ 精度阶(i) · $\mathsf{f}_{\mathrm{conv}.\mathrm{repr}}$ 表示不变(j) |

五个元模式总共展开为 **10 个 L2 MR 族**。字母 a–j 为原枚举锚点，保留以兼容旧引用。每个族再对应具体程序上的若干条 MR（见 §3）。

> **三层记号一览**：L1 元模式 斜体 $m_{\text{词干}}$ · L2 MR 族 无衬线 $\mathsf{f}_{\text{父}.\text{子}}$ · L3 可执行 MR 希腊 $\rho_{...}$（论文已用）。词干 adj/mono 在三层都出现（"一词三层面"），靠字体 + 族的点号尾区分；$\mathsf{f}$ 用无衬线以避开正文里斜体的等变分类器 $f(g\cdot x)$。

### 2.4 三者关系图

```
最小代数基  →  L1 元模式      →  L2 MR 族 (𝗳_父.子)              →  可执行 MR（条）
 (5 块)       (5 个 m_*)       (10 个)                            (84 条 PWR 实证)

 G          → m_inv           → 𝗳_inv.eqv 等变, 𝗳_inv.con 守恒        → Bur-Phy-05, ...
 O_≤        → m_mono          → 𝗳_mono.stat 静态序, 𝗳_mono.shape 动态形态 → Dif-Phy-01, ...
 T*         → m_adj           → 𝗳_adj.self 自伴对称, 𝗳_adj.dual 伴随对偶 → Dif-Phy-14, ...
 T*_rev     → m_rev           → 𝗳_rev.traj 轨迹反演                   → (PWR 预言)
 L*         → m_conv          → 𝗳_conv.lim 收敛, 𝗳_conv.rate 精度阶, 𝗳_conv.repr 表示不变 → Bol-Alg-03, ...
```

层级关系本质：

- **代数基** = 程序属于哪种数学结构（属性）
- **L1 元模式** = 在该数学结构下，存在何种"可保持的量"（抽象规则）
- **L2 MR 族** = 在固定的输入扰动模式下，规则展开为什么形态（半具体）
- **可执行 MR** = 在具体程序上，把 L2 进一步落到代码可断言的二元谓词（具体）

---

## §3 L2 示例：来自 PWR 84-MR 实证库的代表性 MR

> 本节每条示例都从 [`supplementary/S2_pwr_corpus/pwr_84mr_full.csv`](../supplementary/S2_pwr_corpus/pwr_84mr_full.csv) 抽取，对应 [`elementwise_12.md`](../supplementary/S2_pwr_corpus/elementwise_12.md) 12 条"代表 MR"中各 L2 族的代表。
> 五个元模式各覆盖 1–2 个 L2 族，共 10 例。每例包含五字段：
>
> 1. **程序介绍**——这段程序解什么方程、属于反应堆物理哪个子领域
> 2. **IR（输入关系）**——对原始输入做何种变换得到"姊妹输入"
> 3. **OR（输出关系）**——程序对两个姊妹输入的输出之间应保持什么关系
> 4. **参数物理 / 数学意义**——MR 涉及的核心参数代表什么物理量
> 5. **怎么用 MR 判定程序正确**——具体到代码层面的判定逻辑

---

### 3.1 m_inv (L1) → 等变 `𝗳_inv.eqv` (L2-a) — Bur-Phy-05 核素排列不变性

**程序介绍。** Bateman 燃耗求解器（burnup solver）。Bateman 方程描述反应堆内**核素浓度**随时间的演化：每种核素由衰变和中子反应产生/消耗，求解器给出某时刻每种核素的密度向量 $\mathbf{N} = (N_1, N_2, \dots, N_n)^T$。$n$ 通常是几百到上千。

**IR（输入关系）。** 取核素索引的任意置换 $\sigma$，把输入向量 $\mathbf{N}_0$ 按 $\sigma$ 重排，反应速率矩阵 $\mathbf{A}$ 的行列同时按 $\sigma$ 重排。

**OR（输出关系）。** 期望输出 $\mathbf{N}(t)$ 也按 $\sigma$ 重排——也就是说，**核素的编号方式与物理无关**，求解器不能因为"我们把 ²³⁵U 编号为 1 还是 100"而给出不同的密度演化。

**参数物理意义。** 核素索引仅是程序内部的存储顺序；反应物理只取决于核素**身份**与反应矩阵元素，与索引顺序无关。

**怎么用 MR 判定程序正确性。**

```
N1, A1 = original_input, original_matrix
sigma = random_permutation(n_nuclides)
N2 = permute(N1, sigma)
A2 = permute_rows_cols(A1, sigma)

result1 = solve_bateman(N1, A1, t)
result2 = solve_bateman(N2, A2, t)

# 判定：把 result2 反置换回原顺序，应当与 result1 数值一致（误差 < 1e-10）
assert max_abs_diff(permute(result2, sigma_inverse), result1) < 1e-10
```

若违反，说明求解器内部有**索引依赖的副作用**（如某些循环只从 0 开始算或硬编码了 ²³⁵U 的特殊位置），是典型的实现错误。

---

### 3.2 m_inv (L1) → 守恒 `𝗳_inv.con` (L2-b) — Bol-Phy-01 功率归一化无关性

**程序介绍。** Boltzmann 中子输运求解器（如 SN、PN、MC、MOC 各类离散方法）。求解器输出**有效增殖因子** $k_{\mathrm{eff}}$——反应堆是否临界的关键量（$k=1$ 临界、$k<1$ 次临界、$k>1$ 超临界）。

**IR（输入关系）。** 把外加源 $S$ 或初始通量 $\phi_0$ 乘以任意正常数 $c > 0$。

**OR（输出关系）。** $k_{\mathrm{eff}}$ **不变**——因为 $k_{\mathrm{eff}}$ 是中子代数比（每一代中子数 / 上一代），与通量绝对量级无关；通量场 $\phi$ 应等比放大 $c$ 倍。

**参数物理意义。** 功率归一化常数 $c$ 是"工程量级单位选择"——满功率、热态零功率、冷态停堆都不改变堆芯几何与材料构成，因此**临界性参数 $k_{\mathrm{eff}}$ 与其无关**。

**怎么用 MR 判定程序正确性。**

```
k1, phi1 = solve_transport(geometry, source=S0)
k2, phi2 = solve_transport(geometry, source=10*S0)

assert abs(k1 - k2) < 1e-8                              # k_eff 不变
assert max_relative_diff(phi2, 10*phi1) < 1e-6          # 通量等比例
```

若 $k_2 \neq k_1$，说明求解器内部把 $k_{\mathrm{eff}}$ 与绝对通量耦合了（如归一化逻辑写错），是常见的归一化 bug。

---

### 3.3 m_mono (L1) → 静态序 `𝗳_mono.stat` (L2-f) — Dif-Phy-01 硼浓度→k_eff 严格单调降

**程序介绍。** 扩散方程求解器（如 NEM、FDM、有限元节块法）。求解二群或多群中子扩散方程，输出 $k_{\mathrm{eff}}$ 与功率分布。压水堆通常往慢化剂中加**可溶硼**作为反应性补偿。

**IR（输入关系）。** 把硼浓度 $C_B$ 增大：$C_B \uparrow$（如从 1200 ppm 增到 1300 ppm，其他参数不变）。

**OR（输出关系）。** $k_{\mathrm{eff}}$ **严格单调下降**：$C_B^{(1)} < C_B^{(2)} \Rightarrow k_{\mathrm{eff}}^{(1)} > k_{\mathrm{eff}}^{(2)}$。

**参数物理意义。** $C_B$ 直接增大**吸收截面** $\Sigma_a$，吸收截面增大→更多中子被吸收→$k_{\mathrm{eff}}$ 必降。这是反应堆物理铁律。

**怎么用 MR 判定程序正确性。**

```
for delta in [50, 100, 150, 200]:  # ppm 步进
    k_low  = solve_diffusion(C_B = 1200)
    k_high = solve_diffusion(C_B = 1200 + delta)
    assert k_high < k_low - 1e-5   # 不仅要降，且降幅可观（非数值噪声）
```

不必知道 $k_{\mathrm{eff}}$ 在 $C_B=1200$ ppm 时的"正确值"，只要它**响应方向**违反单调性，求解器就一定错了。

---

### 3.4 m_mono (L1) → 动态形态 `𝗳_mono.shape` (L2-g) — Bur-Phy-08 碘坑（Iodine Pit）

**程序介绍。** 燃耗 + 短时动力学耦合求解器。处理"反应堆停堆后短时间内中子毒物（¹³⁵Xe）的演化"——这是反应堆安全分析的核心情景之一。

**IR（输入关系）。** 在某稳态运行后，把反应堆功率突降至零（停堆）；在该时刻之后向求解器取多个时间点的功率反应性 $\rho(t)$。

**OR（输出关系）。** $\rho(t)$ 应呈**先降后升**的 "U 形坑" 形态（停堆后约 7–10 小时达坑底，约 30 小时后回升至接近停堆瞬间值）。**这是一条定性的形态关系**，不是单点比较。

**参数物理意义。** ¹³⁵Xe 是强中子毒物（吸收截面 ≈ 2.65×10⁶ barn），停堆瞬间它仍由 ¹³⁵I 衰变产生（产生项不变），但失去了通量燃烧（消耗项归零），导致 ¹³⁵Xe 短时间内**累积**——这就是"碘坑"。物理机制是两阶衰变链 ¹³⁵I → ¹³⁵Xe（6.6 h 半衰期）→ ¹³⁵Cs（9.2 h 半衰期）+ 中子通量燃烧的相对快慢。

**怎么用 MR 判定程序正确性。**

```
rho_series = []
for t in [0, 1h, 3h, 6h, 9h, 12h, 24h, 48h]:
    rho_series.append(solve_kinetics_with_xenon(t_after_shutdown=t))

# 应满足：先单调降，触底，再单调升
trough_idx = argmin(rho_series)
assert 0 < trough_idx < len(rho_series) - 1            # 谷在中段，不在头尾
assert all_decreasing(rho_series[:trough_idx+1])       # 谷之前递减
assert all_increasing(rho_series[trough_idx:])          # 谷之后递增
```

若求解器算出"单调下降到底"或"立刻回升"，¹³⁵I→¹³⁵Xe 链的耦合一定算错了。

---

### 3.5 m_adj (L1) → 自伴对称 `𝗳_adj.self` (L2-c) — Dif-Phy-14 扩散方程自伴随互易性

**程序介绍。** 扩散方程求解器（同 §3.3），但同时支持解**前向通量** $\phi$ 与**伴随通量** $\phi^{\dagger}$（adjoint flux）。伴随通量是反应堆物理中表示"中子重要性"的物理量。

**IR（输入关系）。** 取两个独立的源项 $\mathrm{S}$ 与 $\mathrm{Q}$；用 $\mathrm{S}$ 解前向方程得 $\phi$，用 $\mathrm{Q}$ 解伴随方程得 $\phi^{\dagger}$。

**OR（输出关系）。** 应满足**互易性恒等式**：

$$
\langle \mathrm{S}, \phi^{\dagger} \rangle = \langle \mathrm{Q}, \phi \rangle
$$

即两个内积应当**精确相等**（差异仅为数值离散误差）。

**参数物理意义。** 这是泛函分析里"自伴算子作用与其伴随作用对偶"的标志——若求解器内部矩阵真的是自伴的，互易性恒成立；不自伴则恒不成立。物理上：**"在 $\mathrm{Q}$ 区放探测器、$\mathrm{S}$ 区放源得到的响应" = "把源探测器互换得到的响应"**。

**怎么用 MR 判定程序正确性。**

```
phi_forward = solve_diffusion_forward(source=S)
phi_adjoint = solve_diffusion_adjoint(source=Q)

lhs = inner_product(S, phi_adjoint)
rhs = inner_product(Q, phi_forward)

assert relative_error(lhs, rhs) < 1e-6   # 自伴 + 数值一致
```

若违反，说明求解器要么矩阵不自伴（前/伴随求解器实现不一致），要么数值方法用了不同精度——是非常细致的实现错误，但 MR 一行代码就能曝光。

---

### 3.6 m_adj (L1) → 伴随对偶 `𝗳_adj.dual` (L2-d) — Bol-Phy-03 源-探测器互易性

**程序介绍。** 同 Boltzmann 输运求解器（§3.2），扩展到含外加源 + 探测响应的场景。

**IR（输入关系）。** 在位置 $A$ 放固定强度的中子源 $S_A$、位置 $B$ 放探测器（响应函数 $R_B$）；记录探测响应 $\mathcal{R}_{A \to B}$。互换：把源放 $B$、探测器放 $A$，记录 $\mathcal{R}_{B \to A}$。

**OR（输出关系）。** 应有 $\mathcal{R}_{A \to B} = \mathcal{R}_{B \to A}$（在源强度归一与探测函数归一一致前提下）。

**参数物理意义。** 这是 Boltzmann 输运算子的伴随对偶性在工程量上的实证——源和探测器的位置在数学上是"对称"的角色。物理直觉：屏蔽设计常用此性质做计算简化，把"难算的远场探测"换成"好算的近场源响应"。

**怎么用 MR 判定程序正确性。**

```
R_AB = transport_solver(source_pos=A, source_strength=S0, detector=B)
R_BA = transport_solver(source_pos=B, source_strength=S0, detector=A_as_detector)

assert relative_error(R_AB, R_BA) < 1e-4
```

适用于核辐射屏蔽程序、放射性核素探测响应模拟器。

---

### 3.7 m_rev (L1) → 轨迹反演 `𝗳_rev.traj` (L2-e) — Collisionless reversibility（PWR 上为预言）

**程序介绍。** 中子输运求解器在**纯几何 + 无碰撞**极限下的子模块（也叫 streaming-only mode）——所有截面 $\Sigma_t = 0$，中子在真空中沿直线传播。

**IR（输入关系）。** 取一条中子轨迹 $(\mathbf{r}(t), \mathbf{\Omega}(t))$（位置 + 飞行方向）。时间反演变换：$t \mapsto -t$，$\mathbf{\Omega} \mapsto -\mathbf{\Omega}$（方向取反）。

**OR（输出关系）。** 反演后的轨迹应**沿原路返回**：$\mathbf{r}(-t) = \mathbf{r}_{\mathrm{forward}}(t)$（位置一致），$\mathbf{\Omega}(-t) = -\mathbf{\Omega}_{\mathrm{forward}}(t)$（方向取反）。

**参数物理意义。** 无碰撞 Liouville 方程在时间反演下不变——这是经典力学的可逆性。一旦有碰撞（截面非零），熵增使可逆性破缺。

**怎么用 MR 判定程序正确性。**

```
# 前向：从 (r0, Omega0) 出发，记录 N 步
trajectory_forward = streaming_step(r0, Omega0, n_steps=N)
r_final = trajectory_forward[-1].r
Omega_final = trajectory_forward[-1].Omega

# 反演：从 (r_final, -Omega_final) 出发，应回到 r0
trajectory_back = streaming_step(r_final, -Omega_final, n_steps=N)
r_back = trajectory_back[-1].r

assert max_abs(r_back - r0) < 1e-10
```

PWR 的 prior catalogue 上没有这条 MR（属于 NOETHER 框架**预言**新 MR 的实例）；它揭示了流动模块的几何对称错误（如 ray-tracing 不可逆 step）。

---

### 3.8 m_conv (L1) → 收敛 `𝗳_conv.lim` (L2-h) — Bol-Alg-03 空间网格收敛

**程序介绍。** 任何用空间离散（FDM / FEM / nodal）的中子输运或扩散求解器。求解结果依赖空间网格密度 $h$。

**IR（输入关系）。** 把网格步长 $h$ 不断减半：$h \to h/2 \to h/4 \to \dots$

**OR（输出关系）。** $k_{\mathrm{eff}}(h)$ 与功率分布应**单调收敛**到 $h \to 0$ 的极限值。残差 $|k_{\mathrm{eff}}(h) - k_{\mathrm{eff}}^*|$ 应**有界递减**。

**参数物理意义。** 网格步长 $h$ 是数值离散精度的代理；解算子在加细网格下的极限是连续问题的真解。**有限差分若不收敛，要么离散格式有 bug，要么差分稳定性条件被违反**。

**怎么用 MR 判定程序正确性。**

```
k_vals = []
for h in [0.1, 0.05, 0.025, 0.0125, 0.00625]:
    k_vals.append(solve_transport(mesh_h=h)[0])

# 后一个比前一个更接近极限
diffs = [abs(k_vals[i+1] - k_vals[i]) for i in range(len(k_vals)-1)]
assert all(diffs[i+1] < diffs[i] for i in range(len(diffs)-1))   # 残差严格递减
```

---

### 3.9 m_conv (L1) → 精度阶 `𝗳_conv.rate` (L2-i) — Dif-Alg-01 Diamond-difference $h^2$ 收敛

**程序介绍。** SN 输运方程的 Diamond-Difference (DD) 空间离散格式。文献证明 DD 在光滑解上有 $O(h^2)$ 精度。

**IR（输入关系）。** 同 §3.8（步长减半）。

**OR（输出关系）。** 不仅要求收敛，**还要求残差以 $h^2$ 速率衰减**：

$$
\frac{|k_{\mathrm{eff}}(h) - k_{\mathrm{eff}}^*|}{|k_{\mathrm{eff}}(h/2) - k_{\mathrm{eff}}^*|} \approx 4
$$

（步长减半，误差减为 1/4）

**参数物理意义。** $h^2$ 阶是 DD 格式的**理论精度阶**——若实现正确这个比例必然约 4；若降到 2 或 1，说明 ghost-cell / 边界条件 / 角通量插值的实现 bug 让精度退化。

**怎么用 MR 判定程序正确性。**

```
k_ref = solve_transport(mesh_h=very_fine)            # 当成 truth
ratios = []
for i in range(4):
    h = 0.1 / (2**i)
    err_h    = abs(solve_transport(mesh_h=h) - k_ref)
    err_h2   = abs(solve_transport(mesh_h=h/2) - k_ref)
    ratios.append(err_h / err_h2)

# 比例应稳定在 4 附近（log 阶为 2）
assert all(3.5 < r < 4.5 for r in ratios[-3:])   # 末段渐进
```

这是比 §3.8 更强的判定：不仅要收敛，还要**按理论速率**收敛。

---

### 3.10 m_conv (L1) → 表示不变 `𝗳_conv.repr` (L2-j) — Dif-Alg-05 CMFD 不改变收敛解

**程序介绍。** 扩散方程节块法 + **CMFD**（Coarse Mesh Finite Difference）加速。CMFD 是一种数值加速技巧——它构造一个粗网格 + 等效系数的低阶问题，与高阶（NEM）问题耦合迭代，目的是加快收敛速度但**不改变收敛后的解**。

**IR（输入关系）。** 同一题，两种跑法：(A) 纯 NEM、(B) NEM + CMFD 加速。

**OR（输出关系）。** 两种跑法**收敛后的 $k_{\mathrm{eff}}$ 与功率分布完全相等**（精度仅由收敛准则决定）；CMFD 应当只影响**迭代次数**，不影响最终答案。

**参数物理意义。** CMFD 是预条件子，理论上不引入额外近似——它只是"换一种数学表示来加速"。若 NEM+CMFD 答案不同于纯 NEM，说明 CMFD 系数构造或耦合迭代有 bug。

**怎么用 MR 判定程序正确性。**

```
k_nem,        n_iter_nem        = solve_diffusion(method="NEM",        tol=1e-8)
k_nem_cmfd, n_iter_nem_cmfd = solve_diffusion(method="NEM+CMFD", tol=1e-8)

# 最终答案应等同
assert abs(k_nem - k_nem_cmfd) < 1e-7

# CMFD 应当真的有加速效果（否则 CMFD 实现也有问题）
assert n_iter_nem_cmfd < 0.5 * n_iter_nem
```

这是"表示不变"的精髓：不同**数学表示路径**（直接迭代 vs 预条件加速）解同一个数学问题，必须给出同一答案。

---

## §4 小结：如何把这套理论用到新程序

拿到一段新程序，按以下三步用元模式：

1. **第一步：识别程序所属的算子代数 $\mathcal{A}_P$**。它解什么方程？方程的算子是线性还是非线性？有无群作用、偏序、自伴、时间反演、参数极限？这一步直接决定 $\mathcal{D}(\mathcal{A}_P)$ 含哪几块代数基。
2. **第二步：把代数基映射到元模式集合 $\mathbb{M}(\mathcal{A}_P)$**。每个非空块给一个 L1 元模式。若某块为空，则该元模式**预先证伪为不可达**——这恰恰是 NOETHER 框架"out-of-scope"诚实声明的来源。
3. **第三步：每个元模式按其 L2 一对多映射展开成具体 MR 族**，再实例化为可执行 MR（写一段如 §3 的代码片段）。若 PWR 84-MR 库里已有同结构 MR，可直接迁移作为模板。

整个过程**不依赖预言机**——预言机问题被"在程序内部找可保持的代数性质"替代。这是 MetaPattern 理论的核心贡献。

---

## 进一步阅读

- 形式定义（canonical SSOT）：[`P1-MetaPattern/shared/two_layer_canon.tex`](../../最小完备MR子集/manuscript/shared/two_layer_canon.tex)
- 五元模式 + 派生 family 完整列表：[`MR_MetaPattern_Survey.md`](historical_notes/MR_MetaPattern_Survey.md) §4.4 + §6
- PWR 84-MR 全量实证库（含 source / prior_pattern / block / metapattern / triviality）：[`pwr_84mr_full.csv`](../supplementary/S2_pwr_corpus/pwr_84mr_full.csv)
- 12 条代表 MR + block 子类覆盖：[`elementwise_12.md`](../supplementary/S2_pwr_corpus/elementwise_12.md)
- 84-MR → NOETHER 块的重赋值规则：[`mapping_protocol.md`](../supplementary/S2_pwr_corpus/mapping_protocol.md)
- NOETHER 主稿（含 CONSTRUCT-MP、Translate、IBT 等理论核心）：[`manuscript/NOETHER_paper_arxiv.tex`](../manuscript/NOETHER_paper_arxiv.tex)
