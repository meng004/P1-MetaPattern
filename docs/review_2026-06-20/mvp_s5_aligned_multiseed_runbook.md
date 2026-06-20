# S5-aligned 多-seed 云执行包 — NOETHER Set N vs GenMorph Set G

> **基础**:升级自 `docs/tosem_maturity_2026-06-16/s5_aligned_cloud_runbook.md`(single-seed 版),把 Set N 的稳健性从单 seed 扩展到 3-seed,并把 Set G 的 single-seed 严格基线与 12-seed 上界两端明确分离。
> **本实验是纯 Java + PIT 变异检测,不调用任何 LLM / API key**;`.env` 只含文件系统路径,由 `setup.sh` 自动生成。
> **命题边界(self-overlap 红线)**:本实验只回答 **generation / detection sufficiency**(Set N 的变异检出充分性)。**严禁**报告 k\*(最小 MR 子集)、selection、domination —— 那是姊妹论文 T2(TSE)的命题。引用 GenMorph 上游(Ayerdi et al. 2024)+ Zenodo 10067096。

---

## 1. 目标与产出

在 GenMorph 自己发表的 **23-subject 公开 benchmark**(Math 10 + Lang 5 + Guava 8,~557–562 mutants)上,固定一切 substrate(JDK8 / Randoop / PIT 1.7.4 / GAssert evaluator / 上游 seed),只让 **MR 集合**这一个变量变化,对比:

| 对比对象 | 取值方式 | 说明 |
|---|---|---|
| **Set N(NOETHER)** multi-seed | 自行重跑 SEED=11/12/13 | Set N 是确定性手写 MR(71 条);跨 3 seed 跑的是 **Randoop 测试输入的随机性**对检出的影响 → 报 Set N 的**稳健性** |
| **Set G(GenMorph)single-seed 严格基线** | 上游 `pitest_seed11/<subj>/mutants_killed.csv` | 与单次 Set N 同等 MR 搜索预算的**严格 like-for-like** 基线 |
| **Set G(GenMorph)12-seed 上界** | 上游 CSV 内 `*` union 行(11/12/13/21..43 共 12 seed) | GenMorph 花 ~12× 搜索预算的**最好情形上界**,刻意偏向对手,作为 upper bound 而非 like-for-like |
| **cost-normalized** | effective-MR-ratio(`n_effective_mrs / n_mrs`) | 把"花多少 MR 预算换多少检出"显式化,佐证 Set N 的 compactness |

**产出文件**:
- `results/comparison_seed11.json`、`results/comparison_seed12.json`、`results/comparison_seed13.json`(每 seed 的 per-subject + 四层 strata)
- `results/seed{11,12,13}/<subject>/{setn,setg}_mutants_killed.csv`(逐 MR × 逐 mutant kill 矩阵)
- 跨 seed 聚合表(回报时人工汇总,见 §4 步骤 5):Set N 的 3-seed 均值 + Wilson95;Set G 的 single-seed 与 12-seed 两端
- 四层(ALL / Math / Lang / Guava)union-kill / Wilson95 / McNemar + per-block 分解 + effective-MR-ratio

---

## 2. 前置:把本地仓库交给云端

`experiment/s5_aligned/` 是一个**独立的 git 仓库**,已配置远程:

```
origin → https://github.com/meng004/S5_aligned_experiment.git   (私有)
```

**本地操作员**(在 `experiment/s5_aligned/` 目录内,先确保 results/ 已被 .gitignore):

```bash
git status                     # 确认无未提交的源码改动(results/ 应被忽略)
git push origin main           # 把最新 main 推到私有 repo
```

**云端**:`git clone https://github.com/meng004/S5_aligned_experiment.git` 即可。若 repo 私有,云端需配置一个**只读 deploy key 或 PAT**(在云平台 secret manager 里生成,**绝不**写进 `.env` 或任何 commit)。

---

## 3. 环境需求

| 项 | 要求 |
|---|---|
| OS | Ubuntu(云 Linux) |
| JDK | OpenJDK **8**(GAssert / PIT 必需)+ 11;`JAVA_HOME` 必须指向 JDK 8(`setup.sh` 自动检测并写入 `.env`) |
| 构建 | Maven + GAssert fat-jar(`setup.sh` 自动构建) |
| 磁盘 | **≥30 GB**(Stage 1 Randoop/PIT 中间产物;3 个 seed 各有独立 `output_dir_*` 与 `results/seed<N>/`,留足余量) |
| egress | **必须放行**:`zenodo.org`(GenMorph 包 ~80 MB)+ apt 源 + Maven Central。这是云端最可能被白名单拦的点 |
| GPU | 不需要 |
| LLM / API | **完全不需要,不调用任何模型** |
| 时间 | 每 seed:Stage 1(Randoop+PIT)~4–7 h + Stage 2(EvaluateMRs)~30 min;3 seed 串行约 **15–22 h**(可断点续跑,断连不丢) |

