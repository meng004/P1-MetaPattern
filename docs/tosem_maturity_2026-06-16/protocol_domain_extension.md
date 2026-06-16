# NOETHER 扩域实验协议(复用 T2 substrate 化解 G1-a / 部分 G1-b)

> 目标:把"三域中仅 1 域有执行 head-to-head"(G1-a)扩到多域,并用**跨实现差分**取得 NOETHER 当前最缺的"中立 + 真 oracle"证据(部分 G1-b)。
> 原则:仅复用 T2 的**公开第三方 substrate + 变异/检测 harness**,NOETHER **自跑 generation→detection**;不搬 T2 的 selection 结论/k\*/见证表/MR catalog。须引用上游 + cover letter 披露共享基础设施。

## 1. 对应的实证 gap
- **G1-a**(域执行深度 1/3 → 多域):加 ≥3 个已执行的 generation→detection 域。
- **G1-b 部分**(缺中立真缺陷正面证据):用 OpenMC↔OpenMOC 跨实现差分作真 oracle(比注入变异更中立可信)。
- 兼顾 **G1-d**(欠功效):每域 n 提升 + Wilson CI + n<10 诚实标注。

## 2. 复用的 T2 substrate(仅程序与 harness,非结论)
| 复用项 | 路径(T2 仓库) | 性质 |
|---|---|---|
| p1–p10 + PINN PUT 适配器 | `experiments/puts/` | 中立 PUT,故障类标签独立于 MR pattern |
| OpenMC/OpenMOC xeval harness | `scripts/mcmr/metbench_put/run_xeval_study.py` | 跨实现检测平台 |
| qchem RHF 3-SCF substrate | `runs/abd-witness-qchem-*` 关联脚本 | 全新非核算子代数域 |
| kill-matrix schema + 验证器 | `scripts/mcmr/abd_structure.py` | 工程约定(含 mr_meta_pattern 列) |
| committed pin-cell 矩阵 | `data/raw/_metbench_pincell/` | runtime-free 检测数据(免重建 OpenMC) |

## 3. 实验 A — 多域 generation→detection(化解 G1-a)
对 ≥4 个**非 reactor** 域(建议:热传导 p1 / 波动 p2 / Burgers p7 / 量子化学 qchem-RHF):
1. NOETHER 从该域算子代数用 CONSTRUCT-MP **自行导出** MR 集(明示 Theorem 1 推导路径;**不照抄** T2 `mr_catalog.csv`);
2. 注入变异(复用 harness 变异池);
3. 测 detection rate + Wilson 95% CI(per-MR + per-block);
4. (可选)与多-LLM 流水线产出的 LLM-MR 作对比 arm。
- **产出**:域覆盖从 1 → 5+,每域有执行的 detection 数据。

## 4. 实验 B — 跨实现差分真 oracle(部分化解 G1-b)
- OpenMC(蒙特卡洛)vs OpenMOC(MOC)求解同一多群中子输运方程;
- NOETHER 从 Boltzmann 算子代数导出 reactor MR;
- 以两独立实现的**真实差分**为 oracle(**非注入变异**):检验 NOETHER MR 能否标记两实现间真实数值/算法差异(离散化、随机 vs 确定收敛);
- **产出**:NOETHER 当前最缺的"中立(非自有目录)+ 真 oracle"reactor 证据,补强 L660 自承的"internal vocabulary coherence, not external transfer"。

## 5. 统计与诚实
- Wilson CI;跨语料 pooled 目标 n≥30;n<10 一律标 underpowered(§6.9);
- **只报 detection / sufficiency(generation 命题);绝不报 k\* / reduction / domination(那是 T2 selection 命题)。**

## 6. self-overlap 防护(硬约束)
- 被测程序引用上游原文(OpenMC / OpenMOC / PySCF / Cantera);
- cover letter **主动披露**与 T2 共享实验基础设施;
- 同一 kill matrix:NOETHER 问"MR 是否充分检出"(generation),T2 问"最小覆盖子集多大"(selection)——问题/结论分离;
- 禁搬 T2 的 MR catalog / 见证表 / k\* / collapse 判定 / 定理(仅 `\cite` 作 companion)。

## 7. 工作量与依赖
- PUT 适配器现成;**MetBench OpenMC runtime 当前 ABSENT,需按 T2 `ENVIRONMENT.md` 重建 conda OpenMC 0.15.3 + ENDF/B-VIII.0**;
- committed pin-cell 矩阵可立即用作 reactor detection 数据(无需重建);
- 主要工作量:NOETHER MR → adapter 桥接 + 每域执行 + 统计。
- **优先级**:实验 A 多域(最高 ROI / 最低风险)> 实验 B 跨实现 oracle(高价值但需重建 runtime)。
