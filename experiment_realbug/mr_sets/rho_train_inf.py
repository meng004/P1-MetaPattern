#!/usr/bin/env python3
"""rho_train_inf - inference-idempotency MR ported to library functions (Set N).

Paper origin (NOETHER_paper_arxiv.tex, L864-866): rho_train is the
"inference-idempotency MR for the L* block". L* is the limit-operator block; the
ML instantiation reads the *trained* network as the fixed point of the training
limit operator, at which repeated inference is idempotent (L1283: a model "passes
inference idempotency"). The literal predicate there is training/inference-time:
put the net in .eval() mode and re-run it - the output is stable.

APPLICABILITY TO A PURE LIBRARY FUNCTION: adaptable, NOT portable verbatim.
A standalone e3nn / PyG tensor op has no training, no .eval()/.train() mode, no
"trained-limit fixed point" - the trained-network framing is *not_applicable*. What
DOES survive the Translate is the L*-block invariant stripped of the training story:
a deterministic operation evaluated twice on the same input must return the same
output and must not mutate that input. This is the library-level reading of
inference idempotency - referential transparency / purity / determinism:

    fn(x) == fn(x)               (call-stability / determinism)
    x unchanged after fn(x)      (no in-place clobber of the input)

We deliberately do NOT assert fn(fn(x)) == fn(x) in general: a tensor product or a
spherical-harmonics evaluation is not an idempotent endomorphism, so demanding
P=P^2 would be a fabricated relation. The honest, general L*-port for an arbitrary
library callable is determinism + input-purity. (An optional true-idempotent check
fires only when ctx explicitly flags the op as idempotent.)

Defect classes this surfaces in e3nn / PyG library code (bug distribution external):
  - non-deterministic scatter/index reductions (scatter_add / index_add ordering,
    unstable atomic accumulation) returning different values on repeat calls;
  - in-place mutation of an input buffer (a tensor-product / irreps path that writes
    back into x, so the 2nd call on the SAME tensor object differs);
  - stale-cache / global-state bugs: e3nn caches Wigner-D, Clebsch-Gordan, or
    irreps metadata keyed wrongly, so a second call returns a stale/corrupted result;
  - buffer aliasing where output views share storage with the input.

CPU-only, no training, no full forward pass. Interface per mr_sets/README.md.

ctx must provide:
  ctx["x"]            : the base input fn accepts (torch.Tensor / np.ndarray, or a
                        tuple/list of such for multi-arg ops). Built by the bug's
                        repro snippet, not here.
ctx may provide:
  ctx["call"]         : optional callable call(fn, x) -> y, if fn needs a custom
                        invocation (e.g. unpacking a tuple of args). Default applies
                        fn(*x) when x is a tuple/list, else fn(x).
  ctx["idempotent"]   : optional bool; if True the op is declared an idempotent
                        endomorphism (e.g. a normalisation / projection) and the
                        fn(fn(x)) == fn(x) check is additionally run. Default False.
  ctx["num_repeats"]  : optional int, how many repeat calls (default 4).
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


def _snapshot(x):
    """Deep, immutable numpy snapshot of x (handles tensor / array / tuple / list)."""
    if isinstance(x, (tuple, list)):
        return tuple(_snapshot(e) for e in x)
    return _to_np(x).copy()


def _flatten(y):
    """Flatten an arbitrary (possibly nested / tuple) output into a list of np arrays."""
    if isinstance(y, (tuple, list)):
        out = []
        for e in y:
            out.extend(_flatten(e))
        return out
    return [_to_np(y)]


def _max_abs_diff(ya, yb):
    fa, fb = _flatten(ya), _flatten(yb)
    if len(fa) != len(fb):
        return float("inf"), f"output arity changed {len(fa)}->{len(fb)}"
    worst = 0.0
    for a, b in zip(fa, fb):
        a = np.asarray(a)
        b = np.asarray(b)
        if a.shape != b.shape:
            return float("inf"), f"output shape changed {a.shape}->{b.shape}"
        if a.size == 0:
            continue
        d = float(np.max(np.abs(a.astype(np.float64) - b.astype(np.float64))))
        worst = max(worst, d)
    return worst, None


def _input_changed(before, x_obj):
    """Did calling fn mutate the input in place? Compare post-call snapshot to the
    pre-call snapshot of the SAME object."""
    after = _snapshot(x_obj)
    bf, af = _flatten(before), _flatten(after)
    if len(bf) != len(af):
        return True, float("inf")
    worst = 0.0
    for a, b in zip(bf, af):
        if a.shape != b.shape:
            return True, float("inf")
        if a.size == 0:
            continue
        worst = max(worst, float(np.max(np.abs(a.astype(np.float64) - b.astype(np.float64)))))
    return (worst > 0.0), worst


def mr_rho_train_inf(fn, ctx, tol):
    if "x" not in ctx:
        return {"status": "not_applicable",
                "detail": "ctx lacks 'x'; no input to probe inference idempotency on"}
    x = ctx["x"]
    num_repeats = int(ctx.get("num_repeats", 4))
    declared_idem = bool(ctx.get("idempotent", False))

    def default_call(f, xx):
        if isinstance(xx, (tuple, list)):
            return f(*xx)
        return f(xx)

    call = ctx.get("call", default_call)

    # Baseline call + record input snapshot taken BEFORE the call.
    pre = _snapshot(x)
    try:
        y0 = call(fn, x)
    except Exception as e:  # noqa: BLE001
        # A baseline that cannot even run is not this MR's signal; rotation-style MRs
        # treat baseline failure as not_applicable, mirror that here.
        return {"status": "not_applicable",
                "detail": f"baseline call failed: {type(e).__name__}: {e}"}

    # (1) Input purity: fn must not mutate its input in place.
    mutated, mut_dev = _input_changed(pre, x)
    if mutated:
        return {"status": "fired",
                "detail": f"input mutated in place by fn (max change {mut_dev:.3e}); "
                          f"breaks inference idempotency / referential transparency"}

    # (2) Determinism: repeated calls on the same input must agree within tol.
    max_dev = 0.0
    for i in range(1, num_repeats + 1):
        try:
            yi = call(fn, x)
        except Exception as e:  # noqa: BLE001
            # An exception only on a repeat call (baseline succeeded) is a real
            # instability; FIXED code does not raise -> counts as fired.
            return {"status": "fired",
                    "detail": f"repeat call {i} raised {type(e).__name__} though baseline succeeded"}
        dev, shape_msg = _max_abs_diff(y0, yi)
        if shape_msg is not None:
            return {"status": "fired", "detail": f"repeat call {i}: {shape_msg}"}
        max_dev = max(max_dev, dev)
        if dev > tol:
            return {"status": "fired",
                    "detail": f"non-deterministic: repeat call {i} deviates {dev:.3e} > tol {tol:.1e}"}

    # (3) Optional TRUE idempotence fn(fn(x)) == fn(x), only if op declares itself
    #     an idempotent endomorphism (else this would be a fabricated relation).
    if declared_idem:
        if isinstance(x, (tuple, list)):
            return {"status": "not_applicable",
                    "detail": "idempotent check unsupported for multi-arg ops"}
        try:
            y2 = call(fn, y0)
        except Exception as e:  # noqa: BLE001
            return {"status": "fired",
                    "detail": f"fn(fn(x)) raised {type(e).__name__} for declared-idempotent op"}
        dev, shape_msg = _max_abs_diff(y0, y2)
        if shape_msg is not None:
            return {"status": "fired", "detail": f"declared-idempotent op: fn(fn(x)) {shape_msg}"}
        if dev > tol:
            return {"status": "fired",
                    "detail": f"declared-idempotent op violates fn(fn(x))=fn(x): dev {dev:.3e} > tol {tol:.1e}"}
        max_dev = max(max_dev, dev)

    return {"status": "held",
            "detail": f"inference idempotency held: pure + deterministic over "
                      f"{num_repeats} repeats, max deviation {max_dev:.3e} <= tol {tol:.1e}"}


# Set N membership marker for the harness loader
MR = {"name": "rho_train_inf", "set": "N", "callable": mr_rho_train_inf}
