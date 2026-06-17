"""N5 leg-2a — non-physics multi-block transferability: numerical linear algebra.

Program under test = numpy.linalg (a real, independent, non-author implementation;
strong anti-circularity). The frozen NOETHER blocks are instantiated on the dense
linear-algebra operator algebra; for each block an algebra-derived MR is stated and
EXECUTABLY CHECKED on numpy. Unlike the single-block industrial corpus (all O<=),
this domain populates MANY blocks, and the two FA-rank-tight blocks (G, T*) get
N4-style tightness evidence here too.

Blocks exercised: G (permutation / orthogonal equivariance), T* (self-adjoint),
O<= (eigenvalue monotonicity), L* (Neumann-series / iterative limit),
E* (LU vs QR method comparison), Conservation (similarity-invariant trace).
"""
from __future__ import annotations

import itertools
import numpy as np

RNG = np.random.default_rng(0)
TOL = 1e-8


def _spd(n):
    M = RNG.standard_normal((n, n))
    return M @ M.T + n * np.eye(n)


def _orth(n):
    Q, _ = np.linalg.qr(RNG.standard_normal((n, n)))
    return Q


def _perm(n):
    P = np.eye(n)[RNG.permutation(n)]
    return P


# ---- per-block algebra-derived MRs, executably checked on numpy.linalg ----

def mr_G_permutation(n=6):
    A = _spd(n); b = RNG.standard_normal(n); P = _perm(n)
    return np.allclose(np.linalg.solve(P @ A @ P.T, P @ b), P @ np.linalg.solve(A, b), atol=TOL)


def mr_G_orthogonal(n=6):
    A = _spd(n); Q = _orth(n)
    return np.allclose(np.sort(np.linalg.eigvalsh(Q @ A @ Q.T)),
                       np.sort(np.linalg.eigvalsh(A)), atol=1e-6)


def mr_T_selfadjoint(n=6):
    A = _spd(n); x = RNG.standard_normal(n); y = RNG.standard_normal(n)
    recip = np.allclose(x @ (A @ y), (A @ x) @ y, atol=TOL)         # <x,Ay>=<Ax,y>
    real_spec = np.allclose(np.linalg.eigvals(A).imag, 0.0, atol=1e-6)
    return recip and real_spec


def mr_O_monotone(n=6):
    A = _spd(n); D = _spd(n)                                        # D positive semidef-ish
    lam_A = np.linalg.eigvalsh(A).min()
    lam_AD = np.linalg.eigvalsh(A + D).min()
    return lam_AD >= lam_A - TOL                                    # Weyl monotonicity


def mr_L_limit(n=6):
    M = 0.3 * RNG.standard_normal((n, n)); M /= (np.linalg.norm(M, 2) + 1e-9) / 0.5  # ||M||~0.5
    target = np.linalg.inv(np.eye(n) - M)
    S = np.zeros((n, n)); errs = []
    P = np.eye(n)
    for _ in range(40):
        S = S + P; P = P @ M
        errs.append(np.linalg.norm(S - target))
    return errs[-1] < errs[0] and errs[-1] < 1e-6                   # Neumann series converges


def mr_E_method(n=6):
    A = _spd(n); b = RNG.standard_normal(n)
    x_lu = np.linalg.solve(A, b)                                    # LU
    x_qr = np.linalg.lstsq(A, b, rcond=None)[0]                     # QR/least-squares
    return np.allclose(x_lu, x_qr, atol=1e-6)


def mr_Conservation_trace(n=6):
    A = _spd(n); Q = _orth(n)
    sim = np.allclose(np.trace(Q @ A @ Q.T), np.trace(A), atol=1e-6)
    eig_sum = np.allclose(np.linalg.eigvalsh(A).sum(), np.trace(A), atol=1e-6)
    return sim and eig_sum


BLOCKS = {
    "G": [("permutation-equivariance", mr_G_permutation),
          ("orthogonal-spectral-invariance", mr_G_orthogonal)],
    "T*": [("self-adjoint reciprocity + real spectrum", mr_T_selfadjoint)],
    "O<=": [("eigenvalue monotonicity (Weyl)", mr_O_monotone)],
    "L*": [("Neumann-series / iterative limit", mr_L_limit)],
    "E*": [("LU vs QR method comparison", mr_E_method)],
    "Conservation": [("similarity-invariant trace", mr_Conservation_trace)],
}


# ---- FA-rank tightness for the two linear-equality blocks (G perm, T*) ----

def _commutator_rank(group_mats, n):
    basis = [np.zeros((n, n)) for _ in range(n * n)]
    for k, E in enumerate(basis):
        E.flat[k] = 1.0
    rows = []
    for E in basis:
        rows.append(np.concatenate([(E @ A - A @ E).ravel() for A in group_mats]))
    J = np.array(rows).T
    return int(np.linalg.matrix_rank(J, tol=1e-9)), n * n


def fa_rank_perm(n=4):
    transp = np.eye(n)[[1, 0] + list(range(2, n))]
    cyc = np.eye(n)[[(i + 1) % n for i in range(n)]]
    gens = [transp, cyc]
    allp = [np.eye(n)[list(p)] for p in itertools.permutations(range(n))]
    rg, K = _commutator_rank(gens, n)
    rd, _ = _commutator_rank(allp, n)
    return rg, rd, K - rg            # rank_gen, rank_all, kernel dim (commutant)


def fa_rank_selfadjoint(n=6):
    rows = []
    for k in range(n * n):
        E = np.zeros((n, n)); E.flat[k] = 1.0
        rows.append((E - E.T).ravel())
    J = np.array(rows).T
    r = int(np.linalg.matrix_rank(J, tol=1e-9))
    return r, n * n - r              # rank, kernel dim (= symmetric, n(n+1)/2)


def main():
    print("N5 leg-2a: numerical linear algebra (SUT = numpy.linalg, independent).\n")
    occ = {}
    for blk, mrs in BLOCKS.items():
        results = [(name, fn()) for name, fn in mrs]
        ok = all(r for _, r in results)
        occ[blk] = ok
        for name, r in results:
            print(f"  [{blk:12}] {name:42} executable-hold: {r}")
    populated = [b for b, ok in occ.items() if ok]
    print(f"\n  blocks populated (algebra-derived MR holds on numpy): {populated}")
    print(f"  block count: {len(populated)} (vs industrial corpus = 1 [O<=])")

    rg, rd, kperm = fa_rank_perm(4)
    rs, ksym = fa_rank_selfadjoint(6)
    print("\n  FA-rank (tight IBT blocks in this domain):")
    print(f"    G (S_4 perm): rank(2 generators)={rg} == rank(all 24 perms)={rd}: {rg==rd}; "
          f"kernel dim={kperm} (commutant span)")
    print(f"    T* (n=6): kernel dim={ksym} == symmetric n(n+1)/2={6*7//2}: {ksym==6*7//2}")

    ok = (len(populated) >= 5) and (rg == rd) and (ksym == 21)
    print(f"\n  leg-2a consistent (multi-block + FA tight on G,T*): {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
