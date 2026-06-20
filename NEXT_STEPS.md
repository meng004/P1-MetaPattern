# Next steps

This document tracks open follow-up work after the initial GitHub
commit. Each item is independent and can be done in any order.

---

## ⭐⭐⭐ TOSEM 投稿成熟度 — fresh 外部网关 + 多智能体复评 (2026-06-20)

> 首次对当前 TOSEM 重写稿跑通 fresh 外部面板：网关 5 厂商（gpt-5.5 / claude-opus-4-7[opus-4-8 限流回退] / glm-5.2 / deepseek-v4-pro / qwen3-max）= **3 Reject + 2 Major**；Claude 30-agent 对抗验证 workflow = **Major Revision / 55-100 / 接收概率 22%（清完 P0/P1→45-55%）**。
> 对抗验证：17 项 blocker/major 仅 **8 项证实为真**（9 项误读/已自界定）。完整报告：`docs/review_2026-06-20/submission_maturity_assessment_2026-06-20.md`。
> 关键洞察：冷读网关比有验证的 Claude 更狠——真实审稿人不买"self-disclosure 即免责"，提接收率须**重构叙事**而非仅修硬伤。

> **【第1轮闭环审稿 2026-06-20】** 5 隔离独立 reviewer（EIC+3peer+DA，`wf_7e1d144f-32b`）全部 **major revision**，4 个非 DA 无一达 minor（目标判据未达）。综合：`docs/review_2026-06-20/round1_review_synthesis.md`。
> **硬墙判定（决定性）**：R2/R3/EIC 达 minor 需 **experiment**（独立人类 inter-rater κ + 一条外部/独立验证腿），我做不到、需作者执行——R2 原话"cannot exceed major regardless of writing quality"。R1（形式方法）则**仅靠 writing 即可达 minor**。
> **写作上限路径**：A9 压缩~40-45页 + 理论 headline 重定位（Theorem 1 降 lemma，IBT/1′证伪 carry）+ Theorem 2 改名（complexity 非 decidability）+ EQ1 reframe 为 definitional + 平衡 contributions（非循环结果 carry）+ title discovery→systematisation + "10 dims"去headline + Zhou cite 核查。做完可让 R1 minor + 清全员 writing blocking，但 R2/R3/EIC 仍卡 experiment。

### 🔴 P0（2026-06-20 已执行，commit ca3f333；构建 80pp/0 undef/0 missing）
- [x] **B1 数据完整性**：Set L 覆盖 `0.40`→`0.20`（arxiv 3 处 + 改假"G and L\*"为只达 G）；analysis.py 重算确认 0.20、H1 仍 HOLDS。submission/(gitignore 派生快照)本地同改，待整体重生。
- [x] **B4 κ 误报**：移除 SSOT 不支持的 Fleiss=1.000/n=33，改报 majority-vs-author Cohen's κ=0.931（n=36,34/36）+ per-rater 0.927/0.927/0.929 + 命名 2 分歧（L_idem_at_one、B_rel_xor_reverse）。
- [x] **B3(i) lrca_audit.md**：创建 `supplementary/S3_case_study/lrca_audit.md` + 复制原始 `lrca_kappa.json`/`lrca_llm_labels.json`，引用可解析。
- [ ] **B3(ii) 18mr_audit κ=0.857（🔴 BLOCKED，需作者）**：raw labels 全仓库不存在，无法 honestly 创建/repoint。选项 (a) 定位/重导原始标注存入 S2；(b) 软化引用（"available on request"/删"released in 18mr_audit/"）。未擅自伪造或弱化。
- [x] **action2**：跨域 "six blocks"→"five blocks"（conservation 是 G 的 MR-class，非第九块）。
- [ ] **B4 复核（需作者）**：本次移除原 Fleiss=1.000 perfect-agreement 表述；若另有真实 Fleiss 计算请确认是否回填。
- [ ] **submission/ 重生（需作者）**：submission/ 为 gitignore 派生快照；relabel/six-blocks/B4 未进快照，投稿前从修正后 arxiv 整体重生。

