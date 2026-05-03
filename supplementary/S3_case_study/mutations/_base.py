"""Common mutation contract for §6.6 case study."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


def head_weight_key(theta: dict) -> str:
    """Return the dict key holding the classification-head weight.

    Handles both StubModel (`head_weight`) and the trained EGNN
    (`head.weight`) naming.
    """
    for k in ("head.weight", "head_weight"):
        if k in theta:
            return k
    raise KeyError(f"no head-weight key found in theta; tried head.weight / head_weight; got keys={list(theta.keys())[:6]}…")


def head_bias_key(theta: dict) -> str:
    for k in ("head.bias", "head_bias"):
        if k in theta:
            return k
    raise KeyError("no head-bias key found in theta; tried head.bias / head_bias")


@dataclass(frozen=True)
class Mutation:
    id: str                          # e.g. "cat_i_01"
    category: str                    # "i" | "ii" | "iii" | "iv"
    label: str                       # short human-readable label
    description: str                 # one-line description
    apply: Callable[[Any], Any]       # baseline model -> mutated model
    sources_p2: bool = False         # True if adapted from P2 mutation operators


# Category mappings to manuscript §6.6:
# i   = wrong-sign loss term
# ii  = equivariance break (insertion of a non-equivariant intermediate)
# iii = numerical-precision degradation
# iv  = gradient-reversal sign error in the training script
