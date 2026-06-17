# B1 — 再定心草案(Abstract / Scope / Contributions / Boundary-box 替换文本)

> **二次状态更新(2026-06-17,作者拍板)**:Scope 段、Contributions(C2c)、Boundary-box
> 已落 `NOETHER_paper_arxiv.tex`;CONSTRUCT-MP Step3/4 **采 Option B**(每等价类一 MP)
> 落入正文,并通过 `rem:single-class-instances` 在三域选定单一 $\sim_s$ 类的 $\pi$-template
> 以保住已发表 "7 MP" 与 $\kappa=0.857$ 审计。Theorem 1/2 **不降级重编号**(per-instance
> 单类下 poly-time 不变)。**新 Abstract 全文替换尚未落**(下方文本待 B2-Abstract 步骤;
> 当前 Abstract 无自相矛盾,非阻塞)。下方表述以本更新为准。

> 用途:把论文重心从"by-construction 闭包 + systematisation"移到"算子代数 → MR 推导
> (核心)+ Invariance-Blindness 限定定理(非平凡)",并落实 Option B。**本文为 docs 草案
> 文本,供评审;B2 再一次性落 `NOETHER_paper_arxiv.tex`。** 每段标注对应 `.tex` 锚点。
> 诚实约束:经验数字(p 值、检出率)不进 Abstract;结构数字(定理、3 域、9 SUT、8 块)可留。

---

## 1. 新 Abstract(替换 `.tex` L120–130,结构化标签,≤350 词)

**Context.** Metamorphic Testing is in the IEEE/ISO testing standards and widely
recommended for AI systems, yet its progress is bottlenecked by metamorphic
relation (MR) identification, which remains inductive: existing frameworks, mining,
LLM-assisted pipelines, and MetaPattern catalogues leave the *origin*, *closure*,
and *transferability* of MR sets unanswered.

**Objective.** We treat the MR set of a mathematical-physics program family as a
*computable function of its operator algebra*, and make the **limits** of that
derivation a theorem rather than a caveat.

**Method.** We present **NOETHER**: an upstream empirical layer curating a
program-induced operator algebra and its block decomposition, and a downstream
deductive layer, `CONSTRUCT-MP`, that derives a MetaPattern set (one per
operator-invariant equivalence class; eight blocks yield $K\ge 7$ patterns). A
well-formedness lemma (algebraic closure under `Translate`; polynomial-time
decidability) guarantees the construction is consistent. The substantive result is
the **Invariance-Blindness Theorem**: for the symmetry and self-adjoint blocks, the
detection kernel of an algebra-derived MR equals *exactly* the faults that preserve
the structure it exploits, with a finite test attaining this characterization
(faithfulness). We instantiate NOETHER on three operator-algebraic domains and a
nine-system home-field benchmark across thermal, fluid, and reactor physics.

**Results.** The block decomposition is a program-family invariant predictable
before testing (reversible systems populate the time-reversal block, dissipative
ones leave it empty). The Invariance-Blindness Theorem is confirmed: symmetry MRs
miss precisely the symmetry-preserving faults; a neutral cross-implementation
differential oracle has the complementary (common-mode) blind spot, so the two are
complementary and their union approaches completeness. The strictly stronger
absolute-completeness conjecture is falsified on a PWR core algebra, with the
obstruction characterized as five independent extension dimensions.

**Conclusion.** MR sets for these families are algebraically derivable with
*characterizable* blind spots; induction is lifted from per-program MR sampling to
a per-domain algebraic layer, and the framework states precisely where its
derivation is tight and where it is not.

---

## 2. 替换"Scope of contribution"段(`.tex` L256)

**删**:"This is a theoretical paper, and its contribution is systematisation
rather than deduction from first principles."

**改为**:

> This is a theoretical paper whose contribution is a *derivation* of MetaPatterns
> from operator-algebraic structure, together with a *limiting theorem* (the
> Invariance-Blindness Theorem, \S\ref{subsec:ibt}) that characterizes which faults
> the derived MRs cannot detect. The derivation's downstream step is mechanical and
> provable; its upstream step (curating $\mathcal{A}_P$ and its block decomposition)
> remains an explicit empirical hypothesis. We do not eliminate induction; we lift
> it from per-program MR sampling to a per-domain algebraic layer, and we make the
> reach *and the boundary* of the algebraic step precise.

---

## 3. Contributions 编辑(`.tex` L246–254)

- **C2a(改:Thm1 降为良构引理)**:把 "we prove an Algebraic Closure Theorem
  (Theorem 1)" 改为 "we establish a **well-formedness lemma** (algebraic closure
  under `Translate`, by construction within Def~\ref{def:alg-induced}; polynomial-time
  decidability), guaranteeing `CONSTRUCT-MP` drops no `Translate`-reachable MR." 保留
  by-construction 自陈(R4)。
- **新增 C2c(IBT,核心定理)**:

> **C2c (limiting theory).** We prove the **Invariance-Blindness Theorem**: for the
> symmetry ($G$) and self-adjoint ($T^{*}$) blocks, an algebra-derived MR's detection
> kernel equals exactly the structure-preserving faults (within the linear
> operator-implementation fault class, under a faithfulness condition that a finite
> test attains; \S\ref{subsec:ibt}). Corollaries: a single-block battery is
> structurally incomplete; completeness requires oracle families with trivial joint
> kernel; a neutral cross-implementation differential oracle is the complementary
> (common-mode) oracle. This converts the by-construction closure of C2a into a
> falsifiable, non-tautological characterization of the derivation's blind spots.

- **C3(改:数字)**:把"reproduces three prior MetaPatterns…"等表述中的"7 个 MP"叙事
  改为"7 个块、$K\ge 7$ 个 MetaPattern(每等价类一个,Option B)"。

---

## 4. Boundary-of-contribution box 编辑(`.tex` L258–273)

- **"establishes" 列**:在第 1 条(closure)前**降级措辞**为 "a well-formedness lemma:
  algebraic closure … (by construction)";**新增**一条:"the Invariance-Blindness
  Theorem for the $G$ and $T^{*}$ blocks: the symmetry/self-adjoint MR detection
  kernel = structure-preserving faults (faithfulness-tight)."
- **"does not establish" 列**:保留 (a) 绝对完备(Thm1′,PWR 证伪);**新增**:"(e) IBT
  tightness beyond the linear operator-implementation fault class and beyond the
  $G,T^{*}$ blocks; $O_\le/\mathcal{T}^{*}_{\mathrm{rev}}/\mathcal{L}^{*}$ admit only the sufficient
  direction (inequality / matrix-inverse / norm-ratio nonlinearity; see classification)."

---

## 5. 全局"7"叙事扫描(B2 落 `.tex` 时执行)

`grep -n "seven\|7 MetaPattern\|seven MetaPattern" NOETHER_paper_arxiv.tex` → 每处把
"7 个 MetaPattern"区分为 **7 个块** vs **$K\ge 7$ 个 MetaPattern**;Abstract / Contributions /
表 caption / Conclusion 同步。精确 $K$ 由 N1 的逐域类数(作者核定)填入。

---

## 6. B1 之后

B2(一次性 `.tex` pass):§3.2 Step3/4 → Option B 文本;新增 §3.4 IBT(Def1–5 + Faithfulness
+ Reachability Lemma + Theorem IBT-G/T\* + 证明 + advdiff worked check + 逐块分类表 +
IBT-1/2/3);§3.3 Thm1 降 lemma;§1/Abstract/Contributions/Boundary 同步(本 B1);
§5 实验(L1/IBT-3/L3 + N3 池化 + FA rank);随后跑 CLAUDE.md §8 grep/编译 audit。
