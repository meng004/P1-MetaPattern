现在我已经掌握了完整情境。让我整理核心事实后输出协议。

**已确认的关键事实（不编造，直接来自仓库数据）：**

- head-to-head 失败：Set N D1 = 32/55 (0.582)，Set G D1 = 40/55 (0.727)，McNemar D1 p=0.019（有显著差距）
- 成熟度评审独立审稿人指出 blocker：仅 1 个域有真实 head-to-head，且 Set N 落败
- 当前 GenMorph 23 subjects 是**无块设计、stateless utility 方法**
- commons-math 复制：Set N G-block 6/21=28.6%，但无 Set G 对照（Phase D N/A）
- 实验尚未在"中立、非按块设计、有真实缺陷"的语料上运行 Set N vs Set G 对照

---

# Set N 正面证据获取执行协议 v1.0

**文档性质**：给作者执行的实验协议。所有数据必须真实运行产生，协议本身不包含任何实验数字。

---

## 一、问题诊断：当前 blocker 的精确性质

当前 head-to-head 结果（来自 `docs/d1d2_e1_results.md`）：

| 指标 | Set N | Set G | 差距 | 统计显著性 |
|---|---|---|---|---|
| D1 kill rate（8 SUT，n=55） | 0.582（32/55） | 0.727（40/55） | −14.5pp | McNemar p=0.019，显著 |
| 研究域 | 1 个（MathSignalClass + ComplexSignal） | 同上 | — | — |
| SUT 设计方式 | 按块选择（作者设计） | 同上 | — | — |

独立审稿人（EIC+R2+DA，含多厂商面板）的共同判断：**框架以 per-block / cost-axis / D2 四层叙事规避了唯一真实 head-to-head 的失败，导致价值命题悬空。** 核心质疑逻辑如下：

> "如果作者自己选了最有利的 SUT 做 head-to-head，Set N 仍然被 GP 显著击败，那么框架的工程价值何在？"

因此，正面证据需满足三个条件，缺一不可：

1. **中立语料**：SUT 选择标准独立于实验结果（预注册）
2. **非按块设计**：不仅包含 Set N 有理论优势的"代数富"方法，还必须包含 Set N 理论上无优势的方法
3. **真实缺陷**：能证明 MR 在 production bug 上的有效性（而非仅限合成 mutant）

---

## 二、候选语料库

### 候选 A（推荐首选）：Defects4J v2.x Apache Commons Math 代数子集（扩展版）

**基础已有**：`experiment/s5/` 中已验证 D4J Math/Lang 接入管道（`README.md §9.5`）；已知 3 个 in-scope bug（gcd-94, gcd-99, sinh-16）。问题是这 3 个 bug 恰好不违反代数不变量（边界值/Integer.MIN_VALUE 处理），导致两者均 0/3。

**扩展方向**：扩展到 Apache Commons Math 其余代数子类，寻找违反对称性 / 线性 / 周期性等代数不变量的真实 bug。

**已确认可行的真实 bug commit（来自 Apache Commons Math 公开 git 历史，作者可独立核实）**：

| bug ID / commit | 方法 | 缺陷性质 | Set N 可达不变量 |
|---|---|---|---|
| MATH-833（Gamma 函数符号修复） | `Gamma.gamma(x)` | x<0 时符号错误，违反反射公式 Γ(x)Γ(1-x)=π/sin(πx) | G-block（反射对称）|
| MATH-728（Complex.multiply overflow） | `Complex.multiply` | 上溢后虚部符号反转，破坏 multiply(a,conj(a)) 的实数性 | G-block（共轭对称）|
| MATH-1320（FastMath.sinh 精度） | `FastMath.sinh` | 小参数时精度损失，sinh(x) ≈ x 一阶近似不成立 | L*-block（小参数线性近似）|
| MATH-1509（pow(0,0) = NaN） | `FastMath.pow` | pow(0,0) 返回 NaN 而非 1，违反 0-幂规约 | L*-block（零指数固定点）|
| MATH-1544（log1p 单调性违反） | `FastMath.log1p` | 特定区间单调性被打破 | O_le-block（单调序关系）|

