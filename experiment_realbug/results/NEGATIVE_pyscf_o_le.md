# Negative result: PySCF O≤ (occupation / density / variational bound) is genuinely scarce

> Honest scarcity confirmation for the NOETHER **O≤** block (monotonicity /
> positivity / order-preservation / variational bound) in the
> `quantum_chemistry` (PySCF) domain. Same structural status as the
> Fock-Hermitian **T\*** constructive-guarantee case noted in
> `bug_pyscf_smearing.json` and the scipy/OpenMC Trev\* negatives.

## Claim

There is **no** in-the-wild, *fixed* PySCF bug whose maintainer patch enforces an
**O≤** invariant (MO/natural-orbital occupation bounds `0 ≤ n_i ≤ 2` (RHF) /
`≤ 1` per spin; electron density `ρ(r) ≥ 0`; 1-RDM positive-semidefinite;
variational bound `E[Ψ] ≥ E_0`; correlation-energy sign monotonicity), because in
PySCF **these quantities are bounded by construction**, so there is no numeric
clamp / positivity-guard fix to reproduce as pre(FIRED)→post(HELD).

This is distinct from the two PySCF positives that **are** in the matrix:
- `bug_pyscf_smearing.json` — electron-number **conservation** (Noether N block),
  `sum(mo_occ) == nelec`, fix `ebf4e676` (gh-2290). A *conservation* bug, not O≤.
