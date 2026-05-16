# A_rel Operator Algebra — Full Per-Block Breakdown

Migrated from §subsec:third-domain body (Tier 1 length compression, 2026-05-16). Body keeps the summary mapping; this document carries the per-block details.

## Per-block enumeration

### $G$ block (symmetry)
- Permutation of inner-join arguments: $q_1 \bowtie q_2 \cong q_2 \bowtie q_1$
- Commutativity and associativity of $\cup$
- Permutation-invariance of `SELECT` clauses with set semantics

### $O_{\le}$ block (order)
- Monotonicity under selection-strengthening: $\sigma_{p \wedge p'}(R) \subseteq \sigma_p(R)$
- Monotonicity under projection-coarsening

### $\mathcal{E}^{*}$ block (method comparison)
- Alternative execution plans for the same query (hash-join vs.\ merge-join vs.\ nested-loop) producing identical relations within their stated cost models. References: Wang et al. 2024 QED; Markl 2022 Learned Query Optimisers.

### $\mathcal{B}^{*}_{\mathrm{rel}}$ block (relational equivalence)

The most algebraically substantive MR phenomena in relational query optimisation are captured neither by $G$, $O_{\le}$, nor $\mathcal{E}^{*}$:

1. **Selection-pushdown equivalence**: $\sigma_p(R \bowtie S) = \sigma_p(R) \bowtie S$ when $p$ refers only to attributes of $R$. Equivalence under *rewriting*.
2. **Distinct-idempotence**: $\sigma_p(\sigma_p(R)) = \sigma_p(R)$. Idempotent identity.
3. **Constant-folding equivalences**: $\sigma_{1=1}(R) = R$, $R \bowtie \emptyset = \emptyset$. Algebraic identities under the relational semiring.

These are exactly the phenomena $\mathcal{B}^{*}_{\mathrm{rel}}$ (Definition 16 in body) is designed to capture.

### Empty blocks under $\mathcal{A}_{\mathrm{rel}}$

- $T^{*}$ (self-adjoint): no inner-product self-adjointness on relational queries.
- $\mathcal{T}^{*}_{\mathrm{rev}}$ (time-reversal): queries do not have a forward/inverse pair in the Boltzmann sense.
- $\mathcal{D}^{*}$ (qualitative dynamics): no trajectory-sense dynamics.
- $\mathcal{L}^{*}$ (limit): no $\epsilon$-limit operator on exact-relational semantics.

Therefore CONSTRUCT-MP on $\mathcal{A}_{\mathrm{rel}}$ yields 3 MetaPatterns from the seven non-$\mathcal{B}^{*}_{\mathrm{rel}}$ blocks ($m^{\mathrm{rel}}_{\mathrm{inv}}$, $m^{\mathrm{rel}}_{\mathrm{mono}}$, $m^{\mathrm{rel}}_{\mathrm{cmp}}$) plus the 1 MetaPattern from the $\mathcal{B}^{*}_{\mathrm{rel}}$ block (set of relational-equivalence rewrites). Total 4 MRs as enumerated in body §subsec:third-domain.
