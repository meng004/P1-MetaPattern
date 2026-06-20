# Next steps

This document tracks open follow-up work after the initial GitHub
commit. Each item is independent and can be done in any order.

---

## ⭐⭐⭐ TOSEM 投稿成熟度 — fresh 外部网关 + 多智能体复评 (2026-06-20)

> 首次对当前 TOSEM 重写稿跑通 fresh 外部面板：网关 5 厂商（gpt-5.5 / claude-opus-4-7[opus-4-8 限流回退] / glm-5.2 / deepseek-v4-pro / qwen3-max）= **3 Reject + 2 Major**；Claude 30-agent 对抗验证 workflow = **Major Revision / 55-100 / 接收概率 22%（清完 P0/P1→45-55%）**。
> 对抗验证：17 项 blocker/major 仅 **8 项证实为真**（9 项误读/已自界定）。完整报告：`docs/review_2026-06-20/submission_maturity_assessment_2026-06-20.md`。
> 关键洞察：冷读网关比有验证的 Claude 更狠——真实审稿人不买"self-disclosure 即免责"，提接收率须**重构叙事**而非仅修硬伤。

### 🔴 P0（2026-06-20 已执行，commit ca3f333；构建 80pp/0 undef/0 missing）
- [x] **B1 数据完整性**：Set L 覆盖 `0.40`→`0.20`（arxiv 3 处 + 改假"G and L\*"为只达 G）；analysis.py 重算确认 0.20、H1 仍 HOLDS。submission/(gitignore 派生快照)本地同改，待整体重生。
- [x] **B4 κ 误报**：移除 SSOT 不支持的 Fleiss=1.000/n=33，改报 majority-vs-author Cohen's κ=0.931（n=36,34/36）+ per-rater 0.927/0.927/0.929 + 命名 2 分歧（L_idem_at_one、B_rel_xor_reverse）。
- [x] **B3(i) lrca_audit.md**：创建 `supplementary/S3_case_study/lrca_audit.md` + 复制原始 `lrca_kappa.json`/`lrca_llm_labels.json`，引用可解析。
- [ ] **B3(ii) 18mr_audit κ=0.857（🔴 BLOCKED，需作者）**：raw labels 全仓库不存在，无法 honestly 创建/repoint。选项 (a) 定位/重导原始标注存入 S2；(b) 软化引用（"available on request"/删"released in 18mr_audit/"）。未擅自伪造或弱化。
- [x] **action2**：跨域 "six blocks"→"five blocks"（conservation 是 G 的 MR-class，非第九块）。
- [ ] **B4 复核（需作者）**：本次移除原 Fleiss=1.000 perfect-agreement 表述；若另有真实 Fleiss 计算请确认是否回填。
- [ ] **submission/ 重生（需作者）**：submission/ 为 gitignore 派生快照；relabel/six-blocks/B4 未进快照，投稿前从修正后 arxiv 整体重生。

### 🟡 P1（2-3 周，最大天花板）
- [ ] **B2 篇幅压缩**：80 页→≤45；L\*/IBT 电池、DeepCrime pilot、METRIC+ 对决、LLM-ensemble 各降为 1 表（全表入 S9），EQ1-EQ3 提为独立主证据节；并清过程叙事残留（pre-register/committed-as-follow-up/活文档措辞 L1357）
- [ ] **B6 最近邻文献**：补并尖锐对照 Khritankov-Iakusheva 2024、Gotlieb Symmetric Testing 2003/2006、Patel-Hierons 2018、Gruver 2023、Kaba-Ravanbakhsh 2023、Saha-Kanewala 2019、MemoRIA 2024、MUT 2024；delta 定位为"construction+proof over the layer"

### 🟢 P2/P3（低成本）
- [ ] **B5** Theorem 2 加一句限定（\|G\| 可指数→output-polynomial，非 input-polynomial）；abstract/intro 同步
- [ ] **B7** 切 `\documentclass[acmsmall,review,manuscript,screen]{acmart}`；清双盲/OpenReview 残留（TOSEM 单盲）；加 ACM GenAI 披露；披露 arXiv 预印本

### ✅ 本会话已完成（relabel-only）
- [x] 2026-06-20 time-reversal 记号归一 → `\mathcal{T}^{*}_{\mathrm{rev}}`（33 处，0 残留；对抗验证确认"不一致"现为 false）
- [x] 2026-06-20 Conservation 第九标签调和（§3.1 L469 加定义句，数值未动）→ EIC 确认"reconciled at L469"

---

## ⭐⭐ TOSEM 投稿成熟度 — 多 LLM 网关评审裁决 (2026-06-17)

