# Invariance-Blindness Theorem — tight G-block proof + cross-block schema (招1)

> Status: **立为定理**(作者已定方向:G 块做紧证明,跨块作 schema)。本文给出
> faithfulness 假设 + G 块双向紧证明 + advdiff worked check + 跨块模板。
> 仍为 `docs/` 草稿,**未进正文**(正文待 P0 的 CONSTRUCT-MP Step3/4 抉择后再写)。
> `[需作者数学判断]` 标注尚需作者核验之处。实证支撑:`supplementary/S10_noether_homefield/`。

---

## 0. 与 Theorem 1 的区别(为何非平凡)

Theorem 1(closure under `Translate`)是 **by-construction**:构造不漏构造能达到的
MR。它不陈述关于世界的任何事。IBT 是 **limiting characterization**:在算子可表达
故障类内,equivariance MR 的检测核 = *恰好* 那些保持对称的故障;**且有限可执行 MR
即可达到这一紧刻画**(因故障参数空间有限维,§2 可达性引理)。后半句是真正的内容——
非平凡、可证伪、已实证——它正面回答"你的理论平凡吗":Thm 1 是恒真,IBT 不是。

---

## 0.5 Scope 与假设(审稿 R1–R4,投稿前硬性;`ibt_reviewer_assessment.md`)

本定理在以下显式假设内成立,**正文不得外推**:

- **R1(故障类线性)**:定理针对**线性 operator-implementation 故障类** $\Theta=\mathbb{R}^{N\times N}$
  (或非线性 solver 的一阶线化子类);**不外推到任意非线性故障**。
- **R2(精确算术 vs 容差)**:Def 检测为精确算术;可执行 MR 用容差 $\tau$,执行核
  $\ker_\tau\supseteq\ker$,低于 $\tau$ 的破对称故障假阴。本定理给的是 $\tau\to0$ 的**极限核**,
  与 §10.2 detectability-floor 交叉引用。
- **R3(单块)**:仅 **$G$ 块**已证;$O_\le/T^{*}/\mathcal{T}^{*}_{\mathrm{rev}}$ 作 schema(§5),
  $\mathcal{L}^{*}$ 因 Richardson 比对 $\theta$ 非线性而**不**自动满足 $E_s$ 线性,需限子类或仅留充分方向。
- **R-a(可达性 ≠ 已忠实)**:Reachability 引理仅保证"**存在**忠实有限测试",不保证"作者所写
  MR 忠实";后者须 per-instance FA rank 检验(`fa_rank_check.py`)。
- **R-b**:"$\dim\Theta<\infty$"是前提;无限维算子族下引理失效。
- **R4($\supseteq$ 平凡)**:充分方向($T_s$-相容 ⟹ 漏检)是定义级;贡献归于 $\subseteq$ 方向 +
  Reachability + 紧刻画,**如实陈述**。

---

## 1. 故障参数空间与缺陷泛函(reusing paper §3.1)

- 程序 $P:\mathcal{X}\to\mathcal{Y}$,族 $\mathcal{F}$,算子代数 $\mathcal{A}_P$。
- **故障模型(算子可表达)**:真程序 $P=P_{\theta^*}$,参数 $\theta^*\in\Theta$,其中
  $\Theta$ 是**有限维**参数空间(算子系数 / 谱 symbol / stencil 项)。变异体 $P_\theta$,
  $\theta\ne\theta^*$。这正是论文与 S10 实验采用的 operator-implementation 故障,**不是**
  任意函数扰动——这一限制是 IBT 紧性成立的关键,且与实验一致。
- 块 $s$ 的结构 $T_s$ 配 equivariance MR $\rho_{\iota,s}=\texttt{Translate}(\iota,s)$,
  对应**缺陷泛函** $E_s(\theta;w)$,见证 $w$ 取遍见证集。对 $s=G$:
  $$E_G(\theta;g,x)\ =\ P_\theta(g\cdot x)-\rho(g)\,P_\theta(x),\qquad w=(g,x).$$
