# NOETHER 主场基准候选清单(home-field benchmark candidates)

> 2026-06-16 · 任务:为"NOETHER 方法占优场景"的对比实验**挑选可用 SUT** 并**扩充主场基准候选清单(含热工、流体方程)**。
> 配套文档:`protocol_domain_extension.md`(扩域协议)、`empirical_reuse_from_T2.md`(T2 资产复用评估)、`differentiation_and_disclosure_draft.md`(salami 划界与披露)。
> SUT substrate 来源:姊妹仓库 T2(Minimum-MR-SubSet)`experiments/puts/`、`scripts/mcmr/*/`、`data/raw/`。本清单只复用**被测程序 + 变异/检测 harness**,NOETHER **自跑 generation→detection**;不搬 T2 的 selection 结论(k\*/reduction/collapse/domination)。

---

## 0. 双场对照:为什么需要"NOETHER 主场"

| 维度 | GenMorph 占优场景(S5 pilot + s5-aligned)| NOETHER 占优场景(本清单,扩域)|
|---|---|---|
| 被测对象 | 单方法、标量 I/O 的纯函数(`MathClass.gcd`、`sin`);s5-aligned 锁定 GenMorph 自家 **23-subject 公开基准**(Math10+Lang5+Guava8,~557 mutants,71 条 Set N MR)| 算子代数丰富的 PDE/科学计算求解器(热工、流体、反应流、输运)|
| I/O 形态 | 标量 → 标量 | 场(N×N 数组)、轨迹、本征值 |
| 单次执行成本 | 微秒级 | 一次求解即毫秒–秒级(隐式解 / 谱步 / Monte-Carlo)|
| 对比设计 | **单变量 0-confounder**:固定 JDK8 / Randoop / PIT 1.7.4 / GAssert evaluator / seed=11,仅变 MR 来源(Set N vs Set G)| 同法移植:固定同一 SUT + 同一变异/跨实现 oracle + 同一 evaluator,仅变 MR 来源(见 §2.1)|
| NOETHER 取胜判据 | **生成时间成本** + **初次获得真实 MR 的时间**(代数推导 ~10 min vs GP ~1 h/subject 上游估计)| **MR 产出量 × 结构块覆盖** + **检出率(Wilson CI / McNemar)** + **GenMorph 在此类 SUT 上的可行性退化** |
| GenMorph 状态 | 可运行、每 subject 进化 4 条 MR,但**仅限两执行 (jir,jor) 关系层**(见 §1.D4)| 进化式 assertion 搜索在场值 I/O + 高成本求解上**退化或不可行**(见 §1.D)|

**执行状态(诚实分级)**:S5 pilot(`java_bridge/`,gcd/sin)**已执行**——产出 gcd/sin 的 per-mutant kill 数据 + 生成成本估计(`efficiency_metrics.py`:Set N ~600 s vs Set G ~3600 s,后者为上游 GP 运行时估计)。s5-aligned(23-subject,`supplementary/S5_genmorph_pilot/aligned/`)**设计/代码就绪、`results/` 待执行**——它是化解 reviewer "单一代码库 / 作者自选 SUT / substrate-bias" 的最高 ROI 中立证据(在对手公开基准上**单变量**对比;runbook 见 `s5_aligned_cloud_runbook.md`)。
本清单服务的**对称命题**(NOETHER 主场):*在算子代数丰富的科学计算 SUT 上,NOETHER 按块机械产出大量可证 MR 并填满 ≥4 块,而 GenMorph 的进化搜索因 I/O 维度、求解成本与两执行表达层限制而退化*。两场用**同一套单变量 aligned 方法论**(§2.1)合并 → 覆盖"对手主场 + 本方主场"的完整证据弧。

---

## 1. "主场"判据(home-field selection criteria)

一个 SUT 进入 NOETHER 主场候选,需满足(A)(B)且尽量满足(C)(D):

