# B1 真缺陷 MT 实验 — 成果索引 (2026-06-22)

> in-the-wild 真缺陷佐证 NOETHER 元模式 MR 检出能力。分支 `claude/b1-realbug-2026-06-21`。
> 全部 git-history 取真 SHA + pip / conda released-to-released 或源码编译复现(pre FIRED / post HELD 自跑核验)。

## 文档导航
- `COVERAGE_SUMMARY.md` — 论文 SUT 域覆盖矩阵 + 块覆盖 + 诚实稀缺结果 + 覆盖规律
- `B1_exploration_plan_2026-06-21.md` — 探索计划 + 验收标准 + 重定向记录
- `RESULTS.md` — analyze 输出(detection / Wilson CI)
- `B1_INDEX.md`(本文件)— 成果索引 + 复现指南

## A. 论文 SUT 域 in-scope 正样本(n=11,pip + conda + 源码编译核验)

| bug_json | 域 | NOETHER 块 | fix SHA | pre→post | 复现脚本 |
|---|---|---|---|---|---|
| bug_scipy_lsoda_densesol.json | pde_numerical | L\* 收敛 | c374ca7fd | scipy 1.11.4→1.12.0 | results/scipy_repro/repro_lsoda_event.py |
| bug_scipy_banded_jac.json | pde_numerical | 守恒/表示不变 | cb0538877 | scipy 1.15.3→1.16.3 | results/scipy_repro/repro_banded.py |
| bug_scipy_eigh_driver.json | pde_numerical | T\* 自伴 | 178a12572 | scipy 1.13.0→1.13.1 | results/scipy_repro/repro_eigh.py |
| bug_scipy_complexsym.json | pde_numerical | T\* 自伴/对称结构 | 50951d25c | scipy 1.18.0.dev0+git20260120.d292d32→1.18.0.dev0+git20260121.50951d2 (源码编译 meson) | results/scipy_repro/repro_complex_sym.py |
| bug_pyscf_smearing.json | quantum_chemistry | 守恒(Noether) | ebf4e676 | pyscf 2.6.2→2.7.0 | results/pyscf_repro/repro_smearing.py |
| bug_pyscf_diis.json | quantum_chemistry | L\* 收敛 | 15920e60 | pyscf 2.2.0→2.2.1 (numpy<1.24+scipy<1.10+h5py<3.9) | results/pyscf_repro/repro_pyscf_diis.py |
| bug_openmc_normalize.json | reactor_physics | G 对称 | 3bf1486f4 | openmc 0.15.0→0.15.3 (conda) | results/openmc_repro/noether_reactor_normalize.py |
| bug_openmc_no_reduce.json | reactor_physics | 守恒(MPI no_reduce) | bd76fc056 | openmc 0.15.2→0.15.3 (conda+MPI) | results/openmc_repro/noether_reactor_no_reduce.py |
| bug_openmc_rotperiodic.json | reactor_physics | G 对称(旋转周期) | c7d7fa461 | openmc 0.15.4-dev30→0.15.4-dev31 (源码编译,parent 818fd11b1) | results/openmc_repro/repro_rotational_periodic.py |
| bug_deepxde_neumann.json | pde_sciml (第三方) | 守恒/flux | 4bac5eb | deepxde 1.3.0→1.3.1 (pip) | results/deepxde_repro/repro_deepxde_neumann.py |
| bug_deepxde_periodic.json | pde_sciml (第三方) | G 对称(周期/平移) | 8353540 | deepxde 0.8.6→0.9.0 (pip) | results/deepxde_repro/repro_deepxde_periodic.py |

**复现命令**(以 pyscf_smearing 为例):
```bash
uv venv --python 3.11 /tmp/v && . /tmp/v/bin/activate
uv pip install "pyscf==2.6.2"                  # PRE  -> FIRED (sum(mo_occ)=14)
python results/pyscf_repro/repro_smearing.py
uv pip install "pyscf==2.7.0"                  # POST -> HELD  (sum(mo_occ)=13)
python results/pyscf_repro/repro_smearing.py
```

## B. 跨域补充(geometric DL,非论文 SUT 域,domain 字段隔离)

| bug_json | 库 | NOETHER 块 | 环境栈 |
|---|---|---|---|
| bug_pyg_6199.json | pytorch_geometric | Sₙ 置换 (m^eq_inv) | env-class-B: py3.10+torch1.13+pyg2.2 |
| bug_e3nn_reduce.json | e3nn | adjoint 反对称 (m^eq_adj) | env-class-C: py3.9+torch1.8.1+e3nn0.2.7 |
| bug_pyg_undirected.json | pytorch_geometric | adjoint 对称化 | env-class-B |

## C. 边界 / out / 排除(诚实记录)

| bug_json | 状态 | 原因 |
|---|---|---|
| bug_scipy_akima_overflow.json | 边界 | O≤ 映射勉强(overflow 鲁棒性,非单调性);极端输入 1e160 |
| bug_pyg_6037.json | out-of-decomposition | 行和守恒,不映射元模式 |

## D. 环境栈(env-class,单容器)

| env-class | 栈 | 用途 |
|---|---|---|
| A | py3.11 + torch2.12 | scipy/pyscf pip venv(/tmp/venv_scipy, /tmp/venv_pyscf) |
| A' | py3.10 + numpy<1.24 + scipy<1.10 + h5py<3.9 | pyscf 2.2.0/2.2.1 DIIS pip venv(/tmp/venv_pyscf22);解 2.2.x vs 现代 numpy/scipy 冲突 |
| B | py3.10 + torch1.13 + pyg2.2 | pyg 跨域(/tmp/venv_6199) |
| C | py3.9 + **torch1.8.1** + e3nn0.2.7 | e3nn 跨域(/tmp/venv_c2);关键:torch1.8.1 解 e3nn fx |
| D (conda) | micromamba + multi-group XS(无 CE 核数据) | openmc normalize / no_reduce(conda 0.15.0/0.15.2/0.15.3,no_reduce 需 MPI build) |
| E (源码编译) | scipy meson editable build,py3.12 + openblas | scipy complex-symmetric(unreleased fix 50951d25c,pre/post 源码编译) |
| F (源码编译) | micromamba omc_src,cmake+ninja Release,MPI/OpenMP,multi-group XS | openmc RotationalPeriodicBC(unreleased fix c7d7fa461,pre=parent 818fd11b1 / post=c7d7fa461,仅 C++ 改动) |

## E. 诚实标注(贯穿)

- **FIRED 类型**:11 个 in-scope 中 5 个 crash-type(3 scipy + 2 DeepXDE,follow-up 合法输入崩溃→违反 MR 关系)、4 个纯数值违反(scipy complexsym、pyscf smearing 14 vs 13、openmc normalize、openmc no_reduce)、1 个收敛/自洽(pyscf DIIS 0/5→5/5)、1 个 transport 失败(openmc rotperiodic 丢粒子)。
- **稀缺块**:scipy Trev\*/O≤/G 在 pip 可复现范围稀缺;pyscf T\* Fock-Hermitian 构造保证(需 int-DM 边界)。
- **不可达(已解决)**:OpenMC/OpenMOC 无 PyPI(需 conda+核数据,Tier-C);unreleased fix(openmc rotperiodic、scipy complexsym)经源码编译 pre/post 闭合。
- **样本量**:n=11 论文 SUT 域,underpowered for α=0.05(C6),descriptive 证据。
- **覆盖规律**:NOETHER 真实 bug 数值算法库(scipy)富集,构造保证物理库(pyscf/e3nn)稀缺,守恒/计数不变量有真实数值 bug。
