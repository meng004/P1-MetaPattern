#!/usr/bin/env python3
"""set_B_lit -- literature MT-for-ML baseline (Set B), ported to library bugs.

Set B in the paper (NOETHER_paper_arxiv.tex L1229) is five metamorphic
relations synthesised from the metamorphic-testing-for-ML literature
(Segura 2016 survey; Shin et al. 2024 LLM-generated executable MRs; AutoMT
2025), *restricted to point-cloud classifiers*. As stated there they are
CLASSIFIER-PREDICTION-LEVEL relations on a trained model's label output:
  (B1) rotation invariance of the predicted class,
  (B2) permutation invariance of the predicted class,
  (B3) inference idempotency,
  (B4) sub-sampling / point-density stability of the prediction,
  (B5) translation / scale invariance of the prediction.

Read literally, B1,B2,B4,B5 require a TRAINED model and a full forward pass
producing a label, and B4 has no oracle for a pure tensor op. Those readings
are NOT applicable to a pure e3nn / PyG library function and are reported as
'not_applicable' here -- never contorted to look applicable (honesty rule).

What DOES port is the function-output-level core of three of these literature
MRs, which is the general MT-for-ML pattern the cited papers describe and is
not bug-specific:
  * PERMUTATION invariance  -> a segment/scatter reduction is invariant to
    reordering of (value, index) pairs (real general property of PyG scatter).
  * IDEMPOTENCY (Shin et al.) -> calling a pure op twice on the same input
    yields identical output (catches in-place input mutation / nondeterminism).
  * input-TRANSFORM invariance-or-equivariance (AutoMT style) -> output
    transforms covariantly under an input transform that ctx supplies.

This module is a single dispatching MR. It tries each branch only when ctx
provides the data that makes that branch *meaningful*, and returns
'not_applicable' when none is. It never injects a specific bug: the transforms
and the oracle come from the bug's repro snippet (ctx), not from this file.

CPU-only, no training, no model forward pass. torch optional.

Interface: mr_set_B_lit(fn, ctx, tol) -> {"status", "detail"}  (mr_sets/README.md)

ctx keys consumed (all optional; the branch is skipped if absent):
  ---- permutation-invariance branch (PyG scatter / segment reductions) ----
  ctx["perm_args"]    : tuple/list of positional args to fn, e.g. (src, index).
  ctx["perm_kwargs"]  : optional dict of kwargs to fn (e.g. {"dim_size": k}).
  ctx["perm_axis"]    : int, the axis along which (value,index) pairs may be
                        permuted without changing the segmented result
                        (default 0).
  ctx["perm_apply"]   : optional callable(args, kwargs, perm) -> (args, kwargs)
                        that applies a row permutation. If absent, a default is
                        used that permutes ctx["perm_axis"] of EVERY tensor arg
                        whose size on that axis equals the index length.
  ctx["perm_index_pos"] : optional int, positional position of the index tensor
                        in perm_args (used by the default permuter to find the
                        segment length). Default: last positional tensor.
  ---- idempotency / determinism branch (Shin et al.) ----
  ctx["x"]            : the single input the op accepts (tensor / ndarray).
                        (Shared with the transform branch below.)
  ctx["idempotent"]   : optional bool, default True -> enable the determinism
                        check fn(x)==fn(x) and the input-immutability check.
  ---- input-transform invariance/equivariance branch (AutoMT style) ----
  ctx["transform"]    : callable transform(x, p) applying a parameterised input
                        transform (e.g. a rotation matrix or a positive scale).
  ctx["transform_params"] : iterable of params p to feed transform (e.g. list
                        of rotation matrices / scale factors). If absent, the
                        branch is skipped (no fabricated transform).
  ctx["out_transform"]    : optional callable(y, p) for the EQUIVARIANT case;
                        absent => invariance expected (out unchanged).

A branch returns 'fired' iff its relation is VIOLATED, or iff the call raises
an exception that the fixed code would not (the caller's post-fix sanity run
filters false positives). If no branch is meaningful, returns 'not_applicable'
with a plain reason -- distinct from 'held', per the contract.
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


def _is_tensor(a):
    return (_HAS_TORCH and isinstance(a, torch.Tensor)) or isinstance(a, np.ndarray)


def _clone(a):
    if _HAS_TORCH and isinstance(a, torch.Tensor):
        return a.detach().clone()
    return np.array(a, copy=True)


def _max_abs_diff(a, b):
    a = _to_np(a)
    b = _to_np(b)
    if a.shape != b.shape:
        return None  # shape mismatch signalled separately
    if a.size == 0:
        return 0.0
    return float(np.max(np.abs(a.astype(np.float64) - b.astype(np.float64))))


# ----------------------------------------------------------------------------
# Branch B2: permutation invariance of a segment / scatter reduction
# ----------------------------------------------------------------------------
def _default_permuter(args, kwargs, perm, axis, index_pos):
    """Permute `axis` of every tensor positional arg whose length on `axis`
    matches the permutation length. Index tensor and value tensor are permuted
    together (that is the relation: reordering the (value,index) PAIRS leaves
    the per-segment reduction unchanged)."""
    n = len(perm)
    new_args = list(args)
    for i, a in enumerate(new_args):
        if _is_tensor(a) and a.ndim > axis and a.shape[axis] == n:
            if _HAS_TORCH and isinstance(a, torch.Tensor):
                idx = torch.as_tensor(np.asarray(perm), dtype=torch.long, device=a.device)
                new_args[i] = a.index_select(axis, idx)
            else:
                new_args[i] = np.take(a, perm, axis=axis)
    return tuple(new_args), dict(kwargs)


def _branch_perm(fn, ctx, tol):
    if "perm_args" not in ctx:
        return None
    args = tuple(ctx["perm_args"])
    kwargs = dict(ctx.get("perm_kwargs", {}))
    axis = int(ctx.get("perm_axis", 0))
    apply_perm = ctx.get("perm_apply")
    index_pos = ctx.get("perm_index_pos")

    # Determine permutation length from the index/value tensors.
    seg_len = None
    if index_pos is not None and 0 <= index_pos < len(args) and _is_tensor(args[index_pos]):
        t = args[index_pos]
        seg_len = t.shape[axis] if t.ndim > axis else t.shape[0]
    else:
        for a in reversed(args):
            if _is_tensor(a) and a.ndim > axis:
                seg_len = a.shape[axis]
                break
    if seg_len is None or seg_len < 2:
        return {"status": "not_applicable",
                "detail": "perm branch: no permutable axis of length>=2 found"}

    try:
        y0 = fn(*args, **kwargs)
    except Exception as e:  # noqa: BLE001
        return {"status": "not_applicable",
                "detail": f"perm baseline call failed: {type(e).__name__}: {e}"}

    rng = np.random.default_rng(20240619)
    max_dev = 0.0
    for trial in range(8):
        perm = rng.permutation(seg_len)
        if np.all(perm == np.arange(seg_len)):
            continue
        try:
            if apply_perm is not None:
                p_args, p_kwargs = apply_perm(args, kwargs, perm)
            else:
                p_args, p_kwargs = _default_permuter(args, kwargs, perm, axis, index_pos)
            yp = fn(*p_args, **p_kwargs)
        except Exception as e:  # noqa: BLE001
            return {"status": "fired",
                    "detail": f"permuted scatter call raised {type(e).__name__}: {e}"}
        dev = _max_abs_diff(y0, yp)
        if dev is None:
            return {"status": "fired",
                    "detail": "scatter output shape changed under input permutation"}
        max_dev = max(max_dev, dev)
        if dev > tol:
            return {"status": "fired",
                    "detail": f"permutation invariance violated: dev {dev:.3e} > tol {tol:.1e}"}
    return {"status": "held",
            "detail": f"permutation invariance held; max dev {max_dev:.3e} <= tol {tol:.1e}"}


# ----------------------------------------------------------------------------
# Branch B3: idempotency / determinism + input immutability (Shin et al.)
# ----------------------------------------------------------------------------
def _branch_idempotent(fn, ctx, tol):
    if "x" not in ctx or not ctx.get("idempotent", True):
        return None
    x = ctx["x"]
    x_before = _clone(x)
    try:
        y1 = fn(x)
    except Exception as e:  # noqa: BLE001
        return {"status": "not_applicable",
                "detail": f"idempotency baseline call failed: {type(e).__name__}"}
    # (a) input must not be mutated in place by a pure op.
    dev_in = _max_abs_diff(x_before, x)
    if dev_in is None or dev_in > tol:
        return {"status": "fired",
                "detail": f"op mutated its input in place (input dev {dev_in})"}
    # (b) calling twice on the same input must give identical output.
    try:
        y2 = fn(x)
    except Exception as e:  # noqa: BLE001
        return {"status": "fired",
                "detail": f"second identical call raised {type(e).__name__}: {e}"}
    dev = _max_abs_diff(y1, y2)
    if dev is None:
        return {"status": "fired", "detail": "nondeterministic output shape across identical calls"}
    if dev > tol:
        return {"status": "fired",
                "detail": f"idempotency/determinism violated: dev {dev:.3e} > tol {tol:.1e}"}
    return {"status": "held",
            "detail": f"idempotent & input-immutable; dev {dev:.3e} <= tol {tol:.1e}"}


# ----------------------------------------------------------------------------
# Branch B1/B5: input-transform invariance or equivariance (AutoMT style)
# ----------------------------------------------------------------------------
def _branch_transform(fn, ctx, tol):
    if "x" not in ctx or "transform" not in ctx or "transform_params" not in ctx:
        return None
    x = ctx["x"]
    transform = ctx["transform"]
    params = list(ctx["transform_params"])
    out_tf = ctx.get("out_transform")  # None => invariance
    if not params:
        return {"status": "not_applicable", "detail": "transform branch: empty transform_params"}
    try:
        y0 = fn(x)
    except Exception as e:  # noqa: BLE001
        return {"status": "not_applicable",
                "detail": f"transform baseline call failed: {type(e).__name__}"}
    max_dev = 0.0
    for i, p in enumerate(params):
        try:
            yt = fn(transform(x, p))
        except Exception as e:  # noqa: BLE001
            return {"status": "fired",
                    "detail": f"transformed call raised {type(e).__name__}: {e}"}
        ref = out_tf(y0, p) if out_tf is not None else y0
        dev = _max_abs_diff(ref, yt)
        if dev is None:
            return {"status": "fired",
                    "detail": "output shape changed under input transform"}
        max_dev = max(max_dev, dev)
        if dev > tol:
            kind = "equivariance" if out_tf is not None else "invariance"
            return {"status": "fired",
                    "detail": f"{kind} violated: dev {dev:.3e} > tol {tol:.1e} at param {i}"}
    kind = "equivariance" if out_tf is not None else "invariance"
    return {"status": "held",
            "detail": f"transform {kind} held; max dev {max_dev:.3e} <= tol {tol:.1e}"}


def mr_set_B_lit(fn, ctx, tol):
    """Dispatch the applicable literature-MR branch(es). 'fired' if any branch
    detects a violation; 'held' if at least one branch ran and all held;
    'not_applicable' if no branch is meaningful for this fn/bug (e.g. the op is
    a classifier-label relation requiring a trained forward pass, or none of
    perm_args / transform / x is supplied)."""
    branches = [
        ("perm", _branch_perm),
        ("idempotent", _branch_idempotent),
        ("transform", _branch_transform),
    ]
    ran = []
    held_details = []
    na_details = []
    for name, br in branches:
        res = br(fn, ctx, tol)
        if res is None:
            continue  # ctx did not supply this branch's data
        if res["status"] == "fired":
            return {"status": "fired", "detail": f"[{name}] " + res["detail"]}
        if res["status"] == "held":
            ran.append(name)
            held_details.append(f"{name}: {res['detail']}")
        else:  # not_applicable returned by a branch that was attempted
            na_details.append(f"{name}: {res['detail']}")

    if ran:
        return {"status": "held", "detail": "; ".join(held_details)}
    if na_details:
        return {"status": "not_applicable",
                "detail": "no literature-MR branch held meaningfully -> " + "; ".join(na_details)}
    return {"status": "not_applicable",
            "detail": ("Set B is classifier-prediction-level (rotation/permutation/"
                       "idempotency/sub-sampling/scale invariance of a trained model's "
                       "label); ctx supplies none of {perm_args, transform+params, x}, so "
                       "no branch is meaningful for this pure library function")}


# Set B membership marker for the harness loader
MR = {"name": "set_B_lit", "set": "B", "callable": mr_set_B_lit}
