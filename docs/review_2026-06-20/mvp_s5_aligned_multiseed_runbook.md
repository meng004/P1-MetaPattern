# MVP S5-aligned 多种子 runbook — 消除 GenMorph head-to-head 的 single-seed 选择偏差

> 任务来源:`fix_plan_2026-06-20.md` 层 2 的 **A16(1)** — “real new experiment: multi-seed GP +
> GenMorph 原 23-method 基准消 selection bias”,配合威胁 **A7**(“占优轴多为 by-construction /
> co-designed 底物 / **single seed=11**”)。
> 目的:把 §empirical 中 “Set N is dominated by Set G(McNemar p=0.0043,seed=11)” 的负结果披露,
> 从**单一种子**升级为**多种子**证据,回答冷读审稿人 “seed=11 是不是挑出来的” 的质疑。
> 诚实基调(CLAUDE.md §诚实优先于救援 / §6 ARS / fix_plan §3 红线):**只报真数据,失败如实记录,
> 不补造数字,不把负结果洗白**;本实验是 `research`,不可伪装成 `writing`。

---

## 0. 一句话结论(本回合已执行部分)

用 GenMorph **自己发表的 12 种子复现包**(Zenodo 10067096)直接量化 Set G 的种子敏感性:
**Set G 的检出在 12 个 GP 种子间显著波动**(gcd 10→18 / 25,sinh 31→56),而 head-to-head 所用的
**seed=11 恰好落在 Set G 的偏弱档**(23 个 subject 中 11/19 落在最低三分位,仅 2/19 在最高三分位)。
因此 “Set N 被 Set G 占优” 的披露**不是用对 Set N 有利的种子挑出来的**;若换种子,Set G 多半更强,
负结果稳健甚至加重。**另发现**:仓库旧 pilot 自行重写的 Set G 与 GenMorph 发表值严重不符
(sin 旧 pilot 记 2/26、发表值 16/26;gcd 旧 pilot 记 17/25、发表值 11/25),旧 sin “Set N 胜” 是
**重写偏差**造成的假象 —— 必须改用发表数据。

---

## 1. 环境与数据来源(本环境实测)

| 项 | 状态 |
|---|---|
| egress `zenodo.org` | ✅ HTTP 200 |
| JDK | ✅ apt 装 OpenJDK 8(`8u492`)+ 11;`config.py` 的 `JAVA8=/usr/lib/jvm/java-8-openjdk-amd64` 命中 |
| Maven | ✅ 3.9.11(`/opt/maven/bin/mvn`) |
| GenMorph 复现包 | ✅ 下载 `genmorph.zip`(82M)+`mrs.zip`(Set G)+`evaluation.zip`(发表结果)到 `/tmp/genmorph_pilot/` |
| GAssert jar | ✅ **包内预编译** `genmorph/build/libs/GAssert-1.0-SNAPSHOT-all.jar`(无需 `gradlew shadowJar`)|
| Randoop/PIT/EvoSuite jar | ✅ 包内自带(`randoop-all-4.3.0.jar`、`pitest-wrapper-1.7.4.jar`、`evosuite-1.1.0.jar`)|
| 发表种子 | ✅ **12 个**:11,12,13,21,22,23,31,32,33,41,42,43(`pitest_seed*` / `assertions_seed*`)|
| Set N MR 文件 | ✅ 仓库 `supplementary/S5_genmorph_pilot/aligned/set_n_mrs/MathClass?{gcd,sin}?0/*.jir/.jor.txt` |

数据布局(发表包):`evaluation/pitest_seed{S}/<subject>/mutants_killed.csv`,行
`assertions_seed{G},MRk` 给出 gen-种子 G 的第 k 条 MR 在 PIT-种子 S 的 mutant 集上的 0/1 杀死向量;
汇总行 `assertions_seed{G},*` = 该 gen 种子全部 **FP=0 有效** MR 的**并集杀死**;`*,*` = 跨全部 gen
种子的并集(= “GenMorph 任一种子可杀” 的 killable 上限)。

---

## 2. 已执行:Set G 多种子选择偏差分析(真实、发表数据、零重算)

脚本:`supplementary/S5_genmorph_pilot/multiseed/analyze_published_multiseed.py`
输出:`multiseed_setg.json` + `multiseed_setg_report.md`

**指标**:每个 subject、每个种子取**匹配对角**(gen 种子 == PIT 种子)的 `assertions_seed{S},*`
并集杀死(GenMorph 自己的 headline 口径),给出跨种子 mean/sd/min/max/spread/CV 与 seed=11 的排名。

### 2.1 焦点 subject(Set N 可比)

