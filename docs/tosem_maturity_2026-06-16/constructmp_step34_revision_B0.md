# B0 — CONSTRUCT-MP Step 3/4 三方案正文级修订草案 + 影响分析

> 用途:解锁 §3.4(IBT)落正文前的承重前置(审稿评估 R-B1)。**本文不动 `.tex`**,
> 仅给出可直接替换的修订文本 + 影响分析,供作者在 A/B/C 中选定。
> 决定性事实须作者判断,标 **[需作者数学判断]**。

---

## 0. 缺陷复述(protocol_theory T1)

现稿 CONSTRUCT-MP(`NOETHER_paper_arxiv.tex` §3.2)逐字:

```
Step 1 — Invariant extraction. For each block s in D(A_P), compute I_s.
Step 2 — MR derivation. For each ι∈I_s, R(ι) = { ρ=Translate(ι',s) : ι'~_s ι }.
Step 3 — Quotient.   Form the MetaPattern m_s = R(ι)/~_s.
Step 4 — Aggregation. Return M(A_P) = { m_s : s ∈ D(A_P) }.
```

**歧义**:Step 4 的集合写法 `{ m_s : s∈D }` 暗示**每块恰好一个 MP**;但若某块 $s$ 下存在
两个 $\sim_s$ 不等价的不变量 $\iota_1\nsim_s\iota_2$,则 $\mathcal{R}(\iota_1),\mathcal{R}(\iota_2)$ 属不同等价类,
Step 3 的商 $\mathcal{R}(\iota)/\!\sim_s$ 实际产出**多个** MP。Step 3(多)与 Step 4(每块一)逻辑不一致。

---

## 1. 三方案的正文级修订文本(可直接替换 Step 3/4)

### 方案 A —— 每块聚合(aggregate per block)

> **Step 3 — Quotient.** Form the *block* MetaPattern as the aggregate over all
> $\sim_s$-classes of block $s$:
> $$m_s \;=\; \bigcup_{[\iota]\in \mathcal{I}_s/\sim_s} \mathcal{R}(\iota),$$
> i.e. $m_s$ collects the \texttt{Translate}-image of every invariant in block $s$.
> **Step 4 — Aggregation.** Return $\mathbb{M}(\mathcal{A}_P)=\{\,m_s:s\in\mathcal{D}(\mathcal{A}_P)\,\}$,
> with $|\mathbb{M}(\mathcal{A}_P)|\le 8$.

> **Remark (aggregate object).** $m_s$ may bundle several $\sim_s$-inequivalent
> invariant families (e.g. on $G$, an $\mathrm{SO}(3)$-orbit invariant and a $\mathbb{Z}_2$-parity
> invariant); it is read as a per-block aggregate, not a single semantic unit.

### 方案 B —— 每等价类一 MP(per $\sim_s$-class)

> **Step 3 — Quotient.** For each $\sim_s$-equivalence class $[\iota]\in\mathcal{I}_s/\sim_s$,
> form the MetaPattern $m_{s,[\iota]}=\mathcal{R}(\iota)$ (the \texttt{Translate}-image of $[\iota]$).
> **Step 4 — Aggregation.** Return
> $$\mathbb{M}(\mathcal{A}_P)=\bigcup_{s\in\mathcal{D}(\mathcal{A}_P)}\{\,m_{s,[\iota]}:[\iota]\in\mathcal{I}_s/\sim_s\,\},
> \quad |\mathbb{M}(\mathcal{A}_P)|=\sum_s|\mathcal{I}_s/\sim_s|\ \ge\ \#\text{blocks}.$$

> **Def (canonical ordering, refined).** 把现 Def canonical-block ordering 由 block 层
> 推广到 (block, class) 层:先按块的全序 $G>O_\le>\dots>\mathcal{B}^{*}_{\mathrm{rel}}$,块内再按一个
> 固定的类序(如不变量 arity 升序、再字典序)消歧。

### 方案 C —— 单类假设(single-class assumption)

> **Assumption (single class per block).** For the operator algebras instantiated in
> this paper ($\mathcal{A}_{\mathrm{Boltz}},\mathcal{A}_{\mathrm{equi}},\mathcal{A}_{\mathrm{rel}}$), each block contributes at
> most one $\sim_s$-equivalence class: $|\mathcal{I}_s/\sim_s|\le 1$ for every $s$.

> 在此假设下 Step 3/4 **保持原文**($m_s=\mathcal{R}(\iota)/\!\sim_s$ 良定义为单类),$|\mathbb{M}|\le 8$。
> 以**实例级假设**陈述,非一般定理。

---

## 2. 影响分析(A/B/C × 关键维度)

