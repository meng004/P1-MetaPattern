"""
NOETHER G (point-group symmetry) block reproduction:
D2h axis-convention bug makes the MO irrep labels of a molecule depend on how its
geometry is entered (orientation), violating point-group invariance.

MR (G symmetry block, point-group invariance of irrep labelling):
    A molecule's point group is a property of the molecule, not of the Cartesian
    orientation in which its atoms are typed in. Hence the symmetry-adapted SCF must
    assign the SAME irreducible-representation label to each canonical molecular
    orbital regardless of an orientation that merely permutes/relabels the Cartesian
    axes (a symmetry-equivalent re-description). Operationally, for planar D2h
    ethylene in STO-3G RHF:
        orbsym(perm) == orbsym(reference)   for every axis permutation `perm`
    where orbsym is the tuple of Mulliken irrep ids of the converged MOs.
    Source     : the canonical reference orbsym (the molecule's true MO symmetries).
    Follow-up  : the same molecule entered with the C, H coordinates' axes permuted.
    Violation (FIRED): the irrep tuple changes with orientation -- the implementation
        picked a D2h axis convention that depends on input orientation, so equivalent
        descriptions of the SAME molecule get DIFFERENT (and partly wrong) irreps.

PySCF target: pyscf/symm/geom.py  _adjust_planar_d2h() + detect_symm() D2 branch.
Fix commit:  4542fe9b "Fix #2773 (cf. #3166) (#3176)" -- corrects the planar-D2h
             axis-selection logic (and an indentation bug on alias_axes) so the X
             axis is perpendicular to the molecular plane and Z passes through the
             most atoms, *independent of input orientation*. The upstream unittest
             test_d2h_conventions.py asserts ethylene's orbsym is identical for all
             six axis permutations.
Pre  v2.12.1: orbsym depends on input orientation (some permutations FIRED).
Post v2.13.0: orbsym identical and correct for all six permutations.

SUT: ethylene C2H4 (planar, D2h), basis STO-3G, RHF, symmetry=True. CPU seconds.

Reproduce (pip released-to-released):
    uv venv --python 3.11 /tmp/venv_pyscf_symm
    # PRE -> FIRED
    VIRTUAL_ENV=/tmp/venv_pyscf_symm uv pip install "pyscf==2.12.1"
    /tmp/venv_pyscf_symm/bin/python results/pyscf_repro/repro_pyscf_d2h_symm.py
    # POST -> HELD
    VIRTUAL_ENV=/tmp/venv_pyscf_symm uv pip install "pyscf==2.13.0"
    /tmp/venv_pyscf_symm/bin/python results/pyscf_repro/repro_pyscf_d2h_symm.py
"""
import numpy as np
from pyscf import gto, scf
import pyscf

print("pyscf version:", pyscf.__version__)
print("numpy version:", np.__version__)

# Ethylene geometry (planar, D2h). Coordinates from the upstream unittest
# pyscf/symm/test/test_d2h_conventions.py (commit 4542fe9b). The molecular plane
# is the y-z plane (x = 0 for every atom); the C2 axes lie along y and z.
yh = 0.92229064
zc = 0.66690396
zh = 1.22952195
el = ['C', 'C', 'H', 'H', 'H', 'H']
x = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
y = [0.0, 0.0, yh, yh, -yh, -yh]
z = [zc, -zc, zh, -zh, zh, -zh]
xyz = np.asarray([x, y, z])          # shape (3, natm): rows are the x,y,z axes

# The canonical MO irrep labels (Mulliken irrep ids) of STO-3G RHF ethylene.
# This is the orientation-independent reference asserted by the upstream test.
REF = (0, 5, 0, 5, 6, 0, 3, 7, 2, 6, 0, 5, 3, 5)

def geom_for_perm(perm):
    """Re-enter the SAME molecule with its three Cartesian axes permuted."""
    carts = xyz[perm, :].T.tolist()
    return '\n'.join('{:s} {} {} {}'.format(e, *c) for e, c in zip(el, carts))

def orbsym_for_perm(perm):
    mol = gto.M(atom=geom_for_perm(perm), basis='sto-3g', verbose=0, symmetry=True)
    mf = scf.RHF(mol).run()
    return mol.groupname, tuple(int(s) for s in mf.mo_coeff.orbsym)

# The six axis permutations -- all describe the identical physical molecule.
perms = [(0, 1, 2), (0, 2, 1), (2, 0, 1), (1, 0, 2), (1, 2, 0), (2, 1, 0)]
names = ['xyz', 'xzy', 'zxy', 'yxz', 'yzx', 'zyx']

results = []
for name, perm in zip(names, perms):
    grp, orbsym = orbsym_for_perm(perm)
    held = (orbsym == REF)
    results.append((name, grp, orbsym, held))
    print(f"  perm {name}: group={grp:4s}  match_ref={held!s:5s}  "
          f"{'HELD' if held else 'FIRED'}")
    if not held:
        print(f"      orbsym = {orbsym}")
        print(f"      ref    = {REF}")

n_held = sum(1 for *_, h in results if h)
n = len(results)
# The MR also requires all orientations to agree WITH EACH OTHER (invariance),
# which the reference comparison subsumes.
distinct = {orbsym for _, _, orbsym, _ in results}

print("-" * 64)
print(f"orientations matching the canonical reference: {n_held}/{n}")
print(f"number of DISTINCT orbsym tuples across orientations: {len(distinct)} "
      f"(point-group invariance requires exactly 1)")

fired = (n_held != n) or (len(distinct) != 1)
print("VERDICT:", "FIRED (irrep labels depend on input orientation)"
      if fired else
      "HELD (irrep labels orientation-invariant and correct)")
