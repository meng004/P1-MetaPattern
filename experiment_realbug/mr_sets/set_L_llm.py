#!/usr/bin/env python3
"""set_L_llm -- LLM-prompt baseline (Set L) ported to library-level e3nn/PyG bugs.

PROVENANCE
----------
Set L is the verbatim GPT-4 output recorded in supplementary
S3_case_study/mr_sets/prompt_log.md (gpt-4-turbo-2024-04-09, T=0.0, seed=4246),
five MRs for "an SE(3)-equivariant point-cloud classifier":
  L_rot   rotation_invariance     L_perm  permutation_invariance
  L_trans translation_invariance  L_noise noise_robustness
  L_scale scaling_robustness

These were authored as *classifier-output* relations: an input transform g acts on
a (n,3) cloud and the relation asserts the predicted class-probability vector is
(near-)unchanged. The library-bug target here is the opposite end of the stack:
PURE FUNCTIONS in e3nn / PyTorch-Geometric (spherical_harmonics, TensorProduct /
FullyConnectedTensorProduct, scatter / segment reductions, irreps bookkeeping),
CPU-only, no model forward pass.

PORTABILITY VERDICT: adaptable (the SET SPLITS).
  * L_rot  -> portable as the GROUP-ACTION relation g.f(x)=f(g.x): for an SH/TP
             library fn the correct contract is *equivariance*
             f(D_in(R) x)=D_out(R) f(x) (out_transform supplied by snippet) or
             genuine invariance for scalar/type-0 output. Same relation as Set N's
             rho_rot (manuscript notes the overlap). Provided here.
  * L_perm -> portable to scatter / segment-reduction library bugs: a reduction
             over (src,index) must be invariant to a row permutation that carries
             src and index together (commutative-reduce contract). Provided here.
  * L_scale-> GPT-4 asserts *invariance under global scaling*. That is FALSE for
             raw spherical_harmonics (homogeneous of degree l) and linear TP, so
             the as-written MR would FIRE on correct code. Honestly NOT a library
             MR as authored => default not_applicable. We DO expose a faithful
             *homogeneity* reformulation f(c x)=c^deg f(x) on explicit opt-in
             (ctx['scale_degree']), clearly flagged as DEVIATING from the GPT-4
             spec, so we never fabricate a relation the baseline did not author.
  * L_trans-> translation has no contract on a pure SH/TP/scatter function
             (translation-invariance is a model-architecture property via relative
             positions). not_applicable at runtime.
  * L_noise-> Gaussian-noise robustness is an ML-testing heuristic with no exact
             post-condition for a deterministic library function. not_applicable.

HONESTY: we do NOT contort L_trans/L_noise into library MRs, and we do NOT silently
ship the wrong L_scale invariance. 'fired' always means a relation VIOLATED; an
exception the FIXED code would not raise counts as fired (post-fix sanity filters FP).

Interface (see mr_sets/README.md): each mr_*(fn, ctx, tol) -> {"status","detail"}.
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


def _random_rotation(seed_idx):
    """Deterministic SO(3) rotation from a fixed-index seed (matches rho_rot.py)."""
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


# -----------------------------------------------------------------------------
# L_rot -- rotation_invariance, ported as group-action equivariance/invariance.
#   ctx must provide:
#     ctx["x"]                   : base input fn accepts (e.g. (n,3) directions or
#                                  an irreps feature tensor), torch.Tensor / ndarray.
#     ctx["rotate"]              : rotate(x, R) applying rotation matrix R the way
#                                  THIS fn expects (snippet-owned; op-specific).
#     ctx.get("equivariant_out") : out_transform(y, R) if fn is equivariant rather
#                                  than invariant; default None => invariance.
# -----------------------------------------------------------------------------
def mr_L_rot(fn, ctx, tol, num_samples=24):
    if "x" not in ctx or "rotate" not in ctx:
        return {"status": "not_applicable",
                "detail": "L_rot: ctx lacks {x, rotate}; fn is not rotation-typed for this bug"}
    x = ctx["x"]
    rotate = ctx["rotate"]
    out_tf = ctx.get("equivariant_out")  # None => invariance expected
    try:
        y0 = _to_np(fn(x))
    except Exception as e:  # noqa: BLE001
        return {"status": "not_applicable", "detail": f"L_rot baseline call failed: {type(e).__name__}"}
    max_dev = 0.0
    for i in range(1, num_samples + 1):
        R = _random_rotation(i)
        try:
            yr = _to_np(fn(rotate(x, R)))
        except Exception as e:  # noqa: BLE001
            return {"status": "fired", "detail": f"L_rot: rotated call raised {type(e).__name__}"}
        ref = _to_np(out_tf(y0, R)) if out_tf else y0
        if ref.shape != yr.shape:
            return {"status": "fired", "detail": f"L_rot: output shape changed under rotation {ref.shape}->{yr.shape}"}
        dev = float(np.max(np.abs(ref - yr)))
        max_dev = max(max_dev, dev)
        if dev > tol:
            return {"status": "fired", "detail": f"L_rot: max deviation {dev:.3e} > tol {tol:.1e} at sample {i}"}
    return {"status": "held", "detail": f"L_rot: rotation relation held; max dev {max_dev:.3e} <= tol {tol:.1e}"}


# -----------------------------------------------------------------------------
# L_perm -- permutation_invariance, ported to scatter / segment-reduction bugs.
#   A reduction y = fn(src, index) over a graph/segment structure must be
#   invariant to any permutation pi applied jointly to (src, index). This is the
#   commutative-reduce contract: exactly where PyG scatter off-by-one / wrong-dim /
#   non-commutative-reduce defects surface.
#   ctx must provide a permutable structure (either form):
#     ctx["perm_apply"]: perm_apply(perm) -> args (tuple/list or single) for fn, OR
#     ctx["src"] + ctx["index"] with fn(src, index) and row dim 0.
#     ctx.get("n_rows"): row count if using perm_apply.
# -----------------------------------------------------------------------------
def mr_L_perm(fn, ctx, tol, num_samples=12):
    perm_apply = ctx.get("perm_apply")
    have_src_index = ("src" in ctx and "index" in ctx)
    if perm_apply is None and not have_src_index:
        return {"status": "not_applicable",
                "detail": "L_perm: ctx lacks perm_apply or (src,index); fn is not a permutable reduction here"}

    def _call(perm):
        if perm_apply is not None:
            args = perm_apply(perm)
            return fn(*args) if isinstance(args, (tuple, list)) else fn(args)
        src = ctx["src"]
        index = ctx["index"]
        return fn(src[perm], index[perm])

    if have_src_index:
        n = int(_to_np(ctx["index"]).shape[0])
    else:
        n = int(ctx.get("n_rows", 0))
    if n and n < 2:
        return {"status": "not_applicable", "detail": "L_perm: <2 permutable rows"}

    try:
        ident = np.arange(n) if n else np.arange(0)
        y0 = _to_np(_call(ident))
    except Exception as e:  # noqa: BLE001
        return {"status": "not_applicable", "detail": f"L_perm baseline call failed: {type(e).__name__}"}

    rng = np.random.default_rng(102)
    max_dev = 0.0
    for i in range(num_samples):
        perm = rng.permutation(n) if n else np.arange(0)
        try:
            yp = _to_np(_call(perm))
        except Exception as e:  # noqa: BLE001
            return {"status": "fired", "detail": f"L_perm: permuted call raised {type(e).__name__}"}
        if yp.shape != y0.shape:
            return {"status": "fired", "detail": f"L_perm: output shape changed under permutation {y0.shape}->{yp.shape}"}
        dev = float(np.max(np.abs(y0 - yp)))
        max_dev = max(max_dev, dev)
        if dev > tol:
            return {"status": "fired", "detail": f"L_perm: max deviation {dev:.3e} > tol {tol:.1e} at sample {i}"}
    return {"status": "held", "detail": f"L_perm: permutation-invariance held; max dev {max_dev:.3e} <= tol {tol:.1e}"}


# -----------------------------------------------------------------------------
# L_scale -- scaling_robustness (GPT-4 asserted INVARIANCE).
#   As authored, invariance under global scaling is FALSE for raw
#   spherical_harmonics (degree-l homogeneous) and linear TP, so shipping it would
#   fire on correct code (false positive). Therefore:
#     - default: not_applicable (faithful to "this baseline MR has no valid library
#       contract"), and
#     - OPTIONAL faithful homogeneity reformulation when the snippet supplies
#       ctx["scale_degree"]: assert f(c x) ~= c^deg * f(x). This DEVIATES from the
#       GPT-4 spec; it is flagged explicitly in the detail and only runs on opt-in,
#       so we never fabricate a relation the baseline did not author.
# -----------------------------------------------------------------------------
def mr_L_scale(fn, ctx, tol, scales=(0.5, 1.3, 2.0)):
    if "x" not in ctx:
        return {"status": "not_applicable", "detail": "L_scale: ctx lacks x"}
    deg = ctx.get("scale_degree", None)
    if deg is None:
        return {"status": "not_applicable",
                "detail": ("L_scale: GPT-4's scaling-INVARIANCE has no valid library contract "
                           "(SH/TP are homogeneous); not asserted to avoid FP. Provide "
                           "ctx['scale_degree'] for the deviating homogeneity check.")}
    x = ctx["x"]
    try:
        y0 = _to_np(fn(x))
    except Exception as e:  # noqa: BLE001
        return {"status": "not_applicable", "detail": f"L_scale baseline call failed: {type(e).__name__}"}
    max_dev = 0.0
    for c in scales:
        xc = (x * c) if (_HAS_TORCH and isinstance(x, torch.Tensor)) else (c * x)
        try:
            yc = _to_np(fn(xc))
        except Exception as e:  # noqa: BLE001
            return {"status": "fired", "detail": f"L_scale: scaled call raised {type(e).__name__}"}
        ref = (c ** deg) * y0
        if ref.shape != yc.shape:
            return {"status": "fired", "detail": f"L_scale: output shape changed under scaling {ref.shape}->{yc.shape}"}
        dev = float(np.max(np.abs(ref - yc)))
        max_dev = max(max_dev, dev)
        if dev > tol:
            return {"status": "fired",
                    "detail": f"L_scale[DEVIATES from GPT-4 spec; homogeneity deg={deg}]: dev {dev:.3e} > tol {tol:.1e} at c={c}"}
    return {"status": "held",
            "detail": f"L_scale[DEVIATES from GPT-4 spec; homogeneity deg={deg}]: held; max dev {max_dev:.3e} <= tol {tol:.1e}"}


# -----------------------------------------------------------------------------
# L_trans -- translation_invariance. No contract on a pure SH/TP/scatter function;
#   translation-invariance is a model-architecture property (relative positions),
#   not a function-level one. Honestly not_applicable to library-function bugs.
# -----------------------------------------------------------------------------
def mr_L_trans(fn, ctx, tol):
    return {"status": "not_applicable",
            "detail": ("L_trans: translation has no contract on a pure e3nn/PyG library function "
                       "(SH/TP/scatter); translation-invariance is a model-level property via "
                       "relative positions, not portable to function bugs.")}


# -----------------------------------------------------------------------------
# L_noise -- noise_robustness. No exact post-condition for a deterministic library
#   function; "robustness to Gaussian noise" is an ML-testing heuristic, not a
#   metamorphic relation. Honestly not_applicable to library-function bugs.
# -----------------------------------------------------------------------------
def mr_L_noise(fn, ctx, tol):
    return {"status": "not_applicable",
            "detail": ("L_noise: Gaussian-noise robustness is an ML-testing heuristic with no exact "
                       "post-condition for a deterministic library function; not a metamorphic "
                       "relation at the function level.")}


# Set L membership markers for the harness loader (mirrors rho_rot.py's MR marker).
MR_LIST = [
    {"name": "L_rot",   "set": "L", "callable": mr_L_rot},
    {"name": "L_perm",  "set": "L", "callable": mr_L_perm},
    {"name": "L_scale", "set": "L", "callable": mr_L_scale},
    {"name": "L_trans", "set": "L", "callable": mr_L_trans},
    {"name": "L_noise", "set": "L", "callable": mr_L_noise},
]
# Primary portable marker (single-MR compatibility with rho_rot.py-style loaders).
MR = {"name": "L_rot", "set": "L", "callable": mr_L_rot}
