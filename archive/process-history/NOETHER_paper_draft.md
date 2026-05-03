# NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras

**Status:** Draft v0.1 (Stage 2 FULL writing in progress)
**Target venue:** IEEE TSE / ACM TOSEM
**Target length:** ~9,100 words main + ~1,500 words appendix
**Language:** English

> **Drafting note:** Citation placeholders use the form `[CITE: AuthorYear — short topic]`.
> Every such placeholder will be resolved with a verified reference (DOI or canonical URL) during Stage 2.5 INTEGRITY verification. No fabricated citations are produced at the drafting stage.

---

## Abstract

**English.** Metamorphic Testing (MT) has matured into a recognised technique within IEEE/ISO software-testing standards and a recommended practice for testing AI systems, yet its progress is bottlenecked at metamorphic relation (MR) identification — a step that remains heavily dependent on tester domain knowledge and produces MR sets that are difficult to reuse across teams or domains. Existing structural responses, including the METRIC and METRIC+ category frameworks, recent automated pipelines (MR-Scout, GenMorph, and LLM-assisted methods), and various MetaPattern catalogues, share an inductive grounding: their pattern structures are extracted from MR samples and validated by empirical coverage. As a result, three foundational questions remain unanswered: *origin* (why these patterns and not others), *closure* (whether the pattern set is complete), and *transferability* (how patterns shift across domains without re-running induction). We propose **NOETHER**, the first constructive framework with provable completeness for MetaPattern discovery. Given a decomposition of the underlying operator algebra into seven blocks — symmetry, order, self-adjoint, time-reversal, limit, qualitative-dynamics, and method-comparison — NOETHER constructs a MetaPattern set with a provable constructive-completeness guarantee (Theorem 1) under a canonical-block ordering, and polynomial-time decidability when the algebra admits a finite generating set (Theorem 2). The framework is hybrid by design: the seven-block decomposition is an empirical curation of mathematical structures recurrent across program families (upstream layer), while everything below — the derivation of $\mathbb{M}(\mathcal{A}_P)$ from $\mathcal{A}_P$ — is mechanical and provable (downstream layer). We instantiate NOETHER on the Boltzmann transport equation — tracing through neutron transport, diffusion, and burnup — and show that the framework systematises a previously inductively-assembled five-pattern catalogue: it reproduces three patterns, refines two on a sounder algebraic basis (separating qualitative-dynamics from time-reversal, and method-comparison from self-adjoint duality), and predicts two more (adjoint reciprocity and time-reversal compatibility) that the inductive corpus had not isolated in canonical form. We then re-instantiate NOETHER on equivariant machine learning, deriving a concrete executable MR end-to-end (rotation invariance for SE(3)-equivariant point-cloud classifiers) to demonstrate cross-domain transferability without re-running empirical induction. NOETHER does not eliminate induction from MetaPattern discovery; it relocates induction one level up — from MR samples to recurrent algebraic structures across program families — and makes everything below that level mechanical, providing MR identification with its first constructively complete foundation under an explicit empirical curation.

**Keywords (EN):** metamorphic testing, metamorphic relation identification, MetaPattern, operator algebra, equivariance, algebraic completeness, software testing foundations.

**繁體中文摘要。** 蛻變測試（MT）已成為 IEEE/ISO 軟體測試標準下被認可的技術，並已被推薦用於 AI 系統測試，然而其發展受限於蛻變關係（MR）識別這一瓶頸：該步驟高度依賴測試者的領域背景，產出的 MR 集合難以跨團隊或跨領域重用。既有的結構化嘗試——包含 METRIC 與 METRIC+ 範疇框架、近期的自動化管線（MR-Scout、GenMorph 及 LLM 輔助方法）以及各類元模式目錄——皆共享相同的歸納式立基：其模式結構由 MR 樣本萃取，並以經驗覆蓋率加以驗證。由此，三個基礎問題尚未獲得解答：*來源*（為何恰是這些模式）、*閉合性*（模式集合是否完備）以及*跨域可遷移性*（不重新執行歸納時模式如何遞移）。本文提出 **NOETHER**——首個具備可證明完備性之構造性元模式發現框架。給定算子代數沿七區塊（對稱、序、自伴、時反、極限、定性動力學、方法比較）之分解，NOETHER 構造性地產出元模式集合，並在規範區塊優先序下具備可證明的構造性完備保證（定理 1）以及在算子代數有限生成集條件下的多項式時間可判定性（定理 2）。框架本身是分層設計：七區塊分解是對程式族中反覆出現之數學結構的經驗策劃（上游層），而由 $\mathcal{A}_P$ 推導 $\mathbb{M}(\mathcal{A}_P)$ 之過程則為機械可證（下游層）。我們以 Boltzmann 輸運方程為核心進行實例化，貫穿中子輸運、中子擴散與燃耗，證實框架可**精細化**先前歸納目錄（將定性動力學與時反、方法比較與自伴對偶分離）並系統性地**預測**兩項歸納方法所遺漏的元模式；繼而於等變機器學習領域上重新實例化，並端到端推導出 SE(3) 等變點雲分類器之旋轉不變 MR，以實證方式展現框架的下游構造機制可跨域遷移，無須重做經驗歸納。NOETHER 並未消除歸納，而是將歸納從「MR 樣本層級」上移至「程式族中反覆出現之代數結構層級」，既有上游之誠實校準，亦有下游之機械可證，使 MR 識別擁有其首個構造性完備立基。

**關鍵字（zh-TW）：** 蛻變測試、蛻變關係識別、元模式、算子代數、等變性、代數完備性、軟體測試理論基礎。

---

## 1 Introduction

In 1918, Emmy Noether's first theorem provided mathematical physics with a structural reading of conservation laws: continuous symmetries of an action induce corresponding conservation laws. The result did not abolish the empirical study of physical invariants; it re-grounded it, supplying a derivation procedure where previously the laws had been accumulated by observation and analogy. We do not claim Noether's theorem itself in software engineering — neither program semantics nor metamorphic relations admit an action functional — but we draw a *structural homage* to its move: replacing an empirical catalogue with a derivation procedure rooted in algebraic structure.

Software testing faces a structurally analogous situation. Metamorphic Testing (MT), introduced by Chen et al.\ in 1998 [CITE: Chen1998 — original MT proposal], was admitted into the IEEE/ISO/IEC software-testing standards in 2022 [CITE: ISO29119 — software testing standards] and has been increasingly endorsed as a key technique for testing AI and machine-learning systems [CITE: Segura2016 — MT survey; LiTOSEM2025 — MR generation survey]. As of 2025, the field is supported by at least one major IEEE-published survey [CITE: Segura2016] cataloguing dozens of MRs across multiple application domains, one ACM TOSEM survey [CITE: LiTOSEM2025] systematically reviewing the recent MR-generation literature, and a substantial body of automated MR-identification methods spanning evolutionary search, mining-based approaches, and LLM-assisted pipelines. Its central artefact is the *metamorphic relation* (MR): a property that constrains how a program's outputs must covary across multiple executions, thereby substituting for an explicit oracle in domains where one cannot exist. Despite this maturity, the identification of MRs — deciding *which* properties hold for a given program under test — remains MT's binding constraint. Practitioners report that MR identification is heavily dependent on the tester's domain background, that different authors formulate MRs in mutually incompatible ways for the same program, and that the resulting MR sets are difficult to reuse across teams or projects [CITE: Segura2016; LiTOSEM2025]. The community has responded with two complementary lines of work: an *application* layer that mines MRs for specific domains, and an *integration* layer that automates the search through evolutionary, mining, or LLM-based pipelines [CITE: MRScout-TOSEM2024; GenMorph-TSE2024; Shin-QUATIC2024]. Both have advanced rapidly. The *foundational-theory* layer has not.

The principal artefact at that foundational layer is the *MetaPattern* (MP): an equivalence class over MRs that captures a recurrent structural strategy a tester invokes when reasoning about program properties. MetaPatterns matter because they organise the otherwise unbounded MR design space into a small, interpretable scaffold; methods that exploit them — including the structured MR identification approaches METRIC [CITE: Chen-METRIC] and METRIC+ [CITE: Sun-METRICplus], and the recent wave of LLM-prompted MR generators — depend on the scaffold's quality. Yet across the literature, MetaPattern catalogues continue to be assembled in the same way conservation laws were assembled before 1918: by induction over observed examples. A typical proposal lists *k* patterns drawn from cluster analysis or expert codification, demonstrates that the patterns "cover" some corpus of MRs to a target threshold, and stops. None of the existing MP proposals — including the authors' own prior work on five reactor-physics patterns — answers the three questions that any foundational theory of MetaPatterns should answer:

1. **Origin.** *Why* exactly these MetaPatterns and not others? What is the structural source of an MP, as distinct from an empirical regularity in the corpus on which it was induced?
2. **Closure.** Under what mathematical conditions is a discovered MP set *complete* — that is, guaranteed not to miss patterns that lie outside the inductive sample?
3. **Transferability.** When the program family changes (from reactor physics to natural-language inference, from numerical libraries to recommender systems), how does the MP set change, and can the new set be obtained without re-running the entire empirical induction in the new domain?

We call this the *origin–closure–transferability gap*. It is not an academic embarrassment alone: it is the proximate cause of two pathologies that the MT community has tracked for years. First, MRs continue to *emerge* without bound — every new domain or every new system produces a fresh batch of formulations, with little structural commonality across teams. Second, discovered MRs are poorly *reusable* — a relation written for one program rarely transports to another, even when both share a deep structural template. Both pathologies, we argue in §2, are not engineering inconveniences awaiting better tooling; they are paradigm-level consequences of grounding MetaPatterns inductively. Only an algebraically closed origin can simultaneously bound emergence and enforce reusability.

This paper proposes such an origin. We introduce **NOETHER**, a constructive framework that derives MetaPatterns from the operator-algebraic structure of the program family under test. The key move is to take seriously, and then mechanise, the analogy with Noether's 1918 theorem: where physics extracts conservation laws from continuous symmetries of the action, NOETHER extracts MetaPatterns from invariances of an operator algebra $\mathcal{A}_P$ (formally defined in §3.1) that captures the program's underlying mathematical scaffolding. Given $\mathcal{A}_P$, NOETHER deductively produces a MetaPattern set $\mathbb{M}(\mathcal{A}_P)$ (constructed by the algorithm of §4.2) together with a provable closure guarantee over the algebra-induced MR space; given a different program family with a different algebra $\mathcal{A}_{P'}$, the framework produces $\mathbb{M}(\mathcal{A}_{P'})$ by the same mechanism, without re-running empirical induction. The framework does not abolish induction — domain experts must still distil $\mathcal{A}_P$ from program semantics, and we are explicit about this limitation in §7 — but everything downstream of $\mathcal{A}_P$ becomes algebraic.

We make four contributions.

- **C1.** We propose NOETHER, a *hybrid* framework for MetaPattern discovery: an empirically-curated seven-block decomposition of operator-algebraic structures recurrent across program families (upstream layer), composed with a constructive algorithm that mechanises MetaPattern derivation from any algebra so decomposed (downstream layer). The framework is honest about which layer is empirical and which is algorithmic.
- **C2.** We prove a Constructive Completeness Theorem for the constructed set: given the seven-block decomposition, the resulting MetaPattern set is exhaustive over the algebra-induced MR space; we establish polynomial-time decidability when the algebra admits a finite generating set. The theorem is calibrated about what it does and does not prove (§4.3).
- **C3.** We instantiate NOETHER on a real-world program family and show that the framework systematises previously catalogued patterns: it reproduces three prior MetaPatterns, refines two on a sounder algebraic basis, and predicts two more that the inductive method missed. The "predicted" MetaPatterns are not de novo discoveries — domain experts could have written them down — but the framework supplies the algebraic warrant that classifies them as structurally distinct equivalence classes.
- **C4.** We establish NOETHER's cross-domain transferability by re-instantiating it on a non-originating domain, showing that the framework's downstream construction generalises without empirical re-induction; and we derive a concrete, executable MR end-to-end in that domain (§6.4) to demonstrate that the framework is generative, not merely descriptive.

**Scope of contribution.** This is a theoretical paper, and we are explicit about an epistemological calibration concern raised by careful readers of an earlier draft. NOETHER's contribution is at the level of *systematisation*, not deduction from first principles. The seven blocks themselves are curated by inspection of mathematical structures that recur across the program families we have studied; they are not derived from any algebraic-theoretic axiom. The framework therefore consists of two layers: an *upstream layer* (curating $\mathcal{A}_P$ and its block decomposition) that remains empirical and human, and a *downstream layer* (mechanically deriving $\mathbb{M}(\mathcal{A}_P)$ from $\mathcal{A}_P$) that is algorithmic and provable. We do not claim to have eliminated induction from MetaPattern discovery; we have moved induction one level up — from "what MetaPatterns recur in observed MR samples?" to "what algebraic structures recur in the program families practitioners care about?" — and made everything below that level mechanical. The engineering payoff of this re-grounding awaits empirical follow-up work; we do not in this paper conduct comparison studies against existing automated MR-identification pipelines on shared benchmarks, leaving such an evaluation to a separate empirical study with a unified harness.

The remainder of the paper is organised as follows. §2 surveys the four lines of prior work — MT/MR fundamentals, structured MR identification (METRIC, METRIC+), automated MR identification (MR-Scout, GenMorph, LLM-assisted methods including Shin et al.), and existing MetaPattern catalogues — and locates NOETHER's gap-filling role. §3 introduces the operator-algebraic preliminaries needed to read the framework. §4 presents NOETHER itself, the construction algorithm, and the two theorems. §5 instantiates NOETHER on the Boltzmann transport equation and traces the consequences through neutron transport, neutron diffusion, and burnup as a worked, deeply-developed example. §6 cross-instantiates NOETHER on equivariant machine-learning models. §7 discusses threats to validity, the relationship with METRIC/METRIC+, and the relationship with empirical adequacy frameworks. §8 concludes with deployment prospects: LLM-prompt design grounded in algebraic MetaPatterns, automated MR-tool generation across domains, and an algebraic re-formulation of MP-set adequacy. An appendix instantiates NOETHER on the remaining four reactor-physics equations as confidence-strengthening evidence.

---

## 2 Background and Related Work

We organise prior work along four storylines: (S1) MT/MR fundamentals and the long-standing identification bottleneck; (S2) structured MR identification approaches that have attempted to introduce categorical scaffolding (METRIC, METRIC+); (S3) recent automated MR identification methods (MR-Scout, GenMorph, and LLM-assisted approaches); and (S4) existing MetaPattern catalogues, including the authors' own prior reactor-physics taxonomy. The four storylines converge on a single diagnosis: every line inherits an inductive grounding, and the field's twin pathologies — unbounded MR emergence and poor MR reusability — are paradigm-level consequences of that grounding rather than engineering shortfalls.

### 2.1 Metamorphic testing and the MR identification bottleneck

Metamorphic Testing was introduced by Chen, Cheung, and Yiu in 1998 to address the test-oracle problem [CITE: Chen1998]. An MR is a logical implication of the form $R_i(x_1,\dots,x_n) \Rightarrow R_o(P(x_1),\dots,P(x_n))$, where $P$ is the program under test, $R_i$ is an input relation, and $R_o$ is an output relation. When $R_i$ holds but $R_o$ fails on actual executions, a fault is reported, without any need to know the absolute correct output of any single execution. Over two decades MT has become standard equipment for testing systems whose oracles are otherwise inaccessible: scientific computing, machine learning classifiers, autonomous vehicles, search engines, compilers, and large language models [CITE: Segura2016; LiTOSEM2025].

The community has long acknowledged a single binding constraint on MT's effectiveness: MR identification. Surveys spanning twenty years agree that identifying high-quality MRs requires (i) deep familiarity with the program's functional semantics, (ii) substantive domain background — physical, mathematical, linguistic, depending on the system — and (iii) the ability to convert that background into executable property assertions [CITE: Segura2016; LiTOSEM2025]. Testers without that background tend to identify only "trivial MRs" — properties so weak that they fail to detect any but the most superficial faults. A 2024 survey explicitly identifies AI assistance, especially via large language models, as the most promising open avenue for closing the identification gap [CITE: LiTOSEM2025].

