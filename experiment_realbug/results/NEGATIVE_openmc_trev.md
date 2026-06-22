# Negative result: OpenMC Trev* (time-reversibility) is genuinely scarce

> Honest scarcity confirmation for the NOETHER **Trev\*** block in the
> `reactor_physics` (OpenMC) domain. Same status as the previously-recorded
> scipy Trev\* negative result (no symplectic basis).

## Claim

There is **no** in-the-wild, fixed OpenMC bug that violates a *time-reversibility*
(microscopic-reversibility / detailed-balance / reversible-integrator) invariant,
because **OpenMC has no reversible-dynamics substrate to begin with**.

## Evidence (git archaeology on a full-history openmc clone, HEAD v0.15.3-181-g09ee8308d, 16181 commits)

Method note: `git log` rejects the combined `-iE` flag (`fatal: unrecognized argument: -iE`);
flags must be separated as `-i -E`, and `grep` alternation needs `-E`. All counts below
were re-verified with the corrected forms (every search genuinely returns 0).

| Search | Command | Result |
|---|---|---|
| time-reversal / reversibility | `git log --all -i -E --grep='time.?revers\|reversib\|micro.?revers'` | 0 commits |
| detailed balance / reciprocity | `git log --all -i -E --grep='detailed.?balance\|recipro'` | 0 commits |
| symplectic / Verlet / leapfrog / Hamiltonian | `git log --all -i -E --grep='symplect\|verlet\|leapfrog\|hamiltonian\|stormer'` | 0 commits |
| reverse / backward depletion, negative timestep | `git log --all -i -E --grep='reverse.?deplet\|backward.?deplet\|negative.?timestep'` | 0 commits |
| source grep | `grep -rliE 'time.?reversal\|reciprocity\|detailed balance\|microscopic revers' src/ openmc/ docs/` | 0 files |

## Why it is structurally absent (not just "we didn't find it")

1. **Monte Carlo neutron transport** in OpenMC solves a **forward stationary**
   problem: the k-eigenvalue (criticality) equation or a fixed-source steady-state
   flux. There is no time-stepping of a reversible dynamical system, hence no
   forward -> reverse -> initial-state invariant to violate.
2. **Depletion / burnup** (`openmc.deplete`) IS time-dependent, but it integrates
   the **Bateman equations** (a strictly dissipative, forward-in-time stiff ODE
   system) via CRAM. Burnup is irreversible by physics (decay + transmutation);
   there is no reversible/symplectic integrator and no negative-timestep mode.
3. The only "adjoint" in OpenMC is the **random-ray mathematical adjoint flux**
   (phi-dagger) and the IFP adjoint-weighted kinetics -- these are the *mathematical*
   adjoint of the transport operator (self-adjointness / adjoint-forward duality),
   already captured by the **T\*** block via the existing
   `bug_openmc_ifp_adjoint.json` (IFP adjoint-weighted beta_eff, 767db7e6a/#3580).
   They are NOT *time*-reversibility.

## Conclusion

Trev\* is **genuinely scarce in OpenMC**, for the same structural reason it is
scarce in SciPy (no symplectic/leapfrog/reversible integrator). This is recorded
as an honest negative result, consistent with CLAUDE.md's "诚实优先于救援" and the
existing scipy Trev\* scarcity note in COVERAGE_SUMMARY.md S3.
