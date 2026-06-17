# NOETHER 投稿成熟度评估报告（多 LLM 网关评审 + 对抗验证 + ARS）

> 日期：2026-06-17
> 评审对象：`NOETHER_paper_arxiv.tex`（arxiv 主稿，含今日 bib/cite 修订；评审时自动展开 `\input{theory/ibt_section_3_4.tex}` 为自包含全文，351,276 字符）
> 目标期刊：ACM TOSEM
> 方法：OpenAI 兼容网关并行调用 5 个跨厂商 LLM 模拟独立 TOSEM 审稿人 → Workflow 编排（归并去重 → 逐议题对照原文对抗验证 → §10 ARS 五维独立扫描 → EIC 综合裁决）
> 计算量：评审脚本 5 模型并行；综合 Workflow 30 个 agent、~2.97M tokens、13 分钟

---

## 0. 执行摘要

| 项 | 结论 |
|---|---|
| **成熟度裁决** | **Major revision before submission（重大修改后可投）** |
| **存活的 publication blocker** | **0** |
| Panel 原始裁决 | 1 Reject (gpt-5) + 4 Major Revision |
| 23 个归并议题对抗验证 | 17 误读/夸大 · 4 major-fixable · 2 minor · **0 blocker** |
| ARS 五维（22 findings） | **0 独立 blocker** |
| 最高优先修复 | **ISS-7 记号冲突**（relabel-only，使头条 per-block 比较当前不可解读） |
| 目标期刊建议 | 非现在投 TOSEM；完成下列重大修改后投 TOSEM |

**一句话**：论文实际状态远好于 "1 Reject + 4 Major" 的原始分数所暗示——对抗验证显示 14 个 panel "blocker" 中 13 个描述的是一篇"已不存在的论文"，因为当前正文已用自己的话承认、降级并预先回应了这些关切（往往比审稿人要求的更诚实）。真正的问题是一簇**可修复缺陷**（记号冲突、实证定位、统计卫生、篇幅），而非 soundness 失败。作者**不应**去追那 13 个被驳回的误读。

---

## 1. 方法

1. **网关**：根 `.env` 的 OpenAI 兼容聚合网关（`BASE_URL`+`API_KEY`，441 个可用 model）。凭据仅从 `.env` 读取，不入库。
2. **评审脚本** [scripts/llm_reviewer_panel.py](../../scripts/llm_reviewer_panel.py)：递归展开 `\input` 成自包含稿件 → 并发派 5 个模型，各以严苛 TOSEM 审稿人 prompt 输出结构化 JSON 裁决（recommendation / 5 维评分 / blockers / major / minor / questions）。
3. **Reviewer 阵容（5 跨厂商）**：`gpt-5`（OpenAI）、`claude-opus-4-6`（Anthropic）、`deepseek-r1`（DeepSeek）、`glm-5.2`（智谱）、`kimi-k2-instruct`（Moonshot）。
4. **综合 Workflow**：Triage 归并去重 → Verify 逐议题对照原文对抗验证（剔除误读/夸大）→ ARS §10 五维独立扫描（方法论 / 外部效度 / 统计偏差 / benchmark 公正 / 新颖性诚实）→ Synthesize EIC 裁决。

原始评审存 [docs/review_2026-06-17/llm_panel/](llm_panel/)（每模型 `.md`+`.json`）。

---

## 2. Panel 原始裁决

| 模型 | 裁决 | conf | soundness | novelty | significance | presentation | reproducibility | blk/maj/min |
|---|---|---|---|---|---|---|---|---|
| gpt-5 | **Reject** | 5 | 2 | 3 | 2 | 2 | 2 | 3/5/5 |
| claude-opus-4-6 | Major Revision | 4 | 3 | 3 | 3 | 2 | 3 | 2/6/9 |
| deepseek-r1 | Major Revision | 4 | 2 | 3 | 3 | 4 | 3 | 2/2/2 |
| glm-5.2 | Major Revision | 4 | 3 | 4 | 3 | 2 | 3 | 2/5/7 |
| kimi-k2-instruct | Major Revision | 2 | 2 | 3 | 3 | 2 | 2 | 1/1/4 |
| **均值** | — | — | **2.4** | **3.2** | **2.8** | **2.4** | **2.6** | — |

presentation（2.4）与 soundness（2.4）最弱；novelty（3.2）最强。

---

## 3. 对抗验证结果（23 归并议题）

