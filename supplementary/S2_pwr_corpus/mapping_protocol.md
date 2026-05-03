# 84-MR Corpus → NOETHER Block Mapping Protocol (S2)

This document records the protocol used to assign each of the 84 MRs in the
PWR corpus to a NOETHER block of the operator algebra
$\mathcal{A}_{\mathrm{Boltz}}$. Together with `pwr_84mr_full.csv` it
underwrites the §5.3 claim of three reproductions, two refinements, and
two predictions.

## Step 1: corpus inventory

The 84 MRs are inventoried by reactor-physics equation source:

| Source | Prefix | Count |
|---|---|---|
| Boltzmann transport | Bol-* | 22 |
| Diffusion | Dif-* | 13 |
| Burnup (Bateman) | Bur-* | 18 |
| Resonance treatment | Res-* | 5 |
| Kinetics | Kin-* | 1 |
| Coupling / PWR-specific | Cpl-* | 9 |
| Mixed application | *-App-* | 16 (subset of above) |

The original distribution by prior MetaPattern (P1–P5) is:
P1 = 16, P2 = 31, P3 = 18, P4 = 10, P5 = 9.

## Step 2: default mapping (5 of 5 prior patterns)

The default mapping uses the structural correspondence reported in §5.3
Table 2:

| Prior pattern | Default NOETHER block | Default MetaPattern |
|---|---|---|
| P1 conservation/invariance | $G$ | $m_{\mathrm{inv}}$ |
| P2 monotonicity | $O_{\le}$ | $m_{\mathrm{mono}}$ |
| P3 convergence | $\mathcal{L}^{*}$ | $m_{\mathrm{conv}}$ |
| P4 trajectory | $\mathcal{D}^{*}$ | $m_{\mathrm{dyn}}$ |
| P5 partial-order/bounding | $\mathcal{E}^{*}$ | $m_{\mathrm{cmp}}$ |

## Step 3: NOETHER reassignment rules

The default mapping is over-ridden in two scenarios:

### Reassignment R1: prior P1/P2 entries that are actually self-adjoint reciprocity → m_adj

P1 was an inductive cluster that conflated symmetry-derived conservation
with self-adjoint reciprocity. Under the canonical-block ordering
$G > T^{*}$, an MR derivable through both blocks goes to $G$
($m_{\mathrm{inv}}$); but an MR whose semantic content is reciprocity
*only* (no group action) goes to $T^{*}$ ($m_{\mathrm{adj}}$).

Two MRs in the corpus satisfy this:

- **Bol-Phy-03** (source-detector reciprocity) — derived from the adjoint
  flux equation $\langle \mathrm{S}, \phi^{\dagger} \rangle = \langle \mathrm{Q}, \phi \rangle$,
  no group action; reassigned P1 → $m_{\mathrm{adj}}$.
- **Dif-Phy-14** (diffusion adjoint reciprocity) — analogous structure
  for diffusion solvers; reassigned P1 → $m_{\mathrm{adj}}$.

This is a *refinement* of the inductive catalogue.

### Reassignment R2: prior P1/P2/P5 entries that are method-comparison error bounds → m_cmp

P1, P2 occasionally absorbed entries that semantically belong to the
method-comparison block $\mathcal{E}^{*}$ — namely, MRs reporting a fixed
error-direction between two numerical methods rather than an invariance
or monotone parameter dependence.

Six MRs in the corpus satisfy this:

- **Bol-App-04** (scattering vs. pure-absorption ordering) — P1 →
  $m_{\mathrm{cmp}}$; this is a partial-order over operator regimes.
- **Bol-Alg-04** ($P_0$ overestimates $k_{\mathrm{eff}}$ in H-systems) —
  P2 → $m_{\mathrm{cmp}}$.
- **Bol-Alg-06** (neglecting upscattering underestimates thermal flux) —
  P2 → $m_{\mathrm{cmp}}$.
