# N1 — 逐域 ∼_s 等价类枚举(锚定 Option B,证伪 Option C)

> 用途:为 B0 决策(采纳 Option B)出证据 —— 证明三域中**某些块含 ≥2 个 $\sim_s$
> 不等价类**,使 Option C 的"每块单类"假设为假。判据来自论文自身的块定义。
> 标 **[需作者数学判断]** 处为精确类数,需作者最终核定;但"$\ge 2$ 类存在"已可定论。

---

## 0. 判据(论文 Def block-invariant)

$\iota=(\Phi,\pi)\sim_s\iota'=(\Phi',\pi')$ **当且仅当** $\Phi=\Phi'$ 且 $\pi,\pi'$ 定义同一约束
(至多坐标重标)。故 **$\Phi$ 不同 或 $\pi$ 不同 ⟹ 不同 $\sim_s$ 类**。

---

## 1. 决定性证据(无需领域细节):$O_\le$ 块按定义即 ≥2 类

论文 Hypothesis 1(ii)与 §3.1 把 $O_\le$ 块定义为收集 **monotone *and* linear operators**:

- **单调不变量**:$\Phi=\{$序算子$\}$,$\pi:\ \theta_1\le\theta_2\Rightarrow P(\theta_1)\le P(\theta_2)$。
- **线性不变量**:$\Phi=\{$线性组合算子$\}$,$\pi:\ P(\alpha x+\beta y)=\alpha P(x)+\beta P(y)$。

二者 $\Phi$ 不同、$\pi$ 不同(一个是不等式序关系,一个是线性等式)⟹ **$O_\le$ 至少 2 个
$\sim_s$ 类**。这是论文**自身定义**蕴含的结论,**与具体域无关** ⟹ Option C 的
"$|\mathcal{I}_s/\sim_s|\le 1$"在任何同时含单调与线性的实例上**为假**。

> 三域实例均含单调性与线性(扩散单调依赖系数;输运/扩散对源线性)⟹ $O_\le$ 普遍 ≥2 类。

---

## 2. 第二证据:$G$ 块的几何对称 vs 代数对称

- **Boltzmann**:$G$ 含 (a) **几何对称**(四分之一旋转、反射;$\Phi=$ 空间旋转/反射算子)与
  (b) **能群置换对称**($\Phi=$ 能群置换算子)。$\Phi$ 不同 ⟹ $\ge 2$ 类。
- **equivariant ML**:$G$ 含 (a) **$\mathrm{SO}(3)$ 旋转等变**($\Phi=\mathfrak{so}(3)$ 生成元)与
  (b) **置换 $\mathfrak{S}_n$ 等变**(若该实例含;$\Phi=$ 置换算子)。$\Phi$ 不同 ⟹ $\ge 2$ 类。

---

## 3. 逐域逐块 $\sim_s$ 类数(下界;精确值标 [需作者])

| 块 | Boltzmann | equivariant ML | relational | 备注 |
|---|---|---|---|---|
| $G$ symmetry | **≥2**(几何 + 能群置换) | **≥2**(SO(3) + 置换?) | (空/1) | $\Phi$ 不同即分类 |
| $O_\le$ order | **≥2**(单调 + 线性) | **≥2**(单调 + 线性) | (1?) | **§1 定义级结论** |
| $T^{*}$ self-adjoint | ≥1(伴随互易) | ≥1(forward/backward 对偶) | 0 | [需作者] 是否 >1 |
| $\mathcal{T}^{*}_{\mathrm{rev}}$ | 0(耗散) | ≥1(训练轨迹可逆) | 0 | — |
| $\mathcal{L}^{*}$ limit | ≥1(网格细化) | ≥1(步长/宽度极限) | 0 | [需作者] |
| $\mathcal{D}^{*}$ qual-dyn | ≥1 | ≥1 | 0 | [需作者] |
| $\mathcal{E}^{*}$ method-cmp | ≥1 | ≥1 | 0 | — |
| $\mathcal{B}^{*}_{\mathrm{rel}}$ | 0 | 0 | ≥1(改写规则族) | — |

**关键**:$O_\le$ 行(普遍 ≥2)与 $G$ 行(Boltzmann/equi ≥2)**已足以**判定"某块 ≥2 类为真"。

---

## 4. 结论

1. **某块 ≥2 个 $\sim_s$ 类为真**(最强:$O_\le$ 由论文定义即 monotone + linear 两类)。
2. ⟹ **Option C(单类假设)在论文自身实例上为假**;**Option A(每块聚合)会把单调与线性
   这类异质语义捆进同一 $m_s$**,且与 IBT 的 per-invariant 粒度冲突(B0 §3)。
3. ⟹ **采纳 Option B**(每等价类一 MP):$\mathbb{M}(\mathcal{A}_P)=\bigcup_s\{m_{s,[\iota]}\}$,
   $K=\sum_s|\mathcal{I}_s/\sim_s|\ \ge\ \#\text{blocks}$。
4. **对"恰好 7 个 MetaPattern"叙事的影响**:原"7"实为**块计数**(= 把每块当一个 MP),
   正是 Step3/4 歧义的根源。正确表述:**7 个块,$K\ge 7$ 个 MetaPattern**(块内多类时 $K>7$)。
   需改 Abstract / Contributions / 表 caption / Conclusion 的"7"叙事(B1 任务)。

---

## 5. 残留 [需作者数学判断]

- 各域 $T^{*}/\mathcal{L}^{*}/\mathcal{D}^{*}/\mathcal{B}^{*}_{\mathrm{rel}}$ 的**精确**类数(本表只给可判定的下界)。
- equivariant ML 的 $G$ 块是否实际含置换对称(决定该格是 ≥2 还是 =1)。
- relational 域 $O_\le$ 是否含线性(决定 rel 的 $O_\le$ 是 1 还是 ≥2)。

以上不影响主结论(Option B):"某块 ≥2 类"已由 $O_\le$ 定义确立。精确 $K$ 在 B1 落数字时
由作者逐域核定。
