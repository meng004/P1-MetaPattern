# Reproduction guide

Step-by-step instructions for reproducing the NOETHER manuscript's
theoretical artefacts (S1 unit tests, §5 Boltzmann mapping) and
empirical results (§6 SE(3)-equivariant case study, §6.6.1 DeepCrime
pilot).

This guide assumes a Unix-like environment (macOS or Linux). Windows
users can adapt the shell commands or use WSL.

---

## 0. Prerequisites

| Tool | Version | Notes |
|---|---|---|
| Python | 3.11.x | Earlier Python ≥ 3.10 may also work |
| conda or mamba | any recent | For the `environment.yml` workflow |
| TeX Live | 2024+ (full preferred) | For rebuilding the PDF. `2026basic` works but requires extra font packages — see §8 |
| make / git | system default | Optional |

### Hardware

- Apple Silicon (M-series) — the manuscript's actual reproduction
  platform; PyTorch MPS backend
- CUDA host (RTX 30/40-series, A100, etc.) — switch the
  `dependencies:` block in `supplementary/S4_reproducibility/environment.yml`

The S3 case study runner completes in minutes on M1 Pro / 32 GB.

---

## 1. Environment setup

```bash
git clone <THIS_REPO>
cd MR元模式

conda env create -f supplementary/S4_reproducibility/environment.yml
conda activate noether-equivariant
```

For Apple Silicon, optionally enable the PyTorch MPS CPU fallback for
unsupported operations:

```bash
export PYTORCH_ENABLE_MPS_FALLBACK=1
```

---

## 2. CONSTRUCT-MP unit tests (S1)

These verify that the algorithm's step semantics in
`supplementary/S1_construct_mp/construct_mp.py` match the specification
in Appendix D of the manuscript.

```bash
cd supplementary/S1_construct_mp
python -m pytest tests/ -v
```

**Expected**: all unit tests pass.

---

## 3. Boltzmann instantiation (§5)

Reproduces the block-mapping output that informs the 12-row subset of
Table 3 in §5.3. The full 84-MR corpus and per-MR block annotations are
in `supplementary/S2_pwr_corpus/`.

```bash
cd supplementary/S1_construct_mp
python boltzmann_instance.py
```

**Expected**: stdout shows the eight-block mapping (G, O_le, T*, T_rev*,
L*, D*, E*, B*_rel) for the Boltzmann transport algebra, with
non-empty blocks listed.

---

## 4. Equivariant-ML case study (§6, §6.6)

### 4a. Train (or load) the SE(3)-equivariant point-cloud classifier

```bash
cd supplementary/S3_case_study/model
python train.py
```

**Expected**: training logs to `model/training_log.json`; checkpoint
written to `model/se3_classifier.pt` (~50 s on M1 Pro). Skip this step
if the checkpoint is already present.

### 4b. Run the three MR sets against the 20 mutation scripts

```bash
cd supplementary/S3_case_study
python runner.py --mr-set N --output results.csv
python runner.py --mr-set L --append-output results.csv
python runner.py --mr-set B --append-output results.csv
```

**Expected**: `results.csv` populated with one row per (mr_set,
mutation_id, category, detected, runtime_seconds) tuple — 60 rows total
(3 MR sets × 20 mutations).

### 4c. Aggregate to Table 4 numbers

```bash
python analysis.py results.csv --output-dir .
cat table4.json
```

**Expected**: `table4.json` matches the §6.6 numbers reported in the
manuscript.

---

## 5. DeepCrime-style pilot (§6.6.1)

```bash
cd supplementary/S3_case_study
python runner_pilot.py
cat deepcrime_pilot_summary.json
```

**Expected**:

- Set N (NOETHER MRs) detects 2 of 5 cat-v mutations
- Sets L (LLM-prompted) and B (literature) detect 0 of 5

The pilot is reported with $n=5$ per MR set; the manuscript (§6.6.1)
explicitly flags the sample size as insufficient for $\alpha = 0.05$
inferential conclusions and reports the result as descriptive evidence
consistent with the structural prediction.

For the inferential statistics:

```bash
cat deepcrime_pilot_stats.json   # Wilson 95% CIs + Fisher exact p-values
```

**Expected**: Fisher-exact $p = 1.00$ for both Set N vs Set L and Set N
vs Set B contrasts at $n=5$.

---

## 6. P2 statistical-utilities reuse (optional, §6.6 Cliff's δ)

`p2_integration.py` is a read-only import shim for the P2 codebase
(`MT完备性/src`). If you have the P2 source tree, set:

```bash
export P2_ROOT=/path/to/MT完备性/src
```

If `P2_ROOT` is not set, `p2_integration.py` raises a clear
`RuntimeError` with the same instructions. The rest of the §6.6
pipeline runs without this shim.

---

## 7. Integrity check (S4)

Verifies the supplementary archive matches the SHA-256 anchor reported
in the manuscript at §7.4.

```bash
cd supplementary
find . -type f ! -name '.DS_Store' ! -name '*.pyc' ! -path '*/__pycache__/*' \
  -print0 | sort -z | xargs -0 cat | shasum -a 256
```

**Expected**:
`dc54d8288205c98e1edd2a96e724cdc9261155990461b1c8efeee2e2db2e77b8`

---

## 8. Manuscript build (optional)

### TOSEM-submission variant

```bash
pdflatex -interaction=nonstopmode NOETHER_paper.tex
bibtex NOETHER_paper
pdflatex -interaction=nonstopmode NOETHER_paper.tex
pdflatex -interaction=nonstopmode NOETHER_paper.tex
```

**Expected**: `NOETHER_paper.pdf` (~840 KB, 40 pages); zero undefined
refs; zero missing characters.

If pdflatex reports missing font errors (`I can't find file 'txsyc'`,
`LinLibertineT-tlf-ot1--base ... not found`, `t1-zi4b-4 ... not found`,
or `LibertinusMath-Regular cannot be found`), your TeX Live install is
missing fonts. The full list of font packages required by this
manuscript:

```bash
# System-wide (requires sudo)
sudo tlmgr install libertine libertinus-otf libertinus-type1 newtx \
                   txfonts fontaxes mweights inconsolata

# OR user-mode (no sudo, installs to ~/Library/texmf)
tlmgr --usermode init-usertree   # first time only
tlmgr --usermode install libertine libertinus-otf libertinus-type1 \
                          newtx txfonts fontaxes mweights inconsolata
```

User-mode installs are scoped to the current user and reversible; system
installs are shared across all users on the machine.

### arXiv preprint variant

See `arxiv/README.md`. Fill in the author block, then:

```bash
cd arxiv && ./build_arxiv.sh
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `runner_pilot.py` reports 0/5 for Set N | Stale `model/se3_classifier.pt` | Delete and rerun §4a |
| Cliff's δ CIs empty | `P2_ROOT` not exported | See §6 |
| `pytest tests/` collects 0 tests | Wrong working directory | Run from `supplementary/S1_construct_mp/`, not the repo root |
| `LibertinusMath-Regular cannot be found` | Minimal TeX Live | See §8 install command |

---

## Provenance

The reported numbers in the manuscript were produced on macOS 14.x,
Apple M1 Pro / 32 GB, Python 3.11, PyTorch 2.4 with the MPS backend.
Random seeds are documented in
`supplementary/S4_reproducibility/seeds.txt`.

If your reproduction differs by more than rounding from the reported
numbers, please open an issue with your platform, seed values, and
output diff.
