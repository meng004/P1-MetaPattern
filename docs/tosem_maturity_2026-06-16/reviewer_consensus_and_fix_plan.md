# Reviewer 意见汇总 + 根因分析 + 修复方案

> 2026-06-16 · Reviewer 池 = 15 个独立实例 × 3 轮:
> 轮1 Claude Opus panel(修复前,5):EIC / R1 形式理论 / R2 实证 / R3 相关工作 / DA
> 轮2 多厂商网关(修复前,5):gpt-5 / grok-4.1 / deepseek / qwen / kimi(`gateway_panel_raw.json`)
> 轮3 多厂商网关量化(修复后,5):同上 5 厂商(`gateway_quant_raw.json`)

## A. 按意见分组(注明持有 reviewer 数)

| # | 意见主题 | 持有数 | 分布(轮1/轮2/轮3) | 状态 |
|---|---|---|---|---|
| G1 | 实证评估不足:仅 1/3 域有执行 head-to-head;唯一中立 head-to-head 中 Set N 被 baseline 显著击败(p=0.0043);METRIC+/MR-Scout/第三厂商比较仍是 protocol;关键统计欠功效 | **14/15** | 4 / 5 / 5 | 🔴 未解 |
| G2 | 相关工作单薄/定位不足:related work ~4 行;与 Ying 2025 单向区分;"三问无人回答"过强 | **10/15** | 1 / 4 / 5 | 🟠 部分(已加 differentiation 段) |
| G3 | 理论内核平凡:Thm 1 by-construction、Thm 2 union-find;最强定理 Thm 1′ 被自证伪;CONSTRUCT-MP Step 3/4 定义歧义 | **8/15** | 2 / 4 / 2 | 🔴 未解 |
| G4 | 篇幅 73–75pp 超 TOSEM 30–50 推荐,贡献密度不匹配 | **7/15** | 2 / 1 / 4 | 🟠 未解 |
| G5 | 缺独立人类 κ:κ=0.857/1.000 来自共享语料 LLM,非独立人类信度;30 条 Set-N MR 单作者推导 | **5/15** | 2 / 3 / 0 | 🟠 已声明、未补人类 κ |
| G6 | 与姊妹论文 T2(NP-hard MR-subset)salami/venue-overlap 未声明 | **4/15** | 1 / 3 / 0 | ✅ 已修(differentiation + cover letter 披露) |
| G7 | overclaim:三域"已测"、ten dimensions、constructive discovery、C3 "predicts two" | **3/15** | 2 / 1 / 0 | ✅ 已修 |
| G8 | 上游 8-block 充分性未证 / "constructive discovery" 名不副实(上游仍人工归纳) | **3/15** | 2 / 1 / 0 | 🔴 未解(定位问题) |
| G9 | Java subjects 从 Sun 2021 prose 重实现、重实现者即框架作者 | 1/15 | 1 / 0 / 0 | ✅ 已在 threats 声明 |
| G10 | artefact 可用性声明缺 S5–S9 | 1/15 | 1 / 0 / 0 | 🟠 待补 |
| G11 | reviewer-process / 版本化措辞残留 | 1/15 | 1 / 0 / 0 | ✅ 已修 |
| G12 | Appendix block 计数 O(7) / eighth-ninth 不一致 | 1/15 | 1 / 0 / 0 | 🟡 待修 |

## B. 根因分析(为什么会出现这些意见)

