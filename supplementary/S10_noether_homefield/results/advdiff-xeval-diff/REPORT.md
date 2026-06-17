# NOETHER home-field detection -- advdiff-xeval-diff

**Equation**: u_t + c.grad(u) = alpha*lap(u) (2-D advection-diffusion, periodic; N=64, alpha=0.01, c=(1.0,0.5), T=0.5)
**Domain**: thermal×fluid
**Implementations**: M-FV, M-SP
**Execution mode**: executed-here
**Provenance**: substrate: Minimum-MR-SubSet mcmr.pde_xeval (solvers, mutations); differential oracle executed here; no selection.
**Tolerance calibration (§10.2)**: tau=0.924844 = 5.0x pristine gap delta=0.184969 (n_probes=5)
**Alignment gate (baseline_control all survive)**: PASS

## Generation / detection (no selection / k* reported)

| Metric | Value |
|---|---|
| M-yield (MRs derived) | 1 |
| M-block (NOETHER blocks covered) | 1 (E*) |
| M-detect (real mutants killed) | 12/29 = 0.414 |
| Wilson 95% CI | [0.255, 0.593] |
| Underpowered (n<10) | False |
| GenMorph feasible | False |

## Per-block detection

| Block | MRs | detected/n | rate | Wilson95 |
|---|---|---|---|---|
| E* | xeval-differential | 12/29 | 0.414 | [0.255, 0.593] |

## Per-fault-class detection

| fault_class | detected/n | rate |
|---|---|---|
| advection_speed_error | 2/3 | 0.667 |
| advection_stencil_fault | 2/4 | 0.500 |
| boundary_index_fault | 0/2 | 0.000 |
| coefficient_inhomogeneity_fault | 0/2 | 0.000 |
| conservation_violation | 1/2 | 0.500 |
| diffusion_coefficient_error | 0/2 | 0.000 |
| laplacian_stencil_fault | 1/4 | 0.250 |
| sign_error | 1/1 | 1.000 |
| spectral_aliasing_fault | 0/1 | 0.000 |
| spectral_normalization_fault | 0/1 | 0.000 |
| spectral_wavenumber_fault | 3/3 | 1.000 |
| time_integration_fault | 2/4 | 0.500 |

## Per-MR kill counts (real mutants)

| MR | block | kills |
|---|---|---|
| xeval-differential | E* | 12 |

## GenMorph feasibility (M-feasible)

- feasible: False
- reason: N x N field comparison across two PDE solves per case (D1-D2); neutral cross-impl oracle, not a single-program GP target.
- expressibility tier: method-comparison oracle (E*), beyond (jir,jor) tier (D4)
