# S3 — SE(3)-Equivariant Case-Study Harness (Section 6.6)

This directory implements the comparative case study reported in
Section 6.6 of the manuscript: NOETHER-derived MR set N vs.
LLM-prompt MR set L vs. literature-baseline MR set B against 20
mutations of an SE(3)-equivariant point-cloud classifier.

## Status

| Component | Status |
|---|---|
| MR set N (5 NOETHER MRs, 1 per non-empty block of $\mathcal{A}_{\mathrm{equi}}$) | ✓ implemented + executable |
| MR set L (LLM-prompt baseline, 5 MRs) | ✓ generated via `gpt-4-turbo-2024-04-09` on 2026-05-15 (UTC), temperature=0.0, seed=4246; raw output in `mr_sets/prompt_log.md`; callables in `mr_sets/set_L_llm.py` |
| MR set B (literature baseline, 5 MRs from Murphy/Xie/Segura/Shin) | ✓ implemented + executable |
| 20 mutations across 4 categories (i/ii/iii/iv) | ✓ implemented; 8/20 adapted from P2 mutation operators |
| Stub model (CPU-only, no torch/e3nn dependency) | ✓ end-to-end pipeline runnable |
| Real model (e3nn SE(3)-Transformer on ModelNet10) | ✗ checkpoint to be trained by authors before camera-ready |
| `runner.py` — execute MR × mutation cross-product | ✓ runnable on stub or real model |
| `analysis.py` — produce Table 4 + verify H1/H2 | ✓ runnable, emits LaTeX + JSON |
| P2 statistical-utilities reuse via shim | ✓ `p2_integration.py` (read-only import; does not modify P2) |

The case study **is fully executable end-to-end on the StubModel today**
and produces a Table 4 demonstrating that H1 and H2 hold *on the stub*.
Once the real e3nn checkpoint is loaded, the same pipeline runs without
modification.

## End-to-end run on StubModel (no GPU, no training)

```bash
cd supplementary/S3_case_study
python3 runner.py --stub --output results_stub.csv
python3 analysis.py results_stub.csv --output-dir .
```

Expected runtime: ~30 seconds. Outputs:

- `results_stub.csv` — 300 rows (15 MRs × 20 mutations)
- `table4.json` — machine-readable Table 4 entries
- `table4.tex` — LaTeX fragment matching §6.6 Table 4 schema
- `hypothesis_check.json` — H1/H2 verdict with supporting numbers

## End-to-end run on real e3nn checkpoint

Once the SE(3)-Transformer is trained (see §"Training the SE(3)-Transformer"
below):

```bash
cd supplementary/S3_case_study
python3 runner.py --checkpoint model/se3_transformer_modelnet10.pt \
                  --output results.csv
python3 analysis.py results.csv --output-dir .
```

The `model_interface.load_model` function currently raises
`NotImplementedError` for non-stub mode — the author wires the e3nn
checkpoint loader once the checkpoint format is fixed. See
`model_interface.py` for the loader stub and contract.

## Reusing P2's statistical utilities

`p2_integration.py` lazily imports the P2 codebase **without modifying
it**. Set the `P2_ROOT` environment variable to the absolute path of
`MT完备性/src` on your machine, e.g.

```bash
export P2_ROOT=/path/to/MT完备性/src
```

If `P2_ROOT` is not set, the module raises a clear `RuntimeError`. The
rest of the §6.6 pipeline (runner.py, analysis.py) does not depend on
this shim and works without it.

```python
from p2_integration import cliffs_delta_from_results
out = cliffs_delta_from_results("results.csv", set_a="N", set_b="L")
print(out)  # {'delta': float, 'ci_lo': float|None, 'ci_hi': float|None}
```

The shim falls back to a local minimal Cliff's δ when the P2 function
signature has drifted; in that case CI is omitted but the point estimate
remains correct.

## Directory layout