- **(A) 算子代数丰富**:`\mathcal{D}(\mathcal{A}_P)` 至少 **3 个非空块**(`G / O_{\le} / T^{*} / \mathcal{T}^{*}_{\mathrm{rev}} / \mathcal{L}^{*} / \mathcal{D}^{*} / \mathcal{E}^{*} / \mathcal{B}^{*}_{\mathrm{rel}}`)。守恒律(Noether)/对称/自伴/单调/极限/定性动力学中至少 3 类同时存在。
- **(B) 可执行**:T2 已有可跑 adapter(纯 numpy/scipy 即跑,或 Cantera/PySCF/OpenMC/torch 重运行时)。
- **(C) 跨实现真 oracle 可得**:存在两个独立实现(M-FV vs M-SP / FE vs FV / Cantera vs scipy / OpenMC vs OpenMOC),可用**真实差分**当中立 oracle,而非仅注入变异(化解 G1-b 之"缺中立真缺陷正面证据")。
- **(D) GenMorph 失效面清晰**:能明确说明 GP 进化式 MR 合成为何在该 SUT 退化——
  - **D1 I/O 维度**:GAssert/GP 在标量/小元组 I/O 上进化布尔 assertion;场值(N×N)/轨迹 I/O 无可处理的 assertion 文法。
  - **D2 单次成本**:GP 需数千次 fitness 评估,每次需一整次 PDE 求解 → 时间预算爆炸;NOETHER 代数推导与求解次数解耦(每条 MR 只需 O(1) 次结构化执行)。
  - **D3 多执行变换**:守恒/标度/网格细化/坐标系变换类 MR 需关联**多次**执行(源 vs 跟随),GP 以单次执行的 mutation-kill 适应度无法发现这类关系。
  - **D4 表达层受限(s5-aligned 实证)**:GenMorph 的 GP 进化 MR 天然只活在**两执行 (jir,jor) 关系层**(源→跟随);NOETHER 算子代数同时产出(i)两执行关系(ρ_perm/ρ_scale/ρ_eqref…)、(ii)**单执行不变量**(极大值原理、正定性、`gcd≤min(|p|,|q|)`、`|sin|≤1` 类)、(iii)**多网格/多坐标系结构关系**(Richardson 自收敛、标度律、Galilean)。在 PDE SUT 上,(ii)(iii) 正是检出算子级缺陷的主力,而 GP 的两执行层无法表达——这是**表达空间**差异,独立于 kill-rate(依据 `supplementary/S5_genmorph_pilot/aligned/README.md` §"expressiveness limit":单执行不变量在对齐对比中以 framework-extension 单列)。

---

## 2. 度量设计(对应"通过 X 可证明优势")

NOETHER 主场对比上报以下度量(均为 **generation/detection 命题**,**不**上报 selection 的 k\*/reduction):

| 度量 | 含义 | 偏向方 |
|---|---|---|
| **M-yield** | 每 SUT 可机械导出的非平凡 MR 条数(按块) | NOETHER(按块产出) |
| **M-block** | 8 块中被非空填充的块数(结构覆盖) | NOETHER(可证覆盖) |
| **M-ttf**(time-to-first-real-MR)| 产出首条通过 SUT 原始程序 sanity 的真实 MR 的墙钟 | NOETHER(代数推导近即时;GP 须跑完一轮进化)|
| **M-cost** | 生成整套 MR 的墙钟 / CPU(沿用 S5 `efficiency_metrics.py` 口径;pilot 为上游估计 ~600 s vs ~3600 s)| NOETHER |
| **M-detect** | 注入变异 + 跨实现差分下的检出率 + **Wilson 95% CI** + **paired McNemar p**(配对设计)+ **per-block 分解**;n<10 标 underpowered(§6.9 / CLAUDE.md C6)| 证据点(诚实分级)|
| **M-feasible** | GenMorph 在该 SUT 上能否运行 / 产出非空 MR + 落在哪个表达层(可行性退化的二元/定性记录)| 揭示主场不对称 |

### 2.1 沿用 s5-aligned 的"单变量 0-confounder"方法论(硬约束)

s5-aligned 的金标准设计是:**除 MR 来源外所有混淆变量全部固定**——其早期并行 `java_bridge/` 管线遗留 5 个未控混淆(PIT 版本 / 测试输入 / evaluator / 变异范围 / 变异字节码),aligned 设计用上游原工具链把混淆降为 **0**。NOETHER 主场实验**同法移植**到 PDE SUT:

- **单变量**:同一 SUT、同一注入变异池 / 同一跨实现差分 oracle、同一检测 harness 与 evaluator;唯一变量 = MR 来源(Set N vs 对照 arm,如 LLM-MR / GenMorph 可行时)。
- **中立 oracle 优先**:能用跨实现差分(M-FV vs M-SP / FE vs FV / Cantera vs scipy / OpenMC vs OpenMOC)处即用**真实差分**当 oracle,而非仅注入变异(对应 s5-aligned 复用上游 published mutant set)。
- **对齐验证(alignment gate)**:对照 arm 必须在**未注入**情形复现 SUT 原始程序 sanity(全 MR 通过);若对齐破裂则判"实验不可信"并停(对应 s5-aligned 重跑 Set G 须**精确**复现上游 `mutants_killed.csv`,否则数据不可信)。
- **统计与诚实**:per-subject + **per-block** 分解;配对设计上报 **paired McNemar p** + Wilson 95% CI;n<10 一律标 underpowered;**只报 detection(generation 命题)**,不报 k\* / 最小子集 / domination(T2 selection 命题)。

---

## 3. 候选清单 — 热工(Thermal / 热工)

> ⊕ = 相对原候选(`protocol_domain_extension.md` §3 仅列 热传导 p1 / 波动 p2 / Burgers p7 / qchem)**新增**的热工候选。
> 块符号:`G`=对称, `O≤`=序/单调/线性, `T*`=自伴, `Trev*`=时间反演, `L*`=极限/收敛, `D*`=定性动力学, `E*`=方法对比;`守恒`=Noether 守恒律(质量/能量/元素)。

| SUT | 方程 / 物理 | 数值方法 | NOETHER 非空块 | 跨实现 oracle | 可用性 | GenMorph 失效面 | T2 路径 |
|---|---|---|---|---|---|---|---|
| **P1 heat** | 1D 热传导(抛物)`u_t=αu_xx` | 显式 FDM | `G,O≤,T*,L*,D*`;`Trev*=∅`(不可逆,负 MR 边界)| 单实现(可加隐式 arm)| 纯 numpy,即跑 | D1 场值 u(x);D3 极值原理/标度需多执行 | `experiments/puts/p1_heat.py` |
| ⊕ **P6 Poisson** | 稳态导热 / 泊松(椭圆)`-u''=f` | 3 点中心 FDM(真解)| `O≤,T*,L*,G` | ⊕ FE vs FV(见 fefv)| 纯 numpy,即跑(`solve_poisson_fdm` 带 residual)| D1 场值;D2 线性解需多右端项关联 | `experiments/puts/p6_poisson.py` |
| ⊕ **fefv** | G 群线性扩散-反应(稳态)`-∇·(D∇φ)+σ_aφ-Σσ_sφ=S` | FE / FV 双解器 | `O≤,T*,L*,E*` | **是**(FE vs FV)| 纯 numpy/scipy | D1 多群场;D3 群-叠加需多执行 | `scripts/mcmr/fefv/` |
| ⊕ **advdiff** | 2D 对流-扩散(对流换热的扩散侧)`u_t+c·∇u=α∇²u` | M-FV(CN 隐式 upwind)/ M-SP(谱 ETD)| `G,O≤,L*,E*` + `守恒` | **是**(M-FV vs M-SP)| 纯 numpy/scipy,即跑 | D1 N×N 场;D2 隐式 LU/谱步成本;D3 标度/平移/Galilean/Richardson 全需多执行 | `scripts/mcmr/pde_xeval/`(10-MR battery,见 §5)|
| ⊕ **radxfer** | 多群辐射扩散(热辐射输运,耗散)`(1/c)∂E_g/∂t=∇·(D_g∇E_g)-σ_{a,g}E_g+Σσ_sE+S` | FD-θ / 谱 双解器 | `O≤,T*,L*,E*`;`Trev*=∅` | **是**(FD-θ vs 谱)| 纯 numpy/scipy | D1 G×N×N 场;D3 群耦合/正定性 | `scripts/mcmr/radxfer/` |
| ⊕ **combustion-gri30** | 绝热定容 0-D 反应器(燃烧反应热,GRI-Mech 3.0,53 种 325 反应)| Cantera CVODE / scipy BDF | `O≤,E*` + `守恒`(元素/能量)| **是**(Cantera vs scipy-BDF)| 重运行时(Cantera)| D2 刚性 ODE 积分;非线性 → 无叠加/标度(诚实) | `scripts/mcmr/combustion/` |
| ⊕ **diffusion2D-PINN** | 2D 热扩散(Neumann 零通量)PINN 代理 | 点式 MLP PINN | `守恒`(Neumann 质量), `L*/O≤`(光滑/参考)| 单模型(参考包络)| 重运行时(torch + 子模块)| D1 场代理;GP 无法对 PINN 推断结构 MR | `experiments/diffusion2d_pinn_mrs.py`(5 MR,已读)|