---

## 4. 精确执行步骤(逐条命令)

> 所有命令在 repo 根目录 `S5_aligned_experiment/` 内执行。先读 `CLAUDE.md`(8 条协作规则)与 `README.md` 再动手。

### 步骤 1 — 测试门(必须 exit 0)

```bash
bash tests/run.sh
```

绿(exit 0)才继续;**红则停下报告**,不要绕过。该门含 Python 单测 + `bash -n` 语法检查 + 23-subject / 142-DSL-file 计数校验 + secret-leak grep。

### 步骤 2 — 一次性环境搭建

```bash
bash setup.sh
```

自动:apt 装 jdk8/jdk11/maven/python3 → 检测 JVM 路径写入 `.env` → pip 装 pandas/numpy/scipy/statsmodels → 下载 GenMorph Zenodo 复现包到 `/tmp/genmorph_pilot/` → 装 Major 2.0.0(jre8)→ 构建 GAssert fat-jar。约 10 min。

> 若 `zenodo.org` 下载被 egress 白名单拦截,**如实报告并停**,不要伪造任何数据。

### 步骤 2.5 — 确认 Set G 各 seed 上游数据是否存在(关键,先做)

`run_all.sh` 对每个 SEED 从上游 `…/evaluation/pitest_seed${SEED}/<subj>/mutants_killed.csv` 取 Set G 的 **strict single-seed** 基线。上游包内 Set G 的 `all-seeds` union 已覆盖 12 个 seed(11/12/13/21/22/23/41/42/43 等,见 `compare_sets.py` 的 `setg_seed_distribution`),说明 **seed 12、13 的上游 Set G 数据应存在**。投跑前逐 seed 确认:

```bash
PILOT=/tmp/genmorph_pilot/evaluation
for S in 11 12 13; do
  d="$PILOT/pitest_seed${S}"
  n=$(ls "$d"/*/mutants_killed.csv 2>/dev/null | wc -l)
  echo "pitest_seed${S}: ${n} subjects with Set G CSV  (dir exists: $([[ -d $d ]] && echo yes || echo NO))"
done
```

**判定**:
- 某 seed 的 `pitest_seed${S}` 目录存在且 23 个 subject 都有 CSV → 该 seed **Set N 与 Set G 都可比**。
- 某 seed 上游**无** Set G 目录或 CSV 缺失 → **如实标注**:该 seed **只报 Set N 稳健性**(Set N 的检出在该 Randoop seed 下的表现),Set G 列填 `N/A — upstream pitest_seed${S} not in Zenodo package`,**不要**用 seed11 的 Set G 冒充。

> 注意:即便某 seed 缺 strict single-seed Set G,**12-seed all-seeds 上界**始终来自上游 CSV 内的 `*` union 行(不依赖 `pitest_seed${S}` 单 seed 目录),所有 seed 都能报。

### 步骤 3 — 对 SEED=11/12/13 分别跑全流程(可断点续跑)

`run_all.sh` 读 `SEED` 环境变量(默认 11),写 `results/seed${SEED}/`,输出 `results/comparison_seed${SEED}.json`。**断点续跑**:某 subject 若 `results/seed${SEED}/<subj>/setn_mutants_killed.csv` 已存在则跳过,断连重连可继续。

逐 seed 串行(每个 seed 起独立 nohup,前一个跑完再起下一个;也可在确认磁盘充足后并行,但更稳妥是串行):

```bash
# seed 11
SEED=11 nohup bash scripts/run_all.sh > results/run_seed11.log 2>&1 &
tail -f results/run_seed11.log        # 跟踪;出现 "Done. Summary: results/comparison_seed11.json" 即完成

# seed 12(seed11 完成后)
SEED=12 nohup bash scripts/run_all.sh > results/run_seed12.log 2>&1 &
tail -f results/run_seed12.log

# seed 13(seed12 完成后)
SEED=13 nohup bash scripts/run_all.sh > results/run_seed13.log 2>&1 &
tail -f results/run_seed13.log
```

