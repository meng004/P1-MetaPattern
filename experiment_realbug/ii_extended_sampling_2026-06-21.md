# B1 — Option (ii) 扩采样 + per-bug 复现探索 (2026-06-21)

> 承接 `candidate_audit_2026-06-21.md`。用户选 (ii)「扩采样凑正样本」。本文记录:关键词回溯扩采样的真 cat 命中、per-bug 复现的实测瓶颈、可供有专用环境时执行的候选锚点。
> 诚实定位:扩采样**可行**;per-bug 复现是 (ii) 的真实成本中心,受当前容器(py3.10/3.11、无 conda/pyenv/docker)硬限制。本会话未凑出可跑 ledger,但确证了路径与边界,并锚定了 2 个真候选。

## 1. 扩采样(GitHub search API,关键词回溯,label:bug + closed)

机械「最近 closed-bug」窗口 0 命中(见 candidate_audit §1-C)。改用关键词回溯搜:
- e3nn:`equivariance / wigner / irreps / rotation`
- PyG:`scatter / permutation / aggregation / segment`

**真 cat 命中候选(2 条;其余命中仍为 JIT/device/dataset 类 none → 印证 cat 命中稀少,IBT)**:

| bug | 缺陷 | cat | 是否标准 cat | fix / parent | MR |
|---|---|---|---|---|---|
| **PyG #6199** | HeteroLinear `is_sorted=False`:内部按 type 排序后**未还原原顺序**,输出被打乱 | 置换等变性破坏 | **是**(set_M / rho_train_inf 置换-顺序不变性可测) | `25abbb15` / `bc47556f`(PR #6198) | set_M / rho_train_inf |
| **e3nn #296** | 等价 irreps 写法(`10x0e` vs `3x0e+7x0e`)在 FullyConnectedTensorProduct 给不同输出(归一化系数 bug) | 表示等价不变性 | **否**(非 cat-i~iv 标准型) | `b9e64db` / `6fc34a9`(PR #301) | **需新 MR(选项 iii)** |

## 2. per-bug 复现实测(核心瓶颈)

每个历史 bug 需**时代匹配栈**;当前容器实测:

- **e3nn #296 — CPU-INFEASIBLE in this container(确证)**：e3nn 0.3.5@6fc34a9 的 `torch.fx` codegen 需 torch ≤ 1.10 + python ≤ 3.9。
  - torch 2.5(避开 2.6+ weights_only):import OK,但 codegen 抛 `RuntimeError: Found multiple different tracers`。
  - torch 1.11(py3.10,最低支持 py3.10 的版本):同样 `multiple tracers`。
  - 容器无 conda/pyenv、无 python3.9（仅 3.10/3.11），无法装 torch ≤ 1.10 → 复现不可达。
- **PyG #6199 — 需 pyg_lib(C++ 扩展)**：官方 fix test `test_hetero_linear_sort` 标注 `@withPackage('pyg_lib')`，bug 路径走 `pyg_lib.ops.segment_matmul`。复现需 pyg_lib CPU wheel + pre-fix PyG@bc47556f(2022)+ 时代 torch，又是时代栈兼容工程。

## 3. (ii) 可行性边界(诚实结论)

- **扩采样**:✅ 可行。真 cat 命中存在但稀少（关键词回溯在两库各仅得 1 条），与 IBT 一致。
- **per-bug 复现**:⚠️ 当前容器不足。历史 bug 普遍需 per-bug 时代环境（旧 python / C++ 扩展 / 时代 torch），当前 CPU 容器（py3.10/3.11、无 conda/docker）无法批量重建。
- **完整 (ii) 成本**:专用 per-bug 环境基础设施（conda 或 docker，每 bug 一套时代栈）+ 数天；且部分命中（#296）还需 (iii) 新 MR 才能被 mr_sets 评测。

## 4. 候选锚点(供有专用环境时直接执行)

```
# PyG #6199 (标准 cat: 置换等变；现有 MR set_M/rho_train_inf 可测)
repo=pyg-team/pytorch_geometric  fix=25abbb15  parent=bc47556f  PR=6198
env: python3.10 + torch(2022-era, e.g. 1.13) + pyg@bc47556f + pyg_lib(CPU)
repro: HeteroLinear(is_sorted=False) on unsorted type_vec; pre-fix 输出顺序错, post-fix 还原
MR: 置换输入 -> 输出应对应置换; pre-fix 违反 => fired

# e3nn #296 (需新 MR: 表示等价不变性)
repo=e3nn/e3nn  fix=b9e64db  parent=6fc34a9  PR=301
env: python3.9 + torch1.10 + e3nn@6fc34a9 (+ opt_einsum_fx 0.1.4)
repro: FCTP("10x0e","10x0e","0e") vs ("3x0e+7x0e",...) 权重填1 同输入; pre-fix 输出不等 => fired
```

## 5. 建议

(ii) 单靠当前容器无法完成完整 confirmatory。三条非互斥路径:
- **(i) IBT 实证**:把「机械全量 + 关键词回溯下真 cat 命中稀少、且多数真 bug 在 MR 盲区」作为 Invariance-Blindness 的实证写入论文（本会话证据已足够支撑）。
- **(ii-cont) 专用环境复现**:在能起 conda/docker per-bug 时代栈的主机上，按 §4 锚点复现 #6199（标准 cat，最高优先）。
- **(iii) 新 MR**:为 #296 类「表示等价不变性」定义可执行 Set N MR（作者方法决策）。

> 复现保真度与诚信硬约束不变：不臆造 bug、不把 cat=none 伪称检出、Set G 记 not-evaluable、负/欠功效如实报。
