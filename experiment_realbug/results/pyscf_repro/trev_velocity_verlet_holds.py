"""
Trev* (time-reversal) probe on PySCF's ONLY reversible-dynamics substrate in the
main pyscf/pyscf repo at modern HEAD: the velocity-Verlet BOMD integrator
(pyscf.md.integrators.VelocityVerlet).

NOETHER Trev* MR: integrate a conservative dynamical system forward to T,
reverse the momenta (v -> -v), integrate again for T steps; the system must
return to its initial geometry. Velocity-Verlet is symplectic and exactly
time-reversible, so this MR is satisfied BY CONSTRUCTION -> no fire-able bug.

This script substantiates the structural negative: the reversible substrate that
exists (BOMD Verlet) holds the Trev* invariant; the candidate that would have a
time-stepping unitary propagator (rt-TDDFT) was REMOVED from the main repo at
v2.0.0 (commit 137c23d3...).
"""
import numpy as np
from pyscf import gto, scf
from pyscf.md.integrators import VelocityVerlet

np.set_printoptions(precision=10, suppress=True)

# Small, cheap, conservative system: H2 at RHF (NVE, no thermostat -> energy-
# conserving, time-reversible Hamiltonian dynamics).
mol = gto.M(atom="H 0 0 0; H 0 0 0.74", basis="sto-3g", unit="Angstrom", verbose=0)
mf = scf.RHF(mol)

DT = 5.0     # a.u. time step
NSTEPS = 20  # forward steps

r0 = mol.atom_coords().copy()          # initial geometry (Bohr)
v0 = np.array([[0.0, 0.0,  3.0e-4],    # small initial velocity, equal/opposite
               [0.0, 0.0, -3.0e-4]])   # (keeps COM fixed)

# ---- forward integration to T ----
fwd = VelocityVerlet(mf, dt=DT, steps=NSTEPS, veloc=v0.copy())
fwd.kernel()
rT = fwd.mol.atom_coords().copy()
vT = fwd.veloc.copy()

# ---- reverse momenta and integrate back for the same number of steps ----
# Time-reversal: r -> r, v -> -v. A reversible integrator must return to r0.
mol_rev = mol.copy()
mol_rev.set_geom_(rT, unit="Bohr")
mf_rev = scf.RHF(mol_rev)
rev = VelocityVerlet(mf_rev, dt=DT, steps=NSTEPS, veloc=-vT)
rev.kernel()
r_back = rev.mol.atom_coords().copy()
v_back = rev.veloc.copy()

# ---- Trev* oracle: forward -> reverse -> initial invariant ----
geom_return_err = np.max(np.abs(r_back - r0))
# After reversing momenta and integrating back, velocity should be -v0.
veloc_return_err = np.max(np.abs(v_back - (-v0)))

TOL = 1e-8
held = (geom_return_err < TOL) and (veloc_return_err < TOL)

print("pyscf version :", __import__("pyscf").__version__)
print("integrator    : VelocityVerlet (pyscf.md.integrators) -- symplectic, reversible")
print("dt / steps    :", DT, "/", NSTEPS)
print("max|r_back - r0|        =", f"{geom_return_err:.3e}")
print("max|v_back - (-v0)|     =", f"{veloc_return_err:.3e}")
print("tolerance               =", TOL)
print("Trev* MR (fwd->rev->init):", "HELD" if held else "FIRED")
print()
print("INTERPRETATION: the only reversible-dynamics substrate present in the main")
print("pyscf/pyscf repo (velocity-Verlet BOMD) satisfies the Trev* invariant by")
print("construction. The rt-TDDFT unitary-propagator module (the genuine Magnus/")
print("MMUT candidate) was removed from the main repo at v2.0.0 (137c23d3...), so it")
print("is out of the paper SUT repo at every modern version. No fire-able Trev* bug.")
assert held, "Velocity-Verlet must be time-reversible"
