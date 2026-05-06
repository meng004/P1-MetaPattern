# NOETHER 论文反例插入与修改方案（第 4 版）

> **版本说明**：第 4 版相对于第 3 版的修订集中在 §6.8.2 末尾与 §6.8.3 全段的物理表述精确化，按反应堆物理资深审稿意见修订 5 处：
>
> 1. **修订 1（C1，§6.8.2 anti-shadowing 段）**：v3 写"anti-shadowing principally observed in small-core or non-standard geometries"低估了其在标准 PWR 中的可观测性。修订后明确：anti-shadowing 在标准商用 PWR 中是次要但可测现象（典型 5–20 pcm），在小堆或强非对称插棒模式下更显著；两种 regime 都在 PWR 启动物理试验中常规测量。
>
> 2. **修订 2（C2，Definition 17 单位约定，技术性必须修订）**：v3 写 $|\partial^2 k_{\text{eff}}/(\partial T_{\text{mod}} \partial C_B)|$ 与 pcm/°F/ppm 容差混用单位。MTC 在反应堆物理工程标准中是反应性对温度的偏导，不是 $k_{\text{eff}}$ 对温度的偏导。修订后改用 $\partial^2 \rho_{\text{static}}/(\partial T_{\text{mod}} \partial C_B)$，其中 $\rho_{\text{static}} = 1 - 1/k_{\text{eff}}$，pcm 单位约定明确，与 Bell & Glasstone §10.3、Stacey §3.4 一致。
>
> 3. **修订 3（C2，§6.8.3 HFP/HZP 工况区分）**：v3 写"BOC ... MTC may be slightly positive"未区分 hot-full-power 与 hot-zero-power 工况。修订后明确：HZP BOC 高硼下 MTC 可接近零或微正（启动物理试验工况）；HFP 下 MTC 始终 $\le 0$ 由 10 CFR 50 App. A GDC 11 监管。Definition 17 的工况限定改为以 hot-full-power, ARO 为参考。
>
> 4. **修订 4（C2，§6.8.3 三机制描述）**：v3 描述 MTC 为"两机制竞争（慢化 + 硼负反馈）"。修订后补充第三机制（谱硬化 + $^{238}$U 共振吸收增强），与 Stacey §3.4 的标准三机制论述一致；这一补充对 MOX 燃料和高富集度 UO$_2$ 燃料尤其重要。
>
> 5. **修订 5（C2，引用文献）**：v3 引用 ANSI/ANS-51.1 作为 MTC 监管来源，但该标准重点是 PWR 整体安全设计准则，对反应性反馈系数无具体约束。修订后删除 ANSI/ANS-51.1，保留 10 CFR 50 App. A GDC 11（监管来源）+ Stacey §3.4 + Lamarsh & Baratta §8.3（教科书背书），可选补充 ANS 19.6.1（PWR 反应性系数测量与不确定度，2011 版）。
>
> v3 → v4 的代数论证（Appendix C.6）保持不变；修订全部限定在 §6.8 的物理表述部分。
>
> ---
>
> **v3 版相对 v2 版的核心调整（保留供参考）**：
>
> - **反例数量从 3 个减为 2 个**。基于 ROI 评估，保留物理表述完美的 C1（控制棒价值非可加性），删除原 ITC 反例和 Gd 自屏蔽反例（前者物理表述与 PWR 监管约束方向矛盾、后者需要重大物理细化）；新增 C2（MTC 对硼浓度的二阶混合偏导）作为代数失败模式正交的第二反例。
> - **C1 物理表述的两处技术修订**：(i) anti-shadowing 机制描述更克制；(ii) Definition 16 增加工程容差量化（5 pcm 量级）。v4 进一步修订了 (i)，使 anti-shadowing 描述更符合 PWR 工程实际。
> - **C2 完整重新设计**：从"ITC 符号反转"改为"MTC 对硼浓度的二阶混合偏导非零"。v4 进一步修订单位约定、HFP/HZP 工况、三机制描述与引用文献。
>
> **文件用途**：本文件提供两个不可分解组合 MR 反例（来自 PWR 反应堆物理域），用于将 NOETHER 论文 Theorem 1′（Conjecture D，绝对完备性）从开放猜想推进到"在 PWR 算子代数 $\mathcal{A}_{\text{PWR}}$ 上为假"的已证明命题。
>
> **使用方式**：本文件按"先新增、后修改"的顺序组织。Part A 是两个完整新增段（§6.8 与 Appendix C.6），可直接拷入原文相应位置；Part B 是对原文八处的修改，每处给出**原文片段**与**修改后片段**，可逐处替换。Part C 是一致性检查清单，在所有修订完成后核对。
>
> **正文语言保持英文**（与原论文一致）；说明性指引使用中文标注。

---

## Part A — 完整新增段

### A.1 §6.8（新增正文章节）

> **插入位置**：在原论文 §6.7 "A third domain: relational query optimisers" 末尾之后、§7 "Discussion and threats to validity" 之前，新增 §6.8。

