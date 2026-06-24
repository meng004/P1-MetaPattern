"""
NOETHER meta-pattern reproduction --- pde_sciml SUT domain (THIRD-PARTY PINN library).

Target bug : DeepXDE commit 4bac5ebb5cd7ac07356c95e283c6a05838f6bf34
             "Bug fix: NeumannBC and RobinBC"
Library    : DeepXDE (lululxvi/deepxde) -- the most widely used PINN library.
             THIRD-PARTY (not authored by this paper); pip released-to-released.
NOETHER block : conservation / flux  (a Neumann boundary  n . grad u = g  is the
                PINN encoding of a prescribed boundary flux; g = 0 is the zero-flux
                / mass-conservation boundary  d/dt int_Omega u = 0 ).
Module        : deepxde.icbc.boundary_conditions.BC.normal_derivative
                -> self.boundary_normal(X, beg, end)        # PRE  v1.3.0  (3 args)
                -> self.boundary_normal(X, beg, end, None)  # POST v1.3.1  (4 args, fix)

Root cause
----------
In v1.3.0 the boundary normal used to build the flux/Neumann residual is wrapped
by `npfunc_range_autocache`, whose every wrapper has signature (X, beg, end, _) --
FOUR positional arguments. `BC.normal_derivative` (used by NeumannBC and RobinBC
to form the flux residual  n . grad u ) called it with only THREE arguments.
Evaluating the Neumann/Robin (flux) boundary residual therefore raises
    TypeError: wrapper_*() missing 1 required positional argument: '_'
so the conservation/flux boundary residual cannot be formed at all.

Metamorphic relation (conservation / flux block)
------------------------------------------------
A Neumann boundary condition  n . grad u = g  on dOmega is exactly the discrete
statement of a prescribed boundary flux; with g = 0 it is the zero-flux
(mass/energy conservation) boundary. The PINN oracle for this block: the flux
residual  r_flux = n . grad u - g  must be COMPUTABLE and finite at the boundary
collocation points. If the library cannot evaluate  n . grad u , the
conservation/flux MR cannot be enforced.

    FIRED <=> evaluating the Neumann (flux) boundary residual fails / is unavailable
    HELD  <=> the flux residual evaluates to a finite tensor

SUT  : 1D Poisson  u_xx = 2  on (-1, 1), NEUMANN (flux) boundary  n . grad u = 2(x+1)
       at x = +1  (the library's own canonical Neumann example).
We drive the *exact* buggy line (BC.error -> normal_derivative -> boundary_normal)
directly, with a tiny net and a single boundary point, so the result is isolated
from any training-loop API drift and runs in CPU milliseconds.
"""
import os
os.environ.setdefault("DDEBACKEND", "pytorch")
import numpy as np
import deepxde as dde
from deepxde import backend as bkd

print("deepxde version :", dde.__version__)
print("backend         :", dde.backend.backend_name)


def boundary_r(x, on_boundary):
    return on_boundary and np.isclose(x[0], 1)


# --- Neumann (flux / conservation) boundary on the right end x = +1 ---
geom = dde.geometry.Interval(-1, 1)
bc = dde.icbc.NeumannBC(geom, lambda X: 2 * (X + 1), boundary_r)

# Boundary collocation point(s): the right end x = 1, where n.grad u is prescribed.
X = np.array([[1.0]])                       # one boundary point is enough
beg, end = 0, 1

# Tiny linear "network" u(x) = x  (so grad u is well-defined & nonzero); we only
# need a differentiable output to exercise the flux-residual code path.
inputs = bkd.as_tensor(X.astype(dde.config.real(np)))
inputs.requires_grad_()
outputs = inputs * 1.0                      # u = x  ->  du/dx = 1

fired = False
detail = ""
try:
    # THE EXACT BUGGY PATH: NeumannBC.error -> BC.normal_derivative
    #                       -> self.boundary_normal(X, beg, end)   [PRE: 3 args]
    err = bc.error(X, inputs, outputs, beg, end)
    val = bkd.to_numpy(err)
    finite = bool(np.all(np.isfinite(val)))
    print(f"  Neumann flux residual (n.grad u - g) = {val.ravel()}")
    fired = not finite
    detail = f"flux residual computed = {val.ravel().tolist()}"
except Exception as e:
    fired = True
    detail = f"{type(e).__name__}: {e}"
    print(f"  Neumann (flux) BC residual RAISED: {detail}")

print("NOETHER conservation/flux MR :",
      "FIRED (flux residual NOT computable -> MR violated -> bug PRESENT)" if fired
      else "HELD (flux residual finite -> MR satisfied -> bug ABSENT)")
print("DETAIL:", detail)
print("VERDICT:", "FIRED" if fired else "HELD")
import sys
sys.exit(1 if fired else 0)
