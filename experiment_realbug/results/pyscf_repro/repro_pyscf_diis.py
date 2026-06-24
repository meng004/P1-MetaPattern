"""
NOETHER L* (self-consistency / convergence) block reproduction:
symmetry-adapted ROHF DIIS instability due to numerical noise.

MR (metamorphic relation / invariant -- L* self-consistency block):
    A correct SCF solver, given a well-posed closed-shell/open-shell problem,
    must reach the *same* fixed point of the self-consistent field regardless of
    numerical noise injected by the symmetry-adapted DIIS error-vector build.
    Operationally the L* relation is:
        (i)  mf.converged is True within max_cycle, AND
        (ii) e_tot equals the reference SCF energy (deterministic across runs).
    A DIIS that lets symmetry-forbidden, numerically-noisy off-diagonal error
    elements accumulate violates (i)/(ii): the iteration fails to converge and
    the returned energy *wanders run-to-run* -- the self-consistency fixed point
    is not reached.

PySCF target: pyscf/scf/diis.py + pyscf/scf/hf_symm.py (symmetry-adapted SCF DIIS).
Fix commit:  15920e60e32ef471f639505720ab18f0ef2c7da9
             "DIIS instability due to numerical noises (fix issue #1524) (#1638)"
             The fix builds the C.T(SDF-FDS)C error vector in an orthonormal
             basis and zeroes symmetry-forbidden elements, so numerical noise no
             longer accumulates in insignificant off-diagonal entries.
Pre  v2.2.0: symmetry-adapted ROHF DIIS unstable -> NOT converged, e_tot drifts.
Post v2.2.1: converged + deterministic e_tot = -74.7874921601008.

SUT: O atom, spin=2 (triplet), basis=cc-pVDZ, symmetry=True, ROHF. CPU seconds.

Reproduce (pip released-to-released, compatible dependency stack):
    uv venv --python 3.10 /tmp/venv_pyscf22
    # PRE -> FIRED (not converged; e_tot wanders run-to-run)
    VIRTUAL_ENV=/tmp/venv_pyscf22 uv pip install "pyscf==2.2.0" "numpy<1.24" "scipy<1.10" "h5py<3.9"
    /tmp/venv_pyscf22/bin/python results/pyscf_repro/repro_pyscf_diis.py
    # POST -> HELD (converged; e_tot = -74.7874921601008)
    VIRTUAL_ENV=/tmp/venv_pyscf22 uv pip install "pyscf==2.2.1"
    /tmp/venv_pyscf22/bin/python results/pyscf_repro/repro_pyscf_diis.py

Dependency note: pyscf 2.2.x (2022 era) is incompatible with numpy>=2 / scipy>=1.10
(cho_solve / lstsq API + removed numpy aliases). The compatible stack that makes
import + SCF run cleanly is numpy 1.23.5 + scipy 1.9.3 + h5py 3.8.0 on Python 3.10.
"""
import numpy as np
from pyscf import gto, scf
import pyscf

print("pyscf version:", pyscf.__version__)
print("numpy:", np.__version__)

REF_ETOT = -74.7874921601008   # post-fix converged ROHF energy (issue #1524 / #1638)
ETOL = 1e-7                    # match-the-reference tolerance for the L* relation

mol = gto.Mole()
mol.atom = 'O 0 0 0'
mol.basis = 'ccpvdz'
mol.spin = 2          # triplet oxygen (open shell -> ROHF)
mol.symmetry = True   # symmetry-adapted SCF triggers the DIIS noise path
mol.verbose = 0
mol.build()
print("groupname:", mol.groupname, "| nelec:", mol.nelectron, "| spin:", mol.spin)

# Repeat the SCF several times: the pre-fix bug is *numerical noise* in the
# symmetry-adapted DIIS, so the failure is non-deterministic in the energy while
# the converged flag stays False. Multiple runs confirm the FIRED verdict is
# stable even though the wandering energy is flaky.
N_REPEAT = 5
results = []
for i in range(N_REPEAT):
    mol_i = gto.Mole()
    mol_i.atom = 'O 0 0 0'
    mol_i.basis = 'ccpvdz'
    mol_i.spin = 2
    mol_i.symmetry = True
    mol_i.verbose = 0
    mol_i.build()
    mf = scf.ROHF(mol_i)
    mf.conv_tol = 1e-9
    mf.max_cycle = 100
    e = mf.kernel()
    held_i = bool(mf.converged) and abs(e - REF_ETOT) < ETOL
    results.append((bool(mf.converged), float(e), held_i))
    print(f"run {i}: converged={mf.converged!s:5s}  "
          f"e_tot={e:.13f}  |e-ref|={abs(e-REF_ETOT):.3e}  "
          f"{'HELD' if held_i else 'FIRED'}")

n_held = sum(1 for _, _, h in results if h)
n_conv = sum(1 for c, _, _ in results if c)
energies = [e for _, e, _ in results]
spread = max(energies) - min(energies)

print("-" * 60)
print(f"converged: {n_conv}/{N_REPEAT}   held: {n_held}/{N_REPEAT}")
print(f"e_tot spread across runs = {spread:.3e}  "
      f"(min={min(energies):.10f}, max={max(energies):.10f})")
print(f"reference e_tot          = {REF_ETOT:.13f}")

# L* verdict: HELD only if every run converged AND matched the reference energy.
all_held = (n_held == N_REPEAT)
print("VERDICT:", "HELD (self-consistency reached, deterministic)"
      if all_held else
      "FIRED (DIIS instability: not converged / energy wanders)")
