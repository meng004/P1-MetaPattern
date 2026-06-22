# 统一元模式模型：最小代数基 + 派生 MR 族 + 实证覆盖 (2026-06-22)

> 单一权威模型。面向数学物理方程**算子的经典代数性质**，把历史上三套枚举（归纳 5-MP、
> 块分解、实验矩阵）统一为：**5 个顶层元模式（最小代数基生成元）→ 10 个派生 MR 族 →
> 实证覆盖矩阵**。本文为 `COVERAGE_SUMMARY.md` / `B1_INDEX.md` /
> `EQUATION_DRIVEN_EVIDENCE_CHAIN.md` 的术语与分类基准。

## 0. 术语

- **元模式 (MetaPattern) := 最小代数基的生成元**（本模型 5 个：$G,\,T^*,\,\mathcal T^*_{\mathrm{rev}},\,O_{\le},\,\mathcal L^*$）。
- **MR 族 (MR family) := 生成元在具体参数 / 子结构上的实例化（张成）**；族是"测哪些"的操作化分类（覆盖矩阵的行）。
- **实证 MR := 某 SUT 上一条具体的蜕变关系**，是某 MR 族的一个实例（矩阵的格）。

## 1. 形式化符号系统

**载体。** 控制方程把程序族归结为结构化函数空间 $V$（必要时到 $W$）上的算子。PUT 实现理想算子 $L$；实测实现记 $\hat\Phi$，缺陷 $\delta=\hat\Phi-L$。$V$ 携带五种经典结构：群作用、内积配对、单参演化、序锥、范数-离散化。

**元模式。** 二元组 $\mathfrak M=(\mathcal S,\ \mathcal C)$：$\mathcal S$ 为 $V$ 上一种代数结构，$\mathcal C$ 为"理想算子与 $\mathcal S$ 相容"的代数律。

**MR 与检测语义。** MR 是元组上的谓词 $R(\mathbb\Phi;\mathbb x)\in\{\top,\bot\}$，$\mathbb\Phi=\langle\hat\Phi^{(1)},\dots\rangle$ 为实现元组、$\mathbb x$ 为输入元组；理想恒满足 $R[L]=\top$（由 $\mathcal C$ 保证）。
$$R\ \text{FIRED}\iff R[\hat\Phi]=\bot,\qquad R\ \text{HELD}\iff R[\hat\Phi]=\top.$$
实证实例 = 一对发布版本：pre $\hat\Phi^-$ 使 $R=\bot$（FIRED）、post $\hat\Phi^+$ 使 $R=\top$（HELD）。

**Mode（变化轴）。** 同一相容律可在两个轴上测：
- **Mode I（输入轨道，intra-implementation）**：$|\mathbb\Phi|{=}1$，对输入施加结构（$x,\pi(g)x$；加密网；时间反演）。
- **Mode M（实现轨道，inter-implementation）**：$|\mathbb\Phi|{\ge}2$（同一理想 $L$、不同方法 / 表示 / 驱动），$|\mathbb x|{=}1$。**"不同代码实现方法被同一 MR 检出"即 Mode M**。

**目标 fault 类与独立性。** 族 $R_i$ 的目标 fault 类 $\Delta_i=\{\delta:\delta\ \text{破坏}\ R_i\ \text{的律}\}$；由不变性盲性，$R_i$ 恰检出 $\Delta_i$。**独立分辨** $\iff\exists\,\delta^\star\in\Delta_i\setminus\bigcup_{j\ne i}\Delta_j$（唯一检出 witness ⟹ 该族在测试套件中必要）。

## 2. 五个顶层元模式（最小代数基）

**$\mathfrak M_{G}$ — 对称（群作用，含 Noether 守恒）**
$\mathcal S$: 群 $\mathcal G$ 及表示 $\pi_V,\pi_W$。$\mathcal C$: 等变 $L\,\pi_V(g)=\pi_W(g)\,L$；连续子群生成元 $\xi$ 诱导守恒泛函 $Q_\xi$，$Q_\xi(Lu)=Q_\xi(u)$。
*通俗示例*：正方形转 90° 仍是它自己；水分子换朝向能级不变。

