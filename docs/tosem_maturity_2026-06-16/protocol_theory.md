已读取所有必要的上下文。现在产出清单。

---

# 理论加强任务清单 — NOETHER 论文

> 产出日期：2026-06-16  
> 范围：仅协议/清单文本，不改文件，不调用实验。  
> 每条均标注 **[需作者数学判断，不可由 agent 代证]**。

---

## 任务 T1：CONSTRUCT-MP Step 3/4 "每 block 一个 MP vs 每 invariant 一个 MP" 定义歧义

### 1.1 歧义的精确定位

当前 LaTeX 源（L529-530）：

- **Step 3**：`Form the MetaPattern m_s = R(ι)/∼_s`
- **Step 4**：`Return 𝕄(A_P) = { m_s : s ∈ D(A_P) }`

隐含的输出基数是：**每个 block 恰好一个 MetaPattern**，无论该 block 下有多少个 ∼_s 等价类（即多少个互不等价的不变量）。

问题：若同一个 block 下存在两个 ∼_s 不等价的不变量 ι₁ ≁_s ι₂，则 R(ι₁) 和 R(ι₂) 属于不同的等价类。Step 3 的商操作 `R(ι)/∼_s` 在这种情况下实际产生的是**多个** MetaPattern，而 Step 4 的集合写法 `{ m_s : s ∈ D }` 暗示每个 block 只输出一个元素。这在逻辑上不一致。

**[需作者数学判断，不可由 agent 代证]**

### 1.2 修法选项A：每 block 一个 MP（聚合解读）

**定义方式**：将 Step 3 改为"令 m_s 为所有 ∼_s 等价类的并集"，即 m_s = ⋃_{[ι]∈ I_s/∼_s} R(ι)。Step 4 保持不变，𝕄 的基数等于 block 数（最多 8）。

**优点**：
- 与论文所有已运行的实例一致（Boltzmann 返回"七个 MetaPattern"，不是七十个）
- 定理 1 的证明 + 定理 2 的计数步骤均无需改动
- 反例（Section 6.6, §subsec:negative-pwr）的叙述保持不变

**缺点**：
- 若同一 block 下 ι₁ ≁_s ι₂（如 G 块下 SO(3) 旋转不变与 Z₂ 奇偶对称是不同 ∼_s 等价类），则 m_s 实际上捆绑了不同语义的 MR 家族，损害了"每个 MetaPattern 对应一个语义单元"的叙事
- 论文的 G 块实例（rotation-invariance + parity-symmetry 不分离）在等价类层面是正确的，但需明确声明这是一个聚合对象

**[需作者数学判断：在已有三个领域实例中，G 块是否确实只包含一个 ∼_s 等价类？如果 SO(3) 旋转和 Z₂ 翻转被分到了同一个 ∼_s 类，则聚合解读是正确的；如果它们是不同等价类，则选项 A 的输出不等于"七个 MetaPattern"。]**

### 1.3 修法选项B：每 ∼_s 等价类一个 MP（精细解读）

**定义方式**：Step 3 改为"对每个 ∼_s 等价类 [ι]，令 m_{s,[ι]} = R(ι)/{∼_s 内的等价}"；Step 4 改为 𝕄 = ⋃_{s} { m_{s,[ι]} : [ι] ∈ I_s/∼_s }，𝕄 的基数是所有 block 的等价类总数（至多 8，可能更多）。

**优点**：
- 语义更精确：每个 MetaPattern 对应一个同结构的 MR 家族
- 定理 1 的证明仍然成立（每个 MR 被 Step 2 放入某 R(ι)，被 Step 3 分配到唯一等价类，被 canonical-block ordering 解歧义）
- 消除了"单 block 多等价类下 m_s 是什么"的模糊

**缺点**：
- 定理 2 的复杂度分析需要修订：当前 Step 3 的 union-find 成本写为 O(n log n)，以 n 为 generator 数；若 MP 基数随等价类数目增加，需要重新说明计数的对象
- 论文所有"七个 MetaPattern"的陈述将改为"最多 8 个（等于 block 数），若同一 block 下不变量不互 ∼_s 等价则超过 8 个"，影响 Abstract、Contributions、表格 caption、Conclusion
- 三个领域实例需要明确报告每个 block 实际产生了几个等价类，否则读者无法核实

**[需作者数学判断：是否愿意放弃"恰好七个 MetaPattern"这一简洁陈述？等价类精细化是否在已有三个实例中确实产生超过 7 个 MP？如果实例中每 block 恰好一个等价类（因为不变量定义足够粗粒度），则选项 B 与 A 等价，但框架的一般性表述必须允许更多。]**

### 1.4 修法选项C：增设条件（等价类唯一性假设）

