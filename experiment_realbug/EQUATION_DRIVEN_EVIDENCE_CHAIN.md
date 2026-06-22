# B1 方程驱动证据链:方程代数 → 先验元模式 → SUT 真实缺陷 (2026-06-22)

> **方法论声明**:MR 从**方程的算子代数先验机械导出**(对称/守恒/自伴/序-正性/收敛由群作用、内积、序锥、离散化结构决定),**不为任何缺陷定制**。先对每个 SUT 域的代表方程做**存在性分析**(纯理论,不看缺陷),再用**独立发现的真实库缺陷**作为该先验 MR 被违反的证据。MR 先验存在 ⟹ 缺陷是独立证据,非 circular。
> **分类基准** = `UNIFIED_BLOCK_MODEL.md`:5 元模式($G,T^*,\mathcal T^*_{\mathrm{rev}},O_{\le},\mathcal L^*$)→ 10 MR 族(a–j)。下文证据按族标注 + Mode(I 输入轨道 / M 实现轨道)。

---

## 域 1:pde_numerical — 热传导方程 `u_t = α u_xx`(抛物)

### 1a. 方程角度元模式存在性(算子 `L = α ∂²/∂x²`,先验)
| 元模式 | 先验导出(数学) | 族 | 是否非空 |
|---|---|---|---|
| **$G$** 对称 | 常系数 ⟹ 平移不变、偶 ⟹ 反射(a);Neumann/周期 ⟹ `d/dt∫u=0` 散度定理(b) | a, b | ✓ |
| **$T^*$** 自伴 | `⟨Lu,v⟩=⟨u,Lv⟩`(两次分部积分)⟹ 离散 L 对称、谱实、特征向量正交(c) | c | ✓ |
| **$O_{\le}$** 序/正性 | L 线性 ⟹ superposition;抛物最大值原理 ⟹ 极值在 parabolic boundary(f);无伪振荡(g) | f, g | ✓ |
| **$\mathcal L^*$** 极限 | 一致+稳定 ⟹ 收敛、稠密插值自洽(h);离散算子表示无关(j);精度阶(i) | h, i, j | ✓ |
| **$\mathcal T^*_{\mathrm{rev}}$** 时间反演 | α>0 耗散 ⟹ **不可逆**(e,先验可证为空) | e | **∅(可证)** |

### 1b. SUT 角度证据(scipy.integrate / linalg 实现该算子)
| 族 (Mode) | 先验 MR | 真实缺陷(独立发现) | 违反证据 |
|---|---|---|---|
| h L\*·conv (I) | 稠密插值穿过求解器网格 `sol(t)==y` | scipy c374ca7fd (LSODA dense-output) | pre 1.11.4 FIRED / post 1.12.0 HELD |
| **j L\*·rep (M)** | 同算子不同存储同轨迹 `y_banded==y_full` | scipy cb0538877 (banded Jacobian) | pre 1.15.3 FIRED / post 1.16.3 (\|y_b-y_f\|=0) |
| c T\*·sa (M) | 自伴谱 driver-invariant `σ(d1)==σ(d2)` | scipy 178a12572 (eigh driver) | pre 1.13.0 FIRED / post 1.13.1 HELD |
| c T\*·sa (M) | 对称结构不变 `solve/inv(A,sym)==solve/inv(A)`(A==A^T) | scipy 50951d25c (complex-symmetric, gh-24359) | pre 1.18.0.dev0+git20260120.d292d32 FIRED (max\|X@a-I\|=9.11) / post 1.18.0.dev0+git20260121.50951d2 HELD(源码编译 meson) |
| f O≤·stat (I) | shape-preserving 插值,2 单调点须为线性弦 `I((x0+x1)/2)==(y0+y1)/2` | scipy ef7437afc (Akima 两点线性, gh-22278) | pre 1.15.2 FIRED (I(0.5)=1.25≠1.0,或 `np.empty` 未初始化斜率致非有限崩溃)/ post 1.16.0 HELD (I(0.5)=1.0,max\|I-弦\|=0) |
| a G·eqv (I,**边际**) | 谱方法依赖 rfft/irfft Hermitian 布局,fast Hankel 须对任意 n 保持该对称 | scipy 170f9e69a (fht Hermitian, gh-21661) | pre 1.14.1 FIRED (奇 n=129 rel-err 7.288e16≥scipy 自带 test_gh_21661 阈 7.28e16)/ post 1.15.0 HELD (7.225e16<阈,偶 n 控制位相同);**信号 edge-dominated,数值边际** |

