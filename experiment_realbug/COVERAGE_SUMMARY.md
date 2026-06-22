# B1 论文 SUT 域真缺陷覆盖总结 (2026-06-22)

> real-bug in-the-wild 佐证,**对齐论文 SUT 域**(subject_catalog.csv:reactor_physics / pde_numerical / quantum_chemistry / pde_sciml)。
> 多数 pip / conda released-to-released 复现(pre FIRED / post HELD 自跑核验);2 个 unreleased-fix(scipy complexsym、openmc rotperiodic)经源码编译 pre/post 闭合。

## 1. 论文 SUT 域 in-scope 正样本(n=13,pip + conda + 源码编译核验)

| # | 域 | 库 | bug | NOETHER 块 | pre→post | FIRED 类型 |
|---|---|---|---|---|---|---|
| 1 | pde_numerical | scipy.integrate.solve_ivp | LSODA dense-output 自洽 (c374ca7fd) | L\* 收敛 | 1.11.4→1.12.0 | crash(事件求根) |
| 2 | pde_numerical | scipy.integrate.ode | banded Jacobian (cb0538877) | 守恒/表示不变 | 1.15.3→1.16.3 | crash(维度) |
| 3 | pde_numerical | scipy.linalg.eigh | driver-invariance (178a12572) | T\* 自伴 | 1.13.0→1.13.1 | crash(lwork) |
| 4 | pde_numerical | scipy.linalg.solve+inv | complex-symmetric A==A^T (50951d25c/#24359) | T\* 自伴/对称结构 | 1.18.0.dev0+git20260120.d292d32→1.18.0.dev0+git20260121.50951d2 (源码编译 meson) | **数值**(max\|X@a-I\|=9.11) |
| 5 | quantum_chemistry | pyscf.scf.addons.smearing | 电子数守恒 (ebf4e676/#2290) | 守恒(Noether) | 2.6.2→2.7.0 | **数值**(14 vs 13) |
| 6 | quantum_chemistry | pyscf.scf.diis+hf_symm | 对称自适应 DIIS 收敛 (15920e60/#1638) | L\* 收敛 | 2.2.0→2.2.1 | 收敛/自洽(0/5→5/5) |
| 7 | reactor_physics | openmc.Surface.normalize | 几何对称规范 (3bf1486f4/#3270) | G 对称 | 0.15.0→0.15.3 | **数值**(符号丢失) |
| 8 | reactor_physics | openmc tally no_reduce (MPI) | 归一化 (bd76fc056/#3619) | 守恒/方法不变 | 0.15.2→0.15.3 | **数值**(偏 1/n_ranks=0.5) |
| 9 | reactor_physics | openmc.RotationalPeriodicBC | 旋转周期对称 (c7d7fa461/gh-3692) | G 对称(旋转) | 0.15.4-dev30→0.15.4-dev31 (源码编译) | transport(丢粒子) |
| 10 | pde_sciml | DeepXDE NeumannBC/RobinBC (第三方) | 通量/守恒边界 (4bac5eb) | 守恒/flux | v1.3.0→v1.3.1 | crash(残差不可构造) |
| 11 | pde_sciml | DeepXDE GeometryXTime.periodic_point (第三方) | 周期/平移对称 (8353540) | G 对称 | v0.8.6→v0.9.0 | crash(对称映射不可构造) |
| 12 | quantum_chemistry | pyscf.symm.geom + scf.hf_symm | D2h 轴向 orbsym 朝向依赖 (4542fe9b/#3176) | G 对称(点群) | 2.12.1→2.13.0 | **数值/标签**(6 朝向→6 个 orbsym,1/6 对) |
| 13 | pde_numerical | scipy.interpolate.Akima1DInterpolator | 两点须为线性弦 (ef7437afc/#22278) | O≤ 单调/线性 | 1.15.2→1.16.0 | **数值/crash**(I(0.5)=1.25≠1.0 或非有限) |

## 2. NOETHER 块 × 论文 SUT 域覆盖矩阵(pip / conda / 源码编译可复现)

| 块 | scipy (pde_numerical) | pyscf (quantum_chemistry) | openmc (reactor_physics) | DeepXDE (pde_sciml) |
|---|---|---|---|---|
| L\* 收敛 | ✓ LSODA dense-output | ✓ DIIS(15920e60, 2.2.0→2.2.1;numpy<1.24+scipy<1.10+h5py<3.9 解依赖) | 未探索 | — |
| 守恒 | ✓ banded Jacobian | ✓ smearing 电子数 | ✓ tally-norm no_reduce (bd76fc056, 0.15.2→0.15.3 conda+MPI) | ✓ Neumann/Robin flux (4bac5eb, 1.3.0→1.3.1) |
| T\* 自伴 | ✓ eigh driver(178a12572)、✓ complex-symmetric solve/inv(50951d25c,源码编译 meson) | ✗ Fock-Hermitian **构造保证**(仅 int-DM 边界) | 未探索 | — |
| G 对称 | ✗ 稀缺(fft array-API dev-regression) | **✓ D2h 轴向 orbsym(4542fe9b/#3176, 2.12.1→2.13.0;乙烯 STO-3G RHF,6 朝向 6 个不同 orbsym→1 个)** | **✓ Surface.normalize (3bf1486f4, 0.15.0→0.15.3)**、✓ RotationalPeriodicBC(c7d7fa461,源码编译 0.15.4-dev30→dev31) | ✓ periodic_point(8353540, 0.8.6→0.9.0) |
| O≤ 单调/线性 | **✓ Akima 两点线性(ef7437afc/#22278, 1.15.2→1.16.0;2 点 shape-preserving 须为线性弦,pre I(0.5)=1.25≠1.0 或非有限崩溃)** | — | 未探索 | — |
| Trev\* 时间反演 | ✗ 未找到 pip 可复现候选(已确认稀缺:scipy 无 symplectic/leapfrog 积分器;唯一 backward 候选 d620670a5 为 2018 v1.2.0 first_step ENH+BUG,非可逆性不变量违反) | — | 未探索 | — |

## 3. 诚实负结果与 caveat(同等重要)

- **scipy Trev\* 稀缺(确认)**:scipy 无 symplectic/leapfrog/Verlet 积分器(`git log` symplectic/leapfrog/verlet/stormer 全空),故"结构保持可逆积分"基底缺失;唯一 backward-time 候选 d620670a5(2018, v1.2.0)为 first_step 启发式 ENH+BUG,非 forward→reverse→初值 可逆性不变量违反,且太老难 py3.11 pip。Trev\* 在 scipy 中真实稀缺,诚实记录为负结果。
- **scipy O≤ 已升级 in-the-wild**:Akima 两点线性(ef7437afc/#22278, 1.15.2→1.16.0)是干净 pip 可复现 shape-preservation bug——2 个单调点的 shape-preserving 插值须为线性弦,pre 因 `np.empty` 未初始化斜率缓冲返回 I(0.5)=1.25≠1.0 或非有限崩溃。区别于先前排除的 overflow 边界(9930630d6)。isotonic_regression 仍仅 ENH 无 bug。
- **pyscf G 已填补 in-the-wild**:D2h 轴向 orbsym(4542fe9b/#3176, 2.12.1→2.13.0)是现代 pip 可复现点群 bug——乙烯 STO-3G RHF 的 MO irrep 标签随输入朝向变化(6 朝向→6 个 orbsym,1/6 对参考),违反"分子点群 ⟹ irrep 标签朝向不变"。先前"点群 v1.4.3 太老"的 caveat 已解决:2.12+ 无 numpy<2 约束。
- **pyscf T\* Fock-Hermitian 构造保证**:vanilla float64 RHF 的 Fock 厄米性由构造保证,真实 bug 仅在**非标准 int-DM 输入**(#1114/#1537)触发——边界,非干净 in-scope。
- **pyscf 老版本 pip 依赖**(已解决):2.2.x 与现代 numpy/scipy 冲突,通过 Python 3.10 上 pin numpy<1.24 + scipy<1.10 + h5py<3.9 解依赖,L\* DIIS(15920e60)已干净 pip released-to-released 复现(0/5→5/5 收敛)。
- **reactor_physics(OpenMC/OpenMOC)无 PyPI**:需 conda + 核数据(Tier-C 重运行时);未 release 的 RotationalPeriodicBC fix(c7d7fa461)无 conda post-binary,已通过源码编译(parent 818fd11b1 → fix c7d7fa461,cmake+ninja Release,multi-group XS)闭合。
- **scipy complex-symmetric T\***:fix(50951d25c)在 1.18.0.dev0 dev-window,无 released wheel,已通过 scipy meson editable build(py3.12 + openblas)源码编译闭合(pre/post)。
- **DeepXDE TF1 默认 backend 绕开**:periodic_point(8353540)为纯 numpy 几何映射、Neumann/Robin flux(4bac5eb)在 PyTorch backend 复现,均不触发 2020-era 的 TF1-默认安装障碍,pip released-to-released CPU 毫秒级复现。

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

- 论文 SUT 域 11 个中,**5 个 crash-type**(3 scipy lsoda/banded/eigh + 2 DeepXDE neumann/periodic,follow-up 在合法输入崩溃 → 违反 MR 不变性关系),**4 个纯数值违反**(scipy complexsym max\|X@a-I\|=9.11、pyscf smearing 14 vs 13、openmc normalize 符号丢失、openmc no_reduce 偏 1/n_ranks),**1 个收敛/自洽**(pyscf DIIS 0/5→5/5),**1 个 transport 失败**(openmc rotperiodic 丢粒子)。
- scipy 真实 bug 多为数值鲁棒性 / 边界 crash;NOETHER 的表示不变性 / 方法对比 / 自洽 MR 通过"合法输入下 follow-up 崩溃"检出它们。

## 7. 样本量诚实标注

n=13 论文 SUT 域 in-scope(+ 3 跨域),**underpowered for α=0.05 confirmatory**(CLAUDE.md C6)。descriptive 证据:NOETHER 块 MR 在论文 SUT 域(scipy/pyscf/openmc/DeepXDE)检出真实缺陷,覆盖 **L\*/守恒/T\*/G/O≤ 五块、四域**(pde_numerical/quantum_chemistry/reactor_physics/pde_sciml);Trev\* 在 scipy pip 可复现范围真实稀缺(无 symplectic 基底,已确认)。
