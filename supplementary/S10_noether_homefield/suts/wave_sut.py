"""Self-contained NOETHER home-field slice: 1-D wave equation (hyperbolic PDE).

Authored here (no T2 dependency): leapfrog explicit FDM for u_tt = c^2 u_xx on
[0,1] with fixed ends u(0)=u(1)=0.

The wave equation is the deliberate CONTRAST to heat/radiation diffusion: it is
energy-CONSERVING and TIME-REVERSIBLE, so its operator algebra populates two
blocks that the dissipative SUTs leave empty -- exercising NOETHER's claim that
the block structure tracks the physics (candidate-list doc §4 note):
  - Conservation : discrete energy is (near-)conserved
  - T_rev*       : leapfrog is exactly time-reversible
  - O_le / G     : linearity, superposition, reflection symmetry

All MRs are oracle-free; tolerances fixed a priori (round-off, plus a generous
leapfrog energy-oscillation bound).
"""
from __future__ import annotations

import numpy as np

NX = 101
NT = 160
C = 1.0
CFL = 0.8                 # r = c*dt/dx = 0.8 < 1 (stable)
TOL = 1e-9               # exact-linear / exact-symmetric properties
TOL_REV = 1e-7           # time-reversal recovery (leapfrog reversible to round-off)
TOL_ENERGY = 5e-2        # leapfrog conserves a discrete energy up to bounded O(dt^2) oscillation

MR_BLOCKS = {
    "rho_linearity": "O_le",
    "rho_superpose": "O_le",
    "rho_reflect": "G",
    "rho_energy_conserve": "Conservation",
    "rho_time_reversal": "T_rev*",
}


def _x() -> np.ndarray:
    return np.linspace(0.0, 1.0, NX)


def ic_pulse(x0: float = 0.5) -> np.ndarray:
    u = np.exp(-180.0 * (_x() - x0) ** 2)
    u[0] = 0.0
    u[-1] = 0.0
    return u


def _l2(u: np.ndarray) -> float:
    return float(np.sqrt(np.sum(u * u)))


def _relerr(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.max(np.abs(a - b)) / (np.max(np.abs(b)) + 1e-15))


def _finite(*arrs: np.ndarray) -> bool:
    return all(np.all(np.isfinite(a)) for a in arrs)


# --- pristine operator pieces (monkeypatch targets) ---

def default_stencil(u_prev, u, r2):
    nxt = u.copy()
    nxt[1:-1] = (2.0 * u[1:-1] - u_prev[1:-1]
                 + r2 * (u[:-2] - 2.0 * u[1:-1] + u[2:]))
    return nxt


def default_bc(u):
    u = u.copy()
    u[0] = 0.0
    u[-1] = 0.0
    return u


def _pristine_ops() -> dict:
    return {"stencil": default_stencil, "bc": default_bc, "damp": 1.0, "cfl": CFL}


def _r2(ops) -> float:
    return (C * ops["cfl"]) ** 2  # r = c*dt/dx = cfl; r2 = (c*dt/dx)^2


def _leap(u_prev, u, ops, nt):
    r2 = _r2(ops)
    stencil, bc, damp = ops["stencil"], ops["bc"], ops["damp"]
    for _ in range(nt):
        u_next = bc(stencil(u_prev, u, r2)) * damp
        u_prev, u = u, u_next
    return u_prev, u


def solve(u0, ops, nt=NT):
    """Forward evolve from rest (zero initial velocity); return (u_prev, u)."""
    r2 = _r2(ops)
    u_prev = ops["bc"](u0.copy())
    u1 = u_prev.copy()
    u1[1:-1] = u_prev[1:-1] + 0.5 * r2 * (u_prev[:-2] - 2.0 * u_prev[1:-1] + u_prev[2:])
    u1 = ops["bc"](u1)
    return _leap(u_prev, u1, ops, nt - 1)


def _energy(u_prev, u, ops) -> float:
    v = (u - u_prev)                       # ~ velocity * dt (constant factor cancels in ratio)
    ux = np.gradient(u)
    return float(np.sum(v * v) + (C * ops["cfl"]) ** 2 * np.sum(ux * ux))


# --- MR battery (True iff the MR HOLDS) ---

def rho_linearity(ops):
    u0 = ic_pulse(0.5)
    _, a = solve(u0, ops)
    _, b = solve(3.7 * u0, ops)
    if not _finite(a, b):
        return False
    return _relerr(b, 3.7 * a) < TOL


def rho_superpose(ops):
    u1, u2 = ic_pulse(0.35), ic_pulse(0.65)
    _, s = solve(u1 + u2, ops)
    _, a = solve(u1, ops)
    _, b = solve(u2, ops)
    if not _finite(s, a, b):
        return False
    return _relerr(s, a + b) < TOL


