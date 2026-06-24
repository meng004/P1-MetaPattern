#!/usr/bin/env python3
"""
Repro for OpenMC O<= (non-negativity) NOETHER block:
  Depletion number densities must be NON-NEGATIVE (atom densities >= 0).

In-the-wild bug fixed by commit 1f7ac4215 (#3879):
  "Clip negative atom densities that result from CRAM"
  openmc/deplete/abc.py  Integrator.integrate():
      + for r in results:
      +     r.clip(min=0.0, out=r)

CRAM (Chebyshev Rational Approximation Method) computes the matrix exponential
exp(A t) n0 for the Bateman depletion equations. For stiff systems it can return
small NEGATIVE number densities, which are UNPHYSICAL (an atom count cannot be < 0).

MR (O<=, physical-quantity non-negativity):
    For every nuclide i, in every material m, at every depletion step t:
        N_{m,i}(t) >= 0
The follow-up "physically-equivalent" relation here is the floor at zero:
    a depletion solver applied to a non-negative initial vector must return a
    non-negative number-density vector (concentrations are intensive >= 0).

Self-contained: uses the in-repo tests/dummy_operator.DummyOperator, a 2-species
toy depletion system y' = f(y) y. NO nuclear data, NO C++ transport needed
(openmc.lib falls back to Mock() when libopenmc is absent).
"""
import sys
import numpy as np

# tests/ holds dummy_operator.py; path injected by the runner via OMC_TREE
OMC_TREE = sys.argv[1] if len(sys.argv) > 1 else "/tmp/omc_pre"
sys.path.insert(0, OMC_TREE + "/tests")

import openmc
import openmc.deplete
from openmc.deplete import abc as _abc
import dummy_operator as do

TOL = 0.0  # O<= is an exact physical bound: N >= 0 (any N < 0 is a violation)


def run_predictor_depletion(tmpdir):
    """Run the predictor integrator on the DummyOperator toy system and
    return the full number-density trajectory for the 2 nuclides."""
    import os
    cwd = os.getcwd()
    os.chdir(tmpdir)
    try:
        operator = do.DummyOperator()
        # predictor scheme, two 0.75 s steps, power 1.0 W (matches in-repo test)
        do.PredictorIntegrator(operator, [0.75, 0.75], 1.0).integrate()
        res = openmc.deplete.Results("depletion_results.h5")
        _, y1 = res.get_atoms("1", "1")
        _, y2 = res.get_atoms("1", "2")
        return np.asarray(y1), np.asarray(y2)
    finally:
        os.chdir(cwd)


def main():
    import tempfile
    print(f"openmc version : {openmc.__version__}")
    print(f"abc module file: {_abc.__file__}")
    clip_present = "clip(min=0.0" in open(OMC_TREE + "/openmc/deplete/abc.py").read()
    print(f"clip(min=0.0) present in abc.py: {clip_present}")

    with tempfile.TemporaryDirectory() as td:
        y1, y2 = run_predictor_depletion(td)

    print(f"\nNuclide 1 atoms over [0, 0.75, 1.5] s: {y1}")
    print(f"Nuclide 2 atoms over [0, 0.75, 1.5] s: {y2}")

    all_atoms = np.concatenate([y1, y2])
    min_density = float(all_atoms.min())
    print(f"\nMIN number density across all nuclides/steps: {min_density:.16g}")

    # O<= MR check: every number density must be >= 0
    violation = min_density < -TOL if TOL > 0 else min_density < 0.0
    if violation:
        n_neg = int((all_atoms < 0).sum())
        print(f"\n[O<= MR] *** VIOLATION (FIRED) ***")
        print(f"  {n_neg} negative number density(ies); most negative = {min_density:.16g}")
        print(f"  An atom count < 0 is physically impossible; CRAM produced an "
              f"unphysical concentration.")
        print("FIRED=True")
        return 1
    else:
        print(f"\n[O<= MR] HELD: all number densities >= 0 (min = {min_density:.16g})")
        print("FIRED=False")
        return 0


if __name__ == "__main__":
    sys.exit(main())
