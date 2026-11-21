# 元模式与 MR 族通俗介绍

> **本文档目的**：用读者无需阅读 NOETHER 论文也能看懂的方式，把 NOETHER 框架的层级结构讲清楚——最上游"物理元原理"（L0，本版新增）从哪里来、上层"元模式"（L1）是什么、下层"MR 族"（L2）是什么、各层怎么派生与衔接、各层完备性的根基是什么，以及拿到一段程序（乃至一个全新物理域）时该怎么用它来判定正确性、预测 MR 结构的"占有率指纹"。
>
> **形式化定义来源**：[`P1-MetaPattern/shared/two_layer_canon.tex`](../../最小完备MR子集/manuscript/shared/two_layer_canon.tex)（canonical SSOT，跨 P-series 共享）。
> **示例参考**：[`docs/historical_notes/MR_MetaPattern_Survey.md`](historical_notes/MR_MetaPattern_Survey.md) §4.4 + §6；实证 MR 数据 [`supplementary/S2_pwr_corpus/pwr_84mr_full.csv`](../supplementary/S2_pwr_corpus/pwr_84mr_full.csv)（PWR 84 条 MR 全量）；PWR 物理+热工 99 条推导库《PWR物理与热工MR库报告》与《热工水力MR推导与跨专业差异分析》。
>
> **版本声明**：§1–§3 忠实转述已发表/在审的两层结构（L1/L2 语义以 canon SSOT 为准，本文不改动）；**§2.5（L0 层）、§5（完备性根基）、§6（占有率指纹）、§7（完备性的边界：三定理一假设）为本版新增的扩展提案**，来自 PWR 物理与热工水力两个专业的推导实践，尚未写入 `two_layer_canon.tex`——按 canon 规则，若采纳须同步 NOETHER 正文 `subsec:generator-family`。L0 不改变 L1/L2 的任何定义，只在其上游加一层"来源解释与预测器"。

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

### 2.4 层级关系图（L0 扩展后的全链）

```
L0 物理元原理        →  最小代数基(生成基) →  L1 元模式    →  L2 MR 族 (𝗳_父.子)                →  L3 可执行 MR
(6 条，开放清单)        (5 块，封闭清单)     (5 个 m_*)      (10 个)                              (84+99 条实证)

对称性原理           →  G                 → m_inv        → 𝗳_inv.eqv 等变                       → Bur-Phy-05, EQV-T01…
守恒原理(Noether)    →  G(平凡表示侧)      → m_inv        → 𝗳_inv.con 守恒                       → Bol-Phy-01, CON-T01…
第二定律/耗散单调     →  O_≤ (并杀死T*_rev) → m_mono       → 𝗳_mono.stat 静态序, 𝗳_mono.shape 动态形态 → Dif-Phy-01, SHAPE-T01…
互易原理(Onsager等)  →  T*                → m_adj        → 𝗳_adj.self 自伴对称, 𝗳_adj.dual 伴随对偶 → Dif-Phy-14, SELF-T01…
微观可逆性(Liouville) →  T*_rev            → m_rev        → 𝗳_rev.traj 轨迹反演                   → REV-P01 (PWR 预言)
尺度分离/对应原理     →  L* (+G 缩放侧)     → m_conv       → 𝗳_conv.lim 收敛, 𝗳_conv.rate 精度阶, 𝗳_conv.repr 表示不变 → Bol-Alg-03, LIM-T02…
```

层级关系本质：

- **L0 物理元原理** = 该物理域"世界必须服从什么"（来源；开放、可违背——见 §2.5）
- **代数基（生成基）** = 程序属于哪种数学结构（属性；封闭清单）
- **L1 元模式** = 在该数学结构下，存在何种"可保持的量"（抽象规则）
- **L2 MR 族** = 在固定的输入扰动模式下，规则展开为什么形态（半具体）
- **L3 可执行 MR** = 在具体程序上，把 L2 进一步落到代码可断言的二元谓词（具体）

### 2.5 L0：物理元原理层（扩展提案）

**动机。** 五个生成基不是凭空的数学选择。回看 §2.1 的表格会发现：每一块代数结构背后都站着一条物理学的"元原理"——生成基是元原理投射到程序算子代数上的**影子**。把这层影子来源显式化，就是 L0。

**L0 清单与投影表（影子形态）：**