```markdown
## 6.8 A negative instantiation: irreducibly compositional MRs in PWR core simulators

Sections 5, 6, and 6.7 instantiated NOETHER on three program families—Boltzmann reactor physics, equivariant ML, and relational query optimisers—where the framework's downstream construction was non-vacuous and produced executable MRs. This section instantiates NOETHER on a fourth program family, the PWR core diffusion solver family, with an inverted purpose: rather than demonstrating coverage, we exhibit two specific MRs from the standard PWR safety-analysis literature that the framework's Translate operator cannot reach under any single-block derivation. The two MRs together identify five pairwise-independent structural obstructions in $\mathrm{Translate}$'s present signature, jointly recasting Theorem 1′ (Conjecture D, Appendix D) from an open conjecture to a falsified statement on a structurally significant operator algebra.

The MRs chosen are not pathological cases. They are core safety-analysis MRs that PWR core simulators are required by regulatory practice and engineering convention to reproduce: non-additivity of control-bank reactivity worth (the algebraic root of rod-bank shadowing and anti-shadowing phenomena) and second-order mixed dependence of $k_{\text{eff}}$ on moderator temperature and boron concentration (the standard MTC-vs-boron design curve). The negative instantiation thus uses NOETHER's flagship application domain (reactor physics) against the framework's strongest claim (algebraic closure over arbitrary single-block-derivable MRs).

### 6.8.1 The PWR core diffusion algebra

Let $\mathcal{F}_{\text{PWR}}$ be the program family of PWR core diffusion solvers (canonical examples: PARCS, SIMULATE-3/5, ANC, SMART). Its operator algebra $\mathcal{A}_{\text{PWR}}$ contains, in addition to the operators of $\mathcal{A}_{\text{Boltz}}$ (Section 5.1), the following PWR-specific generators:

- $\mathcal{O}_{\text{rod}}$: discrete control-rod insertion operators, parametrised by rod-bank label $g$ and insertion depth $d$, generating an additive-on-geometry semigroup under composition. In the steady-state setting we adopt throughout, $\mathcal{O}_{\text{rod}}^A \cdot \mathcal{O}_{\text{rod}}^B$ and $\mathcal{O}_{\text{rod}}^B \cdot \mathcal{O}_{\text{rod}}^A$ act identically on the input space (both yield the same total inserted geometry), so $\mathcal{O}_{\text{rod}}$ is commutative on geometry. Crucially, however, the *reactivity-worth functional* on $\mathcal{O}_{\text{rod}}$ is not a semigroup homomorphism: $d\rho(A \cup B) \neq d\rho(A) + d\rho(B)$ in general. This non-additivity, not non-commutativity, is what the present section exploits.
- $\mathcal{M}_{C_B}$: continuous boration operators acting on the moderator material composition through the soluble-boron concentration $C_B$ (typical PWR operating range: 0–2000 ppm).
- $\mathcal{M}_{T_{\text{mod}}}$: continuous moderator-temperature operators acting on the cross-section library through the parametric dependence $\Sigma(T_{\text{mod}})$ (typical PWR operating range: 290–320°C).

Decomposed along the eight-block decomposition of Section 3.9:

- $G \supseteq \{\mathcal{O}_{\text{rod}}\}$ (treated tentatively as a commutative semigroup—we will see this assignment fails);
- $O_\le \supseteq \{\mathcal{M}_{C_B}, \mathcal{M}_{T_{\text{mod}}}\}$ (parameter-monotonicity operators);
- $T^* \supseteq \{-\nabla \cdot D \nabla + \Sigma_a\}$ (the self-adjoint diffusion operator under isotropic scattering; Bell & Glasstone §6.1, Lewis & Miller §4.2);
- $T_{\text{rev}}^* = \emptyset$ (PWR diffusion is dissipative);
- $L^*, D^*, E^*$ as in $\mathcal{A}_{\text{Boltz}}$ with appropriate restrictions to the diffusion regime;
- $B_{\text{rel}}^* = \emptyset$ (no idempotent-semiring structure on PWR core states).

We will show that despite this rich block structure, two specific PWR-safety MRs cannot be derived through Translate from any single block.

### 6.8.2 Main proposition: non-additivity of rod-bank reactivity worth is not Translate-reachable

**Definition 15 (Differential rod-bank reactivity worth, exact form).** For a base input $x_0 \in \mathcal{X}$ and a rod-bank operator $A \in \mathcal{O}_{\text{rod}}$, the (positive-convention) reactivity worth of $A$ is

$$d\rho(A; x_0) := \frac{1}{k_{\text{eff}}(P(x_0))} - \frac{1}{k_{\text{eff}}(P(\mathcal{O}_{\text{rod}}^A \cdot x_0))} > 0,$$

where $k_{\text{eff}}(P(x))$ denotes the dominant eigenvalue of the diffusion operator at configuration $x$. We write $d\rho(A \cup B; x_0)$ when both banks $A$ and $B$ are inserted simultaneously. Equivalently, in conventional reactor-physics notation, $d\rho(A; x_0) = \rho(x_0) - \rho(\mathcal{O}_{\text{rod}}^A \cdot x_0)$ where $\rho = 1 - 1/k_{\text{eff}}$ is the static reactivity. The exact form (1) avoids first-order perturbation-theoretic approximation; the standard adjoint-perturbation reading is given below.

**Definition 16 (Non-additivity of rod-bank reactivity worth, $\rho_{\text{nonadd}}$).** For two control-rod banks $A, B \in \mathcal{O}_{\text{rod}}$ with disjoint geometric supports and a base input $x_0$, define the mixed-difference functional

$$\Delta_{AB}(x_0) := d\rho(A \cup B; x_0) - d\rho(A; x_0) - d\rho(B; x_0).$$

The non-additivity metamorphic relation asserts: there exist disjoint-support banks $A, B$ and base input $x_0 \in \mathcal{X}$ in the standard PWR operating envelope (typical multi-bank insertion patterns of D, C, B, A control banks at partial insertions) such that

$$\rho_{\text{nonadd}}: \quad |\Delta_{AB}(x_0)| > \tau_{\text{nonadd}},$$

with $\tau_{\text{nonadd}} = 5$ pcm. This tolerance is calibrated to PWR engineering practice: empirical $|\Delta_{AB}|$ for adjacent rod banks ranges over $10^1$–$10^2$ pcm (Stamm'ler & Abbate Ch. 6); the tolerance $\tau_{\text{nonadd}} = 5$ pcm lies safely above PWR core-simulator iterative convergence tolerances (typically 0.1–1 pcm for $k_{\text{eff}}$) and below the physical signal magnitude. Selection of test bank configurations $(A, B)$ is the user's responsibility; the framework's failure to derive $\rho_{\text{nonadd}}$ is independent of the specific tolerance choice.

**Two physical regimes of $\Delta_{AB}$**: when $\Delta_{AB}(x_0) > 0$ for adjacent or geometrically overlapping rod banks, the standard PWR designation is *positive shadowing* (the worth of the second bank is reduced because the adjoint flux $\phi^\dagger$ is depressed in $A$'s geometric support). Positive shadowing is the dominant regime in conventional PWR analyses; it is the phenomenon explicitly addressed in NRC SER reviews of SIMULATE-3/5, ANC, and PARCS, with typical magnitudes of $50$–$500$ pcm for adjacent bank pairs. When $\Delta_{AB}(x_0) < 0$ for distant banks under asymmetric insertion patterns, the designation is *anti-shadowing*; this is a secondary but routinely measurable regime in standard commercial PWRs (typical magnitudes $5$–$20$ pcm for distant bank pairs in 4-loop Westinghouse and EPR configurations), and is more pronounced in small-core or strongly asymmetric insertion patterns. Both regimes are routinely measured in PWR startup physics testing and are documented in Stamm'ler & Abbate (Ch. 6) as second-order but non-negligible phenomena that core simulators must reproduce. The MR $\rho_{\text{nonadd}}$ is direction-agnostic and covers both; the test only requires that $|\Delta_{AB}|$ exceed the tolerance, irrespective of sign. Both regimes are accessible to a verifying core simulator regardless of whether the engineering analysis is concerned primarily with one or the other.

**Standard adjoint-perturbation reading (informative, not load-bearing for the proof).** Under first-order perturbation theory (Bell & Glasstone §6.3; Lewis & Miller §4.4), the worth of bank $B$ in the configuration where bank $A$ is already inserted is

$$d\rho(B; A, x_0) \approx -\frac{\langle \phi^\dagger_A, \, \delta H_B \, \phi_A \rangle}{\langle \phi^\dagger_A, \, F_A \, \phi_A \rangle},$$

where $(\phi_A, \phi^\dagger_A)$ are the forward and adjoint principal eigenfunctions of the $A$-rodded but $B$-unrodded core, $F_A = \chi \nu \Sigma_f$ is the fission source operator at that configuration, and $\delta H_B$ is the operator perturbation produced by inserting $B$ (which generally affects $\Sigma_a$, $\Sigma_t$, and the scattering kernel). The adjoint flux $\phi^\dagger_A$ is the principal eigenfunction of a structurally different adjoint operator $H^\dagger_A$ from $\phi^\dagger_\emptyset$ (the unrodded adjoint): in particular, $\phi^\dagger_A$ is locally depressed in $A$'s geometric support and globally redistributed elsewhere. The non-additivity $\Delta_{AB} \neq 0$ thus follows from $\phi^\dagger_A \neq \phi^\dagger_\emptyset$, which is a consequence of $H^\dagger_A \neq H^\dagger_\emptyset$. The exact form (1) does not require this perturbation-theoretic reading; the proof below uses only the eigenvalue definitions.

**Proposition 1 (Non-additivity is not Translate-reachable on $\mathcal{A}_{\text{PWR}}$).**
*Let $\mathcal{A}_{\text{PWR}}$ be the PWR core diffusion algebra of §6.8.1, with eight-block decomposition $\mathcal{D}(\mathcal{A}_{\text{PWR}})$. For every block $s \in \mathcal{D}(\mathcal{A}_{\text{PWR}})$ and every invariant $\iota \in \mathcal{I}_s$, $\mathrm{Translate}(\iota, s) \neq \rho_{\text{nonadd}}$. Equivalently, $\rho_{\text{nonadd}} \notin \mathrm{MR}(\mathcal{A}_{\text{PWR}})$ in the sense of Definition 13.*

The proof, by exhausting the eight blocks against the per-block Translate templates of Table 6, is given in Appendix C.6.

**Engineering significance.** Non-additivity of control-bank reactivity worth is a textbook PWR safety phenomenon. Bell & Glasstone (*Nuclear Reactor Theory*, §10.4) and Lewis & Miller (*Computational Methods of Neutron Transport*, §4.4) treat the underlying adjoint-perturbation mechanism; Stamm'ler & Abbate (*Methods of Steady-State Reactor Physics in Nuclear Design*, Ch. 6) document its operational consequences in PWR rod-worth measurements. Non-additivity is observed in both critical and sub-critical PWR core configurations, with the sub-critical regime exhibiting larger adjoint-flux distortions and correspondingly larger $|\Delta_{AB}|$. PWR core simulators are required by regulatory practice (e.g. NRC SER for SIMULATE-3/5, ANC, PARCS; cf. NRC Regulatory Guide 1.77 on rod-ejection accident analysis where rod-worth modeling accuracy is a critical input) to reproduce the worth functional with sub-percent accuracy across multi-bank insertion patterns. A framework that cannot, in principle, derive this MR from its algebraic input is missing structural content that PWR engineers routinely test for.

### 6.8.3 Supporting proposition: second-order mixed dependence of $k_{\text{eff}}$ on moderator temperature and boron concentration

**Definition 17 (MTC-vs-boron mixed-derivative MR, $\rho_{\text{MTC-bor}}$).** Let $k_{\text{eff}}(T_{\text{mod}}, C_B; \xi_0)$ denote the dominant eigenvalue of the PWR core diffusion operator as a function of moderator temperature $T_{\text{mod}}$ and soluble-boron concentration $C_B$, holding fixed the auxiliary state $\xi_0 = (\text{BU}_0, T_{\text{fuel},0}, \text{geometry}, \text{loading pattern}, \text{rod-bank position})$. Define the static reactivity

$$\rho_{\text{static}}(T_{\text{mod}}, C_B; \xi_0) := 1 - \frac{1}{k_{\text{eff}}(T_{\text{mod}}, C_B; \xi_0)},$$

expressed in pcm units ($1$ pcm $= 10^{-5}$). The moderator temperature coefficient (MTC) at $(T_{\text{mod}}, C_B; \xi_0)$ is the partial derivative of static reactivity with respect to moderator temperature, in standard PWR engineering convention (Bell & Glasstone §10.3; Stacey, *Nuclear Reactor Physics* §3.4):

$$\alpha_{\text{MTC}}(T_{\text{mod}}, C_B; \xi_0) := \left.\frac{\partial \rho_{\text{static}}}{\partial T_{\text{mod}}}\right|_{C_B, \xi_0 \text{ fixed}}, \quad \text{(units: pcm/°F or pcm/°C)}.$$

The second-order mixed dependence MR asserts: for $(T_{\text{mod}}, C_B; \xi_0)$ in the standard PWR operating envelope at hot-full-power (HFP), all-rods-out (ARO) reference conditions (typical: $T_{\text{mod}} \in [290, 320]$°C, $C_B \in [0, 2000]$ ppm, $\text{BU}_0 \in [0, 50]$ GWd/tU, full-power $T_{\text{fuel},0}$), the mixed second partial derivative satisfies

$$\rho_{\text{MTC-bor}}: \quad \left|\frac{\partial^2 \rho_{\text{static}}}{\partial T_{\text{mod}} \, \partial C_B}\right| > \tau_{\text{MTC-bor}},$$

with $\tau_{\text{MTC-bor}} = 0.01$ pcm/°F/ppm (equivalently $\sim 1.8 \times 10^{-2}$ pcm/°C/ppm). This tolerance is calibrated to PWR engineering practice: the empirical value of $\partial \alpha_{\text{MTC}}/\partial C_B$ in Westinghouse/Framatome PWR designs ranges over $0.02$–$0.04$ pcm/°F/ppm at BOC-to-EOC cycle conditions (Stacey §3.4; Lamarsh & Baratta *Introduction to Nuclear Engineering* §8.3); the tolerance $\tau_{\text{MTC-bor}} = 0.01$ pcm/°F/ppm lies safely below this physical magnitude and well above PWR core-simulator differential-perturbation noise (typically $\sim 10^{-3}$ pcm/°F/ppm for converged eigenvalue calculations).

**Note on equivalent formulations.** Since $\rho_{\text{static}} = 1 - 1/k_{\text{eff}}$ and $k_{\text{eff}} \approx 1$ at critical PWR conditions, $\partial \rho_{\text{static}}/\partial T_{\text{mod}} = (1/k_{\text{eff}}^2) \partial k_{\text{eff}}/\partial T_{\text{mod}} \approx \partial k_{\text{eff}}/\partial T_{\text{mod}}$ to within $\sim 10^{-4}$ relative error. The MR may equivalently be expressed in terms of $|\partial^2 k_{\text{eff}}/(\partial T_{\text{mod}} \partial C_B)| > \tau_{\text{MTC-bor}}$ with the same tolerance, modulo this $k$-vs-$\rho$ scaling factor; the algebraic argument of Appendix C.6.3 (which depends only on $k_{\text{eff}}$ being an operator-spectrum quantity) applies identically to either formulation.

**Equivalent formulation in terms of MTC.** Definition 17 is equivalent to asserting

$$\left|\frac{\partial \alpha_{\text{MTC}}(T_{\text{mod}}, C_B; \xi_0)}{\partial C_B}\right| > \tau_{\text{MTC-bor}}$$

at HFP, ARO conditions. Physically, this captures the well-established PWR design property that MTC becomes monotonically more negative as $C_B$ decreases from BOC values ($\sim$1500 ppm) to EOC values ($\sim$0 ppm). At HFP operating conditions, MTC is regulated to be $\le 0$ pcm/°F across the entire operating range per 10 CFR 50 Appendix A General Design Criterion 11; the slope $\partial \alpha_{\text{MTC}}/\partial C_B$ governs how rapidly MTC moves toward more negative values as boron is depleted over the cycle, with typical magnitudes ranging from near-zero (at BOC, high boron) to $-30$ to $-50$ pcm/°F (at EOC, near-zero boron). At hot-zero-power (HZP) conditions, BOC MTC may approach zero or be slightly positive within the analytical envelope (a regime relevant to startup physics testing but not to power-operation safety analysis); HZP MTC is bounded by separate Technical Specifications limits.

The strength of $\partial \alpha_{\text{MTC}}/\partial C_B$ is the engineering target of "MTC-vs-boron concentration curve" calculations performed for every PWR cycle reload, and is governed by the competition between three physical mechanisms (Stacey §3.4):

(a) **Reduced moderation**: $T_{\text{mod}} \uparrow \Rightarrow$ moderator density $\downarrow \Rightarrow$ neutron moderation reduced $\Rightarrow$ thermal-flux fraction $\downarrow \Rightarrow$ fission rate $\downarrow$. Contributes a *negative* term to MTC.

(b) **Boron poison evacuation**: at high $C_B$, $T_{\text{mod}} \uparrow \Rightarrow$ moderator density $\downarrow \Rightarrow$ boron number density $\downarrow$ (since boron is dissolved in the moderator) $\Rightarrow$ boron absorption $\downarrow$. Contributes a *positive* term to MTC, partially cancelling (a). This term is proportional to $C_B$ and vanishes as $C_B \to 0$.

(c) **Spectrum hardening and $^{238}$U resonance enhancement**: $T_{\text{mod}} \uparrow \Rightarrow$ reduced moderation $\Rightarrow$ harder neutron spectrum $\Rightarrow$ enhanced $^{238}$U resonance absorption (Doppler-weighted by the fuel temperature) $\Rightarrow$ neutron loss $\uparrow$. Contributes a further *negative* term to MTC. This term is small for low-enriched UO$_2$ but becomes significant for MOX fuels and high-enrichment ($> 5$%) UO$_2$.

At high $C_B$ the partial cancellation from (b) is strong; mechanisms (a) and (c) are partially offset and MTC magnitude is small. At low $C_B$, mechanism (b) vanishes; mechanisms (a) and (c) dominate and MTC becomes strongly negative. The mixed second derivative $\partial^2 \rho_{\text{static}}/(\partial T_{\text{mod}} \partial C_B)$ measures the rate at which the boron-mediated cancellation is removed as $C_B$ decreases.

**Proposition 2 (MTC-vs-boron mixed dependence is not Translate-reachable).**
*Let $\mathcal{A}_{\text{PWR}}$ be the PWR core diffusion algebra of §6.8.1. For every block $s \in \mathcal{D}(\mathcal{A}_{\text{PWR}})$ and every invariant $\iota \in \mathcal{I}_s$, $\mathrm{Translate}(\iota, s) \neq \rho_{\text{MTC-bor}}$. Equivalently, $\rho_{\text{MTC-bor}} \notin \mathrm{MR}(\mathcal{A}_{\text{PWR}})$ in the sense of Definition 13.*

The proof, by reducing the obstruction to the high-order-mixed-difference structure of $\rho_{\text{MTC-bor}}$ and verifying that no per-block $\pi$ template captures such structure, is given in Appendix C.6.

**Engineering significance.** The "MTC vs. boron concentration curve" is computed for every PWR cycle reload as part of the safety-analysis report submitted to regulators. The curve underlies the moderator temperature coefficient surveillance requirement at hot-full-power, all-rods-out conditions, where MTC must satisfy a stated upper limit ($\le 0$ pcm/°F per 10 CFR 50 Appendix A General Design Criterion 11; specific numerical limits are given in plant-specific Technical Specifications). The slope $\partial \alpha_{\text{MTC}}/\partial C_B$ is the key sensitivity parameter for projecting MTC behavior across the cycle from a small number of measurement points (typically four-to-six points per cycle, measured at quarter-cycle intervals): it is computed by each cycle-reload core simulator run and reported to the operator. Measurement uncertainties and prediction protocols are documented in ANS 19.6.1 (*Reload Startup Physics Tests for Pressurized Water Reactors*, 2011). A core simulator that cannot reproduce the slope to within the tolerance of $\tau_{\text{MTC-bor}}$ would fail the cycle-reload qualification process. The MR is therefore not a textbook curiosity; it is a routine and regulatory-essential output of every PWR core simulator.

### 6.8.4 Five independent structural obstructions

The two propositions are independent in the strong sense that no single extension of NOETHER's $\mathrm{Translate}$ repairs both:

| Proposition | Failure mode | Required extension to $\mathrm{Translate}$ |
|---|---|---|
| 1 (non-additivity) | Output is an algebraic-spectrum quantity ($k_{\text{eff}}$ as an eigenvalue, not in $\mathcal{Y}$) | Operator-spectrum output relations on $\pi$'s codomain |
| 1 (non-additivity) | Worth functional is non-additive (failure of semigroup homomorphism) | Homomorphism-failure $\pi$-template alongside equivariance / monotonicity / self-adjointness |
| 1 (non-additivity) | Adjoint weighting function $\phi^\dagger_X$ varies with operator history $X$ | Configuration-indexed adjoint structure on $T^*$ |
| 2 (mixed derivative) | MR is a non-zero second-order mixed partial derivative, not a first-order relation | Higher-order mixed-difference $\pi$-templates (currently all $\pi$ templates are first-order) |
| 2 (mixed derivative) | MR involves two independent parameter directions ($T_{\text{mod}}, C_B$) jointly, not chained or single-direction | Two-direction joint parametric dependence beyond the single-$\theta$ partial order of Definition 11 |

The five rows in this table identify *five pairwise-independent structural features* of $\mathrm{Translate}$ that are absent in Definition 12. Each row, considered alone, would require a specific extension of Definition 12; no single extension covers any two rows simultaneously. The eight-block decomposition (Hypothesis 1) is therefore not the only constraint on the framework's reach; the **shape of $\mathrm{Translate}$ itself** is.

The two MRs $\rho_{\text{nonadd}}$ and $\rho_{\text{MTC-bor}}$ are also *physically independent*: they probe disjoint physical mechanisms (rod-induced adjoint distortion vs. moderator-poison density coupling), and a PWR core simulator could pass one MR while failing the other (and vice versa). They are therefore complementary verification targets, not duplicates of a single underlying property.

### 6.8.5 What this section establishes and does not establish

**Established.** Theorem 1′ (Conjecture D) is false on $\mathcal{A}_{\text{PWR}}$: there exist two specific MRs—each empirically realised on every conforming PWR core simulator and each documented in standard PWR safety-analysis literature and regulatory guidance—that are formulable over $\mathcal{A}_{\text{PWR}}$'s operators but not in $\mathrm{MR}(\mathcal{A}_{\text{PWR}})$ in the sense of Definition 13. The two MRs identify five pairwise-independent structural obstructions in $\mathrm{Translate}$'s present signature.

**Not established.** That Theorem 1 itself fails. Theorem 1's closure result is over $\mathrm{MR}(\mathcal{A}_{\text{PWR}})$ as defined by Definition 13; the two MRs of this section lie *outside* that set, so they are out-of-scope for Theorem 1 and consistent with it. The proper characterisation is that Theorem 1 is a substantially weaker statement than Theorem 1′ pretended to be, and the gap is now exhibited concretely with two independent witness MRs.

**Not established.** That a Composite-Translate extension of NOETHER would absorb these two MRs while preserving Theorem 1's closure and Theorem 2's polynomial-time decidability. This is the principal open problem the negative instantiation leaves to follow-up work. The five obstructions of §6.8.4 are pairwise independent, so any candidate extension must address them jointly rather than sequentially.
```

