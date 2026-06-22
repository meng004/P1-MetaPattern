# B1 论文 SUT 域真缺陷覆盖总结 (2026-06-22)

> real-bug in-the-wild 佐证,**对齐论文 SUT 域**(subject_catalog.csv:reactor_physics / pde_numerical / quantum_chemistry / pde_sciml)。
> 多数 pip / conda released-to-released 复现(pre FIRED / post HELD 自跑核验);2 个 unreleased-fix(scipy complexsym、openmc rotperiodic)经源码编译 pre/post 闭合。

## 1. 论文 SUT 域 in-scope 正样本(n=20,pip + conda + 源码编译核验;含 2 个 caveated:#17 fht G 边际、#20 forward-mode Hessian T\* reachability)

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
| 14 | reactor_physics | openmc IFP adjoint-weighted kinetics | 伴随权重朝向不变 (767db7e6a/#3580) | T\* 自伴/伴随对偶 | 66e7d863→767db7e6a (源码编译) | **数值**(beta_eff 687.4→498.7 pcm) |
| 15 | pde_sciml | DeepXDE PDE.train_next_batch (第三方) | 固定 collocation 集收敛 (4adcde7) | L\* 收敛 | v0.5.0→v0.5.1 | 收敛/L\*(5→0 重采样) |
| 16 | reactor_physics | openmc depletion/burnup (CRAM) | 数密度非负 clip (1f7ac4215) | O≤ 正性 | a1df5842e→1f7ac4215 (源码编译) | **数值**(min N=−5.8e-2<0→0) |
| 17 | pde_numerical | scipy.fft.fht | rfft/irfft Hermitian 保持 (170f9e69a/gh-21661) | G 对称(**边际**) | 1.14.1→1.15.0 | **数值/边际**(scipy 自带 test_gh_21661,奇 n 7.288e16≥阈 vs 7.225e16<阈) |
| 18 | reactor_physics | openmc tally trigger | 收敛触发器 score 绑定 (b54de4d76/#3155) | L\* 收敛 | 0.15.0→0.15.3 (conda) | crash(score 名往返失败→收敛环不可建立) |
| 19 | pde_sciml | DeepXDE DirichletBC/geometry (第三方) | float32 边界点检测 (8a644fe/#1267) | O≤ 边界/单调 | 1.8.4→1.9.0 | **数值**(边界点 x≈0 漏判→丢点) |
| 20 | pde_sciml | DeepXDE forward-mode Hessian (第三方) | 算子自伴 H[i,j]=H[j,i] (46e2c2e/#1591) | T\* 自伴(**△ reachability**) | 9d9d0b0→46e2c2e (源码编译) | **数值**(J-col 误差 6.185→0;forward-mode 非默认路径) |

## 2. NOETHER 块 × 论文 SUT 域覆盖矩阵(pip / conda / 源码编译可复现)

| 块 | scipy (pde_numerical) | pyscf (quantum_chemistry) | openmc (reactor_physics) | DeepXDE (pde_sciml) |
|---|---|---|---|---|
| L\* 收敛 | ✓ LSODA dense-output | ✓ DIIS(15920e60, 2.2.0→2.2.1;numpy<1.24+scipy<1.10+h5py<3.9 解依赖) | **✓ tally trigger 收敛准则(b54de4d76/#3155, 0.15.0→0.15.3 conda;eigenvalue 触发器绑定 *-production score 崩溃→收敛环不可建立;post fission 触发器 15→40 批至 rel_err<0.01)** | **✓ train_next_batch 固定 collocation(4adcde7, 0.5.0→0.5.1;5→0 重采样)** |
| 守恒 | ✓ banded Jacobian | ✓ smearing 电子数 | ✓ tally-norm no_reduce (bd76fc056, 0.15.2→0.15.3 conda+MPI) | ✓ Neumann/Robin flux (4bac5eb, 1.3.0→1.3.1) |
| T\* 自伴 | ✓ eigh driver(178a12572)、✓ complex-symmetric solve/inv(50951d25c,源码编译 meson) | ✗ Fock-Hermitian **构造保证**(仅 int-DM 边界) | **✓ IFP 伴随权重(767db7e6a/#3580,源码编译 66e7d863→767db7e6a;beta_eff 687.4→498.7 pcm)** | **△ forward-mode Hessian 自伴(46e2c2e/#1591,源码编译 9d9d0b0→46e2c2e;H[i,j]≠H[j,i] J-col 误差 6.185→0;但 forward-mode 在该 commit 未接入 public 默认路径——稀缺,reachability caveat)** |
| G 对称 | **△ fht Hermitian 保持(170f9e69a/gh-21661, 1.14.1→1.15.0;scipy 自带 test_gh_21661,奇 n rel-err 7.288e16≥阈 vs post 7.225e16<阈,偶 n 控制位相同;edge-dominated 信号边际,scipy G 干净候选仍稀缺)** | **✓ D2h 轴向 orbsym(4542fe9b/#3176, 2.12.1→2.13.0;乙烯 STO-3G RHF,6 朝向 6 个不同 orbsym→1 个)** | **✓ Surface.normalize (3bf1486f4, 0.15.0→0.15.3)**、✓ RotationalPeriodicBC(c7d7fa461,源码编译 0.15.4-dev30→dev31) | ✓ periodic_point(8353540, 0.8.6→0.9.0) |
| O≤ 单调/线性 | **✓ Akima 两点线性(ef7437afc/#22278, 1.15.2→1.16.0;2 点 shape-preserving 须为线性弦,pre I(0.5)=1.25≠1.0 或非有限崩溃)** | ✗ **构造保证**(occupation/density/variational 由构造钳制,负结果) | **✓ CRAM 负密度 clip(1f7ac4215, a1df5842e→1f7ac4215 源码编译;depletion/burnup 数密度 min N=−5.8e-2<0,post Integrator.integrate 加 r.clip(min=0)→0)** | **✓ float32 边界检测(8a644fe/#1267, 1.8.4→1.9.0;Dirichlet 边界点 x≈0 因 np.isclose atol=1e-8 漏判为内部,on_boundary False→True、normal 0→-1、DirichletBC 丢点→保留)** |
| Trev\* 时间反演 | ✗ 未找到 pip 可复现候选(已确认稀缺:scipy 无 symplectic/leapfrog 积分器;唯一 backward 候选 d620670a5 为 2018 v1.2.0 first_step ENH+BUG,非可逆性不变量违反) | — | ✗ 无可逆动力学基底(负结果,git 考古 0 命中,见 NEGATIVE_openmc_trev.md) | — |

## 3. 诚实负结果与 caveat(同等重要)

- **scipy Trev\* 稀缺(确认)**:scipy 无 symplectic/leapfrog/Verlet 积分器(`git log` symplectic/leapfrog/verlet/stormer 全空),故"结构保持可逆积分"基底缺失;唯一 backward-time 候选 d620670a5(2018, v1.2.0)为 first_step 启发式 ENH+BUG,非 forward→reverse→初值 可逆性不变量违反,且太老难 py3.11 pip。Trev\* 在 scipy 中真实稀缺,诚实记录为负结果。
- **scipy O≤ 已升级 in-the-wild**:Akima 两点线性(ef7437afc/#22278, 1.15.2→1.16.0)是干净 pip 可复现 shape-preservation bug——2 个单调点的 shape-preserving 插值须为线性弦,pre 因 `np.empty` 未初始化斜率缓冲返回 I(0.5)=1.25≠1.0 或非有限崩溃。区别于先前排除的 overflow 边界(9930630d6)。isotonic_regression 仍仅 ENH 无 bug。
- **pyscf G 已填补 in-the-wild**:D2h 轴向 orbsym(4542fe9b/#3176, 2.12.1→2.13.0)是现代 pip 可复现点群 bug——乙烯 STO-3G RHF 的 MO irrep 标签随输入朝向变化(6 朝向→6 个 orbsym,1/6 对参考),违反"分子点群 ⟹ irrep 标签朝向不变"。先前"点群 v1.4.3 太老"的 caveat 已解决:2.12+ 无 numpy<2 约束。
- **scipy G 边际填补(caveated)**:fht rfft/irfft Hermitian 保持(170f9e69a/gh-21661, 1.14.1→1.15.0)是真实上游 fix,且为 scipy 自带回归测试 test_gh_21661——pre 1.14.1 未守 `if n%2==0` 无条件 `u.imag[-1]=0`,奇 n=129 破坏非 Nyquist 系数虚部。但信号 edge-dominated:rel-err 在 ~7.2e16 量级,pre 7.288e16≥阈 vs post 7.225e16<阈,偶 n 控制位相同。区分真实但**数值边际**,故矩阵标 △;scipy G 的干净 order-of-magnitude 候选仍稀缺。
- **DeepXDE T\* reachability(caveated)**:forward-mode Hessian 自伴 H[i,j]=H[j,i](46e2c2e/#1591,源码编译 9d9d0b0→46e2c2e)是真实 forward-mode Jacobian 索引 bug(返回第 0 列→Hessian 非对称,J-col 误差 6.185→0)。但 pre/post 两 commit 的 `gradients/__init__.py` 默认走 reverse-mode、forward-mode import 被注释,该缺陷未进 public 默认路径的 released tag(须显式 `from ...gradients_forward import`),故矩阵标 △ reachability;reverse-mode Hessian 对称由 autodiff 构造保证,DeepXDE 算子自伴干净候选稀缺。
- **pyscf T\* Fock-Hermitian 构造保证**:vanilla float64 RHF 的 Fock 厄米性由构造保证,真实 bug 仅在**非标准 int-DM 输入**(#1114/#1537)触发——边界,非干净 in-scope。
- **pyscf O≤ 构造保证(负结果,确认)**:占据数/密度/变分界在 PySCF 中**由构造钳制**——aufbau 占据恒取 0/2、smearing 为单调有界映射(Fermi-Dirac/Gaussian erfc∈(0,1))、变分 RDM 构造 PSD ⟹ NOON≥0、变分界由 Rayleigh 商保证,故无 numeric clamp/positivity fix 可作 pre→post 复现。git 考古(全历史)逐查 negative-occupation/clip/maximum/positive-semidefinite 等关键词,命中的 8 个候选(a140208c 熵项、ebf4e676 守恒已占、a40f48d3/c36be01d raise 守卫、9fc6f993 C 端 shell 索引等)逐一打开 diff 均**非 O≤ 界违反修复**;MP2/CC 微扰 RDM 的 NOON 越界是已知物理性质非软件缺陷,上游无对应 fix。与 Fock-Hermitian T\* 同属构造保证稀缺。详见 `results/NEGATIVE_pyscf_o_le.md`。
- **pyscf 老版本 pip 依赖**(已解决):2.2.x 与现代 numpy/scipy 冲突,通过 Python 3.10 上 pin numpy<1.24 + scipy<1.10 + h5py<3.9 解依赖,L\* DIIS(15920e60)已干净 pip released-to-released 复现(0/5→5/5 收敛)。
- **reactor_physics(OpenMC/OpenMOC)无 PyPI**:需 conda + 核数据(Tier-C 重运行时);未 release 的 RotationalPeriodicBC fix(c7d7fa461)无 conda post-binary,已通过源码编译(parent 818fd11b1 → fix c7d7fa461,cmake+ninja Release,multi-group XS)闭合。
- **scipy complex-symmetric T\***:fix(50951d25c)在 1.18.0.dev0 dev-window,无 released wheel,已通过 scipy meson editable build(py3.12 + openblas)源码编译闭合(pre/post)。
- **DeepXDE TF1 默认 backend 绕开**:periodic_point(8353540)为纯 numpy 几何映射、Neumann/Robin flux(4bac5eb)在 PyTorch backend 复现,均不触发 2020-era 的 TF1-默认安装障碍,pip released-to-released CPU 毫秒级复现。

## 4. 浮现的覆盖规律(论文应呈现的核心结构)

| 不变性来源 | 例子 | 真实可复现 bug |
|---|---|---|
| **数值算法**(非构造保证) | scipy L\*/守恒/T\* | **富集** |
| **构造保证**(Hermitian/等变/有界) | pyscf Fock-Hermitian(T\*)+ 占据/密度/变分界(O≤)、e3nn SO(3) | **稀缺**(构造钳制,真实 bug 仅边界输入) |
| **守恒律/计数**(occupation) | pyscf 电子数 smearing | **有真实数值 bug** |

**关键洞察**:同一个 PySCF,**构造保证的两块**(T\* 自伴 Fock-Hermitian、O≤ 占据/密度/变分界)真实 bug 稀缺,而**非构造保证的三块**(守恒 smearing、L\* DIIS、G D2h orbsym)各有真实数值 bug。这个域内不对称(构造钳制⟹稀缺 vs 数值算法⟹富集)正是论文该诚实呈现的 coverage 精细结构。

## 5. 跨域补充(geometric DL,**非论文 SUT 域**,标注隔离)

e3nn/pyg(domain 字段标 cross-domain):Sₙ 置换(#6199)、adjoint 反对称(e3nn ReducedTensorProducts)、adjoint 对称化(pyg to_undirected)、确定性根因(from_networkx)。证 NOETHER 元模式跨域泛化,但不混入论文 SUT 域主结果。

## 6. FIRED 类型的诚实区分

- 论文 SUT 域 20 个中,**6 个 crash-type**(3 scipy lsoda/banded/eigh + 2 DeepXDE neumann/periodic + openmc keff_trigger fatal_error,follow-up 在合法输入崩溃 → 违反 MR 不变性关系),**11 个纯数值违反**(scipy complexsym max\|X@a-I\|=9.11、scipy akima I(0.5)=1.25≠1.0、scipy fht 奇 n 7.288e16 边际、pyscf smearing 14 vs 13、pyscf D2h orbsym 1/6 对、openmc normalize 符号丢失、openmc no_reduce 偏 1/n_ranks、openmc ifp_adjoint beta_eff 687.4→498.7 pcm、openmc cram_clip min N=−5.8e-2<0、DeepXDE boundary_float32 边界点漏判、DeepXDE forward-mode Hessian J-col 6.185),**2 个收敛/自洽**(pyscf DIIS 0/5→5/5、DeepXDE resample 5→0 重采样),**1 个 transport 失败**(openmc rotperiodic 丢粒子)。
- scipy 真实 bug 多为数值鲁棒性 / 边界 crash;NOETHER 的表示不变性 / 方法对比 / 自洽 MR 通过"合法输入下 follow-up 崩溃"检出它们。

## 7. 样本量诚实标注

n=20 论文 SUT 域 in-scope(+ 3 跨域),**underpowered for α=0.05 confirmatory**(CLAUDE.md C6)。descriptive 证据:NOETHER 块 MR 在论文 SUT 域(scipy/pyscf/openmc/DeepXDE)检出真实缺陷,覆盖 **L\*/守恒/T\*/G/O≤ 五块、四域**(pde_numerical/quantum_chemistry/reactor_physics/pde_sciml);其中 2 个 caveated(scipy fht G 信号边际、DeepXDE forward-mode Hessian T\* 非默认路径 reachability),已诚实标注;Trev\* 在 scipy pip 可复现范围真实稀缺(无 symplectic 基底,已确认)。
