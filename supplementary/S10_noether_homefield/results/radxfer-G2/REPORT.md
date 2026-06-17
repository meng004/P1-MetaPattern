# NOETHER home-field detection -- radxfer-G2

**Equation**: multigroup radiation diffusion (1/c)∂E_g/∂t=∇·(D_g∇E_g)-σ_a,gE_g+scatter (2-D periodic), G=2
**Domain**: thermal
**Implementations**: M-FD-theta, M-SP-IMEX
**Execution mode**: reused-committed-matrix
**Provenance**: T2 committed detection matrix: runs/abd-witness-radxfer-G2-2d-B-20260615T084600Z/kill_matrix.csv (detection-only reuse; selection artefacts not read).

**Alignment gate (baseline_control all survive)**: PASS

## Generation / detection (no selection / k* reported)

| Metric | Value |
|---|---|
| M-yield (MRs derived) | 16 |
| M-block (NOETHER blocks covered) | 4 (Conservation, G, L*, O_le) |
| M-detect (real mutants killed) | 25/31 = 0.806 |
| Wilson 95% CI | [0.637, 0.908] |
| Underpowered (n<10) | False |
| GenMorph feasible | False |

## Per-block detection

| Block | MRs | detected/n | rate | Wilson95 |
|---|---|---|---|---|
| Conservation | fd-scatter_conservation, fd-total_energy_balance, sp-scatter_conservation, sp-total_energy_balance | 16/31 | 0.516 | [0.348, 0.680] |
| G | fd-fundamental_mode_eigenvalue, fd-rotation_invariance, fd-translation_invariance, sp-fundamental_mode_eigenvalue, sp-rotation_invariance, sp-translation_invariance | 18/31 | 0.581 | [0.408, 0.736] |
| L* | fd-refinement_self_convergence, sp-refinement_self_convergence | 3/31 | 0.097 | [0.034, 0.249] |
| O_le | fd-linearity_superposition, fd-scaling_homogeneity, sp-linearity_superposition, sp-scaling_homogeneity | 2/31 | 0.065 | [0.018, 0.207] |

## Per-fault-class detection

| fault_class | detected/n | rate |
|---|---|---|
| absorption_opacity_fault | 4/8 | 0.500 |
| diffusion_coefficient_fault | 6/8 | 0.750 |
| scatter_entry_fault | 6/6 | 1.000 |
| source_fault | 4/4 | 1.000 |
| stencil_fault | 2/2 | 1.000 |
| time_weight_fault | 3/3 | 1.000 |

## Per-MR kill counts (real mutants)

| MR | block | kills |
|---|---|---|
| fd-linearity_superposition | O_le | 1 |
| fd-scaling_homogeneity | O_le | 1 |
| fd-total_energy_balance | Conservation | 4 |
| fd-scatter_conservation | Conservation | 3 |
| fd-fundamental_mode_eigenvalue | G | 10 |
| fd-translation_invariance | G | 1 |
| fd-rotation_invariance | G | 1 |
| fd-refinement_self_convergence | L* | 2 |
| sp-linearity_superposition | O_le | 1 |
| sp-scaling_homogeneity | O_le | 1 |
| sp-total_energy_balance | Conservation | 6 |
| sp-scatter_conservation | Conservation | 3 |
| sp-fundamental_mode_eigenvalue | G | 7 |
| sp-translation_invariance | G | 1 |
| sp-rotation_invariance | G | 1 |
| sp-refinement_self_convergence | L* | 1 |

## GenMorph feasibility (M-feasible)

- feasible: False
- reason: field / trajectory / eigenvalue I/O; per-eval is a full PDE / kinetics / transport solve; structural MRs relate multiple executions (D1–D3).
- expressibility tier: beyond two-execution (jir,jor) tier (D4)
