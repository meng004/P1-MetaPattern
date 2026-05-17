# 关键数据快照（immutable）

**目的**：固化重构前所有关键数字、p 值、计数；重构后逐项比对，发现漂移立即修正。

**日期**：2026-05-16（重构启动）

---

## 数据 1：L*-blindness 中心实证（§7 → 新 §4.4）

| 项目 | 数值 |
|---|---|
| **5/6 verdict** | 5/6 SUTs 在 in-scope substrate 上通过 L*-blindness 预测 |
| Outlier SUT | 1/6 出现 outlier |
| Pre-registration | git commit before data collection |

---

## 数据 2：Head-to-head vs GenMorph（§7 → 新 §4.5）

| Stratum | Test | 数值 | 显著性 |
|---|---|---|---|
| Pooled | McNemar exact | p = 0.0043 | 显著 (Set G 主导) |
| D1 only | McNemar exact | p = 0.019 | 显著 (Set G 主导) |
| Per-block | 详见 tab:per-block-headtohead | 互补 | --- |

**等价 mutant 排除**：62 mutants → 5 equivalents (ConditionalsBoundaryMutator on recursive normalising SUTs) → final n=57

**Stage 4.5 Round 5 修复**：Fisher exact p=1.0 column-degenerate misuse → corrected to McNemar exact p=0.500 + Fisher unpaired p=0.444

---

## 数据 3：METRIC+ Path A 三层（§8.2 → 新 §4.6）

| Tier | Substrate | n (mutants) | Test | p value | 结论 |
|---|---|---|---|---|---|
| Tier 3 (Python reduced) | 4 SUTs Python re-impl | 219 | McNemar | --- | bidirectional asymmetries |
| **Tier 3+ (Java/PIT)** | 4 SUTs Java + PIT 1.7.4 | **120** | McNemar exact (pooled) | **p = 0.625** | NS (92.6% both-kill) |
| **Tier 3++ (Major cross-tool)** | 4 SUTs Java + Major/JDK 11 | **555** | McNemar exact (pooled) | **p = 0.211** | NS, bidirectional cancellation |
| Major / PIT 操作数比 | --- | **4.6×** | --- | --- | larger pool |

**Major mutation ID ranges**:
- SBaggage: 1-135
- SExpense: 136-236
- SMeal: 237-448
- SPhone: 449-555

**Per-subject reach asymmetries** (Major):
- SPhone: Set MP exclusive reach
- SBaggage: Set N exclusive reach
- 两者 cancel pooled → "complementary not competitive" 最强证据

**$H_{\mathrm{MP1}}$ pre-registered subsumption**: falsified **bidirectionally** per-subject

---

## 数据 4：DeepCrime pilot（§6.6 → 新 §4.3 或 §3.5.2 demo）

| 项目 | 数值 |
|---|---|
| pilot 规模 | n = 5 SUTs |
| Detection counts | 详见 tab:pilot |
| Contingency | tab:deepcrime-contingency (2x2 配对) |
| Mode 1+3 fix | Mode 1 + Mode 3 column-degenerate misuse fixed |

**R1-m2 mandate**: pairwise McNemar 必须显式呈现

---

## 数据 5：Apache Commons Math pilot（§6 supp）

| 项目 | 数值 |
|---|---|
| SUTs | 3 |
| Set N MRs | 5 |
| Target-method mutants | 77 |
| Set G | structurally N/A on Maven-resolved substrates |
| Pooled Set N kill rate | 10/77 = **13.0%** |
| G-block kill rate | 6/21 = **28.6%** |
| D2 prediction pass | 2/29 = **6.9%** |

---

## 数据 6：Set L LLM ensemble (Done 2 of 3 vendors)

| 项目 | 数值 |
|---|---|
| Vendors × temps × SUTs | 2 × 5 × 10 = **100 samples** |
| MRs total | 487 |
| Executable | 212 |
| Translation rate | **43.5%** |
| Matchable subset | 34/34 (Set L = Set N) |
| Outside 8-block frame | **56.5%** |
| Third-vendor (Claude Opus) | **Pending** |

