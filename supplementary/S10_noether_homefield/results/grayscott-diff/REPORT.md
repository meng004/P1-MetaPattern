# NOETHER home-field detection -- grayscott-diff

**Equation**: 2-D Gray-Scott reaction-diffusion (U,V), periodic
**Domain**: fluid
**Implementations**: M-FD-IMEX, M-SP-IMEX
**Execution mode**: executed-here
**Provenance**: substrate: Minimum-MR-SubSet mcmr.grayscott; differential oracle executed here; target_impl='both' faults patch shared operators (common-mode, in the oracle kernel).
**Tolerance calibration (§10.2)**: tau=5.4e-05 = 5.0x pristine gap delta=1.1e-05 (n_probes=None)
**Alignment gate (baseline_control all survive)**: PASS

## Generation / detection (no selection / k* reported)

| Metric | Value |
|---|---|
| M-yield (MRs derived) | 1 |
| M-block (NOETHER blocks covered) | 1 (E*) |
| M-detect (real mutants killed) | 28/44 = 0.636 |
| Wilson 95% CI | [0.489, 0.762] |
| Underpowered (n<10) | False |
| GenMorph feasible | False |

## Per-block detection

| Block | MRs | detected/n | rate | Wilson95 |
|---|---|---|---|---|
| E* | xeval-differential | 28/44 | 0.636 | [0.489, 0.762] |

## Per-fault-class detection

| fault_class | detected/n | rate |
|---|---|---|
| boundary_fault | 2/2 | 1.000 |
| coupling_fault | 2/4 | 0.500 |
| feed_fault | 0/6 | 0.000 |
| kill_fault | 6/6 | 1.000 |
| positivity_fault | 2/2 | 1.000 |
| reaction_rate_fault | 0/6 | 0.000 |
| time_integration_fault | 1/3 | 0.333 |
| u_diffusion_fault | 8/8 | 1.000 |
| v_diffusion_fault | 7/7 | 1.000 |

## Per-MR kill counts (real mutants)

| MR | block | kills |
|---|---|---|
| xeval-differential | E* | 28 |

## GenMorph feasibility (M-feasible)

- feasible: False
- reason: G×N×N (radxfer) / N×N field comparison across two full PDE solves per case; neutral cross-impl oracle.
- expressibility tier: method-comparison oracle (E*), beyond (jir,jor) (D4)
