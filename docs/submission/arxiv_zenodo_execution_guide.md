# arXiv + Zenodo 执行指南（step-by-step）

**适用范围**：两篇论文 NOETHER (P1) + P2 Semantic Mutation 的 arXiv 预印本上传 + Zenodo 归档 DOI 铸造。

**前置就绪**（assistant 已完成）：
- ✓ NOETHER arXiv tarball: `<NOETHER_ROOT>/arxiv/noether_arxiv_v1.tar.gz` (123 KB)
- ✓ P2 arXiv tarball: `<P2_ROOT>/submission/p2_arxiv_v1.tar.gz` (641 KB)
- ✓ NOETHER replication.zip: `<NOETHER_ROOT>/noether_replication_v0.1.0.zip` (100 MB)
- ✓ P2 replication.zip: `<P2_ROOT>/p2_replication_v1.0.0.zip` (3.5 MB)
- ✓ arXiv metadata (paste-ready): `<NOETHER_ROOT>/arxiv/arxiv_metadata.md` + `<P2_ROOT>/submission/arxiv_metadata.md`
- ✓ GitHub repos public: meng004/P1-MetaPattern + meng004/P2-Semantic-Mutation

---

## Part A: arXiv 上传（两篇）

### A.1 创建 arXiv 账号（如首次）

1. 浏览器访问 https://arxiv.org/user/register
2. 填写：
   - **Email**: `mlemon@usc.edu.cn`（建议用学校邮箱，便于后续 endorsement）
   - **Password**: 自设（≥ 6 chars，记下来）
   - **First name**: `Meng`
   - **Last name**: `Li`
   - **Affiliation**: `School of Computing, University of South China`
   - **Country**: `China`
   - **Career status**: `Senior` 或 `Staff` 或 `Faculty`（按实际填）
3. 邮箱收到验证链接 → 点开 → 账号激活

### A.2 取得 cs.SE 类别 endorsement（关键瓶颈）

**arXiv 对首次投 `cs.SE` 的作者要求 endorsement**。三条路径：

#### 路径 1：使用机构邮箱自动 endorsement（最快）

如 `mlemon@usc.edu.cn` 域名被 arXiv 识别为受信任学术域：
- 登录后访问 https://arxiv.org/auth/show-endorsers.php?category=cs.SE
- 系统若显示 "you are auto-endorsed for cs.SE based on your institution" → 直接跳到 A.3
- 否则进路径 2

#### 路径 2：联系既有 cs.SE 作者背书（标准做法）

需要 1 位（够用）已在 arXiv 上发过 cs.SE 论文的作者背书。

操作：
1. 登录后访问 https://arxiv.org/auth/need-endorsement.php
2. arXiv 生成一个 6 位 endorsement code（如 `ABC123`）
3. 把这段话发给愿意背书的合作者 / 同事：

   ```
   Dear Prof. <Name>,

   I'm preparing my first arXiv submission to cs.SE: "NOETHER: A Constructive
   Framework for Metamorphic Pattern Discovery from Operator Algebras"
   (manuscript draft attached or at https://github.com/meng004/P1-MetaPattern).

   arXiv requires endorsement for first-time cs.SE submitters. Could you
   endorse me using the following link?
       https://arxiv.org/auth/endorse?x=ABC123
   (replace ABC123 with my actual code from arXiv)

   The endorsement attests that the work is plausibly within cs.SE scope;
   it is not a peer-review or quality endorsement.

   Thank you.
   Meng Li
   School of Computing, University of South China
   ```

4. 一旦背书完成，邮件通知 → 跳到 A.3

#### 路径 3：直接提交并等待 review（最慢）

不取得 endorsement 也能上传，但 arXiv 会把稿件转人工审，1-2 周。**不推荐**，除非路径 1+2 都不可用。

---

### A.3 上传 NOETHER (P1)

