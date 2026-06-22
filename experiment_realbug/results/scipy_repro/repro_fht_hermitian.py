#!/usr/bin/env python3
"""
Repro for SciPy G-symmetry NOETHER block (Hermitian-symmetry preservation).

scipy.fft.fht (fast Hankel transform) computes the transform via a real-FFT
pipeline:  A = rfft(a); A *= u; out = irfft(A, n).  The coefficient array `u`
(from fhtcoeff) must respect the rfft Hermitian layout for the result to be the
correct real Hankel transform.

In-the-wild bug fixed by commit 170f9e69a (gh-21661, PR #21668):
  scipy/fft/_fftlog_backend.py  fhtcoeff():
      - u.imag[-1] = 0                 # unconditional   (BUGGY, v1.7.0..v1.14.1)
      + if n % 2 == 0:                 # only the Nyquist bin is self-conjugate
      +     u.imag[-1] = 0             # (FIXED, v1.15.0+)
  The last rfft bin (index n//2) is the self-conjugate Nyquist bin -- hence real
  -- ONLY when n is EVEN. For ODD n, index (n-1)/2 is an ordinary NON-self-
  conjugate coefficient whose imaginary part carries real information. Forcing
  u.imag[-1]=0 unconditionally destroys it for odd n, breaking Hermitian-symmetry
  consistency.

MR (G-symmetry / Hermitian-symmetry preservation):
  f(r) = r**(mu+1) * exp(-r**2/2) is a SELF-DUAL Hankel pair: its order-mu Hankel
  transform equals f on the conjugate grid k = exp(offset)/flip(r). A correct fast
  Hankel transform must reproduce this for ANY transform length n. The bug fires
  for ODD n only; EVEN n is the control (the unconditional Nyquist zeroing is valid
  there, so even-n output is bit-identical pre/post). This is scipy's own
  regression test test_gh_21661.

HONESTY NOTE: the observable signature is edge-dominated. The maximum relative
error sits at a single far-tail conjugate-grid point where f(k) underflows, so the
pre/post separation is at an enormous magnitude (~7.2e16) and the maintainers used
a deliberately loose pass threshold (7.28e16). The MR therefore uses that exact
maintainer threshold as the FIRED/HELD boundary. On smooth, well-conditioned
inputs (e.g. pure power laws) the corrupted top coefficient carries negligible
energy and the bug does NOT produce a clean order-of-magnitude blow-up; the
violation is real but numerically marginal.
"""
import math
import numpy as np
import scipy
from scipy.fft import fht, fhtoffset

# scipy's own maintainer-chosen pass threshold for test_gh_21661.
SCIPY_THRESHOLD = 7.28e16


def gh21661_relerr(n, mu=0.0):
    """max rel-err of fht(f(r)) vs analytic self-dual transform f(k); scipy test_gh_21661."""
    r = np.logspace(-7, 1, n)
    dln = math.log(r[1] / r[0])
    offset = fhtoffset(dln, initial=-6 * np.log(10), mu=mu)
    k = math.exp(offset) / np.flip(r, axis=-1)
    f = lambda x: x ** (mu + 1) * np.exp(-x ** 2 / 2)
    val = fht(f(r), dln, mu=mu, offset=offset)
    return float(np.max(np.abs((val - f(k)) / f(k))))


def main():
    print(f"scipy version: {scipy.__version__}")
    import inspect
    body = inspect.getsource(scipy.fft._fftlog_backend.fhtcoeff)
    guarded = "n % 2 == 0" in body
    print(f"fhtcoeff guards u.imag[-1] with 'if n % 2 == 0': {guarded}  "
          f"({'FIXED' if guarded else 'BUGGY unconditional'})")

    n_even, n_odd = 128, 129
    e_even = gh21661_relerr(n_even)
    e_odd = gh21661_relerr(n_odd)
    print(f"\nEVEN n={n_even}: max rel-err vs analytic f(k) = {e_even:.6e}")
    print(f"ODD  n={n_odd}: max rel-err vs analytic f(k) = {e_odd:.6e}")
    print(f"scipy pass threshold (test_gh_21661): {SCIPY_THRESHOLD:.3e}")

    # FIRED iff odd-n rel-err EXCEEDS scipy's own pass threshold (their test fails).
    fired_odd = e_odd >= SCIPY_THRESHOLD
    print(f"\n[G-sym MR] odd-n rel-err < scipy threshold (test passes): {not fired_odd}")
    print(f"[G-sym MR] even-n (control) rel-err: {e_even:.3e} "
          f"(bit-identical pre/post; unaffected by the fix)")

    if fired_odd:
        print(f"\n*** VIOLATION (FIRED) ***  odd-n FHT rel-err {e_odd:.6e} >= scipy "
              f"threshold {SCIPY_THRESHOLD:.3e}: the Hermitian-symmetry-consistent "
              f"transform is broken for odd transform length (non-Nyquist coefficient "
              f"imaginary part zeroed).")
        print("FIRED=True")
        return 1
    else:
        print(f"\n[G-sym MR] HELD: odd-n FHT rel-err {e_odd:.6e} < scipy threshold "
              f"{SCIPY_THRESHOLD:.3e} (non-Nyquist coefficient preserved).")
        print("FIRED=False")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
