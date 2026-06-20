# 独立人类 κ 盲标 codebook — NOETHER 8-block 算子分类信度复核

> **版本**: 预注册版 v1（评分前固定，不得事后修改判据）
> **资产来源**: `NOETHER_paper_arxiv.tex` L383–660（算子代数预备 + 8-block 分解）、`supplementary/S3_case_study/lrca_llm_labels.json`（36 条 Set N reactor/MathSignal MR）、`supplementary/S11_n5_industrial/mr_corpora.md`（SACOS order-block 锚）。
> **本 codebook 用途**: 替换现有 LLM-only 的 κ=0.931，用 ≥2 名独立于作者的人类 rater 重新盲标，得到真正的 **human inter-rater κ**。

---

## 1. 任务说明（给 rater）

### 1.1 目的

你将对一批 metamorphic relation（MR，蜕变关系）做**算子块分类**。每条 MR 由两段谓词组成：

- **JIR**（Join Input Relation）= 描述源测试用例输入与衍生测试用例输入之间的变换关系；
- **JOR**（Join Output Relation）= 描述对应两次输出之间应满足的关系。

你的任务：把每条 MR 归入下面 **8 个算子块之一**，或在无法归类时标记为 **`orphan`（不确定/孤立）**。

本次标注的目的是**独立验证**这套 8-block 分类的信度。此前的一致性数字（κ=0.931）来自 3 个大语言模型 + 作者标签的比较，三个模型共享大量预训练语料、彼此不独立（见 `lrca_audit.md` 的 Caveat）。本次用独立人类 rater 重做，是把"LLM 佐证性广度"升级为"人类确证性验证"。

### 1.2 盲标要求（强制）

- 你**看不到**作者标签，也**看不到** LLM 已有标签。本清单只给 MR-ID + JIR + JOR + 一句输入/输出变换描述。
- 你**不得**与另一名 rater 讨论后再填，也**不得**参考论文正文中的 reactor/MathSignal 实证表格（避免锚定）。
- 你**必须独立于论文作者**：作者本人、作者直系学生、共同署名人**不得**担任 rater（见 §6 诚信约束）。

### 1.3 流程

1. 先读完 §2 全部 8 张【判据卡】+ orphan 规则，确保理解每块的判定线索与相邻块区分要点。
2. 逐条读 §3 待标 MR 清单的 JIR/JOR。
3. 在 §4 的 CSV 表中，对每条 MR 在 `block` 列填入一个标签（取值见 §2.10 标签词表）。
4. 不确定时填 `orphan`，并在 `note` 列写一句理由——**不要猜**，orphan 是合法选项。
5. 全部填完前**不得**回头修改判据卡。

---

## 2. 8-block 判据卡

> 标签词表（§4 CSV 的 `block` 列只能取这 9 个值之一）：
> `G` · `O_le` · `T_star` · `T_rev` · `L_star` · `D_star` · `E_star` · `B_rel` · `orphan`
>
> 8 个块的判据**逐字基于** `NOETHER_paper_arxiv.tex` L410–476 的算子定义。规范优先级排序（canonical-block ordering，L583）：当一条 MR 看似可归多块时，归入**优先级更高**的块：
> **G > O_le > T\* > 𝒯\*_rev > L\* > D\* > E\* > B\*_rel**

---

### 2.1 G — 对称群（Symmetry group, building block B1）

**符号**: `G`（论文记 \(G\)）

**一句定义**: 对输入施加一个**群作用 / 置换 / 对合**（交换、取负、镜像、旋转、奇偶号翻转），输出按一个固定表示 \(\rho(g)\) 协变；典范式 \(P(g\cdot x)=\rho(g)\cdot P(x)\)（L414）。

**判定线索**:
- JIR 把输入做**离散的、有限阶的**改写：两参数互换（swap）、整体取负（negate）、镜像/反序+取负组合、奇偶号决定输出符号。
- JOR 要求输出**不变**（\(\tau=\)恒等）或按同一离散变换协变（取负、随奇偶翻号）。
- 关键：变换是**离散群元素**，不是连续标量缩放、也不是加常数平移。

**典型例**（逐字来自资产）:
- `gcdSig / G_swap_negate`: JIR `(i_a_f == i_b_s) && (i_b_f == i_a_s)`；JOR `(o_return_f == o_return_s)` —— 参数互换、输出不变。
- `signum / G_negate`: JIR `Math.abs(i_x_f - (-i_x_s)) < 1e-4`；JOR `o_return_f == - o_return_s` —— 输入取负、输出取负（奇函数对称）。
- `powerSig / G_odd_negate`: JIR 底数取负、指数不变；JOR 偶指数输出相等、奇指数输出取负。

