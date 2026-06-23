# 工业资料评估：6 程序 + 可共用 MR 能否提升 NOETHER 1 区接收概率

> 日期：2026-06-20。来源：核安审中心 SACOS/SPARK/LOCUST 蜕变关系 + 华能耦合/热工/事故测试用例 + 需求分析报告。
> 方法：4-agent workflow `wf_5f23faf4-bb8` 逐字核源；**provenance 经作者澄清修正**（见 §4）。

## 1. 一句话结论

**价值显著、值得纳入**：这批资料同时给出 (a) 真实工业**非-order 多块 MR**（击破"全 order 单块"最致命批评）、(b) **6 程序 2 域 transferability**（强化 C4）、(c) **真正的开发/测试机构分离**（西交开发 + 作者第三方测试，破"作者自实现 substrate"自指硬伤）。**把实证硬墙从 likely-Reject 推向 Major-Revision 可生还，且 evaluation rigor 实质提升**。但 MR 识别/block 分类仍由作者（测试方）完成（独立人类 κ 仍需要），且**不开 1 区 novelty 门**（理论仍 reorganization）。

## 2. 6 程序盘点

| 程序 | 域 | MR 数 | block | 开发方 |
|---|---|---|---|---|
| SACOS | 子通道热工水力 | 46 | 全 order | **NUTHEL（西交核热工水力）** |
| SPARK | 堆芯中子扩散 | 36 | order + borderline（MR33-36 反应性系数；Fuel_heat 矛盾符号=隐含条件）| **NECP（西交核工程计算物理，吴宏春，Bamboo-C，PWR 100+堆年工业确认）** |
| LOCUST | 组件中子输运 | 28 | order + **真非 order（MR9-12 阈值条件、MR21-22 sensitivity）** | **NECP（同 Bamboo-C，与 SPARK 同团队同套件）** |
| 耦合 MULTI | 多尺度耦合热工 | 14 | 全 order | **NUSOL（西交）** |
| 热工 NTHERMIX | 热工水力设计 | 12 | 全 order | **NUSOL（西交）** |
| 事故 REP009 | 事故分析 | 18 | 全 order | **NUSOL（西交）** |

**论文作者（南华大学）= 独立第三方测试方**（核安审中心补充测试 / 华能委托测试）。

## 3. 最大发现（P0）：非-order 多块 MR，来自独立开发的 NECP 中子学程序

第 1 轮审稿最致命的技术批评是"SACOS 全 order 单块 / 多块只在作者自选 numpy 上"。**LOCUST 给出真实反例**（逐字）：

- **LOCUST MR9–12（条件/阈值，非 order）**：`Boron<阈值 AND TBoron↑ → Keff↑`；`Boron>阈值 AND TBoron↑ → Keff↓`。Keff 对慢化剂温度的响应**符号在硼浓度阈值处翻转**（MTC 符号反转）——两输入 guarded、regime-dependent，非单输入单调协变。
- **LOCUST MR21–22（sensitivity/导数，非 order）**：`Burn1<Burn2, ΔT 相同 → ΔKeff2>ΔKeff1`。固定 ΔT 比较反应性响应增量 ΔKeff 幅度跨燃耗态——导数排序。
- **SPARK MR33-36**（输出反应性系数 DTC/MTC=导数）+ Fuel_heat→CBC/TCout 矛盾符号（隐含 regime）——borderline 支撑。

**价值**：填"多块"缺口的真实工业证据，且来自**NECP 独立开发**的程序。直接中和"all-order single-block"批评。

## 4. provenance（作者澄清后修正）：开发/测试机构分离，破"自实现 substrate"自指

**workflow 误判更正**：workflow 据签名页"审查 李萌 / 批准 刘杰"判为"作者自评、自指未破"。**真实关系**：
- **被测程序（SUT）由西交 3 个独立团队开发**：NECP（SPARK/LOCUST）、NUTHEL（SACOS）、NUSOL（华能耦合/热工/事故）。
- **论文作者（南华大学）是独立第三方测试方**，对西交开发的程序做 V&V 独立测试、识别 MR。签名页"审查/批准"是**测试方内部**流程，非开发方。

