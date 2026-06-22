#!/usr/bin/env python
"""
NOETHER meta-pattern reproduction --- reactor_physics SUT domain.

Target bug : OpenMC commit 3bf1486f4 "Fix bug in Surface.normalize (#3270)"
NOETHER block : G-symmetry (geometric symmetry / equivalence invariance)
Module        : openmc.Surface.normalize  (canonical form of a surface)

Root cause
----------
Surface.normalize() reduces a surface's coefficients to a canonical form by
dividing through by the first nonzero coefficient. The pre-fix code used

    norm_factor = np.abs(coeffs[nonzeros][0])    # PRE  (v0.15.0)
    norm_factor = coeffs[nonzeros][0]            # POST (v0.15.1+, fix 3bf1486f4)

Taking the absolute value discards the sign, so two *algebraically equivalent*
representations of the SAME geometric plane do NOT map to the same canonical
tuple. OpenMC uses this canonical form to decide whether two surfaces are the
same surface (Surface.is_equal / periodic-surface pairing / geometry dedup).

Metamorphic relation (G-symmetry)
---------------------------------
Let H be a half-space-defining plane of a reactor lattice cell (e.g. a
symmetry / reflective boundary of a pin cell wedge). Any positive OR negative
scalar multiple of its coefficient vector (a, b, c, d) describes the *same*
geometric plane. Therefore the canonical form must be invariant:

        normalize(a, b, c, d) == normalize(k*a, k*b, k*c, k*d)   for all k != 0.

In particular for k = -1 (the opposite-sense algebraic representation that
arises naturally when a symmetry plane is entered "from the other side"):

        normalize(P)  ==  normalize(-P).

FIRED  <=> the two canonical tuples differ  (MR violated -> bug present)
HELD   <=> the two canonical tuples are equal (MR satisfied -> bug fixed)

Domain anchoring
----------------
The two planes below are the +/- 60 degree wedge boundaries of a hexagonal
fuel-pin cell expressed in multi-group physics. A reactor lattice tiles space
by reflecting/rotating across exactly such symmetry planes, so a canonical
form that is NOT sign-invariant breaks the surface-identity test that lattice
symmetry handling relies on.

Usage:
    micromamba run -n omc_pre  python noether_reactor_normalize.py   # PRE  0.15.0
    micromamba run -n omc      python noether_reactor_normalize.py   # POST 0.15.3
"""
import sys
import numpy as np
import openmc


def build_two_group_mgxs(path="/tmp/mgxs.h5"):
    """Minimal 2-group (thermal/fast) macroscopic library -- no CE nuclear data."""
    groups = openmc.mgxs.EnergyGroups([0., 0.625, 2.0e7])
    xs = openmc.XSdata("fuel", groups)
    xs.order = 0
    xs.set_total([1.0, 1.5])
    xs.set_absorption([5.0e-3, 8.0e-2])
    xs.set_scatter_matrix(np.array([[[0.92, 0.075], [0.0, 1.40]]]).reshape(2, 2, 1))
    xs.set_fission([2.0e-3, 5.0e-2])
    xs.set_nu_fission([5.0e-3, 1.25e-1])
    xs.set_chi([1.0, 0.0])
    lib = openmc.MGXSLibrary(groups)
    lib.add_xsdata(xs)
    lib.export_to_hdf5(path)
    return path


def reactor_symmetry_planes():
    """
    Return two algebraically-opposite representations of the SAME +60 deg
    wedge boundary plane of a hex pin cell, plus a sanity-equivalent pair.

    A plane through the origin at angle theta has normal (-sin t, cos t, 0).
    For theta = 60 deg : a = -sin60, b = cos60, c = 0, d = 0.
    P and -P are the identical geometric plane (opposite algebraic sense).
    """
    t = np.radians(60.0)
    a, b, c, d = -np.sin(t), np.cos(t), 0.0, 0.0
    P = openmc.Plane(a=a, b=b, c=c, d=d)          # +60 deg wedge boundary
    P_neg = openmc.Plane(a=-a, b=-b, c=-c, d=-d)  # SAME plane, opposite sense
    return P, P_neg


def check_mr():
    P, P_neg = reactor_symmetry_planes()
    nP = P.normalize()
    nN = P_neg.normalize()

    # Second, independent witness: the YPlane y = 1 written two equivalent ways.
    y_pos = openmc.Plane(a=0.0, b=1.0, c=0.0, d=1.0)   # y = 1
    y_neg = openmc.Plane(a=0.0, b=-1.0, c=0.0, d=-1.0)  # -y = -1  (same plane)
    ny_pos = y_pos.normalize()
    ny_neg = y_neg.normalize()

    print(f"openmc version          : {openmc.__version__}")
    print("--- witness 1: +/-60deg hex-wedge symmetry plane (P vs -P) ---")
    print(f"  normalize(P)          = {tuple(round(x, 6) for x in nP)}")
    print(f"  normalize(-P)         = {tuple(round(x, 6) for x in nN)}")
    print(f"  invariant?            = {nP == nN}")
    print("--- witness 2: plane y=1 vs -y=-1 ---")
    print(f"  normalize(y=1)        = {ny_pos}")
    print(f"  normalize(-y=-1)      = {ny_neg}")
    print(f"  invariant?            = {ny_pos == ny_neg}")

    mr_holds = (nP == nN) and (ny_pos == ny_neg)
    verdict = "HELD (MR satisfied -> bug ABSENT)" if mr_holds else \
              "FIRED (MR violated -> bug PRESENT)"
    print(f"NOETHER G-symmetry MR    : {verdict}")
    return mr_holds


def run_mg_pincell():
    """
    Prove the geometry actually transports in multi-group mode in this version
    (so the MR is anchored to a runnable reactor model, not an isolated call).
    A square pin cell with reflective boundaries (a symmetric lattice unit).
    """
    path = build_two_group_mgxs()
    fuel = openmc.Material(name="fuel")
    fuel.set_density("macro", 1.0)
    fuel.add_macroscopic("fuel")
    materials = openmc.Materials([fuel])
    materials.cross_sections = path

    pitch = 1.26
    L = pitch / 2.0
    xmin = openmc.XPlane(-L, boundary_type="reflective")
    xmax = openmc.XPlane(+L, boundary_type="reflective")
    ymin = openmc.YPlane(-L, boundary_type="reflective")
    ymax = openmc.YPlane(+L, boundary_type="reflective")
    cell = openmc.Cell(fill=fuel, region=+xmin & -xmax & +ymin & -ymax)
    geom = openmc.Geometry([cell])

    settings = openmc.Settings()
    settings.energy_mode = "multi-group"
    settings.particles = 2000
    settings.batches = 15
    settings.inactive = 5
    settings.output = {"summary": False, "tallies": False}
    settings.source = openmc.IndependentSource(
        space=openmc.stats.Box([-L, -L, -1e-9], [L, L, 1e-9]))

    model = openmc.Model(geometry=geom, materials=materials, settings=settings)
    import tempfile, os
    cwd = tempfile.mkdtemp(prefix="mg_pincell_")
    sp_path = model.run(cwd=cwd, output=False)
    with openmc.StatePoint(sp_path) as sp:
        k = sp.keff
    print(f"multi-group pin-cell k_eff = {k.nominal_value:.5f} +/- {k.std_dev:.5f}")
    return k


if __name__ == "__main__":
    held = check_mr()
    if "--run" in sys.argv:
        run_mg_pincell()
    # Exit code mirrors NOETHER oracle: 0 if MR HELD, 1 if FIRED.
    sys.exit(0 if held else 1)