1. 登录 → 访问 https://arxiv.org/submit
2. 点 **Start a new submission**
3. **License**:
   - 选 `arXiv.org perpetual, non-exclusive license to distribute this article 1.0`
   - 或更宽松：`Creative Commons Attribution 4.0 International` (CC-BY-4.0, 推荐)
4. **Primary archive**: `Computer Science (cs)`
5. **Primary subject class**: `cs.SE` (Software Engineering)
6. **Cross-list categories**: 添加 `cs.LG` 和 `cs.LO`（用逗号分隔填）
7. **Title**:
   ```
   NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
   ```
8. **Authors**:
   ```
   Meng Li (School of Computing, University of South China)
   ```
9. **Abstract**: 粘贴 `<NOETHER_ROOT>/arxiv/arxiv_metadata.md` §3 的 abstract 段（1898 chars，含 Context/Objective/Method/Results/Conclusion 5 段）
10. **Comments** (可选 metadata 字段)：
    ```
    71 pages, 18 tables, 1 figure. Under review at ACM Transactions on Software Engineering and Methodology. Supplementary materials at https://github.com/meng004/P1-MetaPattern
    ```
11. **MSC classification** (optional): `68N30`
12. **ACM classification** (optional): `D.2.5; D.2.4`
13. **Report number**: 留空（除非有实际报告号）
14. **Journal reference**: 留空（投出且接收后再加）
15. **DOI**: 留空（投出且接收后再加）

**上传 tarball**：
1. 点 **Add Files**
2. 选择 `<NOETHER_ROOT>/arxiv/noether_arxiv_v1.tar.gz`
3. arXiv 会自动解压并尝试 build
4. 等待 build 完成（约 2-5 min），点 **Preview** 查看生成的 PDF
5. 验证：
   - 71 pages
   - Title 正确显示 "NOETHER: A Constructive Framework..."
   - Author "Meng Li" 正确显示
   - 摘要可读、数学公式正确渲染
   - 表格 / Figure 1 渲染正常
6. 若 build 失败，下载 arXiv 的 build log，根据错误调整后重新上传

**最终 submit**：
1. 点 **Preview** 再次确认 PDF
2. 点 **Submit**
3. 收到确认邮件（含临时 submission ID）
4. **24h 内**进入 arXiv moderation queue
5. 通过后获得正式 ID：`arXiv:YYMM.NNNNN`（如 `arXiv:2605.12345`）
6. 邮件通知 + 论文 live at `https://arxiv.org/abs/YYMM.NNNNN`

---

### A.4 上传 P2 Semantic Mutation

endorsement 已在 A.2 取得，**不需再次申请**。

重复 A.3 流程，差异：
1. **Title**:
   ```
   A semantic mutation metric for metamorphic relation adequacy in scientific computing programs
   ```
2. **Abstract**: 粘贴 `<P2_ROOT>/submission/arxiv_metadata.md` §3 的 abstract（1893 chars）
3. **Primary**: `cs.SE` | **Cross-list**: `cs.LG`
4. **Comments**:
   ```
   Submitted to Information and Software Technology (IST), Elsevier. 93 pages in elsarticle review mode. Supplementary at https://github.com/meng004/P2-Semantic-Mutation
   ```
5. **Upload**: `<P2_ROOT>/submission/p2_arxiv_v1.tar.gz`
6. 验证 build：93 pages，3 figures，elsarticle 格式

---

### A.5 arXiv 常见 build 错误

| 错误信息 | 原因 | 修复 |
|---|---|---|
| `Missing $ inserted` | 数学环境缺 `$` | 通常源已 OK；arXiv pdflatex 默认（非 xelatex）可能更严格——一般 elsarticle/acmart 都兼容 |
| `LaTeX Error: File 'xxx.sty' not found` | 自定义 .sty 未上传 | 检查 tarball 是否包含所有 .sty（NOETHER：hyperxmp.sty；P2：texmf/） |
| `! Package fontenc Error: Encoding file 'tuenc.def' not found` | TU 编码字体问题 | 用 pdflatex 而非 xelatex；或预编 .bbl 避开 |
| `Output written on ... (0 pages)` | 主 .tex 文件名识别错 | 确认 tarball 顶层有 `\documentclass` 的 .tex；arXiv 取第一个 |
| `LaTeX Warning: Reference 'xxx' undefined` | 缺 .bbl 或交叉引用 | 确认 .bbl 在 tarball 内（NOETHER 已含；P2 用 inline APA 无需） |

