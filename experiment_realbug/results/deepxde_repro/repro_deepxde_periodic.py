"""
NOETHER meta-pattern reproduction --- pde_sciml SUT domain (THIRD-PARTY PINN library).

Target bug : DeepXDE commit 83535401df0a365d9e70f48fc7b0d815dbb1cecc
             "Bug fix: Geometry.periodic_point()"
Library    : DeepXDE (lululxvi/deepxde) -- the most widely used PINN library.
             THIRD-PARTY (not authored by this paper); pip released-to-released.
NOETHER block : SYMMETRY / equivariance ("G" block). A periodic boundary condition
                u(x) = u(x + L e_k) on a periodic axis is a *discrete translation
                symmetry* of the solution: u is invariant under the period-L shift
                that the geometry's  periodic_point()  map realises. (Noether: a
                continuous/discrete symmetry of the system; the periodic-image map
                P is the group action whose orbit the PINN must tie together.)
Module        : deepxde.geometry.timedomain.GeometryXTime.periodic_point
                -> self.geometry.periodic_point(x[:-1])            # PRE  v0.8.6 (1 arg)
                -> self.geometry.periodic_point(x[:-1], component) # POST v0.9.0 (2 args, fix)

Root cause
----------
For a time-dependent PDE the geometry is  GeometryXTime(space_geometry, time) .
A space-time point is  x = [x_0, ..., x_{d-1}, t] . To build a periodic-boundary
residual on spatial component k, the library must map the boundary point to its
periodic partner WHILE leaving the time coordinate untouched:

    GeometryXTime.periodic_point(x, component)
        xp = self.geometry.periodic_point(x[:-1], component)   # space part only
        return np.append(xp, x[-1])                            # re-attach time t

The underlying multi-dimensional geometry (Rectangle -> Hypercube) has

    Hypercube.periodic_point(self, x, component)   # component is REQUIRED, no default

so it needs to know WHICH axis is periodic. In v0.8.6 the GeometryXTime wrapper
dropped the `component` argument and called  self.geometry.periodic_point(x[:-1])
with a single positional argument. Forming the periodic (symmetry) image of any
space-time boundary point therefore raises

    TypeError: periodic_point() missing 1 required positional argument: 'component'

so the translation-symmetry / periodic-BC residual cannot be formed at all.
(The same fix also removes a wrong no-op  Disk.periodic_point: return x  override
that silently ignored periodicity; the crash path reproduced here is the
GeometryXTime missing-component bug.)

Metamorphic relation (symmetry / "G" block)
-------------------------------------------
A periodic boundary condition is the statement  u(x) = u(P(x)) , where
P(x) maps a boundary point on a periodic axis to its periodic partner (the
generator of the discrete translation-symmetry group of the domain). The PINN
oracle for this block requires the symmetry-image map P to be COMPUTABLE, and
to be a correct period map:

    (a) a left-edge point on the periodic axis maps to the right edge (and back);
    (b) P is an involution on the boundary pair:  P(P(x)) = x  (shift by +L, then
        the partner shifts by -L) -- i.e. P realises the Z-translation symmetry;
    (c) the time coordinate is preserved (time is NOT periodic here);
    (d) non-periodic spatial coordinates are preserved.

If P cannot even be evaluated, the symmetry/periodicity MR  u(x) = u(P(x))
cannot be enforced.

    FIRED <=> evaluating the periodic-image (symmetry) map fails / is unavailable
    HELD  <=> P evaluates and satisfies (a)-(d)

SUT  : space = Rectangle [0,1]^2 ,  time = [0,1]  ->  GeometryXTime .
       This is the canonical geometry for a time-dependent PDE with a periodic
       spatial boundary (e.g. periodic 2D heat / wave / advection in time).
We drive the *exact* buggy line (GeometryXTime.periodic_point -> geometry.
periodic_point) directly. periodic_point is PURE NUMPY geometry: it needs no
TensorFlow/PyTorch backend, no network, and no training, so the result is
isolated from any training-loop / backend API drift and runs in CPU
milliseconds.
"""
import numpy as np

# periodic_point is pure-numpy geometry; importing deepxde.geometry does not
# require choosing/loading a tensor backend for THIS code path. (Library default
# backend in this era is TensorFlow; we never touch it -- no net, no training.)
import deepxde as dde

print("deepxde version :", dde.__version__ if hasattr(dde, "__version__")
      else __import__("importlib.metadata", fromlist=["version"]).version("deepxde"))

# --- Space-time geometry with a periodic spatial boundary ---
#   space  : unit square [0,1] x [0,1]   (Rectangle -> Hypercube)
#   time   : [0, 1]
geom = dde.geometry.Rectangle([0.0, 0.0], [1.0, 1.0])
timedomain = dde.geometry.TimeDomain(0.0, 1.0)
gxt = dde.geometry.GeometryXTime(geom, timedomain)

# A boundary collocation point on the LEFT edge of the periodic axis (component 0),
# at interior time t = 0.5:   x = [x0=0, x1=0.4, t=0.5].
x = np.array([0.0, 0.4, 0.5])
component = 0  # spatial axis 0 is the periodic axis

print(f"  space-time boundary point x = {x.tolist()} (periodic component = {component})")

fired = False
detail = ""
try:
    # THE EXACT BUGGY PATH:
    #   GeometryXTime.periodic_point(x, component)
    #     -> self.geometry.periodic_point(x[:-1])            [PRE v0.8.6: 1 arg -> TypeError]
    #     -> self.geometry.periodic_point(x[:-1], component) [POST v0.9.0: 2 args -> OK]
    xp = gxt.periodic_point(x, component)

    # --- Symmetry-MR consistency checks (only reachable on POST) ---
    # (a) periodic partner: x0=0 -> x0=1 (right edge)
    cond_a = np.isclose(xp[component], 1.0)
    # (b) involution P(P(x)) == x  (discrete translation-symmetry generator + inverse)
    xpp = gxt.periodic_point(xp, component)
    cond_b = bool(np.allclose(xpp, x))
    # (c) time coordinate preserved (time is NOT periodic)
    cond_c = bool(np.isclose(xp[-1], x[-1]))
    # (d) non-periodic spatial coordinate x1 preserved
    cond_d = bool(np.isclose(xp[1], x[1]))

    ok = cond_a and cond_b and cond_c and cond_d
    fired = not ok
    detail = (f"P(x) = {xp.tolist()}; "
              f"left->right={cond_a}, involution P(P(x))=x={cond_b} "
              f"(P(P(x))={xpp.tolist()}), time-preserved={cond_c}, "
              f"x1-preserved={cond_d}")
    print(f"  periodic-image (symmetry) map P(x) = {xp.tolist()}")
    print(f"    (a) maps to right edge x0=1 : {cond_a}")
    print(f"    (b) involution P(P(x)) = x  : {cond_b}  (P(P(x)) = {xpp.tolist()})")
    print(f"    (c) time coordinate preserved: {cond_c}")
    print(f"    (d) non-periodic x1 preserved: {cond_d}")
except Exception as e:  # noqa: BLE001
    fired = True
    detail = f"{type(e).__name__}: {e}"
    print(f"  periodic-image (symmetry) map RAISED: {detail}")

print("NOETHER symmetry/periodicity MR :",
      "FIRED (periodic-image map NOT computable/correct -> MR violated -> bug PRESENT)"
      if fired else
      "HELD (periodic-image map correct -> u(x)=u(P(x)) enforceable -> bug ABSENT)")
print("DETAIL:", detail)
print("VERDICT:", "FIRED" if fired else "HELD")

import sys
sys.exit(1 if fired else 0)
