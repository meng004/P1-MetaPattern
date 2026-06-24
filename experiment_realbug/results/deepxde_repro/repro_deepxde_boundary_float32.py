#!/usr/bin/env python
"""
NOETHER pde_sciml O<= boundary-value block -- DeepXDE float32 Dirichlet boundary
detection (np.isclose tolerance).

Target bug   : DeepXDE commit 8a644fe "Fix bug with `np.isclose` for float16 (#1267)"
NOETHER block: O<= monotonicity / boundary-value / order-preservation (a Dirichlet
               boundary condition u=g must be ENFORCED at boundary collocation points;
               a point lying ON the boundary must be detected and selected for BC
               enforcement -- the boundary-value side of the order/boundary block).
Module       : deepxde/geometry/geometry_1d.py Interval.on_boundary / boundary_normal
               / periodic_point (and the same np.isclose pattern in Hypercube /
               Hypersphere), via the new dtype-aware deepxde.utils.isclose.
Released pair: PRE = deepxde 1.8.4  (fix NOT in v1.8.4; 8a644fe^ = v1.8.4-2-gb87c1c6)
               POST = deepxde 1.9.0 (fix is v1.9.0~15)

Root cause
----------
DeepXDE's geometry boundary tests used bare `np.isclose(x, bound)` with the NumPy
default `atol=1e-8`. The fix swaps every geometry call to a dtype-aware
`deepxde.utils.isclose`, which raises `atol` to 1e-6 for float32 (1e-4 for float16,
1e-8 for float64). DeepXDE's DEFAULT dtype is float32. When a boundary coordinate
equals 0 (the left end of [0, L], or t0 = 0), `np.isclose`'s relative term
rtol*|b| vanishes (b = 0), so only `atol` governs the comparison. A float32 boundary
coordinate carries ~3e-8 rounding error -- LARGER than the old 1e-8 atol but smaller
than the new 1e-6 -- so the point is judged INTERIOR and the Dirichlet condition is
silently dropped at that boundary point (no crash, a wrong result).

    PRE  (geometry_1d.py): np.any(np.isclose(x, [self.l, self.r]), axis=-1)
    POST (geometry_1d.py): np.any(   isclose(x, [self.l, self.r]), axis=-1)

Metamorphic relation (O<= boundary-value enforcement)
-----------------------------------------------------
A collocation point lying ON the Dirichlet boundary must satisfy
geom.on_boundary(x) == True, receive a nonzero outward boundary_normal, and be
selected by the BC filter for enforcement. (This is the order/boundary block: the
boundary value u=g must be applied exactly at the boundary; a boundary point that is
silently treated as interior violates the boundary-value constraint.)

    FIRED <=> a float32 boundary point at coordinate ~0 (within float32 rounding of the
              boundary) is NOT detected: on_boundary=False, |normal|=0, BC drops it.
    HELD  <=> the point is detected: on_boundary=True, |normal|=1, BC keeps it.

Domain anchoring
----------------
Interval(0, 1) is the spatial domain of a 1D Dirichlet PINN (e.g. Poisson u''=f,
u(0)=u(1)=g). The left boundary sits at x=0, exactly the coordinate where the bug
bites under DeepXDE's default float32. The exact-0 literal and the right boundary
(x=1) are detected in both versions; only the float32 near-zero boundary coordinate
(which is what a real sampled / transformed collocation point looks like) is dropped.

Pure-numpy geometry path: no tensor backend is exercised, no net, no training. A
backend must merely be importable to load deepxde (DDEBACKEND=pytorch + CPU torch);
the boundary code never touches it. CPU milliseconds.

Usage:
    DDEBACKEND=pytorch <pre_venv>/bin/python  repro_deepxde_boundary_float32.py   # FIRED
    DDEBACKEND=pytorch <post_venv>/bin/python repro_deepxde_boundary_float32.py   # HELD
where pre_venv has deepxde==1.8.4 and post_venv has deepxde==1.9.0 (both + numpy<2 +
CPU torch for the import-only backend).
"""
import sys

import numpy as np
import deepxde as dde


def main():
    print("deepxde:", dde.__version__, "| default float:", dde.config.default_float())
    dt = dde.config.real(np)

    geom = dde.geometry.Interval(0.0, 1.0)  # Dirichlet domain [0, 1]

    # A float32 coordinate that is mathematically 0 but carries float32 rounding error.
    # This is what a sampled/transformed left-boundary collocation point looks like in
    # DeepXDE's default float32 mode.
    res = np.float32(0.7) - np.float32(0.4) - np.float32(0.3)  # = -2.98e-08 (math 0)
    x = np.array([[res], [0.0], [1.0]], dtype=dt)

    on_b = geom.on_boundary(x)
    nrm = geom.boundary_normal(x)

    print("float32 residual standing for x=0:", repr(float(res)),
          "| |x-0| =", abs(float(res)))
    print("points       :", x.ravel().tolist())
    print("on_boundary  :", on_b.tolist())
    print("boundary_norm:", nrm.ravel().tolist())

    # End-to-end: does the Dirichlet BC selection keep the near-zero boundary point?
    bc_kept = None
    try:
        bc = dde.icbc.DirichletBC(geom, lambda _x: 0.0, lambda _x, on: on)
        sel = bc.filter(x)  # the points DirichletBC will enforce u=g on
        bc_kept = np.asarray(sel).reshape(-1, 1).ravel().tolist()
        print("DirichletBC selects:", bc_kept)
    except Exception as e:  # noqa: BLE001  (API shape varies across versions)
        print("DirichletBC.filter probe skipped:", type(e).__name__)

    left_detected = bool(on_b[0])
    left_has_normal = abs(float(nrm[0, 0])) > 0.5
    held = left_detected and left_has_normal
    verdict = "HELD" if held else "FIRED"
    print("MR_RESULT:", verdict,
          "(left-boundary detected=%s, |normal|=%.3f; expect True,1.0)"
          % (left_detected, abs(float(nrm[0, 0]))))
    print("NOETHER-O<= VERDICT=%s  (PRE 1.8.4 expected FIRED / POST 1.9.0 expected HELD)"
          % verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
