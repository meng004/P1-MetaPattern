"""
NOETHER block: O<= (monotonicity / linearity preservation) via interpolate.
Fix commit: 9930630d6 (scipy 1.17.0rc1)
Bug: Akima1DInterpolator computes node slopes as
        t[ind] = (f1*m1 + f2*m2) / (f1+f2)
     The product f1*m1 overflows to +inf for large-magnitude data, even though
     the mathematically-equivalent factored form m1 + (f2/(f1+f2))*(m2-m1)
     stays finite. The inf slope then trips scipy's own finiteness guard
     ("`dydx` must contain only finite values") OR yields a non-finite spline.

MR (metamorphic relation, O<= block):
   An interpolator that passes through its data points must produce finite
   outputs at those nodes for finite inputs: isfinite(I(x_i)) for all i.
   Source : finite data y with large dynamic range.
   Follow-up : build interpolant, evaluate at knots.
   Violation (FIRED): construction raises on non-finite derived slopes,
                      or I(x_i) is non-finite.
"""
import numpy as np
from scipy.interpolate import Akima1DInterpolator
import scipy

print("scipy version:", scipy.__version__)

x = np.arange(1, 10)
# large *finite* dynamic range: step from 0 to ~1e6*sqrt(float_max)
y = 1.0e6 * np.sqrt(np.finfo(float).max) * np.heaviside(x - 4, 0.5)
assert np.isfinite(y).all(), "source data must be finite"

fired = False
for method in ("akima", "makima"):
    try:
        ak = Akima1DInterpolator(x, y, method=method)
        yi = ak(x)            # evaluate AT the knots -> interpolation property
        finite = bool(np.isfinite(yi).all())
        print(f"  method={method:7s}  isfinite(I(x_i)) = {finite}   "
              f"max|I| = {np.nanmax(np.abs(yi)):.3e}")
        if not finite:
            fired = True
            print(f"    >>> MR VIOLATED (FIRED): non-finite interpolant: {yi}")
    except Exception as e:
        fired = True
        print(f"  method={method:7s}  CONSTRUCTION FAILED on finite data: "
              f"{type(e).__name__}: {e}")
        print(f"    >>> MR VIOLATED (FIRED): overflow -> non-finite slopes")

print("VERDICT:", "FIRED" if fired else "HELD")
