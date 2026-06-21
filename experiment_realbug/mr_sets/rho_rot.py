#!/usr/bin/env python3
"""rho_rot - SO(3) rotation-invariance/equivariance metamorphic relation (Set N).

Derived from the paper's executable MR rho_rot (NOETHER_paper_arxiv.tex, eq:rho-rot,
Step 5 listing): for an operation that should be invariant (or equivariant) under
SO(3), rotating the input must leave the output unchanged (resp. transform
covariantly) within tolerance:

    rho_rot:  forall R in SO(3),  || f(R . x) - f(x) ||_inf  <=  tau     (tau=1e-4 fp32)

A pre-fix bug that breaks rotation handling -> the relation is VIOLATED -> 'fired'.

This is the ONE Set N MR that ports cleanly to library-level e3nn / PyTorch-Geometric
bugs in rotation / irreps / spherical-harmonics / tensor-product code. The remaining
Set N MRs (rho_train, rho_train-rev, rho_mono) are training/inference-trajectory
relations and return 'not_applicable' on a pure library function. CPU-only, no
training, no full forward pass.

Interface: mr_rho_rot(fn, ctx, tol) -> {"status", "detail"}  (see mr_sets/README.md)
ctx must provide:
  ctx["x"]      : the base input the op accepts (e.g. an (n,3) point set, an edge-vector
                  tensor, or an irreps feature tensor) as a torch.Tensor / np.ndarray.
  ctx["rotate"] : a callable rotate(x, R) applying rotation matrix R (3x3 np.ndarray)
                  to x in the way THIS op expects (provided by the bug's repro snippet,
                  because how a rotation acts on the input is op-specific:
                  point clouds rotate as x @ R.T, irrep features via Wigner-D, etc.).
  ctx.get("equivariant_out") : optional callable out_transform(y, R) if the op is
                  equivariant rather than invariant (default None => invariance).
"""
import numpy as np

try:
    import torch
    _HAS_TORCH = True
except Exception:  # noqa: BLE001
    _HAS_TORCH = False


def _random_rotation(seed_idx):
    """Deterministic SO(3) rotation from a fixed-index seed (no global RNG; the index
    varies the rotation reproducibly across samples). Returns a 3x3 np.ndarray."""
    ang = (0.37 + 0.61 * seed_idx) % (2 * np.pi)
    ax = np.array([np.sin(seed_idx), np.cos(2 * seed_idx), np.sin(3 * seed_idx + 1)])
    ax = ax / (np.linalg.norm(ax) + 1e-12)
    x, y, z = ax
    c, s, C = np.cos(ang), np.sin(ang), 1 - np.cos(ang)
    return np.array([
        [c + x * x * C, x * y * C - z * s, x * z * C + y * s],
        [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
        [z * x * C - y * s, z * y * C + x * s, c + z * z * C],
    ])


def _to_np(a):
    if _HAS_TORCH and isinstance(a, torch.Tensor):
        return a.detach().cpu().numpy()
    return np.asarray(a)


def mr_rho_rot(fn, ctx, tol, num_samples=24):
    if "x" not in ctx or "rotate" not in ctx:
        return {"status": "not_applicable",
                "detail": "ctx lacks {x, rotate}; op is not rotation-typed for this bug"}
    x = ctx["x"]
    rotate = ctx["rotate"]
    out_tf = ctx.get("equivariant_out")  # None => invariance expected
    try:
        y0 = _to_np(fn(x))
    except Exception as e:  # noqa: BLE001
        return {"status": "not_applicable",
                "detail": f"baseline (unrotated) call failed: {type(e).__name__}"}

    max_dev = 0.0
    for i in range(1, num_samples + 1):
        R = _random_rotation(i)
        try:
            yr = _to_np(fn(rotate(x, R)))
        except Exception as e:  # noqa: BLE001
            # An exception the FIXED code does not raise is itself a detection; the
            # caller's post-fix sanity run distinguishes true positive from false positive.
            return {"status": "fired", "detail": f"rotated call raised {type(e).__name__}"}
        ref = _to_np(out_tf(y0, R)) if out_tf else y0
        if ref.shape != yr.shape:
            return {"status": "fired",
                    "detail": f"output shape changed under rotation {ref.shape}->{yr.shape}"}
        dev = float(np.max(np.abs(ref - yr)))  # L_inf, matching the paper's ||.||_inf
        max_dev = max(max_dev, dev)
        if dev > tol:
            return {"status": "fired",
                    "detail": f"max deviation {dev:.3e} > tol {tol:.1e} at sample {i}"}
    return {"status": "held",
            "detail": f"invariance held; max deviation {max_dev:.3e} <= tol {tol:.1e}"}


# Set N membership marker for the harness loader
MR = {"name": "rho_rot", "set": "N", "callable": mr_rho_rot}