对照论文原文逐条核验，分类统计：**误读/夸大 17 · major-fixable 4 · minor 2 · publication-blocker 0**。

### 3.1 验证为真的 major（4）

- **ISS-7 记号冲突（最高优先）**：规范分类（L454）固定 `T*`=self-adjoint、`\calT*`=time-reversal、idempotent 块为 `\calB*_rel`；但实证章节用裸 `T*` 表 translation（L1594/L1677），引入未定义的 `\calI*` idempotence 块（L1590/L1636/L2187），并把头条 per-block "Set N edge" 行（L1794，n=17，10/17 vs 8/17）标为 `\calT*` 且注释 "translation / self-adjoint"（L1763）。读者无法判定该载荷性结果测的是哪个块。**relabel-only 修复，不需重算**。
- **ISS-2 实证欠功效/碎片化/被 GenMorph 压制**：底物确实小而异构（20 手构造突变/1 模型；62→57 PIT 突变/10 SUT；DeepCrime n=5；Commons-Math n=77@13%），且 Set N 在 D1 上被 Set G 显著压制（McNemar pooled p=0.0043，D1 p=0.019）。**非 blocker**——论文在 Abstract、Boundary box (c)、L1692/L1698、Conclusion 处处显式声明不主张实证优越，定位为理论论文。属 venue-fit/定位风险。
- **ISS-8 篇幅与重复**：编译 PDF 82 页/~45.6k 词；"Boundary of contribution" box 重复 4 次（L259/L643/L1691/L2656）；McNemar p=0.0043 报告 8 次；34 处 "out-of-scope" 重述。表述缺陷非 soundness。（"IBT 未编译"子主张为误读——IBT 已 `\input` 于 L648 并在 PDF 渲染。）
- **ISS-11 METRIC+ Path A 混淆**：4 个 Java 主题是同作者重实现（L2605 已披露混淆），92.6% 双杀显示等价而非增值。**非 blocker**——论文未从该实验主张检错优越。可修：软化 L2499 "unambiguously strengthens"，并解决 L2236（称该 head-to-head 为未跑的 future work）与 L2449+（报告已执行）的内部矛盾。

### 3.2 ARS 五维独立发现的 major（均非 blocker）

- **方法论-A**：LLM 判等投票（驱动 n=62→57 分母、进而头条 D2/M1 数字）仅对单次 pilot analyst 校准，无与人类金标的混淆矩阵、无每判官 FP/FN、无该投票本身的 κ；别处（L2605/L707）的"LLM 共享训练数据"caveat 未延伸到此。可修：加小规模人类金标验证 + 混淆矩阵。
- **方法论-B**：一个 "(e.1) v2 override"（L1958）把 3 个 PrimitiveReturnsMutator 突变从 D1（Set N 计分）移入 D2（声明 Set N out-of-scope），机械缩小 Set N 计漏率的分层；仅 SUT 选择准则预注册，override 规则未预注册。可修：预注册/论证 override + 报告无 override 的敏感性分析。
- **统计**：预设的 aggregate D1 检验偏向基线（p=0.019）后，论文在 3 个自定义块之一（T*，10/17 vs 8/17）定位 Set N 唯一优势，未对 3 块族做 Bonferroni/Holm（校正仅用于另一 16 比较的 per-SUT 族）。已降级为"directional, not inferential at α=0.05"（L1812）缓解。可修：显式陈述多重性。
- **外部效度**：110 条专家批准的工业 MR（SPARK/LOCUST/SACOS）全为单块（order/O_le），仅佐证 O_le 可迁移性（L2609）；载荷性多块检测增益（29/47 vs 17/47）在 home-field SUT 上测得。可修：收紧 Abstract/C4 措辞，使 home-field 多块增益不被读作工业佐证。
- **benchmark 公正性簇**：Set G（随机 GenMorph GP）仅单 seed=11（L1490/L2133）；可执行底物是 NOETHER 作者按框架自身 scope 谓词筛的单代码库 10-SUT 子集，而非 GenMorph 发布的 23-method 基准（L1471/L2607）；利于 NOETHER 的轴（coverage=1.00 by construction、cost、per-block T*）由 NOETHER 定义，而中性指标（aggregate kill rate）是 Set N 落败处。各点零散披露但从未作为一个组合公正性威胁正面对待。可修：加一段组合 benchmark 公正性 + 至少跑 multi-seed GP。

### 3.3 验证为真的 minor（2）

