# Two-Paper arXiv + GitHub + Zenodo Submission Guide

**Date**: 2026-05-17
**Scope**: NOETHER (TOSEM target) + P2 semantic-mutation (IST target)
**Strategy**: 3-channel parallel release (arXiv preprint + GitHub repo + Zenodo archival DOI)

---

## 0. Overview

| Channel | Purpose | Identifier produced | Required for what |
|---|---|---|---|
| **arXiv** (cs.SE) | Preprint priority + academic visibility | `arXiv:YYMM.NNNNN` | Cited by other researchers; community visibility |
| **GitHub public** | Code + replication + collaboration | `github.com/meng004/<repo>` | Issue tracking; ongoing maintenance; visible diff history |
| **Zenodo** | Strong archival DOI for the replication package | `10.5281/zenodo.NNNNNN` | Journal §Data Availability citation; long-term archival |

This guide covers both papers in parallel. Where steps differ per paper, both versions are shown side by side.

---

## 1. Pre-release status

### NOETHER (MR元模式)

| Item | Status | Reference |
|---|---|---|
| Manuscript IMRaD restructured | ✓ | `docs/restructure/phase_D_complete.md` |
| 71 pp, 0 undef refs, 0 em-dash | ✓ | compile log `/tmp/d3.log` |
| 论点-preservation verified | ✓ | `docs/restructure/argument_preservation.md` |
| §9 archival (13 files) | ✓ | `RELEASE_CHECKLIST.md` |
| arXiv-named source variant | ✓ | `NOETHER_paper_arxiv.tex` (Meng Li, USC) |
| arXiv metadata | ✓ | `arxiv/arxiv_metadata.md` |
| Cover letter synced (75→71) | ✓ | `docs/submission/cover_letter.md` |

### P2 semantic mutation (语义变异体)

| Item | Status | Reference |
|---|---|---|
| Round-9 IST-ready | ✓ | `docs/STATE.md` |
| 93 pp (review mode), 0 LaTeX warnings | ✓ | `submission/p2_ist_final.{pdf,docx}` |
| 5/5 reviewer consensus Minor → Accept | ✓ | `docs/release_2026-05-03/sanity_check.log` |
| §9 archival (13 files) | ✓ | (incl. just-added CITATION.cff + requirements.txt) |
| Author block named (Meng Li, USC) | ✓ | inline in `submission/p2_ist_final.tex` |
| arXiv metadata | ✓ | `submission/arxiv_metadata.md` |
| §6.5.2 wording pending commit | ⚠ | per `docs/STATE.md:28` |

---

## 2. Release sequence

### Recommended order

```
Day  0:   arXiv upload (both papers)         ← starts priority clock
Day  0-1: arXiv moderation (24h)             ← arXiv ID assigned
Day  1-2: GitHub repos public                ← issue tracking opens
Day  2-3: Zenodo upload (replication.zip)    ← archival DOI minted
Day  3:   Anchor IDs back into manuscripts   ← arXiv v2 + GitHub commit
Day  3+:  Journal submission                 ← TOSEM (NOETHER), IST (P2)
```

### Why this order

1. **arXiv first** locks priority on the contribution date. Per ACM and Elsevier policy, posting a preprint before journal submission is allowed and recommended.
2. **GitHub second** provides the citable `meng004/<repo>` URL that goes into the arXiv comment and the manuscript artefact statement.
3. **Zenodo third** mints an archival DOI for the replication package; this is the strongest citable archive (DOI stable forever).
4. **Journal submission last** uses the now-stable arXiv ID + GitHub URL + Zenodo DOI as the artefact identifiers.

---

## 3. Per-channel action items

### 3.1 arXiv (cs.SE)

| Step | Who | Reference |
|---|---|---|
| 1. Create arXiv account (if first-time) | **User** | https://arxiv.org/user/register |
| 2. Obtain `cs.SE` endorsement (4+ established `cs.SE` authors must endorse) | **User** | Contact prior collaborators with cs.SE arXiv submissions |
| 3. Submit NOETHER first (larger paper, longer review at TOSEM benefits more from arXiv priority) | **User** | Paste fields from `MR元模式/arxiv/arxiv_metadata.md` §1-§7 |
| 4. Upload `noether_arxiv_v1.tar.gz` | **User** | Build with `cd MR元模式/arxiv/ && ./build_arxiv.sh && tar czf ...` |
| 5. Wait 24h for moderation; obtain `arXiv:2605.NNNNN` | arXiv | --- |
| 6. Submit P2 (endorsement already established) | **User** | Paste from `语义变异体/submission/arxiv_metadata.md` |
| 7. Wait 24h for P2 moderation | arXiv | --- |

**Assistant follow-up** (after arXiv IDs assigned): anchor IDs in `CITATION.cff` + `pyproject.toml` + `README.md` for both papers.