- **Dif-Alg-04** (coarse-FDM $k_{\mathrm{eff}}$ biased low) — P2 →
  $m_{\mathrm{cmp}}$.

### Reassignment R3: prior P5 entries that resolve to $\mathcal{D}^{*}$ or $\mathcal{L}^{*}$ under canonical ordering

P5 was the broadest inductive cluster. Two entries are routed to other
blocks under the canonical-block ordering $\mathcal{L}^{*} > \mathcal{D}^{*} > \mathcal{E}^{*}$:

- **Bol-App-03** (multi-layer moderation peak) — qualitative-shape
  phenomenon; P5 → $m_{\mathrm{dyn}}$.
- **Dif-Alg-03** (NEM-FDM limit consistency) — limit-consistency under
  refinement; P5 → $m_{\mathrm{conv}}$.

### Reassignment R4: superposition / linearity entries from P1 → $m_{\mathrm{mono}}$

Two MRs labelled as P1 (conservation) are in fact linearity statements
over solution operators. Under canonical ordering $G > O_{\le}$, they
remain in P1 only if their linearity is mediated by a group action;
otherwise they go to $O_{\le}$:

- **Bur-Phy-03** (initial-condition linear superposition) — pure
  linearity, no group action; P1 → $m_{\mathrm{mono}}$.
- **Bol-Phy-04** (source-strength multiplication) — scalar linearity;
  P1 → $m_{\mathrm{mono}}$.
- **Bol-Phy-05** (two-source superposition) — additive linearity; P1 →
  $m_{\mathrm{mono}}$.

These three are listed under $O_{\le}$ in `pwr_84mr_full.csv`. (They are
also documented in the notes column.)

## Step 4: predicted MetaPatterns NOT in the inductive corpus

Two NOETHER MetaPatterns have no canonical-form instances in the original
84-MR corpus; they appear in the §5.3 Table 3 in italics as
\textit{(predicted)}:

- **$m_{\mathrm{adj}}$ canonical adjoint reciprocity** — the corpus
  contained Bol-Phy-03 and Dif-Phy-14 (R1 above), but the inductive
  catalogue had not isolated $m_{\mathrm{adj}}$ as a distinct
  MetaPattern.
- **$m_{\mathrm{rev}}$ collisionless time-reversal compatibility** —
  not represented by any MR in the 84-MR corpus. NOETHER predicts this
  block from the existence of $\mathcal{T}^{*}$ in $\mathcal{A}_{\mathrm{Boltz}}$
  (collisionless trajectory regime).

## Final NOETHER distribution

After applying steps 1–4:

| NOETHER block | NOETHER MetaPattern | Count |
|---|---|---|
| $G$ | $m_{\mathrm{inv}}$ | 10 |
| $O_{\le}$ | $m_{\mathrm{mono}}$ | 31 |
| $T^{*}$ | $m_{\mathrm{adj}}$ | 2 |
| $\mathcal{T}^{*}$ | $m_{\mathrm{rev}}$ | 0 (predicted-only) |
| $\mathcal{L}^{*}$ | $m_{\mathrm{conv}}$ | 19 |
| $\mathcal{D}^{*}$ | $m_{\mathrm{dyn}}$ | 11 |
| $\mathcal{E}^{*}$ | $m_{\mathrm{cmp}}$ | 11 |
| **Total** | | **84** |

## Caveat

This mapping is the authors' best-effort categorical assignment given the
canonical-block ordering and the seven-block decomposition of
$\mathcal{A}_{\mathrm{Boltz}}$ (Hypothesis 1, version 1.0). MR-level
disagreement on individual reassignments (e.g., whether Bol-App-03 should
go to $\mathcal{D}^{*}$ or $\mathcal{E}^{*}$) is expected; the
canonical-block ordering rules out ambiguity at the MetaPattern level
but not at the linguistic-classification level. Reviewers are invited to
cross-check `pwr_84mr_full.csv` and the protocol above.
