# 预注册：S5-aligned 多-seed confirmatory 实验（NOETHER）

> **承诺：本文件须在 seed12 / seed13 的 s5_aligned 执行之前 `git commit`；提交后将本行替换为实际 commit hash，作为不可否认的 pre-run 时间戳证据。**
> 起草日期：2026-06-20。提交对象：`docs/review_2026-06-20/prereg_s5_multiseed.md`（本文件）。
> 关联 harness：`experiment/s5_aligned`（`run_all.sh` 已验证可跑，通过 `SEED` 环境变量控制种子，断点可续）。
> 关联探索性评估：`docs/review_2026-06-20/s5_aligned_seed11_assessment.md`（seed11，**探索性**）。

## 元数据块（integrity contract）

| 字段 | 取值 |
|---|---|
| 设计类型 | exploratory-then-confirmatory（探索→确认两阶段）|
| 探索阶段（已观测，**不计入确认**）| s5_aligned SEED=11；routeB SEED=11/12/13（**全部已观测**，见 §1.4 / §2.2）|
| 确认阶段（held-out，**本预注册的唯一检验对象**）| **仅** s5_aligned 23-subject SEED=12，随后 SEED=13 |
| commit-before-run 承诺 | 本文件须在 s5_aligned seed12 / seed13 的任何执行**之前** `git commit` |
| 时间戳证据 | `git commit <hash>`（提交后回填）；该 commit 的 author / committer date 即不可否认的 pre-run 时间戳。文件正文内自述的日期可被编辑，不作为时间戳——以 commit hash 为准 |
| 假设冻结承诺 | 看到 s5_aligned seed12 / seed13 结果后，**不修改** §3 的 H1–H5 措辞、方向、判据 |
| 冻结检测机制 | 冻结基线 = pre-run commit 的 §3 内容；任何对 §3 的后续改动都会在 git history 留痕。seed12/13 跑后须 `git diff <pre-run-hash> -- 本文件` 对 §3 区段为空，否则该 confirmatory 检验作废（§7.2）|
| 定位（不漂移）| 本研究研究 **MR identification（识别）**，**不**研究 fault-detection effectiveness（故障检测优越性）|
| self-overlap 红线 | 只报 detection / generation **sufficiency**（union kill-rate、McNemar、Wilson、reliability）；**禁** k\* / minimal-MR-subset / selection / domination（属姊妹论文 T2，TSE）|

---

## 0. 定位与红线（Positioning and red lines）

### 0.1 论文研究的是什么

NOETHER 论文研究 metamorphic relation（MR / meta-pattern）的**识别（identification）**——即从算子-代数结构出发可靠地、确定性地导出一组 MR，以及该过程的**生成可靠性（generation reliability）**与**结构覆盖（structural coverage）**。

**在 claim 之内（on-claim）**：生成可靠性、确定性、结构覆盖。

**不在 claim 之内（off-claim）**：raw kill-rate 的优越性。本论文**不主张** Set N 在故障检测能力上整体胜过任何搜索式基线。

### 0.2 为什么仍然要做这个 kill-rate 实验

kill-rate / McNemar 在本研究里只承担 **sufficiency（充分性）证据**的角色：证明 NOETHER 确定性导出的 MR 在中立 substrate 上具有非平凡的检测充分性，并暴露其 scope 边界（在哪些 SUT 类型上前提条件满足/不满足）。它**不是**用来 claim 优越性的。任何把本实验结果重述为"NOETHER 故障检测更强"的写法都违反 §0.1，必须在整合阶段拦截。

### 0.3 三条红线（hard constraints）

1. **self-overlap 红线**：本实验只报告 detection / generation **sufficiency** 维度的量（union kill-rate、exact McNemar、Wilson 95% CI、generation reliability）。**禁止**出现 k\*（最小 MR 子集基数）、minimal-MR-subset 存在性、selection（MR 选择）、domination（MR 间支配关系）——这些是姊妹论文 T2（TSE）的命题，搬入本论文构成 salami / self-overlap。
2. **反漂移红线（D1/D4）**：结论必须停留在 identification / generation-reliability 维度。**不得**把实验重述为 fault-detection superiority；**不得**隐藏 Set N 在 Math 上被压制的事实——Math 的 McNemar p 必须明写在正文，不得藏入脚注或 limitations 绕过。
3. **underpowered 诚实红线**：任何小样本层必须标注 "underpowered for α=0.05"，并同时报 Wilson 95% CI 与 exact McNemar p（即便 p>0.05）。underpowered 的判定基于**预先指定的数值触发器**（§4.3），不在跑后选择性套用。

