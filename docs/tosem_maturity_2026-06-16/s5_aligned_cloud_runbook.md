# S5-aligned 云端执行 runbook — NOETHER vs GenMorph (23-subject benchmark)

> **用途**:在云主机执行 `experiment/s5_aligned`(NOETHER Set N vs GenMorph Set G,在 GenMorph 自己发表的 **23-subject 公开 benchmark** / ~557 mutants 上的单变量对比)。产出 `results/aligned_summary.json` = 化解 reviewer "单一代码库 / 作者自选 SUT / substrate-bias" 批评的**中立证据**,跑完可直接补进论文 §empirical(对应 NEXT_STEPS 的 G1 最高 ROI 项)。
> **关键**:此实验是**纯 Java + PIT 变异检测,不调用任何 LLM / API key**;`.env` 只含路径,由 `setup.sh` 自动生成。与本项目此前的多厂商网关评审完全无关。

## 1. 环境需求

| 项 | 要求 |
|---|---|
| OS | Ubuntu(云 Linux) |
| JDK | OpenJDK **8**(GAssert/PIT 必需)+ 11;`JAVA_HOME` 必须指向 JDK 8 |
| 构建 | Maven + GAssert fat-jar(`./gradlew shadowJar`,setup.sh 自动构建) |
| 磁盘 | **≥30 GB**(Stage 1 中间产物 ~10 GB) |
| egress | `zenodo.org`(GenMorph 包 ~80 MB)+ apt 源 + Maven Central — **云端最可能被白名单拦的点,需放行** |
| GPU | 不需要 |
| 时间 | Stage 1(Randoop+PIT,23 subject)~4–7 h;Stage 2(EvaluateMRs)~30 min |

## 2. 依赖(`setup.sh` 自动安装,无需手动)

- **apt**:`openjdk-8-jdk openjdk-11-jdk maven python3-pip wget unzip git curl ca-certificates`
- **pip**:见 `s5_aligned_requirements.txt`(pandas / numpy / scipy / statsmodels)
- **外部数据**:GenMorph Zenodo 复现包 `https://zenodo.org/records/10067096`(evaluation.zip + mrs.zip + genmorph.zip)→ 解包到 `/tmp/genmorph_pilot/`

## 3. 环境变量(`setup.sh` 自动检测 JVM 路径并写 `.env`,**无需手填、无密钥**)

```bash
JAVA8=/usr/lib/jvm/java-8-openjdk-amd64
JAVA_HOME=$JAVA8                                  # 必须 JDK 8
GENMORPH=/tmp/genmorph_pilot/genmorph_full/genmorph
GASSERT_JAR=$GENMORPH/build/libs/GAssert-1.0-SNAPSHOT-all.jar
PITEST_WRAPPER=$GENMORPH/pitest-wrapper-1.7.4.jar
RANDOOP_JAR=$GENMORPH/randoop-all-4.3.0.jar
S5_ROOT=<repo 根>        SEED=11        SUBJECTS=all      # all = 23 个 subject
```

## 4. 云端可行性

✅ **可行**(CLAUDE.md §8 明确许可)。Claude Remote(≥30 GB 盘、容忍长任务)可跑 Stage 1;用 `nohup` 防断连,`run_all.sh` **可断点续跑**(per-subject Randoop/PIT 产物缓存,重跑跳过已完成)。
- README §4 那句 "`--reproduce` LOCAL ONLY" 是**旧注释**,以 §8 为准(云端已许可)。
- **前置步骤 0**:`experiment/s5_aligned/` 是本地独立 git 仓库(未推到远程)。云端要先能拿到它 —— 先把它 push 到一个**私有** GitHub repo,云端再 `git clone`。

## 5. 任务启动 prompt(直接粘给云端 Claude agent)

```text
你在一台全新 Ubuntu 云主机上执行 NOETHER vs GenMorph 单变量对比实验(S5 aligned)。
目标:在 GenMorph 自己发表的 23-subject 公开 benchmark(Math10+Lang5+Guava8,~557 mutants)上,
对比 Set N(NOETHER 算子代数导出的 71 条 MR)与 Set G(GenMorph GP 进化 MR)的变异检出,
其余 substrate(JDK8/Randoop/PIT1.7.4/GAssert evaluator/seed=11)全部固定为 GenMorph 上游配置。

前置:仓库 S5_aligned_experiment 已 clone 到当前目录(若没有,先 git clone <你的私有repo>)。

约束:
- 这是纯 Java/PIT 实验,绝不调用任何 LLM/API;.env 只含路径、由 setup.sh 自动生成。
- 需 ≥30GB 磁盘 + egress 访问 zenodo.org 与 apt 源。
- 先读 CLAUDE.md(8 条规则)与 README.md 再动手。

按序执行:
1. bash tests/run.sh                 # 测试门,必须 exit 0,否则停下报告
2. bash setup.sh                     # 装 JDK8/11+maven+python依赖,下载 GenMorph Zenodo 包,构建 GAssert jar(~10min)
                                     # 若 zenodo 下载被 egress 白名单拦截,如实报告并停,不要伪造数据
3. nohup bash scripts/run_all.sh > run.log 2>&1 &   # 完整 Stage1(Randoop+PIT ~4-7h,可断点续跑)+ Stage2(EvaluateMRs ~30min)
   tail -f run.log                   # 跟踪进度;断连后重连可继续(产物已缓存)
4. 完成后报告 results/aligned_summary.json:
   n_subjects(应=23)、total_mutants、Set N 与 Set G 的 kills/kill_rate/Wilson 95% CI、paired McNemar p。

诚实要求(硬约束):
- Stage1 中对 Set G 单独重跑 EvaluateMRs 必须复现 GenMorph 上游 published mutants_killed.csv(对齐验证);
  若不一致,报告"对齐破裂,实验不可信",不要继续。
- 任何 subject 失败如实记录,不跳过、不补造数字。
- 这是 generation(检出充分性)实验,只报 detection;不报 k*/最小子集/domination(那是姊妹论文 T2 的命题)。
- 样本不足处标注 underpowered;给出每个 subject 的 per-block 分解。
- 跑完把 results/ 整个目录回传给我(尤其 aligned_summary.json + per-subject)。
```

## 6. 产出与回填

- `results/aligned_summary.json`:23-subject pooled Set N vs Set G(kills / kill_rate / Wilson CI / paired McNemar p)+ per-subject 明细。
- 这是在**对手公开 benchmark** 上的中立 head-to-head,补进论文 §empirical 可直接回应 substrate-bias 批评。
- 回填时仍守 self-overlap 红线:只报 detection(generation 命题),不报 k\*/selection(T2 命题);引用 GenMorph 上游(Ayerdi et al. 2024)+ Zenodo 10067096。
