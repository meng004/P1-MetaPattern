# s5_aligned 远端实验评估：是否达到预期效果（seed11）

> 日期：2026-06-20。数据：`experiment/s5_aligned/docs/results/{comparison,per_subject,strata}_seed11.csv/json`（提交 06-17，a3ecf08）。
> 基准：`docs/review_2026-06-20/mvp_s5_aligned_multiseed_runbook.md`（预注册多-seed 计划 + H1-H4）。
> 评估只对照预注册判据，不事后改判据（§10.3 防 HARKing）。

## 0. 一句话结论

**部分达到。** 中立外部腿（GenMorph 公开 23-subject benchmark + GenMorph 自家 evaluator/mutant set/kill 定义）**已真实跑通 seed11**，这实质性地破了"自指" 硬墙；并产出两个值得报的正向发现（Guava 域 Set N 胜过 GenMorph 12-seed 上界；determinism/seed-lottery）。**但它还不是一个 confirmatory 结果**：multi-seed 只完成 1/3、prereg 未在跑前提交且 H1-H4 是对 seed11 的 HARK、aggregate 是 *负* 结果、Math 比较被编码 artifact 混淆。**支持"互补/scope-bound/确定性"的诚实定位，不支持"NOETHER 胜出"主张。**

## 1. 预期 vs 实得

| 预期（runbook） | 实得 | 判定 |
|---|---|---|
| 中立 substrate 头对头（破自指） | seed11 全 23 subject/562 mutant 跑通，GenMorph 原生工具链/mutant/kill 定义 | ✅ 达到 |
| Set N 3-seed 稳健性（11/12/13） | 仅 seed11 | ❌ 1/3 |
| Set G single-seed vs 12-seed 上界 | 两端都报（all-seeds union 来自上游 CSV，不依赖 seed12/13） | ✅ 达到 |
| 预注册 H1-H4 跑前 commit + 跑后裁决 | **prereg 文件不存在**；H1/H2 显式"依据 seed11 已观测…"=对 seed11 HARK；seed12/13 未跑→无 out-of-sample 检验 | ❌ 未达 |
| 诚实报告（含负结果/underpowered） | 实验队 writeup 异常诚实，未 over-claim | ✅ 达到 |

## 2. 实测结果（seed11，逐层）

| Stratum | subj | mut | Set N | G@seed11 | G@all-seeds(12) | McNemar N vs seed |
|---|---:|---:|---:|---:|---:|---|
| **ALL** | 23 | 562 | **0.313** | 0.363 | 0.607 | b=77,c=46, **p=0.0066** |
| Math | 10 | 403 | 0.216 | 0.313 | 0.618 | b=55,c=16, **p≈0** |
| Lang | 5 | 78 | 0.410 | 0.449 | 0.615 | b=17,c=14, p=0.72 |
| **Guava** | 8 | 81 | **0.704** | 0.531 | 0.543 | b=5,c=16, **p=0.027** |

- **Aggregate：Set N 输**（0.313 vs single-seed 0.363, p=0.0066；vs 12-seed 上界 0.607 大幅落后）。
- **Guava：Set N 胜过 GenMorph 12-seed union**（0.704 vs 0.543, p=0.027）——强、值得报。
- **Math：Set N 大幅劣**（0.216 vs 0.618）——但见 §4 G1，疑似编码 artifact。
- **Lang：持平**（p=0.72）。

## 3. 真实正向价值（可报）

1. **中立腿已建立**：在 GenMorph 自家 benchmark + 自家 evaluator 上比较，单变量只动 MR 集——**破"作者自实现 substrate/自评" 硬墙**的另一条腿（与工业开发/测试分离互补）。
2. **Guava 胜出**：Set N 确定性手写 MR 在 Guava 域胜过 GenMorph 花 ~12× 搜索预算的 12-seed union（p=0.027）。
3. **determinism / seed-lottery**：GenMorph 单次 GP 在 6/13 个 Lang+Guava subject 产 0 个有效 MR（indexOf/sort 跨 12 seed 全 0）；Set N 确定性、处处产有效 MR。novel、证据扎实。
4. **真实中介变量**：决定胜负的是 SUT 关系 *exact vs approximate*（超越函数在 1e-4 绝对容差下识别失败 / acos 域外 NaN），即 meta-pattern 前提条件本身——与 NOETHER scope 设计自洽。

## 4. 阻碍"达到预期"的缺口（排序）

- **G0 multi-seed 1/3 + 无 prereg（最致命，方法论）**：prereg 未跑前 commit、H1-H4 对 seed11 HARK、seed12/13 未跑→**当前无任何 HARKing-free 的 confirmatory 检验**。报 seed11 为"预注册确认"= §10.3 HARKing，评审必抓。
- **G1 Math 编码混淆（实验队自评最高优先）**：Set N 的 Math 劣势部分是 artifact——固定 1e-4 *绝对* 容差对大范围超越函数失败；缺 domain/NaN guard 使 acos(x)≤π 在域外 FP→acos/pow 全部 MR 被排除。未修则"Set G>Set N on Math"非公平方法学陈述（H2 也被混淆）。
- **G2 aggregate 是负结果**：与论文诚实定位（非 aggregate 优越）自洽，但不是"胜"；若整合须严格框为互补/scope，**不得**上位成 superiority（撞反漂移 D1/D4）。
- **G3 统计粒度**：pooled per-mutant McNemar 忽略 within-subject 相关；需补 subject-level/clustered 检验。
- **G4 外部效度**：单 benchmark、n=23、Set N 单 seed。

## 5. 让它"达到预期"的最小动作

1. **现在就 commit 真 prereg**（H1-H4 + 时间戳）到 `docs/review_2026-06-20/prereg_s5_multiseed.md`，**在 seed12/13 跑之前**——使 seed12/13 成为 HARKing-free 的 confirmatory 检验（当前 H1-H4 作为对 seed12/13 的预注册是合法的）。
2. **跑 seed12/13** 完成 3-seed：H4 稳健性 + H1-H3 out-of-sample 确认。
3. **修 G1**（相对/ULP 容差 + domain guard）重跑 Math，或显式 scope-limit Math 为"编码混淆，非方法陈述"。
4. **补 subject-level/clustered 统计**（与 pooled McNemar 并列）。
5. **框为 complementary / scope-bound / deterministic**（实验队 SECTION_6_6 已如此），整合前过 D1-D7 反漂移；守 self-overlap 红线（不报 k\*/selection——T2 命题）。

## 6. 对绑定约束的净效果

中立腿**已建立**（破自指），但**当前形态是双刃**：移除了"无外部证据"批评，却引入"你唯一的中立检验显示 aggregate 被压制、且未预注册/单 seed"风险。**只有**按 §5 补全（prereg→seed12/13→修 G1→clustered 统计→互补框架）后，才能把它从"双刃"变成稳的 minor-revision 杠杆。否则它把一个 major 理由换成另一个。