---

### A.2 Appendix C.6（新增附录章节）

> **插入位置**：在原论文 Appendix D 的 §C.5 "Out-of-scope MRs: three concrete classes" 之后、Appendix E 之前，新增 §C.6。

```markdown
## C.6 Proofs for §6.8: Negative instantiation on $\mathcal{A}_{\text{PWR}}$

This appendix supplies the proofs for Propositions 1 and 2 of §6.8. The proof structure for both is the same: enumerate the eight blocks of $\mathcal{D}(\mathcal{A}_{\text{PWR}})$, instantiate the per-block Translate template of Table 6, and verify by inspection that no invariant $\iota \in \mathcal{I}_s$ yields the target MR. The block-by-block exclusions in Proposition 1's proof are the most detailed; Proposition 2 reuses the same exclusion pattern with the obstruction localised to the $O_\le$ block.

### C.6.1 Proof of Proposition 1 (non-additivity is not Translate-reachable)

*Statement.* For $\rho_{\text{nonadd}}$ as in Definition 16 and every $s \in \mathcal{D}(\mathcal{A}_{\text{PWR}})$, every $\iota \in \mathcal{I}_s$: $\mathrm{Translate}(\iota, s) \neq \rho_{\text{nonadd}}$.

*Proof.*

We use the exact-form definition of $d\rho$ (Definition 15) throughout, which depends only on dominant eigenvalues $k_{\text{eff}}$ of operators in $\mathcal{A}_{\text{PWR}}$. The adjoint-perturbation reading of §6.8.2 is the physical motivation but is not invoked in any case below.

**Case $s = G$.** By Definition 11, an invariant $\iota \in \mathcal{I}_G$ has the form $(\Phi, \pi)$ with $\Phi \subseteq G$ a finite operator family and $\pi$ a relation on tuples $(x_i, P(x_i))_{i=1}^{k}$ obtained by applying $\Phi$ to a base input $x_0$. By Table 6 (Appendix D), the canonical $\mathrm{Translate}$ template for $G$ is the equivariance schema

$$\mathrm{Translate}(\iota, G) \equiv \forall x_0 \ \forall g \in \Phi : \ P(g \cdot x_0) = \rho(g) \cdot P(x_0).$$

Two structural mismatches with $\rho_{\text{nonadd}}$:

(a) **Operator-spectrum output, not $P$ output.** $\rho_{\text{nonadd}}$ is an inequality between sums of $1/k_{\text{eff}}$ values, where each $k_{\text{eff}}$ is the dominant eigenvalue of a configuration-specific diffusion operator $H_X \in \mathcal{A}_{\text{PWR}}$. The dominant eigenvalue is a *spectral* quantity of the operator, obtained as part of the simultaneous solution $(k_{\text{eff}}, \phi)$ of $H \phi = (1/k_{\text{eff}}) F \phi$; it is not a function of $P(x)$ alone but a property of the operator $H$ itself. Translate's output relation $\pi$ in Definition 11 ranges over $(\mathcal{X} \times \mathcal{Y})^k$, where $\mathcal{Y}$ is the program output space (flux distributions, in this case). Operator-spectrum quantities are not in $\mathcal{Y}$; they are scalar invariants of operators in $\mathcal{O}$, lying outside Translate's signature by construction.

(b) **Non-additivity is not equivariance.** Even granting a charitable extension to admit $k_{\text{eff}}$ as a derived output, the $G$-template asserts equivariance of the output under the action of $\Phi$: $P(g \cdot x_0)$ is determined by $g$ and $P(x_0)$ through the representation $\rho(g)$. $\rho_{\text{nonadd}}$ asserts that the worth functional $d\rho: \mathcal{O}_{\text{rod}} \to \mathbb{R}_{>0}$ is *not a semigroup homomorphism*: $d\rho(A \cup B) \neq d\rho(A) + d\rho(B)$. Failure of homomorphism is not equivariance failure—it is the absence of an additive structure-preserving map, which has no expression in the equivariance template $\pi$ for $G$. No $\iota \in \mathcal{I}_G$ yields $\rho_{\text{nonadd}}$.

**Case $s = O_\le$.** By Table 6 row 2, the $O_\le$ template is the absolute-monotonicity schema

$$\mathrm{Translate}(\iota, O_\le) \equiv \forall x_1, x_2 : \ x_1 \le_\theta x_2 \implies P(x_1) \le_\mathcal{Y} P(x_2).$$

$\rho_{\text{nonadd}}$ is a *quaternary relation* on the four configurations $(x_0, \mathcal{O}^A x_0, \mathcal{O}^B x_0, \mathcal{O}^{A\cup B} x_0)$: it asserts a non-vanishing mixed second difference

$$\Delta_{AB}(x_0) = \big[k_{\text{eff}}^{-1}(P(x_0)) - k_{\text{eff}}^{-1}(P(\mathcal{O}^{A\cup B} x_0))\big] - \big[k_{\text{eff}}^{-1}(P(x_0)) - k_{\text{eff}}^{-1}(P(\mathcal{O}^A x_0))\big] - \big[k_{\text{eff}}^{-1}(P(x_0)) - k_{\text{eff}}^{-1}(P(\mathcal{O}^B x_0))\big] \neq 0$$

(where the subtractions use Definition 15's positive-worth convention). The $O_\le$ template captures binary monotonicity between two points along a single partial order $\le_\theta$. The mixed-difference structure of $\rho_{\text{nonadd}}$ requires comparison across four configurations forming a "rectangle" $\{x_0, \mathcal{O}^A x_0, \mathcal{O}^B x_0, \mathcal{O}^{A\cup B} x_0\}$ with two independent perturbation directions (insertion of $A$ and insertion of $B$); no $\le_\theta$ relates all four pairwise into a single chain. Furthermore, the assertion is *non-vanishing of a difference*, not a directional inequality—it is direction-agnostic, capturing both shadowing ($\Delta > 0$) and anti-shadowing ($\Delta < 0$). The $O_\le$ template's $\le_\mathcal{Y}$ is a directional partial order, not a non-vanishing constraint. No $\iota \in \mathcal{I}_{O_\le}$ yields $\rho_{\text{nonadd}}$.

**Case $s = T^*$.** By Table 6 row 3, the $T^*$ template asserts $\langle L \, P(x_1), P(x_2)\rangle = \langle P(x_1), L \, P(x_2)\rangle$ for a single self-adjoint operator $L$ in a fixed inner product. The structural mismatch with $\rho_{\text{nonadd}}$ has two components:

(i) **Single operator $L$ vs. configuration-indexed family.** The exact $d\rho$ values entering $\rho_{\text{nonadd}}$ are eigenvalues of *four distinct diffusion operators* $H_\emptyset, H_A, H_B, H_{A\cup B}$, each self-adjoint within its own configuration but pairwise distinct as operators. The $T^*$ template's $L$ is fixed; it does not range over a configuration-indexed family $\{H_X\}_{X \in \mathcal{O}_{\text{rod}}}$. The self-adjointness of any single $H_X$ does not imply or constrain a relation between eigenvalues of *different* $H_X$'s.

(ii) **Adjoint weighting function depends on configuration.** Under the standard adjoint-perturbation reading (Bell & Glasstone §6.3; Lewis & Miller §4.4), each $d\rho(B; X)$ for $X \in \{\emptyset, A\}$ admits the first-order representation

$$d\rho(B; X) \approx -\frac{\langle \phi^\dagger_X, \, \delta H_B \, \phi_X \rangle}{\langle \phi^\dagger_X, \, F_X \, \phi_X \rangle},$$

with $(\phi_X, \phi^\dagger_X)$ the principal eigenfunctions of $(H_X, H^\dagger_X)$. The Hilbert-space inner product $\langle \cdot, \cdot \rangle = \int (\cdot)(\cdot) \, d\Omega \, dE \, d\mathbf{r}$ is unchanged across $X$. What changes across $X$ is the *adjoint weighting function* $\phi^\dagger_X$, which is the principal eigenfunction of a structurally different adjoint operator $H^\dagger_X$ from $H^\dagger_\emptyset$ (because $H_X$ contains $A$'s absorbing material whereas $H_\emptyset$ does not). $\phi^\dagger_A$ is locally depressed in $A$'s geometric support and globally redistributed elsewhere; this is the adjoint-perturbation root cause of the non-additivity $d\rho(A\cup B) \neq d\rho(A) + d\rho(B)$.

The $T^*$ template's structure—single $L$, fixed inner product, asserting $\langle L x_1, x_2 \rangle = \langle x_1, L x_2 \rangle$—has no place to express "the weighting function $\phi^\dagger$ entering the inner product is itself the principal eigenfunction of a configuration-indexed adjoint operator and changes when configuration changes". This is a configuration-dependent adjoint structure, not a self-adjointness identity on a single operator.

No $\iota \in \mathcal{I}_{T^*}$ yields $\rho_{\text{nonadd}}$.

**Case $s = T_{\text{rev}}^*$.** The PWR diffusion operator $-\nabla \cdot D \nabla + \Sigma_a$ is irreversible: it is parabolic (transient form) or elliptic (steady-state form), neither of which admits a time-reversal involution on the relevant solution sub-family. Hence $T_{\text{rev}}^*_{\text{PWR}} = \emptyset$, and vacuously no $\iota \in \mathcal{I}_{T_{\text{rev}}^*}$.

**Case $s = L^*$.** By Table 6 row 5, the $L^*$ template is a convergence statement $\|P_\theta - P_{\theta^*}\|_* = O(f(\theta))$ at a parametric limit. $\rho_{\text{nonadd}}$ contains no limit operation: it is a strict inequality at finite, fixed configurations $(\emptyset, A, B, A\cup B, x_0)$. No $\iota \in \mathcal{I}_{L^*}$.

**Case $s = D^*$.** By Table 6 row 6, the $D^*$ template asserts a qualitative-feature relation (extremum, monotonicity, S-curve) on a solution trajectory $\xi(t)$. $\rho_{\text{nonadd}}$ is a steady-state inequality between four reactivity values; it does not concern trajectory shapes. No $\iota \in \mathcal{I}_{D^*}$.

**Case $s = E^*$.** By Table 6 row 7, the $E^*$ template compares two *methods* $M_1, M_2$ on a benchmark family. $\rho_{\text{nonadd}}$ compares four *operator configurations* on a single fixed method (the same diffusion solver $P$ in all four worth values). No $\iota \in \mathcal{I}_{E^*}$.

**Case $s = B_{\text{rel}}^*$.** Per §6.7, $B_{\text{rel}}^*$ is non-empty only on program families with idempotent-semiring rewriting structure. The PWR diffusion solution operator algebra does not carry such structure (no rewriting rules between core states preserve evaluation under all valid inputs). $B_{\text{rel}}^*_{\text{PWR}} = \emptyset$. Vacuously no $\iota \in \mathcal{I}_{B_{\text{rel}}^*}$.

This exhausts $\mathcal{D}(\mathcal{A}_{\text{PWR}})$. For every block $s$ and every $\iota \in \mathcal{I}_s$, $\mathrm{Translate}(\iota, s) \neq \rho_{\text{nonadd}}$. Hence $\rho_{\text{nonadd}} \notin \mathrm{MR}(\mathcal{A}_{\text{PWR}})$. $\square$

### C.6.2 Remark: three obstructions identified by Proposition 1's proof

Proposition 1's proof identifies three independent structural obstructions in $\mathrm{Translate}$'s present definition:

(O1) **Operator-spectrum output is not in $\mathcal{Y}$.** $\rho_{\text{nonadd}}$ asserts a relation between $1/k_{\text{eff}}$ values, where each $k_{\text{eff}}$ is a dominant eigenvalue of an operator $H_X$. Translate's $\pi$ in Definition 11 ranges over $(\mathcal{X} \times \mathcal{Y})^k$; eigenvalues of operators in $\mathcal{O}$ are scalar invariants of those operators, not elements of $\mathcal{Y}$.

(O2) **Output relation is non-additivity (failure of homomorphism), not equivariance, partial order, or self-adjointness.** The worth functional $d\rho: \mathcal{O}_{\text{rod}} \to \mathbb{R}$ is not a semigroup homomorphism; this is a third type of algebraic relation distinct from the equivariance, monotonicity, and self-adjointness expressed by Translate's per-block $\pi$ templates.

(O3) **The adjoint weighting function $\phi^\dagger_X$ entering the $T^*$ block's inner product is configuration-dependent.** While the Hilbert-space measure $d\Omega \, dE \, d\mathbf{r}$ is fixed, the eigenfunction $\phi^\dagger_X$ varies with $X$ because $H^\dagger_X$ varies with $X$. Definition 5 fixes the self-adjoint operator $L$ once; it does not admit a configuration-indexed family $\{L_X\}$ with $L_X$'s spectrum varying with $X$.

A constructive resolution of Proposition 1's obstructions would require Translate to admit (i) operator-spectrum output relations (eigenvalues, integrals, ratios as the targets of $\pi$), (ii) homomorphism-failure relations as a $\pi$-template type alongside equivariance / monotonicity / self-adjointness, and (iii) configuration-dependent adjoint structure on $T^*$.

### C.6.3 Proof of Proposition 2 (MTC-vs-boron mixed dependence is not Translate-reachable)

*Statement.* For $\rho_{\text{MTC-bor}}$ as in Definition 17 and every $s \in \mathcal{D}(\mathcal{A}_{\text{PWR}})$, every $\iota \in \mathcal{I}_s$: $\mathrm{Translate}(\iota, s) \neq \rho_{\text{MTC-bor}}$.

*Proof.*

The principal obstruction is in the $O_\le$ block; we treat that case in detail and abbreviate the others.

**Case $s = O_\le$.** By Table 6 row 2, the $O_\le$ template is the absolute-monotonicity schema

$$\mathrm{Translate}(\iota, O_\le) \equiv \forall x_1, x_2 : \ x_1 \le_\theta x_2 \implies P(x_1) \le_\mathcal{Y} P(x_2),$$

a *first-order* statement asserting a binary relation between $P(x_1)$ and $P(x_2)$ at $\theta$-comparable inputs along a single partial-order direction $\le_\theta$.

$\rho_{\text{MTC-bor}}$ asserts a *non-zero second-order mixed partial derivative* of $k_{\text{eff}}$ with respect to two *independent* parameter directions $T_{\text{mod}}$ and $C_B$:

$$\left|\frac{\partial^2 k_{\text{eff}}}{\partial T_{\text{mod}} \, \partial C_B}\right| > \tau_{\text{MTC-bor}}.$$

Two independent obstructions in the $O_\le$ template:

(a) **Order vs. mixed-derivative structure.** The mixed second derivative is the limit of a four-point finite-difference quotient over a "rectangle" $\{(T_0, C_0), (T_0+\Delta T, C_0), (T_0, C_0+\Delta C), (T_0+\Delta T, C_0+\Delta C)\}$:

$$\frac{\partial^2 k_{\text{eff}}}{\partial T_{\text{mod}} \, \partial C_B} = \lim_{\Delta T, \Delta C \to 0} \frac{k_{\text{eff}}(T_0+\Delta T, C_0+\Delta C) - k_{\text{eff}}(T_0, C_0+\Delta C) - k_{\text{eff}}(T_0+\Delta T, C_0) + k_{\text{eff}}(T_0, C_0)}{\Delta T \cdot \Delta C}.$$

This is structurally a *four-point relation*, not a two-point relation. The $O_\le$ template's $\pi$ relates $(P(x_1), P(x_2))$ pairwise; it has no expression for a four-point combination weighted by $1/(\Delta T \cdot \Delta C)$. Equivalently, the canonical input-tuple-generation rule for $O_\le$ in Table 6 produces tuples $(x_1, x_2)$ with $x_1 \le_\theta x_2$, not 2-by-2 perturbation rectangles.

(b) **Two independent parameter directions.** The mixed derivative requires *jointly varying* $T_{\text{mod}}$ and $C_B$ along two independent directions. The $O_\le$ template's $\le_\theta$ is a *single* partial order on $\mathcal{X}$ (or on a single coordinate of $\mathcal{X}$). Even granting the construction of a product order $\le_T \times \le_C$ on a 2-D parameter slice of $\mathcal{X}$, the $\pi$ relation still applies along the order chain as a directional inequality, not as a non-vanishing-second-difference statement. The two independent parameter directions are perpendicular, not chained; the $\le_\theta$ formalism collapses them into one chain only by losing the non-vanishing-mixed-difference content.

Furthermore, $\rho_{\text{MTC-bor}}$'s output is again $k_{\text{eff}}$, an operator-spectrum quantity (cf. Proposition 1 Case $G$ obstruction (a)). This gives a *third* obstruction in $O_\le$: even if mixed-second-derivative structure could be embedded into $\pi$, the output value would not lie in $\mathcal{Y}$.

No $\iota \in \mathcal{I}_{O_\le}$ yields $\rho_{\text{MTC-bor}}$.

**Other blocks.**

*Case $s = G$.* No group action in $\mathcal{A}_{\text{PWR}}$ relates $(T_{\text{mod}}, C_B)$ pairs at different parameter values to each other through equivariance: $T_{\text{mod}}$ and $C_B$ are continuous parameters acting on the cross-section library, not group-action coordinates. Even if a charitable embedding in $G$ were attempted, the same operator-spectrum-output obstruction (Proposition 1 Case $G$ (a)) applies: $k_{\text{eff}}$ is not in $\mathcal{Y}$.

*Case $s = T^*$.* The MTC operator $\partial/\partial T_{\text{mod}}$ is not self-adjoint in any natural inner product on the diffusion-solution space (the parameter $T_{\text{mod}}$ enters the cross-section coefficients of $H$ rather than $H$'s acting space, so $\partial H/\partial T_{\text{mod}}$ has no self-adjointness structure analogous to $H$ itself). No $\iota \in \mathcal{I}_{T^*}$.

*Case $s = T_{\text{rev}}^*$.* Empty for PWR diffusion. No $\iota \in \mathcal{I}_{T_{\text{rev}}^*}$.

*Case $s = L^*$.* $\rho_{\text{MTC-bor}}$ does not assert convergence at a parametric limit; it asserts a non-zero finite value of a mixed second derivative at a *finite* parameter point in the operating envelope. The mixed-derivative limit $\Delta T, \Delta C \to 0$ is the *definition* of the derivative, not the MR's claim—the MR's claim is that the resulting derivative exceeds $\tau_{\text{MTC-bor}}$, which is a non-vanishing condition at a finite parameter value, not a convergence rate. No $\iota \in \mathcal{I}_{L^*}$.

*Case $s = D^*$.* $\rho_{\text{MTC-bor}}$ concerns $k_{\text{eff}}$ as a function of two parameters at steady state; it does not involve a solution trajectory of an underlying ODE/PDE. No $\iota \in \mathcal{I}_{D^*}$.

*Case $s = E^*$.* The comparison is between two parameter regimes $(T_0, C_0)$ and $(T_0+\Delta T, C_0+\Delta C)$ of a single fixed method (the same PWR core simulator $P$ in all four eigenvalues), not between two methods. No $\iota \in \mathcal{I}_{E^*}$.

*Case $s = B_{\text{rel}}^*$.* Empty for $\mathcal{A}_{\text{PWR}}$. No $\iota \in \mathcal{I}_{B_{\text{rel}}^*}$.

This exhausts $\mathcal{D}(\mathcal{A}_{\text{PWR}})$. Hence $\rho_{\text{MTC-bor}} \notin \mathrm{MR}(\mathcal{A}_{\text{PWR}})$. $\square$

### C.6.4 Remark: two further obstructions identified by Proposition 2's proof

Proposition 2's proof identifies two further independent structural obstructions in $\mathrm{Translate}$'s present definition, beyond the three identified by Proposition 1:

(O4) **MR is a non-zero second-order mixed partial derivative, not a first-order relation.** All per-block $\pi$ templates in Table 6 are first-order: equivariance is a first-order identity $P(g x_0) = \rho(g) P(x_0)$; monotonicity is a first-order inequality $P(x_1) \le P(x_2)$; self-adjointness is a first-order pairing $\langle L x_1, x_2\rangle = \langle x_1, L x_2 \rangle$. Mixed second differences (and a fortiori higher-order mixed differences) have no expression in any of these.

(O5) **MR involves two independent parameter directions, joined as a 2-by-2 perturbation rectangle, not as a chain.** The $O_\le$ block's $\le_\theta$ is a single partial-order direction; even with multiple independent partial orders in $\mathcal{I}_{O_\le}$, the $\pi$ template relates pairwise inputs along a *single chosen direction*, not jointly across two perpendicular directions in a finite-difference rectangle.

A constructive resolution of Proposition 2's obstructions would require Translate to admit (iv) higher-order mixed-difference $\pi$-templates and (v) two-direction joint parametric dependence beyond the single-$\theta$ partial order of Definition 11.

### C.6.5 Combined corollary

**Corollary 2 (Theorem 1′ is false on $\mathcal{A}_{\text{PWR}}$, two-fold).**
*The MRs $\rho_{\text{nonadd}}, \rho_{\text{MTC-bor}}$ are each formulable over operators of $\mathcal{A}_{\text{PWR}}$ and each empirically realised on every conforming PWR core simulator. By Propositions 1 and 2, neither is in $\mathrm{MR}(\mathcal{A}_{\text{PWR}})$. The structural obstructions O1–O5 identified by the two proofs are pairwise distinct: no single extension of $\mathrm{Translate}$'s signature absorbs any two simultaneously, so the joint obstruction is irreducibly five-fold.*

**Remark 8.** A natural follow-up is to define a *Composite Translate* $\widetilde{\mathrm{Translate}}: \mathcal{I}_{s_1} \times \cdots \times \mathcal{I}_{s_k} \to \mathrm{MR}(P)$ that combines invariants from multiple blocks under a generalised $\pi$ template admitting (i) operator-spectrum output, (ii) homomorphism-failure relations, (iii) configuration-indexed adjoint structure, (iv) higher-order mixed differences, and (v) two-direction joint parametric dependence. Whether such an extension preserves Theorem 1's closure (now over $\widetilde{\mathrm{MR}}(\mathcal{A}_P)$) and Theorem 2's polynomial-time decidability is the principal open problem this section leaves to future work. Five independent extensions are needed; a single uniform Composite Translate covering all of them would be a substantive theoretical contribution.
```