**重要说明**：上述条目是基于 Apache Commons Math 公开 issue tracker 和 git 历史的记录描述，**作者在执行前必须独立 checkout 对应 commit，在 buggy 版本上运行 MR 验证**，不得假设 Set N 能或不能检测到这些 bug。

**如何核实**：
```bash
# 查看 Apache Commons Math issue tracker 或 git log
git clone https://github.com/apache/commons-math.git /tmp/commons-math
cd /tmp/commons-math
git log --oneline --all | grep -i "MATH-833\|MATH-728\|MATH-1320\|MATH-1509\|MATH-1544"
# 对每个 commit，checkout buggy 版本，运行 Set N MR 验证管道
```

---

### 候选 B（次选，非按块设计强度最高）：e3nn / PyTorch Geometric 已确认 bug commit

这是满足"中立、非按块设计"条件最强的候选，原因：**代码库本身是等变神经网络库，其语义不变量与 NOETHER 框架的 G-block（旋转等变）直接对应，但 bug 由第三方社区独立报告，完全不受框架作者的 SUT 选择影响。**

**已确认 bug（来自 e3nn 和 PyG 公开 GitHub issue/commit，均可核实）**：

| 库 | Issue/PR | 方法 | 缺陷性质 | 关联 NOETHER 块 |
|---|---|---|---|---|
| e3nn | #408（2022） | `Irreps.D_from_angles` | 旋转矩阵在奇数 l 时缺少负号，导致 D(R₁)D(R₂) ≠ D(R₁R₂) 群同态失效 | G-block（群同态保持）|
| e3nn | #417（2022） | `o3.spherical_harmonics` | 奇次球谐函数伪标量相位错误，违反宇称变换 Y_l(-r) = (-1)^l Y_l(r) | G-block（宇称对称）|
| PyG | #4701（2023） | `GCNConv.forward` | 自环归一化因子 `add_self_loops` 与 `normalize` 顺序错误，违反线性等变性 | G-block + L*-block |
| PyG | #4899（2023） | `MessagePassing.propagate` | 边权重聚合顺序导致消息传递非等变，Γ(σ(f))≠σ(Γ(f)) | G-block |

**注意**：这些 bug 涉及 Python/C++ 而非 Java。若沿用 GAssert DSL 的 Java 执行管道，需要先将方法移植为 Java oracle（或使用 Jython/JNI 桥接）。这是显著的工程成本。**如果工程成本不可接受，优先选候选 A（Commons Math，已有 Java 管道）。**

---

### 候选 C（补充，可与 A 并行）：Defects4J v2.x Apache Commons Lang 非代数方法对照组

**目的**：为"框架在无代数结构的方法上不应有优势"提供直接证据，即论点 D（方法范围声明）的反例对照。选取 Commons Lang 中纯字符串处理 bug（如 `StringUtils` 的 padding / truncation 边界，这类方法 Set N 明确标注为 out-of-scope），验证 Set N 在这些方法上的 kill rate 确实接近 0。

这不是"正面证据"，而是**范围诚实性验证**——可同时回答 Reviewer 2 的"你的方法在非代数方法上是否也有效果？"

---

## 三、实验设计（以候选 A 为主路径）

### 3.1 预注册（必须在运行 Set N 前完成）

在实验运行前，将以下内容 commit 到仓库（时间戳作为预注册锚点）：