如 build 持续失败，可改用 "PDF-only submission" 兜底：直接上传已编译的 PDF（`noether_arxiv_v1.pdf` 或 `p2_ist_final.pdf`），arXiv 接受但不可重编。损失少量灵活性但保证发布。

---

### A.6 投后 arXiv ID 锚定

一旦两篇都收到 arXiv ID（如 `2605.12345` 和 `2605.12346`），告知我，我会自动执行：

```bash
# NOETHER
cd <NOETHER_ROOT>
sed -i.bak "s|<ARXIV_ID>|2605.12345|g" CITATION.cff pyproject.toml README.md
# P2
cd <P2_ROOT>
sed -i.bak "s|<ARXIV_ID>|2605.12346|g" CITATION.cff submission/arxiv_metadata.md
# Commit + push 各仓库
```

---

## Part B: Zenodo 上传（两篇）

### B.1 创建 Zenodo 账号

1. 浏览器访问 https://zenodo.org/signup
2. 选项：
   - **ORCID 登录**（推荐，自动同步 ORCID iD 与 affiliation）
   - 或 GitHub 登录
   - 或邮箱注册
3. 验证邮箱

### B.2 链接 GitHub 账号（启用自动归档）

1. 登录 Zenodo → 右上角头像 → **Settings**
2. 左侧菜单 **GitHub**
3. 点 **Authorize Zenodo to access your GitHub account**
4. 授权后看到 repo 列表
5. **打开 toggle**：
   - `meng004/P1-MetaPattern` → ON
   - `meng004/P2-Semantic-Mutation` → ON
6. 这样以后在 GitHub 创建 Release（即打 tag）时 Zenodo 会自动归档 + 铸 DOI

### B.3 方案 1：通过 GitHub Release 自动归档（推荐）

1. 浏览器访问 https://github.com/meng004/P1-MetaPattern/releases/new
2. 填：
   - **Choose a tag**: `v0.1.0-arxiv` → Create new tag on publish
   - **Release title**: `v0.1.0 — arXiv preprint`
   - **Describe this release**:
     ```markdown
     Initial public release of NOETHER paper accompanying the arXiv preprint.

     - Paper: NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
     - arXiv: https://arxiv.org/abs/<ARXIV_ID>
     - Manuscript: 71 pages (TOSEM double-blind variant); 71 pages (arXiv named variant)
     - Status: Under review at ACM Transactions on Software Engineering and Methodology
     - Code: reference implementation of CONSTRUCT-MP + 84-MR PWR corpus + SE(3) case study + three-tier METRIC+ replication
     - License: MIT (code) + CC-BY-4.0 (paper, data)

     See CHANGELOG.md for full release notes.
     ```
3. **Attach binary**（可选）：拖入 `noether_replication_v0.1.0.zip`（100 MB）。但 Zenodo auto-archive 会用 GitHub 自动 tarball，所以这个 attach 不强制。
4. 点 **Publish release**
5. 等 30 秒，Zenodo 收到 webhook，自动：
   - 下载 GitHub tagged 状态的 source tar
   - 创建 Zenodo deposit
   - 铸 DOI（如 `10.5281/zenodo.12345678`）
   - 邮件通知 DOI

P2 重复同样步骤：https://github.com/meng004/P2-Semantic-Mutation/releases/new → tag `v1.0.0-arxiv`

### B.4 方案 2：直接上传 replication.zip（如不想用 GitHub Release）