**热工方程小结**(供论文"主场方程"枚举):热传导(抛物)、稳态导热/泊松(椭圆)、多群中子/线性扩散-反应(fefv)、多群辐射扩散(radxfer)、对流-扩散/对流换热(advdiff)、燃烧反应热(combustion)。
反应堆侧的**热工水力**经验锚点见文献语料 `data/raw/_mr_corpus/S3_Zhao2026.json`(HTGR 高温气冷堆:功率-温度单调、流量-温度反单调,正是 `O≤`/`D*` 类热工 MR)。

---

## 4. 候选清单 — 流体(Fluid / 流体)

| SUT | 方程 / 物理 | 数值方法 | NOETHER 非空块 | 跨实现 oracle | 可用性 | GenMorph 失效面 | T2 路径 |
|---|---|---|---|---|---|---|---|
| **P7 Burgers** | 1D 无粘 Burgers 守恒律 `u_t+(u²/2)_x=0` | FVM(通量差分)| `G,O≤,D*` + `守恒`(质量)| 单实现 | 纯 numpy,即跑 | D1 场值 u(x);D3 Galilean/标度需多执行;非线性 → 无叠加 | `experiments/puts/p7_burgers.py` |
| ⊕ **advdiff**(对流侧)| 2D 对流-扩散的**对流**算子 `c·∇u` | M-FV upwind / M-SP 谱 | `G`(Galilean/平移/相位标度), `E*` | **是**(M-FV vs M-SP)| 纯 numpy/scipy | 同 §3 advdiff | `scripts/mcmr/pde_xeval/` |
| ⊕ **cylinder-flow** | 不可压 Navier-Stokes 圆柱绕流(COMSOL 轨迹,速度+压力场,600 步)| MeshGraphNet 代理(训练对照)| `G,D*`(涡脱周期), `E*` + `守恒`(∇·u=0)| 代理 vs 参考轨迹 | 重运行时(图网络 / torch)| D1 非结构网格场;D2 轨迹推演;GP 无文法 | `data/raw/cylinder_flow_deepmind/`, `scripts/mcmr/cylinder_flow/` |
| ⊕ **detonation-znd** | 1D 反应欧拉 / 爆轰(Arrhenius 反应流)| 多通量格式(Rusanov/HLL/Lax)| `O≤`(正定性), `E*`, `D*` + `守恒`(质量/动量/能量)| **是**(多通量差分)| 纯 numpy(反应流)| D1 守恒量场;非线性 → 仅守恒/正定类 MR(诚实)| `scripts/mcmr/detonation/` |
| ⊕ **Burgers2D-PINN** | 2D 粘性 Burgers `ν=0.05` PINN 代理 | 点式 PINN(子模块)| `守恒`, `L*/O≤`(光滑/参考)| 单模型(参考包络)| 重运行时(torch + 子模块)| D1 场代理;GP 无法对 PINN 推断结构 MR | `experiments/puts/p_burgers2d_pinn.py` |
| ⊕ **Gray-Scott / rdscan** | 2D 反应-扩散(图灵斑图 / N 种循环竞争-扩散)| FD-IMEX / 谱 双解器 | `G,D*,E*` + `守恒`(物种/质量)| **是**(FD-IMEX vs 谱)| 纯 numpy/scipy | D1 多物种场;D3 斑图定性不变量;非线性 | `scripts/mcmr/grayscott/`, `scripts/mcmr/rdscan/` |
| **P2 wave**(声学/波动,邻接)| 1D 波动(双曲)`u_tt=c²u_xx` | 蛙跳 FDM | `G,Trev*,D*` + `守恒`(能量)| 单实现 | 纯 numpy,即跑 | D1 场值;D3 能量/时反需多执行 | `experiments/puts/p2_wave.py` |

**流体方程小结**:Burgers(无粘 1D / 粘性 2D)、对流-扩散(advdiff)、不可压 Navier-Stokes(圆柱绕流)、反应欧拉/爆轰(detonation)、反应-扩散输运(Gray-Scott/rdscan)、压力泊松(投影步,见 P6)、波动/声学(P2,邻接)。