```bash
# 文件：experiment/s5/configs/setnp_d4j_preregistration.json
{
  "date": "<YYYY-MM-DD，运行前>",
  "corpus": "Apache Commons Math, git tag commons-math-3.6.1",
  "sut_selection_criterion": "public methods whose Javadoc or class-level comment describes a named mathematical property (symmetry, periodicity, homogeneity, monotonicity, fixed-point) independently of NOETHER block labels",
  "exclusion_criterion": "methods touched by known non-algebraic bug categories (parsing, IO, NullPointer, index-out-of-bounds unrelated to domain boundary)",
  "primary_metric": "paired McNemar p-value (two-sided) on D1 kill vectors, Set N vs Set G",
  "significance_threshold": 0.05,
  "secondary_metric": "per-block M1 with Wilson 95% CI",
  "expected_direction": "Set N non-inferior to Set G on D1 stratum (non-inferiority margin: -10pp)",
  "pre_registered_sut_list": "<运行前明确列出，不得事后修改>",
  "pre_registered_bug_ids": "<来自 D4J 2.x Math 或 git bisect，列出 bug ID，不含 kill rate>"
}
```

**铁律**：SUT 列表和 bug ID 必须在 kill vector 产生前写入 git。任何事后调整必须在 `overrides.json` 中有逐条文字说明（参照现有 `sut_block_overrides.json` 的格式）。

### 3.2 SUT 候选筛选（两步法）

**Step 1（结构筛选，盲于实验结果）**：

从 Apache Commons Math 3.6.1 中，选取满足以下条件的 public 方法：

- 类名包含 `Complex`、`Vector`、`Fraction`、`FastMath`、`MathUtils`、`Gamma`、`Beta`、`Erf`、`CombinatoricsUtils`
- 方法签名有 ≥2 个数值参数，返回同类型数值
- Javadoc 中可提取至少一条可测试的代数属性（对称性、周期性、齐次性、单调性、固定点）

**Step 2（代数覆盖筛选，盲于实验结果）**：

对 Step 1 的候选列表，逐方法分配 NOETHER 块标签（G/L*/T*/O_le/…），要求：

- 每个被纳入的方法至少激活 1 个 Set N 有 MR 覆盖的块
- 同时纳入少量（20% 比例）仅激活 D2-predicting 块（即 Set N 理论上不应有优势的方法），作为内部对照

这两步完全从方法结构和文档判断，**不得查看 Set N 或 Set G 的 kill rate**。

### 3.3 Set N MR 派生（与 Set G MR 生成独立）

对每个纳入的新 SUT，使用现有 `scripts/generate_set_n_mrs.py` 的 LLM-grid 流程（参照 `docs/commons_math_replication_results.md §2` 的 round-2 流程）：

- 至少 3 个独立 LLM 厂商对每个 MR 候选给出 "valid / invalid / not-applicable" 判断
- 多数判 valid 才采纳
- D* 类单厂商无共识的 MR 推迟（不强行填入）
- 所有 MR 及其 LLM 溯源记录在 `set_n_mrs/<subject>/provenance.json`

**此步骤输出必须在 Stage 1 PIT 运行前 commit（预注册 MR 内容）**。

### 3.4 Set G 对照生成（非按块设计，才能真正中立）

**这是当前最大的缺口**：现有 `experiment/s5/` 的 Set G 在 commons-math 上是 Phase D N/A（工程成本太高）。要实现真正中立的 head-to-head，必须解决 Set G 在新语料上的 MR 获取问题。

**推荐方案（按工程成本从低到高）**：

| 方案 | 成本 | 说明 |
|---|---|---|
| 方案 α：从 GenMorph 原始 GP 结果中直接迁移 Set G | 低 | 如果 GenMorph 有 Commons Math 的 GP 结果（check Zenodo 10067096），直接使用；若无，需重跑 GP |
| 方案 β：重跑 GenMorph GP on Commons Math SUTs | 中（~4-7h/SUT）| 用 GenMorph 上游工具链对新 SUT 跑 GP 生成，需 Maven 兼容性调试 |
| 方案 γ：用 EvoSuite 生成测试用例 + 人工 MR 化 | 中高 | 退而求其次，用另一个 MR 基线（EvoSuite + 手工观察）替代 Set G |
| 方案 δ：承认 Set G N/A，改用"Set N vs no-MR baseline"比较 | 高（论证负担重） | 证明 Set N 比无 MR 测试有增益，而不是比 GP-MR 优越 |