### 🟢 MVP 扩张方案 + 执行物（2026-06-20，路径：补实验重投 TOSEM 1区，兜底 IST）
> 完整方案 `docs/review_2026-06-20/mvp_expansion_plan.md`；缺口诊断 `sacos_gap_diagnosis.md`。诚实概率：完整 MVP 后 TOSEM 达 4-minor ≈ 15-30%；更可能第二轮 major+再 R&R；IST 兜底净收益正。
- [x] **MVP 两份执行物已就绪（已逐字核对真实性）**：
  - `docs/review_2026-06-20/mvp_s5_aligned_multiseed_runbook.md`（s5_aligned 多-seed 云执行包，CPU-only，含预注册分层假设防 HARKing + 对齐验证 + 回报模板）
  - `docs/review_2026-06-20/mvp_kappa_codebook.md`（独立人类 κ 盲标 codebook：8-block 判据卡 + 41 条待标 MR[逐字来自 lrca_llm_labels.json 36 条 + SACOS 5 锚] + κ 计算 + 诚信约束）
- [ ] **B 阶段 — 需用户提供**（最小可信组合）：(1) Ubuntu 云主机 ≥30GB+egress 放行 zenodo/apt/maven（无需 GPU）；(2) push `experiment/s5_aligned` 到私有 repo（remote 已配 meng004/S5_aligned_experiment）；(3) 2 名独立 rater（非作者）。
- [ ] **A 阶段（后做）— writing 修复**：A9 压缩≤45页 / 理论 headline 重定位 / EQ1 reframe / 平衡 contributions / abstract SCP→TOSEM framing（用户已选先 B 后 A）。已完成：title discovery→identification、Theorem 2 改名（complexity）、A6 文献、A14 GenAI 披露。

### 🟢 A 阶段工业资料整合（2026-06-20 已执行；评估 `docs/review_2026-06-20/industrial_assets_assessment.md`）
> 编译验证：exit 0 / 0 undef refs（6 处 undefined 全为字体回退 cosmetic）/ 0 missing-char / 0 overfull>50pt / bibtex 0 didn't-find / 75 cited=75 defined / 82pp。
- [x] **P0 破"全 order 单块"**：§Out-of-construction(i) + Expert-monotonicity 段加 LOCUST 非-order 例外（guard-conditioned MTC-vs-boron 接 \S negative-pwr 作 ρ_MTC-bor 工业 witness + burnup-sensitivity）；"all 110"→"large majority"；"subsumed without exception"→"with few exceptions"（消解与 Wilson[0.966,1.000]/LOCUST 例外的内部矛盾）。诚实定位：LOCUST 非-order 是 Translate-unreachable **障碍**（支撑 C2b 边界），非 block-diversity 覆盖。
- [x] **P2 破"作者自实现 substrate"**：§Construct-validity 追加开发/测试分离独立性段——SACOS/SPARK/LOCUST 由作者外的反应堆物理工程团队开发、作者为独立第三方 V&V 方，工业 subject 侧 implementation-fidelity 与 framework-design 解耦；诚实残留：MR 识别+block 标注仍作者方（独立人类 κ 控制 labelling）、域集中（cross-domain 另述）。**不宣称"MR 独立"**。
- [ ] **P1 华能三程序（HTGR）扩张 — 开放决策（需用户拍板）**：耦合/热工/事故（NUSOL，44 MR，HTGR 氦冷，2025 v1.x 新软件）未注入正文/未入 S11 SSOT。注入前需 (a) MR 逐字提取入 supplementary S11；(b) HTGR↔PWR 跨堆型可比性用 governing-eq（能量守恒）论证；(c) DO NOT：SPARK+LOCUST 不算两独立点、non-order/breadth 不进 Abstract、引用非导入防 salami。**当前未注入**——三个核安审码已交付两个最高 ROI 赢点（P0+P2），华能三程序为边际 breadth + 较高 framing 风险，待用户决定是否做。

