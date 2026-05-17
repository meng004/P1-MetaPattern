# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-05-17

Initial public release: IMRaD-restructured paper + reference implementation + 9 supplementary directories.

### Added
- **IMRaD restructure** (Phases B-D of `docs/restructure/phase_*_complete.md`): consolidated theory into §3 (NOETHER framework, 22 pp) and experiment into §4 (Empirical evaluation, 26 pp). Original 9-section layout (§1 Intro / §2 Related / §3-§4 Theory / §5-§6 Instantiations / §7 Empirical / §8 Discussion / §9 Conclusion) consolidated into IMRaD layout (§1 Intro / §2 Related / §3 Framework / §4 Empirical / §5 Threats / §6 Conclusion).
- **Tier 2 prose compressions** (7 items, ~130 lines): §5 Construct validity (LRCA κ detail → Supp S3); §5 External validity (Commons Math pilot detail → Supp S4); tab:elementwise 12→7 MRs (full 12 → Supp S2); §4.5 cost section (methodology → Supp S4); §5.2 K-sweep + Tolerance derivations; §4.7 PMCM Case A-bis (Murphy 6-class itemize → Supp S9); §4.6 METRIC+ sorting worked-example caption.
- **3 new supplementary files**: `supplementary/S2_pwr_corpus/elementwise_12.md` (full 12-MR enumeration with per-block sub-category coverage), `supplementary/S4_reproducibility/cost_breakdown.md` (cost methodology including token-cost protocol and per-SUT human-effort breakdown), `supplementary/S9_migrated_appendices/pmcm_case_abis_full.md` (Murphy 6-class full per-class decoding).
- **§9 archival files** (this release): `REPRODUCTION.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `RELEASE_CHECKLIST.md`, `DATASET.md`, `CITATION.cff`, `requirements.txt`, `requirements-frozen.txt`, `pyproject.toml`, `.env.example`.
- **arXiv variant** (`NOETHER_paper_arxiv.tex` + `arxiv/`): named author block (Meng Li, USC) suitable for arXiv preprint posting; double-blind variant `NOETHER_paper.tex` retained for ACM TOSEM submission.

### Changed
- **Length**: 75 pp (cover-letter declared) → 73 pp (Tier 1 compression) → 73 pp (IMRaD restructure) → 71 pp (Tier 2 compressions); cover letter synced to 71 pp.
- **Cover letter** (`docs/submission/cover_letter.md`): structural breakdown table updated to reflect IMRaD sections; length declaration synced; companion-artefact list updated to include three new supplementary files.
- **Bibliography**: 56 cited keys, 58 defined entries; 2 reactor-physics textbook entries (Stacey 2007, Lamarsh & Baratta 2001) verified to be cited via `\cite[\S...]{}` bracket form (audit regex required updating).
- **Humanizer pass**: 3 minor AI-style fixes — `underscoring the gap` → `which exposes the gap` (L243); `Cross-corroboration via` → `Cross-corroboration from` (L696, L808).

### Verified
- xelatex compile clean: 71 pages, 0 undefined references, 0 undefined citations, 0 multiply-defined labels, 0 em-dashes (U+2014).
- 论点-preservation audit: all 7 论点 (C1, C2a, C2b, C3, C4, H_L*, H_MP) + 10 reserved phrases + 11 key data snapshots verified against pre-restructure baseline (1:1 correspondence).
- 5-perspective re-review (EIC + Methodology + Domain + Perspective + Devil's Advocate): 0 CRITICAL, 1 MAJOR (length over TOSEM ceiling — already disclosed in cover letter), 5 cosmetic MINOR. Editorial decision: Minor revision conditional Accept (Accept if EIC grants foundational-paper exception).
- Humanizer scan: 0 em-dashes, 0 throat-clearing intros, 0 version-narrative leaks, 0 multi-hedge stacks; only minor AI-cliché tells fixed.
- Bib audit (cited vs defined): 0 undefined, 0 unsatisfied; 2 textbook entries verified to be cited via `\cite[\S...]{}` bracket form.

### Repository structure (post-§9 archival)
- Top-level: `README.md`, `REPRODUCTION.md`, `DATASET.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `RELEASE_CHECKLIST.md`, `LICENSE`, `CITATION.cff`, `requirements.txt`, `requirements-frozen.txt`, `pyproject.toml`, `.gitignore`, `.env.example`.
- Paper sources: `NOETHER_paper.tex` (TOSEM double-blind), `NOETHER_paper_arxiv.tex` (arXiv named), `NOETHER_paper.bib`, `NOETHER_paper.pdf`, `NOETHER_paper_arxiv.pdf`.
- `arxiv/`: dedicated arXiv build harness (script + README + source copy).
- `supplementary/`: S1 (CONSTRUCT-MP reference impl), S2 (84-MR PWR corpus + 12-MR enumeration), S3 (SE(3) case study), S4 (reproducibility + cost methodology + future-work tracker), S5 (GenMorph pilot), S6 (RDB algebra breakdown), S7 (D4J algebra-rich subset), S8 (METRIC+ Sun 2021 cross-tool replication), S9 (migrated appendices).
- `docs/`: `restructure/` (phase B-D reports + argument preservation + key data snapshot + section mapping), `review_round_*/`, `submission/` (cover letter), `superpowers/`.
- `scripts/`: `imrad_restructure.py` (reproducible block-level rewrite).
- `archive/`: historical intermediate files.

## Release-history note

Prior round-by-round revision history (pre-public-release) is preserved in `docs/restructure/phase_*_complete.md`. The phase reports cover IMRaD restructure (Phase B), Tier 2 compression (Phase C), and cover-letter synchronisation + verification (Phase D). The previous review history (rounds 1-4, ARS R2 reviewer, polish rounds) lives in `docs/review_round_*/`. None of this material is required to interpret the published paper or replicate its results; it is retained as a lineage record.
