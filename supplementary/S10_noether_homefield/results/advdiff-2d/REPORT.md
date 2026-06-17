# NOETHER home-field detection -- advdiff-2d

**Equation**: u_t + c.grad(u) = alpha*lap(u) (2-D advection-diffusion, periodic; N=64, alpha=0.01, c=(1.0,0.5), T=0.5)
**Implementations**: M-FV, M-SP
**Alignment gate (baseline_control all survive)**: PASS

## Generation / detection (no selection / k* reported)

| Metric | Value |
|---|---|
| M-yield (MRs derived) | 11 |
| M-block (NOETHER blocks covered) | 4 (Conservation, G, L*, O_le) |
| M-detect (real mutants killed) | 13/29 = 0.448 |
| Wilson 95% CI | [0.284, 0.625] |
| Underpowered (n<10) | False |
| GenMorph feasible | False |

## Per-block detection

| Block | MRs | detected/n | rate | Wilson95 |
|---|---|---|---|---|
| Conservation | mass-conservation | 10/29 | 0.345 | [0.199, 0.526] |
| G | galilean-inv, phase-scaling, reflection-sym, spectral-decay-scaling, translation-inv | 11/29 | 0.379 | [0.227, 0.560] |
| L* | energy-decay, richardson-self | 10/29 | 0.345 | [0.199, 0.526] |
| O_le | linearity-scale, max-principle, superposition | 8/29 | 0.276 | [0.147, 0.457] |

## Per-fault-class detection

| fault_class | detected/n | rate |
|---|---|---|
| advection_speed_error | 0/3 | 0.000 |
| advection_stencil_fault | 1/4 | 0.250 |
| boundary_index_fault | 2/2 | 1.000 |
| coefficient_inhomogeneity_fault | 2/2 | 1.000 |
| conservation_violation | 2/2 | 1.000 |
| diffusion_coefficient_error | 0/2 | 0.000 |
| laplacian_stencil_fault | 1/4 | 0.250 |
| sign_error | 1/1 | 1.000 |
| spectral_aliasing_fault | 0/1 | 0.000 |
| spectral_normalization_fault | 1/1 | 1.000 |
| spectral_wavenumber_fault | 1/3 | 0.333 |
| time_integration_fault | 2/4 | 0.500 |

## Per-MR kill counts (real mutants)

| MR | block | kills |
|---|---|---|
| linearity-scale | O_le | 5 |
| superposition | O_le | 5 |
| translation-inv | G | 7 |
| reflection-sym | G | 9 |
| mass-conservation | Conservation | 10 |
| energy-decay | L* | 8 |
| max-principle | O_le | 8 |
| spectral-decay-scaling | G | 4 |
| phase-scaling | G | 2 |
| galilean-inv | G | 9 |
| richardson-self | L* | 7 |

## GenMorph feasibility (M-feasible)

- feasible: False
- reason: N x N field I/O (D1); each fitness eval is a sparse-LU / spectral PDE solve (D2); scaling/Galilean/Richardson MRs relate multiple structured executions (D3).
- expressibility tier: beyond two-execution (jir,jor) tier (D4)