| L0 物理元原理 | 内容 | 投影到的生成基 | 影子形态（在 PWR 两专业中的实例） |
|---|---|---|---|
| ① 对称性原理 | 物理规律与观察者标架、对象编号、单位选择无关；粒子不可分辨；几何对称 | $G$（非平凡表示侧） | 装载图旋转/镜像等变、核素/通道置换等变、密度-几何缩放 |
| ② 守恒原理 | Noether 对应：连续对称 ↔ 守恒流；计数守恒（核子数、质量、能量） | $G$（平凡表示侧） | 中子平衡闭合、质量/能量平衡、$k_{\mathrm{eff}}$ 对功率归一化不变 |
| ③ 第二定律与耗散结构 | 熵产 $\ge 0$、极值原理、被动性、比较原理 | $O_{\le}$；同时是 $\mathcal{T}^{*}_{\mathrm{rev}}$ 的**破坏者** | 吸收↑→$k$↓、热源↑→温度场逐点↑；两相流/扩散不可倒放 |
| ④ 互易原理 | Onsager 倒易关系、格林函数对称、细致平衡、变分/自伴结构 | $T^{*}$ | 源-探测器互易、扩散互易恒等式、导热源-响应互易 |
| ⑤ 微观可逆性 | Hamilton 力学、Liouville 定理、时间反演对称 | $\mathcal{T}^{*}_{\mathrm{rev}}$ | 无碰撞（$\Sigma_t=0$）中子轨迹可倒放 |
| ⑥ 尺度分离与对应原理 | 模型层级嵌套、渐近极限、量纲齐次/相似律 | $\mathcal{L}^{*}$（相似律亦投影到 $G$ 缩放侧） | 输运→扩散渐近、两流体→单相退化链、$h^2$/$1/\sqrt{N}$ 理论阶 |

**三个立刻可用的解释力：**

1. **块占有率的因果解释**。热工水力的 $m_{\mathrm{adj}}$ 为什么薄？因为其封闭关系（流型图、CHF 关联式）没有 Onsager/变分结构——原理④在该域的方程里没有幸存。物理的 $m_{\mathrm{rev}}$ 为什么活着？因为碰撞项可以参数化关断（$\Sigma_t \to 0$），原理⑤在退化极限中复活。占有率指纹不是偶然统计，是 **L0 原理在各专业方程中的存亡记录**（详见 §6）。
2. **可辩护级别 = 翻译保真度**。同一条 L0 原理翻译成算子性质时的保真度不同：无损翻译（置换协变直接就是定理）→ **定理级**；经守恒积分中转（能量平衡推出的单调）→ **平衡级**；只剩经验拟合曲线的形状在撑（CHF 对流量的方向）→ **关联级**。三级标注度量的正是 L0→L1 的翻译损耗。
3. **条件化结构的来源**。模型可以**违背**原理：六方程两流体模型违背双曲性、经验关联式出标定域即失真。L3 上大量前置条件与负面清单（MTC 需低硼、DNBR 对压力方向不入集）不是工程上的凑合，而是"模型对 L0 原理的背叛记录"——识别 MR 时，每一处已知的原理违背都应转录为一条适用域声明。

**L0 与 L1 的分工（一句话）**：**物理提出，代数裁决**（physics proposes, algebra disposes）。L0 是发现侧的启发器与可辩护性的血统证明；L1/L2 是判定侧的完备性载体与断言语法。L0 为什么不能取代 L1 作完备性基础，见 §5。

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

拿到一段新程序，按以下步骤用元模式（L0 扩展后为四步）：

0. **第零步（L0 盘点，扩展提案）：列出该物理域的 L0 元原理存亡记录**。域的主力方程尊重哪几条元原理？哪几条被耗散杀死、被经验封闭抹掉、被模型近似违背？这一步产出"占有率指纹"的预测（§6），并为第一步的结构判定提供血统证明。
1. **第一步：识别程序所属的算子代数 $\mathcal{A}_P$**。它解什么方程？方程的算子是线性还是非线性？有无群作用、偏序、自伴、时间反演、参数极限？这一步直接决定 $\mathcal{D}(\mathcal{A}_P)$ 含哪几块代数基。
2. **第二步：把代数基映射到元模式集合 $\mathbb{M}(\mathcal{A}_P)$**。每个非空块给一个 L1 元模式。若某块为空，则该元模式**预先证伪为不可达**——这恰恰是 NOETHER 框架"out-of-scope"诚实声明的来源。
3. **第三步：每个元模式按其 L2 一对多映射展开成具体 MR 族**，再实例化为可执行 MR（写一段如 §3 的代码片段）。若 PWR 84-MR 库里已有同结构 MR，可直接迁移作为模板——但注意：可迁移的是 π-template 骨架，可辩护性论证、适用域声明与容差协议须按目标域的 L0 存亡记录重做。

