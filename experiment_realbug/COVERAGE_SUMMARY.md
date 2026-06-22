# B1 论文 SUT 域真缺陷覆盖总结 (2026-06-22)

> real-bug in-the-wild 佐证,**对齐论文 SUT 域**(subject_catalog.csv:reactor_physics / pde_numerical / quantum_chemistry / pde_sciml)。
> 分类基准 = `UNIFIED_BLOCK_MODEL.md`:**5 个顶层元模式(最小代数基生成元 $G,T^*,\mathcal T^*_{\mathrm{rev}},O_{\le},\mathcal L^*$)→ 10 个派生 MR 族(a–j)**。
> 多数 pip / conda released-to-released 复现(pre FIRED / post HELD 自跑核验);2 个 unreleased-fix(scipy complexsym、openmc rotperiodic)经源码编译 pre/post 闭合。

## 1. 论文 SUT 域 in-scope 正样本(n=20,pip + conda + 源码编译核验;含 2 个 caveated:#17 fht a 边际、#20 forward-mode Hessian c reachability)

| # | 域 | 库 | bug | MR 族 (Mode) | pre→post | FIRED 类型 |
|---|---|---|---|---|---|---|
| 1 | pde_numerical | scipy.integrate.solve_ivp | LSODA dense-output 自洽 (c374ca7fd) | h L\*·conv (I) | 1.11.4→1.12.0 | crash(事件求根) |
| 2 | pde_numerical | scipy.integrate.ode | banded vs full Jacobian (cb0538877) | **j L\*·rep (M)** | 1.15.3→1.16.3 | crash(维度) |
| 3 | pde_numerical | scipy.linalg.eigh | driver-invariance (178a12572) | c T\*·sa (M) | 1.13.0→1.13.1 | crash(lwork) |
| 4 | pde_numerical | scipy.linalg.solve+inv | complex-symmetric A==A^T (50951d25c/#24359) | c T\*·sa (M) | 1.18.0.dev0+git20260120.d292d32→1.18.0.dev0+git20260121.50951d2 (源码编译 meson) | **数值**(max\|X@a-I\|=9.11) |
| 5 | quantum_chemistry | pyscf.scf.addons.smearing | 电子数守恒 (ebf4e676/#2290) | b G·cons (I) | 2.6.2→2.7.0 | **数值**(14 vs 13) |
| 6 | quantum_chemistry | pyscf.scf.diis+hf_symm | 对称自适应 DIIS 收敛 (15920e60/#1638) | h L\*·conv (I) | 2.2.0→2.2.1 | 收敛/自洽(0/5→5/5) |
| 7 | reactor_physics | openmc.Surface.normalize | 几何对称规范 (3bf1486f4/#3270) | a G·eqv (I) | 0.15.0→0.15.3 | **数值**(符号丢失) |
| 8 | reactor_physics | openmc tally no_reduce (MPI) | MPI 归约方法不变 (bd76fc056/#3619) | **j L\*·rep (M)** | 0.15.2→0.15.3 | **数值**(偏 1/n_ranks=0.5) |
| 9 | reactor_physics | openmc.RotationalPeriodicBC | 旋转周期对称 (c7d7fa461/gh-3692) | a G·eqv (I) | 0.15.4-dev30→0.15.4-dev31 (源码编译) | transport(丢粒子) |
| 10 | pde_sciml | DeepXDE NeumannBC/RobinBC (第三方) | 通量/守恒边界 (4bac5eb) | b G·cons (I) | v1.3.0→v1.3.1 | crash(残差不可构造) |
| 11 | pde_sciml | DeepXDE GeometryXTime.periodic_point (第三方) | 周期/平移对称 (8353540) | a G·eqv (I) | v0.8.6→v0.9.0 | crash(对称映射不可构造) |
| 12 | quantum_chemistry | pyscf.symm.geom + scf.hf_symm | D2h 轴向 orbsym 朝向依赖 (4542fe9b/#3176) | a G·eqv (I) | 2.12.1→2.13.0 | **数值/标签**(6 朝向→6 个 orbsym,1/6 对) |
| 13 | pde_numerical | scipy.interpolate.Akima1DInterpolator | 两点须为线性弦 (ef7437afc/#22278) | f O≤·stat (I) | 1.15.2→1.16.0 | **数值/crash**(I(0.5)=1.25≠1.0 或非有限) |
| 14 | reactor_physics | openmc IFP adjoint-weighted kinetics | 伴随权重朝向不变 (767db7e6a/#3580) | d T\*·dual (M) | 66e7d863→767db7e6a (源码编译) | **数值**(beta_eff 687.4→498.7 pcm) |
| 15 | pde_sciml | DeepXDE PDE.train_next_batch (第三方) | 固定 collocation 集收敛 (4adcde7) | h L\*·conv (I) | v0.5.0→v0.5.1 | 收敛(5→0 重采样) |
| 16 | reactor_physics | openmc depletion/burnup (CRAM) | 数密度非负 clip (1f7ac4215) | f O≤·stat (I) | a1df5842e→1f7ac4215 (源码编译) | **数值**(min N=−5.8e-2<0→0) |
| 17 | pde_numerical | scipy.fft.fht | rfft/irfft Hermitian 保持 (170f9e69a/gh-21661) | a G·eqv (I,**边际**) | 1.14.1→1.15.0 | **数值/边际**(scipy 自带 test_gh_21661,奇 n 7.288e16≥阈 vs 7.225e16<阈) |
| 18 | reactor_physics | openmc tally trigger | 收敛触发器 score 绑定 (b54de4d76/#3155) | h L\*·conv (I) | 0.15.0→0.15.3 (conda) | crash(score 名往返失败→收敛环不可建立) |
| 19 | pde_sciml | DeepXDE DirichletBC/geometry (第三方) | float32 边界点检测 (8a644fe/#1267) | f O≤·stat (I) | 1.8.4→1.9.0 | **数值**(边界点 x≈0 漏判→丢点) |
| 20 | pde_sciml | DeepXDE forward-mode Hessian (第三方) | 算子自伴 H[i,j]=H[j,i] (46e2c2e/#1591) | c T\*·sa (I,**△ reachability**) | 9d9d0b0→46e2c2e (源码编译) | **数值**(J-col 误差 6.185→0;forward-mode 非默认路径) |

## 2. MR 族 × 论文 SUT 域覆盖矩阵(pip / conda / 源码编译可复现)

| 元模式 | MR 族 (Mode) | scipy (pde_numerical) | pyscf (quantum_chemistry) | openmc (reactor_physics) | DeepXDE (pde_sciml) |
|---|---|---|---|---|---|
| $\mathfrak M_G$ | a G·eqv (I) | △ fht Hermitian(谱,边际;170f9e69a) | ✓ D2h 轴向 orbsym(4542fe9b/#3176) | ✓ Surface.normalize(3bf1486f4)、✓ RotationalPeriodicBC(c7d7fa461,源码编译) | ✓ periodic_point(8353540) |
| | b G·cons (I) | — | ✓ smearing 电子数(ebf4e676/#2290) | — | ✓ Neumann/Robin flux(4bac5eb) |
| $\mathfrak M_{T^*}$ | c T\*·sa (I/M) | ✓ eigh driver(178a12572)、✓ complex-symmetric solve/inv(50951d25c,源码编译) | ✗ Fock-Hermitian **构造保证**(仅 int-DM 边界) | — | △ forward-mode Hessian H[i,j]=H[j,i](46e2c2e/#1591,源码编译;非 public 默认路径,reachability caveat) |
| | d T\*·dual (M) | — | — | ✓ IFP 伴随权重(767db7e6a/#3580,源码编译;beta_eff 687.4→498.7 pcm) | — |
| $\mathfrak M_{\mathcal T^*_{\mathrm{rev}}}$ | e Trev·rec (I) | ✗ neg(无 symplectic 积分器) | ✗ neg(rt-TDDFT 已移出主仓;BOMD Verlet 构造可逆) | ✗ neg(无可逆动力学基底) | ✗ neg(无时间步进积分器) |
| $\mathfrak M_{O_{\le}}$ | f O≤·stat (I) | ✓ Akima 两点线性(ef7437afc/#22278) | ✗ **构造保证**(占据/密度/变分界由构造钳制) | ✓ CRAM 负密度 clip(1f7ac4215,源码编译;min N=−5.8e-2→0) | ✓ float32 边界检测(8a644fe/#1267) |
| | g O≤·dyn=𝒟\* (I) | **gap** | **gap** | **gap** | **gap** |
| $\mathfrak M_{\mathcal L^*}$ | h L\*·conv (I) | ✓ LSODA dense-output(c374ca7fd) | ✓ DIIS(15920e60;numpy<1.24+scipy<1.10+h5py<3.9 解依赖) | ✓ tally trigger 收敛准则(b54de4d76/#3155,conda) | ✓ train_next_batch 固定 collocation(4adcde7) |
| | i L\*·acc=ℰ\* (M) | **gap** | **gap** | **gap** | **gap** |
| | j L\*·rep (M) | ✓ banded==full 存储(cb0538877) | — | ✓ no_reduce==reduce(bd76fc056,conda+MPI) | — |

**读出**:5 元模式中 4 个有 in-the-wild 正例($G/T^*/O_{\le}/\mathcal L^*$);$\mathcal T^*_{\mathrm{rev}}$ 四域全负(仅可导出 + mutant 见证)。10 族中 **7 族有正例**(a,b,c,d,f,h,j)、**1 族结构性负**(e Trev)、**2 族 gap**(g 𝒟\* 形状、i ℰ\* 精度阶)。

## 3. 诚实负结果与 caveat(同等重要)

- **$\mathcal T^*_{\mathrm{rev}}$(e Trev·rec)全四域确认结构性稀缺**:Trev\* 是唯一在全部论文 SUT 域均为负结果的元模式——四域核心都不是可逆动力学模拟器。
  - scipy:无 symplectic/leapfrog/Verlet 积分器(`git log` 全空);唯一 backward 候选 d620670a5(2018, v1.2.0)为 first_step 启发式 ENH+BUG,非可逆性不变量违反。
  - openmc:Monte Carlo 求稳态/本征(无可逆时间步进),depletion 解 Bateman(严格耗散前向 ODE,CRAM);git 考古(`-i -E`)0 命中、源码 grep 0 文件;唯一 adjoint 是 IFP(d 族)非时间可逆。见 NEGATIVE_openmc_trev.md。
  - pyscf:唯一酉传播子 rt-TDDFT(`pyscf.rt`,MMUT)已于 v2.0.0(137c23d3)移出主仓;主仓现存唯一可逆基底 BOMD velocity-Verlet 由构造可逆,实测 H2/RHF forward→反转动量→backward 回到初值 6.66e-16(HELD,无可触发 bug)。见 NEGATIVE_pyscf_trev.md。
  - DeepXDE:**无时间步进积分器**(源码 grep leapfrog/verlet/symplectic/odeint/rk4 = 0 文件),`TimePDE`/`GeometryXTime` 把 t 当配点坐标做全时空残差最小化;其 Hessian 自伴属 c 族(已由 bug_deepxde_forward_hessian 覆盖)。见 NEGATIVE_deepxde_trev.md。
- **pyscf T\*(c)Fock-Hermitian 构造保证**:vanilla float64 RHF 的 Fock 厄米性由构造保证,真实 bug 仅在**非标准 int-DM 输入**(#1114/#1537)触发——边界,非干净 in-scope。
- **pyscf O≤(f)构造保证(负结果,确认)**:占据数/密度/变分界由构造钳制——aufbau 占据恒取 0/2、smearing 为单调有界映射(Fermi-Dirac/Gaussian erfc∈(0,1))、变分 RDM 构造 PSD ⟹ NOON≥0、变分界由 Rayleigh 商保证,故无 numeric clamp/positivity fix 可作 pre→post 复现。git 考古(全历史)逐查 negative-occupation/clip/maximum/positive-semidefinite,命中 8 候选(a140208c 熵项、ebf4e676 守恒已占、a40f48d3/c36be01d raise 守卫、9fc6f993 C 端 shell 索引等)逐一打开 diff 均**非 O≤ 界违反修复**;MP2/CC 微扰 RDM 越界为已知物理性质非软件缺陷。见 NEGATIVE_pyscf_o_le.md。
- **scipy a G·eqv 边际填补(caveated)**:fht rfft/irfft Hermitian(170f9e69a/gh-21661, 1.14.1→1.15.0)是真实上游 fix + scipy 自带回归测试 test_gh_21661——pre 未守 `if n%2==0` 无条件 `u.imag[-1]=0`,奇 n=129 破坏非 Nyquist 系数。但信号 edge-dominated:rel-err ~7.2e16,pre 7.288e16≥阈 vs post 7.225e16<阈,偶 n 控制位相同。真实但**数值边际**,标 △;scipy a 的干净 order-of-magnitude 候选仍稀缺。
- **DeepXDE c T\*·sa reachability(caveated)**:forward-mode Hessian H[i,j]=H[j,i](46e2c2e/#1591,源码编译 9d9d0b0→46e2c2e)是真实 forward-mode Jacobian 索引 bug(返回第 0 列→Hessian 非对称,J-col 误差 6.185→0)。但 pre/post 两 commit 的 `gradients/__init__.py` 默认走 reverse-mode、forward-mode import 被注释,缺陷未进 public 默认路径 released tag(须显式 import),标 △ reachability;reverse-mode Hessian 对称由 autodiff 构造保证。
- **scipy f O≤·stat 已升级 in-the-wild**:Akima 两点线性(ef7437afc/#22278, 1.15.2→1.16.0)是干净 pip 可复现 shape-preservation bug——2 单调点的保形插值须为线性弦,pre 因 `np.empty` 未初始化斜率返回 I(0.5)=1.25≠1.0 或非有限崩溃。区别于先前排除的 overflow 边界(9930630d6)。
- **pyscf a G·eqv 已填补 in-the-wild**:D2h 轴向 orbsym(4542fe9b/#3176, 2.12.1→2.13.0)是现代 pip 可复现点群 bug——乙烯 STO-3G RHF 的 MO irrep 标签随输入朝向变化(6 朝向→6 个 orbsym,1/6 对),违反"分子点群 ⟹ irrep 标签朝向不变"。2.12+ 无 numpy<2 约束。
- **pyscf 老版本 pip 依赖**(已解决):2.2.x 与现代 numpy/scipy 冲突,Python 3.10 上 pin numpy<1.24 + scipy<1.10 + h5py<3.9 解依赖,h L\* DIIS(15920e60)已干净 pip released-to-released 复现(0/5→5/5)。
- **reactor_physics(OpenMC)无 PyPI**:需 conda + 核数据(Tier-C);未 release 的 RotationalPeriodicBC fix(c7d7fa461)无 conda post-binary,经源码编译(parent 818fd11b1 → fix,cmake+ninja Release,multi-group XS)闭合。
- **scipy c complex-symmetric**:fix(50951d25c)在 1.18.0.dev0 dev-window,无 released wheel,经 scipy meson editable build(py3.12 + openblas)源码编译闭合。
- **DeepXDE TF1 默认 backend 绕开**:periodic_point(8353540)纯 numpy 几何映射、Neumann/Robin flux(4bac5eb)PyTorch backend 复现,均不触发 2020-era TF1 安装障碍,pip CPU 毫秒级复现。

## 4. 浮现的覆盖规律(论文应呈现的核心结构)

| 不变性来源 | 例子 | 真实可复现 bug |
|---|---|---|
| **数值算法**(非构造保证) | scipy h(L\*·conv)/c(T\*·sa)、各域 a/f/j | **富集** |
| **构造保证**(Hermitian/有界/可逆) | pyscf c(Fock-Herm)+ f(占据/变分)、Trev\* 全域、e3nn SO(3) | **稀缺**(构造钳制,真实 bug 仅边界输入或不可达) |
| **守恒律/计数**(b G·cons) | pyscf 电子数 smearing、deepxde 质量 flux | **有真实数值 bug** |

**关键洞察**:同一个 PySCF,**构造保证的两族**(c T\*·sa Fock-Hermitian、f O≤·stat 占据/变分界)真实 bug 稀缺,而**非构造保证的三族**(b G·cons smearing、h L\*·conv DIIS、a G·eqv D2h orbsym)各有真实数值 bug。这个域内不对称(构造钳制⟹稀缺 vs 数值算法⟹富集)正是论文该诚实呈现的 coverage 精细结构。

## 5. 跨域补充(geometric DL,**非论文 SUT 域**,标注隔离)

e3nn/pyg(domain 字段标 cross-domain):Sₙ 置换(#6199,a 族)、adjoint 反对称(e3nn ReducedTensorProducts,c 族)、adjoint 对称化(pyg to_undirected,c 族)、确定性根因(from_networkx)。证元模式跨域泛化,但不混入论文 SUT 域主结果。

## 6. FIRED 类型的诚实区分

- 论文 SUT 域 20 个中,**6 个 crash-type**(3 scipy lsoda/banded/eigh + 2 DeepXDE neumann/periodic + openmc keff_trigger fatal_error,follow-up 合法输入崩溃 → 违反 MR 关系),**11 个纯数值违反**(scipy complexsym max\|X@a-I\|=9.11、scipy akima I(0.5)=1.25≠1.0、scipy fht 奇 n 7.288e16 边际、pyscf smearing 14 vs 13、pyscf D2h orbsym 1/6 对、openmc normalize 符号丢失、openmc no_reduce 偏 1/n_ranks、openmc ifp_adjoint beta_eff 687.4→498.7 pcm、openmc cram_clip min N=−5.8e-2<0、DeepXDE boundary_float32 漏判、DeepXDE forward-mode Hessian J-col 6.185),**2 个收敛/自洽**(pyscf DIIS 0/5→5/5、DeepXDE resample 5→0 重采样),**1 个 transport 失败**(openmc rotperiodic 丢粒子)。
- scipy 真实 bug 多为数值鲁棒性 / 边界 crash;a/c/j 族 MR 通过"合法输入下 follow-up 崩溃"检出它们。

## 7. 样本量诚实标注

n=20 论文 SUT 域 in-scope(+ 3 跨域),**underpowered for α=0.05 confirmatory**(CLAUDE.md C6)。descriptive 证据:MR 族在论文 SUT 域(scipy/pyscf/openmc/DeepXDE)检出真实缺陷,**5 元模式中 4 个($G/T^*/O_{\le}/\mathcal L^*$)有 in-the-wild 正例、覆盖 7/10 族、四域**(pde_numerical/quantum_chemistry/reactor_physics/pde_sciml);2 个 caveated(scipy fht a 信号边际、DeepXDE forward-mode Hessian c 非默认路径 reachability);**1 元模式($\mathcal T^*_{\mathrm{rev}}$ / e 族)全四域结构性负**(四份 NEGATIVE_*_trev 文档);**2 族实证 gap**(g 𝒟\* 形状/Sturm、i ℰ\* 精度阶),须补真实缺陷或显式标注。