**与相邻块区分**:
- **G vs T\*（自伴）**: G 是输入空间上的**群作用/置换**；T\* 是内积**两个参数的对偶**（互易/转置）。互换两个被加数若输出不变 → G；若关系建立在 \(\langle Lx,y\rangle=\langle x,Ly\rangle\) 式的内积对偶上 → T\*。
- **G vs 𝒯\*_rev（时反）**: 二者都可能"反序"。若反序后输出**不变或协变** → G（如 `negate∘reverse` 输出不变）；若反序后断言的是**前向/后向互斥**（output 不能同时为真，\(\neg(f(x)\wedge f(\mathrm{rev}\,x))\)）→ 𝒯\*_rev。
- **G vs L\***: G 用离散符号翻转；L\* 用连续标量缩放（×k）。"取负"在两块都可能出现——若是 ×(−1) 的群对合且输出协变取负 → G；若是 ×k(k>0) 的齐次缩放 → L\*。

---

### 2.2 O_le — 序算子：单调/线性序（Order operators, building block B2）

**符号**: `O_le`（论文记 \(O_{\le}\)）

**一句定义**: 输入在某个偏序上**单调**，输出保持（或反转）该序；典范式 \(\theta_1\le\theta_2 \Rightarrow P(\theta_1)\le_{\mathcal Y} P(\theta_2)\)（L421，含 anti-monotone）。

**判定线索**:
- JIR 用 **`<=` / `<` / `>`** 在某个输入分量上建立**不等式**（而非等式缩放/平移）。
- JOR 也是输出上的**不等式** `o_return_s <= o_return_f`（或反向）。
- 关键：核心是**序的保持**，不是具体数值变换。

**典型例**（逐字来自资产）:
- `signum / O_le_monotone`: JIR `i_x_s <= i_x_f`；JOR `o_return_s <= o_return_f`。
- `clamp / O_le_mono_in_x`: JIR 保持 lo/hi 不变、`i_x_s <= i_x_f`；JOR `o_return_s <= o_return_f`。
- `isSequence / O_le_transitivity`: JIR `(i_a_f <= i_a_s) && (i_b_s <= i_b_f) && (i_c_s <= i_c_f)`；JOR `(!o_return_s) || o_return_f`（布尔单调蕴含）。
- SACOS order 锚（见 §3.2），如 `r:Fps1>Fps2, R:To1<To2`（反单调协变）。

**与相邻块区分**:
- **O_le vs L\***: O_le 的 JIR 是**不等式**（≤/≥）；L\* 的 JIR 是**等式缩放**（×k）。看到 `<=`/`>` 在输入和输出两端成对出现 → O_le。
- **O_le vs G**: G 是离散对称、JOR 通常等式；O_le 是序保持、JOR 通常不等式。
- 布尔 SUT 的单调蕴含（`if source true then followup true`）仍属 O_le（序在布尔格 false<true 上）。

---

### 2.3 T\* — 自伴算子（Self-adjoint operators, building block B3）

**符号**: `T_star`（论文记 \(T^{*}\)）

**一句定义**: 内积两参数间的**对偶/互易**，\(\langle Lx,y\rangle=\langle x,Ly\rangle\)（L431）；物理互易、转置图恒等、源-探测器互易皆属此。本数据集中的工程化典范子形式为**加常数平移协变**：\(f(x+c)=f(x)+\varphi(c)\)（含对数域的乘→加映射）。

**判定线索**:
- JIR 给输入**加一个常数偏移** `+c`（如 `i_x_f == i_x_s + 1.0`），或将输入做对数域里等价于平移的乘法步进。
- JOR 输出**同步加常数**或按固定双射协变。
- 内积/互易型：源与探测器互换、转置对偶。

**典型例**（逐字来自资产）:
- `clamp / T_shift`: JIR lo/hi/x 各 `+1.0`；JOR `o_return_f == o_return_s + 1.0`。
- `ComplexSignal add / T_shift_re`: JIR 仅 this.real `+1.0`，其余不变；JOR 输出 real `+1.0`。
- `powerSig / T_exp_step`: JIR 指数 `n_f == n_s + 1`、底数不变；JOR `o_return_f == o_return_s * i_base_s`（指数加 1 → 输出乘底数）。

**与相邻块区分**:
- **T\* vs L\***: T\* 是**加性平移**（+c）；L\* 是**乘性缩放**（×k）。这是最易混的边界——看 JIR 是 `+常数` 还是 `×常数`。
- **T\* vs G**: G 是离散群对合（swap/negate）；T\* 是连续平移或内积对偶，不是有限阶置换。
- **争议提示**: 本数据集存在一条 `exactLog2 / L_idem_at_one`（JIR `i_n_f == 2*i_n_s`，JOR `o_return_f == o_return_s + 1`）——作者归 L\*（视为极限/对数幂），LLM 多数归 T\*（视为对数域平移）。此即原 LLM-vs-author 两处分歧之一；请**独立判断**，不要被本提示锚定。

