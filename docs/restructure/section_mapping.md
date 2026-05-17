# 章节映射表（source line → target section）

**目的**：每个现有 subsection 显式指定迁移目标，重构过程中防止内容丢失。

---

## 当前结构（重构前，73 pp）

| 当前位置 | Line | 内容 | 估算行数 |
|---|---|---|---|
| §1 Introduction | 120-233 | Intro + 4 contributions + Figure 1 | 114 |
| §2 Background and related work | 234-309 | 5 sub-sections | 76 |
| - §2.1 MT and MR identification bottleneck | 239 | --- | --- |
| - §2.2 Structured MR: METRIC and METRIC+ | 247 | --- | --- |
| - §2.3 Automated MR identification | 253 | --- | --- |
| - §2.4 MetaPattern catalogues | 261 | --- | --- |
| - §2.5 Convergent diagnosis | 271 | --- | --- |
| §3 Operator-algebraic preliminaries | 310-436 | 8 blocks 定义 + decomposition | 127 |
| - §3.1 Programs and algebras | 315 | --- | --- |
| - §3.2 Symmetry groups (B1=G) | 325 | --- | --- |
| - §3.3 Order/monotonicity/linearity (B2=O_le) | 333 | --- | --- |
| - §3.4 Self-adjoint (B3=T*) | 343 | --- | --- |
| - §3.5 Time-reversal (B4=T*_rev) | 351 | --- | --- |
| - §3.6 Limit (B5=L*) | 359 | --- | --- |
| - §3.7 Qualitative-dynamics (B6=D*) | 365 | --- | --- |
| - §3.8 Method-comparison (B7=E*) | 373 | --- | --- |
| - §3.9 Decomposition + B*_rel | 379 | --- | --- |
| §4 The NOETHER framework | 437-567 | CONSTRUCT-MP + Th 1, 2 | 131 |
| - §4.1 Algebra-induced MRs | 440 | --- | --- |
| - §4.2 Construction of MetaPattern set | 469 | --- | --- |
| - §4.3 Closure / canonical-block / out-of-scope | 480 | Theorem 1 | --- |
| - §4.4 Decidability and complexity | 515 | Theorem 2 + tab:complexity | --- |
| - §4.5 Principal limitation | 559 | --- | --- |
| §5 Boltzmann instantiation | 568-678 | 84-MR + refinement | 111 |
| - §5.1 Boltzmann family and algebra | 573 | --- | --- |
| - §5.2 Running CONSTRUCT-MP on A_Boltz | 584 | --- | --- |
| - §5.3 Refinement plus prediction | 588 | tab:refinement + tab:elementwise | --- |
| - §5.4 Noether-style derivation of m_adj | 651 | --- | --- |
| - §5.5 Specialisation: transport/diffusion/burnup | 668 | --- | --- |
| - §5.6 Summary | 674 | --- | --- |
| §6 Cross-domain equi-ML | 679-1159 | A_equi + case study + RDB + PWR negative | 481 |
| - §6.1 equi-ML family and algebra | 682 | --- | --- |
| - §6.2 Running CONSTRUCT-MP on A_equi | 686 | --- | --- |
| - §6.3 SE(3) end-to-end derivation | 695 | --- | --- |
| - §6.4 Adjoint-attention duality | 738 | --- | --- |
| - §6.5 Training-trajectory time-reversal | 757 | --- | --- |
| - §6.6 Small-scale case study | 782 | tab:case-study + tab:pilot + tab:deepcrime-contingency | --- |
| - §6.7 Third domain RDB (A_rel) | 970 | --- | --- |
| - §6.8 Negative PWR | 999 | tab:five-obstructions + 2 propositions | --- |
| §7 Empirical L*-blindness | 1160-2177 | Full empirical | 1018 |
| - §7.1 Prediction | 1187 | --- | --- |
| - §7.2 PIT × 8-block | 1292 | tab:pit-block | --- |
| - §7.3 Test design | 1355 | --- | --- |
| - §7.4 Central result 5/6 | 1417 | tab:l-blindness | --- |
| - §7.5 Per-block patterns | 1498 | tab:rediscovery | --- |
| - §7.6 Witnesses | 1564 | Witness 2 | --- |
| - §7.7 Head-to-head | 1601 | tab:algebra-rich-pooled + tab:per-block-headtohead + tab:two-stratum | --- |
| - §7.8 Threats and future work | 2021 | --- | --- |
| - §7.9 Cost | 2042 | tab:gen-cost | --- |
| - §7.10 Summary | 2120 | --- | --- |
| §8 Discussion | 2178-2603 | 4 threats + METRIC+ + PMCM + practical | 426 |
| - §8.1 Four threats | 2181 | --- | --- |
| - §8.2 Relationship with METRIC and METRIC+ | 2193 | tab:metricplus-headtohead-small + tab:metricplus-sun2021-scope | --- |
| - §8.3 PMCM worked example | 2530 | tab:metricplus-sorting | --- |
| - §8.4 Practical guidance | 2572 | --- | --- |
| - §8.5 Artefact | 2583 | --- | --- |
| - §8.6 Human role | 2598 | --- | --- |
| §9 Conclusion | 2604-2619 | --- | 16 |
| Appendix C (Proofs) | 2627+ | Lemma C.1, Th 1 + Th 2 proofs, C.4-C.7 | 220 |

