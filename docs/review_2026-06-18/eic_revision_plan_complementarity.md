# TOSEM EIC 修复方案：从“对抗 GenMorph”重构为“互补的系统化 MR 识别方法”

> 目标：回应 2026-06-18 多 reviewer 评审意见，同时保留论文真实主张。  
> 核心判断：NOETHER 不应被包装为 MR effectiveness / fault-detection 评估论文；它的贡献是从数学物理方程的算子代数结构中系统化识别 MR，从而补足专家直觉和搜索式 MR 生成方法在 MR 类型覆盖上的盲区。

## 0. 修订总策略

本文应改写为一篇 **theory-methodology paper with complementary empirical evidence**。

正确主线：

1. **问题**：MR 识别长期依赖领域专家的直觉、经验和局部知识；这种方式会系统性偏向易被人类感知的 MR 类型。例如 SACOS / SPARK / LOCUST 等软件中专家给出的 MR 集合高度集中于单调型 MR，这说明人工 MR 识别存在 coverage bias。
2. **方法**：NOETHER 不从测试运行或 mutation fitness 中搜索 MR，而是从数学物理方程和程序族的算子代数结构中识别 symmetry、order、self-adjoint、time-reversal、limit、qualitative dynamics、method-comparison、relational equivalence 等结构块，再通过 `CONSTRUCT-MP` 系统化导出 MR / MetaPattern。
3. **与 GenMorph 的关系**：GenMorph 是 search / optimization driven；NOETHER 是 structure / equation / operator-algebra driven。二者不是替代关系，而是互补关系：GenMorph 从可执行候选空间中搜索 MR，NOETHER 从方程算子结构中识别 MR 类型并给出可追溯来源。
4. **证据组织**：实验不应被解释为“NOETHER 平均杀 mutant 比 GenMorph 强”。应分成两组：  
   - **GenMorph contrast group**：只用于说明两类 MR 识别机制的目标函数不同，不作为本文主评价轴。  
   - **Mathematical-physics / operator-algebra group**：用于展示 NOETHER 的主场，即从方程结构直接导出 MR，并暴露专家单调型偏置。

### Scope firewall：本文评估 MR identification，不评估 MR effectiveness

修订稿必须把以下边界放在 Introduction 和 Empirical Evaluation 开头：

> This paper evaluates MR identification: whether a method can systematically derive structurally justified MR classes from a program family's governing equations. It does not evaluate MR effectiveness in the sense of observed fault-detection rate, mutation score, or defect-revealing superiority.

因此：

- GenMorph 相关结果只能作为 **method-complementarity / boundary-of-objective**，不能作为核心输赢指标。
- SACOS / SPARK / LOCUST 的核心指标是 **identified MR class coverage / operator-algebra coverage**，不是实际 fault detection。
- “潜在揭错能力”只能作为动机性解释，不进入摘要、贡献或主结果 headline。
- 主结果应围绕：识别了哪些 MR、覆盖了哪些算子代数块、这些 MR 是否由方程结构可追溯地导出、与专家 MR 集相比新增了哪些 MR 类型。

## 1. 对评审意见的重新分类

| 评审意见 | 是否接受 | 修订方式 | 理由 |
|---|---|---|---|
| “NOETHER 在 GenMorph D1 aggregate 上输了，因此实证贡献不足” | 接受其事实，不接受其评价框架 | 明确说明 GenMorph aggregate 是 effectiveness 指标，不是本文主评价指标；该实验只保留为方法目标差异说明。 | reviewer 的隐含前提是本文要评估 MR effectiveness。修订稿必须纠正前提：本文评估 MR identification breadth。 |
| “EGNN n=20 / DeepCrime n=5 小样本，不能证明平均效用” | 接受 | 从主论证中移出，不作为本文贡献支柱。 | 这些实验不能支撑 MR effectiveness；若保留，只能作为 MR 识别机制示例。 |
| “Theorem 1 近同义反复” | 接受其风险，但不接受其 fatal 性质 | 降格 Theorem 1 为 well-formedness / no-drop invariant；把 IBT、negative result、expert-bias correction 前置。 | Theorem 1 的价值是保证 derivation pipeline 不丢失 `Translate` 可达 MR，而非深定理。 |
| “上游 algebra/block distillation 仍靠人” | 接受 | 增加 algebra-distillation protocol 与 SACOS/SPARK/LOCUST expert-bias case。 | 这正是论文要解决的“专家直觉局限”的入口，不能回避。 |
| “需要更大 powered empirical study” | 部分接受 | 不承诺本文证明平均优越；可补小型 human validation / multi-seed sensitivity，但主线转为 methodology。 | TOSEM 可以接受强 theory-methodology 论文；不必把自己变成 empirical competition paper。 |

