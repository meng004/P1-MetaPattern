"""
Set N: NOETHER-derived MRs for TriangleClassification.

Each MR is a callable that takes (mutant_classifier, base_input, follow_up_input)
and returns a 3-valued result: 'pass' / 'fail' / 'na'.

The follow-up generation is per-MR canonical (Section 3.1, Definition Translate).

P : (a, b, c) -> str    where str in {"equilateral", "isosceles", "scalene", "degenerate"}.
"""

from itertools import permutations
from typing import Callable, Tuple

Triangle = Tuple[float, float, float]
Classifier = Callable[[Triangle], str]


def rho_perm(P: Classifier, base: Triangle, _follow_up: Triangle) -> str:
    """
    G-block (block invariant: S_3 permutation symmetry on edge labels).
    All 6 permutations must yield the same classification.
    """
    base_label = P(base)
    for perm in permutations(base):
        permuted: Triangle = (perm[0], perm[1], perm[2])
        if P(permuted) != base_label:
            return "fail"
    return "pass"


def rho_scale(P: Classifier, base: Triangle, _follow_up: Triangle) -> str:
    """
    G-block (block invariant: scaling group action by R_{>0}).
    Uniform scaling preserves classification (within a small set of test scales).
    """
    base_label = P(base)
    for s in (0.5, 2.0, 10.0):
        scaled = (base[0] * s, base[1] * s, base[2] * s)
        if P(scaled) != base_label:
            return "fail"
    return "pass"


def rho_mono(P: Classifier, base: Triangle, follow_up: Triangle) -> str:
    """
    O_le-block (block invariant: degeneracy ordering).
    follow_up should be base with the longest side increased by epsilon (closer
    to triangle inequality boundary). Classification should not move 'away' from
    'degenerate' as the triangle approaches the boundary.

    Encoded as: if base is non-degenerate and follow_up is degenerate, MR holds.
    If base is degenerate and follow_up is non-degenerate, MR fails (regression
    from boundary).
    """
    base_label = P(base)
    fu_label = P(follow_up)
    if base_label == "degenerate" and fu_label != "degenerate":
        a, b, c = follow_up
        max_side = max(a, b, c)
        sum_other = a + b + c - max_side
        if max_side >= sum_other:  # follow-up still degenerate by triangle inequality
            return "fail"
    return "pass"


def rho_eqref(P: Classifier, base: Triangle, follow_up: Triangle) -> str:
    """
    O_le-block (block invariant: edge-equality refinement).
    follow_up: same triangle but with sides modified to be MORE equal.
    Classification should refine: scalene -> isosceles -> equilateral.
    """
    refinement_order = {"scalene": 0, "isosceles": 1, "equilateral": 2, "degenerate": -1}
    base_label = P(base)
    fu_label = P(follow_up)
    base_rank = refinement_order.get(base_label, -1)
    fu_rank = refinement_order.get(fu_label, -1)
    if base_rank < 0 or fu_rank < 0:
        return "na"
    # Follow-up sides should not be 'less equal' than base sides.
    sd = lambda t: max(t) - min(t)
    if sd(follow_up) <= sd(base) and fu_rank < base_rank:
        return "fail"
    return "pass"


# Set N is the union of these four MRs.
SET_N = [rho_perm, rho_scale, rho_mono, rho_eqref]