---

## 重构后结构（目标 ~62 pp）

| 新位置 | 来自 | 内容 | 估算 pp |
|---|---|---|---|
| **§1 Introduction** | 现 §1 | 不变；Figure 1 留此 | 3 |
| **§2 Related Work** | 现 §2 | 5 sub-sections 不变 | 4 |
| **§3 NOETHER Framework**（论点集中）| --- | --- | **~14** |
| - §3.1 Operator-algebraic preliminaries | 现 §3 整章 | 8 blocks + decomposition | ~4 |
| - §3.2 Algebra-induced MRs | 现 §4.1 | --- | ~0.5 |
| - §3.3 CONSTRUCT-MP algorithm | 现 §4.2 | --- | ~1 |
| - §3.4 Theorem 1 (closure) | 现 §4.3 | --- | ~1 |
| - §3.5 Theorem 2 (poly-time) + tab:complexity | 现 §4.4 | --- | ~1 |
| - §3.6 Principal limitation note | 现 §4.5 | --- | ~0.5 |
| - §3.7 Three instantiations (theory)：| --- | --- | --- |
|   - §3.7.1 A_Boltz | 现 §5.1-§5.5 | + tab:refinement + tab:elementwise (12→4) + §5.4 m_adj derivation | ~3 |
|   - §3.7.2 A_equi | 现 §6.1-§6.5 | A_equi theory + SE(3)/adjoint/time-rev MR definitions（不含 case study）| ~2 |
|   - §3.7.3 A_rel | 现 §6.7 | + Supp S6 pointer | ~0.5 |
| - §3.8 Theorem 1' falsification | 现 §6.8 + App C.4 内联 | tab:five-obstructions + 2 propositions + 5 Translate-extension dimensions | ~2 |
| **§4 Empirical Evaluation**（实验集中）| --- | --- | **~22** |
| - §4.1 Research questions + setup | 散落 setup 合并 + 新增 RQ statement | RQ1-RQ5 + SUTs + mutators + baselines | ~2 |
| - §4.2 RQ1: Systematisation (84-MR refinement) | 现 §5.3 内 empirical 部分 | "84/84 mapped" empirical claim | ~1 |
| - §4.3 RQ2: Cross-domain executability | 现 §6.6 (SE(3) case study + DeepCrime pilot) | tab:case-study + tab:pilot + tab:deepcrime-contingency | ~2.5 |
| - §4.4 RQ3: L*-blindness 5/6 | 现 §7.1-§7.4 | tab:pit-block + tab:l-blindness | ~4 |
| - §4.5 RQ4: Head-to-head GenMorph | 现 §7.7 (per-block + pooled + two-stratum + cost) | tab:algebra-rich-pooled + tab:per-block-headtohead + tab:two-stratum + tab:gen-cost (Tier 2 候选降级) | ~5 |
| - §4.6 RQ5: METRIC+ Path A | 现 §8.2 + §8.3 PMCM | tab:metricplus-headtohead-small + tab:metricplus-sun2021-scope + tab:metricplus-sorting (Tier 2 降级) | ~3.5 |
| - §4.7 Two convergent witnesses | 现 §7.5 + §7.6 | tab:rediscovery | ~1.5 |
| - §4.8 Summary of evidence | 现 §7.10 | --- | ~0.5 |
| **§5 Threats to Validity & Limitations** | 现 §8.1 + 现 §7.8 (合并) | 4 threats unified | ~2 |
| **§6 Future Work** | 现 §subsec:future + Supp S4 pointer | Top 5 priorities | ~1 |
| **§7 Conclusion** | 现 §9 | 不变 | 1 |
| Appendix C (Proofs) | 现 App C 不动 | --- | ~7 |
| Bibliography | --- | --- | ~3 |
| **Total** | --- | --- | **~62** |

