"""
NOETHER block: T* self-adjoint (Hermitian/symmetric eigendecomposition).
Fix commit: 178a12572 "BUG: linalg: fix eigh(1x1 array, driver='evd') f2py check (#20516)"
            (scipy 1.13.1)

Bug: scipy.linalg.eigh with driver='evd' (the divide-and-conquer LAPACK
     ?syevd/?heevd path) carried an over-strict f2py `check(lwork>=...)`
     guard. For a 1x1 Hermitian/symmetric matrix, LAPACK only requires
     lwork>=1, but the auto-computed lwork (2*n+1 etc.) tripped the check,
     so eigh([[1]], driver='evd') raised instead of returning the eigenvalue.

MR (T* self-adjoint block):
   For a 1x1 self-adjoint matrix [[a]] (a real), eigh must return
   eigenvalue a and eigenvector [[1]], independent of the LAPACK driver:
        eigh([[a]], driver=d) == ([a], [[1]])   for all d in {ev,evd,evr,evx}.
   Driver choice is a pure backend selection; it must not change the spectrum
   (driver-invariance of the self-adjoint eigenproblem).
   Violation (FIRED): driver='evd' raises while the others succeed.
"""
import numpy as np
from scipy.linalg import eigh
import scipy

print("scipy version:", scipy.__version__)

results = {}
fired = False
for driver in ("ev", "evd", "evr", "evx"):
    try:
        w, v = eigh([[1.0]], driver=driver)
        results[driver] = ("OK", float(w[0]), float(v[0, 0]))
    except Exception as e:
        results[driver] = ("RAISED", type(e).__name__, str(e))

for d, r in results.items():
    if r[0] == "OK":
        print(f"  driver={d:4s}  w={r[1]:.3f}  v={r[2]:.3f}")
    else:
        print(f"  driver={d:4s}  RAISED {r[1]}: {r[2]}")

# evd must behave like the other drivers on this self-adjoint input
ok_drivers = [d for d, r in results.items() if r[0] == "OK"]
if results["evd"][0] == "RAISED" and len(ok_drivers) > 0:
    fired = True
    print(f"    >>> MR VIOLATED (FIRED): driver='evd' raises on 1x1 self-adjoint "
          f"matrix while drivers {ok_drivers} succeed (driver should not change "
          f"the spectrum)")

print("VERDICT:", "FIRED" if fired else "HELD")
