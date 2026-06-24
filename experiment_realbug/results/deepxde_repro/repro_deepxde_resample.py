"""
NOETHER pde_sciml L* (convergence / limit-operator) block
-- DeepXDE PINN training data: collocation set must be FIXED for the loss
   minimisation to converge to a unique limit.

Target bug : DeepXDE commit 4adcde7 "Bug fix: re-generate data each step"
             (in v0.5.1, NOT in v0.5.0).
Library    : DeepXDE (lululxvi/deepxde) -- the most widely used PINN library.
             THIRD-PARTY (not authored by this paper); pip released-to-released
             (pre 0.5.0 / post 0.5.1).

NOETHER block : L* (limit operators / convergence). A PINN minimises a residual
                loss on a FIXED set of collocation points X. The training is a
                discrete limit process theta_t -> theta* that converges to the
                minimiser of L(theta; X) for a fixed X. If X is re-sampled at
                every optimisation step, the objective L(theta; X_t) changes each
                step: the optimiser chases a moving target and the limit operator
                (convergence of the training sequence to a fixed problem's
                minimiser) is broken.

Module / root cause (deepxde/data/pde.py and ide.py)
----------------------------------------------------
PDE.train_next_batch() caches the collocation set via a decorator:

    PRE  (0.5.0):  @run_if_any_none("train_x", "train_y")   def train_next_batch
    POST (0.5.1):  @run_if_all_none("train_x", "train_y")   def train_next_batch

`run_if_any_none(*attr)` re-executes the wrapped method if ANY of the named
attributes is None; `run_if_all_none(*attr)` re-executes only if ALL are None.
For an UNSUPERVISED PINN (func=None -- the standard PINN setting where there is
no reference solution and only the PDE residual drives training), `train_y` is
ALWAYS None. Therefore:

  * PRE: any(train_x, train_y is None) == True on EVERY call (train_y always None)
         -> train_next_batch() re-runs train_points() every step
         -> collocation set re-sampled each step -> objective moves -> no fixed
            limit (L* violation).
  * POST: all(train_x, train_y is None) becomes False once train_x is generated
         -> cached set returned -> the problem is fixed -> training converges to
            the minimiser of a single, fixed objective (L* holds).

Metamorphic relation (L* / convergence)
---------------------------------------
The training objective must be defined on a FIXED collocation set across
optimisation steps, so the loss-minimisation sequence converges to the minimiser
of a single fixed problem:

    Calling train_next_batch() repeatedly (= successive training steps) must NOT
    re-generate the collocation set once it has been built.

    FIRED <=> the collocation set is regenerated on subsequent steps
              (train_points() invoked again -> objective is a moving target)
    HELD  <=> the collocation set is cached / fixed across steps

This is the EXACT buggy decorator path (PDE.train_next_batch -> train_points).
PDE.__init__ itself calls train_next_batch() once, so the path is exercised
directly. The check counts how many times train_points() (the re-generation
routine) is actually invoked across simulated training steps; this is pure NumPy
geometry sampling -- no network, no TensorFlow session, no gradient -- so it runs
in CPU milliseconds. (The 0.5.x-era pde.py does `import tensorflow as tf` at
module top, so TF must be importable, but it is never EXECUTED on this path:
a TF2 wheel satisfies the import while the buggy numpy path is unaffected.)

SUT : 1-D Interval [0,1], dummy PDE residual, one Dirichlet BC, unsupervised
      (func=None) -- the canonical minimal PINN data object. The bug is
      independent of the PDE; any unsupervised PINN (the dominant PINN use case)
      triggers it.
"""
import sys
import importlib.metadata as md

import numpy as np
import deepxde as dde
from deepxde.data.pde import PDE
from deepxde.geometry import Interval

N_STEPS = 5  # number of simulated subsequent training steps


def main():
    ver = md.version("deepxde")
    print("deepxde version:", ver)

    geom = Interval(0.0, 1.0)
    pde = lambda x, y: y  # dummy residual; never executed on the numpy path
    bc = dde.DirichletBC(geom, lambda x: 0.0, lambda x, on: on)

    # Instrument train_points() (the collocation re-generation routine) to count
    # how many times it is actually invoked -- this is the re-generation signal.
    calls = {"n": 0}
    orig_train_points = PDE.train_points

    def counting_train_points(self):
        calls["n"] += 1
        return orig_train_points(self)

    PDE.train_points = counting_train_points
    try:
        # __init__ calls train_next_batch() once -> 1 legitimate generation.
        data = PDE(geom, 1, pde, [bc], num_domain=16, num_boundary=2, func=None)
        n_after_init = calls["n"]
        unsupervised = data.train_y is None
        print(f"  unsupervised (func=None -> train_y is None): {unsupervised}")
        print(f"  train_points() invoked during __init__: {n_after_init}")

        # Simulate N subsequent training steps; each step calls train_next_batch().
        for _ in range(N_STEPS):
            data.train_next_batch()
        regen = calls["n"] - n_after_init
        print(f"  train_points() RE-invoked over {N_STEPS} subsequent steps: {regen}")
    finally:
        PDE.train_points = orig_train_points  # restore

    fired = regen > 0
    print("NOETHER L* (convergence / fixed-objective) MR :",
          f"FIRED (collocation set re-generated each step ({regen} re-samples over "
          f"{N_STEPS} steps) -> objective is a moving target -> training does not "
          "converge to a fixed problem -> bug PRESENT)"
          if fired else
          f"HELD (collocation set cached after first build (0 re-samples over "
          f"{N_STEPS} steps) -> fixed objective -> training converges -> bug ABSENT)")
    print("VERDICT:", "FIRED" if fired else "HELD")
    sys.exit(1 if fired else 0)


if __name__ == "__main__":
    main()