- **G1 + G8(实证薄 + 上游人工)同源**:论文是"理论框架先行,实证后补"。框架最关键一步(从程序蒸馏算子代数 + 8-block)仍是人工归纳;下游算法虽机械,但唯一执行的中立 head-to-head 用了对自己不利的 SOTA 基准且输了,于是把价值命题改用 per-block/cost-axis/D2 叙事承接。**根因:框架的工程价值命题尚未被任何中立、真实缺陷上的正面证据支撑。**
- **G3(理论平凡)根因**:真正有数学深度的强定理(Thm 1′ 绝对完备)被作者自己证伪;剩下的 Thm 1 是 by-construction 闭包、Thm 2 是标准 union-find。论文真实智识增量是"重新奠基/系统化",但标题与摘要卖的是"constructive discovery + provable",**主张与实质错配**。
- **G2 + G4(related work 薄 + 篇幅长)同源**:75 页篇幅大量投在理论铺陈、负面结果(Thm 1′ 证伪)的逐块精细排除、以及反复的自评/边界框;related work 被压到 4 行。**贡献密度低 + 定位投入不足**。
- **G5(κ)根因**:用多 LLM 替代人类第二评者(成本/便利),但三模型共享预训练语料使一致性虚高(κ=1.000 几乎不可能来自真正独立评分者)。
- **G6 + G7(salami + overclaim)根因**:同一研究项目拆成 generation(本文,TOSEM)与 selection(T2,TSE)两篇却未交叉声明;摘要措辞("tested on three domains"、"ten dimensions")超出实际执行/证明强度。**已通过文本修复解决。**

## C. 修复方案(分级 + 次序 + 理由)

### 已完成(✅,2026-06-16 本会话)
| 意见 | 修复 | 理由 |
|---|---|---|
| G6 | §2 插 differentiation 段 + cover letter 披露 | salami 是 ethics 硬门槛,零成本必做;引用+划界而非搬运 T2 硬理论(否则升级为自我抄袭) |
| G7 | abstract 三域分级、ten→5+5、C3 去 predicts | 措辞与证据对齐,消除 overclaim |
| G9/G11 | threats 加 Java 重实现声明 + 删 reviewer-process 残留 | 诚实化;§6.5/§8.3 硬约束 |

### 文本可修(立即可执行,我可做;高 ROI)
| 意见 | 方案 | 理由 | 量化增益 |
|---|---|---|---|
| G2 | 用 `protocol_relatedWork.md` 真实文献候选扩 §2 + 加"prior work × origin/closure/transferability"双向覆盖矩阵 | related_work 3.6 是最低维度;文献是共享资源、低 self-overlap | ≈ +3.4 加权分 |
| G4 | 合并重复 boundary box、protocol 段下放 supplementary、压至 ≤50pp + cover letter 篇幅辩护 | 贡献密度问题,删冗余非删论点 | ≈ +1.3 |
| G8(定位) | 标题/摘要从 "constructive discovery" 重定位为 "systematisation/re-grounding"(候选见 `overclaim_revision_draft.md`) | 让主张匹配实质,化解 G3/G8 错配——**属作者决策,需你拍板** | 间接提 novelty/soundness |
| G10/G12 | §7.3 补列 S5–S9;Appendix 统一 O(8)/ninth | 低成本合规修订 | 小 |

### 需真实研究(不可代执行,已出协议,你执行)
| 意见 | 方案 | 理由 |
|---|---|---|
| G1 | 按 `protocol_realDefect.md`:在中立、非按块设计的真实缺陷(e3nn/PyTorch Geometric 已确认 bug、Defects4J)上取得 Set N 正面证据 | 这是接收的**核心瓶颈**(evaluation_rigor 权重 0.20);不补则价值命题悬空,纯文本无法过线 |
| G3 | 按 `protocol_theory.md`:补非平凡定理(如 Composite-Translate 保闭包+多项式时间),或诚实重定位论文类型 | 需作者数学判断,不可由 agent 代证 |
| G5 | 按 `protocol_humanKappa.md`:自招 ≥2 名独立人类 rater 做 Cohen/Fleiss κ | LLM κ 不能替代;construct validity 的根 |

### 次序(理由:先零成本高杠杆,再硬骨头)
1. G2 + G4 + G10/G12(文本,立即)→ 成熟度 ~62→67(文本上限);
2. G8 重定位(需你拍板标题)→ 化解 G3/G8 主张错配,间接提分;
3. G1(实证)+ G3(理论)+ G5(人类 κ)(研究)→ 逼近接收线 78。
**量化硬结论:G1/G3 不解决,纯文本修复触顶 ~67,无法达 TOSEM 接收线。**