---

## Part B — 对原文若干位置的修改

> 共 8 处修改。每处给出**原文片段**与**修改后片段**，以及定位说明。所有修改保持原文英文风格。
>
> **第 3 版相对第 2 版的差异**：B.1、B.2、B.4、B.7 中"three independent counterexamples"改为"two independent counterexamples"；"四个 obstructions"改为"五个 obstructions"；删除 ITC 与 Gd 反例的引用。其余四处文本基本不变。

### B.1 §1 Introduction — Contribution 列表 C2 修订

> **位置**：§1 Introduction，contribution 列表中的 **C2** 项。

**原文片段（C2）：**

```text
• C2. We prove an Algebraic Closure Theorem (Theorem 1) for the constructed set: given the
seven-block decomposition, the resulting MetaPattern set is closed over the algebra-induced
MR space under the framework's Translate operator. We also establish polynomial-time decidability when the algebra admits a finite generating set (Theorem 2), and identify absolute
completeness over arbitrary properties as an open problem (Theorem 1′). The scope of each
result is stated explicitly in Section 4.3.
```

**修改后片段：**

```text
• C2. We prove an Algebraic Closure Theorem (Theorem 1) for the constructed set: given the
eight-block decomposition, the resulting MetaPattern set is closed over the algebra-induced
MR space under the framework's Translate operator. We also establish polynomial-time
decidability when the algebra admits a finite generating set (Theorem 2). We further establish
that the strictly stronger statement of absolute completeness over arbitrary properties expressible in $\mathcal{A}_P$ (Theorem 1′ / Conjecture D) is false on the PWR core diffusion algebra
$\mathcal{A}_{\text{PWR}}$: two specific MRs from the standard PWR safety-analysis literature
(non-additivity of rod-bank reactivity worth, and second-order mixed dependence of $k_{\text{eff}}$
on moderator temperature and boron concentration) are formulable over $\mathcal{A}_{\text{PWR}}$ but
not in $\mathrm{MR}(\mathcal{A}_{\text{PWR}})$ (§6.8, Appendix C.6). The two MRs identify five
pairwise-independent structural obstructions in $\mathrm{Translate}$'s signature
(operator-spectrum output, homomorphism-failure $\pi$-template, configuration-indexed adjoint
structure, higher-order mixed-difference templates, two-direction joint parametric dependence)
as the principal open problem for follow-up work.
```

