# 两层模型规范定义（NOETHER / P-series 单一真源）

> **权威源**：`P1-MetaPattern/shared/two_layer_canon.tex`（LaTeX 宏 + `\TwoLayerModel` 段落）。
> 其他论文一律 `\input` 该片段、复用其符号宏，**不要各自重定义**，以统一语义。
> 术语锁定：**MR = metamorphic relation = 蜕变关系**；**MetaPattern = 元模式**；**MR family = 蜕变关系族**。禁用同义词（如 generator blocks）。

## 一、说明

把"程序 → 蜕变关系（MR）"分两层：

- **L1 元模式（MetaPattern）**：程序诱导算子代数 $\mathcal{A}_P$ 中，**每个最小代数结构（生成基）所生成的一类 MR 的等价类**。共 **5 个**，由五种最小代数结构生成：**群作用 / 偏序 / 自伴算子 / 时间反演对合 / 参数化极限**。
  （元模式 = "由该结构生成的 MR 等价类" $m_\bullet$；结构本身称"生成基"，二者一一对应。）
- **L2 蜕变关系族（MR family）**：把某元模式的**分量不变量**在**固定 π-template + 选定 MR mode** 下经 **Translate** 实例化得到的**一族可执行蜕变关系**。共 **10 族（a–j）**；一个元模式可生成多族（一对多）。

**关系链**：最小代数结构 $s$ → (CONSTRUCT-MP / Translate) → 元模式 $m_s$（L1）→ (固定 π-template + MR mode) → 蜕变关系族（L2）→ (取具体输入) → 可执行蜕变关系。

## 二、符号表

| 符号 | 含义 |
|---|---|
| $\mathcal{A}_P=(\mathcal{O},\circ,\sim_{\mathcal{F}})$ | 程序诱导算子代数 |
| $\mathcal{D}(\mathcal{A}_P)$ | 结构分解（8 分量：5 元模式 + 2 refinement $\mathcal{D}^*,\mathcal{E}^*$ + 1 relational extension $\mathcal{B}^*_{\mathrm{rel}}$）|
| $G,\ O_{\le},\ T^{*},\ \mathcal{T}^{*}_{\mathrm{rev}},\ \mathcal{L}^{*}$ | 5 个生成结构：群作用 / 偏序 / 自伴算子 / 时间反演对合 / 参数化极限 |
| $m_{\mathrm{inv}},m_{\mathrm{mono}},m_{\mathrm{adj}},m_{\mathrm{rev}},m_{\mathrm{conv}}$ | 5 个元模式（各结构生成的 MR 等价类）|
| $\mathsf{f}_{\mathrm{父}.\mathrm{子}}$ | L2 蜕变关系族符号（无衬线 $\mathsf{f}$，点号双段下标：点前=父 L1 词干，点后=机制标签）|
| $\mathbb{M}(\mathcal{A}_P)$ | 元模式集合（L1）|
| $\iota=(\Phi,\pi)$ | 分量不变量：$\Phi\subseteq s$ 算子集，$\pi$ 为 arity-$k$ 的 π-template |
| $\textsc{Translate}(\iota,s)$ | 把分量不变量实例化为可执行蜕变关系 |
| $\mathrm{MR}(\mathcal{A}_P)$ | $\mathcal{A}_P$ 诱导的蜕变关系集合 |
| MR mode $\in\{\mathrm{I},\mathrm{M}\}$ | Mode-I 输入轨道（固定实现、变输入）；Mode-M 实现轨道（固定输入、变实现）|

## 三、命名规范（三层符号 + 中英文名）

### L1 元模式（5 个，符号沿用 canon，名字锁定）

| 符号 | 英文名 | 中文名 | 生成块 |
|---|---|---|---|
| $m_{\mathrm{inv}}$ | Invariance | 不变 | 群作用 $G$ |
| $m_{\mathrm{mono}}$ | Monotonicity | 单调 | 偏序 $O_{\le}$ |
| $m_{\mathrm{adj}}$ | Adjoint | 伴随 | 自伴算子 $T^{*}$ |
| $m_{\mathrm{rev}}$ | Reversal | 反演 | 时间反演对合 $\mathcal{T}^{*}_{\mathrm{rev}}$ |
| $m_{\mathrm{conv}}$ | Convergence | 收敛 | 参数化极限 $\mathcal{L}^{*}$ |

