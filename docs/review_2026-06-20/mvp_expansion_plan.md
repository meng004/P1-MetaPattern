# NOETHER 最小可信扩张（MVP）方案 — 冲 TOSEM 1 区

> 日期：2026-06-20。基于仓库现有实验资产 + 4-agent workflow（`wf_4a107dfc-15b`）+ 第 1 轮审稿缺口。
> 前提：用户决定走"补实验重投 TOSEM（中科院计算机 1 区）"；本方案定最小可信扩张。
> 诚实总判：做完完整 MVP，TOSEM 达 4-minor 诚实概率 **15%–30%**；更可能结局是第二轮 major + 再一轮 R&R。兜底回退 IST(2 区) MVP 资产仍净收益为正。

---

## 1. MVP 核心配置（回答三问）

**MVP 核心 = 完成 `experiment/s5_aligned`（已就绪、seed11 已验证、results/ 主目录待跑满）。**

| 三问 | 答案 |
|---|---|
| **第二个 SUT 选哪个最省力** | 不引入任何新 substrate——直接跑满 s5_aligned 已含的 GenMorph 公开 **23-subject benchmark**：Math 10 + **Lang 5** + Guava 8。三域在同一份 `run_all.sh`/同一发布 mutant 集/同一 seed 配置里，"第二、第三个 SUT 免费搭车"，零额外工程。中立外部 substrate（GenMorph 自己发表）直接化解 home-field/author-vs-author 批评。 |
| **跑通哪几环** | 四环，只有①耗时：①Stage1（Randoop+PIT per-subject，4–7h/seed，可断点续跑）；②Stage2/aggregate（`compare_sets.py`，<1s 出 ALL+三域四层 union-kill/Wilson95/McNemar）；③Set G baseline 环（**零 compute**，cp 上游 `mutants_killed.csv`，同 CSV 含多 seed 行）；④per-block/per-domain 分解（静态产物 + PLAN-002 effective-MR-ratio）。 |
| **量化 baseline 做哪种** | 三类，全部从已有数据零额外 compute 派生：(1) **single-seed Set G**（seed=11 严格基线）；(2) **multi-seed Set G**（12 seeds union，GP best-case 上界，上游 CSV 免费）；(3) **cost-normalized**（effective-MR-ratio = 有效 MR/总 MR + 每有效 MR 平均 kill，回应"71 条 vs 少量 GP MR 比总 kill 不公平"）。complementarity 由 McNemar 的 b/c 单元轻量呈现（Guava c_setn_only=16 vs b_setg_only=5）。 |
| **seed 数** | Set N 确定性（71 手写 MR 无 seed）；只 Stage1 substrate 侧需多 seed。**推荐 3 个 seed（11/12/13，与上游编号对齐）**，报均值+Wilson95 证稳健；最低 2 个。Set G 的 12-seed 上界上游免费，不重跑。不建议 Set N 铺满 12 seed（边际信息低、每 seed 4–7h）。 |

**seed11 实测信号（中立 benchmark，决定叙事）**：ALL 562 mutants — Set N 31.3% vs Set G 单 seed 36.3%（McNemar p=0.0066 **输**）vs Set G 12-seed 60.7%；**但 Guava 8-subj Set N 70.4% WIN vs 53%（p=0.027 显著）**，且 Set G 有 6 subjects 零有效 MR、Set N 兜底。→ 安全叙事 = **complementarity + 结构域占优 + 确定性 vs 多种子搜索成本**，不是"全面更强"。

---

## 2. 分阶段执行计划 + 算力/凭据/人力矩阵

