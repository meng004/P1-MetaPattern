# NOETHER home-field detection -- pincell-xeval

**Equation**: 2-group neutron transport, pin-cell (OpenMC vs OpenMOC)
**Domain**: reactor
**Implementations**: openmc, openmoc
**Execution mode**: reused-committed-matrix
**Provenance**: T2 committed detection matrix: runs/abd-witness-metbench-pincell-xeval-2g_uo2_offcentre-20260613T154614Z/kill_matrix.csv (detection-only reuse; selection artefacts not read).

**Alignment gate (baseline_control all survive)**: FAIL

## Generation / detection (no selection / k* reported)

| Metric | Value |
|---|---|
| M-yield (MRs derived) | 22 |
| M-block (NOETHER blocks covered) | 3 (G, L*, O_le) |
| M-detect (real mutants killed) | 24/86 = 0.279 |
| Wilson 95% CI | [0.195, 0.382] |
| Underpowered (n<10) | False |
| GenMorph feasible | False |

## Per-block detection

| Block | MRs | detected/n | rate | Wilson95 |
|---|---|---|---|---|
| G | openmc-pincell-group-permute, openmc-pincell-mirror-x, openmc-pincell-mirror-y, openmc-pincell-rotate-90, openmoc-pincell-group-permute, openmoc-pincell-mirror-x, openmoc-pincell-mirror-y, openmoc-pincell-rotate-90 | 7/86 | 0.081 | [0.040, 0.159] |
| L* | openmc-pincell-particles-refine, openmoc-pincell-refine-ray-tracks | 4/86 | 0.047 | [0.018, 0.114] |
| O_le | openmc-pincell-fuel-radius, openmc-pincell-fuel-sigma-s, openmc-pincell-fuel-sigma-t, openmc-pincell-moderator-sigma-a, openmc-pincell-nu-sigma-f, openmc-pincell-sigma-a, openmoc-pincell-fuel-radius, openmoc-pincell-fuel-sigma-s, openmoc-pincell-fuel-sigma-t, openmoc-pincell-moderator-sigma-a, openmoc-pincell-nu-sigma-f, openmoc-pincell-sigma-a | 19/86 | 0.221 | [0.146, 0.320] |

## Per-fault-class detection

| fault_class | detected/n | rate |
|---|---|---|
| absorption_cross_section | 1/4 | 0.250 |
| fuel_geometry_radius | 2/4 | 0.500 |
| geometry_symmetry_transform | 2/4 | 0.500 |
| moderator_material_response | 2/8 | 0.250 |
| monte_carlo_sampling_refinement | 2/4 | 0.500 |
| neutron_source_spectrum | 6/14 | 0.429 |
| pincell_physics_fault | 9/44 | 0.205 |
| thermal_feedback_coupling | 0/4 | 0.000 |

## Per-MR kill counts (real mutants)

| MR | block | kills |
|---|---|---|
| openmc-pincell-nu-sigma-f | O_le | 2 |
| openmc-pincell-sigma-a | O_le | 3 |
| openmc-pincell-group-permute | G | 3 |
| openmc-pincell-fuel-sigma-t | O_le | 1 |
| openmc-pincell-moderator-sigma-a | O_le | 2 |
| openmc-pincell-fuel-sigma-s | O_le | 3 |
| openmc-pincell-fuel-radius | O_le | 2 |
| openmc-pincell-particles-refine | L* | 2 |
| openmc-pincell-rotate-90 | G | 0 |
| openmc-pincell-mirror-x | G | 1 |
| openmc-pincell-mirror-y | G | 1 |
| openmoc-pincell-nu-sigma-f | O_le | 5 |
| openmoc-pincell-sigma-a | O_le | 4 |
| openmoc-pincell-group-permute | G | 4 |
| openmoc-pincell-fuel-sigma-t | O_le | 2 |
| openmoc-pincell-moderator-sigma-a | O_le | 3 |
| openmoc-pincell-fuel-sigma-s | O_le | 4 |
| openmoc-pincell-fuel-radius | O_le | 5 |
| openmoc-pincell-rotate-90 | G | 2 |
| openmoc-pincell-mirror-x | G | 2 |
| openmoc-pincell-mirror-y | G | 2 |
| openmoc-pincell-refine-ray-tracks | L* | 2 |

## GenMorph feasibility (M-feasible)

- feasible: False
- reason: field / trajectory / eigenvalue I/O; per-eval is a full PDE / kinetics / transport solve; structural MRs relate multiple executions (D1–D3).
- expressibility tier: beyond two-execution (jir,jor) tier (D4)
