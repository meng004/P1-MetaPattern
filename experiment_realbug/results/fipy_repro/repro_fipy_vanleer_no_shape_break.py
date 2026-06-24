#!/usr/bin/env python3
r"""
NEGATIVE-result reproduction for NOETHER family g (D*, O<=.dyn dynamic-shape /
no-overshoot / TVD-monotonicity) in the FiPy finite-volume PDE library.

Goal of the search: find an in-the-wild maintainer fix where the PRE-fix code
VIOLATES the no-overshoot / no-spurious-oscillation invariant
        Z(Phi x) <= Z(x)        (Z = #sign-changes / #local-extrema)
in a TVD / flux-limiter advection scheme, and the POST-fix code SATISFIES it.

This script demonstrates two facts that, together, make FiPy a NEGATIVE for
family g (mirroring results/NEGATIVE_scipy_dstar.md for SciPy / PCHIP):

  PART A  (the invariant is REAL and TESTABLE in this substrate):
          Advect a monotone step on a periodic 1-D grid. FiPy's TVD
          `VanLeerConvectionTerm` (and the monotone first-order Upwind /
          PowerLaw schemes) preserve the no-overshoot invariant exactly,
          whereas the non-TVD `CentralDifferenceConvectionTerm` VIOLATES it
          (overshoots beyond [0,1] and gains many spurious extrema). So FiPy
          *does* have a shape-preserving advection substrate where overshoot
          is the natural failure mode -- the substrate SciPy lacked.

  PART B  (the only released limiter fix is ACCURACY-not-SHAPE, wrong direction):
          The single modern FiPy convection-limiter bug-fix,
            a1dd901d23e87fc4d2738dd42e10b28bf677875c
            "Correcting issues in Van Leer raised by Jason Furtney" (ticket:564
             / GitHub issue #377 "VanLeerConvectionTerm MinMod slope limiter is
             broken"); first released in FiPy 3.1 (parent 0c8a5a63 is in 3.0.1),
          changes the interior slope limiter
            PRE : min3 = min(|a|,      |b|,      avg)     # = MinMod (over-diffusive, TVD-SAFE)
            POST: min3 = min(2|a|,     2|b|,     avg)     # = true Van Leer / MC (sharper)
          with avg = 0.5(|a|+|b|).  Because min(|a|,|b|,avg) == min(|a|,|b|) and
          MinMod is itself a TVD limiter, the PRE-fix curve is the *safe*
          (more diffusive) one: it does NOT overshoot.  The fix makes the scheme
          LESS diffusive / MORE accurate, the OPPOSITE of the family-g signature
          (which needs PRE = overshoots, POST = clean).  Reconstructing BOTH the
          pre- and post-fix limiter formulas verbatim from the a1dd901d diff and
          advecting the same monotone step shows NO overshoot on EITHER side.

Deterministic: pure NumPy + FiPy, no randomness; identical numbers on re-run.
Tested with FiPy 4.0.3 / NumPy (pure-python wheel), Python 3.11.

Reproduce:
    uv venv --python 3.11 /tmp/venvg_probe
    VIRTUAL_ENV=/tmp/venvg_probe uv pip install --no-cache-dir fipy numpy scipy
    /tmp/venvg_probe/bin/python results/fipy_repro/repro_fipy_vanleer_no_shape_break.py
"""
import warnings
warnings.filterwarnings("ignore")

import numpy as np
from fipy import CellVariable, PeriodicGrid1D, TransientTerm
from fipy.terms.vanLeerConvectionTerm import VanLeerConvectionTerm
from fipy.terms.upwindConvectionTerm import UpwindConvectionTerm
from fipy.terms.explicitUpwindConvectionTerm import ExplicitUpwindConvectionTerm
from fipy.terms.powerLawConvectionTerm import PowerLawConvectionTerm
from fipy.terms.centralDiffConvectionTerm import CentralDifferenceConvectionTerm
from fipy.tools import numerix


