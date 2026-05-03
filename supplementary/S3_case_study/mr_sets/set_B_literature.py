"""
Set B: five MRs synthesised from prior MT-for-ML literature, restricted
to MRs applicable to point-cloud classifiers.

Source citations follow the manuscript's bibliography keys:
  Murphy2008  — Murphy et al., "Properties of Machine Learning Applications
                for Use in Metamorphic Testing", SEKE 2008.
  Xie2011     — Xie et al., "Testing and Validating Machine Learning
                Classifiers by Metamorphic Testing", JSS 2011.
  Segura2016  — Segura et al., "A Survey on Metamorphic Testing", TSE 2016.
  Shin2024    — Shin et al., "Metamorphic Testing of Machine Learning
                Classifiers", ICSE 2024 (industrial study with Siemens).

Each entry below cites the specific MR pattern from one of these works,
adapted to the point-cloud signature.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mr_interface import MR, MRResult


TAU = 1e-3


# -----------------------------------------------------------------------------
# B1 — Murphy2008 §3.1 "Permutative" MR: reorder input attributes
# -----------------------------------------------------------------------------

def _b1_attribute_permute_fn(model, point_cloud, *, seed: int = 200) -> MRResult:
    """Permute the input feature ordering (here: per-point coordinate axes).

    Adapted from Murphy2008's "Permutative" MR. Note that for an
    SE(3)-equivariant classifier this MR is genuinely failing-by-design
    (axis permutation is not in SO(3)), unlike point-permutation in N.
    """
    rng = np.random.default_rng(seed)
    pc = np.asarray(point_cloud)
    perm = rng.permutation(3)
    p_orig = np.asarray(model.predict(pc))
    p_perm = np.asarray(model.predict(pc[:, perm]))
    dev = float(np.max(np.abs(p_orig - p_perm)))
    # Murphy's formulation uses "<= tolerance"; an honest baseline reports
    # this even when the model is correctly *not* invariant under axis
    # permutation. The MR is part of the literature corpus and we report
    # it faithfully.
    return MRResult(holds=(dev <= TAU), deviation=dev,
                    notes="B_attr_perm [Murphy2008 §3.1]")


# -----------------------------------------------------------------------------
# B2 — Murphy2008 §3.2 "Multiplicative" MR: scale all inputs
# -----------------------------------------------------------------------------

def _b2_multiplicative_fn(model, point_cloud, *, alpha: float = 2.0) -> MRResult:
    """Multiplicative MR adapted to point clouds: scale each coordinate."""
    pc = np.asarray(point_cloud)
    p_orig = np.asarray(model.predict(pc))
    p_scaled = np.asarray(model.predict(alpha * pc))
    dev = float(np.max(np.abs(p_orig - p_scaled)))
    return MRResult(holds=(dev <= 0.05), deviation=dev,
                    notes="B_mult [Murphy2008 §3.2]")


# -----------------------------------------------------------------------------
# B3 — Xie2011 MR-1 (additive): shift all inputs by a constant
# -----------------------------------------------------------------------------

def _b3_additive_fn(model, point_cloud, *, c: float = 0.1) -> MRResult:
    """Additive MR: shift all coordinates by constant c.

    For an SE(3)-equivariant *classifier* (translation by c is in the
    Euclidean group SE(3) but not in SO(3)), the prediction may or may
    not be invariant depending on whether the classifier embeds inputs
    via centred coordinates. We report the literature MR verbatim.
    """
    pc = np.asarray(point_cloud)
    p_orig = np.asarray(model.predict(pc))
    p_shift = np.asarray(model.predict(pc + c))
    dev = float(np.max(np.abs(p_orig - p_shift)))
    return MRResult(holds=(dev <= 0.05), deviation=dev,
                    notes="B_add [Xie2011 MR-1]")


# -----------------------------------------------------------------------------
# B4 — Segura2016 generic-classifier MR: removing one redundant point
# -----------------------------------------------------------------------------

def _b4_subset_fn(model, point_cloud, *, drop_count: int = 1, seed: int = 201) -> MRResult:
    """Subsetting MR: drop a randomly chosen single point and check the
    prediction is approximately preserved (the classifier should be
    robust to small subsetting on dense clouds).
    """
    rng = np.random.default_rng(seed)
    pc = np.asarray(point_cloud)
    if pc.shape[0] <= drop_count:
        return MRResult(holds=None, deviation=0.0, notes="point cloud too small")
    keep_idx = rng.choice(pc.shape[0], size=pc.shape[0] - drop_count, replace=False)
    pc_sub = pc[keep_idx]
    p_orig = np.asarray(model.predict(pc))
    p_sub = np.asarray(model.predict(pc_sub))
    dev = float(np.max(np.abs(p_orig - p_sub)))
    return MRResult(holds=(dev <= 0.05), deviation=dev,
                    notes=f"B_subset [Segura2016 generic; drop_count={drop_count}]")


# -----------------------------------------------------------------------------
# B5 — Shin2024 industrial MR: same input → same output (idempotency)
# -----------------------------------------------------------------------------

def _b5_idempotent_fn(model, point_cloud, **_) -> MRResult:
    """Determinism MR: invoking the classifier twice on the same input
    must produce identical output."""
    p1 = np.asarray(model.predict(point_cloud))
    p2 = np.asarray(model.predict(point_cloud))
    dev = float(np.max(np.abs(p1 - p2)))
    return MRResult(holds=(dev <= TAU), deviation=dev,
                    notes="B_idempot [Shin2024 §IV]")


# -----------------------------------------------------------------------------
# Set B registry
# -----------------------------------------------------------------------------

SET_B: list[MR] = [
    MR(name="B_attr_perm", block="(out)", set_label="B", fn=_b1_attribute_permute_fn),
    MR(name="B_mult",      block="(out)", set_label="B", fn=_b2_multiplicative_fn),
    MR(name="B_add",       block="(out)", set_label="B", fn=_b3_additive_fn),
    MR(name="B_subset",    block="(out)", set_label="B", fn=_b4_subset_fn),
    MR(name="B_idempot",   block="L*",    set_label="B", fn=_b5_idempotent_fn),
]


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from model_interface import StubModel  # type: ignore[import-not-found]
    model = StubModel(equivariant_break=False)
    rng = np.random.default_rng(42)
    pc = rng.standard_normal((128, 3))
    print("Set B on baseline stub:")
    for mr in SET_B:
        r = mr.evaluate(model, pc)
        print(f"  {mr.name:14s} block={mr.block:6s} holds={r.holds!s:6s} dev={r.deviation:.3e}")