## 2. 论文结构重构方案

### 2.1 Introduction 重写

当前 intro 容易让 reviewer 以为本文要证明一个“更强 MR 生成器”。应把 problem statement 改成：

> Existing MR identification methods fall into two broad regimes. Expert-driven methods are interpretable but biased toward relations humans readily perceive; search-driven methods such as GenMorph generate executable MR candidates from program behaviour and search objectives but do not explain the algebraic origin or boundary of the MR space. NOETHER addresses a different question: given a mathematical-physics program family, can we derive the MR design space systematically from the operator algebra of the governing equations?

需要新增一句明确 positioning：

> We do not position NOETHER as a replacement for GenMorph. We position it as a complementary structural method: GenMorph searches for executable high-fitness MRs; NOETHER derives structure-grounded MRs and reveals which classes expert or search-based methods may under-sample.

理由：提前解除 reviewer 对 “为什么 Set N 没打赢 Set G” 的错误期待。

### 2.2 Contributions 重写

建议改成四个贡献，避免 C2a/C2b/C2c 让 Theorem 1 过载：

1. **Systematic derivation framework**：从 program-induced operator algebra 到 MetaPattern / MR 的 derivation pipeline。
2. **Identification-boundary theory**：IBT 说明某些结构型 MR 的适用边界，并解释为什么单一 MR 类型不应被误读为完整 MR 识别空间。
3. **Boundary theory**：Theorem 1' falsification / PWR counterexamples 说明当前 `Translate` 的极限。
4. **Complementary evidence**：两组证据：GenMorph benchmark group 显示互补；math-physics group 显示专家单调偏置与非单调结构 MR 的导出。

Theorem 1 改成 contribution 1 的 internal guarantee：

> The closure proposition is a well-formedness guarantee for the derivation pipeline, not the paper's primary theoretical novelty.

理由：这直接处理 “near-tautological” 评论。

### 2.3 Empirical Evaluation 拆成两组

建议将实证章节重命名为：

> Evidence: Complementarity, Structural Coverage, and Expert-Bias Correction

分为两大组。

#### Group A：Search-baseline / GenMorph contrast group（降级为定位证据）

目的不是证明 NOETHER 胜出，也不是评估 MR effectiveness，而是回答：

- GenMorph 和 NOETHER 的 MR identification objective 有何不同？
- 搜索式 MR 生成与方程结构式 MR 识别各自覆盖哪些 MR 类型？
- GenMorph benchmark 中的不利 effectiveness 结果如何证明“本文不能被解释为 effectiveness paper”？
- NOETHER 是否在 determinism / cold-start / structural traceability / MR-class coverage 上提供不同价值？

写法：

> On the GenMorph benchmark, the search-generated set performs better under the benchmark's effectiveness metric. This result is outside the paper's primary evaluation target: NOETHER is not proposed as an MR-effectiveness benchmark winner. The result is retained only to delimit the objective: GenMorph searches executable MR candidates, whereas NOETHER identifies equation-justified MR classes from operator algebra.

保留表格，但标题改成：

> GenMorph benchmark: objective mismatch and complementary MR-identification regimes

理由：把“不利结果”变成诚实的 scope boundary，而不是把论文拖进 MR effectiveness 评估。

#### Group B：Mathematical-physics / operator-algebra group

这是主场证据，应该前置或至少给同等篇幅：

- SACOS / SPARK / LOCUST 专家 MR 全部或高度集中在 `O_{\le}` 单调型；
- Governing equations 同时含 conservation、symmetry、self-adjoint / adjoint reciprocity、time-reversal、limit / convergence、method-comparison 等结构；
- NOETHER 从方程算子结构中导出这些非单调 MR 类；
- 因此 NOETHER 的价值是纠正 expert monotonicity bias，而不是在 GenMorph 的搜索基准上追求 aggregate kill-rate 胜出。

建议新增小节：

> Expert monotonicity bias in industrial mathematical-physics MR sets

核心表格：

| Source | Expert-approved MR distribution | Algebraic structures present in equations | NOETHER-derived missing MR classes | Interpretation |
|---|---|---|---|---|
| SACOS | mostly / all `O_{\le}` | conservation, balance laws, thermal-hydraulic coupling | conservation / qualitative dynamics / method comparison | expert MR set under-samples equation structure |
| SPARK | mostly / all `O_{\le}` | eigenvalue balance, critical boron, adjoint-like sensitivity | self-adjoint / method comparison / limit | monotonicity bias |
| LOCUST | mostly / all `O_{\le}` | lattice symmetry, homogenisation conservation | symmetry / conservation | monotonicity bias |

