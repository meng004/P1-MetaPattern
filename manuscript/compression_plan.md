# 正文压缩方案 — NOETHER → TOSEM Fast Impact (≤45pp 正文)

> 目标:正文 §1–§8 从 **~75pp → ~45pp**(削 ~30pp)。日期:2026-06-25。
> 本文件仅为**方案**,经作者拍板后再执行。未改正文。

---

## 0. 目标期刊约束(venues/TOSEM.md)

| 项 | 约束 | 对本方案的含义 |
|---|---|---|
| **Fast Impact track** | **≤45pp 正文,不含 bib** | 45 页 = 正文(§1–§8),**不算 References** |
| Appendix > 1 页 | 仅进 ACM DL online 版;**投稿/审稿 PDF 仍含完整 Appendix** | **搬到附录的内容不计入 45pp 主体限**,且审稿人仍能看到 → 首选"搬"而非"删" |
| Fast Impact 定位 | "成熟、限定 scope";review ≤180 天 | 与本文"主张 MR-identification、次要材料明确标 secondary"高度契合 |
| documentclass | `[acmsmall,screen,anonymous,review]` | review 版双倍行距;最终页数以该配置编译为准 |

> **核心原则:RELOCATE > DELETE。** 论文自身已把 head-to-head / case study / DeepCrime pilot 明确标为
> "secondary executability checks, not the main evidence";把它们搬到附录/补充材料,既达标又**不损主张、不丢证据**。

---

## 1. 当前页面分布(91pp 编译实测)

| 区块 | 页 | pp | 性质 |
|---|---|---|---|
| §1 Introduction | 2–5 | 4 | 主体 |
| §2 Related Work | 6–9 | 4 | 主体 |
| §3.1 Operator-algebraic preliminaries | 11–12 | 2 | 理论(核心) |
| §3.1.9 Decomposition(+5 个 remark) | 13–16 | 4 | 理论(核心) |
| §3.1.10 Two-layer model | 17 | 1 | 理论(核心) |
| §3.2 CONSTRUCT-MP(+ Thm1/2 + 多 remark + 复杂度表) | 18–26 | **9** | 理论(核心) |
| §3.4 Boltzmann instantiation | 27–29 | 3 | 实例化 |
| §3.5 Equivariant ML | 30–33 | 4 | 实例化 |
| §3.6 Relational query optimisers | 34–35 | 2 | 实例化 |
| §3.7 Negative instantiation (PWR) | 36–40 | 5 | 理论(负实例) |
| §4 Experiments | 41 | 1 | 主体 |
| §5 Results 引言 + EQ1–EQ3 主证据 | 42–43 | 2 | **主证据(保)** |
| §5.2 Case study (equivariant-ML) | 44–46 | 3 | **secondary** |
| §5.2.1 DeepCrime pilot | 47–50 | 4 | **secondary** |
| §5.3 L\*-blindness(中心结果 + 旁证) | 51–56 | 6 | 中心实证(部分保) |
| §5.3.7 **Head-to-head** (11 段) | 57–71 | **15** | **secondary(自述非 load-bearing)** |
| §5.x METRIC/PMCM/IBT 实证 | (混入 5.x) | ~ | 混合 |
| §6 Threats & Limitations | 72–74 | 3 | 主体 |
| §7 Future Work | 75 | 1 | 主体 |
| §8 Conclusion | 76 | 1 | 主体 |
| §9 Data & Artifact Availability | 77–78 | 2 | (保,不算主体亦可) |
| Appendix(Detailed tables / Proofs / Negative proofs C.6) | 79–87 | 9 | 附录(online DL) |
| References | 88–91 | 4 | **不计入 45pp** |

> 正文(§1–§8)≈ **75pp**。

---

## 2. 削减杠杆(按收益排序)

### L1 — §5.3.7 Head-to-head:15 → 4pp(**省 ~11pp,最大单块**)
论文自述:"The head-to-head is **not** the framework's load-bearing claim"。
- **主体保留**:Scope-of-comparison tcolorbox(1 段)+ 聚合判决一句 + `tab:two-stratum` + **Fig N4**(per-MetaPattern)+ H3a 三句结论。
- **搬到 Appendix/补充**:H3a.1/H3a.2/H3a.3 逐项详证、cost-axis 分析、comparator-scope-and-three-SOTA 段、pooled-vs-D1/D2 分层细节、per-SUT delta、`tab:per-block-headtohead`(已在附录可引)、`tab:gen-cost`。→ Appendix E(新)/ 补充 S5、S9。

### L2 — §5.2 + §5.2.1 Case study + DeepCrime pilot:7 → 2.5pp(**省 ~4.5pp**)
两者均 "secondary executability check"。
- **主体保留**:`tab:case-study` + H2 verdict(construct-validity-controlled 一段)+ "framework boundary: wrong-sign 0/5" 这一最有信息量的格 + pilot 一句(n=5 underpowered,descriptive)。
- **搬到补充**:pre-registered H1/H2 全文、interpretation-conditions 列表、threats(a)–(e)、comparative-evaluation protocol、pilot 机制段、tau-sweep。→ 补充 S3。

