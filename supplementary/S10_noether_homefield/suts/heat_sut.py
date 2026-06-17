"""Self-contained NOETHER home-field slice: 1-D heat conduction (parabolic PDE).

Fully authored in this repository (no T2 dependency): a textbook explicit-FDM
heat solver with monkeypatchable operator pieces, an operator-algebra MR
battery whose relations are DERIVED FROM the diffusion operator's algebra, and
a plausible operator-fault pool (including baseline_control equivalents).

Equation:  u_t = alpha * u_xx  on [0,1], homogeneous Dirichlet u(0)=u(1)=0.

NOETHER block coverage of the MR battery (see candidate-list doc §1/§5):
  - O_le : linearity, superposition, maximum principle (monotone/linear)
  - G    : spatial reflection symmetry (constant-coefficient operator)
  - L*   : energy dissipation + steady-state limit
Empty blocks (documented honestly, the "proves what it cannot derive" point):
  - T_rev* = empty  (heat is irreversible / dissipative)
  - Conservation = empty under Dirichlet BC (heat leaves through the boundary)

All MRs are oracle-free (relate program outputs to each other only); tolerances
are fixed a priori from IEEE-754 round-off, never tuned to outcomes.
"""
from __future__ import annotations

import numpy as np

NX = 41
NT = 80
ALPHA = 0.2
TOL = 1e-9          # exact-linear / exact-symmetric properties: round-off only
ROUND = 1e-9        # absolute round-off allowance for bound oracles

# NOETHER block per MR id.
MR_BLOCKS = {
    "rho_linearity": "O_le",
    "rho_superpose": "O_le",
    "rho_reflect": "G",
    "rho_maxprinciple": "O_le",
    "rho_energy_decay": "L*",
    "rho_steady_limit": "L*",
}


# ---------------------------------------------------------------------------
# Initial conditions
# ---------------------------------------------------------------------------

def _x() -> np.ndarray:
    return np.linspace(0.0, 1.0, NX)


def ic_sin(mode: int = 1) -> np.ndarray:
    return np.sin(mode * np.pi * _x())


def ic_bump(x0: float = 0.5) -> np.ndarray:
    return np.exp(-80.0 * (_x() - x0) ** 2)


def _l2(u: np.ndarray) -> float:
    return float(np.sqrt(np.sum(u * u)))


def _relerr(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.max(np.abs(a - b)) / (np.max(np.abs(b)) + 1e-15))


def _finite(*arrs: np.ndarray) -> bool:
    return all(np.all(np.isfinite(a)) for a in arrs)


# ---------------------------------------------------------------------------
# Pristine operator pieces (monkeypatch targets)
# ---------------------------------------------------------------------------

def default_stencil(u: np.ndarray, coeff: float) -> np.ndarray:
    nxt = u.copy()
    nxt[1:-1] = u[1:-1] + coeff * (u[:-2] - 2.0 * u[1:-1] + u[2:])
    return nxt


def default_bc(u: np.ndarray) -> np.ndarray:
    u = u.copy()
    u[0] = 0.0
    u[-1] = 0.0
    return u


def _pristine_ops() -> dict:
    return {"stencil": default_stencil, "bc": default_bc, "dt_factor": 0.45}


# ---------------------------------------------------------------------------
# Solver (operator pieces taken from `ops`)
# ---------------------------------------------------------------------------

def solve(u0: np.ndarray, ops: dict, nt: int = NT) -> np.ndarray:
    x = _x()
    dx = x[1] - x[0]
    dt = ops["dt_factor"] * dx * dx / ALPHA
    coeff = ALPHA * dt / (dx * dx)
    u = ops["bc"](u0.copy())
    stencil = ops["stencil"]
    bc = ops["bc"]
    for _ in range(nt):
        u = bc(stencil(u, coeff))
    return u


# ---------------------------------------------------------------------------
# Operator-algebra MR battery (each returns True iff the MR HOLDS)
# ---------------------------------------------------------------------------

def rho_linearity(ops: dict) -> bool:
    u0 = ic_sin(1)
    a = solve(u0, ops)
    b = solve(3.7 * u0, ops)
    if not _finite(a, b):
        return False
    return _relerr(b, 3.7 * a) < TOL


def rho_superpose(ops: dict) -> bool:
    u1, u2 = ic_sin(1), ic_sin(2)
    s = solve(u1 + u2, ops)
    a = solve(u1, ops)
    b = solve(u2, ops)
    if not _finite(s, a, b):
        return False
    return _relerr(s, a + b) < TOL


