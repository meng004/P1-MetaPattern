现在已有足够的背景信息。协议设计所需的关键事实已明确：现有 κ 全部来自共享语料 LLM（Fleiss κ = 1.000 是三个 LLM 之间的一致性，本质上是循环），任务是 Set N 的 MR↔block 归类标注（8 个 NOETHER 块：G / L\* / T\* / D\* / E\* / O\_le / T\_rev / B\_rel），以及 D1/D2 分层判定。以下输出完整协议文档：

---

# 独立人类 Inter-Rater 标注协议
## NOETHER 论文 §6.6 — Set N MR 分类可靠性

**文档编号**：IRR-PROTO-001  
**版本**：1.0（2026-06-16）  
**适用论文**：NOETHER: An Algebraic Framework for Metamorphic Testing（目标期刊 TOSEM）  
**触发原因**：独立成熟度评审(6×Opus + 5×多厂商)一致判定 blocker —— 现有 κ = 1.000 来自三个共享预训练语料的 LLM 在共同定义提示下的一致性，等同于"同一评分者投三票"，无法作为方法论意义上的独立人类可靠性证据。

---

## 1. 标注任务定义

### 1.1 被标注对象

**Set N**：由 NOETHER 算子代数的 8-block 分解推导的 MR 集合，在两个实验底层语料上共有以下标注单元：

| 底层 | 主题数 | MR 总数 | 标注单元 |
|---|---|---|---|
| GenMorph 基准（§6.6 主要底层） | 23 个 Java 方法 | 71 条 | 71 条 MR |
| Apache Commons Math 扩展（§6.6 威胁分析）| 3 个方法 | 5 条 | 5 条 MR |
| **合计** | 26 | **76 条 MR** | **76 个标注单元** |

如人手不足，以 GenMorph 底层的 71 条为**最低标注集**（此为 § 6.6 主结果的直接支撑）。

### 1.2 标注任务 A：MR-Block 分类

每个标注单元需要 rater 独立判断该 MR 所对应的 **NOETHER 算子块**，从以下 8 个标签中选 1 个：

| 标签 | 全名 | 代表性不变量示例 |
|---|---|---|
| `G` | 群对称性 / 置换 | `f(−x) = −f(x)`（奇函数）；`gcd(a,b) = gcd(b,a)`（交换律）|
| `L_star` | 极限 / 不动点 / 闭包 | `f(f(x)) = f(x)`（幂等）；`f(0) = 0`（零点）|
| `T_star` | 平移算子 / 可加性 | `log(2x) = log(x)+1`（对数平移）|
| `D_star` | 动力学 / 轨迹不变量 | 物理守恒量（动量、能量）|
| `E_star` | 方法等价性 | 两个独立实现同一规格 |
| `O_le` | 序关系 / 有界性 | `\|sin(x)\| ≤ 1`；`gcd(a,b) ≤ min(a,b)` |
| `T_rev` | 时间反转 / 正反对称 | 布尔排斥：`¬(f(x) ∧ f(rev(x)))` |
| `B_rel` | 关系型（多体）| 序列上的关系断言 |

**判定规则**：选择最主要的代数特征。当 MR 可以论证属于多个块时，选择**最精确**（最不包含）的块。有疑问时可填写第二候选标签并附注理由（这不计入κ，仅用于审计）。

### 1.3 标注任务 B：D1 / D2 分层

对于 GenMorph 底层的每条 MR（71 条），rater 还需判断：该 MR 所关联的算子块，是否能够**理论上**检测到 D1 类突变（违反该块不变量的突变子）？

| 标签 | 定义 |
|---|---|
| `D1` | 该 MR 所在块的不变量在此 MR 中被明确断言；一个违反该不变量的突变子**原则上**应被该 MR 检测到 |
| `D2` | 该 MR 所在块的不变量不针对当前 SUT 的语义；即使突变改变了程序行为，该 MR 的断言形式也不会触发 |

**说明**：D1/D2 是关于**理论可达性**的判断，不是关于实际执行杀死率的判断。rater 不需要运行任何实验。

---

## 2. Rater 资质与数量

### 2.1 最低要求（化解 TOSEM blocker 的底线）

