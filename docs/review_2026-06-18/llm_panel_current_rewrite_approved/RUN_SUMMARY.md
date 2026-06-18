# Current Rewrite External LLM Panel Run Summary

Date: 2026-06-18

Manuscript: `NOETHER_paper_arxiv.tex`

Command:

```bash
rtk .venv-noether/bin/python scripts/llm_reviewer_panel.py --manuscript NOETHER_paper_arxiv.tex --out docs/review_2026-06-18/llm_panel_current_rewrite_approved
```

Kimi retry command:

```bash
rtk .venv-noether/bin/python scripts/llm_reviewer_panel.py --manuscript NOETHER_paper_arxiv.tex --out docs/review_2026-06-18/llm_panel_current_rewrite_approved_kimi_retry --models kimi-k2-instruct
```

## Gateway Status

- Main panel: 4/5 successful.
- `Kimi-K2-Instruct` failed in the main panel with gateway 503: no available distributor/channel.
- Retry with lowercase `kimi-k2-instruct`: successful, but the script did not auto-parse JSON. The fenced JSON in the Markdown report was manually read for this summary.

## Structured Decisions

| Model | Status | Recommendation | Confidence | Soundness | Novelty | Significance | Presentation | Reproducibility |
|---|---|---|---:|---:|---:|---:|---:|---:|
| gpt-5 | ok | Major Revision | 4 | 3 | 4 | 3 | 2 | 2 |
| claude-opus-4-6 | ok | Major Revision | 4 | 2 | 3 | 2 | 1 | 3 |
| deepseek-r1 | ok | Major Revision | 4 | 3 | 5 | 4 | 3 | 4 |
| glm-5.2 | ok | Major Revision | 4 | 3 | 4 | 2 | 2 | 3 |
| kimi-k2-instruct | ok via retry | Major Revision | 2 | 2 | 2 | 2 | 3 | 3 |
| Mean | — | — | 3.6 | 2.6 | 3.6 | 2.6 | 2.2 | 3.0 |

## Consensus

All five available model reports recommend **Major Revision**.

The strongest repeated concerns are:

1. **Theorem 1 / Translate formalization.** Reviewers repeatedly view Theorem 1 as near-tautological because `MR(A_P)` is defined as the `Translate` image, or as under-specified because `Translate`, invariant extraction, equivalence, and complexity bounds lack sufficiently executable formal definitions.
2. **Presentation and length.** Reviewers repeatedly identify excessive length, repeated boundary boxes/caveats, and scattered definitions/results as major barriers to TOSEM readability.
3. **Empirical evidence drift.** Reviewers still read the mutation/head-to-head material as evidence of MR effectiveness, and several note that GenMorph dominates Set N on the D1/pooled fault-detection metrics.
4. **Upstream block decomposition.** Reviewers question whether the eight blocks are reproducible beyond author curation and ask for a clear algebra-distillation protocol and human validation.
5. **Negative result formalization.** Reviewers value the PWR counterexamples but want the boundary proof to be more formal, accessible, and tied to explicit `Translate` limitations.

## Editorial Read

This fresh panel strengthens the previous EIC judgment: the paper has real TOSEM-level originality, especially in operator-algebraic MR identification, IBT, and boundary theory, but it is not yet submission-clean. The highest-ROI revision remains a structural one: reduce the main paper to the MR-identification claim, demote effectiveness-style tables, and make Theorem 1 / `Translate` / block coverage precise enough that reviewers cannot dismiss the theory as definitional.

