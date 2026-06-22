#!/usr/bin/env python3
"""
Repro: diffrax SRK (Stochastic Runge-Kutta) solvers gave WRONG results when
integrating BACKWARDS in time, because the space-time Levy area `H` was used
without accounting for the integration direction.  This violates the
time-reversal / reversibility invariant of family e (Mode I):

    Phi_t( Theta Phi_t x ) = Theta x     (round trip returns the initial state)

Operationalised for an additive-noise SDE under a *fixed* Brownian sample path W:
solve forward 0 -> T to get y(T); then solve the SAME equation backward T -> 0
over the SAME path.  For the (pathwise) strong solution this round trip must
return to y(0), and the discretisation error must -> 0 as dt -> 0 if the solver
is correct.

  * PRE  (diffrax 0.7.2, == parent commit 56d78e1 for srk.py):
        round-trip error ~ 0.67 and DOES NOT shrink under refinement
        (systematic Levy-area sign error on the backward branch)  ->  FIRED
  * POST (fix 12efb5b "fix backwards-in-time solve for srk's"):
        round-trip error -> 0 as dt -> 0  ->  HELD

The fix (diffrax/_solver/srk.py) introduces a signed step `signed_h = drift.contr(t0,t1)`
and multiplies the space-time Levy area H by `direction = sign(signed_h)`, so that
H respects H(h) = H(-h) while the drift control carries the correct sign.

This script runs BOTH branches by swapping the installed diffrax/_solver/srk.py
with the verbatim PRE and POST versions saved next to it, each in a fresh
subprocess (so the module is re-imported cleanly).

Usage:
    # in a venv with `pip install "jax[cpu]" diffrax==0.7.2`
    python repro_diffrax_srk_backward_revers.py            # runs PRE and POST
    python repro_diffrax_srk_backward_revers.py _worker PRE # internal
"""
import os
import sys
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SRK_PRE = os.path.join(HERE, "srk_PRE_56d78e1.py")
SRK_POST = os.path.join(HERE, "srk_POST_12efb5b.py")


# --------------------------------------------------------------------------- #
#  Worker: assumes the desired srk.py is already installed; runs the test.     #
# --------------------------------------------------------------------------- #
def worker(label):
    import jax
    jax.config.update("jax_enable_x64", True)
    import jax.numpy as jnp
    import jax.random as jr
    import diffrax

    SOLVERS = {
        "ShARK": diffrax.ShARK,
        "GeneralShARK": diffrax.GeneralShARK,
        "SlowRK": diffrax.SlowRK,
        "SPaRK": diffrax.SPaRK,
    }

    def drift(t, y, args):
        return -0.5 * y + 0.2 * jnp.cos(0.7 * t)

    def diffusion_add(t, y, args):           # additive noise (2,1)
        return jnp.array([[0.3], [0.15]])

    def diffusion_gen(t, y, args):           # mild general noise, 1 BM
        return jnp.array([[0.3 + 0.05 * jnp.tanh(y[0])], [0.15]])

    y0 = jnp.array([1.0, -0.5])
    t0, T = 0.0, 2.0
    key = jr.key(42)                          # FIXED -> deterministic path

    def solve(solver, a, b, y_init, n, diff):
        # one fixed Brownian path on [t0,T]; same key for fwd & back
        bm = diffrax.VirtualBrownianTree(
            t0=t0, t1=T, tol=1e-4, shape=(1,), key=key,
            levy_area=diffrax.SpaceTimeLevyArea)
        terms = diffrax.MultiTerm(diffrax.ODETerm(drift),
                                  diffrax.ControlTerm(diff, bm))
        sol = diffrax.diffeqsolve(
            terms, solver(), t0=a, t1=b, dt0=(b - a) / n, y0=y_init,
            saveat=diffrax.SaveAt(t1=True), max_steps=100000)
        return sol.ys[-1]

    def roundtrip_err(solver, n, diff):
        yT = solve(solver, t0, T, y0, n, diff)        # forward 0 -> T
        yb = solve(solver, T, t0, yT, n, diff)        # backward T -> 0
        return float(jnp.max(jnp.abs(yb - y0)))

    print(f"diffrax {diffrax.__version__}  [{label}]")
    print("=" * 72)
    summary = {}
    for name, S in SOLVERS.items():
        diff = diffusion_gen if name in ("GeneralShARK", "SlowRK", "SPaRK") else diffusion_add
        print(f"\n--- {name} ---")
        print("  round-trip max|y_back - y0| under refinement (->0 iff reversible):")
        last = None
        for n in (50, 200, 800, 3200):
            e = roundtrip_err(S, n, diff)
            print(f"    n={n:5d}  err={e:.6e}")
            last = e
        summary[name] = last
    print("\n  SUMMARY (n=3200):")
    for k, v in summary.items():
        print(f"    {k:14s} {v:.6e}")


# --------------------------------------------------------------------------- #
#  Driver: swap srk.py -> run worker -> restore.                               #
# --------------------------------------------------------------------------- #
def find_installed_srk():
    import diffrax
    return os.path.join(os.path.dirname(diffrax.__file__), "_solver", "srk.py")


def run_branch(label, srk_src):
    dst = find_installed_srk()
    backup = dst + ".bak_repro"
    shutil.copy(dst, backup)
    try:
        shutil.copy(srk_src, dst)
        # nuke pycache so the swapped source is actually imported
        site = os.path.dirname(os.path.dirname(dst))
        for root, dirs, _ in os.walk(site):
            for d in list(dirs):
                if d == "__pycache__":
                    shutil.rmtree(os.path.join(root, d), ignore_errors=True)
        env = dict(os.environ)
        subprocess.run([sys.executable, os.path.abspath(__file__), "_worker", label],
                       check=True, env=env)
    finally:
        shutil.copy(backup, dst)
        os.remove(backup)


def main():
    for f in (SRK_PRE, SRK_POST):
        if not os.path.exists(f):
            sys.exit(f"missing {f}")
    print("##### PRE  (released 0.7.2 == parent 56d78e1; pre-fix srk.py) #####")
    run_branch("PRE", SRK_PRE)
    print("\n\n##### POST (fix 12efb5b applied to srk.py) #####")
    run_branch("POST", SRK_POST)
    print("\n\nEXPECT: PRE ~0.67 flat under refinement (FIRED);"
          " POST ->0 as dt->0 (HELD).")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "_worker":
        worker(sys.argv[2])
    else:
        main()
