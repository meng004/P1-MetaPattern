# T2(Minimum-MR-SubSet)实证资产 → NOETHER 实证成熟度(G1)补强评估

> 2026-06-16 · 焦点:用 T2 仓库提高 NOETHER 的**实证成熟度**(量化考核 evaluation_rigor 4.6 / 14-15 reviewer 共识 G1)。
> 方法:2 个 subagent 深挖 T2 `experiments/ data/ runs/ submission/sections/06`,分别评证据性质与基础设施复用性。

## 0. 诚实总结论

**T2 不能"搬数据"补 NOETHER 最核心的实证 gap,但其中立 PUT substrate + 跨实现 oracle + 变异 harness 可让 NOETHER 自跑扩展实验,部分化解 G1。** 两个关键事实:
1. **T2 的每一个见证都是注入变异(injected mutation),零真实世界缺陷**——与 NOETHER 现状(构造变异)同级,搬过来**不解决** G1 最痛的"缺中立真实缺陷正面证据"。
2. **T2 是 selection(选最小子集),NOETHER 是 generation(MR 检出能力)**——T2 没有任何 NOETHER-vs-SOTA 的 detection 对比;T2 的 baseline(greedy/random-k)是 selection baseline,与 NOETHER 命题无关。

所以"提高实证成熟度"的可行路径不是搬 T2 结论(那会 salami),而是**复用 T2 的中立被测程序与变异平台,让 NOETHER 在更多域跑自己的 generation→detection 实验**。

## 1. 证据性质(全部注入变异)

| 见证 | 缺陷类型 | 跨实现真 oracle | T2 用途 | 路径 |
|---|---|---|---|---|
| OpenMC/OpenMOC pincell/xeval | 注入变异(44-48) | **是**(MC vs MOC,算法 gap 最宽) | selection,k\*=12-19 | `runs/abd-witness-metbench-pincell-*` |
| qchem-h2o(RHF) | 注入变异(6 类) | **是**(3 独立 SCF) | 非核非崩塌 k\*=9 | `runs/abd-witness-qchem-*` |
| detonation-znd | 注入变异(6×2×3) | **是**(3 数值通量) | honest collapse | `runs/abd-witness-detonation-*` |
| combustion-gri30 | 注入变异(28) | 是(Cantera vs scipy) | DEGRADED | `runs/abd-witness-combustion-*` |
| cylinder-flow / PINN / ONIX / P9 | 注入变异 | 否(单实现) | 各 regime 见证 | `runs/abd-witness-*` |
| csmith / sql / dnn †移出核心 | 分歧标签桶/输入图(非缺陷) | 部分 | external_validity | `runs/abd-witness-{csmith,sql,dnn}-*` |

**零真实世界缺陷;csmith/sql/dnn 已被 T2 自己移出核心(outside operator-algebra,违反 NOETHER scope precondition,搬入反暴露矛盾)。**

## 2. 可复用资产 → G1 补强映射

NOETHER G1 子项:(a) 只 1/3 域执行 head-to-head;(b) 唯一中立对比被 baseline 击败、缺中立真缺陷正面证据;(c) SOTA(METRIC+/MR-Scout)未执行;(d) 样本欠功效。

| T2 资产 | 补 G1 哪项 | 复用方式 | ROI | self-overlap |
|---|---|---|---|---|
| **14 个科学计算 PUT 适配器**(p1–p10 + PINN,`experiments/puts/`) | **(a) 主 + (d)** | 复用代码,NOETHER 在每域跑算子代数生成 MR → harness 评 detection,域 1/3 → 10+ | **最高 ROI / 最低风险** | 🟢 低(共享 PUT pool 是惯例) |
| **OpenMC/OpenMOC 跨实现差分**(`scripts/mcmr/metbench_put/run_xeval_study.py`) | **(b) 部分** | 用两独立实现的差分当**真 oracle**(非注入变异),验证 NOETHER 导出的 reactor MR 检出真实算法差异 | **高**(唯一能触及子项 b 精神:跨实现差分比注入变异更中立) | 🟡 中(须 NOETHER 自跑 detection,非 T2 的 selection;cover letter 披露) |
| **committed pin-cell 检测矩阵**(920 行带 Wilson CI,`data/raw/_metbench_pincell/`) | (d) | 作 detection 数据审计 reactor MR(runtime-free,免重建 OpenMC) | 中 | 🟡 中(矩阵中立,但 T2 的 k\*/collapse 判定禁搬) |
| **qchem RHF substrate**(3 SCF + 6 MR) | **(a)** | NOETHER 加一个全新非核算子代数域(量子化学) | 高 | 🟢 低(PySCF 公开) |
| **多-LLM MR 生成+评级流水线**(`scripts/llm/multi_llm_pipeline.py`) | (c) 部分 + (d) + 方法学 | 复用代码:LLM-MR 作对比 arm + Fleiss κ/n<10 sanity gate 解欠功效诚实标注 | 中 | 🟡 中(重生成自己的 MR,不搬 `_eval` 结论) |
| **`_mr_corpus` S7(84 PWR MR 带元模式标签)/ S6(triviality 真值)** | (d) + 输入 | 直接用作 NOETHER 元模式分类金标准对照 | 中 | 🟢 低(文献抽取,注明来源) |
| **kill-matrix schema + 验证器**(`abd_structure.py`,含 `mr_meta_pattern` 列) | 横切 | 复用工程约定 | 低 | 🟢 低 |

