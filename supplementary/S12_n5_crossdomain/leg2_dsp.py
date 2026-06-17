"""N5 leg-2b — non-physics multi-block transferability: digital signal processing.

Program under test = numpy.fft + circular convolution (real, independent, non-author).
Frozen NOETHER blocks instantiated on the DSP operator algebra; each block's
algebra-derived MR is EXECUTABLY CHECKED on numpy. Populates many blocks, including
Conservation (Parseval) that the industrial corpus lacked. The G block here is the
cyclic-shift group Z_N, whose FA-rank tightness is already established exactly in
fa_rank_check.py (translation Z_N); a confirming check is included.
"""
from __future__ import annotations

import numpy as np

RNG = np.random.default_rng(0)
N = 16
TOL = 1e-9


def _sig():
    return RNG.standard_normal(N) + 1j * RNG.standard_normal(N)


def _smooth():
    t = np.arange(N)
    return np.sin(2 * np.pi * t / N) + 0.5 * np.cos(4 * np.pi * t / N)


def _sym_filter():
    h = RNG.standard_normal(N)
    return (h + h[(-np.arange(N)) % N]) / 2.0          # even-symmetric, real


def mr_G_shift():
    x = _sig(); k = 3
    lhs = np.fft.fft(np.roll(x, k))
    rhs = np.fft.fft(x) * np.exp(-2j * np.pi * k * np.arange(N) / N)
    return np.allclose(lhs, rhs, atol=TOL)


def mr_G_modulation():
    x = _sig(); k0 = 2
    lhs = np.fft.fft(x * np.exp(2j * np.pi * k0 * np.arange(N) / N))
    rhs = np.roll(np.fft.fft(x), k0)
    return np.allclose(lhs, rhs, atol=TOL)


def mr_T_selfadjoint():
    h = _sym_filter()
    return np.allclose(np.fft.fft(h).imag, 0.0, atol=1e-9)         # symmetric -> real response


def mr_Conservation_parseval():
    x = _sig()
    return np.allclose(np.sum(np.abs(x) ** 2), np.sum(np.abs(np.fft.fft(x)) ** 2) / N, atol=1e-9)


def mr_L_limit():
    x = _smooth(); X = np.fft.fft(x)
    errs = []
    for k in range(1, N // 2 + 1):                                 # keep 2k+1 low freqs
        Xk = X.copy()
        if k < N // 2:
            Xk[k + 1:N - k] = 0.0
        errs.append(np.linalg.norm(np.fft.ifft(Xk) - x))
    return errs[-1] < errs[0] + TOL and all(b <= a + 1e-9 for a, b in zip(errs, errs[1:]))


def mr_O_monotone():
    x = _sig(); h = _sym_filter()
    conv = lambda f: np.fft.ifft(np.fft.fft(x) * np.fft.fft(f))
    return np.linalg.norm(conv(2.0 * h)) >= np.linalg.norm(conv(h)) - TOL


def mr_E_method():
    x = RNG.standard_normal(N); h = RNG.standard_normal(N)
    direct = np.array([sum(x[m] * h[(n - m) % N] for m in range(N)) for n in range(N)])
    fft_based = np.fft.ifft(np.fft.fft(x) * np.fft.fft(h)).real
    return np.allclose(direct, fft_based, atol=1e-8)


BLOCKS = {
    "G": [("time-shift -> modulation", mr_G_shift), ("modulation -> shift", mr_G_modulation)],
    "T*": [("symmetric filter -> real response", mr_T_selfadjoint)],
    "Conservation": [("Parseval energy", mr_Conservation_parseval)],
    "L*": [("truncated-Fourier limit", mr_L_limit)],
    "O<=": [("filter-gain monotonicity", mr_O_monotone)],
    "E*": [("direct vs FFT convolution", mr_E_method)],
}


def fa_rank_cyclic_shift():
    """G-block FA on Z_N (= DSP time-shift): generator S vs all powers."""
    S = np.zeros((N, N))
    for i in range(N):
        S[i, (i + 1) % N] = 1.0
    def comm_rank(mats):
        rows = []
        for k in range(N * N):
            E = np.zeros((N, N)); E.flat[k] = 1.0
            rows.append(np.concatenate([(E @ A - A @ E).ravel() for A in mats]))
        return int(np.linalg.matrix_rank(np.array(rows).T, tol=1e-9))
    rg = comm_rank([S])
    rd = comm_rank([np.linalg.matrix_power(S, k) for k in range(1, N)])
    return rg, rd, N * N - rg


def main():
    print(f"N5 leg-2b: digital signal processing (SUT = numpy.fft), N={N}.\n")
    occ = {}
    for blk, mrs in BLOCKS.items():
        results = [(name, fn()) for name, fn in mrs]
        occ[blk] = all(r for _, r in results)
        for name, r in results:
            print(f"  [{blk:12}] {name:34} executable-hold: {r}")
    populated = [b for b, ok in occ.items() if ok]
    print(f"\n  blocks populated: {populated}  (count {len(populated)})")
    rg, rd, kdim = fa_rank_cyclic_shift()
    print(f"  FA-rank G (cyclic shift Z_{N}): rank(1 gen)={rg} == rank(all {N-1} shifts)={rd}: "
          f"{rg==rd}; kernel dim={kdim} (circulant = N)")
    ok = (len(populated) >= 5) and (rg == rd) and (kdim == N)
    print(f"\n  leg-2b consistent (multi-block + FA tight on G): {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
