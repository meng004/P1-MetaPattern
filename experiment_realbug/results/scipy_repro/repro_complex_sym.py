"""
NOETHER block: T* self-adjoint / symmetric structure (scipy.linalg.solve + inv).
Fix commit: 50951d25c "BUG: linalg: fix `inv`, `solve` for complex symmetric inputs (#24367)"
            (scipy 1.18 dev; gh-24359). Parent (pre) = d292d3221.

Bug: scipy 1.18 rewrote inv/solve in C++ (_linalg_inv.hh / _linalg_solve.hh).
     For a COMPLEX SYMMETRIC matrix (A == A^T but A != A^H, i.e. symmetric
     but NOT Hermitian), the new posdef-fallback flow mis-detected the
     structure. The old is_sym_herm() collapsed "symmetric" and "hermitian"
     into a single flag and, in the auto-detect path, routed a complex
     symmetric matrix to the POS_DEF / Hermitian (?hetrf) branch and used
     conjugating triangle-fill. zpotrf on a non-pos-def complex symmetric
     matrix does not error, so inv/solve returned a WRONG inverse silently,
     and inv(a, assume_a='sym') disagreed with inv(a) (general).
     The fix splits is_sym_or_herm() into (is_symm, is_herm) and routes
     complex-symmetric-not-hermitian to the SYM (?sytrf) branch with
     non-conjugating triangle-fill.

MR (T* structure block, representation/structure invariance):
   Symmetry of A is a PROPERTY, not a different problem. Exploiting the
   symmetric structure must not change the (unique) correct solution:
        solve(A, b, assume_a='sym') == solve(A, b)        [general]
        inv(A, assume_a='sym')      == inv(A)             [general]
   and the recovered inverse must actually invert A: X @ A == I.
   SUT: the exact gh-24359 matrix -- complex symmetric, non-Hermitian,
        and NOT positive definite (so the pos-def Cholesky fallback is
        the trigger).
   Source     : general solve/inv (no structure assumption) -- reference.
   Follow-up  : solve/inv with assume_a='sym' (exploit symmetric structure).
   Violation (FIRED): the 'sym' and general results disagree (and at least
        one of them fails X@A==I). On the parent commit it is the general
        auto-detect path that returns a non-inverse (max|X@A-I| ~ 9.1), while
        assume_a='sym' is correct; the fix makes both paths agree and correct.
"""
import numpy as np
from scipy.linalg import solve, inv
import scipy

print("scipy version:", scipy.__version__)

# Exact gh-24359 matrix: complex symmetric (a == a.T), NOT hermitian (a != a.conj().T),
# and NOT positive definite.
a = np.asarray([[182.56985285 - 64.28859483j, -177.24879835 + 11.0780499j],
                [-177.24879835 + 11.0780499j,  177.24879835 - 11.0780499j]])
b = np.eye(2)

# Sanity: confirm the structure assumed by the MR.
is_symm = np.allclose(a, a.T)
is_herm = np.allclose(a, a.conj().T)
print(f"  is_symmetric (a==a.T)   : {is_symm}")
print(f"  is_hermitian (a==a.conj().T): {is_herm}")
assert is_symm and not is_herm, "test matrix must be complex symmetric, not hermitian"

TOL = 1e-10
I2 = np.eye(2)
fired = False

# ---- solve: general and symmetric-structure paths must agree AND invert a ----
x_gen = solve(a, b)                      # reference (general, no structure)
x_sym = solve(a, b, assume_a="sym")      # follow-up (exploit symmetric structure)
solve_gen_resid = np.max(np.abs(x_gen @ a - I2))   # general really inverts a?
solve_sym_resid = np.max(np.abs(x_sym @ a - I2))   # sym path really inverts a?
solve_sym_dev = np.max(np.abs(x_sym - x_gen))      # MR: paths must agree
print(f"  solve : max|x_gen@a - I|        = {solve_gen_resid:.3e}")
print(f"  solve : max|x_sym@a - I|        = {solve_sym_resid:.3e}")
print(f"  solve : max|x_sym - x_gen|      = {solve_sym_dev:.3e}")

# ---- inv: general and symmetric-structure paths must agree AND invert a ----
inv_gen = inv(a)                         # reference (general, no structure)
inv_sym = inv(a, assume_a="sym")         # follow-up (exploit symmetric structure)
inv_gen_resid = np.max(np.abs(inv_gen @ a - I2))
inv_sym_resid = np.max(np.abs(inv_sym @ a - I2))
inv_sym_dev = np.max(np.abs(inv_sym - inv_gen))
print(f"  inv   : max|inv_gen@a - I|      = {inv_gen_resid:.3e}")
print(f"  inv   : max|inv_sym@a - I|      = {inv_sym_resid:.3e}")
print(f"  inv   : max|inv_sym - inv_gen|  = {inv_sym_dev:.3e}")

# MR fires if (a) the two structure-paths disagree, or (b) either path fails to
# invert a. Both are equivalent statements of "symmetry is a property, exploiting
# it (or not) must yield the one correct inverse".
worst_resid = max(solve_gen_resid, solve_sym_resid, inv_gen_resid, inv_sym_resid)
if solve_sym_dev > TOL or inv_sym_dev > TOL or worst_resid > TOL:
    fired = True
    # Report which path(s) actually returned a non-inverse, data-accurately.
    bad = []
    if solve_gen_resid > TOL: bad.append(f"solve(general) X@a-I={solve_gen_resid:.2e}")
    if solve_sym_resid > TOL: bad.append(f"solve(sym) X@a-I={solve_sym_resid:.2e}")
    if inv_gen_resid > TOL:   bad.append(f"inv(general) X@a-I={inv_gen_resid:.2e}")
    if inv_sym_resid > TOL:   bad.append(f"inv(sym) X@a-I={inv_sym_resid:.2e}")
    print(f"    >>> MR VIOLATED (FIRED): general and 'sym' paths disagree "
          f"(solve dev={solve_sym_dev:.3e}, inv dev={inv_sym_dev:.3e}). "
          f"Non-inverting path(s): {', '.join(bad) if bad else 'none'} -- "
          f"complex-symmetric A was routed to the wrong (pos-def/Hermitian) branch.")
else:
    print(f"    MR HELD: general and assume_a='sym' agree (<= {TOL:.0e}) and both "
          f"invert a (max X@a-I={worst_resid:.2e}); structure exploited without "
          f"changing the correct solution.")

print("VERDICT:", "FIRED" if fired else "HELD")
