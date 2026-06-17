# S10 — NOETHER home-field generation→detection

Executable instantiation of the §2 metrics + §2.1 single-variable "aligned"
methodology from
`docs/tosem_maturity_2026-06-16/noether_homefield_benchmark_candidates.md`.

## Scope and red line

- Computes **generation/detection only**: M-yield, M-block, M-detect (+ Wilson
  95% CI), per-block / per-fault-class detection, optional paired McNemar.
- Does **not** compute any **selection** quantity (minimum cover k\*, reduction,
  collapse/trichotomy, SMS, domination) — those are the sibling paper T2's
  claims (salami boundary, candidate-list doc §8).

## Two reuse modes (labelled honestly per SUT)

| `execution_mode` | meaning | SUTs |
|---|---|---|
| `executed-here` | run in this harness now | heat-1d, wave-1d, poisson-1d (self-contained, no T2), advdiff-2d (via T2 substrate) |
| `reused-committed-matrix` | generation metrics re-derived from a **committed** T2 `kill_matrix.csv` (detection data NOT re-run here); selection artefacts not read | radxfer-G2, grayscott, detonation-znd, combustion-gri30, pincell-xeval |

The committed-matrix mode is the sanctioned "same kill matrix, different
question" reuse (`empirical_reuse_from_T2.md`): T2 asked selection, NOETHER asks
generation. `provenance` in each `detection_metrics.json` records the source run.

## SUTs and results (one execution / ingestion in this environment)

| SUT | domain | mode | M-yield | M-block (blocks) | M-detect | Wilson 95% | alignment |
|---|---|---|---|---|---|---|---|
| heat-1d | thermal | exec | 6 | 3 (O≤,G,L\*) | 5/6=0.833 | [0.436,0.970] | PASS |
| wave-1d | fluid | exec | 5 | 4 (O≤,G,Cons,**T_rev\***) | 6/6=1.000 | [0.610,1.000] | PASS |
| poisson-1d | thermal | exec | 5 | 3 (O≤,G,L\*) | 5/6=0.833 | [0.436,0.970] | PASS |
| advdiff-2d | thermal×fluid | exec | 11 | 4 (O≤,G,L\*,Cons) | 13/29=0.448 | [0.284,0.625] | PASS |
| radxfer-G2 | thermal | reused | 16 | 4 (O≤,G,L\*,Cons) | 25/31=0.806 | [0.637,0.908] | PASS |
| grayscott | fluid | reused | 20 | 4 (O≤,G,L\*,Cons) | 41/44=0.932 | [0.818,0.977] | PASS |
| detonation-znd | fluid | reused | 18 | 2 (O≤,Cons) | 12/36=0.333 | [0.202,0.497] | PASS |
| combustion-gri30 | thermal | reused | 16 | 2 (O≤,Cons) | 34/54=0.630 | [0.496,0.746] | PASS |
| pincell-xeval | reactor | reused | 22 | 3 (O≤,G,L\*) | 24/86=0.279 | [0.195,0.382] | **FAIL** |

8 SUTs pass the alignment gate; **pincell-xeval FAILS it** (see Honesty).
heat/wave/poisson are underpowered (n=6, CLAUDE.md C6).

## Run

```bash
pip install -r requirements.txt
python3 run_homefield_detection.py                          # all available SUTs
python3 run_homefield_detection.py --sut heat,wave,poisson  # self-contained only
T2_ROOT=/path/to/Minimum-MR-SubSet/scripts python3 run_homefield_detection.py
```

Outputs: `results/<sut>/detection_metrics.json` + `REPORT.md`, `results/summary.json`.

## Honesty notes

- **Alignment gate (§2.1)** has teeth: `pincell-xeval` is flagged FAIL because
  T2's committed matrix marks 3 `…-identity` baseline_control mutants as killed
  (residual 1.0 > tol 0.5). Its detection rate is therefore **not** treated as a
  trustworthy result; it is retained, flagged, for transparency rather than
  dropped.
- **Self-consistent faults are honestly undetected** (doc §10.2): heat/poisson
  `coeff_x1p1` (+10% coefficient, stable) survive all MRs; advdiff
  `diffusion_coefficient_error` 0/2 and `advection_speed_error` 0/3 likewise.
  Not removed to inflate scores.
- **Blocks track physics**: `wave-1d` (energy-conserving, reversible) uniquely
  populates **Conservation + T_rev\***; the dissipative SUTs (heat, radxfer)
  leave T_rev\* empty by construction — the "proves what it cannot derive" point.
- Tolerances fixed a priori (round-off / physics), never tuned to outcomes.
- **M-feasible**: GenMorph infeasible on every SUT (field / trajectory /
  eigenvalue I/O, per-eval solve cost, two-execution `(jir,jor)` limit; doc §1.D).

## Provenance / attribution

- `advdiff-2d` substrate: Minimum-MR-SubSet `scripts/mcmr/pde_xeval/`.
- `reused-committed-matrix` SUTs ingest `runs/abd-witness-*/kill_matrix.csv`
  from Minimum-MR-SubSet (detection-only; selection artefacts not read). Upstream
  solvers/oracles (OpenMC/OpenMOC, Cantera) are the shared infrastructure
  disclosed in the cover letter.