- `bug_pyscf_diis.json` — DIIS self-consistency / **convergence** (L\* block),
  fix `15920e60` (gh-1524/#1638). A *convergence* bug, not O≤.

## Evidence (git archaeology on /tmp/pyscf_git, full history)

HEAD `47b37cba1d229c1215d66a7197bd06ec26180f19`, `git describe = v2.13.1-19-g47b37cba`.

### Keyword hit counts (`git log --all -i -E --grep=...`)

| grep pattern | commits | verdict after inspection |
|---|---:|---|
| `negative occupation` | 0 | — |
| `occ.*negative` | 0 | — |
| `clip` | 0 | — |
| `np.maximum` | 0 | — |
| `abs(occ)` | 0 | — |
| `natural orbital occ` | 0 | — |
| `density.*negative` | 0 | — |
| `positive semidefinite` | 0 | — |
| `nelec.*negative` | 0 | — |
| `occupation number` | 2 | neither is an occ-bound clamp (see below) |
| `clamp` | 1 | C-side shell-**index** clobber, not occupancy |
| `variational` | 2 | both DMRG-NEVPT config-file overwrite bugs |
| `fractional occ` | 5 | shape / slot-indexing / feature, no negativity |

Reproduce the tally:
```bash
cd /tmp/pyscf_git
for kw in 'negative occupation' 'occupation number' 'occ.*negative' 'clamp' 'clip' \
          'np.maximum' 'abs(occ)' 'natural orbital occ' 'density.*negative' \
          'positive semidefinite' 'variational' 'nelec.*negative' 'fractional occ'; do
  printf "%-22s -> %s\n" "$kw" "$(git log --all -i -E --grep="$kw" --oneline | wc -l)"
done
```

### Source-grep: post-HF code has *no* negative-occupation / NOON-positivity guard
```bash
grep -rn -E 'negative|< 0|maximum\(0|clip\(' \
  pyscf/mp/ pyscf/ci/ pyscf/cc/ pyscf/mcscf/addons.py | grep -iE 'occ|noon|natur|rdm|eig'
# -> 0 hits
grep -rn -E 'noons|natocc' pyscf/ --include=*.py | grep -iE 'neg|< 0|abs|warn|clip|maximum'
# -> 0 hits
```
`make_natural_orbitals` (`pyscf/mcscf/addons.py`) returns `noons = flip(eigh(A,b=S)[0])`
with **no** clamp — confirming occupations are taken as-is from a Hermitian
generalised eigenproblem, not corrected post hoc.

## Candidates inspected and rejected (each is NOT an O≤ bound-violation fix)

| commit | title | why not O≤ |
|---|---|---|
| `a140208c` (v1.4.0→v1.4.1) | Fix entropy of Gaussian smearing | RHF occ `1-erf` (pre) is **algebraically identical** to `2·(0.5-0.5·erf)` (post); both ∈ [0,2], bit-identical occupations (verified numerically). Only the **entropy** term changed. An entropy/free-energy fix, NOT an occupation-bound fix. |
| `ebf4e676` (gh-2290) | Fix addons.smearing RHF electron number | `sum(mo_occ)` off-by-one — a **conservation** (N-block) bug, already the `bug_pyscf_smearing.json` positive. Occupations stayed in [0,2]. |
| `23fc4566`/`65cff4da` (#823/#824) | Fix fractional occupations, zero beta electrons | `nocc=0` → `mo_energy[sorted_idx[nocc]]` index-out-of-range **crash**; the patch guards the empty case. No occupation goes out of bound. |
| `a40f48d3` (#3025) | validate occupancy assignment | Adds `if nocc > nmo: raise RuntimeError` (basis too small) — a **crash-type** guard, raises rather than clamping any out-of-bound number. |
| `c36be01d` | Added a check for fractional occupation numbers | `kmp2.get_nocc` **raises** when a smeared (fractional) `mo_occ` reaches MP2; a guard against mixing smearing with MP2, not a negativity/bound correction. |
| `231492b9` | Fix average occupancy problem in frac_occ | Fixes which **slots** receive the fractional value (`[nsocc:ndocc]`→`[ndocc:nsocc+ndocc]`); the `frac` value is unchanged and stays bounded. Indexing fix. |
| `281a7202` | fci addons handle negative particle numbers | Creation/destruction-operator empty-shape handling (`des_a/cre_a` return zeros); CI-vector shape edge case, not occupation/density positivity. |
| `9fc6f993` (#3214) | batch C-side correctness bugs ("clamp") | `nr_direct.c` clobbered (k,l) **shell indices** (out-of-range array access); unrelated to physical occupation/density bounds. |

## Why it is structurally absent (not just "we didn't find it")

1. **Integer aufbau occupation**: the default `get_occ` sets
   `mo_occ = (mo_e <= fermi) * 2` (RHF) / `* 1` (per spin). Occupations are
   literally `0` or `2` (`0`/`1`) by construction — they cannot be negative or
   exceed the bound.
2. **Smearing occupation is algebraically bounded**: Fermi-Dirac
   `1/(exp((e-μ)/σ)+1) ∈ (0,1)`; Gaussian `0.5·erfc((e-μ)/σ) ∈ (0,1)` (and the
   historical `1-erf` form is the same function after the per-spin/RHF factor).
   `erfc` and the logistic are monotone maps into `[0,1]` — out-of-bound
   occupation is unreachable for any finite `μ, σ`.
3. **Natural-orbital occupations come from a Hermitian eigenproblem**:
   `make_natural_orbitals` diagonalises `S·D·S` (generalised, `b=S`) via
   `scipy.linalg.eigh`. For a *variational* RDM (HF/CASSCF/FCI) `D` is PSD by
   construction, so NOONs are ≥ 0 automatically; PySCF ships no clamp because none
   is needed.
4. **Perturbative RDMs (MP2/CC) can have out-of-[0,2] NOONs by physics**, but this
   is a *known property of the method*, not a software defect — there is no
   upstream commit treating it as a bug to fix, hence no pre→post pair to
   reproduce (the matrix requires a maintainer fix, not a physics caveat).
5. **Variational bound `E ≥ E_0`** is guaranteed by the Rayleigh quotient for any
   diagonalisation-based solver; PySCF has no "variational-collapse" fix in its
   history (`variational` grep = 0 relevant hits).

## Conclusion

O≤ is **genuinely scarce in PySCF**, for the same structural reason it is scarce
elsewhere: the invariant is *constructively guaranteed* (clamped occupations,
monotone bounded smearing maps, PSD-by-construction variational RDMs), so there is
no in-the-wild numeric clamp/positivity fix to reproduce as FIRED→HELD. Recorded as
an honest negative result per CLAUDE.md "诚实优先于救援", consistent with the
Fock-Hermitian T\* constructive-guarantee note in `bug_pyscf_smearing.json` and the
scipy/OpenMC Trev\* scarcity negatives. PySCF's two clean positives remain N-block
(smearing conservation) and L\*-block (DIIS convergence).
