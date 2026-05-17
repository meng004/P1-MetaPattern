# Case A-bis Full Per-Class Decoding (Murphy et al. 2008 → NOETHER)

Migrated from `NOETHER_paper.tex` §subsec:pmcm-worked, Case A-bis (Tier 2 compression, 2026-05-16). Body retains the verdict (denominator 1 not 6) and high-level mechanism (3 vacuous + 3 collapse); this file carries the full per-class decoding.

## Murphy's six classes (full definitions)

Murphy et al.~\cite{Murphy2008} classify MRs for ML applications into six families:

1. **Additive**: $P(\mathbf{x}+\boldsymbol{\delta}) \approx P(\mathbf{x})$ for small $\boldsymbol{\delta}$
2. **Multiplicative**: $P(c\mathbf{x}) \approx P(\mathbf{x})$ for scaling $c$
3. **Permutative**: $P(\sigma(\mathbf{x})) = P(\mathbf{x})$ for input-coordinate permutation $\sigma$
4. **Invertive**: $P(-\mathbf{x})$ has a stated relation to $P(\mathbf{x})$
5. **Inclusive**: a feature added to $\mathbf{x}$ refines $P$ in a stated direction
6. **Exclusive**: a feature removed degrades $P$ in a stated direction

## SUT setup: generic feedforward image classifier

Consider $f: \mathbb{R}^{n} \to \{1, \dots, K\}$ trained on a fixed-dimensional vector input (e.g.\ a flattened MNIST or CIFAR-10 image), with no inherent permutation structure.

Induced operator algebra $\mathcal{A}_{\mathrm{FFN}}$:

- $G$: trivial under input-coordinate permutation (no permutation symmetry on a vector image)
- $O_{\le}$: one non-trivial generator under small additive noise (stability condition with tolerance threshold)
- $\mathcal{L}^{*}$: same generator under vanishing-perturbation reading
- $T^{*}$, $\mathcal{T}^{*}$, $\mathcal{D}^{*}$, $\mathcal{E}^{*}$, $\mathcal{B}^{*}_{\mathrm{rel}}$: empty within a single architecture

Therefore $\mathbb{M}(\mathcal{A}_{\mathrm{FFN}}) \subseteq \{m_{\mathrm{stab}}\}$.

## NOETHER decoding of Murphy's six classes

| Murphy class | NOETHER mapping | Block | Status on generic FFN |
|---|---|---|---|
| **Additive** (small $\boldsymbol{\delta}$) | $m_{\mathrm{stab}}$ | $O_{\le}$ or $\mathcal{L}^{*}$ | Active |
| **Multiplicative** (scaling) | $m_{\mathrm{inv}}$ iff scale-invariant model (rare) | $G$ | Vacuous on raw image classifier |
| **Permutative** | $m_{\mathrm{inv}}$ iff input is set-valued (point-cloud / bag-of-features) | $G$ | Vacuous on vector image classifier |
| **Invertive** | $m_{\mathrm{inv}}$ as $\mathbb{Z}/2$ subgroup iff antipodal symmetry (rare for natural images) | $G$ | Vacuous |
| **Inclusive** | Monotonicity-under-feature-addition; collapses to $m_{\mathrm{stab}}$ on perturbation ball | $O_{\le}$ | Merges with Additive |
| **Exclusive** | Monotonicity-under-feature-removal; collapses to $m_{\mathrm{stab}}$ on perturbation ball | $O_{\le}$ | Merges with Additive |

## Coverage correction

Of Murphy's six classes:

- **3 structurally vacuous**: multiplicative, permutative, invertive (no relevant input symmetries on generic vector image classifier)
- **3 collapse to one**: additive, inclusive, exclusive all map to $m_{\mathrm{stab}}$ under $\mathcal{A}_{\mathrm{FFN}}$'s decomposition

**Structurally meaningful denominator: 1, not 6.**

A user reporting "$k/6$ Murphy-class coverage" on a generic vector image classifier is reporting a claim about Murphy's catalogue's row count rather than a structural-coverage claim about their MR set.

## Caveat — Murphy's intent vs. subsequent usage

Murphy et al.\ explicitly intended their six classes as a **checklist for selecting MRs**, not as a coverage denominator. The target of this correction is subsequent papers that report Murphy-grid coverage figures on tasks lacking the relevant input symmetries~\cite{Saha2019SupervisedMR}, not the original 2008 paper.

The decoding is structurally driven and does not depend on the specific 14.8\% detection figure of \cite{Saha2019SupervisedMR}; that figure is consistent with the structural prediction that few of Murphy's six classes are non-trivially present on a generic supervised classifier.

## Framework-circularity boundary

The deflationary direction here is independent of $T^{*}$ and $\mathcal{T}^{*}$, since neither block is invoked by Murphy's six classes or $\mathcal{A}_{\mathrm{FFN}}$. The decoding therefore does not inherit the prediction-circularity caveat of §subsec:reactor-mapping.