## 3. T2 不能补的 gap(诚实)

| G1 子项 | T2 能否补 | 原因 |
|---|---|---|
| (b) 缺**真实缺陷**正面证据 | ❌ 不能 | T2 零真实缺陷,全注入变异 |
| (b) head-to-head 被 GP 击败 | ❌ 不能 | T2 无 generation/detection 对比;其 baseline 是 selection baseline |
| (c) METRIC+/MR-Scout 比较 | ❌ 不能 | T2 完全未执行这些(全仓仅 review doc 提及,bib 无条目),NOETHER 须自建执行器 |

**额外发现(已核查,2026-06-16)**:
- `experiment/s5/`(主实验)的 head-to-head 数据(8–10 个 algebra-rich SUT,n=62/70 mutants)+ commons-math pilot + L\*-blindness + per-block + κ **已写进论文 §empirical**——**无未用增量**(修正先前"可能比论文更全"的推测)。
- `experiment/s5_aligned/`:NOETHER Set N vs GenMorph Set G 在 **GenMorph 自己发表的 23-subject 公开 benchmark**(Math10+Lang5+Guava8,557 mutants,71 NOETHER MR,单变量设计)上的对比,**设计/代码就绪但 `results/` 为空 = 未执行**。这是化解 reviewer G1"单一代码库 / 作者自选 SUT / substrate selection bias / 外部效度"批评的**最高 ROI 中立证据**(在对手公开 benchmark 上比),仅需执行(Stage1 reproduce ~4–7h + Stage2 evaluate ~30min),**不需新设计**。
- **诚实**:s5_aligned 结果未落盘,不可声称已有;这是"就绪未跑"的实验,需真实执行。

## 4. 红线 + 披露(与 memory `noether-t2-salami-boundary` 一致)

- ⛔ **禁搬**:T2 的 k\*/reduction/domination 数据、collapse/trichotomy(R1-R3)judgement、见证表(27 行 register)、A/B/D claim ledger、`_eval` 对 T2-MR 的评分结论、support-domination 定理/NP-hard/FPT。一律 `\cite` 作 companion。
- ✅ **可复用**(惯例,Defects4J/Papadakis 先例):公开第三方被测程序(OpenMC/OpenMOC/PySCF/Cantera)、PUT 适配器代码、MetBench 变异 harness、多-LLM 流水线代码、kill-matrix schema、`_mr_corpus` 文献语料。
- **同一份 kill matrix:T2 问"最小覆盖子集多大"(selection),NOETHER 问"算子代数导出的 MR 是否充分检出"(generation)——矩阵/harness 可共享,问题与结论各自独立。**
- 即便复用 substrate,因同作者群同主题,**必须在 cover letter 主动披露共享实验基础设施**,否则从"未声明"升级为实质重叠。

## 5. 推荐路径(按 ROI × 风险)

1. **最高 ROI**:复用 14 个科学计算 PUT + qchem,让 NOETHER 在多域跑 generation→detection,域执行从 1/3 → 多域(化解 G1-a)。须 NOETHER 自跑 + 引用上游 + cover letter 披露。
2. **最中立证据**:用 OpenMC/OpenMOC 跨实现差分当真 oracle 验证 reactor MR 检出能力(部分化解 G1-b,比注入变异更可信)。
3. **欠功效诚实化**:复用多-LLM 流水线的 Fleiss κ + n<10 sanity gate + Wilson CI 机制(化解 G1-d 标注)。
4. **先核查自有 s5**:GenMorph arm 已在本地,优先把 s5 数据充分写进论文,可能立即提升 evaluation_rigor。
5. **METRIC+/MR-Scout**:T2 无现成,NOETHER 须自建(或在论文中如实保留为 future work,收缩主张)。

**硬结论:T2 对 NOETHER 实证的价值是"提供中立 substrate 让 NOETHER 自跑扩域/跨实现 oracle 实验",不是"提供可搬的实证结果"。真实缺陷正面证据与 SOTA detection 比较仍需 NOETHER 自己产生,T2 帮不上。**
