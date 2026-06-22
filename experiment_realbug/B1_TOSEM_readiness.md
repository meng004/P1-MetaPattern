# B1 TOSEM 投稿就绪评估 (2026-06-22)

> 内部诚实评估文档(Reviewer-2 / ARS 视角)。基准模型 = `UNIFIED_BLOCK_MODEL.md`
> (5 元模式 → 10 MR 族 a–j)。本文盘点 40-格覆盖、列致命/严重弱点、给 TOSEM 充分性
> 判断与 §Threats 草拟(可粘贴入正文)。**定位:理论为主轴,B1 为多域适用性佐证。**

## A. 40-格覆盖状态表(10 族 × 4 域)

图例:✓ 干净正例 / △ caveated 正例 / ✗c 构造保证负 / ✗s 底座缺失负 / — 空(未追,非负非 gap)

| 族 (fault 类, Mode) | scipy (pde_num) | pyscf (qchem) | openmc (reactor) | deepxde (pde_sciml) |
|---|---|---|---|---|
| a G·eqv (取向依赖, I) | △ fht 170f9e69a | ✓ D2h 4542fe9b | ✓ normalize 3bf1486f4 + rotperiodic c7d7fa461 | ✓ periodic 8353540 |
| b G·cons (守恒荷泄漏, I) | — | ✓ smearing ebf4e676 | — | ✓ Neumann 4bac5eb |
| c T\*·sa (对称非对称处理, I/M) | ✓ eigh 178a12572 + complexsym 50951d25c | ✗c Fock-Hermitian | — | △ Hessian 46e2c2e |
| d T\*·dual (伴随误算, M) | — | — | ✓ IFP 767db7e6a | — |
| e Trev·rec (注入耗散, I) | ✗s | ✗s | ✗s | ✗s |
| f O≤·stat (值越界/非单调, I) | ✓ Akima ef7437afc | ✗c 占据/变分界 | ✓ CRAM 1f7ac4215 | ✓ boundary 8a644fe |
| g O≤·dyn 𝒟\* (伪振荡/overshoot, I) | ✗c PCHIP 构造单调 | ✗ | ✗ | ✗ |
| h L\*·conv (不收敛/不自洽, I) | ✓ LSODA c374ca7fd | ✓ DIIS 15920e60 | ✓ keff b54de4d76 | ✓ resample 4adcde7 |
| i L\*·acc ℰ\* (精度阶退化, M) | ✓ simpson 572a373a | — | — | — |
| j L\*·rep (表示/并行分歧, M) | ✓ banded cb0538877 | — | ✓ no_reduce bd76fc056 | — |

**统计**:40 格 = **19 正(含 2 caveated)+ 10 有据负 + 11 空**。21 个 in-scope 缺陷分布 8 族:a×5、b×2、c×3、d×1、f×3、h×4、i×1、j×2。证据程序:scipy 7、openmc 6、deepxde 5、pyscf 3;另跨域 e3nn/pyg 3、受控 mutant 2;负结果 5 份(openmc/pyscf/deepxde Trev + pyscf O≤ + scipy 𝒟\*)。

**FIRED 类型分布(判别力)**:6 crash + 12 纯数值(含 2 caveated:fht 边际、Hessian reachability)+ 2 收敛 + 1 transport。⟹ **结构判别力充分的强证据 ≈ 13 条**(10 纯数值非 caveated + 2 收敛 + 1 transport);crash 6 条判别力弱(通用测试亦可捕获)。

## B. 优势(可信度加分)

1. **4 个真实第三方库 × 4 个论文 SUT 域**,全部 git-history 真 SHA + pre FIRED→post HELD 自跑核验,作者未介入缺陷生成。
2. **8/10 族有 in-the-wild 正例**;h(L\*·conv)满四域。
3. **5 份有据负结果 + 构造保证⟹稀缺的覆盖规律**:框架不仅预测"有",也预测"无"(Trev\* 无可逆基底、𝒟\* PCHIP 构造单调、pyscf c/f 构造钳制),**falsifiable,是理论可信度而非缺口**。
4. **Mode I/M 区分 + 相对 oracle 处置**(版本闭合 + control 定位)形式化清晰。

## C. Reviewer-2 最严苛清单(投稿前须认领)

| # | 问题 | 等级 | 处置 |
|---|---|---|---|
| R1 | **n=21 欠功效**,无 α=0.05 confirmatory(McNemar b+c=0/1);P4 要求 n≥30 不达 | 严重 | 全程标 descriptive/underpowered(C6);confirmatory 主张下放 |
| R2 | **无对照基线、无 effectiveness**:只证"能检出",未证比 expert/GenMorph/search MR "更广/更强" | 致命(若按效果论文读) | 重定位为 applicability 存在性;effectiveness 靠 Java head-to-head |
| R3 | **6/21 crash-type**,MR 结构判别力未展示(smoke test 亦可捕获) | 致命(诚信) | 单列 6 条,主计数以 ≈13 强证据承载 |
| R4 | **回溯选样 → HARKing/optional stopping**(每族搜到一个为止,未预注册) | 严重 | 方程驱动先验导出 + 5 负结果作缓解,§Threats 显式认领 |
| R5 | **格子稀疏**(19/40 正,b/c/d/i/j 多单域),主要 a/f/h 撑 | 中 | 承认补丁式覆盖,非稠密网格 |
| R6 | **2 族零正例 + 2 caveated**:强证据约 13 条 | 中 | 2 族零正例转为"构造性负=理论预测"正资产 |
| R7 | **可复现负担高**(5 源码编译,openmc 需 conda+核数据 Tier-C) | 中 | 提供 env-class 栈 + repro 脚本;承认非 pip-clean |
| R8 | **族独立性仅 witness 论证**,无正交性定理/最小检测子集/人类 κ | 中 | 列 future work(P3 人类 κ、P4 最小子集) |

