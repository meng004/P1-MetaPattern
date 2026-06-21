#!/usr/bin/env python3
"""rho_mono — redundant-point / redundant-row stability metamorphic relation
(Set N, adapted from the paper's O_le "point-density monotonicity" MR).

Paper source (NOETHER_paper_arxiv.tex, L864-866): rho_mono is the
"point-density-monotonicity MR for the O_le block (top-1 stability under removal
of a small fraction of redundant input points)", derived from the O_le^train
operator restricted to inference-time input perturbations.

APPLICABILITY VERDICT: ADAPTABLE.
  The paper's literal phrasing ("top-1 stability") is a *classifier-level*
  property: it presupposes a trained model emitting a class ranking. That layer
  is NOT_APPLICABLE to a pure library function, and we do not contort it.
  What IS portable is the underlying O_le MetaPattern: removing input elements
  that are *redundant* for the operation must leave the operation's output stable
  within tolerance. For e3nn / PyTorch-Geometric this instantiates directly on
  reduction / aggregation library functions:
    - scatter_max / scatter_min / segment reductions: appending a duplicate of an
      existing (index,value) row is redundant for an idempotent reduce -> output
      must be unchanged. A bug that double-counts, mis-dedups, or uses the wrong
      reduce surfaces here.
    - pooling / message aggregation where a strictly-dominated (redundant) point
      should not move the pooled feature beyond tol.
  The MR is GENERAL: it does not know which bug it faces. The repro snippet must
  declare, via ctx, what "redundant" means for THIS op. We never fabricate a
  relation tuned to a specific defect.

Interface: mr_rho_mono(fn, ctx, tol) -> {"status", "detail"}  (see README.md)

ctx must provide ONE of two redundancy specifications:

 (A) Reduction-stability form (idempotent reduce ops; scatter_max/min/segment):
   ctx["x"]            : base input the op accepts (torch.Tensor / np.ndarray).
   ctx["add_redundant"]: callable add_redundant(x) -> x_aug that appends rows
                         which are REDUNDANT under the op's intended reduce
                         (e.g. a duplicate (index,value) pair for scatter_max).
                         fn(x_aug) MUST equal fn(x) within tol. Op-specific,
                         supplied by the bug's repro snippet.

 (B) Drop-redundant form (pooling / general O_le monotonicity):
   ctx["x"]            : base input.
   ctx["drop_redundant"] : callable drop_redundant(x) -> x_small that removes a
                         small fraction of points flagged redundant for the op
                         (e.g. strictly dominated points for a max-pool).
                         fn(x_small) MUST equal fn(x) within tol.

If neither key is present, the op is not redundancy-typed for this bug ->
NOT_APPLICABLE (distinct from 'held'; excluded from this set's denominator).

A pre-fix bug that breaks redundancy stability -> relation VIOLATED -> 'fired'.
An exception under the perturbed input that the FIXED code does not raise also
counts as 'fired' (post-fix sanity run filters false positives). CPU-only,
no training, no full forward pass.
"""
import numpy as np

try:
    import torch
    _HAS_TORCH = True
except Exception:  # noqa: BLE001
    _HAS_TORCH = False


def _to_np(a):
    if _HAS_TORCH and isinstance(a, torch.Tensor):
        return a.detach().cpu().numpy()
    return np.asarray(a)


def _compare(ref, got, tol):
    """Return (is_violation, detail). Shape mismatch is a violation."""
    ref = np.asarray(ref)
    got = np.asarray(got)
    if ref.shape != got.shape:
        return True, f"output shape changed {ref.shape}->{got.shape}"
    if ref.size == 0:
        return False, "empty output"
    dev = float(np.max(np.abs(ref.astype(np.float64) - got.astype(np.float64))))
    if dev > tol:
        return True, f"max deviation {dev:.3e} > tol {tol:.1e}"
    return False, f"max deviation {dev:.3e} <= tol {tol:.1e}"


def mr_rho_mono(fn, ctx, tol):
    if "x" not in ctx or ("add_redundant" not in ctx and "drop_redundant" not in ctx):
        return {"status": "not_applicable",
                "detail": ("ctx lacks {x, add_redundant|drop_redundant}; op is not "
                           "redundant-point/row-typed for this bug. Note: the paper's "
                           "literal 'top-1 stability' is classifier-level and N/A to a "
                           "pure library fn.")}
    x = ctx["x"]
    try:
        y0 = _to_np(fn(x))
    except Exception as e:  # noqa: BLE001
        return {"status": "not_applicable",
                "detail": f"baseline call failed: {type(e).__name__}: {e}"}

    mode = "add_redundant" if "add_redundant" in ctx else "drop_redundant"
    perturb = ctx.get("add_redundant") or ctx.get("drop_redundant")
    try:
        x_pert = perturb(x)
    except Exception as e:  # noqa: BLE001
        return {"status": "not_applicable",
                "detail": f"{mode} builder failed: {type(e).__name__}: {e}"}

    try:
        y1 = _to_np(fn(x_pert))
    except Exception as e:  # noqa: BLE001
        # Exception the fixed code would not raise == detection.
        return {"status": "fired",
                "detail": f"perturbed ({mode}) call raised {type(e).__name__}: {e}"}

    violated, detail = _compare(y0, y1, tol)
    if violated:
        return {"status": "fired",
                "detail": f"redundancy stability violated under {mode}: {detail}"}
    return {"status": "held",
            "detail": f"redundancy stability held under {mode}: {detail}"}


# Set N membership marker for the harness loader
MR = {"name": "rho_mono", "set": "N", "callable": mr_rho_mono}
