# 参考文献外部真实性校验报告

> 日期：2026-06-17
> 流程依据：项目 CLAUDE.md §3 步骤 2（参考文献真实性校验，paper-search MCP）+ §7 文献检索优先级
> 校验对象：`NOETHER_paper.bib`（根目录，58 条；6 个分支副本内容一致）
> 校验方式：6 个并行 agent，按主题分批，逐条真实调用 paper-search MCP（crossref / dblp / arxiv / openalex / semantic / google_scholar）+ WebFetch（标准/法规/软件仓库）

---

## 1. 汇总与门槛判定

| 指标 | 结果 |
|---|---|
| 总条目 | 58 |
| ✓（外部源完全匹配） | 53 |
| △（命中但有小差异/可达性受限） | 5 |
| ✗（查无此文 / 元数据严重不符） | **0** |

**通过门槛**（§3 步骤 2）：✗ = 0 ✅；△ ≤ 5 ✅（正好 5 条，每条均附合理说明）。

**结论：参考文献外部真实性校验通过（hard-block 解除）。无虚构、无张冠李戴的引用条目。**

---

## 2. 完整审计表

### 批 A：MT 核心理论（7 条）

| key | 状态 | 命中工具 | 核实结论 |
|---|---|---|---|
| Chen1998 | ✓ | semantic | 题名/三作者(Chen, Cheung, Yiu)一致；techreport 无 DOI 属正常 |
| Segura2016 | ✓ | crossref(doi) | 题名+四作者+IEEE TSE 42(9):805-824 全一致 |
| LiTOSEM2025 | ✓ | crossref(doi) | 题名+八作者+2025+ACM TOSEM 全一致 |
| MRScout2024 | ✓ | crossref(doi) | 题名+五作者+2024+ACM TOSEM 全一致 |
| GenMorph2024 | ✓ | crossref(doi) | 题名+五作者+2024+IEEE TSE 50(7):1888-1900 全一致 |
| ChenMETRIC2016 | ✓ | crossref(doi) | 题名+三作者+JSS 116:177-190 全一致（题名仅大小写差异）|
| SunMETRICplus2021 | ✓ | crossref(doi) | 题名+六作者+IEEE TSE 全一致（year=2021 为正式见刊年）|

### 批 B：MT 应用 / LLM / ML 测试（8 条）

| key | 状态 | 命中工具 | 核实结论 |
|---|---|---|---|
| Shin2024 | ✓ | crossref(doi) | 题名/4 作者/2024/QUATIC Springer CCIS 全一致；pp 126-141 |
| GPTMR2025 | ✓ | crossref(doi) | 题名/6 作者/2025/IST 187:107828 全一致 |
| AutoMT2025 | ✓ | arxiv | 题名/6 作者/arXiv:2510.19438/cs.SE 全一致 |
| ZhangChatGPTMR2023 | ✓ | crossref(doi) | 题名/3 作者/2023/COMPSAC pp 1780-1785 全一致 |
| Murphy2008 | ✓ | dblp | 题名/4 作者/2008/SEKE pp 867-872 全一致 |
| Xie2011 | ✓ | crossref(doi) | 题名/6 作者/2011/JSS 84(4):544-558 全一致 |
| Liu2014MTEffectiveness | ✓ | crossref(doi) | 题名/4 作者/IEEE TSE 40(1):4-22 一致；可补 DOI 10.1109/TSE.2013.46（已外部确认）|
| Kanewala2016GraphKernel | △ | crossref(title) | 题名/3 作者/STVR 26(3):245-269 一致；建议补 DOI 10.1002/stvr.1594；年份印刷 2016 vs 在线 2015 |

### 批 C：MT 综述 / 模式 / 关系生成（7 条）

| key | 状态 | 命中工具 | 核实结论 |
|---|---|---|---|
| Zhou2020SymmetryMRP | ✓ | crossref(doi) | 题名/作者/年份/venue/卷期页全一致 |
| Ying2025MRPatterns | ✓ | crossref(doi) | 题名/作者/2025/STVR 35(2) 一致 |
| Tao2010Mettoc | ✓ | dblp | 题名/作者/2010/APSEC pp 270-279 一致；可补 DOI 10.1109/APSEC.2010.39 |
| Segura2022QBSAutoMR | ✓ | crossref(doi) | 题名/作者/2022/MET 一致（题名仅大小写差异）|
| Nolasco2024MemoRIA | ✓ | crossref(doi) | 题名/作者/2024/Proc. ACM SE (FSE) 一致 |
| Saha2019SupervisedMR | ✓ | dblp | 题名/作者/2019/AITest pp 157-164 一致；可补 DOI 10.1109/AITest.2019.00019 |
| Altamimi2022MRSLR | △ | crossref(doi) | DOI 真实命中，作者/题名一致；卷期 35(1) 无误，但线上首发 2022-09-15，须核对年份归属 |