### 🔴 fix_plan 补充（对抗验证 + 人工核验新增，`docs/review_2026-06-20/fix_plan_2026-06-20.md`）
- [x] **A0-sec §5 敏感信息（已执行 2026-06-20）**：shipping 数据文件（`supplementary/S3_case_study/lrca_kappa.json`/`lrca_llm_labels.json`）与 `docs/review_round_polish/round2/rereview_report.md` 的代理商厂商标识已 scrub 为中性名（厂商=Anthropic Opus）；§5.B.2 复扫 tracked 树 0 命中（除 RELEASE_CHECKLIST 扫描器正则）。⚠️ 该标识曾随 ca3f333 进公开 repo 历史，因属代理商**名称**非凭据，未做历史改写——如需彻底清除可 force-push（破坏性，属作者决策）。
- [~] **A5 理论 headline 重定位（B1–B7 遗漏，三轮收敛核心）**：Theorem 1/2 降格为 closure lemma / 复杂度附属，IBT + Theorem 1′ 证伪提为 headline（残留 over-headline 仅 L207-212 图 / L270-271 box / L391 roadmap；Abstract 已对齐）。零新证明（IBT/Thm1′ 证明已在 `theory/` + Appendix C.6）。红线：禁在 response letter 计为 significance 实质回应
  - [x] **Theorem 2 术语一致性（2026-06-20 已执行）**：定理已改名"Complexity"且 L617 statement 自述"complexity bound rather than a decidability result"，但全文 ~14 处仍称"polynomial-time decidability"——内部矛盾，且正中 gpt-5 Reject 理由"Theorem 2 vacuous as decidability"。统一改为 polynomial-time **constructibility**（"holds/preserves/theorem" 语境）/ **complexity**（"bounds the complexity"/proof header/§heading）。保留 L617 disclaimer + L620-622 query-equivalence 的合法 (un)decidable 用法 + 内部 label `thm:decidable`（不可见）。编译 exit0/0undef/0missing/0overfull>50pt/82pp。
  - [ ] **剩余（author-judgment）**：把 Theorem 1 显式降格为 lemma 属叙事重构（C2a 当前已自述"intentionally modest, well-formedness guarantee"，contributions C2b=Thm1′证伪/C2c=IBT 已 prominent）——是否进一步降格留作者拍板，不擅自重构。
- [ ] **B2 压缩护栏**（执行 B2 时强制）：GenMorph 败局 McNemar p=0.0043 + "dominated by Set G" 须留主文（L1855 box 不可降 cross-ref，它唯一承载该定量披露）；欠功效 underpowered 标注 + L\*-blindness "derivable without data" 限定移 supplement 后须保留——否则即 §6.4/§10.7 visibility-laundering
- [ ] **A15 补建脚本**：`scripts/bib_all_cited_check.py` 实际不存在（CLAUDE.md §3 引用它），须新建

### 🟡 P1（2-3 周，最大天花板）
- [~] **B2/A9 篇幅压缩（2026-06-20 停在 81 页，用户决策"停 A9 转绑定约束"）**：方案 `docs/review_2026-06-20/a9_compression_plan.md`。**实测关键发现：表迁移≈每个省 1 页，页数由 verdict 散文主导，非表格**。已做：DeepCrime contingency 表删 + METRIC+ 3 表迁 S8（commit 746e046），82→81。剩余可迁表 per-block-headtohead(7ref)/gen-cost(6ref)/two-stratum(5ref) 高引用、各仅省 1 页、ROI 差。**温和表迁移地板≈75 页，到不了 60-65；60-65 必须压 verdict 散文（撞 B2 护栏，已否决）**。结论：篇幅非 blocker，停在 81，精力转绑定约束（实验）。如日后要继续，只剩压散文一条路。
  - **反漂移核查（事后补，2026-06-20）**：对照 `rq_plan_anchor.md` D1-D7 逐条核本轮全部改动（工业整合 P0/P2 + Theorem 2 一致性 + DeepCrime/METRIC+ 压缩）→ **全部通过，无主题漂移**。证据：McNemar p=0.0043 box 完整(L1833)、四条 "does not establish" 完整(L276-281)、METRIC+ verdict 留主文(9/11 L2378、6/5/3 L2392、卡数 L2431)、underpowered 标注保留。**教训：反漂移 checklist 须动手前跑，不是事后补**（已存记忆 anti-drift-check-before-revision）。
- [x] **B6/A6 最近邻文献（已补 2026-06-20，第1轮）**：6 条经 paper-search-mcp 核实的 bibtex（Gotlieb 2003/2006、Patel-Hierons 2018、Khritankov-Iakusheva 2024、Gruver 2023、Kaba 2023）入 `NOETHER_paper.bib`（69→75 条）+ §2.3 末插入 195 词对照段，delta 定位为"construction+proof over operator-block layer, not inventing the symmetry layer"；Saha-Kanewala/MemoRIA 原已引；Hu/Mariani/Liu 经核查不可定位（L321 已记录）。编译 0 undef cite。

