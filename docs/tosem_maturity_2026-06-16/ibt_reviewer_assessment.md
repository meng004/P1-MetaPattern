# 审稿意见 — Invariance-Blindness 定理与 Reachability 引理

> 角色:IST 资深审稿人(软件测试 / 蜕变测试)。对象:`invariance_blindness_theorem_draft.md`
> 的 Reachability 引理 + Theorem IBT-G,及其 FA rank 证据(`supplementary/S10_noether_homefield/fa_rank_check.py`)。
> 算例均经数值核验(N=3,平移群 $\mathbb{Z}_3$)。

---

## 0. 总体判断

两项证明**数学正确**,构成一个**真正的刻画型(characterization)结果**,严格强于现稿
Theorem 1 的 by-construction 闭包。贡献的**新意在于框架化与有限性**(MT 不完备性 =
非平凡 commutant;完备性 = 联合核平凡;紧性可由有限 MR 达到),**不在线性代数本身**;
且受**线性故障类、精确算术、单块**三项假设强约束,投稿前必须显式声明,否则构成 over-claim。

**建议:Accept with minor revision**(限于把 §4 的 R1–R3 写入 scope)。

---

## 1. 形式化定义(建议入正文 §3.4)

- **Def 1(线性程序与故障类).** $P_L:\mathbb{R}^N\to\mathbb{R}^N,\ P_L(x)=Lx$,$L\in\Theta:=\mathbb{R}^{N\times N}$($\dim\Theta=N^2<\infty$)。真程序 $L^{*}$;故障 $L=L^{*}+\Delta$($\Delta\in\Theta$,operator-implementation 扰动)。
- **Def 2(对称 MR 与检测).** 群 $G\le GL(\mathbb{R}^N)$,见证 $W=S_G\times X_0$。MR $\rho_{G,W}$ 断言 $\forall(A,x)\in W:P_L(Ax)=A\,P_L(x)$。pass $\iff [L,A]x=0\ \forall(A,x)\in W$;否则 detect。
- **Def 3(检测核).** $\ker(\rho_{G,W})=\{L:[L,A]x=0,\forall(A,x)\in W\}$;若 $X_0$ 张成 $\mathbb{R}^N$ 则 $=\bigcap_{A\in S_G}\mathcal{C}(A)$,$\mathcal{C}(A)=\{L:[L,A]=0\}$。
- **Def 4(对称相容故障).** $L$ 是 $G$-相容 $\iff[L,A]=0\ \forall A\in G$;相容子空间 $\mathcal{C}(G)$。
- **Def 5(Faithfulness).** $W$ 忠实 $\iff\ker(\rho_{G,W})=\mathcal{C}(G)$,等价于(因 $E$ 线性)$\operatorname{rank}J_W=\operatorname{rank}J_G$。

---

## 2. 两项证明的评估

### 2.1 Reachability 引理

- **正确性**:✓(有限维对偶空间的线性泛函族必有有限张成子集,标准)。
- **强项**:把"测试充分性"与"故障空间维数"挂钩,MT 文献少见。
- **限制**:
  - **R-a**:只保证"存在忠实有限测试",不保证"作者所写 MR 忠实";缺口由 per-instance
    FA rank 检验填补(平移 1 生成元 rank 56 = 全群 7 个的 56;二面体 2 生成元 rank 59 =
    全 16 元的 59)。正文须显式说明此缺口并引用该检验。
  - **R-b**:"$\dim\Theta<\infty$"承担全部重量;非线性 solver / 无限维算子族下失效——是 scope。
  - **定级**:引理 elementary,**新意在 MT 语境应用**;措辞用 "a standard finite-dimensionality
    argument",勿拔高。

### 2.2 Theorem IBT-G

