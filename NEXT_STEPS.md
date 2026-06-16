# Next steps

This document tracks open follow-up work after the initial GitHub
commit. Each item is independent and can be done in any order.

---

## ⭐ TOSEM submission readiness — independent maturity review (2026-06-16)

> 6 个互相隔离的 Opus subagent 独立重审,综合裁决 **Major Revision**(评分 38–72),显著低于仓库 Round-4 自评(Accept / 65–75%)。
> 详见 `docs/tosem_maturity_2026-06-16/maturity_review_summary.md`。

### 🔴 Blockers(投 TOSEM 前必解,多数需投入实验)
- [ ] 理论内核偏平凡 + CONSTRUCT-MP Step 3/4 定义级 bug(L529-530);最强定理 Thm 1′ 被自证伪 — 补非平凡定理或改论文类型为 systematisation
- [ ] 唯一真实 head-to-head 被 baseline 显著击败(McNemar p=0.0043) — 需中立真实缺陷上的正面证据点,或收缩 fault-detection 主张
- [ ] 缺独立**人类** inter-rater κ(κ=1.000 是共享语料 LLM 循环) — 自招 ≥2 名独立 rater 做 Cohen's κ
- [ ] 与姊妹论文 T2(Minimum-MR-SubSet,TSE)的 salami 未声明 — 草稿已备(见下)
- [ ] 大量经验主张是 protocol 非 result;"three domains tested" overclaim — 如实分级或补执行

### 🟡 草稿已备 / 进行中(零实验成本)
- [x] 删 4 处 reviewer-process 残留 — 主稿 `NOETHER_paper_arxiv.tex` 已改(2026-06-16)
- [ ] 同步删除投稿版残留:`submission/TOSEM_2026-05-20/manuscript_singleblind/` + `manuscript_anonymized/` + 06-16 singleblind humanized zip
- [ ] 插入 T2 differentiation 段 + cover letter 披露 — 草稿 `docs/tosem_maturity_2026-06-16/differentiation_and_disclosure_draft.md`(待确认插入位置)
- [ ] 去 overclaim(标题/摘要/contributions) — 草案 `docs/tosem_maturity_2026-06-16/overclaim_revision_draft.md`(待用户拍板,属作者决策权)
- [ ] 75 页压至 ≤50 + cover letter 篇幅辩护

### 🔵 Open questions(待用户拍板)
- [x] git 作者邮箱已更正为 `meng004@gmail.com`(2026-06-16;gamail 未进任何 commit,无需修历史)
- [x] 多厂商交叉评审已完成(网关 5 厂商:gpt-5 / grok-4.1 / deepseek / qwen / kimi → 2 Reject + 3 Major,确认 Opus panel;`docs/tosem_maturity_2026-06-16/gateway_panel_raw.json`)
- [ ] 100% 联网逐条 bib 真实性校验(见 §C)尚未执行 — 投真实期刊前 hard-block

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