> **P2 wave 的独特价值**:它是少数 `\mathcal{T}^{*}_{\mathrm{rev}}` **非空**(波动可逆)的候选,正好与 P1/radxfer 的 `\mathcal{T}^{*}_{\mathrm{rev}}=∅`(耗散不可逆)形成对照——一次性展示 NOETHER 既能在可逆系统产出时反 MR、又能在耗散系统**可证地**判定该块为空(论文"证明自己导不出什么"的卖点)。

---

## 5. 实证锚:advdiff 的 10-MR 代数 battery → NOETHER 块映射

`scripts/mcmr/pde_xeval/mr_battery.py` 已实现的 10 条 MR,**每条都注明"derived from the operator's algebra"**,且全部 **oracle-free**(只比较程序自身多次输出),与 NOETHER 的"从算子代数 Translate 出 MR"叙事逐条同构,可作主场最强单点证据:

| battery MR | derived_from(原码)| NOETHER 块 |
|---|---|---|
| linearity-scale | `L(βu)=βLu` 齐次 | `O≤` |
| superposition | `L(u+v)=Lu+Lv` 可加 | `O≤` |
| translation-inv | 周期平移与算子对易 | `G` |
| reflection-sym | Laplacian 在 x 反射下的宇称 | `G` |
| mass-conservation | 周期域散度定理 `d/dt∫u=0` | `守恒`(Noether)|
| energy-decay | `α>0` 时 `∇²` 耗散 `d/dt‖u‖²≤0` | `O≤ / L*` |
| max-principle | 对流-扩散比较原理 | `O≤` |
| spectral-decay-scaling | 扩散符号齐次 `λ(2k)=4λ(k)` | `G`(标度)|
| phase-scaling | 对流符号线性 `φ(2k)=2φ(k)` | `G` |
| galilean-inv | 动坐标系把对流-扩散约化为纯扩散 | `G` |
| richardson-self | Richardson 自收敛(一致性)| `L*` |
| (M-FV vs M-SP)| 双独立实现差分 | `E*` |

这 10 条 + 跨实现 = 单 SUT 即填满 `G/O≤/L*/E*` 4 块 + 守恒;GP 因 D1/D2/D3 在同一 SUT 上无法企及。

---

## 6. 可用性分级 + 推荐选定子集(挑选可用 SUT)

### 6.1 三级可用性

- **Tier-A 纯 Python 即跑**(numpy/scipy,无重依赖):P1, P2, P6, P7, advdiff, radxfer, fefv, Gray-Scott/rdscan, detonation。
- **Tier-B 跨实现真 oracle**(Tier-A 中自带双解器):advdiff(M-FV/M-SP)、radxfer(FD-θ/谱)、fefv(FE/FV)、Gray-Scott/rdscan(FD-IMEX/谱)、combustion(Cantera/scipy)、detonation(多通量)。
- **Tier-C 重运行时**:combustion(Cantera)、diffusion2D/Burgers2D-PINN(torch+子模块)、cylinder-flow(图网络)。

### 6.2 推荐选定子集(最大化代表性,覆盖 PDE 类型 × 域 × 可用性)

| 选定 SUT | PDE 类型 | 域 | 选入理由 |
|---|---|---|---|
| **P1 heat** | 抛物 | 热工 | 最简热传导;直接对齐论文 `T*` 自伴扩散算子 + `Trev*=∅` |
| **P6 Poisson** | 椭圆 | 热工 | 稳态导热;带 residual 一致性 oracle |
| **advdiff** | 抛物+对流 | 热工×流体 | **跨实现真 oracle** + 已实现 10-MR 代数 battery(最强单点)|
| **P7 Burgers** | 非线性双曲守恒律 | 流体 | 无粘守恒律;Galilean/激波定性动力学 |
| **radxfer** | 多群抛物(耗散)| 热工(辐射)| 多群 + 跨实现;`T*+L*+Trev*=∅` |
| **detonation-znd** | 反应欧拉 | 流体(反应流)| 非线性守恒/正定;多通量跨实现 |
| **P2 wave** | 双曲(可逆)| 流体邻接(声学)| 唯一填充 `Trev*` 非空,与耗散系统对照 |
| **combustion-gri30** | 刚性反应 ODE | 热工×流体(燃烧)| 真实机理 + Cantera/scipy 跨实现(工业现实性)|

