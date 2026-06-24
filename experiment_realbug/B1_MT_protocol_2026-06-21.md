# B1 真 bug 蜕变测试(MT)标准流程 — 5 步协议 (2026-06-21)

> 作者定义的 5 步流程,映射到本仓库已有工具 + 产物 + 执行环境(env-class)+ 诚信约束。
> **核心合规点(步骤 3)**:MR 是**根据 NOETHER 元模式 *识别***,**不是为 bug 创造**(prereg §3.3 红线)。映射不到任一元模式的 bug → 归 out-of-decomposition,MR 如实记 `held/not_applicable`,**不造 MR**。

## 步骤 1 — 检索真 bug

- 工具:`harvest_bug_candidates.py`(机械列最近 closed-bug,防 cherry-pick)+ GitHub search API 关键词回溯(`equivariance/wigner/scatter/permutation/...`)。
- 选择规则(prereg §3.4,冻结):closed + label:bug + linked merged fix + 复现 snippet,满足 CPU 可复现的最近 N 条(cat-(i)–(iv) 各 ≥1,余 recency)。
- 产物:候选清单 → 核验后落 `bug_ledger.csv`(repo, issue_url, fix_commit, pre_fix_parent_commit, cat, cpu_repro_snippet_path)。**每条须有 fix/parent 锚点,否则 BLOCKED 排除;不臆造。**

## 步骤 2 — 研判 bug 违反哪一类 MR(不变性)

- 判定该缺陷破坏哪类**不变性**:旋转/置换等变(对称)、自伴/转置、幂等/单调冗余、推理确定性/纯度、表示等价(out-of-decomp)、或**无对称破坏**(crash/类型/编译/device/梯度/数据 → none)。
- 工具:逐 issue 核对(本地 git diff + WebFetch),参照 `APPLICABILITY_MANIFEST.md` 的 cat 定义。
- 产物:每条 bug 的 `cat` + 违反的不变性类别(忠实,拿不准标 maybe)。

## 步骤 3 — 根据元模式识别 MR(**识别,不创造**)

- 从 NOETHER 对 `A_equi` 导出的 **5 个元模式**(论文 L810:`m^eq_inv`=rho_rot / `m^eq_mono`=rho_mono / `m^eq_adj`=rho_adj / `m^eq_rev`=rho_train_rev / `m^eq_conv`=rho_train_inf)+ 基线集 M/G/L/B 中,**识别**与步骤 2 不变性匹配的 MR。
- 实现:`mr_sets/*.py` 的每个 MR 依 ctx 自判 `applicable / not_applicable`(applicability 编码于 `APPLICABILITY_MANIFEST.md`)。
- **红线**:若 bug 违反的不变性**不对应任何元模式**(如 #296 表示等价 ∉ 5 元模式)→ 该 bug 是 **out-of-decomposition**,所有 MR `not_applicable/held`,**绝不为它新写 MR**(否则 fabricated MR,confirmatory 作废)。
- 产物:per-bug 的 ctx adapter(把复现接到识别出的 MR;manifest §4 的 x/index/metric_props/rotate)。

## 步骤 4 — 执行 MT,记录测试结果

- 工具:`run_one_bug.py`(STEP-3 driver):per-bug checkout pre-fix(buggy)+ post-fix(fixed)→ 跑识别出的 MR → `fired_pre`(检出)+ `fired_post`(FP-gate,正确 MR 不应在 fixed 上 fire)→ `results/bug_<id>.json`。
- **执行环境(env-class,见 `env_manifest_2026-06-21.md`)**:
  - env-class-A(py3.11+torch2.12):纯 torch 函数 bug(当前容器✅)。
  - env-class-B(py3.10+torch1.13+pyg2022+torch_scatter+pyg_lib):PyG-2022 标准-cat 正样本(如 #6199);需**专用容器**(`envs/Dockerfile.envB`)。
  - env-class-C(py3.9+torch1.10+e3nn0.3.5):e3nn-2021 fx bug;需**专用容器**(`envs/Dockerfile.envC`)。
- 诚信:不臆造;CPU-INFEASIBLE/BLOCKED 如实记并排除;Set G 记 `not-evaluable`(非 0)。

## 步骤 5 — 统计并分析数据

- 工具:`analyze_b1.py`(STEP-4):per-set 检出率 + **Wilson 95% CI**;Set N vs {M,L,B} 的 **exact McNemar**(paired by bug);`b+c<25` → underpowered;**Holm–Bonferroni**;**H4 非劣 Δ=0.10**;Set G not-evaluable;coverage_NOETHER。
- 产物:`RESULTS.md`。
- 诚信:负/非显著/欠功效结果显著报告;非劣框架,**无优越性主张**;out-of-decomposition 计数单列。

## 批量执行(env-class 分容器)

```
# 每个 env-class 一个容器(venv 隔离同解释器包;跨解释器/系统依赖必须分容器)
docker build -f envs/Dockerfile.envB -t b1-envB .   # PyG-2022 + torch_scatter(C++)
docker run --rm -v $PWD/out:/work/out b1-envB bash envs/batch_run.sh B   # 跑 env-class-B ledger 子集
# 容器内 batch_run.sh: clone P1 分支 + per-bug worktree → run_one_bug.py 批量 → analyze_b1.py 汇总
```

## 不变的诚信硬约束(贯穿 5 步)

1. 步骤1:不臆造 bug;机械选择防 cherry-pick。
2. 步骤3:**识别**元模式 MR,**不创造**;out-of-decomposition 如实记 held,不造 MR。
3. 步骤4:Set G not-evaluable;复现保真度(时代栈)不足则 CPU-INFEASIBLE 排除。
4. 步骤5:非劣框架、无优越性主张;负/欠功效如实;n<10 标 underpowered(C6)。
