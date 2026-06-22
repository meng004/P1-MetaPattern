"""
NOETHER block: O<= (monotone / linear shape-preservation) -- scipy Akima1DInterpolator.
Fix commit: ef7437afc "BUG: Fix Akima1DInterpolator by returning linear interpolant
            for y.shape[0] == 2 (#22278)" (gh-22278).
Pre  scipy 1.15.x: Akima1DInterpolator on exactly TWO data points builds the slope
            scratch array m = empty(x.size+3) = empty(5), fills only m[2:3] with the
            single divided difference, then computes the "ghost" slopes
            m[1]=2*m[2]-m[3], m[0]=2*m[1]-m[2], m[-2]=2*m[-3]-m[-4], ...  which READ
            uninitialised entries of the np.empty buffer. The breakpoint slope t is
            therefore garbage, so the cubic Hermite spline is NOT the straight line
            through the two points: the interpolant is neither linear nor monotone.
Post scipy 1.16.0: special-cases y.shape[0]==2 -> slope = (y1-y0)/(x1-x0) -> the
            unique LINEAR (hence monotone) interpolant.

MR (O<= shape-preservation block):
    A shape-preserving 1-D interpolant of MONOTONE data must itself be monotone, and
    through exactly two points the unique shape-preserving (linear) interpolant is the
    straight line: I(x) on [x0,x1] equals the chord, so for any query the value lies
    on the line and the sampled sequence is monotone non-decreasing for increasing y.
    Operationally, with two strictly-increasing points (x0,y0),(x1,y1):
        (a) midpoint identity:  I((x0+x1)/2) == (y0+y1)/2          [on the chord]
        (b) monotone + bounded: y0 <= I(t) <= y1 and the sampled sequence over a fine
            grid in [x0,x1] is non-decreasing.
    Source     : the exact two-point linear data (reference = the chord g(x)).
    Follow-up  : Akima1DInterpolator(x, y) evaluated on the same interior grid.
    Violation (FIRED): I deviates from the chord (a) and/or the sampled sequence is
        non-monotone / leaves [y0,y1] (b) -- shape-preservation broken on 2 points.

SUT: two strictly-increasing points; CPU microseconds (pure NumPy, no train/solve).

Reproduce (pip released-to-released):
    uv venv --python 3.11 /tmp/venv_scipy_akima
    # PRE -> FIRED
    VIRTUAL_ENV=/tmp/venv_scipy_akima uv pip install "scipy==1.15.2"
    /tmp/venv_scipy_akima/bin/python results/scipy_repro/repro_akima_linear2pt.py
    # POST -> HELD
    VIRTUAL_ENV=/tmp/venv_scipy_akima uv pip install "scipy==1.16.0"
    /tmp/venv_scipy_akima/bin/python results/scipy_repro/repro_akima_linear2pt.py
"""
import numpy as np
from scipy.interpolate import Akima1DInterpolator
import scipy

print("scipy version:", scipy.__version__)
print("numpy version:", np.__version__)

# Two strictly-increasing points: the unique shape-preserving interpolant is the
# straight line y = y0 + (y1-y0)/(x1-x0) * (x - x0).
x = np.array([0.0, 1.0])
y = np.array([0.0, 2.0])             # monotone increasing
slope = (y[1] - y[0]) / (x[1] - x[0])

def chord(xq):                       # reference: the exact linear interpolant
    return y[0] + slope * (xq - x[0])

TOL = 1e-9

# Build the two-point Akima interpolant. On the PRE version the slope scratch
# array m=empty(x.size+3)=empty(5) is only filled at m[2:3]; the ghost-slope
# formulas read uninitialised np.empty entries -> non-finite breakpoint slope ->
# construction itself raises ("`dydx` must contain only finite values."). That is
# a crash-type violation of the same O<= relation: the shape-preserving (linear)
# two-point interpolant must EXIST and equal the chord. Catch it as FIRED.
try:
    ak = Akima1DInterpolator(x, y)
except Exception as exc:
    print(f"  Akima1DInterpolator(x, y) RAISED on 2 points: "
          f"{type(exc).__name__}: {exc}")
    print("    >>> MR VIOLATED (FIRED): the two-point shape-preserving (linear) "
          "interpolant cannot even be constructed -- uninitialised slope buffer "
          "produced non-finite breakpoint slopes (crash-type).")
    print("VERDICT: FIRED")
    raise SystemExit(0)

# Interior grid strictly between the two breakpoints (no extrapolation).
xq = np.linspace(x[0], x[1], 11)[1:-1]
iq = ak(xq)
ref = chord(xq)
# (a) midpoint identity / agreement with the chord everywhere on [x0,x1]
max_chord_dev = float(np.max(np.abs(iq - ref)))
mid = float(ak(0.5))
mid_ref = 0.5 * (y[0] + y[1])
mid_dev = abs(mid - mid_ref)

# (b) monotone + bounded inside [y0,y1]
finite = bool(np.all(np.isfinite(iq)))
diffs = np.diff(iq)
monotone = bool(np.all(diffs >= -TOL))
in_range = bool(np.all((iq >= y[0] - TOL) & (iq <= y[1] + TOL)))

print(f"  midpoint  I(0.5)            = {mid:.6g}  (chord expects {mid_ref:.6g}, "
      f"dev={mid_dev:.3e})")
print(f"  max|I - chord| on interior  = {max_chord_dev:.3e}")
print(f"  all finite                  = {finite}")
print(f"  monotone non-decreasing     = {monotone}")
print(f"  stays within [y0,y1]        = {in_range}")

fired = (max_chord_dev > TOL) or (mid_dev > TOL) or (not finite) \
        or (not monotone) or (not in_range)

if fired:
    why = []
    if not finite:        why.append("non-finite values (uninitialised m[] read)")
    if mid_dev > TOL:     why.append(f"midpoint off chord by {mid_dev:.2e}")
    if max_chord_dev > TOL: why.append(f"deviates from linear chord by {max_chord_dev:.2e}")
    if not monotone:      why.append("non-monotone over increasing data")
    if not in_range:      why.append("escapes [y0,y1] envelope")
    print("    >>> MR VIOLATED (FIRED): two-point Akima is not the linear/monotone "
          f"interpolant -- {'; '.join(why)}.")
else:
    print("    MR HELD: two-point Akima == linear chord (monotone, bounded, finite).")

print("VERDICT:", "FIRED" if fired else "HELD")
