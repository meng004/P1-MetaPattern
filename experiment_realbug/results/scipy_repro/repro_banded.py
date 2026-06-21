"""
NOETHER block: conservation / L* (scipy.integrate.ode + LSODA, stiff Robertson ODE).
Fix commit: cb0538877 "BUG: Fix banded Jacobian for lsoda: `ode` and `solve_ivp` (#22283)"
            (scipy 1.16.0rc1)

Bug: In scipy.integrate.ode with the 'lsoda' integrator, a user-supplied
     BANDED Jacobian (lband/uband set) was NOT padded with the extra `ml`
     rows that the f2py LSODA wrapper expects (the padding wrapper existed
     for 'vode' but was simply missing from the 'lsoda' class). LSODA then
     read the banded Jacobian from the wrong rows -> wrong stiff solution,
     silently diverging from the full-Jacobian (correct) result.

MR (representation invariance, conservation block):
   The SAME Jacobian expressed in full vs banded storage must give the SAME
   trajectory for a stiff system:
        y_banded(t) == y_full(t)
   SUT: Robertson stiff kinetics embedded with trivial rows to make it banded.
   Source     : full-Jacobian LSODA solve (reference).
   Follow-up  : banded-Jacobian LSODA solve.
   Violation (FIRED): banded trajectory deviates from full trajectory.
"""
import numpy as np
from scipy.integrate import ode
import scipy

print("scipy version:", scipy.__version__)

def stiff_f(t, y):
    return np.array([
        y[0],
        -0.04 * y[1] + 1e4 * y[2] * y[3],
        0.04 * y[1] - 1e4 * y[2] * y[3] - 3e7 * y[2]**2,
        3e7 * y[2]**2,
        y[4],
    ])

def stiff_jac(t, y):           # full (dense) Jacobian
    return np.array([
        [1,     0,                            0,         0, 0],
        [0, -0.04,                     1e4*y[3],  1e4*y[2], 0],
        [0,  0.04, -1e4 * y[3] - 3e7 * 2 * y[2], -1e4*y[2], 0],
        [0,     0,                   3e7*2*y[2],         0, 0],
        [0,     0,                            0,         0, 1],
    ])

def banded_stiff_jac(t, y):    # SAME Jacobian, banded storage (lband=1, uband=2)
    return np.array([
        [0,     0,                    0,  1e4*y[2], 0],
        [0,     0,             1e4*y[3], -1e4*y[2], 0],
        [1, -0.04, -1e4*y[3]-3e7*2*y[2],         0, 1],
        [0,  0.04,           3e7*2*y[2],         0, 0],
    ])

def solve(banded):
    jac = banded_stiff_jac if banded else stiff_jac
    lband, uband = (1, 2) if banded else (None, None)
    r = ode(stiff_f, jac)
    r.set_integrator('lsoda', lband=lband, uband=uband, rtol=1e-9, atol=1e-10)
    y0 = np.array([1.0, 1.0, 0.0, 0.0, 1.0])
    r.set_initial_value(y0, 0.0)
    t, y = [0.0], [y0]
    while r.successful() and r.t < 10:
        r.integrate(r.t + 1.0)
        t.append(r.t); y.append(r.y)
    return np.array(t), np.array(y), r._integrator.iwork[12]  # iwork[12]=#jac evals

t_full, y_full, nj_full = solve(banded=False)
print(f"  full-Jacobian solve OK; #jac evals={nj_full}; y_full[end]={y_full[-1]}")

fired = False
try:
    t_band, y_band, nj_band = solve(banded=True)
    dev = float(np.max(np.abs(y_band - y_full)))
    print(f"  banded-Jacobian solve OK; #jac evals={nj_band}; y_banded[end]={y_band[-1]}")
    print(f"  max |y_banded - y_full| = {dev:.3e}")
    fired = dev > 1e-6
    if fired:
        print(f"    >>> MR VIOLATED (FIRED): banded vs full Jacobian give DIFFERENT "
              f"stiff trajectories (max dev {dev:.3e})")
except Exception as e:
    fired = True
    print(f"  banded-Jacobian solve RAISED: {type(e).__name__}: {e}")
    print(f"    >>> MR VIOLATED (FIRED): banded Jacobian not row-padded for LSODA "
          f"(same Jacobian, banded storage, cannot be used at all)")

print("VERDICT:", "FIRED" if fired else "HELD")
