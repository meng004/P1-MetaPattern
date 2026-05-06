# S6 Pilot Run Comparison

Two configurations have been run against the QED-Calcite plan-JSON corpus.
Both used identical oracles (`set_n_oracle.py`, `set_segura_oracle.py`) and
identical adapter (`qed_adapter.py`); they differ only in sample size and
random seed.

## Summary table

| Metric                                  | run_50pair_seed11 | run_full444_seed22 |
|-----------------------------------------|-------------------|--------------------|
| n pairs                                 | 50                | 444                |
| Stratification (easy/medium/hard)       | 20 / 20 / 10      | 195 / 184 / 65     |
| Seed                                    | 11                | 22 (full census; sampling unused) |
| **Set N**                               |                   |                    |
| applicable                              | 7                 | 50                 |
| detected                                | 6                 | 34                 |
| rate_overall                            | 12.0%             | 7.66%              |
| rate_when_applicable                    | **85.7%**         | **68.0%**          |
| Wilson 95% CI (overall)                 | [5.6, 23.8]%      | [5.5, 10.5]%       |
| **Set Segura**                          |                   |                    |
| applicable                              | 18                | 139                |
| detected                                | 2                 | 19                 |
| rate_overall                            | 4.0%              | 4.28%              |
| rate_when_applicable                    | **11.1%**         | **13.7%**          |
| Wilson 95% CI (overall)                 | [1.1, 13.5]%      | [2.8, 6.6]%        |
| **Union (N ∪ Segura)**                  |                   |                    |
| detected                                | 7                 | 45                 |
| rate                                    | 14.0%             | 10.1%              |
| **Complementary value**                 |                   |                    |
| both                                    | 1                 | 8                  |
| n_only                                  | 5                 | 26                 |
| segura_only                             | 1                 | 11                 |
| neither                                 | 43                | 399                |
| McNemar exact p (n vs segura)           | 0.219             | **0.0201**         |
| Fisher exact p (n vs segura)            | 0.269             | **0.0464**         |
| **By complexity (set_n_rate)**          |                   |                    |
| easy                                    | 0%                | 0%                 |
| medium                                  | 20%               | 13.6%              |
| hard                                    | 20%               | 13.9%              |

## Key observations

### 1. Set N's precision-when-applicable is robustly above Set Segura's

- 50-pair seed-11 sample: Set N **85.7%** vs Set Segura **11.1%** (8× gap).
- Full 444-pair census: Set N **68.0%** vs Set Segura **13.7%** (5× gap).

The smaller sample over-stated Set N's precision (chance composition) but
the qualitative direction is preserved on the full corpus.

### 2. Statistical significance materialises on the full corpus

- 50-pair: McNemar p = 0.22, Fisher p = 0.27 — underpowered, no significance.
- 444-pair: **McNemar p = 0.020, Fisher p = 0.046** — both significant at
  α = 0.05.

The Set N vs Set Segura difference in detection counts (34 vs 19) on 444
pairs is statistically significant; on 50 pairs (6 vs 2) it was not.

### 3. Complementary value scales

- 50-pair: 5 N-only + 1 Segura-only (≥1 each, claim supported but small).
- 444-pair: **26 N-only + 11 Segura-only** — both substantial. The §6.7
  "complementary, not duplicative" claim is supported by 37 disjoint
  detections on the full corpus.

### 4. Overall coverage stays low (~10%)

The QED-Calcite corpus contains 50+ rule families (aggregate-merge, distinct
rules, predicate coercion, semi-join derivation, etc.). Our two NOETHER
MRs (`ρ_select_push`, `ρ_distinct_idem`) and three Segura MRs cover only
a fraction. The structurally meaningful figure is *rate_when_applicable*,
not *rate_overall*.

### 5. Easy pairs are dominated by patterns out of both sets' range

- All "easy" (< 8 nodes) pairs have set_n_rate = 0% on both runs.
- Detection concentrates in medium and hard pairs (where filter/join/
  distinct/limit structures appear).

## Recommendation for the paper

Use the **full 444-pair seed-22 run** in §6.7 — it has the statistical
power to support the comparison claim. The 50-pair seed-11 run remains
in `archive/run_50pair_seed11/` as a sensitivity check / smoke
verification record.

## Reproducibility

Both runs are deterministic given:

- QED commit at `/tmp/calcite_pilot/QED/` (44 4 .json files in tests/calcite/)
- Python environment per `requirements.txt`
- Seed (11 or 22) — for the 50-pair run only; the 444-pair run is a full
  census and the seed is recorded for traceability but not used for
  sampling.

Re-execution:

```bash
# 50-pair sample
python3 sample_pairs.py --qed-path /tmp/calcite_pilot/QED \
    --counts 20,20,10 --seed 11 --output pairs_sample.json
python3 run_pilot.py --qed-path /tmp/calcite_pilot/QED \
    --pairs-sample pairs_sample.json --seed 11 \
    --output results/results.csv
python3 stats.py --results results/results.csv \
    --output results/pilot_stats.json

# Full 444 corpus
python3 run_pilot.py --qed-path /tmp/calcite_pilot/QED \
    --pairs-sample pairs_sample_full.json --seed 22 \
    --output results_full/results.csv
python3 stats.py --results results_full/results.csv \
    --output results_full/pilot_stats.json \
    --label "Calcite_QED_full444_seed22"
```
