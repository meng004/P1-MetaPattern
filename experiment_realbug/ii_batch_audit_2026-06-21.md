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
| pyg | #6110 | cat-ii maybe | 未复现(需 Data/ogbg-molhiv 装置) | maybe,待复现 |
| pyg | #6299 | cat-ii maybe | 未复现(需 HeteroData 装置) | maybe,待复现 |
| pyg | #6251 | cat-iv maybe | 未复现;Agent 标陷阱(fix 是 raise ValueError,非数值修复) | maybe,oracle 不可 diff |
| pyg | #4826 | cat-v maybe | 未复现(NaN 边界,弱) | maybe,待复现 |
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
