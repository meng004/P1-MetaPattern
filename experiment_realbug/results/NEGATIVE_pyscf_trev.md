# Negative result: PySCF Trev* (time-reversibility) is genuinely scarce

> Honest scarcity confirmation for the NOETHER **Trev\*** block in the
> `quantum_chemistry` (PySCF) domain. Same status as the previously-recorded
> OpenMC and scipy Trev\* negative results (no fire-able reversible-propagator bug).

## Claim

There is **no** in-the-wild, fixed PySCF bug that violates a *time-reversibility*
(forward -> reverse-momenta -> return-to-initial / unitary-propagator / norm-conservation)
invariant, because the **genuine reversible-propagator candidate (real-time TDDFT /
rt-TDSCF) was removed from the main `pyscf/pyscf` repo at v2.0.0** (it now lives in a
separate extended-projects repo), and the **only reversible-dynamics substrate that
remains in the main paper-SUT repo (velocity-Verlet BOMD) is time-reversible by
construction** -- it has no maintainer fix to a reversibility/sign/momentum defect.

## Evidence (git archaeology on /tmp/pyscf_trev, full history, HEAD v2.13.1-19-g47b37cba, 9815 commits)

Method note: `git log` rejects the combined `-iE` flag (`fatal: unrecognized argument`);
flags must be separated as `-i -E`. All counts below use the corrected form.

| Search | Command | Result |
|---|---|---|
| time-reversal / reversibility | `git log --all -i -E --grep='time.?revers\|reversib'` | 1 / 0 (the 1 = 9fe5b824 "Canonical orthogonalization for eigenvalue solver", unrelated) |
| unitarity / norm conservation | `git log --all -i -E --grep='unitar\|norm.?conserv'` | 0 / 0 |
| Magnus / predictor-corrector / MMUT propagator | `git log --all -i -E --grep='magnus\|predictor.?correct\|mmut'` | 0 / 0 / 2 (the 2 mmut = velocity-gauge integrals 13521569 + MPI FP-noncommut 54aed83e, neither a propagator-reversibility fix) |
| symplectic / leapfrog / verlet | `git log --all -i -E --grep='symplect\|leapfrog\|verlet'` | 0 / 0 / 1 (the 1 = `test_velocverlet.py` test file, not a fix) |
| rt-TDDFT / real-time | `git log --all -i -E --grep='rt.?tddft\|real.?time'` | 2 / 1 (all three are 2017 implementation commits c5f35c7f / 3dd50ffb / b5bcf72b, see rejected table) |
| md/ integrator reversibility fix | `git log --all -i -E --grep='revers\|symmetr\|verlet\|momentum\|wrong\|incorrect\|sign error\|backward' -- 'pyscf/md/'` | 1 (e03cd070 "BOMD Cleanup and Maxwell-Boltzmann Velocity Distribution", not a reversibility fix) |
| Verlet equations ever edited after stabilizing | `git log --all -L ':_next_velocity:pyscf/md/integrators.py'` | empty (the velocity-Verlet equations of motion were never patched post-implementation) |

## Candidates inspected and rejected (real SHAs)