# ----------------------------------------------------------------------------
# shared driver: advect a monotone step (Riemann front) at constant velocity
# ----------------------------------------------------------------------------
def advect_step(TermClass, nx=200, steps=80, Co=0.2):
    L = 2.0
    dx = L / nx
    mesh = PeriodicGrid1D(nx=nx, dx=dx)
    var = CellVariable(mesh=mesh, name="u")
    x = mesh.cellCenters[0]
    var.setValue(0.0)
    var.setValue(1.0, where=(x < L / 2))      # monotone step: 1 -> 0
    u0 = np.array(var).copy()
    dt = Co * dx / 1.0                          # velocity = 1.0 to the right
    eq = TransientTerm() + TermClass(coeff=(1.0,))
    for _ in range(steps):
        eq.solve(var=var, dt=dt)
    return u0, np.array(var).copy()


def shape_metrics(u0, uf):
    lo, hi = float(u0.min()), float(u0.max())
    overshoot = max(0.0, float(uf.max()) - hi)
    undershoot = max(0.0, lo - float(uf.min()))

    def n_extrema(u):
        d = np.diff(u)
        s = np.sign(np.where(np.abs(d) < 1e-10, 0, d))
        s = s[s != 0]
        return int(np.sum(s[1:] * s[:-1] < 0))

    tv0 = float(np.sum(np.abs(np.diff(u0))))
    tvf = float(np.sum(np.abs(np.diff(uf))))
    return dict(min=float(uf.min()), max=float(uf.max()),
                overshoot=overshoot, undershoot=undershoot,
                extrema0=n_extrema(u0), extremaf=n_extrema(uf),
                tv_ratio=(tvf / tv0 if tv0 else float("nan")))


# ----------------------------------------------------------------------------
# PART A: the no-overshoot invariant is real -- TVD holds, central-diff breaks
# ----------------------------------------------------------------------------
def part_A():
    print("=" * 92)
    print("PART A  no-overshoot invariant Z(Phi x) <= Z(x): advect a monotone step (periodic, Co=0.2)")
    print("=" * 92)
    hdr = f"{'scheme':<26}{'min':>10}{'max':>10}{'overshoot':>12}{'undershoot':>12}{'extr_in':>8}{'extr_out':>9}{'TVf/TV0':>9}  verdict"
    print(hdr)
    rows = [("Upwind (1st-order)", UpwindConvectionTerm),
            ("ExplicitUpwind", ExplicitUpwindConvectionTerm),
            ("PowerLaw", PowerLawConvectionTerm),
            ("VanLeer (TVD)", VanLeerConvectionTerm),
            ("CentralDifference", CentralDifferenceConvectionTerm)]
    out = {}
    for name, T in rows:
        u0, uf = advect_step(T)
        m = shape_metrics(u0, uf)
        # HELD if no overshoot/undershoot beyond data range (small numerical floor)
        held = (m["overshoot"] < 1e-9) and (m["undershoot"] < 1e-9)
        verdict = "HELD (no overshoot)" if held else "FIRED (overshoot!)"
        out[name] = m
        print(f"{name:<26}{m['min']:>10.4f}{m['max']:>10.4f}{m['overshoot']:>12.2e}"
              f"{m['undershoot']:>12.2e}{m['extrema0']:>8d}{m['extrema_out' if False else 'extremaf']:>9d}"
              f"{m['tv_ratio']:>9.3f}  {verdict}")
    print()
    print("  -> The TVD `VanLeerConvectionTerm` and the monotone Upwind/PowerLaw schemes HOLD the")
    print("     invariant; only the non-TVD CentralDifference FIRES it. So FiPy genuinely possesses")
    print("     a shape-preserving advection substrate (the substrate SciPy lacked).")
    return out


