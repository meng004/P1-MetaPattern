# mr_sets/ — 可执行 MR 定义（B1 真 bug 评测）

> ⚠️ **这是 B1 的最大 binding 缺口**(见 `../README.md` 开放设计问题)。本目录目前只含**接口契约 + ρ_rot 起步**;Set N 其余 MR + 基线 M/G/L/B 需作者实现/判定适用性后才能投跑。

## 接口契约（每条 MR 必须实现）

```python
def mr_<name>(fn, ctx, tol) -> dict:
    """
    fn  : the (buggy pre-fix or fixed post-fix) library callable under test.
    ctx : dict with the bug's tiny CPU inputs + any metadata the snippet provides
          (e.g. irreps, a base point cloud, an index tensor). Built by the bug's
          repro_snippet, NOT by this MR.
    tol : numerical tolerance taken from the bug's fixture / issue.
    Returns:
      {"status": "fired" | "held" | "not_applicable", "detail": "<short>"}
    Semantics:
      fired          : the metamorphic relation is VIOLATED -> the MR surfaced the bug.
      held           : the relation holds within tol -> MR did not surface this bug.
      not_applicable : this MR has no meaning for this fn/bug (e.g. a training-time MR
                       on a pure tensor op). MUST be distinct from 'held' so the
                       analysis excludes it from that set's denominator on this bug,
                       rather than miscounting 'no definition' as 'missed'.
    """
```

`bug_<id>.json` records, per set, whether ANY of its applicable MRs `fired`. A set's
detection on a bug = (≥1 MR `fired`). A set is `not_applicable` on a bug iff ALL its
MRs return `not_applicable` (then that bug is dropped from THAT set's denominator).

## 五个集合（待实现状态）

| Set | 论文来源 | 对库级缺陷的适用性 | 状态 |
|---|---|---|---|
| **N** (NOETHER) | ρ_rot, ρ_adj, ρ_train-rev, ρ_mono, ρ_train | ρ_rot 直接适用(旋转不变);ρ_adj 部分(自伴/互易层);**ρ_train-rev / ρ_mono / ρ_train 多为训练/推理级,对纯库函数缺陷多为 not_applicable** | ρ_rot 起步✅;余待作者 |
| **M** (METRIC+) | §metricplus 类别 | 需对 e3nn/PyG 缺陷重实例化 | 待作者 |
| **G** (GenMorph) | GP-evolved MRs | 需重实例化 | 待作者 |
| **L** (LLM-prompt) | GPT-4 生成 5 条 | 需重实例化 | 待作者 |
| **B** (literature) | MT-for-ML 文献 5 条 | 需重实例化 | 待作者 |

## 诚信约束（同 prereg §3.3）

- **不得为某 bug 新写"恰好能检出它"的 MR**——MR 集是论文既有目录的库级移植,缺陷是外部的。
- 对训练/推理级 MR 在库函数缺陷上,如实返回 `not_applicable`,**不得**强行套用使其偶然 fired。
- 若某 Set 在多数 bug 上全 not_applicable,如实报告其 denominator 缩小(欠功效),不掩盖。

---

## 实测 applicability（workflow we8ipq0ti，已落地 *.py）

完整 manifest 见 [`APPLICABILITY_MANIFEST.md`](APPLICABILITY_MANIFEST.md)。摘要:

| MR/Set | 最终适用性 | 文件 |
|---|---|---|
| rho_rot (N/G) | **portable** | rho_rot.py |
| rho_adj (N/T\*) | adaptable ✅fixed | rho_adj.py(默认 contract 改 trace,转置不变;验证:转置对称→held/破坏→fired/非矩阵→N/A) |
| rho_train_rev (N/𝒯\*rev) | **not_applicable**(SGD 轨迹) | rho_train_rev.py(stub) |
| rho_mono (N/O_le) | adaptable | rho_mono.py |
| rho_train_inf (N/L\*) | adaptable | rho_train_inf.py |
| Set L (LLM) | adaptable | set_L_llm.py |
| Set B (literature) | adaptable | set_B_lit.py |
| Set G (GenMorph) | **not_applicable / not evaluable** | set_G_genmorph.py(stub) |
| Set M (METRIC+) | adaptable ✅fixed | set_M_metric.py(死分支已修:perm_equivariant+index 跑 invariant 检查;验证:buggy scatter→fired) |

**Set N 4/5 适用(最强腿)**;G 不可评(报 not-evaluable 非 0);分母按 per-set applicable 计,非 catalogue 原始大小。两处 fix_needed(rho_adj/set_M)**已于 2026-06-21 修复并功能验证**。投跑前作者剩余:per-bug 写 ctx adapter(x/rotate/equivariant_out/metric_props/index 等),把每条 bug 的复现 snippet 接到对应 MR。