> 该 8 选子集:抛物/椭圆/双曲/非线性守恒律/反应流/刚性 ODE 全覆盖;热工 4 + 流体 4(含交叉);Tier-A 6 + Tier-C 2;跨实现真 oracle ≥ 4。化解 G1-a(域执行 1/3 → 多域)与 reviewer 的"作者自选 SUT / substrate selection bias"。

---

## 7. 可提议的扩展方程(暂未在 substrate,future candidate)

为把"热工/流体"覆盖做厚,以下经典方程是自然增量(当前 T2 substrate **尚无**对应 adapter,列为提议,**不得**当作已有证据):

- **热工**:共轭传热(固-流耦合)、自然对流 Boussinesq、瞬态对流换热(Nu-Re-Pr 标度律,`G`+`O≤`)。
- **流体**:可压缩欧拉激波管(Sod,`守恒`+`D*`)、浅水方程(`守恒`+`G` Galilean)、不可压 NS 顶盖驱动方腔(`G`+`D*`)。

提议方程一旦落地为可执行 adapter,按 §1 判据与 §2 度量并入正表。

---

## 8. salami 红线与披露(硬约束)

- ✅ **可复用**:T2 的公开第三方/自建被测程序、PUT adapter 代码、变异 harness、双实现求解器、kill-matrix schema、`_mr_corpus` 文献语料(注明出处)。
- ⛔ **禁搬**:T2 的 k\*/reduction/domination/collapse(R1-R3)judgement、见证 register、A/B/D claim ledger、`_eval` 对 T2-MR 的评分、support-domination/NP-hard/FPT 定理——一律 `\cite` 作 companion。
- **同一 kill matrix 双问题分离**:T2 问"最小完备子集多大"(selection);NOETHER 问"算子代数导出的 MR 是否充分检出"(generation)。矩阵/harness 共享,问题与结论各自独立。
- **scope precondition**:`csmith / sql / dnn` 已被 T2 移出核心(超出算子代数,违反 NOETHER scope 前置)——**不纳入**本主场清单。
- **披露**:同作者群同主题,**必须**在 cover letter 主动披露共享实验基础设施(措辞见 `differentiation_and_disclosure_draft.md`),并引用上游(OpenMC/OpenMOC/PySCF/Cantera/DeepMind cylinder-flow)。

---

## 9. 与 protocol_domain_extension.md 的衔接

- 本清单**扩充** `protocol_domain_extension.md` §3「实验 A — 多域 generation→detection」的候选域:原列(热传导 p1 / 波动 p2 / Burgers p7 / qchem-RHF)→ 扩为本表的热工 6 + 流体 6 候选,并给出 §6.2 的 8 选推荐子集。
- 跨实现真 oracle(§3/§4 标"是"者)直接服务 `protocol_domain_extension.md` §4「实验 B — 跨实现差分真 oracle」,把原仅 OpenMC↔OpenMOC 一例扩到 advdiff/radxfer/fefv/Gray-Scott/combustion/detonation 多例。
- 度量(§2)沿用 S5 `efficiency_metrics.py`(M-cost / M-ttf)+ 新增 M-yield / M-block / M-detect(Wilson CI / McNemar)/ M-feasible。
- **与 s5-aligned 对称**:GenMorph 主场已有 `supplementary/S5_genmorph_pilot/aligned/`(23-subject 单变量 0-confounder;runbook `s5_aligned_cloud_runbook.md`;`results/` 待执行);本主场实验沿用同一 aligned 设计(§2.1),与之构成"对手主场 + 本方主场"的对称证据弧,共同回应 substrate-bias 批评。

---

## 10. 代表性与威胁(threats to validity)

### 10.1 主场清单是"声明在案的主场",非中立集

- 本清单**有意**选 NOETHER 占优场景,**不假装中立**。公正性不来自本清单自身,而来自三重配套:(a) 配对 GenMorph 主场(s5-aligned 的 gcd/sin + 23-subject);(b) 中立第三方基准(s5-aligned 用 GenMorph **自家发表** benchmark);(c) 主张层级——只报 generation/detection + underpowered,不声称 average superiority。
- **过度主张红线**:GenMorph 在这些 SUT 上 D1–D4 退化甚至**不可行**;若对手进不了场,"NOETHER 赢 kill 比拼"半属同义反复。诚实口径 = **NOETHER 适用域 / 表达空间严格更大(M-feasible)**,而非同场 kill 击败。
- **缓解 selection bias**:SUT 来自姊妹论文 T2 既有 substrate(为 *selection* 命题而建,与 *generation* 正交),**非为本论文新造** → 被测对象选择权不在本方;代价是同作者群,须 cover letter 披露(§8)。
- **pre-registration**:§6.2 选定子集与 per-block 假设须在跑 detection **前冻结**,避免 HARKing。

