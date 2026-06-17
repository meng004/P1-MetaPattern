# NOETHER home-field detection -- detonation-znd

**Equation**: 1-D reactive Euler / ZND detonation (Arrhenius)
**Domain**: fluid
**Implementations**: reactive_euler_znd
**Execution mode**: reused-committed-matrix
**Provenance**: T2 committed detection matrix: runs/abd-witness-detonation-znd-1d-B-20260616T0235Z/kill_matrix.csv (detection-only reuse; selection artefacts not read).
**Alignment gate (baseline_control all survive)**: PASS

## Generation / detection (no selection / k* reported)

| Metric | Value |
|---|---|
| M-yield (MRs derived) | 18 |
| M-block (NOETHER blocks covered) | 2 (Conservation, O_le) |
| M-detect (real mutants killed) | 12/36 = 0.333 |
| Wilson 95% CI | [0.202, 0.497] |
| Underpowered (n<10) | False |
| GenMorph feasible | False |

## Per-block detection

| Block | MRs | detected/n | rate | Wilson95 |
|---|---|---|---|---|
| Conservation | D1-energy_conservation, D1-mass_conservation, D1-momentum_conservation, D1-positivity, D1-realizability, D2-energy_conservation, D2-mass_conservation, D2-momentum_conservation, D2-positivity, D2-realizability, D3-energy_conservation, D3-mass_conservation, D3-momentum_conservation, D3-positivity, D3-realizability | 6/36 | 0.167 | [0.079, 0.319] |
| O_le | D1-entropy, D2-entropy, D3-entropy | 12/36 | 0.333 | [0.202, 0.497] |

## Per-fault-class detection

| fault_class | detected/n | rate |
|---|---|---|
| entropy_fault | 3/6 | 0.500 |
| flux_conservation_fault | 6/6 | 1.000 |
| galilean_fault | 0/6 | 0.000 |
| positivity_fault | 0/6 | 0.000 |
| progress_realizability_fault | 3/6 | 0.500 |
| reaction_rate_fault | 0/6 | 0.000 |

## Per-MR kill counts (real mutants)

| MR | block | kills |
|---|---|---|
| D1-mass_conservation | Conservation | 2 |
| D1-momentum_conservation | Conservation | 2 |
| D1-energy_conservation | Conservation | 2 |
| D1-positivity | Conservation | 0 |
| D1-realizability | Conservation | 0 |
| D1-entropy | O_le | 4 |
| D2-mass_conservation | Conservation | 2 |
| D2-momentum_conservation | Conservation | 2 |
| D2-energy_conservation | Conservation | 2 |
| D2-positivity | Conservation | 0 |
| D2-realizability | Conservation | 0 |
| D2-entropy | O_le | 4 |
| D3-mass_conservation | Conservation | 2 |
| D3-momentum_conservation | Conservation | 2 |
| D3-energy_conservation | Conservation | 2 |
| D3-positivity | Conservation | 0 |
| D3-realizability | Conservation | 0 |
| D3-entropy | O_le | 4 |

## GenMorph feasibility (M-feasible)

- feasible: False
- reason: field / trajectory / eigenvalue I/O; per-eval is a full PDE / kinetics / transport solve; structural MRs relate multiple executions (D1–D3).
- expressibility tier: beyond two-execution (jir,jor) tier (D4)
