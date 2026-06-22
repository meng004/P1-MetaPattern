#!/usr/bin/env python
"""
NOETHER meta-pattern reproduction --- reactor_physics SUT domain.

Target bug : OpenMC commit c7d7fa461 "Fix a bug in rotational periodic
             boundary conditions (#3692)".
NOETHER block : G-symmetry (geometric symmetry / rotational-equivalence
                invariance).
Module        : RotationalPeriodicBC (src/boundary_condition.cpp,
                src/surface.cpp, src/geometry_aux.cpp).

Environment note
----------------
This fix first appears in the development line (v0.15.4-dev, commit count 31
after v0.15.3) and has NOT shipped in any tagged release, so there is no conda
post-binary. Both PRE (parent 818fd11b1) and POST (c7d7fa461) are therefore
built FROM SOURCE; see repro driver / build script. The two OpenMC binaries
are selected with the OPENMC_BIN environment variable.

Root cause
----------
A rotational-periodic boundary maps a particle that leaves through one bounding
plane back in through the partner plane, rotated about the symmetry axis. The
pre-fix code

  * computed the rotation angle from theta2 - theta1 with a hard-coded +PI
    "anti-normal" assumption, and
  * decided forward/backward rotation and the new-surface sense from *which*
    of the two surfaces was struck (i_particle_surf == i_surf_ / j_surf_),

both of which are wrong once the bounding planes are written with the opposite
algebraic sense (the plane coefficient vector negated, i.e. the cell is built
with -plane instead of +plane). The fix instead

  * derives a *signed* angle directly from the surface normals,
        angle = atan2( (n1 x n2).a , n1.n2 )     (a = rotation axis)
    with the surface signs folded into n1, n2 via copysign(1, i_surf) /
    -copysign(1, j_surf), and
  * introduces flip_sense_ = (i_sign * j_sign > 0) to flip the partner
    surface's sense when the two normals point the same general way.

Consequently, before the fix, two geometries that are the SAME physical
rotational-periodic wedge but whose bounding planes are written with flipped
algebraic sense transport particles differently and produce different k_eff.

Metamorphic relation (G-symmetry)
---------------------------------
Take a wedge of a "circle of half-cylinders" closed by two periodic planes that
subtend the rotational-symmetry angle (the canonical periodic_6fold geometry
from OpenMC's own regression suite, ported to 2-group multi-group physics).
Each bounding plane can be written two algebraically-equivalent ways: a*x+b*y=0
or (-a)*x+(-b)*y=0. These describe the IDENTICAL half-space pair and hence the
IDENTICAL reactor, so the eigenvalue must be invariant under the sign choice:

    k_eff(flip1, flip2) == k_eff(False, False)   for all (flip1, flip2).

FIRED  <=> the four sign-flip representations do NOT all agree (MR violated ->
           bug present: rotational-periodic sense/angle handling is not
           invariant to the algebraic sense of the bounding planes).
HELD   <=> all four agree within Monte-Carlo statistics (MR satisfied -> fixed).

This mirrors OpenMC's own fix-commit regression test
(tests/regression_tests/periodic_6fold/test.py), which asserts that all four
(flip1, flip2) cases give the same k-combined.

Usage
-----
    OPENMC_BIN=/tmp/omc_pre/build/bin/openmc  python repro_rotational_periodic.py
    OPENMC_BIN=/tmp/omc_post/build/bin/openmc python repro_rotational_periodic.py

The Python openmc API (model building / statepoint reading) comes from the
PyAPI of whichever build's `pip install -e .` is active; only the compiled
transport kernel differs between PRE and POST. The driver script
run_rotational_periodic.py sets this up for both.
"""
import os
import sys
import tempfile
from math import sin, cos, pi

import numpy as np
import openmc


# Per-flip statistical tolerance on k_eff. The four representations are the
# identical physical model, so post-fix they agree to Monte-Carlo noise; the
# pre-fix bug shifts k by O(10%) or invalidates the geometry, far outside this.
KTOL = 5.0e-3


def build_two_group_mgxs(path="/tmp/mgxs_rotper.h5"):
    """Minimal 2-group (thermal/fast) macroscopic library -- no CE nuclear data.

    Identical spectrum/cross-sections to the sibling reactor_physics repros
    (noether_reactor_normalize.py / noether_reactor_no_reduce.py) so the MG
    physics is shared across the reactor_physics block.
    """
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


