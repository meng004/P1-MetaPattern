# S5 multiseed — Set G selection-bias check (GenMorph published 12-seed data)

Executes the Set-G side of fix-plan **A16(1)** / threat **A7**: quantify how much the
GenMorph head-to-head depends on the single comparison seed (seed=11), using GenMorph's
**own** published 12-seed replication results (Zenodo 10067096, `evaluation.zip`).

- `analyze_published_multiseed.py` — parser/analysis (no recomputation, no MR reimplementation).
- `multiseed_setg.json` — per-subject, per-seed matched union-kill + cross-seed stats.
- `multiseed_setg_report.md` — human-readable report (focus gcd/sin + all 23 subjects).

**Key results** (matched gen==PIT seed, union of FP-valid Set G MRs):
- `gcd`: 11/25 (seed11) … up to 18/25; seed11 is rank 3/12 (low end, 61% of best seed).
- `sin`: 16/26 (seed11), range 13–17; seed11 rank 6/12 (median).
- Across 23 subjects, **seed=11 is bottom-third for Set G on 11/19 subjects, top-third on 2** —
  the head-to-head seed is unfavourable to Set G, not favourable, so the disclosed
  "Set N dominated by Set G" result is not a seed cherry-pick.

**Reconciliation finding:** the older pilot's *reimplemented* Set G
(`../results/{gcd,sin}/pilot_stats.json`) disagrees with GenMorph's published values
(gcd 17 vs 11; sin 2 vs **16** — the sin direction flips). Use published Set G; the
old reimplemented Set G is superseded.

Full protocol, environment, and the remaining paired Set-N multiseed step:
see `docs/review_2026-06-20/mvp_s5_aligned_multiseed_runbook.md`.
