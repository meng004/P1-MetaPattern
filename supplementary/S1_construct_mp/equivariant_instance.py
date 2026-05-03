"""
NOETHER instantiation: equivariant ML program family (Section 6).

Constructs A_equi, runs CONSTRUCT-MP, and emits five non-empty MetaPatterns
M(A_equi)_non-empty = {m_inv, m_mono, m_adj, m_rev, m_conv}.

D* and E* are empty within a single feedforward classifier architecture
(Section 6.1).
"""

from __future__ import annotations

from construct_mp import (
    DEFAULT_EXTRACTORS,
    Invariant,
    Operator,
    construct_mp,
    coverage_noether,
)


def build_a_equi() -> list[Operator]:
    """Operators of A_equi (Section 6.1).

    For an SE(3)-equivariant point-cloud classifier with G = SO(3) x S_n.
    """
    return [
        # G: symmetry (SO(3) x S_n)
        Operator("SO3_rotation", "G"),
        Operator("S_n_permutation", "G"),
        # O_le: order (training-set inclusion monotonicity, etc.)
        Operator("O_train_set_inclusion", "O_le"),
        # T*: self-adjoint (Hermitian-attention, Section 6.4)
        Operator("T_attention_kernel_symmetric", "T*"),
        # T_rev*: time-reversal (training-trajectory reversibility, Section 6.5)
        Operator("T_sgd_step_reversible", "T_rev*"),
        # L*: limit (training-size, depth, dimension)
        Operator("L_train_size_limit", "L*"),
        Operator("L_depth_limit", "L*"),
        Operator("L_dim_limit", "L*"),
        # D*: empty for feedforward classifiers (Section 6.1)
        # E*: empty within a single architecture (Section 6.1)
    ]


EQUI_EXTRACTORS = dict(DEFAULT_EXTRACTORS)


def equi_extractor_G(op: Operator) -> list[Invariant]:
    if "SO3" in op.name:
        return [
            Invariant(
                op,
                "f(R . x) = f(x) for R in SO(3) "
                "[rho_rot, Section 6.3]",
            )
        ]
    if "S_n" in op.name:
        return [
            Invariant(
                op,
                "f(sigma . x) = f(x) for sigma in S_n "
                "[rho_perm, Appendix D]",
            )
        ]
    return [Invariant(op, f"f-equivariance under {op.name}")]


def equi_extractor_T_star(op: Operator) -> list[Invariant]:
    return [
        Invariant(
            op,
            "Tr A(x1, x2) = Tr A(x2, x1) "
            "[rho_adj, Section 6.4]",
        )
    ]


def equi_extractor_T_rev(op: Operator) -> list[Invariant]:
    return [
        Invariant(
            op,
            "(T o U_eta o T^-1 o U_eta)(theta) = theta + O(eta^2) "
            "[rho_train-rev, Section 6.5]",
        )
    ]


def equi_extractor_L_star(op: Operator) -> list[Invariant]:
    return [
        Invariant(
            op,
            f"convergence as {op.name.split('_')[1]} -> infinity "
            "[rho_train et al.]",
        )
    ]


EQUI_EXTRACTORS["G"] = equi_extractor_G
EQUI_EXTRACTORS["T*"] = equi_extractor_T_star
EQUI_EXTRACTORS["T_rev*"] = equi_extractor_T_rev
EQUI_EXTRACTORS["L*"] = equi_extractor_L_star


def main() -> None:
    a_equi = build_a_equi()
    metapatterns = construct_mp(a_equi, EQUI_EXTRACTORS)
    print("=== M(A_equi) ===")
    for mp in metapatterns:
        print(f"\n{mp.label} ({mp.block}):")
        for mr in mp.members:
            print(f"  - {mr.template}")
    print(
        f"\nNon-empty MetaPatterns: {len(metapatterns)} "
        "(expected 5: m_inv, m_mono, m_adj, m_rev, m_conv)"
    )
    all_mrs = {mr for mp in metapatterns for mr in mp.members}
    cov = coverage_noether(all_mrs, metapatterns)
    print(f"coverage_NOETHER (full N set) = {cov:.2f}")


if __name__ == "__main__":
    main()
