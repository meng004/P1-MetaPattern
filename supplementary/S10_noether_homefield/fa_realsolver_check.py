"""N4 — FA / tight-IBT bound to the REAL advection-diffusion operator.

fa_rank_check.py established faithfulness on the abstract operator space
Theta = R^{NxN}. Reviewer point R-a/N4: bind that result to an ACTUAL solver's
operator and its real fault families. Here the linear spatial operator of the
2-D periodic advection-diffusion solver (same stencils as mcmr.pde_xeval) is
reconstructed explicitly,
    L(alpha, cx, cy) = alpha * Lap5  -  cx * Dx_central  -  cy * Dy_central,
and the fault parameter space Theta_real is spanned by the real S10 mutation
families:
    constant-coefficient (translation-equivariant, circulant):
        d_diff = Lap,  d_advx = -Dx,  d_advy = -Dy,  d_stencil = Dx_fwd - Dx_central
    spatially-inhomogeneous (translation-breaking):
        d_inhom_diff = diag(w).Lap,  d_inhom_adv = diag(w).Dx   (w[i,j]=cos 2pi i/n)

We compute, ON THIS REAL OPERATOR, the tight kernels of the two FA-rank blocks:
  - G (translation): defect [L,A]; kernel = constant-coefficient faults
    (uniform diffusion / advection-SPEED / stencil) -> UNDETECTED by symmetry MR,
    matching S10 advection-speed 0/n; inhomogeneous faults DETECTED.
  - T* (self-adjoint, on the pure-diffusion operator): defect L - L^T; kernel =
    symmetric (diffusion-magnitude) faults; advection (skew) and inhomogeneous
    faults DETECTED.
Cross-block (IBT-2) on the real operator: the advection fault is IN G's kernel
(translation-undetected) but OUTSIDE T*'s kernel (self-adjoint-detected) -> the
two blocks' kernels differ, union covers strictly more. Pure linear algebra.
"""
from __future__ import annotations

import numpy as np

TOL = 1e-9


def build_operators(n):
    """2-D periodic FD operators on an n x n grid, flattened to N = n^2."""
    N = n * n
    idx = lambda i, j: (i % n) * n + (j % n)
    Sx = np.zeros((N, N)); Sy = np.zeros((N, N))
    Dx = np.zeros((N, N)); Dy = np.zeros((N, N))
    Dxf = np.zeros((N, N)); Lap = np.zeros((N, N))
    for i in range(n):
        for j in range(n):
            p = idx(i, j)
            Sx[p, idx(i + 1, j)] = 1.0
            Sy[p, idx(i, j + 1)] = 1.0
            Dx[p, idx(i + 1, j)] += 0.5; Dx[p, idx(i - 1, j)] -= 0.5     # central
            Dy[p, idx(i, j + 1)] += 0.5; Dy[p, idx(i, j - 1)] -= 0.5
            Dxf[p, idx(i + 1, j)] += 1.0; Dxf[p, p] -= 1.0              # forward
            Lap[p, idx(i + 1, j)] += 1; Lap[p, idx(i - 1, j)] += 1
            Lap[p, idx(i, j + 1)] += 1; Lap[p, idx(i, j - 1)] += 1; Lap[p, p] -= 4
    return N, Sx, Sy, Dx, Dy, Dxf, Lap


def real_fault_basis(n):
    """Return (names, list of N x N fault-direction matrices) = S10 mutation families."""
    N, Sx, Sy, Dx, Dy, Dxf, Lap = build_operators(n)
    w = np.array([np.cos(2 * np.pi * i / n) for i in range(n) for j in range(n)])
    W = np.diag(w)
    faults = [
        ("d_diff   (uniform diffusion)",   Lap),
        ("d_advx   (advection speed x)",   -Dx),
        ("d_advy   (advection speed y)",   -Dy),
        ("d_stencil(fwd-central, const)",  Dxf - Dx),
        ("d_inhom_diff (varying coeff)",   W @ Lap),
        ("d_inhom_adv  (varying coeff)",   W @ Dx),
    ]
    return N, (Sx, Sy), faults