| 角色 | 人数 | 资质要求 |
|---|---|---|
| 主 rater（Primary rater） | **2 人** | 软件工程研究生或以上；有变异测试（MT）或蜕变测试（MRT）相关课程/项目经历；能阅读 Java 函数签名及简单断言 |
| 第三 rater（Tiebreaker） | **1 人** | 相同资质；**仅在主 rater 出现分歧时**调度介入；不参与初始独立标注 |

**合计最低：2 人主标注 + 1 人备用 tiebreaker（共 3 人）**

### 2.2 推荐规模（增强说服力）

| 方案 | 规模 | 适用场景 |
|---|---|---|
| 最低方案 | 2 主 + 1 备 | 单一报告期刊（TOSEM）|
| 推荐方案 | **3 主** | 所有三人同时独立标注，直接用 Fleiss κ；不需要 tiebreaker 机制 |
| 增强方案 | 4 主 | 可交叉计算多对 Cohen κ；适合高重视 inter-rater 的安全关键领域期刊 |

### 2.3 独立性要求（关键，针对现有 LLM-κ 缺陷的直接应对）

- 主 rater 之间**禁止讨论**，直至各自完成全部标注并提交
- 主 rater **不得事先阅读**作者给出的 block 归类结果（即论文附录 / 代码中的 `configs/lrca_llm_labels.json` 内容）
- 主 rater 可以阅读 NOETHER 框架中的 **8-block 定义说明**（培训材料），但该材料**不得包含**任何 MR 的例题答案

---

## 3. 培训材料（Training Materials）

培训材料须在标注开始前发给每位 rater，包含以下内容，且**不含**任何 Set N MR 的参考答案：

### 3.1 必须提供

1. **8-block 定义卡**（见 3.2 节）— 每个块的定义、数学含义、1 个训练例题（来自 Set N 之外的函数）
2. **JIR/JOR DSL 简介**（1 页）— GAssert `.jir.txt` / `.jor.txt` 格式说明：`i_<arg>_{s,f}` 是输入的 source/follow 执行；`o_return_{s,f}` 是输出的 source/follow 执行
3. **D1/D2 判定指南**（0.5 页）— 含 2 个明确的 D1 示例和 2 个明确的 D2 示例（来自 Set N 之外的函数）
4. **标注表格**（Excel 或 Google Sheets）— 每行 1 条 MR，包含 MR ID、JIR 文本、JOR 文本，共 4 列输出：Block-Task-A、D1D2-Task-B、可选第二候选、备注

### 3.2 8-Block 定义卡（核心培训内容）

rater 培训卡应包含以下定义，**用自然语言**而非公式（以提高非理论背景 rater 的可及性）：

> **G（群对称性）**：输入做某种变换后，输出做对应变换，或输出不变。例："交换两个参数，结果不变"；"翻转符号，输出也翻转符号"。JIR 会改变输入，JOR 断言输出与原始输出之间有对称关系。
>
> **L\_star（极限/不动点/闭包）**：特殊边界输入产生特殊固定输出；或对输出再应用函数等于不变。例："输入 0 输出 0"；"对一个已排好序的列表再排序，结果不变"；"空字符串情形"。
>
> **T\_star（平移/可加性）**：对输入做倍数缩放，输出按可加量移动。原型：对数函数的乘法→加法性质，即 `f(c·x) = f(x) + const`。
>
> **O\_le（序/有界性）**：输出满足某个不等式约束。例："gcd 不超过两个参数的最小值"；"sin 的绝对值不超过 1"。JOR 通常包含 `<=` 或 `>=`，JIR 通常是 identity（source 和 follow 输入相同）。
>
> **T\_rev（时间反转/前向-后向排斥）**：对输入做某种"逆操作"（逆序、取反），布尔输出与原始输出互斥。JOR 形式为 `!(f(x) && f(rev(x)))`。
>
> **B\_rel（关系型）**：对多个输入的关系进行断言，不对某单一变换做断言。
>
> **D\_star（动力学/轨迹）**：系统随时间演化的物理不变量（守恒律）。在本语料（Java 数学工具方法）中通常为**空块**。
>
> **E\_star（方法等价性）**：同一规格的两个独立实现给出相同输出。在本语料中通常为**空块**。

