# B1 真缺陷 MT 实验 — 成果索引 (2026-06-22)

> in-the-wild 真缺陷佐证 MR 族检出能力。分支 `claude/b1-realbug-2026-06-21`。
> 全部 git-history 取真 SHA + pip / conda released-to-released 或源码编译复现(pre FIRED / post HELD 自跑核验)。
> 分类基准 = `UNIFIED_BLOCK_MODEL.md`:**5 元模式(最小代数基 $G,T^*,\mathcal T^*_{\mathrm{rev}},O_{\le},\mathcal L^*$)→ 10 MR 族(a–j)**。

## 文档导航
- `UNIFIED_BLOCK_MODEL.md` — 统一模型:元模式形式化 + 10 族增强表 + Mode I/M + 覆盖矩阵 + caveat(分类基准)
- `COVERAGE_SUMMARY.md` — 论文 SUT 域覆盖矩阵 + 族覆盖 + 诚实稀缺结果 + 覆盖规律
- `B1_exploration_plan_2026-06-21.md` — 探索计划 + 验收标准 + 重定向记录
- `RESULTS.md` — analyze 输出(detection / Wilson CI)
- `B1_INDEX.md`(本文件)— 成果索引 + 复现指南

## A. 论文 SUT 域 in-scope 正样本(n=20,pip + conda + 源码编译核验;含 2 个 caveated:fht a 边际、forward-mode Hessian c reachability)

| bug_json | 域 | MR 族 (Mode) | fix SHA | pre→post | 复现脚本 |
|---|---|---|---|---|---|
| bug_scipy_lsoda_densesol.json | pde_numerical | h L\*·conv (I) | c374ca7fd | scipy 1.11.4→1.12.0 | results/scipy_repro/repro_lsoda_event.py |
| bug_scipy_banded_jac.json | pde_numerical | **j L\*·rep (M)** | cb0538877 | scipy 1.15.3→1.16.3 | results/scipy_repro/repro_banded.py |
| bug_scipy_eigh_driver.json | pde_numerical | c T\*·sa (M) | 178a12572 | scipy 1.13.0→1.13.1 | results/scipy_repro/repro_eigh.py |
| bug_scipy_complexsym.json | pde_numerical | c T\*·sa (M) | 50951d25c | scipy 1.18.0.dev0+git20260120.d292d32→1.18.0.dev0+git20260121.50951d2 (源码编译 meson) | results/scipy_repro/repro_complex_sym.py |
| bug_scipy_akima_linear2pt.json | pde_numerical | f O≤·stat (I) | ef7437afc | scipy 1.15.2→1.16.0 | results/scipy_repro/repro_akima_linear2pt.py |
| bug_pyscf_smearing.json | quantum_chemistry | b G·cons (I) | ebf4e676 | pyscf 2.6.2→2.7.0 | results/pyscf_repro/repro_smearing.py |
| bug_pyscf_diis.json | quantum_chemistry | h L\*·conv (I) | 15920e60 | pyscf 2.2.0→2.2.1 (numpy<1.24+scipy<1.10+h5py<3.9) | results/pyscf_repro/repro_pyscf_diis.py |
| bug_pyscf_d2h_symm.json | quantum_chemistry | a G·eqv (I,点群) | 4542fe9b | pyscf 2.12.1→2.13.0 | results/pyscf_repro/repro_pyscf_d2h_symm.py |
| bug_openmc_normalize.json | reactor_physics | a G·eqv (I) | 3bf1486f4 | openmc 0.15.0→0.15.3 (conda) | results/openmc_repro/noether_reactor_normalize.py |
| bug_openmc_no_reduce.json | reactor_physics | **j L\*·rep (M,MPI)** | bd76fc056 | openmc 0.15.2→0.15.3 (conda+MPI) | results/openmc_repro/noether_reactor_no_reduce.py |
| bug_openmc_rotperiodic.json | reactor_physics | a G·eqv (I,旋转周期) | c7d7fa461 | openmc 0.15.4-dev30→0.15.4-dev31 (源码编译,parent 818fd11b1) | results/openmc_repro/repro_rotational_periodic.py |
| bug_openmc_ifp_adjoint.json | reactor_physics | d T\*·dual (M) | 767db7e6a | openmc 66e7d863→767db7e6a (源码编译,parent 66e7d863) | results/openmc_repro/repro_ifp_adjoint.py |
| bug_deepxde_neumann.json | pde_sciml (第三方) | b G·cons (I,flux) | 4bac5eb | deepxde 1.3.0→1.3.1 (pip) | results/deepxde_repro/repro_deepxde_neumann.py |
| bug_deepxde_periodic.json | pde_sciml (第三方) | a G·eqv (I,周期/平移) | 8353540 | deepxde 0.8.6→0.9.0 (pip) | results/deepxde_repro/repro_deepxde_periodic.py |
| bug_deepxde_resample.json | pde_sciml (第三方) | h L\*·conv (I) | 4adcde7 | deepxde 0.5.0→0.5.1 (pip) | results/deepxde_repro/repro_deepxde_resample.py |
| bug_openmc_cram_clip.json | reactor_physics | f O≤·stat (I,正性) | 1f7ac4215 | openmc a1df5842e→1f7ac4215 (源码编译,纯 Python depletion) | results/openmc_repro/repro_cram_clip.py |
| bug_scipy_fht_hermitian.json | pde_numerical | a G·eqv (I,**边际**) | 170f9e69a | scipy 1.14.1→1.15.0 (pip) | results/scipy_repro/repro_fht_hermitian.py |
| bug_openmc_keff_trigger.json | reactor_physics | h L\*·conv (I) | b54de4d76 | openmc 0.15.0→0.15.3 (conda) | results/openmc_repro/repro_keff_trigger_convergence.py |
| bug_deepxde_boundary_float32.json | pde_sciml (第三方) | f O≤·stat (I,边界) | 8a644fe | deepxde 1.8.4→1.9.0 (pip) | results/deepxde_repro/repro_deepxde_boundary_float32.py |
| bug_deepxde_forward_hessian_symmetry.json | pde_sciml (第三方) | c T\*·sa (I,**△ reachability**) | 46e2c2e | deepxde 9d9d0b0→46e2c2e (源码编译 worktree) | results/deepxde_repro/repro_deepxde_forward_hessian_symmetry.py |