**定义方式**：在 Definition [Block invariant] 之后增加一个 Assumption，声明"本文所涉及的三个代数 A_Boltz, A_equi, A_rel 在每个 block 下恰有一个 ∼_s 等价类"；正文作为有限实例的陈述，不作为一般框架的定理。

**优点**：用最小改动消除歧义，不影响任何定理或实例叙述

**缺点**：将框架降格为"满足特定 Assumption 时才无歧义"，审稿人会质疑这个 Assumption 是否可证明而非临时约定

**[需作者数学判断：是否可以为三个实例证明每 block 只有一个等价类？对 G 块，SO(3) 的轨道不变量在 ∼_s 意义下是否构成单一等价类？]**

### 1.5 对 Theorem 1 闭包和 Theorem 2 多项式时间的影响

| 选项 | Thm 1 影响 | Thm 2 影响 |
|---|---|---|
| A（聚合） | 无影响，证明逻辑不变 | 无影响，n 仍指 generator 数 |
| B（精细） | 证明仍成立，但 uniqueness 的陈述需要把 canonical-block ordering 推广到等价类层，而不是仅 block 层 | Step 3 计数对象变为等价类数，需重新说明 n 的含义 |
| C（Assumption） | 无影响 | 无影响 |

---

## 任务 T2：Composite-Translate 是否保 Theorem 1 闭包 + Theorem 2 多项式时间

### 2.1 问题的精确陈述

论文 Remark C.7（L2817-2818）定义了 Composite Translate 的候选形式：

Translatẽ: I_{s₁} × ⋯ × I_{s_k} → MR(P)

需要同时覆盖五个独立障碍（Table \ref{tab:obstruction set}，L995-1003）：

- **O1**：operator-spectrum output（k_eff 不在 𝒴 中）
- **O2**：homomorphism-failure π-template（非加性 worth functional）
- **O3**：configuration-indexed adjoint structure（φ†_X 随 X 变化）
- **O4**：higher-order mixed-difference π-templates（二阶混合偏差）
- **O5**：bidirectional joint parametric dependence（T_mod 与 C_B 双向联合依赖）

**问题（a）**：Composite Translate 是否保 Theorem 1 的闭包？即是否存在某个扩展定义，使得 CONSTRUCT-MP 仍能把每个 Translatẽ-reachable MR 分配到唯一的某个 m ∈ 𝕄(A_P)？

**问题（b）**：上述扩展是否保 Theorem 2 的多项式时间可判定性？

**[需作者数学判断，不可由 agent 代证]**

### 2.2 攻法一：规范化路径（尝试证 Thm 1′ 的弱变体）

**思路**：证明"每个由多个 block 不变量通过某种组合规则生成的 MR，均可被一个扩展的 canonical-block ordering（现定义在 I_{s₁} × … × I_{s_k} 的笛卡尔积上）唯一分配"。

**子问题清单**（每条需作者判断）：

- **[需作者判断]** O1（k_eff 作为算子谱量）：是否可以将 k_eff 视为一个新的"谱 block"（即增加第九 block，其 operator 是"取支配特征值"的函数），从而让 Translate 对该 block 的不变量仍然适用单 block 形式？若可以，Theorem 1 对这一扩展 block 的闭包证明是否逐字可复用？
- **[需作者判断]** O2（同态失败 π-template）：当前 Definition [Block invariant] 的 π 是 (𝒳 × 𝒴)^k 上的关系，约束 P(x_i) 的组合。非加性条件是 Δ_{AB}(x₀) ≠ 0，它是四个 P(x_i) 的算术组合不等于零，形式上是一个四元关系——是否可以放宽 π 到"允许有限元组的算术组合"？放宽后 Theorem 1 的存在性证明（Step 1→2→3→4）是否仍然机械可走？
- **[需作者判断]** O4（高阶混合差分）：若 π 允许二阶混合差分，则 π 的"first-order"约束解除，Translate 的 canonical order 在多个 block 参数方向上是否仍然能定义一个良基序？anti-symmetry 是否可能失效（即同一个 MR 在两个不同方向上都有高阶描述，无法单一排序）？

**[需作者判断，核心问题]**：放宽 π 到高阶组合后，"闭包"的含义是否仍然有意义？若 π 的语言过于丰富，Theorem 1 实际上退化为"任何可描述的 MR 都被某个 m 覆盖"，即平凡恒真。作者需要在"表达力足够覆盖 O1-O5"与"表达力不至于使定理平凡"之间找到非平凡的分界线——这是唯一可能使 Composite-Translate 定理成为非平凡结果的地方。

### 2.3 攻法二：通过反例证明不可保（尝试证 Thm 1 + Composite-Translate 不相容）

**思路**：试图构造一个 Composite-Translate 的候选定义，证明在这个定义下 Theorem 1 的唯一性（uniqueness）失效，即存在某个 MR 可同时被两个不同的 (s₁, s₂) 对通过不同 π 组合推出，且 canonical-block ordering 无法消除歧义。

