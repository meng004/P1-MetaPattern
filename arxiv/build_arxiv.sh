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
# Distinguish real ref/cite undefs from cosmetic font-shape warnings.
UNDEF_REF=$(grep -cE "Reference \`.*' on page.*undefined" "${JOB}.log" || true)
UNDEF_CITE=$(grep -cE "Citation .* undefined" "${JOB}.log" || true)
MISS=$(grep -c "Missing character" "${JOB}.log" || true)
FONT_WARN=$(grep -cE "Font shape .* undefined" "${JOB}.log" || true)
echo "---"
echo "PDF: ${JOB}.pdf ($(wc -c <"${JOB}.pdf") bytes)"
echo "Undefined references: ${UNDEF_REF}  (target: 0)"
echo "Undefined citations:  ${UNDEF_CITE}  (target: 0)"
echo "Missing characters:   ${MISS}  (target: 0)"
echo "Font-shape warnings:  ${FONT_WARN}  (cosmetic, non-blocking)"

if [[ "${UNDEF_REF}" != "0" || "${UNDEF_CITE}" != "0" || "${MISS}" != "0" ]]; then
  echo "FAIL: clean compile not achieved." >&2
  exit 2
fi
echo "OK."
