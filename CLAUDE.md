# CLAUDE.md — P-series 论文协作规则（项目级）

适用范围：本目录及其子目录的所有论文写作任务（P1-P5 共用 12-PUT × 5-MP 实验基础设施）。

---

## 0. 不允许只说不做（ANTI-CLAIM-WITHOUT-ACTION，最高优先级）

任何回复中出现以下表述时，必须 *在同一回合内* 真实执行对应工具调用并将证据回显给用户：

**触发表述**（中英文均触发）：
- 中文：`已记住`、`已保存`、`已添加`、`已修改`、`已写入`、`已更新`、`已删除`、`已重命名`、`已提交`
- 英文：`I've noted`、`I've saved`、`I'll remember`、`I've added`、`I've modified`、`I've updated`、`I've committed`、`I've removed`

**强制验证规则**：

| 触发表述 | 必须执行的验证 |
|---|---|
| "已修改文件 X" / "I've modified X" | 紧接 `Read` 工具调用，显示修改后的相关行段（≥ 3 行上下文）|
| "已记住偏好 Y" / "I'll remember Y" | 紧接 `Write` 工具调用，写入 `~/.claude/projects/.../memory/feedback_*.md` 并更新 `MEMORY.md` 索引 |
| "已添加任务 Z" / "I've added Z" | 紧接 `TaskCreate` 工具调用，并在响应中给出 task ID |
| "已提交 commit ABC" | 紧接 `Bash git log --oneline -1` 显示实际 commit hash |
| "已删除 / 已移除" | 紧接 `Bash ls` 或 `grep` 验证目标已消失 |
| "已重命名 X → Y" | 紧接 `Bash ls` 验证两个名字的存在状态 |

**禁止行为**：
1. 只说不做：声称"已记住"但未写入 memory 文件
2. 假执行：声称"已修改"但实际未调用 Edit / Write 工具
3. 推迟：用"稍后会..."、"将会..."替代立即执行
4. 模糊化：用"已处理"、"已完成"等不可验证的笼统表述

**例外**：仅当所述操作 *已在前序回合中以工具调用形式完成*，且本回合只是回顾汇报时，可免重复执行——但必须以 `（前序 commit ABC / Edit at L123 已完成）` 之类的引用替代裸声明。

---

## 1. 写作规范

### Abstract / 摘要

- **逻辑结论优先**：以"做了什么、得出什么结论、为什么可信"为骨架，每段 1–2 句。
- **具体数字下放正文**：effect size、CI、p 值、count、percentage 不进 Abstract；正文相应章节才承载。
- **结构性数字可保留 vs 经验性数字严禁**：Theorem 1/2、three domains、two-layer 等指代贡献的数字保留；n=5、2/5、p=1.0、α=0.05、Wilson 区间、百分比一律下放。
- **不得使用内部 `\ref{}` 交叉引用**：Abstract 必须 stand-alone，读者无需翻正文即可读懂。
- **保留**：定性结论性陈述（"达到 / 未达到阈值"、"X 不显著影响 Y"、"X 在 Z 配置下不可达"）。
- **结构化标签**：Context / Objective / Method / Results / Conclusion，IST 偏好。

### 章节标题与拼写一致性

- **章节标题 sentence case**：除首词与专有名词外其余小写；如 `Algebraic closure under Translate` 而非 `Algebraic Closure Under Translate`。TOSEM/IEEE TSE/ACM 期刊体例。
- **拼写一致性**：British 或 American 全文统一二选一；`itemize` / `footnotesize` 等 LaTeX 命令不计。投稿前用 `grep -nE '\\b\\w+i[sz]e[sd]?\\b'` 抽样审计。

### 标记符号节制

- `†`、`R[0-9]+` 等内部记号在添加前必须验证：该数值是否 *真的* 依赖被标记的条件。
- 常见反例：class-mean SMS 在所有 cells 上求平均 → *与 primary-MP 选择无关* → 不应加 `†`。
- 主叙事不引 `†` 数字；如需保留 sensitivity，下放到 Appendix。

### 模拟评审 vs 真评审

- **模拟评审**：可激进删除被污染分析（无外部 selective-reporting 嫌疑）。
- **真评审**：保留 Appendix transparency demotion 优于删除。
- 区分明确写在 response letter，避免混淆。

### 诚实优先于救援

- H 阈值不达 → 承认欠功效，不 retroactive 改预注册。
- v3b 类 selection-on-the-response → 删除或下放到 Sensitivity，不 disguise。