**族分布**:a×5(normalize,rotperiodic,periodic,d2h,fht△)、b×2(smearing,neumann)、c×3(eigh,complexsym,forward-hessian△)、d×1(ifp)、f×3(akima,cram,boundary)、h×4(lsoda,diis,resample,keff)、j×2(banded,no_reduce)。e(Trev)全负、g(𝒟\*)与 i(ℰ\*)为 gap。

**复现命令**(以 pyscf_smearing 为例):
```bash
uv venv --python 3.11 /tmp/v && . /tmp/v/bin/activate
uv pip install "pyscf==2.6.2"                  # PRE  -> FIRED (sum(mo_occ)=14)
python results/pyscf_repro/repro_smearing.py
uv pip install "pyscf==2.7.0"                  # POST -> HELD  (sum(mo_occ)=13)
python results/pyscf_repro/repro_smearing.py
```

## B. 跨域补充(geometric DL,非论文 SUT 域,domain 字段隔离)

| bug_json | 库 | MR 族 | 环境栈 |
|---|---|---|---|
| bug_pyg_6199.json | pytorch_geometric | a G·eqv (Sₙ 置换) | env-class-B: py3.10+torch1.13+pyg2.2 |
| bug_e3nn_reduce.json | e3nn | c T\*·sa (adjoint 反对称) | env-class-C: py3.9+torch1.8.1+e3nn0.2.7 |
| bug_pyg_undirected.json | pytorch_geometric | c T\*·sa (adjoint 对称化) | env-class-B |

## C. 边界 / out / 排除(诚实记录)

| bug_json | 状态 | 原因 |
|---|---|---|
| bug_scipy_akima_overflow.json | 边界 | f O≤ 映射勉强(overflow 鲁棒性,非单调性);极端输入 1e160 |
| bug_pyg_6037.json | out-of-decomposition | 行和守恒,不映射任何元模式 |

## D. 环境栈(env-class,单容器)

