"""
NOETHER reference implementation: CONSTRUCT-MP.
Implements the four-step procedure of Section 4.2 and the canonical-block
ordering of Definition (canonical-block-ordering).

This is the production-grade analogue of the toy sketch in Appendix D.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable

# Section 3.10 / Hypothesis 1: the seven blocks, in canonical priority order.
# This ordering is also Definition (canonical-block-ordering).
CANONICAL_ORDER: tuple[str, ...] = (
    "G",        # Symmetry
    "O_le",     # Order (monotone / linear)
    "T*",       # Self-adjoint
    "T_rev*",   # Time-reversal
    "L*",       # Limit
    "D*",       # Qualitative-dynamics
    "E*",       # Method-comparison
)

BLOCK_LABELS: dict[str, str] = {
    "G": "m_inv",
    "O_le": "m_mono",
    "T*": "m_adj",
    "T_rev*": "m_rev",
    "L*": "m_conv",
    "D*": "m_dyn",
    "E*": "m_cmp",
}


# -----------------------------------------------------------------------------
# Core data types
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class Operator:
    """An operator in the program-induced operator algebra A_P."""
    name: str
    block: str  # one of CANONICAL_ORDER

    def __post_init__(self) -> None:
        if self.block not in CANONICAL_ORDER:
            raise ValueError(
                f"Operator block {self.block!r} not in CANONICAL_ORDER"
            )


@dataclass(frozen=True)
class Invariant:
    """An invariant of A_P under a given block."""
    operator: Operator
    description: str


@dataclass(frozen=True)
class MR:
    """A metamorphic relation derived via Translate."""
    invariant: Invariant
    template: str

    @property
    def block(self) -> str:
        return self.invariant.operator.block


@dataclass
class MetaPattern:
    """An equivalence class of MRs sharing a structural source."""
    block: str
    label: str
    members: set[MR] = field(default_factory=set)


# -----------------------------------------------------------------------------
# Step 1: invariant extraction (per-block)
# -----------------------------------------------------------------------------

# An invariant extractor for a block returns the invariants discovered for an
# operator in that block. Each block has block-specific extraction logic; in a
# production system these would call back into a domain-specific analysis
# (group-theory library, partial-order analyser, inner-product checker, etc.).
# Here we accept user-supplied extractors keyed by block name.

InvariantExtractor = Callable[[Operator], Iterable[Invariant]]


def extract_invariants(
    generators: Iterable[Operator],
    extractors: dict[str, InvariantExtractor],
) -> dict[str, list[Invariant]]:
    """Step 1: for each block, gather invariants from each generator."""
    inv_by_block: dict[str, list[Invariant]] = {b: [] for b in CANONICAL_ORDER}
    for g in generators:
        if g.block in extractors:
            inv_by_block[g.block].extend(extractors[g.block](g))
    return inv_by_block


# -----------------------------------------------------------------------------
# Step 2: Translate
# -----------------------------------------------------------------------------

def translate(iota: Invariant) -> MR:
    """Step 2: derive an MR from an invariant. Domain-specific in practice."""
    return MR(invariant=iota, template=iota.description)


# -----------------------------------------------------------------------------
# Step 3-4: quotient and aggregation
# -----------------------------------------------------------------------------

def construct_mp(
    generators: Iterable[Operator],
    extractors: dict[str, InvariantExtractor],
) -> list[MetaPattern]:
    """The full CONSTRUCT-MP procedure (Steps 1-4 of Section 4.2)."""
    inv_by_block = extract_invariants(generators, extractors)
    metapatterns: list[MetaPattern] = []
    for block in CANONICAL_ORDER:
        invariants = inv_by_block[block]
        if not invariants:
            continue
        mrs = {translate(i) for i in invariants}
        metapatterns.append(
            MetaPattern(
                block=block,
                label=BLOCK_LABELS[block],
                members=mrs,
            )
        )
    return metapatterns


# -----------------------------------------------------------------------------
# Canonical-block-ordering reduction (Definition canonical-order)
# -----------------------------------------------------------------------------

def canonical_assign(rho: MR, block_candidates: set[str]) -> str:
    """Assign rho to its highest-priority block from block_candidates.

    Theorem (Algebraic Closure under Translate): for an algebra-induced MR
    derivable through multiple blocks, the canonical-block ordering returns a
    unique block.
    """
    for b in CANONICAL_ORDER:  # iterate in priority order
        if b in block_candidates:
            return b
    raise ValueError(
        f"MR {rho.template!r} has no candidate block in CANONICAL_ORDER"
    )


# -----------------------------------------------------------------------------
# Coverage metric (Section 7.3)
# -----------------------------------------------------------------------------

def coverage_noether(
    mr_set: set[MR],
    metapatterns: list[MetaPattern],
) -> float:
    """coverage_NOETHER from Section 7.3: |covered MPs| / |total MPs|.

    A MetaPattern is 'covered' by mr_set if at least one MR in mr_set falls
    in that MetaPattern.
    """
    if not metapatterns:
        return 0.0
    covered = 0
    for mp in metapatterns:
        if any(mr.block == mp.block for mr in mr_set):
            covered += 1
    return covered / len(metapatterns)


# -----------------------------------------------------------------------------
# Default extractors for the toy bit-flip algebra (parallel to Appendix D)
# -----------------------------------------------------------------------------

def default_extractor_G(op: Operator) -> list[Invariant]:
    return [Invariant(op, f"P(g.x) = rho(g).P(x) for g={op.name}")]


def default_extractor_Ole(op: Operator) -> list[Invariant]:
    return [
        Invariant(
            op,
            f"x1 <=_theta x2 => P(x1) <=_Y P(x2) for theta={op.name}",
        )
    ]


def default_extractor_Tstar(op: Operator) -> list[Invariant]:
    return [Invariant(op, f"<L x, y> = <x, L y> for L={op.name}")]


def default_extractor_Trev(op: Operator) -> list[Invariant]:
    return [Invariant(op, f"P(T x) determined by P(x) via {op.name}")]


def default_extractor_Lstar(op: Operator) -> list[Invariant]:
    return [Invariant(op, f"L_theta -> L_* as theta -> theta_* via {op.name}")]


def default_extractor_Dstar(op: Operator) -> list[Invariant]:
    return [Invariant(op, f"qualitative invariant under {op.name}")]


def default_extractor_Estar(op: Operator) -> list[Invariant]:
    return [Invariant(op, f"M1 <=_E M2 partial order via {op.name}")]


DEFAULT_EXTRACTORS: dict[str, InvariantExtractor] = {
    "G": default_extractor_G,
    "O_le": default_extractor_Ole,
    "T*": default_extractor_Tstar,
    "T_rev*": default_extractor_Trev,
    "L*": default_extractor_Lstar,
    "D*": default_extractor_Dstar,
    "E*": default_extractor_Estar,
}


# -----------------------------------------------------------------------------
# Demonstration
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # Toy bit-flip algebra (parallel to Appendix D)
    Z2 = Operator("bit_flip", "G")
    perm = Operator("permutation_S3", "G")
    scale = Operator("input_scaling", "O_le")

    mp_set = construct_mp([Z2, perm, scale], DEFAULT_EXTRACTORS)
    for mp in mp_set:
        print(f"MetaPattern {mp.label} (block {mp.block}):")
        for mr in mp.members:
            print(f"  - {mr.template}")