---

## 4. 标注程序

### 4.1 总体流程

```
阶段 0：招募与培训（共约 2 小时）
  └─ 0.1  rater 签署独立性承诺（不讨论、不看参考答案）
  └─ 0.2  发放培训材料（3.1 节）
  └─ 0.3  培训练习：共同完成 3 条来自 Set N 之外的练习题，讨论到共识后开始正式标注

阶段 1：独立标注（每人约 2–4 小时）
  └─ 1.1  每位 rater 独立完成全部 71（或 76）条标注
  └─ 1.2  不得相互讨论，不得查阅参考答案
  └─ 1.3  按 4.3 节检查表自查后提交标注表格

阶段 2：κ 计算与分歧审计（约 0.5 小时）
  └─ 2.1  汇集所有 rater 表格，运行 4.4 节脚本
  └─ 2.2  输出 Cohen κ（两两）、Fleiss κ（全体）
  └─ 2.3  列出所有分歧条目（rater 间不一致的 MR）

阶段 3：分歧解决（约 1 小时）
  └─ 3.1  全体 rater 公开讨论分歧条目（此时才允许讨论）
  └─ 3.2  若 2 主 rater 方案，tiebreaker 对分歧条目单独标注
  └─ 3.3  采用多数裁定，记录最终标签与分歧原因

阶段 4：文档化
  └─ 4.1  写入论文附录：κ 值、分歧条目数、解决机制
  └─ 4.2  将标注表格与 lrca_llm_labels.json 并排存入 docs/
```

### 4.2 时间估算

| 任务 | 每条 MR 耗时 | 71 条合计 |
|---|---|---|
| Task A（Block 分类）| 2–4 分钟 | 2.4–4.7 小时 |
| Task B（D1/D2）| 1–2 分钟 | 1.2–2.4 小时 |
| 合计（含休息）| — | **3.5–6 小时 / 人** |

建议分两个 session（上午 Task A，下午 Task B）完成，避免疲劳效应。

### 4.3 rater 自查检查表（提交前）

```
□ 是否每一条 MR 都填写了 Task A（Block 标签）？
□ 是否每一条 MR 都填写了 Task B（D1/D2 标签）？
□ 空块（D_star、E_star）若被选中，是否附写了理由？
□ 没有与其他 rater 讨论过任何标注内容。
□ 没有参阅 configs/lrca_llm_labels.json 或任何参考答案。
```

---

## 5. Cohen / Fleiss κ 计算规范

### 5.1 适用公式选择

| 方案 | rater 数 | 公式 | 报告指标 |
|---|---|---|---|
| 最低方案（2 主 rater）| 2 | Cohen's κ | κ ± 95% CI；p 值（双侧）|
| 推荐方案（3 主 rater）| 3 | Fleiss' κ（全体）+ Cohen's κ（两两）| Fleiss κ；三对 Cohen κ 分别报告 |

**Task A（Block 分类）** 与 **Task B（D1/D2）** 分别独立计算 κ，因为两者是不同类别数量的分类问题（Task A 为 8 类；Task B 为 2 类二元分类）。

### 5.2 Cohen's κ 计算公式

$$\kappa = \frac{p_o - p_e}{1 - p_e}$$

其中：
- $p_o$：观察一致率 = (一致条目数) / (总条目数)
- $p_e$：期望一致率 = $\sum_k p_{k,R1} \cdot p_{k,R2}$（$k$ 遍历所有标签类别）

95% CI 使用 Fleiss-Cohen 渐近正态近似：

$$SE(\kappa) = \sqrt{\frac{p_o(1-p_o)}{n(1-p_e)^2}}$$

$$95\% \text{ CI} = \kappa \pm 1.96 \cdot SE(\kappa)$$

### 5.3 Fleiss' κ 计算公式（3+ rater）

$$\bar{P} = \frac{1}{n \cdot r} \sum_{i=1}^{n} \sum_{j=1}^{k} n_{ij}(n_{ij}-1) / (r-1)$$

$$P_e = \sum_{j=1}^{k} \left(\frac{\sum_i n_{ij}}{n \cdot r}\right)^2$$

$$\kappa_F = \frac{\bar{P} - P_e}{1 - P_e}$$

