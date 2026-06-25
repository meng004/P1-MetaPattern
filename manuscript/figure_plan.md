# 插图与表格规划 — NOETHER: Constructive Metamorphic Pattern Identification from Operator Algebras

> 源文件：`manuscript/NOETHER_paper_arxiv.tex`（+ `theory/ibt_section_3_4.tex`，经 `\input` 并入）
> 评估日期：2026-06-24 · 目标期刊：TOSEM（acmart 单栏）
> 本文件仅为**评估规划**，未生成任何图、未改动正文。经作者确认取舍后再进入生成阶段。

---

## 一、现有插图盘点

| 编号 | 当前位置 | 类型 | 工具 | 评估 |
|------|---------|------|------|------|
| `fig:noether-arch` | §1 Intro, L184 | 两层工作流架构图 | (已有 tikz) | **保留**。upstream/downstream 两层 + Thm1/Thm2 + 三域实例化，承载全文骨架，必要。 |
| `fig:blocks` | §3.2.9 分解, L481 | 结构分解示意（5 MetaPattern + 2 精化 + 1 关系扩展，8 格） | (已有 tikz) | **保留**。但建议核对图内措辞与现行"two-layer / 五 MetaPattern"命名一致（caption 已用新词，图内仍是结构分量罗列，OK）。 |
| `fig:ibt` | §3.4 IBT（theory 文件）, L106 | 概念图：检测核 = 保结构故障 + 互补差分预言机 | (已有 tikz) | **保留**。IBT 是全文 load-bearing 理论结果，概念图已到位，**不重复造图**。 |

> 现状：3 张图全部是概念/示意图，**全文无一张数据图**；所有实证结果（case study、L\*-盲性、head-to-head、real-bug）都只以表格呈现。对一篇约 50 页、含多组可量化实证的方法论文，这是图配置的主要缺口。

### TOSEM 投稿目录里的旧图（`submission/TOSEM_2026-05-20/.../figures/`）

| 旧文件 | 状态 | 处置建议 |
|--------|------|---------|
| `fig_2_eight-block-decomposition.mmd` | 与 `fig:blocks` 重复，且用旧"八块/B1–B8"命名 | **弃用**（已有 tikz 版） |
| `fig_3_construct-mp.mmd` | 当前主稿**没有**对应图；命名旧（block/八块） | **可复用**，但须改写为"五 MetaPattern / structural component"命名 → 见 Fig N1 |
| `fig_4_l-blindness.py` | 当前主稿**没有**对应图；数据取自论文自有表 | **可复用**，须核对数字与现行 `tab:l-blindness` 一致 → 见 Fig N3 |

> ⚠️ 命名一致性硬约束（配合 §4 反自发改写 + 近期 two-layer 命名统一 commit）：任何复用旧图都必须把 "block / eight-block / B1–B8" 全部改为现行 "structural component / MetaPattern"，否则图与正文术语冲突。

---

## 二、建议新增插图清单

> 排序按必要性。**Tier A（推荐先做）= Fig N1、N3**；其余按作者取舍。

### Fig N1 — CONSTRUCT-MP 四步推导流水线
- 位置：§3.3.2 "Construction of the MetaPattern set"，Step 1–4 描述列表之后（L649 之后）
- 类型：流程图 → **Mermaid**
- 必要性：**高** — 四步机械推导（不变量提取 → Translate → 商 → 聚合）是方法的核心引擎，目前仅有一个 bullet 描述列表 + 架构图里一根箭头；一张 input(分解)→4 步→output(MetaPattern 集，Translate-闭合) 的流程图让"可证明的下游"一眼可见。
- 内容要点：输入 `D(A_P)`（五 MetaPattern + 两精化 + 关系扩展）→ (a) 不变量提取 `I_s` → (b) MR 派生 via `Translate` → (c) 按 `~_s` 取商成 MetaPattern → (d) 聚合 → 输出 `M(A_P)`，标注 Theorem 1（闭合）/ Theorem 2（多项式时间）落点
- 数据来源：无（结构图，非数据图）
- caption 草稿：*CONSTRUCT-MP: from the structural decomposition $\mathcal{D}(\mathcal{A}_P)$, four mechanical steps (invariant extraction, MR derivation via \texttt{Translate}, quotient under $\sim_s$, aggregation) produce the MetaPattern set $\mathbb{M}(\mathcal{A}_P)$, closed under \texttt{Translate} (Theorem~\ref{thm:closure}) and polynomial-time constructible under a finite generating set (Theorem~\ref{thm:decidable}).*
- 拟生成：`fig_N1_construct-mp.{pdf,png}`（可在旧 `fig_3_construct-mp.mmd` 基础上改命名）

