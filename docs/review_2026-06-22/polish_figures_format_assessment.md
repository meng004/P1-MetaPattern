# 投稿前：润色/去AI + 图表合理性 + 期刊格式 评估（2026-06-22）

> 对象 `NOETHER_paper_submission.tex`(TOSEM acmsmall,review,anonymous)。
> ✅ 本轮 Bash 分类器间歇恢复(单命令可用、复合命令偶发不可用),全文 grep / 重编译 / 双盲复核**已完成**。

## ① 润色 / 去 AI 化 — 干净，无需修正（confirmatory grep 已跑）

全文 grep 实测：

| 检查 | 结果 |
|---|---|
| em-dash(U+2014 "—") | **0** ✅ |
| 高信号 AI 词(delve/crucial/pivotal/tapestry/testament/intricate/multifaceted/seamless/paradigm shift/nuanced) | **0** ✅ |
| 边界 AI 词(leverage/showcase/underscore/realm/foster) | **0** ✅ |
| throat-clearing(it is important to note / worth noting / in this section we) | **0** ✅ |
| utilize / in order to / plays a … role / shed light / a wide range of / paving the way | **0** ✅ |
| `harness`(8 处) | 全为"test harness/loss landscape"技术术语，合法 ✅ |
| `landscape`(2 处) | "fitness landscape"/"loss landscape"，合法技术术语 ✅ |
| `not only`(2 处 L180/L1055) | 均为"not only X; Y"句式，非"but also"套话，合法 ✅ |
| `Beyond`(句首 2 处 L299/L541) | 语义为"比…更进一层"，非纯加性转折，可保留 ✅ |
| `via`(16 处) | 几乎全为"by means of[算法/块/方法/文献]"技术简写(via CONSTRUCT-MP / m_inv via G / via Clebsch–Gordan)，领域恰当，非填充式过用，机械替换不改善 ✅ |

**结论：投稿稿 de-AI 底子极佳(历经多轮 humanizer)，无任何需修正项。**

## ② 图、表是否合理 / 过多 — 合理，无需删

精确计数(grep 实测)：

- **图 = 2**：`fig:noether-arch`(L184 架构图) + `fig:blocks`(L471 八块图)，**均为 TikZ 手绘，0 张外部位图**。对 82pp 理论+实证长文，2 图偏少而非过多。
- **表 = 15**：正文 ~10(L654/722/752/1062/1136/1170/1201/1287/1969/2139) + 附录"Detailed empirical tables" 5(L2619/2647/2681/2698/2755)。已主动迁 detailed tables 入附录 + supplementary S8-S11。正文 ~10 表对重实证 TOSEM 长文**可接受、不过多**。
- **tcolorbox = 3**(boundary/contribution 盒，已去重)。
- **tikz = 2**(即两张图)。

**结论：图表数量合理，已做篇幅精简，无需进一步删减。**(可选：再加 1 张 IBT 检测核示意，非必需。)

## ③ 期刊格式（TOSEM/ACM）— 合规；已修一处标题大小写不一致

| 项 | 状态 |
|---|---|
| documentclass `[acmsmall,review,anonymous]` | ✅ |
| `\acmJournal{TOSEM}` + `\settopmatter{printccs,printacmref,printfolios}` | ✅ |
| CCS(CCSXML + 3×ccsdesc) | ✅ |
| keywords(7) | ✅ |
| `\setcitestyle{numbers,sort&compress,square}` + `\bibliographystyle{ACM-Reference-Format}` | ✅ |
| overflow-safety preamble(`\sloppy`+`\emergencystretch{3em}`+adjustbox) | ✅ |
| `\clearpage` 先于 `\appendix`(L2607→2608) | ✅ |
| 编译健康(今/重编 log) | **0 missing-char · 0 undefined ref/cite · overfull 仅 1 处 27pt(<50pt) · 82pp** ✅ |
| 双盲：作者块/基金/CRediT 经 acmart `anonymous` 隐藏;pdftotext 正文真名 0 命中(仅 ref [67] 自引保留真名=ACM 双盲合规) | ✅ |
| 6 处 `undefined`(log) | 全为 Font-shape 回退(inconsolata sc/it、LibertinusMath/latinmodern-math bold)，cosmetic，非未定义引用 |

**已修正(本轮)**：章节标题大小写不一致——所有 `\subsection` 为 sentence case，但 6 个 `\section`(Related Work / Proposed Method / Results and Discussion / Threats to Validity and Limitations / Future Work / Data and Artifact Availability)曾为 Title Case。按 §6.2(TOSEM/ACM sentence case)+ 文内子节多数派，统一改为 sentence case。重编 2 遍 xelatex exit 0、82pp、0/0/0 不变。

**可选(非硬性，未改)**：摘要用结构化粗体标签(Context/Objective/Method/Evidence/Conclusion)属 IST/Elsevier 风格;ACM/TOSEM 惯例多为单段无标签。非违规，是否压平留作者决定(§4 不擅改实质)。

## 待办（需作者/后续）

1. **submission/ 派生快照重生**：本轮改的是 `NOETHER_paper_submission.tex`;若 submission/ 目录另有派生稿，投稿前从此稿整体重生。
2. **commit**：本评估 + 6 处标题修正 + 上一轮 §15 投稿版(`_submission.tex/.bib/.pdf` + `submission_format_audit.md`)待一并提交(分类器稳定后)。