### 敏感信息硬约束（任何文件、任何 commit）

- **任何文件**（`.py` / `.md` / `.tex` / `.json` / `.yaml` / `.sh` / `.log` / `.txt`）出现以下内容均**严禁**进 commit：
  - 真实 API key（OpenAI / Anthropic / DeepSeek / Zhipu / Moonshot / Gemini / 阿里灵积 / 任何第三方服务）
  - 自定义 base_url 含厂商域名 + 已暴露的代理凭据
  - 个人绝对路径（`/Users/<name>/...` / `C:\Users\<name>\...`）—— 即便在注释、log、README 中
  - 个人邮箱（除作者公开信箱外）、内部 IP、机器名
  - Bearer token、access_token、refresh_token、client_secret
- **占位符规范**：
  - API key 写 `your_anthropic_api_key` / `your_openai_api_key`（或 `<API_KEY>`）
  - Base URL 写 `your_anthropic_base_url`（或 `<BASE_URL>`）
  - 路径写 `<PROJECT_ROOT>/...` / `<P2_SOURCE_PATH>` 或用环境变量 `os.environ["P2_ROOT"]`
- **强制配套**：
  - 仓库根目录必须有 `.gitignore` 并包含 `.env`、`.env.local`、`*.key`、`secrets/`、`credentials/`
  - 仓库提供 `.env.example` 模板，所有敏感字段为占位符
  - `.log` / `*.aux` / `*.bbl` / `*.blg` / `*.out` / `__pycache__/` 也要进 `.gitignore`
- **每次 commit 前 grep 自检**：
  ```bash
  grep -rIn -E "(/Users/[^/]+|sk-[A-Za-z0-9]{16,}|Bearer\s+[A-Za-z0-9]+|api_key\s*=\s*['\"][^'\"]{8,})" \
    --exclude-dir=.venv* --exclude-dir=.git --exclude-dir=texmf-dist --exclude-dir=node_modules
  # 必须无输出
  ```
- 若误提交，**立即** `git rm --cached`、改写历史（`git filter-repo`）、并 rotate 真实凭据。

---

## 2. 期刊合规硬约束

### IST (Information and Software Technology)

| 项 | 约束 |
|---|---|
| Title | ≤ 15 词建议 |
| Highlights | **3–5 条，每条 ≤ 85 字符**（投稿系统硬截断）|
| Abstract | ≤ 350 词，结构化 |
| Keywords | 5–8 个 |
| Main body | 8k–12k 词 |
| References | 30+ 推荐 |

### 投稿前自检脚本

```python
import re
content = open("论文.md").read()
title = content.split("\n")[0].lstrip("# ")
# Highlights bullet 长度
m = re.search(r"## Highlights\s*\n(.*?)\n## ", content, re.DOTALL)
for b in [b.lstrip("- ") for b in m.group(1).strip().split("\n")]:
    assert len(b) <= 85, f"Highlight 超 85 char: {b}"
# Abstract 词数
m = re.search(r"## Abstract\s*\n(.*?)\n## Keywords", content, re.DOTALL)
words = len(re.sub(r"\*+", "", m.group(1)).split())
assert words <= 350, f"Abstract 超 350 词: {words}"
```

---

## 3. 提交前流水线（5 步，必须按序执行）

### 步骤 1：academic-pipeline 整体审视

调用 `academic-pipeline` skill 做 stage 检测；如已是终稿，直接进入 stage 4.5 (FINAL INTEGRITY)。

### 步骤 2：参考文献真实性校验（paper-search MCP）

后台 agent 任务，对 References 每条调用：
- DOI 条目：`mcp__paper-search__get_crossref_paper_by_doi`
- 标题查找：`mcp__paper-search__search_crossref` / `search_google_scholar` / `search_semantic`
- arXiv preprint：`mcp__paper-search__search_arxiv`
- 软件仓库：直接 WebFetch GitHub URL

输出审计表：每条标 ✓ / △ / ✗ + 修订建议。审计报告存 `docs/review_*/reference_verification_*.md`。

**通过门槛**：✗ = 0；△ ≤ 5（且每条有合理解释）。

#### 步骤 2a：Bib 全引用审计（必跑）

