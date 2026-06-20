# A9 篇幅压缩方案（82 → 目标页）

> 日期：2026-06-20。基线：`NOETHER_paper_arxiv.tex` 3167 行 / 82 页 / 21 表 / 1 图 / 4 tcolorbox。
> 目的：降到 TOSEM 评审可读区间，**同时**与 A5（理论 headline 上位、淡化争议实证）协同。
> 红线：守 B2 护栏，不动数值，不删 verdict，下放≠删除（详细表迁 supplementary S9，主文留摘要表 + cross-ref）。

## 0. 现状页面预算（按 section）

| 区块 | 行域 | ~页 | 表 | 压缩定位 |
|---|---|---|---|---|
| front+Intro | 1–288 | ~7 | 0 | 基本不动 |
| Related Work | 288–385 | ~3 | 0 | 不动 |
| Proposed Method | 385–1074 | ~17 | 1 | 轻压（证明细节已在 Appendix；正文叙事可紧凑 ~3 页）|
| Experiments(stub) | 1074–1091 | ~0.5 | 0 | 不动 |
| Primary MR 证据(EQ1) | 1099–1215 | ~4 | 3 | **保留**（主证据）；3 表可并 2 |
| 等变-ML 案例 + DeepCrime pilot | 1215–1411 | ~6 | 4 | DeepCrime 2 表 → 1 摘要表 + 全表迁 S9（~2 页）|
| **L\*-blindness 实证电池** | 1411–2398 | ~25 | ~8 | **主战场**：详细 per-block/per-mutant 表迁 S9，留中心结果表 + verdict（~省 14–16 页）|
| METRIC+/Path-A 对比 | 2398–2700 | ~9 | 4 | 3 大表 → 1 摘要表 + 全表迁 S9（~省 6 页）|
| PMCM + IBT 实证 E1–E3 | 2700–2763 | ~2 | 0 | 轻压 |
| Threats/Future/Concl | 2763–2896 | ~5 | 0 | Future "16 items" 列表压成段（~省 1 页）|
| Appendix 证明 C | 2896–3123 | ~6 | 0 | **保留**（理论 headline 支撑）；C.7 "worked enumeration (migrated)" 可全迁 S（~省 2 页）|
| Data/bib | 3123–3167 | ~3 | 0 | 不动 |

## 1. B2 护栏（必须留主文，禁迁/禁删）

- L1860 tcolorbox（head-to-head restatement）承载 **GenMorph 败局 McNemar p=0.0043 + "dominated by Set G"**——唯一定量披露点，**留主文**。
- 所有 **underpowered / n=N insufficient for α=0.05** 标注（C6）——留主文。
- L\*-blindness "derivable without data" 限定 + 中心结果表（L1674）——留主文。
- EQ1 primary MR-identification 证据（Table L1110/1144/1175）——主证据，留主文。
- 理论：Theorem 1/1′/2、IBT、negative-pwr 命题及其 Appendix C 证明——留。

## 2. 分批方案（每批独立编译 + 独立 commit）

### Batch 1（低风险，~省 4–5 页）
- DeepCrime pilot 2 表（L1308, L1324）→ 1 摘要表，全表迁 `supplementary/S9`。
- Future Work "Committed future work (16 items)"（L2336）枚举 → 紧凑段。
- Appendix C.7 worked enumeration (migrated)（L3118）→ 全迁 supplementary，主文留 1 句 + cross-ref。
- Primary MR 证据 3 表（L1110/1144/1175）→ 评估能否并 2。

### Batch 2（中风险，~省 6 页）——METRIC+/Path-A
- METRIC+ 3 表（L2407, L2454, L2540）+ Path-A 表（~L2540-2700）→ 主文留 1 摘要表（含 Path-A McNemar verdict）+ 全表迁 S9。
- 保留：Path-A head-to-head verdict 句、三-SOTA-category caveat。

### Batch 3（高风险，~省 14–16 页）——L\*-blindness 电池
- 详细 per-block 表（L1557, L1674, L1835, L1890, L1934, L2142, L2309）→ 主文留**中心结果表（L1674）** + **L1860 McNemar box** + 各 verdict 段；其余 per-mutant/per-block 明细表迁 S9。
- 大量 `\paragraph{...}` 逐块叙事（L1762–2240）→ 合并为每块 1–2 句 + 指向 S9。
- 保留：falsification verdict、hypotSig outlier 处理、D2 prediction 6.9%、coverage extension(两 SUT only Set N)。

### Batch 4（低风险收尾，~省 3–4 页）
- Proposed Method 正文叙事紧凑化（不动定义/定理/算法）。
- 全局 cross-ref 重扫（迁表后 `\ref{tab:...}` 悬空检查）。

## 3. 现实目标取舍（需用户拍板）

| 目标 | 做法 | 风险 |
|---|---|---|
| **~50–52 页（推荐）** | Batch 1+2+4 全做，Batch 3 做一半（留更多实证叙事）| 低；保留 thoroughness 观感 |
| **~45–47 页（激进）** | Batch 1–4 全做，L\*电池几乎只留中心表+verdict | 中；可能被"看重实证细节"的评审视为单薄，但与 A5 淡化争议实证协同 |

## 4. 执行纪律

- 每批后跑：`xelatex×2` → 0 undef refs / 0 missing-char / 0 overfull>50pt + 记录页数 delta。
- 迁走的表内容**逐字**进 `supplementary/S9_*`（数据 SSOT，不丢）；主文 cross-ref 指向 S9。
- 每批独立 commit（`phase-D(round-1): A9 batch-N ...`）。
- 任一批触碰 B2 护栏 → 停，回退该处。