### Fig N3 — L\*-MetaPattern 盲性：逐 SUT kill 率 vs 1/3 证伪阈值
- 位置：§4 "Central result: $\mathcal{L}^{*}$-MetaPattern blindness, confirmed"（subsec:l-blindness-confirmed, L1677），`tab:l-blindness` 之后
- 类型：柱状图（含参照线）→ **seaborn / matplotlib**
- 必要性：**高** — 本节自述为"the central content of this section"，是全文唯一**可证伪的定量预测**。柱状图 + 阈值线让"6 个 SUT 中 5 个零 kill、hypotSig 唯一离群 2/4、pooled 2/44≈4.5%"瞬间可读，远胜逐行读表。
- 内容要点：x = 6 个 L\*-admitting SUT（midpoint/clamp/signum/gcdSig/lcmSig/hypotSig），y = `L_scale` kill 率；虚线标 1/3 证伪阈值；柱顶标原始分数 k/n
- 数据来源：**论文自有表 `tab:l-blindness`** — midpoint 0/3, clamp 0/7, signum 0/6, gcdSig 0/9, lcmSig 0/11, hypotSig 2/4；pooled 2/44。（生成前以现行表逐一核对，不引入任何额外点）
- caption 草稿：*Per-SUT $L_{\mathrm{scale}}$ kill rate on PIT mutants of the six $\mathcal{L}^{*}$-admitting SUTs. Five of six register zero kills; \texttt{hypotSig} ($2/4$) is the sole homogeneity-breaking outlier. Pooled $2/44\approx4.5\%$, an order of magnitude below Set~N's $0.486$ average. Counts from Table~\ref{tab:l-blindness}.*
- 拟生成：`fig_N3_l-blindness.{pdf,png}`（可复用旧 `fig_4_l-blindness.py`，核对数字）

### Fig N2 — 两层模型：5 MetaPattern (L1) → 10 MR 族 (L2) 映射
- 位置：§3.2.10 "The two-layer model"（subsec:generator-family, L566），`tab:mr-families`（L575）之前或之后
- 类型：二部/树状映射图 → **Mermaid**（或 draw.io 求精细对齐）
- 必要性：**中–高** —"two-layer model"是被命名的概念贡献；L1→L2 是**一对多**且依赖 `A_P`（如 G→equivariance+conservation；T\*→self-adjoint+adjoint-duality；O≤→static-order+dynamic-shape(D\*)；L\*→convergence+accuracy-order(E\*)+representation-invariance）。这种分叉结构 `tab:mr-families` 的 4 列表读不出来；映射图能呈现表没展示的"父→子分叉 + 精化/扩展归属"维度。风险：与 Table 1 部分重叠 → 若作者认为表已够，可降级。
- 内容要点：左列 5 个 MetaPattern（`m_inv,m_mono,m_adj,m_rev,m_conv`），右列 10 个 MR 族（按 `tab:mr-families` 的 a–j），连线标 mode (I/M)；用样式区分两个精化（D\*→g、E\*→i）与关系扩展（B\*rel）
- 数据来源：无（结构映射，取自 `tab:mr-families` + §3.2.10 正文）
- caption 草稿：*The two-layer model: the five MetaPatterns (L1) and the ten executable MR families (L2) they instantiate. The map is one-to-many and program-family dependent; refinements ($\mathcal{D}^{*},\mathcal{E}^{*}$) and the relational extension ($\mathcal{B}^{*}_{\mathrm{rel}}$) enter at L2. Modes I/M per Definition~\ref{def:mr-mode}.*
- 拟生成：`fig_N2_two-layer-map.{pdf,png}`

