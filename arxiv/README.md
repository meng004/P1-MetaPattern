# NOETHER — arXiv preprint package

This directory contains the arXiv-ready variant of the manuscript.

## Files

| File | Purpose |
|---|---|
| `NOETHER_paper_arxiv.tex` | LaTeX source (acmart class, `nonacm` option) — author block has placeholders |
| `NOETHER_paper.bib` | Bibliography (53 entries, all cited; identical to project root copy) |
| `build_arxiv.sh` | Build script (xelatex + bibtex + xelatex × 2; audits 0 undef / 0 missing char) |

## Before submitting to arXiv

1. **Fill in author metadata** in `NOETHER_paper_arxiv.tex` (lines ~50–60):

   ```tex
   \author{Your Name}
   \affiliation{%
     \institution{Your University}
     \city{Your City}
     \country{Your Country}
   }
   \email{your.email@example.org}
   ```

   Add additional `\author{...}\affiliation{...}\email{...}` blocks for co-authors.

2. **Build & verify**:

   ```bash
   cd arxiv/
   ./build_arxiv.sh
   ```

   Expected: `NOETHER_paper_arxiv.pdf` produced; 0 undef refs, 0 missing chars.

3. **Bundle the source** for arXiv upload (arXiv accepts `.tar.gz` of source):

   ```bash
   tar czf noether_arxiv_source.tar.gz \
     NOETHER_paper_arxiv.tex NOETHER_paper.bib NOETHER_paper_arxiv.bbl
   ```

   arXiv compiles from source; the `.bbl` is recommended to avoid bibtex
   compatibility issues on arXiv's TeX system.

4. **Suggested arXiv categories**:

   - **Primary**: `cs.SE` (Software Engineering)
   - **Cross-listings**: `cs.LO` (Logic in Computer Science),
     `cs.AI` (if emphasising the equivariant-ML instantiation)

5. **Suggested arXiv abstract**: copy the manuscript abstract verbatim
   (≤ 1920 chars; current word count well within limit).

## What differs from the venue submission variant

| Item | Venue (TOSEM) | arXiv |
|---|---|---|
| Class options | `[acmsmall, screen]` | `[acmsmall, screen, nonacm]` |
| Copyright | `\setcopyright{none}` (anonymised) | `\setcopyright{rightsretained}` |
| `\acmJournal` / `\acmConference` | TOSEM headers | suppressed via `nonacm` option |
| Author block | `[Anonymised for Review]` | placeholders for real author info |
| §7 Artefact subsection | "review-stage anonymised + acceptance-stage public" two-stage release | single-stage public release with SHA-256 anchor |

The manuscript body, theorems, proofs, hypotheses, instantiations, and
bibliography are otherwise identical between the two variants.

## Reproducibility note

The supplementary materials referenced by §7.4 live one directory above
this one, at `<PROJECT_ROOT>/supplementary/`. The SHA-256 content hash
`dc54d8288205c98e1edd2a96e724cdc9261155990461b1c8efeee2e2db2e77b8`
covers that archive.