### 批 D：等变 / 几何深度学习（9 条）

| key | 状态 | 命中工具 | 核实结论 |
|---|---|---|---|
| CohenWelling2016 | ✓ | arxiv | 题名/作者一致；arXiv:1602.07576，ICML 2016 PMLR v48 |
| ThomasSmidt2018 | ✓ | arxiv | 题名/7 作者/2018 一致；arXiv:1802.08219 |
| Satorras2021EGNN | ✓ | semantic | 题名/3 作者/2021/ICML 一致；arXiv:2102.09844 |
| FuchsTransformer2020 | ✓ | dblp | 题名/4 作者/2020/NeurIPS 一致；arXiv:2006.10503 |
| ChenStein2014 | △ | semantic | 内容(题名/作者/年份/venue)全部真实；**cite key 命名有误导**（详见 §3）|
| Bronstein2021GDL | ✓ | semantic | 题名/4 作者/2021 一致；arXiv:2104.13478 |
| KondorTrivedi2018 | ✓ | semantic | 题名/作者/2018/ICML 一致；arXiv:1802.03690 |
| Deng2021VectorNeurons | ✓ | semantic | 题名/6 作者/2021/ICCV 一致；DOI 10.1109/ICCV48922.2021.01198 |
| Cohen2019Gauge | ✓ | arxiv+openalex | 题名/4 作者/2019 一致；arXiv:1902.04615，PMLR v97 (ICML 2019) |

### 批 E：DL 测试 / SQL / 数据库（12 条）

| key | 状态 | 命中工具 | 核实结论 |
|---|---|---|---|
| DeepXplore2017 | ✓ | arxiv | 题名/4 作者/2017/SOSP 一致；DOI 10.1145/3132747.3132785 |
| Gomez2017Reversible | ✓ | arxiv | 题名/4 作者/2017 一致；arXiv:1707.04585，NeurIPS(NIPS) 2017 |
| Humbatova2021DeepCrime | ✓ | crossref | 题名/3 作者/2021/ISSTA pp 67-78 一致；DOI 10.1145/3460319.3464825 |
| Wang2024QED | ✓ | crossref(doi) | DOI 直查命中；题名/3 作者/2024/PVLDB 17(11):3602-3614 一致 |
| Markl2022LearnedQO | △ | crossref | 单作者属实(Volker Markl)/SIGMOD Record 51(1)；实为 1 页 keynote abstract（详见 §3）|
| Slutz1998RAGS | ✓ | semantic | 题名/作者/1998/VLDB 一致 |
| Bati2007GeneticDB | ✓ | semantic | 题名/4 作者/2007/VLDB pp 1243-1251 一致 |
| Zhou2022SPES | ✓ | crossref | 题名/5 作者/2022/ICDE pp 2735-2748 一致；DOI 10.1109/icde53745.2022.00250 |
| Mohamed2024SQLTables | ✓ | crossref(doi)+arxiv | DOI 10.29007/rlt7(EasyChair)命中；题名/4 作者一致；arXiv:2405.03057 同文 |
| Ba2024DQP | ✓ | crossref | 题名/2 作者/2024/PACMMOD(SIGMOD) 2(3):1-26 一致；DOI 10.1145/3654991 |
| Fu2025Thanos | ✓ | crossref(doi) | DOI 直查命中；题名/8 作者/2025/ICSE pp 655-666 一致 |
| Zhong2025SQLancerPP | ✓ | arxiv | 题名/2 作者/2025 一致；arXiv:2503.21424 |

### 批 F：书籍 / 标准 / 软件 / 会议（15 条）