### Fig N4 — 逐 MetaPattern head-to-head：Set N vs Set G（含 Wilson CI）
- 位置：§4 head-to-head（subsec:pooled-headtohead），`tab:per-block-headtohead` 之后
- 类型：分组柱状图（含误差棒）→ **seaborn / matplotlib**
- 必要性：**中** — 把"mixed verdict / 互补性"一眼呈现：Set N 在 `G_tr` 反超（10/17 vs 8/17）、Set G 在 `G`、`L*` 占优。正文为这点写了很长一段。但该证据被论文自身定位为 secondary，且 CI 重叠（欠功效），图不能过度强调 → 评中。
- 内容要点：x = 三个 operative MetaPattern（G / L\* / G_tr），每组两柱（Set N、Set G），y = kill 率 + Wilson 95% CI 误差棒
- 数据来源：**论文自有表 `tab:per-block-headtohead`** — G: 0.182[0.051,0.477] vs 0.818[0.523,0.949]；L\*: 0.417[0.245,0.612] vs 0.667[0.467,0.820]；G_tr: 0.588[0.360,0.784] vs 0.471[0.262,0.690]
- caption 草稿：*Per-MetaPattern kill rate, Set~N (algebra-derived) vs Set~G (GP-evolved), with Wilson 95\% CIs, on the PIT-covered substrate. Set~N edges Set~G on the $G_{\mathrm{tr}}$ translation sub-class; Set~G dominates on $G$ and $\mathcal{L}^{*}$. Intervals overlap ($n$ per MetaPattern underpowered); read as complementarity, not superiority. Data: Table~\ref{tab:per-block-headtohead}.*
- 拟生成：`fig_N4_per-metapattern-h2h.{pdf,png}`

### （备选，低）Fig N5 — equivariant-ML case study 逐类检出
- 位置：§4 case study，`tab:case-study` 之后
- 类型：分组柱状图 → seaborn
- 必要性：**低** — 论文明确把 case study 降级为"secondary executability check, construct-validity-controlled"。配图会放大一个被刻意压低的结果，与论文诚实性框架（§6.8/C4）相悖。**默认不做**，仅在作者特别想可视化 cat-(iv) 的 5/5 unique detection 时考虑。

---

## 三、建议新增表格清单

> 现有 16 张表已偏多；新增只在"净读者收益为正"（把密集散文转成可查矩阵 / 暴露表未展示维度）时才提。

### Tab N1 — Real-bug 实证：MR 族 × 域 覆盖矩阵
- 位置：§4 "Real-bug evaluation"（para:real-bug-protocol, L1437–1445），替换/伴随当前约 250 词的 "Coverage" 密集散文段
- 必要性：**高** — 这是 EQ3 在真实缺陷层面的 load-bearing 证据（21 个 in-the-wild 缺陷，8/10 个 MR 族 × 4 个库，外加 2 个 structure-present 正例 diffrax/Clawpack 与 5 个 evidenced-negative）。目前正文是一整段难以检索的散文，完整矩阵只在 supplementary S5。一张主文矩阵表是全篇**最大的可读性收益**。
- 结构：行 = 10 MR 族（a–j）；列 = 4 SUT 域（SciPy / PySCF / OpenMC / DeepXDE）+ 2 结构探针库（diffrax→e、Clawpack→g）；单元格 = 命中（计数或 ✓），标注 2 个 caveated 正例（SciPy `fht` 数值边缘、DeepXDE Hessian 非默认路径）与 5 个 evidenced-negative
- 数据来源：正文 L1441–1445 散文（族×域 presence 可直接抽出）+ **supplementary S5 `real_bugs/`**（精确每格计数 / SHA，生成前以 S5 核对）
- caption 草稿：*In-the-wild fault coverage by MR family and SUT domain (21 in-scope faults, four libraries), with the two structure-present positives (diffrax / Clawpack) and the five evidenced negatives. Per-fault SHAs, versions, and FIRED/HELD numbers in supplementary~S5.*

