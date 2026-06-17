# S10 — NOETHER home-field generation→detection (executable first increment)

Executable instantiation of the §2 metrics + §2.1 single-variable "aligned"
methodology from
`docs/tosem_maturity_2026-06-16/noether_homefield_benchmark_candidates.md`.

## Scope and red line

- Computes **generation/detection only**: M-yield, M-block, M-detect (+ Wilson
  95% CI), per-block / per-fault-class detection, optional paired McNemar.
- Does **not** compute any **selection** quantity (minimum cover k\*, reduction,
  collapse/trichotomy, SMS, domination) — those are the sibling paper T2's
  claims (salami boundary, candidate-list doc §8).
- `heat-1d` is fully self-contained (authored here, no T2 dependency).
  `advdiff-2d` **reuses** the T2 (Minimum-MR-SubSet) operator-algebra substrate
  (two independent solvers + algebra-MR battery + operator-fault pool) and runs
  a detection-only loop over it, with attribution.

## SUTs

| SUT | source | equation | MRs | mutants | blocks |
|---|---|---|---|---|---|
| `heat-1d` | self-contained (`suts/heat_sut.py`) | `u_t=α u_xx`, Dirichlet, explicit FDM | 6 | 8 (incl. 2 baseline) | O_le, G, L\* |
| `advdiff-2d` | T2 `mcmr.pde_xeval` (reused) | `u_t+c·∇u=α∇²u`, periodic; M-FV vs M-SP | 11 | 31 (incl. 2 baseline) | O_le, G, L\*, Conservation |

## Run

```bash
# heat needs numpy; advdiff also needs scipy + the T2 substrate on disk
pip install -r requirements.txt
python3 run_homefield_detection.py                 # all available SUTs
python3 run_homefield_detection.py --sut heat      # one SUT
T2_ROOT=/path/to/Minimum-MR-SubSet/scripts python3 run_homefield_detection.py
```

Outputs land in `results/<sut>/detection_metrics.json` + `REPORT.md`, plus
`results/summary.json`.

## Results (one execution in this environment)

| SUT | M-yield | M-block | M-detect | Wilson 95% | alignment | GenMorph feasible |
|---|---|---|---|---|---|---|
| heat-1d | 6 | 3 (O_le,G,L\*) | 5/6 = 0.833 | [0.436, 0.970] | PASS | False |
| advdiff-2d | 11 | 4 (O_le,G,L\*,Conservation) | 13/29 = 0.448 | [0.284, 0.625] | PASS | False |

heat-1d is underpowered (n=6, CLAUDE.md C6); advdiff-2d n=29.

## Honesty notes

- **Alignment gate (§2.1)**: every `baseline_control` equivalent survives all
  MRs in both SUTs (else the run is flagged untrustworthy).
- **Self-consistent faults are honestly undetected** — direct evidence for doc
  §10.2 (MT's oracle-free limit): heat `coeff_x1p1` (+10% diffusion, stable)
  survives all MRs; advdiff `diffusion_coefficient_error` 0/2 and
  `advection_speed_error` 0/3 are likewise undetected. These are NOT removed to
  inflate the score.
- **Tolerances are fixed a priori** from IEEE-754 round-off / physics, never
  tuned to outcomes.
- **M-feasible**: GenMorph is infeasible on both SUTs (field-valued I/O,
  per-eval PDE-solve cost, and the two-execution `(jir,jor)` expressibility
  limit — doc §1.D / §10).

## Provenance / attribution

`advdiff-2d` substrate: Minimum-MR-SubSet `scripts/mcmr/pde_xeval/`
(`solvers.py`, `mr_battery.py`, `mutations.py`). Upstream solvers and the
fault pool are the shared experimental infrastructure disclosed in the cover
letter; this harness contributes only the NOETHER-side generation/detection
evaluation and the §2 metrics.