- $P_\theta$ 尊重 $T_s$(**$T_s$-compatible**)$\iff E_s(\theta;w)=0\ \forall w\in W_s^{\mathrm{full}}$
  (全体见证;对 $G$ 即 $\forall g\in G_\iota,\forall x$)。
- 可执行 MR 只测**有限**见证 $W_s^{\mathrm{test}}\subseteq W_s^{\mathrm{full}}$;
  $\rho_{\iota,s}$ 在 $P_\theta$ 上 **pass** $\iff E_s(\theta;w)=0\ \forall w\in W_s^{\mathrm{test}}$。
- **检测核** $\ker(\rho_{\iota,s}):=\{\theta:\rho\ \text{pass}\}=\{\theta:E_s(\theta;\cdot)=0\ \text{on}\ W_s^{\mathrm{test}}\}$。

---

## 2. Faithfulness 假设(可检验)+ 可达性引理

设 $E_s(\theta;w)$ 对 $\theta$ **仿射**(affine);记 $a_w:=\partial_\theta E_s(\cdot;w)\in\Theta^{*}$。
- 全条件解集 $K^{\mathrm{full}}=\{\theta:E_s(\theta;w)=0\ \forall w\in W_s^{\mathrm{full}}\}$($=T_s$-compatible 集),
- 测试条件解集 $K^{\mathrm{test}}=\{\theta:E_s(\theta;w)=0\ \forall w\in W_s^{\mathrm{test}}\}$($=\ker$)。

> **(FA) Faithfulness.** 测试见证 $W_s^{\mathrm{test}}$ 对故障类 $\Theta$ **unisolvent**:
> $K^{\mathrm{test}}=K^{\mathrm{full}}$,等价地
> $\mathrm{span}\{a_w:w\in W_s^{\mathrm{test}}\}=\mathrm{span}\{a_w:w\in W_s^{\mathrm{full}}\}\subseteq\Theta^{*}$。

> **可达性引理(Reachability).** 若 $\Theta$ 有限维且 $E_s$ 对 $\theta$ 仿射,则**存在
> 有限** $W_s^{\mathrm{test}}$ 使 FA 成立。
>
> *证.* $V_{\mathrm{full}}:=\mathrm{span}\{a_w:w\in W^{\mathrm{full}}\}\subseteq\Theta^{*}$ 是有限维
> 对偶空间的子空间,故有限维;取其一组基对应的有限见证 $W^{\mathrm{test}}$,则
> $\mathrm{span}\{a_w:w\in W^{\mathrm{test}}\}=V_{\mathrm{full}}$;又 $W^{\mathrm{test}}\subseteq W^{\mathrm{full}}$ 保证
> 截距 $b_w$ 一致,故 $K^{\mathrm{test}}=K^{\mathrm{full}}$。$\square$

**这条引理是 IBT 的真正非平凡核**:紧性不是恒真,而是"**有限故障维 ⇒ 有限可执行
MR 足以精确刻画盲区**"。FA 本身可检(对见证设计做有限线代 rank 检验)。

---

## 3. 定理(G 块,紧)

> **Theorem IBT-G (Invariance-Blindness, symmetry block, tight).**
> 故障类为算子可表达 $\theta\in\Theta$(有限维);equivariance 缺陷 $E_G$ 对 $\theta$
> 仿射;测试 $W_G^{\mathrm{test}}$ 满足 FA。则
> $$\ker(\rho_{\iota,G})\ =\ K^{\mathrm{full}}\ =\ \{\theta:\ P_\theta\ \text{是}\ G_\iota\text{-equivariant}\}.$$
> 即:算子可表达故障通过 equivariance MR **当且仅当**它保持对称 $G_\iota$。

**证明.**
- ($\supseteq$,充分)$\theta\in K^{\mathrm{full}}\Rightarrow E_G(\theta;\cdot)=0$ on $W^{\mathrm{full}}\supseteq W^{\mathrm{test}}\Rightarrow\theta\in\ker$。
- ($\subseteq$,必要)$\theta\in\ker\Rightarrow E_G(\theta;\cdot)=0$ on $W^{\mathrm{test}}$;由 FA $K^{\mathrm{test}}=K^{\mathrm{full}}$,故 $\theta\in K^{\mathrm{full}}$。$\square$