**$\mathfrak M_{T^*}$ — 自伴（内积配对）**
$\mathcal S$: 内积 $\langle\cdot,\cdot\rangle$，伴随 $L^*$ 由 $\langle Lu,v\rangle=\langle u,L^*v\rangle$ 定义。$\mathcal C$: 自伴 $L=L^*$（$A=A^\top$）⟹ 谱实、特征向量正交；推广 forward↔adjoint 互易 $\langle L^{-1}s,q\rangle=\langle s,(L^*)^{-1}q\rangle$。
*通俗示例*：城市距离表关于对角线对称（京→沪 = 沪→京）。

**$\mathfrak M_{\mathcal T^*_{\mathrm{rev}}}$ — 时间反演（演化对合）**
$\mathcal S$: 单参演化 $\Phi_t=e^{tL}$，时间反演对合 $\Theta$（$\Theta^2{=}\mathrm{id}$，动量反向）。$\mathcal C$: $\Theta\,\Phi_t\,\Theta=\Phi_{-t}$（$\Phi$ 为群/辛/酉成立；真半群=耗散则破）。
*通俗示例*：无摩擦钟摆视频正放倒放都合物理；有摩擦就不行。

**$\mathfrak M_{O_{\le}}$ — 序/正性（序锥）**
$\mathcal S$: 序锥 $V_+$、偏序 $\le$、线性结构。$\mathcal C$: $L$ 保正 $LV_+\subseteq W_+$、单调 $u\le v\Rightarrow Lu\le Lv$、极大值原理、变分界 $E\ge E_0$、线性叠加；Sturm 比较给轨迹形状不变。
*通俗示例*：温度计越热读数越高、人数永不为负 $-3$。

**$\mathfrak M_{\mathcal L^*}$ — 极限/收敛（范数-离散化）**
$\mathcal S$: 拓扑/范数 + 加密网 $h\to0$ 的离散族 $L_h$。$\mathcal C$（Lax）: 一致 + 稳定 ⟹ 收敛 $\|L_h x-Lx\|\to0$，极限与表示无关。
*通俗示例*：牛顿法算 $\sqrt2$，任何初值都收敛到 $1.41421356\ldots$，收敛后再迭代不动。

## 3. 派生 MR 族（10 个，增强表）

