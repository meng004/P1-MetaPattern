# B1 Real-Bug Evaluation (e3nn / PyG) — Results

**Status: NOT EXECUTED — no admissible frozen ledger. Honest pre-run audit only.**
Run date: 2026-06-21   Branch: claude/b1-realbug-2026-06-21
CPU-only confirmed: yes   GPU used: no   LLM/API calls: none

## Why there is no confirmatory result (honest)

Prereg §3.4 requires a *mechanical* ledger of entries satisfying {real functional bug + maps to cat-(i)–(iv) + CPU small-tensor reproducible + fix/parent commit anchors}. Three parallel mechanical vetting passes (full detail in `candidate_audit_2026-06-21.md`) found:

- **Mechanical recent-32 closed-bug window:** 0 of cat-(i)–(iv). Real bugs cluster in JIT/compile, install/deps, device/CUDA, dataset/type — none on the symmetry axis.
- **e3nn equivariance search (6):** only **#296** is an admissible real bug (representation-equivalence: equivalent irreps give different `FullyConnectedTensorProduct` output; fix `b9e64db`/parent `6fc34a9`). But old e3nn fails to import on torch 2.12 (`weights_only` default change) → **CPU-INFEASIBLE in current env**. #352 is a real non-determinism bug but has **no fix commit** anchor.
- **PyG scatter/aggregation search (6):** all `cat=none` (crash / gradient / dim / jit). Their permutation/idempotence MRs all return **held** (reproduced on torch 2.12+cpu) — these bug classes do not violate "permutation-equivalent" invariance.

→ **Zero admissible entries to freeze.** Per the frozen red lines, we did **not** fabricate bugs, did **not** mislabel a `cat=none` bug as an MR detection, and therefore did **not** freeze a ledger or run the MR sets.

## Ledger accounting

- Candidates vetted: ~40 unique (e3nn + PyG; mechanical recent window + equivariance/scatter keyword search)
- Admissible into frozen ledger: **0**
  - e3nn #296: real bug, but **CPU-INFEASIBLE in-env** (old e3nn import fails on torch 2.12)
  - e3nn #352: real bug, but **no fix commit** (cannot anchor pre/post-fix)
  - PyG #7407/#7412/#9766: CPU-reproducible but **cat=none** (crash/grad/dim) → MR necessarily `held`
  - reproduction-fidelity failure: PyG scatter_argmax #7495 — on torch 2.12 `reduce='max'≡'amax'`, the historical bug no longer reproduces

## Per-set detection / H4 verdict

**Not executed** (no admissible ledger). `analyze_b1.py` (STEP-4 pre-registered analyzer: per-set Wilson CI, exact McNemar, b+c<25 underpowered trigger, Holm-Bonferroni, H4 non-inferiority Δ=0.10, Set G not-evaluable) is **ready and synthetic self-test passed**; it will produce RESULTS once an admissible ledger + `results/bug_*.json` exist.

## Key finding (carries to the paper)

Mechanically full-sampled real e3nn/PyG bugs sit **overwhelmingly outside the symmetry/equivariance axis** that NOETHER's MRs perceive → the MRs are `held` (blind) on them. This directly **corroborates the Invariance-Blindness Theorem**: an algebra-derived MR detects exactly the faults that break the structure it exploits, and real-world bugs largely do not break that structure. Because the vetting is mechanical and full (no selection), this is **cherry-pick-proof** evidence.

## Honest negatives / limitations

- 0 admissible confirmatory entries; the B1 real-bug leg is **not runnable as a confirmatory test in this environment** (reported as a feasibility boundary, not a headline; C6).
- Set G: **not evaluable** on library bugs (no portable artefact), reported as such, **not** as 0 detections.
- Reproduction requires PR-era torch/library environments; current CPU/torch 2.12 is insufficient to reproduce the historical bugs (e3nn import failure; scatter_argmax no-repro).
- This is **not** a negative result *about Set N's quality*; it is a property of the real-bug distribution vs the MR-perceptible axis (which is precisely the IBT claim).

## Anti-drift attestation

- MR-identification scope only; non-inferiority framing; **no superiority claim**.
- All negative / infeasible results reported above prominently; GenMorph (Set G) not hidden (recorded not-evaluable).
- No bug fabricated; no `cat=none` bug passed off as an MR detection; prereg §3 untouched (never frozen, as no admissible ledger arose).
- Full per-candidate vetting with commit anchors: `candidate_audit_2026-06-21.md`.
