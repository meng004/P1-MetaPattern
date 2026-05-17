# Phase C 进度 — Tier 2 简化（部分完成）

**执行日期**: 2026-05-16
**输入**: NOETHER_paper.tex（IMRaD 重组后，73 pp）
**当前状态**: 72 pp（-1 pp 第一波 Tier 2）

## 已完成的 Tier 2 简化

| # | 项目 | 节省（行）| 节省（pp）| 来源 → 去处 |
|---|---|---|---|---|
| 1 | §5 Construct validity (LRCA κ 细节压缩) | ~10 行 | --- | body → supp~S3 (\texttt{lrca\_audit.md}) |
| 2 | §5 External validity (Commons Math pilot 长段压缩) | ~25 行 | --- | body → supp~S4 (\texttt{future\_work.md} item (b.cm)) |
| 3 | tab:elementwise 12→7 MRs + caption 压缩 | ~10 行 | --- | body → supp~S2 (\texttt{elementwise\_12.md}) ✅ 新文件 |
| 4 | §4.5 MR-generation cost lead-in + table caption + three-axis args 压缩 | ~30 行 | --- | body → supp~S4 (\texttt{cost\_breakdown.md}) ✅ 新文件 |
| 5 | §5.2 Audit guidance + Tolerance selection 压缩 | ~15 行 | --- | body → supp~S1 (k_sweep_audit) + supp~S3 (tau_sweep.json) |
| **合计** | --- | **~90 行** | **-1 pp** | --- |

页数节省与行数节省不成正比：page break 边界 + floats 重排导致 90 行节省只触发 1 个 page break。

## 编译验证（每次简化后）

| 检查 | 结果 |
|---|---|
| xelatex 退出码 | 0 (clean) |
| pages | 72 |
| undefined references | 0 |
| multiply-defined labels | 0 |
| em-dash (U+2014) | 0 |

## 论点保鲜核查（vs IMRaD 重组后）

| 关键短语/数字 | IMRaD | Tier 2 部分简化后 | ✓ |
|---|---|---|---|
| Theorem 1' falsified | 保留 | 保留 | ✓ |
| 5/6 L\*-blindness | 保留 | 保留 | ✓ |
| Fleiss κ = 1.000 | 保留 | 保留 | ✓ |
| Commons Math pilot ratio (10/77 = 13.0\%) | 保留 | 保留 | ✓ |
| D2 prediction passes (2/29 = 6.9\%) | 保留 | 保留 | ✓ |
| coverage_NOETHER metric | 保留 | 保留 | ✓ |
| McNemar p = 0.625 (Path A PIT) | 保留 | 保留 | ✓ |
| McNemar p = 0.211 (Path A Major) | 保留 | 保留 | ✓ |

## 仍可继续的 Tier 2 候选（未执行）

| 候选 | 预期节省 | 风险 | 说明 |
|---|---|---|---|
| PMCM Case A-bis (Murphy ML decoding) 压缩 | ~15 行 | 低 | 保留 verdict, 详细映射 → supp~S9 |
| tab:metricplus-sorting (11 D×R × NOETHER 8-block) → Supp | ~30 行 | 中 | C3 deflationary worked example 的 visualization, 移到 supp 后 body 留 narrative |
| §4.7 Two convergent witnesses 合并 | ~10 行 | 低 | Witness 1+2 当前是 \\subsubsection + 2 \\paragraph, 可合并为 1 段 |
| §5.4 Human role 段轻度压缩 | ~5 行 | 低 | 不损论点 |
| **合计预期** | **~60 行 = ~1-2 pp** | --- | --- |

## 新增 Supp 文件

1. `supplementary/S2_pwr_corpus/elementwise_12.md` — 12-MR 完整表 + 选择 protocol
2. `supplementary/S4_reproducibility/cost_breakdown.md` — 完整 cost 方法学（token 估算, 人工时, MR-Scout scope）

## 备份与可回滚性

| 文件 | 状态 |
|---|---|
| `NOETHER_paper.tex` | 当前（IMRaD + Tier 2 部分，72 pp） |
| `NOETHER_paper_imrad.tex` | IMRaD 后立即快照（73 pp）|
| `NOETHER_paper_pre_imrad.tex` | 原文备份（73 pp 原始结构）|

任何时刻可回滚：`cp NOETHER_paper_pre_imrad.tex NOETHER_paper.tex`

## 后续路径

**继续 Tier 2 剩余项**（预期 -1~2 pp，达到 70-71 pp）— 推荐
**或进入 Phase D**（cover letter 同步 + 验证）— 当前页数 72 仍超 TOSEM foundational 50 pp 上限，但相比初始 75 pp 已大幅压缩
