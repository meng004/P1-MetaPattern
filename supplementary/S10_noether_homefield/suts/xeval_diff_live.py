"""LIVE cross-implementation differential oracles for the multi-implementation
T2 SUTs (radxfer, grayscott), executed here -- not read from committed matrices.

Same neutral-oracle principle as advdiff_xeval_diff, generalized to the correct
form for SUTs whose two implementations may share monkeypatch targets:

    under each mutation, run BOTH implementations and compare their output fields;
    a mutant is detected iff the two implementations DISAGREE by more than a
    calibrated tolerance tau = SAFETY * delta, where delta is the legitimate
    pristine cross-implementation gap (normalized by initial amplitude, §10.2).

Consequence (this is a feature, and a live confirmation of ANALYSIS.md IBT-3):
faults that patch code SHARED by both implementations (radxfer absorption /
scatter / source operators) are COMMON-MODE -- both implementations fault
identically, still agree, and are therefore invisible to the differential
oracle. Faults in implementation-specific operators (FD diffusion stencil / theta;
SP symbol / etd) break one side only and are detected. The differential oracle's
detection kernel is thus exactly the common-mode set.

NO selection / k* / collapse is computed. Provenance: substrate solvers/mutations
= Minimum-MR-SubSet mcmr.{radxfer,grayscott}.
"""
from __future__ import annotations

import sys

import numpy as np

from suts.advdiff_sut import _resolve_t2_scripts

SAFETY = 5.0
SENS_FACTORS = (1.5, 2.0, 3.0, 5.0, 10.0)


def _ensure_path():
    root = _resolve_t2_scripts()
    if root is None:
        raise ImportError(
            "T2 substrate not found; set T2_ROOT to Minimum-MR-SubSet/scripts.")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))


def _l2(x) -> float:
    x = np.real(np.asarray(x, dtype=complex)).astype(float)
    return float(np.sqrt(np.sum(x ** 2)))


def _fielddiff(a, b, scale: float) -> float:
    a = np.real(np.asarray(a, dtype=complex)).astype(float)
    b = np.real(np.asarray(b, dtype=complex)).astype(float)
    return float(np.sqrt(np.sum((a - b) ** 2))) / (scale + 1e-15)


def _core(solve_field, probes, scales, mutations, apply_ctx):
    """Generic differential loop. Returns (delta, tau, records, sensitivity).

    solve_field(impl, case) -> ndarray field
    apply_ctx(mut)          -> context manager applying the mutation
    each mut has .id, .fault_class, .target_impl
    """
    # calibration: pristine cross-impl gap
    gaps = []
    for case, scale in zip(probes, scales):
        with np.errstate(all="ignore"):
            ea = solve_field("A", case)
            eb = solve_field("B", case)
        gaps.append(_fielddiff(ea, eb, scale))
    delta = max(gaps)
    tau = SAFETY * delta

    records = []
    for mut in mutations:
        diff_max = 0.0
        try:
            with apply_ctx(mut):
                with np.errstate(all="ignore"):
                    for case, scale in zip(probes, scales):
                        ea = solve_field("A", case)   # impl A under mutation
                        eb = solve_field("B", case)   # impl B under mutation
                        diff_max = max(diff_max, _fielddiff(ea, eb, scale))
            detected = diff_max > tau
        except Exception:
            detected, diff_max = True, float("inf")
        records.append({
            "mutant_id": mut.id,
            "fault_class": mut.fault_class,
            "target_impl": mut.target_impl,
            "baseline": (mut.fault_class == "baseline_control"),
            "kills": {"xeval-differential": bool(detected)},
            "diff_max": (None if diff_max == float("inf") else round(diff_max, 6)),
        })

    def _dm(r):
        return float("inf") if r["diff_max"] is None else r["diff_max"]
    reals = [r for r in records if not r["baseline"]]
    bases = [r for r in records if r["baseline"]]
    sensitivity = [{
        "safety": s, "tau": round(s * delta, 6),
        "detected": sum(_dm(r) > s * delta for r in reals), "n_real": len(reals),
        "baseline_false_positives": sum(_dm(r) > s * delta for r in bases),
        "n_baseline": len(bases),
    } for s in SENS_FACTORS]
    return delta, tau, records, sensitivity