```python
# scripts/bib_all_cited_check.py
import re, pathlib
tex = pathlib.Path("NOETHER_paper.tex").read_text()
bib = pathlib.Path("NOETHER_paper.bib").read_text()
cited = set(re.findall(r"\\cite[a-z]*\{([^}]+)\}", tex))
cited = {k.strip() for chunk in cited for k in chunk.split(",")}
defined = set(re.findall(r"@\w+\{([^,]+),", bib))
uncited = defined - cited
undefined = cited - defined
assert not uncited, f"Bib 中未被引用条目: {uncited}"
assert not undefined, f"正文引用未在 bib 定义: {undefined}"
print(f"OK: {len(cited)} cited, {len(defined)} defined, all match.")
```

**通过门槛**：`uncited == ∅` 且 `undefined == ∅`。投稿前必须 0 警告。

#### 步骤 2b：编译循环 + Undef 审计（必跑）

```bash
# scripts/compile_and_audit.sh
set -e
xelatex -interaction=nonstopmode NOETHER_paper.tex > /tmp/c1.log
bibtex NOETHER_paper > /tmp/b.log
xelatex -interaction=nonstopmode NOETHER_paper.tex > /tmp/c2.log
xelatex -interaction=nonstopmode NOETHER_paper.tex > /tmp/c3.log
grep -c "undefined" /tmp/c3.log     # 必须为 0
grep -c "I didn't find" /tmp/b.log  # 必须为 0
grep -c "Missing character" /tmp/c3.log  # 必须为 0
```

#### 步骤 2c：匿名 companion paper 必须落地

任何 anonymous `[1]` / `[2]` / `Anonymous2025` 占位条目，**投稿前必须替换为真实 reference 或删除该引用**——不允许带匿名条目投稿。本 round 投稿前 grep `Anonymous|anonymous reference|\[1\]|\[2\]` 出空清单。

#### 步骤 2d：文献来源权威性

References 的出版源需达到以下权威性下限（任一即合格）：

| 学科 | 合格出版源 |
|---|---|
| 中文期刊 | 北大中文核心期刊 / CSSCI / CSCD |
| 国际期刊 | JCR Q3 及以上 / SCI / SSCI / SCI-E |
| 国际会议 | CCF-C 及以上 / 学会主会议（IEEE / ACM / AAAI / ACL / NeurIPS / ICML / ICLR 等）|
| 标准 / 法规 | IEC / ISO / IEEE Std / 国家标准 / 行业标准 |
| 经典专著 | 牛津 / 剑桥 / Springer / Wiley / 高等教育出版社 / 科学出版社等正规出版社 |
| 预印本 | 仅作 supplementary，不能作为主要支撑文献（除非该领域接受 arXiv 为主流，如 ML 顶会习惯）|

不达标的来源（如个人博客、Wikipedia、未出版灰色文献、营销白皮书）**不得**进入 References；正文如必须引用，下放到脚注并标注 "non-peer-reviewed"。

#### 步骤 2e：`.env` 与凭据保护

- 仓库根目录必须含 `.gitignore`，包含 `.env`、`.env.local`、`*.key`、`secrets/` 等条目
- 真实密钥（OPENAI / ANTHROPIC / DEEPSEEK / ZHIPU 等）只写本地 `.env`，**绝不**进 prompt、代码、log 或 commit
- 仓库内提供 `.env.example` 模板，所有 KEY 和 BASE_URL 列为 `your_*_api_key` / `your_*_base_url` 占位
- 提交前 grep `sk-[A-Za-z0-9]{16,}|Bearer\s|api_key\s*=\s*['\"]` 出空清单

### 步骤 3：proofread 校对正文

调用 `academic-paper` skill 的 peer-reviewer 模式 *或* 直接读 §1-§8 + Appendix，扫描：
- 拼写、语法、标点
- 内部一致性（数字、章节交叉引用、symbol 定义先用后定义）
- 假设链完整性（每个 RQ → H → 实验 → 结论 → 反思）
- 表格 / 图 caption 与正文叙述匹配

### 步骤 4：humanizer 去 AI 化

调用 `humanizer_academic` skill。重点扫描：
- **em-dash (—, U+2014) 零容忍** — 全部替换为 `,` / `;` / `:` / `(...)` / 句号
- AI 高频词：delve / crucial / pivotal / landscape / underscore / leverage / showcase / robust signal / intricate / tapestry / testament
- Throat-clearing 起手：`It is important to note that` / `In this section, we will`
- "via" 过用 → "through"
- "linked to" → "associated with"
- 多层 hedging 堆叠
- Negative parallelism (`not only ... but also`)
- "Beyond X," 转折 → "In addition to X,"