- **正确性**:✓(FA + $E$ 对 $L$ 线性下双向干净)。
- **强项**:刻画(核 = 恰好等变故障)+ 可证伪预测 + S10/FA 双重实证;Theorem 1 所缺。
- **必须写入 scope 的三条限制**:
  - **R1(故障类线性,中)**:定理针对线性化故障类 $\Theta=\mathbb{R}^{N\times N}$;**不得外推非线性**。
    最大 over-claim 风险点。
  - **R2(精确算术,中)**:执行核 $\ker_\tau\supseteq\ker$;低于容差 $\tau$ 的破对称故障假阴。
    须与 §10.2 detectability-floor 交叉引用;定理给的是 $\tau\to0$ 极限核。
  - **R3(单块,低)**:仅 $G$ 块已证;$O_\le/T^{*}/\mathcal{T}^{*}_{\mathrm{rev}}$ 作 schema、$\mathcal{L}^{*}$
    因 Richardson 比对 $\theta$ 非线性而不自动满足 $E_s$ 线性。勿宣称八块全证。
- **$\supseteq$ 平凡**:成立但不致命;如实承认为定义级反增可信度(**R4**)。

---

## 3. 解释定理的算例(N=3,$\mathbb{Z}_3$,已数值核验)

$S=\bigl[\begin{smallmatrix}0&1&0\\0&0&1\\1&0&0\end{smallmatrix}\bigr]$;等变算子 = circulant $aI+bS+cS^2$;真程序 $L^{*}=\mathrm{circ}(2,-1,-1)$。

### 3.1 正例(故障 ∈ 核 ⟹ 漏检 ⟹ MR 不完备)

均匀系数误差 $\tilde L=\mathrm{circ}(2.2,-1.1,-1.1)$(整体 +10%)。仍 circulant ⟹ $[\tilde L,S]=0$ ⟹
任何输入下平移 MR pass ⟹ **漏检**。对应 S10 advection-speed `0/n`。含义:核非平凡 ⊇ circulant
全族 → 单块结构性不完备(IBT-1)。

### 3.2 反例(故障 ∉ 核 ⟹ 被检)

单节点非齐次误差 $\tilde L=L^{*}+\tfrac12E_{00}$。非 circulant,
$[E_{00},S]=\bigl[\begin{smallmatrix}0&1&0\\0&0&0\\-1&0&0\end{smallmatrix}\bigr]\ne0$。见证 $(S,e_0)$:
$[\tilde L,S]e_0=\tfrac12(0,0,-1)^\top\ne0$ ⟹ **被检**。对应 S10 coeff-inhomogeneity 被检。

### 3.3 边界(FA 必要性,已核验)

节点 1 故障 $\tilde L=L^{*}+\tfrac12E_{11}$(真实破对称),$[E_{11},S]e_0=(0,0,0)^\top$:
**只用 $x=e_0$ 的欠功效测试假阴漏检**;补 $x=e_1$ 后 $[E_{11},S]e_1=(-1,0,0)^\top\ne0$ 抓到。
→ 紧刻画在非忠实测试下失效,FA 不可省、须 per-instance 检验;亦为定理可证伪性来源。

---

## 4. 修改要求(投稿前)

| # | 要求 | severity |
|---|---|---|
| R1 | 全程限定 "linear operator-implementation fault class";不外推非线性 | 中(必改) |
| R2 | detect 精确算术 vs 容差 $\tau$,交叉引用 §10.2 floor;定理为 $\tau\to0$ 极限核 | 中(必改) |
| R3 | $G$ 块已证、余块 schema、$\mathcal{L}^{*}$ 非线性除外——如实陈述 | 低 |
| R-a | "存在忠实测试"≠"本 MR 忠实",引用 FA rank 检验 | 低 |
| R-b | 前置声明 $\dim\Theta<\infty$ 为前提 | 低 |
| R4 | $\supseteq$ 方向如实承认定义级;贡献归 $\subseteq$+Reachability+刻画 | 低 |

**若 R1–R3 写入,审稿结论 Accept**:诚实、可证伪、有实证的 limiting theorem,明确优于
by-construction 的 Theorem 1,对 MT 基础理论是实质(虽不宏大)推进。