> **推论 IBT-1(单块不完备).** $\ker(\rho_{\iota,G})\supsetneq\{\theta^{*}\}$ 当且仅当存在
> 非平凡保对称故障;此时单块 equivariance battery 必漏该故障,结构性不完备。

---

## 4. $E_G$ 仿射的条件 + advdiff worked check

- **仿射条件**:当群作用 $g\cdot(-)$ 与表示 $\rho(g)$ 线性,且 $P_\theta$ 对 $\theta$ 仿射
  (线性 PDE:参数进入线性算子,$P_\theta=A(\theta)^{-1}f$ 在参数一阶展开;或参数本身仿射
  进入解),则 $E_G(\theta;g,x)=P_\theta(g\cdot x)-\rho(g)P_\theta(x)$ 对 $\theta$ 仿射。
  **[需作者]** 非线性 solver 取一阶线化,或限制到参数仿射子类(范围声明)。
- **advdiff(平移 / Galilean $G$)worked check**:常系数 advection $c\cdot\nabla$ + diffusion
  $\alpha\nabla^2$ 对平移 equivariant,$\forall$ 常数 $(c,\alpha)$。故 $E_G(\theta;\text{shift})\equiv 0$
  在**整个常系数族**上 $\Rightarrow\ker\supseteq$ 常系数族 $\supseteq$ 速度故障 $c\to c'$。
  即 **advection-speed 故障在核中,equivariance MR 不可检** —— 与 S10 实测
  advection-speed `0/n`、wavenumber-sign 漏检**完全一致**。反之空间非齐次系数 $c(x)$
  破坏平移 equivariance $\Rightarrow E_G\ne 0\Rightarrow$ 被检(与 inhomogeneous 故障被检一致)。
  FA 在此可验:平移生成元 + 一个 generic $x_0$ 已 unisolvent,足以区分常系数 vs 非齐次。

---

## 5. 跨块 schema(G 证毕;其余作实例)

通用模板:块 $s$ + 结构 $T_s$ + 保结构谓词 + 缺陷泛函 $E_s$;**当 $E_s$ 对 $\theta$ 仿射且
FA 成立,§3 证明逐字复用**,得 $\ker(\rho_{\iota,s})=\{T_s\text{-compatible}\}$。逐块谓词:

| 块 | $T_s$ 结构 | 保结构谓词(故障在核 $\iff$) | $E_s$ |
|---|---|---|---|
| $G$ | 群作用 | $\delta$ 保 equivariance(**已证**) | $P_\theta(gx)-\rho(g)P_\theta(x)$ |
| $O_\le$ | 偏序 | $\delta$ 保单调/线性 | $P_\theta(\theta_1)\not\le P_\theta(\theta_2)$ 的违反量 |
| $T^{*}$ | 内积自伴 | $\delta$ 保 $\langle Lx,y\rangle=\langle x,Ly\rangle$ | 内积对称差 |
| $\mathcal{T}^{*}_{\mathrm{rev}}$ | 时反对合 | $\delta$ 与时反交换 | $P_\theta(\mathcal{T}x)$ vs $\mathcal{T}$-像 |
| $\mathcal{L}^{*}$ | 极限/收敛阶 | $\delta$ 保收敛阶 | Richardson 比偏离 |

**[需作者]** 逐块确认 $E_s$ 仿射性:$G,O_\le,T^{*},\mathcal{T}^{*}_{\mathrm{rev}}$ 的缺陷在线性
PDE 下仿射;**$\mathcal{L}^{*}$ 的 Richardson 比对 $\theta$ 非线性**,需单独论证或限子类
(否则 $\mathcal{L}^{*}$ 块只保留充分方向,不立紧性)。

---

## 6. 推论 IBT-2 / IBT-3(参数空间语言)

- 每个 oracle $O_j$ 有核 $K_j\subseteq\Theta$。**IBT-2(联合核完备条件)**:$\{O_j\}$ 检出
  一切非平凡故障 $\iff\bigcap_j K_j=\{\theta^{*}\}$。完备性要求核**平凡相交**的 oracle 族,
  而非同对称类的更多 MR。
