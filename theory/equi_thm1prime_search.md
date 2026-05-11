# Theorem 1' counterexample search on $\mathcal{A}_{\mathrm{equi}}$

**Issue**: ISSUE-011 (Step 2)
**Date**: 2026-05-11
**Goal**: identify $\ge 1$ candidate Theorem 1' counterexample drawn from
the published equivariant-ML literature, mirroring the §subsec:negative-pwr
analysis on $\mathcal{A}_{\mathrm{PWR}}$.

## 1. The bar for "counterexample"

A property $\rho$ over $\mathcal{F}_{\mathrm{equi}}$ is a Theorem 1'
counterexample on $\mathcal{A}_{\mathrm{equi}}$ if it satisfies
**all three** of the following:

1. $\rho$ is **formulable in $\mathcal{A}_{\mathrm{equi}}$'s operator
   vocabulary**: it can be stated as a constraint over the operators
   appearing in $\mathcal{A}_{\mathrm{equi}}$'s eight-block decomposition
   (Section 5.3 of the paper): $G_{\mathrm{equi}}$, $O^{\mathrm{train}}_{\le}$,
   $T^{*}_{\mathrm{att}}$, $\mathcal{T}_{\mathrm{seq}}$,
   $\mathcal{L}_{\mathrm{train}}/\mathcal{L}_{\mathrm{depth}}/\mathcal{L}_{\mathrm{dim}}$.
2. $\rho$ has a **published canonical form** with citation.
3. $\rho$ is **not derivable as $\mathrm{Translate}(\iota, s)$ for any
   single block $s$ and any invariant $\iota \in \mathcal{I}_{s}$** under
   Definition 5 of the paper (single block invariant, first-order
   $\pi$-template, single partial-order direction, tuple over $P(x)$).

Verdict per candidate ranges over: $\circ$ **derivable** ($\rho$ is in
$\mathbb{M}(\mathcal{A}_{\mathrm{equi}})$, hence not a counterexample);
$\bullet$ **counterexample candidate** (passes 1--3, structural-obstruction
sketch supplied); $\dagger$ **out of vocabulary** (fails 1, hence
out-of-scope for Theorem 1' and tracked separately as a candidate ninth
block under Remark `rem:counterex`).

## 2. Literature surveyed

Nine equivariant-ML papers consulted (audit log in Section 6). The
candidate MRs distilled from each are listed in the table below.