---

## 内容删减/降级映射（Tier 2）

| 项目 | 来源 | 目标 | 节省 (pp) |
|---|---|---|---|
| tab:elementwise 12-MR → 4-MR 代表 | 现 §5.3 (~1 pp) | body 留 4-MR; 完整 12-MR → Supp S1 | -0.5 |
| §7.9 cost analysis + tab:gen-cost | 现 §7.9 (~1.5 pp) | body 留 1 段 narrative; tab:gen-cost → Supp | -1 |
| §7.5 + §7.6 Witnesses 合并 | 现 §7.5 + §7.6 (~2 pp) | 新 §4.7 合并为 1.5 pp | -0.5 |
| §8.1 4 threats 合并 | 现 §8.1 (~2 pp) | 新 §5 合并为 1 段叙述 (1 pp) | -1 |
| §8.3 PMCM tab:metricplus-sorting | 现 §8.3 (~2 pp) | body 留 1 段; tab → Supp | -1 |
| §8.4 Practical guidance | 现 §8.4 (~1 pp) | 压缩到 0.5 pp | -0.5 |
| §6.4 Adjoint-attention duality | 现 §6.4 (~1 pp) | 新 §3.7.2 内压缩 (definition + 1 example) | -0.3 |
| §6.5 Training-trajectory time-reversal | 现 §6.5 (~1 pp) | 新 §3.7.2 内压缩 | -0.3 |
| Reference 重复整理 | 散落 | --- | -0.5 |
| **合计 Tier 2 节省** | --- | --- | **~-5.6** |

---

## 内容删除清单（彻底删除，仅迁至 Supp）

| 项目 | 当前位置 | 去处 | 理由 |
|---|---|---|---|
| 84-MR 全表 | 已在 Supp S1 | 不变 | body 只保 tab:refinement + 4-MR 代表 + 一句统计 |
| tab:elementwise 8 MRs (12 - 4) | 现 §5.3 | Supp S1 | 代表性子集足够 |
| tab:gen-cost 详表 | 现 §7.9 | Supp | cost-axis 是 tertiary |
| tab:metricplus-sorting (PMCM worked) | 现 §8.3 | Supp S9 (PMCM coverage doc) | §5 refinement 已强支撑 C3 |
| §7.8 threats 内 future-work 段（与 §8.1 重复）| 现 §7.8 | Supp S4 | 单一 threats 章统一 |

---

## Cross-reference 重映射任务（phase D）

需要更新的 \ref / \cite / \pageref 类型：

1. `\ref{sec:framework}` → `\ref{sec:framework}` (assuming label preserved; 取决于新章 label)
2. `\ref{subsec:negative-pwr}` → 新 §3.8 label
3. `\ref{subsec:case-study}` → 新 §4.3 label
4. `\ref{subsec:headtohead}` → 新 §4.5 label
5. `\ref{tab:refinement}` → 不变 (table 留 body)
6. `\ref{tab:l-blindness}` → 不变
7. `\ref{tab:elementwise}` → 不变 (body 留 4-MR)
8. **方案 A 影响**：完整 12-MR 表的引用必须改为 "supplementary~S1"

将在 Phase D 用 sed/regex 批量替换 + pdflatex 编译验证 0 undef ref。

---

## 编译验证清单（Phase D 末）

- [ ] `pdflatex NOETHER_paper.tex` 0 errors
- [ ] 0 undefined references
- [ ] 0 multiply-defined labels
- [ ] 0 em-dash (U+2014) — 严格 zero tolerance
- [ ] page count: 60-65 pp 范围内
- [ ] 18 tables + 1 figure 全部正确编号
- [ ] argument_preservation.md 7 论点逐条核查通过
- [ ] key_data_snapshot.md 所有数字逐项核查通过
- [ ] cover letter 同步更新 length declaration + structural breakdown table
