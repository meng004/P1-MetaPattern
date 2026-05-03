# Next steps

This document tracks open follow-up work after the initial GitHub
commit. Each item is independent and can be done in any order.

---

## A. arXiv preprint upload (when ready to publish)

Status: `arxiv/` directory contains a preprint-ready variant. Author
metadata is left as placeholders so the manuscript stays anonymous in
the repository until the user is ready to de-anonymise.

**Steps**:

1. Open `arxiv/NOETHER_paper_arxiv.tex` and replace the three
   placeholders with actual author information:

   ```tex
   \author{<AUTHOR_NAME>}
   \affiliation{%
     \institution{<INSTITUTION>}
     \city{<CITY>}
     \country{<COUNTRY>}
   }
   \email{<your_corresponding_email>}
   ```

   Add additional `\author{...}\affiliation{...}\email{...}` blocks per
   co-author if applicable.

2. Build & verify:

   ```bash
   cd arxiv && ./build_arxiv.sh
   ```

   Expected: `NOETHER_paper_arxiv.pdf` produced; 0 undef refs;
   0 missing characters.

3. Bundle source for arXiv upload:

   ```bash
   cd arxiv
   tar czf noether_arxiv_source.tar.gz \
     NOETHER_paper_arxiv.tex NOETHER_paper.bib NOETHER_paper_arxiv.bbl
   ```

4. Upload at <https://arxiv.org/submit>. Suggested categories:
   primary `cs.SE`, cross-list `cs.LO` and (optionally) `cs.AI`.

5. After arXiv assigns a DOI, update the citation block in `README.md`
   and add the arXiv ID to the `Citing this work` section.

---

## B. Bibliography polish (78 bibtex warnings)

Status: paper builds cleanly (0 undef refs, 0 missing chars). The 78
bibtex warnings are all "missing publisher / address / page numbers"
on conference and journal entries. They do not affect rendering but
are flagged by some venues' submission systems.

**Steps**:

```bash
# List all warnings to see which entries need polishing
bibtex NOETHER_paper 2>&1 | grep "Warning--" | sort -u | head -40
```

For each entry: open `NOETHER_paper.bib`, fill in the missing field
(publisher / address / pages / numpages) from the canonical source.
Re-run the pdflatex chain to verify warnings drop.

Lower priority — not a publication blocker.

---

## C. Reference verification audit (CLAUDE.md §3 步骤 2 + D1)

Status: not run for the current bib state. CLAUDE.md mandates a
paper-search-mcp-driven audit before submission.

**Steps**:

1. Parse `NOETHER_paper.bib` into a checklist (53 entries).
2. For each entry, route through:
   - `mcp__paper-search__get_crossref_paper_by_doi` if DOI present
   - `mcp__paper-search__search_crossref` (title + first author)
   - `mcp__paper-search__search_arxiv` for preprints
   - `mcp__paper-search__search_dblp` for SE / top-tier conference
   - `mcp__paper-search__search_openalex` / `search_semantic` /
     `search_google_scholar` as fallback
   - `WebFetch` for textbooks / standards / GitHub repos

3. Output `docs/review_round{N}/reference_verification.md` with
   ✓ / △ / ✗ per row.

4. Pass gate: ✗ = 0; △ ≤ 5 with explanation.

Required before any real venue submission (TOSEM, IST, etc.). Not
required before arXiv upload (arXiv does not enforce reference
verification).

---

## D. P-series follow-up

The repository is part of a `P1`–`P5` programme of papers (see
`CLAUDE.md` §5). NOETHER corresponds to P4 (formal theory). Adjacent
work threads, not started here, include:

- **P3** — industrial Java / C++ port + LRCA (two-rater κ)
- **P5 / P2-CN** — regulatory translation (IEC 60880, ISO 26262,
  DO-178C); Chinese version under review

These are independent of the GitHub release of P4 / NOETHER and live
in their own repositories or sibling project directories.

---

## E. PDF rebuild after future `.tex` edits

The current PDF is up to date with `NOETHER_paper.tex`. Future edits
require re-running the chain:

```bash
pdflatex -interaction=nonstopmode NOETHER_paper.tex
bibtex NOETHER_paper
pdflatex -interaction=nonstopmode NOETHER_paper.tex
pdflatex -interaction=nonstopmode NOETHER_paper.tex
```

Verification:

```bash
echo "Undef:  $(grep -cE 'Reference.*undefined|Citation.*undefined' NOETHER_paper.log)"
echo "MissCh: $(grep -c 'Missing character' NOETHER_paper.log)"
echo "Pages:  $(pdfinfo NOETHER_paper.pdf | grep ^Pages | awk '{print $2}')"
```

Expected: Undef 0, MissCh 0, Pages 40.

If TeX Live is missing fonts, see `REPRODUCTION.md` §8.