整个过程**不依赖预言机**——预言机问题被"在程序内部找可保持的代数性质"替代。这是 MetaPattern 理论的核心贡献。

---

## §5 各层完备性的根基与联系（扩展提案）

四层结构的完备性不是同一种"完备"。分层剖析其根基，才能知道每一层坏了该修哪里。

### 5.1 L0：开放清单（不完备，也不需要完备）

L0 元原理清单是**开放的**：新物理带来新原理（规范对称、拓扑守恒……），清单随物理学前沿生长。它也**不互斥**（守恒与对称经 Noether 定理本是一体两面）、且**可违背**（模型对原理的背叛是常态：非双曲的六方程模型、出域的经验关联式）。这三条性质决定了 L0 只能当**来源解释器与预测器**，不能当完备性基础——完备性需要封闭分类，L0 给不出。

### 5.2 L1：结构-数学完备（封闭清单）

L1 的完备性根基是：**五个生成基是"算子代数可承载的可保持性质"的结构类穷举**——对称（群作用）、序（偏序）、对偶（自伴/伴随）、对合（时间反演）、极限（参数化收敛）穷尽了"对输入做变换后输出可预测"的代数机制类型。换物理域只是换 $\mathcal{A}_P$ 的算子内容，改变的是各块的占有率与退化程度，**不改变结构类清单**。这是 canon 把 L1 定义在代数结构而非物理现象上的根本用意，也是 §6 指纹预测得以成立的前提。

### 5.3 L2：规范-分类学完备（后果解剖 + 闭合性检验）

L2 的完备性根基与 L1 不同类：它是**每个生成基对程序可观测输入-输出映射 $\mathcal{K}:p\mapsto U$ 的"后果解剖"（consequence anatomy）**——一个代数结构能以几种**不可再合并**的形态约束住 $\mathcal{K}$，每种形态固定一个 π-template（加 MR mode），就是一个族。十族 = 各生成基后果解剖的基数之和 **2+2+2+1+3**：

| 生成基 | 后果解剖 | 剖分依据 | 得族 |
|---|---|---|---|
| $G$ | **表示型二分** | 解算子与群作用对易时，输出泛函在群下只有两种表示行为：按非平凡表示协变（输出跟着变换走），或落在平凡表示上（派生标量不动）。表示论意义上无第三种 | $\mathsf{f}_{\mathrm{inv.eqv}}$ / $\mathsf{f}_{\mathrm{inv.con}}$ |
| $O_{\le}$ | **断言元数二分** | 序约束 I/O 映射只有两个层面：点对层面（两个有序输入的输出保序，二元 π-template）；路径层面（沿扫掠参数的整条响应曲线的序型——单调分段/单峰/S 形，序列级 π-template）。形态断言是序结构在轨道上的高阶表现（导数符号模式），与点对比较不可互相归约 | $\mathsf{f}_{\mathrm{mono.stat}}$ / $\mathsf{f}_{\mathrm{mono.shape}}$ |
| $T^{*}$ | **对合定位二分** | 伴随对合 $*$ 约束系统的方式，要么落在 $*$ 的不动点上（$T=T^{*}$，单算子对称→互易恒等式），要么落在对偶对 $(T,T^{*})$ 的双线性配对恒等式上（源-探测器互换） | $\mathsf{f}_{\mathrm{adj.self}}$ / $\mathsf{f}_{\mathrm{adj.dual}}$ |
| $\mathcal{T}^{*}_{\mathrm{rev}}$ | **后果单型** | 对合只产生一种可断言后果：共轭闭合（轨迹倒放回原点） | $\mathsf{f}_{\mathrm{rev.traj}}$ |
| $\mathcal{L}^{*}$ | **极限解剖三元组** | 分析学里一个极限恰有三件可断言的事：存在且趋近、趋近速度、极限对路径/表示的唯一性。不多不少 | $\mathsf{f}_{\mathrm{conv.lim}}$ / $\mathsf{f}_{\mathrm{conv.rate}}$ / $\mathsf{f}_{\mathrm{conv.repr}}$ |

