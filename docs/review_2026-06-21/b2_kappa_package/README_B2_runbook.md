# B2 — 独立人类 κ 执行包（runbook）

> **目的**：把 LLM-only 的 κ=0.931 升级为真正的 **human inter-rater κ**，破除自指评估的 *labelling 半壁*（B1 真 bug 腿破除 *fault-data 半壁*；两腿合起来才完整破 G3 硬墙）。
> **预注册 codebook（判据冻结）**：[`docs/review_2026-06-20/mvp_kappa_codebook.md`](../../review_2026-06-20/mvp_kappa_codebook.md) —— 评分前已固定的 8-block 判据卡 + 41 条待标 MR + 诚信约束。本包是它的**可执行化**。

---

## 1. 包内文件

| 文件 | 用途 | 谁动 |
|---|---|---|
| `author_labels.csv` | 41 条作者标签(36 条逐字来自 SSOT `lrca_llm_labels.json` + 5 条 SACOS 锚=O_le)。**只读**对照基准 | 已生成,勿改 |
| `kappa_labels_raterA_BLANK.csv` | rater A 空白模板(mr_id/sut_method/block/confidence/note) | 复制为 `kappa_labels_raterA.csv` 后由 rater A 填 |
| `kappa_labels_raterB_BLANK.csv` | rater B 空白模板 | 复制为 `kappa_labels_raterB.csv` 后由 rater B 填 |
| `compute_kappa.py` | 算 Cohen κ(A-B 主结果 / A-author / B-author)+ Fleiss κ + Wilson CI + 分歧清单 + conf≤2 敏感性 | 填完后跑 |

> **实测标签分布(36 条,SSOT 为准)**：G×9 · L_star×10 · O_le×6 · T_star×6 · D_star×2 · T_rev×1 · E_star×1 · B_rel×1（+ SACOS O_le×5 = O_le 共 11）。注：codebook §3.1 编者note 旧写"G8/L11/T_rev2/E2"算术有误，以本分布为准；逐条标签正确。
> **两处预置争议点(检验人类是否复现边界模糊)**：M08 exactLog2(作者 L_star vs LLM 多数 T_star)；M16/M20 字面完全相同的反序+互斥(作者分别归 B_rel / T_rev)。

---

## 2. 执行流程（作者侧）

```bash
cd docs/review_2026-06-21/b2_kappa_package
cp kappa_labels_raterA_BLANK.csv kappa_labels_raterA.csv   # 交 rater A
cp kappa_labels_raterB_BLANK.csv kappa_labels_raterB.csv   # 交 rater B
# 两名 rater 各自独立、盲标(见 §3)，填 block 列(+confidence 1-5, orphan 必填 note)
pip install scikit-learn statsmodels pandas
python3 compute_kappa.py        # 产出 kappa_results.md
```

`compute_kappa.py` 会校验：标签只能取 9 个合法值；不得留空(不确定填 `orphan`)；否则报错退出。

---

## 3. 招募与盲标硬约束（预注册，评分前固定）

1. **rater 须独立于作者**：作者本人、直系学生、共同署名人**不得**当 rater。需 ≥2 名对 NOETHER 无利益关系、具备读懂 JIR/JOR 最低基础的人员。
2. **盲标**：rater 只拿 codebook §2 判据卡 + §3 待标清单(已去作者/LLM 标签);**看不到** `author_labels.csv`、不参考论文实证表格、两名 rater 互不通气。
3. **判据冻结**：评分中不得改判据卡 / 不得增删块 / 不得调 canonical ordering。评分后发现歧义记入 limitations,**不回填**。

---

## 4. 如实报告（禁止救援，codebook §6）

- 若 human κ **显著低于** 0.931：**如实报告**,正文**弱化 C4**——把 0.931 改述为"LLM 佐证性广度",human κ 作确证数字("独立人类 κ=X(band Y),提示分类边界在人类判读下存在 Z% 分歧")。
- n=41 属 **underpowered for tight CI**：必同时报 Wilson 95% CI,明示样本量限制;**禁** "trends suggest / encouraging"(§6.9/C6)。
- 两处争议点(M08、M16/M20)若人类再现分歧,**保留并讨论**,不得删项抬 κ(selection-on-the-response 禁止)。

---

## 5. 结果回插论文

- κ 三份 CSV(raterA/raterB/author)+ `kappa_results.md` 归档到 `docs/review_<DATE>/`,response letter 引用,复核者可重算。
- 正文 §8(现报 majority-vs-author Cohen κ=0.931 处)补 human inter-rater κ 为**领头数字**;LLM-κ 降为佐证。
- 与 **B1 真 bug 腿**(`b1_cloud_task.md`)合起来,才完整回应面板 G3 自指 CRITICAL：B1 破 fault-data 自指,B2 破 labelling 自指。**单做一腿不够。**

