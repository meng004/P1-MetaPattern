# Phase B 完成报告 — IMRaD 章节重组

**执行日期**: 2026-05-16
**输入**: NOETHER_paper.tex (73 pp, 2874 lines)
**输出**: NOETHER_paper_imrad.tex (73 pp, 2906 lines after 5 edits)
**备份**: NOETHER_paper_pre_imrad.tex (md5: a561e05a86285532a21ee76dcf3363c3)
**脚本**: scripts/imrad_restructure.py

## 新结构（达成 IMRaD）

| 新章节 | 来自 | 内容 |
|---|---|---|
| §1 Introduction | 原 §1 (L120-233) | 4 contributions + Figure 1 |
| §2 Background and related work | 原 §2 (L234-309) | 5 sub-sections |
| **§3 The NOETHER framework** | 原 §3+§4+§5+§6.1-§6.5+§6.7+§6.8 | 论点集中：8-block + CONSTRUCT-MP + Th 1, 2 + 3 instantiations + Th 1' falsification |
| **§4 Empirical evaluation** | 原 §6.6+§7+§8.2+§8.3 | 实验集中：case study + L*-blindness + METRIC+ |
| **§5 Threats to validity and limitations** | 原 §8.1+§8.4+§8.5+§8.6 | 威胁集中 |
| §6 Conclusion | 原 §9 | 不变 |
| Appendix C Proofs | 原 App C | 不变 |

## 编译验证

| 检查项 | 结果 |
|---|---|
| xelatex 退出码 | 0 (成功) |
| pages 输出 | 73 pp |
| undefined references | **0** |
| multiply-defined labels | **0** |
| undefined citations | **0** |
| bibtex "didn't find" | **0** |
| em-dash (U+2014) | **0** |

## 论点保鲜核查（vs 原文）

| 关键短语 | 原文 | IMRaD | 一致性 |
|---|---|---|---|
| "5/6" (L\*-blindness verdict) | 5 | 5 | ✓ |
| "two pairwise-independent" | 1 | 2 (+1 在新 §3 intro) | ✓ 增强 |
| "McNemar" | 27 | 27 | ✓ |
| "p = 0.625" / "p=0.625" (Path A PIT) | 3 | 3 | ✓ |
| "bidirectional" (Major asymmetries) | 1 | 1 | ✓ |
| "two-layer" framework | 3 | 3 | ✓ |
| "Set~N is" (head-to-head disclosure) | 9 | 9 | ✓ |
| "Path A" (METRIC+ pre-registered) | 3 | 3 | ✓ |
| "555" (Major mutants) | 3 | 3 | ✓ |
| "L\*-blindness" | 30 | 32 (+2 在新 §3/§4 intros) | ✓ 增强 |

## 表/图/Theorem 保鲜

| 类型 | 原文 | IMRaD | 一致性 |
|---|---|---|---|
| Tables (\\label{tab:...}) | 18 | 18 | ✓ |
| Figures (\\label{fig:...}) | 1 | 1 | ✓ |
| Theorems (\\begin{theorem}) | 2 | 2 | ✓ |
| Propositions (\\begin{proposition}) | 2 | 2 | ✓ |

## 重构机制

脚本 `imrad_restructure.py` 完成的核心操作：

1. **块抽取**：按 1-indexed 行号边界切分原文为 17 个语义块
2. **选择性降级**：
   - `\\section` → `\\subsection`（对 prelim/framework/boltz/equi/empirical 块）
   - `\\subsection` → `\\subsubsection`（同上块的子节）
   - rdb/negative/threats_4/metric/pmcm/practical/artefact/human 保持 `\\subsection` 不降级（它们将成为新章节的直接子节）
3. **章节头注入**：
   - 新 \\section{The NOETHER framework} + \\label{sec:noether-framework}
   - 新 \\section{Empirical evaluation} + \\label{sec:empirical-evaluation}
   - 新 \\section{Threats to validity and limitations} + \\label{sec:threats-limitations}
4. **chapter intro 段落写入**：每个新章节配 100-180 字符的引言，指引读者到子节

## 后续修复（5 处 Edit）

脚本生成后，5 处 Edit 修复了 undefined references：

1. §1 (L137): `\\ref{sec:discussion}` → `\\ref{sec:threats-limitations}` （discussion 章已删除）
2. §1 (L231): 重写 paper-organization 段为新 IMRaD 结构
3. §3 intro: 替换 8 个 invented labels 为已存在的 `sec:prelim`, `sec:framework`, `sec:reactor`, `sec:cross-domain` 等
4. §4 intro: 替换 invented labels 为 `subsec:case-study`, `sec:empirical-vs-sota`, `subsec:pooled-headtohead`, `subsec:metricplus-relationship`
5. §4.6 METRIC+: 添加 `\\label{subsec:metricplus-relationship}`

## 论点未漂移

按 docs/restructure/argument_preservation.md 7 论点核查清单：

- [x] C1 (two-layer): 措辞保留 (3 次)
- [x] C2a (Th 1, 2): 2 个 theorem 完整保留；tab:complexity 在新 §3 内
- [x] C2b (Th 1' falsified): 2 个 propositions 保留；tab:five-obstructions 在新 §3
- [x] C3 (systematisation): tab:refinement 在新 §3 (Boltzmann instantiation)
- [x] C4 (3 instantiations): A_Boltz / A_equi / A_rel 均在新 §3
- [x] H L*: 5/6 + McNemar p 值 + "Set N dominated" + 三层 reading 全部保留
- [x] H_MP: n=120/555 + McNemar p=0.625/0.211 + bidirectional + Path A 全部保留

## 下一步选项

### Phase C 候选（Tier 2 简化，~5 pp 节省）

| 候选 | 节省 | 风险 |
|---|---|---|
| tab:elementwise 12→4 MRs (Plan A) | -0.5 pp | 无 (8 移至 Supp) |
| §7.10 cost compression | -1.5 pp | 低 (H3a.3 tertiary) |
| §8.1 4 threats 合并 | -1 pp | 低 (DA form) |
| §7.5+§7.6 Witnesses 合并 | -0.5 pp | 无 |
| §8.3 PMCM table → Supp | -1 pp | 无 (C3 由 §5 强支撑) |
| §8.4 practical guidance 压缩 | -0.5 pp | 低 |
| **合计** | **~-5 pp (73 → 68)** | --- |

### Phase D 候选

- 同步更新 cover letter（length declaration 73→ 当前页数，structural breakdown）
- 删除 NOETHER_paper.tex 旧文，改名 NOETHER_paper_imrad.tex → NOETHER_paper.tex
- 删除备份 NOETHER_paper_pre_imrad.tex（用户确认后）
- 全文 grep 反模式：`v1\.0|R[1-9] adds|first.{0,30}adversarial`（CLAUDE.md C1 严禁版本化叙事）
