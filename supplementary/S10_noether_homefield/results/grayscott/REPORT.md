# NOETHER home-field detection -- grayscott

**Equation**: 2-D Gray-Scott reaction-diffusion (u,v)
**Domain**: fluid
**Implementations**: M-FD-IMEX, M-SP-IMEX
**Execution mode**: reused-committed-matrix
**Provenance**: T2 committed detection matrix: runs/abd-witness-grayscott-xeval-2d-B-20260615T023057Z/kill_matrix.csv (detection-only reuse; selection artefacts not read).

**Alignment gate (baseline_control all survive)**: PASS

## Generation / detection (no selection / k* reported)

| Metric | Value |
|---|---|
| M-yield (MRs derived) | 20 |
| M-block (NOETHER blocks covered) | 4 (Conservation, G, L*, O_le) |
| M-detect (real mutants killed) | 41/44 = 0.932 |
| Wilson 95% CI | [0.818, 0.977] |
| Underpowered (n<10) | False |
| GenMorph feasible | False |

## Per-block detection

| Block | MRs | detected/n | rate | Wilson95 |
|---|---|---|---|---|
| Conservation | fd-reaction-mass-transfer, fd-u-mass-balance, fd-v-mass-balance, sp-reaction-mass-transfer, sp-u-mass-balance, sp-v-mass-balance | 30/44 | 0.682 | [0.534, 0.800] |
| G | fd-rotation-inv, fd-translation-inv, sp-rotation-inv, sp-translation-inv | 3/44 | 0.068 | [0.024, 0.182] |
| L* | fd-refinement-self, sp-refinement-self | 2/44 | 0.045 | [0.013, 0.151] |
| O_le | fd-positivity-u, fd-positivity-v, fd-u-diffusion-dissipativity, fd-v-diffusion-dissipativity, sp-positivity-u, sp-positivity-v, sp-u-diffusion-dissipativity, sp-v-diffusion-dissipativity | 14/44 | 0.318 | [0.200, 0.466] |

## Per-fault-class detection

| fault_class | detected/n | rate |
|---|---|---|
| boundary_fault | 2/2 | 1.000 |
| coupling_fault | 4/4 | 1.000 |
| feed_fault | 6/6 | 1.000 |
| kill_fault | 6/6 | 1.000 |
| positivity_fault | 2/2 | 1.000 |
| reaction_rate_fault | 6/6 | 1.000 |
| time_integration_fault | 3/3 | 1.000 |
| u_diffusion_fault | 6/8 | 0.750 |
| v_diffusion_fault | 6/7 | 0.857 |

## Per-MR kill counts (real mutants)

| MR | block | kills |
|---|---|---|
| fd-u-mass-balance | Conservation | 9 |
| fd-v-mass-balance | Conservation | 8 |
| fd-reaction-mass-transfer | Conservation | 1 |
| fd-positivity-u | O_le | 0 |
| fd-positivity-v | O_le | 1 |
| fd-u-diffusion-dissipativity | O_le | 4 |
| fd-v-diffusion-dissipativity | O_le | 3 |
| fd-translation-inv | G | 2 |
| fd-rotation-inv | G | 2 |
| fd-refinement-self | L* | 2 |
| sp-u-mass-balance | Conservation | 8 |
| sp-v-mass-balance | Conservation | 11 |
| sp-reaction-mass-transfer | Conservation | 1 |
| sp-positivity-u | O_le | 0 |
| sp-positivity-v | O_le | 1 |
| sp-u-diffusion-dissipativity | O_le | 4 |
| sp-v-diffusion-dissipativity | O_le | 4 |
| sp-translation-inv | G | 0 |
| sp-rotation-inv | G | 0 |
| sp-refinement-self | L* | 0 |

## GenMorph feasibility (M-feasible)

- feasible: False
- reason: field / trajectory / eigenvalue I/O; per-eval is a full PDE / kinetics / transport solve; structural MRs relate multiple executions (D1–D3).
- expressibility tier: beyond two-execution (jir,jor) tier (D4)