# ----------------------------------------------------------------------------
# PART B: the only released limiter fix (a1dd901d) is accuracy, not shape
#         -> reconstruct PRE (MinMod) and POST (true MC) limiters verbatim
# ----------------------------------------------------------------------------
def _pre_getGradient(self, normalGradient, gradUpwind):
    """PRE a1dd901d (ticket:564 / issue #377): min(|a|,|b|,avg) == MinMod (TVD-safe)."""
    gradUpUpwind = -gradUpwind + 2 * normalGradient
    avg = 0.5 * (abs(gradUpwind) + abs(gradUpUpwind))
    min3 = numerix.minimum(numerix.minimum(abs(gradUpwind), abs(gradUpUpwind)), avg)
    return numerix.where(gradUpwind * gradUpUpwind < 0., 0.,
                         numerix.where(gradUpUpwind > 0., min3, -min3))


def _post_getGradient(self, normalGradient, gradUpwind):
    """POST a1dd901d: min(2|a|,2|b|,avg) == true Van Leer / monotonized-central."""
    gradUpUpwind = -gradUpwind + 2 * normalGradient
    avg = 0.5 * (abs(gradUpwind) + abs(gradUpUpwind))
    min3 = numerix.minimum(numerix.minimum(abs(2 * gradUpwind), abs(2 * gradUpUpwind)), avg)
    return numerix.where(gradUpwind * gradUpUpwind < 0., 0.,
                         numerix.where(gradUpUpwind > 0., min3, -min3))


def part_B():
    print("=" * 92)
    print("PART B  fix a1dd901d (issue #377 'VanLeer MinMod slope limiter is broken'; FiPy 3.0.1 -> 3.1)")
    print("        reconstruct PRE (MinMod) vs POST (true MC) limiter, advect the SAME monotone step")
    print("=" * 92)
    print(f"{'side':<34}{'min':>10}{'max':>10}{'overshoot':>12}{'undershoot':>12}{'extra_extrema':>14}{'TVf/TV0':>9}")
    out = {}
    for label, gg in [("PRE  min(|a|,|b|,avg)  [MinMod]", _pre_getGradient),
                      ("POST min(2|a|,2|b|,avg) [MC/VL]", _post_getGradient)]:
        VanLeerConvectionTerm._getGradient = gg
        u0, uf = advect_step(VanLeerConvectionTerm)
        m = shape_metrics(u0, uf)
        out[label] = m
        print(f"{label:<34}{m['min']:>10.4f}{m['max']:>10.4f}{m['overshoot']:>12.2e}"
              f"{m['undershoot']:>12.2e}{m['extremaf']:>14d}{m['tv_ratio']:>9.3f}")
    print()
    print("  -> BOTH PRE and POST have ZERO overshoot: the fix changes the limiter from the")
    print("     over-diffusive MinMod to the sharper true Van Leer (MC) -- an ACCURACY refinement,")
    print("     NOT a no-overshoot restoration. Direction is the OPPOSITE of family g (need PRE bad).")
    return out


if __name__ == "__main__":
    import fipy
    print(f"FiPy {fipy.__version__}\n")
    A = part_A()
    print()
    B = part_B()
    print()
    print("=" * 92)
    print("VERDICT: NEGATIVE for family g (D*) in FiPy.")
    print("  - The invariant IS testable here (VanLeer/Upwind HOLD; CentralDifference FIRES, "
          f"overshoot={A['CentralDifference']['overshoot']:.2e}, +{A['CentralDifference']['extremaf']} extrema).")
    print("  - But the ONLY released convection-limiter fix (a1dd901d / #377) is accuracy-not-shape,")
    print("    and is clean on BOTH sides (PRE overshoot=%.1e, POST overshoot=%.1e)."
          % (B["PRE  min(|a|,|b|,avg)  [MinMod]"]["overshoot"],
             B["POST min(2|a|,2|b|,avg) [MC/VL]"]["overshoot"]))
    print("  - The oscillatory Roe/MC-limiter work (commit 55071cea, 'broke the rotation example')")
    print("    lives ONLY on the unmerged `riemann` branch and was NEVER released (not on HEAD).")
    print("  Like SciPy/PCHIP, FiPy's shipped TVD limiter is constructively non-oscillatory; its")
    print("  fixes are accuracy/refactor, never a shape-guarantee restoration. Recorded as negative.")