**认识论上的不对称必须挑明**：L1 完备是**结构-数学性的**（结构类清单封闭）；L2 完备是**规范-分类学性的**——它相对于 canon 选定的 π-template 分类粒度而言完备，canon 自己留了压力阀（八分量深分解中 $\mathcal{D}^{*}$、$\mathcal{E}^{*}$、$\mathcal{B}^{*}_{\mathrm{rel}}$ 作为 g/i/j 族的 refinement/extension）。其完备性证据是**闭合性检验**而非定理：PWR 物理+热工 99 条推导 MR 每条恰落一族、无归属歧义、无落族失败（含热工全部"疑似新族候选"——条件化、定量带、模型退化链——经甄别均为 π-template 修饰或 $\mathcal{L}^{*}$ 定义本身）。**判据**：若第 $n$ 条 MR 无家可归，修的是 L2 清单（经压力阀），不是 L1。

### 5.4 L3：经验完备（覆盖率，永远开放）

L3 只有相对于具体程序、具体输出集的覆盖率概念，随 deck 能力与输出接口生长，无封闭清单可言。

### 5.5 四层联系对 MR 结构的影响（合成图景）

$$\text{L0 决定"哪些块有血统"} \;\Rightarrow\; \text{L1 决定"块清单封闭"} \;\Rightarrow\; \text{L2 决定"每块几种断言语法"} \;\Rightarrow\; \text{L3 决定"断言在此程序上长什么样"}$$

对一条具体 MR 而言：它的**存在性**由 L0 存亡记录裁定（原理死了块就空）；它的**归族**由 L2 后果解剖裁定（协变还是守恒、点对还是形态）；它的**强度**（等式/带状/条件化）由 L0→L1 翻译保真度裁定（定理级/平衡级/关联级）；它的**判定工程**（容差、死区、三态输出）在 $\textsc{Translate}$ 之后的执行侧，不回写代数层。

---

## §6 占有率指纹：预测新物理域的 MR 结构（扩展提案）

### 6.1 定义

一个物理域（或程序家族）的**占有率指纹** = （五生成基的载体厚度向量，十族的非空性/条目密度模式）。已测得的两个标定样本：

- **反应堆物理**：五块全满——线性特征值问题 + 连续/离散对称群 + 天然伴随结构 + 可关断碰撞 + 全套理论阶。
- **热工水力**：三厚两薄——$G$/$O_{\le}$/$\mathcal{L}^{*}$ 厚（守恒、单调、模型退化链），$T^{*}$ 近空（仅导热载体），$\mathcal{T}^{*}_{\mathrm{rev}}$ 稀薄。

指纹的因果来源即 §2.5 解释力 1：它是 **L0 六原理在该域方程中的存亡记录**。

### 6.2 预测流程（五步，全程可证伪）

1. **列方程**：写出目标域的主力方程与封闭方式，区分第一性项与经验项；
2. **判存亡**：对 L0 六条原理逐条判定——存活 / 受限（仅某极限或子模块存活）/ 被耗散杀死 / 被经验封闭抹掉 / 被模型近似违背；
3. **映指纹**：经 §2.5 投影表把存亡记录映射为五块厚薄预测（指纹向量）；
4. **展族级**：经 §5.3 后果解剖把块级预测展开为十族非空性预测；
5. **落地检验**：每个预测厚块给出至少一条候选 L3 MR，每个预测空块写成 out-of-scope 主张——**两个方向都可被反例驳斥**（厚块找不到任何 L3 即预测失败；空块被一条合法 MR 填上即声明作废）。

### 6.3 三个待检验的域预测（作为方法的可证伪承诺）