**保留**：技术术语、Notably/Furthermore/Specifically 等学术过渡词、合规 en-dash (U+2013) 复合修饰。

### 步骤 5：构建 + 验证 + 提交

```bash
bash scripts/build_ist_submission_v{N}.sh
cd submission && \
  TEXINPUTS=./texmf//: xelatex -interaction=nonstopmode p2_ist_v{N}.tex && \
  TEXINPUTS=./texmf//: xelatex -interaction=nonstopmode p2_ist_v{N}.tex
grep -c "Missing character" /tmp/v{N}p2.log    # 必须为 0
```

提交 message 模板：

```
phase-D(round-{N}): {一句话主题}

{2-3 段说明：动机 → 改动范围 → 验证结果}

Affected sections:
  {章节 1} — {改动}
  {章节 2} — {改动}
  ...

Build: {pages}, {size}, zero "Missing character" warnings
```

---

## 4. 已知陷阱速查

- `scripts/postprocess_unicode.py` 模块的 `mod.TEX = ...` 必须在 `spec.loader.exec_module(mod)` *之后* 设置，否则被模块体重写。
- `build_ist_submission_v{N}.sh` 硬编码 LaTeX preamble 的 Highlights / Abstract / Keywords；markdown 源修订需 *两处同步*。
- `" — " → ", "` 全局替换在含逗号列表的 appositive 里产生 ambiguity；先按上下文分类（heading 用 `:`，clause-break 用 `;`，appositive 用 `,`）再批量。
- 大改前 grep audit 影响范围（`v3b|†|R\d+|旧锚点`），出清单再统一编辑，避免漏改。

### 终稿严禁版本化叙事（C1）

- 论文是**研究结果的呈现**，不是**研究过程的记录**。`v1.0 / v1.1 / v1.2`、"first/second adversarial test"、"R1/R2/R3 round" 等表述只属于 response letter / process summary，**严禁**进终稿正文、abstract、contributions、roadmap。
- 检查清单：grep `v1\.0|v1\.1|v1\.2|R[1-9] adds|round-?[0-9]|first.{0,30}adversarial|second.{0,30}adversarial` 应返回 0 命中。
- 若需在论文中表达"该方法已被反例证伪并扩展"，应**直接呈现扩展后的版本**作为单一 hypothesis；反例则以 `Remark`/`out-of-scope` 形式列于 boundary 段。

### 修订溯源表只属于 Response Letter（C2）

- "Round 4 → Round 5 添加 Higham 引用" 这类条目是 **R&R Traceability Matrix** 内容，写在 Response to Reviewers，不写正文。
- 正文 Limitations / Future Work 只表达**当前论文的真实立场**，不表达"上一版我们说过 X，本版改为 Y"。

### "First/Second adversarial test" 时序措辞陷阱（C3）

- 一旦论文去版本化，"first/second adversarial" 失去时序锚点，必须改为定性描述："the equivariant-ML instantiation **is itself an adversarial test of Hypothesis 1's sufficiency**, and the §6.6.1 pilot **further exposes** an out-of-scope class"。
- 不要用 "we encountered" / "after submission we found" 等暗示时间序的措辞。

### 经验诚实化 ≠ 版本化（C4）

- 当 pilot/case study 的 effect direction 与预期一致但样本不足时，**必须**写出："direction observed (X/N vs Y/N) with sample size insufficient for α = 0.05 confirmation"——不要藏起来，也不要包装成"另一版本会解决"。
- 拒绝以下 escape hatch：用脚注 disclaim、把 underpowered finding 移到 abstract 主结论、用 "preliminary evidence supports" 这类 hedge 替代 "underpowered"。

### 小样本 pilot 必须诚实标注 underpowered（C6）

- n ≤ 10 的 pilot：abstract 与正文必须明确写 "n=N, underpowered for α = 0.05 hypothesis testing"。
- 不允许用以下措辞掩盖样本不足：
  - ❌ "trends suggest"、"pattern observed"、"directional evidence"（不带样本数）
  - ❌ "encouraging"、"promising"、"supports the hypothesis"
- 推荐措辞：
  - ✓ "Set N achieved 2/5 detection vs Sets L, B at 0/5; n is insufficient for inferential conclusions, reported as descriptive evidence consistent with H1's structural prediction."
