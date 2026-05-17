# Full 12-MR Element-wise Correspondence Table

Migrated from `NOETHER_paper.tex` Table `tab:elementwise` (Tier 2 compression, 2026-05-16). Body retains 7 representative MRs (one canonical per non-empty block plus 2 predicted MetaPatterns); this file carries the full 12-MR enumeration with per-block sub-category coverage.

## Selection protocol (from body)

The 12 MRs were selected by the following protocol so that the table is structurally rather than numerically representative:

1. Every block $s \in \mathcal{D}(\mathcal{A}_{\mathrm{Boltz}})$ that is non-empty is represented at least once.
2. Within each block, the most frequent canonical-form MR in the literature is selected first.
3. Where a block contains MRs from two distinct sub-categories (e.g.\ geometric vs.\ energy-group symmetry within $G$), each sub-category is given at least one representative.
4. The two predicted MetaPatterns $m_{\mathrm{adj}}$ and $m_{\mathrm{rev}}$ are listed at the bottom in italics to indicate that no MR was previously catalogued in this form; the block placement is derived.

A larger 84-MR corpus underlying the selection protocol is in this directory (`S2_pwr_corpus/`).

## Table: 12 representative MRs

| MR ID | Plain-text MR | P# | Block | NOETHER MP | Sub-category | In body table? |
|---|---|---|---|---|---|---|
| Bur-Phy-01 | Step-splitting invariance | P1 | $G$ | $m_{\mathrm{inv}}$ | geometric | ✓ |
| Bol-Phy-02 | Quarter-symmetry rotation | P1 | $G$ | $m_{\mathrm{inv}}$ | geometric | --- |
| Bol-Phy-11 | $\Sigma_a\!\uparrow \Rightarrow k_{\mathrm{eff}}\!\downarrow$ | P2 | $O_{\le}$ | $m_{\mathrm{mono}}$ | physical | ✓ |
| Bol-Phy-12 | $\nu\Sigma_f\!\uparrow \Rightarrow k_{\mathrm{eff}}\!\uparrow$ | P2 | $O_{\le}$ | $m_{\mathrm{mono}}$ | physical | --- |
| Dif-Alg-01 | Diamond-difference $h^2$ convergence | P3 | $\mathcal{L}^{*}$ | $m_{\mathrm{conv}}$ | spatial limit | ✓ |
| Bur-Alg-01 | CRAM order $N\!\to\!\infty$ convergence | P3 | $\mathcal{L}^{*}$ | $m_{\mathrm{conv}}$ | temporal limit | --- |
| Bur-Phy-08 | Iodine pit qualitative shape | P4 | $\mathcal{D}^{*}$ | $m_{\mathrm{dyn}}$ | transient | ✓ |
| Cpl-App-06 | Gd self-shielding S-curve | P4 | $\mathcal{D}^{*}$ | $m_{\mathrm{dyn}}$ | depletion | --- |
| Bur-Alg-04 | CRAM no-worse-than TTA | P5 | $\mathcal{E}^{*}$ | $m_{\mathrm{cmp}}$ | algorithmic | ✓ |
| Bol-Alg-04 | $P_0$ over-estimates $k$ in H-systems | P5 | $\mathcal{E}^{*}$ | $m_{\mathrm{cmp}}$ | approximation | --- |
| *(predicted)* | Adjoint reciprocity | --- | $T^{*}$ | $m_{\mathrm{adj}}$ | --- | ✓ |
| *(predicted)* | Collisionless reversibility | --- | $\mathcal{T}^{*}$ | $m_{\mathrm{rev}}$ | --- | ✓ |

## Compression delta (body → supplementary)

| Item | Body table (compressed) | This file (full) |
|---|---|---|
| Rows | 7 | 12 |
| $G$ block coverage | 1 (geometric only) | 2 (geometric + geometric) |
| $O_{\le}$ block coverage | 1 ($\Sigma_a$ direction) | 2 ($\Sigma_a$ + $\nu\Sigma_f$ directions) |
| $\mathcal{L}^{*}$ block coverage | 1 (spatial) | 2 (spatial + temporal) |
| $\mathcal{D}^{*}$ block coverage | 1 (transient) | 2 (transient + depletion) |
| $\mathcal{E}^{*}$ block coverage | 1 (algorithmic) | 2 (algorithmic + approximation) |
| Predicted MRs | 2 ($m_{\mathrm{adj}}$, $m_{\mathrm{rev}}$) | 2 (same) |

The body's 7-row presentation preserves "one canonical MR per non-empty block" representativeness; this file's additional 5 rows provide per-block sub-category coverage as design intent of the original 12-MR selection.

## References

- Bell & Glasstone 1970, *Nuclear Reactor Theory*
- Lewis & Miller 1993, *Computational Methods of Neutron Transport*
- Stamm'ler & Abbate 1983, *Methods of Steady-State Reactor Physics in Nuclear Design*
