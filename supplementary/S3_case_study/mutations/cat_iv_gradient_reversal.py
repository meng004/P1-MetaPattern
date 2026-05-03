"""
Category (iv) — Gradient-reversal sign error (5 mutations).

These mutations specifically target the training trajectory's reversal
property — the MR rho_train_rev (§6.5) is the unique-detection prediction
of H2 (§6.6). They CANNOT be borrowed from P2 because P2's PUTs have no
SGD training loop in the testable scope.

Each mutation patches the model's sgd_step method so that the inverse
update (called with eta < 0) does not actually invert the forward step.
The five flavours cover progressively more subtle errors.
"""

from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mutations._base import Mutation


def _mut_iv_01(model):
    """Inverse update uses |eta| instead of -eta (sign error in inverse step)."""
    m = deepcopy(model)
    base_sgd = m.sgd_step

    def sgd_step_with_sign_bug(theta, batch, eta):
        # BUG: use abs(eta) so reverse direction never actually reverses
        return base_sgd(theta, batch, eta=abs(eta))

    m.sgd_step = sgd_step_with_sign_bug
    return m


def _mut_iv_02(model):
    """Inverse step uses 0.5 * eta instead of -eta (magnitude error)."""
    m = deepcopy(model)
    base_sgd = m.sgd_step

    def sgd_step_half_inverse(theta, batch, eta):
        if eta < 0:
            return base_sgd(theta, batch, eta=0.5 * eta)
        return base_sgd(theta, batch, eta=eta)

    m.sgd_step = sgd_step_half_inverse
    return m


def _mut_iv_03(model):
    """Inverse step swaps head-weight and head-bias gradients (entangled bug)."""
    from mutations._base import head_weight_key, head_bias_key

    m = deepcopy(model)
    base_sgd = m.sgd_step

    def sgd_step_swapped_grad(theta, batch, eta):
        result = base_sgd(theta, batch, eta=eta)
        if eta < 0:
            wk = head_weight_key(result)
            bk = head_bias_key(result)
            # BUG: on inverse, swap which tensor receives which gradient
            tmp = result[wk].copy()
            result[wk] = theta[wk]
            # Mean over the larger axis to match shape of bias
            mean_axis = tmp.mean(axis=tuple(i for i in range(tmp.ndim) if tmp.shape[i] != result[bk].shape[0]))
            result[bk] = result[bk] - 0.01 * mean_axis
        return result

    m.sgd_step = sgd_step_swapped_grad
    return m


def _mut_iv_04(model):
    """No-op on inverse: forward step works, inverse silently does nothing."""
    m = deepcopy(model)
    base_sgd = m.sgd_step

    def sgd_step_silent_noop(theta, batch, eta):
        if eta < 0:
            # BUG: silently no-op on inverse direction
            return {k: v.copy() for k, v in theta.items()}
        return base_sgd(theta, batch, eta=eta)

    m.sgd_step = sgd_step_silent_noop
    return m


def _mut_iv_05(model):
    """Inverse uses gradient of NEXT batch instead of current (lookahead error)."""
    m = deepcopy(model)
    base_sgd = m.sgd_step
    state: dict = {"prev_batch": None}

    def sgd_step_lookahead(theta, batch, eta):
        if eta < 0 and state["prev_batch"] is not None:
            # BUG: use prev batch on inverse step, not current
            result = base_sgd(theta, state["prev_batch"], eta=eta)
        else:
            result = base_sgd(theta, batch, eta=eta)
        state["prev_batch"] = batch
        return result

    m.sgd_step = sgd_step_lookahead
    return m


MUTATIONS_CAT_IV = [
    Mutation(
        id="cat_iv_01", category="iv", label="abs_eta_inverse",
        description="reverse SGD step uses |eta| instead of -eta",
        apply=_mut_iv_01, sources_p2=False,
    ),
    Mutation(
        id="cat_iv_02", category="iv", label="half_magnitude_inverse",
        description="reverse step uses 0.5*eta",
        apply=_mut_iv_02, sources_p2=False,
    ),
    Mutation(
        id="cat_iv_03", category="iv", label="swapped_grad_inverse",
        description="reverse step swaps weight/bias gradients",
        apply=_mut_iv_03, sources_p2=False,
    ),
    Mutation(
        id="cat_iv_04", category="iv", label="silent_inverse_noop",
        description="reverse step silently does nothing",
        apply=_mut_iv_04, sources_p2=False,
    ),
    Mutation(
        id="cat_iv_05", category="iv", label="lookahead_inverse",
        description="reverse uses previous batch instead of current",
        apply=_mut_iv_05, sources_p2=False,
    ),
]