> $m_{\mathrm{adj}}$ 命名为 **Adjoint/伴随**（属概念），**不叫**"自伴/self-adjoint"——后者是其子族 c，父名若同名则与子撞。

### L2 蜕变关系族（10 个，新增符号，按父分组）

| 父 (L1) | 族符号 | 英文名 | 中文名 |
|---|---|---|---|
| $m_{\mathrm{inv}}$ | $\mathsf{f}_{\mathrm{inv}.\mathrm{eqv}}$ (a) | Equivariance | 等变 |
| $m_{\mathrm{inv}}$ | $\mathsf{f}_{\mathrm{inv}.\mathrm{con}}$ (b) | Conservation | 守恒 |
| $m_{\mathrm{adj}}$ | $\mathsf{f}_{\mathrm{adj}.\mathrm{self}}$ (c) | Self-adjoint | 自伴对称 |
| $m_{\mathrm{adj}}$ | $\mathsf{f}_{\mathrm{adj}.\mathrm{dual}}$ (d) | Adjoint duality | 伴随对偶 |
| $m_{\mathrm{rev}}$ | $\mathsf{f}_{\mathrm{rev}.\mathrm{traj}}$ (e) | Trajectory reversal | 轨迹反演 |
| $m_{\mathrm{mono}}$ | $\mathsf{f}_{\mathrm{mono}.\mathrm{stat}}$ (f) | Static order | 静态序 |
| $m_{\mathrm{mono}}$ | $\mathsf{f}_{\mathrm{mono}.\mathrm{shape}}$ (g) | Dynamic shape | 动态形态 |
| $m_{\mathrm{conv}}$ | $\mathsf{f}_{\mathrm{conv}.\mathrm{lim}}$ (h) | Convergence | 收敛 |
| $m_{\mathrm{conv}}$ | $\mathsf{f}_{\mathrm{conv}.\mathrm{rate}}$ (i) | Accuracy order | 精度阶 |
| $m_{\mathrm{conv}}$ | $\mathsf{f}_{\mathrm{conv}.\mathrm{repr}}$ (j) | Representation invariance | 表示不变 |

> 字母 a–j 为原枚举锚点，保留以兼容旧引用（如 S2 语料、lay 文档）。
> 三层记号：L1 斜体 $m_{\text{词干}}$ · L2 无衬线 $\mathsf{f}_{\text{父}.\text{子}}$ · L3 可执行 MR 希腊 $\rho_{...}$。词干 adj/mono 在三层都出现（"一词三层面"），靠字体 + 族的点号尾区分。
> 注：更深的 8 分量分解里，g 关联 $\mathcal{D}^*$、i 关联 $\mathcal{E}^*$、j 关联 $\mathcal{B}^*_{\mathrm{rel}}$ 等 refinement/extension 块；在 5-元模式规范模型中它们作为 $m_{\mathrm{mono}}$/$m_{\mathrm{conv}}$ 的子族列出。

## 四、各论文如何复用

1. 预导言：`\input{shared/two_layer_canon.tex}`（定义符号宏 + `\TwoLayerModel`，clash-safe）。
2. 正文需要定义段处：`\TwoLayerModel`。
3. 复用符号宏（`\minv`、`\MM`、`\Trev` 等），不要自造同义符号/术语。
4. 引用口径示例：「we adopt the two-layer model of [NOETHER]: five MetaPatterns $\mathbb{M}(\mathcal{A}_P)$ (L1) and their MR families (L2)」。

> 与 NOETHER 正文一致性锚点：概念定义（元模式=MR 等价类）、五结构名（群作用/偏序/自伴/时间反演对合/参数化极限）、L2=Translate 实例化。改动本规范须同步 NOETHER 正文 `subsec:generator-family`。
