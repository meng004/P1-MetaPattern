# NOETHER home-field detection -- combustion-gri30

**Equation**: adiabatic const-UV 0-D reactor, GRI-Mech 3.0 (53 sp.)
**Domain**: thermal
**Implementations**: M-CANTERA, M-PYODE
**Execution mode**: reused-committed-matrix
**Provenance**: T2 committed detection matrix: runs/abd-witness-combustion-gri30-B-20260616T075927Z/kill_matrix.csv (detection-only reuse; selection artefacts not read).
**Alignment gate (baseline_control all survive)**: PASS

## Generation / detection (no selection / k* reported)

| Metric | Value |
|---|---|
| M-yield (MRs derived) | 16 |
| M-block (NOETHER blocks covered) | 2 (Conservation, O_le) |
| M-detect (real mutants killed) | 34/54 = 0.630 |
| Wilson 95% CI | [0.496, 0.746] |
| Underpowered (n<10) | False |
| GenMorph feasible | False |

## Per-block detection

| Block | MRs | detected/n | rate | Wilson95 |
|---|---|---|---|---|
| Conservation | ct-element_conservation_C, ct-element_conservation_H, ct-element_conservation_N, ct-element_conservation_O, ct-energy_conservation, ct-equilibrium_consistency, ct-mass_conservation, ode-element_conservation_C, ode-element_conservation_H, ode-element_conservation_N, ode-element_conservation_O, ode-energy_conservation, ode-equilibrium_consistency, ode-mass_conservation | 34/54 | 0.630 | [0.496, 0.746] |
| O_le | ct-positivity, ode-positivity | 4/54 | 0.074 | [0.029, 0.175] |

## Per-fault-class detection

| fault_class | detected/n | rate |
|---|---|---|
| missing_reaction_fault | 0/4 | 0.000 |
| rate_constant_fault | 0/12 | 0.000 |
| stoichiometry_fault | 28/28 | 1.000 |
| thermo_fault | 6/6 | 1.000 |
| thirdbody_fault | 0/4 | 0.000 |

## Per-MR kill counts (real mutants)

| MR | block | kills |
|---|---|---|
| ct-element_conservation_C | Conservation | 6 |
| ct-element_conservation_H | Conservation | 6 |
| ct-element_conservation_O | Conservation | 6 |
| ct-element_conservation_N | Conservation | 4 |
| ct-mass_conservation | Conservation | 14 |
| ct-energy_conservation | Conservation | 17 |
| ct-equilibrium_consistency | Conservation | 9 |
| ct-positivity | O_le | 0 |
| ode-element_conservation_C | Conservation | 6 |
| ode-element_conservation_H | Conservation | 6 |
| ode-element_conservation_O | Conservation | 6 |
| ode-element_conservation_N | Conservation | 4 |
| ode-mass_conservation | Conservation | 14 |
| ode-energy_conservation | Conservation | 0 |
| ode-equilibrium_consistency | Conservation | 12 |
| ode-positivity | O_le | 4 |

## GenMorph feasibility (M-feasible)

- feasible: False
- reason: field / trajectory / eigenvalue I/O; per-eval is a full PDE / kinetics / transport solve; structural MRs relate multiple executions (D1–D3).
- expressibility tier: beyond two-execution (jir,jor) tier (D4)