| env-class | 栈 | 用途 |
|---|---|---|
| A | py3.11 + torch2.12 | scipy/pyscf pip venv(/tmp/venv_scipy, /tmp/venv_pyscf) |
| A' | py3.10 + numpy<1.24 + scipy<1.10 + h5py<3.9 | pyscf 2.2.0/2.2.1 DIIS pip venv(/tmp/venv_pyscf22);解 2.2.x vs 现代 numpy/scipy 冲突 |
| B | py3.10 + torch1.13 + pyg2.2 | pyg 跨域(/tmp/venv_6199) |
| C | py3.9 + **torch1.8.1** + e3nn0.2.7 | e3nn 跨域(/tmp/venv_c2);关键:torch1.8.1 解 e3nn fx |
| D (conda) | micromamba + multi-group XS(无 CE 核数据) | openmc normalize / no_reduce / keff_trigger(conda 0.15.0/0.15.2/0.15.3,no_reduce 需 MPI build;keff_trigger 0.15.0 FIRED→0.15.3 HELD,复用 omc_pre/omc) |
| E (源码编译) | scipy meson editable build,py3.12 + openblas | scipy complex-symmetric(unreleased fix 50951d25c,pre/post 源码编译) |
| F (源码编译) | micromamba omc_src,cmake+ninja Release,MPI/OpenMP,multi-group XS | openmc RotationalPeriodicBC(unreleased fix c7d7fa461,pre=parent 818fd11b1 / post=c7d7fa461,仅 C++ 改动) |
| G (源码编译) | micromamba omc_src,cmake+ninja Release,continuous-energy ENDF/B-VIII.0 U235 via NJOY | openmc IFP adjoint-weighted kinetics(unreleased fix 767db7e6a/#3580,pre=parent 66e7d863 / post=767db7e6a,仅 C++ 改动;CE U235 + 6 延迟群数据 on-box NJOY 生成) |
| H (源码编译) | uv venv py3.12,openmc editable 纯 Python install(numpy/scipy/h5py/uncertainties/endf),openmc.lib 经 READTHEDOCS=True 强制 Mock(C++ libopenmc.so 未 build,DummyOperator depletion 路径不调用 C++) | openmc CRAM 负密度 clip(a1df5842e→1f7ac4215;depletion/burnup 纯 Python 数密度轨迹,无需核数据) |
| I (源码编译) | deepxde git worktree(/tmp/dde_wt_pre @ 9d9d0b0 / post @ 46e2c2e)+ 逐 commit pip --no-deps install,py3.11 + CPU torch/jax | DeepXDE forward-mode Hessian 自伴(9d9d0b0→46e2c2e,fix 首入 released v1.10.1;forward-mode 须显式 import,非默认路径) |

## E. 诚实标注(贯穿)

- **FIRED 类型**:20 个 in-scope 中 6 个 crash-type(3 scipy lsoda/banded/eigh + 2 DeepXDE neumann/periodic + openmc keff_trigger fatal_error,follow-up 合法输入崩溃→违反 MR 关系)、11 个纯数值违反(scipy complexsym、scipy akima、scipy fht 边际、pyscf smearing 14 vs 13、pyscf D2h orbsym 1/6 对、openmc normalize、openmc no_reduce、openmc ifp_adjoint beta_eff 687.4→498.7 pcm、openmc cram_clip min N=−5.8e-2、DeepXDE boundary_float32 漏判、DeepXDE forward-mode Hessian J-col 6.185)、2 个收敛/自洽(pyscf DIIS 0/5→5/5、DeepXDE resample 5→0 重采样)、1 个 transport 失败(openmc rotperiodic 丢粒子)。
- **稀缺元模式 / 族**:**$\mathcal T^*_{\mathrm{rev}}$(e Trev·rec)全四域结构性稀缺**(scipy 无 symplectic 积分器、openmc 无可逆动力学基底、pyscf rt-TDDFT 已 v2.0.0 移出主仓 + BOMD velocity-Verlet 构造可逆、DeepXDE 无时间步进积分器;见 `NEGATIVE_{openmc,pyscf,deepxde}_trev.md`);scipy a G·eqv 由 fht(170f9e69a/gh-21661)**边际**填补(scipy 自带 test_gh_21661,信号 edge-dominated 7.2e16 量级,干净候选仍稀缺);scipy f O≤·stat 已由 Akima 两点线性(ef7437afc)升级为 in-the-wild;pyscf c T\*·sa Fock-Hermitian 构造保证(需 int-DM 边界)、pyscf f O≤·stat 占据/密度/变分界构造保证(负结果,git 考古 8 候选全排除,见 `results/NEGATIVE_pyscf_o_le.md`);DeepXDE c T\*·sa 由 forward-mode Hessian(46e2c2e)填补但 **△ reachability**(非 public 默认路径)。
- **实证 gap**:g(𝒟\* 形状/Sturm 振荡 overshoot)、i(ℰ\* 精度-阶退化)两族 B1 未测——须补真实缺陷或显式标注。
- **不可达(已解决)**:OpenMC/OpenMOC 无 PyPI(需 conda+核数据,Tier-C);unreleased fix(openmc rotperiodic、scipy complexsym)经源码编译 pre/post 闭合。
- **样本量**:n=20 论文 SUT 域(含 2 个 caveated:fht a 边际、forward-mode Hessian c reachability),underpowered for α=0.05(C6),descriptive 证据。
- **覆盖规律**:真实 bug 在数值算法库(scipy)富集,在构造保证物理库(pyscf 的 c/f、各域 Trev\*)稀缺;b G·cons 守恒/计数不变量有真实数值 bug。