| key | 状态 | 命中工具 | 核实结论 |
|---|---|---|---|
| ISO29119 | ✓ | webfetch | ISO/IEC/IEEE 29119-1:2022 真实；副题建议核对（见 §4）|
| BellGlasstone1970 | ✓ | scholar(OSTI 4074688) | 作者+书名+1970 一致 |
| LewisMiller1993 | ✓ | scholar(OSTI 5538794) | 作者+书名一致；1993 为 ANS 重印版（原版 1983，见 §4）|
| Wohlin2012EmpiricalSE | ✓ | crossref | DOI 10.1007/978-3-642-29044-2，Springer，2012，6 作者，2nd ed |
| Noether1918 | ✓ | crossref×2 | 原文 + Tavel 英译 DOI 10.1080/00411457108231446 均命中 |
| e3nn2022software | ✓ | webfetch(github) | github.com/e3nn/e3nn 存在，Geiger/Smidt 等 |
| Fey2019PyG | ✓ | semantic | 题名/2 作者/2019/ICLR RLGM Workshop 一致；arXiv:1903.02428 |
| Higham2002Accuracy | ✓ | openalex | DOI 10.1137/1.9780898718027，SIAM，2002，2nd ed |
| StammlerAbbate1983 | ✓ | scholar(CiNii) | 作者+书名+1983 一致 |
| Stacey2007 | ✓ | crossref | DOI 10.1002/9783527611041，Wiley，2007，ISBN 与 bib 一致 |
| LamarshBaratta2001 | ✓ | scholar | 3rd ed/Prentice Hall/作者一致 |
| NRC10CFR50AppA | ✓ | webfetch(govinfo.gov) | 10 CFR 50 App A GDC，含 Criterion 11，官方源一致 |
| ANS196_1 | ✓ | scholar | ANSI/ANS-19.6.1 真实标准 |
| NRCRG177 | △ | (NRC 超时/Scholar 未索引) | 真实 NRC RG 1.77；工具可达性受限（详见 §3）|
| Coles2016PIT | ✓ | crossref(doi) | DOI 10.1145/2931037.2948707，ISSTA 2016 demo pp 449-452 一致 |

---

## 3. △ 条目详细说明（5 条，均非投稿阻塞）

1. **Kanewala2016GraphKernel** — CrossRef 命中无误，题名/Kanewala·Bieman·Ben-Hur 三作者/页码 245-269/Wiley STVR 完全吻合。差异：bib year=2016（印刷期 vol 26(3)）vs 在线先行 2015-11-16（版权页 ©2015），属常见"在线 vs 印刷年"差异，2016 为正确印刷年。建议补 DOI `10.1002/stvr.1594`。

2. **Altamimi2022MRSLR** — DOI `10.1002/smr.2509` 真实命中，三作者/题名/venue(JSEP)一致，卷期 35(1) 无误。差异：线上首发 2022-09-15，正式卷期 35(1) 归 2023 年第 1 期。建议确认期刊体例要求按线上首发年(2022)还是正式卷期年(2023)；卷期号无误。

3. **ChenStein2014** — ⚠️ **本批最值得注意。** 文献内容完全真实：Semantic Scholar 命中题名 "Stochastic Gradient Hamiltonian Monte Carlo"、作者 Tianqi Chen / Emily Fox / Carlos Guestrin、2014、ICML(PMLR v32) pp 1683-1691、arXiv:1402.4102，与 bib 全部吻合。判 △ 的唯一原因是 **cite key `ChenStein2014` 含 "Stein" 字样，但该论文是 SGHMC（二阶 Langevin 动力学），与 Stein 方法无任何关系**。建议：(a) 将 key 重命名为 `Chen2014SGHMC` 或 `ChenFoxGuestrin2014`，正文 `\cite{}` 同步替换；(b) 核查正文引用该 key 处的上下文，确认未把它误当作"Stein 方法/Stein 变分"类文献引用（key 误导有诱发正文张冠李戴的风险）。bib 字段本身无需改动。

4. **Markl2022LearnedQO** — 外部源证实单作者 Volker Markl、ACM SIGMOD Record 51(1)、DOI `10.1145/3542700.3542702`。差异：该条目页码 `5-5`，实为 **1 页 keynote/perspective 摘要**，非完整研究论文。建议：补 DOI；若正文将其作为完整方法论文献引用，措辞宜调整为 "keynote/perspective"。作者无缺，bib 无误。

5. **NRCRG177**（Regulatory Guide 1.77, Rev 1）— 真实且权威的一手监管文件（NRC 评估 PWR 控制棒弹出事故/RIA 的标准指南）。判 △ 仅因工具可达性：NRC 官网对 WebFetch 反复 403/超时，Google Scholar 不索引 regulatory guide。属 §2d "标准/法规"合格来源，bib 年份 2020 与 Rev 1 一致。建议人工访问 nrc.gov 上 RG 1.77 Rev.1 页面核对一次以转为 ✓。

---

## 4. 可选元数据润色（非 △/✗，不影响真实性判定）

