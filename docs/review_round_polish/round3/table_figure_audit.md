# Table / Figure Audit — NOETHER Round 3.6

**Manuscript**: NOETHER (commit `<HEAD>` after Phase 1-3 compression)
**Pages**: 74
**Audit date**: 2026-05-15
**Auditor**: editorial_synthesizer_agent (Stage 5 prep)

---

## 1. Current inventory

**Tables**: 19. **Figures**: 0.

### Tables list (by location and purpose)

| # | Label | Section | Purpose | Verdict |
|---|---|---|---|---|
| 1 | `tab:complexity` | §3 Operator-algebraic preliminaries | Per-generator cost in each of 8 blocks (Theorem 2 evidence) | **KEEP** — load-bearing for Theorem 2 polynomial-time claim |
| 2 | `tab:refinement` | §5 Boltzmann instantiation | Prior catalogue ↔ NOETHER deductive output | **KEEP** — load-bearing for C3 systematisation |
| 3 | `tab:elementwise` | §5 Boltzmann instantiation | 12 representative MRs with NOETHER placement | **KEEP** — load-bearing for §5 instantiation |
| 4 | `tab:case-study` | §6 Equi-ML case study | Small-scale comparative case study results | **KEEP** — case study results |
| 5 | `tab:pilot` | §6 DeepCrime pilot | $n=5$ pilot detection counts | **KEEP** — pilot's load-bearing data |
| 6 | `tab:deepcrime-contingency` | §6 DeepCrime pilot | Paired 2x2 contingency for McNemar | **KEEP** — added in R1-m2 for inference clarity |
| 7 | `tab:five-obstructions` | §6 Negative-PWR | 5 pairwise-independent Translate obstructions | **KEEP** — load-bearing for Theorem 1' falsification |
| 8 | `tab:pit-block` | §7 PIT compatibility | PIT mutator × 8-block compatibility matrix | **KEEP** — load-bearing for L*-blindness derivation |
| 9 | `tab:l-blindness` | §7 Central result | Per-SUT $L_{\mathrm{scale}}$ kill rate | **KEEP** — load-bearing for 5/6 verdict |
| 10 | `tab:rediscovery` | §7 Two convergent witnesses | Cross-pipeline rediscovery on `midpoint` | **KEEP** — supports H3a.2 complementarity witness |
| 11 | `tab:algebra-rich-pooled` | §7 Head-to-head | Per-SUT PIT mutation kill counts | **KEEP** — load-bearing per-SUT data |
| 12 | `tab:per-block-headtohead` | §7 Head-to-head | Per-block head-to-head, 3 PIT-covered blocks | **KEEP** — primary head-to-head table (H3a.1 primary reading) |
| 13 | `tab:two-stratum` | §7 Head-to-head | D1/D2 two-stratum head-to-head | **KEEP** — H3a.1 secondary D1-aggregate reading |
| 14 | `tab:gen-cost` | §7 MR-generation cost | 4-method cost components | **KEEP** — load-bearing for H3a.3 cost-axis claim |
| 15 | `tab:future-work` | §7 Future work | 16-item future-work table (terse after Round 3.5 compression) | **KEEP** — readers expect explicit future-work catalogue |
| 16 | `tab:metricplus-sorting` | §8 METRIC+ comparison | 11 D×R framework "type catalogue" | **MERGE CANDIDATE** — overlap with #17 |
| 17 | `tab:metricplus-headtohead-small` | §8 METRIC+ comparison | Manual METRIC+ analysis on 3 SUTs | **KEEP** — distinct from #16 (this has data, #16 has framework) |
| 18 | `tab:metricplus-sun2021-scope` | §8 METRIC+ comparison | NOETHER scope on Sun 2021's 4 subjects (Path B) | **KEEP** — DA NEW-A refutation evidence |
| 19 | `tab:translate` | Appendix C | Per-block Translate instantiations (formal definitions) | **KEEP** — appendix reference table |