- **ISS-20**：~10h `A_P` 蒸馏的摊销仅定性陈述（L2142/L2161/L2165），无 break-even SUT 数；且 caption 与 table 对 10h 的两种读法（per-SUT 求和 vs 一次性家族蒸馏）存在张力。
- **ISS-23**：Def 5 的 `~_s`"same constraint up to relabelling"中"relabelling"从未形式定义（无坐标-索引置换）。一句话可补，对任何定理零影响。

---

## 4. 必须在投稿前修复（按优先级，源自 EIC 裁决）

1. **ISS-7 记号重命名（最高优先，唯一触及头条结果可解读性）**：对实证章节做一次有界 rename，使每个块字形匹配 L454 规范分类——translation 不变量标为 `G` 的子情形（按 IBT L117-125，translation 是 G 的格作用），**不是** `T*` 也不是 `\calT*`；time-reversal 全程统一用 `\calT*_rev`；所有未定义 `\calI*`（L1590/L1636/L1641/L2187）映射到已定义的 `\calB*_rel`。完成后 grep 确认无游离 `T*/\calT*/\calI*`。**不动 "MetaPattern" 用法与任何数值结果**。传播到 L1440/L1692/L1812/L1836/L1865/L2165。
2. **ISS-8 篇幅 + 重复**：把 worked 枚举 / per-MR provenance / 冗余推导迁入既有 S1-S10 supplements 向 TOSEM 规范靠拢；保留 L259 完整 Boundary box，其余三处（L643/L1691/L2656）替换为一行 cross-reference；每个头条统计量只报一次。卫生项：删除 `theory/ibt_section_3_4.tex` L2-4 过期注释，解决三个 `% TODO-ref`（L124/L127/L164），重跑 xelatex。
3. **ISS-2 定位**：在实证章节起始（~L1057）加一句明确语句，声明实证章节刻意定位为 instantiation/falsifiability 探针（非 powered utility benchmark），并把 GenMorph 压制 + 底物异构作为单一具名 limitation 上浮到 Threats/Boundary box。
4. **方法论-A + B**：把 LLM 共享训练数据 caveat 延伸到判等投票，并加小规模人类金标验证（混淆矩阵、FP/FN，最好一个人类 κ）；预注册或显式论证 D1→D2 "(e.1) v2 override" 规则，报告无 override 的敏感性分析。**这两条是最强的 Reviewer-2 杠杆**。
5. **统计**：显式陈述 3 块 per-block 族的多重性并保持 T* edge 为 directional-only；对 case-study N-vs-B/N-vs-L 应用论文自采的 Bonferroni（L1206）或说明为何不用；把 L*-blindness outlier-rescue 规则的事后性（L1357-1360 已披露）整合进 Threats。
6. **ISS-11**：软化 L2499 "unambiguously strengthens" 并内联指向 construct-validity 威胁；调和 L2236 与 L2449+ 矛盾。
7. **benchmark 公正性**：加一段组合公正性段落（home-field 底物 + 单 GP seed + NOETHER 定义指标一起正面对待），至少跑 multi-seed GP。
8. **外部效度**：收紧 Abstract/C4，使 home-field 多块增益（29/47）不被读作单块工业证据佐证。
9. **ISS-20 + ISS-23（minor，低成本）**：加量化摊销 break-even；补 Def 5 "relabelling" 为坐标-索引置换的一句话定义。

---

## 5. 被驳回的误读（保护作者不去白费功夫）

以下是 panel（含 gpt-5 Reject 所依据的）提出但对照原文核验为**误读/夸大**的议题——论文当前文本已承认/降级/预先回应，**不应**为此返工：

