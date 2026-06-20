# 云端执行计划 — 实验加固（攻势在主张维度，effectiveness 保持诚实）

> 日期：2026-06-20。前置评估：见本回合对话 + `s5_aligned_seed11_assessment.md`。
> harness：`experiment/s5_aligned`（run_all.sh = done，覆盖全 23 subject，支持 `SEED` 环境变量、可断点续跑）。
> remote：`meng004/S5_aligned_experiment`（origin）。

## 0. 诚实定位与天花板（先读）

- **能达成**：① 坐实/收回 Guava effectiveness 胜（多种子）；② Set N 跨 Randoop seed 稳健性（H4）；③ GP 生成可靠性 / seed-lottery 作**支撑指标**（非 headline）；④ 修 G1 编码让 Math 比较公平。
- **不能达成**：翻转"Math 上 Set G seed-robust 压制"（12 种子已锁死，硬翻=cherry-pick）；关闭**独立人类 κ** 那条腿（需人，云端做不了）。
- **定位红线**：所有结论框在 **identification / generation-reliability** 维度（论文真实主张），**不**改写成 fault-detection effectiveness 论文（反漂移 D1）；**self-overlap 红线**：只报 detection/generation sufficiency，**禁** k\*/selection/domination（那是 T2/TSE）。

## 1. 预检（投跑前，逐条确认，任一不过即停并如实报告）

```bash
# 环境
echo "$GENMORPH" "$MAJOR_HOME"; java -version 2>&1 | head -1   # JDK8
df -h .                                                        # ≥30 GB
# Set G 上游 seed12/13 是否存在(决定 H1-H3 能否 like-for-like)
for S in 12 13; do d="$GENMORPH/.../evaluation/pitest_seed${S}"; \
  echo "seed${S}: $(ls $d 2>/dev/null | wc -l) subjects, dir=$([[ -d $d ]] && echo yes || echo NO)"; done
# 某 seed 无上游 Set G → 该 seed 只报 Set N 稳健性, Set G 列填 N/A, 不拿 seed11 冒充
```

## 2. Step 0 —— 预注册（**投跑前必做，修上次 HARKing 漏洞**）

上次 H1-H4 未跑前 commit、且"依据 seed11 已观测"=对 seed11 HARK。**本次：把 H1-H4 + 可靠性假设写进 `docs/review_2026-06-20/prereg_s5_multiseed.md`，加时间戳，commit，然后才跑 seed12/13**——使 seed12/13 成为 HARKing-free 的 out-of-sample 检验。

预注册内容（a-priori，对 seed12/13 固定）：
- **H1**(Guava): Set N union kill-rate ≥ Set G single-seed；强形式 ≥ Set G 12-seed union。
- **H2**(Math): Set N 劣于 Set G（single & all-seeds）。
- **H3**(Lang): Set N 与 Set G single-seed 统计持平。
- **H4**(robustness): Set N 跨 seed11/12/13 kill-rate 离散度小（确定性 MR，变异仅来自 Randoop 输入）。
- **H5**(generation reliability, a-priori): Set G 单跑产有效 MR 的成功率 < 100%（部分 subject 跨 seed 全 0），Set N 确定性产同一 MR 集（FP-validity 是 (MR,SUT,encoding) 的固定属性，无 seed lottery）。**定义钉死**：valid MR = 在原始 SUT 上 FP=0 的 MR；reliability = #seeds-with-≥1-valid-MR / #seeds。
- 报告承诺：结果无论是否符合 H1-H5 一律照报；不事后分层；per-stratum n 小标 underpowered + Wilson95 + exact McNemar(即便 p>0.05)。

## 3. Run A —— s5_aligned 多种子（主跑，全 23 subject）

```bash
for S in 12 13; do
  SEED=$S nohup bash scripts/run_all.sh > results/seed${S}/_logs/run.log 2>&1 &
  wait    # 串行(磁盘稳妥);出现 comparison_seed${S}.json 即完成
done
```
产出：`results/comparison_seed{12,13}.json` + per-subject + 四层 strata（同 seed11 格式）。
覆盖：① Guava 多种子（H1 effectiveness 探针）② Set N 3-seed 稳健性（H4）③ 每 seed 的 Set G valid-MR 成功率（H5 可靠性）④ H1-H3 out-of-sample。

