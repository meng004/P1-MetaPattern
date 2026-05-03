"""
Category (v) — DeepCrime-style real-fault operators (5 mutations).

A pilot extension of the case study with 5 mutation operators inspired by the
DeepCrime taxonomy of Humbatova et al. (ISSTA 2021), which systematically
extracted 35 mutation operators from real DL fault studies. We implement here
5 representative operators applicable to a trained classifier checkpoint at
post-training time, since the case study uses a frozen EGNN checkpoint.

This category was added in revision Round-2 in response to the reviewer's
request to ground the comparative-evaluation protocol in real-fault mutation
operators rather than only hand-crafted defects.

Operators implemented:
  cat_v_01 (LR / Loss Reduction)   — head-weight scaled by 1/N (mean->sum-like effect)
  cat_v_02 (ACH / Activation Change) — head-weight passed through tanh-like saturation
  cat_v_03 (LRM / Layer Removal)    — zero out the head weight (layer effectively removed)
  cat_v_04 (BR  / Bias Removal)     — zero out the bias vector
  cat_v_05 (WCI / Weight Re-init)   — replace head-weight with fresh Glorot init

Detection follows the same strict-transition criterion as cat_i--cat_iv.
"""

from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mutations._base import Mutation, head_bias_key, head_weight_key


def _mut_v_01(model):
    """LR — Loss-reduction-like effect: scale head-weight by 1/N (N=num classes)."""
    m = deepcopy(model)
    k = head_weight_key(m.theta)
    n_classes = m.theta[k].shape[-1] if m.theta[k].ndim >= 2 else len(m.theta[k])
    m.theta[k] = m.theta[k] / float(max(n_classes, 1))
    return m


def _mut_v_02(model):
    """ACH — Activation Change: pass head-weight through tanh saturation."""
    m = deepcopy(model)
    k = head_weight_key(m.theta)
    m.theta[k] = np.tanh(m.theta[k] * 2.0).astype(m.theta[k].dtype)
    return m


def _mut_v_03(model):
    """LRM — Layer Removal: zero out the entire head-weight tensor."""
    m = deepcopy(model)
    k = head_weight_key(m.theta)
    m.theta[k] = np.zeros_like(m.theta[k])
    return m


def _mut_v_04(model):
    """BR — Bias Removal: zero out the head bias vector."""
    m = deepcopy(model)
    k = head_bias_key(m.theta)
    m.theta[k] = np.zeros_like(m.theta[k])
    return m


def _mut_v_05(model):
    """WCI — Weight Re-init: replace head-weight with fresh Glorot init."""
    m = deepcopy(model)
    k = head_weight_key(m.theta)
    rng = np.random.default_rng(20260502)
    w = m.theta[k]
    fan_in = w.shape[0]
    fan_out = w.shape[1] if w.ndim >= 2 else 1
    bound = float(np.sqrt(6.0 / max(fan_in + fan_out, 1)))
    m.theta[k] = rng.uniform(-bound, bound, size=w.shape).astype(w.dtype)
    return m


MUTATIONS_CAT_V = [
    Mutation(
        id="cat_v_01", category="v", label="loss_reduction_like",
        description="scale head weight by 1/N (mean-to-sum-like reduction effect)",
        apply=_mut_v_01, sources_p2=False,
    ),
    Mutation(
        id="cat_v_02", category="v", label="activation_saturation",
        description="pass head weight through tanh saturation",
        apply=_mut_v_02, sources_p2=False,
    ),
    Mutation(
        id="cat_v_03", category="v", label="layer_zeroed",
        description="zero out head weight (layer-removal effect)",
        apply=_mut_v_03, sources_p2=False,
    ),
    Mutation(
        id="cat_v_04", category="v", label="bias_removed",
        description="zero out head bias",
        apply=_mut_v_04, sources_p2=False,
    ),
    Mutation(
        id="cat_v_05", category="v", label="weight_reinit",
        description="re-initialise head weight with Glorot init",
        apply=_mut_v_05, sources_p2=False,
    ),
]
