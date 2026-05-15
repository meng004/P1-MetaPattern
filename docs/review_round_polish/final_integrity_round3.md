# Stage 4.5 FINAL INTEGRITY — Round 3 Verification Report

**Date**: 2026-05-15
**Verifier**: academic-pipeline orchestrator (from-scratch independent verification)
**Base commit**: `33db749` (Stage 4.5 R2 — Mode 1+3 BLOCKING fixes)
**Branch**: `feat/section-7-empirical-vs-sota`
**Verdict**: **PASS** — zero issues remain; pipeline ready to advance to Stage 5 FINALIZE pending user confirmation.

---

## 1. Verification scope

Per IRON RULE (academic-pipeline Anti-Pattern #6), this round verifies from scratch — not only the R2-targeted fixes but the full integrity surface.

Six work tasks were executed:

| # | Task | Status |
|---|------|--------|
| 1 | Verify R2 Mode 1 fixes (4 bib author lists) | ✓ |
| 2 | Verify R2 Mode 3 fixes (§6.6 three arithmetic/data items) | ✓ |
| 3 | From-scratch 5-phase integrity sweep | ✓ |
| 4 | 7-mode AI Research Failure Mode Checklist | ✓ |
| 5 | Compile loop + Undef audit | ✓ |
| 6 | Bib all-cited audit | ✓ |

---

## 2. R2 Mode 1 verification (4 bib author lists)

CrossRef / arXiv canonical lookup vs current `NOETHER_paper.bib`:

| Key | DOI / arXiv | Canonical authors | bib current | ✓ |
|---|---|---|---|---|
| `GPTMR2025` | 10.1016/j.infsof.2025.107828 | Yifan Zhang; Tsong Yueh Chen; Matthew Pike; Dave Towey; Zhihao Ying; Zhi Quan Zhou | matches | ✓ |
| `AutoMT2025` | arXiv 2510.19438 | Linfeng Liang; Chenkai Tan; Yao Deng; Yingfeng Cai; T. Y. Chen; Xi Zheng | matches | ✓ |
| `Ying2025MRPatterns` | 10.1002/stvr.70003 | Zhihao Ying; Dave Towey; Anthony Bellotti; Caslon Chua; Zhi Quan Zhou | matches | ✓ |
| `Altamimi2022MRSLR` | 10.1002/smr.2509 | Emran Altamimi; Abdullah Elkawakjy; Cagatay Catal | matches | ✓ |

**Verdict**: 4/4 ✓.

---

## 3. R2 Mode 3 verification (§6.6 three arithmetic items)

### 3.1 H3a.2 union arithmetic (~L1969)

Paper text (current): "Union coverage on the PIT-covered substrate is $22 + 4 + 15 = 41 / 52 = 78.8\%$ ... modestly above Set G alone's $37 / 52 = 71.2\%$ and materially above Set N alone's $26 / 52 = 50.0\%$."

Re-derivation:
- both = 22, N-only = 4, G-only = 15, neither = 11; total = 22+4+15+11 = 52 ✓
- Set N kills: 22 + 4 = 26 → 26/52 = 50.000% → "50.0%" ✓
- Set G kills: 22 + 15 = 37 → 37/52 = 71.154% → "71.2%" ✓
- Union: 22 + 4 + 15 = 41 → 41/52 = 78.846% → "78.8%" ✓
- delta (union − Set G) = 7.6 pp → "modestly above" ✓
- delta (union − Set N) = 28.8 pp → "materially above" ✓

### 3.2 T* prose (~L1693)

Paper text (current): "n=17, Set N kills 10, Set G kills 8, Set N exclusive 3, Set G exclusive 1, both 7, jointly missed 6, union 11/17=64.7%, +11.7pp."

Re-derivation:
- 10 + 8 − 7 (common) = 11 covered; 17 − 11 = 6 missed ✓
- Set N alone: 10 − 7 = 3 ✓
- Set G alone: 8 − 7 = 1 ✓
- Union: 11/17 = 64.706% → "64.7%" ✓
- Set N rate: 10/17 = 58.824% → "58.8%" ✓
- Set G rate: 8/17 = 47.059% → "47.1%" ✓
- diff: 58.8 − 47.1 = 11.7 pp → "+11.7pp" ✓

Wilson 95% CI:
- 10/17: p̂'≈0.572, half-width≈0.212 → [0.360, 0.784] — matches paper ✓
- 8/17: p̂'≈0.477, half-width≈0.214 → [0.263, 0.691] — paper states [0.262, 0.690] (rounding-consistent) ✓

### 3.3 Pooled footnote D2 denominator (~L1801)

Paper text (current): "the $5$ D2 mutants in the denominator".

Cross-check:
- §6.6 D2 stratum is explicitly stated at n=5
- §6.6 H3a.2 D2 footnote: Set N 0/5, Set G 3/5 → 3 b-cell discordances → pooled McNemar (b,c) = (15+3, 4) = (18, 4) on n=52+5=57 ✓

**Verdict**: 3/3 ✓.

---

## 4. From-scratch 5-phase integrity sweep

### Phase A — References

10 of 57 bib entries cross-verified via CrossRef DOI:

| Key | DOI | Source | ✓ |
|---|---|---|---|
| `GPTMR2025` | 10.1016/j.infsof.2025.107828 | CrossRef | ✓ |
| `AutoMT2025` | arXiv 2510.19438 | arXiv | ✓ |
| `Ying2025MRPatterns` | 10.1002/stvr.70003 | CrossRef | ✓ |
| `Altamimi2022MRSLR` | 10.1002/smr.2509 | CrossRef | ✓ |
| `GenMorph2024` | 10.1109/TSE.2024.3407840 | CrossRef | ✓ |
| `MRScout2024` | 10.1145/3656340 | CrossRef | ✓ |
| `Shin2024` | 10.1007/978-3-031-70245-7_9 | CrossRef | ✓ |
| `ChenMETRIC2016` | 10.1016/j.jss.2015.07.037 | CrossRef | ✓ |
| `SunMETRICplus2021` | 10.1109/TSE.2019.2934848 | CrossRef | ✓ |
| `Saha2019SupervisedMR` | 10.1109/aitest.2019.00019 (△ DOI not in bib) | CrossRef | △ |

Note (△): `Saha2019SupervisedMR` has no DOI in bib but verifies via CrossRef title+author match. Optional: add DOI in future polish round.

### Phase B — Citation context

Sampled cross-context references checked: METRIC / METRIC+ are correctly attributed in §2 related-work as structured MR-identification approaches; GenMorph is correctly attributed as GP-evolved baseline in §6.6 head-to-head; Wang2024QED is correctly attributed as the 145-unverified-cases substrate for §subsec:third-domain.

### Phase C — Statistical data

All §6.6 numerical claims re-derived: Wilson CIs, McNemar (b,c) pairs, kill counts, union arithmetic, percentage rounding. All match within rounding tolerance.

### Phase D — Originality + AI text characteristics

- em-dash (—, U+2014) count in `NOETHER_paper.tex`: **0**
- em-dash count in `NOETHER_paper.bib`: **0**
- AI-vocabulary scan (crucial / pivotal / delve / leverage / tapestry / underscore / robust signal / intricate / showcase / testament): **0 hits each**
- Soft hits inspected and ruled out:
  - `landscape` × 2 — "fitness landscape" / "loss landscape" (legitimate technical use)
  - `via` × 5 — citation / inline ρ_train / line ranges (legitimate)
  - `beyond` × 14 — scope statements ("beyond the Lie-group core", "beyond this case-study scope") (legitimate)
  - `yield` × 5 — template-yield / case-study-yield (legitimate)
- Surprise-language grep (surprising / unexpected / counterintuit / contrary to / in hindsight / we realized): **0 hits**

### Phase E — Claims

Abstract central claims sampled and traced to body:
- "five of six SUTs admitting an L_scale MR" → §subsec:l-blindness-confirmed L1103/L1334 ✓
- "Set N is dominated by the GP-evolved baseline on the scope-matched D1 stratum" → §6.6 head-to-head ✓
- "five PWR + five (A_equi/A_rel) = ten pairwise-independent extensions" → §subsec:negative-pwr Table tab:five-obstructions + §subsec:third-domain product-group/bundle-section/aggregate-project ✓
- "Theorem 1' is falsified on A_PWR via two independent counterexamples" → §subsec:negative-pwr Propositions 1+2 + Appendix C.6 ✓

---

## 5. 7-mode AI Research Failure Mode Checklist

| Mode | Description | R3 verdict | Evidence |
|---|---|---|---|
| 1 | Implementation bug passing AI self-review | **CLEAR** | R2 caught "26+4+15=45/52=86.5%" arithmetic bug (double-counted "both"); R3 re-derivation confirms current 22+4+15=41/52=78.8% |
| 2 | Hallucinated citation | **CLEAR** | R2 caught 4 bib author errors; R3 CrossRef/arXiv cross-verification on 10/57 entries all match |
| 3 | Hallucinated experimental result | **CLEAR** | R2 caught D2 denominator (5 not 2) + T* stale pre-codegen numbers; R3 verifies current numbers + Wilson CIs reproduce by hand |
| 4 | Shortcut reliance | **CLEAR** | Paper explicitly states "Set N is dominated by GP-evolved baseline on D1" + "head-to-head superiority claim is not asserted" — anti-shortcut framing |
| 5 | Bug-as-insight (surprise reframing) | **CLEAR** | grep for surprise/unexpected/counterintuitive/hindsight = 0 hits |
| 6 | Methodology fabrication | **CLEAR** | §6.6.1 DeepCrime pilot n=5/Set matches `supplementary/S3_case_study/deepcrime_pilot_summary.json` total=5/Set; analysis pipeline reproducible per `supplementary/S3_case_study/analysis.py` |
| 7 | Pipeline-level frame-lock | **CLEAR** | Paper actively presents framework falsifications (Theorem 1' false on A_PWR; 5+5 obstructions on A_equi/A_rel) rather than locking on framework-wins narrative |

Block conditions: no SUSPECTED, no INSUFFICIENT EVIDENCE on Modes 1/3/5/6. Pipeline does **not** block.

---

## 6. Compile loop + Undef audit (CLAUDE.md §3 step 2b)

```
xelatex (pass 1) → OK
bibtex          → OK
xelatex (pass 2) → OK
xelatex (pass 3) → OK
```

Audit (final pass):
- Undefined references: **0**
- "I didn't find" (bibtex): **0**
- "Missing character": **0**
- Pages: 76
- PDF size: 577,944 B

Soft warnings (not blockers per NEXT_STEPS.md §B):
- bibtex warnings: 66 (missing publisher / address / pages on conference & journal entries — flagged for optional future polish)
- Overfull/underfull boxes: 79 (typesetting nits, no missing characters)

---

## 7. Bib all-cited audit (CLAUDE.md §3 step 2a)

```python
cited count: 57
defined count: 57
uncited (defined but not cited): []
undefined (cited but not defined): []
```

Anonymous / placeholder grep: 0 hits (`Anonymous|anonymous reference|\[1\]|\[2\]|personal communication`).

---

## 8. Quality trajectory self-check (academic-pipeline IRON RULE)

| Question | Answer |
|---|---|
| Are all R2 (commit 33db749) fixes correctly applied to the .tex file? | Yes — verified line-by-line |
| Are the fixes themselves correct (i.e., the new values are right)? | Yes — re-derived from underlying data + canonical sources |
| Did R3 from-scratch sweep introduce any new findings beyond R2? | No new issues found; the corpus is internally consistent |
| Is R3 output quality ≥ R2 quality? | Yes — R2 reported targeted blockers; R3 adds independent confirmation + extends to 7-mode failure-mode audit |
| Are all required Stage 4.5 deliverables present? | Yes — see §1 task table |

---

## 9. Aggregate verdict

**PASS with zero ✗ and zero suspected failure modes.**

Pipeline state machine transition:
- Stage 4.5 FINAL INTEGRITY → PASS → ready to advance to Stage 5 FINALIZE

Per academic-pipeline IRON RULE, transition to Stage 5 requires explicit user confirmation at the MANDATORY checkpoint. See orchestrator response for the checkpoint presentation.

---

## 10. Deferred items (not blockers)

These items are explicitly tracked in `NEXT_STEPS.md` and are **not** Stage 4.5 PASS prerequisites:

- **NEXT_STEPS §B** — 66 bibtex warnings (missing publisher / address / pages on some entries; render-time non-issue; flagged for optional future polish round)
- **NEXT_STEPS §A** — arxiv author placeholders awaiting de-anonymisation at publication time
- **ISSUES/011** — Theorem 1' counterexample search on A_equi / A_rel (already partially landed in §subsec:third-domain; full survey artefacts in `theory/`)
- **ISSUES/012** — LRCA two-rater κ (deferred to P3 phase per CLAUDE.md §5)
- 79 overfull/underfull boxes (typesetting nits, no missing characters)

---

*End of report.*