| 目标域 | L0 存亡关键 | 指纹预测 | 落地候选 / out-of-scope 主张 |
|---|---|---|---|
| **屏蔽与辐射防护**（固定源线性输运） | 原理④互易是该域"看家结构"（CADIS 减方差本身靠伴随通量运转）；线性、无特征值反馈；原理⑤在 streaming 区存活 | $m_{\mathrm{adj}}$ **厚块**（与热工相反）；$m_{\mathrm{mono}}$ 稳（屏蔽厚度→剂量单调）；$m_{\mathrm{rev}}$ 有管道/空腔 streaming 载体；$m_{\mathrm{conv}}$ 全套但 MC 深穿透使 rate 判定要防欠采样假收敛 | 候选：源-探测器互易（$\mathsf{f}_{\mathrm{adj.dual}}$，DUAL-P01 直接迁移）、伴随指导的权窗一致性（$\mathsf{f}_{\mathrm{conv.repr}}$：开/关 CADIS 不改期望值只改方差） |
| **燃料性能/结构力学**（热-力耦合） | 弹性算子自伴 ⇒ 原理④以 **Maxwell–Betti 互功定理**形态存活；蠕变/塑性/损伤不可逆 ⇒ 原理⑤死、原理③厚 | $\mathsf{f}_{\mathrm{adj.self}}$ **非空**（载荷-位移互易 MR 可在 BISON 类程序上直接构造，限线弹性域）；$O_{\le}$ 厚（载荷/温度单调）；$m_{\mathrm{rev}}$ 空（塑性加载路径依赖） | 候选：两点载荷互易 $\delta_{A\to B}=\delta_{B\to A}$；out-of-scope：卸载-再加载轨迹闭合（损伤模型下预先证伪） |
| **严重事故系统程序**（现象学模型集合） | 经验参数模型抹掉原理④；耗散杀死原理⑤；守恒（原理②）与序（原理③）在集总参数层存活；多解风险动摇不动点唯一性 | $G$ 仅剩守恒闭合（等变近零：无几何对称可用）；$O_{\le}$ 厚但几乎全为**关联级**（负面清单预计密集）；$m_{\mathrm{adj}}$ 空；$m_{\mathrm{rev}}$ 空；$\mathsf{f}_{\mathrm{conv.repr}}$ 受多解风险削弱（稳态路径一致 MR 须先证不动点唯一） | 候选：安全壳质能闭合（$\mathsf{f}_{\mathrm{inv.con}}$）、氧化放热↑→升温率↑（$\mathsf{f}_{\mathrm{mono.stat}}$ 条件化）；out-of-scope：任何伴随/反演族条目 |

### 6.4 指纹对 MR 识别工作的反向指导

指纹不只是预测——它直接决定识别策略的资源分配与话语纪律：

1. **厚块深挖，薄块存档**：预测厚块投入 π-template 展开与 deck 设计；预测空块直接写 out-of-scope 主张入档，禁止硬凑（伪 MR 比空缺更伤判定体系）。
2. **级别先于数量**：指纹附带各块的可辩护级别预期（第一性项→定理级，守恒积分→平衡级，经验封闭→关联级）；关联级占比高的域（严重事故）应把负面清单和适用域声明当作与 MR 同等的一等产出。
3. **迁移有边界**：同族 MR 跨域迁移只带 π-template 骨架；论证、适用域、容差按目标域 L0 存亡记录重做（物理的定理级单调迁到热工可能降级为关联级——降级不是失败，是指纹差异的忠实记录）。
4. **指纹本身入库**：每完成一个域，把实测指纹与预测指纹的偏差记录归档——偏差是对 §2.5 投影表的修正信号，这是 L0 层作为"活理论"的更新机制。

---

## §7 完备性的边界：三定理一假设（扩展提案）

> 本节回答一个必然被问到的问题：**这套理论是否穷尽了所有可能的 MR，并且可以证明？** 答案的结构是：绝对穷尽不可能且不可能性可证（T3）；能证的是来源层的相对完备（T1）与产出的可靠性（T2）；机制清单的闭合是可证伪假设而非定理（H1）；工程上应追求的完备是另一个可达靶子——故障检测完备性（§7.6）。记号沿用 §2：解算子 $\mathcal{K}:p\mapsto U$，可观测泛函 $Q$，生成基 $s$，分量不变量 $\iota=(\Phi,\pi)$，实例化 $\textsc{Translate}(\iota,s)$。

### 7.1 问题的精确化

"穷尽所有 MR"有三种不同强度的读法：（i）**绝对读法**——枚举并证明程序 $P$ 的全部真 MR；（ii）**相对读法**——枚举并证明"由既定结构本体经既定语法可导出"的全部 MR；（iii）**工程读法**——构造一个 MR 集，使既定故障模型中的任何缺陷都以给定概率被至少一条 MR 击杀。三种读法的可行性截然不同：（i）不可能，（ii）可证，（iii）在受限设定可证、一般设定可量化。

### 7.2 定理 T3（绝对穷尽的不可能性）

**命题。** 不存在一个递归程序，能枚举某个非平凡数值程序 $P$ 的全部真 MR 并逐条给出证明。

**证明（三根独立的钉子，任一根即足够）。**

*钉子 1（逻辑封闭 → Gödel）。* 真 MR 集对逻辑运算封闭：两条真 MR 的合取是真 MR；把等式 OR 弱化为不等式仍真；输入变换的复合仍真。故"$P$ 的全部真 MR"$=$"解算子 $\mathcal{K}$ 的理论中全部真的 $\Pi_1$ 型全称命题"。穷尽并证明它们等价于给出该理论的完全且递归的公理化；而 $\mathcal{K}$ 的理论解释实数算术（数值程序的语义包含算术），由 Gödel 第一不完备定理，此公理化不存在。$\square$