- **ISS-1 Theorem 1 同义反复**（5 模型共识 blocker）：论文已承认并降级为 well-formedness/structural-adequacy 性质（Abstract L125, C2a L250），L586-588 有对 "near-tautological" 的逐字反驳；要求的更大空间完备性结果（Theorem 1'）已在场且被证伪，实质内容在 IBT。
- **ISS-3 反应堆 m_adj/m_rev 预测循环**：循环性 L703 已逐字点名，L675 重构为 internal-consistency systematisation，C3 不再主张裸预测。
- **ISS-5 Theorem 2 vacuous**：t_i 已按块/regime 制表（Table 1, L608-631），三个算法均实例化为"非约束瓶颈"（L635-637），定理显式条件化（L263）。
- **ISS-6 IBT 仅限线性故障类**：scope 已在定理标题、Definition、Remark R1-R3、Abstract、C2c 声明；论文不主张 finite-τ tightness 并报告实际覆盖率（25.5% non-order-only，85.6% union）。
- **ISS-9 严重依赖不可访问 supplements**：所有核心定义、两个定理、完整证明、可执行 MR set 均在主文；review-stage 匿名 artifact + SHA-256 在投稿时可得（L2631），仅永久 Zenodo DOI 延至 camera-ready（标准双盲实践）。
- **ISS-10 LLM κ 误作独立评分**：每处 κ 已带共享训练数据 caveat 与"breadth 非 correctness"框定（L707/L2605/L2744），承诺人类 inter-rater 研究，κ 不入 Abstract。
- **ISS-13 Translate 无法表达高阶/谱/参数依赖 MR**：这**正是论文的中心负面结果**——两个 PWR 反例形式化为 Propositions（prop:nonadd/prop:mtcbor）证伪 Theorem 1'，五维 obstruction 表（L1018）。审稿人要的正是已有的头条贡献。
- **ISS-14 L*-blindness 是数学恒等式非检测效力**：论文自陈"identically zero by direct calculation"（L1322），从未主张实践优势，定位为预注册 falsifiability check。
- 其余（ISS-12/15/16/17/18/19/21/22）：均为论文已显式 caveat/disclose 的内容被当成缺陷。完整逐条理由见 Workflow 原始结果 `dismissed_as_misreading`。

---

## 6. 目标期刊建议

**非现在投 TOSEM；完成 §4 重大修改后投 TOSEM。**

理由：无存活 blocker——14 个 panel "blocker" 中 13 个是对一篇预先回应了这些关切的论文的误读，存活的 ISS-7 是 relabel-only。但四位审稿人独立给 soundness/significance/presentation 打 2-3，对 TOSEM 的真实风险是 **venue-fit 而非 soundness**：一篇理论优先的论文，其唯一可执行的 head-to-head 在中性指标上、在 co-designed home-field 底物上、单 GP seed 下显示框架**落败**。TOSEM 会按理论贡献接收强理论工作，但前提是记号冲突消除（当前头条比较结果字面不可解读）、篇幅压缩到规范、实证定位 + benchmark 公正性 + LLM-judge/override 关切被"拥有"而非散落。完成后，IBT + 诚实的 Theorem 1' 证伪 + 跨域实例化是可信的 TOSEM 理论贡献。

若作者不愿执行已预注册的更大评估、也不愿完全转向理论优先框定，则比强行推一个 TOSEM 审稿人会拒的实证-效用叙事更低风险的替代，是一个对"理论贡献 + 示意性（非 powered）实证"更友好的强 SE 理论 track。

---

## 7. 总评（EIC）

本稿状态远好于 "1 Reject / 4 Major" 原始 panel 所暗示：对抗验证显示 14 个 panel 议题中 13 个——包括五位审稿人共享的 "Theorem 1 是同义反复" blocker 以及 "反应堆预测循环"、"Theorem 2 vacuous"、"supplements 不可访问" 三个 blocker——描述的是一篇已不存在的论文，因为当前正文以自己的话承认、降级、预先回应了每一条，往往比审稿人要求的更诚实。论文的真实问题是一簇可修复缺陷而非 soundness 失败：一个 verified 的记号冲突（T* 同时表 self-adjoint 与 translation、未定义 I* 块、头条 per-block "Set N edge" 上自相矛盾的 "translation/self-adjoint" 注释）使中心比较当前不可解读；真实的过长（82pp/~45.6k 词、Boundary box 重复 4 次、统计量重复至 8 次）；以及一个透明披露但散落的实证弱点（唯一可执行 head-to-head 在 co-designed home-field 底物、单 GP seed 下被 GenMorph 压制，部分由未验证的 LLM 判等投票 + directional D1→D2 重分类判定）。无一是 publication blocker——记号问题 relabel-only，实证关切被一篇显式理论优先、声明不主张优越的论文所"拥有"。正确处置因此是 **Major revision before submission**，ISS-7 优先修，随后压缩篇幅并把实证/benchmark/统计 caveat 整合为被拥有的单点陈述；作者**不应**去追那 13 个被误读的 "blocker"。

---

*完整结构化结果（23 议题逐条验证 verdict + ARS 五维 findings + EIC schema）见 Workflow 运行记录；原始 5 模型评审见 [llm_panel/](llm_panel/)。*