**子问题清单**：

- **[需作者判断]** O3（configuration-indexed adjoint）：φ†_X 对每个控制棒配置 X 不同，这个依赖是否可以被编码为 O_≤ block（用控制棒插入深度的偏序）+ T* block（自伴算子）的乘积？若是，Composite-Translate 在这个乘积上是否保唯一性？若否，需要构造一个显式反例。
- **[需作者判断]** O5（双向联合参数依赖）：T_mod 和 C_B 各自可由 O_≤ block 描述单方向单调性，但联合的二阶混合偏差不是两个 O_≤ 不变量的乘积（因为两个方向的偏序并非相互独立地约束同一输出）。这个"非乘积"性质是否可以被严格证明（即证明 ρ_{MTC-bor} ∉ span(I_{O_≤} × I_{O_≤})，其中 span 指 Composite-Translate 的某个合理定义）？

### 2.4 攻法三：多项式时间可判定性（Theorem 2）的单独分析

**当前 Theorem 2 的时间分析**（L2658-2667）：Step 1 成本 O(n · max t_i)；Step 2 O(1)；Step 3 union-find O(n log n)；Step 4 O(1)。总 O(n · max t_i · log n)。

**Composite-Translate 对 Theorem 2 的威胁**：

- 若 Composite-Translate 需要检查 I_{s₁} × I_{s₂} 的笛卡尔积（两个 block 的不变量对），则 Step 2 的成本从 O(1) 变为 O(|I_{s₁}| × |I_{s₂}|)，在最坏情况下是二次于不变量数量的
- 若 |I_s| 在某些 block 下是指数增长的（如 G block 在大有限群上），则 Composite-Translate 的总成本可能是指数级的

**[需作者判断]**：当前论文 Theorem 2 的约束"A_P admits a finite generating set of cardinality n"是否足以控制 |I_s| 的大小？对于 Composite-Translate，是否需要增加额外的 finiteness 假设（如 |I_{s₁} × I_{s₂}| ≤ n²）才能保多项式时间？这个额外假设在三个已有实例上是否成立（可检验，无需数学证明）？

---

## 任务 T3：若补不出非平凡定理，论文类型的诚实重定位

### 3.1 现状诊断（来自仓库现有 maturity review）

NEXT_STEPS.md 的 TOSEM maturity review（2026-06-16，6 个独立 subagent 综合裁决 Major Revision，评分 38-72）指出核心问题是：

> "理论内核偏平凡 + CONSTRUCT-MP Step 3/4 定义级 bug；最强定理 Thm 1′ 被自证伪"

目前论文的自我定位属于"constructive discovery"类型：NOETHER 通过代数结构推导出此前未被归纳发现的 MR（adjoint reciprocity、time-reversal compatibility 各自在先前文献中无记录）。

### 3.2 重定位选项 I："Systematisation"（最小改动路径）

**目标读者**：SE 形式化方法社区，不要求新的数学定理，接受"统一框架 + 已有知识的代数重组"作为贡献

**论文核心主张调整**：
- 原主张：NOETHER 通过代数闭包保证推导出此前未知的 MR（constructive discovery）
- 改为：NOETHER 提供一个统一的代数语言，将此前分散的 MR 识别实践（归纳、挖掘、LLM 辅助）重新编码为一个公理化体系，其主要价值在于可比性和可传递性，而非穷举性

**需要修改的关键位置**（零实验成本，仅文本）：

| 位置 | 当前表述 | 改为 |
|---|---|---|
| Abstract，Contribution C2a | "proves Algebraic Closure Theorem" | "establishes an algebraic closure guarantee within explicitly bounded scope" + 明确 by-construction 性质 |
| Contribution C2a 末尾 | 目前已有 by-construction 声明但被 Theorem 1 的排版压制 | 将 by-construction 声明提前至 C2a 首句 |
| Section 1 boundary box | "Theorem 1 converts an empirical-adequacy claim into a structural-adequacy obligation" | 补充"within the scope of Definition [Algebra-induced MR]; the framework's transferability claim rests on the instantiation evidence of §§4-6, not on Theorem 1 alone" |
| Conclusion "Open" list item (a) | 当前已声明为 open problem | 可保持不变；但需在 Introduction 提前告知读者这是 open，而非仅在 Conclusion box 中透露 |

**[需作者判断]**：这次重定位是否会触发 TOSEM 的 "not novel enough" 拒稿路径？TOSEM 接受 systematisation 论文，但需要作者在 submission letter 中显式声明并引用先前类似贡献（如 Segura 2016 的 MR 类型分类是 systematisation 先例）。是否需要在 Related Work 增加一段比较 NOETHER 与其他 systematisation 工作？

### 3.3 重定位选项 II："Re-grounding"（中度改动路径）

