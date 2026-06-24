"""
NEGATIVE-result supporting evidence for NOETHER family g (O<=.dyn = D*, dynamic
shape / overshoot / spurious extrema).

Claim under test: the scipy PCHIP slope-formula fixes that look like the cleanest
"shape" candidates -- b127884e7 "make PCHIP slopes agree with the literature"
(#5351, first released in v0.17.0) and 2e60b7c8e "change the prescription for PCHIP
endslopes" (#3453, v0.17.0) -- are NOT dynamic-shape (D*) bugs. They change the
*accuracy* of the slopes (to match MATLAB / NAG / Fritsch-Carlson), but the PCHIP
construction is monotonicity-preserving *by design* (harmonic-mean of same-signed
secant slopes => the interpolant cannot overshoot monotone data regardless of the
m[i+1] vs m[i-1] pairing or of the endpoint recipe). Hence the family-g invariant
Z(Phi x) <= Z(x) (no spurious extrema / no overshoot beyond [min,max]) is HELD by
*both* the pre-fix and the post-fix slope formulas. There is no FIRED witness, so
these commits cannot fill the g cell.

This script reconstructs BOTH the pre-fix and post-fix interior + endpoint slope
formulas (verbatim from the two diffs) in pure NumPy, builds the resulting cubic
Hermite interpolant with the modern, *unrelated* CubicHermiteSpline, and measures
the g invariants on several MONOTONE datasets:
    - non_monotone_steps : count of sampled steps with negative increment
    - overshoot          : amount the interpolant leaves [min(y), max(y)]
    - sign_changes       : interior local-extrema count (= 0 for monotone data)
A genuine D* (family g) bug would show non_monotone_steps>0 OR overshoot>0 on at
least one monotone dataset for the PRE formula. The output shows it does NOT: PRE
and POST both keep the interpolant monotone and within range. That is the empirical
core of NEGATIVE_scipy_dstar.md.

Run (no pip pin needed -- only the modern CubicHermiteSpline primitive is used):
    uv venv --python 3.11 /tmp/venv_g
    VIRTUAL_ENV=/tmp/venv_g uv pip install scipy numpy
    /tmp/venv_g/bin/python results/scipy_repro/repro_pchip_slope_no_shape_break.py
"""
import numpy as np
from scipy.interpolate import CubicHermiteSpline
import scipy

print("scipy version:", scipy.__version__)
print("numpy version:", np.__version__)
print()


def pchip_interior_slopes(x, y, formula):
    """Interior PCHIP slopes. 'PRE' = pre-b127884e7 pairing, 'POST' = literature."""
    hk = x[1:] - x[:-1]
    mk = (y[1:] - y[:-1]) / hk
    smk = np.sign(mk)
    condition = (smk[1:] != smk[:-1]) | (mk[1:] == 0) | (mk[:-1] == 0)
    w1 = 2 * hk[1:] + hk[:-1]
    w2 = hk[1:] + 2 * hk[:-1]
    with np.errstate(divide="ignore", invalid="ignore"):
        if formula == "PRE":   # buggy pairing: w1/mk[1:] + w2/mk[:-1]
            whmean = 1.0 / (w1 + w2) * (w1 / mk[1:] + w2 / mk[:-1])
        else:                  # literature: w1/mk[:-1] + w2/mk[1:]
            whmean = (w1 / mk[:-1] + w2 / mk[1:]) / (w1 + w2)
    dk = np.zeros_like(y)
    dk[1:-1][condition] = 0.0
    dk[1:-1][~condition] = 1.0 / whmean[~condition]
    return dk, hk, mk


def edge_PRE(m0, d1):
    """Pre-2e60b7c8e endpoint: out = 1/(1/m0 + 1/d1) where d1!=0 & m0!=0, else 0."""
    m0 = np.atleast_1d(float(m0)); d1 = np.atleast_1d(float(d1))
    out = np.zeros_like(m0)
    mask = (d1 != 0) & (m0 != 0)
    out[mask] = 1.0 / (1.0 / m0[mask] + 1.0 / d1[mask])
    return out[0]