- 同时报告 Wilson 95% CI 与 Fisher exact / McNemar 的 p 值（即便 p > 0.05），让读者看到样本不足是数据本身的限制，不是隐瞒。

---

## 5. P-series roadmap 锚点

- **P1**: MR meta-pattern audit (12-PUT 基础设施) — Progress in Nuclear Energy / SANER 2027 在审
- **P2**: SMS 度量 + 退化定理 + 12-PUT 实证 — IST 投稿就绪
- **P3**: 工业 Java / C++ port + LRCA 二评者 κ — 未启动
- **P4**: 形式理论 (minimal MR-subset 存在 + 三柱耦合) + n ≥ 30 — 未启动，targeted TOSEM
- **P5 / P2-CN**: 法规转化 (IEC 60880 / ISO 26262 / DO-178C) — 中文在审

---

## 6. 增强对抗审议（Adversarial Review Strengthening, ARS）

`academic-paper-reviewer` 的 Devil's Advocate 阶段完成后，**必须额外执行** Reviewer 2 视角的严苛审视。Devil's Advocate 关注论证一致性；Reviewer 2 关注 *学术诚信* 与 *可发表性硬伤*。

### 扫描维度（5 类，逐项核对）

1. **方法论缺陷**
   - 控制变量是否充分？是否有未声明的混淆因素？
   - 关键操作是否可重现？protocol 是否完整记录在 Appendix？
   - 实验组 / 对照组是否可比？

2. **外部效度问题**
   - 样本代表性：n 是否足够？覆盖的子群是否典型？
   - 泛化能力：结论能否外推到声称的目标域？
   - PUT / 数据集 / 群体的选择是否引入了 selection bias？

3. **统计选择偏差**
   - Cherry-picking：是否只报告显著结果，遗漏不显著的？
   - 多重比较：是否做了 Bonferroni / FDR 校正？
   - Sub-group 分析：是否预注册？事后分组是否被标记？
   - HARKing (Hypothesizing After Results are Known)：假设是否在数据收集前固定？

4. **Benchmark 不公正**（核行业 / 工业控制系统 / 安全关键软件常见痛点）
   - 对比基线是否是该领域的 SOTA？还是挑了较弱的对手？
   - 评估指标是否对自己有利？是否报告对自己不利的指标？
   - 测试集是否独立于训练 / 调参集？

5. **霍桑效应**（教改 / 行为干预 / 流程改造类论文常见痛点）
   - 实验对象是否知道自己在被观察？
   - 观察行为本身是否改变了被观察对象的行为？
   - 长期可持续性 vs 短期热度效应是否区分？

### 输出格式（强制）

```
## Reviewer 2 视角的最严苛审稿意见

- [致命问题 1]
- [致命问题 2]
...

（无致命问题时明确写：Reviewer 2 视角扫描通过——5 类维度均无 publication blocker。）
```

### 处理原则

| 识别结果 | 必须做 | 禁止做 |
|---|---|---|
| 致命问题（publication blocker） | **投稿前修改**正文 / 设计 / 数据 / 假设 | 装作没看见；用脚注 disclaim 替代修改；藏到 "limitations" 段绕过 |
| 严重但非致命 | 在 §Threats / §Limitations 显式承认 + 提出后续验证路径 | 弱化措辞使其不可见 |
| 已知小瑕疵 | 一句话脚注或 Appendix 提及 | — |

### 与 Devil's Advocate 的分工

| 阶段 | 关注点 | 典型问题 |
|---|---|---|
| Devil's Advocate | 论证内部一致性 | "你的 H2 verdict 与 Abstract 表述矛盾" |
| Reviewer 2 (ARS) | 学术诚信 + 外部效度 | "n=12 的 cohort 凭什么外推到工业级" |

ARS 是 *补充* 不是 *替代*——两者都必须执行。

---

## 7. 文献检索优先级（Paper-Search-First Policy）

所有文献检索任务（含 ARS 13-Agent 研究队、reference verification、related-work 扩充、prior-art 防御），**必须优先调用 `paper-search-mcp` 工具**；Web 搜索仅作为降级 fallback。

### 调用顺序（强制）

```
1. paper-search-mcp 学科首选数据库（见下表）
2. paper-search-mcp 通用兜底：search_crossref / search_openalex / search_google_scholar
3. WebSearch / WebFetch（仅当上述全部失败）
```

### 学科 → 首选数据库映射