---

### B.2 §1 "Boundary of contribution"框 — 调整

**原文片段（"It does not establish:" 列表中的 (a)）：**

```text
(a) Absolute completeness over arbitrary properties expressible in $\mathcal{A}_P$. This is Theorem 1′
(Conjecture D in Appendix D) and remains open.
```

**修改后片段：**

```text
(a) Absolute completeness over arbitrary properties expressible in $\mathcal{A}_P$. This is
Theorem 1′ (Conjecture D, Appendix D); §6.8 establishes that it is false on the PWR core
diffusion algebra $\mathcal{A}_{\text{PWR}}$ via two independent counterexamples (non-additivity
of rod-bank reactivity worth, and second-order mixed dependence of $k_{\text{eff}}$ on moderator
temperature and boron concentration), but the question of whether a Composite-Translate
extension absorbs the five obstructions identified by the counterexamples while preserving
Theorem 1's closure and Theorem 2's polynomial-time decidability remains open.
```

---

### B.3 §3.9 — 在 Hypothesis 1 后新增 Remark

> **位置**：§3.9，Hypothesis 1 与 Remark 1 之间，新增一条 Remark。

**新增片段：**

```text
**Remark (Block sufficiency vs. Translate sufficiency).** Hypothesis 1 asserts that the eight
blocks suffice to *assign* every operator in $\mathcal{A}_P$ relevant to MR derivation. It does not
assert that every MR formulable over $\mathcal{A}_P$'s operators is reachable via the framework's
$\mathrm{Translate}$ operator from a single block invariant. Section 6.8 exhibits, on the PWR core
diffusion algebra $\mathcal{A}_{\text{PWR}}$, two MRs whose constituent operators are individually
assigned to blocks of $\mathcal{D}(\mathcal{A}_{\text{PWR}})$ (rod-insertion semigroup; boration
and moderator-temperature scaling), yet whose MR content is not in
$\mathrm{MR}(\mathcal{A}_{\text{PWR}})$ in the sense of Definition 13. The block decomposition is
therefore a necessary but not sufficient input to MetaPattern construction: $\mathrm{Translate}$'s
expressive form (single-block invariants, first-order $\pi$-template, single partial-order direction,
operating on $P(x)$ tuples rather than on operator-spectrum quantities) is a second, independent
constraint on the framework's reach. This distinction between "block sufficiency" (Hypothesis 1)
and "Translate sufficiency" (open) is made explicit in §6.8.4.
```

