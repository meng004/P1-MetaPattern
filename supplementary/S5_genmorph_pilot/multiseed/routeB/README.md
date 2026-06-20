# Route B — Set N vs Set G 配对多种子(真实 GenMorph PIT 机制)

执行 runbook §4 的 Route B:在**同一 PIT mutant 集、同一评测机制**下得到 Set N(NOETHER 算子代数导出)
与 Set G(GenMorph GP 进化)的逐 mutant 杀死向量,做逐种子 + pooled paired McNemar。
回答威胁 A7(原 head-to-head 仅用 single seed=11)并纠正旧 pilot 的 Python 重写偏差。

## 方法(全部真实工具链,无重写)

| 环节 | 做法 |
|---|---|
| mutant 集 | GenMorph 的 PIT 1.7.4(pitest-wrapper),对 `MathClass` 限定目标方法行 → 与发表 M1..Mk 同源 |
| source 输入 | GenMorph `eval` 的 Randoop 产物(每种子 budget 120s,采样 100 = 对齐 `max_tests=100`) |
| Set N followup | 克隆 source 的 MethodTest XStream-XML,按 Set N 变换改参数值(gcd:swap/×2/(p,q+p)/id;sin:id/π−x/−x/x+2π,Java int32 wrap / inf-nan 处理) |
| MR oracle | Set N 的 `.jor`(repo `aligned/set_n_mrs/`),经 GenMorph `PITestGenerator` → JUnit → PIT |
| FP 规则 | 与 GenMorph 一致:在**原始 SUT** 上 FP>0 的 MR 作废(不计杀死) |
| Set G | 直接用 GenMorph **发表** `mutants_killed.csv` 的 matched-seed union(不重跑,无重写) |
| 配对 | 逐 mutant 2×2 + 精确 McNemar;前提"同工具链 PIT mutant 同序" |

脚本:`setn_eval.py`(gcd)、`setn_eval2.py`(通用 gcd+sin)、`summarize_multiseed.py`、`pair_seed11.py`、
批量编排 `run_gcd_multiseed.sh`、`run_sin_multiseed.sh`。
原始结果:`gcd/setn_result_seed*.json`、`sin/setn_result_seed*.json`、`multiseed_pair_summary.json`。

### 端到端复现

```
# 0. 前置:JDK8/11 + maven;GenMorph 包 Zenodo 10067096 解压到
#    /tmp/genmorph_pilot/genmorph_full/(见 ../analyze_published_multiseed.py 与
#    docs/review_2026-06-20/mvp_s5_aligned_multiseed_runbook.md §5);JAVA_HOME 指向 JDK8。
# 1. source + 评测(每 subject 12 种子):批量脚本内部 = 配置 seed →
#    genmorph.py eval 生成 source test inputs(Randoop;followup 阶段会因缺 gen-transformations
#    报错,但 source 已落地)→ setn_eval{,2}.py 克隆 source XML 生成 Set N followup →
#    PITestGenerator → PIT → setn_result.json。
bash run_gcd_multiseed.sh      # MathClass?gcd?0 × 12 seeds
bash run_sin_multiseed.sh      # MathClass?sin?0 × 12 seeds
# 2. 配对汇总(Set N vs 发表 Set G,逐种子 + pooled McNemar):
python3 summarize_multiseed.py "MathClass?gcd?0" "MathClass?sin?0"
# 3. 对齐校验(seed11 gcd:25 mutant 与发表一致,setG_only=0):
python3 pair_seed11.py
```

> 注:脚本中 `setn_eval*.py` 与 GenMorph 包路径(`/tmp/genmorph_pilot`)是执行时的位置,
> 按你的 checkout / 解压位置调整;`NSAMPLE=100`(对齐 GenMorph `max_tests=100`)。

## 对齐校验(seed11 gcd,`pair_seed11.json` + `gcd/mutations_eqref.csv`)

- 我的 PIT 产出 **25 个 gcd-line mutant**(= 发表 gcd 的 25),算子分布合理(ConditionalsBoundary/InvertNegs/Math/NegateConditionals/PrimitiveReturns)。
- 配对 `both=11, setN_only=2, setG_only=0` → **Set G 杀的 11 个全是 Set N 杀的子集**;`setG_only=0` 在未对齐时几乎不可能出现,强证 mutant 同序对齐成立。

## 结果

### gcd（12 种子全有效）