| 学科领域 | 首选 paper-search-mcp 工具（按优先级） | 备注 |
|---|---|---|
| **软件工程 / 计算机科学** | `search_dblp` → `search_arxiv` → IEEE / ACM via `search_crossref` | dblp 对 SE 顶会覆盖最全；arXiv 对最新 preprint |
| **核行业 / 安全关键系统** | `search_crossref` → `search_openalex` → IEEE via `search_crossref` | Scopus 经 OpenAlex 间接覆盖；IEEE 对核仪控 |
| **教改 / 教育研究** | ERIC（如可达）→ `search_crossref` → `search_openalex` | ERIC 是教育领域权威库 |
| **生物医学 / 临床** | `search_pubmed` → `search_europepmc` → `search_medrxiv` / `search_biorxiv` | preprint 用 medrxiv / biorxiv |
| **数学 / 物理 / 理论** | `search_arxiv` → `search_crossref` → `search_semantic` | arXiv 优先 |
| **DOI 已知** | `get_crossref_paper_by_doi`（直查） | 跳过 search 阶段 |

### ARS 13-Agent 研究队的硬约束

**禁止**：将 `WebSearch` / `WebFetch` 作为首选检索工具。

**必须**：先用 `paper-search-mcp` 学科首选 → 通用兜底 → 三连失败后才允许降级 Web 搜索；降级时必须在审计日志中记录"paper-search-mcp 在 [tool A, tool B, tool C] 上失败"。

### 工具失败处理

- **rate limit / timeout**：等 30 秒重试 1 次，仍失败则切换下一个 paper-search 工具
- **DOI not found**：用 title + 第一作者 fuzzy search（`search_crossref`）
- **author 名字变体**（如 Romanisation 不同）：尝试两种拼写
- **conference paper without DOI**：用 `search_dblp` + venue 缩写
- **textbook / standard / software repo**：跳过 paper-search，直接用 WebFetch 出版社页 / 标准官网 / GitHub 仓库

### 审计日志格式

每次文献检索任务结束须输出：

```
## 检索审计

| Ref | 工具链 | 命中工具 | 耗时 | 状态 |
|-----|--------|---------|------|------|
| Sun 2024 | crossref(doi) | crossref | 0.8s | ✓ |
| Romano 2006 | crossref(title) → openalex → google_scholar | google_scholar | 4.2s | △ no DOI |
| ASME V&V 20 | webfetch(asme.org) | webfetch | 2.1s | ✓ standard |
```

### 投稿前 Paper-Search-MCP 必查清单（hard-block，D1）

终稿提交前对 References **逐条**调用 paper-search-mcp 校验，输出审计表。**任一条目无外部源可校（即三档兜底全失败），必须删除该引用或换为可校的替代条目**——不允许带"unverifiable"条目投稿。

#### 强制流程

1. 把 `NOETHER_paper.bib` 解析为 `key -> (title, author, year, doi?, venue)` 列表
2. 对每条按下表调用 paper-search-mcp：

   | 优先级 | 工具 | 触发条件 |
   |---|---|---|
   | 1 | `mcp__paper-search__get_crossref_paper_by_doi` | 有 DOI |
   | 2 | `mcp__paper-search__search_crossref` | title + 第一作者 |
   | 3 | `mcp__paper-search__search_arxiv` | preprint / ML CS |
   | 4 | `mcp__paper-search__search_dblp` | SE / 顶会 paper |
   | 5 | `mcp__paper-search__search_openalex` / `search_semantic` / `search_google_scholar` | 兜底 |
   | 6 | `WebFetch` 出版社 / 标准官网 / GitHub | 教材 / 标准 / 软件仓库 |

3. 输出 `reference_verification_round{N}.md`，每条标 ✓ / △ / ✗ + 命中工具 + 耗时

#### 通过门槛（hard-block）

- ✗ = 0：任何 ✗ 条目必须**当场删除或替换**，不允许残留
- △ ≤ 5：每条 △ 必须附"无 DOI 但已通过 OpenAlex/Scholar 命中"之类合理说明
- 审计表必须 commit 到 `docs/review_round{N}/reference_verification_round{N}.md`，并在 response letter 中引用

#### 反模式（投稿前 grep 出空清单）

- `Anonymous2025` / `[1]` / `[2]` 等 placeholder cite key
- 自引匿名：`Authors 2024 (under review)`
- 仅有 URL 无作者 / 年份的 `@misc` 条目（除非是软件仓库或标准）
- "personal communication" 进 References（应放脚注）
