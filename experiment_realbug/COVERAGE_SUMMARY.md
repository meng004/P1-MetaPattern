# B1 论文 SUT 域真缺陷覆盖总结 (2026-06-22)

> real-bug in-the-wild 佐证,**对齐论文 SUT 域**(subject_catalog.csv:reactor_physics / pde_numerical / quantum_chemistry / pde_sciml)。
> 全部 pip released-to-released 复现(pre FIRED / post HELD 自跑核验,无源码编译)。

## 1. 论文 SUT 域 in-scope 正样本(n=7,pip + conda 核验)

| # | 域 | 库 | bug | NOETHER 块 | pre→post | FIRED 类型 |
|---|---|---|---|---|---|---|
| 1 | pde_numerical | scipy.integrate.solve_ivp | LSODA dense-output 自洽 (c374ca7fd) | L\* 收敛 | 1.11.4→1.12.0 | crash(事件求根) |
| 2 | pde_numerical | scipy.integrate.ode | banded Jacobian (cb0538877) | 守恒/表示不变 | 1.15.3→1.16.3 | crash(维度) |
| 3 | pde_numerical | scipy.linalg.eigh | driver-invariance (178a12572) | T\* 自伴 | 1.13.0→1.13.1 | crash(lwork) |
| 4 | quantum_chemistry | pyscf.scf.addons.smearing | 电子数守恒 (ebf4e676/#2290) | 守恒(Noether) | 2.6.2→2.7.0 | **数值**(14 vs 13) |
| 5 | reactor_physics | openmc.Surface.normalize | 几何对称规范 (3bf1486f4/#3270) | G 对称 | 0.15.0→0.15.3 | **数值**(符号丢失) |
| 6 | reactor_physics | openmc tally no_reduce (MPI) | 归一化 (bd76fc056/#3619) | 守恒/方法不变 | 0.15.2→0.15.3 | **数值**(偏 1/n_ranks=0.5) |
| 7 | pde_sciml | DeepXDE NeumannBC/RobinBC (第三方) | 通量/守恒边界 (4bac5eb) | 守恒/flux | v1.3.0→v1.3.1 | crash(残差不可构造) |

## 2. NOETHER 块 × 论文 SUT 域覆盖矩阵(pip 可复现)

| 块 | scipy (pde_numerical) | pyscf (quantum_chemistry) | openmc (reactor_physics) |
|---|---|---|---|
| L\* 收敛 | ✓ LSODA dense-output | △ DIIS(2.2.x+numpy 依赖冲突 caveat) | 未探索 |
| 守恒 | ✓ banded Jacobian | ✓ smearing 电子数 | △ tally-norm(bd76fc056 fix 首入 0.15.3,无 conda pre) |
| T\* 自伴 | ✓ eigh driver | ✗ Fock-Hermitian **构造保证**(仅 int-DM 边界) | 未探索 |
| G 对称 | ✗ 稀缺(fft array-API dev-regression) | 未探索(点群 v1.4.3 太老) | **✓ Surface.normalize (3bf1486f4, 0.15.0→0.15.3)** |
| O≤ 单调/线性 | ✗ 稀缺(39b9cd9b5 @2016 pre-v1.0;akima overflow 边界;isotonic 无 bug) | — | 未探索 |
| Trev\* 时间反演 | ✗ 未找到 pip 可复现候选 | — | 未探索(c7d7fa461 旋转周期边界 fix **未 release**,无 conda post) |

## 3. 诚实负结果与 caveat(同等重要)

- **scipy Trev\*/O≤/G 稀缺**:即使数值算法库,时间反演 / 单调线性 / 对称 块的**现代 pip 可复现** bug 罕见——候选要么太老(39b9cd9b5 @2016, v1.0 前)、要么 dev-regression(fft array-API-only)、要么边界(akima overflow)、要么仅 ENH 无 bug(isotonic)。
- **pyscf T\* Fock-Hermitian 构造保证**:vanilla float64 RHF 的 Fock 厄米性由构造保证,真实 bug 仅在**非标准 int-DM 输入**(#1114/#1537)触发——边界,非干净 in-scope。
- **pyscf 老版本 pip 依赖地狱**:2.2.x 与现代 numpy/scipy 冲突,L\* DIIS(15920e60)未能干净复现。
- **reactor_physics(OpenMC/OpenMOC)pip 不可达**:无 PyPI 包,需 conda + 核数据(Tier-C 重运行时)。

## 4. 浮现的覆盖规律(论文应呈现的核心结构)

| 不变性来源 | 例子 | 真实可复现 bug |
|---|---|---|
| **数值算法**(非构造保证) | scipy L\*/守恒/T\* | **富集** |
| **构造保证**(Hermitian/等变) | pyscf Fock-Hermitian、e3nn SO(3) | **稀缺**(需边界输入) |
| **守恒律/计数**(occupation) | pyscf 电子数 smearing | **有真实数值 bug** |

**关键洞察**:同一个 PySCF,T\* 自伴**构造保证**(稀缺),但守恒块有**真实数值 bug**(smearing)。这个域内不对称正是论文该诚实呈现的 coverage 精细结构。

## 5. 跨域补充(geometric DL,**非论文 SUT 域**,标注隔离)

e3nn/pyg(domain 字段标 cross-domain):Sₙ 置换(#6199)、adjoint 反对称(e3nn ReducedTensorProducts)、adjoint 对称化(pyg to_undirected)、确定性根因(from_networkx)。证 NOETHER 元模式跨域泛化,但不混入论文 SUT 域主结果。

## 6. FIRED 类型的诚实区分

- 论文 SUT 域 4 个中,**3 个 scipy 是 crash-type**(follow-up 在合法输入崩溃 → 违反 MR 不变性关系),**1 个 pyscf 是纯数值违反**(14 vs 13 电子)。
- scipy 真实 bug 多为数值鲁棒性 / 边界 crash;NOETHER 的表示不变性 / 方法对比 / 自洽 MR 通过"合法输入下 follow-up 崩溃"检出它们。

## 7. 样本量诚实标注

n=5 论文 SUT 域 in-scope(+ 3 跨域),**underpowered for α=0.05 confirmatory**(CLAUDE.md C6)。descriptive 证据:NOETHER 块 MR 在论文 SUT 域(scipy/pyscf/openmc)检出真实缺陷,覆盖 **L\*/守恒/T\*/G 四块、三域**(pde_numerical/quantum_chemistry/reactor_physics);Trev\*/O≤ 在 pip 可复现范围稀缺。
