# NOETHER home-field detection -- wave-1d

**Equation**: u_tt = c^2 u_xx (1-D wave, fixed ends), leapfrog FDM
**Domain**: fluid
**Implementations**: FDM
**Execution mode**: executed-here


**Alignment gate (baseline_control all survive)**: PASS

## Generation / detection (no selection / k* reported)

| Metric | Value |
|---|---|
| M-yield (MRs derived) | 5 |
| M-block (NOETHER blocks covered) | 4 (Conservation, G, O_le, T_rev*) |
| M-detect (real mutants killed) | 6/6 = 1.000 |
| Wilson 95% CI | [0.610, 1.000] |
| Underpowered (n<10) | True |
| GenMorph feasible | False |

## Per-block detection

| Block | MRs | detected/n | rate | Wilson95 |
|---|---|---|---|---|
| Conservation | rho_energy_conserve | 6/6 | 1.000 | [0.610, 1.000] |
| G | rho_reflect | 4/6 | 0.667 | [0.300, 0.903] |
| O_le | rho_linearity, rho_superpose | 2/6 | 0.333 | [0.097, 0.700] |
| T_rev* | rho_time_reversal | 3/6 | 0.500 | [0.188, 0.812] |

## Per-fault-class detection

| fault_class | detected/n | rate |
|---|---|---|
| advective_contamination | 1/1 | 1.000 |
| coeff_inhomogeneity | 1/1 | 1.000 |
| dissipation_fault | 1/1 | 1.000 |
| stencil_asymmetry | 1/1 | 1.000 |
| time_integration_fault | 1/1 | 1.000 |
| wave_speed_error | 1/1 | 1.000 |

## Per-MR kill counts (real mutants)

| MR | block | kills |
|---|---|---|
| rho_linearity | O_le | 2 |
| rho_superpose | O_le | 2 |
| rho_reflect | G | 4 |
| rho_energy_conserve | Conservation | 6 |
| rho_time_reversal | T_rev* | 3 |

## GenMorph feasibility (M-feasible)

- feasible: False
- reason: field-valued u(x,t) I/O (D1); energy-conservation and time-reversal MRs relate multiple structured executions (D3).
- expressibility tier: incl. time-reversal (multi-exec) -- beyond two-execution (jir,jor) tier (D4)