### L3 — §3.2 CONSTRUCT-MP:9 → 5pp(**省 ~4pp**)
核心理论,**主张本身保留**,削的是证明与旁注。
- **主体保留**:Definitions(component invariant / Translate / algebra-induced MR)+ CONSTRUCT-MP 四步 + **Fig N1** + Theorem 1/2 **陈述** + 一段 closure 的"非平凡性"说明。
- **搬到 Appendix**:Theorem 1/2 **证明**(若在正文)、复杂度逐分量 `tab:complexity` + §complexity-prose、Remark(scope-of-thm1 三类 out-of-scope 细列、closure-brel、decidable-brel、block-vs-translate)。→ Appendix B(Proofs,已存在)。

### L4 — §3.7 Negative PWR:5 → 2.5pp(**省 ~2.5pp**)
- **主体保留**:两条反例的**陈述** + 五障碍 `table`(L1113)+ "证伪 Thm1′、定位 5 扩展维度"的结论一段。
- **搬到 Appendix C.6**(已存在 `app:negative-proofs`):逐障碍 per-MetaPattern exhaustion 详证、pairwise-independence 证明。

### L5 — §5.3 L\*-blindness:6 → 3.5pp(**省 ~2.5pp**)
中心可证伪结果**全保**。
- **主体保留**:预测推导 + `tab:l-blindness` + **Fig N3** + falsification verdict + hypotSig outlier 解释。
- **搬到 Appendix**:§5.3 "Corroborating per-MetaPattern patterns"(G_tr/G/I\* 旁证)、"Two convergent witnesses"(rediscovery / coverage-extension)。→ Appendix E。

### L6 — §3.1.9 Decomposition 的 5 个 Remark:4 → 2.5pp(**省 ~1.5pp**)
- **合并**:`rem:counterex`(6 候选附加)+ `rem:domain-out-of-scope`(4 域)→ 已建的 **`tab:out-of-scope`** 承载,正文只留 2 句导引。`rem:metric-stability-block`、`rem:single-class-instances`、`rem:block-vs-translate` 压成脚注或并入 Hypothesis 1 后一段。

### L7 — §1 Intro + §2 Related:8 → 6pp(**省 ~2pp**)
- §1:删 `Boundary of contribution` tcolorbox 与 abstract/contributions 的重复(保留 contributions 列表,盒子内容下放或删);origin–closure–transferability 三问压缩。
- §2:`Comparators in the head-to-head` 段(para:comparators-and-why)移到 §4 Experiments;related-work 四线每线收 1–2 句。

### L8 — 跨节去重 + §6 Threats:3 → 2pp(**省 ~2–3pp**)
- 全文重复的 scope 套话("by-construction / not superiority / out-of-scope / construct-validity-controlled")只在首次出现处详述,后续引用而非重述。
- 140 个 `\paragraph` 微标题:合并同节相邻短段,减少标题碎片。
- §6 Threats:validity framework 表化,limitations 收口。

---

## 3. 页面预算(目标 ~45pp 主体)

| 节 | 现 pp | 目标 pp | 动作 |
|---|---|---|---|
| §1 Intro | 4 | 3 | 删 boundary 盒、压三问 |
| §2 Related | 4 | 3 | 收四线、移 comparator 段 |
| §3.1 prelim | 2 | 2 | 保 |
| §3.1.9 decomposition | 4 | 2.5 | 5 remark→表+脚注 |
| §3.1.10 two-layer | 1 | 1 | 保 |
| §3.2 CONSTRUCT-MP | 9 | 5 | 证明/复杂度/remark→附录 |
| §3.4 Boltzmann | 3 | 2.5 | 轻收 |
| §3.5 Equivariant ML | 4 | 3 | 保派生、收旁注 |
| §3.6 Relational | 2 | 1.5 | 轻收 |
| §3.7 Negative PWR | 5 | 2.5 | 详证→C.6 |
| §4 Experiments | 1 | 1.5 | +comparator 段 |
| §5 引言+EQ1–3 主证据 | 2 | 2 | **保(主证据)** |
| §5.2 case study | 3 | 1.5 | secondary→补充 |
| §5.2.1 pilot | 4 | 1 | secondary→补充 |
| §5.3 L\*-blindness | 6 | 3.5 | 旁证→附录 |
| §5.3.7 head-to-head | 15 | 4 | 详证→附录/补充 |
| §6 Threats | 3 | 2 | 表化收口 |
| §7 Future Work | 1 | 1 | 保 |
| §8 Conclusion | 1 | 1 | 保 |
| **合计** | **~75** | **~44.5** | ✅ |

> References(4pp)不计入;附录(现 9pp + 接收搬入内容)只进 online DL,不计入 45pp 主体。

---

## 4. 主体必须保留的 load-bearing 内容(压缩红线,不得动)