```
S3_case_study/
├── README.md                           (this file)
├── runner.py                           Run MR×mutation cross-product
├── analysis.py                         Compute Table 4 + verify H1/H2
├── mr_interface.py                     MR + MRResult + ModelLike protocol
├── model_interface.py                  load_model + StubModel
├── p2_integration.py                   Read-only shim for P2 stats
├── mr_sets/
│   ├── __init__.py
│   ├── set_N_noether.py               5 NOETHER MRs (rho_rot, rho_mono,
│   │                                   rho_train, rho_adj, rho_train_rev)
│   │                                   + auxiliary rho_perm in SET_N_PLUS
│   ├── set_L_llm.py                    5 GPT-4-generated MRs (raw output in prompt_log.md)
│   ├── set_B_literature.py            5 literature MRs
│   └── prompt_log.md                   GPT-4 prompt + raw-output log
├── mutations/
│   ├── __init__.py                     Aggregates ALL_MUTATIONS (=20)
│   ├── _base.py                        Mutation dataclass
│   ├── manifest.json                   Mutation metadata + P2 attribution
│   ├── cat_i_wrong_sign_loss.py        Cat (i) × 5 (4 adapted from P2 CE)
│   ├── cat_ii_equivariance_break.py    Cat (ii) × 5 (new)
│   ├── cat_iii_precision.py            Cat (iii) × 5 (3 adapted from P2 HP)
│   └── cat_iv_gradient_reversal.py     Cat (iv) × 5 (new)
├── results_stub.csv                    Latest stub-mode output (regenerated)
├── table4.json                         Latest Table 4 (regenerated)
├── table4.tex                          Latest LaTeX fragment (regenerated)
└── hypothesis_check.json               Latest H1/H2 verdict (regenerated)
```

## Pre-registered hypotheses

The case study commits in advance to two falsifiable hypotheses
(§6.6 manuscript):

- **H1 (coverage):** $\mathrm{coverage}_{\mathrm{NOETHER}}(N) = 1.0$ ;
  $\mathrm{coverage}_{\mathrm{NOETHER}}(L)$ and $\mathrm{coverage}_{\mathrm{NOETHER}}(B)$ are strictly < 1.0.
- **H2 (unique detection):** Set N has at least one cat-(iv) mutation
  it uniquely detects, via $\rho_{\mathrm{train\text{-}rev}}$.

`analysis.py` reports the verdict in `hypothesis_check.json`. On the
StubModel, both H1 and H2 hold:

```
H1: HOLDS  (cov N=1.00, L=0.40, B=0.20)
H2: HOLDS  (N uniquely detects 4 of 5 cat-iv mutations via rho_train_rev;
            L and B detect 0 cat-iv mutations)
```

## Training the SE(3)-Transformer (≈ 0.5-1 day)

1. `pip install e3nn==0.5.1 torch==2.4` (matches `S4_reproducibility/environment.yml`)
2. Clone <https://github.com/e3nn/e3nn> reference recipe for ModelNet10
3. Train to baseline accuracy (~30 epochs on 1×A100 ≈ 30 min)
4. Save checkpoint as `model/se3_transformer_modelnet10.pt`
5. Wire `load_model()` in `model_interface.py` to load the checkpoint
   format (the placeholder raises NotImplementedError until then)

Expected post-real-model differences from stub-mode results:

- Cat (i) detection rate by Set N may rise from 0 → 3-5 (real
  classification head's sign matters for the `predict()` output, unlike
  StubModel's softmax-saturation behaviour on a small head).
- Cat (iii) detection rate by all sets may rise as fp16/quantisation
  affects features more strongly than the StubModel's 6-dim head.
- Cat (ii) and (iv) detection patterns by Set N should remain
  qualitatively identical (these are the structural-coverage cases
  Theorem 1 predicts).

## Regenerating Set L from the GPT-4 prompt

Set L was generated against `gpt-4-turbo-2024-04-09` on 2026-05-15
(UTC). The raw JSON output is recorded verbatim in
`mr_sets/prompt_log.md` and translated to Python callables in
`mr_sets/set_L_llm.py`. To regenerate (e.g. if the LLM is updated or
the prompt is revised):

1. Restore the `[TO BE FILLED at experiment time]` sentinels in
   `mr_sets/prompt_log.md` (or use `git checkout` to revert).
2. Set `OPENAI_API_KEY` (or `CHATGPT_API_KEY`) and optionally
   `OPENAI_BASE_URL` / `CHATGPT_BASE_URL` in the environment.
3. Run `python mr_sets/run_gpt4_prompt.py` — it sends the same
   prompt at temperature=0.0, seed=4246, and updates `prompt_log.md`
   in place.
4. Translate each of the 5 returned MR specs into Python callables
   in `set_L_llm.py` (or accept the current translations if the
   output is unchanged from 2026-05-15).
5. Re-run `runner.py` and `analysis.py`.

## Troubleshooting

- **"WARNING: mutation … did not change model fingerprint"**: expected
  for cat (iv) mutations (these change `sgd_step`, not `predict`); for
  cat (i)/(iii) it indicates the mutation is too weak — investigate.
- **`load_model` raises NotImplementedError**: pass `--stub` to use
  StubModel until the e3nn checkpoint loader is wired.
- **`p2_integration` raises RuntimeError**: set `P2_ROOT=/path/to/MT完备性/src`
  or omit the integration (analysis.py works without it).
