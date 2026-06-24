# Negative result: DeepXDE Trev* (time-reversibility) is genuinely scarce

> Honest scarcity confirmation for the NOETHER **Trev\*** block in the
> `pde_sciml` (DeepXDE) domain. Same status as the PySCF, OpenMC, and scipy
> Trev\* negative results (no fire-able reversible-propagator bug).

## Claim

There is **no** in-the-wild, fixed DeepXDE bug that violates a *time-reversibility*
(forward -> reverse -> return-to-initial / reversible-propagator) invariant, because
**DeepXDE has no time-stepping integrator at all**: it is a physics-informed neural
network (PINN) library that solves PDEs by minimizing a residual loss over the whole
space-time domain, treating time `t` as just another collocation coordinate. There is
no forward propagator to integrate, hence no forward -> reverse -> initial invariant to
violate.

## Evidence (git archaeology on /tmp/deepxde_trev, full history, HEAD v1.15.0-6-gb8d69c4, 1261 commits)

Method note: `git log` rejects the combined `-iE` flag; flags separated as `-i -E`
(verified working: `--grep='fix'` -> 152, `--grep='bug'` -> 61).

| Search | Command | Result |
|---|---|---|
| time-reversal / reversibility | `git log --all -i -E --grep='time.?revers\|reversib'` | 0 / 0 commits |
| unitarity / norm conservation | `git log --all -i -E --grep='unitar\|norm.?conserv'` | 0 / 0 commits |
| Magnus / symplectic / leapfrog / Verlet | `git log --all -i -E --grep='magnus\|symplect\|leapfrog\|verlet'` | 0 / 0 / 0 / 0 commits |
| propagator / time-stepping / time-marching | `git log --all -i -E --grep='propagat\|time.?step\|time.?march'` | 0 / 0 / 0 commits |
| Hamiltonian / conservation | `git log --all -i -E --grep='hamiltonian\|conserv'` | 0 / 0 commits |
| integrator | `git log --all -i -E --grep='integrat'` | 1 (0b518c6 "Update build test and integration testing suite", CI tooling, not a physics integrator) |
| source: any time-stepping integrator | `grep -rliE 'leapfrog\|verlet\|symplectic\|time.?march\|odeint\|runge.?kutta\|\brk4\b' deepxde/` | 0 files |

## Candidates inspected and rejected (real SHAs)

| Full SHA | Date | Subject | Why rejected |
|---|---|---|---|
| `0b518c6354e4b1aaec8c1ed386d3a80d75c195e7` | 2023-09-18 | Update build test and integration testing suite (#1324) | Sole `integrat` grep hit; it is CI/build *integration testing* infrastructure, not a numerical time-integrator. |
| `examples/pinn_forward/wave_1d.py` (in-tree) | -- | wave-equation PINN (`utt = c^2 uxx`, the canonical time-reversal-symmetric PDE) | The wave example exists but is a **residual-loss PINN**: its `pde(x, y)` returns `hessian(y,x,i=1,j=1) - C**2*hessian(y,x,i=0,j=0)` minimized globally over `GeometryXTime`. Time index `i=1` is a coordinate axis identical to space index `i=0`. There is no propagator, no time-stepping, hence nothing whose reversibility could break. |
| `22e613d`, `07f15b0`, `8a644fe`, `b49874f`, `3fe523a`, `1180c3c`, `13974c7` (the 7 `fix.*bug` commits) | various | float16/float64 dtype fixes, tuple-input predict, MIONet, paddle examples | None touches a time-integrator or a reversibility invariant; they are dtype/backend/IO fixes. |

## Why it is structurally absent (not just "we didn't find it")

1. **DeepXDE has no time-stepping integrator.** A repo-wide source grep for every standard
   reversible/explicit integrator name (`leapfrog`, `verlet`, `symplectic`, `time-march`,
   `odeint`, `runge-kutta`, `rk4`) returns **0 files**. The only `def *step` symbols in the
   source are `train_step` / `train_step_lbfgs` / `train_step_nncg` (optimizer training steps
   in `deepxde/model.py` and `deepxde/zcs/model.py`), `nncg.step` (a line-search step in the
   NysNewtonCG optimizer), and `_check_dynamic_stepsize` (fractional-derivative quadrature in
   `data/fpde.py`). None is a physics time-propagator.

2. **Time-dependent PDEs are solved as a global residual minimization, not by propagation.**
   `deepxde.data.TimePDE(geometryxtime, pde, ic_bcs, ...)` extends `PDE` and samples
   collocation points over the *whole* spatio-temporal domain `GeometryXTime = geom x
   TimeDomain`; the network is trained to drive the PDE residual (plus IC/BC penalties) to
   zero everywhere at once. There is no initial state advanced forward in time, so the
   forward -> reverse -> initial construction has no operational meaning here.

3. **The reversible-operator structure that DeepXDE *does* expose is the autodiff Hessian,
   and that is already captured by the T\* (self-adjoint / operator-symmetry) block, not
   Trev\*.** The Hessian-symmetry (`H[i,j] == H[j,i]`, mixed-partial / Schwarz) operator
   invariant -- and a forward-mode-AD indexing bug that breaks it -- is recorded separately in
   `bug_deepxde_forward_hessian_symmetry.json` (fix 46e2c2e8..., #1591). That is *operator*
   self-adjointness (T\*), a spatial-differential-operator symmetry, **not** the *time*-reversal
   propagation invariant Trev\* requires.

## Conclusion

Trev\* is **genuinely scarce in DeepXDE (`pde_sciml` paper SUT domain)**, for the most basic
structural reason of the four Trev\* negatives: the library contains **no reversible
propagator and no time-stepping integrator** to begin with -- time is a collocation
coordinate in a residual-loss optimization. This mirrors the OpenMC negative (no
reversible-dynamics substrate) and the scipy negative (no symplectic/leapfrog integrator),
and is recorded as an honest negative result per CLAUDE.md "诚实优先于救援".
DeepXDE's contributions to the NOETHER matrix remain its boundary/IC bugs
(`bug_deepxde_neumann.json`, `bug_deepxde_periodic.json`, `bug_deepxde_boundary_float32.json`),
the resample bug (`bug_deepxde_resample.json`), and the forward-mode Hessian self-adjointness
(T\*) bug (`bug_deepxde_forward_hessian_symmetry.json`).