### 3.2 GitHub (public release)

| Step | Who | Reference |
|---|---|---|
| 1. Decide GitHub username (or org name) | **User** | --- |
| 2. Create empty public repos: `noether` and `p2-semantic-mutation` | **User** | https://github.com/new |
| 3. Add SSH key to GitHub account | **User** | https://github.com/settings/keys |
| 4. Replace `meng004` placeholder in `pyproject.toml`, `CITATION.cff`, `README.md` (both papers) | Assistant (once user gives username) | --- |
| 5. Initial commit + push | Assistant or user | `git push -u origin main` |
| 6. Tag `v0.1.0-submission` (NOETHER) and `v1.0.0-submission` (P2) | Assistant | --- |
| 7. Optional: Add `.github/ISSUE_TEMPLATE/` + `PULL_REQUEST_TEMPLATE.md` + `workflows/sanity.yml` | Assistant | --- |
| 8. Verify CI green (if workflows added) | --- | --- |

### 3.3 Zenodo

| Step | Who | Reference |
|---|---|---|
| 1. Create Zenodo account (free, ORCID login recommended) | **User** | https://zenodo.org/signup |
| 2. Link GitHub account to Zenodo (auto-archive on Release) | **User** | https://zenodo.org/account/settings/github/ |
| 3. Build `replication.zip` for NOETHER from `supplementary/` + `scripts/` + paper files | Assistant | See §4.1 below |
| 4. Build `replication.zip` for P2 from `data/` + `scripts/` + paper files | Assistant | See §4.2 below |
| 5. Upload via Zenodo web UI (or via GitHub Release auto-archive after step 2) | **User** | --- |
| 6. Fill metadata: title, authors, keywords, license (CC-BY-4.0), related identifiers (arXiv, GitHub URL) | **User** | Pre-filled in `zenodo.json` (Assistant will prepare) |
| 7. Reserve DOI (Zenodo gives a DOI before publishing); use it in journal submission | **User** | --- |
| 8. Publish; DOI becomes permanent | **User** | --- |

**Assistant follow-up**: anchor Zenodo DOI in `CITATION.cff` + `DATASET.md` + paper artefact statements.

---

## 4. Replication-package builds

### 4.1 NOETHER `replication.zip`

```bash
cd <NOETHER_ROOT>
zip -r noether_replication_v0.1.0.zip \
    supplementary/ \
    scripts/ \
    NOETHER_paper.tex NOETHER_paper.bib NOETHER_paper.pdf \
    NOETHER_paper_arxiv.tex NOETHER_paper_arxiv.pdf \
    README.md REPRODUCTION.md DATASET.md CHANGELOG.md \
    CONTRIBUTING.md RELEASE_CHECKLIST.md LICENSE CITATION.cff \
    requirements.txt requirements-frozen.txt pyproject.toml \
    .env.example .gitignore \
    -x "*.pyc" -x "*__pycache__*" -x "*.aux" -x "*.bbl" -x "*.blg" -x "*.log" -x "*.out"
```

Expected size: ~5-10 MB (paper PDFs dominate). Within Zenodo's 50 GB single-file limit.

### 4.2 P2 `replication.zip`

```bash
cd <P2_ROOT>
zip -r p2_replication_v1.0.0.zip \
    src/ data/ scripts/ tests/ figs/ figures/ replication/ third_party/ \
    submission/p2_ist_final.{tex,pdf,docx} \
    submission/cover_letter_final.{md,pdf} \
    README.md REPRODUCIBILITY.md DATASET.md CHANGELOG.md \
    CONTRIBUTING.md RELEASE_CHECKLIST.md LICENSE CITATION.cff \
    requirements.txt requirements-frozen.txt pyproject.toml \
    .env.example .gitignore \
    -x "*.pyc" -x "*__pycache__*" -x ".pytest_cache/*" -x "*.venv*"
```

Expected size: 50-200 MB depending on cached LLM responses in `data/operator_campaign/cache*`. If > 100 MB, split cache into separate Zenodo deposit.

---

## 5. Cross-references after IDs assigned

After arXiv IDs and Zenodo DOI are assigned, anchor everywhere:

```bash
# For NOETHER
cd <NOETHER_ROOT>
NOETHER_ARXIV_ID="2605.XXXXX"          # user-provided
NOETHER_ZENODO_DOI="10.5281/zenodo.XXXXXXX"  # user-provided
NOETHER_GITHUB="github.com/meng004/P1-MetaPattern"

# Replace placeholders
sed -i.bak "s|<ARXIV_ID>|${NOETHER_ARXIV_ID}|g" CITATION.cff pyproject.toml README.md
sed -i.bak "s|meng004|<actual-username>|g" CITATION.cff pyproject.toml README.md DATASET.md
# Insert Zenodo DOI into CITATION.cff under doi: and into DATASET.md integrity section

# Rebuild PDFs
xelatex NOETHER_paper.tex
cd arxiv/ && ./build_arxiv.sh

# Commit and re-upload arXiv v2 with anchored IDs
```

