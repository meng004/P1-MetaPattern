"""
NOETHER instantiation: Boltzmann transport equation (Section 5).

Constructs A_Boltz, runs CONSTRUCT-MP, and emits the seven-MetaPattern set
M(A_Boltz) = {m_inv, m_mono, m_adj, m_rev, m_conv, m_dyn, m_cmp}.
"""

from __future__ import annotations

from construct_mp import (
    DEFAULT_EXTRACTORS,
    Invariant,
    Operator,
    construct_mp,
    coverage_noether,
)


def build_a_boltz() -> list[Operator]:
    """Operators of A_Boltz, decomposed into the seven blocks (Section 5.1)."""
    return [
        # G: symmetry
        Operator("G_geom_quarter_rotation", "G"),
        Operator("R_E_energy_group_permutation", "G"),
        # O_le: order (cross-section monotonicity)
        Operator("L_Sigma_a_monotone", "O_le"),
        Operator("L_nu_monotone", "O_le"),
        # T*: self-adjoint (adjoint transport)
        Operator("L_star_adjoint_transport", "T*"),
        # T_rev*: time-reversal (collisionless sub-formulation)
        Operator("T_collisionless_reverse", "T_rev*"),
        # L*: limit (mesh refinement, CRAM order)
        Operator("L_h_mesh_refinement", "L*"),
        Operator("L_cram_order_limit", "L*"),
        # D*: qualitative-dynamics (Bateman, iodine pit, Gd self-shielding)
        Operator("D_bateman_iodine_pit", "D*"),
        Operator("D_gd_s_curve", "D*"),
        # E*: method-comparison (CRAM vs TTA, P0 vs higher-order scattering)
        Operator("E_cram_vs_tta", "E*"),
        Operator("E_p0_vs_pn", "E*"),
    ]


# Domain-specific invariant descriptions for the Boltzmann case
BOLTZ_EXTRACTORS = dict(DEFAULT_EXTRACTORS)


def boltz_extractor_G(op: Operator) -> list[Invariant]:
    return [
        Invariant(op, f"flux invariant under {op.name}"),
    ]


def boltz_extractor_T_star(op: Operator) -> list[Invariant]:
    return [
        Invariant(
            op,
            "<L psi, phi*> = <psi, L^dagger phi*> "
            "(adjoint-flux reciprocity)",
        ),
    ]


def boltz_extractor_T_rev(op: Operator) -> list[Invariant]:
    return [
        Invariant(
            op,
            "P(T x) = T P(x) for collisionless trajectories "
            "(time-reversal symmetry)",
        ),
    ]


def boltz_extractor_L_star(op: Operator) -> list[Invariant]:
    return [
        Invariant(
            op, f"||P^(h) - P^(h*)||_L2 = O(h^k) under refinement {op.name}"
        ),
    ]


def boltz_extractor_D_star(op: Operator) -> list[Invariant]:
    return [
        Invariant(
            op, f"qualitative shape invariant for {op.name} (Sturm-type)"
        ),
    ]


def boltz_extractor_E_star(op: Operator) -> list[Invariant]:
    return [Invariant(op, f"err(M1) <= err(M2) on benchmark via {op.name}")]


BOLTZ_EXTRACTORS["G"] = boltz_extractor_G
BOLTZ_EXTRACTORS["T*"] = boltz_extractor_T_star
BOLTZ_EXTRACTORS["T_rev*"] = boltz_extractor_T_rev
BOLTZ_EXTRACTORS["L*"] = boltz_extractor_L_star
BOLTZ_EXTRACTORS["D*"] = boltz_extractor_D_star
BOLTZ_EXTRACTORS["E*"] = boltz_extractor_E_star


def main() -> None:
    a_boltz = build_a_boltz()
    metapatterns = construct_mp(a_boltz, BOLTZ_EXTRACTORS)
    print("=== M(A_Boltz) ===")
    for mp in metapatterns:
        print(f"\n{mp.label} ({mp.block}):")
        for mr in mp.members:
            print(f"  - {mr.template}")
    print(f"\nTotal MetaPatterns: {len(metapatterns)} (expected 7)")
    # Coverage check: an MR set spanning all blocks gives 100%
    all_mrs = {mr for mp in metapatterns for mr in mp.members}
    cov = coverage_noether(all_mrs, metapatterns)
    print(f"coverage_NOETHER (full set) = {cov:.2f}")


if __name__ == "__main__":
    main()