| Full SHA | Date | First tag | Subject | Why rejected |
|---|---|---|---|---|
| `c5f35c7fe1c238d2fb47b76a9c349b6071ba69ee` | 2017-06-22 | v1.4-alpha | RTTDDFT code (#94) | **Initial** RT-TDDFT (MMUT) implementation, not a fix to an existing propagator's reversibility. Module later removed (see 137c23d3). |
| `3dd50ffb997b7efe7dec9845e4a0ded4e1edec61` | 2017-07-25 | v1.4-beta | Dev (#98) | Wholesale rewrite/refactor of the same MMUT class (all `+`/`-` lines redefine `TransMat`/`split_rk4_step_mmut` from scratch); not a reversibility bug fix. |
| `b5bcf72bfde9a2fb113f81795429986bec6a8864` | 2017-08-24 | v1.4.0 | Fixes; rename to rt (Realtime Tdscf) (#116) | Rename `tdscf` -> `rt` + import/restructure; the propagator equations are re-added unchanged, no reversibility/unitarity correction. |
| `137c23d3757fb096b51ccd7e6eb635a343deaa4b` | 2021-03-07 | **v2.0.0** | Put some modules in github/pyscf extended projects | **Removes the entire `pyscf/rt` module** from the main repo (listed under "Modules removed: ... rt ..."). Confirmed: `git ls-tree v1.7.6 -- pyscf/rt` = 1 dir present; `git ls-tree v2.0.0 -- pyscf/rt` = 0 (absent). So the only unitary time-propagator is GONE from the paper SUT repo from v2.0.0 onward. |
| `f596660cafab485232127adbc56e009e864cdd6e` | 2022-04-21 | v2.1.0 | updated the algorithm, need to check if it works though | Early BOMD development; the diff is the *initial* velocity-Verlet equations (`r + dt*v + dt^2*F/2m`, `v + dt*(Fn1+Fn2)/2m`), which are time-reversible by construction. Not a fix to a broken-then-restored reversibility. |
| `e03cd0705920adce37979263472c15640a0e1a78` | 2023-03-02 | v2.2.0 | BOMD Cleanup and Maxwell-Boltzmann Velocity Distribution (#1308) | Touches thermostat / initial-velocity sampling and cleanup, not the conservative Verlet step's reversibility. (Only md/ commit matching the broad keyword set, hence inspected.) |
| `9fe5b824926b6d7458bb237eaed971195a6c6df6` | 2026-04-20 | v2.13.0 | Canonical orthogonalization for eigenvalue solver in SCF (#3191) | Sole `time.?revers` grep hit; it is linear-algebra orthogonalization for the SCF eigensolver, with no relation to time-reversal dynamics. |

## Why it is structurally absent (not just "we didn't find it")

1. **Linear-response TDDFT (`pyscf.tdscf`, 38 commits) has no propagator.** It solves the
   Casida eigenvalue problem for excitation energies (the `tdscf` history is dominated by
   "TDDFT eigenvalue solver", "TDDFT initial guess", "tdscf hdiag", "diagonalization
   program"). An eigenvalue solve is **not** a time-stepping reversible integrator, so
   there is no forward -> reverse -> initial invariant to violate.

2. **Real-time TDDFT (`pyscf.rt`, the genuine MMUT/unitary candidate) was removed from the
   main repo at v2.0.0** (137c23d3, 2021-03-07) and relocated to a separate extended-projects
   repository. During its entire life *inside the main repo* (2017-2021, 12 commits across
   the `tdscf/` and `rt/` paths via `--follow`), the propagator code received only initial
   implementation, a rewrite, a rename, an Apache header, a Python-3 compat fix, a
   static-analysis style pass, examples, and a logger-time alias -- **no commit fixed a
   time-reversibility / unitarity / norm-conservation defect** in the MMUT step. Even if such
   a fix existed in the downstream extended-projects repo, it would be **out of the paper SUT
   repo (`pyscf/pyscf`)** at every modern released version the study uses.

3. **The only reversible-dynamics substrate left in the main repo is velocity-Verlet BOMD
   (`pyscf.md.integrators.VelocityVerlet`), which is time-reversible by construction.** The
   equations of motion are the textbook symplectic form
   `r(t+dt) = r(t) + dt*v + 0.5*dt^2*a(t)` and `v(t+dt) = v(t) + 0.5*dt*(a(t)+a(t+dt))`;
   the symmetric force average makes the step exactly invertible under `dt -> -dt, v -> -v`.
   `git log -L ':_next_velocity:...'` shows these equations were **never patched** after they
   stabilized, so there is no broken-then-fixed reversibility bug. Empirically confirmed:
   propagating H2/RHF forward 20 velocity-Verlet steps, reversing momenta, and integrating
   back returns to the initial geometry/velocity to machine precision
   (`max|r_back - r0| = 6.66e-16`, `max|v_back - (-v0)| = 9.27e-18`; Trev\* MR HELD).
   Repro: `results/pyscf_repro/trev_velocity_verlet_holds.py` (pyscf 2.13.1, py3.11, CPU,
   no net). A construction-guaranteed invariant offers no triggerable defect, exactly as the
   T\* Fock-Hermiticity invariant is construction-guaranteed and scarce
   (see `bug_pyscf_smearing.json` note: "T\* Fock-Hermitian is constructively guaranteed
   (scarce)").

## Conclusion

Trev\* is **genuinely scarce in PySCF (`quantum_chemistry` paper SUT domain)**, for a
structural reason that parallels OpenMC and SciPy: the one genuine unitary time-propagator
(rt-TDDFT) is not in the main paper-SUT repo at modern versions, and the one reversible
integrator that is (velocity-Verlet BOMD) is reversible by construction with no
fire-able bug. This is recorded as an honest negative result, consistent with CLAUDE.md's
"诚实优先于救援" and the existing OpenMC (NEGATIVE_openmc_trev.md) and scipy
(COVERAGE_SUMMARY.md S3) Trev\* scarcity records. PySCF's contributions to the NOETHER
matrix remain its conservation block (`bug_pyscf_smearing.json`), DIIS (`bug_pyscf_diis.json`),
and D2h-symmetry (`bug_pyscf_d2h_symm.json`) bugs.
