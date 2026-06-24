# B1 cat-ii 批量执行审计 (2026-06-21)

本轮在三个 env-class 全部建成后执行批量。记录检索代理候选 + 逐个复现状态 + 诚实 IBT 结论。

## 复现环境(全部当前单容器内建成,无 docker/多环境)

| env-class | 栈 | 状态 |
|---|---|---|
| A | py3.11 + torch2.12 | ✓ 主 venv |
| B | py3.10 + torch1.13 + pyg2.2 + torch_scatter/sparse(C++)+ pyg_lib | ✓ /tmp/venv_6199 |
| C | py3.9 + torch1.10 + e3nn0.3.5(uv) | ✓ /tmp/venv_c |

## 检索代理候选(general-purpose agent,WebFetch GitHub,SHA 经真实核验)

| repo | issue# | Agent cat | 复现状态 | 最终归类 |
|---|---|---|---|---|
| pyg | #6199 | cat-ii | ✓ 完整走通(N rho_perm + M fired, FP-gate pass) | **in-scope 正样本** |
| pyg | #6037 | cat-iii | ✓ 复现:行和≠0 但 L=Lᵀ 对称完好 | **out-of-decomposition**(Agent 误判已纠正) |
| pyg | #6241 | cat-ii maybe | ✗ GDC PPR 复现 AssertionError(无确切 snippet) | BLOCKED(待确切 repro) |
| pyg | #6110 | cat-ii maybe | ✗ 复现失败(pyg2.2 Data 无 index_select 方法,API 与版本不符) | BLOCKED |
| pyg | #6299 | cat-ii maybe | ✗ fix SHA 内容是 to_heterogeneous 空边 test,与 Agent 描述(to_homogeneous ptr)不符 | BLOCKED(SHA 内容不符) |
| pyg | #6251 | cat-iv maybe | 未复现;Agent 标陷阱(fix 是 raise ValueError,非数值修复) | maybe,oracle 不可 diff |
| pyg | #4826 | cat-v maybe | fix SHA 准(HANConv 空 tensor NaN guard,`numel()==0` early-return);性质=边界 NaN 非不变性;复现需 parent worktree(3d76627)未执行 | out-of-decomposition(by fix-code nature) |
| e3nn | #258 | cat-i/v maybe | 未复现(梯度 NaN,非纯前向不变性) | maybe,待复现 |
| e3nn | #296 | out | 复现确认(表示等价 ∉ 元模式) | **out-of-decomposition** |
| pyg #5921 / #5409, e3nn #316 / #266 | — | out/BLOCKED | Agent 标 negative(crash/export/device/API) | out |

## 批量 IBT 结论(n=2 已执行,underpowered C6)

**detection(in-scope,denominator=applicable bugs)**:N 1/1、M 1/1、B 0/1、G not-evaluable。
**coverage_NOETHER**:1/2 = 0.500(仅 #6199 in-scope;#6037 out)。
**out-of-decomposition 已确认**:#6037(行和守恒)、#296(表示等价)= 2 个真实 bug 落在 NOETHER 5 元模式外。
**FP-gate**:post-fix 全 held,无误报。

### 核心诚实发现(IBT)

1. **in-scope detection 高,coverage 有限**:NOETHER 元模式在其覆盖范围内检出可靠(#6199 N+M fired),但真实 bug 频繁落在分解之外(#6037 行和守恒、#296 表示等价)。
2. **Agent cat 判定需逐个复现核实**:#6037 被标 cat-iii(self-adjoint),实测破坏的是行和守恒而非对称(L=Lᵀ 完好)→ 实为 out。**不可凭检索标签计数,必须复现验证**。
3. **无确切 snippet 的候选复现易失败**:#6241 GDC PPR 复现 AssertionError。可靠正样本需 issue 内最小 snippet 或 fix 回归测试。
4. **样本量**:n=2 OK bugs,远低于 α=0.05 推断所需;本轮为 descriptive pilot,非 confirmatory。

## 未尽事项(继续批量需逐个工程)

- #6110/#6299/#4826/e3nn#258:逐个构造复现装置(每个 PyG/e3nn 数据结构 + ctx adapter),工程量大且部分弱(maybe)。
- #6241:需从 issue 原文取确切 GDC 参数 + 图,重试复现。
- #6251:fix 语义是 raise,oracle 需人工预期,不能 diff pre/post——做 MT 需特殊处理。
- 扩大 n 至 ≥10 in-scope 正样本:需更大检索池 + 逐个复现,跨多 env-class。

## fix-test 反推结果 + 检索代理候选可靠性(关键 meta-发现)

采用"从 fix PR 取确切复现"策略后,逐个核验 Agent 候选的 fix SHA:

| 候选 | Agent fix SHA 是否对应所述 bug | 结论 |
|---|---|---|
| #6037 | ✓ SHA 准,但 **cat 误判**(标 cat-iii,实为行和守恒 out) | 复现后纠正 |
| #4826 | ✓ SHA 准(HANConv 空 NaN guard) | 性质 out |
| #6299 | ✗ SHA 内容是 to_heterogeneous 空边,与所述 to_homogeneous ptr **不符** | BLOCKED |
| #6110 | ✗ 所述 API(Data.index_select)在 pyg2.2 不存在 | BLOCKED |
| #6241 | ✗ 无确切 snippet,GDC 参数复现 AssertionError | BLOCKED |

**检索代理候选可靠性约 2/5 SHA 准、且 SHA 准的也可能 cat 误判**。结论:自动检索的候选**不可直接用于批量计数**,每条必须复现 + 核验 fix 内容 + 核验 cat。可靠 in-scope 正样本(#6199)来自作者手工核验链(#6198/#6199 HeteroLinear),非自动代理。

## 批量最终诚实结论(本轮)

- **in-scope 正样本**:#6199(1 个,完整走通,N rho_perm + M fired,FP-gate pass)。
- **out-of-decomposition 确认**:#6037(行和守恒)、#296(表示等价)、#4826(空输入 NaN,by fix-code nature)= 3 个。
- **BLOCKED(代理数据不准)**:#6110、#6241、#6299 = 3 个。
- **detection(in-scope)**:N 1/1、M 1/1、B 0/1;**coverage 极有限**(1 in-scope vs 3 out)。
- **核心 IBT 发现**:NOETHER 元模式 in-scope 检出可靠,但真实 bug 中 in-scope 比例低(多为行和守恒/表示等价/空输入边界等元模式外类别);且自动检索候选需逐个复现核验,不可凭标签计数。
- **样本量**:n=2 OK(underpowered C6),descriptive pilot,非 confirmatory。