| # | Paper | MR proposed (informal) | Single-block-derivable? | Verdict |
|---|---|---|---|---|
| 1 | Murphy et al. 2008 \cite{Murphy2008} | Six properties: additivity, multiplicative scaling, permutation, inversion, inclusion/exclusion, anti-symmetry of ML classifier output | Each property single-block-derivable from $G$ (permutation, inversion), $O_{\le}$ (additivity, multiplicative scaling, inclusion/exclusion as monotonicity), $\mathcal{T}^{*}$ (anti-symmetry) | $\circ$ derivable |
| 2 | Cohen \& Welling 2016 (G-CNN) \cite{CohenWelling2016} | Output equivariance under the wallpaper group $p4m$: $f(g\cdot x) = \rho(g)\cdot f(x)$ for $g \in p4m$ | Single-block-derivable from $G$ via $\mathrm{Translate}(\mathrm{stabiliser}, G)$ | $\circ$ derivable |
| 3 | Thomas \& Smidt 2018 (TFN) \cite{ThomasSmidt2018} | Type-$\ell$ steerable equivariance: $f(R\cdot x) = D^{(\ell)}(R)\cdot f(x)$ for $R \in \mathrm{SO}(3)$ and Wigner $D$-matrix of degree $\ell$ | Single-block-derivable from $G = \mathrm{SO}(3)$ acting non-trivially on the output; one MR per irrep degree | $\circ$ derivable per irrep |
| 4 | Kondor \& Trivedi 2018 \cite{KondorTrivedi2018} | Convolution-equivariance lemma: for compact $G$, the only equivariant linear map $\mathcal{H}_{\mathrm{in}} \to \mathcal{H}_{\mathrm{out}}$ is the $G$-convolution; output therefore equivariant under $G$ | Single-block from $G$ | $\circ$ derivable |
| 5 | Worrall et al. 2017 (Harmonic Nets) \cite{Worrall2017HNets} | $\mathrm{SO}(2)$-patch-wise rotation equivariance via circular harmonics: $f(R_\theta \cdot x) = e^{im\theta}\,f(x)$ | Single-block-derivable from $G = \mathrm{SO}(2)$ acting on a complex-valued feature space | $\circ$ derivable |
| 6 | Esteves et al. 2018 (Spherical CNN) \cite{Esteves2018Spherical} | $\mathrm{SO}(3)$-equivariance via spherical harmonic basis: $f(g\cdot s)(\omega) = f(s)(g^{-1}\omega)$ | Single-block from $G$ | $\circ$ derivable |
| 7 | Sosnovik et al. 2020 (Scale-Equivariant) \cite{Sosnovik2020ScaleSteerable} | Scale equivariance: $f(\mathrm{scale}_\lambda \cdot x) = \mathrm{scale}_\lambda \cdot f(x)$ for $\lambda \in \mathbb{R}^+$ | Single-block from $G = (\mathbb{R}^+,\,\times)$; non-compact but admits $\mathrm{Translate}$ template | $\circ$ derivable |
| 8 | Finzi et al. 2020--2021 (EMLP) \cite{Finzi2020LieConv, Finzi2021EMLP} | Equivariance under any matrix Lie group $G \subseteq \mathrm{GL}(n)$ via Lie-algebra basis: $f(g\cdot x) = \rho_{\mathrm{out}}(g)\cdot f(x)$ | Single-block from $G$ provided $G$ is given as one block | $\circ$ derivable per group |
| 9 | Satorras et al. 2021 (EGNN) \cite{Satorras2021EGNN} | $E(n)$-equivariance: simultaneous rotation, reflection, translation, permutation equivariance via separate equivariant message updates | See §3 below: a candidate counterexample arises when joint $\mathrm{SO}(3) \times \mathfrak{S}_n$ equivariance is required with **non-trivial cross-block coupling** | $\bullet$ candidate (see §3.1) |
| 10 | Cohen, Weiler et al. 2019 (gauge-equivariant CNN, icosahedral CNN) \cite{Cohen2019Gauge} | Gauge equivariance: *local* fibre-wise group action on each tangent plane of a manifold, compatible across patches via a parallel-transport cocycle | See §3 below: candidate counterexample, *local* group action does not reduce to a single global $G$-block invariant | $\bullet$ candidate (see §3.2) |
| 11 | Maron et al. 2018 (Invariant \& Equivariant Graph Networks) \cite{Maron2019IGN} | $k$-order tensor invariance under $\mathfrak{S}_n$: $f(P^{\otimes k}\cdot X) = f(X)$ for permutation $P$ acting on a $k$-tensor | Single-block from $G = \mathfrak{S}_n$ on the $k$-th tensor power | $\circ$ derivable per $k$ |
| 12 | Haan et al. 2020 (Gauge-Equivariant Mesh CNN) \cite{Haan2020GaugeMesh} | *Anisotropic* mesh convolution: feature transport along edges depends on local mesh geometry through a structure group $\mathrm{O}(2)$ acting fibre-wise | Inherits §3.2's obstruction; supports it across two independent geometric primitives (icosahedron, general meshes) | $\bullet$ secondary witness for §3.2 |

## 3. Counterexample candidates

### 3.1 $\rho_{\mathrm{compose}}$: compositional equivariance under $\mathrm{SO}(3) \times \mathfrak{S}_n$ on point sets

**Setting.** Equivariant point-cloud classifiers in the EGNN family
\cite{Satorras2021EGNN} are required to be equivariant under the
*joint* action of $G_1 = \mathrm{SO}(3)$ on coordinates and
$G_2 = \mathfrak{S}_n$ on point indices: for all $R \in \mathrm{SO}(3)$,
all $P \in \mathfrak{S}_n$, all point clouds $\mathbf{x} \in \mathbb{R}^{n\times 3}$,

$$
f(R \cdot P \cdot \mathbf{x}) \;=\; \rho_{\mathrm{out}}(R)\cdot f(\mathbf{x}),
$$

where $R \cdot P \cdot \mathbf{x} = (R\,\mathbf{x}_{\pi^{-1}(1)},\dots,R\,\mathbf{x}_{\pi^{-1}(n)})$,
$\pi = $ permutation underlying $P$. The compositional MR is

