# NOETHER TOSEM Fast Impact Submission Package

Built: 2026-06-30

Template: ACM official `acmart-primary.zip`, `acmart` v2.18 (2026-05-31),
downloaded from the ACM/TOSEM template source and cached under
`source/acmart-v2.18/`.

## Primary Review Files

- `review_files/NOETHER_paper_main_submission.pdf` — TOSEM Fast Impact single-blind review manuscript, 45 pages, compiled with ACM `acmart` v2.18.
- `review_files/NOETHER_data_artifact_availability.pdf` — separate single-blind data and artifact availability statement, 2 pages.
- `cover_letter/cover_letter_TOSEM.pdf` — cover letter identifying the TOSEM Fast Impact track, contributions, arXiv/preprint disclosure, overlap statement, COI statement, and generative-AI disclosure.

TOSEM is single-blind. The review manuscript and artifact statement show all authors and affiliations on the first page. Do not replace these PDFs with anonymous versions.

## Reference Files

- `reference_full_pdf/NOETHER_paper_submission.pdf` — full manuscript PDF with references, appendices, and data/artifact material, 61 pages. This file is included for internal/reference use; do not substitute it for the 45-page Fast Impact review manuscript unless the submission system explicitly requests a full combined PDF.

## Source Snapshot

The `source/` directory contains the LaTeX source snapshot used to build the PDFs:

- `NOETHER_paper_main_submission.tex`
- `NOETHER_paper_submission.tex`
- `NOETHER_data_artifact_availability.tex`
- `NOETHER_paper.bib`
- `NOETHER_paper_submission.bbl`
- `NOETHER_paper_main_submission.bbl`
- `acmart.cls`
- `ACM-Reference-Format.bst`
- `acmart-v2.18/acmart.cls`
- `acmart-v2.18/ACM-Reference-Format.bst`
- `acmart-v2.18/acmart-primary.zip`
- `acmart-v2.18/acmart.pdf`
- `acmart-v2.18/acmguide.pdf`
- `figures/`
- `theory/`

Compile from `source/` with:

```sh
pdflatex -interaction=nonstopmode NOETHER_paper_main_submission.tex
pdflatex -interaction=nonstopmode NOETHER_paper_submission.tex
pdflatex -interaction=nonstopmode NOETHER_data_artifact_availability.tex
```

The source root includes `acmart.cls` and `ACM-Reference-Format.bst`, so LaTeX
will load the official v2.18 files before any older system/user TeX-tree copy.

## Supplementary Materials

The non-main supplementary PDF, separated from
`source/NOETHER_paper_submission.pdf`, is:

- `supplementary/NOETHER_supplementary_non_main.pdf` — Data/artifact statement plus appendices migrated out of the Fast Impact main manuscript. This file excludes the main Sections 1--8 and does not repeat the references already included in the review manuscript.

Upload supplementary material separately in Manuscript Central using the system's supplementary-material designation.