---

## 数据 7：18-MR audit Fleiss κ

| 项目 | 数值 |
|---|---|
| Fleiss κ | **0.857** |
| Raters | --- |
| Subset | 18 MRs |

---

## 数据 8：Boltzmann 84-MR PWR corpus（§5 → 新 §3.5.1）

| 项目 | 数值 |
|---|---|
| Total MRs | **84** |
| Mapped to 8-block | **84/84** = 100% |
| Blocks exercised | **5 of 8** (G, O_le, L*, T_rev, D*) |
| Empty blocks | 3 (T*, E*, B*_rel for PWR) |
| Inductive → deductive | tab:refinement (17 old → 5 deductive) |
| Representative MRs (body) | tab:elementwise: 现 12 → 方案 A 后 **7** (5 canonical per non-empty block + 2 predicted) |
| Full 12-MR table → Supp S2 | 方案 A 迁移到 `supplementary/S2_pwr_corpus/elementwise_12.md` |

---

## 数据 9：Theorem 1' falsification（§6.8 → 新 §3.6）

| 项目 | 数值 |
|---|---|
| Counterexamples | **2 pairwise-independent** |
| 1st counterexample | Non-additivity of rod-bank reactivity worth |
| 2nd counterexample | Second-order mixed dependence of $k_{\mathrm{eff}}$ on moderator temperature and boron concentration |
| Translate-extension dimensions | **5** (from PWR) + **5** (from equi-ML/RDB surveys) = **10** total |
| Pairwise-independent obstructions | **5** (tab:five-obstructions) |
| PIT-unexercised blocks | 5 |

---

## 数据 10：Tables 与 Figures 计数

| 类型 | Body | Appendix | Total |
|---|---|---|---|
| Tables | 17 | 1 | **18** |
| Figures | 1 | 0 | **1** |

**Tables 列表**（必须全部保留位置——重构后位置见 section_mapping.md）：
1. tab:complexity (§4 → §3.4)
2. tab:refinement (§5 → §3.5.1)
3. tab:elementwise (§5 → 方案 A: 压缩 12→4, body; 完整 12 → Supp)
4. tab:case-study (§6.6 → §4.3)
5. tab:pilot (§6.6 DeepCrime → §4.3)
6. tab:deepcrime-contingency (§6.6 → §4.3)
7. tab:five-obstructions (§6.8 → §3.6)
8. tab:pit-block (§7.2 → §4.4 setup)
9. tab:l-blindness (§7.4 → §4.4)
10. tab:rediscovery (§7.5 → §4.7 Witness 1)
11. tab:algebra-rich-pooled (§7.7 → §4.5)
12. tab:per-block-headtohead (§7.7 → §4.5)
13. tab:two-stratum (§7.7 → §4.5)
14. tab:gen-cost (§7.9 → §4.5 cost-axis；Tier 2 候选降级)
15. tab:metricplus-sorting (§8.3 → §4.6 PMCM; Tier 2 候选降级到 Supp)
16. tab:metricplus-headtohead-small (§8.2 → §4.6)
17. tab:metricplus-sun2021-scope (§8.2 → §4.6)
18. tab:translate (App C → App C)

---

## 数据 11：页数比较

| 状态 | 正文 | 附录 | Total |
|---|---|---|---|
| **Tier 1 后（当前）** | **61** | **12** | **73** |
| Tier 2 简化预期 | 56-57 | 12 | 68-69 |
| **IMRaD 重构后预期** | **~55** | **7** | **~62** |
| Cover letter 已声明 | 75 | --- | 75 |
| TOSEM foundational 上限 | 50 | --- | --- |
| **重构后偏离上限** | +5 | --- | --- |

---

## 重构核查工作流

每个 phase 完成后：
1. 用本快照逐项核查
2. 任何漂移立即在 commit 前修正
3. 最终 phase D 完成后再次全表核查