### Tab N2 — 框架边界：out-of-scope 程序族 → 候选附加 MetaPattern
- 位置：§3.2.9，Remark `rem:counterex`（L535）与 `rem:domain-out-of-scope`（L549）处，将两个 enumerate 列表并为一表
- 必要性：**中** — 把"6 个候选附加 MetaPattern 族 + 4 类完全 out-of-scope 域"的边界变成可一眼审计的表，强化论文诚实性叙事（明确写出 framework 不覆盖什么 + 经验见证）。
- 结构：列 = 程序族 / 缺失的代数结构 / 候选附加 MetaPattern / 经验见证（如 cat-v-02/04/05、metric-stability orphan）/ 类别（candidate-MP vs domain-out-of-scope）
- 数据来源：`rem:counterex`（symplectic / sheaf / martingale / topological / label-consistency / parameter-distribution）+ `rem:domain-out-of-scope`（web app / RLHF / consensus / compiler-internal）+ `rem:metric-stability-block`
- caption 草稿：*Documented out-of-scope program-family classes. Candidate-additional-MetaPattern families (top) signal in-programme extensions; domain-out-of-scope classes (bottom) lack any operator-algebraic representation. Each row names the missing structure and, where available, the empirical witness.*

### （备选，低）Tab N3 — 三域实例化汇总
- 一行一个被实例化的代数（Boltz / equi / rel / PWR-负例），列 = 非空结构分量、`|M|`、代表 MR、角色（positive/negative）。
- 必要性：**低–中** — 与 `tab:cross-domain-trace`（EQ3，按分量组织）较多重叠，**默认不做**。

---

## 四、合理性评估

- **数量**：现有 3 图 + 16 表。建议新增图：Tier A 2 张（N1、N3）必要性高；N2、N4 中；N5 不建议。建议新增表：N1 高、N2 中、N3 不建议。
  - 推荐落地组合：**+Fig N1、Fig N3、Tab N1**（3 项，全部高必要性）；Fig N2 / Fig N4 / Tab N2 由作者按版面与侧重取舍。
  - 若全采纳高+中项：终态 ≈ 6 图 + 18 表。6 图对 50 页 TOSEM 方法论文合理；**18 表偏多**——建议把新增表的代价用"替换散文/合并"对冲（Tab N1 替换 L1441 散文段即为净减负）。
- **期刊惯例**：TOSEM 方法论文常见 4–8 图；当前 3 图偏少，补 2–3 张（尤其至少 1 张数据图）更符合惯例。表无硬上限，但 16→18 已属高位，慎增。
- **图表重复检查**：
  - `fig:ibt` 已存在 → IBT 概念图**不再新造**。
  - Fig N2 与 `tab:mr-families` 有部分重叠（同一 L1→L2 信息）→ 图呈现"分叉拓扑"，表呈现"逐族不变量"，维度不同，可共存；若版面紧张优先保表。
  - Fig N3 / Fig N4 与各自来源表（`tab:l-blindness` / `tab:per-block-headtohead`）信息同源 → 图的增值是"核心发现一眼可见 + 阈值线/CI 可视"，符合"图必须挣得其位置"判据。
  - Tab N1 与 supplementary S5 矩阵同源 → 主文需要一个摘要矩阵，S5 留全量，不算冗余。
- **删减 / 合并建议**：弃用 TOSEM 目录旧 `fig_2_eight-block`（与 `fig:blocks` 重复）。
- **命名一致性（务必）**：所有复用旧资产（fig_3、fig_4）须把 "block / 八块 / B1–B8" 改为 "structural component / MetaPattern"，与现行两层命名对齐。

---

## 五、待作者拍板的问题

1. **核心组合是否采纳**：Fig N1（CONSTRUCT-MP）、Fig N3（L\*-盲性数据图）、Tab N1（real-bug 矩阵）三项是否全做？
2. **中等项取舍**：Fig N2（两层映射）、Fig N4（逐 MetaPattern head-to-head）、Tab N2（out-of-scope 边界表）各做哪些？
3. **Tab N1 数据**：是否提供 supplementary S5 `real_bugs/` 的精确每格计数？（否则我按正文 presence 做"命中/缺席 + 2 正例 + 5 负例"的标记型矩阵，不编造计数。）
4. **目标格式**：TOSEM 矢量 PDF 优先（我默认同时产出 PDF + 300dpi PNG）。

> 确认后我再进入生成阶段（建 `figures/src/`，逐图渲染矢量 PDF + 300dpi PNG，并给可粘贴的 `figure` 环境片段；**不直接改正文**）。
