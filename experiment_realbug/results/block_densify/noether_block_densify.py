"""
Block densification (controlled-mutant path) on REAL scipy.integrate solvers.
Two NOETHER blocks whose in-the-wild scipy bugs are scarce, derived a priori from
the equation algebra and shown detectable via injected mutants:

  (A) heat u_t = a u_xx, no source -> MAXIMUM PRINCIPLE (O<=):  max_x u(t) <= max_x u(0).
      Prior: parabolic maximum principle. Mutant: inject a positive source s>0
      (violates the no-source maximum principle -> max grows).

  (B) wave u_tt = c^2 u_xx, undamped -> TIME REVERSAL (Trev*): integrate forward to T,
      flip velocity, integrate again -> returns to initial state.
      Prior: the wave operator is time-reversal symmetric. Mutant: inject damping
      (dissipation breaks reversibility -> does not return).

SUT = scipy.integrate.solve_ivp (real library); mutant = controlled injection.
"""
import numpy as np
from scipy.integrate import solve_ivp


def heat_max_principle(mutant=False):
    N, L, a, T = 80, 1.0, 0.02, 0.4
    dx = L / (N - 1)
    x = np.linspace(0, L, N)
    u0 = np.sin(np.pi * x) + 0.4 * np.sin(3 * np.pi * x)
    u0[0] = u0[-1] = 0.0
    src = 3.0 if mutant else 0.0  # mutant: positive source violates no-source max-principle

    def rhs(t, u):
        d2 = np.zeros_like(u)
        d2[1:-1] = (u[2:] - 2 * u[1:-1] + u[:-2]) / dx**2
        du = a * d2 + src * np.sin(np.pi * x)
        du[0] = du[-1] = 0.0
        return du

    sol = solve_ivp(rhs, [0, T], u0, t_eval=np.linspace(0, T, 25), method="RK45",
                    rtol=1e-8, atol=1e-10)
    max0 = float(u0.max())
    maxt = float(sol.y.max())
    violation = maxt - max0
    fired = violation > 1e-4
    return max0, maxt, fired


def wave_time_reversal(mutant=False):
    N, L, c, T = 80, 1.0, 1.0, 0.6
    dx = L / (N - 1)
    x = np.linspace(0, L, N)
    u0 = np.sin(np.pi * x)
    v0 = np.zeros(N)
    damp = 0.8 if mutant else 0.0  # mutant: damping breaks time-reversal symmetry

    def rhs(t, y):
        u, v = y[:N], y[N:]
        d2 = np.zeros(N)
        d2[1:-1] = (u[2:] - 2 * u[1:-1] + u[:-2]) / dx**2
        du = v.copy()
        dv = c**2 * d2 - damp * v
        du[0] = du[-1] = 0.0
        dv[0] = dv[-1] = 0.0
        return np.concatenate([du, dv])

    fwd = solve_ivp(rhs, [0, T], np.concatenate([u0, v0]), method="RK45",
                    rtol=1e-9, atol=1e-11)
    yT = fwd.y[:, -1]
    uT, vT = yT[:N], yT[N:]
    y_rev = np.concatenate([uT, -vT])  # flip velocity = reverse time
    bwd = solve_ivp(rhs, [0, T], y_rev, method="RK45", rtol=1e-9, atol=1e-11)
    u_back = bwd.y[:N, -1]
    err = float(np.abs(u_back - u0).max())
    fired = err > 1e-3
    return err, fired


if __name__ == "__main__":
    import scipy
    print("scipy", scipy.__version__)
    print("=== (A) heat MAXIMUM PRINCIPLE (O<=) ===")
    for mut in (False, True):
        m0, mt, fired = heat_max_principle(mut)
        tag = "MUTANT(+source)" if mut else "BASELINE(no-source)"
        print(f"  {tag:22s} max(u0)={m0:.4f} max_t(u)={mt:.4f} -> "
              f"{'FIRED (max-principle violated)' if fired else 'HELD'}")
    print("=== (B) wave TIME REVERSAL (Trev*) ===")
    for mut in (False, True):
        err, fired = wave_time_reversal(mut)
        tag = "MUTANT(+damping)" if mut else "BASELINE(undamped)"
        print(f"  {tag:22s} |u_back-u0|={err:.3e} -> "
              f"{'FIRED (time-reversal broken)' if fired else 'HELD'}")
