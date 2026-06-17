"""Self-contained NOETHER home-field slice: 1-D Poisson (elliptic PDE / steady heat).

Authored here (no T2 dependency): a 3-point central FDM solve of
    -u''(x) = f(x),  u(0)=u(1)=0
via numpy.linalg.solve on the interior tridiagonal system.

NOETHER block coverage:
  - O_le : linearity, superposition, positivity (f>=0 => u>=0; Green's function >0)
  - G    : reflection symmetry of -d^2/dx^2
  - L*   : grid self-convergence (Richardson ratio ~4 for O(dx^2)), oracle-free

All MRs are oracle-free; tolerances fixed a priori.
"""
from __future__ import annotations

import numpy as np

NX = 41
TOL = 1e-9
ROUND = 1e-9
RICH_LO, RICH_HI = 2.5, 6.0     # O(dx^2) Richardson self-convergence window

MR_BLOCKS = {
    "rho_linearity": "O_le",
    "rho_superpose": "O_le",
    "rho_reflect": "G",
    "rho_positivity": "O_le",
    "rho_grid_convergence": "L*",
}


def _x(nx: int = NX) -> np.ndarray:
    return np.linspace(0.0, 1.0, nx)


def f_mode(k: int = 1, nx: int = NX) -> np.ndarray:
    return np.sin(k * np.pi * _x(nx))


def f_bump(x0: float = 0.3, nx: int = NX) -> np.ndarray:
    return np.exp(-60.0 * (_x(nx) - x0) ** 2)


def _relerr(a, b):
    return float(np.max(np.abs(a - b)) / (np.max(np.abs(b)) + 1e-15))


def _finite(*arrs):
    return all(np.all(np.isfinite(a)) for a in arrs)


# --- pristine operator pieces (monkeypatch targets) ---

def default_build_A(n_int: int, dx: float) -> np.ndarray:
    A = (np.diag(np.full(n_int, 2.0))
         - np.diag(np.ones(n_int - 1), 1)
         - np.diag(np.ones(n_int - 1), -1)) / (dx * dx)
    return A


def default_rhs(f: np.ndarray) -> np.ndarray:
    return f


def _pristine_ops() -> dict:
    return {"build_A": default_build_A, "rhs": default_rhs}


def solve(f: np.ndarray, ops: dict) -> np.ndarray:
    nx = len(f)
    x = _x(nx)
    dx = x[1] - x[0]
    n_int = nx - 2
    A = ops["build_A"](n_int, dx)
    rhs = ops["rhs"](f)
    u = np.zeros(nx)
    u[1:-1] = np.linalg.solve(A, rhs[1:-1])
    return u


# --- MR battery (True iff the MR HOLDS) ---

def rho_linearity(ops):
    f = f_mode(1)
    a = solve(f, ops)
    b = solve(3.7 * f, ops)
    if not _finite(a, b):
        return False
    return _relerr(b, 3.7 * a) < TOL


def rho_superpose(ops):
    f1, f2 = f_mode(1), f_mode(2)
    s = solve(f1 + f2, ops)
    a = solve(f1, ops)
    b = solve(f2, ops)
    if not _finite(s, a, b):
        return False
    return _relerr(s, a + b) < TOL


def rho_reflect(ops):
    f = f_bump(0.3)
    out = solve(f, ops)
    out_r = solve(f[::-1], ops)
    if not _finite(out, out_r):
        return False
    return _relerr(out_r, out[::-1]) < TOL


def rho_positivity(ops):
    f = f_bump(0.4)                 # f >= 0 everywhere
    u = solve(f, ops)
    if not _finite(u):
        return False
    return u.min() >= -ROUND        # Green's function positive => u >= 0


def rho_grid_convergence(ops):
    # Richardson self-convergence on three grids; oracle-free (program-to-program).
    nxs = (21, 41, 81)
    sols = [solve(f_mode(1, nx), ops) for nx in nxs]
    if not _finite(*sols):
        return False
    d1 = float(np.max(np.abs(sols[0] - sols[1][::2])))
    d2 = float(np.max(np.abs(sols[1] - sols[2][::2])))
    if d2 < 1e-14:
        return True
    return RICH_LO <= (d1 / d2) <= RICH_HI