---

## 6. Compliance audit (pre-publication)

Run before any external upload:

```bash
# Sensitive-info scan (CLAUDE.md §8.8)
for repo in MR元模式 语义变异体; do
  cd "<WORKSPACE_ROOT>/$repo"
  echo "=== $repo ==="
  git ls-files 2>/dev/null | xargs grep -lE "sk-[a-zA-Z0-9]{20,}|/Users/[^/]+|Bearer\s+[A-Za-z0-9]+" 2>/dev/null
done
# Both should output empty.
```

```bash
# Em-dash zero-tolerance (CLAUDE.md §3 step 4)
for f in MR元模式/NOETHER_paper.tex MR元模式/NOETHER_paper_arxiv.tex 语义变异体/submission/p2_ist_final.tex; do
  cd <WORKSPACE_ROOT>
  echo "$f: $(grep -c '—' $f) em-dashes"
done
# Expected: 0 for both NOETHER variants; 1 for P2 (in comment, see arxiv_metadata.md §11)
```

```bash
# §9 archival completeness
for repo in MR元模式 语义变异体; do
  cd "<WORKSPACE_ROOT>/$repo"
  echo "=== $repo §9 ==="
  for f in README*.md REPRODUC*.md DATASET.md CHANGELOG.md CONTRIBUTING.md RELEASE_CHECKLIST.md LICENSE CITATION.cff requirements.txt requirements-frozen.txt pyproject.toml .gitignore .env.example; do
    ls $f 2>/dev/null | head -1 || echo "MISSING: $f"
  done
done
# Both should list all 13 files.
```

---

## 7. Outstanding user actions (cannot delegate)

| # | Action | Time | Risk if skipped |
|---|---|---|---|
| 1 | Decide GitHub username / org name | 5 min | Cannot complete steps 3.2 / 4 / 5 |
| 2 | Create GitHub account (if first-time) | 10 min | Cannot push code |
| 3 | Create arXiv account + obtain endorsement | 10 min + endorser response time | Cannot upload preprint |
| 4 | Create Zenodo account + link to GitHub | 10 min | Cannot mint archival DOI |
| 5 | SSH key generation + GitHub registration | 5 min | Cannot push code without HTTPS auth |
| 6 | Sensitive-info final eye-check on PDFs | 10 min | Risk of leaking private paths to public preprint |
| 7 | Confirm `meng004` placeholder before push | 1 min | Wrong URL in committed files |
| 8 | Sign-off on per-channel publication | 5 min | Premature / accidental public release |

---

## 8. Roll-back / supersede

| Channel | Roll-back option |
|---|---|
| arXiv | **Cannot delete**; can only supersede with v2 (new revision under same arXiv ID). Old version remains downloadable forever. |
| GitHub | Can delete repo (loses Issue history). Can rewrite history (loses commit lineage). Force-push warned. |
| Zenodo | **Cannot delete** published deposits (only restrict access). Can create new version (chained DOI). |

**Implication**: scrutinise everything before the first arXiv/Zenodo publish. GitHub force-push is the only fully reversible channel.

---

## 9. Submission decision summary

| Channel | NOETHER | P2 | Action this week |
|---|---|---|---|
| **arXiv** | Submit Day 0 | Submit Day 0 (or after NOETHER endorsement) | User action; tarball ready |
| **GitHub** | Push Day 1 after arXiv | Push Day 1 after arXiv | Awaiting username |
| **Zenodo** | Upload Day 2-3 | Upload Day 2-3 | Awaiting GitHub link |
| **Journal** | TOSEM Day 3+ | IST Day 3+ | After arXiv ID anchored |

---

## 10. Single-table verification before pushing the publish button

| Gate | NOETHER | P2 |
|---|---|---|
| Title char count | 91 ≤ 240 ✓ | 95 ≤ 240 ✓ |
| Abstract char count | 1898 ≤ 1920 ✓ | 1893 ≤ 1920 ✓ |
| PDF compile clean | ✓ | ✓ |
| Em-dash count | 0 ✓ | 1 (in `%` comment, harmless) ⚠ |
| §9 file count | 13/13 ✓ | 13/13 ✓ |
| Author block named | ✓ | ✓ |
| Sensitive-info scan | needs final user check ⚠ | needs final user check ⚠ |
| arXiv endorsement | not yet obtained ⚠ | inherits from NOETHER |
| GitHub username decided | not yet provided ⚠ | not yet provided ⚠ |
| Zenodo account exists | unknown ⚠ | unknown ⚠ |

Three open items remain on the user side: GitHub username, arXiv endorsement, Zenodo account. Once these are resolved, the publishing pipeline can complete in a single sitting (~30 min total).