| 族 | 元模式 | Mode | MR 形式 schema | 目标 fault 类 | 独立 witness | 一条实证 SUT MR |
|---|---|---|---|---|---|---|
| **a** G·eqv | $G$ | I | $\hat\Phi(\pi_V(g)x)=\pi_W(g)\hat\Phi(x)$ | 取向/标号/坐标系依赖 | 场被错转但荷守恒、谱正确 → 仅 a 报；openmc rotperiodic 混合 sense 丢粒子 | openmc `normalize`: $\mathrm{norm}(kP){=}\mathrm{norm}(P)$ [3bf1486f4] |
| **b** G·cons | $G$ | I | $Q_\xi(\hat\Phi(x))=Q_\xi(x)$ | 守恒荷泄漏/重复计数 | 电子数错而轨道对称完好 → 仅 b 报；pyscf 14 vs 13 | pyscf `smearing`: $\sum_i\mathrm{occ}_i{=}N_{\mathrm{elec}}$ [ebf4e676] |
| **c** T\*·sa | $T^*$ | I/M | $A{=}A^\top\!\Rightarrow\hat\Phi_{\mathrm{sym}}{=}\hat\Phi_{\mathrm{gen}};\ \mathrm{Im}\,\lambda{=}0;\ H_{ij}{=}H_{ji}$ | 对称算子的非对称处理（虚谱/Hessian 非对称）| 谱虚部对守恒/等变/收敛不可见；scipy eigh driver 谱不一致 | scipy `eigh`: 驱动无关实谱 $\sigma(\hat\Phi_{d_1}){=}\sigma(\hat\Phi_{d_2})$ [178a12572] |
| **d** T\*·dual | $T^*$ | M | $\langle\hat\Phi^{-1}s,q\rangle{=}\langle s,\widehat{(L^*)^{-1}}q\rangle$ | 伴随/重要性误算（错代/源）| 前向解全对而伴随泛函错 → 自伴谱 MR 也不报；openmc IFP β_eff 687→499，k_eff 正常 | openmc `IFP`: 伴随权 β_eff 代际/朝向不变 [767db7e6a] |
| **e** Trev·rec | $\mathcal T^*_{\mathrm{rev}}$ | I | $\hat\Phi_t(\Theta\,\hat\Phi_t x)=\Theta x\ (\pm\varepsilon)$ | 守恒传播子注入不可逆/耗散 | 非辛格式能量近守恒且收敛却不可逆；wave+阻尼 mutant | （in-the-wild $\varnothing$）见证 block_wave mutant FIRED |
| **f** O≤·stat | $O_{\le}$ | I | $u\le v\Rightarrow\hat\Phi u\le\hat\Phi v;\ x\ge0\Rightarrow\hat\Phi x\ge0;\ \hat E\ge E_0$ | 值的序/号违反（负密度、非单调、$E<E_0$）| 总质量守恒但局部负值 → 仅 f 报；openmc CRAM N=−5.8e-2 | scipy `Akima`: 两点保形 $I(\tfrac{x_0+x_1}2){=}\tfrac{y_0+y_1}2$ [ef7437afc] |
| **g** O≤·dyn=𝒟\* | $O_{\le}$ 派生 | I | $Z(\hat\Phi x)\le Z(x)$（振荡/极值/overshoot 有界）| 伪振荡/Gibbs/新增极值 | 数据单调 (f✓) 且收敛 (h✓) 却 Gibbs overshoot → 仅 g 报 | **GAP（B1 未测）** |
| **h** L\*·conv | $\mathcal L^*$ | I | $\hat\Phi_{n+k}x{=}\hat\Phi_n x$（收敛后）/ $\|\hat\Phi_{h_2}{-}\hat\Phi_{h_1}\|\le C\omega(h_1)$ | 不收敛/不一致/自不洽 | 自洽 bug 在对称/正性/守恒 HELD 下发生；scipy LSODA 稠密插值不洽 | scipy `LSODA`: 稠密插值自洽 $\mathrm{sol}(t){=}y$ [c374ca7fd] |
| **i** L\*·acc=ℰ\* | $\mathcal L^*$ 派生 | M | $\|\mathrm{err}(M_2)\|\le\|\mathrm{err}(M_1)\|$（精度阶偏序）| 精度阶退化（声称 4 阶实为 2 阶）| 收敛 (h✓: err→0) 但速率错 (i✗: 以 $h^p$ 退化)；与 h 正交 | **GAP（B1 未测）** |
| **j** L\*·rep | $\mathcal L^*$ 派生 | M | $\hat\Phi^{(r_1)}x=\hat\Phi^{(r_2)}x$（表示/方法精确相等）| 表示/并行分歧（存储/MPI 归约/布局改变结果）| 零容差精确相等，与收敛速率无关；openmc no_reduce 偏 1/n_ranks | openmc `no_reduce`: $\mathrm{flux}(\text{nr}){=}\mathrm{flux}(\text{rd})$ [bd76fc056]、scipy `banded`==full [cb0538877] |

注：`g`=𝒟\*（动态形状）派生自 $O_{\le}$（+ 自伴 Sturm-Liouville）；`i`=ℰ\*（精度阶）、`j`（表示不变）派生自 $\mathcal L^*$。论文 $\mathcal B^*_{\mathrm{rel}}$（关系半环重写）是 `j` 在离散代数上的特例，物理 4 域为空。`j` 在论文 8 块里无干净归宿（ℰ\* 是近似序、$\mathcal B^*_{\mathrm{rel}}$ 是关系代数），是本模型显式补回的操作化族。

## 4. 实证覆盖矩阵（10 族 × 4 论文 SUT 域；n=20 in-scope）

| 元模式 | MR 族 | scipy (pde_num) | pyscf (qchem) | openmc (reactor) | DeepXDE (pde_sciml) |
|---|---|---|---|---|---|
| $\mathfrak M_G$ | a G·eqv | △ fht(谱,边际) | ✓ D2h orbsym | ✓ normalize / rotperiodic | ✓ periodic_point |
| | b G·cons | — | ✓ smearing(电子数) | — | ✓ Neumann(质量) |
| $\mathfrak M_{T^*}$ | c T\*·sa | ✓ eigh / complexsym | ✗ 構造(Fock-Herm) | — | △ Hessian(可达性) |
| | d T\*·dual | — | — | ✓ IFP(β_eff) | — |
| $\mathfrak M_{\mathcal T^*_{\mathrm{rev}}}$ | e Trev·rec | ✗ neg | ✗ neg | ✗ neg | ✗ neg |
| $\mathfrak M_{O_{\le}}$ | f O≤·stat | ✓ Akima(2点线性) | ✗ 構造(占据/变分) | ✓ CRAM(N≥0) | ✓ boundary(float32) |
| | g O≤·dyn(𝒟\*) | **gap** | **gap** | **gap** | **gap** |
| $\mathfrak M_{\mathcal L^*}$ | h L\*·conv | ✓ LSODA | ✓ DIIS | ✓ keff-trigger | ✓ resample |
| | i L\*·acc(ℰ\*) | **gap** | **gap** | **gap** | **gap** |
| | j L\*·rep | ✓ banded(存储) | — | ✓ no_reduce(MPI) | — |

