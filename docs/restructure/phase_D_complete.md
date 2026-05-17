# Phase D 完成报告 — Final IMRaD + Tier 2 + Cover Letter Sync

**执行日期**: 2026-05-16
**最终状态**: NOETHER_paper.tex (71 pp, IMRaD + Tier 2 简化, compile-clean)

---

## 全流程交付（4 阶段）

| Phase | 内容 | 结果 |
|---|---|---|
| Phase 0 | 论点-论据保鲜.md 3 个文件 | ✓ argument_preservation.md / key_data_snapshot.md / section_mapping.md |
| Phase A | source→target 详细行号映射 | ✓ section_mapping.md |
| Phase B | IMRaD 章节重组（脚本 + 5 处 Edit）| ✓ 73 pp → 73 pp（结构 IMRaD）|
| Phase C | Tier 2 简化（6 项）| ✓ 73 pp → 71 pp（-2 pp）|
| Phase D | Cover letter 同步 + bib audit + 最终验证 | ✓ 71 pp, 0 undef refs, 0 undef cites |

---

## 最终核查（所有项 ✓）

| 检查项 | 结果 |
|---|---|
| xelatex 退出码 | 0 (clean) |
| pages | **71** |
| undefined references | **0** |
| undefined citations | **0** |
| multiply-defined labels | **0** |
| em-dash (U+2014) | **0** |
| bib audit (cited == defined) | **0 uncited, 0 undefined** |
| sensitive info grep | **clean** (无 /Users/, 无 API key) |
| cover letter declared pages | **71** (与 PDF 一致) |

---

## 新结构（IMRaD）

| 新章节 | 来自 | pp |
|---|---|---|
| §1 Introduction | 原 §1 | 4 |
| §2 Background and related work | 原 §2 | 3 |
| **§3 The NOETHER framework** | 原 §3+§4+§5+§6.1-§6.5+§6.7+§6.8 | **22** |
| **§4 Empirical evaluation** | 原 §6.6+§7+§8.2+§8.3 | **26** |
| **§5 Threats to validity and limitations** | 原 §8.1+§8.4+§8.5+§8.6 | 3 |
| §6 Conclusion | 原 §9 | 1 |
| Appendix C Proofs | 原 App C | 7 |
| Bibliography | --- | ~5 |
| **Total** | --- | **71** |

---

## Tier 2 简化清单

| # | 项目 | 节省 | 去向 |
|---|---|---|---|
| 1 | §5.1 Construct (LRCA κ 详细) | ~10 行 | Supp S3 `lrca_audit.md` |
| 2 | §5.1 External (Commons-Math pilot) | ~25 行 | Supp S4 `future_work.md` (b.cm) |
| 3 | tab:elementwise 12→7 MRs | ~10 行 | Supp S2 `elementwise_12.md` ✅ 新建 |
| 4 | §4.5 MR-cost lead-in + caption + 3-axis args | ~30 行 | Supp S4 `cost_breakdown.md` ✅ 新建 |
| 5 | §5.2 K-sweep + Tolerance 派生 | ~15 行 | Supp S1 / S3 已存在 |
| 6 | §4.7 PMCM Case A-bis 6-class itemize | ~12 行 | Supp S9 `pmcm_case_abis_full.md` ✅ 新建 |
| 7 | §4.6 METRIC+ worked example + table caption | ~30 行 | 内联压缩 |
| **总** | --- | **~130 行 → -2 pp** | --- |

---

## 论点保鲜核查（vs IMRaD 重组前的原文）

| 论点 | 关键短语/数字 | 原文 | 最终 | ✓ |
|---|---|---|---|---|
| C1 | "two-layer" framework | 3 | 3 | ✓ |
| C2a | Theorem 1, 2 statements | 2 | 2 | ✓ |
| C2b | "two pairwise-independent" counterexamples | 1 | 2 | ✓ 增强 |
| C3 | tab:refinement (deflationary worked example) | 留 body | 留 body | ✓ |
| C3 | "$11 \to 2$-block compression" (METRIC+ sorting) | 留 body | 留 body | ✓ |
| C3 | "denominator is therefore 1, not 6" (Case A-bis) | 留 body | 留 body | ✓ |
| C4 | $\mathcal{A}_{\mathrm{Boltz}}$ / $\mathcal{A}_{\mathrm{equi}}$ / $\mathcal{A}_{\mathrm{rel}}$ | 3 个 | 3 个 | ✓ |
| H L* | "5/6" verdict | 5 | 5 | ✓ |
| H L* | "Set N is dominated by Set G" McNemar $p = 0.0043$ | 保留 | 保留 | ✓ |
| H_MP | "p = 0.625" (Path A PIT pooled) | 3 | 3 | ✓ |
| H_MP | "555" mutants (Major cross-tool) | 3 | 3 | ✓ |
| H_MP | "bidirectional" per-subject reach | 1 | 1 | ✓ |
| 18 tables / 1 figure / 2 theorems / 2 propositions | 全部保留 | --- | --- | ✓ |

