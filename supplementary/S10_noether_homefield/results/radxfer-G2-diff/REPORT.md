# NOETHER home-field detection -- radxfer-G2-diff

**Equation**: multigroup radiation diffusion (1/c)dE_g/dt=div(D_g grad E_g)-sigma_a,g E_g+scatter (2-D periodic, G=2)
**Domain**: thermal
**Implementations**: M-FD-theta, M-SP-IMEX
**Execution mode**: executed-here
**Provenance**: substrate: Minimum-MR-SubSet mcmr.radxfer; differential oracle executed here; absorption/scatter/source faults are common-mode (shared operators), diffusion/stencil/theta/etd are impl-specific.
**Tolerance calibration (§10.2)**: tau=0.008457 = 5.0x pristine gap delta=0.001691 (n_probes=None)
**Alignment gate (baseline_control all survive)**: PASS

## Generation / detection (no selection / k* reported)

| Metric | Value |
|---|---|
| M-yield (MRs derived) | 1 |
| M-block (NOETHER blocks covered) | 1 (E*) |
| M-detect (real mutants killed) | 10/31 = 0.323 |
| Wilson 95% CI | [0.186, 0.499] |
| Underpowered (n<10) | False |
| GenMorph feasible | False |

## Per-block detection

| Block | MRs | detected/n | rate | Wilson95 |
|---|---|---|---|---|
| E* | xeval-differential | 10/31 | 0.323 | [0.186, 0.499] |

## Per-fault-class detection

| fault_class | detected/n | rate |
|---|---|---|
| absorption_opacity_fault | 0/8 | 0.000 |
| diffusion_coefficient_fault | 8/8 | 1.000 |
| scatter_entry_fault | 0/6 | 0.000 |
| source_fault | 0/4 | 0.000 |
| stencil_fault | 1/2 | 0.500 |
| time_weight_fault | 1/3 | 0.333 |

## Per-MR kill counts (real mutants)

| MR | block | kills |
|---|---|---|
| xeval-differential | E* | 10 |

## GenMorph feasibility (M-feasible)

- feasible: False
- reason: G×N×N (radxfer) / N×N field comparison across two full PDE solves per case; neutral cross-impl oracle.
- expressibility tier: method-comparison oracle (E*), beyond (jir,jor) (D4)