*钉子 2（成员资格不可判定 → Rice）。* 退一步只问判定问题："给定候选关系 $\rho$，$\rho$ 是否为 $P$ 的真 MR？"这是关于程序的非平凡语义性质，由 Rice 定理对一般程序不可判定；且真 MR 是对无穷输入空间的 $\Pi_1$ 断言，其集合一般非递归可枚举。枚举的前提（成员可判）不成立。$\square$

*钉子 3（数值层的边界模糊）。* 即便数学上为真，离散实现只近似满足：非对称网格合法破坏旋转等变，浮点破坏结合律，封闭分区切换破坏光滑性。"$P$ 的真 MR"必须相对容差协议 $\tau$ 定义，连待穷尽集合的边界都是带状的——穷尽一个无锐利边界的集合在定义层就不成立。$\square$

*注。* 钉子 3 的正面价值在 T2 的推论中兑现：MR 判 fail 的归因必须三叉。

### 7.3 定理 T1（L2 对五生成基的相对完备性）

**命题。** 凡由 $\textsc{Translate}(\iota,s)$、$s\in\{G,\,O_{\le},\,T^{*},\,\mathcal{T}^{*}_{\mathrm{rev}},\,\mathcal{L}^{*}\}$ 导出的 MR，必落入且仅落入十族 $\{\mathsf{f}_{\mathrm{inv.eqv}},\ldots,\mathsf{f}_{\mathrm{conv.repr}}\}$ 之一。

**证明 = 五条后果解剖引理。**

**引理 G（表示型二分）。** 设群 $G$ 作用于输入空间与输出空间，且 $\mathcal{K}\circ g=g\circ\mathcal{K}$。对任一可观测泛函 $Q$，考察 $g$ 在 $Q$ 值域上的诱导作用：要么 $g$ 作用平凡（$Q(\mathcal{K}(g\cdot p))=Q(\mathcal{K}(p))$，守恒断言），要么非平凡（$Q(\mathcal{K}(g\cdot p))=g\cdot Q(\mathcal{K}(p))$，等变断言）。"平凡/非平凡"由排中律穷尽——对有限群与紧群，输出空间按同型分量分解，任一 $Q$ 的像落在平凡分量或非平凡分量的并上，断言按分量拆分后仍归两型。故 $G$ 块的 π-template 恰两种：$\mathsf{f}_{\mathrm{inv.con}}$ 与 $\mathsf{f}_{\mathrm{inv.eqv}}$。$\square$

**引理 O（断言元数二分）。** 偏序结构对 $\mathcal{K}$ 的全部可执行断言，均可归约为"沿可比链上 $\Delta Q$ 的符号模式"：元数 2 的断言（一对可比输入的输出保序）即静态序；元数 $\ge 3$ 的断言刻画符号模式的变化（单调分段、单峰、S 形——即离散导数符号的序列型），且不可归约为若干独立的二元断言（单峰性要求"先正后负且恰变号一次"，是对整条链的联合约束）。元数 1 是单次执行属性，不构成 MR（canon 的 MR 定义要求 $\ge 2$ 次执行的 arity-$k$ π-template）。故 $O_{\le}$ 块恰两族：$\mathsf{f}_{\mathrm{mono.stat}}$（二元）与 $\mathsf{f}_{\mathrm{mono.shape}}$（序列级）。$\square$

**引理 A（对合定位二分）。** 伴随 $*$ 是算子代数上的对合反自同构（$T^{**}=T$）。$*$ 在算子集上的轨道大小只能为 1 或 2：轨道大小 1（$T=T^{*}$，不动点）给出单算子对称性的互易恒等式 $\langle S,\mathcal{K}Q\rangle=\langle Q,\mathcal{K}S\rangle$，即 $\mathsf{f}_{\mathrm{adj.self}}$；轨道大小 2（对偶对 $(T,T^{*})$）给出配对恒等式 $\langle T^{*}\psi,\varphi\rangle=\langle\psi,T\varphi\rangle$ 的工程化（源-探测器互换），即 $\mathsf{f}_{\mathrm{adj.dual}}$。对合的轨道分类无第三种。$\square$