断连后重连任一 seed 直接重跑同一条命令即可(已完成 subject 自动跳过)。

> 不要用 `--compare-only` 跳过 Stage 1,除非该 seed 的 per-subject CSV 已齐全且通过步骤 4 对齐验证。

### 步骤 4 — 对齐验证(诚信硬约束,每 seed 必做)

Set G 是直接 adopt 上游 published CSV,所以"对齐"= **确认 run_all.sh 拷进 `results/seed${SEED}/<subj>/setg_mutants_killed.csv` 的内容逐字节等于上游 `pitest_seed${SEED}/<subj>/mutants_killed.csv`**。任一不一致即"对齐破裂,停"。

```bash
PILOT=/tmp/genmorph_pilot/evaluation
for S in 11 12 13; do
  echo "=== seed $S alignment ==="
  for f in results/seed${S}/*/setg_mutants_killed.csv; do
    subj=$(basename "$(dirname "$f")")
    up="$PILOT/pitest_seed${S}/$subj/mutants_killed.csv"
    if [[ -f "$up" ]]; then
      diff -q "$f" "$up" >/dev/null && echo "  OK  $subj" || echo "  BROKEN  $subj  (停:对齐破裂)"
    else
      echo "  N/A  $subj  (上游无 pitest_seed${S},该 subject Set G 不可比)"
    fi
  done
done
```

任一 `BROKEN` → **停止实验,报告"对齐破裂,数据不可信"**,不要继续聚合。

### 步骤 5 — 跨 seed 聚合 + 四层分解

每个 `comparison_seed${SEED}.json` 已含四层(ALL / Math / Lang / Guava)的 strata:`setn` / `setg_seed`(strict single-seed)/ `setg_allseeds`(12-seed 上界)各自的 kills / rate / Wilson95,以及 `mcnemar_vs_seed` 与 `mcnemar_vs_allseeds`(exact McNemar 的 b/c/p)。

跨 3 seed 聚合(只聚合 **Set N** 的 multi-seed 稳健性;Set G 报两端):

```bash
python3 - <<'PY'
import json, glob, math
def wilson(k,n,z=1.96):
    if n==0: return [0.0,0.0]
    p=k/n; d=1+z*z/n; c=p+z*z/(2*n)
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
    return [round((c-h)/d,4), round((c+h)/d,4)]

files=sorted(glob.glob("results/comparison_seed*.json"))
print("seeds found:", files)
strata=["ALL","Math","Lang","Guava"]
acc={s:{"setn_k":[], "setn_n":[], "gseed_k":[], "gall_k":[]} for s in strata}
for fp in files:
    d=json.load(open(fp))
    for s in strata:
        st=d["strata"].get(s)
        if not st: continue
        acc[s]["setn_k"].append(st["setn"]["kills"])
        acc[s]["setn_n"].append(st["mutants_total"])
        acc[s]["gseed_k"].append(st["setg_seed"]["kills"])
        acc[s]["gall_k"].append(st["setg_allseeds"]["kills"])

print(f"\n{'stratum':7} | SetN 3-seed mean rate (Wilson95 pooled) | G@seed | G@all")
for s in strata:
    a=acc[s]
    if not a["setn_n"]: continue
    nseed=len(a["setn_n"])
    # Set N: pool across seeds (sum kills / sum mutants) + per-seed mean rate
    K=sum(a["setn_k"]); N=sum(a["setn_n"])
    pooled=K/N if N else 0
    per_seed_rates=[k/n for k,n in zip(a["setn_k"],a["setn_n"]) if n]
    mean_rate=sum(per_seed_rates)/len(per_seed_rates) if per_seed_rates else 0
    spread=f"[{min(per_seed_rates):.3f},{max(per_seed_rates):.3f}]" if per_seed_rates else "-"
    w=wilson(K,N)
    gseed=sum(a["gseed_k"])/N if N else 0
    gall=sum(a["gall_k"])/N if N else 0
    print(f"{s:7} | N {mean_rate:.3f} (per-seed {spread}, pooled {pooled:.3f} W95 {w}) over {nseed} seeds | G@seed {gseed:.3f} | G@all {gall:.3f}")
PY
```

