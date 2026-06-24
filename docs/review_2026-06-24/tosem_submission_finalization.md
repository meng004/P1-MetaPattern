# TOSEM 投稿定稿与打包 — 2026-06-24

执行用户 6 项指令的完整记录。

## 结构（最终）

```
manuscript/                         原始手稿（arXiv SoT，真名，[manuscript]{acmart}）
  NOETHER_paper_arxiv.tex           86 pp，standalone 编译（theory/ 已本地化）
  NOETHER_paper.bib                 73 条（删 2 未引用孤儿）
  theory/ibt_section_3_4.tex        从仓库根 theory/ 迁入（git mv，自包含）

submissions/TOSEM/                  TOSEM 双盲投稿包
  NOETHER_paper_submission.tex      [acmsmall,screen,anonymous,review]；87 pp
  NOETHER_paper_submission.bib      73 条
  NOETHER_paper_submission.bbl      预生成（随包提交）
  NOETHER_paper_submission.pdf      评审 PDF（首页 "ANONYMOUS AUTHOR(S)"）
  theory/ibt_section_3_4.tex        自包含副本
  cover_letter.md / highlights.md / README.md
  templates/                        官方 acmart 2.18 模板（参考，不入包）

dist/tosem-submission-2026-06-24.zip  投稿压缩包（8 文件，1.1 MB，已验证 standalone 可编译）
```

> PDF / bbl / zip / dist 均被 .gitignore 排除（构建产物，可复现）；zip 实体在 `dist/` 磁盘上。

## ① 投稿稿来源（关键修正）

旧 `submissions/TOSEM/` tex **早于两层模型重写**（无 tab:mr-families），已废弃。
新投稿稿从当前 `manuscript/NOETHER_paper_arxiv.tex`（86 pp 两层模型 SoT）**重导**：
documentclass→`[acmsmall,screen,anonymous,review]`、bib 指向 submission、theory 本地化、arXiv DOI 评审期隐去。

## ② 双盲匿名化

- `anonymous` 选项自动隐藏作者块 / ORCID / email / `acks`（基金/CRediT/GenAI/COI）。
- 正文 7 处第一人称自指 → 第三人称（"the present authors' prior X" → "a prior X" 等）。
- 自引保留在 reference list（ACM 双盲政策合规）。
- PDF 首页实测 "ANONYMOUS AUTHOR(S)"。

## ③ 作者信息（用户提供，已在 SoT）

4 作者 + ORCID + 3 单位，Meng Li 通讯，均已在 manuscript 作者块（前序会话写入，本次核对与用户数据**逐字一致**）。

## ④ academic-pipeline Stage 4.5 FINAL INTEGRITY（integrity_verification_agent）

**GATE: PASS**（0 P0 阻塞；所有重算统计逐一复现；7 模式 AI 研究失败清单全 CLEAR）。
发现并**已修复** 3 项：

1. **双盲泄漏（P1）**：Zenodo DOI `10.5281/zenodo.20250634` 在评审 PDF 出现 3 次（可解析→去匿名）。§15 grep 只查姓名/邮箱未覆盖 DOI。→ 投稿稿 3 处全部改为 "DOI withheld for double-anonymous review"。manuscript（arXiv 公开）保留 DOI。
2. **all-cited gate（P1）**：`e3nn2022software`、`Fey2019PyG` 定义但未引用（73/75）。→ 两份 bib 均删除（不影响渲染，孤儿不入 .bbl）。现 73 cited = 73 defined。
3. **数值一致性（P2）**：点云 train 64 点 / test 128 点（runner.py 实测 N_POINTS=128 为真实设计）。→ 两份 tex 加一句"held-out test clouds of 128 points, a deliberate point-count generalisation"说明。

## ⑤ paper-search MCP 核 bib

submission bib 与 round2 已核验 bib **逐字一致**（diff exit 0），75/75 PASS（71 verified + 4 soft + 0 unverified，见 `docs/review_2026-06-22/reference_verification_round2.md`）。删 2 孤儿后 73 条。

## ⑥ 润色 / 去 AI / 格式

- em-dash 0；AI 高频词全 0（delve/crucial/pivotal/leverage/...）；via/not-only-but-also/linked-to 0。
- 拼写统一英式（optimizers→optimisers，3 处）。
- 格式：CCS×3 / keywords×7 / ACM-Reference-Format / 数字引用 / `\clearpage` 先于 `\appendix` / overflow safety preamble 全在位。

## 编译验证（两份）

| | manuscript | submission |
|---|---|---|
| 页数 | 86 | 87 |
| undef ref | 0 | 0 |
| missing-char | 0 | 0 |
| overfull>50pt | 0 | 0 |
| bibtex didn't-find | 0 | 0 |
| standalone（无 TEXINPUTS） | ✅ | ✅ |
| zip 解压后 standalone | — | ✅（undef 0/miss 0/ANONYMOUS） |

## ⚠️ 未执行（需用户决策）：supplementary 迁移

用户要求"manuscript 唯一存放 tex、supplementary、figure"。`theory/` 已迁入 manuscript/。但 `supplementary/`（**600 MB · 362 tracked 文件**）被 **10+ 文件**按路径引用（README / DATASET / REPRODUCTION / CHANGELOG / CONTRIBUTING / experiment_realbug/human_kappa/compute_kappa.py 等）。整体迁移=600 MB git churn + 断 10+ 引用，属高风险不可逆操作，**未擅自执行**。figures 为 TikZ 内联，无独立目录。

**待用户拍板**：(a) 确认迁移 supplementary→manuscript/ 并同步更新 10+ 路径引用；或 (b) 保持 supplementary 在仓库根（作为 manuscript 与 submission 共享的学术支撑material）。
