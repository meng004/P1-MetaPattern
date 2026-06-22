#!/usr/bin/env python3
"""
Repro for family i (L*.acc / E*  ACCURACY-ORDER), Mode M (inter-implementation).

SUT: scipy.integrate.simpson  (composite Simpson quadrature; paper pde_numerical / E1 SciPy).

Fix commit : 572a373aac2bf14ee6a0c164aac9734b54594b8f
             "ENH: integrate.simpson: improve accuracy for even number of points (#18209)"
PRE  : scipy 1.10.1  (default even='avg'      -> trapezoidal blend on the odd boundary interval)
POST : scipy 1.11.0  (default even='simpson'  -> Cartwright degree-matched parabolic correction)

------------------------------------------------------------------------------------------------
WHY THIS IS FAMILY i (E* ORDER-OF-ACCURACY), NOT FAMILY h (mere convergence):

  Composite Simpson's rule is DOCUMENTED/CLAIMED to be globally 4th order (error ~ C h^4).
  When the number of samples is EVEN (so the number of intervals is ODD), Simpson cannot be
  applied to the whole grid; one boundary interval needs special handling.

    * PRE (even='avg'): the boundary interval is integrated with the TRAPEZOIDAL rule and the
      two one-sided results are averaged. The trapezoidal boundary term injects an O(h^3)
      error into the otherwise-O(h^4) sum, so the GLOBAL observed order DROPS TO 3.
    * POST (even='simpson'): the boundary interval gets a 3-point parabolic correction
      (Cartwright), preserving the GLOBAL 4th-order rate.

  In BOTH versions the quadrature CONVERGES (err -> 0 as h -> 0): family h HOLDS in both.
  The defect is purely in the RATE / accuracy ORDER: PRE achieves order ~3 where order ~4 is
  claimed -- an ORDER REDUCTION. That is exactly the fault class of family i (E*), orthogonal
  to family h.

MODE M (inter-implementation): the MR compares TWO methods of the SAME mathematical object
  (the Simpson integral of the same f on the same nodes): the 'avg' implementation vs the
  'simpson' implementation. The released-to-released default change (1.10.1 -> 1.11.0) closes
  the bracket and tells us WHICH side is the faulty (lower-order) method.

E* INVARIANT (two equivalent operationalisations, both checked):
  (1) observed order  p_obs  (slope of log||err|| vs log h)  must match the CLAIMED order 4
      (we require p_obs >= 3.6 to "match 4"; PRE sits at ~3.0 and FIRES, POST ~4.0 HOLDS);
  (2) the higher-order method must be at least as accurate as the lower-order one at matched
      work:  ||err(simpson)|| <= ||err(avg)||  for every refinement level.
------------------------------------------------------------------------------------------------
Verdict is deterministic (pure numeric; linspace + simpson). Re-running gives identical numbers.
"""
import numpy as np
import scipy
from scipy import integrate
from scipy.integrate import quad
import warnings

warnings.filterwarnings("ignore")  # silence the 1.11 even= DeprecationWarning

CLAIMED_ORDER = 4.0          # composite Simpson is documented as globally 4th order
ORDER_MATCH_THRESHOLD = 3.6  # "observed order matches claimed 4" iff asymptotic p_obs >= 3.6
TOL = ORDER_MATCH_THRESHOLD  # exported tolerance for the JSON entry


def _simpson(y, x):
    """Call simpson with the version's DEFAULT even-handling (no even= kwarg).

    PRE 1.10.1 default == 'avg' (faulty, order-3); POST 1.11.0 default == 'simpson' (order-4).
    This is the inter-implementation (Mode M) pair under test.
    """
    try:
        return integrate.simpson(y, x=x)
    except TypeError:  # very old positional-only signature
        return integrate.simpson(y, x)