### 5.4 标准计算脚本（Python）

```python
#!/usr/bin/env python3
"""
usage:  python3 scripts/compute_human_kappa.py \
            --input data/human_rater_labels.csv \
            --task A   # 或 --task B
"""
import argparse
import pandas as pd
import numpy as np
from itertools import combinations

def cohen_kappa(labels_r1, labels_r2):
    n = len(labels_r1)
    assert n == len(labels_r2), "rater arrays must have same length"
    cats = sorted(set(labels_r1) | set(labels_r2))
    agree = sum(a == b for a, b in zip(labels_r1, labels_r2))
    p_o = agree / n
    p_e = sum(
        (labels_r1.count(c) / n) * (labels_r2.count(c) / n)
        for c in cats
    )
    if p_e == 1.0:
        return 1.0, 0.0   # constant rater edge case — see §6
    kappa = (p_o - p_e) / (1 - p_e)
    se = np.sqrt(p_o * (1 - p_o) / (n * (1 - p_e) ** 2))
    return kappa, 1.96 * se

def fleiss_kappa(rating_matrix):
    """rating_matrix: ndarray shape (n_items, n_raters), values = category indices"""
    n, r = rating_matrix.shape
    cats = np.unique(rating_matrix)
    # Build n×k count matrix
    k = len(cats)
    counts = np.zeros((n, k), dtype=int)
    for j, c in enumerate(cats):
        counts[:, j] = (rating_matrix == c).sum(axis=1)
    p_j = counts.sum(axis=0) / (n * r)
    P_e = (p_j ** 2).sum()
    P_i = ((counts * (counts - 1)).sum(axis=1)) / (r * (r - 1))
    P_bar = P_i.mean()
    if P_e == 1.0:
        return 1.0
    return (P_bar - P_e) / (1 - P_e)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--task", choices=["A", "B"], required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    col = "block" if args.task == "A" else "d1d2"
    rater_cols = [c for c in df.columns if c.startswith("rater_")]
    
    print(f"\n=== Task {args.task} ({'Block classification' if args.task=='A' else 'D1/D2 layering'}) ===")
    print(f"Items: {len(df)}, Raters: {len(rater_cols)}\n")

    # Cohen κ for each pair
    kappas = []
    for r1, r2 in combinations(rater_cols, 2):
        mask = df[r1].notna() & df[r2].notna()
        l1 = list(df.loc[mask, r1])
        l2 = list(df.loc[mask, r2])
        k, ci = cohen_kappa(l1, l2)
        kappas.append(k)
        print(f"Cohen κ ({r1} vs {r2}): {k:.3f}  [95% CI ±{ci:.3f}]  n={mask.sum()}")

    # Fleiss κ
    if len(rater_cols) >= 3:
        mat_df = df[rater_cols].dropna()
        # Encode categories to integers
        all_cats = sorted(set(v for col in rater_cols for v in df[col].dropna()))
        cat_map = {c: i for i, c in enumerate(all_cats)}
        mat = mat_df.applymap(lambda x: cat_map[x]).values
        fk = fleiss_kappa(mat)
        print(f"\nFleiss κ (all {len(rater_cols)} raters): {fk:.3f}  n={len(mat_df)}")

    print(f"\nMean Cohen κ across pairs: {np.mean(kappas):.3f}")
    print(f"\nLandis-Koch band:")
    kappa_val = np.mean(kappas)
    if kappa_val < 0:    band = "poor"
    elif kappa_val < 0.20: band = "slight"
    elif kappa_val < 0.40: band = "fair"
    elif kappa_val < 0.60: band = "moderate"
    elif kappa_val < 0.80: band = "substantial"
    else:                band = "almost perfect"
    print(f"  κ = {kappa_val:.3f} → {band}")

if __name__ == "__main__":
    main()
```

**输入格式**（`data/human_rater_labels.csv`）：

```
mr_id,rater_1,rater_2,rater_3
MathClass?gcd?0@rho_perm,G,G,G
MathClass?gcd?0@rho_scale,O_le,O_le,G
MathClass?sin?0@rho_oddsym,G,G,G
...
```

Task B 时将 `block` 列替换为 `d1d2` 列，值为 `D1` 或 `D2`。