**per-block 分解 + effective-MR-ratio**:per-subject 的 `aligned_metrics.json`(由 `parse_results.py` 写)含 `set_n.effective_mr_ratio` / `set_g.effective_mr_ratio`(= 实际 fire 的 MR 数 / 可用 MR 数);跨 subject 池化见 `aggregate_metrics.py`。如需 effective-MR-ratio,对每 seed 额外跑:

```bash
for S in 11 12 13; do
  python3 scripts/aggregate_metrics.py --results-dir results/seed${S} \
      --output results/aligned_summary_seed${S}.json 2>/dev/null \
    && echo "seed${S} effective-MR-ratio 已写入 aligned_summary_seed${S}.json" \
    || echo "seed${S}: aggregate_metrics 需要 aligned_metrics.json(由 parse_results.py 产生);如缺则只报 comparison_seed${S}.json 的 union-kill"
done
```

> per-block(NOETHER 8-block:G / O_le / L\* 三块非空,T\*/T\*_2/D\*/E\*/I\* 在此 benchmark 全空)分解:从 `set_n_mrs/<subj>/*@<block>_*.jir.txt` 的文件名前缀回溯每条 MR 所属 block,对照 `setn_mutants_killed.csv` 的逐 MR kill 行统计。block 全空本身是 NOETHER 的结构性预测(stateless utility 方法),如实报告,不当作缺陷。

---

## 5. 【预注册分层假设】模板(防 HARKing,必须在跑 multi-seed 前书面填写并提交)

> 在执行步骤 3(multi-seed 正式跑)**之前**,把下文填好、加时间戳、commit 进 `docs/review_<DATE>/prereg_s5_multiseed.md`。跑完后无论结果是否符合预期,**一律如实报告**,不得 retroactive 改假设。
> 依据:seed11 已观测 Guava 域 Set N kill-rate **0.704(57/81)** vs G@all-seeds **0.543(44/81)**(McNemar p=0.027),vs G@seed11 **0.531(43/81)**;Math 域 Set N **0.216** 明显劣于 G@all-seeds **0.618**。

```markdown
# 预注册声明 — S5-aligned multi-seed(Set N 稳健性)

Pre-registered on: <YYYY-MM-DD HH:MM UTC>  by <executor-tag>
Frozen before running: SEED=11/12/13 full pipeline
Commit: <填 commit hash>

## A-priori 分层假设(在看到 seed12/13 结果之前固定)

H1 (a-priori, directional, Guava): 在 Guava 域,Set N 的 union kill-rate
   将 > Set G single-seed(strict like-for-like)基线。
   依据:seed11 已观测 0.704 vs 0.531(G@seed11),McNemar p=0.027(vs G@all-seeds)。
   强形式(也预注册):Set N 在 Guava 域将 ≥ Set G 12-seed all-seeds 上界(0.543)。

H2 (a-priori, directional, Math): 在 Math 域,Set N 预期 *劣于* Set G,
   无论 single-seed 还是 all-seeds(算子代数手写 MR 在数值连续函数上覆盖弱于 GP 进化)。
   依据:seed11 观测 Set N 0.216 vs G@all-seeds 0.618。

H3 (a-priori, Lang): 在 Lang 域,Set N 与 Set G single-seed 预期统计持平(无明确方向预测)。

H4 (robustness, all strata): Set N 跨 3 个 Randoop seed 的 kill-rate 离散度小
   (Set N 是确定性 MR,变异仅来自测试输入随机性);预期 per-seed rate spread 窄。

## 报告承诺
- seed12/13 跑完后,逐层报告实际 kill-rate,即便与 H1–H4 相悖也照报。
- 任何 subject 失败 / 上游 Set G 缺失 / 对齐破裂,如实标注,不补造、不跳过。
- 不做事后分层(post-hoc sub-grouping);本预注册之外的任何分层一律标 "exploratory, not pre-registered"。
- 样本不足处(per-stratum n 小,如 Guava 81 mutants)标 underpowered,同报 Wilson95 + exact McNemar p(即便 p>0.05)。
```

---

## 6. 诚信硬约束(执行者必须遵守)

1. **对齐破裂即停**:步骤 4 任一 `BROKEN` → 停,报"对齐破裂,实验不可信",不聚合、不回填。
2. **不伪造**:zenodo 下载失败 / subject 失败 / 上游 seed 缺失 → 如实报告并停或标注,绝不补造数字。
3. **self-overlap 红线**:只报 **detection / generation sufficiency**(union kill-rate、McNemar、Wilson95、effective-MR-ratio)。**严禁**报 k\*(最小 MR 子集)、selection、domination —— 那是 T2(TSE)命题。
4. **样本不足诚实标注**:per-stratum n 小处标 `underpowered for α=0.05`,同报 Wilson95 + exact McNemar p(即便 p>0.05)。
5. **不改预注册**:跑完结果无论是否符合 §5 假设,照实报。