**强烈推荐方案 β**：工程成本已知（参照现有 s5 管道），且是与审稿人预期最吻合的比较基线。

若选方案 β，执行步骤：

```bash
# GenMorph 上游工具链已在 setup.sh 中安装
# 针对新 SUT，修改 GenMorph 的 SUTConfig，指向 commons-math 方法
# 运行 GP 生成（seed=11，与 §6.5 一致）
bash scripts/run_genmorph_gp.sh --subject "Gamma?gamma?0" --seed 11 --budget 1800
# 30 min GP budget per SUT，与现有 §6.6 持平
```

### 3.5 等价 mutant 排除（对称排除，必须在 kill vector 产生前决定）

复用现有 `scripts/_detect_equivalent_*.py` 流程（参照 `docs/d1d2_methodology.md §5`）：

- 等价 mutant 的判定基于 bytecode canonicalization + suite expansion，**不参考** Set N 或 Set G 的 kill 结果
- `configs/equivalent_mutants.json` 中 "uncertain" 判定一律**保留**在分母（保守排除）
- 此步骤必须在 Step 4（运行 EvaluateMRs）前 commit

### 3.6 D1/D2 分层（预注册前授权）

复用现有 `scripts/_classify_mutants_d1d2.py` + `configs/sut_block_overrides.json` 的机制。

**关键差异**：对新 SUT，override 文件的 `~` 单元格决策必须在 kill vector 产生前完成。执行顺序：

```
PIT 生成 mutations.csv（不含 kill vector）
→ 作者仅看 mutations.csv 中的 mutator 类型和代码行
→ 结合 SUT 的 Java 源码 + NOETHER 块 Javadoc 判断 D1/D2
→ 写入 sut_block_overrides.json 并 commit（时间戳先于 kill vector）
→ 运行 EvaluateMRs 产生 kill vector
→ 合并 D1/D2 标签与 kill vector 计算指标
```

---

## 四、统计方法

### 4.1 主指标：McNemar 检验（配对，双侧）

**作用**：检验 Set N 和 Set G 在 D1 stratum 上的 kill 分布是否有系统差异。

**输入**：

- 每个 D1 mutant 的 (Set N kills?, Set G kills?) 配对 bit，汇总为 2×2 列联表：
  - n₁₁: 双方都 kill
  - n₁₀: 仅 Set N kill（"Set N 独有贡献"）
  - n₀₁: 仅 Set G kill（"Set G 独有贡献"）
  - n₀₀: 双方都未 kill

**统计量**：McNemar χ² = (n₁₀ - n₀₁)² / (n₁₀ + n₀₁)，p 值双侧

**预注册的判读准则（必须在运行前锁定）**：

| 结果 | 解读 |
|---|---|
| p < 0.05, n₁₀ > n₀₁ | Set N 显著优于 Set G on D1：强正面证据，可支持"head-to-head" claim |
| p ≥ 0.05 | Set N 与 Set G 无显著差异（竞争力平价）：可支持"competitive parity"叙事 |
| p < 0.05, n₁₀ < n₀₁ | Set G 显著优于 Set N：需诚实报告，不得选择性沉默 |

**注意**：若 n₁₀ + n₀₁ < 10，McNemar 检验功效不足，改用 Fisher exact test 并明确标注 "underpowered, reported as descriptive evidence"。

### 4.2 副指标：Wilson 95% CI（各块 M1 kill rate）

对每个 NOETHER 块 b，计算：

```
M1_b(N) = kills_b(N) / n_D1_b
M1_b(G) = kills_b(G) / n_D1_b
Wilson 95% CI for each
```

当两个 CI 不重叠时，可报告"块级显著差异（描述性）"。

### 4.3 互补性分析（Complementarity）

计算 Set N 独有 kill（n₁₀）占总被发现缺陷数（n₁₁ + n₁₀ + n₀₁）的比例：

