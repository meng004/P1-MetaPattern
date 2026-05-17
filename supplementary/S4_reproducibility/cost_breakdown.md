# MR-Generation Cost Components — Full Methodology

Migrated from `NOETHER_paper.tex` §subsec:gen-cost (Tier 2 compression, 2026-05-16). Body retains the cost-component summary table (`tab:gen-cost`) and the H3a.3 verdict paragraph; this file carries the full derivation methodology and per-cost-axis sensitivity analysis.

## Cost components compared

NOETHER's cost profile differs qualitatively from each of the three SOTA-category representatives across four independent components:

1. **Algorithmic time per SUT**: CONSTRUCT-MP's polynomial-time bound under Theorem~2 vs.\ GP search wall-time vs.\ LLM API latency vs.\ mining wall-time after corpus assembly.
2. **Human effort per program family**: operator-algebra distillation vs.\ prompt design vs.\ seed-suite assembly vs.\ none-after-setup.
3. **LLM-token cost (USD)**: only applicable to the LLM-assisted arm.
4. **Seed-corpus dependency**: required for MR-Scout (mining-based); not required for the other three.

## Token-cost derivation methodology

The token-cost estimate for the LLM-assisted arm is derived from a multi-vendor × multi-temperature protocol scale:

- **3 LLMs × 5 samples × ≈ 600 tokens per SUT-prompt-and-output cycle**
- On the $n = 10$ SUT substrate of §subsec:test-design
- Output cost dominates at GPT-4 January 2026 pricing of \$30 per million output tokens
- **Reported as an order-of-magnitude estimate**; chain-of-thought or few-shot prompting raises the estimate by approximately one order of magnitude

## NOETHER human-effort derivation

The NOETHER human-effort estimate of ≈ 10 hours per program family is taken from the experiment notes (`paper_claims_summary.md`) and aggregates:

- Set~N's 30-MR manual derivation across the 10 SUTs of §subsec:test-design
- ≈ 1~h per SUT under CONSTRUCT-MP's four-step procedure
- The per-SUT cost amortises across SUTs that share an operator algebra

## MR-Scout human-effort scope

The MR-Scout human-effort estimate captures **seed-suite assembly only** and excludes downstream MR-cleanup. Full per-step accounting is in `S4_reproducibility/mr_scout_estimate.md`.

## Cost-axis structural advantages (full prose)

The table operationalises three structural advantages of NOETHER as distinct cost-axis arguments rather than as a single "best" verdict:

1. **vs. GP-evolved baselines**: NOETHER replaces a 30-min stochastic search per SUT with a polynomial-time deterministic construction (Theorem~2), with a one-time human cost amortising across SUTs sharing an operator algebra.
2. **vs. LLM-assisted baselines**: NOETHER's $\mathrm{coverage}_{\mathrm{NOETHER}}$ diagnostic on §subsec:case-study (1.00 vs.\ 0.40) operationalises the algebraic-prior gap that prompt-based generation does not close, with the additional property that NOETHER's token-cost is zero (the construction does not invoke an LLM in-loop).
3. **vs. mining-based baselines**: NOETHER is operative at cold start (no seed test suite is required), which is the regime in which most algebra-rich scientific-computing programs arrive on a tester's desk.

None of these advantages is a fault-detection-superiority claim; they are cost-profile and coverage-profile claims that hold within the framework's scope precondition.

## Compression delta (body → supplementary)

| Item | Body (compressed) | This file (full) |
|---|---|---|
| Cost-axis intro paragraph | 1 sentence | 4 components + derivation method |
| Token-cost methodology | 1 reference | Full multi-vendor protocol + GPT-4 pricing |
| Human-effort breakdown | 1 reference | Per-SUT amortisation across same-algebra SUTs |
| MR-Scout scope caveat | --- | Seed-suite assembly only excludes cleanup |
| Three cost-axis args paragraph | Compressed 1 paragraph | Same as body now |
