#!/usr/bin/env python3
# ⚠️ FIX_NEEDED (verifier): dead branch — if ctx declares ONLY 'perm_equivariant'
# together with ctx['index'] (scatter), NO check runs and a buggy order-dependent
# scatter is silently 'held' (false negative). Fix: in the perm branch, when
# has_index and 'perm_equivariant' in props, run the invariant check (lockstep perm
# of (src,index) IS invariance) or return not_applicable instead of vacuous 'held'.
"""set_M_metric — METRIC+ category-enumeration scaffold (Set M baseline).

Source in the paper: NOETHER_paper_arxiv.tex L303 (METRIC+ "input-domain x
output-relation category" scaffold of Sun et al. 2021, the 9-category METRIC
base extended by 2 output-domain pairs = 11 D x R category pairs) and the
head-to-head scope note at L355-357: "no public METRIC+ implementation
auto-generates MRs from a A_P specification; a full PIT-based METRIC+ vs Set N
comparison is committed as supplementary S4 (future_work.md) item (i)."

ADAPTABILITY (honest triage)
----------------------------
Set M is NOT a single MR. METRIC+ is a *meta-method*: the tester enumerates
relevant input-transformation categories (D: permutation/reordering, additive
shift, multiplicative scaling, sign/negation, ...) and output relations (R:
equality, equality-up-to-permutation, order/monotonicity, proportional change,
magnitude/norm preservation), then composes candidate MRs from the D x R cross
product (the worked examples in the paper: sorting -> {permutation, order};
midpoint/hypotSig/powerSig -> {additive, multiplicative, scaling}, L2369-2410).

Because the paper states plainly that NO public METRIC+ implementation exists
(the head-to-head is committed future work, re-implementing METRIC+ "from
prose"), porting it requires re-instantiating the GENERIC D x R category pairs
as concrete executable MRs. That is exactly the committed-S4 task, done here at
library-function granularity. Hence Set M is ADAPTABLE, not directly portable:
the *scaffold* ports; the concrete MRs must be re-derived from the category
catalogue.

HONESTY GUARDRAILS
  - Each sub-MR below is a GENERIC metamorphic category, identical in form to
    METRIC+'s published catalogue. None is tailored to any specific e3nn/PyG
    defect; the bug distribution is external.
  - A category fires ONLY when the relation it asserts is genuinely a semantic
    property the op is *claimed* to have. We therefore require the repro snippet
    to declare, per op, which output-relation classes hold (ctx["metric_props"])
    -- because "permuting inputs leaves the output unchanged" is a real MR for
    scatter-mean but NOT for a generic map. We do NOT guess; if no applicable
    property is declared, we return not_applicable rather than forcing a fit
    (per mr_sets/README.md).
  - 'fired' means a declared D x R relation is VIOLATED (or the transformed call
    raises where the fixed code does not); the post-fix sanity run filters false
    positives.

target_bug_categories (e3nn / PyG, library level):
  - scatter / segment-reduce permutation-order bugs (D=permutation x R=equality).
  - irreps-bookkeeping ordering bugs as input-row-permutation sensitivity.
  - homogeneity / scaling defects (D=multiplicative x R=proportional change).
  - additive-offset / centering bugs (D=additive x R=equality).
  - sign / parity bugs (D=negation x R=equality|sign-flip).

When NOT applicable:
  - ctx declares no METRIC+ output-relation class for the op -> not_applicable.

ctx contract (built by the bug's repro snippet, NOT here):
  ctx["x"]            : base input (np.ndarray / torch.Tensor), OR
  ctx["args"]         : tuple; op called fn(*args), FIRST arg is transformed.
  ctx["metric_props"] : list of declared D x R category tokens:
                          "perm_invariant"   D=row-perm,  R=equality
                          "perm_equivariant" D=row-perm,  R=eq-up-to-perm
                          "additive_invariant" D=+c,      R=equality
                          "scale_homogeneous"  D=*c,      R=output *c^k
                          "sign_invariant"     D=-x,      R=equality
                          "sign_flip"          D=-x,      R=-output
  ctx["scale_degree"] : k for scale_homogeneous (default 1).
  ctx["perm_axis"]    : axis permuted (default 0).
  ctx["index"]        : index tensor permuted in lockstep with x (scatter ops).

Interface: mr_set_M_metric(fn, ctx, tol) -> {"status","detail"}
CPU-only, no training, no full forward pass.
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


def _like(template, arr):
    """Return arr typed like template (torch.Tensor in, torch.Tensor out)."""
    if _HAS_TORCH and isinstance(template, torch.Tensor):
        return torch.as_tensor(np.asarray(arr), dtype=template.dtype)
    return np.asarray(arr)


def _call(fn, x, ctx):
    """Call fn with x substituted as the first/only transformed argument."""
    if "args" in ctx and ctx["args"] is not None:
        rest = tuple(ctx["args"][1:])
        return fn(x, *rest)
    return fn(x)


def _perm(x_np, axis, perm):
    return np.take(x_np, perm, axis=axis)


def mr_set_M_metric(fn, ctx, tol, num_samples=8):
    props = ctx.get("metric_props")
    if not props:
        return {"status": "not_applicable",
                "detail": "no METRIC+ D x R category declared for this op; "
                          "scaffold has nothing to enumerate"}

    if "x" not in ctx and "args" not in ctx:
        return {"status": "not_applicable",
                "detail": "ctx lacks {x|args}; METRIC+ category pairs un-instantiable"}

    x = ctx["x"] if "x" in ctx else ctx["args"][0]
    x_np = _to_np(x)

    # Baseline output. A baseline failure is not a metamorphic violation here.
    try:
        y0 = _to_np(_call(fn, x, ctx))
    except Exception as e:  # noqa: BLE001
        return {"status": "not_applicable",
                "detail": f"baseline call failed: {type(e).__name__}"}

    rng = np.random.default_rng(20240601)
    axis = int(ctx.get("perm_axis", 0))
    k = float(ctx.get("scale_degree", 1.0))
    n = x_np.shape[axis] if x_np.ndim > axis else x_np.size
    applicable_any = False

    def _violation(cat, detail):
        return {"status": "fired", "detail": f"[{cat}] {detail}"}

    # ---- D=row-permutation x R=equality / equality-up-to-permutation ----
    if ("perm_invariant" in props or "perm_equivariant" in props) and n > 1:
        applicable_any = True
        has_index = ctx.get("index") is not None
        idx_np = _to_np(ctx["index"]) if has_index else None
        for _ in range(num_samples):
            perm = rng.permutation(n)
            xp_in = _like(x, _perm(x_np, axis, perm))
            if has_index:
                # scatter-style: permute (src rows, index) in lockstep -> same
                # grouping, so a correct reduction is output-invariant.
                base_args = list(ctx["args"])
                base_args[0] = xp_in
                if len(base_args) > 1:
                    base_args[1] = _like(ctx["index"], _perm(idx_np, axis, perm))
                try:
                    yp = _to_np(fn(*base_args))
                except Exception as e:  # noqa: BLE001
                    return _violation("perm", f"permuted scatter call raised {type(e).__name__}")
            else:
                try:
                    yp = _to_np(_call(fn, xp_in, ctx))
                except Exception as e:  # noqa: BLE001
                    return _violation("perm", f"permuted call raised {type(e).__name__}")

            if "perm_invariant" in props:
                if yp.shape != y0.shape:
                    return _violation("perm_inv", f"output shape changed {y0.shape}->{yp.shape}")
                dev = float(np.max(np.abs(yp - y0)))
                if dev > tol:
                    return _violation("perm_inv", f"max dev {dev:.3e} > tol {tol:.1e}")
            if "perm_equivariant" in props and not has_index:
                if yp.shape != y0.shape:
                    return _violation("perm_equiv", f"output shape changed {y0.shape}->{yp.shape}")
                inv = np.empty_like(perm)
                inv[perm] = np.arange(n)
                y_un = _perm(yp, axis, inv)
                dev = float(np.max(np.abs(y_un - y0)))
                if dev > tol:
                    return _violation("perm_equiv", f"un-permuted output max dev {dev:.3e} > tol {tol:.1e}")

    # ---- D=multiplicative scaling x R=proportional (degree-k homogeneity) ----
    if "scale_homogeneous" in props:
        applicable_any = True
        for c in (2.0, 0.5, 3.0):
            xs = _like(x, x_np * c)
            try:
                ys = _to_np(_call(fn, xs, ctx))
            except Exception as e:  # noqa: BLE001
                return _violation("scale", f"scaled call raised {type(e).__name__}")
            if ys.shape != y0.shape:
                return _violation("scale", f"output shape changed under scaling {y0.shape}->{ys.shape}")
            ref = y0 * (c ** k)
            denom = np.maximum(np.abs(ref), 1.0)
            dev = float(np.max(np.abs(ys - ref) / denom))
            if dev > tol:
                return _violation("scale", f"degree-{k:g} homogeneity broken: rel dev {dev:.3e} > tol {tol:.1e} at c={c}")

    # ---- D=additive shift x R=equality (translation invariance) ----
    if "additive_invariant" in props:
        applicable_any = True
        for c in (1.0, -2.0, 0.3):
            xa = _like(x, x_np + c)
            try:
                ya = _to_np(_call(fn, xa, ctx))
            except Exception as e:  # noqa: BLE001
                return _violation("additive", f"shifted call raised {type(e).__name__}")
            if ya.shape != y0.shape:
                return _violation("additive", f"output shape changed under shift {y0.shape}->{ya.shape}")
            dev = float(np.max(np.abs(ya - y0)))
            if dev > tol:
                return _violation("additive", f"additive invariance broken: max dev {dev:.3e} > tol {tol:.1e} at c={c}")

    # ---- D=negation x R=equality | sign-flip (parity) ----
    if "sign_invariant" in props or "sign_flip" in props:
        applicable_any = True
        xn = _like(x, -x_np)
        try:
            yn = _to_np(_call(fn, xn, ctx))
        except Exception as e:  # noqa: BLE001
            return _violation("sign", f"negated call raised {type(e).__name__}")
        if yn.shape != y0.shape:
            return _violation("sign", f"output shape changed under negation {y0.shape}->{yn.shape}")
        if "sign_invariant" in props:
            dev = float(np.max(np.abs(yn - y0)))
            if dev > tol:
                return _violation("sign_inv", f"sign-invariance broken: max dev {dev:.3e} > tol {tol:.1e}")
        if "sign_flip" in props:
            dev = float(np.max(np.abs(yn + y0)))
            if dev > tol:
                return _violation("sign_flip", f"odd-parity (sign-flip) broken: max dev {dev:.3e} > tol {tol:.1e}")

    if not applicable_any:
        return {"status": "not_applicable",
                "detail": f"declared props {props} not instantiable on this input "
                          f"(e.g. n<=1 for permutation); no METRIC+ category fired"}

    return {"status": "held",
            "detail": f"all declared METRIC+ D x R categories {props} held within tol {tol:.1e}"}


# Set M membership marker for the harness loader
MR = {"name": "set_M_metric", "set": "M", "callable": mr_set_M_metric}
