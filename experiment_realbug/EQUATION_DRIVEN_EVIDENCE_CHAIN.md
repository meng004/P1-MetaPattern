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

### 1c. 证据链闭合
热方程算子代数**先验**给出 T\*/O≤/L\*/守恒/G(+Trev\*=∅);scipy 实现中 **L\*/守恒/T\* 三块各有独立真实缺陷**违反对应先验 MR。**完整。**

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
| T\* Fock-Hermitian | 构造保证 ⟹ vanilla 真实 bug 稀缺(仅 int-DM 边界 #1114) | — (诚实负结果) |

### 2c. 证据链闭合
RHF 先验给出 T\*/守恒/L\*/O≤/G;pyscf **守恒块有独立真实缺陷**(smearing,纯数值违反 14 vs 13)。T\* 由实现**构造保证**(印证论文:构造保证块真实 bug 稀缺)。**守恒块完整。**

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
| 守恒:tally 归一化一致 | openmc bd76fc056 (#3619) — fix 首入 0.15.3,**无 conda pre**(候选,未闭合) | — |

### 3c. 证据链闭合
输运先验给出 守恒/G/O≤/T\*;openmc **G 几何对称块有独立真实缺陷**(normalize 符号丢失),锚定 2-群 MG pin-cell 输运(k_eff)。**G 块完整。** 守恒块候选(bd76fc056)pre 无 conda binary,未闭合。

---

## 域 4:pde_sciml — PINN(diffusion2d / Burgers2d)

### 4a. 方程角度元模式存在性(PINN 代理 2D 扩散,先验)
| 块 | 先验导出 | 是否非空 |
|---|---|---|
| **守恒** | Neumann 零通量 ⟹ 质量守恒 `d/dt ∫u=0` | ✓ |
| **L\*** | 解光滑性、参考包络 | ✓ |
| **G** 对称 | 域对称 ⟹ 解对称 | ✓ |

### 4b. SUT 角度证据(论文 T2 已有 PINN witness)
| 先验 MR | SUT 证据 | 检出 |
|---|---|---|
| 守恒:Neumann 零通量 ⟹ `∫u` 跨快照守恒(梯形积分) | diffusion2d PINN + mutant `M_TIME_NEG` | **killed=1**(residual 0.326 > tol 0.023);coord/act mutant killed=0(MR 不误杀) |

- 路径:`Minimum-MR-SubSet/runs/abd-witness-diffusion2d-pinn-20260608T032704Z/kill_matrix.csv`(论文 T2 已跑)。
- MR catalog:`DIFFUSION_PINN_MR_NEUMANN_MASS_CONSERVATION`("integral of u over spatial domain must be conserved across snapshots")。
- **诚实区分**:此为 **mutant 注入**(论文受控实验),非 B1 in-the-wild 真实库缺陷。

### 4c. 证据链闭合(mutant 路径)
方程先验 **Neumann 质量守恒 MR** ← diffusion2d PINN 上 `M_TIME_NEG` mutant 违反(killed,residual 14× 超容差)。**守恒块闭合(mutant 路径,诚实标注非 in-the-wild)。**

---

## 总览:每域完整性

| SUT 域 | 方程先验 | SUT 真实缺陷证据 | 完整元模式实例 |
|---|---|---|---|
| pde_numerical (scipy) | ✓ 6 块 | ✓ L\*/守恒/T\* (3 真实缺陷) | **✓ 完整** |
| quantum_chemistry (pyscf) | ✓ 5 块 | ✓ 守恒 (1) + T\* 构造保证负结果 | **✓ 守恒完整** |
| reactor_physics (openmc) | ✓ 4 块 | ✓ G 几何对称 (1,conda) | **✓ G 完整** |
| pde_sciml (PINN) | ✓ 3 块 | ✓ 守恒 mutant `M_TIME_NEG` killed(论文 T2) | **✓ 守恒闭合(mutant 路径)** |

**4/4 域均有完整元模式实例**:**3 域 in-the-wild 真实库缺陷**(scipy/pyscf/openmc)+ **1 域 mutant**(pde_sciml PINN,论文受控实验)。诚实区分两类证据。

## 证据来源分层(诚实)
| 层 | 域 | 证据性质 |
|---|---|---|
| **in-the-wild 真实缺陷**(B1 本体) | scipy / pyscf / openmc | git-history fix 的 pre/post,pip/conda 实测,作者未介入缺陷生成 |
| **受控 mutant**(论文 T2 已有) | PINN diffusion2d | 注入 mutant + 守恒 MR kill,受控实验 |

## 待补缺口(下一步候选,可选)
1. **块加密**:heat 的 O≤ 最大值原理、wave 的 Trev\* 时间反演——方程先验存在,in-the-wild 真实库证据稀缺,可用 mutant 补(同 PINN 路径)。
2. **reactor 守恒块闭合**:openmc bd76fc056 (tally-norm) fix 首入 0.15.3,需找 conda pre 或源码编译。
