# NOETHER Release Checklist

This checklist must pass before any public release (arXiv, GitHub, Zenodo). The checklist is derived from CLAUDE.md §8 (Release-Prep Policy) and §9 (Post-Paper Archival Policy).

## Pre-release verification (must pass all)

### A. §9 archival completeness

- [x] `README.md` (full 9-section template)
- [x] `REPRODUCTION.md` (system requirements + three-tier replication)
- [x] `DATASET.md` (provenance + version lineage + reverse lookup)
- [x] `CHANGELOG.md` (Keep-a-Changelog format)
- [x] `CONTRIBUTING.md` (scope + workflow + style)
- [x] `RELEASE_CHECKLIST.md` (this file)
- [x] `LICENSE` (MIT for code; CC-BY-4.0 for paper / data noted in DATASET.md)
- [x] `CITATION.cff` (machine-readable, GitHub-renderable)
- [x] `requirements.txt` (runtime, unpinned)
- [x] `requirements-frozen.txt` (pinned, frozen 2026-05-17)
- [x] `pyproject.toml` (package metadata)
- [x] `.gitignore` (§8.7 13-item baseline)
- [x] `.env.example` (placeholder template)

### B. Compile health

- [ ] `xelatex NOETHER_paper.tex` exits 0 (TOSEM double-blind variant, 71 pp)
- [ ] `cd arxiv/ && ./build_arxiv.sh` exits 0 (arXiv named variant, 71 pp)
- [ ] 0 undefined references in both PDFs
- [ ] 0 undefined citations in both PDFs
- [ ] 0 multiply-defined labels in both PDFs
- [ ] 0 em-dashes (U+2014) in both `.tex` sources
- [ ] 0 missing characters in both PDFs

### C. Sensitive-information scan

- [ ] `grep -lE "sk-[A-Za-z0-9]{20,}"` → 0 matches across tracked files
- [ ] `grep -lE "/Users/[^/]+"` → 0 matches in `.tex`, `.bib`, `.md`, `.py`
- [ ] `grep -lE "(api\.bltcy\.ai|company-internal)"` → 0 matches (extend grep list per CLAUDE.md §8.8)
- [ ] No personal email beyond `mlemon@usc.edu.cn` in tracked files
- [ ] `.env` is gitignored and not tracked

### D. Bibliography integrity

- [ ] cited == defined (handle `\cite[\S...]{key}` bracket form)
- [ ] 0 `Anonymous2025` / `[1]` / `[2]` placeholder cite keys
- [ ] All references have at least DOI / arXiv ID / publisher URL where available
- [ ] paper-search MCP audit pass: 0 ✗, ≤ 5 △ (with rationale)

### E. 论点-preservation (post-restructure)

- [ ] All 7 论点 statements verified against `docs/restructure/argument_preservation.md`
- [ ] All 11 key data snapshots verified against `docs/restructure/key_data_snapshot.md`
- [ ] All 10 reserved phrases verbatim-present in the manuscript
- [ ] 18 tables / 1 figure / 2 theorems / 2 propositions all in place
- [ ] Cover letter declared page count matches PDF page count

### F. Smoke replication

- [ ] `cd supplementary/S1_construct_mp && python -m pytest -q test_construct_mp.py` → all pass
- [ ] `python scripts/imrad_restructure.py` is reproducible (idempotent on a clean checkout)

## Per-channel pre-publish gates

### arXiv (cs.SE)

- [ ] `arxiv/NOETHER_paper_arxiv.tex` synced from current root version
- [ ] Author block named (Meng Li, USC, mlemon@usc.edu.cn) — not anonymised
- [ ] `\acmConference` placeholder replaced with arXiv-appropriate header
- [ ] `.bbl` included in tarball (arXiv does not run bibtex reliably)
- [ ] `tar tzf <bundle>.tar.gz` shows: `.tex`, `.bib`, `.bbl`, all custom `.sty` files
- [ ] Abstract ≤ 1920 characters (arXiv form limit; current paper structured-abstract is ~2200 chars and needs condensing for the form)
- [ ] arXiv categories chosen: primary `cs.SE`; cross-listings `cs.LG` (equi-ML), `cs.LO` (Theorem 1' falsification)
- [ ] Endorsement obtained for first-time `cs.SE` submission (if applicable)
- [ ] **User-side action**: confirm endorsement, fill arXiv submission form, upload tar.gz, schedule for the next announce window

### GitHub (public release)

- [ ] `README.md` 9-section template fully populated
- [ ] `meng004` placeholder in `pyproject.toml` + `CITATION.cff` replaced with real GitHub username
- [ ] Repository initialised and pushed to `github.com/meng004/P1-MetaPattern`
- [ ] First tag `v0.1.0-submission` created
- [ ] GitHub Issue templates + PR template added (`.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md`)
- [ ] At minimum a sanity CI workflow added (`.github/workflows/sanity.yml`)
- [ ] **User-side action**: GitHub account / SSH key / push authorisation

### Zenodo (replication archive)

- [ ] `replication/noether-v0.1.0.zip` assembled from `supplementary/` + `scripts/` + key paper files
- [ ] Bundle size ≤ 100 MB (use Zenodo for > 50 MB; GitHub for < 50 MB)
- [ ] Zenodo metadata file `zenodo.json` prepared with title, authors, keywords, license
- [ ] **User-side action**: Zenodo account / login / DOI minting

## Post-publish housekeeping

- [ ] arXiv ID anchored in `CITATION.cff` (`<ARXIV_ID>` placeholder)
- [ ] arXiv ID anchored in `pyproject.toml` URLs
- [ ] arXiv ID anchored in `README.md` Citation section
- [ ] Zenodo DOI anchored in `CITATION.cff` (`doi:` field)
- [ ] Zenodo DOI anchored in `DATASET.md` integrity section
- [ ] Both anchored in `NOETHER_paper.tex` artefact subsection (post-acceptance for TOSEM)
- [ ] Single commit `release-prep: anchor arXiv ID + Zenodo DOI`
- [ ] PDF rebuild with anchored IDs; re-upload arXiv v2 if needed

## Sign-off

| Stage | Date | Sign-off |
|---|---|---|
| §9 archival complete | 2026-05-17 | (this release) |
| arXiv upload | _pending user action_ | |
| GitHub push | _pending user action_ | |
| Zenodo upload | _pending user action_ | |
| Post-publish anchoring | _pending arXiv ID + DOI_ | |