### 1c. 证据链闭合
热方程算子代数**先验**给出 $G/T^*/O_{\le}/\mathcal L^*$(+$\mathcal T^*_{\mathrm{rev}}$=∅);scipy 实现中 **h/j/c/f 四族各有独立真实缺陷**违反对应先验 MR(c 两实例:eigh driver-invariance + complex-symmetric 对称结构;j:banded 表示不变,Mode M),**a 族由谱方法 fht Hermitian 实例边际填补**(scipy 自带 test_gh_21661,信号 edge-dominated 标 △)。scipy 无 b(Noether 守恒)in-the-wild;g(𝒟\* 形状)、i(ℰ\* 精度阶)gap;e(Trev\*)可证为空。**h/j/c/f 完整,a 边际。**

---

## 域 2:quantum_chemistry — RHF Fock 方程 `FC = SCε`

### 2a. 方程角度元模式存在性(Fock 算子 F,先验)
| 元模式 | 先验导出 | 族 | 是否非空 |
|---|---|---|---|
| **$G$** 对称 | 分子点群 ⟹ MO irrep 标签朝向不变(a);`N_elec=tr(PS)` 电子数守恒(b) | a, b | ✓ |
| **$T^*$** 自伴 | `F=F†`(h,J,K 厄米)、`S=S†` ⟹ MO 实正交 `C†SC=I`(c) | c | ✓ |
| **$O_{\le}$** 序/变分 | `0≤n_i≤2`、`ρ≥0`、1-RDM PSD、变分界 `E[Ψ]≥E_0`(f) | f | ✓ |
| **$\mathcal L^*$** 极限 | SCF 不动点迭代收敛(h) | h | ✓ |