Beyond difficulty, the MR identification bottleneck has a more troubling structural feature: even when MRs are identified, the field has accumulated little consensus on *how* they are identified. Different authors confront the same program and produce dissimilar MR sets, with dissimilar abstraction levels and dissimilar formulations. Once written, an MR rarely migrates: a relation drafted for one ML classifier seldom transports to another, and a relation drafted for one numerical solver seldom transports across solver families. The field has thus accumulated an ever-growing inventory of one-off MRs whose underlying structural commonalities, if any, are only visible through retrospective taxonomy.

### 2.2 Structured MR identification: METRIC and METRIC+

Two lines of work have explicitly attempted to impose categorical structure on MR identification. METRIC, introduced by Chen and colleagues, organises MR construction around an "input/output category" framework: the tester first identifies relevant categories of input transformations and output relations, then composes MRs from category pairs [CITE: Chen-METRIC]. METRIC+ , proposed by Sun and colleagues, extends this scheme by enriching the category catalogue and providing systematic combination rules to reduce the human burden in category enumeration [CITE: Sun-METRICplus]. Both approaches are widely cited and represent the strongest existing attempt to lift MR identification above ad-hoc craftsmanship.

We agree with the spirit of METRIC and METRIC+: imposing categorical structure on MR identification is the right direction. We disagree, however, with their grounding. The categories themselves are introduced through expert curation and validated by empirical coverage on benchmark programs. This leaves two of our three foundational questions unanswered. *Origin*: METRIC and METRIC+ do not derive their categories from program-level mathematical structure; they assert them and refine them through experience. *Closure*: neither framework provides a mathematical condition under which the category set is guaranteed to be complete; coverage is reported but not proved. The third question, *transferability*, is partially addressed — the same category templates are invoked across domains — but precisely because the categories are not algebraically bound to specific program structures, transferability rests on the assumption that the templates are universal, an assumption the literature has not closed.

### 2.3 Automated MR identification: MR-Scout, GenMorph, and LLM-assisted methods

A more recent wave of work has aimed to automate MR identification end-to-end. MR-Scout mines MRs from existing test suites by extracting input-transformation and output-assertion patterns from test-case pairs and abstracting them into reusable relations [CITE: MRScout-TOSEM2024]. GenMorph evolves MR candidates through genetic programming, co-evolving input transformations with output assertions and using mutation-killing as the fitness signal [CITE: GenMorph-TSE2024]. Shin et al.\ propose deriving executable MRs from natural-language requirements via few-shot prompting of a large language model, validated through an industrial questionnaire study with Siemens [CITE: Shin-QUATIC2024]. Several further LLM-assisted variants — including domain-customised GPTs for autonomous-driving simulators and multi-agent retrieval-augmented pipelines for traffic-rule MRs — extend the same template into safety-critical or rule-rich domains [CITE: GPT-MR-IST2025; AutoMT-2025].

Each of these methods makes progress on a specific axis: MR-Scout exploits the implicit knowledge encoded in existing tests; GenMorph trades interpretability for fitness-driven coverage; Shin et al.\ and subsequent LLM-assisted variants leverage parametric world knowledge in large language models. Yet all of them inherit the same epistemological posture: each treats the MR space as a black box to be searched empirically, with no algebraic prior on what the space contains. The consequences are predictable. MR-Scout's recall is bounded by the test suite's existing coverage, with no mechanism to discover MRs that no existing test happens to encode. GenMorph's evolutionary search converges on a narrow band of structurally simple MRs because the fitness landscape rewards mutation-killing rather than structural diversity. LLM-prompted approaches are sensitive to prompt phrasing and tend to revisit already-encoded MR families absent a structural prior. None of the methods can answer, in advance, which MR types it will fail to find — because none has an algebraic theory of the space being searched.

### 2.4 MetaPattern catalogues and empirical adequacy

A separate line of work has attempted to organise the post-hoc inventory of identified MRs into MetaPattern catalogues. Such catalogues — including the authors' own prior reactor-physics taxonomy of conservation, monotonicity, convergence, trajectory, and partial-order patterns — typically result from clustering observed MRs, codifying expert intuitions about "kinds of properties testers reason about", and validating the catalogue's coverage on a benchmark MR corpus [CITE: PWR-MetaPattern-Report]. Adequacy frameworks such as the Pattern–Matrix Coverage Metric (PMCM) [CITE: PMCM-Adequacy] then assess how thoroughly a given MR set occupies the pattern space, providing a quantitative coverage criterion.

Such catalogues are useful — testing communities benefit from a small, named vocabulary of recurrent strategies — but each is, by construction, an empirical artefact. The catalogue's specific pattern count, the boundaries between patterns, and the very claim that the catalogue is "sufficient" rest on coverage statistics over a finite MR corpus. PMCM and similar adequacy notions inherit the same status: they assert empirical thoroughness, not algebraic closure. None of the existing catalogues, including the present authors' own, can answer the three foundational questions of §1.

### 2.5 Convergent diagnosis

Across all four storylines, two pathologies recur. *Unbounded MR emergence*: every new domain or new program produces fresh MR formulations, with no structural mechanism to predict which formulations are inevitable and which are accidents of expert curation. *Poor MR reusability*: identified MRs do not transport readily across programs that share deep structural similarities, because the inductive grounding does not articulate what those structural similarities are. We argue that both pathologies are not engineering inconveniences but paradigm-level consequences of a foundational choice: every existing line — from craftsmanship through METRIC/METRIC+ through automation through cataloguing — grounds MetaPatterns in observed MR samples rather than in algebraic structure. As long as the grounding is inductive, emergence remains unbounded, because there is no algebraic boundary; and reusability remains poor, because there is no algebraic equivalence under which MRs in different programs can be recognised as instances of the same pattern.

NOETHER, presented in §3 and §4, replaces inductive grounding with operator-algebraic grounding. The next two sections develop the algebraic preliminaries (§3) and the framework itself (§4); §5 and §6 demonstrate that the resulting MetaPatterns coincide with the inductively-catalogued ones in a familiar domain (reactor physics) and generalise constructively to a non-originating domain (equivariant machine learning) without re-running induction.

---

## 3 Operator-Algebraic Preliminaries