def edge_POST(h0, h1, m0, m1):
    """Post-2e60b7c8e endpoint: Moler 3-point estimate with shape clamps."""
    d = ((2 * h0 + h1) * m0 - h0 * m1) / (h0 + h1)
    d = np.atleast_1d(float(d)); m0a = np.atleast_1d(float(m0)); m1a = np.atleast_1d(float(m1))
    mask = np.sign(d) != np.sign(m0a)
    mask2 = (np.sign(m0a) != np.sign(m1a)) & (np.abs(d) > 3.0 * np.abs(m0a))
    mmm = (~mask) & mask2
    d[mask] = 0.0
    d[mmm] = 3.0 * m0a[mmm]
    return d[0]


def shape_metrics(x, y, dk):
    sp = CubicHermiteSpline(x, y, dk)
    xx = np.linspace(x[0], x[-1], 8001)
    yy = sp(xx)
    d = np.diff(yy)
    nonmono = int(np.sum(d < -1e-12))
    overshoot = float(max(0.0, yy.max() - y.max()) + max(0.0, y.min() - yy.min()))
    # Genuine interior local extrema = sign of the derivative flips between strictly
    # positive and strictly negative (a peak or a valley). Flat (~0) stretches in the
    # data -- e.g. the plateaus of step_up -- are NOT extrema, so drop near-zero
    # derivatives before counting flips. For monotone data the count must be 0.
    s = np.sign(d)
    s = s[np.abs(d) > 1e-12]            # ignore flat regions (derivative ~ 0)
    extrema = int(np.sum(np.abs(np.diff(s)) == 2)) if s.size else 0
    return nonmono, overshoot, extrema, float(yy.min()), float(yy.max())


datasets = {
    "convex_mono":  (np.array([0., 1., 2., 3., 4.]),       np.array([0., 0.1, 0.3, 2.0, 9.0])),
    "concave_mono": (np.array([0., 1., 2., 3., 4.]),       np.array([0., 7.0, 8.5, 8.9, 9.0])),
    "step_up":      (np.array([0., 1., 2., 3., 4., 5.]),   np.array([0., 0., 0., 1., 1., 1.])),
    "NAG_sigmoid":  (np.array([7.99, 8.09, 8.19, 8.70, 9.20, 10.0, 12.0, 15.0, 20.0]),
                     np.array([0., 0.27643e-4, 0.43750e-1, 0.16918, 0.46943, 0.94374, 0.99864, 0.99992, 0.99999])),
    "sharp_first":  (np.array([0., 1., 2., 3., 4.]),       np.array([0., 5.0, 5.1, 5.2, 5.3])),
}

any_fired = False
for name, (x, y) in datasets.items():
    print(f"[{name}] monotone increasing data")
    for tag in ("PRE", "POST"):
        dk, hk, mk = pchip_interior_slopes(x, y, tag)
        dk = dk.copy()
        if tag == "PRE":
            dk[0] = edge_PRE(mk[0], dk[1]); dk[-1] = edge_PRE(mk[-1], dk[-2])
        else:
            dk[0] = edge_POST(hk[0], hk[1], mk[0], mk[1]); dk[-1] = edge_POST(hk[-1], hk[-2], mk[-1], mk[-2])
        nm, ov, ex, mn, mx = shape_metrics(x, y, dk)
        violated = (nm > 0) or (ov > 1e-9) or (ex > 0)
        any_fired = any_fired or violated
        flag = "  <== D* VIOLATED (would be family g)" if violated else "  (shape held)"
        print(f"   {tag:4s}: non_monotone_steps={nm}  overshoot={ov:.3e}  "
              f"local_extrema={ex}  range=[{mn:.4f},{mx:.4f}]{flag}")
    print()

print("=" * 72)
if any_fired:
    print("RESULT: at least one PRE formula VIOLATES the D* invariant -> NOT a negative.")
else:
    print("RESULT: NO D* violation on any monotone dataset for PRE or POST formulas.")
    print("        PCHIP is monotone-by-construction; the slope/endslope fixes change")
    print("        ACCURACY, not SHAPE. These commits cannot witness family g (O<=.dyn).")
    print("VERDICT: NEGATIVE (consistent with NEGATIVE_scipy_dstar.md).")
