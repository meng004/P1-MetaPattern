"""20 mutations for the §6.6 case study, in 4 categories of 5 each.

Each mutation is a callable that wraps a baseline model and returns a
mutated model exposing the same ModelLike interface. This monkey-patch
pattern avoids editing the trained checkpoint on disk.
"""

from .cat_i_wrong_sign_loss import MUTATIONS_CAT_I
from .cat_ii_equivariance_break import MUTATIONS_CAT_II
from .cat_iii_precision import MUTATIONS_CAT_III
from .cat_iv_gradient_reversal import MUTATIONS_CAT_IV
from .cat_v_deepcrime import MUTATIONS_CAT_V

ALL_MUTATIONS = [
    *MUTATIONS_CAT_I,
    *MUTATIONS_CAT_II,
    *MUTATIONS_CAT_III,
    *MUTATIONS_CAT_IV,
]

assert len(ALL_MUTATIONS) == 20, f"expected 20 mutations, got {len(ALL_MUTATIONS)}"

DEEPCRIME_PILOT_MUTATIONS = list(MUTATIONS_CAT_V)
assert len(DEEPCRIME_PILOT_MUTATIONS) == 5, (
    f"expected 5 DeepCrime-style pilot mutations, got {len(DEEPCRIME_PILOT_MUTATIONS)}"
)
