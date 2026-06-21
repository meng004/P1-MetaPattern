"""
NOETHER block: L* convergence (solve_ivp LSODA dense-output / event self-consistency).
Fix commit: c374ca7fd "BUG: Fix LSODA interpolation scheme (#14552)"  (scipy 1.12.0rc1)

Bug: With method='LSODA' + dense_output=True, after an internal ORDER change the
     local continuous interpolant used the WRONG Nordsieck-history segment
     (order read from iwork[14]=next-order rather than iwork[13]=last-used-order).
     The bad interpolant (a) makes res.sol(res.t) disagree with res.y, and
     (b) breaks event root-finding because the local interpolant no longer
     matches the solver state, so brentq sees no sign change.

This is the EXACT upstream regression scenario (#14552).

MR (L* block):
   For a correct dense interpolant, the event y(t)=2.02e-5 (which the true
   solution crosses inside the span) must be located, integration must succeed,
   and res.sol(res.t) == res.y to machine precision.
   Violation (FIRED): integration raises (event root-finder fails on the bad
   interpolant) OR res.sol(res.t) deviates from res.y by >> 1e-12.
"""
import numpy as np
from scipy.integrate import solve_ivp
import scipy

print("scipy version:", scipy.__version__)

def fun(t, y):
    return y * (t - 2)
def jac(t, y):
    return t - 2
def exact(t):
    return np.exp(t ** 2 / 2 - 2 * t + np.log(0.05) - 6)
def event_lsoda(t, y):
    return y[0] - 2.02e-5

rtol, atol = 1e-3, 1e-6
y0, t_span, first_step = [0.05], [-2, 2], 1e-3

fired = False
try:
    res = solve_ivp(fun, t_span, y0, method="LSODA", dense_output=True,
                    events=event_lsoda, first_step=first_step, max_step=1,
                    rtol=rtol, atol=atol, jac=jac)
    if not res.success:
        fired = True
        print(f"  integration FAILED: status={res.status} msg={res.message}")
        print(f"    >>> MR VIOLATED (FIRED)")
    else:
        interp = res.sol(res.t)
        denom = np.maximum(np.abs(res.y), 1e-300)
        max_rel = float(np.max(np.abs(interp - res.y) / denom))
        n_events = res.t_events[0].size
        print(f"  success; grid={res.t.size}; events found={n_events}")
        print(f"  max relative |sol(t)-y|/|y| = {max_rel:.3e}")
        fired = max_rel > 1e-12
        if fired:
            print(f"    >>> MR VIOLATED (FIRED): dense interpolant deviates "
                  f"(max rel {max_rel:.3e})")
except Exception as e:
    fired = True
    print(f"  integration RAISED on the upstream scenario: {type(e).__name__}: {e}")
    print(f"    >>> MR VIOLATED (FIRED): bad LSODA interpolant breaks event "
          f"root-finding (interpolant inconsistent with solver state)")

print("VERDICT:", "FIRED" if fired else "HELD")
