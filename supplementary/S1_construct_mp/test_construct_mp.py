"""
Unit tests for construct_mp.py.

Run with: python -m pytest test_construct_mp.py -v
"""

from __future__ import annotations

import pytest

from construct_mp import (
    BLOCK_LABELS,
    CANONICAL_ORDER,
    DEFAULT_EXTRACTORS,
    Invariant,
    Operator,
    canonical_assign,
    construct_mp,
    coverage_noether,
    translate,
)


# -----------------------------------------------------------------------------
# Construct validity (Theorem closure: existence + uniqueness)
# -----------------------------------------------------------------------------

def test_canonical_order_is_total() -> None:
    """Canonical-block ordering covers all seven blocks exactly once."""
    assert len(CANONICAL_ORDER) == 7
    assert len(set(CANONICAL_ORDER)) == 7


def test_block_labels_cover_canonical_order() -> None:
    """Every block has a MetaPattern label."""
    for b in CANONICAL_ORDER:
        assert b in BLOCK_LABELS


def test_operator_validates_block() -> None:
    """Operator constructor rejects unknown blocks."""
    with pytest.raises(ValueError):
        Operator("bad", "Z*")


# -----------------------------------------------------------------------------
# CONSTRUCT-MP step semantics
# -----------------------------------------------------------------------------

def test_construct_mp_empty_input_returns_empty_set() -> None:
    """No generators -> no MetaPatterns."""
    assert construct_mp([], DEFAULT_EXTRACTORS) == []


def test_construct_mp_single_block_yields_one_metapattern() -> None:
    """A single G-block generator yields exactly one MetaPattern (m_inv)."""
    g = Operator("test_sym", "G")
    result = construct_mp([g], DEFAULT_EXTRACTORS)
    assert len(result) == 1
    assert result[0].block == "G"
    assert result[0].label == "m_inv"


def test_construct_mp_respects_canonical_order() -> None:
    """MetaPatterns appear in canonical block order."""
    ops = [
        Operator("comp", "E*"),
        Operator("dyn", "D*"),
        Operator("sym", "G"),
    ]
    result = construct_mp(ops, DEFAULT_EXTRACTORS)
    blocks = [mp.block for mp in result]
    assert blocks == ["G", "D*", "E*"]


def test_construct_mp_aggregates_within_block() -> None:
    """Multiple generators in the same block produce one MetaPattern with
    multiple members."""
    ops = [Operator("g1", "G"), Operator("g2", "G")]
    result = construct_mp(ops, DEFAULT_EXTRACTORS)
    assert len(result) == 1
    assert len(result[0].members) == 2


# -----------------------------------------------------------------------------
# Canonical-block-ordering reduction (Lemma C.1)
# -----------------------------------------------------------------------------

def test_canonical_assign_picks_highest_priority() -> None:
    """An MR derivable through G and T* is assigned to G (G > T*)."""
    op = Operator("dummy", "G")
    iota = Invariant(op, "test invariant")
    rho = translate(iota)
    assert canonical_assign(rho, {"G", "T*"}) == "G"


def test_canonical_assign_uniqueness() -> None:
    """For any nonempty subset of CANONICAL_ORDER, canonical_assign returns
    a single, deterministic block."""
    op = Operator("dummy", "G")
    iota = Invariant(op, "test")
    rho = translate(iota)
    candidates = {"D*", "L*", "E*"}
    assert canonical_assign(rho, candidates) == "L*"  # L* > D* > E*


def test_canonical_assign_empty_raises() -> None:
    """Empty candidate set is an error (no block to assign to)."""
    op = Operator("dummy", "G")
    iota = Invariant(op, "test")
    rho = translate(iota)
    with pytest.raises(ValueError):
        canonical_assign(rho, set())


# -----------------------------------------------------------------------------
# coverage_NOETHER (Section 7.3)
# -----------------------------------------------------------------------------

def test_coverage_full_is_one() -> None:
    """An MR set spanning every MetaPattern has coverage 1.0."""
    ops = [Operator(f"op_{b}", b) for b in CANONICAL_ORDER]
    metapatterns = construct_mp(ops, DEFAULT_EXTRACTORS)
    all_mrs = {mr for mp in metapatterns for mr in mp.members}
    assert coverage_noether(all_mrs, metapatterns) == 1.0


def test_coverage_partial() -> None:
    """An MR set covering 2 of 3 MetaPatterns gives coverage 2/3."""
    ops = [Operator("g", "G"), Operator("o", "O_le"), Operator("d", "D*")]
    metapatterns = construct_mp(ops, DEFAULT_EXTRACTORS)
    # Only G and O_le members in the test MR set
    test_mrs = {
        mr for mp in metapatterns if mp.block in ("G", "O_le") for mr in mp.members
    }
    assert coverage_noether(test_mrs, metapatterns) == pytest.approx(2 / 3)


def test_coverage_empty() -> None:
    """Empty MR set has coverage 0."""
    ops = [Operator("g", "G")]
    metapatterns = construct_mp(ops, DEFAULT_EXTRACTORS)
    assert coverage_noether(set(), metapatterns) == 0.0
