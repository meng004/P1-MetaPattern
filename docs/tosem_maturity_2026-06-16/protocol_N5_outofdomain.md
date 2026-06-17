# N5 协议 — 域外迁移性验证(防循环,辩护 C4)

> 状态:**方案**(待执行;需新域 + ≥2 名非作者领域专家)。本文不执行实验,只定协议 + 说明理由。
> 目标贡献:把 C4(transferability)从"只在我们设计的域上成立"(circular)升级为
> "在框架未参与构建的新域上,冻结的 8-block 仍能迁移并推导出专家确认的有效 MR"。

> **执行状态(2026-06-17)**:**工业代码 leg 已执行**(`N5_industrial_results.md` /
> `supplementary/S11_n5_industrial/`):110 条专家认可 MR(BAMBOO-C SPARK/LOCUST + SACOS)
> 由冻结 O≤ 块 100% 覆盖、0 orphan、18 条超集发现。**诚实限定:单块(O≤)+ 同核领域代码级
> held-out**,非"非物理多块跨域"。**待补 leg 2(数值线代/DSP/几何)**以激发 G/T\*/L\*/E\* +
> IBT 紧块,合成完整 C4。

---

## 0. 为什么需要 N5(说明理由)

**被辩护的攻击(circularity)**:C4 现有的三个域(Boltzmann / equivariant ML / relational)
中,8-block 分解**部分是从这些域(及作者 PWR 目录)归纳蒸馏出来的**。审稿人最可能的
攻击:"你的块是为你测试的域量身定制的(fit-to-test);迁移性是同义反复。"§5 的 9-SUT
home-field 虽是执行型证据,但**仍在物理域内**,未脱离这一质疑。

**N5 如何破循环**:在一个**未参与块构建的新域**上,用**冻结的(已发表的)8-block**跑
CONSTRUCT-MP,由**不知情的非作者领域专家**盲评。若冻结块在未见域上 (i) 覆盖该域已知 MR
且 (ii) 推导出专家确认、此前未编目的有效 MR,则 fit-to-test 闭环被打破,C4 得到**非循环**
证据。其逻辑等价于机器学习的 held-out test:块在"训练域"上拟合,N5 是"测试域"。

**附带收益**:N5 的专家评估是**人类 + 领域特定**,因此也是对 N2(shared-corpus)blocker
的最强可得回应(虽 N2 本身已按 b 诚实降级)。

---

## 1. 域选择(criteria + 候选)

**必备判据**:
- (C-a) 满足框架 scope precondition:该域**有显式算子代数**;
- (C-b) **未用于 8-block 构建**(非 Boltzmann / equivariant ML / relational / PWR);
- (C-c) 存在**独立发表的 MR / 性质语料**(使"覆盖"与"新颖"可核验);
- (C-d) 可获得 **≥2 名非作者领域专家**;
- (C-e) 与现有三域**结构有别**(最好非 PDE 物理,最大化反循环)。

**候选(供作者按 C-d 专家可得性定选)**:

| 候选域 | 算子代数 | 已知 MR 语料 | 反循环强度 | 备注 |
|---|---|---|---|---|
| **数值线性代数库**(dense solve / eig / QR,LAPACK 类) | 自伴($A=A^\top$)、序(谱)、method-comparison(直接 vs 迭代)、limit(收敛) | Xie/Siegmund 科学函数 MT;线代恒等式 | 高(非 PDE) | T\*/E\*/L\* 块直接;专家易得(SE/HPC) |
| **数字信号处理**(FFT / 滤波器) | 平移/调制对称(G)、自伴、limit、相位 | 经典 MR:线性、时移、Parseval、调制 | 高(非物理-PDE) | G/T\* 强;语料成熟 |
| **计算几何谓词**(凸包 / Delaunay,CGAL 类) | 刚体运动 + 点置换(G)、定向序(O≤)、exact-vs-float(E\*)、几何恒等(B_rel) | 谓词鲁棒性 MR;几何恒等式 | 最高(完全非物理) | 四块覆盖好;专家=计算几何 |

**首选建议**:**数值线性代数库** —— 算子代数最显式(矩阵即算子)、与 IBT 的线性故障类
天然契合(可直接复用 N4 的 FA-rank 机制做该域的紧性验证)、专家最易得。**次选**:DSP。

---

## 2. 预注册 + 盲化(反循环核心)

1. **冻结块**:8-block 定义 + CONSTRUCT-MP **以已发表版本为准,N5 期间不得修改**(若新域
   暴露缺块,记为候选第九块,不回改框架——符合论文 open-block 立场)。
2. **预注册**(实验前公开存档,时间戳):
   - 新域的算子代数 $\mathcal{A}_{\mathrm{new}}$ 蒸馏;
   - **块占据预测**:在看任何 MR 语料**之前**,预测哪些块非空(检验 L1/block-law 迁移);
   - CONSTRUCT-MP 运行配置 + 容差;
   - 成功判据(§4,预注册,事后不得改)。