---

## 1. 实验设计与每个 seed 变化的是什么（Experiment design and what each seed varies）

### 1.1 中立 substrate（全程固定）

- substrate：GenMorph 公开的 23-subject benchmark（Math 10 + Lang 5 + Guava 8，约 562 个 PIT mutant）。
- 固定不动的要素：JDK8 / Randoop / PIT 1.7.4 / GenMorph evaluator / GenMorph 原生 mutant 集 / GenMorph 原生 kill 定义。
- **唯一变量：MR 集**（Set N vs Set G）。这是破"作者自实现 substrate / 自评"硬墙的设计核心——比较发生在 GenMorph 自家 benchmark + 自家 evaluator 上，单变量只动 MR 集。

### 1.2 Set N（NOETHER）：确定性手写 MR

- Set N 是从 NOETHER 算子-代数框架确定性导出的手写 MR，**每次运行的 MR 集完全相同**。
- 多 seed 改变的是 **Randoop 的测试输入**（test inputs），而不是 MR 集本身。
- 因此对 Set N 而言，多 seed 测量的是 **Set N 的鲁棒性（robustness）**：MR 集固定，结果的离散度只来自测试输入的随机性。

### 1.3 Set G（GenMorph）：GP 演化 MR，报两个诚实参照

- Set G 由遗传规划（GP）演化得到，跨 seed 会得到**不同的** MR 集。
- 报告两个诚实参照，二者都不依赖 s5_aligned seed12/13：
  1. **single-seed strict like-for-like baseline**：每个 seed 对齐上游 `pitest_seedN`，做严格同 seed 的头对头。
  2. **12-seed published union（上界）**：GenMorph 发表的 12-seed 并集，作为 Set G 的能力上界。
- 来源约束：Set G 一律使用 GenMorph **发表数据**（published `mutants_killed.csv` 等）。旧的重新实现版 Set G 已废弃（它把 sin 的有效 MR 数算成 2，而发表数据是 16），**不得**作为证据。

### 1.4 confirmatory 范围的精确界定（哪些 seed 是 held-out，哪些不是）

- **held-out / confirmatory（唯一）**：s5_aligned 23-subject 的 **SEED=12，随后 SEED=13**。截至本预注册提交时，`experiment/s5_aligned/docs/results/` 仅含 `*_seed11.*`，seed12/13 **尚未执行**——这是真正的样本外检验。§3 的假设对它们而言是 a-priori（先验）。
- **已观测 / exploratory（不计入确认）**：routeB（gcd + sin）的 SEED=11/12/13 **已经存在并已 commit**（routeB seed12/13 在提交 0417284 中 landed，文件 `supplementary/S5_genmorph_pilot/multiseed/routeB/{gcd,sin}/setn_result_seed{12,13}.json`）。routeB 的全部 seed 数据均为**已观测**，因此 routeB 一律为探索性，**不**作为任何样本外确认。§2.2 的 routeB 证据只用于提出方向，不用于"预测"。

---

## 2. 探索性观测（EXPLICITLY exploratory，NOT confirmatory）

> **本节全部数据为探索性（hypothesis-generating）。它们用于提出 §3 假设的方向，但本身不计入任何确认。**
> seed11（s5_aligned）与全部 routeB seed（含已观测的 seed12/13）在本设计中都是 exploratory leg；它们**不是**"预注册确认"。任何把它们报为确认证据的写法都构成 HARKing，必须拦截。

### 2.1 逐层探索性观测（s5_aligned seed11）