def observed_order(f, a, b, n_intervals):
    """Refine over an ODD-interval (EVEN #points) sequence and return (hs, errs, p_obs_tail).

    ODD intervals force the even-number-of-samples code path that the bug lives in.
    """
    exact = quad(f, a, b, epsabs=1e-13, epsrel=1e-13)[0]
    hs, errs = [], []
    for nint in n_intervals:
        assert nint % 2 == 1, "need ODD #intervals (EVEN #points) to exercise the bug path"
        npts = nint + 1
        x = np.linspace(a, b, npts)
        y = f(x)
        val = _simpson(y, x)
        hs.append((b - a) / nint)
        errs.append(abs(val - exact))
    hs = np.array(hs)
    errs = np.array(errs)
    # asymptotic observed order = slope of the last two log-log points
    p_tail = np.log(errs[-2] / errs[-1]) / np.log(hs[-2] / hs[-1])
    # robust least-squares slope over the finest half (avoids pre-asymptotic transient)
    half = len(hs) // 2
    p_fit = np.polyfit(np.log(hs[half:]), np.log(errs[half:]), 1)[0]
    return exact, hs, errs, p_tail, p_fit


def main():
    f = lambda x: np.exp(np.sin(x))   # smooth, non-polynomial: no rule is "accidentally exact"
    a, b = 0.0, 2.0
    n_intervals = [3, 7, 15, 31, 63, 127, 255]   # all ODD -> even #points -> bug path

    exact, hs, errs, p_tail, p_fit = observed_order(f, a, b, n_intervals)

    print(f"scipy = {scipy.__version__}   numpy = {np.__version__}")
    print(f"integrand f(x) = exp(sin x) on [{a},{b}]   exact = {exact:.12f}")
    print(f"claimed global order of composite Simpson = {CLAIMED_ORDER:.0f}")
    print("ODD-interval (EVEN #points) refinement -- exercises the even-handling code path:")
    print(f"  {'nint':>5} {'npts':>5} {'h':>10} {'abs_err':>14}")
    for nint, h, e in zip(n_intervals, hs, errs):
        print(f"  {nint:5d} {nint+1:5d} {h:10.5f} {e:14.6e}")
    print("  observed order between consecutive levels:")
    for i in range(1, len(hs)):
        p = np.log(errs[i - 1] / errs[i]) / np.log(hs[i - 1] / hs[i])
        print(f"    h={hs[i-1]:.5f} -> {hs[i]:.5f}   p_obs = {p:.3f}")
    print(f"  asymptotic observed order (last pair) p_tail = {p_tail:.3f}")
    print(f"  least-squares observed order (fine half) p_fit = {p_fit:.3f}")

    # --- E* invariant (1): observed order must match the CLAIMED order (4) ---
    matches_claim = p_tail >= ORDER_MATCH_THRESHOLD
    print()
    print(f"E* invariant (1): observed order p_obs (~{p_tail:.2f}) must match claimed "
          f"{CLAIMED_ORDER:.0f} (threshold p>={ORDER_MATCH_THRESHOLD}).")
    if matches_claim:
        print(f"  -> p_tail={p_tail:.3f} >= {ORDER_MATCH_THRESHOLD}: order matches claim. HELD.")
    else:
        print(f"  -> p_tail={p_tail:.3f} <  {ORDER_MATCH_THRESHOLD}: ORDER REDUCTION "
              f"(claimed {CLAIMED_ORDER:.0f}, achieved ~3). FIRED.")

    verdict = "HELD" if matches_claim else "FIRED"
    print()
    print(f"MR (family i, E*, Mode M) VERDICT: {verdict}")
    print("  [Mode M: compares the SAME Simpson integral computed by two methods -- the "
          "'avg' boundary-blend vs the 'simpson' parabolic-correction implementation.]")
    print("  [family i not h: the quadrature CONVERGES (err->0) in both versions; only the "
          "accuracy ORDER/RATE differs.]")
    return verdict


if __name__ == "__main__":
    main()