3. **盲化**:
   - 领域专家**不得事先看** NOETHER 对该域的推导 / 块归类;
   - 专家拿到的是**混合 MR 池**(NOETHER 推导 arm + 该域已知语料 arm),**provenance 抹去**,
     随机排序;专家不知道哪条来自哪 arm。

---

## 3. 两臂盲评

| Arm | 来源 | 用途 |
|---|---|---|
| **A(NOETHER)** | 冻结块 CONSTRUCT-MP 在 $\mathcal{A}_{\mathrm{new}}$ 上推导的 MR | 测覆盖 + 新颖性 |
| **B(对照)** | 该域**独立发表**的 MR 语料 | 锚点(已知 MR 基线) |

每条 MR,≥2 名专家**独立**判:
- **(J1) 有效性**:该 MR 对该域程序是否成立(valid / invalid / uncertain);
- **(J2) 新颖性**:是否已在该域文献中编目(known / novel / uncertain);
- 专家间 agreement 报 Cohen/Fleiss κ(**该域人类 κ**,顺带补 N2 的人类信度证据)。

---

## 4. 度量 + 预注册成功判据

| 指标 | 定义 | 预注册门槛 |
|---|---|---|
| **块占据预测命中** | 预测非空块 = 实际非空块(逐块二元) | ≥ (#块−1)/#块 命中 |
| **覆盖(subsumption)** | Arm B 已知 MR 中被某 NOETHER 块捕获的比例 | ≥ 70%(Wilson 95% CI 报告) |
| **构造性发现(novelty)** | Arm A 中"专家判 valid ∧ novel"的 MR 数 | ≥ 1(非循环 discovery) |
| **专家信度** | J1/J2 的 inter-rater κ | substantial ≥ 0.6 |
| **缺块(honest failure)** | Arm B 中无任何 NOETHER 块捕获的 MR 类 | 如实记为候选第九块,不隐瞒 |

**判读**:
- 覆盖达标 + 块预测命中 → **迁移性(C4 的 transfer 部分)非循环成立**;
- novelty ≥ 1(专家确认)→ **constructive discovery 在未见域成立**(C3 升级,脱离 shared-corpus);
- 出现缺块 → 不是失败,是框架 open-block 立场的**预期可证伪点**,据实报告。

---

## 5. 威胁与诚实处理

- **专家偏差**:专家可能偏好熟悉的 Arm B 形式 → 盲化 + provenance 抹除 + 随机序缓解。
- **语料不全**:Arm B 若不完整,novelty 可能假阳(把已知误判为新)→ 用 ≥2 专家 + 文献复核。
- **新域选择偏差**:不得"试多个域只报成功的"——**预注册单一首选域**,失败则如实报告并按
  §6 回退,不换域重试(HARKing 红线,CLAUDE.md §6)。
- **冻结违例**:N5 期间若手痒改块定义以迁就新域,即自我污染——严禁,块必须冻结。

---

## 6. 回退(若无专家 / 资源)

若 C-d(≥2 非作者专家)无法满足:**诚实降级 C4** —— 正文把 transferability 明确限定为
"structural transferability **within the designed domains**(Boltzmann / equivariant ML /
relational)+ a same-physics home-field benchmark(§5)",并把 N5 列为 committed follow-up。
此回退**可投**(C4 弱化但不虚假),与 N2(b) 的降级姿态一致。

---

## 7. 执行清单(供将来落地)

```
□ 0  选定首选域(默认:数值线性代数库)+ 招募 ≥2 非作者专家
□ 1  冻结 8-block 版本(git tag);预注册 A_new 蒸馏 + 块占据预测 + 判据(时间戳存档)
□ 2  跑 CONSTRUCT-MP(冻结块)→ Arm A MR 集
□ 3  收集 Arm B(该域已发表 MR 语料)+ 文献核实
□ 4  构建混合盲评包(抹 provenance、随机序)
□ 5  ≥2 专家独立判 J1/J2 → 计 κ + 覆盖 + novelty + 块预测命中
□ 6  对照 §4 判据;缺块如实记为候选第九块
□ 7  结果写入正文 §Empirical(C4 / C3)+ 审计存档 docs/review_N5/
```

---

## 8. 与 N2/N4 的关系

- **N4**(已完成):FA/紧性绑定到真算子;若 N5 选数值线代域,**N4 的 FA-rank 脚本可直接复用**
  到新域算子,给该域的 IBT 紧性提供同款证据。
- **N2(b)**(已完成):κ 诚实降级;N5 的**领域专家 κ**是对 N2 的正向补强(人类、域特定)。
- 三者合力:N4 加固理论-真算子绑定,N2(b) 卸下循环 κ,N5 在未见域上非循环验证 C4 + C3。