| 腿 | 阶段 | 本地可做 | 需 GPU | 需凭据 | 需人力 | 时间 |
|---|---|---|---|---|---|---|
| **s5_aligned multi-seed**（中立 substrate 腿）| **MVP-must** | 否（云）| **否** | 云主机 egress 放行 zenodo/apt/maven；私有 GitHub repo 供云端 clone | 基本无（挂机）| Stage1 4–7h/seed + Stage2 30min；3 seed 约 1–3 天挂机 |
| **独立人类 κ**（block 信度腿）| **MVP-must** | **是** | 否 | 无 | **2 名独立 rater**（非作者、盲标）| 标注半天–1天/人；含招募 3–7 天 |
| 独立重实现 Path-A | phase2 | 否 | 否 | 无 | **1 名独立工程师**（仅凭 Sun 2021 散文重实现）| 1–2 周 |
| 中立 real-bug（e3nn/PyG）| phase2 | 否 | **是** | 开源免凭据 | 懂等变 ML 的工程师 | 1–3 周 |
| n5 工业多块（SACOS/LOCUST/SPARK）| optional | 否 | 否 | **核工业机构代码运行权限** | 内部人员跑算例 | 数天–2 周 |

**最小可信组合 = s5_aligned multi-seed（云算力）+ 独立人类 κ（纯标注）**。两腿同时落地，R2/R3 从 major 推向 minor 的核心条件首次同时满足（s5 解外部 substrate、κ 解独立人类信度）。real-bug/Path-A/n5 是 phase2 加分腿。

---

## 3. claim-ledger（实验 → 解锁 claim → 稿件影响 → reviewer → 残留）

| 实验 | 解锁 claim | 稿件影响 | reviewer major→minor | 残留 |
|---|---|---|---|---|
| **s5_aligned multi-seed** | complementarity（最强）+ 受限 EQ3；EQ1 从 author-vs-author 升级为中立 substrate 背书 | Results（commons-math 单 corpus → 多 corpus 分层）+ Abstract（complementarity 替 effectiveness 退避）+ EQ1/EQ3 reframe + Threats | R2/R3 → near-minor（外部 substrate 腿之一）；EIC payoff 部分缓解 | MR 来源仍作者两方；block 信度墙未动；ALL/Math/Lang 仍输需如实报 |
| **独立人类 κ** | C4 construct validity（分类可被独立复现）| Method block-label 协议（LLM-κ 下放）+ Results 信度 + Threats + Appendix | R2/R3/EIC 三方硬墙第二腿；两腿落地后核心 minor 条件首次同时满足；EIC construct-validity experiment 要求清除 | 只证可复现非有用；rater 质量风险；若 κ<<0.931 反噬须诚信弱化 C4 |
| n5 工业多块（optional）| 多块 MR 工业可执行存在性；补强 IBT/scope | Evaluation 工业 case（SACOS 单块→多块可执行）+ Scope + Threats | R3 加固 + EIC scope 边际 | **非中立第三方（不可宣称独立腿）**；MR-PASS 非 real-bug；机构访问限复现 |
| real-bug e3nn/PyG（phase2）| 唯一解锁 EQ3 真效力（杀中立 real-bug）| 跑则 Evaluation real-bug 子节 + Abstract effectiveness 结论；不跑则 Threats 锁定 definitional | 纳入则 R2/R3 near-minor→minor（补自指墙最后一块）| 不跑则 EQ3 effectiveness 永远 definitional |

---

## 4. 你必须提供的清单

**MVP-must：**
1. **一台 Ubuntu 云主机**：≥30GB 磁盘、容忍长任务、egress 放行 `zenodo.org`+apt+Maven Central；**无需 GPU**。
2. 把本地 `experiment/s5_aligned`（独立 git 仓库）**push 到一个私有 GitHub repo**，供云端 clone。
3. **2 名独立于作者的人类 rater**（有 MR/MT 或核工程背景，盲标，作者本人不能充当）；我提供盲标 codebook + 待标 MR 清单。

**phase2（冲满 4-minor 才需）：**
4. 1 名独立工程师（重实现 1 个 Path-A subject，只给 Sun 2021 散文）。
5. GPU 资源 + 懂等变 ML 的工程师（real-bug e3nn/PyG）。

**optional：** 6. SACOS/LOCUST/SPARK 运行权限 + 内部人员（n5 工业多块）。