**Total verdict**: 19 tables, none excessive for a 74-page foundational paper with three instantiation domains, formal theorem proofs, and detailed empirical evaluation. One marginal "merge candidate" (#16 ↔ #17) but the two tables serve distinct purposes (framework definition vs applied analysis).

### Figures list

**Currently**: 0 figures.

### Inverse density: tables per page

19 tables / 74 pages = $\approx$0.26 tables per page. For an empirical SE paper with substantial data tables, this is high but reasonable; the alternative (presenting all kill-rate data in prose alone) would substantially harm readability.

---

## 2. Figure recommendations

For a foundational theory + three-instantiation + empirical evaluation paper, having 0 figures is unusual. Suggested additions:

### Figure 1 (RECOMMENDED): NOETHER framework architecture flow

**Location**: §1 Introduction or §4 NOETHER framework opening.
**Purpose**: Convey the two-layer architecture (upstream eight-block hypothesis + downstream CONSTRUCT-MP algorithm) at a glance.
**Content**:
- Top half: program $P$ → operator algebra $\mathcal{A}_P$ (curated by human + LLM grid; UPSTREAM, hypothesis layer)
- Bottom half: $\mathcal{A}_P$ → 8-block decomposition $\mathcal{D}(\mathcal{A}_P)$ → CONSTRUCT-MP algorithm → MetaPattern set $\mathbb{M}(\mathcal{A}_P)$ → MR space $\mathrm{MR}(\mathcal{A}_P)$ (DOWNSTREAM, mechanical layer)
- Side annotations: Theorem 1 (closure under Translate); Theorem 2 (polynomial-time decidability)
- Right side: instantiation domains (Boltzmann; equi-ML; relational queries)
**Cost**: ~2-3 hours TikZ design + verification.
**Benefit**: Reader can grasp the framework's two-layer structure without reading §1 prose first; especially useful for skimming reviewers.

### Figure 2 (OPTIONAL): Translate operator block diagram

**Location**: §4 or §subsec:translate-templates.
**Purpose**: Show how Translate maps each of 8 blocks' invariants to a MetaPattern.
**Content**: Eight rows (one per block) each showing: invariant template → Translate operator → MetaPattern instance.
**Cost**: ~1-2 hours TikZ.
**Benefit**: Currently this content lives in `tab:translate` (appendix) + prose. A figure would shorten body prose.
**Verdict**: Useful but not critical; the existing `tab:translate` covers the formal definitions.

### Figure 3 (NOT RECOMMENDED): Operator-algebra Venn diagram

Initially considered (8-block Venn diagram showing block overlap), but: NOETHER's blocks are formally orthogonal under the canonical-block ordering (Definition 13), so a Venn diagram would mislead readers into thinking blocks overlap when they do not.

---

## 3. Recommendation summary

| Action | Item | Priority |
|---|---|---|
| **ADD** | Figure 1: NOETHER framework architecture flow | **High** (high readability gain, moderate cost) |
| **ADD** | Figure 2: Translate per-block block diagram | Medium (lower priority; appendix table covers content) |
| **KEEP** | All 19 tables | — (none excessive) |
| **MERGE** | #16 + #17 (METRIC+ framework + applied) | Low (current separation is defensible) |
| **REMOVE** | None | — |

The minimal-edit recommendation is: **add Figure 1 only**. This single addition addresses the 0-figure concern raised in this audit without disturbing existing table structure or introducing论点 drift.

---

## 4. Implementation status

| Item | Status | Note |
|---|---|---|
| Audit document | DONE (this file) | — |
| Figure 1 TikZ source | NOT STARTED | Requires user decision (cost ~2-3h;论点 preservation neutral) |
| Figure 2 TikZ source | DEFERRED | Lower priority |
| Table merges | DEFERRED | Tables #16 + #17 serve distinct purposes |

The figure additions are recommendations only; this audit document does not modify the manuscript. User direction is needed before implementing Figure 1.
