# Minimal-detecting-subset / family-necessity analysis (task C, 2026-06-22)

Reproduce: `python3 experiment_realbug/minimal_subset_analysis.py`

**Scope.** This audits the family-independence claim of the paper
(`subsec:generator-family`, "Fault classes and detection independence") on the
B1 real-bug corpus, now **n=23** (the 21 four-SUT-domain faults + the two
structure-present positives `diffrax`/family-e and `clawpack`/family-g). It is
computed from the recorded FIRED/HELD detections (no re-runs).

Provenance of the data: `COVERAGE_SUMMARY.md` §1 (fault list + MR family + Mode)
and §6 (FIRED-type split), plus `results/bug_diffrax_srk_backward.json` and
`results/bug_clawpack_tvd2_recon_bounds.json`.

## What this CAN establish rigorously (from the recorded detections)

1. **Set-cover minimal detecting subset** under the recorded one-family-per-fault
   assignment.
2. **Discriminating necessity**: for each family, whether its necessity rests on a
   genuine *non-crash* law violation (numeric / convergence / transport) or only
   on a crash that a generic smoke test would also surface.

## What this CANNOT establish (honest limit)

True **pairwise orthogonality** — whether family X's MR *also* fires on family
Y's fault — needs the full **cross-detection matrix** (every family MR × every
fault), i.e. rebuilding the per-fault library environments (multiple SciPy /
PySCF / OpenMC / DeepXDE / diffrax / Clawpack versions, several requiring
conda + nuclear data or removed `numpy.distutils`). That is not achievable in
this environment and remains future work. This analysis therefore establishes
**necessity** (a lower bound), not non-redundancy beyond the recorded partition.

## Result

| fam | #faults | #non-crash | witnesses (`*` = non-crash discriminating) |
|---|---|---|---|
| a | 5 | 4 | `*`normalize[num], `*`rotperiodic[transport], periodic_point[crash], `*`d2h_orbsym[num], `*`fht[num,marginal] |
| b | 2 | 1 | `*`smearing[num], neumann_robin[crash] |
| c | 3 | 2 | eigh[crash], `*`complexsym[num], `*`fwd_hessian[num,reach-caveat] |
| d | 1 | 1 | `*`ifp_adjoint[num] |
| e | 1 | 1 | `*`diffrax_srk_backward[num] (NEW) |
| f | 3 | 3 | `*`akima[num], `*`cram_clip[num], `*`boundary_float32[num] |
| g | 1 | 1 | `*`clawpack_tvd2[num] (NEW) |
| h | 4 | 2 | lsoda[crash], `*`diis[conv], `*`train_next_batch[conv], tally_trigger[crash] |
| i | 1 | 1 | `*`simpson_even_order[num] |
| j | 2 | 1 | banded_jac[crash], `*`no_reduce[num] |

- **Populated families:** 10 / 10 (a–j).
- **Families with ≥1 non-crash witness:** **10 / 10**.
- **Families resting only on a crash:** **0**.
- **Families on a single non-crash witness:** 6 (b, d, e, g, i, j) — thin but present.
- **Faults covered:** 23 / 23.

**Minimal detecting subset** (set cover, under the recorded one-family-per-fault
partition): **all 10 populated families**. Every populated family is necessary —
removing it drops the fault(s) assigned only to it.

## Verdict

The family-independence claim holds at **witness level for all ten families, on a
non-crash basis**: every family detects at least one genuine numeric, convergence,
or transport law violation that a crash-only smoke test would miss. This directly
answers the paper's own threat that "6 of 21 are crash-type" — the discriminating
power does not rest on crash faults for any family. Six families (b, d, e, g, i, j)
currently rest on a single non-crash witness, so widening the corpus for those is
the natural next strengthening. Full pairwise orthogonality and a provably minimal
(non-redundant) subset remain future work pending the cross-detection matrix.
