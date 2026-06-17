# NOETHER home-field detection -- heat-1d

**Equation**: u_t = alpha*u_xx (1-D heat conduction, Dirichlet), explicit FDM
**Domain**: thermal
**Implementations**: FDM
**Execution mode**: executed-here


**Alignment gate (baseline_control all survive)**: PASS

## Generation / detection (no selection / k* reported)

| Metric | Value |
|---|---|
| M-yield (MRs derived) | 6 |
| M-block (NOETHER blocks covered) | 3 (G, L*, O_le) |
| M-detect (real mutants killed) | 5/6 = 0.833 |
| Wilson 95% CI | [0.436, 0.970] |
| Underpowered (n<10) | True |
| GenMorph feasible | False |

## Per-block detection

| Block | MRs | detected/n | rate | Wilson95 |
|---|---|---|---|---|
| G | rho_reflect | 2/6 | 0.333 | [0.097, 0.700] |
| L* | rho_energy_decay, rho_steady_limit | 3/6 | 0.500 | [0.188, 0.812] |
| O_le | rho_linearity, rho_maxprinciple, rho_superpose | 4/6 | 0.667 | [0.300, 0.903] |

## Per-fault-class detection

| fault_class | detected/n | rate |
|---|---|---|
| boundary_source_fault | 1/1 | 1.000 |
| coeff_inhomogeneity | 1/1 | 1.000 |
| diffusion_coeff_error | 0/1 | 0.000 |
| sign_error | 1/1 | 1.000 |
| stencil_asymmetry | 1/1 | 1.000 |
| time_integration_fault | 1/1 | 1.000 |

## Per-MR kill counts (real mutants)

| MR | block | kills |
|---|---|---|
| rho_linearity | O_le | 3 |
| rho_superpose | O_le | 3 |
| rho_reflect | G | 2 |
| rho_maxprinciple | O_le | 3 |
| rho_energy_decay | L* | 3 |
| rho_steady_limit | L* | 3 |

## GenMorph feasibility (M-feasible)

- feasible: False
- reason: array-valued field I/O u(x); GP assertion grammar targets scalar/tuple I/O (D1). Conservation/scaling/reflection MRs relate multiple structured executions (D3).
- expressibility tier: single-exec invariants + multi-exec structured relations (beyond GenMorph's two-execution (jir,jor) tier, D4)
