# T2 划界段 + cover letter 披露(草稿,待用户定夺)

> 用途:化解评审 🔴#4(与姊妹论文 Minimum-MR-SubSet / T2 的 venue-overlap / salami 未声明)。
> 这是**零实验成本的 must-do**。措辞采用去时序、中性表述(§6.7),不写 "companion under review" / "round" / "this revision"。
> 边界口径取自 T2 仓库 `cover_letter_novelty_statement.md`:NOETHER = generation(MR 从哪来),T2 = selection(给定 MR 集选最小完备子集),二者正交。

## A. 可插入正文的 differentiation 段(LaTeX)
建议位置:§2(Related Work)末,或 §8(Discussion)。**未插入正文**,待你确认位置后再动稿。

```latex
\paragraph{Relation to a separate line of work on minimum complete MR subsets.}
A separate line of work by some of the present authors addresses the
\emph{orthogonal} problem of \emph{selecting} a minimum complete subset from a
\emph{given} metamorphic-relation pool: taking an MR set as input, it
characterises the smallest subset that preserves the pool's fault-detection
power under a fixed fault model, proves the corresponding decision problem
NP-hard, and provides approximation and exact (ILP) solvers. That work takes
the MR set as given and optimises its cardinality; the present paper is
concerned with the upstream question of where MRs and MetaPatterns
\emph{come from} --- their constructive derivation from a program-induced
operator algebra and algebraic closure under \texttt{Translate}. The two are
complementary: NOETHER \emph{generates} the algebra-induced MR space that a
subset-selection procedure would then \emph{minimise}. No theorem or empirical
claim is shared: the present paper makes no minimality or subset-selection
claim, and the subset-selection work makes no derivation or closure claim.
```

## B. cover letter 披露段(英文,主动向主编披露)

```
Disclosure of related work by the authors.
For full transparency, a separate manuscript by some of the present authors
addresses an orthogonal problem in metamorphic testing: selecting a minimum
complete subset from a *given* metamorphic-relation pool (an NP-hard
optimisation problem, with approximation and ILP solvers). The present
submission, NOETHER, concerns the complementary upstream question of
constructively *deriving* metamorphic relations and MetaPatterns from a
program-induced operator algebra. The two manuscripts share experimental
infrastructure (the operator-algebraic substrate and reactor-physics
witnesses) but make disjoint technical claims --- generation/closure here,
subset-minimality there --- and target distinct reviewer audiences. The
related manuscript is available to the editor on request
[据仓库记录 T2 已上 arXiv,请在此填实际 preprint ID,例如 arXiv:XXXX.XXXXX]。
```

## C. 措辞红线(取自 T2 cover_letter_novelty_statement §2.3)
- ✓ "separate line of work" / "complementary" / "orthogonal" / "disjoint technical claims"
- ✓ "shares experimental infrastructure"(显式承认数据复用,引 Defects4J/Papadakis 跨论文复用惯例)
- ✗ 避免:"extension of" / "follow-up"(暗示从属/渐进)
- ✗ 避免:完全不提(隐瞒重叠最危险)
- ✗ 避免:版本化/时序措辞("our other submission under review at TSE")

## D. 重要警示
评审 EIC 把"T2 的存在"本身判为 🔴 风险。正确动作是**引用 + 划界 + cover letter 披露**(本草稿),**不是**把 T2 的硬理论(domination 定理 / NP-hard / FPT)搬进 NOETHER——后者会把"未声明"升级为实质性自我抄袭。T2 硬理论只能 `\cite` 作 companion。
