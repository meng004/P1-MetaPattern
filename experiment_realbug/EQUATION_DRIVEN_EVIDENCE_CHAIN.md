# B1 方程驱动证据链:方程代数 → 先验元模式 → SUT 真实缺陷 (2026-06-22)

> **方法论声明**:NOETHER 元模式 MR 从**方程的算子代数先验机械导出**(守恒律/自伴/对称/单调/收敛由 Noether 定理与算子性质决定),**不为任何缺陷定制**。本文先对每个 SUT 域的代表方程做**存在性分析**(纯理论,不看缺陷),再用**独立发现的真实库缺陷**作为该先验 MR 被违反的证据。MR 先验存在 ⟹ 缺陷是独立证据,非 circular。

---

## 域 1:pde_numerical — 热传导方程 `u_t = α u_xx`(抛物)

### 1a. 方程角度元模式存在性(算子 `L = α ∂²/∂x²`,先验)
| 块 | 先验导出(数学) | 是否非空 |
|---|---|---|
| **T\*** 自伴 | `⟨Lu,v⟩=⟨u,Lv⟩`(两次分部积分,边界项消)⟹ 离散 L 对称、谱实、特征向量正交 | ✓ |
| **O≤** 线性/单调 | L 线性 ⟹ superposition;抛物最大值原理 ⟹ 极值在 parabolic boundary | ✓ |
| **L\*** 收敛 | 离散格式一致收敛 ⟹ Richardson 自收敛、稠密插值自洽 | ✓ |
| **守恒** | Neumann/周期 ⟹ `d/dt ∫u = 0`(散度定理) | ✓ |
| **G** 对称 | 常系数 ⟹ 平移不变;偶 ⟹ 反射对称 | ✓ |
| **Trev\*** 时间反演 | α>0 耗散 ⟹ **不可逆**(先验可证为空) | **∅(可证)** |

### 1b. SUT 角度证据(scipy.integrate / linalg 实现该算子)
| 先验 MR | 真实缺陷(独立发现) | 违反证据 |
|---|---|---|
| L\*:稠密插值穿过求解器网格(`sol(t)==y`) | scipy c374ca7fd (LSODA dense-output) | pre 1.11.4 FIRED / post 1.12.0 HELD |
| 守恒/表示不变:同算子不同存储同轨迹 | scipy cb0538877 (banded Jacobian) | pre 1.15.3 FIRED / post 1.16.3 (\|y_b-y_f\|=0) |
| T\*:自伴谱 driver-invariant | scipy 178a12572 (eigh driver) | pre 1.13.0 FIRED / post 1.13.1 HELD |
| T\*:对称结构不变 `solve/inv(A,sym)==solve/inv(A)`(A==A^T) | scipy 50951d25c (complex-symmetric, gh-24359) | pre 1.18.0.dev0+git20260120.d292d32 FIRED (max\|X@a-I\|=9.11) / post 1.18.0.dev0+git20260121.50951d2 HELD(源码编译 meson) |
| O≤:shape-preserving 插值,2 个单调点须为线性弦 `I((x0+x1)/2)==(y0+y1)/2` | scipy ef7437afc (Akima 两点线性, gh-22278) | pre 1.15.2 FIRED (I(0.5)=1.25≠1.0,或 `np.empty` 未初始化斜率致非有限崩溃)/ post 1.16.0 HELD (I(0.5)=1.0,max\|I-弦\|=0) |

### 1c. 证据链闭合
热方程算子代数**先验**给出 T\*/O≤/L\*/守恒/G(+Trev\*=∅);scipy 实现中 **L\*/守恒/T\*/O≤ 四块各有独立真实缺陷**违反对应先验 MR(T\* 两实例:eigh driver-invariance + complex-symmetric 对称结构;O≤:Akima 两点线性 shape-preservation)。**完整。**

---

## 域 2:quantum_chemistry — RHF Fock 方程 `FC = SCε`

