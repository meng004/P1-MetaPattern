# experiment_realbug/ — B1 真 bug 评测（e3nn / PyG，CPU-only 独立验证腿）

> 这是 B1(`docs/review_2026-06-21/b1_cloud_task.md`)的代码/数据家目录。
> 冻结预注册:`docs/review_2026-06-21/prereg_b1_realbug.md`(§3 为不可变冻结区)。
> 目的:用作者未针对设计的上游真实缺陷,检验 Set N 的 MR 识别**非劣性**(非优越性),破 G3 自指的 fault-data 半壁。

---

## 投跑前构建顺序（不可跳步——否则云端 STEP 0 会 ABORT）

```
[1] 实现 mr_sets/ 可执行 MR 定义        ← 最大缺口,需作者(见下"开放设计问题")
[2] 跑 harvest_bug_candidates.py 机械列候选 → 人工核 CPU 可复现 → 落 bug_ledger.csv
[3] commit 冻结: prereg_b1_realbug.md + bug_ledger.csv + mr_sets/(同一 commit)
    回填 freeze hash 到 prereg 头部
[4] git push 到 meng004/P1-MetaPattern 分支 codex-tosem-maturity-review-2026-06-20
[5] 云端 fresh agent: 粘贴 b1_cloud_task.md §B 提示词执行(它会 git clone + 校验 STEP 0)
```

云端 agent 只 **执行** 已冻结的 ledger + mr_sets,**不选 bug、不写 MR、不改 prereg**。

---

## 目录约定

| 路径 | 内容 | 谁产 |
|---|---|---|
| `bug_ledger.csv` | 冻结的待测 bug 清单(机械选,防 cherry-pick) | 作者(harvester + 人工核) |
| `harvest_bug_candidates.py` | GitHub API 机械列候选(可复现选择,见 §3.4 规则) | 已提供 |
| `mr_sets/` | Set N/M/G/L/B 的**可执行** MR 定义 + 接口契约 | **作者(最大缺口)** |
| `repro_snippets/` | 每条 bug 的 CPU 复现 snippet(harvester 落,人工核) | 作者 |
| `results/` | 云端产 `bug_<id>.json` + `RESULTS.md`(跑后) | 云端 agent |

---

## ⚠️ 开放设计问题（mr_sets 的真实工程缺口，必须作者决策）

b1_cloud_task.md §B Step 3c 假设 `mr_sets/` 里是"与论文同目录的 Set N/M/G/L/B"。但**论文的 MR 是针对论文特定 SUT 定义的**(Set N=ρ_rot/ρ_adj/ρ_train-rev/ρ_mono/ρ_train,绑定 EGNN 点云分类器;基线 M/G/L/B 同理)。**真实 e3nn/PyG 缺陷在库内部**(tensor-product / spherical-harmonics / scatter / irreps-bookkeeping)。两者并非天然对齐:

- ρ_rot(SO(3) 旋转不变)**可**直接套到任何"输入旋转→输出应不变"的 e3nn 等变层缺陷上 → 见 `mr_sets/rho_rot.py` 起步。
- 但 ρ_train-rev(SGD 轨迹时反)绑定**训练过程**,对一个 tensor-product **库函数**缺陷无定义;ρ_mono(点密度单调)绑定**分类器推理**。这些对库级缺陷需**重新设计或判定不适用**。
- 基线 M(METRIC+)/G(GenMorph)/L(LLM)/B(literature)同样需对 e3nn/PyG 缺陷重新实例化。

**因此投跑前必须由作者决定**:(a) 哪些块级 MR 能套到库级缺陷(给出可执行实现);(b) 对不适用的 MR,在该 bug 上记 `not-applicable`(非 fired=False,避免把"无定义"当"未检出"污染检出率)。这是**方法决策 + 工程实现**,不能由云端 agent 或脚手架臆造。`mr_sets/README.md` 给出接口契约 + ρ_rot 范例,其余待作者实现。

> 诚实定位:在 mr_sets 实现到位前,B1 **不可投跑**。这是 B1 的真实 binding 工作量(估计数天-1周作者工程),也是面板"真 bug 腿"含金量的来源——它必须是真实现,不能脚手架带过。