| subject | mutants | killable | 每种子 Set G 并集杀死(s11…s43) | mean | sd | min–max | CV | **seed11** |
|---|--:|--:|---|--:|--:|--:|--:|--|
| `MathClass?gcd?0` | 25 | 21 | 11,17,18,17,12,10,17,18,18,18,14,10 | 15.0 | 3.21 | 10–18 | 0.214 | **11 → 排名 3/12(低端,best 的 61%)** |
| `MathClass?sin?0` | 26 | 17 | 16,16,16,13,16,15,13,17,13,17,15,17 | 15.33 | 1.49 | 13–17 | 0.097 | **16 → 排名 6/12(中位,best 的 94%)** |

### 2.2 全 23 subject:seed=11 是否代表性?

完整表见 `multiseed_setg_report.md`。汇总:**seed=11 在 11/19 个可比 subject 上落在 Set G 检出的
最低三分位,仅 2/19 在最高三分位**。即 head-to-head 的种子对 Set G 偏不利,而非偏有利。
极端例:`GuavaClass?{indexOf,sort,difference}` 在 seed=11 Set G=0(最差种子);`MathClass?sinh`
spread 高达 25(31→56)。

### 2.3 对论文 §empirical / Threats 的诚实落位

- **A7(benchmark 公正性)**:可由 “single seed” 软化为 “我们核对了 GenMorph 全部 12 个发表种子;
  seed=11 对 Set G 偏弱(11/19 落最低三分位),故占优结论不是有利种子挑选的产物”。这是**写作层
  承认 + 真数据支撑**,不替代 A16 的完整配对实验(§4)。
- **诚实红线**:不得反过来宣称 “Set N 跨种子更强”——本回合**没有**产生 Set N 的多种子配对数据
  (见 §3 阻塞与 §4 协议)。只能说 Set G 侧的种子稳健性已核验。

---

## 3. 关键发现 + 阻塞:为何 Set N 多种子配对未在本回合落地

### 3.1 旧 pilot 的 Set G 与发表值严重不符(必须改用发表数据)

| subject(seed=11) | 旧 pilot 重写 Set G | GenMorph **发表** Set G |
|---|--:|--:|
| gcd | 17/25 | **11/25** |
| sin | **2/26** | **16/26** |

旧 `supplementary/S5_genmorph_pilot/results/{gcd,sin}/pilot_stats.json` 用**自行重写**的 GenMorph
MR(Python 端口),与 GenMorph 用 GAssert `EvaluateMRs`+PIT 的发表结果不一致,sin 方向甚至**翻转**
(旧 pilot “Set N 11 胜 Set G 2” → 发表 Set G 16 反而占优)。这正是审稿人会抓的 **self-reimplementation
bias**。**结论:Set G 一律以发表 `mutants_killed.csv` 为准,旧 pilot 的 Set G 数字作废。**

### 3.2 用原生管线评 Set N 的真实阻塞

GenMorph `eval` 在 `evaluation_states_followup` 阶段需要 **per-(MR,seed) 的 followup 状态**,由
`{system_id}_seed{S}.transformations.txt` 生成;该文件**只在 `gen`(GP 合成)阶段产出**,
**不在 `mrs.zip`**。因此:

- 直接 `eval` 发表 Set G:缺 transformations,跑不动(但 Set G 结果已发表,无需重跑)。
- 把我们的 Set N 注入 `eval`:同样缺 Set N 的 followup 状态;Set N 的变换虽简单(置换/缩放),
  但需写成 GenMorph transformations 格式或自建对齐求值器。
- `all`(gen+eval)能产出 followup,但会**重新 GP 出一套与发表不同的 Set G**,且耗时大、需另证对齐。

~~因此本回合不强行产出 Set N 多种子配对数据~~ → **已由 Route B 执行并产出**(见 §4 与
`supplementary/S5_genmorph_pilot/multiseed/routeB/`):自建 followup(克隆 source XML 改参数值)绕过了
GP-transformation 耦合,经真实 PITestGenerator + PIT 评测 Set N,与发表 Set G 配对。

---

## 4. 已执行:Set N vs Set G 完整配对多种子(Route B,真实 PIT 机制)