**引理 R（后果单型）。** 时间反演 $R$（$R^2=\mathrm{id}$，$R\,\Phi^{t}R=\Phi^{-t}$）对演化算子可断言的独有内容只有共轭闭合：$\Phi^{t}\circ R\circ\Phi^{t}\circ R=\mathrm{id}$（轨迹倒放回到原点）。$R$ 作为 $\mathbb{Z}_2$ 群元的等变/守恒断言已被引理 G 吸收进 $m_{\mathrm{inv}}$；扣除后 $\mathcal{T}^{*}_{\mathrm{rev}}$ 块的净内容恰一个模板，即 $\mathsf{f}_{\mathrm{rev.traj}}$。$\square$

**引理 L（极限三元组）。** 参数化极限 $\lim_{\varepsilon\to0}\mathcal{K}_\varepsilon=\mathcal{K}^{*}$ 面向**有限次执行**可见证的量只有三类：残差序列（$\|\mathcal{K}_{\varepsilon_{i+1}}-\mathcal{K}_{\varepsilon_i}\|$ 递减→存在且趋近，$\mathsf{f}_{\mathrm{conv.lim}}$）、残差比值（$\approx 2^{p}$→趋近速度，$\mathsf{f}_{\mathrm{conv.rate}}$）、跨路径/跨表示的极限一致（$\mathsf{f}_{\mathrm{conv.repr}}$）。有限样本对一个极限能构造的断言只有值、差、差之比、跨族相等四类，其中"值"是属性（元数 1），高阶比值归约为更高阶的 rate——故恰三族。$\square$

**合成。** $2+2+2+1+3=10$。T1 的完备性是**构造-定义性的**：相对于（i）五块结构本体（其闭合即 H1）与（ii）canon 选定的 π-template 语法（其压力阀为八分量深分解的 $\mathcal{D}^{*},\mathcal{E}^{*},\mathcal{B}^{*}_{\mathrm{rel}}$）。$\blacksquare$

### 7.4 定理 T2（Translate 产出的可靠性，soundness）

**命题。** 设（P1）连续问题确有结构 $s$（L0 血统成立且未被模型近似违背），（P2）离散格式保持 $s$，或以可量化的方式破坏之（破缺项 $\le$ 容差协议 $\tau$ 的裕量）。则 $\textsc{Translate}(\iota,s)$ 产出的关系在程序上以容差 $\tau$ 为真 MR。

**证明骨架（交换图论证）。** 以等变为例：设 $\mathcal{K}_h=\mathcal{K}+E_h$，$\|E_h\|=O(h^{p})$。若格式严格保结构（如置换：离散方程对指标重排逐位协变），则 $\mathcal{K}_h\circ g=g\circ\mathcal{K}_h$ 精确成立，MR 在机器精度为真；若格式近似保结构（如旋转作用在非对称网格上），则 $\|\mathcal{K}_h(g\cdot p)-g\cdot\mathcal{K}_h(p)\|\le C\,h^{p}$，取 $\tau\ge C h^{p}$ 即真。序与极限类同理（离散极值原理、离散守恒格式分别承接 $O_{\le}$ 与守恒断言）。$\square$

**推论（三叉归因，判定协议的理论依据）。** MR 判 fail 时逻辑上恰有三种互斥归因：**代码缺陷**（P1、P2 成立而断言违反）／**格式合法破缺**（P2 不成立：非保结构格式，如非对称网格破坏旋转等变——修的是 MR 适用域或换保结构格式，不是代码）／**适用域外**（P1 不成立：前置条件未满足，如高硼下考 MTC 负号）。这正是三态判定（pass/fail/适用域外）与"每条 MR 强制适用域声明"的定理级依据。

### 7.5 假设 H1（五块闭合假设）

**命题（不可证，只可证伪）。** 五个生成基穷尽了"对输入做变换后输出可预测"的结构性机制。

**为何不可证**：'机制'没有先验封闭定义——若把机制形式化为"作用于 $\mathcal{K}$ 之图像的变换范畴"，其对象类无界。**其认识论地位**是自然科学式核心假设：证据为语料闭合检验（84 条 PWR 语料 + 99 条物理/热工推导库，每条恰落一族、无归属歧义、无落族失败；含热工全部"疑似新族候选"——条件化、定量带、模型退化链——经甄别均为 π-template 修饰或 $\mathcal{L}^{*}$ 定义本身，见《热工水力MR推导与跨专业差异分析》§2）。**证伪协议**：孤儿 MR（无家可归的可辩护关系）一旦出现 → 经 canon 压力阀修订 L2（refinement/extension 块），若孤儿源于全新变换机制则修订 L1 清单并同步 NOETHER 正文。canon 设计者对此早有自觉——五块规范模型从未被当作定理，八分量深分解就是预置的修订接口。

