# A2 篇幅压缩审计（workflow `wf_826dc459-ac4`，2026-06-21）

> 方法：8-agent 分节 fan-out 审计 `NOETHER_paper_arxiv.tex`(81pp),逐处压缩点按 **B2 护栏**分类 SAFE/RISK/BORDERLINE,估页省，editor 合成排序方案。
> **B2 护栏**:verdict 散文 / 四条"does not establish" / GenMorph 落败披露(McNemar p=0.0043) / underpowered 标注 / 任何数字(effect size/p/CI/κ/n) / 任何 weakness-caveat —— **砍/迁=visibility-laundering=禁止**。SAFE=迁移详表到 supplement(留 1 行指针+载力数字)/ 去重 near-identical box / 合并重复 disclaimer / 精简无 verdict-数字-caveat 的冗长散文。

---

## 0. 核心结论（决定性，需作者拍板）

**SAFE 压缩天花板 ≈ 81pp → 78pp(仅 ~2.8pp)。到面板要的 ~45pp 结构上不可能,除非动 B2-RISK。**

| 路径 | 可达页数 | 是否需作者授权 |
|---|---|---|
| 仅 SAFE(去重+迁移 illustrative 表/代码) | 81 → **~78pp** | 否(我可执行) |
| + BORDERLINE 表迁移(每条须人工确认 verdict 在迁移后存活) | → **~64-66pp** | 是(逐条确认) |
| + B2-RISK(砍 verdict 散文/数字/caveat) | → **~45pp** | **是(放松 B2,不推荐)** |

**理由**:论文主体是 load-bearing——证明(C.6 block exhaustion)、饱和数字表(head-to-head / pilot / METRIC+ / PMCM / IBT)、B2 禁动的诚信 caveat。SAFE 池压倒性是散文去重 + illustrative 表/代码迁 supplement,上限不到 3 页。**这与 A9 历史结论一致(温和表迁移地板 ~75pp)。**

---

## 1. 已执行(SAFE,本轮 down payment)

- **第 4 个"Boundary of contribution (Conclusion restatement)" box(L2707-2723)→ 去重为 5 行 cross-ref**:内容全在 canonical §1 box + C2b + §negative-pwr + L2705 散文;(e) 上游 A_P 自动化点在替换句显式保留。面板点名"near-identical box restatement"冗余。省 ~0.3pp。编译验证通过。

---

## 2. SAFE 执行方案(排序,未执行项待批量授权)

| # | 位置 | 动作 | 省页 | 保留的载力元素 |
|---|---|---|---|---|
| 1 | L726-744 tab:elementwise | 删 7 行 MR→block 表,留 L722/L728 supplement 指针 | 0.38 | "seven blocks, two predicted" 散文 + κ/% 在 L724 |
| 2 | L810-826 ρ_rot Python listing | 迁 supplement S9,留 eq:rho-rot + τ=10⁻⁴ | 0.36 | 可执行 MR 方程 + fp32 容差 |
| 3✅ | L2707-2723 第4 box | 已去重(见 §1) | 0.30 | 见上 |
| 4 | L2725-2747 vs L2982-2995 两个 data-availability 节 | 合并为一,留 richer manifest | 0.30 | DOI 10.5281/zenodo.20250634 + 36/5-MR 计数 |
| 5 | L511-521 rem:domain-out-of-scope | 4 bullet→1 句 + L520 verdict 逐字 | 0.15 | reach verdict 逐字 |
| 6 | L410-462 B1-B7 定义后散文 | 3 个 illustrative 段各 2-3 句→1 句(定义块不动) | 0.17 | 7 定义 + empty-MetaPattern 句 |
| 7 | L309-311 自动 MR survey | 14 方法各压到 cite+1 句 | 0.10 | 全 \cite + convergent-diagnosis claim |
| 8 | L1218-1226/1330/1333 secondary-scope disclaimer ×4 | 合并为 1 + cross-ref | 0.09 | underpowered 标注 L1325 + 四条"consistent but does not establish"不动 |
| 9 | L1286-1287 construct-validity caveat ×4 | 留 1 canonical,余 cross-ref | 0.13 | "5/5 unique-detection" + "construct validity not superiority" |
| 10 | L2378/2392/2413/2465 "S4 item (i)" deferral ×4 | 合并 boilerplate | 0.12 | kill counts + block-mapping verdict |
| 其余 #11-17 | 见 workflow 输出 | 散文去重/转场精简 | ~0.5 | 各项保留载力元素 |

SAFE 合计 ≈ 2.8pp(净 DOI 重叠后)。

## 3. BORDERLINE(每条须作者确认 verdict 迁移后存活，~10-12pp)

tab:complexity(L626-648)/ tab:refinement(L696-714)/ tab:two-stratum(L2115-2135)/ tab:metricplus dedup(L2381-2417)/ §empirical-summary recap(L2313-2361)。每条触及一个 verdict 或数字,迁移须人工核对。

## 4. REQUIRES-AUTHOR-APPROVAL(B2-RISK，列出但不推荐)

剩余 ~30pp 都在这里:四个 boundary box 的非 canonical 内容、negative-PWR 证明+obstruction 枚举(L478/600-605/1062-1067/2860-2961)、全部数字结果表(expert-coverage/search-boundary/cross-domain-trace/pilot/Path A/Major replication/E1-E3/pit-block matrix)、construct/external/transferability caveat 段。**砍这些=visibility-laundering,需作者明确放松 B2。**

---

*原始 8-section 审计 + 排序方案见 workflow `wf_826dc459-ac4` 输出。*