- 理论三柱:Theorem 1(closure 陈述)、Theorem 2(complexity 陈述)、**Invariance-Blindness Theorem**(thm:ibt 全保)。
- 两层模型(5 MetaPatterns + 10 MR families)定义 + Table 2 + Fig N2/N3 架构与映射。
- 三域实例化的**派生结论**(各留一条端到端 MR)。
- 负实例的**结论**(证伪 Thm1′ + 5 扩展维度)。
- EQ1–EQ3 **主证据**(Tables 5–7 + real-bug 矩阵 Tab N1)。
- L\*-blindness **中心可证伪结果** + Fig N3。

## 5. 风险与对策

| 风险 | 对策 |
|---|---|
| 搬走 head-to-head 详证后审稿人质疑"证据不足" | Fast Impact 审稿 PDF **仍含附录**;cover letter 注明"detailed head-to-head in Appendix E, summarised in §5.3.7" |
| 交叉引用悬空(§X.Y 移位) | 执行后跑 §15 grep audit(`§[0-9]+\.[0-9]` 悬空)+ 全编译 0 undefined |
| 删 remark 误删 load-bearing 限定 | 只**合并/下放**不**删**;§4 红线清单逐项核对 |
| 双盲/track 标注 | cover letter 显式标 **Fast Impact**;documentclass 用官方 `[acmsmall,screen,anonymous,review]` |

## 5.5 执行进度(2026-06-25,实时)

> 全程 xelatex 编译干净(0 undefined / 0 Missing character / 0 overfull>50pt),每步重指向区外引用 + 验证。

| 步骤 | 内容 | 总页 | 累计削 |
|---|---|---|---|
| 起点 | — | 91 | — |
| L1 | §5.3.7 head-to-head 15→4pp(详证→S5/S9) | 84 | 7 |
| L2 | §5.2 case study + pilot 压缩 + 删 Boundary 盒 | 78 | 13 |
| §5.4 | Relationship with METRIC 185行→~12行 | 76 | 15 |
| L5/§5.6 | §5.3 corroborating+witnesses、§5.6 IBT-empirical 压缩 | 74 | 17 |
| L6 | §3.1.9 两个 out-of-scope remark → Table N2 指针 | 73 | 18 |
| §2 | comparators 段压缩 | 73 | 18 |

**当前:73 页,正文 §1–§8 ≈ 58pp。已削全部"明确次要"材料(论文自述 secondary/not load-bearing 的部分)。**

### 剩余到 45pp(~13pp)——须动核心理论/实例化(更高风险,逐项判断)

| 来源 | 现 | 目标 | 削 | 风险 |
|---|---|---|---|---|
| §3.2 CONSTRUCT-MP | 9pp | 5–6 | ~3 | 中(保定义+Thm1/2+4步;复杂度表/brel-remark→附录) |
| §3.4–3.6 三域实例化 | ~9pp | 6 | ~3 | 中(每域保 1 条端到端 MR + 迁移结论;细派生→补充) |
| §3.7 negative PWR | 5pp | 2.5 | ~2.5 | 中高(保 2 命题+障碍表+结论;物理细描述/工程意义→附录 C.6) |
| §2 五个 related 子节 | 5pp | 3 | ~2 | 低(每子节收尾收 1–2 句,保全部 \cite) |
| §6 Threats + §1 + 跨节去重 | — | — | ~2 | 低 |

> 这些是 load-bearing 段,剪裁须逐句判断"保结论、移细节",不能机械删。

## 6. 执行顺序(经批准后)

1. 建 Appendix E(head-to-head 详证 + L\*-blindness 旁证容器)。
2. L1→L8 逐杠杆:**先搬后删**,每杠杆完一次编译 + 交叉引用 grep。
3. 全文跑 §11/§15 audit(undefined / Missing character / overfull>50 / 悬空 §ref 全 0)。
4. 编译 `[acmsmall,...,review]` 实测页数 ≤45(主体);若超,二轮收 §3.2/§5.3.7。
5. 出 cover letter(标 Fast Impact + 附录位置说明)。

---

## 7. 作者已拍板(2026-06-25)

1. **下放到附录**✅ — secondary 材料(head-to-head 详证 / case study / pilot / 证明 / 复杂度表)下放。
   - **保险策略(防 45pp 硬限把附录计页)**:**最重详证下放到已有补充材料 S-files**(S1–S12,肯定不计页);
     次重(must-be-in-PDF 的表/证明)放 in-PDF Appendix。即"补充优先,附录其次"。
2. **删** `Boundary of contribution` tcolorbox ✅(与 contributions 列表重复)。
3. **track**:推荐 **Fast Impact**(成熟+限定 scope,与本文契合,180 天周转);45pp 按硬限执行。待最终确认。

> 区别速记:Fast Impact = ≤45pp 硬限 + 180 天;Regular = 不限页 + 6–12 月。45pp 目标 ⇒ Fast Impact。
