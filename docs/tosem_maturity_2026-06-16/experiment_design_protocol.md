# 实验方案设计(NOETHER,IBT-centered)— 预注册式协议

> 角色:IST 资深审稿人推进。范围:为再定心后的 NOETHER(核心 = 算子代数 → MR 推导,
> 由 IBT 承担非平凡性)设计**可证伪、预注册式**实验。RQ/假设在数据分析前固定(防 HARKing)。
> 已落地证据见 `supplementary/S10_noether_homefield/`;**正文 `.tex` 不在本文改动范围**。
> 理论侧采纳 **Option B**(每等价类一 MP;见 `constructmp_step34_revision_B0.md` 决策记录)。

---

## 0. 实验须确立的命题(对应论文主张)

| 命题 | 来源 | 类型 |
|---|---|---|
| 核心:MR 集是算子代数的可计算函数(推导有预测力) | §1 + §3 | 定性 + 跨域 |
| L1 block-occupancy 律 | §5.1 | 跨域,可证伪 |
| IBT-G / IBT-T\*(紧:核 = 恰好保对称故障) | §3.4 定理 | 形式 + FA 实证 |
| IBT-1(单块结构不完备) | 推论 | 实证 |
| IBT-2(联合核平凡 ⇒ 完备;union 趋完备) | 推论 | 实证(paired) |
| IBT-3(微分 oracle 核 = 共模故障,与 MR 互补) | 推论 | 实证(paired) |
| L3 detectability floor δ | §5.3 | 实证 + 敏感度 |
| 边界:Thm1′ 在 $\mathcal{A}_{\mathrm{PWR}}$ 证伪(5 维) | §3.6 | 构造性反例 |

---

## 1. 研究问题与 ex-ante 假设(预注册)

- **RQ1(L1)**:NOETHER block 占据是否为 program-family 不变量、可在测试前预测?
  **H1**:占据由 PDE 类决定——可逆系统 ⟹ $\mathcal{T}^{*}_{\mathrm{rev}}\ne\varnothing$;耗散 ⟹ $\mathcal{T}^{*}_{\mathrm{rev}}=\varnothing$;
  有守恒律 ⟹ Conservation$\ne\varnothing$。**Falsifier**:某耗散 SUT 有合法 $\mathcal{T}^{*}_{\mathrm{rev}}$ MR。
- **RQ2(IBT 紧,G/T\*)**:对称 MR 的检测核是否**恰好** = 保对称故障?
  **H2**:FA 下 $\ker=\{$compatible$\}$(rank 检验确认)。**Falsifier**:FA-忠实测试检出某保对称故障。
- **RQ3(IBT-1)**:单块 battery 是否漏其保结构故障?**H3**:是(equivariance MR 漏 speed/均匀系数)。
- **RQ4(IBT-3)**:微分 oracle 核是否 = 共模故障,且与 MR **交叉**(非嵌套)?
  **H4**:微分漏共享算子(共模)故障、抓 impl-specific;paired McNemar 的 $b,c>0$。
- **RQ5(IBT-2)**:互补核 oracle 合并是否趋完备?**H5**:$K_{\mathrm{MR}}\cap K_{\mathrm{diff}}\to\{\theta^{*}\}$,union > 各自。
- **RQ6(L3)**:是否存在硬下限 δ,低于它的故障在 FP=0 下不可微分检出?
  **H6**:签名 $<\delta$ 的故障在任何无假阳容差下漏检。
- **RQ7(边界)**:绝对完备(Thm1′)是否为假、障碍可代数刻画?**H7**:PWR 上假,5 个独立扩展维。

---

## 2. 实验单元(SUT)、故障模型、oracle

- **SUT(9,跨 thermal/fluid/reactor)**:heat / wave / poisson / advdiff / radxfer / grayscott /
  detonation / combustion / pincell。其中 **heat / wave / poisson 自包含(纯 numpy,无 T2、无 LLM)**
  —— 作为**抗 shared-corpus 质疑的核心证据**;advdiff / radxfer / grayscott 为 live 双实现。
- **故障模型**:operator-implementation 变异(Def 1;IBT 取线性故障类);每 SUT 含
  `baseline_control` 用于 alignment gate。
- **Oracle 三类**:(a) 代数-MR battery(逐块);(b) 中立跨实现微分 oracle;(c) FA rank 检验
  (精确线代,验 IBT 紧性)。

---

## 3. 度量

| 度量 | 用于 RQ |
|---|---|
| M-yield;M-block(块占据)| RQ1 |
| M-detect + Wilson 95% CI;per-block;per-fault-class | 全 |
| paired McNemar(MR vs 微分)+ $b/c/both/neither$ | RQ4, RQ5 |
| FA rank(test vs dense)+ 核 dim vs 解析值 | RQ2 |
| detectability floor δ + 容差敏感度(各 τ 的 FP)| RQ6 |
| alignment gate(baseline 全存活)| 全(可信度门) |