理由：这正面支持你的主张：NOETHER 避免专家直觉局限。

### 2.4 SACOS / SPARK / LOCUST 结果应升级为主结果，而不只是 threat

你的补充论点应成为修订稿的中心证据之一：

> Applying NOETHER to SACOS, SPARK, and LOCUST identifies an MR set whose coverage of the governing-equation operator algebra is broader than the expert-approved MR sets. Expert MR identification in these systems is concentrated in monotone/order relations, whereas the operator algebra exposes additional structures (e.g., conservation, symmetry, adjoint/self-adjoint relations, limit/convergence, qualitative dynamics, method-comparison constraints). These additional algebra-derived MR classes show broader MR-identification coverage: they make explicit relation classes that are absent from an order-only expert MR set.

但证据强度必须分层写清：

| Claim | 可主张强度 | 需要的证据 |
|---|---|---|
| 专家认可 MR 集偏向单调型 | 强主张 | `supplementary/S11_n5_industrial/results/n5_coverage.*`：110/110 expert MRs 落入 `O_{\le}`，0 orphan。 |
| NOETHER 可为 SACOS / SPARK / LOCUST 系统识别更多 MR | 强主张，若已列出 MR 清单 | 新增表格：每个代码的 NOETHER-derived MR、对应方程算子、所属 block、是否专家集已有。 |
| NOETHER-derived MR 覆盖更广算子代数性质 | 强主张，若 block occupancy 明确多于 `O_{\le}` | 新增 coverage table：expert set vs NOETHER set 的 block occupancy / operator coverage。 |
| 覆盖更广 MR 类型 / 算子代数性质 | 合格主张，作为本文主结果 | 基于 expert set 与 NOETHER-derived set 的 block occupancy / operator coverage 对比。 |
| 对有效性的潜在意义 | 只能作讨论区动机，不作主结果 | 更广 MR 类型可能服务于后续 effectiveness study；本文不评估这一点。 |
| 实际有效性更强 | 本文不主张 | 这是 MR effectiveness 评估，超出本文定位。 |

因此正文应采用如下边界句：

> The evaluation target is identification breadth, not fault-detection effectiveness. The algebra-derived MR set covers operator blocks and MR classes that an order-only expert MR set does not identify. We do not claim higher observed fault-detection rate on SACOS/SPARK/LOCUST.

这会让 reviewer 难以攻击 “overclaim”，同时保留你的核心贡献：NOETHER 系统导出更广泛的 MR 类型。

建议新增一个主文表：

| Code | Expert MR block occupancy | NOETHER-derived block occupancy | Additional algebraic structures covered | Newly identified MR classes |
|---|---|---|---|---|
| SPARK | `O_{\le}` | `O_{\le}` + [to fill: e.g., `T^{*}`, `\mathcal{E}^{*}`, `\mathcal{L}^{*}`] | critical-boron/eigenvalue balance, adjoint sensitivity, convergence/comparison | adjoint-style, convergence, method-comparison MR classes |
| LOCUST | `O_{\le}` | `O_{\le}` + [to fill] | lattice symmetry, homogenisation conservation, burnup/boron regimes | symmetry, conservation, regime-conditioned MR classes |
| SACOS | `O_{\le}` | `O_{\le}` + [to fill] | mass/momentum/energy balance, thermal-hydraulic coupling, spacer/local-resistance dynamics | conservation, coupling, qualitative-dynamics MR classes |

方括号中的 block 必须由实际 MR 清单支持；不能仅凭方程中“可能有”这些结构就写成已识别。

## 3. 针对 raw blockers 的具体修复

### 3.1 Theorem 1 near-tautological

修复动作：

1. 标题从 “Algebraic Closure Theorem” 改为 “Closure invariant of the derivation pipeline” 或在文中降格为 Proposition。
2. 摘要和贡献列表中减少 “closure theorem” 权重。
3. 强调真正理论贡献是：
   - IBT；
   - Theorem 1' false；
   - Translate-extension dimensions；
   - complementarity between structure-derived and search-derived MRs。

理由：reviewer 攻击 Theorem 1 时，不应继续守这个山头。要把战场转移到 IBT 和 boundary theory。

### 3.2 EGNN / DeepCrime 小样本

修复动作：

