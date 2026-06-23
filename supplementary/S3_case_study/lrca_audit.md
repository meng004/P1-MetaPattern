# LRCA second-rater audit — Set N block labels

Label-Reliability Cross-Audit (LRCA) for the 36 Set N metamorphic-relation
block assignments derived by a single author under CONSTRUCT-MP. Three
large-language-model raters (DeepSeek, ChatGPT, Anthropic Claude Opus)
independently relabel each MR into the eight canonical operator blocks plus an
`orphan` category; the LLM majority is then compared against the author's label.

Raw data in this directory:
- `lrca_llm_labels.json` — per-rater labels and the prompt/JIR/JOR for all 36 MRs.
- `lrca_kappa.json` — computed agreement statistics (source of every number below).

## Agreement (source of truth: `lrca_kappa.json`)

| Comparison | Cohen's kappa | n | Band (Landis-Koch) |
|---|---:|---:|---|
| LLM-majority vs. author (human validation) | **0.931** | 36 | almost perfect |
| Opus vs. author | 0.927 | 34 | almost perfect |
| ChatGPT vs. author | 0.927 | 34 | almost perfect |
| DeepSeek vs. author | 0.929 | 35 | almost perfect |

`n` differs per rater because some rater outputs were not machine-parseable
(n_items = 36; per-rater parseable = 34/34/35). Cross-LLM Fleiss' kappa is not
computed in the released artifact (`fleiss_kappa_across_llms: null`); the
load-bearing figure is the LLM-majority-vs-author Cohen's kappa.

## The two majority-vs-author disagreements (2 of 36)

| Subject | MR | Author label | Majority label |
|---|---|---|---|
| `MathSignalClass exactLog2` | `L_idem_at_one` | `L*` (limit) | `T*` (self-adjoint) |
| `MathSignalClass isSequence` | `B_rel_xor_reverse` | `B*_rel` (relational) | `T*_rev` (time-reversal) |

## Caveat

The three LLM raters share substantial pre-training corpora, so their mutual
consistency is not independent; the majority-vs-author Cohen's kappa provides a
human anchor (the author's labels), but a full independent **human** inter-rater
kappa study is committed as follow-up and is not claimed here. The audit is
reported as corroborative breadth, not as confirmatory verification.

Regenerate: `python experiment/s5/scripts/_lrca_compute_kappa.py` (raw inputs are
`experiment/s5/configs/lrca_llm_labels.json`).
