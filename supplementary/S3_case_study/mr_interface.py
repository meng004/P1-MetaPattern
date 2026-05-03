"""
MR interface for the §6.6 case study.

A metamorphic relation here is a callable that takes a model and an input,
runs whatever transformation/comparison the MR encodes, and returns:

  - True  iff the MR holds (no fault detected)
  - False iff the MR is violated (fault detected)
  - None  iff the MR is not applicable (e.g. a training-time MR on an
            inference-only mutation; counted as non-detection, not as failure)

Each MR also exposes a `block` attribute (one of the seven NOETHER blocks)
and a `name` attribute used in result reporting.

Three MR sets (N, L, B) all conform to this interface so that runner.py
can iterate uniformly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional, Protocol


class ModelLike(Protocol):
    """Minimum contract a model must satisfy to be testable by these MRs."""

    def predict(self, point_cloud):
        """point_cloud: numpy array of shape (n, 3); returns probability
        vector of shape (C,) summing to 1."""
        ...

    def attention_trace(self, x1, x2) -> float:
        """For models exposing a Hermitian attention layer; raises
        NotImplementedError otherwise."""
        ...

    def sgd_step(self, theta, batch, eta: float):
        """One SGD update: returns theta_next. Required only for
        training-time MRs (rho_train-rev)."""
        ...


@dataclass(frozen=True)
class MRResult:
    """Outcome of evaluating one MR on one input."""
    holds: Optional[bool]   # True / False / None (not-applicable)
    deviation: float        # numerical violation magnitude; 0 if holds=True
    notes: str = ""         # optional debugging information


@dataclass
class MR:
    """A metamorphic relation."""
    name: str
    block: str              # one of NOETHER blocks: G / O_le / T* / T_rev* / L*
    set_label: str          # "N" (NOETHER) / "L" (LLM) / "B" (literature)
    fn: Callable[[ModelLike, Any], MRResult]

    def evaluate(self, model: ModelLike, x: Any) -> MRResult:
        return self.fn(model, x)


# A "point cloud input" is a numpy ndarray of shape (n, 3). We keep the
# parameter type as Any in the dataclass above to avoid a hard numpy
# dependency in this contract module.