---

### B.4 §4.3 Theorem 1 后 Remark 2 — 增加交叉引用

**原文片段（Remark 2 末尾）：**

```text
The strictly stronger statement that every MR formulable as a property over $\mathcal{A}_P$'s
operators (without restricting to $\mathrm{Translate}$-reachable derivations) is contained in
some $m \in \mathcal{M}(\mathcal{A}_P)$ is identified as Theorem 1′ in Appendix D and remains
an open conjecture.
```

**修改后片段：**

```text
The strictly stronger statement that every MR formulable as a property over $\mathcal{A}_P$'s
operators (without restricting to $\mathrm{Translate}$-reachable derivations) is contained in
some $m \in \mathcal{M}(\mathcal{A}_P)$ is identified as Theorem 1′ in Appendix D. Section 6.8
and Appendix C.6 establish that this stronger statement is false on the PWR core diffusion
algebra $\mathcal{A}_{\text{PWR}}$, by exhibiting two concrete counterexamples
($\rho_{\text{nonadd}}, \rho_{\text{MTC-bor}}$) whose obstructions identify five structurally
independent extensions of $\mathrm{Translate}$'s signature. The combined open problem—whether
such an extended Translate preserves Theorem 1's closure and Theorem 2's polynomial-time
decidability—is the principal open question for follow-up work.
```

---

### B.5 §4.5 "The principal limitation" — 段尾增补

**原文片段：**

```text
NOETHER replaces inductive grounding with algebraic grounding downstream of $\mathcal{A}_P$.
Upstream, the distillation of $\mathcal{A}_P$ from a program family remains a human task. This
limitation is central to the framework's scope: NOETHER does not automate domain modelling,
but it turns the step after domain modelling into a well-defined construction.
```

**修改后片段：**

```text
NOETHER replaces inductive grounding with algebraic grounding downstream of $\mathcal{A}_P$.
Upstream, the distillation of $\mathcal{A}_P$ from a program family remains a human task. This
limitation is central to the framework's scope: NOETHER does not automate domain modelling,
but it turns the step after domain modelling into a well-defined construction. A second
limitation, made explicit in §6.8 and Appendix C.6, is that even when $\mathcal{A}_P$ is fully
specified, $\mathrm{Translate}$'s present signature (single-block, first-order $\pi$-template,
single partial-order direction, operating on $P(x)$ tuples rather than on operator-spectrum
quantities) systematically excludes a class of MRs that engineering practice treats as
standard—non-additivity of operator-composition functionals and higher-order mixed parametric
dependences. The principal limitation is therefore not only the upstream distillation of
$\mathcal{A}_P$ but also the present signature of $\mathrm{Translate}$.
```

---

### B.6 §7.1 Internal validity — 增加引用

**原文片段：**

```text
Internal validity. Theorem 1's uniqueness depends on the canonical-block ordering of Definition 14.
The proof in Appendix D catalogues every block-block interaction for the algebras instantiated.
The closure result is over algebra-induced MRs in the sense of Definition 13; out-of-scope MRs
that fall outside Definition 13 are catalogued in Appendix D.
```