def rho_reflect(ops):
    u0 = ic_pulse(0.3)
    _, out = solve(u0, ops)
    _, out_r = solve(u0[::-1], ops)
    if not _finite(out, out_r):
        return False
    return _relerr(out_r, out[::-1]) < TOL


def rho_energy_conserve(ops):
    u0 = ic_pulse(0.5)
    p0 = ops["bc"](u0.copy())
    e0 = _energy(p0, p0, ops)              # at rest: v=0 -> potential energy only
    pf, uf = solve(u0, ops)
    if not _finite(uf):
        return False
    ef = _energy(pf, uf, ops)
    if e0 <= 0:
        return True
    return abs(ef - e0) / e0 < TOL_ENERGY


def rho_time_reversal(ops):
    u0 = ic_pulse(0.5)
    pf, uf = solve(u0, ops)               # forward NT steps -> (prev, cur)
    if not _finite(uf):
        return False
    # reverse: run leapfrog from the swapped pair; should retrace to the start
    _, back = _leap(uf, pf, ops, NT - 1)
    return _relerr(ops["bc"](back), ops["bc"](u0)) < TOL_REV


BATTERY = {
    "rho_linearity": rho_linearity,
    "rho_superpose": rho_superpose,
    "rho_reflect": rho_reflect,
    "rho_energy_conserve": rho_energy_conserve,
    "rho_time_reversal": rho_time_reversal,
}


# --- operator-fault pool ---

def _stencil_damped_only(u_prev, u, r2):     # handled via ops["damp"], stencil unchanged
    return default_stencil(u_prev, u, r2)


def _stencil_drop_left(u_prev, u, r2):
    nxt = u.copy()
    nxt[1:-1] = 2.0 * u[1:-1] - u_prev[1:-1] + r2 * (-2.0 * u[1:-1] + u[2:])
    return nxt


def _stencil_inhomogeneous(u_prev, u, r2):
    nxt = u.copy()
    ramp = 1.0 + 0.5 * np.arange(1, len(u) - 1) / len(u)
    nxt[1:-1] = 2.0 * u[1:-1] - u_prev[1:-1] + r2 * ramp * (u[:-2] - 2.0 * u[1:-1] + u[2:])
    return nxt


def _stencil_first_order_drift(u_prev, u, r2):
    # add a spurious first-order advection term (breaks reflection parity + reversal)
    nxt = u.copy()
    nxt[1:-1] = (2.0 * u[1:-1] - u_prev[1:-1]
                 + r2 * (u[:-2] - 2.0 * u[1:-1] + u[2:])
                 + 0.05 * (u[2:] - u[1:-1]))
    return nxt


def _stencil_reorder(u_prev, u, r2):
    nxt = u.copy()
    nxt[1:-1] = (r2 * (u[2:] + u[:-2] - 2.0 * u[1:-1])
                 - u_prev[1:-1] + 2.0 * u[1:-1])
    return nxt


def _mut_ops(**ov) -> dict:
    ops = _pristine_ops()
    ops.update(ov)
    return ops


MUTATIONS = [
    ("wave_damping", "dissipation_fault", _mut_ops(damp=0.999)),
    ("wave_speed_x1p1", "wave_speed_error", _mut_ops(cfl=0.88)),  # self-consistent (CFL<1)
    ("wave_drop_left", "stencil_asymmetry", _mut_ops(stencil=_stencil_drop_left)),
    ("wave_inhomogeneous", "coeff_inhomogeneity", _mut_ops(stencil=_stencil_inhomogeneous)),
    ("wave_first_order_drift", "advective_contamination", _mut_ops(stencil=_stencil_first_order_drift)),
    ("wave_cfl_unstable", "time_integration_fault", _mut_ops(cfl=1.2)),  # r>1 -> blows up
    ("wave_baseline_noop", "baseline_control", _pristine_ops()),
    ("wave_baseline_reorder", "baseline_control", _mut_ops(stencil=_stencil_reorder)),
]


def _safe(fn, ops) -> bool:
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
        "sut": "wave-1d",
        "domain": "fluid",
        "equation": "u_tt = c^2 u_xx (1-D wave, fixed ends), leapfrog FDM",
        "impls": ["FDM"],
        "mr_blocks": MR_BLOCKS,
        "pristine_holds": pristine_holds,
        "genmorph": {
            "feasible": False,
            "reason": "field-valued u(x,t) I/O (D1); energy-conservation and "
                      "time-reversal MRs relate multiple structured executions (D3).",
            "expr_tier": "incl. time-reversal (multi-exec) -- beyond two-execution "
                         "(jir,jor) tier (D4)",
        },
        "records": records,
    }
