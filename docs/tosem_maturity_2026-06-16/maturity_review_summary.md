# NOETHER — TOSEM 投稿成熟度评估(独立重审)

> 日期:2026-06-16 · 主稿:`NOETHER_paper_arxiv.tex` · 目标:ACM TOSEM
> 方法:6 个互相隔离的 Claude Opus subagent 独立评审(EIC + R1 形式理论 + R2 实证 + R3 相关工作 + Devil's Advocate;另 1 个盘点外部 P4 仓库)。**非多厂商交叉**(会话内无外部 LLM 网关时的实现)。

## 综合裁决:Major Revision(逼近 R&R)

| 审稿人 | 评分/100 | Verdict |
|---|---|---|
| EIC | 48 | Major → R&R |
| R1 形式理论 | 60 | Major |
| R2 实证统计 | 62 | Major |
| R3 相关工作 | 72 | Major |
| Devil's Advocate | 38 | Major(逼近 Reject) |

**与仓库 Round-4 自评的分歧**:`docs/review_round_polish/round4/tosem_compliance_audit.md` 判 Accept / 接受概率 65–75% / 0 major / 0 critical。本次 6 个全新隔离实例独立重审,共识地把多项"被自评判为 minor"的项重判为 major/blocker。乐观自评源于同一团队迭代(确认偏误);按 §10(ARS)+§6(诚实),以更严的独立结论为准。

## 多厂商交叉验证(.env 网关,2026-06-16)

经 `.env` 网关用 5 个不同厂商模型独立重评(中性材料包,**未**告知 Opus panel 结论以免锚定);原始结果 `gateway_panel_raw.json`。

| 模型 | 厂商 | 评分 | Verdict |
|---|---|---|---|
| gpt-5-chat-latest | OpenAI | 38 | Reject |
| grok-4.1 | xAI | 32 | Reject |
| deepseek-v3.2-exp | DeepSeek | 55 | Major |
| qwen3-max-preview | 阿里 | 58 | Major |
| kimi-k2.5 | Moonshot | 58 | Major |

**两套完全独立的评审系统(Claude Opus ×5 + 多厂商 ×5)得出几乎相同的 blocker 清单与 Major/Reject 裁决**,与仓库 Round-4 自评(Accept)形成稳健反差。多厂商一致 blocker:
1. 实证薄弱 / 大量 deferred 到 protocol(只 1/3 域有 head-to-head)— 5/5
2. 理论内核平凡(Thm 1 by-construction、Thm 2 union-find)— 4/5
3. 缺独立人类 κ,依赖共享语料 LLM — 3/5
4. 与 companion(NP-hard MR-subset)无区分 — 3/5(独立确认 salami 风险真实可见)
5. related work 仅 4 行 / 三域 overclaim — grok+kimi+deepseek
一致认可优点(5/5):Thm 1′ 证伪的诚实性、算子代数 framing 新颖、边界声明清晰。

## 已 grep 核实的硬事实(区别于审稿主观判断)
- ✅ head-to-head 落败:L1666/L1702/L1726 — Set N=26 vs Set G=40,Δ=−14,McNemar p=0.0043(pooled)/0.019(D1)。
- ✅ reviewer-process 残留(原 L311/1328/2139/2414)——**已于 2026-06-16 在主稿删除**(本次安全修订)。投稿版(`submission/TOSEM_*`、06-16 zip)尚未同步,见 NEXT_STEPS。
- ◐ block 计数:正文 "7 canonical + 1 relational = 8 / candidate ninth" 自洽;Appendix `O(7)`、C.5.2 "eighth vs ninth" 混用(R1 指出,未逐行复核)。

## 分级不足清单

### 🔴 Publication Blocker(≥2 审稿人共识 / 已核实)
1. 理论内核偏平凡 + 最强定理(Thm 1′)被自己证伪(R1+DA);Theorem 1 自承 by-construction、Theorem 2 = union-find;R1 另指 CONSTRUCT-MP Step 3/4 类型不自洽(L529-530)。
2. 唯一真实 head-to-head 主方法被 baseline 显著击败(EIC+R2+R3+DA,✅),框架以 per-block/cost-axis/D2 四层叙事规避 → 价值命题悬空。
3. 缺独立**人类** inter-rater κ(R2+DA);κ=1.000 来自共享语料多 LLM,近"同一评分者投三票"。
4. 与姊妹论文 T2(Minimum-MR-SubSet,据仓库记录已上 arXiv、投 TSE)的 venue-overlap / salami **未作任何声明**(EIC) — ethics/policy 硬门槛。
5. 大量经验主张是 protocol(未执行)而非 result;"three domains tested" overclaim(EIC+R2)。

### 🟠 Major
6. ~~reviewer-process / 版本化残留 4 处~~ — **主稿已修(2026-06-16)**;投稿版待同步。
7. 75 页超 TOSEM 30–50 推荐,膨胀主因为自评/边界框(EIC+DA)。
8. 相关工作与 Ying 2025 单向区分 + "三问无人回答"过强(R3) → 需双向覆盖矩阵。
9. Java 实验对象从 Sun 2021 prose 重实现而非原始源码,重实现者即框架作者(R2)。

### 🟡 Minor
- 标题/摘要 "constructive discovery / provable" 偏强;"ten Translate dimensions" 中 5 个仅 by-inspection;§7.3 artefact 声明缺 S5–S9;Appendix `O(7)`。

## 未执行项(诚实声明)
- 100% 联网逐条 bib 真实性校验(Stage 2.5/4.5)本轮**未执行**。
- 多厂商交叉评审**已完成**(网关 5 厂商,见上"多厂商交叉验证"节)。