- **DOI 补全**（增强可检索性）：Liu2014→`10.1109/TSE.2013.46`；Tao2010→`10.1109/APSEC.2010.39`；Saha2019→`10.1109/AITest.2019.00019`；Kanewala2016→`10.1002/stvr.1594`；Markl2022→`10.1145/3542700.3542702`。
- **题名大小写**（CrossRef 官方为句首大写，用 `{}` 保护即可，内容真实）：ChenMETRIC2016、SunMETRICplus2021、Segura2022QBSAutoMR。
- **ISO29119**：bib 副题 "General Concepts" vs 官方 "Concepts and definitions"，建议统一为 ISO 官方副题。
- **LewisMiller1993**：1993 对应 ANS 重印版（原版 1983 Wiley-Interscience），建议确认引用的是 1993 ANS 版。
- **Gomez2017Reversible**：2017 当年会议官方名为 "NIPS"，"NeurIPS 2017" 为通行回溯写法，可保留。

---

## 5. 检索审计备注

- 工具链整体健康。CrossRef DOI 直查命中率最高；arXiv 对 ML 预印本覆盖完整；标准/法规/书籍依赖 WebFetch + Google Scholar(OSTI/CiNii)。
- **dblp 服务本轮不稳定**：批 D、E 多次查询返回空（疑似服务端临时问题），已按 §7 协议逐条切换 semantic/arxiv/openalex/crossref 二次核实，全部命中，不影响判定。
- 每个 ✗ 候选在判定前均尝试 ≥ 2 个不同工具；最终全批无 ✗。
- NRC 官网（nrc.gov / ADAMS）对自动化 WebFetch 持续返回 403/超时，regulatory guide 类引用如需转 ✓ 需人工核对。

---

## 6. 修订执行记录（2026-06-17，本轮已落实）

修改范围：仅 **git 跟踪的活跃文件**——根目录 `NOETHER_paper.bib`/`NOETHER_paper_arxiv.tex` 与 `arxiv/NOETHER_paper.bib`/`arxiv/NOETHER_paper_arxiv.tex`。`submission/TOSEM_2026-05-19|20/`（历史投稿快照）、`docs/historical_notes/superseded_*`（废弃归档）、`arxiv/pdflatex_test/`（未跟踪）按归档原则**冻结不动**。

| # | 改动 | 文件 | 状态 |
|---|---|---|---|
| 1 | cite key `ChenStein2014` → `Chen2014SGHMC`（消除 "Stein" 误导；正文 `\cite{}` 同步）| 2 bib + 2 tex | ✅ |
| 2 | Liu2014MTEffectiveness 补 `doi=10.1109/TSE.2013.46`（直查确认）| 2 bib | ✅ |
| 3 | Kanewala2016GraphKernel 补 `doi=10.1002/stvr.1594`（直查确认）| 2 bib | ✅ |
| 4 | Tao2010Mettoc 补 `doi=10.1109/APSEC.2010.39`（直查确认）| 2 bib | ✅ |
| 5 | Saha2019SupervisedMR 补 `doi=10.1109/AITest.2019.00019`（直查确认）| 2 bib | ✅ |
| 6 | Markl2022LearnedQO 补 `doi=10.1145/3542700.3542702`（直查确认）| 2 bib | ✅ |

**核查结论（选项 1）**：`ChenStein2014` 正文唯一引用位于时间反演块论证（§rho-rev），语境为 "Hamiltonian-Monte-Carlo / continuous-time-flow view of stochastic optimisation"——与 SGHMC 论文主题完全一致，**无张冠李戴**，正文无 "Stein" 字样。仅 key 名误导，已重命名修复。

**未执行项**：题名 `{}` 保护（ChenMETRIC2016/SunMETRICplus2021/Segura2022）经复查认定不必要——题名已是规范 Title Case + 专有名词内层保护，与全 bib 风格一致，CrossRef 句首大写仅为其存储风格，强加整标题保护反破坏一致性。

**验证**：旧 key 活跃文件 0 残留；新 key 2 bib + 2 tex 各 1 落位；5 DOI 直查元数据全部匹配；bib `cited(58)==defined(58)`，undefined/uncited 均为 ∅。

**仍需人工/后续**：(a) Altamimi2022 年份 2022 vs 2023 卷期归属按目标期刊体例核对；(b) Markl2022 若作完整论文引用，措辞宜标注 keynote/perspective；(c) NRCRG177 人工访问 nrc.gov 核对一次转 ✓；(d) 投稿前按 §11.5 跑完整 xelatex+bibtex 编译循环复核 undefined=0。
