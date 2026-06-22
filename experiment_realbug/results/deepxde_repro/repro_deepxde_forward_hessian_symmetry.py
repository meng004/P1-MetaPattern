#!/usr/bin/env python
"""
NOETHER pde_sciml T* self-adjoint block -- DeepXDE forward-mode (JAX) Hessian operator
symmetry.

Target bug   : DeepXDE commit 46e2c2e "Backend jax: Bug fix in forward-mode gradients
               (#1591)"
NOETHER block: T* self-adjoint / operator-symmetry (the Hessian of a scalar field is a
               SELF-ADJOINT operator: H[i,j] == H[j,i] -- the discrete mixed-partial /
               Schwarz symmetry; the self-adjointness the T* block tests).
Module       : deepxde/gradients/gradients_forward.py  Jacobian.__call__ (dim_y==1
               branch) and hessian().
Commit pair  : PRE  = parent 9d9d0b0 (1.10.1.dev12+g9d9d0b0f7)
               POST = fix    46e2c2e (1.10.1.dev13+g46e2c2e8a; first released in v1.10.1)

*** REACHABILITY CAVEAT (read first) ***
At BOTH the pre and post commits, deepxde/gradients/__init__.py imports the
REVERSE-mode autodiff (`from .gradients_reverse import ...`) and the forward-mode
import is commented out. So forward-mode AD was NOT reachable through the public
`deepxde.grad.jacobian/hessian` default path at these commits -- it was a
developer module under active construction, reachable only by an explicit
`from deepxde.gradients.gradients_forward import jacobian, hessian` (or forward-mode
config in later versions). The buggy state therefore never shipped in the user-DEFAULT
path of a released tag. This makes the bug WEAKER than a clean default-path
released-to-released positive; it is recorded honestly with this caveat. The defect
itself is a genuine, upstream-fixed operator self-adjointness violation, reproduced at
the commit level via git worktrees + per-commit installs (the protocol's source-build
allowance), and the executed code object is byte-for-byte the repo source at the commit.

Root cause
----------
The forward-mode Jacobian cache self.J is keyed by the INPUT-axis index j (it stores
dy/dx_j computed via jax.jvp along the basis tangent e_j). The dim_y==1 branch returned

    self.J[i]    # PRE  (parent 9d9d0b0) -- indexed by OUTPUT row i (always 0 here)

so every requested column k returned column 0. Off-diagonal Hessian entries built by
composing two forward Jacobians then become wrong and ASYMMETRIC. The fix indexes by
the input column:

    self.J[j]    # POST (46e2c2e)

The same commit also defaults hessian(component=None) -> 0 (PRE raised
TypeError: '<=' not supported between 'int' and 'NoneType' because jacobian(i=None)
hit `0 <= i`).

Metamorphic relation (T* self-adjoint / operator symmetry)
----------------------------------------------------------
The Hessian of a scalar field is a self-adjoint operator: H[i,j] == H[j,i] for all i,j
(mixed-partial / Schwarz symmetry). For f(x0,x1) = sin(x0)*x1^2 + 3*x0*x1 (dim_y=1,
dim_x=2, non-zero cross term so an index swap is detectable), forward-mode AD must give
a SYMMETRIC and CORRECT Hessian.

    FIRED <=> the forward Jacobian returns the wrong column (col k -> col 0), so the
              Hessian is wrong/asymmetric (and component=None crashes with TypeError).
    HELD  <=> Jacobian columns correct; Hessian symmetric (H[0,1]==H[1,0]) and correct
              vs the analytic Hessian.

The script loads the EXACT gradients_forward.py source at the chosen commit in
isolation (stubbing only the deepxde.backend symbols it imports: backend_name='jax',
jax), because the module is not wired into the public package at these commits and
pulling full deepxde would drag in flax.

Usage:
    <jax_venv>/bin/python repro_deepxde_forward_hessian_symmetry.py \
        <jax_venv>/lib/pythonX.Y/site-packages/deepxde/gradients/gradients_forward.py
PRE venv: deepxde @ 9d9d0b0 ; POST venv: deepxde @ 46e2c2e ; both with jax[cpu]==0.4.23,
numpy<2, x64 enabled. CPU milliseconds, no net, no training.
"""
import importlib.util
import sys
import types

import numpy as np

SRC = sys.argv[1]  # absolute path to gradients_forward.py at the chosen commit

import jax
import jax.numpy as jnp

jax.config.update("jax_enable_x64", True)

# Stub parent package `deepxde.backend` exposing what the file imports:
#   `from ..backend import backend_name, jax`
pkg_deepxde = types.ModuleType("deepxde")
pkg_deepxde.__path__ = []
backend_mod = types.ModuleType("deepxde.backend")
backend_mod.backend_name = "jax"
backend_mod.jax = jax
pkg_deepxde.backend = backend_mod
sys.modules["deepxde"] = pkg_deepxde
sys.modules["deepxde.backend"] = backend_mod

