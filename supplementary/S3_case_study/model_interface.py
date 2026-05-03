"""
Model loader and stub model for §6.6 case study.

Provides:
  - load_model(path) -> ModelLike: load a trained SE(3)-Transformer
    checkpoint
  - StubModel: a non-equivariant CPU-only stand-in usable for end-to-end
    pipeline validation BEFORE the real e3nn checkpoint is available.
    Produces deterministic outputs from a hash of the input.

Stub-mode design notes
----------------------
The stub *intentionally* breaks SE(3) equivariance — it computes outputs
from element-wise statistics rather than from rotational features. This
makes it useful for sanity-checking the runner and for verifying that
rho_rot detects a non-equivariant model (an MR-self-test). When the real
e3nn checkpoint is loaded, rho_rot is expected to *not* detect any fault
on the unmutated baseline.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import numpy as np


class StubModel:
    """A non-equivariant CPU stub that accepts the same interface as a
    real SE(3)-Transformer."""

    NUM_CLASSES = 10  # ModelNet10

    def __init__(self, *, equivariant_break: bool = True, seed: int = 42) -> None:
        self.equivariant_break = equivariant_break
        self.rng = np.random.default_rng(seed)
        self.theta = {
            "head_weight": self.rng.standard_normal((6, self.NUM_CLASSES)),
            "head_bias": np.zeros(self.NUM_CLASSES),
        }

    def predict(self, point_cloud: np.ndarray) -> np.ndarray:
        """Return shape (C,) probabilities."""
        x = np.asarray(point_cloud, dtype=np.float64)
        # Build a 6-dim feature: per-axis mean and per-axis std.
        # Mean is rotation-sensitive (breaks SO(3)) when equivariant_break=True;
        # std is rotation-invariant. The stub blends them.
        if self.equivariant_break:
            features = np.concatenate([x.mean(axis=0), x.std(axis=0)])
        else:
            # An attempt at rotation invariance: only use radial statistics
            radii = np.linalg.norm(x, axis=1)
            features = np.array([
                radii.mean(), radii.std(),
                radii.min(), radii.max(),
                radii.mean() ** 2, radii.std() ** 2,
            ])
        logits = features @ self.theta["head_weight"] + self.theta["head_bias"]
        # Softmax
        e = np.exp(logits - logits.max())
        return e / e.sum()

    def attention_trace(self, x1: np.ndarray, x2: np.ndarray) -> float:
        """Stub bilinear form A(x1, x2) = <Q phi(x1), K phi(x2)>.

        With Q = K = I (so the form is symmetric), and phi(x) = sum-of-points,
        Tr A(x1, x2) reduces to <sum(x1), sum(x2)> which is symmetric. This
        means rho_adj returns holds=True on the unmutated stub.
        """
        s1 = np.asarray(x1).sum(axis=0)
        s2 = np.asarray(x2).sum(axis=0)
        return float(np.dot(s1, s2))

    def sgd_step(self, theta: dict, batch, eta: float) -> dict:
        """One vanilla SGD step on the stub head weights.

        batch: tuple of (point_cloud, label).
        """
        x, y = batch
        probs = self.predict(x)
        target = np.zeros(self.NUM_CLASSES)
        target[int(y)] = 1.0
        grad = (probs - target)[None, :] * np.linalg.norm(x, axis=1).mean()
        new_theta = {
            "head_weight": theta["head_weight"] - eta * grad,
            "head_bias": theta["head_bias"] - eta * (probs - target),
        }
        return new_theta

    @property
    def parameters(self) -> dict:
        return self.theta


# -----------------------------------------------------------------------------
# Loader
# -----------------------------------------------------------------------------

def load_model(checkpoint_path: str | Path | None, *, stub: bool = False) -> Any:
    """Load a model under test.

    Parameters
    ----------
    checkpoint_path: path to a checkpoint produced by
        ``model/train.py`` (saves an EGNN E(3)-equivariant classifier).
        If None or stub=True, returns a StubModel.
    stub: if True, force StubModel even if checkpoint_path is given.
    """
    if stub or checkpoint_path is None:
        return StubModel(equivariant_break=False)  # baseline stub passes rho_rot

    try:
        import torch  # type: ignore[import-not-found]  # noqa: F401
    except ImportError as exc:
        raise RuntimeError(
            "Real model loading requires torch. Either install it (see "
            "../S4_reproducibility/environment.yml) or pass stub=True."
        ) from exc

    # Wire to the EGNN classifier defined in model/equivariant_classifier.py.
    import sys
    model_dir = Path(__file__).resolve().parent / "model"
    sys.path.insert(0, str(model_dir))
    from equivariant_classifier import load_equivariant_classifier  # type: ignore[import-not-found]
    return load_equivariant_classifier(str(checkpoint_path))


def model_fingerprint(model: Any, num_probes: int = 5, seed: int = 0) -> str:
    """Deterministic fingerprint of a model's behaviour, for sanity-checking
    that mutations actually change the model and that re-loaded checkpoints
    are bit-identical."""
    rng = np.random.default_rng(seed)
    parts = []
    for _ in range(num_probes):
        cloud = rng.standard_normal((128, 3))
        out = model.predict(cloud)
        parts.append(np.array(out).tobytes())
    return hashlib.sha256(b"".join(parts)).hexdigest()[:16]