### 5.5 通过门槛（TOSEM 可接受下限）

| 指标 | 化解 blocker 最低门槛 | 推荐目标 |
|---|---|---|
| Task A Cohen κ（任意两人对）| ≥ 0.60（substantial）| ≥ 0.80（almost perfect）|
| Task A Fleiss κ（3 人方案）| ≥ 0.60 | ≥ 0.80 |
| Task B Cohen κ（D1/D2 二元）| ≥ 0.70 | ≥ 0.80 |
| 分歧条目占比 | ≤ 25%（任意一对）| ≤ 15% |

如低于最低门槛，必须：(1) 检查是否存在 rater 理解偏差（通过培训不足的 8-block 定义），(2) 检查是否有 rater 触发常数 rater 排除条件（§6 节），(3) 修订培训材料后重新标注。

---

## 6. Rater-Validity Screen（常数 rater 排除）

### 6.1 常数 rater 定义

若某 rater 对 Task A 中 ≥ 80% 的 MR 分配了**同一个块标签**（如全部标注为 `G`），则该 rater 被判定为**常数 rater（constant rater）**，其数据须从 κ 计算中排除。

**形式化定义**：设 rater $r$ 的标注向量为 $\mathbf{l}_r = (l_1, \ldots, l_n)$，若 $\max_k \text{count}(l_r = k) / n > 0.80$，则判定为常数 rater。

### 6.2 检测脚本

```python
def screen_constant_rater(labels: list, threshold=0.80) -> tuple[bool, str]:
    """
    Returns (is_constant, majority_label).
    A constant rater assigns >threshold of items to one category.
    """
    from collections import Counter
    counts = Counter(labels)
    n = len(labels)
    most_common_label, most_common_count = counts.most_common(1)[0]
    ratio = most_common_count / n
    return ratio > threshold, most_common_label

# 集成到主脚本
for rater_col in rater_cols:
    labels = list(df[rater_col].dropna())
    is_const, majority = screen_constant_rater(labels)
    if is_const:
        print(f"WARNING: {rater_col} is a constant rater "
              f"(>{80}% assigned '{majority}') — EXCLUDED from κ")
```

### 6.3 排除后处理

- 常数 rater 数据从 κ 计算中排除，但其个体标注数据保留存档
- 若排除后剩余 rater 少于 2 人，需招募额外 rater 后重新计算
- 在论文附录中明确报告："共招募 N 人，其中 M 人因常数 rater 测试被排除"

---

## 7. 与现有共享语料 LLM κ 的关系

### 7.1 现有 LLM κ 数据（`docs/lrca_results.md`）

| 指标 | 值 | 问题 |
|---|---|---|
| Cohen κ（作者 vs 任意单 LLM）| 0.927–0.929 | LLM 提示嵌入了 block 定义，等同于开卷考试 |
| Fleiss κ（三 LLM 之间）| **1.000** | 三个 LLM 共享预训练语料，等同于"同一评分者三票" |
| 分歧审计 | 2/36（5.6%）| 两处分歧均有 LLM 论据，但 LLM 倾向于依赖表面结构匹配 |

**根本缺陷**：Fleiss κ = 1.000 在技术上成立，但不具备独立性（independent raters）的核心假设。三个 LLM 在相同提示和相同定义下达成一致，与三个被告知答案后打分的人类达成一致，在统计上等价。TOSEM R2 和 DA 审稿人正确识别了这一缺陷。

### 7.2 两种 κ 的互补角色（论文中的呈现方式）

建议在论文 §6.6（威胁分析或可靠性分析）中采用以下分层呈现：

**第一层（量产式可靠性）**：  
"我们使用三个 LLM 进行 inter-rater 一致性测试（Cohen κ ≈ 0.93），以快速覆盖全部 71 条 MR 的分类。该设置的局限是 LLM 之间共享预训练知识，Fleiss κ = 1.000 不等于独立的人类判断。"

**第二层（独立性证据）**：  
"为建立独立可靠性基准，我们另行招募 [N] 位人类 rater（具备变异测试知识，未参与论文写作）对 [71] 条 MR 进行盲标注，获得人类 Cohen/Fleiss κ = [X.XXX]（[band]），与 LLM κ 量级一致，且满足独立性要求。"