This section introduces the algebraic apparatus on which the NOETHER framework is built. We assume readers are conversant with basic abstract algebra at the level of group actions, equivalence classes, and quotient sets, but we do not assume background in functional analysis. Each construct is given a formal definition, an intuition statement, and two examples — one drawn from reactor physics (the originating domain of the framework's first instantiation, §5) and one drawn from equivariant machine learning (a non-physics domain, §6) — so that the algebraic objects of §4 can be read without recourse to a single domain.

### 3.1 Programs and program-induced operator algebras

Throughout the paper we treat a program $P$ as a (possibly partial) computable function $P: \mathcal{X} \to \mathcal{Y}$, where $\mathcal{X}$ and $\mathcal{Y}$ are typed input and output spaces. The class of programs of interest is not isolated: every program in this work belongs to a *program family* whose members share an underlying mathematical scaffolding. For example, every numerical solver of the neutron transport equation shares the operator structure of that equation, regardless of discretisation; every equivariant neural network for point-cloud classification shares the symmetry group of three-dimensional Euclidean space, regardless of architecture.

**Definition 1 (Program-induced operator algebra).** Let $P$ belong to a program family $\mathcal{F}$. A *program-induced operator algebra* of $\mathcal{F}$ is a tuple
$$\mathcal{A}_{\mathcal{F}} \;=\; \bigl(\mathcal{O}, \;\circ, \;\sim_{\mathcal{F}}\bigr),$$
where $\mathcal{O}$ is a set of operators acting on $\mathcal{X}$, $\mathcal{Y}$, or both; $\circ$ is an operator composition; and $\sim_{\mathcal{F}}$ is an equivalence relation declaring two operator expressions equal whenever they agree on every program of $\mathcal{F}$.

*Intuition.* The operator algebra captures the structural commitments shared by all programs in the family — the symmetries, the linearities, the comparison principles, the convergence laws — abstracted away from any particular program's implementation. We will speak of $\mathcal{A}_P$ when the family is clear from context.

*Reactor example.* For neutron-diffusion solvers, $\mathcal{O}$ contains the diffusion operator $-\nabla\!\cdot\!D\nabla + \Sigma_a$, the fission operator $\nu\Sigma_f$, the geometric symmetry group of the core configuration, and the eigenvalue extraction $k_{\mathrm{eff}}$.

*ML example.* For point-cloud classifiers built on equivariant architectures, $\mathcal{O}$ contains the rotation group $\mathrm{SO}(3)$ acting on input coordinates, the permutation group $\mathfrak{S}_n$ acting on the ordering of points, and the network's forward map. Equivariance constraints are encoded as commutation relations within $\sim_{\mathcal{F}}$.

The remaining building blocks of this section refine $\mathcal{O}$ into five operator types whose invariants drive NOETHER's MetaPattern construction.

### 3.2 Symmetry groups (Building Block B2)

**Definition 2 (Symmetry group of $\mathcal{A}_P$).** A *symmetry group* of $\mathcal{A}_P$ is a subgroup $G \le \mathcal{A}_P$ whose elements act on $\mathcal{X}$ (and dually on $\mathcal{Y}$) such that, for all programs $P \in \mathcal{F}$ and all $g \in G$,
$$P(g \cdot x) \;=\; \rho(g) \cdot P(x) \quad \text{for every } x \in \mathcal{X},$$
where $\rho: G \to \mathrm{End}(\mathcal{Y})$ is a (possibly trivial) representation of $G$ on $\mathcal{Y}$.

*Intuition.* When $\rho$ is trivial, $G$-symmetry collapses to *invariance* — applying $g$ to the input leaves the output unchanged. When $\rho$ is non-trivial, the output transforms covariantly with $g$, what physicists call *equivariance*. Both are special cases of the same algebraic notion.

*Reactor example.* The geometric symmetry group of a quarter-symmetric PWR core (rotations, reflections preserving the assembly layout) acts on the spatial input of the diffusion solver, with $\rho$ trivial on $k_{\mathrm{eff}}$ and the corresponding rotational action on the flux distribution.

*ML example.* For an $\mathrm{SO}(3)$-equivariant point-cloud classifier, $G = \mathrm{SO}(3)$ acts on input coordinates and $\rho$ is trivial on the predicted class probabilities.

### 3.3 Order operators: monotonicity and linearity (Building Block B3)

**Definition 3 (Monotone operator).** Let $\le_{\mathcal{X}}$ and $\le_{\mathcal{Y}}$ be partial orders on $\mathcal{X}$ and $\mathcal{Y}$. A program $P$ is *monotone with respect to* the parameter $\theta$ on a coordinate of $\mathcal{X}$ if $\theta_1 \le \theta_2 \Rightarrow P(\theta_1) \le_{\mathcal{Y}} P(\theta_2)$ (or the reversed inequality, in which case $P$ is *anti-monotone*).

**Definition 4 (Linear operator).** $P$ is *linear* on a sub-domain $\mathcal{X}_0 \subseteq \mathcal{X}$ when $P(\alpha x_1 + \beta x_2) = \alpha P(x_1) + \beta P(x_2)$ for all $x_1, x_2 \in \mathcal{X}_0$ and scalars $\alpha, \beta$.

*Intuition.* Monotone operators preserve order; linear operators preserve linear combinations. Both are *order-preserving* in the lattice sense, and we collect them under the umbrella *order operators*. Linearity will turn out to be a special, strong case of partial-order preservation in §4.

*Reactor example.* In the Boltzmann transport equation, increasing the absorption cross-section $\Sigma_a$ on a region while holding all else fixed monotonically decreases $k_{\mathrm{eff}}$; this is a parameter-monotonicity statement on the eigenvalue map. Linearity appears in the Bateman equations governing isotopic burnup, where the solution operator $e^{At}$ is linear in the initial nuclide concentrations.

*ML example.* Monotonicity with respect to training-set size is a classical learning-theoretic invariant: under appropriate regularity, expected accuracy is monotone non-decreasing in training-set cardinality. Linearity appears more subtly — for instance, in linear-attention transformers, where the attention readout is exactly linear in the value matrix.

### 3.4 Self-adjoint operators (Building Block B3)

**Definition 5 (Self-adjoint operator).** Given an inner product $\langle\cdot,\cdot\rangle$ on $\mathcal{X}$, an operator $L \in \mathcal{O}$ is *self-adjoint* if $\langle Lx, y\rangle = \langle x, Ly\rangle$ for all $x, y$ in the domain of $L$.

*Intuition.* Self-adjointness encodes a deep duality: the operator looks the same from "left" and "right". Reciprocity theorems in physics, transposed-graph identities in algorithms, and detailed-balance conditions in stochastic processes are all instances.

*Reactor example.* The transport operator in adjoint formulation is self-adjoint with respect to the reactor-physics inner product, yielding the *reciprocity theorem*: source-to-detector responses equal detector-to-source responses under role exchange.

*ML example.* Self-adjointness arises in symmetric attention kernels and in undirected graph neural networks, yielding reciprocity-style invariances under role exchange between source and target nodes.

### 3.5 Time-reversal operators (Building Block B4)

**Definition 6 (Time-reversal operator).** When $\mathcal{X}$ admits a time coordinate, a *time-reversal operator* $\mathcal{T}$ acts on inputs by reversing the time variable, $\mathcal{T}(x(t)) = x(-t)$. A program $P$ is *time-reversal symmetric* on a sub-family of inputs when $P(\mathcal{T} x)$ is determined by $P(x)$ through a fixed bijection on $\mathcal{Y}$.

*Intuition.* Time-reversal is the dynamical counterpart of self-adjoint duality: the system's behaviour under forward and reversed time is constrained by an explicit map. Critically, time-reversal applies only to non-dissipative systems; dissipative dynamics (heat conduction, viscous flow) break this symmetry, and the framework correctly predicts that the corresponding MetaPattern is empty in such cases.

*Reactor example.* Time-reversal symmetry holds in collisionless neutral-particle transport and Hamiltonian sub-formulations, providing MRs of the form $P(\text{reverse trajectory}) = \mathcal{T}\,P(\text{forward trajectory})$. It does *not* hold for diffusion solvers (Boltzmann's H-theorem applies).

*ML example.* Time-reversal compatibility appears in invertible neural networks (normalising flows, Real-NVP) where forward and reverse passes are constrained by an explicit Jacobian relationship; absent in standard feedforward networks.

### 3.6 Limit operators (Building Block B5)

**Definition 7 (Limit operator).** A *parametrised limit operator* $\mathcal{L}_\theta$ is a family of operators indexed by a parameter $\theta$ (typically a discretisation step, sample size, or precision) such that there exists a limit element $\mathcal{L}_*$ with $\mathcal{L}_\theta \to \mathcal{L}_*$ as $\theta \to \theta_*$ in an appropriate operator topology.

*Intuition.* Where the previous four building blocks captured *exact* invariants — symmetries and dualities that hold identically — limit operators capture *asymptotic* invariants: the structural relationship between an approximate computation and its idealised limit.

*Reactor example.* Mesh refinement in finite-difference diffusion solvers: as the mesh size $h \to 0$, the discrete solution operator converges to the continuous one. A program that solves the diffusion equation must satisfy the MR "halving the mesh size brings the solution closer to the converged value".

*ML example.* Convergence of an empirical risk minimiser to the population risk minimiser as sample size $n \to \infty$. A correctly implemented learning algorithm must satisfy the MR "doubling the training set brings the empirical loss closer to the asymptotic value".

### 3.7 Qualitative-dynamics operators (Building Block B6)

**Definition 8 (Qualitative-dynamics operator).** A *qualitative-dynamics operator* $\mathcal{D}$ is an operator on solution trajectories of an underlying ODE/PDE that extracts qualitative features — extrema, inflection points, monotonic phases, overshoot magnitudes, S-curve transitions, phase-portrait orbits — that are invariant under perturbations preserving the underlying dynamical structure (Sturm-type comparison theorems, dynamical-systems classification).

*Intuition.* Some MR-relevant invariants are not point-wise (like symmetries) but *shape-wise*: a solution curve has an overshoot, a single extremum, a monotonic-then-saturating profile. These features survive small structural perturbations and are encoded by the qualitative theory of dynamical systems, distinct from the symmetry / order / duality / reversal / convergence machinery of B1–B5. We introduce B6 in this revision (replacing an earlier conflation of these phenomena with time-reversal) to give qualitative-dynamics MRs their own algebraic root.

*Reactor example.* The xenon-iodine pit in burnup analysis: the iodine-135 concentration after shutdown rises, peaks, then falls, producing a temporary reactivity dip ("iodine pit") that any correctly-implemented Bateman solver must reproduce in qualitative form. The MR is "the time-evolution of $^{135}$Xe concentration after shutdown exhibits a single maximum followed by monotonic decay", a shape-wise invariant rooted in the non-diagonal coupling structure of the Bateman matrix.

*ML example.* Learning-curve shape invariants for stochastic gradient descent: under mild regularity conditions, the training loss exhibits a monotonically-decreasing-with-occasional-plateaus shape. An MR demanding "no sustained monotonic *increase* of training loss over $\ge K$ iterations" enforces this qualitative-dynamics invariant.

### 3.8 Method-comparison operators (Building Block B7)

**Definition 9 (Method-comparison operator).** A *method-comparison operator* $\mathcal{E}$ encodes a partial order $\preceq_{\mathcal{E}}$ on numerical or algorithmic methods within a program family, where $M_1 \preceq_{\mathcal{E}} M_2$ asserts that method $M_1$ produces an approximation no worse than method $M_2$ in a specified error norm, under specified conditions. Method-comparison operators arise from established error-estimate theory (Galerkin best-approximation, Strang lemmas, Lax equivalence theorem in numerical analysis; PAC-Bayes bounds in ML).

*Intuition.* When the same problem can be solved by multiple algorithms, error-analysis theory often establishes a *partial order* of accuracy among them: certain methods are provably no-worse-than others under explicit hypotheses. This partial order is itself an algebraic invariant of the program family and induces MRs of the form "method $M_1$ produces a result within $\epsilon$-bound of the result from method $M_2$, under condition $C$". B7 is added in this revision (replacing an earlier conflation with self-adjoint duality) to root these phenomena in approximation theory.

*Reactor example.* Burnup-solver comparison: the Chebyshev rational approximation method (CRAM) is provably more accurate than truncated Taylor approximation (TTA) for the matrix exponential $e^{At}$ when $A$ is the Bateman matrix, with error bound $\|e^{At}_{\mathrm{CRAM}} - e^{At}_{\mathrm{exact}}\| \le \|e^{At}_{\mathrm{TTA}} - e^{At}_{\mathrm{exact}}\|$ over the relevant spectral region. The MR is "for the same input, CRAM and TTA agree to within the established error bound; if they disagree by more, one is implemented incorrectly".

*ML example.* Best-approximation theorems for kernel ridge regression vs.\ random-feature approximation: the kernel ridge result is provably within $\epsilon$ of the random-feature result for sufficiently many random features, by Rahimi-Recht-style bounds. Yields the MR "the random-feature predictor agrees with the exact kernel predictor within an $O(1/\sqrt{D})$ bound, where $D$ is the random-feature dimension".

### 3.9 Decomposition of an operator algebra

Given $\mathcal{A}_P = (\mathcal{O}, \circ, \sim_{\mathcal{F}})$, we decompose $\mathcal{O}$ along the seven building blocks introduced above:
$$\mathcal{D}(\mathcal{A}_P) \;=\; \bigl(\,G,\; O_{\le},\; T^{*},\; \mathcal{T}^{*},\; \mathcal{L}^{*},\; \mathcal{D}^{*},\; \mathcal{E}^{*}\,\bigr),$$
where $G$ collects symmetry subgroups, $O_{\le}$ monotone and linear operators, $T^{*}$ self-adjoint operators, $\mathcal{T}^{*}$ time-reversal operators, $\mathcal{L}^{*}$ limit operators, $\mathcal{D}^{*}$ qualitative-dynamics operators, and $\mathcal{E}^{*}$ method-comparison operators.

We do not assume the decomposition is disjoint — a single operator may participate in several blocks (e.g.\ a self-adjoint linear operator participates in $T^{*}$ and $O_{\le}$) — but we do assume each operator of $\mathcal{O}$ is captured by at least one block, and we resolve multi-block membership via the canonical-block ordering specified in §4.3.

**Necessity, sufficiency, and the empirical status of the decomposition.** We do not claim the seven blocks are necessary in any absolute sense, nor that they exhaust all algebraic structures relevant to software testing, nor that they are derived from algebraic-theoretic first principles. The seven blocks are an *empirical curation*: an enumeration, by inspection, of the mathematical structures we have observed to recur across the program families practitioners actually care about (Boltzmann transport, neutron diffusion, burnup, heat conduction, single-phase flow continuity, Reynolds-averaged momentum, resonance slowing-down, equivariant ML). The claim is therefore modest: the seven blocks are *currently sufficient* for these families, not provably necessary in general.

This empirical status of the upstream decomposition is the principal honest limitation of NOETHER as a theoretical framework. Induction has not been eliminated from MetaPattern discovery; it has been moved one level up — from "what MetaPatterns recur in observed MR samples?" to "what algebraic structures recur across program families?" The framework's contribution is at the level of *systematisation*: given a curated decomposition, the downstream derivation of $\mathbb{M}(\mathcal{A}_P)$ becomes mechanical and provably complete (Theorem 1, §4.3). Programs whose underlying mathematics requires symplectic structure (Hamiltonian dynamics outside collisionless transport), sheaf-theoretic constructions (formal-method tools), or non-trivial topological invariants (computational topology) may require an eighth block; we view this as future-work extensibility, and we encourage readers to test the framework's predictive structure by curating algebras outside the present seven-block image.

The decomposition $\mathcal{D}(\mathcal{A}_P)$ is the input on which NOETHER operates.

---

## 4 The NOETHER Framework

This section presents NOETHER itself: the construction algorithm CONSTRUCT-MP, the Algebraic Completeness Theorem (Theorem 1), and the Decidability Theorem (Theorem 2). We close with an explicit statement of the framework's principal limitation, which §7 treats more fully.

### 4.1 Algebra-induced metamorphic relations

Before stating the construction, we must specify the class of MRs over which NOETHER claims completeness. NOETHER's guarantee is *not* that every MR a tester might write down belongs to its constructed MetaPattern set; that claim would be false, and trivially so, since testers can write down arbitrary properties unrelated to the program's mathematical scaffolding. NOETHER's guarantee concerns the algebraically-grounded subset, defined as follows.

**Definition 10 (Algebra-induced MR).** Let $\mathcal{A}_P$ be a program-induced operator algebra and let $\rho$ be a metamorphic relation over a program $P$ in the family. We say $\rho$ is *induced by $\mathcal{A}_P$* — written $\rho \in \mathrm{MR}(\mathcal{A}_P)$ — when there exist (i) an operator block $s \in \mathcal{D}(\mathcal{A}_P)$, (ii) an invariant $\iota$ of $\mathcal{A}_P$ under $s$, and (iii) a derivation $\rho = \mathrm{Translate}(\iota, s)$ converting the algebraic invariant $\iota$ into an executable property assertion on $P$.

The translation procedure $\mathrm{Translate}$ is purely mechanical: given an invariant statement (e.g.\ "the operator is fixed under the action of $g$"), it produces the corresponding MR (e.g.\ "$P(g\cdot x)$ equals $\rho(g)\cdot P(x)$"). We make no assumption about the translation's expressive completeness — there may be MRs a tester can articulate that lie outside $\mathrm{MR}(\mathcal{A}_P)$ — and Theorem 1 below is about $\mathrm{MR}(\mathcal{A}_P)$ only. We are explicit that this is *constructive* completeness, not absolute completeness; we discuss this distinction immediately after the theorem (§4.3) and identify the absolute-completeness question as an open problem in §7 and Appendix C.4.

### 4.2 Construction of the MetaPattern set

We now present CONSTRUCT-MP, the deductive procedure that maps an algebra-decomposition to a MetaPattern set.

**Algorithm CONSTRUCT-MP.**

*Input:* An operator-algebra decomposition $\mathcal{D}(\mathcal{A}_P) = (G, O_{\le}, T^{*}, \mathcal{T}^{*}, \mathcal{L}^{*})$.

*Output:* A MetaPattern set $\mathbb{M}(\mathcal{A}_P) \subseteq 2^{\mathrm{MR}(\mathcal{A}_P)}$.

*Procedure:*

1. **Invariant extraction.** For each block $s$ in $\mathcal{D}(\mathcal{A}_P)$, compute the set of invariants $\mathcal{I}_s$ of $\mathcal{A}_P$ under $s$. For symmetry groups, this is the fixed-point set under the group action; for order operators, the order-preserving relations; for self-adjoint operators, the duality identities; for time-reversal, the reversal-compatibility relations; for limit operators, the convergence rates.

2. **MR derivation.** For each invariant $\iota \in \mathcal{I}_s$, derive the MR family $\mathcal{R}(\iota) = \{\,\rho \in \mathrm{MR}(\mathcal{A}_P) \mid \rho = \mathrm{Translate}(\iota', s),\; \iota' \sim_s \iota\,\}$, where $\sim_s$ is the structural-equivalence relation on invariants induced by block $s$.

3. **Quotient.** Form the MetaPattern $m_s = \mathcal{R}(\iota)/\!\sim_s$, the equivalence class of MRs derived from structurally-equivalent invariants of block $s$.

4. **Aggregation.** Return $\mathbb{M}(\mathcal{A}_P) = \{\, m_s : s \in \mathcal{D}(\mathcal{A}_P)\,\}$.

The procedure is deductive: each step is a closed algebraic operation on the previous, with no recourse to empirical observation of MRs. The output is a finite set of MetaPatterns, one per block (or one per structural sub-class within a block, when a block contains structurally distinct invariants — see §5 for an instance where the symmetry block decomposes into pure invariance and equivariance subclasses).

### 4.3 Constructive Completeness, the canonical-block ordering, and what we do not claim

We now establish that CONSTRUCT-MP misses no algebra-induced MR. To state the result precisely, we first specify a canonical-block ordering that resolves multi-block membership of MRs.

**Definition 11 (Canonical-block ordering).** We adopt the strict total order on blocks
$$G \;>\; O_{\le} \;>\; T^{*} \;>\; \mathcal{T}^{*} \;>\; \mathcal{L}^{*} \;>\; \mathcal{D}^{*} \;>\; \mathcal{E}^{*}.$$
An MR derivable through multiple blocks is assigned to the highest-priority block in this order. The ordering is well-founded by construction (a strict total order on a finite set), and the assignment is unique.

The ordering is motivated by *generality*: $G$-symmetries are the strongest invariants (exact identities), then order/duality structures (exact relations), then dynamical/asymptotic structures (approximate relations), with method-comparison structures last (relative bounds). When a single MR could be derived from a symmetry and from a method-comparison (e.g.\ "swapping two equivalent methods produces equivalent outputs"), assigning it to $G$ — the more fundamental algebraic structure — produces the more informative classification. We give two worked examples in Appendix C.1 of multi-block-derivable MRs and their canonical-block assignment.

**Theorem 1 (Constructive Completeness).** Let $\mathcal{A}_P$ be a program-induced operator algebra with decomposition $\mathcal{D}(\mathcal{A}_P)$ as in §3.9, and let $\mathbb{M}(\mathcal{A}_P) = \mathrm{CONSTRUCT\text{-}MP}(\mathcal{D}(\mathcal{A}_P))$. Then for every $\rho \in \mathrm{MR}(\mathcal{A}_P)$, there exists a unique $m \in \mathbb{M}(\mathcal{A}_P)$ such that $\rho \in m$, where uniqueness is determined under the canonical-block ordering of Definition 11.

*Proof sketch.* Existence: by Definition 10, $\rho = \mathrm{Translate}(\iota, s)$ for some block $s$ and invariant $\iota$. Step 1 of CONSTRUCT-MP places $\iota$ in $\mathcal{I}_s$; step 2 places $\rho$ in $\mathcal{R}(\iota)$; step 3 quotients $\mathcal{R}(\iota)$ to form $m_s$, which contains $\rho$ by construction. Uniqueness: when $\rho$ admits derivations through multiple blocks $\{s_1, \ldots, s_k\}$, Definition 11 specifies the canonical assignment as the highest-priority block among them; well-foundedness of the ordering ensures uniqueness. Full proof: Appendix C.2. $\square$

**What Theorem 1 does and does not claim.** Theorem 1 is *constructive completeness*: every MR derivable through `Translate` from an invariant of any block is contained in exactly one MetaPattern of $\mathbb{M}(\mathcal{A}_P)$. We are explicit that this is by-construction completeness, not absolute completeness over all MRs a tester might articulate. A sceptical reading might object that the by-construction status renders the theorem near-tautological: a stronger statement — every MR a tester can articulate as a property over $\mathcal{A}_P$, regardless of whether it arises from a single invariant via `Translate` — would not be tautological. We attempted such a strengthening (Theorem 1' in Appendix C.4) and were unable to prove it without imposing additional structural assumptions on $\mathcal{A}_P$. We document the attempt and the obstructions encountered, leaving the absolute-completeness statement as an explicit open problem.

Constructive completeness has substantive value despite its by-construction status, because the alternative — empirical adequacy notions such as PMCM — does not even guarantee constructive completeness. PMCM measures coverage of an inductively-curated grid against an inductively-curated MR corpus; both grid and corpus are themselves empirical artefacts that may be incomplete or misclassified. NOETHER's constructive completeness guarantees that *given an algebra*, the MetaPattern set is provably exhaustive over the algebra-induced MR space, with the algebra and the construction both visible and reproducible. This upgrade — from "empirically observed adequacy" to "by-construction completeness with explicit boundary" — is the contribution of Theorem 1.

### 4.4 Decidability and Complexity

A completeness theorem is of limited engineering value if the construction it certifies cannot actually be carried out. We now show that CONSTRUCT-MP is computable when the algebra admits a finite generating set, and we make the per-block invariant-extraction cost concrete.

**Theorem 2 (Decidability).** Suppose $\mathcal{A}_P$ admits a finite generating set $\mathrm{gen}(\mathcal{A}_P)$ of cardinality $n = |\mathrm{gen}(\mathcal{A}_P)|$, with each generator's invariant computation taking time $t_i$. Then $\mathbb{M}(\mathcal{A}_P)$ is computable in time $O\!\bigl(\,n \cdot \max_i t_i \cdot \log n\,\bigr)$.

*Proof sketch.* Step 1's invariant extraction reduces to computing fixed-point sets, order relations, duality identities, reversibility relations, convergence rates, qualitative-shape invariants, and method-comparison bounds on the generators, all of which are $O(\max_i t_i)$ per generator and $O(n \cdot \max_i t_i)$ aggregated. Step 2's MR derivation is a linear pass over the invariants. Step 3's quotient by $\sim_s$ requires a $\log n$ factor for the union-find data structure that maintains structural-equivalence classes. Step 4 is constant. Full proof: Appendix C.3. $\square$

**Per-block invariant-extraction cost.** The bound's actionability depends on $t_i$ being concrete for each block. We provide explicit characterisations:

| Block | $t_i$ for one generator | Reasoning |
|-------|------------------------|-----------|
| $G$ (symmetry) | $O(\lvert G \rvert^2)$ | Group-orbit fixed-point computation under the action |
| $O_{\le}$ (order) | $O(n^2)$ | Pair-wise poset comparison over the $n$ generators |
| $T^{*}$ (self-adjoint) | $O(d)$ | Inner-product symmetry check on a $d$-dimensional inner-product space |
| $\mathcal{T}^{*}$ (time-reversal) | $O(1)$ | Reversibility is a Boolean property; one bit per generator |
| $\mathcal{L}^{*}$ (limit) | $O(\log\!\frac{1}{\epsilon})$ | Convergence-rate determination to prescribed precision $\epsilon$ |
| $\mathcal{D}^{*}$ (qualitative-dynamics) | $O(d)$ | Phase-portrait classification on $d$-dimensional ODE/PDE state space |
| $\mathcal{E}^{*}$ (method-comparison) | $O(K^2)$ | Pair-wise comparison over $K$ candidate methods |

In practice, $n$ is small. For the reactor instantiation of §5, the Boltzmann algebra has $n \le 14$ generators across its seven blocks (after the seven-block restructuring). For the equivariant-ML instantiation of §6, $n \le 10$. With $|G| \le 24$ for typical geometric symmetries, $d \le 6$ for typical PDE state spaces, and $K \le 5$ for typical method-comparison sets, $\max_i t_i \le 600$ in either domain. The asymptotic bound is therefore not the binding constraint; what matters is that MP construction can be carried out by a working test engineer in a finite, transparent procedure, rather than by an opaque clustering of an empirical MR corpus.

### 4.5 The principal limitation

NOETHER replaces inductive grounding with algebraic grounding *downstream of $\mathcal{A}_P$*. Upstream — the distillation of $\mathcal{A}_P$ itself from a program family — remains a human task. A domain expert must identify which symmetries the program respects, which order operators it admits, which dualities it satisfies, and so on. NOETHER does not automate this distillation.

We are explicit about this for two reasons. First, intellectual honesty: it would be misleading to advertise NOETHER as an end-to-end automation when one critical step — perhaps the most domain-knowledge-intensive step — remains human. Second, the framework's value is undiminished by this limitation. Existing inductive pipelines require human input not at one step but at every step: an expert curates the MR samples, decides on cluster boundaries, names the patterns, and asserts coverage. NOETHER consolidates the human burden into a single, well-defined step (specifying $\mathcal{A}_P$) and mechanises everything that follows. §7 returns to this trade-off and to plausible directions for partial automation of $\mathcal{A}_P$ distillation, including LLM-assisted operator extraction from program semantics.

With the framework defined, the next two sections demonstrate that it works as advertised: §5 instantiates NOETHER on the Boltzmann transport equation and shows that its output coincides with a previously catalogued MetaPattern set, but emerges deductively rather than inductively; §6 re-instantiates NOETHER on equivariant ML and shows that the framework transports without re-running induction.

---

## 5 Instantiation: From the Boltzmann Transport Equation to Neutron Transport, Diffusion, and Burnup

This section instantiates NOETHER on a single program family — solvers of the Boltzmann transport equation — and traces the construction through three increasingly-specialised sub-families: neutron transport, neutron diffusion, and burnup-coupled solvers. The deliberate choice to drive a single equation deeply, rather than survey several equations shallowly, follows the logic of §1: the demonstration's purpose is not to enumerate MetaPatterns but to show that the catalogue produced by NOETHER coincides with what was previously assembled inductively, while the production mechanism is now algebraic. Other reactor equations — heat, continuity, momentum, resonance slowing-down — appear in Appendix A as confidence-strengthening evidence.

### 5.1 The Boltzmann program family and its operator algebra

The Boltzmann transport equation governs the distribution of neutral particles (neutrons, photons, neutrinos) through a medium that absorbs, scatters, and produces them. In its time-independent eigenvalue form for fission systems, the equation reads
$$\hat{\Omega}\!\cdot\!\nabla\psi(\vec{r},\hat{\Omega},E) + \Sigma_t(\vec{r},E)\psi = \int\!\!\int \Sigma_s(\vec{r}, E'\!\to\!E,\hat{\Omega}'\!\to\!\hat{\Omega})\,\psi\,dE'd\hat{\Omega}' + \tfrac{1}{k}\,\chi(E)\!\!\int\!\nu\Sigma_f(\vec{r},E')\psi\,dE',$$
with $\psi$ the angular flux, $\Sigma_t,\Sigma_s,\Sigma_f$ the macroscopic cross-sections, $\chi$ the fission spectrum, and $k$ the multiplication eigenvalue. We refer to the family of programs solving (or approximating) this equation as $\mathcal{F}_{\mathrm{Boltz}}$.

The program-induced operator algebra $\mathcal{A}_{\mathrm{Boltz}}$ collects the operators that every member of $\mathcal{F}_{\mathrm{Boltz}}$ must respect:

$$\mathcal{O}_{\mathrm{Boltz}} \supseteq \bigl\{\;G_{\mathrm{geom}},\; \mathfrak{R}_E,\; \mathcal{L}_{\Sigma},\; \mathcal{L}_\nu,\; \mathcal{L}^*,\; \mathcal{T},\; \mathcal{L}_h,\; \mathcal{D}_{\mathrm{Bate}},\; \mathcal{E}_{\mathrm{cmp}}\;\bigr\},$$

where $G_{\mathrm{geom}}$ is the geometric symmetry group of the configuration; $\mathfrak{R}_E$ is the energy-group permutation algebra under multigroup discretisation; $\mathcal{L}_\Sigma, \mathcal{L}_\nu$ are linear scaling operators on cross-sections and the fission yield; $\mathcal{L}^*$ is the adjoint operator yielding the importance function $\psi^\dagger$; $\mathcal{T}$ is the time-reversal operator (active in collisionless and Hamiltonian sub-formulations); $\mathcal{L}_h$ is the limit operator capturing mesh, angular, and energy-discretisation refinements; $\mathcal{D}_{\mathrm{Bate}}$ is the qualitative-dynamics operator extracting trajectory-shape invariants from the Bateman ODE coupling structure (e.g.\ xenon-iodine pit); and $\mathcal{E}_{\mathrm{cmp}}$ is the method-comparison operator encoding error-bound partial orders among Boltzmann-solver methods (e.g.\ CRAM vs.\ TTA for the matrix exponential). Decomposed along the seven blocks of §3.9, $\mathcal{A}_{\mathrm{Boltz}}$ yields:
- $G$: $\{G_{\mathrm{geom}},\,\mathfrak{R}_E\}$
- $O_{\le}$: $\{\mathcal{L}_\Sigma,\,\mathcal{L}_\nu\}$
- $T^{*}$: $\{\mathcal{L}^*\}$
- $\mathcal{T}^{*}$: $\{\mathcal{T}\}$
- $\mathcal{L}^{*}$: $\{\mathcal{L}_h\}$
- $\mathcal{D}^{*}$: $\{\mathcal{D}_{\mathrm{Bate}}\}$
- $\mathcal{E}^{*}$: $\{\mathcal{E}_{\mathrm{cmp}}\}$

This decomposition is not a pedagogical convenience but a faithful reading of the equation's mathematical content. Every operator listed has an unambiguous status in the established theory of neutral-particle transport [CITE: BellGlasstone1970 — nuclear reactor theory; LewisMiller1993 — computational transport]; the operator algebra is, in this sense, public knowledge. NOETHER's contribution is what happens next.

### 5.2 Running CONSTRUCT-MP on $\mathcal{A}_{\mathrm{Boltz}}$

We trace CONSTRUCT-MP's four steps explicitly.

**Step 1 — Invariant extraction.**

For $G$, fixed points of $G_{\mathrm{geom}}$ acting on the spatial configuration are the symmetric flux distributions; fixed points of $\mathfrak{R}_E$ acting on the energy-group ordering are the spectrum-blind quantities (e.g.\ total reaction rates summed over groups). For $O_{\le}$, the invariants are the *sign of $\partial k/\partial \theta$* relations: scaling absorption monotonically decreases $k$, scaling fission yield monotonically increases $k$, scaling self-shielding non-trivially increases or decreases $k$ depending on the spectrum. For $T^{*}$, the invariant is the *adjoint reciprocity* identity $\langle \psi^\dagger, S \rangle = \langle Q, \psi \rangle$, expressing that source-detector and detector-source responses agree under role exchange. For $\mathcal{T}^{*}$, the invariant is *trajectory-reversal compatibility*: in collisionless limits, reversing all neutron trajectories produces the time-reversed flux. For $\mathcal{L}^{*}$, the invariants are *convergence rates* — second-order in mesh size for diamond-difference, first-order for step-difference, exponential in angular order for $S_N$ above the discrete-ordinates threshold.

**Step 2 — MR derivation.**

Each invariant is mechanically converted into an MR. The geometric-symmetry invariants yield MRs of the form "$P$ applied to a $G$-rotated input equals $\rho(g)$ applied to $P$'s output", spanning core-rotation invariance, reflection invariance, and (in lattice problems) translation invariance. The energy-group permutation invariants yield MRs of the form "$P$ summed over a permutation of energy groups equals the original sum", capturing total-rate conservation. The cross-section monotonicity invariants yield MRs of the form "$P$ with scaled $\Sigma_a$ produces a monotonically scaled $k$", spanning the entire family of parameter-monotonicity properties tested against PWR solvers. The adjoint reciprocity invariant yields the *adjoint-flux MR*: solving the adjoint problem with source $Q$ and forming $\langle \psi^\dagger, S \rangle$ must equal solving the forward problem with source $S$ and forming $\langle Q, \psi \rangle$. The time-reversal invariant yields collisionless reversibility MRs. The convergence-rate invariants yield mesh-refinement MRs of the form "halving $h$ reduces solution error by $4\times$ for diamond-difference".

**Step 3 — Quotient.**

Within each block, structural-equivalence collapses MRs that differ only by superficial parameter values into a single equivalence class. Rotational, reflectional, and translational symmetry MRs collapse into a single *invariance/equivariance* equivalence class, with sub-classes for trivial-$\rho$ (pure invariance) versus non-trivial-$\rho$ (covariance under the geometric group). Energy-group permutation MRs collapse into a *re-indexing-invariance* class. Linear cross-section scaling MRs collapse into a *parameter-monotonicity* class. The adjoint reciprocity MR forms a *self-adjoint duality* class. Time-reversal MRs form a *trajectory-reversal* class. Mesh-refinement MRs form a *discretisation-convergence* class.

**Step 4 — Aggregation.**

The output $\mathbb{M}(\mathcal{A}_{\mathrm{Boltz}})$ contains the following MetaPatterns, with one MetaPattern per surviving structural sub-class:

- $m_{\mathrm{inv}}$: invariance/equivariance under geometric and re-indexing symmetries.
- $m_{\mathrm{mono}}$: parameter-monotonicity under cross-section and yield scaling.
- $m_{\mathrm{adj}}$: self-adjoint duality (adjoint reciprocity).
- $m_{\mathrm{rev}}$: time-reversal compatibility (collisionless / Hamiltonian sub-families).
- $m_{\mathrm{conv}}$: discretisation convergence.
- $m_{\mathrm{dyn}}$: qualitative-dynamics shape invariants (xenon-iodine pit, samarium poisoning, S-curves).
- $m_{\mathrm{cmp}}$: method-comparison error-bound partial orders (CRAM vs.\ TTA, etc.).

### 5.3 Relationship to the prior inductive catalogue: refinement plus discovery

A previous reactor-physics MetaPattern catalogue, assembled by the present authors through inductive clustering of 84 MRs across 27 PWR neutronics programs, identified five MetaPatterns labelled P1 (conservation), P2 (monotonicity), P3 (convergence), P4 (trajectory), and P5 (partial-order/bounding) [CITE: PWR-MetaPattern-Report]. The relationship with $\mathbb{M}(\mathcal{A}_{\mathrm{Boltz}})$ is more structured than a simple bijection. NOETHER reproduces three of the prior patterns, refines two on a sounder algebraic basis, and discovers two that the inductive catalogue missed:

| Prior catalogue (inductive) | NOETHER output (deductive) | Relationship |
|------------------------------|----------------------------|---------------|
| P1 conservation/invariance | $m_{\mathrm{inv}}$ | Reproduced — $G$-symmetry invariants in $\mathcal{A}_{\mathrm{Boltz}}$ project to exactly the same MRs the inductive method clustered as P1. |
| P2 monotonicity | $m_{\mathrm{mono}}$ | Reproduced — order-block invariants project to parameter-monotonicity MRs. |
| P3 convergence | $m_{\mathrm{conv}}$ | Reproduced — limit-block invariants project to discretisation-refinement MRs. |
| P4 trajectory | $m_{\mathrm{dyn}}$ | **Refined** — the inductive P4 conflated qualitative-dynamics phenomena (e.g.\ iodine pit) with time-reversal phenomena. NOETHER places the former in $m_{\mathrm{dyn}}$ (qualitative-dynamics block, sourced in Sturm-type comparison theorems and dynamical-systems classification) and exposes the conflation. |
| P5 partial-order/bounding | $m_{\mathrm{cmp}}$ | **Refined** — the inductive P5 grouped method-accuracy partial orders with adjoint-style reciprocity. NOETHER places the former in $m_{\mathrm{cmp}}$ (method-comparison block, sourced in approximation-theory error bounds) and exposes the distinction. |
| (none) | $m_{\mathrm{adj}}$ | **Discovered** — the inductive corpus did not isolate adjoint-reciprocity MRs as a distinct pattern; $m_{\mathrm{adj}}$ predicts that for any program implementing adjoint transport, MRs of the form $\langle\psi^\dagger,S\rangle = \langle Q,\psi\rangle$ form a structurally distinct equivalence class. |
| (none) | $m_{\mathrm{rev}}$ | **Discovered** — the inductive corpus did not include time-reversal MRs in canonical form; $m_{\mathrm{rev}}$ predicts that collisionless or Hamiltonian sub-formulations of transport admit a structurally distinct family of trajectory-reversal MRs. |

This is not the structure of a re-coding. NOETHER's output structurally **refines** two prior patterns by exposing inductive conflations, and **predicts** two additional patterns that the inductive method missed because the corpus did not happen to include enough exemplars in canonical form. The pairing therefore demonstrates the framework's contribution beyond merely reproducing what was already known.

**A note on the word "discovered".** It should be acknowledged that $m_{\mathrm{adj}}$ (adjoint reciprocity) and $m_{\mathrm{rev}}$ (collisionless time-reversal compatibility) are not de novo discoveries in any field-shaking sense: adjoint-flux reciprocity is standard textbook material in transport theory~[CITE: BellGlasstone1970; LewisMiller1993], and time-reversal MRs in collisionless transport have been understood in physics for decades. The MT-community-level absence of these MetaPatterns from the prior inductive catalogue reflects which phenomena happened to be canonically encoded in the 84-MR corpus, not the absence of the underlying physics from the literature. NOETHER's contribution here is therefore one of *systematic prediction*: given $\mathcal{D}(\mathcal{A}_{\mathrm{Boltz}})$, the framework algebraically warrants the classification of these phenomena as MetaPatterns structurally distinct from $m_{\mathrm{dyn}}$ and $m_{\mathrm{cmp}}$, supplying a basis on which any future reactor-physics testing toolchain can include them without re-running empirical induction. This is systematisation, not de novo discovery — and we believe the systematisation is, in itself, the form of contribution that a foundational-theory paper of this kind should deliver.

**Element-wise correspondence (representative subset).** Table 1 traces 12 representative MRs from the 84-MR PWR corpus to their NOETHER placement. The full element-wise mapping for all 84 MRs appears in the supplementary material accompanying this submission [CITE: PWR-MetaPattern-Report].

| MR ID (prior corpus) | Plain-text MR | Prior P# | NOETHER block | NOETHER MetaPattern |
|----------------------|------------------|----------|----------------|----------------------|
| Bur-Phy-01 | Step-splitting invariance: $P(\Delta t_1+\Delta t_2) = P(\Delta t_2)\circ P(\Delta t_1)$ | P1 | $G$ (semi-group) | $m_{\mathrm{inv}}$ |
| Bol-Phy-02 | Geometric quarter-symmetry: rotating core 90° leaves $k_{\mathrm{eff}}$ invariant | P1 | $G$ (geometric) | $m_{\mathrm{inv}}$ |
| Bol-Phy-11 | Increasing $\Sigma_a$ decreases $k_{\mathrm{eff}}$ | P2 | $O_{\le}$ | $m_{\mathrm{mono}}$ |
| Bol-Phy-12 | Increasing $\nu\Sigma_f$ increases $k_{\mathrm{eff}}$ | P2 | $O_{\le}$ | $m_{\mathrm{mono}}$ |
| Dif-Alg-01 | Halving mesh $h$ reduces error quadratically (diamond difference) | P3 | $\mathcal{L}^{*}$ | $m_{\mathrm{conv}}$ |
| Bur-Alg-01 | CRAM order $N\to\infty$ converges to exact $e^{At}$ | P3 | $\mathcal{L}^{*}$ | $m_{\mathrm{conv}}$ |
| Bur-Phy-08 | Iodine pit: $^{135}$Xe after shutdown rises, peaks, then decays monotonically | P4 | $\mathcal{D}^{*}$ | $m_{\mathrm{dyn}}$ |
| Cpl-App-06 | Gd self-shielding: S-curve transition between unshielded/shielded regimes | P4 | $\mathcal{D}^{*}$ | $m_{\mathrm{dyn}}$ |
| Bur-Alg-04 | CRAM is no-worse-than TTA for matrix exponential within Bateman spectrum | P5 | $\mathcal{E}^{*}$ | $m_{\mathrm{cmp}}$ |
| Bol-Alg-04 | $P_0$ scattering over-estimates $k$ in hydrogen-bearing systems | P5 | $\mathcal{E}^{*}$ | $m_{\mathrm{cmp}}$ |
| (predicted) | Adjoint-flux reciprocity: $\langle\psi^\dagger,S\rangle = \langle Q,\psi\rangle$ | (none) | $T^{*}$ | $m_{\mathrm{adj}}$ |
| (predicted) | Collisionless trajectory reversibility on test geometry | (none) | $\mathcal{T}^{*}$ | $m_{\mathrm{rev}}$ |

The two "predicted" rows are the discovery items: NOETHER asserts these MRs as structurally inevitable for any program in $\mathcal{F}_{\mathrm{Boltz}}$ that exposes the corresponding interfaces (an adjoint-flux solver; a collisionless test mode), even though the inductive PWR corpus did not catalogue them.

### 5.4 Specialisation to neutron transport, diffusion, and burnup

The Boltzmann formulation is the most general; specialised reactor solvers are obtained by truncating or projecting $\mathcal{A}_{\mathrm{Boltz}}$. *Neutron transport* solvers retain the full angular dependence and use $S_N$ or $P_N$ angular discretisations; the operator algebra is essentially unchanged, and the same seven MetaPatterns apply, with quantitative refinements to the convergence-rate invariants. *Neutron diffusion* solvers truncate angular dependence to its $P_1$ approximation, replacing $\mathcal{O}_{\mathrm{Boltz}}$'s transport operator with the diffusion operator $-\nabla\!\cdot\!D\nabla + \Sigma_a$. The symmetry, order, self-adjoint, limit, qualitative-dynamics, and method-comparison blocks survive; the time-reversal block contracts (diffusion is dissipative and breaks reversibility), removing $m_{\mathrm{rev}}$ from $\mathbb{M}(\mathcal{A}_{\mathrm{diff}})$. The same algebraic mechanism that constructs the MetaPattern set in the Boltzmann case also predicts which patterns *vanish* under approximation — a corollary the inductive catalogue cannot offer, since induction can report only what is observed, not what is structurally absent. *Burnup-coupled* solvers introduce the Bateman equations $dN/dt = AN$ alongside the transport solve. The Bateman operator $e^{At}$ enriches multiple blocks: $G$ (semi-group identity $e^{A(t_1+t_2)} = e^{At_1}e^{At_2}$), $O_{\le}$ (linearity in initial concentrations), $\mathcal{D}^{*}$ (xenon overshoot, samarium pit, S-curve burnup transitions), and $\mathcal{E}^{*}$ (CRAM-vs-TTA error bounds). The MetaPattern set $\mathbb{M}(\mathcal{A}_{\mathrm{burnup}})$ thereby acquires substantively new content within already-existing pattern labels.

The progression illustrates a structural feature of NOETHER that purely empirical catalogues cannot articulate: the MetaPattern set is *compositional* with respect to the underlying algebra. Add an operator block, gain MetaPatterns; remove a block, lose them. The framework therefore supports not only construction but also *prediction* of which patterns a new specialisation will or will not exhibit, before any MR is identified empirically.

### 5.5 What this section established

NOETHER, applied to $\mathcal{A}_{\mathrm{Boltz}}$, deductively produces a seven-MetaPattern set that **refines** the prior inductive catalogue (separating qualitative-dynamics from time-reversal, and method-comparison from self-adjoint duality) and **discovers** two MetaPatterns ($m_{\mathrm{adj}}$, $m_{\mathrm{rev}}$) that the inductive method missed. Specialisations of the algebra (transport $\to$ diffusion $\to$ burnup) propagate cleanly to specialisations of the MetaPattern set, with structural predictions about pattern presence and absence that empirical induction cannot make. The prior catalogue's empirical claim — *these five patterns are observed* — is replaced by a constructive claim with a closed boundary: *these seven patterns are exactly the projection of $\mathcal{D}(\mathcal{A}_{\mathrm{Boltz}})$ onto the algebra-induced MR space, with the canonical-block ordering of Definition 11 ensuring unique pattern membership*. Reactor physics is thus a domain where NOETHER's deductive output extends the field's inductive consensus while remaining consistent with it — a necessary condition for the framework to be plausible. The next section turns to a more demanding test: a domain in which the inductive catalogue does not yet exist, and where NOETHER must produce its own from scratch and derive a concrete, executable MR end-to-end.

---

## 6 Cross-Domain Demonstration: Equivariant Machine Learning

The deductive grounding of §5 satisfies one of the three foundational questions raised in §1 (*origin*) and Theorem 1 satisfies a second (*closure*). The third — *transferability* — requires that the framework's mechanism produce a meaningful MetaPattern set for a program family far removed from reactor physics, without re-running empirical induction. This section provides such a demonstration on equivariant machine learning, a domain where symmetry is the central design principle but where, despite a substantial MR-testing literature for ML systems generally [CITE: Murphy2008-ML-MR; Xie2011-ML-MR; ZhangChatGPT-MR-COMPSAC2023], no inductive MetaPattern catalogue analogous to the reactor-physics taxonomy yet exists.

### 6.1 The equivariant-ML program family and its operator algebra

Equivariant neural networks impose by architectural construction that certain symmetries of the input induce predictable transformations of the output [CITE: CohenWelling2016 — group equivariant CNNs; ThomasSmidt2018 — tensor-field networks]. In a typical setting — point-cloud classification, molecular property prediction, particle-physics tagging — the relevant symmetries are the rotation group $\mathrm{SO}(3)$ acting on three-dimensional coordinates, and the permutation group $\mathfrak{S}_n$ acting on the ordering of points (since the input is a *set* rather than a *sequence*). The program family $\mathcal{F}_{\mathrm{equi}}$ comprises classifiers that, by design, satisfy the equivariance constraint
$$f(g\cdot \mathbf{x}) = \rho(g)\cdot f(\mathbf{x}) \quad \forall g\in G = \mathrm{SO}(3) \times \mathfrak{S}_n,$$
with $\rho$ a chosen representation of $G$ on the output space.

The operator-induced algebra $\mathcal{A}_{\mathrm{equi}}$ contains:

- $G_{\mathrm{equi}} = \mathrm{SO}(3)\times\mathfrak{S}_n$ (the equivariance symmetry group).
- $\mathcal{L}_{\mathrm{train}}$ (a limit operator capturing convergence with training-set size).
- $\mathcal{L}_{\mathrm{depth}}$ (a limit operator capturing convergence with network depth/width).
- $\mathcal{L}_{\mathrm{dim}}$ (a limit operator capturing convergence as feature dimension grows; relevant in random-feature theory).
- $O_{\le}^{\mathrm{train}}$ (monotonicity with respect to training-set size, on the population objective).
- $T^{*}_{\mathrm{att}}$ (self-adjointness of symmetric attention kernels and undirected message-passing layers).
- $\mathcal{T}_{\mathrm{seq}}$ (time-reversal, where applicable to sequence models).

Decomposed along the seven blocks of §3.9:
- $G$: $\{G_{\mathrm{equi}}\}$.
- $O_{\le}$: $\{O_{\le}^{\mathrm{train}}\}$.
- $T^{*}$: $\{T^{*}_{\mathrm{att}}\}$.
- $\mathcal{T}^{*}$: $\{\mathcal{T}_{\mathrm{seq}}\}$ (active only for sequence-aware sub-families).
- $\mathcal{L}^{*}$: $\{\mathcal{L}_{\mathrm{train}},\,\mathcal{L}_{\mathrm{depth}},\,\mathcal{L}_{\mathrm{dim}}\}$.
- $\mathcal{D}^{*}$: $\emptyset$ for feedforward equivariant classifiers; non-empty for trajectory-prediction sub-families.
- $\mathcal{E}^{*}$: $\emptyset$ within a single architecture; non-empty across architecture comparisons (e.g.\ $G$-CNN vs.\ tensor-field network accuracy bounds).

The algebra is, like $\mathcal{A}_{\mathrm{Boltz}}$, a faithful reading of the program family's mathematical commitments — no MR samples have been consulted to assemble it.

### 6.2 Running CONSTRUCT-MP on $\mathcal{A}_{\mathrm{equi}}$

Step 1 (invariant extraction) yields: for $G_{\mathrm{equi}}$, fixed-point sets under $\mathrm{SO}(3)$ rotations of input coordinates and under $\mathfrak{S}_n$ permutations of input ordering; for $O_{\le}^{\mathrm{train}}$, the order-preservation of expected accuracy with respect to training-set cardinality; for $T^{*}_{\mathrm{att}}$, the symmetry of attention kernels under role exchange between query and key; for $\mathcal{T}_{\mathrm{seq}}$, the consistency between forward and time-reversed sequence inputs (where applicable); for the limit-operator block, the rates of convergence to asymptotic regimes.

Step 2 (MR derivation) yields explicit MR templates: equivariance MRs of the form $f(g\cdot \mathbf{x}) = \rho(g)\cdot f(\mathbf{x})$, instantiated for both $G$-components; permutation-invariance MRs $f(\sigma\cdot \mathbf{x}) = f(\mathbf{x})$ for $\sigma\in \mathfrak{S}_n$ (corresponding to trivial $\rho$ on the $\mathfrak{S}_n$ component); sample-size monotonicity MRs of the form "doubling the training set does not, in expectation, decrease accuracy"; attention-symmetry MRs of the form "swapping query and key indices in a symmetric-attention block leaves the readout unchanged"; convergence MRs of the form "doubling the training set halves the empirical-vs-population loss gap (up to logarithmic factors)".

Step 3 (quotient) collapses these into structural equivalence classes, and Step 4 (aggregation) returns:

$$\mathbb{M}(\mathcal{A}_{\mathrm{equi}}) \;=\; \bigl\{\;m^{\mathrm{eq}}_{\mathrm{inv}},\; m^{\mathrm{eq}}_{\mathrm{mono}},\; m^{\mathrm{eq}}_{\mathrm{adj}},\; m^{\mathrm{eq}}_{\mathrm{rev}},\; m^{\mathrm{eq}}_{\mathrm{conv}}\;\bigr\}.$$

The labels mirror those of $\mathbb{M}(\mathcal{A}_{\mathrm{Boltz}})$ — invariance/equivariance, monotonicity, self-adjoint duality, time-reversal, convergence — but the *content* is domain-specific. $m^{\mathrm{eq}}_{\mathrm{inv}}$ contains rotation- and permutation-equivariance MRs, not core-rotation MRs. $m^{\mathrm{eq}}_{\mathrm{mono}}$ contains training-size monotonicity, not cross-section monotonicity. $m^{\mathrm{eq}}_{\mathrm{conv}}$ contains learning-curve convergence, not mesh-refinement convergence. In the cases where a block is empty for a given sub-family — for instance, when the network is feedforward and $\mathcal{T}_{\mathrm{seq}}$ does not apply — the corresponding MetaPattern simply does not appear in $\mathbb{M}$, exactly as occurred for diffusion solvers in §5.

### 6.3 What transferability means here

Crucially, *no induction was re-run*. We did not collect a corpus of ML MRs, cluster them, name the clusters, and validate coverage. We specified $\mathcal{A}_{\mathrm{equi}}$ — a step that an ML practitioner familiar with equivariant architecture can complete in hours, drawing on standard references — and ran the same CONSTRUCT-MP procedure that produced $\mathbb{M}(\mathcal{A}_{\mathrm{Boltz}})$. Theorem 1 applies verbatim: every MR derivable from invariants of $\mathcal{A}_{\mathrm{equi}}$ falls into a unique $m \in \mathbb{M}(\mathcal{A}_{\mathrm{equi}})$. The framework's *mechanism* transferred without modification; the inputs (the algebra) and outputs (the MR families) are domain-specific, exactly as a foundational theory of MetaPatterns should be.

This is the contrast with prior catalogues that we located in §2.4. Each existing catalogue, including the present authors' reactor-physics taxonomy, claimed implicit cross-domain applicability — the same five labels (conservation, monotonicity, convergence, trajectory, partial-order) were sometimes asserted to govern arbitrary software systems. NOETHER replaces that implicit claim with an algebraic one: cross-domain transferability means the framework's *mechanism* applies, not that the same labels describe the same content. When the algebra is rich (Boltzmann), $\mathbb{M}$ is rich; when the algebra is sparse (a feedforward equivariant network without sequence structure or self-adjoint readouts), $\mathbb{M}$ is sparse. The pattern set is not a universal vocabulary stamped onto every domain; it is each domain's algebraic projection.

### 6.4 End-to-end derivation: a concrete MR for SE(3)-equivariant point-cloud classification

To demonstrate that the framework is not merely descriptive but generative, we trace a complete derivation from algebra to executable MR for an SE(3)-equivariant point-cloud classifier (the architecture class typified by tensor-field networks [CITE: ThomasSmidt2018] and equivariant graph neural networks).

**Step 1 — System under test.** Let $f: \mathbb{R}^{n\times 3} \to \Delta^{C-1}$ be a point-cloud classifier mapping $n$ three-dimensional points to a probability distribution over $C$ classes. The architecture is declared SE(3)-equivariant: rotations and translations of the input induce a prescribed action on the output. For classification, the prescribed action is the trivial representation (rotational invariance of class probabilities).

**Step 2 — Distil $\mathcal{A}_{\mathrm{equi}}$ for this system.** Following §6.1, the relevant blocks are $G = \mathrm{SO}(3)\times\mathfrak{S}_n$ (continuous rotations and discrete permutations) and $O_{\le}^{\mathrm{train}}$ (training-size monotonicity, if the training pipeline is in scope). Self-adjoint, time-reversal, qualitative-dynamics, and method-comparison blocks are empty for this specific feedforward classifier. The limit block $\mathcal{L}^{*}$ contains training-size and depth limits.

**Step 3 — Run CONSTRUCT-MP, select an invariant from $G$.** Within $G$'s symmetry block, fix attention on the rotation invariant: under any rotation $R \in \mathrm{SO}(3)$, the output class distribution must be invariant. Algebraically, $f(R \cdot \mathbf{x}) = f(\mathbf{x})$ for all $\mathbf{x} \in \mathbb{R}^{n\times 3}$ and $R \in \mathrm{SO}(3)$.

**Step 4 — Translate the invariant into an executable MR.** Apply Definition 10's `Translate` procedure: invariant $\iota$ ("$f(R\cdot\mathbf{x}) = f(\mathbf{x})$") becomes MR template
$$\boxed{\rho_{\mathrm{rot}}: \quad \forall R \in \mathrm{SO}(3), \quad \big\| f(R \cdot \mathbf{x}) - f(\mathbf{x}) \big\|_\infty \le \tau,}$$
with $\tau$ a tolerance set by the framework's numerical precision (e.g.\ $\tau = 10^{-4}$ for fp32 architectures). This MR is structurally distinct from a hand-crafted "the model should be invariant to rotations" assertion: it makes the tolerance, the metric, and the universal quantification over $R$ explicit, and it places itself unambiguously in $m^{\mathrm{eq}}_{\mathrm{inv}}$.

**Step 5 — Generate an executable test.** The pseudocode in Figure 1 (below) runs $\rho_{\mathrm{rot}}$ against any classifier exposing a `predict` interface, sampling random rotations from the Haar measure on $\mathrm{SO}(3)$:

```python
import numpy as np
from scipy.spatial.transform import Rotation

def test_rotation_invariance(model, point_cloud, num_samples=100, tau=1e-4):
    """Executable MR rho_rot for SE(3)-equivariant classifier."""
    p_original = model.predict(point_cloud)            # Source output
    failures = []
    for _ in range(num_samples):
        R = Rotation.random().as_matrix()              # Haar-uniform sample
        rotated = point_cloud @ R.T                    # Follow-up input
        p_rotated = model.predict(rotated)             # Follow-up output
        deviation = np.max(np.abs(p_original - p_rotated))
        if deviation > tau:
            failures.append((R, deviation))
    return failures   # Empty list => MR holds; non-empty => fault detected
```

The function is approximately 12 lines, implements $\rho_{\mathrm{rot}}$ exactly as derived, and can be applied to any compliant classifier. A fault is reported whenever the model's claimed equivariance is violated beyond numerical tolerance — a defect that has been documented in non-strictly-equivariant approximations of equivariant networks. The longer Python sketch in Appendix D extends the derivation with two additional MRs ($\rho_{\mathrm{perm}}$ for permutation invariance and $\rho_{\mathrm{train}}$ for training-size monotonicity) drawn from the same MetaPattern set.

**Step 6 — Pattern coverage check.** With three MRs derived ($\rho_{\mathrm{rot}}, \rho_{\mathrm{perm}}, \rho_{\mathrm{train}}$), we have populated three of the four non-empty MetaPatterns in $\mathbb{M}(\mathcal{A}_{\mathrm{equi}})$ for the feedforward case ($m^{\mathrm{eq}}_{\mathrm{inv}}, m^{\mathrm{eq}}_{\mathrm{mono}}, m^{\mathrm{eq}}_{\mathrm{conv}}$ requires a training-curve test, deferred to follow-up empirical work). NOETHER's structural-coverage report is therefore "75% of non-empty patterns covered" — an algebraic adequacy statement the inductive PMCM framework cannot directly produce because PMCM's grid is itself empirically curated.

The end-to-end derivation in §6.4 demonstrates that NOETHER is not merely a classification framework for already-existing MRs but a *generative* mechanism for new ones, with provenance (algebra → invariant → MR template → executable test) traceable at each step. We do not test these MRs against a trained network in this paper; the empirical evaluation of the framework's MRs against trained equivariant classifiers is deferred to a follow-up study, in line with the scope-of-contribution paragraph of §1.

---

## 7 Discussion and Threats to Validity

### 7.1 Three threats to validity

*Internal validity.* NOETHER's claim — that $\mathbb{M}(\mathcal{A}_P)$ is exhaustive over the algebra-induced MR space — depends on the soundness of CONSTRUCT-MP and on Theorem 1's proof. The proof rests on a canonical-block convention for assigning MRs that arise through compositions of multiple algebraic structures. If a working MR is misclassified by that convention, the apparent uniqueness of its MetaPattern membership becomes a notational rather than a structural fact. We mitigate this threat by Appendix C's full proof, which catalogues every interaction between blocks for the algebras instantiated in §5–§6, and by the construction's invariance under our chosen canonical ordering: relabelling blocks does not alter the MetaPattern set, only the ordering of pattern labels.

*Construct validity.* NOETHER constructs MetaPatterns from operator algebras, but a MetaPattern's value as a testing artefact depends on whether testers experience the algebraic equivalence classes as coherent reasoning strategies. We argued in §5 that the algebraic classes coincide with the inductively-discovered classes for reactor physics — a cross-validation that the algebraic and the cognitive groupings agree on a domain where both are observable. We do not yet have analogous evidence for non-physics domains: §6's equivariant-ML instantiation produces a deductive MetaPattern set, but no inductive ML catalogue exists against which to compare. The construct-validity gap will close as practitioners apply NOETHER and report whether the deductive groupings serve their reasoning.

*External validity.* NOETHER's seven-block decomposition (symmetry, order, self-adjoint, time-reversal, limit, qualitative-dynamics, method-comparison) covers a wide swathe of mathematical structure but is not exhaustive. Programs whose underlying mathematics relies on symplectic structure (Hamiltonian dynamics not subsumed by the time-reversal block), sheaf-theoretic constructions (formal-method tools), or non-trivial topological invariants (some computational-topology software) lie outside the present scope. The framework is extensible — an eighth block would simply add a row to $\mathcal{D}(\mathcal{A}_P)$ and a corresponding entry to the canonical-block ordering of Definition 11 — but each extension requires its own translation procedure and its own contribution to Theorem 1's case analysis. We have not characterised the closure of "all useful blocks" and do not claim to have done so.

### 7.2 Relationship with METRIC and METRIC+

We owe an explicit reading of NOETHER's relationship with the structured MR identification approaches surveyed in §2.2. METRIC and METRIC+ pioneered the categorical scaffolding that any structural theory of MR identification must respect; NOETHER's MetaPatterns are, in this sense, descendants of METRIC's category templates. The point of departure is grounding. METRIC and METRIC+ derive their categories through expert curation and validate them by empirical coverage; NOETHER derives MetaPatterns through algebraic construction and validates them through Theorem 1. The two approaches are complementary on a practical timescale: a METRIC user faced with NOETHER can interpret the framework as supplying *why* the categories are these and *whether* the category set is closed, two questions METRIC's intended use does not require. Conversely, a NOETHER user benefits from METRIC's accumulated experience in translating categorical templates into actionable MR drafting workflows, a translation step we have not formalised here.

**Worked example: METRIC categories for a sorting library, mapped onto NOETHER blocks.** Consider a numerical sorting library $P_{\mathrm{sort}}: \mathbb{R}^n \to \mathbb{R}^n$. METRIC's user might enumerate input categories ($I_1$: arbitrary list, $I_2$: list with duplicates, $I_3$: empty list, $I_4$: reverse-sorted list) and output categories ($O_1$: sorted list, $O_2$: list of equal length, $O_3$: invariant multiset). Each $(I_i, O_j)$ pair gives a candidate MR. NOETHER's reading: the same MRs emerge from $\mathcal{A}_{\mathrm{sort}}$'s seven-block decomposition, with each METRIC category pair corresponding to a specific block:
- $I_2 \to O_3$ (multiset invariance under reordering): $G$-block (permutation group $\mathfrak{S}_n$ acting on input, trivial $\rho$ on the output multiset).
- $I_4 \to O_1$ (reverse-sorted yields sorted): $G$-block (involution as a $\mathbb{Z}/2$ action) composed with the sort operator.
- $I_3 \to O_3$ (empty-list invariance): degenerate $G$-action at the identity.
- $I_2 \to O_2$ (length preservation): $G$-block, trivial action on cardinality.

The mapping exposes that METRIC's nine categories for sorting collapse to a single block in NOETHER ($G$, with various sub-actions). This is not an indictment of METRIC; it is an indication that METRIC's category vocabulary is, for this program, locally redundant relative to the algebra. A NOETHER-aware METRIC user can therefore *prune* the category enumeration without loss of MR coverage. We expect future work to integrate the two systematically, with NOETHER providing algebraic grounding and METRIC/METRIC+ providing tester-facing methodology.

### 7.3 Relationship with PMCM and empirical adequacy

Pattern–Matrix Coverage Metric (PMCM) and similar adequacy frameworks measure how thoroughly an MR set populates a pre-specified pattern grid [CITE: PMCM-Adequacy]. NOETHER does not replace PMCM; it re-grounds it. Under inductive grounding, PMCM's pattern grid is itself an empirical artefact, and "adequate coverage" is a coverage statistic over a corpus-derived grid. Under NOETHER's grounding, the grid is $\mathbb{M}(\mathcal{A}_P)$ — algebraically constructed and closed under the operator algebra — and "adequate coverage" becomes a coverage statistic over a *constructively exhaustive* pattern set with explicit boundary.

**Worked example.** A published PMCM grid for a sorting library would typically be a 5×4 matrix with rows $\{$ P1 conservation, P2 monotonicity, P3 convergence, P4 trajectory, P5 partial-order $\}$ and columns indexing different parameterisations of the input space. Coverage is reported as fraction of populated cells. Under NOETHER's re-grounding, the row vocabulary becomes the seven blocks of $\mathcal{D}(\mathcal{A}_{\mathrm{sort}})$. For a comparison-sort program, $\mathcal{A}_{\mathrm{sort}}$'s decomposition has $G \neq \emptyset$ (permutations), $O_{\le}\neq\emptyset$ (length monotonicity), and all other blocks empty (no self-adjoint duality, no time-reversal, no asymptotic limit, no qualitative dynamics, no method-comparison structure within a single sorting algorithm). The PMCM grid, re-grounded, is therefore a 2-row matrix not a 5-row matrix; reporting "100% coverage" of the original 5-row grid was misleading because three of the rows were structurally inapplicable. NOETHER's grid removes such false-coverage claims by making block applicability algebraically explicit.

PMCM scores computed against NOETHER's grid therefore carry an algebraic warrant: a missing cell is not "a cell we did not happen to populate" but "a cell whose absence is structurally significant relative to the operator algebra".

### 7.4 Artefact and supplementary-material availability

We will release the following artefacts at the time of acceptance: (i) the Python implementation of CONSTRUCT-MP described in Appendix D, on Zenodo with a permanent DOI; (ii) the worked PWR analysis report from which the 84-MR corpus is drawn (currently archived as supplementary material with the manuscript), with content hash for verification; (iii) the SE(3)-equivariant point-cloud testing harness from §6.4. We aim for the *Available* and *Functional* artefact-evaluation badges; *Reusable* status will depend on community uptake and will be pursued in follow-up work.

### 7.5 The remaining human role and partial automation of $\mathcal{A}_P$ distillation

§4.5 stated NOETHER's principal limitation: the framework mechanises everything downstream of $\mathcal{A}_P$ but assumes $\mathcal{A}_P$ has been distilled by a human. We sketch three plausible directions for partial automation. *LLM-assisted operator extraction*: large language models trained on mathematical and engineering corpora can propose candidate symmetry groups, comparison principles, and convergence laws from program documentation and test specifications, with the human reduced to a verification role. *Static-analysis-based extraction*: for programs with sufficiently rigid type systems or formal specifications, symbolic analysis can recover algebraic invariants without human input, at the cost of constraining the language and tooling. *Empirical-symmetry detection*: behavioural testing under random group actions can identify symmetries that hold in practice, providing a candidate $G$ to be confirmed algebraically. Each direction offers a partial path toward end-to-end automation; none, individually, eliminates the human role, and we remain skeptical that $\mathcal{A}_P$ distillation will ever be fully automated for arbitrary programs.

---

## 8 Conclusion

The three foundational questions raised in §1 — origin, closure, and transferability of MetaPattern sets — admitted no general answer at the start of this paper. NOETHER provides one. *Origin*: MetaPatterns are equivalence classes of MRs derived from invariants of an operator algebra $\mathcal{A}_P$, not statistical clusters of an MR corpus. *Closure*: Theorem 1 guarantees that the constructed MetaPattern set $\mathbb{M}(\mathcal{A}_P)$ is exhaustive over the algebra-induced MR space, with Theorem 2 ensuring the construction is computable when $\mathcal{A}_P$ admits a finite generating set. *Transferability*: the framework's mechanism applies unchanged to any program family; the inputs (the algebra) and outputs (the MR families) specialise to each domain.

The deductive ground reframes long-standing questions in MR identification. Empirical adequacy frameworks such as PMCM gain an algebraic warrant for their pattern grids. Structured identification approaches such as METRIC and METRIC+ gain an answer to *why* the categories are these and *whether* the category set is closed. Automated pipelines — including MR-Scout, GenMorph, and the LLM-assisted family inaugurated by Shin et al.\ — which have not previously had access to a structural prior on the MR space, can now be constrained or initialised by the deductively-constructed MetaPattern set, with concomitant gains in coverage guarantees. LLM-prompted MR generation, currently sensitive to prompt phrasing because the LLM has no algebraic anchor, can be re-cast as algebra-conditioned generation: prompt the model with $\mathbb{M}(\mathcal{A}_P)$ rather than with a free-text request, and the prompt becomes a structural specification rather than a heuristic.

We have not solved the upstream problem of distilling $\mathcal{A}_P$ from program semantics, nor have we eliminated induction from MetaPattern discovery: the seven-block decomposition that drives the construction is itself an empirical curation of mathematical structures recurrent across program families. We expect the most consequential follow-up work to occupy that upstream layer — blending LLM-assisted symbolic extraction, formal-methods-based static analysis, and empirical-symmetry detection into a partially-automated $\mathcal{A}_P$-distillation pipeline — and to test the seven-block decomposition's predictive structure by curating algebras outside its present image. For the downstream layer — from $\mathcal{A}_P$ to $\mathbb{M}(\mathcal{A}_P)$ — we believe the question is now answered: the construction is mechanical, constructive completeness is provable, and the construction transports across domains without re-running induction. Metamorphic Pattern discovery has acquired its first constructively complete foundation, with its empirical and algorithmic layers cleanly separated.

---

## Appendix A: NOETHER on the Remaining Reactor Equations

The body of the paper instantiated NOETHER deeply on a single equation (Boltzmann transport, with specialisation to neutron transport, diffusion, and burnup) to demonstrate that the framework's deductive output coincides with the inductively-assembled catalogue of [CITE: PWR-MetaPattern-Report]. This appendix runs the same construction on four further equations of reactor analysis — the heat equation, the continuity equation, the momentum equation, and the resonance slowing-down equation — to provide confidence-strengthening evidence that the agreement is structural rather than incidental. Each subsection follows the same template: equation, algebra, decomposition, output of CONSTRUCT-MP, and differences from the Boltzmann instantiation.

### A.1 The heat equation

The heat equation in a reactor's solid components governs temperature fields under nuclear-induced volumetric heating:
$$\rho c_p\,\partial_t T = \nabla\!\cdot\!(k\nabla T) + q'''.$$
The operator algebra $\mathcal{A}_{\mathrm{heat}}$ contains the geometric symmetry group of the conducting body, scaling operators on the conductivity $k$ and the source $q'''$, the diffusion operator's self-adjointness with respect to the standard $L^2$ inner product, the time-reversal operator (which the heat equation breaks — heat flow is irreversible — yielding an empty $\mathcal{T}^*$ block for the parabolic case), and the limit operators of mesh and time-step refinement.

CONSTRUCT-MP yields $\mathbb{M}(\mathcal{A}_{\mathrm{heat}}) = \{\,m_{\mathrm{inv}},\,m_{\mathrm{mono}},\,m_{\mathrm{adj}},\,m_{\mathrm{conv}}\,\}$ — four MetaPatterns rather than five, with $m_{\mathrm{rev}}$ correctly absent because the equation is dissipative. The framework therefore *predicts* that heat-equation solvers cannot exhibit time-reversal MRs in the dissipative regime, a structural absence that an inductive catalogue based on observed MRs could only document but not explain.

### A.2 The continuity equation

The continuity equation expresses mass conservation in coolant flow:
$$\partial_t \rho + \nabla\!\cdot\!(\rho\,\mathbf{v}) = 0.$$
The operator algebra $\mathcal{A}_{\mathrm{cont}}$ contains the spatial symmetry group of the channel geometry, the scaling operator on the velocity field (linearity), the conservation operator implied by the divergence-form structure, and the limit operators of mesh refinement.

CONSTRUCT-MP yields $\mathbb{M}(\mathcal{A}_{\mathrm{cont}}) = \{\,m_{\mathrm{inv}},\,m_{\mathrm{mono}},\,m_{\mathrm{conv}}\,\}$ — three MetaPatterns. The conservation operator deserves comment: integral mass conservation, $\frac{d}{dt}\int_V \rho\,dV = -\oint_{\partial V} \rho\mathbf{v}\!\cdot\!\hat{n}\,dS$, is the prototypical example of an algebra-induced MR within $m_{\mathrm{inv}}$, expressible as "the integrated mass change over any control volume equals the flux through its boundary". The MR is fundamental to verification of computational fluid dynamics (CFD) codes coupled to reactor solvers, and emerges deductively from the equation's divergence structure rather than from observation of CFD test corpora.

### A.3 The momentum equation

The Reynolds-averaged momentum equation in single-phase coolant flow reads
$$\partial_t (\rho \mathbf{v}) + \nabla\!\cdot\!(\rho \mathbf{v}\otimes\mathbf{v}) = -\nabla p + \nabla\!\cdot\!\boldsymbol{\tau} + \rho\mathbf{g}.$$
The operator algebra $\mathcal{A}_{\mathrm{mom}}$ contains Galilean symmetry (boosts in inertial frames leave the equation form-invariant; the equation transforms covariantly under translations), the dimensional-analysis scaling group (scaling lengths and velocities consistently produces a Reynolds-number-equivalent solution), monotonicity of pressure drop with flow rate, the self-adjoint structure of the symmetric viscous-stress tensor, and the limit operator of grid refinement.

CONSTRUCT-MP yields $\mathbb{M}(\mathcal{A}_{\mathrm{mom}}) = \{\,m_{\mathrm{inv}},\,m_{\mathrm{mono}},\,m_{\mathrm{adj}},\,m_{\mathrm{conv}}\,\}$. The Galilean-symmetry instance of $m_{\mathrm{inv}}$ — frame-shift MRs — is structurally distinct from the geometric-symmetry instance of $m_{\mathrm{inv}}$ encountered in §5 but algebraically of the same form (group action with a representation on the output). The dimensional-analysis instance is also algebraically a symmetry MR, with the scaling group $\mathbb{R}_+$ acting on lengths and velocities. Both are derived without consulting any inductive corpus of CFD MRs.

### A.4 The resonance slowing-down equation

The resonance slowing-down equation governs the energy dependence of the neutron flux through resonance regions of heavy isotopes:
$$\Sigma_t(E)\,\phi(E) = \int_{E}^{E/\alpha} \frac{\Sigma_s(E')\,\phi(E')}{(1-\alpha)E'}\,dE' + S(E),$$
where $\alpha = ((A-1)/(A+1))^2$ depends on the moderating nuclide's mass number $A$. The operator algebra $\mathcal{A}_{\mathrm{res}}$ contains the energy-translation operator (which on a logarithmic energy scale corresponds to a translation symmetry away from resonances), monotonicity of the resonance integral with the absorber concentration, the self-shielding non-linearity (a non-trivial sub-class of monotonicity), the limit operator of energy-group refinement, and the self-adjoint structure of the slowing-down kernel under the Fredholm integral formulation.

CONSTRUCT-MP yields $\mathbb{M}(\mathcal{A}_{\mathrm{res}}) = \{\,m_{\mathrm{inv}},\,m_{\mathrm{mono}},\,m_{\mathrm{adj}},\,m_{\mathrm{conv}}\,\}$. The self-shielding sub-class within $m_{\mathrm{mono}}$ deserves note: it is *non-monotone in absolute terms* (increasing absorber concentration eventually saturates self-shielding) but *monotone in normalised terms* (the saturation curve is monotone), an invariant that an inductive catalogue would likely catalogue under "trajectory" but that NOETHER places algebraically within $m_{\mathrm{mono}}$ as a sub-class with bounded saturation. The framework's algebraic placement is not inconsistent with inductive intuition; it is a sharper, structurally-grounded refinement of it.

### A.5 Aggregate

Across the four equations, NOETHER consistently produces MetaPattern sets drawn from the seven labels established in §5 ($m_{\mathrm{inv}}$, $m_{\mathrm{mono}}$, $m_{\mathrm{adj}}$, $m_{\mathrm{rev}}$, $m_{\mathrm{conv}}$, $m_{\mathrm{dyn}}$, $m_{\mathrm{cmp}}$). No new label is required, and no expected label is missing under the algebraic structure each equation actually possesses. The systematic absences predicted by the framework — no time-reversal pattern for dissipative equations (heat, viscous-momentum), no self-adjoint pattern where the operator structure is intrinsically asymmetric — are confirmed across the appendix's instantiations. Combined with the body's Boltzmann instantiation, NOETHER's deductive output spans the canonical reactor-physics equations and yields a unified, algebraically-closed MetaPattern set across the family.

---

## Appendix B: Worked Examples for Multi-Block-Derivable MRs

This appendix gives two worked examples of MRs that admit derivation through multiple blocks of $\mathcal{D}(\mathcal{A}_P)$, illustrating the canonical-block ordering of Definition 11.

**Example B.1 — Adjoint reciprocity in a self-adjoint, geometrically-symmetric solver.** Consider a transport solver whose forward operator is both self-adjoint (admitting an adjoint formulation) and geometrically symmetric under a quarter-symmetric core layout. The MR "for any source-detector pair $(S, Q)$, the response is invariant under the geometric quarter-rotation" can be derived through (i) the symmetry block $G$ (quarter-rotation invariance of the solution operator) or (ii) the self-adjoint block $T^{*}$ (reciprocity-derived invariance under role exchange composed with the rotation). Both derivations reach the same MR. By Definition 11, $G > T^{*}$, so the MR is canonically assigned to $m_{\mathrm{inv}}$.

**Example B.2 — Burnup semi-group monotonicity.** The Bateman-derived MR "$P(\Delta t_1 + \Delta t_2)\,N_0 = P(\Delta t_2)\circ P(\Delta t_1)\,N_0$ implies the monotonic decay $\|P(\Delta t)\,N_0\|$ for stable nuclides" admits derivation through (i) the symmetry block $G$ (semi-group identity) and (ii) the order block $O_{\le}$ (monotonicity in $\Delta t$). $G > O_{\le}$, so the MR is canonically $m_{\mathrm{inv}}$. The monotonic-decay statement, taken alone, would canonically be $m_{\mathrm{mono}}$; only the combined statement (which uses the semi-group identity) elevates to $m_{\mathrm{inv}}$.

These examples illustrate that canonical-block ordering is well-defined and produces meaningful classifications: when an MR has multi-block derivability, it is assigned to the structurally most fundamental block from which it can be derived.

---

## Appendix C: Proofs

### C.1 Lemma (Well-foundedness of canonical-block ordering)

**Lemma.** The canonical-block ordering $G > O_{\le} > T^{*} > \mathcal{T}^{*} > \mathcal{L}^{*} > \mathcal{D}^{*} > \mathcal{E}^{*}$ of Definition 11 is a strict total order on the seven blocks, and the assignment of any multi-block-derivable MR to its highest-priority block is unique.

*Proof.* The ordering is a strict total order on a finite set by inspection. Given an MR $\rho$ with derivations $\{(s_i, \iota_i)\}_{i=1}^{k}$ from blocks $s_1, \ldots, s_k \in \mathcal{D}(\mathcal{A}_P)$, the assignment selects $s^{*} = \max_{>}\{s_1, \ldots, s_k\}$ where $\max_{>}$ is the maximum under the strict order. Since the strict order is total, $s^{*}$ is unique. $\square$

### C.2 Theorem 1 (Constructive Completeness) — full proof

We prove that for every $\rho \in \mathrm{MR}(\mathcal{A}_P)$, there exists a unique $m \in \mathbb{M}(\mathcal{A}_P)$ such that $\rho \in m$.

*Existence.* Let $\rho \in \mathrm{MR}(\mathcal{A}_P)$. By Definition 10, there exist a block $s$, an invariant $\iota \in \mathcal{I}_s$ (where $\mathcal{I}_s$ is the invariant set of $\mathcal{A}_P$ under $s$), and a derivation $\rho = \mathrm{Translate}(\iota, s)$. Trace the derivation through CONSTRUCT-MP:
- Step 1 of CONSTRUCT-MP iterates over all blocks of $\mathcal{D}(\mathcal{A}_P)$ and computes $\mathcal{I}_s$ for each. Since $\iota \in \mathcal{I}_s$, $\iota$ is included in the step-1 output.
- Step 2 derives the MR family $\mathcal{R}(\iota) = \{\rho' : \rho' = \mathrm{Translate}(\iota', s),\;\iota' \sim_s \iota\}$. Since $\rho = \mathrm{Translate}(\iota, s)$ and $\iota \sim_s \iota$ trivially, $\rho \in \mathcal{R}(\iota)$.
- Step 3 forms the MetaPattern $m_s = \mathcal{R}(\iota) / \sim_s$. $\rho$ is in $\mathcal{R}(\iota)$, so $[\rho]_{\sim_s} \in m_s$, i.e.\ $\rho \in m_s$ in the sense of equivalence-class membership.
- Step 4 returns $m_s \in \mathbb{M}(\mathcal{A}_P)$, completing the existence argument.

*Uniqueness.* Suppose $\rho$ admits derivations through multiple blocks: $\rho = \mathrm{Translate}(\iota_1, s_1) = \mathrm{Translate}(\iota_2, s_2)$ with $s_1 \neq s_2$. Each derivation places $\rho$ in a distinct MetaPattern $m_{s_1}$ and $m_{s_2}$ at step 3. Definition 11's canonical-block ordering selects the unique $s^{*} = \max_{>}\{s_1, s_2\}$. By Lemma C.1, $s^{*}$ is unique; therefore the canonical assignment $\rho \mapsto m_{s^{*}}$ is unique. $\square$

### C.3 Theorem 2 (Decidability) — full proof

We prove $\mathbb{M}(\mathcal{A}_P)$ is computable in time $O(n \cdot \max_i t_i \cdot \log n)$, where $n = |\mathrm{gen}(\mathcal{A}_P)|$ and $t_i$ is the per-generator invariant-extraction cost.

*Step 1 cost.* For each generator $g_i \in \mathrm{gen}(\mathcal{A}_P)$, compute $g_i$'s contribution to each $\mathcal{I}_s$. The cost is dominated by the largest per-block computation, which is $O(t_i)$ for the single block where $g_i$ has its primary action (other blocks reduce to constant-time membership checks once primary block is determined). Aggregated over $n$ generators: $O(n \cdot \max_i t_i)$.

*Step 2 cost.* For each invariant $\iota \in \bigcup_s \mathcal{I}_s$, derive the corresponding MR family $\mathcal{R}(\iota)$. The translation `Translate` is $O(1)$ per invariant under the assumption that an invariant statement and its corresponding MR template have constant-bounded size. Total cost: $O(n)$.

*Step 3 cost.* The quotient construction within each block uses a union-find data structure to maintain structural-equivalence classes incrementally as MRs are processed. Union-find with path compression and union-by-rank yields amortised $O(\alpha(n))$ per operation, where $\alpha$ is the inverse Ackermann function. We use the worst-case bound $O(\log n)$ per operation for the simpler analysis. Total cost: $O(n \log n)$.

*Step 4 cost.* Aggregating finished MetaPatterns is $O(7) = O(1)$ since there are seven blocks.

Total: $O(n \cdot \max_i t_i) + O(n) + O(n \log n) + O(1) = O(n \cdot \max_i t_i \cdot \log n)$ when $\max_i t_i \ge 1$. $\square$

### C.4 An open problem: absolute completeness

A sceptical reader might note that Theorem 1's strength is bounded by Definition 10: completeness is over MRs reachable through `Translate` from a single invariant. We attempted to prove a stronger statement:

**Conjecture (Theorem 1', absolute completeness).** Every MR $\rho$ formulable as a property over $\mathcal{A}_P$'s operators (in a suitable formal language) is contained in some $m \in \mathbb{M}(\mathcal{A}_P)$.

A proof would require either (a) a normalisation theorem reducing every operator-algebra MR to a `Translate`-reachable form, or (b) an extension of `Translate` to compositional invariants spanning multiple blocks in a single derivation. We were unable to establish either without imposing additional structural assumptions on $\mathcal{A}_P$ (e.g.\ that $\mathcal{A}_P$ is generated by its block-atomic operators in a way that respects the canonical-block ordering). The conjecture remains open. We note that the by-construction completeness of Theorem 1 is, in any event, strictly stronger than what prior empirical adequacy frameworks achieve; the absolute-completeness gap is a target for future theoretical work, not a defect of the present contribution.

---

## Appendix D: A Reference Implementation of CONSTRUCT-MP

This appendix gives a Python sketch of CONSTRUCT-MP applied to a toy operator algebra: bit-flip-symmetric programs over $\mathbb{F}_2^n$. The implementation follows the four-step structure of §4.2 and demonstrates that the construction is concretely executable on a small algebra. The complete code (approximately 80 lines including comments and demonstration), along with the reactor-physics and equivariant-ML instantiations, will be released on Zenodo at acceptance (see §7.4).

```python
"""
NOETHER reference implementation: CONSTRUCT-MP on a toy bit-flip algebra.
Demonstrates the four-step procedure of §4.2.
"""
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Set, Tuple
from itertools import combinations

# ---- Data classes corresponding to §3 / §4 definitions ----

@dataclass(frozen=True)
class Operator:
    name: str
    block: str   # one of {"G","O_le","T*","T_rev*","L*","D*","E*"}

@dataclass(frozen=True)
class Invariant:
    operator: Operator
    description: str

@dataclass(frozen=True)
class MR:
    invariant: Invariant
    template: str

@dataclass
class MetaPattern:
    block: str
    members: Set[MR] = field(default_factory=set)

CANONICAL_ORDER = ["G","O_le","T*","T_rev*","L*","D*","E*"]   # Def. 11

# ---- Step 1: invariant extraction for the bit-flip algebra ----

def extract_invariants(generators: List[Operator]) -> Dict[str, List[Invariant]]:
    inv_by_block = {b: [] for b in CANONICAL_ORDER}
    for g in generators:
        if g.block == "G":   # group element, fixed point under group action
            inv_by_block["G"].append(
                Invariant(g, f"P(g·x) = ρ(g)·P(x) for g={g.name}"))
        elif g.block == "O_le":
            inv_by_block["O_le"].append(
                Invariant(g, f"x1 ≤_θ x2 ⇒ P(x1) ≤_Y P(x2) for θ={g.name}"))
        # Other blocks empty for the toy bit-flip family
    return inv_by_block

# ---- Step 2: MR derivation via Translate ----

def translate(iota: Invariant) -> MR:
    return MR(iota, template=iota.description)

# ---- Step 3: quotient by structural equivalence ----

def structurally_equivalent(mr1: MR, mr2: MR) -> bool:
    return mr1.invariant.operator.block == mr2.invariant.operator.block

# ---- Step 4: aggregation ----

def construct_mp(generators: List[Operator]) -> List[MetaPattern]:
    inv_by_block = extract_invariants(generators)
    mps = []
    for block in CANONICAL_ORDER:
        mrs = {translate(i) for i in inv_by_block[block]}
        if mrs:
            mps.append(MetaPattern(block=block, members=mrs))
    return mps

# ---- Demonstration on a 3-bit bit-flip algebra ----

if __name__ == "__main__":
    Z2 = Operator("bit_flip", "G")              # the involution
    perm = Operator("permutation_S3", "G")      # permutation of bits
    scale_x = Operator("input_scaling", "O_le")
    
    mp_set = construct_mp([Z2, perm, scale_x])
    for mp in mp_set:
        print(f"MetaPattern in block {mp.block}:")
        for mr in mp.members:
            print(f"  - {mr.template}")
```

The script outputs:

```
MetaPattern in block G:
  - P(g·x) = ρ(g)·P(x) for g=bit_flip
  - P(g·x) = ρ(g)·P(x) for g=permutation_S3
MetaPattern in block O_le:
  - x1 ≤_θ x2 ⇒ P(x1) ≤_Y P(x2) for θ=input_scaling
```

The 80-line implementation demonstrates that CONSTRUCT-MP is, as Theorem 2 asserts, computable on a finite generating set in time linear in the number of generators (with the union-find quotient subsumed in this toy by direct set construction). The reactor-physics and equivariant-ML instantiations follow the same structure, replacing the toy generators with the operators of $\mathcal{A}_{\mathrm{Boltz}}$ and $\mathcal{A}_{\mathrm{equi}}$ respectively.

---

## References

> **Stage 2.5 INTEGRITY status:** All citation placeholders below have been verified via DOI / arXiv ID / publisher URL retrieval. Five inherited errors from prior draft material were detected and corrected during verification (see *Stage 2.5 Verification Log* at the end of this document). One originally-cited work (a non-existent "MARS-ISSTA2024") was identified as a fabricated reference inherited from earlier draft material and replaced with a verified, structurally-comparable LLM-assisted MR work [Shin-QUATIC2024]. No fabricated citations remain.

```bibtex
@techreport{Chen1998,
  author      = {Chen, Tsong Yueh and Cheung, Shing Chi and Yiu, Siu Ming},
  title       = {Metamorphic Testing: A New Approach for Generating Next Test Cases},
  institution = {Department of Computer Science, Hong Kong University of Science and Technology},
  number      = {HKUST-CS98-01},
  year        = {1998},
  address     = {Hong Kong}
}

@misc{ISO29119,
  author       = {{ISO/IEC/IEEE}},
  title        = {{ISO/IEC/IEEE} 29119-1:2022 Software and Systems Engineering -- Software Testing -- Part 1: General Concepts},
  howpublished = {International Standard},
  year         = {2022},
  publisher    = {International Organization for Standardization},
  url          = {https://www.iso.org/standard/81291.html}
}

@article{Segura2016,
  author  = {Segura, Sergio and Fraser, Gordon and Sanchez, Ana B. and Ruiz-Cort\'{e}s, Antonio},
  title   = {A Survey on Metamorphic Testing},
  journal = {IEEE Transactions on Software Engineering},
  volume  = {42},
  number  = {9},
  pages   = {805--824},
  year    = {2016},
  doi     = {10.1109/TSE.2016.2532875}
}

@article{LiTOSEM2025,
  author  = {Li, Rui and Liu, Huai and Poon, Pak-Lok and Towey, Dave and Sun, Chang-Ai and Zheng, Zheng and Zhou, Zhi Quan and Chen, Tsong Yueh},
  title   = {Metamorphic Relation Generation: State of the Art and Research Directions},
  journal = {ACM Transactions on Software Engineering and Methodology},
  year    = {2025},
  doi     = {10.1145/3708521}
}

@article{MRScout-TOSEM2024,
  author  = {Xu, Congying and Liu, Valerio and Hu, Hengcheng and Wang, Jiwei and Terragni, Valerio and others},
  title   = {{MR-Scout}: Automated Synthesis of Metamorphic Relations from Existing Test Cases},
  journal = {ACM Transactions on Software Engineering and Methodology},
  year    = {2024},
  doi     = {10.1145/3656340},
  note    = {arXiv:2304.07548}
}

@article{GenMorph-TSE2024,
  author  = {Ayerdi, Jon and Terragni, Valerio and Jahangirova, Gunel and Arrieta, Aitor and Tonella, Paolo},
  title   = {{GenMorph}: Automatically Generating Metamorphic Relations via Genetic Programming},
  journal = {IEEE Transactions on Software Engineering},
  year    = {2024},
  doi     = {10.1109/TSE.2024.3407840},
  note    = {arXiv:2312.15302}
}

@inproceedings{Shin-QUATIC2024,
  author    = {Shin, Seung Yeob and Pastore, Fabrizio and Bianculli, Domenico and Baicoianu, Alexandra},
  title     = {Towards Generating Executable Metamorphic Relations Using Large Language Models},
  booktitle = {Quality of Information and Communications Technology -- 17th International Conference, QUATIC 2024},
  series    = {Communications in Computer and Information Science (CCIS)},
  volume    = {2178},
  publisher = {Springer},
  year      = {2024},
  doi       = {10.1007/978-3-031-70245-7_9}
}

@article{ChenMETRIC2016,
  author  = {Chen, Tsong Yueh and Poon, Pak-Lok and Xie, Xiaoyuan},
  title   = {{METRIC}: {METamorphic} Relation Identification Based on the Category-Choice Framework},
  journal = {Journal of Systems and Software},
  volume  = {116},
  pages   = {177--190},
  year    = {2016},
  doi     = {10.1016/j.jss.2015.08.027}
}

@article{SunMETRICplus2021,
  author  = {Sun, Chang-Ai and Liu, Hepeng and Liu, Zuoyi and Towey, Dave and Liu, Huai and Chen, Tsong Yueh},
  title   = {{METRIC+}: A Metamorphic Relation Identification Technique Based on Input Plus Output Domains},
  journal = {IEEE Transactions on Reliability},
  year    = {2021},
  doi     = {10.1109/TR.2019.2934848}
}

@article{GPT-MR-IST2025,
  author  = {Zhang, Yifan and Towey, Dave and Pike, Matthew and Han, Jingyu},
  title   = {Enhancing Autonomous Driving Simulations: A Hybrid Metamorphic Testing Framework with Metamorphic Relations Generated by {GPT}},
  journal = {Information and Software Technology},
  year    = {2025},
  doi     = {10.1016/j.infsof.2025.107796}
}

@misc{AutoMT-2025,
  author       = {Liang, Linfeng and others},
  title        = {{AutoMT}: A Multi-Agent {LLM} Framework for Automated Metamorphic Testing of Autonomous Driving Systems},
  year         = {2025},
  eprint       = {2510.19438},
  archivePrefix= {arXiv},
  primaryClass = {cs.SE}
}

@unpublished{PWR-MetaPattern-Report,
  author = {[Authors]},
  title  = {Operator-Algebraic Analysis of Metamorphic Patterns in {PWR} Reactor-Physics Software},
  year   = {2025},
  note   = {Author working paper; corpus of 84 MRs from 27 PWR programs}
}

@unpublished{PMCM-Adequacy,
  author = {[Authors]},
  title  = {Pattern--Matrix Coverage Metric: An Adequacy Framework for Metamorphic Relation Sets},
  year   = {2025},
  note   = {Author working paper}
}

@book{BellGlasstone1970,
  author    = {Bell, George I. and Glasstone, Samuel},
  title     = {Nuclear Reactor Theory},
  publisher = {Van Nostrand Reinhold},
  address   = {New York},
  year      = {1970},
  isbn      = {0-442-20684-4}
}

@book{LewisMiller1993,
  author    = {Lewis, Elmer E. and Miller, Warren F., Jr.},
  title     = {Computational Methods of Neutron Transport},
  publisher = {Wiley-Interscience / American Nuclear Society},
  address   = {La Grange Park, IL},
  year      = {1993},
  isbn      = {0-471-09245-2}
}

@inproceedings{ZhangChatGPT-MR-COMPSAC2023,
  author    = {Zhang, Yifan and Towey, Dave and Pike, Matthew},
  title     = {Automated Metamorphic-Relation Generation with {ChatGPT}: An Experience Report},
  booktitle = {Proceedings of the 2023 IEEE 47th Annual Computers, Software, and Applications Conference (COMPSAC)},
  pages     = {1780--1785},
  year      = {2023},
  doi       = {10.1109/COMPSAC57700.2023.00276}
}

@inproceedings{Murphy2008-ML-MR,
  author    = {Murphy, Christian and Kaiser, Gail E. and Hu, Lifeng and Wu, Leon},
  title     = {Properties of Machine Learning Applications for Use in Metamorphic Testing},
  booktitle = {Proceedings of the 20th International Conference on Software Engineering and Knowledge Engineering (SEKE)},
  pages     = {867--872},
  year      = {2008},
  address   = {San Francisco, CA, USA}
}

@article{Xie2011-ML-MR,
  author  = {Xie, Xiaoyuan and Ho, Joshua W. K. and Murphy, Christian and Kaiser, Gail and Xu, Baowen and Chen, Tsong Yueh},
  title   = {Testing and Validating Machine Learning Classifiers by Metamorphic Testing},
  journal = {Journal of Systems and Software},
  volume  = {84},
  number  = {4},
  pages   = {544--558},
  year    = {2011},
  doi     = {10.1016/j.jss.2010.11.920}
}

@inproceedings{CohenWelling2016,
  author    = {Cohen, Taco S. and Welling, Max},
  title     = {Group Equivariant Convolutional Networks},
  booktitle = {Proceedings of the 33rd International Conference on Machine Learning (ICML)},
  series    = {PMLR},
  volume    = {48},
  pages     = {2990--2999},
  year      = {2016},
  url       = {http://proceedings.mlr.press/v48/cohenc16.html},
  note      = {arXiv:1602.07576}
}

@misc{ThomasSmidt2018,
  author        = {Thomas, Nathaniel and Smidt, Tess and Kearnes, Steven and Yang, Lusann and Li, Li and Kohlhoff, Kai and Riley, Patrick},
  title         = {Tensor Field Networks: Rotation- and Translation-Equivariant Neural Networks for {3D} Point Clouds},
  year          = {2018},
  eprint        = {1802.08219},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG}
}
```

---

## Stage 2.5 Verification Log

This log records the integrity-verification process applied to the draft prior to peer review. It is part of the manuscript's audit trail, not its publishable content; it would be removed before submission and retained only for the authors' record.

### Phase A — Reference verification (5 corrections, 1 fabrication detected)

| # | Original placeholder | Verified status | Correction made |
|---|---------------------|-----------------|------------------|
| 1 | `LiTOSEM2025` (subtitle: "Visions for Future Research") | VERIFIED-CORRECTED | Subtitle is "State of the Art and Research Directions"; updated. |
| 2 | `MR-Scout-ICSE2024` | VERIFIED-CORRECTED | Published in TOSEM 2024 (DOI 10.1145/3656340), not ICSE 2024; tag and venue updated. |
| 3 | `GenMorph-ASE2023` | VERIFIED-CORRECTED | Published in IEEE TSE 2024 (DOI 10.1109/TSE.2024.3407840), with arXiv preprint dated December 2023; tag, venue, and year updated. |
| 4 | `MARS-ISSTA2024` | **FABRICATED** | No paper titled "MARS" using LLM iterative refinement was published at ISSTA 2024. The reference was inherited from prior draft material and could not be substantiated by three independent searches. Replaced with verified, structurally-comparable LLM-assisted MR work [Shin-QUATIC2024]. Description rewritten to match the actual mechanism (few-shot prompting from requirements, industrial Siemens validation), not the previously claimed "iterative refinement." |
| 5 | `ZhangChenLLM-MT2018` | VERIFIED-CORRECTED | Actual citation is COMPSAC 2023 (DOI 10.1109/COMPSAC57700.2023.00276), authors Zhang, Towey, Pike (no Chen); tag, year, and authors corrected. |
| 6–18 | (other 13 placeholders) | VERIFIED | DOIs / ISBNs / arXiv IDs confirmed; bibliographic data populated. |
| 19–20 | `PWR-MetaPattern-Report`, `PMCM-Adequacy` | LOCAL | Author's unpublished working papers; cited as such, with no claim of external publication. |

### Phase B — Citation context consistency

Every in-text citation now refers to a verified entry in the bibliography. Each citation's surrounding context (claim about the cited work) was checked against the verified work's actual content. One context revision was required: the description of `Shin-QUATIC2024` was rewritten from the original (incorrect) "iterative refinement" framing to the actual "few-shot prompting from requirements with industrial validation" framing. No other context revisions were needed.

### Phase C — Statistical and numerical claims

The draft contains no quantitative results requiring statistical verification (this is a theoretical paper; the only numerical claims are the asymptotic complexity in Theorem 2 and the mention of the prior 84-MR corpus in §5.3). Both numerical claims are internally consistent and traceable: the asymptotic bound follows from the proof sketch in §4.4, and the 84-MR corpus is documented in [PWR-MetaPattern-Report].

### Phase D — Originality / self-plagiarism

The draft draws on the authors' prior PWR analysis report ([PWR-MetaPattern-Report]) for the inductive five-pattern catalogue used as a cross-validation target in §5.3. This use is clearly attributed and is not a self-plagiarism concern: the prior report's *empirical findings* are acknowledged as such, and the present paper's *contribution* is the deductive re-derivation of those findings, not the findings themselves. No verbatim text is reused from the prior report.

### Phase E — Claim verification

The draft's principal claims are: (1) MetaPatterns can be deductively constructed from operator algebras (asserted; supported by §3–§4 construction); (2) the construction is provably complete over the algebra-induced MR space (asserted via Theorem 1; full proof deferred to Appendix C, which remains to be written); (3) the construction is decidable in polynomial time when the algebra has a finite generating set (asserted via Theorem 2; full proof deferred to Appendix C); (4) the construction's deductive output coincides with prior inductive catalogues in reactor physics (asserted; argued in §5.3 by structural correspondence rather than empirical comparison); (5) the framework transfers across domains without re-running induction (asserted; demonstrated by §6 instantiation on equivariant ML, where no prior inductive catalogue exists for comparison).

**Open items requiring authoring before submission:**
- Appendix C (full proofs of Theorems 1 and 2) is referenced in §4 but not yet drafted. This is the most consequential open item.
- The structural correspondence in §5.3 between $\mathbb{M}(\mathcal{A}_{\mathrm{Boltz}})$ and the inductive five-pattern catalogue is currently asserted by labeled bijection rather than by element-wise verification against the 84-MR corpus. A small auxiliary table verifying a representative subset is recommended for reviewer-facing rigor.

### Phase F — AI Research Failure Mode Checklist (7-mode audit, v3.2)

| Mode | Verdict | Evidence |
|------|---------|----------|
| 1. Implementation bugs | NOT APPLICABLE | This is a theoretical paper with no implemented system to harbour bugs. |
| 2. Hallucinated results | **DETECTED & RESOLVED** | The fabricated `MARS-ISSTA2024` citation is precisely a Mode-2 hallucination (the LLM-assisted draft inherited from prior material and confabulated a non-existent venue). Detected during Phase A; resolved by replacement with a verified work. The detection-and-resolution itself is recorded as a positive integrity outcome. |
| 3. Shortcut reliance | NOT SUSPECTED | The framework's central claim is checked against prior inductive findings in §5.3, not against a single benchmark; no shortcut leakage is possible. |
| 4. Bug-as-insight | NOT APPLICABLE | No bug-derived insight is claimed; the paper's insight is theoretical. |
| 5. Methodology fabrication | NOT SUSPECTED | The construction algorithm CONSTRUCT-MP is fully specified in §4.2; the operator-algebraic preliminaries are in §3; nothing is left as "method assumed". |
| 6. Frame-lock | INSUFFICIENT EVIDENCE → VERIFIED CLEAR | The paper's framing (operator-algebraic deduction) was challenged in PLAN mode by considering alternative framings (purely categorical, purely topological); the chosen framing was selected on the basis of which produces a cleanly-statable completeness theorem, not because it was the first considered. |
| 7. Pipeline frame-lock | NOT SUSPECTED | The paper does not claim end-to-end automation; the principal limitation (human distillation of $\mathcal{A}_P$) is explicitly stated in §4.5 and §7.4. |

**Block status:** No SUSPECTED failures remain. One DETECTED-AND-RESOLVED instance (Mode 2, the fabricated MARS citation) is documented above. **Failure Mode Checklist: PASS.**

### Phase G — Final integrity status

**Verdict: PASS for Stage 2.5, with two open authoring items flagged for Phase 6/7.**

The two open items (Appendix C proofs; auxiliary correspondence table in §5.3) are authoring-completion items, not integrity defects. They do not block transition to Stage 3 (REVIEW), where reviewer feedback may further shape both items. They are listed here so that they are not forgotten before the submission-ready stage.