def _theta_nullspace(faults, defect_of):
    """Columns = fault directions; rows = vec(defect(d_k)). Null space in theta = R^K."""
    cols = [defect_of(M).ravel() for _, M in faults]
    J = np.array(cols).T                       # (rows, K)
    K = len(faults)
    r = int(np.linalg.matrix_rank(J, tol=TOL)) if J.size else 0
    # nullspace basis via SVD
    if J.size:
        _, s, Vt = np.linalg.svd(J, full_matrices=False)
        null = Vt[r:]                           # (K-r, K)
    else:
        null = np.eye(K)
    return r, K - r, null


def _in_kernel(null, k, K):
    """Is unit fault e_k in the theta-nullspace (i.e. that single fault undetected)?"""
    e = np.zeros(K); e[k] = 1.0
    if null.shape[0] == 0:
        return False
    # project e onto nullspace; in-kernel iff projection recovers e
    P = null.T @ null                            # nullspace is orthonormal (SVD rows)
    return bool(np.linalg.norm(P @ e - e) < 1e-7)


def report(n=6):
    N, (Sx, Sy), faults = real_fault_basis(n)
    K = len(faults)
    names = [nm for nm, _ in faults]
    print(f"Real advection-diffusion operator, n={n} (N={N}); "
          f"fault basis K={K} (S10 families).\n")

    # G block: translation defect [L, A] for A in {Sx, Sy} (generators)
    def gdef(M):
        return np.concatenate([(M @ Sx - Sx @ M).ravel(), (M @ Sy - Sy @ M).ravel()])
    rg, ng, nullg = _theta_nullspace(faults, gdef)
    print(f"=== G (translation), defect [L,A], witnesses {{Sx,Sy}} ===")
    print(f"  rank={rg}  kernel(theta) dim={ng}")
    for k, nm in enumerate(names):
        print(f"    {nm:32} in-kernel(undetected): {_in_kernel(nullg, k, K)}")

    # FA: generators vs dense (all 2-D shifts) give same kernel
    shifts = [np.linalg.matrix_power(Sx, a) @ np.linalg.matrix_power(Sy, b)
              for a in range(n) for b in range(n) if (a, b) != (0, 0)]
    def gdef_dense(M):
        return np.concatenate([(M @ A - A @ M).ravel() for A in shifts])
    rgd, ngd, _ = _theta_nullspace(faults, gdef_dense)
    print(f"  FA: rank(test {{Sx,Sy}})={rg} == rank(dense, {len(shifts)} shifts)={rgd}: "
          f"{rg == rgd}  (finite generators pin the full translation kernel)")

    # T* block: self-adjoint defect L - L^T (on the diffusion operator; advection is skew)
    def tdef(M):
        return (M - M.T).ravel()
    rt, nt, nullt = _theta_nullspace(faults, tdef)
    print(f"\n=== T* (self-adjoint), defect L - L^T ===")
    print(f"  rank={rt}  kernel(theta) dim={nt}")
    for k, nm in enumerate(names):
        print(f"    {nm:32} in-kernel(undetected): {_in_kernel(nullt, k, K)}")

    # Cross-block (IBT-2) on the real operator
    advx_in_G = _in_kernel(nullg, 1, K)
    advx_in_T = _in_kernel(nullt, 1, K)
    print(f"\n--- cross-block (IBT-2) on the real operator ---")
    print(f"  advection-speed fault: in G-kernel={advx_in_G} (translation MR misses it), "
          f"in T*-kernel={advx_in_T} (self-adjoint MR catches it)")
    print(f"  => the two blocks' kernels differ; union detects strictly more.")
    print(f"  bridge: G-kernel = constant-coefficient faults (uniform diffusion / "
          f"advection-speed / const stencil) -> matches S10 advection-speed 0/n;")
    print(f"          inhomogeneous faults leave both kernels -> detected.")

    ok = (rg == rgd) and advx_in_G and (not advx_in_T)
    print(f"\nN4 evidence consistent (FA on real operator; G/T* kernels as predicted): {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(report())
