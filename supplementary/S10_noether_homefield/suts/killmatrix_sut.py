"""NOETHER home-field slices ingested from committed T2 kill matrices.

Sanctioned reuse path (empirical_reuse_from_T2.md §2, candidate-list doc §8):
"the SAME kill matrix -- T2 asks the selection question (minimum cover), NOETHER
asks the generation question (do the algebra-derived MRs detect sufficiently?)".
This adapter reads a committed `kill_matrix.csv` (a detection matrix produced by
the shared mutation/cross-implementation harness) and computes GENERATION /
DETECTION metrics only. It does NOT read or reproduce any selection artefact
(REPORT.md / minimize.json / abd_witness_report.json: k*, collapse, SMS).

IMPORTANT honesty label: these SUTs are `execution_mode = "reused-committed-matrix"`
-- the detection data was produced by an earlier T2 run, NOT re-executed here
(contrast heat/wave/poisson = "executed-here", advdiff = "executed-here-via-substrate").

Kill-matrix schema (long form):
    sut, mutant_id, fault_class, mr_id, mr_meta_pattern, trial_id,
    killed, residual, tolerance, seed, status
"""
from __future__ import annotations

import csv
import os
from pathlib import Path

# T2 mr_meta_pattern -> NOETHER block.
META_TO_BLOCK = {
    "m_balance": "Conservation",
    "m_conv": "L*",
    "m_inv": "G",
    "m_lin": "O_le",
    "m_mono": "O_le",
    "m_spec": "G",
}


def _runs_dir() -> Path | None:
    if os.environ.get("T2_ROOT"):
        scripts = Path(os.environ["T2_ROOT"])
    else:
        scripts = (Path(__file__).resolve().parents[3].parent
                   / "Minimum-MR-SubSet" / "scripts")
    runs = scripts.parent / "runs"
    return runs if runs.exists() else None


def _find_csv(glob_pat: str) -> Path | None:
    runs = _runs_dir()
    if runs is None:
        return None
    cands = sorted(runs.glob(f"{glob_pat}/kill_matrix.csv"))
    return cands[-1] if cands else None     # newest (UTC-timestamped dir names sort)


# Committed-matrix SUT specs (thermal / fluid / reactor home field).
SPECS = {
    "radxfer": {
        "glob": "abd-witness-radxfer-G2-2d-*",
        "sut": "radxfer-G2", "domain": "thermal",
        "equation": "multigroup radiation diffusion (1/c)∂E_g/∂t=∇·(D_g∇E_g)"
                    "-σ_a,gE_g+scatter (2-D periodic), G=2",
        "impls": ["M-FD-theta", "M-SP-IMEX"], "cross_impl": True,
    },
    "grayscott": {
        "glob": "abd-witness-grayscott-xeval-2d-*",
        "sut": "grayscott", "domain": "fluid",
        "equation": "2-D Gray-Scott reaction-diffusion (u,v)",
        "impls": ["M-FD-IMEX", "M-SP-IMEX"], "cross_impl": True,
    },
    "detonation": {
        "glob": "abd-witness-detonation-znd-1d-*",
        "sut": "detonation-znd", "domain": "fluid",
        "equation": "1-D reactive Euler / ZND detonation (Arrhenius)",
        "impls": ["reactive_euler_znd"], "cross_impl": False,
    },
    "combustion": {
        "glob": "abd-witness-combustion-gri30-*",
        "sut": "combustion-gri30", "domain": "thermal",
        "equation": "adiabatic const-UV 0-D reactor, GRI-Mech 3.0 (53 sp.)",
        "impls": ["M-CANTERA", "M-PYODE"], "cross_impl": True,
    },
    "pincell": {
        "glob": "abd-witness-metbench-pincell-xeval-*",
        "sut": "pincell-xeval", "domain": "reactor",
        "equation": "2-group neutron transport, pin-cell (OpenMC vs OpenMOC)",
        "impls": ["openmc", "openmoc"], "cross_impl": True,
    },
}


def available(name: str) -> bool:
    spec = SPECS.get(name)
    return bool(spec) and _find_csv(spec["glob"]) is not None


def _evaluate(name: str) -> dict:
    spec = SPECS[name]
    csv_path = _find_csv(spec["glob"])
    if csv_path is None:
        raise ImportError(
            f"committed kill matrix for {name!r} not found "
            f"(glob {spec['glob']}); set T2_ROOT to Minimum-MR-SubSet/scripts.")

    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))

    # mr_id -> NOETHER block (via mr_meta_pattern).
    mr_blocks = {}
    for r in rows:
        mr_blocks.setdefault(
            r["mr_id"], META_TO_BLOCK.get(r["mr_meta_pattern"], "Other"))

    # group by (impl, mutant_id) -> record.
    groups: dict[tuple, dict] = {}
    for r in rows:
        key = (r["sut"], r["mutant_id"])
        rec = groups.setdefault(key, {
            "mutant_id": r["mutant_id"], "fault_class": r["fault_class"],
            "target_impl": r["sut"],
            "baseline": (r["fault_class"] == "baseline_control"),
            "kills": {},
        })
        rec["kills"][r["mr_id"]] = (str(r["killed"]).strip().lower() == "true")

    runs_root = _runs_dir()
    prov = str(csv_path.relative_to(runs_root.parent)) if runs_root else str(csv_path)
    return {
        "sut": spec["sut"],
        "equation": spec["equation"],
        "domain": spec["domain"],
        "impls": spec["impls"],
        "mr_blocks": mr_blocks,
        "execution_mode": "reused-committed-matrix",
        "provenance": f"T2 committed detection matrix: {prov} "
                      f"(detection-only reuse; selection artefacts not read).",
        "cross_impl": {"impls": spec["impls"], "enabled": spec["cross_impl"]},
        "genmorph": {
            "feasible": False,
            "reason": "field / trajectory / eigenvalue I/O; per-eval is a full "
                      "PDE / kinetics / transport solve; structural MRs relate "
                      "multiple executions (D1–D3).",
            "expr_tier": "beyond two-execution (jir,jor) tier (D4)",
        },
        "records": list(groups.values()),
    }


def make_evaluate(name: str):
    return lambda: _evaluate(name)