| Stratum | subj | mut | Set N | G@seed11 | G@12-seed union | McNemar（N vs seed）|
|---|---:|---:|---:|---:|---:|---|
| ALL | 23 | 562 | 0.313 | 0.363 | 0.607 | b=77, c=46, **p=0.0066**（Set N 被压制）|
| Math | 10 | 403 | 0.216 | 0.313 | 0.618 | b=55, c=16, **p≈0**（Set N 强烈劣于 Set G）|
| Lang | 5 | 78 | 0.410 | 0.449 | 0.615 | b=17, c=14, **p=0.72**（不显著）|
| Guava | 8 | 81 | 0.704 | 0.531 | 0.543 | b=5, c=16, **p=0.027**（Set N 胜，甚至胜过 12-seed union）|

### 2.2 routeB 探索性观测（含已观测的 seed12/13，**NOT held-out**）

> 本小节的 routeB 数据（gcd + sin，跨 GenMorph 全部 12 发表 seed，**包括已 commit 的 seed12/13**）全部为已观测。它们是探索性观测，**不**构成对 s5_aligned seed12/13 的样本外确认，也**不**作为 H2/H4 的前瞻性证据。

- routeB（gcd + sin，逐 mutant 配对）：Set G 的压制是 **seed-robust** 的。
  - gcd：pooled McNemar p=2.97e-11；Set N≥Set G 仅在 4/12 个 seed 成立。
  - sin：pooled McNemar p=0.012（11 个有效 seed，seed31 运行失败）。
- **探索性观测（不作前瞻论证）**：在已观测的 routeB 逐 seed 排名中，seed11 是对 Set N 相对有利的 seed 之一（seed11 gcd: N=13 / G=11）。这是对已观测数据的**事后描述**，**不**用来"预测" s5_aligned seed12/13 的方向；H2 的方向仅由 §2.1 的 s5_aligned Math gap（探索性→a-priori）支撑。

### 2.3 generation reliability 探索性信号（来自发表的 12-seed 数据）

- Set G（GenMorph 单次 GP）在若干 subject 的某些 seed 上产出 **0 个有效 MR**；indexOf 与 sort 跨 **全部 12 seed** 都是 0 个有效 MR。
- Set N 是确定性的：每次运行提出相同的 MR 集。
- **必须明写的 caveat（不得违反）**：Set N 目前在 acos 与 pow 上也产出 0 个有效 MR——原因是 1e-4 **绝对**容差的编码 artifact（gap G1）。因此 **"Set N 始终有效" 这一陈述目前为假**，在 G1 修复之前**绝不**断言。generation reliability 的对比必须把这条 caveat 放在明面上。

---

## 3. held-out s5_aligned seed12 / seed13 的 a-priori 假设（H1–H5）

> 以下假设的方向受 §2 探索性数据启发，但它们是对 s5_aligned seed12 / seed13 的 **out-of-sample（样本外）** 检验。看到 seed12/13 结果后**不修改**本节。
> 诚实声明：H2 预测我们自己在 Math 上会**输**——这是有意为之的诚实预测，不是事后救援。

### H1（Guava，方向性，单侧）

- **弱形式（预注册主假设）**：Set N 的 union kill-rate ≥ Set G single-seed（在 Guava 层，seed12 与 seed13 各自）。
- **强形式（探索性、高风险，非co-equal 主假设）**：Set N ≥ Set G 12-seed union（在 Guava 层）。
  - **诚实标注**：强形式的阈值正是 seed11 的点估计（Guava 0.704 vs 12-seed union 0.543）——即把界限设在唯一一次观测落点上。在 n=8 subject / 81 mutant（§4.3 判定为 underpowered）下，"确定性单次运行 ≥ 12× 搜索预算并集"是一个非常规、高风险的命题，预期是**最可能在样本外失败**的一条。强形式作为探索性次级观测报告，**不**与弱形式并列为 co-equal 预注册假设；其成立或失败都不得被叙述为"计划内确认"。

### H2（Math，方向性，单侧——预测我方失利）

