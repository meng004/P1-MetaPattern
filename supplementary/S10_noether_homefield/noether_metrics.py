"""Generation/detection metrics for the NOETHER home-field experiment.

Implements §2 of docs/tosem_maturity_2026-06-16/noether_homefield_benchmark_candidates.md.

SCOPE (salami red line, see §8 of the candidate-list doc): this module computes
ONLY generation/detection quantities (M-yield, M-block, M-detect with Wilson CI,
per-block / per-fault-class detection, optional paired McNemar against a
comparator MR set). It deliberately does NOT compute any selection quantity
(minimum-cover k*, reduction ratio, collapse/trichotomy, domination) -- those
are the sibling paper T2's claims and must not be reproduced here.

Pure standard library (math/json); no numpy/scipy dependency.
"""
from __future__ import annotations

import math
from typing import Any


# ---------------------------------------------------------------------------
# Interval + test statistics (closed-form; no scipy)
# ---------------------------------------------------------------------------

def wilson_ci(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Wilson score 95% CI for a binomial proportion k/n (z = 1.96 for 95%)."""
    if n <= 0:
        return (0.0, 1.0)
    p = k / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2.0 * n)) / denom
    half = (z * math.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n))) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def mcnemar_exact_p(b: int, c: int) -> float:
    """Two-sided exact McNemar p-value on discordant pair counts (b, c).

    b = # mutants killed by set A but not B; c = # killed by B but not A.
    Exact binomial test with p=0.5 on n=b+c discordant pairs.
    """
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) * (0.5 ** n)
    return min(1.0, 2.0 * tail)


# ---------------------------------------------------------------------------
# Summary over a detection result
# ---------------------------------------------------------------------------

def summarize(result: dict[str, Any]) -> dict[str, Any]:
    """Summarise one SUT's detection result into the §2 metric set.

    Expected `result` schema (produced by each SUT adapter's evaluate()):
        {
          "sut": str, "equation": str, "impls": [str, ...],
          "mr_blocks": {mr_id: noether_block},
          "genmorph": {"feasible": bool, "reason": str, "expr_tier": str},
          "records": [
            {"mutant_id": str, "fault_class": str, "target_impl": str,
             "baseline": bool, "kills": {mr_id: bool}},
            ...
          ],
        }
    """
    records = result["records"]
    mr_blocks = result["mr_blocks"]

    real = [r for r in records if not r["baseline"]]
    baseline = [r for r in records if r["baseline"]]

    # Alignment gate (§2.1): every baseline_control equivalent must SURVIVE all
    # MRs (= original program sanity). A killed baseline means the harness is
    # mis-aligned and the numbers are not trustworthy.
    baseline_killers = [
        {"mutant_id": r["mutant_id"],
         "killed_by": [m for m, k in r["kills"].items() if k]}
        for r in baseline if any(r["kills"].values())
    ]
    alignment_ok = (len(baseline_killers) == 0)

    n_real = len(real)
    killed_real = [r for r in real if any(r["kills"].values())]
    k = len(killed_real)
    lo, hi = wilson_ci(k, n_real)

    # M-block: distinct non-empty NOETHER blocks spanned by the MR set
    blocks = sorted(set(mr_blocks.values()))

    # Per-block detection: a real mutant is "block-detected" if any MR of that
    # block flags it.
    per_block = {}
    for blk in blocks:
        blk_mrs = [m for m, b in mr_blocks.items() if b == blk]
        det = [r for r in real if any(r["kills"].get(m, False) for m in blk_mrs)]
        plo, phi = wilson_ci(len(det), n_real)
        per_block[blk] = {
            "mrs": sorted(blk_mrs),
            "detected": len(det), "n": n_real,
            "rate": (len(det) / n_real) if n_real else 0.0,
            "wilson95": [round(plo, 4), round(phi, 4)],
        }

    # Per-fault-class detection.
    fault_classes = sorted(set(r["fault_class"] for r in real))
    per_fault = {}
    for fc in fault_classes:
        grp = [r for r in real if r["fault_class"] == fc]
        det = [r for r in grp if any(r["kills"].values())]
        per_fault[fc] = {"detected": len(det), "n": len(grp),
                         "rate": (len(det) / len(grp)) if grp else 0.0}

    # Per-MR kill counts (over real mutants).
    per_mr = {}
    for m in mr_blocks:
        cnt = sum(1 for r in real if r["kills"].get(m, False))
        per_mr[m] = {"block": mr_blocks[m], "kills": cnt}

    return {
        "sut": result["sut"],
        "equation": result["equation"],
        "impls": result["impls"],
        "domain": result.get("domain"),
        "execution_mode": result.get("execution_mode", "executed-here"),
        "provenance": result.get("provenance"),
        "cross_impl": result.get("cross_impl"),
        "calibration": result.get("calibration"),
        "genmorph": result.get("genmorph", {}),
        "alignment_ok": alignment_ok,
        "baseline_killers": baseline_killers,
        "M_yield": len(mr_blocks),                 # # non-vacuous MRs derived
        "M_block": len(blocks),                    # # NOETHER blocks covered
        "blocks_covered": blocks,
        "M_detect": {
            "killed": k, "n_real_mutants": n_real,
            "rate": (k / n_real) if n_real else 0.0,
            "wilson95": [round(lo, 4), round(hi, 4)],
            "underpowered": n_real < 10,           # CLAUDE.md C6 honesty flag
        },
        "per_block": per_block,
        "per_fault_class": per_fault,
        "per_mr": per_mr,
    }


def paired_mcnemar(records_a: list[dict], records_b: list[dict]) -> dict[str, Any]:
    """Paired McNemar on two MR sets over the SAME mutant list (per-mutant
    killed-by->=1 indicator). Used only when a comparator arm (e.g. LLM-MR)
    is supplied; on array-I/O SUTs GenMorph is typically infeasible (see
    each SUT's `genmorph.feasible`), in which case this is not applicable.
    """
    by_id_b = {r["mutant_id"]: any(r["kills"].values()) for r in records_b}
    b = c = 0
    for r in records_a:
        ka = any(r["kills"].values())
        kb = by_id_b.get(r["mutant_id"], False)
        if ka and not kb:
            b += 1
        elif kb and not ka:
            c += 1
    return {"b_only_A": b, "c_only_B": c, "mcnemar_p": mcnemar_exact_p(b, c)}