---

## 5. 诚实风险 + 1 区 novelty 残险 + IST 兜底

### 残余 1 区风险（即便做完 MVP）
1. **novelty 立场实验弥补不了**：论文自己 L603 承认 closure by-construction、L720 承认 reactor prediction circularity、反复自定性 "systematises/re-classifies, not de novo discovery"；R1 判 IBT = "textbook linear algebra repackaged"。补实验只洗 evaluation rigor，不改"已知结构系统化重排"定性。
2. **headline 实证方向是负的**：s5_aligned 总体 Set N 输 GenMorph（多 seed 后大概率稳定），正中 EIC P0 identification-payoff 缺口（"为何用 NOETHER"无正面答案）。
3. **Guava 赢是 post-hoc subgroup**（n=8, p=0.027 接近边界）：未预注册分层假设就当卖点 = HARKing/selective reporting 红线，多 seed 后可能翻转。
4. **MVP 两腿仍有自指残留**：独立 κ 不触及 MR 设计者=实现者(L2771)与 corpus 非外部(L692)；substrate 中立 ≠ MR 来源中立（71 条仍作者导出）。
5. presentation 是独立 blocker（40–45 页 vs 补实验增内容冲突）。
6. salami 边界：向理论侧加码冲 novelty 可能踩 T2(TSE) 边界。

### 为何 1 区可能仍拒（核心）
TOSEM 的 significance gate 判的是"**是否产生新概念知识**"，与实验厚度正交。本文理论核心已被作者自己三重削弱到 reviewer 可直接引用；叠加经验上打不过现成 GP 基线 → 给 1 区 reject 一个连贯叙事（已知结构重排 + 打不过基线），**MVP 任何一条腿都不正面反驳这条叙事**。MVP 能把"evaluation 太弱/自指"这条硬伤降级，但**1 区的 novelty/significance 是另一道门，MVP 不开这道门**。

### IST(2 区) 兜底净收益为正
IST 门槛 = sound + relevant + adequately evaluated，**不把概念 novelty 设硬 gate**，接受"系统化重组已有结构 + 中立 benchmark 实证"。MVP 两腿恰好把 IST 最看重的 evaluation rigor + reproducibility 拉满，几乎为 2 区量身定做；s5_aligned 中立对照（即便总体输）可诚实写成 identification/coverage + 分层 trade-off，站得住、不需赢 GenMorph；写作修复对任何 venue 纯增益。**把 MVP 定位为"为 IST 投稿做的 evaluation 升级"，无论 TOSEM 成败都净收益为正**——资产可无缝转 IST。

### 诚实概率
做完完整 MVP（独立人类 κ + ≥1 条非自指腿 + 全部写作修复 + s5_aligned 多 seed）后，TOSEM 达 4-minor：**15%–30%**。拆解：R2 ~55–65%、R1 ~60–70%、R3/EIC ~40–50%（被 novelty + Set N 输拖住），近似连乘 0.15–0.30。下沿 15%（ALL 层稳定输），上沿 30%（Guava-WIN 多 seed 稳健 + 预注册分层 + payoff 量化）。**更可能现实结局：TOSEM 第二轮 major + 再一轮 R&R；转投 IST 录用概率 60–75%。**

---

## 6. 建议的执行顺序

1. **本地/云无成本先行**：写作修复（压 40–45 页、headline 重定位、Theorem 2 改名、EQ1 reframe、title）——对任何 venue 纯增益。
2. **MVP-must 两腿并行**：(a) 你提供云主机 → 我准备 s5_aligned 云执行包跑 multi-seed；(b) 你招 2 名 rater → 我出 κ 盲标 codebook+清单。
3. **预注册 Guava 分层假设**（避免 HARKing）——在跑 multi-seed 前写下分层预测。
4. phase2（视 4-minor 决心）：Path-A 独立重实现 / real-bug。
5. 投 TOSEM；若第二轮 major，资产无缝转 IST（录用概率显著更高）。
