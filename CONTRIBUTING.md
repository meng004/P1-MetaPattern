# Contributing to NOETHER

Thanks for considering a contribution. NOETHER is a research artefact accompanying a single-author paper; the contribution model is therefore narrower than a typical open-source project. Please read this document before opening an issue or pull request.

## Scope

### Contributions in scope

| Type | Example |
|---|---|
| **Bug reports** | The CONSTRUCT-MP reference implementation produces a wrong block assignment on a specific operator algebra |
| **Replication failures** | The smoke or cache-replay tier fails on a documented platform (Linux + Python 3.10/3.11/3.12, macOS + Apple Silicon, macOS + Intel) |
| **Documentation gaps** | An equation, theorem, or data file referenced from the paper is unclear or undocumented |
| **Operator-algebra instantiations** | A new program family with an operator algebra outside the three instantiated ones (Boltzmann, equivariant ML, relational queries); please open an issue first to discuss whether the algebra fits the eight-block decomposition or requires a candidate ninth block |
| **Negative instances** | A program family where the framework fails to produce a useful MetaPattern set (this is scientifically valuable — see Theorem 1' falsification on $\mathcal{A}_{\mathrm{PWR}}$ for the reference treatment) |

### Contributions out of scope

| Type | Reason |
|---|---|
| Translations of the paper text | The author maintains the canonical English version; translations are welcome as forks but will not be merged |
| Reformatting of the supplementary corpus | The 84-MR PWR corpus and 12-MR elementwise table are research artefacts with curatorial decisions documented in `supplementary/S2_pwr_corpus/elementwise_12.md`; structural changes break paper cross-references |
| Refactors of the IMRaD-structured paper | The paper's section structure is fixed for submission to ACM TOSEM; structural changes belong in a follow-up paper, not in this repository |
| Adoption-outcome claims | The paper explicitly does not claim adoption outcomes on each domain; please do not open issues asserting that a particular team uses or does not use NOETHER |

## Issue workflow

1. **Search existing issues first** — many questions have been raised during review rounds (preserved in `docs/review_round_*/`).
2. **Provide a minimal reproducible example** for bug reports — include the operator algebra specification, the input MR set, and the observed-vs-expected behaviour.
3. **Label appropriately**:
   - `bug` — implementation defect
   - `replication` — failure to reproduce a paper claim
   - `documentation` — paper or `README.md` is unclear
   - `algebra-extension` — request to add a new operator-algebra instantiation
   - `theorem-extension` — request to extend Theorem 1' falsification or the eight-block decomposition

## Pull-request workflow

1. **Open an issue first** for any non-trivial change. PRs without a corresponding issue may be closed without review.
2. **One topic per PR**. Bundled PRs are difficult to review and may be split.
3. **Run the smoke tier** before submitting: `cd supplementary/S1_construct_mp && python -m pytest -q test_construct_mp.py`.
4. **Update `CHANGELOG.md`** under the next-release section.
5. **No reformatting commits mixed with substantive changes**.

## Code style

| Language | Style |
|---|---|
| Python | `ruff` defaults; type hints encouraged (`from __future__ import annotations` + `typing` module); `dataclasses` over plain classes for data containers |
| LaTeX | Sentence-case section titles (per CLAUDE.md); zero em-dashes (U+2014); American or British English consistently within a file |
| Markdown | One sentence per line for prose (helps PR diffs); tables aligned by column |

## Code of conduct

Be respectful. Disagree on the technical substance; do not attack the person. The author reserves the right to close issues or PRs that violate this standard without further engagement.

## Licensing

By contributing code or documentation, you agree that your contribution is released under the same licence as the corresponding artefact: MIT for code, CC-BY-4.0 for paper text and data.

## Author and maintainer

Meng Li, School of Computing, University of South China.
Contact: `mlemon@usc.edu.cn` (please prefix subject with `[NOETHER]`).
