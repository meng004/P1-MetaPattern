# B1 候选 bug 机械核对审计 (2026-06-21)

> 目的:为 `prereg_b1_realbug.md` §3.4 的 bug 选择做**机械、防 cherry-pick**的候选核对,判定每个候选是否「真功能 bug + 映射 cat-(i)–(iv) + CPU 小张量可复现 + 有 fix/parent commit 锚点」。
> 方法:3 个并行 agent,工具用**本地已 clone 的 e3nn/PyG git 历史(`git show` 实证 diff/parent)+ WebFetch 公开 issue 页**,**不经 api.github.com**(避免 token 扩散与 rate limit)。部分条目在 `torch 2.12.1+cpu` 上实证复现。
> 诚实定位:本审计是**投跑前的 ledger 可填性核验**,不是实验结果(尚无合格 ledger,故未跑 MR set)。

---

## 1. 三路核对汇总

### 路径 C — 机械最近 closed-bug 窗口(32 候选,防偏采样)

`harvest_bug_candidates.py` 机械列出 e3nn+PyG 最近 closed `bug` issue 共 32 条,逐条分类:

**结果:映射 cat-(i)–(iv) 的 = 0。全部 none。** 成因高度集中于四类(均非对称性/等变破坏):
1. JIT / torchscript / torch.fx / torch.compile / export(占比最大)
2. install / 依赖版本 / 打包 / 序列化
3. device / CUDA
4. dataset 下载-加载-数据质量 / type-hint / doc

擦边项核实后仍 none:e3nn #368(S2conv 缺归一化,非等变破坏)、pyg #10560(QM9 上游 SDF 数据质量)、e3nn #466(教程绘图)。

### 路径 A — e3nn 专搜等变性/张量积(6 候选)

| issue | 真bug | cat | CPU可复现 | fix / parent | 根因 | 入ledger |
|---|---|---|---|---|---|---|
| #420 | **no**(约定) | none | — | — | `1o` 分量按 (y,z,x) 实球谐基排序 ≠ 笛卡尔 R;用户误解约定 | no |
| #296 | **yes** | rho_train_inf(「表示等价」,非标准4类) | yes 逻辑上;**当前环境 infeasible** | `b9e64db` / `6fc34a9` | TP 归一化系数 sum 内漏乘 connection-mode mul → 等价 irreps 不同输出 | **maybe**(见复现保真度) |
| #352 | **yes**(现象真实) | rho_train_inf(非确定性) | yes(报告者 CPU 复现) | **NOT-FOUND** | FCTP fx-codegen 浮点规约顺序不定,~50%,`use_deterministic_algorithms` 无效 | maybe(无 fix 锚点) |
| #466 | no | none | — | — | transformer **教程**结果,需整模型 forward | no |
| #316 | no | none | — | `d8e735a`/`e4842dd` | CartesianTensor 非 nn.Module,device 迁移 | no |
| #374 | no | none | — | — | `_wigner` cosmetic deprecation warning,数值正确 | no |

### 路径 B — PyG 专搜 scatter/聚合(6 候选,均本地 git + torch2.12 实证)

| commit/PR | 真bug | cat | CPU可复现 | fix / parent | 根因 | MR | 入ledger |
|---|---|---|---|---|---|---|---|
| scatter_argmax #7495 | yes(crash) | **none** | **no(当前torch不复现)** | 788fc10a / 93d50662 | `reduce='max'` 旧torch报错(须`'amax'`);torch2.12 已等价 | held | no |
| PointTransformerConv #5332 | yes | none | maybe(需整层) | 3c02604d / c18bced5 | softmax 后应 sum 却 mean | held(mean/sum 皆置换不变) | no |
| QuantileAggregation #7407 | **yes** | none(crash) | **yes(实证)** | dd20c206 / 18f16ad0 | `dim_size>index.max()+1` 悬空索引越界 | held | maybe |
| SortAggregation #7412 | **yes** | none(梯度) | **yes(实证)** | 18f16ad0 / 1de9dee1 | `fill_value=x.min()-1` 携带梯度,in-place 掩码写触发 backward 错 | held | maybe |
| group_cat #9766 | **yes** | none(形状/dim) | **yes(实证)** | 599fce93 / 353ab90a | `dim` 参数被忽略,恒按 dim=0 拼接 | held | maybe |
| scatter jit-trace #7350 | yes(compat) | none | no(数值无关) | 06a86f6d / 09739349 | torch.jit.trace 兼容守卫,数值与原版一致 | held | no |

