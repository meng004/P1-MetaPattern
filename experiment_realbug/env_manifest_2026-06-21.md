# B1 执行环境分类与批量策略 (env-class manifest, 2026-06-21)

> 承接 (ii) 扩采样。落实「先对执行环境分类,再批量执行」:不同时代 bug 需不同栈,按 **env-class** 分组,组内 venv 隔离 torch/库版本,**跨解释器或跨系统依赖则分容器**(作者指示)。
> pipeline 机制(`run_one_bug.py` STEP-3 + `analyze_b1.py` STEP-4)已端到端走通(见 §3)。

## 1. 环境分类矩阵(实测)

| env-class | python | torch | 库栈 | 关键系统依赖 | 适用 bug | 当前容器可建? | 隔离方式 |
|---|---|---|---|---|---|---|---|
| **A** | 3.11 | 2.12 | 纯 torch 函数 / 新 PyG | 无 | 新 PyG util(纯 torch,无 C++ 扩展) | ✅ venv | venv |
| **B** | 3.10 | 1.13 | pyg@2022 + pyg_lib + torch_scatter/sparse | **C++ 编译链 或 prebuilt wheel** | #6199(置换等变,**标准 cat**)及 PyG-2022 scatter/聚合/HeteroLinear | ❌ torch_scatter 无 prebuilt + 无编译链 → build 失败 | **专用容器** |
| **C** | 3.9 | 1.10 | e3nn@0.3.5 + opt_einsum_fx 0.1.4 | **py3.9 解释器**(e3nn0.3.5 fx 需 torch≤1.10) | #296(表示等价,需 (iii) 新 MR)及 e3nn-2021 fx | ❌ 无 py3.9(无 conda/pyenv);torch2.5/1.11 实测 `multiple tracers` | **专用容器** |

## 2. venv vs 多容器(实现策略)

- **venv**:同一 python 解释器下隔离 torch/库版本(env-class 内,或 torch 2.x 多版本)。已用:`.venv_realbug`(A)、`venv310`、`venv_6199`。
- **多容器(必须,非可选)**:
  - env-class-C 需 **py3.9 解释器** —— venv 基于现有解释器,建不出 py3.9 → 必须 py3.9 base image 容器。
  - env-class-B 需 **系统 C++ 编译链 / torch_scatter prebuilt** —— venv 是 Python 隔离,装不上 C++ 扩展 → 必须预装编译链(或 prebuilt wheel)的容器。
- **磁盘**:当前 252G 卷、剩 23G,各 env ~0.9–1.3G,libs 42M。**单容器容量充足(未超 30G)**;分容器是为**系统依赖隔离**,不是容量。

## 3. pipeline 机制(已走通,env-class-A)

`run_one_bug.py --spec <bug_spec.py>` → `results/bug_<id>.json` → `analyze_b1.py` → RESULTS.md。
- 合成受控 scatter(SELFTEST:last-write-wins buggy vs scatter-add correct)验证:set_M `perm_equivariant+index` 在 buggy **fired**、post-fix **held**(FP-gate)、Set G `not evaluable`、Wilson CI 正确。
- 端到端机制 ✓。真实正样本待 env-class-B/C 容器。

## 4. 批量执行计划(供专用环境)

每 env-class 一个容器,容器内对该 class 的 ledger 子集批量 `run_one_bug.py` → `analyze_b1.py` 汇总:
- **env-class-A 容器**(当前可建):纯 torch util bug(注:已知这些 cat=none / MR held,信息量低)。
- **env-class-B 容器**(docker,预装 torch_scatter prebuilt for torch1.13 或编译链):#6199 等 PyG-2022 标准-cat 正样本。
- **env-class-C 容器**(docker,py3.9 base + torch1.10):#296 等 e3nn-2021 fx bug。

## 5. 候选锚点 → env-class 归属

| bug | cat | env-class | fix / parent | MR | 复现要点 |
|---|---|---|---|---|---|
| PyG #6199 | 置换等变(标准) | **B** | 25abbb15 / bc47556f | set_M / rho_train_inf | HeteroLinear(is_sorted=False) unsorted type_vec;lockstep 置换 → 输出应不变;pre-fix 顺序错 → fired |
| e3nn #296 | 表示等价(需新 MR) | **C** | b9e64db / 6fc34a9 | 需 (iii) 新「表示等价」MR | FCTP("10x0e")vs("3x0e+7x0e")权重填1 同输入;pre-fix 输出不等 |
| PyG #7407/#7412/#9766 | none | A | (Agent B 实证) | held/NA | crash/grad/dim 类,非对称破坏 → MR held |

## 6. 诚实结论

- pipeline 机制可用且已验证;**瓶颈在环境**:真 cat 命中正样本(#6199/#296)所需 env-class-B/C 在当前 CPU 容器不可建(C++ 编译链 / 旧 python),需作者起专用容器。
- 当前容器能建的 env-class-A 无正样本(能跑的 bug 均 cat=none/MR held)——与 IBT 一致(真实 bug 多在 MR 盲区)。
- 不变的诚信约束:不臆造、不把 cat=none 伪称检出、Set G 记 not-evaluable、负/欠功效如实报。