- Set N 在 Math 层劣于 Set G single-seed（方向性单侧预测）。对 all-seeds 上界的比较一并报告，但 **all-seeds 上界对比为探索性参照**（其逐 seed 池含已观测 routeB seed12/13），不计为样本外确认；唯一的 Math confirmatory 量是 s5_aligned seed12/13 的 single-seed McNemar。
- 此为对我方劣势的诚实先验预测；不得在看到 seed12/13 后改写为"持平/胜出"。

### H3（Lang，描述性 null，无方向）

- **不作方向性主张，也不主张等价。** 在 Lang 层报告 Set N vs Set G single-seed 的 exact McNemar p 与双方 Wilson 95% CI，**描述性**呈现。
- **明确声明**：非显著（p≥0.05）是"未能拒绝原假设"，**不是**等价的证据；在 Lang 这样小样本层，缺乏显著极可能仅由功效不足导致。因此本层不使用"持平 / tied"作为确认结论；若 p≥0.05 仅因功效不足（CI 极宽），如实记为 "underpowered, inconclusive"，不记为 "confirmed tie"。

### H4（鲁棒性，全部层，描述性）

- Set N 的 per-seed kill-rate 在 seed11 / seed12 / seed13 间的离散度（MR 集确定性，变异只来自 Randoop 输入）。
- **描述性度量，无推断性 claim**：逐层报告三 seed 的 range（max−min）与 SD。本预注册**不**对 H4 设推断性证伪判据（见 §7.1）——离散度是描述量，照实呈现即可。

### H5（generation reliability，描述性）

- Set G 的 single-run valid-MR 成功率 **< 100%**（某些 subject 跨 seed 为 0；indexOf / sort 已知 0/12）。
- Set N 确定性地提出相同的 MR 集（validity 是 (MR, SUT, encoding) 的固定属性，不存在 seed 抽签）。
- **描述性度量，非假设检验，非配对对比**：Set G 的 reliability 分母为 12（发表 seed），Set N 在本实验的分母为 3（seed11/12/13）。二者为**不同-n 的描述性度量**，**不**对二者跑任何 p 值或推断性对比。H5 不进入 §4.3 的多重比较族。
- **受 §2.3 caveat 约束**——在 G1 修复前不得断言 "Set N 始终有效"（见 §7.2 的 date-deterministic 降级）。

---

## 4. 预先指定的检验与钉死的定义（Pre-specified tests and pinned definitions）

### 4.1 钉死的定义（no post-hoc redefinition）

- **valid MR（有效 MR）**：在**原始 SUT** 上 false-positive-free（FP=0）的 MR（沿用 GenMorph 自家规则）。
- **kill-rate（杀伤率）**：被 FP-free MR 们 union 杀掉的 mutant 数 / 总 mutant 数。一个 mutant 被"杀掉"当且仅当其状态为 KILLED / TIMED_OUT / MEMORY_ERROR（upstream-native 定义）。
- **paired test（配对检验）**：逐 mutant discordant 计数上的 **exact McNemar**（条件于 discordant pairs 的精确二项检验）；每个 rate 同时报 **Wilson 95% CI**。
- **generation reliability（生成可靠性）**：(≥1 valid MR 的 seed 数) / (seed 总数)；单一固定定义；**仅用** GenMorph 发表数据（旧重新实现版 Set G 已废弃——它把 sin 算成 2 而发表为 16）。

### 4.2 预先指定的检验（含 sidedness、统计单元、CI 构造）

| 假设 | 检验 | sidedness | 报告量 |
|---|---|---|---|
| H1（Guava）| exact McNemar，Set N vs Set G single-seed（弱形式）；探索性附 vs 12-seed union（强形式）| **单侧**（H1 方向：b>c 利于 Set N）α=0.05 | p、b/c、双方 Wilson 95% CI |
| H2（Math）| exact McNemar，Set N vs Set G single-seed（confirmatory）；探索性附 vs all-seeds 上界 | **单侧**（H2 方向：c>b 利于 Set G）α=0.05 | p、b/c、Wilson 95% CI |
| H3（Lang）| exact McNemar，Set N vs Set G single-seed | **双侧**（无方向）| p、b/c、Wilson 95% CI（描述性，不作等价判定）|
| H4（全部层）| per-seed kill-rate 的 range 与 SD（seed11/12/13）| — | 逐层逐 seed 的 rate + 离散度（描述性，无 p）|
| H5（逐 subject）| generation reliability = (≥1 valid MR 的 seed 数)/(seed 数)| — | reliability 度量 + 描述性逐 subject 表 + §2.3 caveat（不同-n，不作对比 p）|

