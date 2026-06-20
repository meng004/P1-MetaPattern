# 云端启动提示词 — s5_aligned seed12/13 confirmatory

> 用途：把下面 §2 的提示词整段粘贴进一个新的 Claude Code 云端会话即可启动。
> 日期：2026-06-20。prereg pre-run 证据：commit `f2a5980`（在 P1-MetaPattern 分支 codex-tosem-maturity-review-2026-06-20）。

## 1. 需要克隆的仓库（2 个）+ 1 个自动下载

| # | 仓库 | 分支 | 作用 |
|---|---|---|---|
| 1 | `meng004/S5_aligned_experiment` | 默认 | 实验 harness（run_all.sh / 自带 Set N 生成器 / setup.sh 自举）。结果提交在此。 |
| 2 | `meng004/P1-MetaPattern` | **codex-tosem-maturity-review-2026-06-20** | 冻结的 prereg（commit `f2a5980`）+ brief + cloud_exec_plan + 红线。只读治理 + 跑后 §3 freeze 校验。 |
| — | GenMorph 包（Zenodo 10067096，~80MB）| — | **由 S5_aligned_experiment/setup.sh 自动下载**，无需手动 clone/fetch。 |

注：P1 的 `experiment/` 是 gitignored，s5_aligned 是独立仓库——必须单独 clone `S5_aligned_experiment`。

## 2. 粘贴给云端会话的提示词（整段复制）

```
你是云端执行 agent。任务：执行 NOETHER 论文的 s5_aligned 多种子 confirmatory 实验（seed12/13），严格遵守已冻结的预注册（HARKing-free）。

## 克隆两个仓库
git clone https://github.com/meng004/S5_aligned_experiment.git
git clone -b codex-tosem-maturity-review-2026-06-20 https://github.com/meng004/P1-MetaPattern.git

## 先读（逐字遵守，治理/规范）
- P1-MetaPattern/docs/review_2026-06-20/prereg_s5_multiseed.md  ← 冻结预注册（pre-run commit f2a5980）。定义 H1-H5、钉死定义、单侧/多重比较规则、underpowered 触发器、self-overlap 红线。**绝不编辑其 §3。**
- P1-MetaPattern/docs/review_2026-06-20/cloud_task_brief_seed12_13.md  ← 自包含执行 brief。
- S5_aligned_experiment/CLAUDE.md  ← 该仓库 8 条协作规则（issue/plan-first、branch-per-task、no-test-no-merge、secret 边界）。

## 环境自举（幂等，自动下载 GenMorph）
cd S5_aligned_experiment && bash setup.sh
# setup.sh：装 JDK8+11/Maven/Python、写 .env（JAVA8/GENMORPH/MAJOR_HOME）、下载 GenMorph Zenodo 包、装 Major、建 GAssert。
# （brief §2 里写的手动 fetch_genmorph.sh 被 setup.sh 取代——以 setup.sh 为准。）

## 预检（任一不过即停、如实报告、绝不补造数字）
- setup.sh 成功；.env 含 GENMORPH / MAJOR_HOME / JAVA8。
- 上游 pitest_seed12 与 pitest_seed13 存在（Set G like-for-like 基线）。某 seed 缺 → 该 seed 只报 Set N 稳健性、Set G 记 N/A，**不拿 seed11 冒充**。

## 执行（断点可续）
SEED=12 bash scripts/run_all.sh    # 产出 results/comparison_seed12.json
SEED=13 bash scripts/run_all.sh    # seed12 完成后再起

## 裁决 H1-H5（严格按 prereg §7.1）
单侧 H1/H2、双侧 H3；seed12=primary、seed13=replication；per-mutant Wilson + subject-level cluster-bootstrap 95% CI(10000) + paired Wilcoxon；underpowered 当 discordant b+c<25；b+c=0 记 test undefined。

## 诚信硬约束（违反即该 confirmatory 作废）
- 不编辑 P1 的 prereg §3；跑完在 P1 仓库执行 `git diff f2a5980 -- docs/review_2026-06-20/prereg_s5_multiseed.md`，§3 区段须为空。
- report-all：每层都报，含 ALL/Math 负结果，Math McNemar p 写明面，不藏脚注。
- 不 cherry-pick seed/subject；非预注册分层一律标 exploratory。
- self-overlap 红线：只报 detection/generation sufficiency；**禁** k* / minimal-MR-subset / selection / domination（姊妹论文 T2，TSE）。
- Set G 只用 GenMorph 发表数据（重写版已废弃：sin 16→2）。
- 保留 G1 caveat：不得断言 "Set N 始终有效"（acos/pow 受 1e-4 绝对容差 artifact 排除）。

## 可选 Run B（有余力）
G1 修复的 Math arm（相对/ULP 容差 + acos domain guard + pow 溢出保护），输出 results/seed*_g1fixed/，作为独立标注的 arm 并列报（预期缩小 Math 差距、不翻盘）。

## 产出与回报
- 在 S5_aligned_experiment 新建分支 claude/s5-seed12-13-<short-id>，commit results/comparison_seed{12,13}.json + 跨 seed 聚合（Set N 3-seed range/SD；Set G single/12-seed 两端）+ H1-H5 裁决报告，push。
- 回报：commit hash + H1-H5 裁决表（逐条 支持/不支持/inconclusive + 实测值 + 单侧 p + CI）+ 任何 abort/缺失数据，诚实。
```

## 3. 完成后回到本地

云端跑完会 push 分支 `claude/s5-seed12-13-<id>` 到 `S5_aligned_experiment`。本地 `git -C experiment/s5_aligned fetch && git -C experiment/s5_aligned checkout <分支>` 取回结果，我据 prereg 解读裁决、再决定整合（过 D1-D7）。