def _result(sut, domain, equation, impls, delta, tau, records, sensitivity, prov):
    return {
        "sut": sut, "domain": domain, "equation": equation, "impls": impls,
        "execution_mode": "executed-here",
        "mr_blocks": {"xeval-differential": "E*"},
        "calibration": {
            "method": "tau = SAFETY * max-probe pristine cross-impl reldiff (§10.2); "
                      "both impls run UNDER the mutation (common-mode-aware)",
            "safety_factor": SAFETY, "n_probes": len(sensitivity) and None,
            "pristine_gap_delta": round(delta, 6), "tau": round(tau, 6),
            "sensitivity_posthoc": sensitivity,
        },
        "cross_impl": {"impls": impls, "enabled": True,
                       "oracle": "neutral per-field differential (no ground truth); "
                                 "common-mode faults are in the oracle's kernel (IBT-3)"},
        "genmorph": {"feasible": False,
                     "reason": "G×N×N (radxfer) / N×N field comparison across two "
                               "full PDE solves per case; neutral cross-impl oracle.",
                     "expr_tier": "method-comparison oracle (E*), beyond (jir,jor) (D4)"},
        "provenance": prov,
        "records": records,
    }


# --------------------------------------------------------------------------
# radxfer (multigroup radiation diffusion): M-FD-theta vs M-SP-IMEX
# --------------------------------------------------------------------------

def evaluate_radxfer(G: int = 2) -> dict:
    _ensure_path()
    import mcmr.radxfer.solvers as solvers
    import mcmr.radxfer.mr_battery as battery
    import mcmr.radxfer.mutations as mutations

    impl_map = {"A": "M-FD-θ", "B": "M-SP-IMEX"}

    def solve_field(tag, case):
        return solvers.solve(impl_map[tag], case, G)["E"]

    probes = [
        battery._make_case(battery._ic_smooth(G)),
        battery._make_case(battery._ic_symmetric(G)),
        battery._make_case(battery._ic_checkerboard(G)),
    ]
    scales = [_l2(c["E0"]) for c in probes]
    muts = mutations.build_mutations(G)

    def apply_ctx(mut):
        return mut.patch()

    delta, tau, records, sens = _core(solve_field, probes, scales, muts, apply_ctx)
    return _result(
        sut=f"radxfer-G{G}-diff", domain="thermal",
        equation=("multigroup radiation diffusion (1/c)dE_g/dt=div(D_g grad E_g)"
                  f"-sigma_a,g E_g+scatter (2-D periodic, G={G})"),
        impls=["M-FD-theta", "M-SP-IMEX"],
        delta=delta, tau=tau, records=records, sensitivity=sens,
        prov="substrate: Minimum-MR-SubSet mcmr.radxfer; differential oracle "
             "executed here; absorption/scatter/source faults are common-mode "
             "(shared operators), diffusion/stencil/theta/etd are impl-specific.")


# --------------------------------------------------------------------------
# grayscott (reaction-diffusion, two fields U,V): M-FD-IMEX vs M-SP-IMEX
# --------------------------------------------------------------------------

def _gs_ic(battery, cx: float, cy: float):
    x, y = battery._grid()
    seed = np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * 0.05 ** 2))
    return 1.0 - 0.5 * seed, 0.25 * seed


def evaluate_grayscott() -> dict:
    _ensure_path()
    import mcmr.grayscott.solvers as solvers
    import mcmr.grayscott.mr_battery as battery
    import mcmr.grayscott.mutations as mutations

    impl_map = {"A": "M-FD-IMEX", "B": "M-SP-IMEX"}

    def solve_field(tag, case):
        r = solvers.solve(impl_map[tag], case)
        return np.stack([np.asarray(r["U"]), np.asarray(r["V"])])

    u0a, v0a = battery._default_IC()
    u0b, v0b = _gs_ic(battery, 0.35, 0.6)
    u0c, v0c = _gs_ic(battery, 0.65, 0.4)
    probes = [battery._make_case(u0a, v0a),
              battery._make_case(u0b, v0b),
              battery._make_case(u0c, v0c)]
    scales = [_l2(np.stack([c["U0"], c["V0"]])) for c in probes]
    muts = list(mutations.MUTATIONS)

    def apply_ctx(mut):
        return mut.patch()

    delta, tau, records, sens = _core(solve_field, probes, scales, muts, apply_ctx)
    return _result(
        sut="grayscott-diff", domain="fluid",
        equation="2-D Gray-Scott reaction-diffusion (U,V), periodic",
        impls=["M-FD-IMEX", "M-SP-IMEX"],
        delta=delta, tau=tau, records=records, sensitivity=sens,
        prov="substrate: Minimum-MR-SubSet mcmr.grayscott; differential oracle "
             "executed here; target_impl='both' faults patch shared operators "
             "(common-mode, in the oracle kernel).")