---

### 2.4 𝒯\*_rev — 时反算子（Time-reversal operators, building block B4）

**符号**: `T_rev`（论文记 \(\mathcal{T}^{*}_{\mathrm{rev}}\)）

**一句定义**: 当输入含时间/序坐标时，对时间变量取反 \(\mathcal{T}(x(t))=x(-t)\)（L439）；\(P(\mathcal{T}x)\) 由 \(P(x)\) 通过固定双射决定。耗散系统破坏此对称，对应 MetaPattern 为空。

**判定线索**:
- JIR 对一个**有序序列/三元组做反序**（首尾互换、(a,b,c)→(c,b,a)），且**不**伴随符号翻转使输出协变。
- JOR 表达**前向/后向互斥**：原序与反序不能同时满足谓词，\(\neg(f(x)\wedge f(\mathrm{rev}\,x))\)。

**典型例**（逐字来自资产）:
- `isSequence / T_rev_exclusion`: JIR `i_a_f≈i_c_s && i_b_f≈i_b_s && i_c_f≈i_a_s`（三元组反序）；JOR `!(o_return_s && o_return_f)`。

**与相邻块区分**:
- **𝒯\*_rev vs G**: 两者都"反序"。判别点在 **JOR**：若 JOR 是**互斥**（`!(A && B)`）→ 𝒯\*_rev；若 JOR 是**输出不变/协变取负**→ G。注意数据集里 `isSequence / G_negate_reverse`（`negate∘reverse`，JOR 输出相等）作者归 **G**，而 `isSequence / B_rel_xor_reverse`（反序、JOR 互斥）作者归 **B_rel**——后者是原 LLM-vs-author 第二处分歧（LLM 多数归 𝒯\*_rev）。请独立判断。

---

### 2.5 L\* — 极限算子（Limit operators, building block B5）

**符号**: `L_star`（论文记 \(\mathcal{L}^{*}\)）

**一句定义**: 参数化算子族 \(\mathcal{L}_\theta\) 随 \(\theta\to\theta_*\) 收敛到极限元 \(\mathcal{L}_*\)（L447）：网格细化、参数摄动、渐近极限。本数据集中的工程化典范子形式为**乘性缩放齐次性**：\(f(k\cdot x)=\varphi(k)\cdot f(x)\)（含 degree-1 \(\varphi(k)=k\)、degree-0 \(\varphi(k)=\mathrm{id}\) 的尺度不变）。

**判定线索**:
- JIR 把输入**乘以一个正常数 k**（`×2`、`×3`），其余结构不变。
- JOR 输出按 \(\varphi(k)\) 缩放：degree-1 → `×k`；degree-0（尺度不变）→ 输出不变。
- 网格细化 / mesh-refinement / 参数极限型。

**典型例**（逐字来自资产）:
- `hypotSig / L_scale`: JIR 两输入各 `×2.0`；JOR 输出 `×2.0`（欧氏范数 degree-1 齐次）。
- `signum / L_scale_pos`: JIR `i_x_f ≈ 3*i_x_s`；JOR `o_return_f == o_return_s`（degree-0 尺度不变）。
- `powerSig / L_scale_base`: JIR 底数 `×3.0`、指数不变；JOR 输出 `× powerSig(3.0, n_s)`。

**与相邻块区分**:
- **L\* vs T\***: L\* 是**×k 乘性**；T\* 是 **+c 加性**。
- **L\* vs O_le**: L\* 用**等式缩放**；O_le 用**不等式**序。
- **L\* vs G**: 缩放因子 k>0 连续 → L\*；离散 ×(−1) 对合且输出协变取负 → G。

---

### 2.6 D\* — 定性动力学算子（Qualitative-dynamics operators, building block B6）

**符号**: `D_star`（论文记 \(\mathcal{D}^{*}\)）

**一句定义**: 作用于 ODE/PDE 解轨迹的算子，提取**定性特征**——极值、拐点、单调相、超调幅度、S 曲线转变、相图轨道（L453），在保持动力学结构的摄动下不变。本数据集中的工程化典范子形式为**倒数/取逆关系**：\(f(1/x)=\psi(f(x))\)、\(f(b,-n)=1/f(b,n)\)。

