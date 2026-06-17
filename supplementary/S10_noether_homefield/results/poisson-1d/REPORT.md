# NOETHER home-field detection -- poisson-1d

**Equation**: -u'' = f (1-D Poisson / steady heat, Dirichlet), 3-point FDM
**Domain**: thermal
**Implementations**: FDM
**Execution mode**: executed-here


**Alignment gate (baseline_control all survive)**: PASS

## Generation / detection (no selection / k* reported)

| Metric | Value |
|---|---|
| M-yield (MRs derived) | 5 |
| M-block (NOETHER blocks covered) | 3 (G, L*, O_le) |
| M-detect (real mutants killed) | 5/6 = 0.833 |
| Wilson 95% CI | [0.436, 0.970] |
| Underpowered (n<10) | True |
| GenMorph feasible | False |

## Per-block detection

| Block | MRs | detected/n | rate | Wilson95 |
|---|---|---|---|---|
| G | rho_reflect | 2/6 | 0.333 | [0.097, 0.700] |
| L* | rho_grid_convergence | 0/6 | 0.000 | [0.000, 0.390] |
| O_le | rho_linearity, rho_positivity, rho_superpose | 3/6 | 0.500 | [0.188, 0.812] |

## Per-fault-class detection

| fault_class | detected/n | rate |
|---|---|---|
| coeff_inhomogeneity | 1/1 | 1.000 |
| coefficient_error | 0/1 | 0.000 |
| consistency_fault | 1/1 | 1.000 |
| rhs_affine_fault | 1/1 | 1.000 |
| sign_error | 1/1 | 1.000 |
| stencil_asymmetry | 1/1 | 1.000 |

## Per-MR kill counts (real mutants)

| MR | block | kills |
|---|---|---|
| rho_linearity | O_le | 1 |
| rho_superpose | O_le | 1 |
| rho_reflect | G | 2 |
| rho_positivity | O_le | 2 |
| rho_grid_convergence | L* | 0 |

## GenMorph feasibility (M-feasible)

- feasible: False
- reason: field-valued u(x) I/O (D1); grid-convergence MR relates multiple structured executions across grids (D3).
- expressibility tier: single-exec invariants + multi-grid relations -- beyond two-execution (jir,jor) tier (D4)