- **IBT-3(微分 oracle 为代数补)**:微分 oracle 核 $K_{\mathrm{diff}}=\{\theta:$ 两实现被
  **同样**扰动$\}$(共模)。$K_{\mathrm{MR}}$(保对称)$\cap\,K_{\mathrm{diff}}$(共模)= 同时
  保对称且共模的故障。故障逃逸二者 $\iff$ 同时保结构且共模。

---

## 7. 实证(S10,3 SUT,live)

| SUT | MR | diff | MR-only | diff-only | both | neither | union | McNemar $p$ |
|---|---|---|---|---|---|---|---|---|
| advdiff-2d | 13/29 | 12/29 | 6 | 5 | 7 | 11 | 18/29 | 1.0 |
| radxfer-G2 | 25/31 | 10/31 | 17 | 2 | 8 | 4 | 27/31 | 7.3e-4 |
| grayscott | 41/44 | 28/44 | 16 | 3 | 25 | **0** | **44/44** | 4.4e-3 |

- **IBT-G / IBT-1**:advection-speed / wavenumber-sign 保平移对称 → 在核 → MR 漏检
  (实测确认);非齐次/边界故障破坏结构 → 被检。
- **IBT-3(核=共模),3 SUT live**:radxfer abs/scatter/source `0/18`、grayscott
  feed/reaction `0/12`(改共享算子 → 共模);impl-specific 扩散 radxfer `8/8`、
  grayscott `15/15`。
- **IBT-2(联合核平凡)**:grayscott neither$=0$、union$=44/44$ —— $K_{\mathrm{MR}}\cap K_{\mathrm{diff}}=\{\theta^{*}\}$ 在测试故障集上的直接实证。
- 诚实方向:radxfer/grayscott 的 MR raw recall 显著更高($p<0.01$);主张为**互补**
  (核不同、并集趋完备),非微分更优。

---

## 8. 剩余 [需作者数学判断]

1. **非 G 块 $E_s$ 仿射性**:$O_\le/T^{*}/\mathcal{T}^{*}_{\mathrm{rev}}$ 在线性 PDE 下确认仿射;
   $\mathcal{L}^{*}$ Richardson 比非线性,需子类或仅留充分方向。
2. **FA 的 per-instance rank 检验**:有限线代,可脚本化(advdiff 已论证 unisolvent);
   建议对每个立紧性的块/SUT 跑一次 rank 检验并记档。
3. **核非空一般性**:每个非平凡 $T_s$ 是否必有非平凡 compatible 故障(per-instance 易,
   一般性需证)。
4. **与 Composite-`Translate`(protocol_theory T2)**:IBT-2 的完备性是否在多项式可
   判定的扩展内可达——与 T2 同一开放问题。

---

## 9. 反驳条件(courage to be questioned)

- **反驳 IBT-G(紧)**:给出算子可表达、保 $G_\iota$ 对称、却被 equivariance MR 检出的
  故障(在 FA 下违反紧性)。
- **反驳可达性引理**:证明某有限维故障类无任何有限 unisolvent 测试。
- **反驳 IBT-3**:在 one-sided mutation 的 SUT 上 $K_{\mathrm{MR}}$ 与 $K_{\mathrm{diff}}$ 嵌套
  (一方 $\subseteq$ 另一方)而非交叉。

---

## 10. 正文落位(待 P0 Step3/4 抉择后)

立为 **§3.4**(CONSTRUCT-MP 之后):Definition(故障参数空间 + 缺陷泛函)+ Definition
(Faithfulness)+ Reachability Lemma + **Theorem IBT-G** + 证明 + advdiff worked check;
跨块 schema 一段(G 证毕,其余 Remark 实例);IBT-1/2/3 推论;实证下放 §5.2(L2)。
$\mathcal{L}^{*}$ 块按 §8.1 结论决定立紧性或仅充分方向。**仍待 Step3/4 抉择后再动正文。**
