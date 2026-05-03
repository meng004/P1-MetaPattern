# NOETHER Supplementary Materials — Anonymised Submission Archive

This archive accompanies the manuscript "NOETHER: A Constructive Framework
for Metamorphic Pattern Discovery from Operator Algebras" submitted in
double-blind form. It contains four supplementary items (S1–S4) referenced
from the manuscript at Section 7.4 (Artefact and Supplementary-Material
Availability). All identifying metadata has been stripped.

## Integrity anchor

Current archive SHA-256 (computed over `supplementary/` at submission):

```
dc54d8288205c98e1edd2a96e724cdc9261155990461b1c8efeee2e2db2e77b8
```

(Round-3 anchor `2dad7bcfee29d4d19a7da1210a877143009cd00a33c2f01e4e02b7dd6828b914` superseded by Round-4 with the addition of S3 `runner_pilot.py`, `cat_v_deepcrime.py`, `deepcrime_pilot_results.csv`, `deepcrime_pilot_stats.json`, `deepcrime_pilot_summary.json`, and S2 `independent_citation_provenance.md`.)

Re-compute the hash with:

```
cd supplementary
find . -type f ! -name '.DS_Store' ! -name '*.pyc' ! -path '*/__pycache__/*' -print0 | sort -z | xargs -0 cat | shasum -a 256
```

This hash covers the populated submission archive, including the trained
EGNN checkpoint, MR-set implementations, 20 mutation scripts, runner.py,
analysis.py, and the executed results.csv / table4.json / hypothesis_check.json.
The hash above is the submission anchor; the camera-ready hash will be
re-computed at acceptance after final formatting passes.

## Contents

### S1 — Reference implementation of CONSTRUCT-MP
Path: `S1_construct_mp/`
- `construct_mp.py` — algorithm implementation matching Appendix D
- `boltzmann_instance.py` — Boltzmann instantiation (Section 5)
- `equivariant_instance.py` — equivariant ML instantiation (Section 6)
- `tests/` — unit tests verifying CONSTRUCT-MP step semantics
- `requirements.txt` — Python dependencies

### S2 — 84-MR PWR corpus with NOETHER block annotations
Path: `S2_pwr_corpus/`
- `pwr_84mr_full.csv` — full 84-row table with columns:
  `mr_id, plain_text, source_equation, prior_pattern_p_number,
   noether_block, noether_metapattern, sub_pattern_notes`
- `mapping_protocol.md` — protocol for assigning each MR to a block
  (sources Section 5.3 selection rules into reproducible form)
- `table3_subset.csv` — the 12-row subset reproduced as Table 3 in §5.3,
  with the selection-protocol decision for each row

### S3 — SE(3)-equivariant case-study harness
Path: `S3_case_study/`
- `model/` — frozen e3nn-based SE(3)-Transformer checkpoint and config
- `mr_sets/`
  - `set_N_noether.py` — five MRs derived in §6.3–§6.5
  - `set_L_llm.py` — five MRs from GPT-4 prompt (prompt + raw output in
    `prompt_log.md`)
  - `set_B_literature.py` — five MRs from the metamorphic-testing
    literature
- `mutations/` — 20 mutation scripts categorised i–iv per Section 6.6
- `runner.py` — executes each MR set against each mutation; outputs
  `results.csv` with columns:
  `set, mutation_id, category, detected, runtime_seconds`
- `analysis.py` — produces Table 4 (case study) numbers from `results.csv`

### S4 — Reproducibility manifest
Path: `S4_reproducibility/`
- `seeds.txt` — random seeds used in case study
- `dataset_versions.txt` — dataset and checkpoint version hashes
- `environment.yml` — conda environment specification
- `compute_environment.md` — hardware and software environment used

## Anonymisation status

- All file headers stripped of author names and institutions
- Git history flattened to single commit
- Logs and saved outputs pruned of paths containing user-identifying strings

## Acceptance-stage release plan

At acceptance:
1. Replace anonymised institutional placeholders in `S1_construct_mp/setup.py`
   and other metadata files with canonical citations
2. Deposit the entire archive on Zenodo and record the permanent DOI
3. Anchor the SHA-256 hash and DOI in the camera-ready manuscript at §7.4
4. Replace blinded references "[1]" and "[2]" in §5.3 and §6.3 with
   canonical citations and DOIs