### 2b. SUT 角度证据(pyscf 实现)
| 族 (Mode) | 先验 MR | 真实缺陷 | 违反证据 |
|---|---|---|---|
| b G·cons (I) | `sum(occ)=N_elec` | pyscf ebf4e676 (smearing #2290) | pre 2.6.2 FIRED (14≠13) / post 2.7.0 HELD |
| h L\*·conv (I) | 对称自适应 SCF 不动点不受数值噪声影响(收敛+e_tot 确定) | pyscf 15920e60 (DIIS 数值噪声 #1638) | pre 2.2.0 FIRED (0/5 收敛,e_tot 抖动 1.76e-2) / post 2.2.1 HELD (5/5,e_tot=-74.7874921601011) |
| a G·eqv (I,点群) | 分子点群 ⟹ MO irrep 标签朝向不变 `orbsym(perm)==orbsym(ref)` | pyscf 4542fe9b (D2h 轴向 #3176) | pre 2.12.1 FIRED (乙烯 STO-3G RHF,6 朝向 6 个 orbsym,1/6 对)/ post 2.13.0 HELD (6/6 对,1 个 orbsym) |
| c T\*·sa | Fock-Hermitian | 构造保证 ⟹ vanilla 真实 bug 稀缺(仅 int-DM 边界 #1114) | — (诚实负结果) |
| f O≤·stat | 占据/密度/变分界 `0≤n_i≤2`、`ρ≥0`、`E≥E_0` | 构造保证 ⟹ aufbau 钳制 0/2、smearing 单调有界、变分 RDM PSD、Rayleigh 商 | — (诚实负结果,git 考古全历史 8 候选逐一排除,见 `results/NEGATIVE_pyscf_o_le.md`) |

### 2c. 证据链闭合
RHF 先验给出 $G/T^*/O_{\le}/\mathcal L^*$;pyscf **b 守恒族有独立真实缺陷**(smearing,14 vs 13),**h 收敛族亦有独立真实缺陷**(对称自适应 DIIS,0/5→5/5),**a 点群族亦有独立真实缺陷**(D2h 轴向 orbsym,6→1)。**c(Fock-Hermitian)与 f(占据/变分界)两族均由实现构造保证**(印证核心规律:构造保证族真实 bug 稀缺——pyscf 构造保证两族 c+f 皆负结果,非构造三族 a/b/h 各有真实缺陷)。**a/b/h 完整,c+f 构造保证负结果。**

---

## 域 3:reactor_physics — 中子输运 Boltzmann 方程

### 3a. 方程角度元模式存在性(输运+碰撞算子,先验)
| 元模式 | 先验导出 | 族 | 是否非空 |
|---|---|---|---|
| **$G$** 几何对称 | 反射/旋转/周期边界 ⟹ 对称等价位置通量相等、几何等价代数表示规范唯一(a);中子平衡守恒(b) | a, b | ✓ |
| **$T^*$** 自伴 | adjoint flux(importance)`L†φ†`;forward↔adjoint 互易(d) | c, d | ✓ |
| **$O_{\le}$** 正定 | 通量 `φ≥0`;depletion 数密度 `N≥0`(f) | f | ✓ |
| **$\mathcal L^*$** 极限 | `k_eff` 本征值幂迭代(源迭代)收敛(h);MPI 归约方法不变(j) | h, j | ✓ |

### 3b. SUT 角度证据(openmc 实现)
| 族 (Mode) | 先验 MR | 真实缺陷 | 违反证据 |
|---|---|---|---|
| a G·eqv (I) | 同一几何平面等价代数表示规范一致 `normalize(kP)==normalize(P)` | openmc 3bf1486f4 (Surface.normalize #3270) | pre 0.15.0 FIRED (符号丢失) / post 0.15.3 HELD(conda) |
| **j L\*·rep (M,MPI)** | tally MPI 归约方法不变 `flux(no_reduce)==flux(reduce)` | openmc bd76fc056 (#3619) | pre 0.15.2 FIRED (偏 1/n_ranks=0.5) / post 0.15.3 HELD(conda+MPI,rel_diff 2e-16) |
| a G·eqv (I,旋转) | 四种平面 sense 描述同一旋转周期楔形,`k_eff` 不变 | openmc c7d7fa461 (RotationalPeriodicBC gh-3692) | pre 0.15.4-dev30 FIRED (混合 sense 丢粒子) / post 0.15.4-dev31 HELD(源码编译,四 rep k=1.527569) |
| d T\*·dual (M) | IFP 伴随权重 beta_eff 应源自母中子延迟群(forward↔adjoint 对偶),朝向/代际不变 | openmc 767db7e6a (IFP #3580) | pre 66e7d863 FIRED (beta_eff=687.4 pcm,误用子裂变点延迟群) / post 767db7e6a HELD(源码编译,beta_eff=498.7 pcm,与 conda 0.15.3 一致到 7e-8) |
| f O≤·stat (I,正性) | depletion/burnup 数密度 `N≥0`(物理量非负) | openmc 1f7ac4215 (CRAM 负密度 clip) | pre a1df5842e FIRED (min N=−5.8e-2<0,轨迹 [1,0.986,−0.058])/ post 1f7ac4215 HELD (min N=0,Integrator.integrate 加 `r.clip(min=0)`)(源码编译纯 Python depletion)|
| h L\*·conv (I) | 源迭代收敛触发器须绑定其 score(收敛准则成立前提) | openmc b54de4d76 (tally trigger #3155) | pre 0.15.0 FIRED(`*-production` 触发器 fatal_error,收敛环不可建立)/ post 0.15.3 HELD(绑定成功,fission 触发器 15→40 批至 rel_err=0.00983<0.01)(conda)|

### 3c. 证据链闭合
输运先验给出 $G/T^*/O_{\le}/\mathcal L^*$;openmc **a 几何对称族有独立真实缺陷**(normalize 符号丢失 + RotationalPeriodicBC 旋转周期),锚定 2-群 MG pin-cell / 楔形输运(k_eff);**j 表示不变族亦有独立真实缺陷**(no_reduce tally MPI 偏 1/n_ranks,Mode M);**d 伴随对偶族亦有独立真实缺陷**(IFP adjoint-weighted kinetics,beta_eff 687.4→498.7 pcm,锚定 Godiva-like CE U235 球);**f 正性族亦有独立真实缺陷**(CRAM depletion 数密度负值 clip,min N=−5.8e-2→0);**h 收敛族亦有独立真实缺陷**(tally 触发器 score 绑定)。**a + j + d + f + h 五族完整(openmc 域族覆盖最全)。** openmc 无 b(Noether 守恒)独立 in-the-wild(no_reduce 属 j 表示不变,非守恒)。

---

## 域 4:pde_sciml — PINN(diffusion2d / Burgers2d)

### 4a. 方程角度元模式存在性(PINN 代理 2D 扩散,先验)
| 元模式 | 先验导出 | 族 | 是否非空 |
|---|---|---|---|
| **$G$** 对称 | 域对称 ⟹ 解对称、周期 BC 平移对称(a);Neumann 零通量 ⟹ 质量守恒 `d/dt∫u=0`(b) | a, b | ✓ |
| **$T^*$** 自伴 | PDE 算子标量场 Hessian 自伴 `H[i,j]=H[j,i]`(混合偏导 Schwarz)(c) | c | ✓ |
| **$O_{\le}$** 边界/单调 | Dirichlet BC `u\|∂Ω=g` 须在边界配点强制 ⟹ 边界点须被检出并选中(f) | f | ✓ |
| **$\mathcal L^*$** 极限 | 固定 collocation 集上残差损失收敛(h) | h | ✓ |

### 4b. SUT 角度证据(主:第三方 DeepXDE in-the-wild;补:论文 T2 PINN mutant)

**主证据(第三方 in-the-wild,最流行 PINN 库 lululxvi/deepxde)**:
| 族 (Mode) | 先验 MR | SUT 证据 | 检出 |
|---|---|---|---|
| b G·cons (I,flux) | Neumann `n·∇u=g`(g=0 即 `d/dt∫u=0`)⟹ 通量残差可计算 | DeepXDE NeumannBC/RobinBC (4bac5eb) | pre v1.3.0 FIRED(TypeError,通量残差不可构造)/ post v1.3.1 HELD(残差=-3.0) |
| a G·eqv (I) | 周期 BC `u(x)=u(x+L e_k)` 离散平移对称,`periodic_point` 为轨道映射 ⟹ 对称映射可计算 | DeepXDE GeometryXTime.periodic_point (8353540) | pre v0.8.6 FIRED(TypeError,对称映射不可构造)/ post v0.9.0 HELD(P([0,0.4,0.5])=[1,0.4,0.5],对合 P(P(x))=x) |
| h L\*·conv (I) | PINN 须在**固定** collocation 集上极小化残差,迭代收敛到单一固定问题极小点 ⟹ `train_next_batch` 不得重采样 | DeepXDE PDE.train_next_batch (4adcde7) | pre v0.5.0 FIRED(5 步重采样 5/5,目标漂移)/ post v0.5.1 HELD(0/5 重采样,缓存固定) |
| f O≤·stat (I,边界) | Dirichlet BC 须在边界配点强制,边界点(含 float32 舍入)须被检出并选中 | DeepXDE DirichletBC/geometry (8a644fe) | pre 1.8.4 FIRED(float32 边界点 x≈0 因 isclose atol=1e-8 漏判,on_boundary False、normal 0、丢点)/ post 1.9.0 HELD(on_boundary True、normal −1、保留)|
| c T\*·sa (I,**△ reachability**) | 标量场 Hessian 自伴 `H[i,j]=H[j,i]`(Schwarz 混合偏导)| DeepXDE forward-mode Hessian (46e2c2e) | pre 9d9d0b0 FIRED(forward Jacobian col1 返回 col0,max\|err\|=6.185,Hessian 非对称)/ post 46e2c2e HELD(对称 gap 0.0);**caveat:forward-mode 非 public 默认路径,须显式 import**(源码编译)|

路径:`results/deepxde_repro/` + `results/bug_deepxde_{neumann,periodic,resample,boundary_float32,forward_hessian_symmetry}.json`。

**补充证据(论文 T2 受控 mutant)**:
| b 守恒:`∫u` 跨快照守恒 | 自建 diffusion2d PINN + `M_TIME_NEG` | killed=1(residual 0.326 > tol 0.023);coord/act 不误杀 |
- 路径:`Minimum-MR-SubSet/runs/abd-witness-diffusion2d-pinn-20260608T032704Z/kill_matrix.csv`。

### 4c. 证据链闭合(第三方 in-the-wild 为主 + mutant 补)
方程先验 **b 守恒/flux** ← (主)DeepXDE NeumannBC 第三方真实缺陷(pre 崩溃/post 修复)+(补)自建 PINN `M_TIME_NEG` mutant killed。**a 对称(周期平移)** ← periodic_point(pre 崩溃/post 修复)。**h 收敛** ← train_next_batch(pre 重采样致漂移 5/5 / post 固定 0/5)。**f O≤/边界** ← float32 边界点检测(pre 漏判丢点/post 保留)。**c T\*/自伴** ← forward-mode Hessian(pre J-col 6.185 非对称/post gap 0.0),但 **△ reachability**(非默认路径)。**b+a+h+f 四族闭合,c 族边际填补(△),均第三方 in-the-wild。**

---

## 总览:每域族覆盖

| SUT 域 | 方程先验(元模式) | SUT 真实缺陷证据(族) | 完整族实例 |
|---|---|---|---|
| pde_numerical (scipy) | $G/T^*/O_{\le}/\mathcal L^*$(+Trev\*=∅) | h(LSODA)、j(banded)、c(eigh+complexsym)、f(Akima)、a(fht 边际)(6 缺陷) | **✓ h/j/c/f 完整,a 边际** |
| quantum_chemistry (pyscf) | $G/T^*/O_{\le}/\mathcal L^*$ | b(smearing)、h(DIIS)、a(D2h)(3 缺陷)+ c/f 构造保证负结果 | **✓ a/b/h 完整,c+f 构造负** |
| reactor_physics (openmc) | $G/T^*/O_{\le}/\mathcal L^*$ | a(normalize+rotperiodic)、j(no_reduce)、d(IFP)、f(CRAM)、h(keff)(6 缺陷) | **✓ a/j/d/f/h 完整(族覆盖最全)** |
| pde_sciml (DeepXDE) | $G/T^*/O_{\le}/\mathcal L^*$ | b(Neumann)、a(periodic)、h(resample)、f(boundary)、c(forward-Hessian △)(5 缺陷)+ T2 mutant | **✓ b/a/h/f 完整,c 边际(第三方)** |

**4/4 域均有完整族实例,全部第三方 in-the-wild 真实库缺陷证据**(scipy/pyscf/openmc/DeepXDE);pde_sciml 额外有论文 T2 自建 PINN mutant 受控补充。**共 20 个论文 SUT 域 in-scope 真实缺陷**,分布于 **7 族(a,b,c,d,f,h,j)**,in-scope N detection 20/20(含 2 caveated:scipy fht a 信号边际、DeepXDE forward-mode Hessian c 非默认路径 reachability)。

## 证据来源分层(诚实)
| 层 | 域 | 证据性质 |
|---|---|---|
| **in-the-wild 真实缺陷**(B1 本体,**全部第三方库**) | scipy / pyscf / openmc / DeepXDE | git-history fix 的 pre/post,pip / conda / 源码编译实测,作者未介入缺陷生成 |
| **受控 mutant**(论文 T2,补充) | 自建 PINN diffusion2d | 注入 mutant + b 守恒 MR kill,受控实验 |

## 缺口进展 + 剩余(诚实)
1. **本轮填补的 in-the-wild 族**:openmc f O≤(CRAM clip 1f7ac4215)、openmc h L\*(tally trigger b54de4d76)、DeepXDE f O≤(float32 8a644fe)、DeepXDE c T\*(forward Hessian 46e2c2e,**△ reachability**)、scipy a G(fht Hermitian 170f9e69a,**边际**);no_reduce/banded 从"守恒"归位为 **j L\*·rep 表示不变**。
2. **块加密(mutant,受控补)**:heat 的 f O≤ 最大值原理、wave 的 e Trev\* 时间反演 mutant(`/tmp/noether_block_densify.py`,baseline HELD / mutant FIRED)——Trev\* 在 pip 真实稀缺(无 symplectic 基底),以 mutant 补。
3. **已闭合(源码编译 / 非默认路径)**:scipy c complex-symmetric(50951d25c)、openmc a RotationalPeriodicBC(c7d7fa461)、openmc d IFP(767db7e6a)、openmc f CRAM(1f7ac4215 纯 Python)、DeepXDE c forward Hessian(46e2c2e)——unreleased / 非默认路径 fix 经源码编译 pre/post 闭合。
4. **剩余诚实负结果与 gap**:
   - **e Trev\* 全四域确认结构性稀缺**(scipy 无 symplectic 积分器、openmc 无可逆动力学基底、pyscf rt-TDDFT 已 v2.0.0 移出主仓 + BOMD velocity-Verlet 构造可逆实测 6.66e-16 HELD、DeepXDE 无时间步进积分器;四份 `NEGATIVE_*_trev.md`)。**Trev\* 是唯一在全部四域均为结构性负结果的元模式——因四域核心都不是可逆动力学模拟器(稳态求解/本征/不动点 SCF/残差最小化 PINN)。**
   - pyscf **c Fock-Hermitian + f 占据/密度/变分界**(均构造保证,`NEGATIVE_pyscf_o_le.md`);scipy a 干净 order-of-magnitude 候选(fht 边际填补后,非边际候选仍稀缺)。
   - **实证 gap:g(𝒟\* 形状/Sturm 振荡 overshoot)、i(ℰ\* 精度-阶退化)两族 B1 未测**——须补真实缺陷或显式标注。