### 10.2 跨实现差分 oracle 的威胁

- **共模故障盲点**:两实现共享同一 bug(同一错边界条件 / 同一底层库)时差分失效 → 故意配**最大算法 gap** 的实现对(MC vs MOC、FV vs 谱、Cantera vs 独立 scipy)压低共享假设;并辅以注入变异补共模。
- **离散差异 ≠ 缺陷**:正常离散误差不得被误记为检出 → 容差**先验**设定(精确线性性质 1e-9;方法相关性质放宽,见 `pde_xeval/mr_battery.py` 容差 rationale),禁事后拟合。
- **差分不指明谁对**:只给"不一致"信号;对"MR 能否标记分歧"的 detection 命题已足够,但**不**据此论断"哪个实现正确"。
- **自洽故障的固有上限**:保持代数性质的全局一致故障(如全局错 α)MT 不可检——如实承认(`pde_xeval/mr_battery.py` 已注),不掩盖。

### 10.3 其余效度

- **外部效度**:物理 SUT 不触及 `\mathcal{B}^{*}_{\mathrm{rel}}`(关系代数块,属查询优化器域);本清单覆盖 `G/O≤/T*/Trev*/L*/D*/E*` 七块,`B_rel*` 由 NOETHER 第三域单独 instantiate,不在本主场。
- **欠功效**:每 SUT n 小 → Wilson CI + paired McNemar + n<10 标 underpowered(§2.1)。

---

> **执行进展**:§6.2 选定子集已扩到 **9 个 SUT**(`supplementary/S10_noether_homefield/`),覆盖热工/流体/反应堆;**只报 generation/detection,不报 selection**(k\*/min-cover/collapse):
>
> | SUT | 域 | 模式 | M-yield | M-block | M-detect | Wilson95 | alignment |
> |---|---|---|---|---|---|---|---|
> | heat-1d | 热工 | exec | 6 | 3 | 5/6 | [.436,.970] | PASS |
> | wave-1d | 流体 | exec | 5 | 4(含 Trev\*) | 6/6 | [.610,1.000] | PASS |
> | poisson-1d | 热工 | exec | 5 | 3 | 5/6 | [.436,.970] | PASS |
> | advdiff-2d | 热工×流体 | exec | 11 | 4 | 13/29 | [.284,.625] | PASS |
> | radxfer-G2 | 热工 | reused | 16 | 4 | 25/31 | [.637,.908] | PASS |
> | grayscott | 流体 | reused | 20 | 4 | 41/44 | [.818,.977] | PASS |
> | detonation-znd | 流体 | reused | 18 | 2 | 12/36 | [.202,.497] | PASS |
> | combustion-gri30 | 热工 | reused | 16 | 2 | 34/54 | [.496,.746] | PASS |
> | pincell-xeval | 反应堆 | reused | 22 | 3 | 24/86 | [.195,.382] | **FAIL** |
>
> - **exec** = 本 harness 执行(heat/wave/poisson 自包含纯 numpy;advdiff 经 T2 substrate);**reused** = 复用 T2 已提交 `kill_matrix.csv` 重算 generation 指标(未重跑;provenance 记录来源;不读其 selection 产物)。
> - **alignment gate 有牙**:pincell-xeval FAIL —— T2 committed 矩阵 3 个 `…-identity` baseline 被判杀(resid 1.0>tol 0.5),其检出率不作可信结论,保留并标注。
> - self-consistent 故障如实未检出(heat/poisson coeff×1.1;advdiff diffusion 0/2、speed 0/3)→ §10.2;**wave 独占 Conservation+Trev\***(耗散 SUT 的 Trev\* 为空)→ 块随物理。
> **后续增量**:跨实现差分逐场 oracle(§10.2 容差校准)、LLM-MR 对比 arm(paired McNemar)、fefv(需补变异池)。