**两者不冲突**：LLM κ 是效率工具（快速覆盖，低成本），人类 κ 是独立性证明（满足期刊方法论要求）。在 TOSEM 期望的可靠性报告中，**人类 κ 是必须的**，LLM κ 可作为补充。

### 7.3 如果人类 κ < LLM κ（预期场景处理）

LLM κ ≈ 0.93 设置了一个几乎不可能达到的比较基准（因为是开卷+共享语料）。人类 κ 很可能落在 0.70–0.85 区间，低于 0.93。

**这不是问题**，应在论文中主动说明：

> "Human κ = X.XX（substantial/almost perfect），低于 LLM κ = 0.93，这一差异是预期的：LLM 标注基于嵌入 block 定义的提示（相当于参考答案辅助），而人类 rater 仅有培训材料且独立作出判断。人类 κ 体现的是无提示援助下的分类难度，LLM κ 体现的是框架定义本身的内部一致性。两者均为 substantial/almost perfect，共同支持 Set N block 分类的可靠性。"

---

## 8. 协议执行检查清单

### 8.1 启动前（研究者）

```
□ 标注材料已准备：8-block 定义卡 + DSL 简介 + D1/D2 指南 + 标注表格
□ 培训材料中不含任何 Set N MR 的参考答案（不包含 configs/lrca_llm_labels.json 内容）
□ 3 条练习题来自 Set N 之外的函数，已附答案
□ 每位 rater 已签署独立性承诺
□ 标注期间沟通禁止期已明确（阶段 1 禁止讨论）
□ 数据收集格式（CSV）已确认
```

### 8.2 标注结束后（研究者）

```
□ 所有 rater 已提交标注表格
□ 已运行 §6.2 常数 rater 排除检测
□ 已运行 §5.4 κ 计算脚本（Task A 和 Task B 分别运行）
□ κ 达到 §5.5 通过门槛
□ 分歧条目已列出，已按阶段 3 流程解决
□ 最终标签表已存入 docs/human_rater_labels_final.csv
□ 审计摘要已存入 docs/human_kappa_audit.md
□ 论文 §6.6 可靠性分析段已引用人类 κ 结果
```

### 8.3 TOSEM blocker 化解确认

本协议执行完毕后，下列 blocker 条目可标记为已解决：

> NEXT_STEPS.md 🔴 Blockers 第 3 条：  
> "缺独立人类 inter-rater κ（κ=1.000 是共享语料 LLM 循环）— 自招 ≥2 名独立 rater 做 Cohen's κ"

**达成条件**：Task A Cohen κ ≥ 0.60（substantial），Task B Cohen κ ≥ 0.70，分歧条目已解决，结果写入论文 §6.6。

---

## 附录 A：标注输入材料格式（MR 呈现方式）

每条 MR 向 rater 呈现如下（以 `MathClass?gcd?0@rho_perm` 为例）：

```
MR ID:  MathClass?gcd?0@rho_perm
方法名: gcd(int a, int b)
方法说明: 返回 a 和 b 的最大公因数

输入变换（JIR）:
  i_a_f = i_b_s
  i_b_f = i_a_s
  （即交换两个参数）

输出断言（JOR）:
  o_return_f == o_return_s
  （即输出不变）

Task A: 该 MR 对应哪个 NOETHER 算子块？
  [ ] G  [ ] L_star  [ ] T_star  [ ] O_le
  [ ] T_rev  [ ] B_rel  [ ] D_star  [ ] E_star
  第二候选（可选）: ___  理由: ___

Task B: 该 MR 是否理论上能检测违反其所在块不变量的突变子（D1）？
  [ ] D1  [ ] D2  备注: ___
```

---

## 附录 B：分歧解决记录模板

```
MR ID: _______________
Task A / B: ___
Rater 1 标签: ___  Rater 2 标签: ___  (Rater 3 标签: ___)
分歧类型: [ ] 边界案例  [ ] 培训理解差异  [ ] 真实语义模糊
解决方法: [ ] 多数裁决  [ ] tiebreaker  [ ] 专家协商
最终标签: ___
解决依据（1–2 句）: _______________________________
```