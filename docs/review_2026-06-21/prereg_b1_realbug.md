# 预注册 — B1 真 bug 评测（e3nn / PyG，CPU-only 独立验证腿）

> **状态**：草稿 v1 —— **投跑前必须 commit 冻结并回填 freeze hash 到本文件头**（机制同 s5_aligned 的 `f2a5980`）。
> **冻结契约**：§3「假设与分析规则」为不可变区。跑后 `git diff <FREEZE_HASH> -- docs/review_2026-06-21/prereg_b1_realbug.md` 对 §3 须为空,否则 confirmatory 作废、结果降级 exploratory。
> **pre-run 证据 commit**：`<FREEZE_HASH 待回填>`（与 `experiment_realbug/bug_ledger.csv` 同一 commit 冻结）。
> **目的**：破除面板 G3 自指硬墙的 *fault-data 半壁*——用作者未针对设计的上游真实缺陷分布,检验 Set N 的 MR 识别非劣性。配套 B2(独立人类 κ)破 *labelling 半壁*。两腿缺一不可。
> **范围铁律(D1/D4 反漂移)**：本腿是 **MR identification** 的 *非劣性*(non-inferiority)证据,**非** fault-detection 优越性。Set N/M/G/L/B 是论文既有 MR 目录,本腿唯一的新外部输入是 bug 分布。

---

## 1. 背景与定位

论文 §4.2(`para:real-bug-protocol`, L1374–1382)已**预注册**真 bug 协议、§3.7/H4(L1369)已声明 *detection-rate non-inferiority on real faults*(Δ=0.10 a-priori)。本腿即该协议的 **CPU-only 受限执行**:只取在小张量上、无训练、无整模型前向即可复现的 e3nn/PyG 上游缺陷子集。因 H4 已在论文,冻结它**天然 HARKing-free**(非事后追加)。

## 2. 资产与可复现边界

- **受测上游库(外部、自指破除来源)**：e3nn(`github.com/e3nn/e3nn`)、PyTorch Geometric(`github.com/pyg-team/pytorch_geometric`),按各 bug 的 pre-fix parent commit 检出。
- **缺陷来源(数据)**：两库 *closed* issues(标 `bug`)+ linked merged fix commit + issue/PR 内复现 snippet。无私有数据。
- **CPU 可复现过滤**：缺陷须在 tensor-product / spherical-harmonics / scatter / irreps-bookkeeping 等代码上、用手搭小张量复现,**无 GPU / 无训练 / 无整模型前向**。不满足者记 `CPU-INFEASIBLE` 排除。
- **MR 集**：`experiment_realbug/mr_sets/` 内的 Set N/M/G/L/B 可执行定义(与论文同目录,**不得新写 MR**)。⚠️ 见 §5 实施缺口。

## 3.〔冻结区 — 不可变〕假设与分析规则

### 3.1 假设

- **H4(主,预注册,非劣)**：在冻结 bug ledger 上,Set N 的真 bug 检出率与最佳非-NOETHER 集(M/G/L/B 中最高者)之差 `gap = best_other − N` **≤ Δ = 0.10**。**非劣性**主张,**非**优越性。
- **H4-complement(描述性,次要)**：逐 bug × 逐集报 "MR fired = True/False"(集内 ≥1 条 MR 在 published tolerance 下暴露 buggy 行为即 fired)。报 fired MR 的算子块覆盖。**无优越性检验**。
- **H4-coverage(描述性)**：`coverage_NOETHER` = ledger 中出现的 cat-(i)–(iv) 类别里,Set N 含 ≥1 条块对齐 MR 的比例。仅描述,无 p。

### 3.2 统计契约（冻结）