spec = importlib.util.spec_from_file_location(
    "deepxde.gradients.gradients_forward", SRC
)
gf = importlib.util.module_from_spec(spec)
sys.modules["deepxde.gradients.gradients_forward"] = gf
spec.loader.exec_module(gf)
print(f"[loaded] {SRC}")


def f_point(x):
    # x: shape (2,) -> returns shape (1,)  (dim_y = 1).  Cross term => H[0,1] != 0.
    return jnp.array([jnp.sin(x[0]) * x[1] ** 2 + 3.0 * x[0] * x[1]])


xs = jnp.array([[0.3, 0.7], [1.1, -0.4], [-0.6, 0.9]], dtype=jnp.float64)
ys = (jax.vmap(f_point)(xs), f_point)


def analytic_hessian(x0, x1):
    H00 = -np.sin(x0) * x1 ** 2
    H01 = 2 * np.cos(x0) * x1 + 3.0
    H11 = 2 * np.sin(x0)
    return np.array([[H00, H01], [H01, H11]])


def to_np(v):
    if isinstance(v, tuple):
        v = v[0]
    return np.asarray(v)


print("\n=== ORACLE 1: forward-mode Jacobian column correctness ===")
jac_status = "n/a"
try:
    gf.jacobian._Jacobians.clear()
    J0 = to_np(gf.jacobian(ys, xs, i=0, j=0)).reshape(-1)
    J1 = to_np(gf.jacobian(ys, xs, i=0, j=1)).reshape(-1)
    x0 = np.asarray(xs)[:, 0]
    x1 = np.asarray(xs)[:, 1]
    true_J0 = np.cos(x0) * x1 ** 2 + 3 * x1
    true_J1 = 2 * np.sin(x0) * x1 + 3 * x0
    err_J0 = float(np.max(np.abs(J0 - true_J0)))
    err_J1 = float(np.max(np.abs(J1 - true_J1)))
    print(f"  J col0 computed = {J0}")
    print(f"  J col1 computed = {J1}")
    print(f"  J col1 analytic = {true_J1}   max|err| = {err_J1:.3e}")
    jac_status = "OK" if (err_J0 < 1e-8 and err_J1 < 1e-8) else \
        f"WRONG (errs {err_J0:.2e},{err_J1:.2e})"
except Exception as e:  # noqa: BLE001
    jac_status = f"CRASH: {type(e).__name__}: {e}"
    print(f"  Jacobian raised: {type(e).__name__}: {e}")
print(f"  --> Jacobian-correctness verdict: {jac_status}")

print("\n=== ORACLE 2 (T* self-adjoint): Hessian symmetry H[i,j] == H[j,i] ===")
hess_status = "n/a"
try:
    H = np.zeros((len(np.asarray(xs)), 2, 2))
    raw = {}
    for i in range(2):
        for j in range(2):
            gf.jacobian._Jacobians.clear()
            try:
                gf.hessian._Hessians.clear()
            except Exception:
                pass
            v = to_np(gf.hessian(ys, xs, component=None, i=i, j=j)).reshape(-1)
            raw[(i, j)] = v
            H[:, i, j] = v
    sym_gap = float(np.max(np.abs(H[:, 0, 1] - H[:, 1, 0])))
    print(f"  H[0,1] = {raw[(0,1)]}")
    print(f"  H[1,0] = {raw[(1,0)]}")
    print(f"  max|H[0,1]-H[1,0]| (symmetry gap) = {sym_gap:.3e}")
    Xn = np.asarray(xs)
    max_corr_err = max(
        float(np.max(np.abs(H[k] - analytic_hessian(Xn[k, 0], Xn[k, 1]))))
        for k in range(Xn.shape[0])
    )
    print(f"  max|H - H_analytic| (full matrix) = {max_corr_err:.3e}")
    hess_status = "SYMMETRIC+CORRECT" if (sym_gap < 1e-8 and max_corr_err < 1e-8) \
        else "VIOLATED"
except Exception as e:  # noqa: BLE001
    hess_status = f"CRASH: {type(e).__name__}: {e}"
    print(f"  Hessian raised: {type(e).__name__}: {e}")
print(f"  --> T* self-adjoint Hessian-symmetry verdict: {hess_status}")

fired = (not jac_status.startswith("OK")) or (not str(hess_status).startswith("SYMMETRIC"))
print("\n=== SUMMARY ===")
print(f"  jacobian_column_correctness = {jac_status}")
print(f"  hessian_symmetry            = {hess_status}")
print(f"  NOETHER-T* MR_RESULT = {'FIRED' if fired else 'HELD'}  "
      f"(PRE 9d9d0b0 expected FIRED / POST 46e2c2e expected HELD)")