**主 Wilson CI 的统计单元**：主报告的 Wilson 95% CI 建立在 **per-mutant pooled proportion**（以 mutant 为单元）之上，并**显式标注其忽略 within-subject 相关**，故为乐观（偏窄）下限。

**预先指定的 clustered 稳健性检验（与主检验并列，非新假设）**：为缓解 pooled per-mutant McNemar / Wilson 忽略 within-subject 相关的问题，报告 **subject-level cluster-bootstrap 95% CI（按 subject 重采样，10000 次）**，并辅以 **subject-level paired Wilcoxon signed-rank** 对逐 subject kill-rate 差值检验。该检验在跑前钉死，不在见 seed12/13 后选择。

### 4.3 多重比较与功效判据（pre-specified，blocking）

- **多重比较族划分**：H1、H2、H3 方向各异，**不**并入同一 α 池。每个假设自成一族。
  - **每族指定 primary endpoint = seed12**；**seed13 = replication（复制）检验**。由此每层每参照只有 1 个 primary confirmatory p 值，避免在 seed 维度做校正。
  - H1 在单一 seed 内含两参照（single-seed 弱形式 = primary；12-seed union 强形式 = 探索性，不进 confirmatory 族）。故 H1 confirmatory 族在 seed12 内仅 1 个检验。
  - 若任一假设在单一 seed 内出现 >1 个 confirmatory 检验，对该族施 **Holm–Bonferroni**（family α=0.05）。
- **discordant-cell 守护**：
  - 报告每个 McNemar 的 b、c。功效与 **b+c（discordant 对数）**直接相关，故"underpowered"的判定基于 b+c，而非总 mutant 数。
  - **b+c = 0**（无 discordant 对）：记为 "no discordant pairs, test undefined, rates identical"，**不**报伪 p 值。
- **underpowered 数值触发器（pre-specified）**：任一层若 **discordant 对 b+c < 25**，标注 "underpowered for α=0.05"，仍报 Wilson 95% CI 与 exact McNemar p。该阈值在跑前固定，不在跑后调整。

---

## 5. 报告承诺（Reporting commitments）

1. **report-all**：每一层都报告，即便结果与假设矛盾。不挑 seed、不挑 subject。
2. **非预注册的层一律标 exploratory**：任何不在 §3 假设清单内的切分（额外分层、事后分组、H1 强形式、routeB 全部 seed、all-seeds 上界对比）必须显式标注为 exploratory。
3. **Math 失利必须明面报**：ALL 层与 Math 层若仍为负结果，McNemar p 写入正文（不藏脚注），与 §0.3 红线 2 一致。
4. **Wilson 95% CI 强制**：每个报告的 rate 都附 per-mutant Wilson 95% CI（标注忽略 within-subject 相关）+ subject-level cluster-bootstrap CI。
5. **underpowered 标注强制**：按 §4.3 触发器（b+c < 25）标 "underpowered for α=0.05"，即便 p>0.05 也报 Wilson + exact McNemar。
6. **Set G 双参照都报**：single-seed strict like-for-like 与 12-seed published union 同时呈现，不只报对我方有利的一个。
7. **G1 caveat 随附**：凡涉及 acos / pow / Math 的 valid-MR 与 kill-rate 结论，附 1e-4 绝对容差 artifact 说明。

---

## 6. integrity 硬约束（Integrity hard constraints）