---

## 4. 统计分析与功效(诚实优先)

- **per-SUT 检出率为描述性**(小样本、underpowered),**不作头条**;结论由
  (i) 跨 SUT 结构律(L1:9/9 零例外)、(ii) paired McNemar、(iii) **精确** FA rank 承担。
- **功效**:paired McNemar 需 ~30 discordant pairs 才单独显著。现状:grayscott $p=4.4\times10^{-3}$、
  radxfer $p=7.3\times10^{-4}$ 已显著;**advdiff $p=1.0$ 欠功效**。计划 N3:跨 SUT **分层合并**
  discordant pairs(Cochran–Mantel–Haenszel)或扩故障池,使 RQ4/5 达推断级。
- **多重比较**:全 RQ 报告;per-SUT paired 检验做 **Holm** 校正。
- **预注册**:本文 RQ/假设固定在先;**全部结果报告**(含 pincell ALIGNMENT-FAIL、advdiff $p=1.0$)。

---

## 5. 已完成 vs 待补(gap 分析)

**已完成(S10,已并入 main)**:
- L1:9 SUT 块占据(唯 wave 占 $\mathcal{T}^{*}_{\mathrm{rev}}$,耗散全空);
- IBT-3:advdiff/radxfer/grayscott 三 SUT paired(共模漏检 radxfer abs/scat/src 0/18、grayscott feed/reaction 0/12);
- FA rank:G、T\* 紧(核 dim = circulant N / 对称阵 N(N+1)/2);逐块分类(O≤/T_rev\*/L\* 线性机制外);
- L3:advdiff δ=0.185、τ 敏感度(FP=0 至 1.5δ);
- 边界:PWR Thm1′ 反例(正文 §3.6)。

**待补(本协议新增任务)**:
- **N1(Option B 必需)**:逐域报告每块 $\sim_s$ **类数**($\mathcal{A}_{\mathrm{Boltz}}/\mathcal{A}_{\mathrm{equi}}/\mathcal{A}_{\mathrm{rel}}$);
  确认 G 块 $\ge 2$ 类(SO(3) 旋转 vs 反射/parity)→ 锚定 B、证伪 C 假设。**可由结构枚举给出。**
- **N2(抗 shared-corpus,审稿 Blocker)**:对一组 NOETHER 推导的 MR 做**独立人类双评者** κ
  (≥2 评者,目标 κ≥0.7),protocol 见 `protocol_humanKappa.md`。**需人力。**
- **N3(功效)**:跨 SUT 合并 discordant pairs 使 paired McNemar 达显著(CMH 分层)。**可计算。**
- **N4(紧性接地真 solver)**:在一个真实 SUT 的算子参数化上跑 FA rank(超出抽象 $\mathbb{R}^{N\times N}$),
  把 IBT 紧性绑定到实际 solver 故障空间。**可计算。**
- **N5(防循环的迁移性)**:在一个 NOETHER **未参与推导**的域上跑 CONSTRUCT-MP,由该域专家
  评估是否识别出先前未知 MR。**需新域 + 专家。**

---

## 6. 效度威胁与缓解(Reviewer-2 / ARS)

| 类别 | 威胁 | 缓解 |
|---|---|---|
| Construct | 用检出率代结构主张 | 头条用定性律(L1/IBT);率退完整性 |
| Internal | 容差/离散 floor 混淆缺陷 | R2/§10.2 交叉引用;a-priori 容差;alignment gate |
| External | 9 SUT 限教科书 PDE 域 | scope precondition 明示;N5 域外 SUT |
| Selection-on-response | 只报显著 | 预注册 RQ;**全报**(pincell FAIL、advdiff p=1.0) |
| Shared-corpus / LLM 循环 | 推导与评估共语料 | 自包含 heat/wave/poisson + 中立微分 oracle + 人类 κ(N2) |
| 功效不足 | 单 SUT n 小 | 跨 SUT 结构律 + 精确 FA rank + CMH 合并(N3) |

---

## 7. 优先级与执行序

| 优先 | 任务 | 性质 | 阻塞 |
|---|---|---|---|
| P1 | N1 ∼_s 类数枚举(锚定 B) | 结构枚举 | 无(可即做) |
| P1 | N3 CMH 合并 paired McNemar | 计算 | 无(数据已在) |
| P2 | N4 真 solver FA rank | 计算 | 需算子参数化 |
| P2 | N5 域外 SUT 迁移 | 新实验 | 需新域 |
| P3 | N2 人类 κ | 人力 | 需第二评者 |

**建议下一步**:先做 **N1 + N3**(纯计算/枚举、无需外部资源),把 Option B 与 RQ4/5 的
推断级证据补齐,再进 B1(§1/abstract 再定心)与 §3.4/§5 落正文。
