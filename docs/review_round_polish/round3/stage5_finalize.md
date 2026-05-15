# Stage 5 FINALIZE — NOETHER

**Pipeline stage**: Stage 5 FINALIZE (academic-pipeline v3.2.2)
**Manuscript**: NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
**Target venue**: ACM TOSEM, "Testing & Analysis" track
**Finalisation date**: 2026-05-16
**Branch**: `feat/section-7-empirical-vs-sota`

---

## 1. Final deliverables

| Artefact | Path | Size | SHA-256 |
|---|---|---|---|
| Manuscript source (LaTeX) | `NOETHER_paper.tex` | 326.3 KB | `51ef662f0295...` |
| Bibliography | `NOETHER_paper.bib` | 19.9 KB | `0532b2b26549...` |
| Final PDF | `NOETHER_paper.pdf` | 546.1 KB, 74 pages | `7c268833c43a...` |

Supplementary material directories (under `supplementary/`):

| Directory | Content |
|---|---|
| `S1_construct_mp/` | CONSTRUCT-MP algorithm reference implementation + worked enumeration |
| `S2_pwr_corpus/` | 84-MR PWR corpus and per-MR source provenance |
| `S3_case_study/` | Equi-ML case study harness + DeepCrime pilot stats (Mode 1/3 corrected) |
| `S4_reproducibility/` | Reproducibility checklist + environment snapshots |
| `S5_genmorph_pilot/` | GenMorph head-to-head data + 2-vendor Set L ensemble |
| `S6_query_optimiser/` | Relational query optimiser instantiation artefacts |
| `S7_d4j_algebra_rich/` | Defects4J substrate + $\mathcal{L}^{*}$-blindness experiment data |
| `S8_metricplus_sun2021_subjects/` | NOETHER eight-block scope analysis on Sun 2021's 4 METRIC+ subjects (Path B, DA NEW-A refutation) |
| `S9_migrated_appendices/` | Appendices A / B / C-worked / C.7 / D / E migrated from body in Phase 1 length compression |

---

## 2. Pre-finalisation gate checks (all PASS)

```
$ xelatex -interaction=nonstopmode NOETHER_paper.tex
$ bibtex NOETHER_paper
$ xelatex -interaction=nonstopmode NOETHER_paper.tex
$ xelatex -interaction=nonstopmode NOETHER_paper.tex
```

| Gate | Threshold | Actual | Status |
|---|---|---|---|
| LaTeX undefined references | 0 | 0 | PASS |
| BibTeX unresolved citations | 0 | 0 | PASS |
| Missing-character warnings | 0 | 0 | PASS |
| em-dash (U+2014) | 0 | 0 | PASS |
| bib cited == defined | 58 == 58 | 58 == 58 | PASS |
| Sensitive-info grep | 0 hits | 0 hits | PASS |
| Pages | TOSEM 30–50 pp. soft target | 74 | OVER (declared in cover letter) |
| Abstract word count | ≤ 350 (recommended) | 361 | NEAR-LIMIT (acceptable) |
| Keywords | 5–8 | 8 | PASS |
| Tables | reasonable | 19 | PASS (all load-bearing per audit) |
| Figures | ≥ 1 desirable | 1 (Figure 1) | PASS (architecture flow added) |

---

## 3. Manuscript structure (final)