**对齐校验**：每 seed 跑 `pair_seed11.py` 同款 sanity（mutant 集与发表一致、setG_only=0）；**对齐破裂即停，不聚合**。

## 4. Run B —— G1 编码修复后重跑 Math（单独标注的 arm，使比较公平）

G1：当前 1e-4 **绝对**容差对大范围超越函数失败 + 缺 domain guard 使 acos(x)≤π 在域外 FP → acos/pow 的 Set N MR 全被排除。

```bash
# 改 eval 容差为 相对/ULP + 加 domain/NaN guard(acos |x|≤1, pow 溢出保护)
# 以独立 EXP 标签跑,产 results/seed11_g1fixed/ 等,与原编码 arm 并列报,不混淆
SETN_TOL_MODE=relative SETN_DOMAIN_GUARD=1 SEED=11 bash scripts/run_all.sh
```
**诚实预期**：缩小 Math 差距 + 让 Set N 在 acos/pow 产有效 MR（强化 H5 的"Set N 处处有效"对比）；**不翻盘**（gcd 12-seed 已锁死）。原编码 arm 与 G1 arm **都报**，差异归因写清。

## 5. Analysis C —— 生成可靠性指标（单一权威定义，离线可做）

```bash
# 仅用 GenMorph 发表 12-seed 数据(Zenodo 10067096)重算,不重跑 Set G,不重写
python3 supplementary/S5_genmorph_pilot/multiseed/analyze_published_multiseed.py
# 输出: 每 subject 的 #seeds-with-valid-MR / 12, 跨 seed kill 方差; 对照 Set N 确定性(方差=0)
```
**交叉核对**：与 routeB `published_setg_union.json` 一致；与 s5_aligned per_subject CSV 的列**定义对齐后**才用（当前两源 reliability 列定义打架，必须统一）。**禁**用旧重写 Set G（sin 16→2 已 superseded）。

## 6. 输出与回报模板

- `prereg_s5_multiseed.md`（Step 0，跑前 commit）
- `results/comparison_seed{12,13}.json` + 跨 seed 聚合表（Set N 3-seed 均值+Wilson95；Set G single/12-seed 两端）
- `results/seed*_g1fixed/`（Run B，独立标注）
- 生成可靠性表（Analysis C）
- 回报：逐层 kill-rate + H1-H5 裁决（支持/不支持 + 实测值 + p）+ 失败/缺失如实标注

## 7. 诚信硬约束（执行者必守）

1. **预注册先行**：未 commit prereg 不得跑 seed12/13。
2. **不改预注册**：结果无论是否符合 H1-H5 照报。
3. **不 cherry-pick**：不换 seed/subject 凑 Set N 赢；不藏 Math 输；本预注册外的分层标 "exploratory"。
4. **不伪造/不重写**：Set G 用发表数据；下载/subject 失败如实标注并停。
5. **self-overlap 红线**：只报 detection/generation sufficiency，禁 k\*/selection/domination。
6. **样本不足诚实标注**：per-stratum n 小标 underpowered + Wilson95 + exact McNemar。

## 8. 整合回论文（跑完后，过 D1-D7 反漂移再动手）

- **frame 换位**（攻势）：把 generation-reliability + structural-coverage 提为结果维度；effectiveness head-to-head **降权**为 scope/complementarity（与 A5/A9 协同）。
- **诚实降权 ≠ 藏**：Math 被压制 + McNemar p 留 Threats；G1 修复后的公平数字并列报。
- **Guava 多种子**：若稳 → scope-bound effectiveness 胜点（坐实）；若不稳 → 诚实收回，只留 reliability/coverage。
- **不碰**：独立人类 κ 那条腿仍需人执行（本计划不覆盖，单列）。

## 9. 中止条件

- 对齐校验 BROKEN → 停，报"对齐破裂,实验不可信"。
- 上游 Set G seedN 缺失 → 该 seed 只报 Set N 稳健性，不拿 seed11 冒充。
- 任一 subject 失败 → 如实标注，不补造。