### 🟢 P2/P3（低成本）
- [ ] **B5** Theorem 2 加一句限定（\|G\| 可指数→output-polynomial，非 input-polynomial）；abstract/intro 同步。注：当前文本已大量限定（L626 caption/L648-652 "On infinite groups"/C2a/boundary box 均带 "finite generating set"），实际缺口极小，避免 over-editing
- [ ] **B7 合规**：[x] ACM GenAI 披露段已补（2026-06-20，acks 内，引 §case-study/§threats，两类用途）；[ ] documentclass→acmsmall,review；[ ] 清双盲残留；[ ] 披露 arXiv 预印本

### ✅ 本会话已完成（relabel-only）
- [x] 2026-06-20 time-reversal 记号归一 → `\mathcal{T}^{*}_{\mathrm{rev}}`（33 处，0 残留；对抗验证确认"不一致"现为 false）
- [x] 2026-06-20 Conservation 第九标签调和（§3.1 L469 加定义句，数值未动）→ EIC 确认"reconciled at L469"

---

## ⭐⭐ TOSEM 投稿成熟度 — 多 LLM 网关评审裁决 (2026-06-17)

> 5 跨厂商 LLM（gpt-5 / claude-opus-4-6 / deepseek-r1 / glm-5.2 / kimi-k2-instruct）网关评审 + 30-agent 对抗验证 Workflow（triage → 逐议题对照原文验证 → §10 ARS 五维 → EIC 裁决）。
> 裁决：**Major revision before submission**；**0 存活 publication blocker**（23 归并议题中 17 误读/夸大 · 4 major · 2 minor）。
> 详见 `docs/review_2026-06-17/submission_maturity_assessment_2026-06-17.md`。

### 🟡 In Progress
- [ ] **ISS-7 记号冲突修复（最高优先，relabel-only，本会话执行中）** — 实证章节把 `\mathcal{T}^{*}`/裸 `T^{*}` 用于 translation/period，并引入未定义的 `\mathcal{I}^{*}`（idempotence）块，与 L454 规范分类（`T^{*}`=self-adjoint、`\mathcal{T}^{*}`=time-reversal、`\mathcal{B}^{*}_{\mathrm{rel}}`=relational）冲突，使头条 per-block "Set N edge" 比较不可解读。映射：translation→`G` 子情形；time-reversal 全程统一 `\mathcal{T}^{*}_{\mathrm{rev}}`；未定义 `\mathcal{I}^{*}`→`\mathcal{B}^{*}_{\mathrm{rel}}`。**不动任何数值、不动 "MetaPattern" 用法。** ⚠️ 含一个待作者判断点：headline n=17 行测的是 translation-under-G 还是 time-reversal。

### 🔴 Must-fix before submission（其余 8 项，按 EIC 优先级）
- [ ] 2. **ISS-8 篇幅压缩**（82pp/~45.6k 词 → TOSEM 规范）：Boundary box 4→1（保 L259，其余转 cross-ref）；头条统计量（McNemar p=0.0043、D2 6.9%）各报一次；删 `theory/ibt_section_3_4.tex` L2-4 过期注释 + 3 处 `% TODO-ref`；重跑 xelatex
- [ ] 3. **ISS-2 实证定位**：实证章节起始（~L1057）加一句明确定位为 instantiation/falsifiability 探针（非 powered utility benchmark）；GenMorph 压制 + 底物异构上浮为单一具名 limitation 到 Threats/Boundary box
- [ ] 4. **ARS 方法论 A+B**：LLM 判等投票加小规模人类金标验证（混淆矩阵/FP/FN/κ）+ 延伸共享训练数据 caveat；预注册/论证 D1→D2 "(e.1) v2 override" 规则 + 报告无 override 敏感性分析（最强 Reviewer-2 杠杆）
- [ ] 5. **ARS 统计**：3 块 per-block 族显式陈述多重性 + T* edge 保持 directional-only；case-study N-vs-B/N-vs-L 应用 Bonferroni 或说明；L*-blindness outlier-rescue 事后性整合进 Threats
- [ ] 6. **ISS-11 METRIC+**：软化 "unambiguously strengthens"（L2499）+ 调和 L2236（称未跑）与 L2449+（称已跑）矛盾
- [ ] 7. **benchmark 公正性**：加一段组合公正性段落（home-field 底物 + 单 GP seed=11 + NOETHER 定义指标一起对待）+ 至少跑 multi-seed GP
- [ ] 8. **ARS 外部效度**：收紧 Abstract/C4，使 home-field 多块增益（29/47）不被读作单块工业证据（110 SPARK/LOCUST/SACOS MR 全为 order/O_le）佐证
- [ ] 9. **ISS-20 + ISS-23（minor，低成本）**：加量化摊销 break-even（共享 A_P 的 SUT 数）+ 调和 10h 两种读法；Def 5（L521）补 "relabelling"=坐标-索引置换的一句话定义