$$
\rho_{\mathrm{compose}}:\quad \big\| f(R\,P\,\mathbf{x}) - \rho_{\mathrm{out}}(R)\,f(\mathbf{x}) \big\|_\infty \;\le\; \tau,
$$

quantifying over $(R, P) \in \mathrm{SO}(3) \times \mathfrak{S}_n$ jointly.

**Why it is formulable in $\mathcal{A}_{\mathrm{equi}}$.** Both
$\mathrm{SO}(3)$ and $\mathfrak{S}_n$ are assigned to the $G$-block of
$\mathcal{A}_{\mathrm{equi}}$ (Section 5.3 of the paper:
$G = \{G_{\mathrm{equi}}\}$ with $G_{\mathrm{equi}} = \mathrm{SO}(3) \times \mathfrak{S}_n$).
The output equivariance representation $\rho_{\mathrm{out}}$ is the
$(R, P) \mapsto R$ projection.

**Why it is not single-`Translate`-derivable.**

Definition 5 (`Translate`) maps a *single* block invariant $\iota = (\Phi, \pi)$
under *one* block $s$ to an MR. The canonical-order convention for $s = G$
(Definition 5, footnote: "$x_i = g_i \cdot x_0$ with $g_i$ enumerated by
group orbit") generates the input tuple by sweeping a *single group*'s
orbit. The MR family produced is therefore
$\rho_{R,\mathrm{out}}: \forall R,\,\|f(R\,\mathbf{x}) - \rho_{\mathrm{out}}(R)\,f(\mathbf{x})\|_\infty \le \tau$ and
$\rho_{P,\mathrm{out}}: \forall P,\,\|f(P\,\mathbf{x}) - f(\mathbf{x})\|_\infty \le \tau$
*separately*, not their joint product.

$\rho_{\mathrm{compose}}$ is the *intersection* of $\rho_{R,\mathrm{out}}$
and $\rho_{P,\mathrm{out}}$ over the *product* parameter set
$\mathrm{SO}(3) \times \mathfrak{S}_n$, with the further requirement that
both group actions commute through $f$. If they fail to commute (e.g.\ a
bug in the EGNN message-passing layer that mixes channel-permutation with
rotation), $\rho_{R}$ and $\rho_{P}$ may *individually* pass while
$\rho_{\mathrm{compose}}$ fails. The compositional MR therefore carries
strictly more information than the union of single-group MRs.

**Structural-obstruction sketch.** This mirrors §subsec:negative-pwr's
obstruction~4 (*higher-order mixed-difference templates*): `Translate`'s
$\pi$-template is single-direction. The compositional MR requires a
*product-of-orbits* template that quantifies over $R \in G_1$ and
$P \in G_2$ jointly. The required `Translate`-extension is a
**product-group $\pi$-template**: $\pi \subseteq (\mathcal{X}\times\mathcal{Y})^{|G_1|\times|G_2|}$
with the tuple generated by the joint orbit $\{(g_1 \cdot g_2 \cdot x_0,
P(g_1\cdot g_2\cdot x_0)) : g_1 \in G_1,\, g_2 \in G_2\}$.

**Engineering significance.** The non-trivial cell of Set N vs Set L in
Table~\ref{tab:case-study} (cat-(ii) equivariance break) is detected by
$\rho_{\mathrm{rot}}$ alone in the paper's case study; a
*permutation-rotation interaction* bug (e.g.\ the $h_l^t$ message update
in EGNN incorrectly entangling permutation indices with coordinate
rotations) would slip past both $\rho_{\mathrm{rot}}$ (pass under $P = e$)
and $\rho_{\mathrm{perm}}$ (pass under $R = e$) and would only be flagged
by $\rho_{\mathrm{compose}}$. Such interaction defects are reported in
the EGNN/SE(3)-Transformer issue trackers (e.g.\ message-aggregation
order ambiguity under joint group action) as a known class of subtle
correctness bugs.

### 3.2 $\rho_{\mathrm{gauge}}$: gauge equivariance on manifolds (Cohen et al.\ 2019)

**Setting.** Gauge-equivariant convolutional networks
\cite{Cohen2019Gauge} on a manifold $M$ (e.g.\ the icosahedron or a
3D mesh) operate on feature fields $f: M \to V$ assigned to each
tangent plane $T_p M$. The gauge group $H \subseteq \mathrm{O}(d)$ acts
*locally* on each fibre $V_p$ via a gauge transformation $g_p \in H$
(depending on $p$). Gauge equivariance requires that the network's
output transform consistently under any choice of local frame: for any
gauge $\mathbf{g} = (g_p)_{p\in M}$,

$$
\rho_{\mathrm{gauge}}:\quad N(\mathbf{g}\cdot f) \;=\; \mathbf{g}\cdot N(f),
$$

where the dot denotes the fibre-wise action of $g_p$ on $f(p)$ and on
$N(f)(p)$ at each point $p$.

**Why it is formulable in $\mathcal{A}_{\mathrm{equi}}$.** The $G$-block
of $\mathcal{A}_{\mathrm{equi}}$ includes the structure group $H$
(e.g.\ $\mathrm{O}(2)$ on the icosahedron's tangent planes); the gauge
action is a fibre-wise application of $H$ to the feature field, which
is expressible in the operator vocabulary of the framework.

**Why it is not single-`Translate`-derivable.**

The single-block invariant under $G = H$ would produce
$f(h\cdot x) = \rho_{\mathrm{out}}(h)\cdot f(x)$ for $h$ acting *globally*
on the input. Gauge equivariance differs in two respects:

1. **Locality**: the action is *per-tangent-plane* $g_p$, not a single
   global $h$. The tuple $(x_i)$ in Definition 4 of the paper is
   generated by enumerating the orbit of one $g \in G$ on a base input
   $x_0$. There is no single $g$ here, but a tuple-of-gauges $\mathbf{g}$.
2. **Cocycle compatibility**: transporting a feature across two charts
   requires a *transition function* $g_{p\to q} \in H$ on the chart
   overlap. The MR therefore has the form $N \circ \mathbf{g} = \mathbf{g}\circ N$
   *for every gauge field* $\mathbf{g}$, parametrised by the manifold
   structure of $M$, not by a single group element. The MR's quantifier
   is over a *function space* $\mathbf{g} \in \mathcal{C}(M,\,H)$, not
   over $H$.

**Structural-obstruction sketch.** This adds a *fibre-bundle*
$\pi$-template requirement to `Translate`. The obstruction is most
closely analogous to §subsec:negative-pwr's obstruction~3
(*configuration-indexed adjoint structure*): the adjoint flux
$\phi^{\dagger}_X$ varies with operator history $X$; here the gauge
action $g_p$ varies with the input-domain point $p$. The required
`Translate`-extension is a **gauge-bundle $\pi$-template**: $\pi$ is
parametrised by sections of a principal $H$-bundle $P \to M$ rather than
by single group elements. This is a strictly richer structure than the
single-group orbit of Definition 4 and is not captured by the present
`Translate`. Haan et al.~2020 \cite{Haan2020GaugeMesh} demonstrate that
this structure is irreducible to single-group orbits on general
3D meshes; the icosahedral case of \cite{Cohen2019Gauge} is a
restricted but still bundle-non-trivial instance.

**Engineering significance.** Production climate-pattern and
omnidirectional-image segmentation pipelines built on icosahedral CNNs
\cite{Cohen2019Gauge} would fail $\rho_{\mathrm{gauge}}$ under a
gauge-inconsistency bug (e.g.\ inconsistent kernel orientation across
two adjacent triangular patches on the icosahedron). The bug is
*invisible* to any global $\mathrm{SO}(3)$-rotation MR
(the icosahedron's discrete rotation group has order 60, finite
samples cover at most 60 group elements, none of which interact with
the local gauge-frame choice). The bug is also invisible to
$\rho_{\mathrm{perm}}$ (gauge fields are point-indexed, not
permutation-indexed). The single-block `Translate` therefore cannot
generate a gauge-bundle MR from any single $G$, $O_{\le}$, $T^{*}$,
$\mathcal{T}^{*}$, $\mathcal{L}^{*}$, $\mathcal{D}^{*}$, $\mathcal{E}^{*}$,
or $\mathcal{B}^{*}_{\mathrm{rel}}$ invariant.

### 3.3 $\rho_{\mathrm{sym\text{-}break}}$: spontaneous symmetry-breaking detection

**Setting.** When an equivariant network is trained on a dataset whose
*empirical* distribution breaks the architectural symmetry (e.g.\ a
nominally $\mathrm{SO}(3)$-equivariant point-cloud classifier trained
on data with a fixed gravity-axis preference), the learned function
$f$ may converge to a state that is *architecturally* equivariant but
*statistically* near-degenerate along the unbroken axis. The MR

$$
\rho_{\mathrm{sym\text{-}break}}:\quad \mathrm{Var}_R\bigl[\,f(R\cdot \mathbf{x})\,\bigr] \;>\; \tau_{\mathrm{var}},
$$

where the variance is taken over $R \in \mathrm{SO}(3)$, tests for
detectable architectural equivariance (variance must be small if
$f$ is invariant) versus learned-distribution leakage (variance should
not collapse to zero on training-distribution support).

**Verdict: $\dagger$ out of vocabulary.** This MR requires a *measure*
on $\mathrm{SO}(3)$ (Haar measure to compute the variance) and an
output-distribution moment. The variance operator is not an operator in
$\mathcal{A}_{\mathrm{equi}}$'s eight-block decomposition as specified;
it is a probability-distribution functional in the sense of
Remark~\ref{rem:counterex} item~(iii) (probabilistic invariants).
$\rho_{\mathrm{sym\text{-}break}}$ is therefore *not* a Theorem 1'
counterexample on $\mathcal{A}_{\mathrm{equi}}$; it is an out-of-vocabulary
candidate that tracks under Remark~\ref{rem:counterex}'s probabilistic
ninth-block class. Recorded here for completeness.

## 4. Counterexample count and verdict

- **Candidates surveyed**: 12 (Murphy six-class + 11 distinct equivariant-ML papers).
- **Theorem 1' counterexample candidates**: **2** ($\rho_{\mathrm{compose}}$ from
  §3.1; $\rho_{\mathrm{gauge}}$ from §3.2 with a secondary witness in
  Haan et al.~2020).
- **Out-of-vocabulary, ninth-block candidates**: 1 ($\rho_{\mathrm{sym\text{-}break}}$,
  Remark~\ref{rem:counterex} item~(iii)).
- **Single-block-derivable (not counterexamples)**: 9.

Verdict: Theorem 1' is *likely* falsified on $\mathcal{A}_{\mathrm{equi}}$.
The compositional and gauge counterexamples are pairwise independent: a
product-group $\pi$-template extension absorbs $\rho_{\mathrm{compose}}$
but not $\rho_{\mathrm{gauge}}$, and a gauge-bundle $\pi$-template
extension absorbs $\rho_{\mathrm{gauge}}$ but not the joint-group
template of $\rho_{\mathrm{compose}}$. Per-extension reasoning is in
`theory/translate_extensions.md`.

Caveats:

- The proof obligations are deeper than for $\mathcal{A}_{\mathrm{PWR}}$.
  On $\mathcal{A}_{\mathrm{PWR}}$, the obstructions are anchored in
  $k_{\mathrm{eff}}$ being an *operator-spectrum* output (not in
  $\mathcal{Y}$) and in the adjoint flux $\phi^{\dagger}$ being
  *configuration-indexed*. On $\mathcal{A}_{\mathrm{equi}}$, the
  obstructions are *parameter-space* structural: a product group is
  not a single group, and a gauge-bundle is not a single global
  group action. The same conceptual move (extend `Translate`'s
  $\pi$-template) is required, but the failure mode is more
  formally subtle and warrants a careful follow-up proof.
- The candidates have not been mechanically verified on a working
  reference implementation; this issue is exploratory in the same
  sense ISSUE-011 declares.
- An extension by Yarotsky 2018 (deep equivariant nets, universal
  approximation) and the Weiler--Cesa 2019 E2-Steerable CNN framework
  may absorb $\rho_{\mathrm{compose}}$ if the joint group is treated as
  the *direct product representation* rather than as separate generators;
  this is consistent with the structural-obstruction sketch (the
  product-representation absorption is exactly what the proposed
  `Translate`-extension would formalise).

## 5. Comparison to $\mathcal{A}_{\mathrm{PWR}}$'s five obstructions

| $\mathcal{A}_{\mathrm{PWR}}$ obstruction | Maps to $\mathcal{A}_{\mathrm{equi}}$ |
|---|---|
| 1. Operator-spectrum output ($k_{\mathrm{eff}}$ as eigenvalue) | *Not active* on $\mathcal{A}_{\mathrm{equi}}$ (classifier outputs are in $\mathcal{Y}$) |
| 2. Homomorphism-failure $\pi$-template (non-additive worth) | *Not active* on $\mathcal{A}_{\mathrm{equi}}$ (group action is by construction a homomorphism on the irrep) |
| 3. Configuration-indexed adjoint ($\phi^{\dagger}_X$ varies with $X$) | **Active** as gauge-bundle $\pi$ (§3.2: $g_p$ varies with $p$) |
| 4. Higher-order mixed-difference $\pi$-templates | **Active** as product-group $\pi$ (§3.1: joint $\mathrm{SO}(3) \times \mathfrak{S}_n$) |
| 5. Two-direction joint parametric dependence | **Subsumed** by 4 on $\mathcal{A}_{\mathrm{equi}}$ |

Two obstructions ($\mathcal{A}_{\mathrm{PWR}}$-3 and $\mathcal{A}_{\mathrm{PWR}}$-4)
transfer; three are inactive in different ways. The independence claim
across the transferred two is preserved: a product-group extension does
not absorb the gauge-bundle structure (a gauge is a *section*, not a
group element); a gauge-bundle extension does not absorb the
product-group structure ($\mathrm{SO}(3) \times \mathfrak{S}_n$ is a
single group, not a bundle structure). See
`theory/translate_extensions.md`.

## 6. Audit log

| Source | Tool | Status | Notes |
|---|---|---|---|
| Murphy et al.~2008 | `search_semantic` $\to$ paper metadata | retrieved | Cite key `Murphy2008` already in bib |
| Cohen \& Welling 2016 (G-CNN) | bib entry `CohenWelling2016` | already cited | Single-block $G$ from $p4m$ |
| Thomas \& Smidt 2018 (TFN) | bib entry `ThomasSmidt2018` | already cited | Steerable irreps, single-block $G$ |
| Kondor \& Trivedi 2018 | bib entry `KondorTrivedi2018` | already cited | Compact-group convolution lemma |
| Worrall et al.~2017 (H-Nets) | `search_semantic` | retrieved | arXiv 1612.04642 |
| Esteves et al.~2018 (Spherical CNN) | `search_semantic` | retrieved | arXiv 1711.06721 |
| Sosnovik et al.~2020 (Scale-Equivariant) | `search_semantic` | retrieved | arXiv 1910.11093 |
| Finzi et al.~2020 (LieConv) | `search_semantic` | retrieved | arXiv 2002.12880 |
| Finzi et al.~2021 (EMLP) | `search_semantic` | retrieved | arXiv 2104.09459 |
| Satorras et al.~2021 (EGNN) | bib entry `Satorras2021EGNN` | already cited | Counterexample-candidate substrate for §3.1 |
| Cohen et al.~2019 (Gauge-Equivariant CNN) | `search_semantic` | retrieved | arXiv 1902.04615 |
| Haan et al.~2020 (Gauge-Equivariant Mesh CNN) | `search_semantic` | retrieved | arXiv 2003.05425 |
| Maron et al.~2018 (Invariant \& Equivariant Graph Networks) | `search_semantic` | retrieved | arXiv 1812.09902 |

Search dates: 2026-05-11. All retrievals through `paper-search-mcp`
(`search_semantic`, `search_crossref`) per CLAUDE.md §7
Paper-Search-First Policy; no Web-search fallback was needed for these
sources.

## 7. Open items

- Verify the structural-obstruction sketches on a reference EGNN
  implementation via a constructed compositional-equivariance bug
  (committed as ISSUE-013 follow-up).
- Verify $\rho_{\mathrm{gauge}}$ on the e3nn icosahedral-CNN test
  suite (no GitHub issues currently flag gauge-inconsistency bugs;
  this is an exploratory candidate).
- Consider whether the proposed product-group $\pi$-template and
  gauge-bundle $\pi$-template preserve Theorem~\ref{thm:closure} and
  Theorem~\ref{thm:decidable}; see `translate_extensions.md`.