> **结果**(完整表 + 数据 + 脚本见 `supplementary/S5_genmorph_pilot/multiseed/routeB/README.md`):
> 用真实 GenMorph 工具链(Randoop 输入 + 自建 Set N followup + PITestGenerator + PIT 1.7.4)在与发表
> 同源的 mutant 集上评测 Set N,与发表 Set G 配对。
> - **gcd(12 种子)**:Set N mean 10.8 vs Set G mean 15.0;Set N≥Set G 仅 4/12;
>   **pooled McNemar p=2.97e-11 → Set G 显著支配 Set N**。
> - **sin(11 有效种子;seed31 因采样含 inf/nan 全 FP 排除)**:Set N mean 14.0 vs Set G mean 15.5;
>   **pooled p=0.0115 → Set G 支配**。
> - **seed11(原 head-to-head 种子)对 Set N 偏有利**(gcd 唯一 Set G⊆Set N 的点)→ 单种子不代表性,
>   正是 A7 选择偏差的实证。**旧 pilot 的 gcd 5/17、sin 11/2 是 Python 重写失真,已被真实机制数字替换。**
> - 对齐校验(seed11 gcd):25 mutant 与发表一致,setG_only=0(Set G⊆Set N),强证 mutant 同序对齐。
> - 诚实 caveat 见 routeB/README.md(mono/bound 为 O≤ 单次不变量;scale int 溢出;complement/period 浮点 FP;
>   seed31 inf/nan 全作废不重采样)。
>
> 以下为执行所用协议(留档):

目标:在**同一 mutant 集、同一评测机制**下,得到 Set N 与 Set G 的逐 mutant 0/1 杀死向量,
做**逐种子 paired McNemar + pooled**。两条等价路线,任选其一:

**路线 A(原生管线,最权威):** 对 `{gcd,sin}` × 12 种子跑 GenMorph `all`,把
`aligned/set_n_mrs/<subject>/*.jir/.jor` 与发表 Set G 一并放入 `assertions_seed{S}/<subject>/`,
经 `EvaluateMRs`+PIT 得双方杀死向量。**对齐校验(硬门槛)**:重跑的 Set G `COUNT` 必须复现
`evaluation/pitest_seed{S}` 发表值;不符则报 “对齐破裂”,停。

**路线 B(自包含对齐求值器,较轻):** 用包内 `pitest-wrapper` 对 `MathClass` 生成 PIT mutant
(确定性,应得与发表一致的 M1..M25 / M1..M26),写一个最小求值器:对每个 mutant、每个种子的输入
样本,执行 Set N 关系(gcd: `gcd(a,b)=gcd(b,a)`、`gcd(ka,kb)=k·gcd(a,b)` 等)→ 杀死向量;
Set G 直接取发表向量。**对齐校验**:用本求值器复算一条已知 Set G MR 的杀死向量,与发表逐位一致
才认为 mutant 编号对齐,Set N 配对方有效。

**汇报模板(每 subject×seed 一行)**:
```
subject | seed | setN_kills | setG_kills(published) | both | N_only | G_only | neither | mcnemar_p
```
完成后:(i) 把 §empirical 的 seed=11 单点升为 12-seed 配对;(ii) 若 Set N 仍被占优(很可能),
如实保留负结果披露,只是把 “single seed” 去掉;(iii) 任一 subject/seed 失败如实记录。

---

## 5. 复现本回合(Set G 侧)

```bash
# 1. 取数据(若 /tmp 已清空)
mkdir -p /tmp/genmorph_pilot && cd /tmp/genmorph_pilot
for f in genmorph.zip mrs.zip evaluation.zip; do
  wget -qO $f "https://zenodo.org/api/records/10067096/files/$f/content"; done
mkdir -p genmorph_full && cd genmorph_full
unzip -oq ../genmorph.zip; unzip -oq ../evaluation.zip -d eval_unpacked; unzip -oq ../mrs.zip -d mrs_unpacked
# 2. 跑分析
cd <repo>/supplementary/S5_genmorph_pilot/multiseed
python3 analyze_published_multiseed.py \
    /tmp/genmorph_pilot/genmorph_full/eval_unpacked/evaluation \
    multiseed_setg.json multiseed_setg_report.md
```

产物 `multiseed_setg.json` / `multiseed_setg_report.md` 已随仓库提交。

---

## 6. 诚实备案(本回合做了 / 没做)

- ✅ 做了:用 GenMorph 发表的 12 种子真数据量化 Set G 选择偏差;核出 seed=11 对 Set G 偏弱;
  核出旧 pilot Set G 重写偏差(sin 方向翻转)。
- ❌ 没做(如实记录,非跳过):Set N 的多种子配对杀死向量(因 §3.2 followup 状态耦合 gen 阶段);
  故**未**声称任何 Set N 跨种子优劣。协议见 §4,留作 committed follow-up。
- 红线遵守:只报 detection(generation 命题),不报 k\*/最小子集/domination 选择(姊妹论文 T2);
  负结果(Set N 被占优)保留,未洗白。