适合需要上传大文件（如 cached LLM 响应）的场景。

1. https://zenodo.org/uploads/new
2. **Type**: `Software` 或 `Dataset`（建议 Software）
3. **Title**:
   - NOETHER: `NOETHER: Reference implementation, PWR corpus, and replication harness (v0.1.0)`
   - P2: `Semantic Mutation Score (SMS): 12-PUT replication harness (v1.0.0)`
4. **Authors**:
   - Name: `Li, Meng`
   - Affiliation: `School of Computing, University of South China`
   - ORCID: 若有则填
5. **Description**: 粘贴对应论文的 abstract（用 `CITATION.cff` 的 abstract 字段）
6. **Keywords**: 从 `CITATION.cff` 复制（NOETHER 8 个 / P2 7 个）
7. **License**: `Creative Commons Attribution 4.0 International (CC-BY-4.0)`
8. **Related identifiers**（关键）：
   - 添加 `arXiv` ID（投出后才有）：relation = `isSupplementTo`
   - 添加 GitHub URL：relation = `isDerivedFrom`
   - 例：
     ```
     | Identifier             | Type   | Relation        |
     |------------------------|--------|-----------------|
     | arXiv:YYMM.NNNNN       | arxiv  | isSupplementTo  |
     | https://github.com/meng004/P1-MetaPattern | url | isDerivedFrom |
     ```
9. **Reserve DOI**: 点 **Reserve DOI** → 立即得 `10.5281/zenodo.NNNNNN`（即使没 publish，DOI 已锁，可用于论文引用）
10. **Files**: 拖入对应的 `*_replication_*.zip`
11. **Communities** (optional): 搜索 `software-citation` 或相关 community 加入
12. **Publish**: 点 **Save** → 检查无误 → 点 **Publish**

⚠️ **Publish 不可撤销**。检查再三。

### B.5 投后 Zenodo DOI 锚定

收到 Zenodo DOIs 后告知我：

```bash
# NOETHER 例
NOETHER_ZENODO_DOI="10.5281/zenodo.12345678"
# Anchor in CITATION.cff (in identifiers: section)
# Anchor in DATASET.md (in integrity section)
# Anchor in NOETHER_paper.tex (artefact subsection — post-acceptance for TOSEM)
```

我会执行替换 + commit + push。

---

## Part C: 时序与依赖

```
Day  0 (now):  arXiv account 创建 + endorsement 申请
Day  1-2:      endorsement 等待
Day  2 (上午): arXiv NOETHER 上传 + submit → 进 moderation
Day  2 (下午): arXiv P2 上传 + submit → 进 moderation
Day  3:        两篇收到 arXiv ID
Day  3 (上午): GitHub Release × 2 (tag v0.1.0-arxiv / v1.0.0-arxiv)
Day  3 (上午+): Zenodo auto-archive 触发 → 收 DOI × 2
Day  3 (下午): 告知我 arXiv IDs + Zenodo DOIs → anchoring + 重 push
Day  4+:       TOSEM 投稿（NOETHER）+ IST 投稿（P2）使用完整 ID 集
```

**关键依赖**：arXiv endorsement 是最大不确定项。若 1 周内未取得，可考虑：
- 改投 IST/TOSEM 不依赖 arXiv（直接 journal submission，arXiv 延后）
- 或暂用 PDF-only arXiv（无 endorsement 也可，但 review 更慢）

---

## Part D: 常见疑问

### Q1: arXiv 必须先 endorsement 吗？

是。cs.SE 是 endorsement-protected category。一旦取得一次，后续投同类别（cs.SE）不需重申请；跨 category（如投 cs.PL）需要新 endorsement。

### Q2: arXiv 文章发出去后还能改吗？

可，但只能"replace"（v2, v3 ...），不能删。每个版本独立 timestamped，旧版本对外可访问。改后引用应该用 arXiv ID base（不带版本），自动指 latest。

### Q3: Zenodo DOI 在 publish 之前能用吗？