> 5 跨厂商 LLM（gpt-5 / claude-opus-4-6 / deepseek-r1 / glm-5.2 / kimi-k2-instruct）网关评审 + 30-agent 对抗验证 Workflow（triage → 逐议题对照原文验证 → §10 ARS 五维 → EIC 裁决）。
> 裁决：**Major revision before submission**；**0 存活 publication blocker**（23 归并议题中 17 误读/夸大 · 4 major · 2 minor）。
> 详见 `docs/review_2026-06-17/submission_maturity_assessment_2026-06-17.md`。

### 🟡 In Progress
- [ ] **ISS-7 记号冲突修复（最高优先，relabel-only，本会话执行中）** — 实证章节把 `\mathcal{T}^{*}`/裸 `T^{*}` 用于 translation/period，并引入未定义的 `\mathcal{I}^{*}`（idempotence）块，与 L454 规范分类（`T^{*}`=self-adjoint、`\mathcal{T}^{*}`=time-reversal、`\mathcal{B}^{*}_{\mathrm{rel}}`=relational）冲突，使头条 per-block "Set N edge" 比较不可解读。映射：translation→`G` 子情形；time-reversal 全程统一 `\mathcal{T}^{*}_{\mathrm{rev}}`；未定义 `\mathcal{I}^{*}`→`\mathcal{B}^{*}_{\mathrm{rel}}`。**不动任何数值、不动 "MetaPattern" 用法。** ⚠️ 含一个待作者判断点：headline n=17 行测的是 translation-under-G 还是 time-reversal。

### 🔴 Must-fix before submission（其余 8 项，按 EIC 优先级）
- [ ] 2. **ISS-8 篇幅压缩**（82pp/~45.6k 词 → TOSEM 规范）：Boundary box 4→1（保 L259，其余转 cross-ref）；头条统计量（McNemar p=0.0043、D2 6.9%）各报一次；删 `theory/ibt_section_3_4.tex` L2-4 过期注释 + 3 处 `% TODO-ref`；重跑 xelatex
- [ ] 3. **ISS-2 实证定位**：实证章节起始（~L1057）加一句明确定位为 instantiation/falsifiability 探针（非 powered utility benchmark）；GenMorph 压制 + 底物异构上浮为单一具名 limitation 到 Threats/Boundary box
- [ ] 4. **ARS 方法论 A+B**：LLM 判等投票加小规模人类金标验证（混淆矩阵/FP/FN/κ）+ 延伸共享训练数据 caveat；预注册/论证 D1→D2 "(e.1) v2 override" 规则 + 报告无 override 敏感性分析（最强 Reviewer-2 杠杆）
- [ ] 5. **ARS 统计**：3 块 per-block 族显式陈述多重性 + T* edge 保持 directional-only；case-study N-vs-B/N-vs-L 应用 Bonferroni 或说明；L*-blindness outlier-rescue 事后性整合进 Threats
- [ ] 6. **ISS-11 METRIC+**：软化 "unambiguously strengthens"（L2499）+ 调和 L2236（称未跑）与 L2449+（称已跑）矛盾
- [ ] 7. **benchmark 公正性**：加一段组合公正性段落（home-field 底物 + 单 GP seed=11 + NOETHER 定义指标一起对待）+ 至少跑 multi-seed GP
- [ ] 8. **ARS 外部效度**：收紧 Abstract/C4，使 home-field 多块增益（29/47）不被读作单块工业证据（110 SPARK/LOCUST/SACOS MR 全为 order/O_le）佐证
- [ ] 9. **ISS-20 + ISS-23（minor，低成本）**：加量化摊销 break-even（共享 A_P 的 SUT 数）+ 调和 10h 两种读法；Def 5（L521）补 "relabelling"=坐标-索引置换的一句话定义

### 🟢 不要返工 — 对抗验证驳回的误读（保护作者）
- [ ] （参考，勿动）ISS-1/3/5/6/9/10/12/13/14/15/16/17/18/19/21/22 经对照原文核验为误读/夸大——论文当前文本已自述这些边界（含 5 模型共识的 "Theorem 1 同义反复" 与 gpt-5 Reject 所依据的 "Theorem 2 vacuous"）。逐条理由见报告 §5。

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
- [ ] **执行就绪的 `experiment/s5_aligned`**(NOETHER vs GenMorph,在 GenMorph 公开 23-subject benchmark / 557 mutants)——化解 G1 substrate-bias 的最高 ROI 中立证据;代码就绪、`results/` 空待执行(Stage1 ~4–7h + Stage2 ~30min);见 `docs/tosem_maturity_2026-06-16/protocol_domain_extension.md`

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
