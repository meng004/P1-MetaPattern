# §15 投稿版格式审计 + 双盲匿名化 — NOETHER → TOSEM（2026-06-22）

> CLAUDE.md §15(arXiv→期刊投稿同步审计)。从 `NOETHER_paper_arxiv.tex` 派生 `NOETHER_paper_submission.tex`(+ `_submission.bib`),转 TOSEM `acmsmall,review,anonymous` 格式 + double-anonymous 匿名化(用户 2026-06-22 选定双盲)。

## 结论:投稿版就绪（double-anonymous）

编译 **82pp · 0 undef-ref · 0 undef-cite · 0 missing-char · 0 overfull>50pt · bibtex 0 didn't-find**。pdftotext 实证:作者块显示 **"Anonymous"**,基金/单位/CRediT 真名 **0 命中**于正文与可见区。

## §15.2 preamble 防护（propagate 检查）

| 项 | 状态 |
|---|---|
| `\sloppy` + `\emergencystretch{3em}` | ✅ 继承 |
| `\usepackage{adjustbox}` + 表格 max-width 包裹 | ✅ 继承(acmsmall 窄版下 overfull>50pt=0,无 §15 警示的 458pt 灾难) |
| `\setcounter{secnumdepth}{0}` / `fvextra` | ⚠️ 缺,但**当前无需**:无 markdown 手动章节编号(§X.Y.Z 文本引用=0)、无 verbatim 溢出 |

## §15.3 grep 审计（全部期望 0）

| 检查 | 结果 |
|---|---|
| A/B reviewer-speak / process 标记(this revision / Round N / R# W#) | **0** ✅ |
| C 占位符(<ARXIV_ID>/<DOI>/XXXX/TBD/Anonymous2025) | **0** ✅ |
| E 悬空 §X.Y.Z 交叉引用(另会话迁表/加图后高发) | **0** ✅ |
| F 双盲 leak(正文真名/单位) | **0**(仅 reference list [67],见下,ACM 合规) |

## §15.4 编译 + §15.5 排版

- 82pp;undef/missing/overfull>50/bibtex 全 0 ✅
- `\clearpage` 先于 `\appendix`(§15.5.2)✅
- 内联编号:仅 1 处 (i)(ii)(minor,§15.5.1 容许的 cat 标签类)

## 双盲匿名化（已执行）

1. **documentclass** `[manuscript]` → `[acmsmall,review,anonymous]`。
2. **作者块 + 致谢块**(基金 NSFC/Hunan/University of South China + CRediT 真名 + COI + GenAI 披露,全在 `\begin{acks}` 内)→ acmart `anonymous` **自动隐藏**;pdftotext 确认 PDF 无这些。
3. **正文 7 处自指中和为第三人称**(保留诚信含义):
   - "the present authors' prior PWR MR catalogue" → "a prior PWR MR catalogue"
   - "our prior reactor-physics taxonomy" → "a prior reactor-physics taxonomy"
   - "the (present )authors' own [prior work]" ×2(§1 L172 + 收敛诊断)→ "prior work / prior reactor-physics catalogues"
   - "the authors' own catalogue, not an external corpus" → "a prior catalogue from the same research line, not an external corpus"(**保留 self-referential 非外部的诚信披露**,去身份)
   - "by some of the present authors addresses the orthogonal problem"(salami 划界)→ "A separate line of work addresses..."(保留 cite+划界)
   - "block-labelled by the framework's authors" → "by the framework's designers"(保留标注非独立的诚信点)
   - "developed by teams distinct from the present authors" → "distinct from the present study's contributors"
4. **arXiv 自披露移除**:`\acmDOI{10.48550/arXiv...}` 注释掉、`\acmConference[arXiv preprint]{...}` 删(均 de-anon 风险 + 期刊不用 conference);"conference submission system" → "journal submission system"。

## 残留（作者知悉，非阻塞）

1. **reference [67]**(作者 2022 reactor 先验 "Identification Algorithm Framework",Yan/Yang/Lu/Li/Gong/Liu)在参考列表显示真名——**ACM double-anon 合规**:政策要求自引**保留在 reference list、正文第三人称引用**(删名反而违规+破坏文献)。正文已第三人称化。残留推断风险(reviewer 或可从 reactor 主题 + 该自引推测)是双盲固有张力,ACM 接受;作者可选进一步弱化 [67] 的描述性限定词,非必需。
2. **GenAI 披露**当前在 `\begin{acks}` 内 → review 期被 anonymous 隐;camera-ready(去 anonymous)恢复。ACM 接受;若希望 review 期可见,可移出 acks 到正文脚注。

## 文件

- `NOETHER_paper_submission.tex`(acmsmall,review,anonymous)+ `NOETHER_paper_submission.bib`
- 审计据 §15.6 元流程:从 `_arxiv.tex` 派生(非 Pandoc 重生)→ preamble 继承 → grep+编译审计 → 目视匿名确认。
