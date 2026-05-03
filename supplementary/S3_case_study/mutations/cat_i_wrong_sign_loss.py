"""
Category (i) — Wrong-sign loss term (5 mutations).

Adapted in spirit from P2's CE (Constant Edit) operator class. Each
mutation flips a sign or magnitude in the classification-head weights
(the post-loss-function effect on parameters).

Compatible with both StubModel (head_weight/head_bias dict) and the
trained EGNN classifier (head.weight/head.bias state_dict).
"""

from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mutations._base import Mutation, head_bias_key, head_weight_key


def _mut_i_01(model):
    """Negate the entire classification-head weight (full sign flip)."""
    m = deepcopy(model)
    k = head_weight_key(m.theta)
    m.theta[k] = -m.theta[k]
    return m


def _mut_i_02(model):
    """Negate only the bias vector (partial sign flip)."""
    m = deepcopy(model)
    k = head_bias_key(m.theta)
    m.theta[k] = -m.theta[k]
    return m


def _mut_i_03(model):
    """Flip sign on the first half of head-weight columns."""
    m = deepcopy(model)
    k = head_weight_key(m.theta)
    w = m.theta[k]
    n_half = w.shape[-1] // 2 if w.ndim >= 2 else len(w) // 2
    if w.ndim == 2 and w.shape[0] >= w.shape[1]:
        # StubModel layout: (in_dim, n_classes)
        w[:, :n_half] = -w[:, :n_half]
    else:
        # PyTorch nn.Linear layout: (out_features, in_features)
        w[:n_half, :] = -w[:n_half, :]
    m.theta[k] = w
    return m


def _mut_i_04(model):
    """Replace head with -head + small noise (sign flip + perturbation)."""
    m = deepcopy(model)
    k = head_weight_key(m.theta)
    rng = np.random.default_rng(2001)
    m.theta[k] = (-m.theta[k] + 0.01 * rng.standard_normal(m.theta[k].shape).astype(m.theta[k].dtype))
    return m


def _mut_i_05(model):
    """Multiply head-weight by -2.0 (sign flip + magnitude inflation)."""
    m = deepcopy(model)
    k = head_weight_key(m.theta)
    m.theta[k] = -2.0 * m.theta[k]
    return m


MUTATIONS_CAT_I = [
    Mutation(
        id="cat_i_01", category="i", label="full_head_negation",
        description="negate entire classification head weight",
        apply=_mut_i_01, sources_p2=True,
    ),
    Mutation(
        id="cat_i_02", category="i", label="bias_negation",
        description="negate classification bias vector",
        apply=_mut_i_02, sources_p2=True,
    ),
    Mutation(
        id="cat_i_03", category="i", label="half_block_flip",
        description="flip sign on first half of head weight columns",
        apply=_mut_i_03, sources_p2=True,
    ),
    Mutation(
        id="cat_i_04", category="i", label="sign_flip_with_noise",
        description="negate head + add 1% Gaussian noise",
        apply=_mut_i_04, sources_p2=True,
    ),
    Mutation(
        id="cat_i_05", category="i", label="negation_2x_magnitude",
        description="multiply head by -2 (sign + magnitude)",
        apply=_mut_i_05, sources_p2=True,
    ),
]