**判定线索**:
- JIR 把输入做**取倒数 / 指数取负**等（`i_x_f ≈ 1.0/i_x_s`、`i_n_f == -i_n_s`）。
- JOR 输出取倒数 \(1/f(x)\) 或按固定 \(\psi\) 协变（含 \(\psi=\) 恒等）。
- 或：定性形状特征（极值/超调/单调段）在动力学保持摄动下不变。

**典型例**（逐字来自资产）:
- `powerSig / D_reciprocal_exp`: JIR `i_base_f≈i_base_s && i_n_f == -i_n_s`；JOR `o_return_f ≈ 1.0/o_return_s`。
- `signum / D_reciprocal`: JIR `i_x_f ≈ 1.0/i_x_s`；JOR `o_return_f == o_return_s`（signum 在取倒数下不变，\(\psi=\)恒等）。

**与相邻块区分**:
- **D\* vs G**: G 是离散群对合（取负、互换）；D\* 是**取逆/倒数**这类动力学结构变换。`signum` 在 negate 下属 G、在 reciprocal 下属 D\*——看 JIR 是 `-x` 还是 `1/x`。
- **D\* vs L\***: L\* 是 ×k 缩放；D\* 是 1/x 取逆（非线性）。

---

### 2.7 E\* — 方法比较算子（Method-comparison operators, building block B7）

**符号**: `E_star`（论文记 \(\mathcal{E}^{*}\)）

**一句定义**: 在数值/算法方法上的**偏序** \(\preceq_{\mathcal E}\)，\(M_1\preceq_{\mathcal E}M_2\) 断言 \(M_1\) 在指定误差范数下产生不劣于 \(M_2\) 的近似（L461）。本数据集中的工程化典范子形式为**方法自复合/幂的幂恒等**：\(f(f(b,m),n)=f(b,m\cdot n)\)。

**判定线索**:
- JIR 把**前一次输出当作后一次输入**（链式/迭代复合，`i_base_f ≈ powerSig(i_base_s, i_n_s)`）。
- JOR 用一个**合成方法/复合调用**作为参照断言：`o_return_f ≈ powerSig(i_base_s, i_n_s * i_n_f)`。
- 或：两种方法（高/低精度、不同算法）在指定条件下的误差偏序比较。

**典型例**（逐字来自资产）:
- `powerSig / E_power_of_power`: JIR `Math.abs(i_base_f - o_return_s) < 1e-4`（后一次底数=前一次输出）；JOR `o_return_f ≈ powerSig(i_base_s, i_n_s * i_n_f)`（幂的幂 = 指数相乘）。

**与相邻块区分**:
- **E\* vs L\***: E\* 是**方法/调用之间**的比较或自复合；L\* 是单方法下的输入缩放极限。
- **E\* vs T\***: E\* 涉及输出回喂为输入的链式结构；T\* 是单步加常数平移。
- **关键信号**: JIR 里出现"用上一次输出作下一次输入"或在 JOR 里调用 SUT 自身做参照 → 强烈指向 E\*。

---

### 2.8 B\*_rel — 关系等价算子（Relational-equivalence block）

**符号**: `B_rel`（论文记 \(\mathcal{B}^{*}_{\mathrm{rel}}\)）