BATTERY = {
    "rho_linearity": rho_linearity,
    "rho_superpose": rho_superpose,
    "rho_reflect": rho_reflect,
    "rho_positivity": rho_positivity,
    "rho_grid_convergence": rho_grid_convergence,
}


# --- operator-fault pool ---

def _A_sign_flip(n_int, dx):
    return -default_build_A(n_int, dx)            # solves +u''=f -> wrong-sign solution


def _A_drop_lower(n_int, dx):
    A = (np.diag(np.full(n_int, 2.0))
         - np.diag(np.ones(n_int - 1), 1)) / (dx * dx)   # drop sub-diagonal: asymmetric
    return A


def _A_inhomogeneous(n_int, dx):
    ramp = 1.0 + 0.5 * np.arange(n_int) / n_int
    A = (np.diag(2.0 * ramp)
         - np.diag(np.ones(n_int - 1), 1)
         - np.diag(np.ones(n_int - 1), -1)) / (dx * dx)
    return A


def _A_dx_inconsistent(n_int, dx):
    off = (1.0 + dx)                              # dx-dependent -> breaks O(dx^2) convergence
    A = (np.diag(np.full(n_int, 2.0))
         - off * np.diag(np.ones(n_int - 1), 1)
         - off * np.diag(np.ones(n_int - 1), -1)) / (dx * dx)
    return A


def _A_coeff_x1p1(n_int, dx):
    return 1.1 * default_build_A(n_int, dx)       # stable, self-consistent (MT-undetectable)


def _A_reorder(n_int, dx):
    A = (-np.diag(np.ones(n_int - 1), -1)
         - np.diag(np.ones(n_int - 1), 1)
         + np.diag(np.full(n_int, 2.0))) / (dx * dx)   # same matrix, reordered build
    return A


def _rhs_offset(f):
    return f + 0.5                                # affine RHS -> breaks linearity/superposition


def _mut_ops(**ov):
    ops = _pristine_ops()
    ops.update(ov)
    return ops


MUTATIONS = [
    ("poisson_sign_flip", "sign_error", _mut_ops(build_A=_A_sign_flip)),
    ("poisson_drop_lower", "stencil_asymmetry", _mut_ops(build_A=_A_drop_lower)),
    ("poisson_inhomogeneous", "coeff_inhomogeneity", _mut_ops(build_A=_A_inhomogeneous)),
    ("poisson_dx_inconsistent", "consistency_fault", _mut_ops(build_A=_A_dx_inconsistent)),
    ("poisson_rhs_offset", "rhs_affine_fault", _mut_ops(rhs=_rhs_offset)),
    ("poisson_coeff_x1p1", "coefficient_error", _mut_ops(build_A=_A_coeff_x1p1)),
    ("poisson_baseline_noop", "baseline_control", _pristine_ops()),
    ("poisson_baseline_reorder", "baseline_control", _mut_ops(build_A=_A_reorder)),
]


def _safe(fn, ops):
    try:
        return bool(fn(ops))
    except Exception:
        return False


def evaluate() -> dict:
    pristine = _pristine_ops()
    pristine_holds = {m: _safe(fn, pristine) for m, fn in BATTERY.items()}
    records = []
    for mut_id, fc, ops in MUTATIONS:
        kills = {m: (not _safe(fn, ops)) for m, fn in BATTERY.items()}
        records.append({
            "mutant_id": mut_id, "fault_class": fc, "target_impl": "FDM",
            "baseline": (fc == "baseline_control"), "kills": kills,
        })
    return {
        "sut": "poisson-1d",
        "domain": "thermal",
        "equation": "-u'' = f (1-D Poisson / steady heat, Dirichlet), 3-point FDM",
        "impls": ["FDM"],
        "mr_blocks": MR_BLOCKS,
        "pristine_holds": pristine_holds,
        "genmorph": {
            "feasible": False,
            "reason": "field-valued u(x) I/O (D1); grid-convergence MR relates "
                      "multiple structured executions across grids (D3).",
            "expr_tier": "single-exec invariants + multi-grid relations -- beyond "
                         "two-execution (jir,jor) tier (D4)",
        },
        "records": records,
    }
