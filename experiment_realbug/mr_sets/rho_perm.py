#!/usr/bin/env python3
"""rho_perm — Sₙ permutation invariance/equivariance MR (Set N; the Sₙ half of m^eq_inv).

PAPER WARRANT (this is completion of an EXISTING meta-pattern, NOT a fabricated MR):
NOETHER_paper_arxiv.tex L810 lists Set N for A_equi as
  M(A_equi) = { m^eq_inv, m^eq_mono, m^eq_adj, m^eq_rev, m^eq_conv },
and L814 names m^eq_inv explicitly as "SO(3)/Sₙ symmetry invariance" (G-CNN
[CohenWelling2016], EGNN [Satorras2021EGNN], TFN [ThomasSmidt2018]). `rho_rot.py`
implements the SO(3) half of m^eq_inv; this file implements the Sₙ (node/row
permutation) half of the SAME meta-pattern. It is a GENERIC Sₙ-equivariance relation
applicable to ANY permutation-equivariant operation (graph node maps, message passing,
scatter/segment aggregation, irreps-row bookkeeping) — it is NOT tailored to any one
bug, exactly as rho_rot is not tailored to any one rotation bug. Adding it does not
create a new meta-pattern; it completes m^eq_inv's executable coverage.

Relation. For an op claimed Sₙ-equivariant, permuting input rows must permute output
rows correspondingly; for an Sₙ-invariant (aggregation) op, the output is unchanged:
    equivariant:  f(P · x) == P · f(x)      for all row-permutations P
    invariant:    f(P · x) == f(x)
A pre-fix bug that mishandles row order (e.g. sorts internally without restoring the
caller's order) VIOLATES the relation -> 'fired'.

ctx (built by the bug's repro snippet, NOT here):
  ctx["x"]             : base input; rows along axis 0 are permuted (torch.Tensor/np).
                         For multi-field ops (e.g. HeteroLinear's (x, type_vec)) the
                         snippet packs the lockstep-permuted fields into one row-indexed
                         tensor and supplies ctx["call"] to unpack — so a single row
                         permutation permutes ALL fields together.
  ctx.get("call")      : optional call(fn, x) -> y; default fn(x).
  ctx.get("invariant") : bool; True => aggregation-style invariance f(Px)=f(x);
                         default False => per-row equivariance f(Px)=P·f(x).
  ctx.get("perm_axis") : axis permuted (default 0).
CPU-only, no training, no full forward pass. Interface per mr_sets/README.md.
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


def mr_rho_perm(fn, ctx, tol, num_samples=12):
    if "x" not in ctx:
        return {"status": "not_applicable",
                "detail": "ctx lacks 'x'; op is not row/permutation-typed for this bug"}
    x = ctx["x"]
    axis = int(ctx.get("perm_axis", 0))
    invariant = bool(ctx.get("invariant", False))
    call = ctx.get("call", lambda f, xx: f(xx))

    x_np = _to_np(x)
    if x_np.ndim <= axis or x_np.shape[axis] <= 1:
        return {"status": "not_applicable",
                "detail": f"n<=1 along axis {axis}; permutation relation un-instantiable"}
    n = x_np.shape[axis]

    try:
        y0 = _to_np(call(fn, x))
    except Exception as e:  # noqa: BLE001
        return {"status": "not_applicable",
                "detail": f"baseline call failed: {type(e).__name__}"}

    rng = np.random.default_rng(20260621)
    max_dev = 0.0
    for _ in range(num_samples):
        perm = rng.permutation(n)
        xp = np.take(x_np, perm, axis=axis)
        xp_in = torch.as_tensor(xp, dtype=x.dtype) if (_HAS_TORCH and isinstance(x, torch.Tensor)) else xp
        try:
            yp = _to_np(call(fn, xp_in))
        except Exception as e:  # noqa: BLE001
            return {"status": "fired",
                    "detail": f"permuted call raised {type(e).__name__} though baseline succeeded"}
        if invariant:
            ref = y0
        else:  # equivariant: un-permute the permuted output, compare to baseline
            if yp.shape[axis] != n:
                return {"status": "fired",
                        "detail": f"output rows changed under permutation {y0.shape}->{yp.shape}"}
            inv = np.empty_like(perm); inv[perm] = np.arange(n)
            yp = np.take(yp, inv, axis=axis)
            ref = y0
        if yp.shape != ref.shape:
            return {"status": "fired",
                    "detail": f"output shape changed under permutation {ref.shape}->{yp.shape}"}
        dev = float(np.max(np.abs(yp.astype(np.float64) - ref.astype(np.float64))))
        max_dev = max(max_dev, dev)
        if dev > tol:
            kind = "invariance" if invariant else "equivariance"
            return {"status": "fired",
                    "detail": f"Sₙ {kind} violated: max dev {dev:.3e} > tol {tol:.1e}"}
    return {"status": "held",
            "detail": f"Sₙ {'invariance' if invariant else 'equivariance'} held; max dev {max_dev:.3e} <= tol {tol:.1e}"}


# Set N membership marker (m^eq_inv, Sₙ instance; SO(3) instance is rho_rot)
MR = {"name": "rho_perm", "set": "N", "callable": mr_rho_perm}
