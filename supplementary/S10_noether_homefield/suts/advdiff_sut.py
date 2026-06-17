"""NOETHER home-field slice: 2-D advection-diffusion, cross-implementation.

Equation:  u_t + c.grad(u) = alpha * laplacian(u)  on a periodic unit square.

This adapter REUSES the sibling-repo (T2, Minimum-MR-SubSet) operator-algebra
substrate -- the two independent solvers (M-FV finite-volume/Crank-Nicolson and
M-SP Fourier spectral), the algebra-derived MR battery, and the operator-fault
pool -- and runs a GENERATION/DETECTION loop over them.

Salami red line (candidate-list doc §8): this adapter computes ONLY per-(mutant,
MR) detection. It deliberately does NOT call T2's selection machinery
(abd_collect / abd_structure: k*, minimum cover, collapse/trichotomy, SMS rank).
Substrate provenance is attributed below; upstream solvers/mutations are cited.

Provenance:
  mcmr.pde_xeval.solvers / mr_battery / mutations  (Minimum-MR-SubSet)
T2 path resolution: env T2_ROOT, else the sibling checkout next to this repo.
"""
from __future__ import annotations

import os
import sys
import traceback
from pathlib import Path

# NOETHER block per (algebra-derived) MR id in the reused battery.
MR_BLOCKS = {
    "linearity-scale": "O_le",
    "superposition": "O_le",
    "translation-inv": "G",
    "reflection-sym": "G",
    "mass-conservation": "Conservation",
    "energy-decay": "L*",
    "max-principle": "O_le",
    "spectral-decay-scaling": "G",
    "phase-scaling": "G",
    "galilean-inv": "G",
    "richardson-self": "L*",
}

_PATCH_ATTRS = [
    "laplacian_operator", "advection_operator", "cn_step", "apply_periodic_bc",
    "wavenumbers", "spectral_laplacian_symbol", "spectral_advection_symbol",
    "etd_step",
]


def _resolve_t2_scripts() -> Path | None:
    cands = []
    if os.environ.get("T2_ROOT"):
        cands.append(Path(os.environ["T2_ROOT"]))
    here = Path(__file__).resolve()
    # repo is <root>/P1-MetaPattern ; sibling checkout <root>/Minimum-MR-SubSet/scripts
    cands.append(here.parents[3].parent / "Minimum-MR-SubSet" / "scripts")
    for c in cands:
        if (c / "mcmr" / "pde_xeval" / "solvers.py").exists():
            return c
    return None


def available() -> bool:
    return _resolve_t2_scripts() is not None


def _import_substrate():
    root = _resolve_t2_scripts()
    if root is None:
        raise ImportError(
            "T2 substrate not found. Set T2_ROOT to the Minimum-MR-SubSet/scripts "
            "directory (the shared advection-diffusion solvers + MR battery)."
        )
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    import mcmr.pde_xeval.solvers as solvers
    import mcmr.pde_xeval.mr_battery as battery
    import mcmr.pde_xeval.mutations as mutations
    return solvers, battery, mutations


def _mr_holds(impl: str, mr: dict, battery) -> bool:
    """True iff the MR holds (mutant survives); error -> killed (False)."""
    try:
        base = battery.build_base_case(mr)
        follow = mr["transform"](base)
        src = battery.solve_for_mr(impl, base, mr)
        fol = battery.solve_for_mr(impl, follow, mr)
        return bool(mr["assertion"](src, fol))
    except Exception:
        return False


def evaluate() -> dict:
    solvers, battery, mutations = _import_substrate()

    records = []
    for impl, want in (("M-FV", "M-FV"), ("M-SP", "M-SP")):
        muts = [m for m in mutations.MUTATIONS if m.target_impl == want]
        for mut in muts:
            saved = {a: getattr(solvers, a) for a in _PATCH_ATTRS
                     if hasattr(solvers, a)}
            kills = {}
            try:
                mut.apply(solvers)
                for mr in battery.MR_BATTERY:
                    kills[mr["mr_id"]] = (not _mr_holds(impl, mr, battery))
            except Exception:
                for mr in battery.MR_BATTERY:
                    kills[mr["mr_id"]] = True   # apply failed -> killed on all
            finally:
                for a, orig in saved.items():
                    setattr(solvers, a, orig)
            records.append({
                "mutant_id": mut.id,
                "fault_class": mut.fault_class,
                "target_impl": impl,
                "baseline": (mut.fault_class == "baseline_control"),
                "kills": kills,
            })

    cfg = solvers.CONFIG
    return {
        "sut": "advdiff-2d",
        "domain": "thermal×fluid",
        "equation": ("u_t + c.grad(u) = alpha*lap(u) (2-D advection-diffusion, "
                     f"periodic; N={cfg['N']}, alpha={cfg['alpha']}, "
                     f"c=({cfg['cx']},{cfg['cy']}), T={cfg['T']})"),
        "impls": ["M-FV", "M-SP"],
        "mr_blocks": MR_BLOCKS,
        "genmorph": {
            "feasible": False,
            "reason": "N x N field I/O (D1); each fitness eval is a sparse-LU / "
                      "spectral PDE solve (D2); scaling/Galilean/Richardson MRs "
                      "relate multiple structured executions (D3).",
            "expr_tier": "beyond two-execution (jir,jor) tier (D4)",
        },
        "cross_impl": {
            "impls": ["M-FV", "M-SP"],
            "note": "E* method-comparison block exercised by two independent "
                    "implementations (Phase B). A per-field differential oracle "
                    "needs discretisation-aware tolerance (doc §10.2) and is left "
                    "to the calibrated harness; not fabricated here.",
        },
        "provenance": "substrate: Minimum-MR-SubSet mcmr.pde_xeval (solvers, "
                      "mr_battery, mutations); detection-only, no selection.",
        "records": records,
    }