**读出**：5 元模式中 4 个有 in-the-wild 正例（$G/T^*/O_{\le}/\mathcal L^*$），$\mathcal T^*_{\mathrm{rev}}$ 四域全负（仅可导出 + mutant 见证）。10 族中 **7 族有正例**（a,b,c,d,f,h,j）、**1 族结构性负**（e Trev）、**2 族 gap**（g 𝒟\* 形状、i ℰ\* 精度阶）。域内构造负：pyscf c（Fock-Hermitian）、pyscf f（占据/变分界）。

20 个 in-scope 实证缺陷→族分布：a×5(normalize,rotperiodic,periodic,D2h,fht△)、b×2(smearing,Neumann)、c×3(eigh,complexsym,Hessian△)、d×1(IFP)、f×3(Akima,CRAM,boundary)、h×4(LSODA,DIIS,resample,keff)、j×2(banded,no_reduce)。其中 2 个 caveated（fht G 信号边际、forward-Hessian T\* 非默认路径 reachability）。

## 5. Mode-M（同一 MR 检出不同实现方法）的处理

1. **归属**：Mode-M MR 是生成元的实例，不新增生成元。一个 Mode-M 族可检出多对实现方法——它们是**同族多实例**（矩阵同行不同列），非新族。例：`j` 同检 banded≠full（scipy）与 reduce≠no_reduce（openmc），`c` 的 driver-invariance 同检 eigh 不同 LAPACK 驱动。
2. **相对 oracle**：Mode-M 触发只断定 $\hat\Phi^{(1)}\ne\hat\Phi^{(2)}$ 在结构上分歧，**不定位哪侧错**。定位须补：第三方法/参考、必须相等的 control 输入、或 pre/post 版本闭合（fix 指明错侧）。B1 已用：no_reduce 单 rank 无差作 control、版本闭合定位。
3. **形式化**：每实证条目打 Mode 标签（见 §3 列）。Mode-M 族：c(driver)、d、i、j；Mode-I 族：a、b、c(谱)、e、f、g、h。

## 6. 专家 caveat（必须显式声明）

1. **完备性未证**：这是*已知最小基*，非可证完备基。orphan（Lipschitz/度量稳定性收缩）= 候选第 6 生成元；绝对完备性开放。
2. **两种"最小"勿混**：本模型给*最小生成基*（代数无冗余，服务 origin / P4 最小子集存在性）；**不等于最小检测 MR 套件**（给定 mutant 池上的最小覆盖集，是 P4 的独立形式化任务）。同生成元下族（a/b、h/i/j）可同时 FIRED（相关而非独立）。
3. **独立性以 witness 论证**：§3 每族"独立"= 存在唯一检出 witness（故必要），**非穷尽正交性证明**。
4. **生成元→族 一对多且 domain-relative**：哪些族非空取决于 PUT（$\mathcal B^*_{\mathrm{rel}}$ 物理域空、查询优化器非空）。矩阵是域相对覆盖。
5. **$\mathcal T^*_{\mathrm{rev}}$ present-by-derivation**：in-the-wild $=\varnothing$，靠"可导出 + mutant 可证伪"立足，与另 4 个 present-by-instance 不同，须诚实标注。
6. **术语迁移**：论文现稿 "MetaPattern" 在族级（$m_{\mathrm{inv}},\dots$）；采纳本定义须全稿改名（基级=MetaPattern/生成元，族级=MR family），否则两义混淆。
7. **实证缺口**：g（𝒟\* 形状/Sturm）、i（ℰ\* 精度阶）两族 B1 未测——须补真实缺陷或显式标 gap。