→ 这是软件 V&V 的**标准独立测试 setup（测试方 ≠ 开发方）**，**破了论文最大的"作者自实现 Java subjects"自指硬伤**（对比现有 Path-A：作者自写被测程序，开发=测试=框架设计三合一）。**SUT 独立性是铁的，且是真实工业级程序**（Bamboo-C 已 PWR 100+堆年工业确认）。机构层面：开发方西交 + 测试方南华 = **两所不同高校的开发/测试分离**。

**仍诚实标注的残留**：
- **MR 识别由作者团队（作为独立测试方）完成**——V&V 标准做法，但仍是"提出 NOETHER 的同一团队识别 MR"；MT 领域通常认可测试方识别 MR，但不能宣称"MR 独立于框架设计者"。
- **block 分类**（哪个 MR 属哪个 NOETHER block）仍作者做 → 独立人类 κ 仍需要（分类信度，与程序/MR 来源无关）。
- SPARK+LOCUST 同 NECP 同 Bamboo-C，**不算两个独立 SUT 点**。
- 反应堆类型：华能 3 程序 HTGR（氦冷，2025 v1.x 新软件）vs SACOS/SPARK/LOCUST PWR（水冷）——跨堆型可比性须用 governing-eq（能量守恒）论证。

## 5. 怎么用（P0/P1/P2 + DO NOT）

- **P0（最高 ROI）**：meta-pattern 覆盖子节加 LOCUST MR9-12 + MR21-22（逐字含 guard 条件）作 taxonomy 覆盖**非 order 块的真实反应堆物理证据**；SPARK MR33-36 + Fuel_heat 矛盾作 borderline。击破"all-order single-block"。
- **P1**：Evaluation 把 corpus 从"1 程序 SACOS"改为"**6 程序 2 域、3 个独立开发团队**"；报 shared trio 跨 4 热工程序，绑定同一**能量守恒律**作 C4 transferability。
- **P2（独立性论证，Evaluation + Threats）**：明确写"**独立第三方测试方（南华）对 3 个西交团队独立开发的工业程序识别 MR**"——这是新的、强的独立性论点，破"自实现 substrate"。**紧接诚实承认**：MR 识别仍由测试方（=NOETHER 团队）完成、block 分类需独立人类 κ、未做完全独立复现、HTGR↔PWR caveat。
- **DO NOT**：① 宣称"MR 也独立于框架设计者"（MR 是测试方识别）；② 把 SPARK+LOCUST 算两个独立点；③ 把 non-order/breadth 放进 Abstract 主结果；④ 与姊妹论文/P1 salami（**引用非导入**共享 corpus，MR-count 表跨论文目的不同，MEMORY `noether-t2-salami-boundary`）；⑤ 暗示 HTGR↔PWR 可比性而无 governing-eq 论证。

## 6. 诚实风险

1. **novelty 不变**：仍 operator-algebraic reorganization；1 区若因 novelty 拒，加 corpus 救不了。
2. **MR 识别/block 分类仍作者方**：SUT 独立 ≠ MR 独立；独立人类 κ 仍是必需的另一条腿。
3. **仍 order 主导**：非 order 证据薄（LOCUST 4 条 + SPARK borderline）=existence proof 非分布覆盖；勿宣称 block 均衡。
4. **salami（中-高）**：与 P1（12-PUT audit）+ T2（TSE）边界重叠；NOETHER 用严格限于 operator-algebra 实例化 + block diversity，引用非导入。
5. **HTGR↔PWR 堆型不一致** + 华能 3 程序 2025 v1.x 新软件（不如 SACOS 工业确认成熟）。

## 7. 净效果 + 纳入建议

**净效果（修正 provenance 后高于 workflow 初判）**：这批资料破了论文**两个**实证硬伤——"自实现 substrate"（开发/测试分离）+ "全 order 单块"（LOCUST 非 order）——并强化 C4 transferability。实证维度从 likely-Reject 推向 Major-Revision 可生还、evaluation rigor 实质上移。**但**仍需独立人类 κ（block 信度）、仍不开 novelty 门。

**纳入建议：INCLUDE，优先级最高的扩张之一。** 它比 s5_aligned 更现成（MR 已识别、程序已工业确认），且独立性论证（开发/测试分离）是 s5_aligned（GenMorph benchmark）之外的另一条强腿。优先级：P0 非 order block diversity > P1 多程序 transferability > P2 开发/测试分离独立性论证（含诚实残留）。严格诚实 framing，不夸大为"MR 独立"或"完全外部验证"。