def rho_reflect(ops: dict) -> bool:
    # Evaluate parity at a moderate horizon (a priori NT//4) where the field is
    # still O(1); a symmetry test on a fully-decayed (~0) field is vacuous.
    u0 = ic_bump(0.3)               # asymmetric IC
    nt = max(1, NT // 4)
    out = solve(u0, ops, nt)
    out_r = solve(u0[::-1], ops, nt)   # solve(reflect(u0)) == reflect(solve(u0))
    if not _finite(out, out_r):
        return False
    return _relerr(out_r, out[::-1]) < TOL


def rho_maxprinciple(ops: dict) -> bool:
    u0 = ic_bump(0.5)
    out = solve(u0, ops)
    if not _finite(out):
        return False
    # homogeneous Dirichlet injects the boundary value 0 into the bounds.
    lo = min(0.0, float(u0.min()))
    hi = max(0.0, float(u0.max()))
    return (out.min() >= lo - ROUND) and (out.max() <= hi + ROUND)


def rho_energy_decay(ops: dict) -> bool:
    u0 = ic_bump(0.5)
    out = solve(u0, ops)
    if not _finite(out):
        return False
    e0, e1 = _l2(u0), _l2(out)
    return (e1 <= e0 + 1e-12) and (e1 >= 0.0)   # dissipative, non-growing, finite


def rho_steady_limit(ops: dict) -> bool:
    u0 = ic_sin(1)
    e1 = _l2(solve(u0, ops, NT))
    e2 = _l2(solve(u0, ops, 2 * NT))
    if not np.isfinite(e1) or not np.isfinite(e2):
        return False
    return e2 < e1 + 1e-12                       # monotone approach to steady 0


BATTERY = {
    "rho_linearity": rho_linearity,
    "rho_superpose": rho_superpose,
    "rho_reflect": rho_reflect,
    "rho_maxprinciple": rho_maxprinciple,
    "rho_energy_decay": rho_energy_decay,
    "rho_steady_limit": rho_steady_limit,
}


# ---------------------------------------------------------------------------
# Operator-fault pool (plausible bugs in the operator code)
# ---------------------------------------------------------------------------

def _stencil_sign_flip(u, coeff):
    nxt = u.copy()
    nxt[1:-1] = u[1:-1] - coeff * (u[:-2] - 2.0 * u[1:-1] + u[2:])   # anti-diffusion
    return nxt


def _stencil_coeff_x1p1(u, coeff):
    # +10% diffusion coefficient: STABLE (0.45*1.1 = 0.495 < 0.5) and
    # self-consistent, so every oracle-free algebra MR still holds. An honest
    # example of a real fault MT cannot detect without an oracle (doc §10.2).
    nxt = u.copy()
    nxt[1:-1] = u[1:-1] + (1.1 * coeff) * (u[:-2] - 2.0 * u[1:-1] + u[2:])
    return nxt


def _stencil_drop_left(u, coeff):
    nxt = u.copy()
    nxt[1:-1] = u[1:-1] + coeff * (-2.0 * u[1:-1] + u[2:])           # asymmetric
    return nxt


def _stencil_inhomogeneous(u, coeff):
    nxt = u.copy()
    ramp = 1.0 + 0.5 * np.arange(1, len(u) - 1) / len(u)            # space-varying coeff
    nxt[1:-1] = u[1:-1] + coeff * ramp * (u[:-2] - 2.0 * u[1:-1] + u[2:])
    return nxt


def _bc_source(u):
    u = u.copy()
    u[0] = 0.0
    u[-1] = 0.0
    u[len(u) // 2] += 0.02                                          # affine source term
    return u


def _stencil_reorder(u, coeff):
    nxt = u.copy()
    nxt[1:-1] = u[1:-1] + coeff * (u[2:] + u[:-2] - 2.0 * u[1:-1])  # same value, reordered
    return nxt


def _mut_ops(**overrides) -> dict:
    ops = _pristine_ops()
    ops.update(overrides)
    return ops


MUTATIONS = [
    ("heat_lap_sign_flip", "sign_error", _mut_ops(stencil=_stencil_sign_flip)),
    ("heat_coeff_x1p1", "diffusion_coeff_error", _mut_ops(stencil=_stencil_coeff_x1p1)),
    ("heat_drop_left", "stencil_asymmetry", _mut_ops(stencil=_stencil_drop_left)),
    ("heat_inhomogeneous", "coeff_inhomogeneity", _mut_ops(stencil=_stencil_inhomogeneous)),
    ("heat_bc_source", "boundary_source_fault", _mut_ops(bc=_bc_source)),
    ("heat_unstable", "time_integration_fault", _mut_ops(dt_factor=0.8)),
    # baseline_control equivalents -- MUST survive every MR (alignment gate)
    ("heat_baseline_noop", "baseline_control", _pristine_ops()),
    ("heat_baseline_reorder", "baseline_control", _mut_ops(stencil=_stencil_reorder)),
]


# ---------------------------------------------------------------------------
# evaluate() -- detection result in the schema noether_metrics.summarize expects
# ---------------------------------------------------------------------------

def _safe(fn, ops) -> bool:
    try:
        return bool(fn(ops))
    except Exception:
        return False


def evaluate() -> dict:
    # Pristine sanity: every MR must hold on the unmutated solver.
    pristine = _pristine_ops()
    pristine_holds = {mid: _safe(fn, pristine) for mid, fn in BATTERY.items()}

    records = []
    for mut_id, fault_class, ops in MUTATIONS:
        kills = {mid: (not _safe(fn, ops)) for mid, fn in BATTERY.items()}
        records.append({
            "mutant_id": mut_id,
            "fault_class": fault_class,
            "target_impl": "FDM",
            "baseline": (fault_class == "baseline_control"),
            "kills": kills,
        })

    return {
        "sut": "heat-1d",
        "domain": "thermal",
        "equation": "u_t = alpha*u_xx (1-D heat conduction, Dirichlet), explicit FDM",
        "impls": ["FDM"],
        "mr_blocks": MR_BLOCKS,
        "pristine_holds": pristine_holds,
        "genmorph": {
            "feasible": False,
            "reason": "array-valued field I/O u(x); GP assertion grammar targets "
                      "scalar/tuple I/O (D1). Conservation/scaling/reflection MRs "
                      "relate multiple structured executions (D3).",
            "expr_tier": "single-exec invariants + multi-exec structured relations "
                         "(beyond GenMorph's two-execution (jir,jor) tier, D4)",
        },
        "records": records,
    }
