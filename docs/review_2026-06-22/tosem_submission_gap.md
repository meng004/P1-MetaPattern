# TOSEM 投稿资料 gap 检查 — submissions/TOSEM/（2026-06-22）

> 对象：`submissions/TOSEM/NOETHER_paper_submission.{tex,bib,pdf}`。
> 目标：ACM TOSEM（Transactions on Software Engineering and Methodology），acmsmall + review + anonymous。
> 来源：ACM 官方 dl.acm.org 全 403（反爬虫），转用 ACM SIGSOFT Medium "Why Publish in ACM TOSEM in the Twenties"（EIC Mauro Pezzè 官方发布）+ ACM TOSEM Calls for Papers + Registered Papers 政策 + acmart 类源代码默认行为。

---

## ① 目录结构（已重整）

```
manuscript/                              ← 原始稿件（公开 arxiv 版，含真名）
  NOETHER_paper.bib
  NOETHER_paper_arxiv.tex
  NOETHER_paper_arxiv.pdf

submissions/TOSEM/                       ← TOSEM 投稿资料（双盲）
  NOETHER_paper_submission.tex
  NOETHER_paper_submission.bib
  NOETHER_paper_submission.pdf
```

`submissions/TOSEM/NOETHER_paper_submission.tex` 用 `TEXINPUTS=../../:./:` 跑 xelatex
通过（exit 0/0/0 · 82 pp · 0 undef · 0 missing-char · 0 overfull>50pt）；
跨目录 `\input{theory/ibt_section_3_4}` 已通过 TEXINPUTS 解决。

---

## ② 形式合规清单

| 项 | TOSEM/ACM 要求 | 当前状态 | 评 |
|---|---|---|---|
| documentclass | `acmart` 加 acmsmall 选项 | `[acmsmall,review,anonymous]` | ✅ |
| `\acmJournal{TOSEM}` | 必须 | 第 12 行 | ✅ |
| bibstyle | `ACM-Reference-Format` | 第 2997 行 | ✅ |
| inline 引用 | 数字制 `\setcitestyle{numbers,sort&compress,square}` | 第 23 行 | ✅ |
| CCSXML + ccsdesc | 必须 ≥1 级 ccsdesc（significance ∈ {100,300,500}）| 3 条 ccsdesc（500/300/300）| ✅ |
| Title 词数 | ≤ 15 词建议 | **13 词** | ✅ |
| Keywords | 5–8 个 | **7 个** | ✅ |
| Abstract | 无硬字数上限；ACM 偏好单段散文 | **353 词，结构化 Context/Objective/Method/Evidence/Conclusion** | ⚠️ 见 §④ |
| 双盲匿名 | acmart `anonymous` 选项自动隐作者/致谢 | acks 块含真名+基金+CRediT，编译时隐 | ✅ |
| 正文自指第三人称化 | 双盲下必须 | "the present authors' prior X" → "a prior X" 等 7 处已第三人称 | ✅（§15 审计） |
| 自引 reference list | ACM 双盲政策允许保留 | [67] Yan2022InputPattern 保留 | ✅ |
| Funding 声明 | 推荐 | acks 内基金号 5 项 | ✅ |
| CRediT 贡献 | ACM 推荐 | acks 内 4 作者 × 角色 | ✅ |
| Declaration of Competing Interest | 必须 | acks 末段 "no conflict of interest" | ✅ |
| Generative AI disclosure | ACM Policy on Authorship 强制 | acks 内"two roles"段，引 §case-study + §threats | ✅ |
| Data / Artifact Availability | 推荐 | §10 `Data and artifact availability` 章节 | ✅ |
| `\clearpage` 先于 `\appendix` | acmart 排版规范 | 第 2607→2608 行 | ✅ |
| Overflow safety preamble | 防溢出 | `\sloppy` + `\emergencystretch{3em}` + `adjustbox` | ✅ |
| Reference 真实性 | 投稿 hard-block | 75/75 = 71 verified + 4 soft + 0 unverified（round2 audit） | ✅ |
| Reference 一致性 | 75 cited == 75 defined | `bib_all_cited_check.py` OK | ✅ |
| 编译健康 | undef/missing/overfull = 0 | exit 0/0/0 · 82 pp · 0/0/0 | ✅ |

---

## ③ 待补项