| 维度 | A 聚合 | B 每类 | C 假设 |
|---|---|---|---|
| Theorem 1(closure) | 不变(块层唯一性) | 仍成立,但唯一性/canonical order 须升到**类层** | 不变 |
| Theorem 2(poly-time) | 不变($n=$ generators) | 计数对象变为**类数**;需补 finiteness「$\mathcal{I}_s/\sim_s$ 有限」 | 不变 |
| **IBT 粒度一致性**(见 §3) | **不匹配**:MP 每块、IBT 的 $\rho_{\iota,s}$ 每不变量 | **匹配**:MP=类=不变量粒度 | 匹配(假设把两者压平) |
| "seven MetaPatterns" 叙事 | 保留(7 块→7 MP) | 改为"$K\ge 7$;若每块单类则 $K=7$" → 改 Abstract/Contrib/表 caption/Conclusion | 保留 |
| PWR 反例叙事(§3.6) | 不变 | 不变(反例是 Translate 可达性,与聚合粒度无关) | 不变 |
| 实例报告负担 | 无 | 须逐块报告 $\sim_s$ 类数 | 须**验证**每块单类(否则假设假) |
| 审稿风险 | 语义单元被捆绑;**叠加 IBT 后粒度矛盾**(§3) | 叙事改动大,但语义最干净、与 IBT 自洽 | "临时假设"质疑;若实例中某块多类则**假设被证伪** |
| 改动量 | 小 | 中(theorem 计数 + 全篇数字) | 最小 |

---

## 3. IBT 耦合的专门说明(本轮新增,决定性)

IBT 的 MR、核、推论**都在 per-invariant 粒度**陈述:$\rho_{\iota,s}=\texttt{Translate}(\iota,s)$,
$\ker(\rho_{\iota,s})$,IBT-1 是"单个 $\rho_{\iota,s}$ 漏掉保对称故障"。因此:

- **方案 A 现在多一项硬伤**:MP 在**块**粒度($m_s$ 聚合),而 IBT 的分析单元在**不变量/类**
  粒度。同篇出现"MP=块"与"limiting theorem 作用于每不变量 MR"两套粒度 → 审稿人会问
  "$m_s$ 是聚合体,IBT-1 说的是其中哪一个 $\rho_{\iota,s}$?" —— **粒度不一致**。IBT 入正文后,
  A 从"可接受"降为"不推荐"。
- **方案 B 与 IBT 天然自洽**:$m_{s,[\iota]}$ 一一对应一个 $\sim_s$ 类 = 一族同构 MR =
  IBT 的作用单元;IBT-2 的"oracle 族 $\{O_j\}$"自然就是 $\{m_{s,[\iota]}\}$,$\bigcap_j\ker$ 在此族上。
- **方案 C 把粒度压平**(每块=单类),IBT 自洽,但代价是 §4 的可证伪假设。

---

## 4. 决定性 [需作者数学判断]

**唯一关键事实**:三个域($\mathcal{A}_{\mathrm{Boltz}},\mathcal{A}_{\mathrm{equi}},\mathcal{A}_{\mathrm{rel}}$)中,**是否存在某块含 $\ge 2$ 个
$\sim_s$ 不等价类?** 重点核 $G$ 块:

- equivariant ML 的 $G$ 块是否**同时**含 $\mathrm{SO}(3)$ 旋转不变与 $\mathbb{Z}_2$ 反射/parity 不变,
  且二者在 $\sim_s$ 下**不等价**?若是 → 某块多类为真 → **C 假设被证伪、A 捆绑异质语义、B 是唯一诚实选择**。
- 若三域每块确为单类 → A=B=C 外延一致,可走 **C**(最省、保"7"),或 **B**(更一般、更诚实)。

---

## 5. 审稿人推荐

1. **首选 B**:与 IBT per-invariant 粒度自洽,语义最干净,可证伪性最强;代价是放弃"恰好 7"
   并改 Thm 2 计数 + 全篇数字。**IBT 入正文后,B 的相对优势上升。**
2. **C 作回退**:仅当 §4 检验确认"三域每块单类"成立——届时 C 最省且保"7",但须把该检验
   写入正文(把假设变为已验证事实,消解"临时假设"质疑)。
3. **不推荐 A**:IBT 入正文后产生块 vs 不变量的粒度矛盾(§3);除非作者放弃 IBT 的
   per-invariant 表述(代价更大)。

---

## 6. 落正文序(B0 之后)

B0 选定 → **B1**(§1/Abstract/Contributions/Boundary-box 再定心 diff:删 "systematisation
rather than deduction"、Thm 1 降 lemma、IBT 升 contribution、按选定方案改 MP 计数叙事)→
**B2**(一次性把 §3.2 Step3/4 修订 + §3.4 IBT + §3.3 Thm1 降级 + 全篇数字同步落 `.tex`,
随后跑 CLAUDE.md §8 grep/编译 audit)。
