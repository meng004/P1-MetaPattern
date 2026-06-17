"""Faithfulness (FA) rank check for the Invariance-Blindness Theorem (IBT-G).

Operationalizes FA on the linear-operator fault class. For a symmetry group acting
on R^N, the fault space is Theta = R^{NxN} (all linear operators L; the program is
P_L(x) = L x). The equivariance MR's defect at a group element A and input x is
    E(L; A, x) = L(Ax) - A(Lx) = [L, A] x      (linear/affine in L),
so the per-A defect vanishes for all inputs iff the commutator [L, A] = 0.

  - undetected-fault subspace (the MR's kernel) = { L : [L, A] = 0 for A in WITNESSES }
                                                = the commutant of the witness set,
  - the *compatible* (symmetry-preserving) subspace = commutant of the WHOLE group.

FA (faithfulness) holds for a finite test witness set W_test iff
    kernel(W_test) = kernel(W_full),   equivalently   rank(J_test) = rank(J_dense),
i.e. a finite test (e.g. the group GENERATORS) already pins the full commutant.
This script builds J exactly (acting the commutator on a basis of Theta), and
checks rank/kernel equality of test (generators) vs dense (all group elements).

This is the exact, runnable witness for the Reachability Lemma + Theorem IBT-G:
the undetected set is *exactly* the equivariant operators, and a finite MR attains
it. NOT selection; pure linear algebra over the fault space.
"""
from __future__ import annotations

import numpy as np

TOL = 1e-9


def shift(N):
    S = np.zeros((N, N))
    for i in range(N):
        S[i, (i + 1) % N] = 1.0
    return S


def reversal(N):
    R = np.zeros((N, N))
    for i in range(N):
        R[i, N - 1 - i] = 1.0
    return R


def _commutator_jacobian(group_mats, N):
    """Stack, over A in group_mats, the linear map L |-> [L,A]=LA-AL acting on a
    basis of R^{NxN}. Returns J of shape (len*N*N, N*N): columns index vec(L)."""
    basis = []
    for a in range(N):
        for b in range(N):
            E = np.zeros((N, N)); E[a, b] = 1.0
            basis.append(E)                       # N^2 basis operators
    cols = []
    for E in basis:
        col = []
        for A in group_mats:
            col.append((E @ A - A @ E).ravel())   # [E,A] flattened
        cols.append(np.concatenate(col))
    return np.array(cols).T                        # (len*N^2, N^2)


def _rank_null(J):
    r = int(np.linalg.matrix_rank(J, tol=TOL))
    return r, J.shape[1] - r                       # rank, nullspace dim


def check(name, N, test_mats, dense_mats, analytic_equivariant_dim=None):
    Jt = _commutator_jacobian(test_mats, N)
    Jd = _commutator_jacobian(dense_mats, N)
    rt, nt = _rank_null(Jt)
    rd, nd = _rank_null(Jd)
    fa = (rt == rd)                                # nested => equal kernels iff equal rank
    print(f"\n=== {name} (N={N}) ===")
    print(f"  fault-space dim |Theta| = N^2 = {N*N}")
    print(f"  test witnesses (generators): {len(test_mats)}   "
          f"dense witnesses (whole group): {len(dense_mats)}")
    print(f"  rank(J_test) = {rt:3d}   rank(J_dense) = {rd:3d}")
    print(f"  undetected (kernel) dim: test = {nt:3d}   dense = {nd:3d}")
    print(f"  -> FA holds (finite test pins full commutant): {fa}")
    if analytic_equivariant_dim is not None:
        ok = (nd == analytic_equivariant_dim)
        print(f"  kernel == equivariant subspace?  dim {nd} == analytic "
              f"{analytic_equivariant_dim}: {ok}")
    return fa


def main():
    N = 8
    S, R = shift(N), reversal(N)
    print("Faithfulness rank check (IBT-G): undetected subspace = commutant; "
          "FA = finite generators pin the full commutant.")

    # 1) Translation Z_N: generator {S} vs all powers {S^1..S^{N-1}}.
    Sk = [np.linalg.matrix_power(S, k) for k in range(1, N)]
    fa1 = check("Translation Z_N  (advdiff translation-inv)", N,
                test_mats=[S], dense_mats=Sk,
                analytic_equivariant_dim=N)            # circulants: dim N

    # 2) Reflection Z_2: single nontrivial element {R}.
    fa2 = check("Reflection Z_2   (advdiff reflection-sym)", N,
                test_mats=[R], dense_mats=[R],
                analytic_equivariant_dim=2 * (N // 2) ** 2)  # commutant of R

    # 3) Dihedral D_N = <S, R>: 2 generators vs all 2N elements.
    dihedral = [np.linalg.matrix_power(S, k) for k in range(N)]
    dihedral += [np.linalg.matrix_power(S, k) @ R for k in range(N)]
    fa3 = check("Dihedral D_N     (translation + reflection)", N,
                test_mats=[S, R], dense_mats=dihedral)

    print("\n--- bridge to S10 advdiff (translation block) ---")
    print("  uniform advection-speed change c->c': operator stays constant-coeff")
    print("  => circulant => IN the Z_N kernel => UNDETECTED by translation MR")
    print("     (matches S10: advection_speed_error 0/n).")
    print("  inhomogeneous coeff c(x): operator non-circulant => OUTSIDE kernel")
    print("     => DETECTED (matches S10: coeff_inhomogeneity detected).")
    print(f"\nFA holds on all three symmetry instances: {fa1 and fa2 and fa3}")
    return 0 if (fa1 and fa2 and fa3) else 1


if __name__ == "__main__":
    raise SystemExit(main())