1. **exploratory-then-confirmatory 显式化**：s5_aligned seed11 + 全部 routeB seed（含已 commit 的 seed12/13）= exploratory（提出假设，不计确认）；**仅** s5_aligned seed12/13 = held-out confirmatory 检验。假设对 s5_aligned seed12/13 是先验的。
2. **commit-before-run + 冻结检测**：本文件须在 s5_aligned seed12/13 执行前 `git commit`（时间戳由 commit date 钉死，见元数据块）；冻结基线 = 该 pre-run commit 的 §3 内容；seed12/13 跑后 `git diff <pre-run-hash> -- 本文件` 对 §3 区段须为空。
3. **report-all + no cherry-picking**：见 §5。
4. **self-overlap 红线**：只报 sufficiency（union kill-rate / McNemar / Wilson / reliability）；**禁** k\* / minimal-MR-subset / selection / domination（属 T2，TSE）。
5. **anti-drift D1/D4**：停留在 identification / generation-reliability 维度；不重述为 fault-detection superiority；不隐藏 Set N 在 Math 上被压制。
6. **underpowered honesty**：按 §4.3 数值触发器标 underpowered，附 Wilson95 + exact McNemar（即便 p>0.05）。
7. **数据来源单一**：Set G 一律用 GenMorph 发表数据；废弃的重新实现版不得入证。
8. **多重比较 / sidedness 钉死**：§4.2 的 sidedness 与 §4.3 的 primary-endpoint / Holm–Bonferroni 规则在跑前固定，不在见 seed12/13 后改动。

---

## 7. 可证伪性与中止条件（Falsifiability and abort conditions）

### 7.1 每个假设如何被证伪

- **H1 被证伪**：seed12（primary）上，Guava 层 Set N union kill-rate < Set G single-seed（弱形式、单侧 p）；seed13 作为 replication 一并报告。强形式（vs 12-seed union）为探索性，其成立/失败如实记为探索性观测，**不**计入 confirmatory 裁决。
- **H2 被证伪**：seed12（primary）上，Math 层 Set N 在 single-seed 单侧检验下 ≥ Set G（我方预测的失利未出现）。若被证伪，如实报告 Set N 在 Math 上未被压制，**不**改写 H2。all-seeds 上界对比为探索性参照，不参与 H2 的证伪判定。
- **H3（描述性，无证伪）**：H3 不设方向性证伪判据。报告 Lang 层 exact McNemar p 与 Wilson CI；显著（p<0.05）如实报为存在差异，非显著如实报为 "underpowered, inconclusive"（不报为 confirmed tie）。
- **H4（描述性，无证伪）**：H4 为描述性离散度，不设推断性证伪判据；如实报告 range 与 SD。若离散度异常大，作为观测如实呈现并讨论其来源，不作"鲁棒性主张被推翻"的二元裁决。
- **H5（描述性，无证伪）**：H5 为不同-n 描述性度量，不设推断性证伪判据；如实报告 Set G 与 Set N 的 reliability，并附 §2.3 / §7.2 的 G1 caveat。

### 7.2 中止 / 降级条件（abort conditions）

- **harness 不可比中止**：若 seed12/13 在固定要素（JDK8 / Randoop / PIT 1.7.4 / GenMorph evaluator / mutant 集 / kill 定义）上无法严格复现 seed11 的 substrate，则中止本次运行，先修复可比性，不在不可比 substrate 上报数。
- **G1 状态 date-deterministic 钉死 H5 强度（非跑后选择）**：截至本预注册提交时，G1（acos / pow 的 1e-4 绝对容差 artifact）**未修复**，故 H5 的 "Set N 始终有效" 强形式**自始即降级**为弱形式："Set N 确定性提出相同 MR 集；validity 在 acos/pow 上受 G1 编码 artifact 限制"，并把该 caveat 写入正文。强形式**仅**在 G1 修复并重跑后才重新激活，且须以新 commit 记录。该降级由提交时已知的 G1 状态决定，**不**是见结果后的事后选择。
- **integrity 失败中止**：若 §6.2 的 `git diff <pre-run-hash> -- 本文件` 显示本预注册在 seed12/13 跑后被编辑过 §3，则该 confirmatory 检验作废，必须以新的 held-out seed 重新预注册。
- **聚合负结果不构成中止**：ALL / Math 层为负结果是预期内的（H2 预测我方失利），**不**触发中止；负结果如实进入正文并框为 scope-bound / complementary，**不得**上位成 superiority。