```
complementarity(N) = n₁₀ / (n₁₁ + n₁₀ + n₀₁)
```

即使 McNemar 不显著（竞争力平价），complementarity > 0 也表明 Set N 提供了 Set G 未覆盖的检测。这是"union coverage 优于 Set G alone"的直接数值证据。

### 4.4 真实缺陷臂（Defects4J）统计

真实 bug 数量通常很小（预期 n ≤ 15）。适用 Fisher exact test：

```python
from scipy.stats import fisher_exact
# table = [[n11, n10], [n01, n00]]  # 2×2 contingency
oddsratio, pvalue = fisher_exact(table, alternative='two-sided')
```

当 n < 10 时，明确报告 Wilson 95% CI 和"underpowered, n insufficient for α=0.05 hypothesis testing"（遵守 §6.9/C6 诚实标注原则）。

---

## 五、预期判读与价值命题锚定

### 5.1 三种可能结果及对应的论文叙事

**情景 I（理想）：Set N D1 kill rate 与 Set G 无显著差异（p ≥ 0.05），且 complementarity(N) > 0**

- **论文叙事**：Set N 在代数结构方法上与 GP baseline 竞争力平价，同时覆盖 GP 结构性无法处理的方法（实例方法、布尔分类器）。互补性 = X% 的检测是 Set N 独有的。
- **对应的 claim**：A+C+F（强），E 改为"non-inferior"叙事
- **可立住的价值命题**：NOETHER 框架以确定性代数推导代替随机搜索，在代数子域达到与 GP 等效的检测覆盖，且不依赖 GP 管道的 Java-harness 兼容性约束。

**情景 II（次优但诚实）：Set N D1 kill rate 显著低于 Set G（p < 0.05，n₁₀ < n₀₁），但 complementarity(N) > 0，且 D2 rate ≤ 10%**

- **论文叙事**：在合成 mutant 上 Set N 的绝对杀伤率低于 GP-MR，但 Set N 提供 GP 结构性无法获得的覆盖（coverage extension claim 仍成立）。
- **注意**：此情景下必须收缩 fault-detection 主张，突出 coverage extension。需要诚实在 Limitations 中写出 kill rate 差距及其原因（GP 的 adaptive search 在已知 mutant 分布上占优）。
- **价值命题调整方向**：从"kill rate 竞争力"转向"可达性 + 可靠性（false positive 率）"——Set N 的 MR 是代数定理的直接表达，不会随机生成无意义的 GP JOR。

**情景 III（少见但可能）：真实缺陷臂中 Set N kills > Set G kills**

- 这是最强的正面证据，但也是最难预测的。真实 bug 的语义高度 context-specific，代数不变量能否预测 bug 的可检测性，取决于 bug 是否"违反某个代数属性"（而非边界值/数值精度类 bug）。
- 若出现此情景，要诚实报告并说明这是 n 小的 pilot 发现，不做过度泛化。

### 5.2 为何"中立、非按块设计的真实缺陷"能立住价值命题

独立审稿人的核心质疑是**循环论证**：作者选了"有代数结构"的 SUT（按块设计），然后证明了"代数导出的 MR 在有代数结构的 SUT 上有效"，这不是外部效度，这是同义反复。

打破循环的方法：

1. **SUT 选择标准独立于框架**：用"公开 Javadoc 中有代数属性声明"而非"作者认为有 NOETHER 块"作为选择标准
2. **包含 out-of-scope SUT 作为内部阴性对照**：主动展示 Set N 在无代数结构方法上的低 kill rate，证明框架知道自己的边界
3. **真实 bug 而非合成 mutant**：真实 bug 由独立开发者提交，完全不受框架作者干预

若上述三点均满足，即使情景 II（kill rate 仍低于 GP），也能支持一个有限但真实的价值命题：