### 7.6 工程靶：故障检测完备性（可达且部分可证）

绝对穷尽既不可能，工程上真正需要的完备是另一个概念——项目名"最小完备MR子集"中的"完备"应精确化为：

**定义（$(1-\varepsilon)$-故障检测完备）。** MR 集 $S$ 相对三元组 $(\mathcal{F},O,\tau)$——故障模型 $\mathcal{F}$（变异算子类/缺陷模式库）、可观测输出集 $O$、容差协议 $\tau$——是 $(1-\varepsilon)$-完备的，若
$$\forall f\in\mathcal{F}:\quad \Pr\big[\exists\,\rho\in S:\ \rho\ \text{在}\ P_f\ \text{上判 fail}\big]\ \ge\ 1-\varepsilon .$$

**受限设定的可证实例（Freivalds 式）。** 设程序族为线性解算子，$\mathcal{F}=\{\mathcal{K}\mapsto\mathcal{K}+E:\ E\neq0\ \text{且}\ E\ \text{破坏至少一个已编目结构}\}$。取随机化结构检验（随机输入上的等变/叠加/互易断言），则单次检验击杀任一 $f\in\mathcal{F}$ 的概率 $\ge 1/2$（违反集是非零多项式的零点补集，Schwartz–Zippel 式论证），$k$ 次独立检验的漏检率 $\le 2^{-k}$。**一般设定**（非线性+经验封闭）无此定理，改为量化承诺：以变异测试实测击杀率替代证明，《PWR物理与热工MR库报告》§3.4 的"缺陷模式→MR 针对性矩阵"即 $\mathcal{F}\to S$ 覆盖表的雏形。

**盲区定理（必须诚实陈述的对偶面）。** 与 $S$ 所检验的全部结构对易的缺陷，$S$ 原理上不可见（例：对所有输出施加同一系统性标定偏移，可通过全部等变/守恒/单调检验）。这不是 $S$ 的缺陷而是 MR 测试的本质边界，也正是 $(\mathcal{F},O,\tau)$ 三元组必须显式声明的原因——完备性永远相对于故障模型，正如覆盖率永远相对于覆盖准则。盲区内的缺陷须由 MR 之外的手段（基准题定标、不确定性量化）承接。

### 7.7 一句话总结

**绝对穷尽：不可能，且不可能性可证（T3）；相对穷尽：来源层可证完备（T1）、产出可证可靠（T2）、机制清单闭合为可证伪假设（H1）；工程完备：追故障检测完备性——受限设定可证，一般设定可量化，盲区显式入档。** 理论的贡献不是承诺穷尽 MR，而是把"穷尽"从不可达的命题空间搬进可检验的机制空间——如同化学不穷尽分子而穷尽元素与键规则。

---

## 进一步阅读

- 形式定义（canonical SSOT）：[`P1-MetaPattern/shared/two_layer_canon.tex`](../../最小完备MR子集/manuscript/shared/two_layer_canon.tex)
- PWR 物理+热工 99 条推导库（含结构性空缺声明与勘误记录）：《PWR物理与热工MR库报告》
- 热工水力逐生成基推导、L1/L2 无新增的根因、跨专业差异七原则：《热工水力MR推导与跨专业差异分析》
- 五个专业的方程/方法/缺陷背景：《PWR研究背景概论》
- 五元模式 + 派生 family 完整列表：[`MR_MetaPattern_Survey.md`](historical_notes/MR_MetaPattern_Survey.md) §4.4 + §6
- PWR 84-MR 全量实证库（含 source / prior_pattern / block / metapattern / triviality）：[`pwr_84mr_full.csv`](../supplementary/S2_pwr_corpus/pwr_84mr_full.csv)
- 12 条代表 MR + block 子类覆盖：[`elementwise_12.md`](../supplementary/S2_pwr_corpus/elementwise_12.md)
- 84-MR → NOETHER 块的重赋值规则：[`mapping_protocol.md`](../supplementary/S2_pwr_corpus/mapping_protocol.md)
- NOETHER 主稿（含 CONSTRUCT-MP、Translate、IBT 等理论核心）：[`manuscript/NOETHER_paper_arxiv.tex`](../manuscript/NOETHER_paper_arxiv.tex)
