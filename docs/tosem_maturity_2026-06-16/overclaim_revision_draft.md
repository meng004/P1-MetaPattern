# 去 overclaim 修订草案(仅草案,未动稿)

> 用户已选"安全修订+草案":标题/摘要/contributions 的 overclaim **只出草案供定夺,不直接改稿**。
> 这些改动改变论文核心学术定位,属作者决策权(§4 + "人类拥有最终决策权")。确认后我再动 `NOETHER_paper_arxiv.tex` 与投稿版。

## 1. 标题(DA #5:"constructive discovery" 名不副实——upstream 仍是人工归纳)
当前:`NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras`

候选(供选,均弱化"discovery/constructive"的自动发现暗示):
- (a) `NOETHER: A Structural Re-grounding of MetaPattern Catalogues via Operator Algebras`
- (b) `NOETHER: Algebraic Derivation and Closure of MetaPatterns from Program-Induced Operator Algebras`
- (c) 保留原标题,但在 Abstract/Intro 明确"discovery"指 given-algebra 后的机械推导,upstream 蒸馏仍属人工(诚实声明)

建议:(b) 最贴合实际贡献(deductive derivation + closure),不过度承诺。

## 2. 摘要(R2 #1 + DA #1/#5 + R1)
- "We test the framework on **three** operator-algebraic domains" → 分级如实:
  `instantiated on three domains — empirically head-to-head evaluated on one (Java/PIT), case-study evaluated on one (equivariant ML), and analytically mapped to published identities on one (relational query)`。
- "...identify **five** Translate-extension dimensions, with **five further** candidate dimensions..." → 区分已证/未证:
  `five Translate-extension dimensions proven pairwise-independent on the PWR algebra, plus five candidate dimensions on the equivariant-ML and relational algebras asserted by inspection (formal exhaustion as future work)`。
- "mechanical and **provable**" 语气 → 明确 Theorem 1 是 by-construction well-definedness 结果,而非深层定理。

## 3. Contributions(DA #4:C3 "predicts two" 与同节自承循环矛盾)
- C3 当前含 "reproduces three, refines two, and **predicts two** structurally distinct classes"。
- 改:删 "predicts two",保留 "re-classifies / de-duplicates";或限定为"deflationary(over/under-counting)reading 是 non-circular 的"那部分。
- 理由:L673 自承 $T^*/\mathcal{T}^*$ 块从反应堆物理归纳而来,$m_{adj}/m_{rev}$ 再从这些块导出 → "prediction" 在自有语料上循环。

## 4. (可选)κ=1.000 处理(R2/DA 🔴#3)
- 正文不应把多 LLM κ=1.000 作为独立信度证据;明确标注"not an independent-rater statistic,共享语料"。
- 真正解法是补独立人类 κ(需自招 rater,见 NEXT_STEPS,属需投入项)。

---
确认要动稿的范围后告诉我,我会同步改 `NOETHER_paper_arxiv.tex` + `submission/TOSEM_*` 投稿版,并跑编译验证。