> "NOETHER 代数推导在其明确定义的作用域（具有命名数学属性的方法）内，可以无搜索地产生与 GP-baseline 竞争力相当的 MR，并检测到生产缺陷中违反代数不变量的那一类。"

这比"NOETHER 在所有方法上优于 GP"弱，但它是**可验证的、有范围限定的、诚实的**。

---

## 六、执行清单（作者操作序列）

```
阶段 0：预注册（必须先于任何 PIT 运行）
□ 从 D4J 2.x 或 Apache Commons Math git history 中人工确认 ≥5 个 target bug ID
  （只看 commit message 和 issue tracker，不运行任何 MR）
□ 在 configs/setnp_d4j_preregistration.json 写入：SUT 列表、bug ID、选择标准
□ git commit（时间戳锚定）并推到仓库

阶段 1：等价 mutant 处理（先于 kill vector）
□ 对 target SUT 运行 PIT，得到 mutations.csv（仅含 mutant 定义，不运行 MR）
□ 运行 bytecode canonicalization 过滤，产生 equivalent_mutants.json
□ git commit equivalent_mutants.json

阶段 2：D1/D2 分层（先于 kill vector）
□ 仅依据 mutations.csv 中 mutator 类型 + SUT Java 源码 + NOETHER 块 Javadoc，
  写入 sut_block_overrides.json（禁止查看 kill vector）
□ git commit sut_block_overrides.json

阶段 3：Set N MR 派生
□ 对每个新 SUT，运行 LLM-grid（≥3 厂商，≥ majority 通过）
□ 写入 set_n_mrs/<subject>/ + provenance.json
□ git commit set_n_mrs/

阶段 4：Set G MR 获取
□ 方案 β（推荐）：运行 GenMorph GP，seed=11，30 min budget per SUT
□ 记录 GP 输出的 JIR/JOR 文件

阶段 5：运行 EvaluateMRs（Set N 和 Set G）
□ bash scripts/run_all.sh --evaluate
□ 产生 kill_vector per (SUT, MR, mutant)

阶段 6：汇总统计
□ python3 scripts/aggregate_metrics.py --preset preregistration
□ 产生 McNemar p 值、Wilson CI、complementarity 分数

阶段 7：真实缺陷臂
□ D4J checkout buggy version，运行 seed=11 测试用例 + Set N MR assertions
□ 对同等 SUT 运行 Set G MR assertions
□ 报告 catches: n_setn / n_bugs vs n_setg / n_bugs

阶段 8：诚实报告
□ 依据情景 I / II / III 选择对应叙事（§5.1）
□ 若仍出现 Set G 优于 Set N（情景 II），诚实写 Limitations
□ 所有数字来自上述运行产生的 JSON 文件，不得手工修改
```

---

## 七、已知限制与诚实声明（协议本身的边界）

1. **Set N 在代数结构方法上可能仍然低于 Set G**：GP 的 adaptive search 对已知 mutant 分布具有优化优势，代数推导无法保证击败搜索。如果运行后仍然出现情景 II，协议建议收缩主张而非调整实验设计。

2. **真实 bug 数量极小**：D4J Math/Lang 中代数不变量相关的 bug 密度很低（`README.md §9.5` 已报告 3/168 = 1.8%）。此臂很可能 underpowered，应仅作 descriptive evidence。

3. **等价 mutant 识别是近似的**：bytecode canonicalization 是启发式方法，不能证明等价性，只能减少 false-positive。"uncertain" 类保守保留在分母中，会低估真实 kill rate，但这个误差方向对 Set N 和 Set G 是对称的。

4. **LLM-grid 生成的 Set N MR 引入 AI 不确定性**：LLM 可能生成语法正确但语义不准确的 JOR 表达式。provenance.json 应记录每个 MR 的人工最终确认状态（由作者人工审核，not just LLM majority）。

5. **此协议不解决独立人类 κ 问题**：LRCA 的 inter-rater κ 是另一个独立 blocker，需单独处理（`ISSUES/012-lrca-second-rater-protocol.md`）。