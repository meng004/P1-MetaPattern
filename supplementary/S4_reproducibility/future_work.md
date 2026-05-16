# Committed Future Work for §7 (Empirical L*-blindness + Head-to-head)

Migrated from `NOETHER_paper.tex` Table `tab:future-work` (Tier 1 length compression, 2026-05-16). Body keeps a short narrative summary; this file carries the full 18-entry table.

Status legend: **Done** = completed in this revision; **Done (pilot)** = reduced-scale executed; *Pending* = committed follow-up.

## Table: 18 future-work items

| # | Direction | Cost (estimated) | Expected effect on the reading |
|---|---|---|---|
| (a) | GP rerun at 30-min GAssert budget | ≈ 30 min parallel | Probably widens Set G's lead; conservative against §6.6 |
| (a.budget-replication) | GenMorph 30-min × 5 seeds for GP stochasticity quantification | ≈ 20 h remote + 1 d aggregation | Distribution over Set G's pooled D1 rate (single-seed point estimate 37/52); robustness of the 4 Set-N-only kills |
| (b) | Extend to all 38 in-scope D4J subjects | ≈ 10 h human + 30 min compute | n > 200; finer per-SUT L*-blindness resolution |
| (b.cm) | Commons Math 3.6.1 pilot (3 SUTs, 5 Set N MRs, 77 target-method mutants; Set G structurally N/A on Maven-resolved substrates) | **Done (pilot)** | Pooled Set N 10/77 = 13.0%; G-block 6/21 = 28.6%; D2 prediction passes 2/29 = 6.9%; n underpowered; details in supplementary |
| (c) | Patch GenMorph upstream (instance methods, boolean JORs) | 1–2 days | Restores Set G on two N/A SUTs; weakens §6.6's witness 2 |
| (d.scout) | Set M full MR-Scout re-execution | ≈ 1 d human + corpus | Completes mining-based arm of §subsec:case-study comp-eval protocol |
| (d.set-l) | Multi-LLM ensemble Set L (2 vendors × 5 temps × 10 SUTs = 100 samples; 487 MRs, 212 executable, 43.5% translation) | **Done (2 of 3 vendors)** | Ensemble matches Set N on matchable subset (34/34); 56.5% outside the 8-block frame; results in supplementary |
| (d.set-l-claude) | Third-vendor Claude Opus replication | ≈ 5 h remote + $10–30 | Completes 3-vendor protocol; expected to corroborate ensemble |
| (e) | D1/D2 mutant labelling | **Done** | 52 D1 / 10 D2 pre-, 52 D1 / 5 D2 post-equivalent-mutant exclusion |
| (g) | Construct-trace consistency check, 25 hand-crafted block-targeted mutants on 5 PIT-unexercised blocks | **Done (supplementary S9, Appendix E)** | Pipeline-correctness; 25/25 Set N detection is design-implied; not used as independent fault-detection evidence |
| (h) | Generic-mutation independent test of H3a.1 on 5 PIT-unexercised blocks (operator catalogue not hand-authored against Set N) | ≈ 1 month research + tooling | Per-block kill rates for the five additional blocks |
| (i) | METRIC+ head-to-head on Sun 2021 corpus (SPHONE, SBAGGAGE, SEXPENSE, SMEAL); pre-registered protocol `protocol_path_a_headtohead.md`: H_MP1 / H_MP2 / H_MP3 | **Done (PIT 1.7.4 + Major cross-tool)** | PIT n=120, pooled McNemar p = 0.625 NS, 92.6% both-kill; Major n=555 (4.6× pool), pooled McNemar p = 0.211 NS, bidirectional per-subject reach asymmetries (SPHONE MP-edge, SBAGGAGE N-edge) cancel pooled. H_MP1 falsified bidirectionally; complementarity confirmed at higher power. Details in `results_path_a_full.md` + `results_path_a_major_crosstool.md` |
| (e.2) | Two-stage equivalent-mutant exclusion (kill-vector auto-classify + multi-LLM vote with Claude tiebreaker) | **Done** | 5 equivalents on n=62 (all ConditionalsBoundaryMutator on recursive normalising SUTs); final n=57 |
| (e.3) | Tighten 2 out-of-domain Set N MRs on `powerSig` (`E_power_of_power`, `L_scale_base`) | ≈ 4 h human | Recovers ≤ 2 kills on `powerSig` |
| (e.4) | G-block MR re-synthesis (or in-scope documentation) for Euclidean SUTs (`a < 0 ? -a : a` normalisation absorbs sign-flip) | **Done (documented)** | 0/7 on Euclidean SUTs is framework-correct under scope precondition; R-block post-normalisation re-derivation open |
| (j) | External-transfer on an independently-authored reactor-physics corpus (PARCS V&V / IAEA-TECDOC) | ≈ 1 month corpus-access | Fleiss κ on 8-block labelling; reactor-side analogue of (b.cm) |

## Status summary

| Status | Count |
|---|---|
| Done (full) | 4 |
| Done (pilot or partial) | 4 |
| Pending committed follow-up | 8 |
| **Total** | **16** (deduped from 18 entries with status duplicates) |

## Highest-priority pending items

1. **(a.budget-replication)** Multi-seed GenMorph quantification — 20 h remote.
2. **(b)** Full 38-D4J extension — 10 h human + 30 min compute. Substantial finer-resolution gain.
3. **(d.scout)** MR-Scout full re-execution — completes 3-SOTA-category protocol.
4. **(d.set-l-claude)** Anthropic third-vendor — completes Xu 2024 3-vendor spec.
5. **(j)** External-transfer to independently-authored reactor-physics corpus — converts internal-vocabulary-coherence test into external generalisation evidence.