- **单位**：bug 为独立单元(一缺陷一条);多输入先聚合到 bug 级二元(≥1 输入 fired 即 fired),防伪重复。
- **检出率**：per-set = (#bugs 该集 pre-fix fired 且非 FP) / (#OK bugs);报 **Wilson 95% CI**。
- **配对检验**：Set N vs 各 {M,G,L,B} 的 **exact McNemar**(paired by bug),报 discordant b,c。
- **欠功效触发(冻结,同 `f2a5980`)**：某对 `b + c < 25` → 记 **"underpowered, inconclusive"** + exact two-sided McNemar p + 双方 Wilson CI,**绝不**升级为 "confirmed non-inferiority / tie"。`b + c = 0` → "test undefined"。
- **多重比较(冻结)**：Holm–Bonferroni 校正全部 pairwise McNemar 族(primary family = N-vs-others 4 对;若比 5 集则 10 对全族)。
- **H4 裁决**：`gap ≤ 0.10` → "H4 非劣支持(within Δ=0.10)";`gap > 0.10` → "H4 不支持:Set N 落后最佳基线 <gap>"(直说,不重框)。

### 3.3 诚信红线（冻结）

- **方向诚实**：若 Set N 非非劣(gap>0.10),如实记负结果,不下放脚注、不在别处重框为优越、不删 GenMorph(Set G)落败。
- **self-overlap 红线**：ledger 缺陷必须 100% 来自上游 maintainer fix commit;**零**作者注入/选择以偏向块的缺陷。任一条可追溯到作者注入 → confirmatory 作废。
- **欠功效如实**：若 `n_ok < 10` 或 primary McNemar `b+c < 25`,正文必标 "n=<n_ok>, underpowered for α=0.05; descriptive evidence"(C6),不作 headline win。非劣 PASS 在小外部样本上仍有意义(破自指),但须带 Wilson CI + 欠功效 caveat。
- **scope**：不外推出 e3nn/PyG SE(3)-equivariant 代码;跨域广度与 reactor-corpus 外部腿(Option 1)仍 future work。不主张 fault-detection 优越;detection 在论文维持 secondary executability check(C5/L262)。

### 3.4 bug 选择规则（冻结，机械、防 cherry-pick）

从两库 *closed* + 标 `bug` + 有 linked merged fix commit + issue/PR 内有复现 snippet 的 issue 中,取满足 CPU 可复现过滤(§2)的 **最近修复的 N 条**,上限 = 协议目标 10 条,尽量 cat-(i)–(iv) 各 ≥1,余按 recency。每条记 `{repo, issue_url, fix_commit, pre_fix_parent_commit, cat, cpu_repro_snippet_path}` 入 `experiment_realbug/bug_ledger.csv`,与本 prereg **同一 commit 冻结**。冻结后云端只 *执行* 该 ledger,**不选 bug**。

### 3.5 abort / 降级条件

- prereg 或 ledger 在跑后被改(git diff §3 非空)→ confirmatory 作废,结果记 exploratory。
- ledger 任一条缺 `{issue_url, fix_commit, pre_fix_parent_commit}` → 该条 BLOCKED 排除(不臆造缺陷)。
- 复现需 GPU/训练/整模型前向 → CPU-INFEASIBLE 排除(记原因)。

---

## 4. 回插论文（跑后，不 overclaim）

- §4.2 由"committed but not run"→ 实测结果子节(H4 非劣裁决 + per-set Wilson CI + Holm-corrected McNemar + 欠功效/负结果 caveat)。
- §Threats 构念效度威胁 (c)(L1333/L2629):由"hand-constructed mutation"→ "在作者未针对设计的固定外部缺陷分布上,Set N 非劣 within Δ=0.10(或落后 <gap>,直说)"。
- §6/G3 自指:本腿把 fault 来源改为作者独立(上游 maintainer fix),破 EQ1/EQ3 author-vs-author 循环 **的 real-bug 半壁**。
- **不做**:不使 κ 独立(需 B2);不立优越性(H4 仅非劣);不外推 e3nn/PyG 外。

---

## 5. ⚠️ 实施缺口（投跑前必须先解决，非云端 agent 能自动补）

1. **`experiment_realbug/mr_sets/` 可执行 MR 定义**(最大缺口):论文 Set N(ρ_rot/ρ_adj/ρ_train-rev/ρ_mono/ρ_train)+ 基线 M/G/L/B 的 MR 是针对论文特定 SUT(MathSignal 方法 / EGNN 分类器)定义的;**它们对 e3nn/PyG 库级缺陷(tensor-product/spherical-harmonics/scatter)的适用性需作者设计**——这是真实工程+方法决策,不能由云端 agent 或本草稿臆造。`mr_sets/` 目录、MR 接口契约、ρ_rot 起步示例见 `experiment_realbug/README.md`。
2. **`experiment_realbug/bug_ledger.csv`**:按 §3.4 机械规则从 GitHub 选,需作者执行(可用 `experiment_realbug/harvest_bug_candidates.py` 机械列候选,再人工核 CPU 可复现 + 落 ledger)。
3. **push**:本文件 + ledger + mr_sets + b1_cloud_task.md 须 commit 并 **push 到 `meng004/P1-MetaPattern` 分支 `codex-tosem-maturity-review-2026-06-20`**,云端 clone 才拿得到。

---

*冻结后本文件 §3 不可变;§1/§2/§4/§5 可在跑后补注(标注 post-run)。*
