# N5 执行(工业代码 leg)— BAMBOO-C + SACOS 覆盖分析

> 输入:作者提供的**专家认可** MR 语料(N5 协议 Arm B,J1 有效性已给定)。
> 代码:`supplementary/S11_n5_industrial/`(`mr_corpora.md` 语料 + `classify_n5.py` 分类 +
> `results/`)。冻结 8-block,无重拟合。

## 1. 做了什么

把 110 条专家 MR(BAMBOO-C 的 SPARK 36 + LOCUST 28 + SACOS 46)对照**冻结的** NOETHER
8-block 做覆盖分类(规则式,按各块结构线索归类;非套套逻辑——若有对称/守恒/极限/方法
比较等线索会归别处)。这是 N5 的 **coverage / block-occupancy arm**,代码级 held-out
(框架未对这些代码的 MR 拟合)。

## 2. 结果

| 代码 | MRs | 覆盖 | 占据块 | 新发现 |
|---|---|---|---|---|
| SPARK | 36 | 36/36 | O≤ | 6 |
| LOCUST | 28 | 28/28 | O≤ | 6 |
| SACOS | 46 | 46/46 | O≤ | 6 |
| **合计** | **110** | **110/110 = 1.000**(Wilson95 [.966,1.0]) | **O≤** | **18** |

- **0 orphan**(无需第九块);子类:plain 104 / conditional 4(LOCUST MR9-12 硼阈值分段)/
  increment 2(LOCUST MR21-22 ΔKeff vs 燃耗,二阶)。
- 18 条"新发现/隐含"MR(SPARK 31-36、LOCUST 23-28、SACOS 41-46)在初始专家集之外,
  仍被专家认可且全部落入 O≤。

## 3. 诚实评估(关键)

**它辩护了什么(正面)**:
- 冻结的 **O≤ 块迁移到三个未见的生产级核电代码**,覆盖完整、0 orphan(Hypothesis 1 在
  这些代码上未被证伪)、并有 18 条超出初始专家集的有效 MR(O≤ 内的构造性发现)。
- 这是**工业级、专家验证**的迁移证据,可信度高于现有 §5 同物理 home-field 与小样本 pilot。

**它没有辩护什么(限制,必须随结论同列)**:
- **单块**:110/110 全是 O≤;G / T\* / L\* / E\* / Conservation / T_rev\* **均未被激发** → 不
  验证多块分解的**广度**,也不触及 **IBT 紧块(G, T\*)**。
- **O≤ 是非紧块**(不等式/锥,见 `fa_block_classification.py`)→ 这些 MR 证 **coverage(C4)**,
  **不**证 IBT 紧刻画。
- **同一大领域(核反应堆代码)**:代码级 held-out,**非**结构相异的非物理跨域;最强反循环
  形态(非物理域)仍待补。
- **占据为 post-hoc**(语料已见):描述性,非预注册确认(HARKing 红线)。

**数据质量旗标**(已在 `mr_corpora.md` 标注,未擅改):SACOS MR35-40 对同一 `Tm1<Tm2`
给出相反输出序(疑两分段/条件);SPARK MR23/27/25 前件重叠;Kform 源作 "Kfrom"。
不影响块归类(均 O≤),建议向作者核实。

## 4. 对 C4 的更新(草案,待落 `.tex` 确认)

C4 现可新增一条**工业迁移性**证据,**诚实限定为 O≤ 块**:

> *Industrial transferability (order block).* The frozen block decomposition was
> applied, without re-fitting, to three production nuclear codes outside the
> framework's construction set: BAMBOO-C's SPARK (core depletion) and LOCUST
> (lattice), and the SACOS sub-channel thermal-hydraulics code. Their 110
> expert-approved metamorphic relations are subsumed without exception by the order
> ($O_{\le}$) block (Wilson 95\% CI on subsumption $[0.966, 1.000]$), with no orphan
> requiring a ninth block, and 18 further valid relations beyond the initial expert
> sets fall in the same block. This is a code-level held-out confirmation that the
> order block transfers to unseen industrial codes; it exercises a single block, so
> it corroborates transferability of $O_{\le}$ rather than of the full decomposition,
> and is distinct from the symmetry / self-adjoint blocks on which the
> Invariance-Blindness Theorem is tight.

## 5. 建议

1. **落 C4(scoped)**:把 §4 草案以"O≤ 工业迁移"口径加入正文 C4/§Empirical(诚实单块限定)。
   工业 + 专家验证是真增量,值得收。**需你确认 scoping 与是否动 `.tex`。**
2. **补非物理多块 leg**:按 `protocol_N5_outofdomain.md` 首选 **数值线性代数库**(或 DSP/
   几何)跑一遍——它能激发 G / T\* / L\* / E\*,补上本 leg 缺的广度 + IBT 紧块覆盖。两条腿
   合起来才是完整 C4(单块工业 + 多块跨域)。
3. **构造性发现可加强**:若 CONSTRUCT-MP 在这些代码变量代数的 O≤ 块上能**系统生成**那 18
   条"新发现"MR,则把"专家未列、框架可导"做成显式 discovery 证据(目前只确认它们是 O≤)。

## 6. 与 N2/N4 的衔接

- 本 leg 的**专家认可**本身是**人类**判定 → 对 N2(b 已降级的 κ)是正向补强(真实领域专家、
  生产代码),虽非正式 inter-rater κ。
- N4 的 FA-rank 机制对 O≤ 不适用(非紧块);要在工业代码上展示 IBT 紧性,需补 leg 2 的
  G/T\* 类 MR(数值线代域)。