**B 路径结论:无一命中 set_M/rho_train_inf/rho_mono;6 条对应不变性/幂等 MR 一律 held**——reduce-模式/dtype/越界/梯度/dim/jit 类 bug 本就不破坏「置换后等价」,强行说能检出即造假。

---

## 2. 复现保真度限制(诚实硬约束)

历史 bug 需**时代环境**,当前 `torch 2.12.1+cpu` 上:
- **e3nn #296**:旧 e3nn@6fc34a9(2021)`import e3nn` 即失败 —— `_pickle.UnpicklingError: Weights only load failed`(torch 2.6+ 改 `weights_only` 默认 True)。直接 import infeasible;需 per-bug 绕过/降 torch(属 STEP 3a「per-bug isolated env」)。
- **scatter_argmax #7495**:`reduce='max'` 在 torch 2.12 已被接受且等价于 `'amax'`(实证 pre/post 输出相同)→ **历史 bug 在当前 torch 根本不复现**。

---

## 3. 对 B1 与论文的意义(关键)

1. **真实库 bug 分布的对称性覆盖极窄**:机械采样 0 命中,专搜等变性仅得 1 条「表示等价」真 bug(且当前 infeasible),专搜 scatter 0 命中。真实 bug 主要落在 JIT/编译/类型/device/梯度/数据维度,**不在 NOETHER MR 可感知的对称性维度**。
2. **直接印证 Invariance-Blindness Theorem**:算法导出的 MR 只检出「破坏其所利用结构」的 fault;真实 bug 大多不破坏这些结构 → MR `held`(盲)。本审计「机械全量 0 命中」因不挑选而**天然防 cherry-pick**,是 IBT 的有力实证。
3. **当前 B1 不可投跑完整 confirmatory**:无足够 cat-(i)–(iv) 真 bug 正样本(可入条目仅 e3nn #296,且当前环境复现 infeasible);PyG 实证可复现的 3 条 cat=none、MR 必 held,入 ledger 只会得到 trivial all-held。

---

## 4. 建议下一步(供作者定夺)

- **(i) 作为 IBT 实证写入论文**:把「机械采样真实 bug 中对称性破坏类极少 → MR 覆盖窄」诚实呈现,支持 IBT,并如实标注 B1 real-bug 腿的可行性边界。
- **(ii) 扩采样 + per-bug 时代环境**(数天工程):回溯更早、专搜 `equivariance/wigner/scatter/permutation/transpose` 关键词的 issue,逐 bug 重建 PR 时代 torch/库环境复现。须在论文区分「机械最近窗口」与「关键词回溯」两种采样,避免 cherry-pick 嫌疑。
- **(iii) 重定义 cat 与 MR 适用域**:若把 #296「表示等价不变性」纳入 Set N 的可执行 MR(当前 mr_sets 无此 MR),需作者方法决策(属新 MR,不能为某 bug 现写)。

---

## 5. 可信度声明

- 所有 fix_commit / parent 均由本地 `git show -s --format=%P` 实证;PyG #7407/#7412/#9766 在 `torch 2.12.1+cpu` 实际运行复现。
- GitHub issue 评论线程因 JS 渲染 WebFetch 抓不全:#420 的「not-a-bug」依赖 WebSearch 摘要 + 本地代码/CHANGELOG 旁证;#352 的官方 closing 方式未逐字取证(已据本地 git diff 最保守判定 fix=NOT-FOUND)。
- 本审计**未跑 MR set**(无合格 ledger);`analyze_b1.py`(STEP 4 分析器)已就绪并合成自测通过,待合格 ledger + 复现产出 `results/bug_*.json` 后执行。
