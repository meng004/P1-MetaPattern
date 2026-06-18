# NOETHER EIC ROI Repair Plan for Current External Panel

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the current TOSEM rewrite from a broad, effectiveness-looking manuscript into a focused MR-identification theory-method paper whose primary evidence is operator-block coverage, MR origin/boundary explanation, and cross-domain derivation.

**Architecture:** The revision does not add new experiments. It reorders and relabels existing evidence so that the main text answers EQ1/EQ2/EQ3 before any secondary mutation or GenMorph material. Theorem 1 is demoted from headline theory to a pipeline invariant, while IBT, PWR boundary results, and coverage evidence become the load-bearing claims.

**Tech Stack:** LaTeX `acmart`, existing supplementary evidence in `supplementary/S11_n5_industrial` and `supplementary/S12_n5_crossdomain`, external panel outputs in `docs/review_2026-06-18/llm_panel_current_rewrite_approved`.

---

## EIC Assessment of the Fresh Panel

The fresh panel is reasonable and directionally reliable. All five available model reports recommend **Major Revision**. The panel is not useful as a cardinal acceptance predictor, but it is useful as an issue-finding ensemble because the strongest concerns recur across vendors:

- Theorem 1 / `Translate` reads as definitional unless its role is demoted.
- Presentation length and scattered evidence are publication risks.
- Mutation/head-to-head sections keep pulling the manuscript into MR effectiveness.
- Upstream block curation needs a reproducible distillation protocol.
- PWR negative results are valued but need clearer boundary-proof exposition.

The highest-ROI response is therefore structural: change what the paper asks the reader to evaluate.

## Highest-ROI Tasks

### Task 1: Demote Theorem 1 in the Contribution Spine

**Goal:** Prevent reviewers from treating a by-construction closure invariant as the primary theoretical novelty.

**Files:**
- Modify: `NOETHER_paper_arxiv.tex`

**Acceptance Criteria:**
- Introduction contribution C2a calls Theorem 1 a closure invariant / well-formedness guarantee, not the paper's primary theoretical novelty.
- Boundary boxes say Theorem 1 establishes no-drop closure only within `Translate`-reachable MRs.
- Conclusion foregrounds IBT, PWR negative result, and origin/boundary framing before Theorem 1.

**Theme Drift Check:**
- Pass if the edited text says the contribution is MR identification / MR-class origin and boundary.
- Fail if the edited text implies average fault-detection or mutant-kill superiority.

### Task 2: Add Primary EQ1/EQ2/EQ3 Evidence Tables Before Secondary Results

**Goal:** Make the first Results reading unambiguously about MR identification.

**Files:**
- Modify: `NOETHER_paper_arxiv.tex`

**Acceptance Criteria:**
- A new subsection appears immediately after `Results and Discussion` opening.
- It contains three compact tables:
  1. `Expert vs NOETHER binary operator-block coverage`
  2. `Search-based vs NOETHER origin/boundary comparison`
  3. `Cross-domain shared operator-block derivation trace`
- Tables cite current evidence honestly:
  - S11: expert MR sets for SPARK/LOCUST/SACOS are 110/110 `O_{\le}` with 18 implicit/new monotone MRs.
  - S12: `numpy.linalg` and `numpy.fft` populate six blocks each with executable-hold checks.
- No table counts an operator block as covered solely because a structure exists in equations; it must have an explicit MR class or executable check.

**Theme Drift Check:**
- Pass if the tables use binary coverage, origin/boundary, and derivation trace.
- Fail if the tables use mutation score, kill rate, or effectiveness as the primary metric.

### Task 3: Mark Legacy Mutation / GenMorph Sections as Secondary

**Goal:** Stop reviewers from reading GenMorph dominance as a failed main result.

**Files:**
- Modify: `NOETHER_paper_arxiv.tex`

**Acceptance Criteria:**
- The first empirical subsection after the primary evidence tables is titled as secondary executability / complementarity evidence.
- The opening paragraph states that GenMorph and mutation material are retained to delimit objectives and demonstrate executable sanity checks, not to evaluate MR effectiveness.
- The phrase "primary empirical evidence" does not refer to mutation/head-to-head results.

**Theme Drift Check:**
- Pass if GenMorph is framed as complementary search-based MR generation.
- Fail if the manuscript suggests NOETHER wins an aggregate fault-detection contest.

### Task 4: Add Algebra-Distillation Protocol as Future Work / Limitation Bridge

**Goal:** Convert "upstream still human" from an uncontrolled weakness into an auditable workflow.

**Files:**
- Modify: `NOETHER_paper_arxiv.tex`

**Acceptance Criteria:**
- Future Work includes a concrete six-step algebra-distillation protocol:
  1. collect governing equations / operator definitions / boundary conditions,
  2. enumerate candidate operators,
  3. map each operator to blocks or mark orphan,
  4. derive MR classes only for block-supported invariants,
  5. record interface executability,
  6. independently audit block assignment.
- The protocol explicitly states that it is not full automation.

**Theme Drift Check:**
- Pass if design-for-testability remains future work / implication.
- Fail if the text claims the upstream extraction problem is solved.

### Task 5: Format Hygiene Pass

**Goal:** Remove easy desk-reject signals after the conceptual repair.

**Files:**
- Modify: `NOETHER_paper_arxiv.tex`
- Modify: `theory/ibt_section_3_4.tex`

**Acceptance Criteria:**
- No `TODO-ref` strings remain in included manuscript sources.
- The main figure has a `\Description{}`.
- Bibliography style is `ACM-Reference-Format`, or the report explicitly records why this is deferred.
- `pdflatex -interaction=nonstopmode -halt-on-error NOETHER_paper_arxiv.tex` succeeds.

**Theme Drift Check:**
- Pass if format edits do not alter claim scope.
- Fail if format edits introduce new substantive claims.

## Execution Order

1. Task 1
2. Task 2
3. Task 3
4. Task 4
5. Task 5
6. Verification: structure scan, drift scan, LaTeX compile

## Verification Commands

```bash
rtk rg -n "TODO-ref|Thread to validity|Weaknesses|primary empirical evidence|fault-detection superiority" NOETHER_paper_arxiv.tex theory/ibt_section_3_4.tex
rtk rg -n -F "\\begin{table" NOETHER_paper_arxiv.tex
rtk pdflatex -interaction=nonstopmode -halt-on-error NOETHER_paper_arxiv.tex
```

Expected:

- No `TODO-ref`, `Thread to validity`, or `Weaknesses`.
- Any `fault-detection superiority` occurrence appears only in explicit non-claim scope language.
- LaTeX exits 0.

