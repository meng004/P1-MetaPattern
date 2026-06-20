# 云端任务 Brief — s5_aligned seed12/13 confirmatory 跑（冷启动自包含）

> 给云端 Claude Code 会话 / 云主机的**自包含**指令。执行者无本对话记忆，所有上下文在此。
> 日期：2026-06-20。Repo：`meng004/P1-MetaPattern`。基线分支：`codex-tosem-maturity-review-2026-06-20`。

## 0. 任务一句话
按**已冻结的预注册** `docs/review_2026-06-20/prereg_s5_multiseed.md`（pre-run commit `f2a5980`），在 GenMorph 公开 23-subject benchmark 上跑 `experiment/s5_aligned` 的 **SEED=12 然后 SEED=13**，产出 confirmatory 结果并裁决 H1–H5。**这是 HARKing-free 的样本外检验——不得改预注册 §3。**

## 1. 必读（执行前）
1. `docs/review_2026-06-20/prereg_s5_multiseed.md` —— H1–H5、钉死定义、单侧/多重比较规则、underpowered 触发器、红线。**§3 已冻结于 `f2a5980`，禁止编辑。**
2. `docs/review_2026-06-20/cloud_exec_plan_experimental_strengthening.md` —— 步骤、预检、中止条件、回报模板。

## 2. 预检（任一不过即停并如实报告，不补造）
- JDK8（+JDK11）、Maven 3.6+、磁盘 ≥30 GB。
- 取第三方 GenMorph 包（不入库，Zenodo 10067096）：`bash supplementary/S5_genmorph_pilot/multiseed/routeB/fetch_genmorph.sh /tmp/genmorph_pilot`。
- 确认上游 `pitest_seed12`、`pitest_seed13` 存在（Set G like-for-like 基线）；某 seed 缺 → 该 seed 只报 Set N 稳健性，Set G 列填 N/A，**不拿 seed11 冒充**。

## 3. 执行（断点可续）
```
cd experiment/s5_aligned
export GENMORPH=/tmp/genmorph_pilot/...   # 按 fetch 脚本输出
export MAJOR_HOME=...                       # PIT/Major 依赖
SEED=12 nohup bash scripts/run_all.sh > results/seed12/_logs/run.log 2>&1   # 完成出 comparison_seed12.json
SEED=13 nohup bash scripts/run_all.sh > results/seed13/_logs/run.log 2>&1   # seed12 完成后再起
```
对齐校验：每 seed 跑 `pair_seed11.py` 同款 sanity（mutant 集与发表一致、setG_only=0）；**对齐破裂即停，不聚合**。

## 4. 可选 Run B（G1 公平性，独立标注，勿混淆）
相对/ULP 容差 + domain/NaN guard（acos |x|≤1、pow 溢出保护）重跑 Math，输出 `results/seed*_g1fixed/`，与原编码 arm **并列报**。预期缩小 Math 差距、让 Set N 在 acos/pow 产有效 MR；**不翻盘**。

## 5. 诚信硬约束（必守，来自预注册 §6）
- **不改预注册 §3**；跑完 `git diff f2a5980 -- docs/review_2026-06-20/prereg_s5_multiseed.md` 对 §3 区段须为空，否则 confirmatory 作废。
- **report-all**：每层都报，含 ALL/Math 负结果；Math McNemar p 写正文不藏。
- **不 cherry-pick** seed/subject；非预注册分层标 exploratory。
- **self-overlap 红线**：只报 detection/generation sufficiency；禁 k\*/minimal-MR-subset/selection/domination（T2/TSE）。
- **Set G 仅用 GenMorph 发表数据**（重写版已废弃：sin 16→2）。
- **统计**：单侧 H1/H2、双侧 H3；每假设 seed12=primary、seed13=replication；per-mutant Wilson + **subject-level cluster-bootstrap CI（10000）+ paired Wilcoxon**；underpowered 触发 b+c<25；b+c=0 记 test undefined。
- **G1 caveat**：未修 G1 前不得断言 "Set N 始终有效"。

## 6. 产出与回报
- `results/comparison_seed{12,13}.json` + per-subject + 四层 strata；跨 seed 聚合（Set N 3-seed range/SD；Set G single/12-seed 两端）。
- `results/seed*_g1fixed/`（若做 Run B）。
- **H1–H5 裁决报告**（按预注册 §7.1 证伪判据，逐条 支持/不支持/inconclusive + 实测值 + 单侧 p + CI）。
- commit 到新分支 `claude/s5-seed12-13-<id>`，push；回报 commit hash + 裁决摘要。失败/缺失如实标注。

## 7. 启动方式（三选一，同一 brief 驱动）
- **A（推荐，与上次同）**：开一个 Claude Code 云端会话，指向本 repo + 基线分支，把本文件作为任务指令。
- **B**：用 RemoteTrigger 在 claude.ai/code 起远程 routine（由仓库维护者授权）。
- **C**：自有 Ubuntu 云主机，clone repo 后按 §2–§6 手动执行。