def build_model(flip1, flip2, xs_path):
    """Build the 6-fold rotational-periodic wedge as 2-group multi-group.

    Geometry ported from OpenMC's own fix-commit regression test
    (tests/regression_tests/periodic_6fold/test.py): a wedge of a "circle of
    half-cylinders" closed by two periodic planes at +-60 deg, plus a reflective
    outer x-plane and a fuelled half-cylinder. flip1/flip2 negate the algebraic
    sense (coefficient vector) of each periodic plane; this must not change the
    physics.
    """
    fuel = openmc.Material(name="fuel")
    fuel.set_density("macro", 1.0)
    fuel.add_macroscopic("fuel")
    materials = openmc.Materials([fuel])
    materials.cross_sections = xs_path

    theta1 = (-1/6 + 1/2) * pi
    theta2 = (1/6 - 1/2) * pi
    if flip1:
        plane1 = openmc.Plane(a=-cos(theta1), b=-sin(theta1), boundary_type="periodic")
    else:
        plane1 = openmc.Plane(a=cos(theta1), b=sin(theta1), boundary_type="periodic")
    if flip2:
        plane2 = openmc.Plane(a=-cos(theta2), b=-sin(theta2), boundary_type="periodic")
    else:
        plane2 = openmc.Plane(a=cos(theta2), b=sin(theta2), boundary_type="periodic")
    plane1.periodic_surface = plane2

    x_max = openmc.XPlane(5., boundary_type="reflective")
    z_cyl = openmc.ZCylinder(x0=3*cos(pi/6), y0=3*sin(pi/6), r=2.0)

    s1 = -plane1 if flip1 else +plane1
    s2 = -plane2 if flip2 else +plane2
    outside_cyl = openmc.Cell(fill=fuel, region=(s1 & s2 & -x_max & +z_cyl))
    inside_cyl = openmc.Cell(fill=fuel, region=(s1 & s2 & -z_cyl))
    root = openmc.Universe(cells=(outside_cyl, inside_cyl))
    geom = openmc.Geometry(root)

    settings = openmc.Settings()
    settings.energy_mode = "multi-group"
    settings.run_mode = "eigenvalue"
    settings.particles = 5000
    settings.batches = 60
    settings.inactive = 20
    settings.output = {"summary": False, "tallies": False}
    settings.source = openmc.IndependentSource(
        space=openmc.stats.Box((0., 0., -1e-9), (4., 4., 1e-9)))

    return openmc.Model(geometry=geom, materials=materials, settings=settings)


def run_keff(flip1, flip2, xs_path):
    """Return (k_eff, std_dev) or (None, None) if transport failed.

    A failed run (e.g. "Maximum number of lost particles" because the
    rotational-periodic boundary does not correctly map particles across for
    this sign convention) is itself an MR violation: the same physical model,
    written with a different algebraic plane sense, must transport identically.
    """
    model = build_model(flip1, flip2, xs_path)
    cwd = tempfile.mkdtemp(prefix=f"rotper_{flip1}_{flip2}_")
    # Select the source-built transport kernel (PRE parent vs POST fix).
    openmc_exec = os.environ.get("OPENMC_BIN", "openmc")
    try:
        sp_path = model.run(cwd=cwd, output=False, openmc_exec=openmc_exec)
    except RuntimeError as exc:
        msg = str(exc).splitlines()[0] if str(exc) else repr(exc)
        print(f"    -> transport FAILED: {msg[:90]}")
        return None, None
    with openmc.StatePoint(sp_path) as sp:
        k = sp.keff
    return float(k.nominal_value), float(k.std_dev)


def check_mr():
    xs_path = build_two_group_mgxs()
    print(f"openmc version          : {openmc.__version__}")
    print(f"openmc exe              : {os.environ.get('OPENMC_BIN', '(default PATH)')}")
    print("--- 6-fold rotational-periodic wedge, four sign-flip representations ---")

    results = {}
    failures = []
    for flip1 in (False, True):
        for flip2 in (False, True):
            k, sd = run_keff(flip1, flip2, xs_path)
            results[(flip1, flip2)] = (k, sd)
            if k is None:
                failures.append((flip1, flip2))
            else:
                print(f"  k_eff(flip1={flip1!s:5s}, flip2={flip2!s:5s}) "
                      f"= {k:.6f} +/- {sd:.6f}")

    k_ref, sd_ref = results[(False, False)]
    if k_ref is None:
        # The canonical representation itself must always work; if not, we cannot
        # form the MR baseline (should not happen for either PRE or POST here).
        raise RuntimeError("baseline (False,False) representation failed to run")

    max_dev = 0.0
    worst = None
    for key, (k, sd) in results.items():
        if k is None:
            continue
        dev = abs(k - k_ref)
        if dev > max_dev:
            max_dev, worst = dev, key
    print(f"  reference (False,False) = {k_ref:.6f}")
    if failures:
        print(f"  transport-failed reps   = {failures} "
              f"(lost particles: periodic BC did not map across)")
    print(f"  max |k - k_ref| (ran)   = {max_dev:.6f}  (at {worst}), tol = {KTOL}")

    # MR holds iff ALL four representations ran AND agree within tolerance.
    mr_holds = (not failures) and (max_dev <= KTOL)
    verdict = "HELD (MR satisfied -> bug ABSENT)" if mr_holds else \
              "FIRED (MR violated -> bug PRESENT)"
    print(f"NOETHER G-symmetry MR    : {verdict}")
    return mr_holds, results, k_ref, max_dev, worst, failures


if __name__ == "__main__":
    held, results, k_ref, max_dev, worst, failures = check_mr()
    # Exit code mirrors NOETHER oracle: 0 if MR HELD, 1 if FIRED.
    sys.exit(0 if held else 1)