---

## 6. 范例 walkthrough（✅ 可随判据卡一并发给 rater）

> ⚠️ **锚定红线**：本节示例**只用语料外的全新 MR**,不含 41 条待标题中的任何一条,故不会泄露答案、不锚定 rater。请勿在发给 rater 的材料中附带 §1 的 `author_labels.csv` 或 §7。

每条 MR 看两段谓词:**JIR**(源输入→衍生输入怎么变)与 **JOR**(两次输出该满足的关系)。读完判据卡后,逐条问"JIR 是哪种变换?JOR 是哪种关系?"再对照 §2.10 速查表落一个标签。

**范例 A（→ G）** SUT `cube(x)=x³`
- JIR:`x_f = -x_s`(输入整体取负) JOR:`out_f = -out_s`(输出取负)
- 判读:离散 ×(−1) 对合 + 输出协变取负(奇函数对称)→ 判据卡 §2.1 → **`G`**,confidence 5。

**范例 B（→ L_star）** SUT `circleArea(r)=πr²`
- JIR:`r_f = 2·r_s`(输入 ×2) JOR:`out_f = 4·out_s`(输出 ×4)
- 判读:乘性缩放齐次 `f(k·x)=φ(k)·f(x)`,这里 φ(k)=k²(degree-2)→ 判据卡 §2.5 → **`L_star`**。注意:JIR 是 ×k 不是 +c(那会是 `T_star`),也不是 ≤ 不等式(那会是 `O_le`)。

**范例 C（→ orphan，合法）** SUT `embed(x)`(向量嵌入)
- JIR:`x_f = x_s + ε·u`(微扰,‖u‖=1) JOR:`dist(out_f, out_s) ≤ K·ε`(Lipschitz 界)
- 判读:这是**度量稳定性**关系。判据卡 §2.9 明确:Lipschitz/度量稳定属"候选第九块/8 块之外"→ 不要硬塞进 8 块,填 **`orphan`** + note 写"metric-stability / Lipschitz, not an 8-block operator"。**orphan 是合法答案,不是失败。**

**填表**(在你那份 `kappa_labels_raterX.csv`):
```csv
mr_id,sut_method,block,confidence,note
M01,ComplexSignal.add,G,5,
...
M08,exactLog2,<你的判断>,3,<不确定就写理由>
...
```
要点:`block` 列只能取 9 个合法值(`G/O_le/T_star/T_rev/L_star/D_star/E_star/B_rel/orphan`,大小写逐字);**不得留空**,不确定就填 `orphan`;`confidence` 1–5;遇到看似可归多块,按 canonical 优先级 **G > O_le > T\* > 𝒯\*_rev > L\* > D\* > E\* > B\*_rel** 取更高块。**两名 rater 互不通气、不参考论文表格。**

---

## 7. 协调者参考：κ 输出范例与解读（⚠️ 勿展示给 rater——含 41 题分歧,会锚定）

下面是用脚本跑出的**示意输出**(rater 标签为演示编造,非真实数据),供你理解 `kappa_results.md` 长什么样、怎么解读:

```
$ python3 compute_kappa.py
OK: n=41  Cohen kappa(A,B)=0.847 (almost perfect)  Fleiss=0.898
```

| 比较 | κ | Landis-Koch |
|---|---:|---|
| **raterA vs raterB(主结果,人类互评)** | **0.847** | almost perfect |
| raterA vs author | 0.908 | almost perfect |
| Fleiss(A,B,author) | 0.898 | almost perfect |

观察一致率 36/41=0.878,**Wilson 95% CI [0.745, 0.947]**。脚本自动列出分歧项,通常集中在两处预置争议点 + 个别边界:

| mr_id | A | B | author |
|---|---|---|---|
| M08 | T_star | L_star | L_star |（exactLog2:对数域平移 vs 极限/对数幂）
| M16 | T_rev | B_rel | B_rel |（反序+互斥）
| M20 | T_rev | B_rel | T_rev |（与 M16 字面完全相同）

**解读三要点**：
1. **若 human κ < LLM-only 0.931**(本例 0.847)→ 正文**弱化 C4**:0.931 改述为"LLM 佐证性广度",human κ 作确证数字。
2. **n=41 欠功效** → 必报 Wilson CI,**禁** "trends suggest / encouraging"。
3. **M16/M20**(字面完全相同却被作者分标 B_rel/T_rev)若在人类处被给同一标签 → 这正是 B2 要暴露的:该区分在独立盲标下站不住。**保留并讨论,不得删项抬 κ。**