1. 删除 “comparative superiority / effectiveness” 类表述。
2. 标题改成 “Mechanism check on an equivariant ML substrate”。
3. 明确写：
   > This experiment is not an MR-effectiveness evaluation. It is a mechanism check showing that the algebraic derivation identifies an MR class absent from prompt/literature baselines.
4. cat-(iv) 结果写成 identification-mechanism evidence，不进入 effectiveness headline。

理由：承认小样本不能做的事，保留它能做的机制验证。

### 3.3 GenMorph aggregate dominance

修复动作：

1. 在结果首段直接写 “The GenMorph benchmark evaluates an effectiveness objective, whereas this paper evaluates MR-identification breadth.”
2. 随后定义 MR-identification complementarity metrics：
   - MR class overlap；
   - MR class unique to NOETHER；
   - MR class unique to GenMorph/search；
   - operator-block coverage；
   - derivation cost；
   - determinism / cold-start capability。
3. 不再用 “approximate parity” 这类容易被理解为强行追平的词。改成：
   > Complementary MR-identification value under a different objective function.

理由：如果对方的指标赢了，就承认；然后说明本文指标不同且有独立价值。

### 3.4 Upstream distillation 依赖人

修复动作：

新增 “Algebra-distillation protocol”：

1. 输入：governing equations / operator definitions / boundary conditions / numerical method family。
2. 提取 candidate operators。
3. 映射到 blocks。
4. 记录 rejected / orphan structures。
5. 输出 MR derivation trace。
6. 用一个 held-out SUT 做 worked example。

理由：这把“仍靠人”从缺陷变为可审计步骤。论文不能声称完全自动化，但可以声称系统化、可复核、减少直觉偏置。

### 3.5 专家单调偏置

修复动作：

把 SACOS/SPARK/LOCUST 从 threats 或边缘段落提升到 main evidence。

写法：

> In the industrial expert-approved MR sets, all accepted relations fell into the order block. This does not mean the programs lack other algebraic structures; the governing equations contain conservation, symmetry, adjoint, and comparison structures. The gap is evidence of expert-recognition bias, not absence of structure. NOETHER's role is to expose this latent structure and convert it into candidate MR classes.

理由：这是你的论文区别于 GenMorph 和专家法的最强应用动机。

## 4. 修订后的摘要/结论口径

摘要中避免：

- “outperforms GenMorph”
- “superior MR generation”
- “complete MR identification”

改用：

- “systematises MR derivation”
- “complements search-based MR generation”
- “exposes expert monotonicity bias”
- “derives non-monotonic MR classes from operator structure”
- “characterizes blind spots”

结论建议句：

> NOETHER should not be read as replacing search-based MR generators such as GenMorph. Search-based methods generate executable candidates from program behaviour and search objectives; NOETHER derives MR classes from the algebraic structure of the governing equations. The two methods therefore answer different questions. Their overlap and disagreement are evidence of complementary MR-identification regimes: NOETHER reveals structural MR classes, especially beyond the monotonicity relations that dominate expert-approved industrial MR sets.

## 5. 最小可执行修订清单

如果时间有限，优先做这 8 件：

1. Introduction 加 “not replacement, complementary structural method”。
2. Contributions 重写，Theorem 1 降格，IBT / boundary / expert-bias correction 前置。
3. Empirical evaluation 拆成 GenMorph benchmark group 与 mathematical-physics group。
4. GenMorph 部分首句说明该 benchmark 属于 effectiveness objective，不作为本文评价轴。
5. EGNN / DeepCrime 从主结果中降级为 mechanism 示例，不写 effectiveness / superiority。
6. SACOS/SPARK/LOCUST 专家单调偏置升为 main evidence。
7. 新增 algebra-distillation protocol。
8. 全文替换 “superiority / dominance / better than GenMorph” 为 “complementarity / structural derivability / different objective”。

## 6. 为什么这个方案能回应审稿人

1. 对 “GenMorph 更强” 的回应不再是辩解，而是承认其强项并重新定义本文问题。
2. 对 “实证不足” 的回应不是强行扩大 claim，而是把实证证据限定在 mechanism / complementarity / expert-bias correction。
3. 对 “专家仍参与上游” 的回应是提供 protocol，让专家参与变成可审计步骤，而非不可复现直觉。
4. 对 “Theorem 1 同义反复” 的回应是主动降格，把真正理论贡献放在 IBT 和 boundary theory。
5. 对 TOSEM EIC 来说，这会把稿件从“输了 benchmark 还想证明优越”改成“提出一个与 search 方法互补的系统化 MR 识别理论”，审稿阻力会显著降低。
