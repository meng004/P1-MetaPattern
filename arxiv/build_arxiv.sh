#!/usr/bin/env bash
# Build NOETHER_paper_arxiv.pdf for arXiv submission.
# Run from the arxiv/ directory.
set -euo pipefail

JOB="NOETHER_paper_arxiv"

if ! command -v xelatex >/dev/null 2>&1; then
  echo "ERROR: xelatex not found. Install MacTeX, TeX Live, or use 'tectonic ${JOB}.tex' instead." >&2
  exit 1
fi

xelatex -interaction=nonstopmode "${JOB}.tex"
bibtex "${JOB}"
xelatex -interaction=nonstopmode "${JOB}.tex"
xelatex -interaction=nonstopmode "${JOB}.tex"

# Audit: zero undef refs / cites / missing chars
UNDEF=$(grep -c "undefined" "${JOB}.log" || true)
MISS=$(grep -c "Missing character" "${JOB}.log" || true)
echo "---"
echo "PDF: ${JOB}.pdf ($(wc -c <"${JOB}.pdf") bytes)"
echo "Undefined refs/cites: ${UNDEF}  (target: 0)"
echo "Missing characters:   ${MISS}  (target: 0)"

if [[ "${UNDEF}" != "0" || "${MISS}" != "0" ]]; then
  echo "FAIL: clean compile not achieved." >&2
  exit 2
fi
echo "OK."
