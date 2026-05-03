"""
Category (ii) — Equivariance break (5 mutations).

These mutations specifically violate the SE(3) equivariance contract.
They CANNOT be borrowed from P2's mutation operators because P2's PUTs
have no equivariance structure.

For StubModel, equivariance is only present when equivariant_break=False;
the cat-ii mutations switch this off or add explicitly non-equivariant
post-processing. In the real SE(3)-Transformer these correspond to
inserting a non-equivariant intermediate layer (e.g., a coordinate-frame
look-up table or a max-over-axis pooling) that breaks the rotation-
equivariance contract.
"""

from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mutations._base import Mutation


def _mut_ii_01(model):
    """Flip on equivariant_break flag (StubModel: switches to mean-axis features)."""
    m = deepcopy(model)
    m.equivariant_break = True
    return m


def _mut_ii_02(model):
    """Insert axis-dependent post-processing: rescale predictions by x[:,0].mean()."""
    m = deepcopy(model)
    base_predict = m.predict

    def predict_with_axis_bias(point_cloud):
        out = base_predict(point_cloud)
        bias = float(np.asarray(point_cloud)[:, 0].mean())
        return out * (1.0 + 0.1 * bias)

    m.predict = predict_with_axis_bias
    return m


def _mut_ii_03(model):
    """Insert frame-dependent class-1 boost when first-axis mean > 0."""
    m = deepcopy(model)
    base_predict = m.predict

    def predict_with_frame_dependence(point_cloud):
        out = np.asarray(base_predict(point_cloud)).copy()
        if float(np.asarray(point_cloud)[:, 0].mean()) > 0:
            out[1] += 0.05
            out = out / out.sum()
        return out

    m.predict = predict_with_frame_dependence
    return m


def _mut_ii_04(model):
    """Hard-coded coordinate-frame asymmetry: scale Z-axis features by 1.5."""
    m = deepcopy(model)
    base_predict = m.predict

    def predict_with_z_asymmetry(point_cloud):
        pc = np.asarray(point_cloud).copy()
        pc[:, 2] *= 1.5  # break Z-axis equivariance
        return base_predict(pc)

    m.predict = predict_with_z_asymmetry
    return m


def _mut_ii_05(model):
    """Argmax-perturbation tied to first-point coordinate sign."""
    m = deepcopy(model)
    base_predict = m.predict

    def predict_with_argmax_perturbation(point_cloud):
        out = np.asarray(base_predict(point_cloud)).copy()
        first_x = float(np.asarray(point_cloud)[0, 0])
        if first_x > 0:
            out[0], out[-1] = out[-1], out[0]  # swap first and last classes
        return out

    m.predict = predict_with_argmax_perturbation
    return m


MUTATIONS_CAT_II = [
    Mutation(
        id="cat_ii_01", category="ii", label="equivariant_flag_off",
        description="enable equivariant_break flag in StubModel",
        apply=_mut_ii_01, sources_p2=False,
    ),
    Mutation(
        id="cat_ii_02", category="ii", label="axis_dependent_postproc",
        description="rescale output by first-axis mean",
        apply=_mut_ii_02, sources_p2=False,
    ),
    Mutation(
        id="cat_ii_03", category="ii", label="frame_dependent_boost",
        description="boost class 1 when x-axis mean > 0",
        apply=_mut_ii_03, sources_p2=False,
    ),
    Mutation(
        id="cat_ii_04", category="ii", label="z_axis_asymmetry",
        description="hard-coded 1.5x Z-axis pre-scaling",
        apply=_mut_ii_04, sources_p2=False,
    ),
    Mutation(
        id="cat_ii_05", category="ii", label="argmax_swap_on_x_sign",
        description="swap first and last class probs when x[0,0]>0",
        apply=_mut_ii_05, sources_p2=False,
    ),
]