**一句定义**: 幂等半环上表达式的**改写等价** \(E\equiv_{\mathcal R}E'\)（当且仅当在所有合法求值上下文下相等，L473–476），由一组保恒等的改写规则生成（选择下推、投影下推、连接重排、去重消除等）。对无幂等半环改写结构的程序族**为空**（Boltzmann 反应堆物理、等变 ML），对关系查询优化器**非空**。

**判定线索**:
- MR 表达**两个表达式/查询/序列在改写规则下的等价或排斥**，而非单纯算术变换。
- 关系代数 / SQL bag 语义 / 半环改写语境。
- 本数据集中作者把一条 `isSequence` 的**反序异或**关系（JIR 反序、JOR `!(s && f)` 互斥）归入 B_rel——视为序列谓词在反序改写下的关系等价/排斥，而非时反。

**典型例**（逐字来自资产）:
- `isSequence / B_rel_xor_reverse`: JIR `i_a_f≈i_c_s && i_b_f≈i_b_s && i_c_f≈i_a_s`；JOR `!(o_return_s && o_return_f)`。
  （注意：本条 JIR/JOR 与 §2.4 的 `T_rev_exclusion` **字面完全相同**，仅 MR 名不同——作者一条归 B_rel、一条归 T_rev。这是判据卡里**唯一一对字面相同、标签不同**的项；它就是原 LLM-vs-author 分歧之一。请对两条都按你自己的判据独立填写，不要因相同字面而强行一致。）

**与相邻块区分**:
- **B\*_rel vs 𝒯\*_rev**: 𝒯\*_rev 强调**时间坐标反转**的物理对称；B\*_rel 强调**改写规则下的关系等价/排斥**。在本数据集这对是真实争议点。
- **B\*_rel vs G**: G 是输入群作用；B\*_rel 是表达式层改写等价。

---

### 2.9 orphan — 孤立/不确定

**何时用**:
- 读完 8 张判据卡仍**无法确定**归哪一块；
- MR 看似横跨多块且 canonical ordering 也难裁决；
- JIR/JOR 描述的关系**不属于**上述任何算子结构（如概率/分布散度、度量稳定性 Lipschitz、标签一致性等——这些在论文 Remark（L497–509）中明确列为候选第九块或域外，**不在** 8 块内）。

**规则**: orphan 是**合法答案**，不是失败。宁填 orphan + 一句理由，也不要强行套一个块。在 §4 CSV 的 `note` 列写明为何无法归类。

### 2.10 标签速查表

| 标签 | 块名 | 一句线索 |
|---|---|---|
| `G` | 对称群 B1 | 离散群作用：swap / negate / 镜像；输出不变或协变 |
| `O_le` | 序 B2 | JIR/JOR 都是 `<=`/`>` 不等式；单调保序 |
| `T_star` | 自伴 B3 | 加常数 `+c` 平移协变 / 内积互易对偶 |
| `T_rev` | 时反 B4 | 序列反序 + JOR 前后向**互斥** `!(s&&f)` |
| `L_star` | 极限 B5 | 乘常数 `×k` 缩放齐次 / 网格细化极限 |
| `D_star` | 定性动力学 B6 | 取倒数 `1/x` / 指数取负 / 形状特征不变 |
| `E_star` | 方法比较 B7 | 输出回喂为输入的链式自复合 / 方法误差偏序 |
| `B_rel` | 关系等价 | 改写规则下表达式等价/排斥（半环/关系代数）|
| `orphan` | — | 无法归类（合法）|

---

## 3. 待标 MR 清单

> **总量 ~41 条** = lrca 36 条 Set N 跨块 MR（主体）+ 5 条 SACOS order 锚。
> 块覆盖（按作者标签，仅供本 codebook 编者核对覆盖度，**不展示给 rater**）：G×8、L_star×11、T_star×6、O_le×6、T_rev×2、D_star×2、E_star×2、B_rel×1。每个非空块 ≥2 条，唯 B_rel 仅 1 条（数据集本身只产出 1 条 B_rel；SACOS 锚补强 O_le）。
> **抽样规则**（若需精简）: 必须**覆盖每个非空块 ≥2 条**；B_rel 唯一一条**必保留**（它是争议核心）；T_rev 两条必保留（其中一条与 B_rel 字面相同）。下表 §3.1 给出全部 36 条的盲标格式（已去标签），§3.2 给出 5 条 SACOS 锚。完整 JIR/JOR 原文从 `lrca_llm_labels.json` 逐条生成（本表 JIR/JOR 已逐字转录）。

### 3.1 主体：36 条 Set N MR（盲标格式，已去作者/LLM 标签）

| MR-ID | SUT 方法 | 输入变换 + 输出关系描述（JIR / JOR，逐字） |
|---|---|---|
| M01 | ComplexSignal.add | JIR: 两复数加数互换（this↔other）。JOR: `o_return_real/imag` 两次相等 |
| M02 | ComplexSignal.add | JIR: 两加数各分量 `×2.0`。JOR: 输出实/虚部 `×2.0` |
| M03 | ComplexSignal.add | JIR: this.real `+1.0`，其余不变。JOR: 输出 real `+1.0`，imag 不变 |
| M04 | clamp | JIR: `lo_f=-hi_s, hi_f=-lo_s, x_f=-x_s`（取负+换界）。JOR: `o_return_f = -o_return_s` |
| M05 | clamp | JIR: `lo/hi/x` 各 `×2.0`。JOR: 输出 `×2.0` |
| M06 | clamp | JIR: lo/hi 不变，`i_x_s <= i_x_f`。JOR: `o_return_s <= o_return_f` |
| M07 | clamp | JIR: `lo/hi/x` 各 `+1.0`。JOR: `o_return_f = o_return_s + 1.0` |
| M08 | exactLog2 | JIR: `i_n_f == 2*i_n_s`。JOR: `o_return_f == o_return_s + 1` |
| M09 | exactLog2 | JIR: 两个 2 的幂且 `i_n_s <= i_n_f`。JOR: `o_return_s <= o_return_f` |
| M10 | exactLog2 | JIR: `i_n_f ≈ 2.0*i_n_s`。JOR: `o_return_f ≈ o_return_s + 1.0` |
| M11 | gcdSig | JIR: `(i_a_f==i_b_s) && (i_b_f==i_a_s)`（互换）。JOR: `o_return_f == o_return_s` |
| M12 | gcdSig | JIR: `i_a_f=2*i_a_s, i_b_f=2*i_b_s`。JOR: `o_return_f = 2*o_return_s` |
| M13 | hypotSig | JIR: `i_a_f≈i_b_s, i_b_f≈i_a_s`（互换）。JOR: 输出两次相等 |
| M14 | hypotSig | JIR: `i_a_f≈2*i_a_s, i_b_f≈2*i_b_s`。JOR: `o_return_f ≈ 2*o_return_s` |
| M15 | hypotSig | JIR: `|i_a_s| <= |i_a_f|` 且 b 近似不变。JOR: `o_return_s <= o_return_f` |
| M16 | isSequence | JIR: `i_a_f≈i_c_s, i_b_f≈i_b_s, i_c_f≈i_a_s`（三元组反序）。JOR: `!(o_return_s && o_return_f)` |
| M17 | isSequence | JIR: `i_a_f=-i_c_s, i_b_f=-i_b_s, i_c_f=-i_a_s`（取负+反序）。JOR: `o_return_f == o_return_s` |
| M18 | isSequence | JIR: `i_a/b/c_f ≈ 2.0×` 对应 s。JOR: `o_return_f == o_return_s` |
| M19 | isSequence | JIR: `(i_a_f<=i_a_s) && (i_b_s<=i_b_f) && (i_c_s<=i_c_f)`。JOR: `(!o_return_s) || o_return_f` |
| M20 | isSequence | JIR: `i_a_f≈i_c_s, i_b_f≈i_b_s, i_c_f≈i_a_s`（三元组反序）。JOR: `!(o_return_s && o_return_f)` |
| M21 | isSequence | JIR: 三分量增量相等（`(a_f-a_s)≈(b_f-b_s)≈(c_f-c_s)`，统一平移）。JOR: `o_return_f == o_return_s` |
| M22 | lcmSig | JIR: `(i_a_f==i_b_s) && (i_b_f==i_a_s)`（互换）。JOR: `o_return_f == o_return_s` |
| M23 | lcmSig | JIR: `i_a_f=2*i_a_s, i_b_f=2*i_b_s`。JOR: `o_return_f = 2*o_return_s` |
| M24 | midpoint | JIR: `i_a_f≈i_b_s, i_b_f≈i_a_s`（互换）。JOR: 输出两次相等 |
| M25 | midpoint | JIR: `i_a_f≈2*i_a_s, i_b_f≈2*i_b_s`。JOR: `o_return_f ≈ 2*o_return_s` |
| M26 | midpoint | JIR: `i_a_s <= i_a_f` 且 b 近似不变。JOR: `o_return_s <= o_return_f` |
| M27 | midpoint | JIR: `i_a_f≈i_a_s+1.0, i_b_f≈i_b_s+1.0`。JOR: `o_return_f ≈ o_return_s + 1.0` |
| M28 | powerSig | JIR: `i_base_f≈i_base_s, i_base_s≠0, i_n_f==-i_n_s`（指数取负）。JOR: `o_return_f ≈ 1.0/o_return_s` |
| M29 | powerSig | JIR: `i_base_f ≈ o_return_s`（后一次底数=前一次输出）。JOR: `o_return_f ≈ powerSig(i_base_s, i_n_s*i_n_f)` |
| M30 | powerSig | JIR: `i_n_f==i_n_s, i_base_f≈-i_base_s`（底数取负）。JOR: 偶指数输出相等 / 奇指数输出取负 |
| M31 | powerSig | JIR: `i_base_f≈3.0*i_base_s, i_n_f==i_n_s`（底数 ×3）。JOR: `o_return_f ≈ powerSig(3.0, i_n_s)*o_return_s` |
| M32 | powerSig | JIR: `i_base_f==i_base_s, i_n_f==i_n_s+1`（指数 +1）。JOR: `o_return_f ≈ o_return_s * i_base_s` |
| M33 | signum | JIR: `i_x_s≠0, i_x_f≈1.0/i_x_s`（取倒数）。JOR: `o_return_f == o_return_s` |
| M34 | signum | JIR: `i_x_f≈-i_x_s`（取负）。JOR: `o_return_f == -o_return_s` |
| M35 | signum | JIR: `i_x_f≈3.0*i_x_s`（×3）。JOR: `o_return_f == o_return_s` |
| M36 | signum | JIR: `i_x_s <= i_x_f`。JOR: `o_return_s <= o_return_f` |

> 提示给 rater: **M16 与 M20 的 JIR/JOR 字面完全相同**（同为 isSequence 反序+互斥）。请对两条都各自独立填写，不要因字面相同而刻意一致或刻意区分——按你的判据卡判断即可。这是本研究的关键观察点。

### 3.2 SACOS order 锚（5 条，逐字来自 `mr_corpora.md` 的 SACOS 段 L122–167）

| MR-ID | 来源 | 输入序 → 输出序（逐字） |
|---|---|---|
| S01 | SACOS MR1 | `r:Fps1>Fps2, R:To1<To2` |
| S02 | SACOS MR7 | `r:Tin1>Tin2, R:To1>To2` |
| S03 | SACOS MR13 | `r:Po1>Po2, R:Pa1>Pa2` |
| S04 | SACOS MR25 | `r:Lf1>Lf2, R:Vf1<Vf2` |
| S05 | SACOS MR45 | `r:Fps1<Fps2, R:Re1<Re2` |

> 格式说明给 rater: `r:` 后为输入分量的序关系（一个量增/减），`R:` 后为输出分量的协变序关系（同增/同减或反向）。这 5 条都是**单调协变**关系，预期归 `O_le`（含 anti-monotone）。它们作为 order-block 锚校准 rater 对 O_le 的理解。

---

## 4. rater 盲标表（CSV）

每名 rater 独立填一份。文件名建议 `kappa_labels_raterA.csv` / `kappa_labels_raterB.csv`。

### 4.1 CSV 表头

```csv
mr_id,sut_method,block,confidence,note
M01,ComplexSignal.add,,,
M02,ComplexSignal.add,,,
M03,ComplexSignal.add,,,
M04,clamp,,,
M05,clamp,,,
M06,clamp,,,
M07,clamp,,,
M08,exactLog2,,,
M09,exactLog2,,,
M10,exactLog2,,,
M11,gcdSig,,,
M12,gcdSig,,,
M13,hypotSig,,,
M14,hypotSig,,,
M15,hypotSig,,,
M16,isSequence,,,
M17,isSequence,,,
M18,isSequence,,,
M19,isSequence,,,
M20,isSequence,,,
M21,isSequence,,,
M22,lcmSig,,,
M23,lcmSig,,,
M24,midpoint,,,
M25,midpoint,,,
M26,midpoint,,,
M27,midpoint,,,
M28,powerSig,,,
M29,powerSig,,,
M30,powerSig,,,
M31,powerSig,,,
M32,powerSig,,,
M33,signum,,,
M34,signum,,,
M35,signum,,,
M36,signum,,,
S01,SACOS,,,
S02,SACOS,,,
S03,SACOS,,,
S04,SACOS,,,
S05,SACOS,,,
```

### 4.2 填写说明

- `block`: **必填**，取值仅限 §2.10 的 9 个标签（`G`/`O_le`/`T_star`/`T_rev`/`L_star`/`D_star`/`E_star`/`B_rel`/`orphan`）。大小写敏感，请逐字照抄。
- `confidence`: 1–5 整数（1=很不确定，5=很确定）。用于事后敏感性分析（如剔除 conf≤2 后重算 κ）。
- `note`: 标 `orphan` 时**必填**理由；其余可选。
- 不得留空 `block`；不确定就填 `orphan`，不要跳过。

---

## 5. κ 计算

### 5.1 要计算的统计量

| 统计量 | 比较对象 | 用途 |
|---|---|---|
| Cohen κ | raterA vs raterB | 两名人类 rater 互评（**主结果**：真正的 human inter-rater）|
| Cohen κ | raterA vs author、raterB vs author | 各 rater 与作者标签的一致（与现 κ=0.931 同口径，可比）|
| Fleiss κ | {raterA, raterB, author}（≥3 评者）| 多评者总体一致 |
| Wilson 95% CI | 每个 κ 对应的逐项一致率 \(p_o\) | 报告 observed agreement 的区间（小样本必报）|
| Fisher exact / 类别分布 | 分歧项 | 描述哪些块最易混 |

**Landis-Koch 解读带**（报告时附）: <0=poor；0.00–0.20=slight；0.21–0.40=fair；0.41–0.60=moderate；0.61–0.80=substantial；0.81–1.00=almost perfect。

### 5.2 最小可跑 python 片段思路（不需完整代码）

```python
# 依赖: pip install scikit-learn statsmodels
import pandas as pd
from sklearn.metrics import cohen_kappa_score
from statsmodels.stats.inter_rater import fleiss_kappa, aggregate_raters
from statsmodels.stats.proportion import proportion_confint

# 1) 读三列标签（对齐 mr_id）：raterA, raterB, author
A = pd.read_csv("kappa_labels_raterA.csv").set_index("mr_id")["block"]
B = pd.read_csv("kappa_labels_raterB.csv").set_index("mr_id")["block"]
author = pd.read_csv("author_labels.csv").set_index("mr_id")["block"]  # 现有作者标签
df = pd.concat([A, B, author], axis=1, keys=["A","B","author"]).dropna()

# 2) pairwise Cohen κ（注意 labels 取并集，保证类别空间一致）
labels = sorted(set(df.values.ravel()))
k_AB     = cohen_kappa_score(df.A, df.B,      labels=labels)
k_A_auth = cohen_kappa_score(df.A, df.author, labels=labels)
k_B_auth = cohen_kappa_score(df.B, df.author, labels=labels)

# 3) Fleiss κ（先 aggregate_raters 成 n_items×n_categories 计数矩阵）
mat, cats = aggregate_raters(df[["A","B","author"]].values)
k_fleiss = fleiss_kappa(mat)

# 4) Wilson 95% CI on observed agreement（以 A vs B 为例）
n   = len(df)
agr = int((df.A == df.B).sum())          # 一致项数
lo, hi = proportion_confint(agr, n, alpha=0.05, method="wilson")

# 5) 分歧项导出（人类互评分歧 + 与作者分歧），用于定性讨论最易混块对
disagree_AB   = df[df.A != df.B]
disagree_auth = df[(df.A != df.author) | (df.B != df.author)]
```

报告时给出：每个 κ 值 + 其 Landis-Koch 带 + observed agreement 的 Wilson CI + 分歧项清单（哪些 SUT/块对）。

---

## 6. 诚信约束（预注册，评分前固定）

1. **作者本人不得当 rater**: 论文作者、其直系学生、共同署名人均排除。rater 须为对 NOETHER 项目无利益关系的独立人员（领域具备读懂 JIR/JOR 的最低基础即可）。
2. **盲标**: rater 看不到作者标签与 LLM 标签；不参考论文实证表格；两名 rater 互不通气。
3. **预注册判据卡**: 本 codebook §2 判据卡在**任何评分开始前**固定。评分过程中**不得**修改判据、不得新增/删除块定义、不得调整 canonical ordering。如评分后发现判据有歧义，记录在 response/limitations，**不回填**改判据卡。
4. **如实报告，禁止救援**:
   - 若独立人类 κ **显著低于** 现有 LLM-only 的 0.931，**必须如实报告**该数字，并在正文**弱化 C4**（不得继续把 0.931 当作主结果，应改述为"LLM 佐证性广度；独立人类 κ = X（band Y），低于 LLM 内部一致，提示分类边界在人类判读下存在 Z% 分歧"）。
   - 小样本（n=41，含 36 跨块 + 5 锚）属 **underpowered for tight CI**：必须同时报告 Wilson 95% CI，明示样本量限制，不得用"trends suggest / encouraging"等措辞掩盖（遵循 §6.9/C6）。
   - 已知争议点（M08 exactLog2 的 L\*↔T\*；M16/M20 反序+互斥的 B_rel↔T_rev）若在人类 rater 处再现分歧，**保留并讨论**，不得删项以抬高 κ（selection-on-the-response 禁止）。
5. **可追溯**: 三份标签 CSV（raterA/raterB/author）+ κ 计算脚本输出，归档到 `docs/review_<DATE>/`，response letter 中引用，使复核者可重算。

---

**附：编者核对（不展示给 rater）** — 现 κ=0.931 用的同一批 36 条 MR 已逐字纳入 §3.1，去除了 `votes`/`author_label`；§2 判据卡的 8 块定义逐字对应 `NOETHER_paper_arxiv.tex` L410–476，conservation 不另列为第九块（按 L471，它是 G 块的 \(m_{\mathrm{inv}}\) 实例）；两处原 LLM-vs-author 分歧（`exactLog2/L_idem_at_one`、`isSequence/B_rel_xor_reverse`）已分别落到 M08、M16 并在判据卡 §2.3/§2.4/§2.8 显式标注为争议点，供检验人类 rater 是否复现该边界模糊。

相关文件路径（相对仓库根 `<PROJECT_ROOT>`）:
- `<PROJECT_ROOT>/supplementary/S3_case_study/lrca_llm_labels.json`（36 条 MR 原文 + 作者标签，生成 §3.1 与作者对照列的源）
- `<PROJECT_ROOT>/supplementary/S3_case_study/lrca_audit.md`（现 κ=0.931 口径）
- `<PROJECT_ROOT>/supplementary/S11_n5_industrial/mr_corpora.md`（SACOS 锚源，L122–146）
- `<PROJECT_ROOT>/NOETHER_paper_arxiv.tex`（8-block 定义，L410–476；canonical ordering L583）