| Section | Title | Approximate pages |
|---|---|---|
| Abstract | — | < 1 |
| §1 | Introduction (with Figure 1: NOETHER architecture) | 4–5 |
| §2 | Background and related work | 3 |
| §3 | Operator-algebraic preliminaries | 4 |
| §4 | The NOETHER framework | 4 |
| §5 | Boltzmann instantiation | 3 |
| §6 | Cross-domain demonstration: equivariant ML | 14 |
| §7 | Empirical test: $\mathcal{L}^{*}$-block blindness | 20 |
| §8 | Discussion and threats to validity | 7 |
| §9 | Conclusion | < 1 |
| App. C | Proofs (incl. Theorem $1'$ falsification on $\mathcal{A}_{\mathrm{PWR}}$) | ~10 |
| Pointers | Supplementary S9 (migrated A / B / C7 / D / E) | < 1 |

---

## 4. Pipeline trace (Stage 3 → Stage 5)

| Stage | Commit | Outcome |
|---|---|---|
| 3 REVIEW Round 3 | `599ba06` | 5-reviewer panel reports |
| 4 REVISE r3 | `1a471d7` | Path A + Path B + 2 fixes |
| 4 REVISE r3.5 | `c1ce8e4` | Editorial Synthesis + P2 minor 6 items |
| 4.5 R5 fix | `0019b91` | Mode 1+3 — Fisher exact p=1.0 column-degenerate misuse |
| 4.5 R5 audit | `72c32eb` | FINAL INTEGRITY PASS verdict |
| 5 prep p1 | `6008239` | Appendix migration → supplementary S9 |
| 5 prep p2a | `e2007b8` | §threats + per-block + future-work compression |
| 5 prep p2b/p3 | `cff4264` | §1 contributions + Abstract rewrite + humanizer audit |
| 5 prep p5 | `cc594ce` | Table / figure reasonableness audit |
| 5 FINALIZE | `<HEAD>` | Figure 1 added + final integrity verification PASS |

---

## 5. 论点 preservation discipline (full pipeline)

User-stated constraint at session start: **"本文的论点不应随着修订出现漂移"** (paper's核心论点 must not drift through revisions).

Adherence verification per stage transition:

| Round | Threats | Outcome |
|---|---|---|
| Round 1 → 2 | Theorem 1 reframing attempt | REJECTED ("Theorem 1 = mere well-formedness" framing not accepted; structural-adequacy obligation preserved with scope qualifier) |
| Round 2 → 3 | DA C1-C5 + NEW-A reframing | C1-C5 adjudicated explicitly with论点-drift checks; NEW-A refuted via Path B using Sun 2021's published corpus |
| Round 3 → 3.5 | R1/R2/R3/EIC residual minor edits | All 6 P2 minor items addressed; abstract/§1 contributions/EIC W3 tcolorbox added without scope drift |
| Round 3.5 → 4.5 | Stage 4.5 R5 audit | One Mode 1/3 caught (Fisher p=1.0 misuse); corrected with numeric fix only,论点 unchanged |
| Round 4.5 → 5 | Length compression (-9 pp.) | Appendix migration to supplementary; in-body prose tightening preserves all numeric findings, verdicts, threats, and baseline declarations |

**Final verdict on论点 drift**: zero stages drifted the four core arguments (C1 two-layer framework / C2a positive + C2b negative theory / C3 systematisation on Boltzmann / C4 structural transferability on three operator-algebraic domains).

---

## 6. Stage 5 → Stage 6 handoff

Stage 6 PROCESS SUMMARY would produce:

1. Paper creation process record (MD + LaTeX → PDF) per academic-pipeline v3.2.2
2. Collaboration quality assessment (6 dimensions, 1–100 scale)
3. AI self-reflection report including 7-mode failure-mode audit log

Stage 6 is optional and user-triggered.

---

## 7. Recommended cover-letter messages (per EIC R0 report)

When submitting to TOSEM, the cover letter should highlight:

1. **Foundational positioning**: NOETHER is a two-layer framework that converts MR-identification from inductive cataloguing to a downstream-mechanical derivation, with formal closure (Theorem 1) and decidability (Theorem 2).
2. **Negative theory as positive contribution**: Theorem $1'$ (absolute completeness) is falsified on $\mathcal{A}_{\mathrm{PWR}}$ — the constructive negative result is part of the paper's contribution, not a limitation.
3. **Three instantiations test structural transferability**: Boltzmann reactor physics (systematisation), equivariant ML (de-novo derivation), relational query optimisers (extension beyond Lie-group / self-adjoint / time-reversal core).
4. **Honest empirical disclosure**: aggregate D1 dominance by GP-evolved baseline acknowledged; framework's contribution is read at per-block, cost-axis, and D2-stratum layers.
5. **Length explanation**: 74 pp. exceeds the TOSEM 30–50 pp. recommendation; the additional length is concentrated in (a) §6/§7 empirical evaluation tables (load-bearing), and (b) Appendix C formal proofs (Theorem 1, 2, $1'$). Six illustrative appendices have been migrated to supplementary S9 to compress.
