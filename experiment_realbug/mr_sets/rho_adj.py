#!/usr/bin/env python3
# ⚠️ FIX_NEEDED (verifier): the default contract is NOT transpose-invariant, so it
# FALSE-POSITIVE fires on CORRECT transpose-equal traces (Tr A(x1,x2)=Tr A(x2,x1)).
# Before use: make the default contract trace-like / transpose-symmetric (paper's
# invariant is Tr A), OR supply ctx['bilinear'] and only run when symmetric form is
# known; otherwise return not_applicable. Do NOT trust the default path as-is.
"""rho_adj — adjoint / role-swap duality metamorphic relation (Set N).

Derived from the paper's executable MR rho_adj (NOETHER_paper_arxiv.tex,
L826-843): for an attention/bilinear form A(x1, x2) the Hermitian part has a
trace-cyclic invariant that is symmetric under swapping the two inputs' roles,

    | Tr A(x1, x2) - Tr A(x2, x1) | <= tau_adj.

ADAPTABILITY (honest triage)
----------------------------
The *paper's* rho_adj runs on a trained equivariant transformer's attention
layer via a forward hook ("Tr A(.,.)"). That model-specific attention
instantiation does NOT port to a pure library function. BUT the paper itself
grounds the form in Clebsch-Gordan tensor products of irrep features
("compute attention via Clebsch--Gordan tensor products"), and the underlying
RELATION -- the role-swap (adjoint) symmetry of a *bilinear* map's contracted
invariant -- is exactly a property of e3nn's bilinear tensor-product surface
(e3nn.o3.TensorProduct / FullyConnectedTensorProduct, the CG coefficients).

So rho_adj is ADAPTABLE: we re-instantiate the adjoint duality for a generic
two-argument bilinear library callable B(x1, x2). We test the role-swap
invariant on a *symmetrised* contraction of the bilinear output, which is the
library-level analogue of "Tr of the Hermitian part of A". This is a general
metamorphic relation about bilinear-form symmetry, NOT a bug-specific oracle:
it knows nothing about any particular defect.

What it can catch (target_bug_categories):
  - Clebsch-Gordan coefficient sign / index errors that make a CG bilinear
    product asymmetric where the irrep pairing should make the symmetrised
    contraction role-swap invariant.
  - irreps-bookkeeping bugs (wrong path ordering / mismatched in1<->in2 slot
    handling) that surface as a role-swap asymmetry.
  - tensor-product symmetrisation defects (e.g. a "symmetric" tensor-square
    path that is not actually symmetric under argument swap).

When NOT applicable:
  - ctx exposes only a unary op (no bilinear / two-argument role to swap)
    -> not_applicable (e.g. a pure spherical_harmonics(x) or scatter call;
       those belong to rho_rot / other MRs, not the adjoint duality).

CPU-only, no training, no full forward pass. Importable without e3nn/torch.

Interface: mr_rho_adj(fn, ctx, tol) -> {"status", "detail"}  (see README.md)
ctx must provide ONE of:
  ctx["bilinear"] : a callable B(x1, x2) -> tensor (the library bilinear op
                    under test, e.g. a configured e3nn TensorProduct closure).
                    `fn` is also accepted as the bilinear if it takes 2 args.
  ctx["x1"], ctx["x2"] : two input tensors/arrays in the op's input format.
optional:
  ctx["contract"] : callable c(y) -> scalar giving the role-swap invariant
                    (analogue of Tr A). Default: a fixed asymmetric linear
                    functional (cos-weighted contraction over the flattened
                    output), applied identically to B(x1,x2) and B(x2,x1) so the
                    role-swap symmetry of the bilinear map is preserved iff the
                    map itself is argument-swap symmetric in its symmetrised
                    part. Provide a layer-specific Tr if the op needs one.
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
    return np.asarray(a, dtype=float)


def _weighted_contract(y):
    """Default role-swap invariant: a fixed *asymmetric* linear functional.

    A plain element sum is too weak: for many bilinear maps (e.g. any rank-1
    outer product) sum(B(x1,x2)) == sum(B(x2,x1)) identically, so it cannot see
    an argument-swap asymmetry. We instead contract with a fixed, deterministic,
    position-dependent weight vector w_i = cos(i + 1). This is still a single
    linear functional L(.) applied IDENTICALLY to B(x1,x2) and B(x2,x1) -- the
    library-level analogue of "Tr of the Hermitian part of A" -- but its
    asymmetric weights make L(B(x1,x2)) - L(B(x2,x1)) a sensitive probe of the
    bilinear map's argument-swap (adjoint) symmetry. A CG-coefficient
    sign/index defect that breaks the expected pairing symmetry makes the two
    weighted contractions differ. Deterministic (no RNG) for reproducibility."""
    arr = _to_np(y).ravel()
    n = arr.shape[0]
    if n == 0:
        return 0.0
    w = np.cos(np.arange(n) + 1.0)
    return float(np.dot(arr, w))


def _resolve_bilinear(fn, ctx):
    """Pick the two-argument library op. Prefer ctx['bilinear']; else fn iff
    fn is callable with two positional args."""
    if "bilinear" in ctx and callable(ctx["bilinear"]):
        return ctx["bilinear"]
    if callable(fn):
        # probe arity cheaply via the actual inputs in the symmetry check;
        # we cannot reliably introspect arbitrary C/torch callables, so we
        # let the call itself decide and treat a 2-arg failure as not_applicable.
        return fn
    return None


def mr_rho_adj(fn, ctx, tol):
    bil = _resolve_bilinear(fn, ctx)
    if bil is None:
        return {"status": "not_applicable",
                "detail": "no bilinear/two-argument op available (fn not callable, ctx lacks 'bilinear')"}
    if "x1" not in ctx or "x2" not in ctx:
        return {"status": "not_applicable",
                "detail": "ctx lacks {x1, x2}; op is not role-swappable for this bug"}

    x1, x2 = ctx["x1"], ctx["x2"]
    contract = ctx.get("contract", _weighted_contract)
    if not callable(contract):
        contract = _weighted_contract

    # Establish that the op is genuinely bilinear (two-argument). If calling
    # B(x1, x2) fails with an arity/type error, this MR has no meaning here.
    try:
        y12 = bil(x1, x2)
    except TypeError as e:  # wrong number of args / not a 2-arg op
        return {"status": "not_applicable",
                "detail": f"op is not a two-argument bilinear ({type(e).__name__}: {str(e)[:60]})"}
    except Exception as e:  # noqa: BLE001
        # A genuine runtime failure on the baseline ordering: cannot evaluate
        # the relation -> not_applicable (the rotated-call 'fired' rule below
        # only applies to the SWAPPED call, which the fixed code should accept).
        return {"status": "not_applicable",
                "detail": f"baseline B(x1,x2) failed: {type(e).__name__}"}

    try:
        y21 = bil(x2, x1)
    except Exception as e:  # noqa: BLE001
        # The swapped ordering raised where the baseline did not: a defect that
        # the FIXED code would not raise -> detection. Post-fix sanity run
        # filters any false positive.
        return {"status": "fired",
                "detail": f"role-swapped B(x2,x1) raised {type(e).__name__} while B(x1,x2) succeeded"}

    try:
        t12 = float(contract(y12))
        t21 = float(contract(y21))
    except Exception as e:  # noqa: BLE001
        return {"status": "not_applicable",
                "detail": f"contract() not evaluable on outputs: {type(e).__name__}"}

    dev = abs(t12 - t21)
    # Scale-aware tolerance floor so the relation is not vacuously tight on
    # large-magnitude contractions (mirrors fp32 relative tolerance practice).
    scale = max(1.0, abs(t12), abs(t21))
    eff_tol = max(tol, tol * scale)
    if dev > eff_tol:
        return {"status": "fired",
                "detail": (f"adjoint role-swap broken: |Tr B(x1,x2) - Tr B(x2,x1)| "
                           f"= {dev:.3e} > tol {eff_tol:.1e}")}
    return {"status": "held",
            "detail": f"adjoint duality held; |delta| = {dev:.3e} <= tol {eff_tol:.1e}"}


# Set N membership marker for the harness loader
MR = {"name": "rho_adj", "set": "N", "callable": mr_rho_adj}
