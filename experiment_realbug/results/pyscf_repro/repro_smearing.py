"""
NOETHER conservation-block reproduction: RHF Fermi-smearing electron-number conservation.

MR (metamorphic relation / invariant):
    For a converged SCF density P and overlap S, the integrated electron number
    must equal the true electron count:   trace(P @ S) == N_elec
    Equivalently for the occupation vector:  sum(mo_occ) == N_elec.

PySCF target: pyscf/scf/addons.py  (_SmearingSCF, RHF branch)
Bug (pre v2.7.0): for an ODD-electron RHF system, nocc = (nelectron + 1) // 2
rounds the half-occupied count UP, so the smearing optimizer conserves the wrong
particle number -> sum(mo_occ) overshoots N_elec by 1.

SUT: RHF + Fermi smearing on N2+ cation (13 electrons, odd), STO-3G. CPU seconds.
"""
import numpy as np
from pyscf import gto, scf
from pyscf.scf import addons
import pyscf

print("pyscf version:", pyscf.__version__)

mol = gto.Mole()
mol.atom = '''
    N   0.0  0.0  -0.55
    N   0.0  0.0   0.55'''
mol.basis = 'sto-3g'
mol.charge = +1     # N2+  -> 14 - 1 = 13 electrons (ODD)
mol.spin = 1        # RHF/ROHF spin handle; smearing uses RHF branch
mol.verbose = 0
mol.build()

N_elec = mol.nelectron
print("N_elec (true):", N_elec, "(odd ->triggers bug)")

mf = scf.RHF(mol)
mf = addons.smearing(mf, sigma=1e-3, method='fermi')
mf.conv_tol = 1e-10
mf.max_cycle = 200
e = mf.kernel()

S = mol.intor_symmetric('int1e_ovlp')
P = np.asarray(mf.make_rdm1())
if P.ndim == 3:          # ROHF/UHF return (2, nao, nao); total density = alpha+beta
    P = P[0] + P[1]
trace_PS = np.einsum('ij,ji->', P, S)
sum_occ = mf.mo_occ.sum()

print(f"E_tot                 = {e:.10f}")
print(f"sum(mo_occ)           = {sum_occ:.10f}")
print(f"trace(P @ S)          = {trace_PS:.10f}")
print(f"N_elec (target)       = {N_elec}")
print(f"|sum(mo_occ) - N_elec|= {abs(sum_occ - N_elec):.3e}")
print(f"|trace(PS)  - N_elec| = {abs(trace_PS - N_elec):.3e}")

tol = 1e-4
ok = abs(trace_PS - N_elec) < tol and abs(sum_occ - N_elec) < tol
print("VERDICT:", "HELD (electron number conserved)" if ok else "FIRED (electron number NOT conserved)")
