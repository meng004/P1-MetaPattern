# TOSEM submission package — NOETHER

This directory is the **double-anonymous TOSEM submission package**, derived
from the canonical manuscript in `../../manuscript/`. The manuscript is the
single source of truth; this directory is the venue-specific build for ACM
TOSEM (acmart `acmsmall`, double-anonymous review).

## Contents

| File | Purpose |
|---|---|
| `NOETHER_paper_submission.tex` | Submission manuscript. `\documentclass[acmsmall,screen,anonymous,review]{acmart}`. The `anonymous` option hides the author block, ORCIDs, e-mails, and the `acks` block (funding / CRediT / GenAI disclosure / COI) during review. |
| `NOETHER_paper_submission.bib` | Bibliography (75 entries, `ACM-Reference-Format`; all externally verified). |
| `NOETHER_paper_submission.bbl` | Pre-built bibliography (include in upload so the PDF compiles without re-running BibTeX). |
| `NOETHER_paper_submission.pdf` | Compiled review PDF (title page renders "ANONYMOUS AUTHOR(S)"). |
| `theory/ibt_section_3_4.tex` | `\input` dependency (Invariance-Blindness Theorem section). Bundled so the package compiles stand-alone. |
| `cover_letter.md` | Cover letter to the EIC (track, contributions, length, arXiv + companion-paper disclosures). |
| `highlights.md` | Optional highlights (TOSEM does not require them). |
| `templates/` | Official ACM `acmart` 2.18 templates (acmsmall-submission.tex, acmsmall.tex, acmart.pdf, acmguide.pdf) vendored from CTAN, for reference. |

## Build

```bash
cd submissions/TOSEM
xelatex  -interaction=nonstopmode NOETHER_paper_submission.tex
bibtex   NOETHER_paper_submission
xelatex  -interaction=nonstopmode NOETHER_paper_submission.tex
xelatex  -interaction=nonstopmode NOETHER_paper_submission.tex
```

`theory/` is local, so no `TEXINPUTS` override is needed. Expected: ~86 pages,
0 undefined references, 0 missing characters, 0 overfull `\hbox` > 50 pt,
BibTeX "0 didn't find".

## Anonymity

- Author block, ORCIDs, e-mails, affiliations, and the `acks` block are hidden
  automatically by the `anonymous` class option (verify: page 1 reads
  "ANONYMOUS AUTHOR(S)").
- In-text self-references to the authors' prior reactor-physics work are written
  in the third person ("a prior catalogue from the same research line", etc.).
- Self-citations remain in the reference list per ACM double-anonymous policy
  (the policy requires third-person *in-text* citation, not removal).

## Relationship to the canonical manuscript

`../../manuscript/NOETHER_paper_arxiv.tex` is the public (arXiv) version with
real author identities (`\documentclass[manuscript]{acmart}`). This submission
shares the identical body; it differs only in (i) the documentclass options
(anonymous + review), (ii) the withheld arXiv DOI, and (iii) in-text
third-person self-references. To re-derive after a manuscript change, copy the
manuscript `.tex`, re-apply those three deltas, and rebuild.

## Reproducibility

The replication package (data, scripts, PIT mutation traces, aggregation
pipeline) is archived on Zenodo: DOI 10.5281/zenodo.20250634. The supplementary
material referenced as S1–S12 lives under `../../supplementary/` in the source
repository.