可。**Reserve DOI** 后 DOI 立即锁定（即使 deposit 处于 draft）。可在论文 §Data Availability 引用，再于稿件最终化时确保 deposit publish。

### Q4: GitHub release 触发的 Zenodo auto-archive 与手动 Zenodo upload 有何不同？

| 特性 | Auto (via GitHub Release) | Manual upload |
|---|---|---|
| Source | GitHub 自动 tarball (current HEAD) | 用户指定 zip |
| 体积 | GitHub repo 全大小 | 用户控制 |
| 元数据 | 从 CITATION.cff 自动 | 手动填表 |
| 触发 | 每个 release 自动 | 手动 |
| DOI 关系链 | 自动 ConceptDOI + VersionDOI | 同 |

推荐用 GitHub Release 触发 auto-archive（少手动出错）。replication.zip 仍可作为 GitHub Release 的 binary attachment。

### Q5: 100 MB 的 NOETHER replication.zip 能上 Zenodo 吗？

可。Zenodo 单文件上限 50 GB。100 MB 完全 OK。但若想优化体积，可：
- 排除 `supplementary/S7_d4j_algebra_rich/d4j/`（D4J subjects 体积大）
- 仅留 metadata + scripts；让用户 `pip install + clone` 完整跑通

### Q6: 如何确认 Zenodo 已正确链接 arXiv？

Zenodo deposit 页面右侧应显示 "Related identifiers" 板块，列出 arXiv ID（带 `isSupplementTo` 关系）。在 https://arxiv.org/abs/<arXiv_ID> 页面，则不主动显示 Zenodo（arXiv 不渲染 reverse links），但 Zenodo → arXiv 单向链可作为 archival 凭证。

---

## Part E: Checklist（每步打勾）

### arXiv NOETHER
- [ ] arXiv account 创建并激活
- [ ] cs.SE endorsement 取得
- [ ] 上传 noether_arxiv_v1.tar.gz
- [ ] Preview PDF 验证 71 pages + 正确 author + 摘要
- [ ] Submit
- [ ] 收到 arXiv ID `arXiv:YYMM.NNNNN`

### arXiv P2
- [ ] 上传 p2_arxiv_v1.tar.gz
- [ ] Preview PDF 验证 93 pages + author + 摘要
- [ ] Submit
- [ ] 收到 arXiv ID

### Zenodo NOETHER
- [ ] Zenodo account 创建
- [ ] GitHub linked
- [ ] GitHub Release `v0.1.0-arxiv` 发布（或手动上传 replication.zip）
- [ ] 收到 Zenodo DOI

### Zenodo P2
- [ ] GitHub Release `v1.0.0-arxiv` 发布
- [ ] 收到 Zenodo DOI

### Post-anchoring
- [ ] 告知 assistant arXiv IDs + Zenodo DOIs
- [ ] Assistant 完成 anchoring + 重 push 两仓库
- [ ] arXiv 上传 v2 with anchored Zenodo DOI（如需要）

### 期刊投稿
- [ ] NOETHER 投 TOSEM（cover letter 含 arXiv + GitHub + Zenodo 三 ID）
- [ ] P2 投 IST（同上）

---

## 立即开始

最简执行顺序（约 1 小时本会话外）：

1. **现在做**（5 min）：访问 https://arxiv.org/user/register 创建账号
2. **现在做**（5 min）：访问 https://zenodo.org/signup 创建账号（用 ORCID 登录最方便）
3. **现在做**（10 min）：申请 cs.SE endorsement（看 A.2 路径 1/2）
4. **等 endorsement 时**（5 min）：Zenodo 链接 GitHub（B.2）
5. **endorsement 拿到后**（30 min）：上传两篇 arXiv（A.3 + A.4）
6. **arXiv ID 到手后**（10 min）：GitHub Release × 2（B.3）
7. **Zenodo DOI 到手后**：告知 assistant，触发 anchoring