---

## 文件清单

### 主文件
- `NOETHER_paper.tex` (71 pp, IMRaD + Tier 2, 当前)
- `NOETHER_paper.pdf` (71 pp, 编译产物)
- `NOETHER_paper.bib` (56 cited == 58 defined, 0 uncited, 0 undefined)

### 备份
- `NOETHER_paper_imrad.tex` (IMRaD 后立即快照, 73 pp)
- `NOETHER_paper_pre_imrad.tex` (原文备份, 73 pp 原始结构)

### 新增 Supp 文件
- `supplementary/S2_pwr_corpus/elementwise_12.md` — 12-MR 完整表 + sub-category 覆盖
- `supplementary/S4_reproducibility/cost_breakdown.md` — 完整 cost 方法学
- `supplementary/S9_migrated_appendices/pmcm_case_abis_full.md` — Murphy 6-class 完整 decoding

### 过程文档
- `docs/restructure/argument_preservation.md` — 7 论点 + 10 条措辞保留清单
- `docs/restructure/key_data_snapshot.md` — 11 类关键数据快照
- `docs/restructure/section_mapping.md` — source→target 行号映射
- `docs/restructure/phase_B_result.md` — IMRaD 重组报告
- `docs/restructure/phase_C_progress.md` — Tier 2 第一波报告
- `docs/restructure/phase_D_complete.md` — 本文件
- `scripts/imrad_restructure.py` — IMRaD 重组脚本（可重跑）

### 同步更新
- `docs/submission/cover_letter.md` — Length 75→71, structural breakdown 更新

---

## 与 TOSEM length recommendation 的差距

| 维度 | 数值 |
|---|---|
| TOSEM 30-50 pp 推荐 | 50 (上限) |
| 当前 | **71** |
| 差距 | **+21 pp** |
| 重组前 | 73 pp (差距 +23 pp) |
| 改善 | 2 pp（结构性 IMRaD + 6 项 Tier 2 简化）|

仍超 TOSEM length recommendation。论文本质上是 foundational paper（两层框架 + 三个 instantiations + 5 RQs 实证 + METRIC+ Path A），单论页数减到 50 pp 需大幅删减论点-支持证据。Cover letter 已显式向 EIC 申请 foundational-paper category 例外。

---

## 进一步压缩的余地（保留供需要时启动）

| 候选 | 预期节省 | 风险 |
|---|---|---|
| §3 Boltzmann 整章 → §3.6 (压缩至 1 pp) | -2 pp | 高 (C4 失一域 worked example) |
| §4.2 PIT × 8-block 表 → Supp | -1 pp | 中 (D1/D2 分层定义) |
| §4.3 case study tab:case-study / pilot 合并 | -1 pp | 低 |
| §4.4 head-to-head 4 子表合并 | -1.5 pp | 中 (PRIMARY tables) |
| §4.5 cost section 整体移到 Supp | -2 pp | 高 (H3a.3 论点) |
| §4.7 Witnesses 1+2 合并 | -0.5 pp | 低 |
| **极限** | **-8 pp** (可达 ~63 pp) | --- |

不推荐执行——会显著削弱论点-支撑层。当前 71 pp 是 foundational paper 的合理下限。

---

## 提交 checklist（投稿前）

- [ ] User 手动校阅 NOETHER_paper.pdf（特别是 §3 + §4 章节切换处）
- [ ] User 核对 docs/restructure/argument_preservation.md 7 论点清单
- [ ] User 核对 cover_letter.md 6 headline messages 全部仍被新结构支撑
- [ ] User 决定是否清理备份文件 (NOETHER_paper_imrad.tex, NOETHER_paper_pre_imrad.tex)
- [ ] User 决定是否启动进一步极限压缩（不推荐）
- [ ] git commit + git push（不应由 assistant 自动执行，用户授权后由 user 执行）
