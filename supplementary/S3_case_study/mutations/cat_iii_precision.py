"""
Category (iii) — Numerical-precision degradation (5 mutations).

Adapted from P2's HP (Hyperparameter) operator class. Operates on the
classification head weight (key auto-resolved via head_weight_key).
"""

from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mutations._base import Mutation, head_weight_key


def _mut_iii_01(model):
    """Cast head from fp32/fp64 to fp16 then back (lossy)."""
    m = deepcopy(model)
    k = head_weight_key(m.theta)
    orig_dtype = m.theta[k].dtype
    m.theta[k] = m.theta[k].astype(np.float16).astype(orig_dtype)
    return m


def _mut_iii_02(model):
    """Truncate head weight to 4 decimal places."""
    m = deepcopy(model)
    k = head_weight_key(m.theta)
    m.theta[k] = np.round(m.theta[k], 4).astype(m.theta[k].dtype)
    return m


def _mut_iii_03(model):
    """Symmetric int8 quantisation of head weight (lossy)."""
    m = deepcopy(model)
    k = head_weight_key(m.theta)
    w = m.theta[k]
    scale = max(abs(w.min()), abs(w.max())) / 127.0 if w.size > 0 else 1.0
    if scale > 0:
        m.theta[k] = (np.round(w / scale).astype(np.int8) * scale).astype(w.dtype)
    return m


def _mut_iii_04(model):
    """Inject a single NaN at head_weight[0,0]."""
    m = deepcopy(model)
    k = head_weight_key(m.theta)
    m.theta[k][0, 0] = np.nan
    return m


def _mut_iii_05(model):
    """Flush near-zero head entries (|w| < 1e-3) to zero (denormal flush)."""
    m = deepcopy(model)
    k = head_weight_key(m.theta)
    w = m.theta[k]
    w[np.abs(w) < 1e-3] = 0.0
    m.theta[k] = w
    return m


MUTATIONS_CAT_III = [
    Mutation(
        id="cat_iii_01", category="iii", label="fp16_round_trip",
        description="cast head to fp16 and back",
        apply=_mut_iii_01, sources_p2=True,
    ),
    Mutation(
        id="cat_iii_02", category="iii", label="truncate_4dp",
        description="round head to 4 decimal places",
        apply=_mut_iii_02, sources_p2=True,
    ),
    Mutation(
        id="cat_iii_03", category="iii", label="int8_quantize",
        description="symmetric int8 quantisation of head",
        apply=_mut_iii_03, sources_p2=True,
    ),
    Mutation(
        id="cat_iii_04", category="iii", label="nan_injection",
        description="set head[0,0] = NaN",
        apply=_mut_iii_04, sources_p2=False,
    ),
    Mutation(
        id="cat_iii_05", category="iii", label="denormal_flush",
        description="zero out head entries with |w|<1e-3",
        apply=_mut_iii_05, sources_p2=False,
    ),
]