**修改后片段：**

```text
Internal validity. Theorem 1's uniqueness depends on the canonical-block ordering of Definition 14.
The proof in Appendix D catalogues every block-block interaction for the algebras instantiated.
The closure result is over algebra-induced MRs in the sense of Definition 13; out-of-scope MRs
that fall outside Definition 13 are catalogued in Appendix D, and two concrete counterexamples
on the PWR core diffusion algebra are proved out-of-scope in Appendix C.6 (corresponding to
the negative instantiation of §6.8). The latter two jointly establish that Theorem 1′
(Conjecture D, absolute completeness) is false on $\mathcal{A}_{\text{PWR}}$, and identify five
independent extensions of $\mathrm{Translate}$'s signature as the locus of follow-up theoretical
work.
```

---

### B.7 §8 Conclusion — "Boundary of contribution" 框调整

**原文片段：**

```text
Boundary of contribution (Conclusion restatement)
Established. (i) Algebraic closure under Translate given a block decomposition (Theorem 1);
(ii) polynomial-time decidability under finite generating-set assumption (Theorem 2); (iii) three
non-vacuous instantiations across structurally distinct algebraic skeletons.
Open. (a) Absolute completeness (Theorem 1′, Conjecture D); (b) sufficiency of Hypothesis 1's
eight-block list (Remark 1's six out-of-scope classes are candidate ninth blocks); (c) superiority
over existing automated MR-identification pipelines on average defect distributions (the
comparative-evaluation protocol in §6.6 establishes effects, not averages); (d) elimination of
induction (relocated, not eliminated). Hypothesis 1 is the locus where future induction-eliminating
work should target.
```

**修改后片段：**

```text
Boundary of contribution (Conclusion restatement)
Established. (i) Algebraic closure under Translate given a block decomposition (Theorem 1);
(ii) polynomial-time decidability under finite generating-set assumption (Theorem 2); (iii) three
non-vacuous instantiations across structurally distinct algebraic skeletons; (iv) a negative
instantiation on the PWR core diffusion algebra $\mathcal{A}_{\text{PWR}}$ (§6.8, Appendix C.6),
in which two MRs from the standard PWR safety-analysis literature (non-additivity of rod-bank
reactivity worth, second-order mixed $T_{\text{mod}}$-vs-$C_B$ dependence of $k_{\text{eff}}$) are
proved not in $\mathrm{MR}(\mathcal{A}_{\text{PWR}})$, falsifying Theorem 1′ (Conjecture D) on a
structurally significant operator algebra and identifying five pairwise-independent extensions
of $\mathrm{Translate}$'s signature as the locus of repair.
Open. (a) Whether a Composite-Translate extension covering the five obstructions of §6.8.4 and
§C.6.4 preserves Theorem 1's closure and Theorem 2's polynomial-time decidability; (b)
sufficiency of Hypothesis 1's eight-block list (Remark 1's six out-of-scope classes are candidate
ninth blocks); (c) superiority over existing automated MR-identification pipelines on average
defect distributions (the comparative-evaluation protocol in §6.6 establishes effects, not
averages); (d) elimination of induction (relocated, not eliminated). Both Hypothesis 1 (block
sufficiency) and $\mathrm{Translate}$'s signature (Translate sufficiency) are the loci where
future induction-eliminating and completeness-establishing work should target.
```

---

### B.8 Appendix C.5 末尾 — 链接到 C.6

**新增片段（追加在 C.5.3 末尾）：**

```text
The three classes of §C.5.1–§C.5.3 are *abstract* characterisations of MRs outside Theorem 1's
scope. Appendix C.6 supplements them with two *concrete instances* drawn from the PWR core
diffusion algebra $\mathcal{A}_{\text{PWR}}$, each of which is empirically realised on every
conforming PWR core simulator and documented in the standard reactor-physics literature. Together
with §6.8, Appendix C.6 establishes that Theorem 1′ (Conjecture D) is false on
$\mathcal{A}_{\text{PWR}}$, and identifies five structural obstructions in $\mathrm{Translate}$'s
signature (operator-spectrum output, homomorphism-failure $\pi$-template, configuration-indexed
adjoint structure, higher-order mixed-difference templates, two-direction joint parametric
dependence) that any positive resolution would have to repair.
```

---

## Part C — 修改后整体一致性检查清单

完成 Part A、Part B 八处修改后，建议按以下清单核对全文一致性：

1. **Theorem 1′ 状态一致性。** 原文有 5 处提及 Theorem 1′（即 Conjecture D）作为"open"；修改后这些位置应统一为"在 $\mathcal{A}_{\text{PWR}}$ 上为假，Composite-Translate 扩展是否成立仍开放"。逐处核对：§1 contribution C2；§1 boundary; §4.3 Remark 2；§8 Conclusion；Appendix D §C.4。

2. **"七个 / 八个 block" 一致性。** 原文偶有"seven blocks"残留（§5.3 表 2 注释、§A.5 段首）；本方案 §A.1 已用 eight。需对全文做一次"seven block"全局搜索并统一。

3. **C2 contribution 计数。** 修改后 C2 涵盖三件事（closure、decidability、否证 Theorem 1′），可考虑拆为 C2a、C2b、C2c 或在 §1 中明确。

4. **图表编号。** §6.8 的 Definitions 15–17、Propositions 1–2 需在原文 LaTeX 模板中给出新计数器；Appendix C.6 的 Remark 编号需与原 Appendix D 衔接（建议 Remark 5–8）。

5. **物理一致性核对。** 关键术语统一：
   - **MR 名称**：通篇使用 `ρ_nonadd`（非可加性）和 `ρ_MTC-bor`（MTC-vs-硼浓度二阶混合偏导）。
   - **微扰公式**：标准带负号形式 `dρ ≈ −⟨φ†_A, δH_B φ_A⟩/⟨φ†_A, F_A φ_A⟩`，作为"informative reading"出现，不是证明的 load-bearing 部分。证明本身用 Definition 15 的 exact 1/k 差异形式。
   - **基态约定**：`(φ_X, φ†_X)` 明确为"X-rodded but B-unrodded"配置的基态本征对。
   - **测度 vs 权重函数**：Hilbert-space measure `dΩ dE dr` 不变；变化的是 adjoint weighting function `φ†_X`。这一区分在 §6.8.2 和 §C.6.1 Case T* 中明确。
   - **k_eff 是算子谱量**：在 §6.8.2 Definition 15、§C.6.1 Case G (a)、§C.6.2 (O1)、§C.6.3 Case $O_\le$ 后两段、§C.6.4 (O4) 均一致表述。
   - **MTC 单位约定（v4 修订）**：MTC 在反应堆物理工程标准中是反应性对温度的偏导 $\alpha_{\text{MTC}} = \partial \rho_{\text{static}}/\partial T_{\text{mod}}$，其中 $\rho_{\text{static}} = 1 - 1/k_{\text{eff}}$ 用 pcm 单位（$1$ pcm $= 10^{-5}$）。Definition 17 主形式用 $\rho_{\text{static}}$；Appendix C.6.3 证明用 $k_{\text{eff}}$ 形式（$k \approx 1$ 近似下二者等价，"Note on equivalent formulations"段说明）。
   - **MTC 工况限定（v4 修订）**：MR 参考工况为 hot-full-power (HFP), all-rods-out (ARO)；HFP 下 MTC 必须 $\le 0$（10 CFR 50 App. A GDC 11 监管）；HZP BOC 高硼下 MTC 可微正（启动物理试验工况，由各机组 Tech Specs 限定，不在 MR 主形式覆盖范围）。运行包络 $T_{\text{mod}} \in [290, 320]$°C, $C_B \in [0, 2000]$ ppm, $\text{BU}_0 \in [0, 50]$ GWd/tU。
   - **MTC 三机制描述（v4 修订）**：(a) 慢化降低（负贡献）+ (b) 高 $C_B$ 下硼负反馈（正贡献，正比于 $C_B$）+ (c) 谱硬化与 $^{238}$U 共振增强（负贡献，对 MOX 与高富集燃料显著）。Stacey §3.4 标准三机制论述。
   - **anti-shadowing（v4 修订）**：明确为标准 PWR 中的"次要但可测"现象（典型 5–20 pcm，相比相邻棒组 shadowing 的 50–500 pcm 小一个量级），在 PWR 启动物理试验中常规测量；并非"仅在小堆中出现"。

6. **References。** 引入了 PWR 反应堆物理的标准文献；需在 References 段补全：
   - Bell, G. I. and Glasstone, S. *Nuclear Reactor Theory*. Van Nostrand Reinhold, 1970.（已在原文 [6]）— 引用章节 §6.1（自伴随）、§6.3（一阶微扰）、§10.3（反应性温度系数）、§10.4（控制棒价值与 shadowing）。
   - Lewis, E. E. and Miller, W. F. *Computational Methods of Neutron Transport*. Wiley-Interscience, 1993.（已在原文 [23]）— 引用章节 §4.2、§4.4。
   - Stamm'ler, R. J. J. and Abbate, M. J. *Methods of Steady-State Reactor Physics in Nuclear Design*. Academic Press, 1983. — 新增引用，第 6 章关于控制棒价值的工程测量与 shadowing/anti-shadowing 的运行后果。
   - Stacey, W. M. *Nuclear Reactor Physics* (2nd ed.). Wiley-VCH, 2007. — 新增引用，§3.4 关于反应性温度系数的工程化论述（含三机制竞争模型）。
   - Lamarsh, J. R. and Baratta, A. J. *Introduction to Nuclear Engineering* (3rd ed.). Prentice Hall, 2001. — 新增引用，§8.3 关于 PWR MTC 与硼浓度依赖的入门级论述。
   - 10 CFR 50 Appendix A, *General Design Criterion 11: Reactor Inherent Protection*. — 新增引用，作为 PWR 反应性反馈系数监管要求的来源（HFP MTC ≤ 0 的硬性约束）。
   - ANS 19.6.1, *Reload Startup Physics Tests for Pressurized Water Reactors*, 2011. — 新增引用，作为 MTC 测量协议与不确定度量化的标准来源；用于 §6.8.3 末尾的"Engineering significance"段。
   - U.S. Nuclear Regulatory Commission, *Regulatory Guide 1.77: Assumptions Used for Evaluating a Control Rod Ejection Accident for Pressurized Water Reactors*. — 新增引用，**仅用于** §6.8.2 的 rod-worth 监管引用（控制棒价值精度要求是 RG 1.77 安全分析输入的一部分）；不再用于 ITC/MTC 引用。
   - PWR MR 文档（用户自有 PWR_MR_Analysis 报告，作为 in-house technical report 引用）。
   
   **不再引用**：v3 引用的 ANSI/ANS-51.1（*Nuclear Safety Criteria for the Design of Stationary Pressurized Water Reactor Plants*）已删除——该标准重点是 PWR 整体安全设计准则，对反应性反馈系数的具体约束并不在 51.1 中；MTC 监管的真正来源是 10 CFR 50 App. A GDC 11 + 各机组 Technical Specifications（具体限值在每个机组的 Tech Specs 中规定，不需在通用论文中引用）。

