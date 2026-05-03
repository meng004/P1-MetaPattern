# NOETHER

**A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras**

This repository accompanies the paper *NOETHER: A Constructive Framework
for Metamorphic Pattern Discovery from Operator Algebras*. It contains
the LaTeX source of the manuscript, an arXiv-ready preprint variant, a
Python reference implementation of the **CONSTRUCT-MP** algorithm, the
84-MR PWR corpus, an SE(3)-equivariant point-cloud testing harness, and
a reproducibility manifest.

---

## Motivation

Metamorphic Testing (MT) is recognised in IEEE/ISO software-testing
standards and is widely recommended for testing AI systems. Its
progress, however, remains constrained by **metamorphic relation (MR)
identification** — a step that depends heavily on tester domain
knowledge and yields MR sets that are difficult to reuse across teams
and across program families.

Existing approaches share an inductive grounding that leaves three
foundational questions open:

1. **Origin** — where do MetaPattern categories come from?
2. **Closure** — is a given MetaPattern set closed under reasonable
   composition operators, or are recurrent MR families silently
   missing?
3. **Transferability** — can the same construction mechanism be applied
   to a new program family without re-doing the inductive work?

Structured frameworks (METRIC, METRIC+), mining and evolutionary
pipelines (MR-Scout, GenMorph), LLM-assisted methods, and the original
MetaPattern catalogues each answer one of these questions while leaving
the other two open. NOETHER addresses all three by relocating induction
from MR samples to *recurrent algebraic structures*, then making the
downstream construction mechanical.

---

## Core contributions

The framework is **two-layer**:

### Downstream layer (mechanical, provable)

Given an operator-algebra block decomposition of a program family $P$,
the **CONSTRUCT-MP** algorithm produces a MetaPattern set with:

- **Theorem 1** — algebraic closure of the constructed MetaPattern set
  under the framework's `Translate` operator, within the algebra-induced
  MR space. Absolute completeness over arbitrary properties is
  identified as an open conjecture (Theorem 1$'$).
- **Theorem 2** — polynomial-time decidability of the construction
  under a finite generating set.

### Upstream layer (curated, explicit empirical hypothesis)

An eight-block decomposition over recurrent mathematical structures
common to many program families, stated as **Hypothesis 1** with a
documented out-of-scope catalogue rather than as an axiom:

| Block | Mathematical structure |
|---|---|
| $\mathcal{G}^*$ | Symmetry / group action |
| $\mathcal{O}_{\le}^*$ | Order / monotonicity |
| $\mathcal{T}^*$ | Self-adjoint duality |
| $\mathcal{T}_{\mathrm{rev}}^*$ | Time-reversal |
| $\mathcal{L}^*$ | Limit / convergence |
| $\mathcal{D}^*$ | Qualitative dynamics |
| $\mathcal{E}^*$ | Method-comparison equivalence |
| $\mathcal{B}_{\mathrm{rel}}^*$ | Relational equivalence |

A `Remark` enumerates six program-family classes likely to require
additional blocks beyond Hypothesis 1; these are explicitly
out-of-scope for the present work.

### Three instantiations

- **Boltzmann reactor-physics transport solver** — the framework
  systematises a prior 84-MR inductive PWR catalogue and re-classifies
  further equivalence classes.
- **Equivariant machine learning** — executable MRs are derived for
  rotation invariance, adjoint duality, and training-trajectory
  reversibility; a §6.6.1 DeepCrime-style pilot evaluates structural
  coverage on five mutation classes.
- **Relational query optimisers** — the idempotent-semiring algebra
  exercises the relational-equivalence block, $\mathcal{B}_{\mathrm{rel}}^*$.

Structural-coverage predictions hold across the three instantiations.
Comparative evaluation against existing automated pipelines is
reported as a *pre-registered protocol* rather than a claim of
average superiority — the §6.6.1 pilot's sample size is insufficient
for $\alpha = 0.05$ inferential conclusions and is reported as
descriptive evidence consistent with the structural prediction.

---

## Repository layout

```
.
├── README.md                    # This file
├── REPRODUCTION.md              # Step-by-step replication guide
├── LICENSE                      # CC-BY 4.0 (manuscript) / MIT (code)
├── .gitignore
│
├── NOETHER_paper.tex            # Manuscript source (TOSEM submission variant)
├── NOETHER_paper.bib            # Bibliography (53 entries, all cited)
├── NOETHER_paper.pdf            # Compiled manuscript
│
├── arxiv/                       # arXiv preprint variant (de-anonymised)
│   ├── NOETHER_paper_arxiv.tex
│   ├── NOETHER_paper.bib
│   ├── build_arxiv.sh
│   └── README.md
│
├── supplementary/               # S1-S4 reproducibility archive
│   ├── README.md
│   ├── S1_construct_mp/         # Python reference implementation
│   ├── S2_pwr_corpus/           # 84-MR PWR corpus (CSV + protocol)
│   ├── S3_case_study/           # SE(3)-equivariant harness
│   └── S4_reproducibility/      # Seeds, env, dataset hashes
│
├── docs/                        # Planning notes (gitignored locally)
├── archive/                     # Process history (not for active use)
│   ├── process-history/         # Earlier drafts, review reports, response letters
│   └── pre-noether-research/    # Parallel-research markdown predating NOETHER
└── 已有论文/                     # Reference reading (PDFs, not redistributed)
```

---

## Reproducing the experimental results

The full step-by-step guide is in [`REPRODUCTION.md`](REPRODUCTION.md).
Quick version:

### 1. Environment

```bash
# Apple Silicon (the manuscript's actual platform — see S4 environment.yml)
conda env create -f supplementary/S4_reproducibility/environment.yml
conda activate noether-equivariant
```

For CUDA hosts, swap the `dependencies:` block as documented in the
`environment.yml` comments.

### 2. CONSTRUCT-MP unit tests (S1)

Verifies that the algorithm's step semantics match the specification in
Appendix D of the manuscript.

```bash
cd supplementary/S1_construct_mp
python -m pytest tests/ -v
```

Expected: all unit tests pass.

### 3. Boltzmann instantiation (§5)

```bash
cd supplementary/S1_construct_mp
python boltzmann_instance.py
```

Reproduces the block-mapping output that informs the 12-row subset of
Table 3 in §5.3. The full 84-MR corpus and the per-MR block annotations
live at `supplementary/S2_pwr_corpus/`.

### 4. Equivariant-ML case study (§6.6)

```bash
cd supplementary/S3_case_study

# (a) Train (or load) the SE(3)-equivariant point-cloud classifier.
#     Skip this if a checkpoint is already present at model/se3_classifier.pt.
python model/train.py

# (b) Run the three MR sets against the 20 mutation scripts.
python runner.py --mr-set N --output results.csv
python runner.py --mr-set L --append-output results.csv
python runner.py --mr-set B --append-output results.csv

# (c) Aggregate to Table 4 numbers.
python analysis.py results.csv --output-dir .
cat table4.json
```

### 5. DeepCrime-style pilot (§6.6.1)

```bash
cd supplementary/S3_case_study
python runner_pilot.py
cat deepcrime_pilot_summary.json
```

The pilot is reported with $n=5$ per MR set; the manuscript explicitly
flags the sample size as insufficient for $\alpha = 0.05$ inferential
conclusions and reports the result as descriptive evidence consistent
with the structural prediction (Set N: 2/5; Sets L, B: 0/5).

### 6. Integrity check

```bash
cd supplementary
find . -type f ! -name '.DS_Store' ! -name '*.pyc' ! -path '*/__pycache__/*' \
  -print0 | sort -z | xargs -0 cat | shasum -a 256
```

Expected output: `dc54d8288205c98e1edd2a96e724cdc9261155990461b1c8efeee2e2db2e77b8`.

---

## Building the manuscript

### TOSEM submission variant (anonymised, root-level `.tex`)

```bash
xelatex -interaction=nonstopmode NOETHER_paper.tex
bibtex NOETHER_paper
xelatex -interaction=nonstopmode NOETHER_paper.tex
xelatex -interaction=nonstopmode NOETHER_paper.tex
```

### arXiv preprint variant

See [`arxiv/README.md`](arxiv/README.md). Fill in the author block,
then:

```bash
cd arxiv && ./build_arxiv.sh
```

---

## Sensitive-information policy

The repository follows a strict no-credentials policy:

- `.env` is `.gitignore`d; only `.env.example` with `your_*_api_key` /
  `your_*_base_url` placeholders is committed.
- No personal absolute paths (`/Users/<name>/...`) appear in any file.
  Use the environment variable `P2_ROOT` to point at the optional P2
  codebase from `supplementary/S3_case_study/p2_integration.py`.
- LaTeX `.log` / `.aux` artefacts are regenerated on each build and are
  also `.gitignore`d.

Pre-commit grep verification:

```bash
grep -rIn -E "(/Users/[^/]+|sk-[A-Za-z0-9]{16,}|Bearer\s+[A-Za-z0-9]+|api_key\s*=\s*['\"][^'\"]{8,})" \
  --exclude-dir=.git --exclude-dir=.venv* --exclude-dir=texmf-dist --exclude-dir=node_modules
# expected: empty output
```

---

## Citing this work

A BibTeX entry will be added once the arXiv DOI is assigned. In the
meantime:

```bibtex
@unpublished{NOETHER2026,
  title  = {{NOETHER}: A Constructive Framework for Metamorphic Pattern
            Discovery from Operator Algebras},
  author = {<AUTHOR_NAME>},
  year   = {2026},
  note   = {Manuscript; arXiv preprint forthcoming}
}
```

---

## License

- **Manuscript and figures** (`NOETHER_paper.*`, `arxiv/*`,
  `supplementary/S2_pwr_corpus/*.csv`, `supplementary/*.md`):
  [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) — please cite
  the paper.
- **Code** (`supplementary/S1_construct_mp/`,
  `supplementary/S3_case_study/`, `supplementary/S4_reproducibility/`,
  `arxiv/build_arxiv.sh`): MIT.

See [`LICENSE`](LICENSE) for the full text.

---

## Contact

Issues and pull requests are welcome on the GitHub repository. For
academic collaboration enquiries, see the corresponding-author email
in the manuscript.
