# NOETHER TOSEM Fast Impact Submission Package

Built: 2026-06-27

## Primary Review Files

- `review_files/NOETHER_paper_main_submission.pdf` — anonymous TOSEM Fast Impact review manuscript, 45 pages, compiled with `acmart` v2.18.
- `review_files/NOETHER_data_artifact_availability.pdf` — separate data and artifact availability statement, 1 page.
- `cover_letter/cover_letter_TOSEM.pdf` — cover letter identifying the TOSEM Fast Impact track, contributions, preprint disclosure, overlap statement, COI statement, and generative-AI disclosure.

## Reference Files

- `reference_full_pdf/NOETHER_paper_submission.pdf` — full manuscript PDF with references, appendices, and data/artifact material, 60 pages. This file is included for internal/reference use; do not substitute it for the 45-page Fast Impact review manuscript unless the submission system explicitly requests a full combined PDF.

## Source Snapshot

The `source/` directory contains the LaTeX source snapshot used to build the PDFs:

- `NOETHER_paper_main_submission.tex`
- `NOETHER_paper_submission.tex`
- `NOETHER_data_artifact_availability.tex`
- `NOETHER_paper.bib`
- `NOETHER_paper_submission.bbl`
- `NOETHER_paper_main_submission.bbl`
- `acmart-v2.18/acmart.cls`
- `acmart-v2.18/ACM-Reference-Format.bst`
- `figures/`
- `theory/`

Compile from `source/` with:

```sh
TEXINPUTS=./acmart-v2.18//: xelatex -interaction=nonstopmode NOETHER_paper_main_submission.tex
TEXINPUTS=./acmart-v2.18//: xelatex -interaction=nonstopmode NOETHER_paper_submission.tex
TEXINPUTS=./acmart-v2.18//: xelatex -interaction=nonstopmode NOETHER_data_artifact_availability.tex
```

## Supplementary Materials

The large S1-S12 supplementary artifact archive is packaged separately as:

- `../NOETHER_supplementary_S1-S12_2026-06-27_artifact.zip`

Upload supplementary material separately in Manuscript Central using the system's supplementary/anonymous artifact designation.