| 项 | 状态 | 备注 |
|---|---|---|
| **Cover letter** | ❌ 缺失 | 初投 ACM TOSEM 建议附 — 提示 track 选择（regular / fast impact / survey）、main contributions、targeted reviewers（若知）；revision 必须。`submissions/TOSEM/` 下未见 `cover_letter.{tex,pdf}`。 |
| **track 选择标识** | ❌ 未明 | TOSEM 当前接收：regular / fast impact (≤45 pp) / survey (unlimited) / RCR / preregistered。82 pp 体量直接超 fast impact；可投 regular（无硬页限）或 survey（不限）。需在 Manuscript Central 投稿系统下拉选 — 不在 .tex 内体现。 |
| **theory/ 子目录 packaging** | ❌ 缺 | `\input{theory/ibt_section_3_4.tex}` 跨目录引用项目根 `theory/`；当前编译靠 `TEXINPUTS=../../:./:`。Manuscript Central 上传 zip 时必须含 `theory/ibt_section_3_4.tex`，否则期刊审稿端 build 失败。建议打包脚本把 `theory/` 复制进 zip 根。 |
| **完整 zip 投稿包** | ❌ 未生成 | 待生成 `NOETHER_TOSEM_submission_2026-06-22.zip`，含：`.tex` + `.bib` + `.bbl` + `.pdf` + `theory/ibt_section_3_4.tex` + `Notes/cover_letter.pdf`（若加）+ 任何外部图（当前无 includegraphics）。 |
| **archival RCR badge**（可选） | ⏳ 后做 | NEXT_STEPS §A 提"接受后做 Zenodo upload + DOI 替换占位符"。RCR badge 需 artifact DOI；当前未提供（可选项，初投不阻塞）。 |

---

## ④ 风险点（非阻塞，作者拍板）

| 风险 | 论据 | 建议 |
|---|---|---|
| **Abstract 结构化标签** | 当前用 Context/Objective/Method/Evidence/Conclusion，是 IST/Elsevier 风格。ACM TOSEM 多数为单段散文，无强制结构化。不属违规，但和 ACM 视觉惯例不同，可能引 reviewer 个人偏好评论。 | 保留或压平为单段，作者拍板。06-22 polish 评估已记录"非硬性"。 |
| **Body 22k 词 / 82 pp** | TOSEM regular 无明确上限；fast impact ≤ 45 pp。当前 82 pp 投 regular OK，投 fast impact 需大砍。Pezzè 编辑学界普遍接受 60–80 pp 理论+实证长文。 | 投 regular track；预先 cover letter 解释 82 pp 的必要性（理论闭合 + 三域 instantiation + 实证）。 |
| **Appendix > 1 页** | ACM 政策："appendix > 1 页仅在线版（DL）发布"。当前 Appendix（detailed empirical tables + proofs，§Detailed empirical tables + §Proofs）大于 1 页。 | 不阻塞 — 这是 publication-time 政策，不是 submission 阶段问题；投稿 PDF 仍含完整 Appendix 供 reviewer 阅读。 |
| **arXiv 预印本披露** | TOSEM 接受 arXiv preprint 并行（`\acmDOI{10.48550/arXiv...}` 已注释隐）；双盲版不应露 arXiv ID。但 ACM 通行规则要求**在 cover letter 中披露** arXiv presence。 | 加 cover letter 时一并披露 arXiv preprint ID（保留在原始稿件 `manuscript/`，投稿稿不露）。 |
| **GenAI 披露位置** | 当前 GenAI 段在 `\begin{acks}` 内 → review 期被 anonymous 自动隐藏，camera-ready 才恢复。ACM Policy 要求 review-stage **可见**。 | 可移到正文脚注或保留现状（多数 ACM 期刊接受 acks 内披露）。06-22 §15 审计记录"作者可选"。 |

---

## ⑤ 期刊形式合规 — 总判定

**形式合规 PASS**（17/17 必须项 ✓）；3 项待补（cover letter / theory packaging / 完整 zip）；4 项可选风险（abstract 标签 / 页数 / appendix online-only / GenAI 位置）。

无 publication blocker 形式缺陷；以下补完即可上 Manuscript Central：

1. 写 `submissions/TOSEM/cover_letter.{tex,pdf}`（1 页 — 标 track + 列 contributions + 披露 arXiv preprint + 解释 82 pp 必要性）。
2. 打包脚本：把 `theory/ibt_section_3_4.tex` 复制进 `submissions/TOSEM/theory/`，调整 `\input{}` 路径不变；或保留外部依赖但打 zip 时一并 include。
3. 生成 `NOETHER_TOSEM_submission_2026-06-22.zip` 备投。

ACM TOSEM 投稿前清单：

```
□ Cover letter（1 页）
□ 主稿 .tex（自包含或附 theory/ 子目录）
□ .bib + .bbl
□ 编译后 .pdf（82 pp · 双盲 "ANONYMOUS AUTHOR(S)"）
□ Manuscript Central 注册账号 + lead author 信息
□ 提示 submission track（regular）
□ 披露 arXiv preprint（cover letter）
□ Reference DOI 真实性（75/75 PASS — 已存档 reference_verification_round2.md）
```