### 🟢 不要返工 — 对抗验证驳回的误读（保护作者）
- [ ] （参考，勿动）ISS-1/3/5/6/9/10/12/13/14/15/16/17/18/19/21/22 经对照原文核验为误读/夸大——论文当前文本已自述这些边界（含 5 模型共识的 "Theorem 1 同义反复" 与 gpt-5 Reject 所依据的 "Theorem 2 vacuous"）。逐条理由见报告 §5。

---

## ⭐ TOSEM submission readiness — independent maturity review (2026-06-16)

> 6 个互相隔离的 Opus subagent 独立重审,综合裁决 **Major Revision**(评分 38–72),显著低于仓库 Round-4 自评(Accept / 65–75%)。
> 详见 `docs/tosem_maturity_2026-06-16/maturity_review_summary.md`。

### 🔴 Blockers(投 TOSEM 前必解,多数需投入实验)
- [ ] 理论内核偏平凡 + CONSTRUCT-MP Step 3/4 定义级 bug(L529-530);最强定理 Thm 1′ 被自证伪 — 补非平凡定理或改论文类型为 systematisation
- [ ] 唯一真实 head-to-head 被 baseline 显著击败(McNemar p=0.0043) — 需中立真实缺陷上的正面证据点,或收缩 fault-detection 主张
- [ ] 缺独立**人类** inter-rater κ(κ=1.000 是共享语料 LLM 循环) — 自招 ≥2 名独立 rater 做 Cohen's κ
- [ ] 与姊妹论文 T2(Minimum-MR-SubSet,TSE)的 salami 未声明 — 草稿已备(见下)
- [ ] 大量经验主张是 protocol 非 result;"three domains tested" overclaim — 如实分级或补执行

### 🟡 草稿已备 / 进行中(零实验成本)
- [x] 删 4 处 reviewer-process 残留 — 主稿 `NOETHER_paper_arxiv.tex` 已改(2026-06-16)
- [ ] 同步删除投稿版残留:`submission/TOSEM_2026-05-20/manuscript_singleblind/` + `manuscript_anonymized/` + 06-16 singleblind humanized zip
- [ ] 插入 T2 differentiation 段 + cover letter 披露 — 草稿 `docs/tosem_maturity_2026-06-16/differentiation_and_disclosure_draft.md`(待确认插入位置)
- [ ] 去 overclaim(标题/摘要/contributions) — 草案 `docs/tosem_maturity_2026-06-16/overclaim_revision_draft.md`(待用户拍板,属作者决策权)
- [ ] 75 页压至 ≤50 + cover letter 篇幅辩护
- [ ] **执行就绪的 `experiment/s5_aligned`**(NOETHER vs GenMorph,在 GenMorph 公开 23-subject benchmark / 557 mutants)——化解 G1 substrate-bias 的最高 ROI 中立证据;代码就绪、`results/` 空待执行(Stage1 ~4–7h + Stage2 ~30min);见 `docs/tosem_maturity_2026-06-16/protocol_domain_extension.md`

### 🔵 Open questions(待用户拍板)
- [x] git 作者邮箱已更正为 `meng004@gmail.com`(2026-06-16;gamail 未进任何 commit,无需修历史)
- [x] 多厂商交叉评审已完成(网关 5 厂商:gpt-5 / grok-4.1 / deepseek / qwen / kimi → 2 Reject + 3 Major,确认 Opus panel;`docs/tosem_maturity_2026-06-16/gateway_panel_raw.json`)
- [ ] 100% 联网逐条 bib 真实性校验(见 §C)尚未执行 — 投真实期刊前 hard-block

---

## A. arXiv preprint upload (when ready to publish)

Status: `arxiv/` directory contains a preprint-ready variant. Author
metadata is left as placeholders so the manuscript stays anonymous in
the repository until the user is ready to de-anonymise.

**Steps**:

1. Open `arxiv/NOETHER_paper_arxiv.tex` and replace the three
   placeholders with actual author information:

   ```tex
   \author{<AUTHOR_NAME>}
   \affiliation{%
     \institution{<INSTITUTION>}
     \city{<CITY>}
     \country{<COUNTRY>}
   }
   \email{<your_corresponding_email>}
   ```

   Add additional `\author{...}\affiliation{...}\email{...}` blocks per
   co-author if applicable.

2. Build & verify:

   ```bash
   cd arxiv && ./build_arxiv.sh
   ```

   Expected: `NOETHER_paper_arxiv.pdf` produced; 0 undef refs;
   0 missing characters.

3. Bundle source for arXiv upload:

   ```bash
   cd arxiv
   tar czf noether_arxiv_source.tar.gz \
     NOETHER_paper_arxiv.tex NOETHER_paper.bib NOETHER_paper_arxiv.bbl
   ```

4. Upload at <https://arxiv.org/submit>. Suggested categories:
   primary `cs.SE`, cross-list `cs.LO` and (optionally) `cs.AI`.

5. After arXiv assigns a DOI, update the citation block in `README.md`
   and add the arXiv ID to the `Citing this work` section.

---

## B. Bibliography polish (78 bibtex warnings)

Status: paper builds cleanly (0 undef refs, 0 missing chars). The 78
bibtex warnings are all "missing publisher / address / page numbers"
on conference and journal entries. They do not affect rendering but
are flagged by some venues' submission systems.

**Steps**:

```bash
# List all warnings to see which entries need polishing
bibtex NOETHER_paper 2>&1 | grep "Warning--" | sort -u | head -40
```

For each entry: open `NOETHER_paper.bib`, fill in the missing field
(publisher / address / pages / numpages) from the canonical source.
Re-run the pdflatex chain to verify warnings drop.

Lower priority — not a publication blocker.

---

## C. Reference verification audit (CLAUDE.md §3 步骤 2 + D1)

Status: not run for the current bib state. CLAUDE.md mandates a
paper-search-mcp-driven audit before submission.

**Steps**:

1. Parse `NOETHER_paper.bib` into a checklist (53 entries).
2. For each entry, route through:
   - `mcp__paper-search__get_crossref_paper_by_doi` if DOI present
   - `mcp__paper-search__search_crossref` (title + first author)
   - `mcp__paper-search__search_arxiv` for preprints
   - `mcp__paper-search__search_dblp` for SE / top-tier conference
   - `mcp__paper-search__search_openalex` / `search_semantic` /
     `search_google_scholar` as fallback
   - `WebFetch` for textbooks / standards / GitHub repos

3. Output `docs/review_round{N}/reference_verification.md` with
   ✓ / △ / ✗ per row.

4. Pass gate: ✗ = 0; △ ≤ 5 with explanation.

Required before any real venue submission (TOSEM, IST, etc.). Not
required before arXiv upload (arXiv does not enforce reference
verification).

---

## D. P-series follow-up

The repository is part of a `P1`–`P5` programme of papers (see
`CLAUDE.md` §5). NOETHER corresponds to P4 (formal theory). Adjacent
work threads, not started here, include:

- **P3** — industrial Java / C++ port + LRCA (two-rater κ)
- **P5 / P2-CN** — regulatory translation (IEC 60880, ISO 26262,
  DO-178C); Chinese version under review

These are independent of the GitHub release of P4 / NOETHER and live
in their own repositories or sibling project directories.

---

## E. PDF rebuild after future `.tex` edits

The current PDF is up to date with `NOETHER_paper.tex`. Future edits
require re-running the chain:

```bash
pdflatex -interaction=nonstopmode NOETHER_paper.tex
bibtex NOETHER_paper
pdflatex -interaction=nonstopmode NOETHER_paper.tex
pdflatex -interaction=nonstopmode NOETHER_paper.tex
```

Verification:

```bash
echo "Undef:  $(grep -cE 'Reference.*undefined|Citation.*undefined' NOETHER_paper.log)"
echo "MissCh: $(grep -c 'Missing character' NOETHER_paper.log)"
echo "Pages:  $(pdfinfo NOETHER_paper.pdf | grep ^Pages | awk '{print $2}')"
```

Expected: Undef 0, MissCh 0, Pages 40.

If TeX Live is missing fonts, see `REPRODUCTION.md` §8.
