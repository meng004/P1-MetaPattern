# S10 — NOETHER home-field generation→detection

Executable instantiation of the §2 metrics + §2.1 single-variable "aligned"
methodology from
`docs/tosem_maturity_2026-06-16/noether_homefield_benchmark_candidates.md`.

## Thesis (the argument — see `ANALYSIS.md`)

The contribution is not the per-SUT detection rates (small-n, reported only for
completeness). It is three falsifiable **detectability laws** argued from
cross-SUT structure: (P1) the MR battery's block pattern is a function of the
operator's symmetry algebra, predictable before testing; (P2) a symmetry-based
oracle is structurally blind to faults living in the invariance it exploits, so a
single oracle family is incomplete and the MR battery + differential oracle are
provably complementary; (P3) differential testing has a hard detectability floor
at the discretisation gap δ. Each law ships with its one-line refutation in
`ANALYSIS.md`.

## Scope and red line

- Computes **generation/detection only**: M-yield, M-block, M-detect (+ Wilson
  95% CI), per-block / per-fault-class detection, optional paired McNemar.
- Does **not** compute any **selection** quantity (minimum cover k\*, reduction,
  collapse/trichotomy, SMS, domination) — those are the sibling paper T2's
  claims (salami boundary, candidate-list doc §8).

## Two reuse modes (labelled honestly per SUT)

| `execution_mode` | meaning | SUTs |
|---|---|---|
| `executed-here` | run in this harness now | heat-1d, wave-1d, poisson-1d (self-contained, no T2), advdiff-2d + advdiff-xeval-diff (via T2 substrate) |
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
| advdiff-xeval-diff | thermal×fluid | exec | 1 | 1 (E\*) | 12/29=0.414 | [0.255,0.593] | PASS |
| radxfer-G2 | thermal | reused | 16 | 4 (O≤,G,L\*,Cons) | 25/31=0.806 | [0.637,0.908] | PASS |
| grayscott | fluid | reused | 20 | 4 (O≤,G,L\*,Cons) | 41/44=0.932 | [0.818,0.977] | PASS |
| detonation-znd | fluid | reused | 18 | 2 (O≤,Cons) | 12/36=0.333 | [0.202,0.497] | PASS |
| combustion-gri30 | thermal | reused | 16 | 2 (O≤,Cons) | 34/54=0.630 | [0.496,0.746] | PASS |
| pincell-xeval | reactor | reused | 22 | 3 (O≤,G,L\*) | 24/86=0.279 | [0.195,0.382] | **FAIL** |

9 SUTs pass the alignment gate; **pincell-xeval FAILS it** (see Honesty).
heat/wave/poisson are underpowered (n=6, CLAUDE.md C6).

## Cross-implementation differential oracle (§10.2, live)

`advdiff-xeval-diff` executes what the MR adapter deferred: a **neutral**
per-field differential oracle. M-FV and M-SP are run on the same case (their
operators are disjoint, so a mutation to one leaves the other a clean
reference); a mutant is detected when the mutated field diverges from the clean
field by more than a calibrated tolerance.

**§10.2 tolerance calibration.** Field difference is normalized by the initial
amplitude (not the evolved field — diffused-away modes would otherwise
manufacture spurious gaps). The legitimate pristine cross-impl gap is
δ=0.185 (max over 5 probes); the headline tolerance is τ=5·δ=0.925, fixed a
priori. Post-hoc sensitivity (transparency, not tuned to outcome):

| safety | τ | detected | baseline FP |
|---|---|---|---|
| 1.5 | 0.278 | 16/29 | 0/2 |
| 2.0 | 0.370 | 15/29 | 0/2 |
| 3.0 | 0.555 | 13/29 | 0/2 |
| **5.0** | **0.925** | **12/29** | **0/2** |
| 10.0 | 1.850 | 7/29 | 0/2 |

**Paired comparison (algebra-MR battery vs differential oracle, same 29 real
mutants):** MR 13/29, differential 12/29; **MR-only=6, differential-only=5**
(McNemar exact p=1.0). The two oracles are **complementary**, not redundant:

- differential-only catches *advection-speed* and *wavenumber/symbol-sign*
  faults — the MR battery is invariant (translation/Galilean) to exactly the
  broken parameter, so it is structurally blind to them;
- MR-only catches *conservation*, *boundary*, and *inhomogeneity* faults that
  perturb the field below τ but break a structural invariant;
- both miss self-consistent coefficient errors. Notably `fv_lap_coeff_x2`
  (doubled diffusion) gives a 0.31 field change — *above* δ=0.185 but *below*
  τ=0.925, i.e. the legitimate discretisation gap masks the defect. This is the
  §10.2 thesis made quantitative.

Blind spot (§10.2): faults in code shared by both implementations are
common-mode and invisible to this oracle; here every mutation targets one
implementation, so that case is not exercised.

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