7. **Abstract 调整。** 原 abstract 末尾"comparative evaluation … pre-registered protocol rather than a claim of average superiority" 一句之后，可考虑增补一句反映 §6.8 的否证结果，例如：

   > "A negative instantiation on a fourth program family (PWR core simulators) falsifies the absolute-completeness conjecture (Theorem 1′) on a structurally significant operator algebra, via two independent counterexamples that jointly identify five pairwise-independent extensions of the framework's Translate operator as the principal locus of follow-up work."

---

## 第 4 版相对第 3 版的修订总结

按反应堆物理资深审稿意见，第 4 版对第 3 版的物理表述做 5 处修订（全部限定在 §6.8.2–§6.8.3 与引文清单，Appendix C.6 代数证明保持不变）：

| 修订项 | 第 3 版 | 第 4 版 |
|---|---|---|
| C1 anti-shadowing 描述 | "principally observed in small-core or non-standard geometries"（低估其在标准 PWR 中的可观测性） | "secondary but routinely measurable regime in standard commercial PWRs (typical $5$–$20$ pcm); both regimes routinely measured in PWR startup physics testing" |
| C2 Definition 17 单位 | $\|\partial^2 k_{\text{eff}}/(\partial T_{\text{mod}} \partial C_B)\|$（与 pcm/°F/ppm 容差混用单位） | $\|\partial^2 \rho_{\text{static}}/(\partial T_{\text{mod}} \partial C_B)\|$，其中 $\rho_{\text{static}} = 1 - 1/k_{\text{eff}}$，明确 pcm 单位约定 |
| C2 工况限定 | 含糊的"BOC ... MTC may be slightly positive" | HFP/HZP 工况明确区分；HFP MTC $\le 0$ 由 GDC 11 监管；HZP BOC 微正属启动物理试验工况 |
| C2 物理机制描述 | 双机制（慢化 + 硼负反馈） | 三机制（慢化 + 硼负反馈 + 谱硬化与 $^{238}$U 共振增强），与 Stacey §3.4 一致 |
| C2 引文 | 引用 ANSI/ANS-51.1（标准范围不含 MTC 具体约束） | 删除 ANSI/ANS-51.1；保留 GDC 11 + Stacey §3.4 + Lamarsh & Baratta §8.3；新增 ANS 19.6.1（PWR 启动物理测量协议）|

## 第 3 版相对第 2 版的修订总结（保留供参考）

按 ROI 评估与反应堆物理审稿意见，第 3 版的实质修订是：

| 维度 | 第 2 版 | 第 3 版 |
|---|---|---|
| 反例数量 | 3 个（C1, C2-ITC, C3-Gd） | 2 个（C1, C2-MTC-bor） |
| C1 物理表述 | 基本完整 | 修订两处：anti-shadowing 描述更克制；Definition 16 加入工程容差 $\tau_{\text{nonadd}} = 5$ pcm |
| C2 反例 | ITC 符号反转（与 PWR 监管约束矛盾、混淆 ITC 与 MTC、引文错误） | MTC 对 $C_B$ 的二阶混合偏导（PWR 工程实际计算量、引文严格） |
| C3 反例 | Gd 自屏蔽守恒约束（需重大物理细化） | 删除 |
| 代数失败模式覆盖 | 4 个（O1–O4） | 5 个（O1–O5，新增"高阶混合差分 + 两方向联合参数依赖"） |
| 总工作量 | 3 反例并行设计，物理风险高 | 2 反例严格设计，物理风险低 |

## 第 4 版的整体效果

v4 在 v3 的代数论证骨架（已经达到代数严谨度）基础上，把物理表述精度提升到反应堆物理审稿可发表水平：

(i) C1 anti-shadowing 描述符合 Stamm'ler & Abbate Ch. 6 的工程实际，避免审稿人质疑"标准 PWR 中是否一定出现 anti-shadowing"；

(ii) C2 单位约定遵循 Bell & Glasstone §10.3、Stacey §3.4 的反应堆物理标准（MTC 是 $\partial \rho/\partial T$ 而非 $\partial k/\partial T$），消除单位混用的技术性错误；

(iii) C2 HFP/HZP 区分避免与 GDC 11 监管约束矛盾——HFP MTC 必须 $\le 0$ 是工程硬性要求，HZP BOC 微正才是 MR 测试可触及的物理现象；

(iv) C2 三机制描述对 MOX 与高富集燃料的物理覆盖完整，避免审稿人质疑"机制描述不全"；

(v) C2 引文严格收敛到 GDC 11（监管来源）+ Stacey/Lamarsh & Baratta（教科书）+ ANS 19.6.1（测量协议），所有反应堆物理论断都有可核对来源。

## 修改后的论文整体定位变化

完成上述修改后，论文的理论贡献从原版的：

> "建立 Theorem 1（Translate 闭包）+ Theorem 2（多项式可判定）+ 三个 positive instantiation；Theorem 1′ 开放"

调整为：

> "建立 Theorem 1（Translate 闭包）+ Theorem 2（多项式可判定）+ 三个 positive instantiation **+ 一个 negative instantiation（PWR）以两个独立反例否证 Theorem 1′**；Composite-Translate 扩展（涵盖五类结构性缺失）开放"

理论增量的关键是：将原版 §C.5.3 中只在抽象层面列出的"irreducibly compositional MR"反例类，**用 PWR 域的两个具体 MR 实例化**，且物理表述达到反应堆物理领域专家审稿的精度。这把一个开放猜想从"等待解决"推进到"在结构上重要的具体代数上已知为假"，是科学论文中比"再加一个定理"更强的贡献。

审稿人无法用以下理由驳回：

- **"这只是病态例子"**：两个反例都是 PWR 安全监管要求的 MR（rod worth 在 RG 1.77 安全分析输入中、MTC vs $C_B$ 在 GDC 11 与 ANS 19.6.1 测量协议中），每个核安全审查都验证；物理表述符合 Bell & Glasstone、Lewis & Miller、Stamm'ler & Abbate、Stacey、Lamarsh & Baratta 五本标准教科书的精度要求。
- **"shadowing 不是对所有 $A, B$ 都成立"**：v3 已改用非可加性 MR，对存在性形式的 $A, B$ 成立，覆盖 shadowing 和 anti-shadowing 两种物理表现；v4 进一步将 anti-shadowing 描述为标准 PWR 中"次要但可测"的现象（5–20 pcm 量级），符合 PWR 启动物理试验实测。
- **"微扰公式不严格"**：v3 的证明 load-bearing 部分使用 exact 1/k 差异形式，不依赖于一阶微扰；微扰公式仅作为物理直觉说明出现，公式本身按 Bell & Glasstone §6.3、Lewis & Miller §4.4 标准带负号、$(\phi_A, \phi^\dagger_A)$ 基态约定明确给出。
- **"MTC 单位混淆"（v4 修订）**：v4 严格区分 $\alpha_{\text{MTC}} = \partial \rho_{\text{static}}/\partial T_{\text{mod}}$（反应堆物理工程标准）与 $\partial k_{\text{eff}}/\partial T_{\text{mod}}$（数学等价但单位不同）；Definition 17 主形式用 $\rho_{\text{static}}$，证明用 $k_{\text{eff}}$ 的合理性在"Note on equivalent formulations"段明确说明。
- **"MTC 微正与 GDC 11 矛盾"（v4 修订）**：v4 严格区分 HFP（GDC 11 监管，MTC 必须 $\le 0$）与 HZP（启动物理试验工况，BOC 高硼可微正）；Definition 17 的 MR 参考工况限定为 HFP, ARO，与 GDC 11 监管完全一致。
- **"MTC 三机制描述不完整"（v4 修订）**：v4 补充第三机制（谱硬化与 $^{238}$U 共振增强），与 Stacey §3.4 标准三机制论述一致；这一补充对 MOX 与高富集 UO$_2$ 燃料尤为重要。
- **"换一种归类方式就能修复"**：两个反例对应五个独立的 Translate 结构缺失（操作算子谱输出、同态失败 $\pi$ 模板、配置依赖伴随结构、高阶混合差分模板、两方向联合参数依赖），单一扩展无法同时覆盖。
- **"你应该自己解决 Composite-Translate"**：论文明确把 Composite-Translate 作为开放问题留给后续工作，反例本身已有充分理论增量。
- **"反例数量太少，不能反映普遍性"**：两个反例分别击中 PWR 物理的两个核心安全机制（控制棒价值与反应性反馈系数），代数失败模式正交，覆盖 NOETHER Translate 签名的五个独立结构维度。再增加反例只能增加重复覆盖，不能提升论证强度。
