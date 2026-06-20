# 分支合并分析：codex-tosem-... ↔ cloud A16 routeB

> 日期：2026-06-20。merge-base = `02d8aee`（PR#34 merge）。
> MINE = `codex-tosem-maturity-review-2026-06-20`（HEAD f6dc01a）；CLOUD = `origin/claude/pensive-turing-0x5kyw`（HEAD 1cd40b7）。
> 方法：merge-base diff + `git merge-tree --write-tree`（权威冲突检测）。

## 1. 两分支对 paper 的改动

| | NOETHER_paper_arxiv.tex | NOETHER_paper.bib | .pdf | supplementary/docs |
|---|---|---|---|---|
| **MINE** | 270 行：§2.3 文献段、Theorem 2 一致性(~14 处)、工业整合 P0/P2(§2774-2780)、METRIC+ 3 表迁 S8(§2371-2556)、DeepCrime contingency 删、L1364 版本泄漏 | +71（6 条文献） | 重生(598KB) | docs/review_2026-06-20/* 多个评估 |
| **CLOUD** | **仅 1 段**：Threats "(f) Three SOTA-category coverage" item (i)：`multi-seed committed as follow-up` → `multi-seed done + routeB 结果(gcd p=2.97e-11, sin p=0.012, N≥G 4/12)` | 未改 | 重生(726KB) | +41 文件 routeB/multiseed 数据脚本 |

## 2. 冲突点（`git merge-tree` 权威）

| 文件 | 类型 | 判定 |
|---|---|---|
| **NOETHER_paper_arxiv.tex** | **自动合并干净** | ✅ **无冲突**。cloud 的 (f) 段落在 MINE 未触碰区域（MINE 逐字保留 base 版 L2275），cloud 改动自动并入。已验证：合并后 (f) 段引用 para:comp-eval-protocol / tab:gen-cost / subsec:case-study / subsec:test-design 全部解析；MINE 无其他处说"multi-seed committed"会与之矛盾。 |
| **NOETHER_paper_arxiv.pdf** | 二进制冲突 | ⚠ **派生物，非真冲突**。两分支各自重生 → 合并后从合并 .tex **重编译**，丢弃两版。 |
| **docs/.../mvp_s5_aligned_multiseed_runbook.md** | **add/add 真冲突** | 🔴 唯一内容冲突（docs，非 paper）。MINE 321 行 = a-priori 计划 + H1-H4 **预注册**；CLOUD 175 行 = post-execution routeB 记录。见 §4 决策。 |
| 41 个 cloud-only 文件 | 干净新增 | ✅ supplementary/S5_genmorph_pilot/multiseed/routeB/* 数据+脚本，MINE 无同名 → clean add。 |

无 modify/delete 冲突（merge-tree 全扫，只报上述 3 项）。

## 3. 合并方案（推荐 cherry-pick，跳过 PDF rebuild）

**总原则**：以 MINE 为基（它含全部 A 阶段 + 评估），并入 cloud 的内容。

### 步骤
1. **paper .tex**：自动合并 cloud 的 (f) 段（替换 MINE L2275）。无需手解。
2. **41 个 routeB/multiseed 文件**：clean add。
3. **runbook.md add/add**：按 §4 决策手解。
4. **.pdf**：**不取任一版**，合并后从合并 .tex 重编译（`xelatex×2`）。
5. **验证**（合并后必跑）：
   - 编译 0 undef refs / 0 missing char / 0 overfull>50pt；页数记录。
   - `python bib_all_cited_check`：cited==defined。
   - grep 一致性：(f) 段说 multi-seed done，全文无残留"committed as follow-up~(a.budget-replication)"。
   - **D1-D7 反漂移**：cloud 的 (f) 改动在 **Threats**、未上位 superiority（强化披露 Set G 占优）→ D1/D4 ✓；守 self-overlap 红线（routeB 只报 detection sufficiency，不报 k\*）。

### 执行选项
- **A. `git merge CLOUD`**：一次并入全部 cloud commits；PDF 冲突手解=重编译；runbook 手解。简单但带 PDF 冲突标记。
- **B. cherry-pick 内容 commits（推荐）**：`git cherry-pick 5fabbe2 0417284 3669215 75db10b 1cd40b7`（**跳过 51c7565 PDF-rebuild commit**），最后重编译。历史干净、规避 PDF 冲突。runbook 冲突在 cherry-pick 0417284 时手解（routeB commit 含 runbook 改写）。
- **C. 手动**：Edit 应用 (f) 段 + `git checkout CLOUD -- <41 routeB 路径>` + runbook 手解 + 重编译。最可控。

## 4. runbook add/add 决策（推荐）

两版本是"计划 vs 执行记录"，非矛盾：
- MINE 版（321 行）：完整 a-priori 多-seed 计划 + **H1-H4 预注册模板 + 对齐验证 + 回报模板**——仍是前向计划（seed12/13 尚未跑）。
- CLOUD 版（175 行）：A16 routeB 已执行的 post-hoc 记录——但该内容**已在** supplementary routeB README + `s5_aligned_seed11_assessment.md §7` 中。

**推荐：保留 MINE 版（计划+预注册不可丢），在其顶部加一节"已执行：routeB（见 supplementary/.../routeB/README.md + s5_aligned_seed11_assessment.md §7）"指针**，不用 cloud 的 175 行覆盖（避免丢失 H1-H4 预注册）。cherry-pick 时对该文件取 MINE 版 + 手加指针节。

## 5. 一句话
**paper 合并零冲突**（cloud 仅动 1 段 Threats，落在我未碰的区域，已验证引用全解析、无残留矛盾）。唯一真冲突是 docs/runbook 的 add/add（保留 MINE 计划+预注册，加 routeB 已执行指针）。PDF 重编译。全流程过 D1-D7。