（无更高级别致命问题被隐藏:R2/R3 一旦按"理论+佐证"定位并主动认领,即从 blocker 降为 acknowledged limitation。）

## D. TOSEM 充分性判断

**理论(载重,大概率够)**:算子代数分解 + CONSTRUCT-MP + Invariance-Blindness 定理 + 代数闭包/可判定性定理 + "归纳从 MR-实例下放到代数-块" + 本轮统一 5 生成元/10 族模型。**前提**:IBT 与闭包/可判定性证明无懈可击;Theorem 1′(绝对完备)开放须诚实框定为 scope。⟹ **达 TOSEM 量级**。

**实证(不足以独立支撑 effectiveness,合格作多域佐证)**:B1 作"跨 4 真实科学计算域的适用性存在性"合格且有亮点(诚实负结果 + 覆盖规律);但 n=21 欠功效、无 head-to-head、6 crash 稀释、2 族零正例。真正对照证据(commons-math Java pilot n=3 SUT/77 mutants)亦欠功效。

**净判断**:**以"理论/foundations + B1 多域适用性佐证 + 诚实负结果"定位 → 可冲 TOSEM;以"实证 effectiveness"定位 → 不够。** 三大致命问(R2 无效果对照、R3 crash 稀释、R4 回溯选样)须在 §Threats 主动认领。

## E. 最低限度补强(按性价比)

1. **重定位**:正文把 B1 写成 applicability corroboration / existence-across-domains,每格 = 一个 IBT 实例,**不碰 effectiveness 措辞**;n=21 全程 descriptive。
2. **crash 诚实处置**:6 条单列,主计数 ≈13 强证据。
3. **做实 Java head-to-head**(哪怕 n 小)——唯一支撑"更广/可复用"的对照;reactor 侧外部迁移作 future work。
4. **2 族零正例转正资产**:Trev\*/𝒟\* in-the-wild 稀缺 = 框架预测的构造保证后果,与 pyscf Fock-Hermitian/占据界同列。
5. confirmatory 一律下放或扩至 n≥30;最小 MR 子集(P4)+ 人类 κ(P3)列 future work。

## F. §Threats-to-Validity 草拟(paste-ready, English)

> **Construct validity.** The B1 corpus evaluates *applicability* (whether algebra-derived MR families correspond to faults that actually occurred in deployed scientific-computing libraries), not fault-revealing *effectiveness*. We make no superiority claim over expert-authored, GenMorph, or search-based MRs from B1; the only head-to-head effectiveness evidence is the small commons-math Java pilot (n=3 SUTs, 77 mutants), itself underpowered. Of the 21 in-scope faults, 6 are crash-type follow-ups detectable by a generic smoke test; the MR's structural discriminating power is therefore carried mainly by the ≈13 non-crash, non-caveated numeric/convergence violations, and we report the crash subset separately rather than folding it into the headline count.

> **Internal validity.** Faults were located retrospectively by git-archaeology, one representative per family, which risks optional stopping and HARKing. We mitigate by deriving each MR a priori from the governing-equation operator algebra (independent of the fault) and by reporting five evidenced negative results (Trev* across all four domains; PySCF O<=; SciPy D*), so the corpus is not a pure success-only selection. The family classification of the 21 faults was performed by the authors and an LLM panel (Fleiss' kappa = 0.857 on a related 18-MR audit, with a shared-pretraining caveat); an independent human inter-rater study is future work.

> **External validity.** Coverage is a patchwork, not a dense grid: 19 of 40 (family x domain) cells carry in-the-wild positives, with families b/c/d/i/j realized in a single domain each; the matrix is load-bearing on families a, f, and h. Two families (Trev* and D*) have no in-the-wild instance in any of the four domains. We argue these absences are predicted by the framework (time-reversal needs a reversible/symplectic propagator absent from steady-state/eigen/fixed-point/residual-minimizing solvers; dynamic-shape D* is constructively guaranteed by monotone-by-construction interpolants such as PCHIP and the absence of TVD/WENO substrates), i.e. present-by-derivation, absent-by-instance.

> **Conclusion / statistical validity.** With n=21 the study is underpowered for alpha=0.05 hypothesis testing (paired McNemar discordance b+c = 0 or 1); all B1 results are reported as descriptive evidence with Wilson 95% intervals, not as confirmatory tests. Confirmatory claims and the minimal-MR-subset question are deferred to future work at n>=30.

> **Reproducibility.** Five faults require source compilation (SciPy meson; OpenMC cmake/ninja with conda + nuclear data; DeepXDE worktrees) and OpenMC additionally needs conda + cross-section data (Tier-C runtime); these are not pip-clean. We release per-fault reproduction scripts and an environment-class stack (A–I) to make each closure independently re-runnable.

## G. 一句话结论

理论够 TOSEM;实证是"够格的多域适用性佐证、不够格的效果评估"。**论文必须以理论为主轴、B1 为佐证定位,并在 §Threats 主动认领 R2(无效果对照)/R3(crash 稀释)/R4(回溯选样);否则 Reviewer-2 会当 publication blocker。** 5 份诚实负结果与构造保证覆盖规律是把"覆盖缺口"翻成"理论可证伪性"的关键资产,应在正文显式呈现。