### 2a. 方程角度元模式存在性(Fock 算子 F,先验)
| 块 | 先验导出 | 是否非空 |
|---|---|---|
| **T\*** 自伴 | `F=F†`(h,J,K 厄米)、`S=S†` ⟹ MO 实正交 `C†SC=I` | ✓ |
| **守恒** | `N_elec = tr(P S)`(密度矩阵迹) | ✓ |
| **L\*** 收敛 | SCF 不动点迭代收敛 | ✓ |
| **O≤** 变分 | `E[Ψ] ≥ E_0`(Rayleigh-Ritz) | ✓ |
| **G** 对称 | 分子点群 ⟹ 简并/对称轨道 | ✓ |

### 2b. SUT 角度证据(pyscf 实现)
| 先验 MR | 真实缺陷 | 违反证据 |
|---|---|---|
| 守恒:`sum(occ)=N_elec` | pyscf ebf4e676 (smearing #2290) | pre 2.6.2 FIRED (14≠13) / post 2.7.0 HELD |
| L\*:对称自适应 SCF 不动点不受数值噪声影响(收敛 + e_tot 确定) | pyscf 15920e60 (DIIS 数值噪声 #1638) | pre 2.2.0 FIRED (0/5 收敛,e_tot 抖动 1.76e-2) / post 2.2.1 HELD (5/5 收敛,e_tot=-74.7874921601011) |
| G 点群:分子点群 ⟹ MO irrep 标签朝向不变 `orbsym(perm)==orbsym(ref)` | pyscf 4542fe9b (D2h 轴向 #3176) | pre 2.12.1 FIRED (乙烯 STO-3G RHF,6 朝向 6 个 orbsym,1/6 对参考)/ post 2.13.0 HELD (6/6 对,1 个 orbsym) |
| T\* Fock-Hermitian | 构造保证 ⟹ vanilla 真实 bug 稀缺(仅 int-DM 边界 #1114) | — (诚实负结果) |

### 2c. 证据链闭合
RHF 先验给出 T\*/守恒/L\*/O≤/G;pyscf **守恒块有独立真实缺陷**(smearing,纯数值违反 14 vs 13),**L\* 收敛块亦有独立真实缺陷**(对称自适应 DIIS 数值噪声,0/5→5/5),**G 点群块亦有独立真实缺陷**(D2h 轴向 orbsym 朝向依赖,6→1)。T\* 由实现**构造保证**(印证论文:构造保证块真实 bug 稀缺)。**守恒 + L\* + G 块完整。**

---

## 域 3:reactor_physics — 中子输运 Boltzmann 方程

### 3a. 方程角度元模式存在性(输运+碰撞算子,先验)
| 块 | 先验导出 | 是否非空 |
|---|---|---|
| **守恒** | 中子平衡 产生=吸收+泄漏;`k_eff` 本征 | ✓ |
| **G** 几何对称 | 反射/旋转/周期边界 ⟹ 对称等价位置通量相等;几何等价代数表示**规范唯一** | ✓ |
| **O≤** 正定 | 通量 `φ ≥ 0` | ✓ |
| **T\*** 自伴 | adjoint flux(importance)`L†φ†` | ✓ |

### 3b. SUT 角度证据(openmc 实现)
| 先验 MR | 真实缺陷 | 违反证据 |
|---|---|---|
| G:同一几何平面的等价代数表示规范一致 `normalize(kP)==normalize(P)` | openmc 3bf1486f4 (Surface.normalize #3270) | pre 0.15.0 FIRED (符号丢失) / post 0.15.3 HELD(conda) |
| 守恒:tally 归一化方法不变 `flux(no_reduce)==flux(reduce)` | openmc bd76fc056 (#3619) | pre 0.15.2 FIRED (偏 1/n_ranks=0.5) / post 0.15.3 HELD(conda+MPI,rel_diff 2e-16) |
| G(旋转):四种平面 sense 描述同一旋转周期楔形,`k_eff` 不变 | openmc c7d7fa461 (RotationalPeriodicBC gh-3692) | pre 0.15.4-dev30 FIRED (混合 sense 丢粒子) / post 0.15.4-dev31 HELD(源码编译,四 rep k=1.527569) |
| T\*(伴随对偶):IFP 伴随权重 beta_eff 应源自母中子的延迟群(forward↔adjoint 对偶),朝向/代际不变 | openmc 767db7e6a (IFP #3580) | pre 66e7d863 FIRED (beta_eff=687.4 pcm,误用子裂变点延迟群) / post 767db7e6a HELD(源码编译,beta_eff=498.7 pcm,与 released conda 0.15.3 一致到 7e-8) |

### 3c. 证据链闭合
输运先验给出 守恒/G/O≤/T\*;openmc **G 几何对称块有独立真实缺陷**(normalize 符号丢失 + RotationalPeriodicBC 旋转周期),锚定 2-群 MG pin-cell / 楔形输运(k_eff);**守恒块亦有独立真实缺陷**(no_reduce tally MPI 偏 1/n_ranks);**T\* 伴随对偶块亦有独立真实缺陷**(IFP adjoint-weighted kinetics,beta_eff 687.4→498.7 pcm,锚定 Godiva-like CE U235 球)。**G + 守恒 + T\* 块完整。**

---

## 域 4:pde_sciml — PINN(diffusion2d / Burgers2d)

### 4a. 方程角度元模式存在性(PINN 代理 2D 扩散,先验)
| 块 | 先验导出 | 是否非空 |
|---|---|---|
| **守恒** | Neumann 零通量 ⟹ 质量守恒 `d/dt ∫u=0` | ✓ |
| **L\*** | 解光滑性、参考包络 | ✓ |
| **G** 对称 | 域对称 ⟹ 解对称 | ✓ |

### 4b. SUT 角度证据(主:第三方 DeepXDE in-the-wild;补:论文 T2 PINN mutant)

**主证据(第三方 in-the-wild,最流行 PINN 库)**:
| 先验 MR | SUT 证据 | 检出 |
|---|---|---|
| 守恒/flux:Neumann `n·∇u=g`(g=0 即 `d/dt∫u=0`)⟹ 通量残差可计算 | DeepXDE NeumannBC/RobinBC (4bac5eb) | pre v1.3.0 FIRED(TypeError,通量残差不可构造)/ post v1.3.1 HELD(残差=-3.0) |
| G/对称:周期 BC `u(x)=u(x+L e_k)` 为离散平移对称,`periodic_point` 为轨道映射 ⟹ 对称映射可计算 | DeepXDE GeometryXTime.periodic_point (8353540) | pre v0.8.6 FIRED(TypeError,对称映射不可构造)/ post v0.9.0 HELD(P([0,0.4,0.5])=[1,0.4,0.5],对合 P(P(x))=x) |
| L\* 收敛:PINN 训练须在**固定** collocation 集上极小化残差损失,迭代收敛到单一固定问题的极小点 ⟹ `train_next_batch` 重复调用不得重采样 | DeepXDE PDE.train_next_batch (4adcde7) | pre v0.5.0 FIRED(5 步重采样 5/5,目标函数漂移)/ post v0.5.1 HELD(0/5 重采样,集合缓存固定) |
- DeepXDE = 最流行第三方 PINN 库(lululxvi/deepxde),上游维护者 fix,pip 实测,非自建非 mutant。路径:`results/deepxde_repro/` + `results/bug_deepxde_neumann.json` + `results/bug_deepxde_periodic.json` + `results/bug_deepxde_resample.json`。

**补充证据(论文 T2 受控 mutant)**:
| 守恒:`∫u` 跨快照守恒 | 自建 diffusion2d PINN + `M_TIME_NEG` | killed=1(residual 0.326 > tol 0.023);coord/act 不误杀 |
- 路径:`Minimum-MR-SubSet/runs/abd-witness-diffusion2d-pinn-20260608T032704Z/kill_matrix.csv`。

### 4c. 证据链闭合(第三方 in-the-wild 为主 + mutant 补)
方程先验 **Neumann 守恒/flux MR** ← (主)DeepXDE NeumannBC 第三方真实缺陷违反(pre 崩溃 / post 修复)+ (补)自建 PINN `M_TIME_NEG` mutant killed。方程先验 **G/对称(周期平移)MR** ← DeepXDE periodic_point 第三方真实缺陷违反(pre 崩溃 / post 修复)。方程先验 **L\* 收敛 MR** ← DeepXDE train_next_batch 第三方真实缺陷违反(pre 每步重采样致目标漂移 5/5 / post 固定缓存 0/5)。**守恒 + G + L\* 三块均闭合,升级为第三方 in-the-wild。**

---

## 总览:每域完整性

| SUT 域 | 方程先验 | SUT 真实缺陷证据 | 完整元模式实例 |
|---|---|---|---|
| pde_numerical (scipy) | ✓ 6 块 | ✓ L\*/守恒/T\*(T\* 两实例:eigh + complex-symmetric)/O≤(Akima 两点线性)(5 真实缺陷) | **✓ 完整** |
| quantum_chemistry (pyscf) | ✓ 5 块 | ✓ 守恒 + L\* 收敛 + G 点群(D2h orbsym)(3 真实缺陷) + T\* 构造保证负结果 | **✓ 守恒+L\*+G 完整** |
| reactor_physics (openmc) | ✓ 4 块 | ✓ G 几何对称(normalize + RotationalPeriodicBC)+ 守恒 + T\* 伴随对偶(IFP)(4,conda/MPI/源码编译) | **✓ G+守恒+T\* 完整** |
| pde_sciml (DeepXDE) | ✓ 3 块 | ✓ 守恒/flux + G/对称 + L\* 收敛(均 DeepXDE 第三方 in-the-wild)(3)+ 自建 PINN mutant(论文 T2 补) | **✓ 守恒+G+L\* 完整(第三方)** |

**4/4 域均有完整元模式实例,且全部有第三方 in-the-wild 真实库缺陷证据**(scipy/pyscf/openmc/DeepXDE);pde_sciml 额外有论文 T2 自建 PINN mutant 作为受控补充。**共 15 个论文 SUT 域 in-scope 真实缺陷**(scipy 5 + pyscf 3 + openmc 4 + DeepXDE 3),N detection 15/15。

## 证据来源分层(诚实)
| 层 | 域 | 证据性质 |
|---|---|---|
| **in-the-wild 真实缺陷**(B1 本体,**全部第三方库**) | scipy / pyscf / openmc / DeepXDE | git-history fix 的 pre/post,pip / conda / 源码编译实测,作者未介入缺陷生成 |
| **受控 mutant**(论文 T2,补充) | 自建 PINN diffusion2d | 注入 mutant + 守恒 MR kill,受控实验 |

## 待补缺口(下一步候选,可选)
1. **块加密(mutant)**:heat 的 O≤ 最大值原理、wave 的 Trev\* 时间反演——以 mutant 补(scipy O≤ 块已另有 Akima 两点线性 in-the-wild;Trev\* 在 scipy 真实稀缺,无 symplectic 基底)。
2. **DeepXDE G 对称块(已闭合)**:`8353540`(periodic_point,v0.8.6→v0.9.0)纯几何无需训练;TF1.x backend 障碍经"纯 numpy 几何路径不触发 backend"绕开,已 pip 实测 FIRED→HELD。
3. **scipy complex-symmetric T\* / openmc RotationalPeriodicBC G(已闭合)**:两 unreleased fix(50951d25c / c7d7fa461)经源码编译 pre/post 闭合,无需 released wheel / conda binary。