| seed | Set N | Set G | N_only | G_only | McNemar p |
|--:|--:|--:|--:|--:|--:|
| 11 | 13 | 11 | 2 | 0 | 0.500 |
| 12 | 6 | 17 | 0 | 11 | 0.001 |
| 13 | 11 | 18 | 0 | 7 | 0.016 |
| 21 | 6 | 17 | 0 | 11 | 0.001 |
| 22 | 13 | 12 | 1 | 0 | 1.000 |
| 23 | 11 | 10 | 1 | 0 | 1.000 |
| 31 | 13 | 17 | 0 | 4 | 0.125 |
| 32 | 11 | 18 | 0 | 7 | 0.016 |
| 33 | 13 | 18 | 0 | 5 | 0.063 |
| 41 | 11 | 18 | 0 | 7 | 0.016 |
| 42 | 11 | 14 | 1 | 4 | 0.375 |
| 43 | 11 | 10 | 1 | 0 | 1.000 |

Set N mean=10.8 (6–13);Set G mean=15.0 (10–18);Set N≥Set G 仅 **4/12** 种子。
**POOLED:both=124, N_only=6, G_only=56, McNemar p=2.97e-11 → Set G 显著支配 Set N。**

### sin（11 种子有效;seed31 见 caveat）

| seed | Set N | Set G | N_only | G_only | McNemar p |
|--:|--:|--:|--:|--:|--:|
| 11 | 14 | 16 | 1 | 3 | 0.625 |
| 12 | 14 | 16 | 0 | 2 | 0.500 |
| 13 | 14 | 16 | 1 | 3 | 0.625 |
| 21 | 14 | 13 | 3 | 2 | 1.000 |
| 22 | 14 | 16 | 1 | 3 | 0.625 |
| 23 | 14 | 15 | 2 | 3 | 1.000 |
| 32 | 14 | 17 | 0 | 3 | 0.250 |
| 33 | 14 | 13 | 3 | 2 | 1.000 |
| 41 | 14 | 17 | 0 | 3 | 0.250 |
| 42 | 14 | 15 | 1 | 2 | 1.000 |
| 43 | 14 | 17 | 0 | 3 | 0.250 |

Set N mean=14.0 (恒 14;`oddsym`+`bound` 有效);Set G mean=15.5 (13–17);Set N≥Set G 仅 **2/11** 种子。
**POOLED:both=142, N_only=12, G_only=29, McNemar p=0.0115 → Set G 显著支配 Set N。**

## 结论（诚实，以多种子为准）

1. **两个 subject 上 pooled 均为 Set G 显著支配 Set N**(gcd p≈3e-11,sin p≈0.012)——与论文现有
   "Set N is dominated by Set G" 披露**定性一致**(强化,非推翻)。Set N 的检出效果从来不是本文卖点。
2. **single seed=11 不代表性**:gcd 上 seed11 是 12 个种子里**唯一** Set N>Set G 且 Set G⊆Set N 的点
   (Set N 偏高、Set G 偏低),即原单种子结果**高估了 Set N 相对 Set G**。这就是 A7 选择偏差的实证。
3. **旧 pilot 数字失真已被真实机制替换**:旧 `results/{gcd,sin}/pilot_stats.json`(Python 重写)给出
   gcd 5/17、sin 11/2,与真实机制(seed11 gcd 13/11、sin 14/16)严重不符,作废。

## Caveat（诚实标注，勿洗白）

- **Set N 各 MR 性质不同**:`rho_mono`(gcd)/`rho_bound`(sin)是 **identity-followup 的 O≤ 单次不变量**,
  非严格双输入 metamorphic;`rho_eqref/perm/scale`(gcd)、`oddsym/complement/period`(sin)是双输入 MR。
- **gcd `rho_scale`**:多数种子因 Java int 溢出(2p/2q wrap)在原始程序上即 FP,被作废(仅 seed33 有效)。
- **sin `rho_complement`/`rho_period`**:浮点 π 精度使 sin(π−x)/sin(x+2π) 与 sin(x) 之差偶超 1e-4 → FP,
  **全种子作废**;仅 `oddsym`(精确)+`bound` 有效。这反映 Set N 的等式 oracle 缺浮点/边界 guard,而
  Set G 的 GP 进化 MR 被 FP 惩罚逼出了 guard(更鲁棒)——Set G 的真实优势,亦为 Set N 可改进点。
- **sin seed31 排除**:该种子随机采样含 `Infinity/NaN` 输入,4 条 MR 全 FP 作废(Set N=0)。如实记录,
  **不重采样**(避免 cherry-pick);pooled sin 基于 11 个有效种子。
- **配对前提**:McNemar 假设我重跑的 PIT mutant 与发表 M1..Mk 同序(同 SUT/同 PIT 1.7.4/同 excludedMethods,
  确定性);seed11 gcd 的 `setG_only=0` 与 mutant 数一致是支持证据。
- **采样波动**:每种子随机采样 100 source 致 Set N 检出波动(gcd 6–13);这是种子敏感性的体现,双方皆有。
- 仍守 salami 红线:仅报 detection(generation 命题),不报 k\*/最小子集/domination 选择(姊妹论文 T2)。
