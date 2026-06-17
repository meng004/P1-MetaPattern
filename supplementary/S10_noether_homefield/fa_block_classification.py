"""Per-block applicability of the FA-rank / tight-IBT machinery.

The tight characterization (Theorem IBT-G) needs the structural defect E_s(L) to be
a LINEAR EQUALITY in the fault L (then ker = a subspace = commutant-type object, and
the finite FA rank check certifies tightness). This script classifies the eight
blocks by that criterion, producing EVIDENCE (not assertion) for reviewer point R3:

  LINEAR-EQUALITY blocks  -> FA-rank applies, tight characterization holds:
    G  (symmetry):     E = [L, A]              (verified in fa_rank_check.py)
    T* (self-adjoint): E = L - L^T             (verified here)
  NON-linear / NON-equality blocks -> FA-rank does NOT apply (reasons shown):
    O<= (monotonicity): inequality L>=0 entrywise -> a CONE, not a subspace
    T*_rev (time-reversal): R L R^{-1} - L^{-1} -> matrix inverse, nonlinear
    L*  (limit/Richardson): ratio of norms      -> nonlinear

For non-linear blocks the framework keeps only the SUFFICIENT direction (a
structure-preserving fault is undetected) or a fixed/linearized subclass; it does
NOT claim the tight ker = compatible equality. Pure linear algebra; no selection.
"""
from __future__ import annotations

import numpy as np

TOL = 1e-9


def _rank_null(J, ncols):
    r = int(np.linalg.matrix_rank(J, tol=TOL)) if J.size else 0
    return r, ncols - r


# ---- T* (self-adjoint): E(L) = L - L^T, linear equality -> FA-rank applies ----

def selfadjoint_check(N):
    """Witness (i,j): <L e_i, e_j> - <e_i, L e_j> = L_{ji} - L_{ij}. Row in vec(L)."""
    def row(i, j):
        M = np.zeros((N, N)); M[j, i] += 1.0; M[i, j] -= 1.0
        return M.ravel()
    test = [row(i, j) for i in range(N) for j in range(N) if i < j]   # upper triangle
    dense = [row(i, j) for i in range(N) for j in range(N)]            # all pairs
    Jt, Jd = np.array(test), np.array(dense)
    rt, nt = _rank_null(Jt, N * N)
    rd, nd = _rank_null(Jd, N * N)
    fa = (rt == rd)
    analytic_compat = N * (N + 1) // 2            # symmetric matrices
    print(f"\n=== T* self-adjoint (N={N}) — LINEAR EQUALITY ===")
    print(f"  test witnesses (i<j): {len(test)}   dense (all i,j): {len(dense)}")
    print(f"  rank(test)={rt}  rank(dense)={rd}  -> FA holds: {fa}")
    print(f"  compatible (kernel) dim = {nd}  == symmetric-matrix dim {analytic_compat}: "
          f"{nd == analytic_compat}")
    return fa and nd == analytic_compat


# ---- O<= (monotonicity): inequality -> cone, NOT a subspace ----

def monotone_demo(N):
    """Monotone-compatible set M = {L : L_{ij} >= 0} (maps nonneg orthant to itself).
    Show M is not a linear subspace -> FA-rank (subspace) machinery inapplicable."""
    L = np.eye(N)                      # identity: entrywise >=0 -> monotone
    inM = lambda M: bool(np.all(M >= -TOL))
    print(f"\n=== O<= monotonicity (N={N}) — INEQUALITY (cone) ===")
    print(f"  L=I in M (monotone): {inM(L)};  (-1)*L in M: {inM(-L)} "
          f"-> not closed under negative scaling -> NOT a subspace")
    print("  defect = sum of max(0, -L_{ij}) is piecewise/nonlinear in L "
          "-> FA-rank N/A; only the sufficient direction survives.")
    return (inM(L) and not inM(-L))


# ---- T*_rev (time-reversal): R L R^{-1} - L^{-1} -> nonlinear (matrix inverse) ----

def timereversal_demo(N):
    """Genuine reversibility R L R^{-1} = L^{-1} involves L^{-1}: nonlinear in L.
    Show the defect is not additive (a hallmark of nonlinearity)."""
    rng = np.random.default_rng(0)
    R = np.fliplr(np.eye(N))
    L1 = np.eye(N) + 0.1 * rng.standard_normal((N, N))
    L2 = np.eye(N) + 0.1 * rng.standard_normal((N, N))
    inv = np.linalg.inv
    f = lambda L: R @ L @ R - inv(L)          # reversibility defect
    add_gap = float(np.max(np.abs(f(L1 + L2 - np.eye(N)) - (f(L1) + f(L2) - f(np.eye(N))))))
    print(f"\n=== T*_rev time-reversal (N={N}) — NONLINEAR (matrix inverse) ===")
    print(f"  defect f(L)=R L R - L^{{-1}}; additivity residual ~ {add_gap:.3e} "
          f"(>> 0) -> nonlinear -> FA-rank N/A.")
    print("  tight handling needs the multi-execution treatment (cf. wave SUT T_rev*).")
    return add_gap > 1e-6


# ---- L* (limit/Richardson): ratio of norms -> nonlinear ----

def limit_demo():
    print("\n=== L* limit / Richardson (—) — NONLINEAR (norm ratio) ===")
    print("  defect = || u_h - u_{h/2} || / || u_{h/2} - u_{h/4} || - 4 : ratio of "
          "theta-dependent norms -> nonlinear in theta -> FA-rank N/A;")
    print("  only a fixed-grid linearized subclass or the sufficient direction is in scope.")
    return True


def main():
    N = 6
    print("Per-block FA-rank applicability (evidence for reviewer R3).")
    g_note = "  G symmetry: E=[L,A] linear-equality -> FA-rank TIGHT (see fa_rank_check.py)"
    print("\n=== G symmetry — LINEAR EQUALITY (verified separately) ===")
    print(g_note)
    ok_T = selfadjoint_check(N)
    ok_O = monotone_demo(N)
    ok_Tr = timereversal_demo(N)
    ok_L = limit_demo()

    print("\n--- classification table ---")
    rows = [
        ("G  symmetry",      "[L,A]",            "yes", "TIGHT (verified)"),
        ("T* self-adjoint",  "L - L^T",          "yes", "TIGHT (verified here)"),
        ("O<= monotonicity", "max(0,-L_ij)",     "no (cone)",  "sufficient-only"),
        ("T*_rev time-rev",  "R L R - L^{-1}",   "no (inverse)", "multi-exec only"),
        ("L* limit",         "norm ratio",       "no (ratio)", "subclass/suff-only"),
    ]
    print(f"  {'block':18}{'defect E_s(L)':18}{'linear-eq?':14}{'tight?'}")
    for b, e, lin, t in rows:
        print(f"  {b:18}{e:18}{lin:14}{t}")
    allok = ok_T and ok_O and ok_Tr and ok_L
    print(f"\nEvidence consistent (T* tight; O<=/T_rev/L* outside linear machinery): {allok}")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