**定义**：Re-grounding 是 systematisation 的一个更强版本，声称"将此前基于归纳/经验的工作放置到一个可以检验假设的演绎框架中"，其贡献在于**改变可证伪性结构**，即使无新定理。

**论文现有的 re-grounding 证据**（已在论文中存在，无需额外实验）：

1. 反例构造（§subsec:negative-pwr）：提供了"NOETHER 的 Theorem 1′ 是可以被证伪的"，这本身是一个 re-grounding 的贡献——对比先前归纳 MetaPattern 框架，没有任何一个框架为自身设置了可被证伪的 completeness 断言
2. 先验预测（§subsec:reactor-mapping）：NOETHER 预测 m_adj 和 m_rev 这两类 MR，先于 empirical 验证——这是一个再接地性声明
3. 跨域迁移（三个领域相同的 8-block 分解）：归纳框架无法在代数层面保证跨域等价，NOETHER 提供了这一代数保障

**核心论点重构**：

"NOETHER's contribution is not a new theorem about MRs in general, but a change in the \emph{epistemic structure} of MR identification: it replaces the question `which MRs are empirically observed?' with the question `which MRs are algebraically derivable from a given program family's operator algebra?' The former is answered by inductive catalogues; the latter is answered deductively, and the answer is falsifiable in the sense made precise by Theorem~1's scope boundary and the two concrete counterexamples to Theorem~1' in \S\ref{subsec:negative-pwr}."

**[需作者判断]**：这个论点是否能被 TOSEM 审稿人接受为 SE 方向的贡献，还是会被判定为"philosophy of science"类论断而缺乏工程实质？TOSEM 的 scope 包含"theoretical foundations of software testing"，但具体审稿人的偏好无法预测。

### 3.4 重定位选项 III：暂不投 TOSEM，补实验后以"constructive discovery"路径投

**前提**：论文当前最强的可证伪性贡献是"先验预测了 m_adj 和 m_rev 两类 MR，且在 Boltzmann 域验证"。要将此升级为 TOSEM 接受的"constructive discovery"，需要：

- 独立人类评分者（≥ 2 人）对 NOETHER 推导的 MR 进行独立验证（κ ≥ 0.7），以排除共享语料 LLM 循环的质疑（对应 NEXT_STEPS.md 中的 "缺独立人类 inter-rater κ" Blocker）
- 在至少一个新域（NOETHER 未参与推导）上运行 CONSTRUCT-MP 并报告 MR，由该域专家（非作者）评估是否识别出先前未知的 MR

**[需作者判断]**：是否有条件在近期（3-6 个月内）完成上述实验？如无，则选项 I 或 II 是唯一投稿路径。

### 3.5 三个选项的诚实程度与期望审稿结果对比

| 选项 | 论文类型声明 | 理论深度要求 | 实验要求 | 预期 TOSEM 结果 |
|---|---|---|---|---|
| I：Systematisation | 明确声明 | Theorem 1 保留但不作为 novelty 核心 | 无新增 | 可能 Minor Revision，但需 Related Work 扩充 |
| II：Re-grounding | 隐含，通过 epistemic argument 表达 | 同 I，需 Introduction 重写 | 无新增 | 结果不定，取决于 AE 领域背景 |
| III：Constructive discovery（延迟） | 维持当前定位 | 需 Step 3/4 bug 修复 + 可能补非平凡定理 | 需人类评分者 + 新域实验 | 接受概率较高但时间成本高 |

**[需作者判断]**：对于 NOETHER 当前稿件，选项 I + II 的联合路径（即：在 Abstract/Contributions 中明确说明论文是"re-grounding that enables falsifiability"，在 Related Work 中定位为 systematisation of foundations，同时保留 Theorem 1 作为框架完整性的内部一致性保证）是否准确反映了作者对这项工作价值的判断？这一判断只能由作者做出。

---

## 总结：三个任务的优先级与相互依赖

| 任务 | 阻塞投稿 | 可由 agent 准备草稿 | 必须作者判断的核心问题 |
|---|---|---|---|
| T1（Step 3/4 歧义） | 是，属 NEXT_STEPS 中的"定义级 bug" | 是，可起草选项 A/B/C 的修改文本 | 三个领域实例中每个 block 的 ∼_s 等价类是否恰好为 1 个 |
| T2（Composite-Translate） | 否，当前论文已将其定位为 open problem，无需解决 | 部分（可列出所需引理的命题形式） | π 表达力的上下界、O1-O5 在 Composite 框架下的独立性证明 |
| T3（类型重定位） | 取决于对审稿意见的判断 | 是，可起草各选项的关键段落改写 | 作者对论文价值的定位判断，以及对 TOSEM 受众的预判 |

**建议执行顺序**：T1 → T3（选项 I 或 II 的文本草稿）→ T2（开放问题章节的精确化，无需解决）。