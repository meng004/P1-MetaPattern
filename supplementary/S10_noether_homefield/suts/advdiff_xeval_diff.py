"""LIVE cross-implementation per-field differential oracle for advection-diffusion.

This executes what the MR adapter (advdiff_sut) deliberately deferred:
    "A per-field differential oracle needs discretisation-aware tolerance
     (doc §10.2) and is left to the calibrated harness; not fabricated here."

Neutral oracle (no ground truth): the two independent solvers M-FV (finite
volume / Crank-Nicolson) and M-SP (Fourier spectral) are run on the SAME case.
A mutation targets exactly one implementation's operators (FV ops and SP ops are
disjoint in the substrate), so the OTHER implementation stays a clean reference.
A mutant is DETECTED iff the mutated implementation's output field diverges from
the clean implementation's field by more than a calibrated tolerance tau.

§10.2 tolerance calibration ("discretisation difference != defect"): tau is set
ABOVE the legitimate pristine cross-implementation gap,
    tau = SAFETY * delta_pristine,   delta_pristine = max over probes of d(FV,SP),
with SAFETY fixed a priori. Baselines must stay below tau (false-positive gate).

This is `executed-here` (真跑), distinct from the algebra-derived MR battery and
from the reused committed matrices. It exercises the E* method-comparison block.
NO selection / k* / collapse is computed.

Provenance: substrate solvers/mutations = Minimum-MR-SubSet mcmr.pde_xeval.
"""
from __future__ import annotations

import numpy as np

from suts.advdiff_sut import _PATCH_ATTRS, _import_substrate

SAFETY = 5.0   # a-priori margin above the legitimate discretisation gap (doc §10.2)


def _l2(x: np.ndarray) -> float:
    x = np.real(np.asarray(x, dtype=complex)).astype(float)
    return float(np.sqrt(np.sum(x ** 2)))


def _fielddiff(a: np.ndarray, b: np.ndarray, scale: float) -> float:
    """Field difference as a fraction of a FIXED amplitude scale (the initial
    condition norm). Normalizing by the *evolved* field would blow up for modes
    that diffuse to ~0 (tiny/tiny), manufacturing spurious cross-impl gaps; the
    initial amplitude is the stable, physically meaningful normalizer (§10.2)."""
    a = np.real(np.asarray(a, dtype=complex)).astype(float)
    b = np.real(np.asarray(b, dtype=complex)).astype(float)
    return float(np.sqrt(np.sum((a - b) ** 2))) / (scale + 1e-15)


def _probe_cases(battery) -> list[dict]:
    """Fixed probe suite (varied ICs); identical for calibration and detection."""
    return [
        battery._base_case(battery._gaussian(0.5, 0.5)),
        battery._base_case(battery._gaussian(0.35, 0.6)),
        battery._base_case(battery._mode(1, 0)),
        battery._base_case(battery._mode(1, 1)),
        battery._base_case(battery._mode(2, 1)),
    ]


def evaluate() -> dict:
    solvers, battery, mutations = _import_substrate()
    probes = _probe_cases(battery)

    # --- calibration: legitimate pristine cross-implementation gap ---
    scales = [_l2(c["u0"]) for c in probes]    # fixed per-probe amplitude scale
    gaps = []
    for case, scale in zip(probes, scales):
        u_fv = solvers.solve("M-FV", case)["u"]
        u_sp = solvers.solve("M-SP", case)["u"]
        gaps.append(_fielddiff(u_fv, u_sp, scale))
    delta = max(gaps)
    tau = SAFETY * delta

    # --- per-mutant differential detection (mutated impl vs clean other impl) ---
    records = []
    for want in ("M-FV", "M-SP"):
        other = "M-SP" if want == "M-FV" else "M-FV"
        for mut in [m for m in mutations.MUTATIONS if m.target_impl == want]:
            saved = {a: getattr(solvers, a) for a in _PATCH_ATTRS
                     if hasattr(solvers, a)}
            diff_max = 0.0
            try:
                mut.apply(solvers)
                with np.errstate(all="ignore"):   # unstable mutants overflow -> still detected
                    for case, scale in zip(probes, scales):
                        u_t = solvers.solve(want, case)["u"]    # mutated target impl
                        u_o = solvers.solve(other, case)["u"]   # clean reference impl
                        diff_max = max(diff_max, _fielddiff(u_t, u_o, scale))
                detected = diff_max > tau
            except Exception:
                detected, diff_max = True, float("inf")     # crash = divergence
            finally:
                for a, orig in saved.items():
                    setattr(solvers, a, orig)
            records.append({
                "mutant_id": mut.id,
                "fault_class": mut.fault_class,
                "target_impl": want,
                "baseline": (mut.fault_class == "baseline_control"),
                "kills": {"xeval-differential": bool(detected)},
                "diff_max": (None if diff_max == float("inf") else round(diff_max, 6)),
            })

    # Post-hoc sensitivity of the margin choice (transparency; NOT tuned to
    # outcome -- the headline uses the pre-set SAFETY above). Shows the §10.2
    # tension: tightening the margin gains detection but risks baseline false
    # positives once tau approaches the legitimate discretisation gap.
    def _dm(r):
        return float("inf") if r["diff_max"] is None else r["diff_max"]
    reals = [r for r in records if not r["baseline"]]
    bases = [r for r in records if r["baseline"]]
    sensitivity = []
    for s in (1.5, 2.0, 3.0, 5.0, 10.0):
        tau_s = s * delta
        sensitivity.append({
            "safety": s, "tau": round(tau_s, 6),
            "detected": sum(_dm(r) > tau_s for r in reals),
            "n_real": len(reals),
            "baseline_false_positives": sum(_dm(r) > tau_s for r in bases),
            "n_baseline": len(bases),
        })

    cfg = solvers.CONFIG
    return {
        "sut": "advdiff-xeval-diff",
        "domain": "thermal×fluid",
        "equation": ("u_t + c.grad(u) = alpha*lap(u) (2-D advection-diffusion, "
                     f"periodic; N={cfg['N']}, alpha={cfg['alpha']}, "
                     f"c=({cfg['cx']},{cfg['cy']}), T={cfg['T']})"),
        "impls": ["M-FV", "M-SP"],
        "execution_mode": "executed-here",
        "mr_blocks": {"xeval-differential": "E*"},
        "calibration": {
            "method": "tau = SAFETY * max-probe pristine cross-impl reldiff (doc §10.2)",
            "safety_factor": SAFETY,
            "n_probes": len(probes),
            "pristine_gap_per_probe": [round(g, 6) for g in gaps],
            "pristine_gap_delta": round(delta, 6),
            "tau": round(tau, 6),
            "sensitivity_posthoc": sensitivity,
        },
        "cross_impl": {"impls": ["M-FV", "M-SP"], "enabled": True,
                       "oracle": "neutral per-field differential (no ground truth)"},
        "genmorph": {
            "feasible": False,
            "reason": "N x N field comparison across two PDE solves per case (D1-D2); "
                      "neutral cross-impl oracle, not a single-program GP target.",
            "expr_tier": "method-comparison oracle (E*), beyond (jir,jor) tier (D4)",
        },
        "provenance": "substrate: Minimum-MR-SubSet mcmr.pde_xeval (solvers, "
                      "mutations); differential oracle executed here; no selection.",
        "records": records,
    }