---

## 7. 回报模板(执行者跑完后回填给作者)

```markdown
# S5-aligned multi-seed 执行回报

## 0. 元信息
- 云主机:Ubuntu, <核数/内存/磁盘 GB>
- 起止时间(UTC):seed11 <..>;seed12 <..>;seed13 <..>
- setup.sh:✓ / 失败原因
- tests/run.sh:exit 0 ✓ / 失败项
- 预注册 commit:<hash>(跑 multi-seed 之前已冻结)

## 1. 对齐验证(步骤 4)
| seed | OK subjects | BROKEN | N/A(上游无 Set G) |
|---|---|---|---|
| 11 | 23 | 0 | 0 |
| 12 | <n> | <n> | <列出 subject> |
| 13 | <n> | <n> | <列出 subject> |
（任一 BROKEN>0:实验中止,以下数据不可信）

## 2. Set N 稳健性(3-seed)+ Set G 两端,四层
| 层 | subj | mut | SetN per-seed rate (spread) | SetN pooled (Wilson95) | G@seed(strict) | G@all(12-seed 上界) | McNemar N vs seed (b,c,p) | McNemar N vs all (b,c,p) |
|---|---|---|---|---|---|---|---|---|
| ALL | 23 | ~557 | | | | | | |
| Math | 10 | ~403 | | | | | | |
| Lang | 5 | ~73 | | | | | | |
| Guava | 8 | ~81 | | | | | | |

## 3. 预注册假设裁决(如实)
- H1(Guava: SetN > G single-seed):支持 / 不支持 — 实测 SetN <r> vs G@seed <r>,p=<>
- H1 强形式(SetN ≥ G all-seeds):支持 / 不支持 — <r> vs <r>,p=<>
- H2(Math: SetN 劣于 G):支持 / 不支持 — <r> vs <r>
- H3(Lang: 持平):支持 / 不支持 — <r> vs <r>,p=<>
- H4(SetN 跨 seed 稳健):per-seed spread = <[min,max]>,判定 窄/宽

## 4. per-block 分解(NOETHER 8-block;G/O_le/L* 非空,余 5 块空=结构性 finding)
| block | SetN MR 数 | 跨 3-seed union kills(均值) | 备注 |
|---|---|---|---|

## 5. effective-MR-ratio(cost-normalized)
| seed | SetN eff/total (ratio) | SetG eff/total (ratio) |
|---|---|---|

## 6. 异常 / 缺失 / underpowered 标注
- 失败 subject:<列出 + 日志位置>
- 上游 Set G 缺失 seed:<列出,该 seed 只报 SetN 稳健性>
- underpowered 层:<标注 + Wilson95 + exact p>

## 7. 命题边界声明
本回报仅涉及 detection / generation sufficiency。未涉及 k*/selection/domination(T2 命题)。
引用:GenMorph 上游 Ayerdi et al. 2024;Zenodo 10067096;复现 seed 11/12/13。

## 8. 回传
results/ 整目录(尤其 comparison_seed{11,12,13}.json + 各 seed per-subject CSV + run_seed*.log)。
```

---

**相关真实资产路径**(供作者核对):
- `experiment/s5_aligned/scripts/run_all.sh`(SEED 环境变量、results/seed${SEED}、Set G adopt 上游 pitest_seed${SEED}、可续跑)
- `experiment/s5_aligned/scripts/compare_sets.py`(G@seed strict / G@all-seeds 12-seed 上界 / per-seed 分布 / Wilson95 / exact McNemar / 四层 strata)
- `experiment/s5_aligned/scripts/aggregate_metrics.py`(effective-MR-ratio 池化)
- `experiment/s5_aligned/setup.sh`、`tests/run.sh`、`.env.example`
- `experiment/s5_aligned/docs/SECTION_6_6_RESULTS.md`(seed11 已观测:Guava 0.704 vs G@all 0.543 p=0.027;Math 0.216 vs 0.618;12-seed = 上游包内 11/12/13/21..43)
- git remote:`origin → https://github.com/meng004/S5_aligned_experiment.git`(已是私有 repo,前置只需 `git push origin main`)