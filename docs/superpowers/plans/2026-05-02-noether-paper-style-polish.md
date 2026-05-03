# NOETHER Paper Style Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Polish `NOETHER_paper.tex` into natural, idiomatic, reviewer-facing academic English while removing AI-like prose, translationese, overclaiming, and terminological drift.

**Architecture:** Treat `NOETHER_paper.tex` as the source of truth, use `NOETHER_paper_draft.md` only as provenance/reference, and keep every edit traceable through an audit file. The work proceeds from global style rules to section-level rewriting, then to terminology, citations, LaTeX compilation, and final integrity checks.

**Tech Stack:** LaTeX (`acmart`), BibTeX, Markdown audit notes, shell verification commands with mandatory `rtk` prefix in this workspace.

---

## Scope And Assumptions

Primary file:
- Modify: `NOETHER_paper.tex`

Reference files:
- Read-only reference: `NOETHER_paper_draft.md`
- Read-only bibliography unless a citation key is actually broken: `NOETHER_paper.bib`
- Read-only review context: `NOETHER_review_reports.md`, `NOETHER_review_round2.md`, `NOETHER_re_review.md`, `NOETHER_revision_response.md`, `NOETHER_final_integrity_log.md`

New working files:
- Create: `style_audit/NOETHER_style_sheet.md`
- Create: `style_audit/NOETHER_edit_log.md`
- Create: `style_audit/NOETHER_ai_translationese_audit.md`
- Create: `style_audit/NOETHER_final_language_check.md`

Assumption about the user's wording:
- "口语化、翻译化" is implemented as "natural academic English": shorter, more idiomatic sentences, less translated-from-Chinese phrasing, but not casual conversation.
- The paper remains a theoretical software-engineering paper for TOSEM/TSE-like readership.
- Terminology must preserve the current research positioning: `metamorphic relation identification`, `MetaPattern`, `operator algebra`, `constructive completeness`, `algebra-induced MR space`, `upstream layer`, and `downstream layer`.

Non-goals:
- Do not change the paper's scientific claims.
- Do not invent new citations.
- Do not silently strengthen the theorem claims.
- Do not rewrite mathematical definitions unless the sentence-level prose around them is unclear.
- Do not convert British/American spelling globally until the target venue style is chosen; for this pass, preserve the existing British spelling unless a phrase is unnatural.

## Global Editing Rules

Use these rules in every task:

1. Keep claims calibrated: prefer "we show", "we argue", "we instantiate", "the framework provides" over "we revolutionize", "paradigm-shifting", or unsupported "first" claims unless already defended.
2. Remove AI-like connective padding: reduce "furthermore", "moreover", "it is worth noting", "significant", "comprehensive", "robust", "seamless", "leverage", "utilize", "delve", "underscore" unless technically necessary.
3. Replace translationese with idiomatic academic English:
   - "the problem has not been closed" -> "the problem remains open"
   - "the paper conducts a discussion on" -> "the paper discusses"
   - "from the perspective of" -> "in terms of" or delete
   - "make contributions as follows" -> "This paper makes four contributions"
4. Prefer concrete verbs:
   - "provides a derivation procedure" can remain if mathematically accurate.
   - "has advanced rapidly" is acceptable.
   - "achieves a good effect" must be replaced with a measurable claim or removed.
5. Preserve technical nouns exactly unless the style sheet changes them:
   - `metamorphic testing (MT)`
   - `metamorphic relation (MR)`
   - `MetaPattern (MP)`
   - `operator algebra`
   - `program-induced operator algebra`
   - `constructive completeness`
   - `canonical-block ordering`
   - `equivariant machine learning`
6. On first use, define abbreviation once. After first use, use the abbreviation consistently.
7. Prefer one idea per sentence in the abstract and introduction. Break sentences longer than 45 words unless mathematical notation requires otherwise.
8. Keep reviewer-facing humility: when a block decomposition is empirical, say so directly.
9. Do not introduce casual contractions such as "can't", "doesn't", or "we're".
10. Every edited section must preserve all `\label{...}`, `\cite{...}`, theorem references, and equation references.

## Task 1: Establish Style Baseline And Terminology Sheet

**Files:**
- Create: `style_audit/NOETHER_style_sheet.md`
- Create: `style_audit/NOETHER_ai_translationese_audit.md`
- Read: `NOETHER_paper.tex`
- Read: `NOETHER_final_integrity_log.md`

- [ ] **Step 1: Create the style sheet**

Create `style_audit/NOETHER_style_sheet.md` with this structure:

```markdown
# NOETHER Style Sheet

## Target Register

Natural, precise academic English for software-engineering and formal-methods reviewers. The prose should read as written by a careful researcher, not as promotional copy or literal translation.

## Spelling And Venue Convention

- Preserve the current British spellings already used in the manuscript: `recognised`, `organise`, `systematises`, `artefact`.
- Preserve ACM/TOSEM LaTeX conventions in `NOETHER_paper.tex`.

## Canonical Terms

| Canonical term | Allowed abbreviation | Do not use |
|---|---:|---|
| metamorphic testing | MT | metamorphic test technology |
| metamorphic relation | MR | metamorphic relationship |
| metamorphic relation identification | MR identification | MR recognition in body prose |
| MetaPattern | MP after definition | meta pattern, meta-pattern |
| operator algebra | none | operator-algebra theory unless naming the approach |
| program-induced operator algebra | none | program algebra if ambiguity is possible |
| constructive completeness | none | absolute completeness unless discussing the conjecture |
| algebra-induced MR space | none | entire MR space |
| upstream layer | none | upper layer |
| downstream layer | none | lower layer |

## Claim Calibration

- Use `constructive completeness` only for completeness over the algebra-induced MR space.
- Use `first` only where the manuscript explicitly scopes the claim and cites prior work.
- Use `predicts` only for structurally derived MetaPatterns or systematic absences; otherwise use `suggests`, `derives`, or `classifies`.

## Preferred Sentence Patterns

- Prefer: `NOETHER derives MetaPatterns from invariants of a program-induced operator algebra.`
- Avoid: `NOETHER is able to effectively derive MetaPatterns by leveraging the invariants of the program-induced operator algebra.`
- Prefer: `The seven-block decomposition remains empirical.`
- Avoid: `It is worth noting that the seven-block decomposition is actually still empirical.`
```

- [ ] **Step 2: Run a first AI/translationese scan**

Run:

```bash
rtk rg -n "It is worth noting|Moreover|Furthermore|significant|comprehensive|robust|seamless|leverage|utilize|delve|underscore|paradigm|novel|first|effectively|in order to|from the perspective of|conduct|play an important role|very|clearly|obviously" NOETHER_paper.tex
```

Expected:
- The command prints candidate lines.
- Some matches are legitimate technical prose; do not mechanically delete all matches.

- [ ] **Step 3: Save the scan results**

Create `style_audit/NOETHER_ai_translationese_audit.md` with this structure:

```markdown
# NOETHER AI And Translationese Audit

## Scan Command

`rtk rg -n "It is worth noting|Moreover|Furthermore|significant|comprehensive|robust|seamless|leverage|utilize|delve|underscore|paradigm|novel|first|effectively|in order to|from the perspective of|conduct|play an important role|very|clearly|obviously" NOETHER_paper.tex`

## Required Manual Review

| Location | Phrase | Decision | Rewrite principle |
|---|---|---|---|
| `NOETHER_paper.tex:65` | `the first constructive framework` | keep only if scoped and defended | preserve but ensure limitations remain explicit |

## General Decisions

- Replace promotional adjectives with specific claims.
- Keep `paradigm-level consequences` only if the surrounding argument justifies the phrase; otherwise replace with `structural consequences`.
- Keep `first` only where the novelty claim is scoped to `constructive framework with provable completeness for MetaPattern discovery`.
```

- [ ] **Step 4: Verify files exist**

Run:

```bash
rtk ls -la style_audit
```

Expected:
- `NOETHER_style_sheet.md` exists.
- `NOETHER_ai_translationese_audit.md` exists.

## Task 2: Polish Abstract, Keywords, And Contribution Framing

**Files:**
- Modify: `NOETHER_paper.tex`
- Modify: `style_audit/NOETHER_edit_log.md`
- Reference: `style_audit/NOETHER_style_sheet.md`

- [ ] **Step 1: Back up the current manuscript**

Run:

```bash
rtk cp NOETHER_paper.tex NOETHER_paper.before-style-polish.tex
```

Expected:
- `NOETHER_paper.before-style-polish.tex` exists and has the same size as the pre-edit manuscript.

- [ ] **Step 2: Rewrite the abstract for natural academic English**

Edit only the text inside:

```latex
\begin{abstract}
...
\end{abstract}
```

Required rewrite direction:
- Split the first sentence into two or three sentences.
- Reduce stacked parentheticals.
- Preserve the seven-block list.
- Preserve Theorem 1 and Theorem 2 claims exactly in scope.
- Preserve the empirical/upstream and mechanical/downstream calibration.
- Replace any overlong sentence with shorter sentences that retain the same claim.

Example target style:

```latex
Metamorphic Testing (MT) is now recognised in IEEE/ISO software-testing standards and is widely recommended for testing AI systems. Its progress, however, remains constrained by metamorphic relation (MR) identification. This step still depends heavily on tester domain knowledge, and the resulting MR sets are difficult to reuse across teams and domains.
```

- [ ] **Step 3: Rewrite the contribution bullets**

Edit the `\begin{itemize}` contribution list in the introduction.

Required rewrite direction:
- Keep labels `C1` to `C4`.
- Start each contribution with a concrete verb: `introduce`, `prove`, `instantiate`, `demonstrate`.
- Remove duplicated claims already stated in the abstract.
- Keep the caution that predicted MetaPatterns are not de novo discoveries.

Example target style:

```latex
\item \textbf{C1.} We introduce NOETHER, a hybrid framework that combines an empirically curated seven-block decomposition with a constructive algorithm for deriving MetaPatterns from a program-induced operator algebra.
```

- [ ] **Step 4: Log the edit**

Append to `style_audit/NOETHER_edit_log.md`:

```markdown
## Abstract And Contributions

- Edited range: abstract and introduction contribution list in `NOETHER_paper.tex`.
- Main changes: shortened long sentences, reduced promotional wording, preserved theorem scope and empirical/upstream calibration.
- Claims changed: none.
- Citations changed: none.
```

- [ ] **Step 5: Compile after the abstract pass**

Run:

```bash
rtk tectonic NOETHER_paper.tex
```

Expected:
- Compilation succeeds, or fails only because `tectonic` is not installed.

Fallback if `tectonic` is unavailable:

```bash
rtk pdflatex -interaction=nonstopmode NOETHER_paper.tex
```

Expected:
- `NOETHER_paper.pdf` is produced, or LaTeX reports a specific syntax error introduced by the edit.

## Task 3: Polish Introduction And Problem Framing

**Files:**
- Modify: `NOETHER_paper.tex`
- Modify: `style_audit/NOETHER_edit_log.md`
- Reference: `NOETHER_review_reports.md`
- Reference: `NOETHER_revision_response.md`

- [ ] **Step 1: Identify introduction boundaries**

Run:

```bash
rtk rg -n "\\\\section\\{Introduction\\}|\\\\section\\{Background and Related Work\\}" NOETHER_paper.tex
```

Expected:
- The command prints the line for `Introduction` and the following `Background and Related Work` section.

- [ ] **Step 2: Rewrite the Noether analogy conservatively**

Edit the opening paragraphs so they:
- Keep the structural homage.
- Avoid implying the paper imports Noether's theorem directly.
- Avoid grand phrasing such as `paradigm-level` unless the claim is immediately justified.

Preferred replacement pattern:

```latex
We do not invoke Noether's theorem as a theorem about programs. Program semantics and metamorphic relations do not provide the action functional that the theorem requires. The analogy is instead methodological: a catalogue of observed invariants can sometimes be replaced by a derivation procedure grounded in structure.
```

- [ ] **Step 3: Rewrite the MR identification bottleneck paragraph**

Required rewrite direction:
- Use `MR identification` after the first definition.
- Make the bottleneck concrete: domain knowledge, inconsistent formulations, low reuse.
- Remove broad claims about the whole field unless cited.

- [ ] **Step 4: Rewrite `origin--closure--transferability gap` paragraph**

Required rewrite direction:
- Keep the three terms `origin`, `closure`, and `transferability`.
- Replace any inflated causal phrasing with concrete reviewer-facing logic.
- Preserve the distinction between tooling limitations and foundational limitations.

Example target style:

```latex
We refer to this as the origin--closure--transferability gap. The gap matters because it explains why MR sets continue to grow as one-off artefacts: without a structural source, there is no clear boundary on what the pattern space contains; without a transfer rule, relations written for one family rarely move cleanly to another.
```

- [ ] **Step 5: Compile after the introduction pass**

Run:

```bash
rtk tectonic NOETHER_paper.tex
```

Expected:
- No LaTeX syntax errors from edited prose.

- [ ] **Step 6: Log the edit**

Append to `style_audit/NOETHER_edit_log.md`:

```markdown
## Introduction

- Edited range: `\section{Introduction}`.
- Main changes: made the Noether analogy more conservative, clarified MR identification bottleneck, reduced translationese and overclaiming.
- Claims changed: none.
- Citations changed: none.
```

## Task 4: Polish Related Work For Reviewer Readability

**Files:**
- Modify: `NOETHER_paper.tex`
- Modify: `style_audit/NOETHER_edit_log.md`
- Reference: `NOETHER_paper.bib`

- [ ] **Step 1: Check related-work subsections**

Run:

```bash
rtk rg -n "\\\\subsection\\{" NOETHER_paper.tex
```

Expected:
- The output includes the related-work subsections for MT/MR fundamentals, METRIC/METRIC+, automated MR identification, MetaPattern catalogues, and convergent diagnosis.

- [ ] **Step 2: Rewrite topic sentences**

For each related-work subsection, ensure the first sentence has this shape:
- Subject: the line of work.
- Action: what it contributes.
- Limitation: why NOETHER is still needed.

Example target style:

```latex
Structured MR identification has already moved the field away from ad hoc relation design. METRIC and METRIC+ organise MR construction through input and output categories, but those categories remain expert-curated and empirically validated rather than algebraically derived.
```

- [ ] **Step 3: Reduce list-like citation dumping**

When a paragraph contains three or more methods in one sentence, split it into:
- one sentence stating the line of work;
- one sentence giving representative methods;
- one sentence stating the shared limitation.

- [ ] **Step 4: Preserve citation-key integrity**

Run:

```bash
rtk rg -n "\\\\cite\\{[^}]+\\}" NOETHER_paper.tex
```

Expected:
- Citation keys remain unchanged unless a key is known broken.

- [ ] **Step 5: Compile after related-work pass**

Run:

```bash
rtk tectonic NOETHER_paper.tex
```

Expected:
- No LaTeX syntax errors.

- [ ] **Step 6: Log the edit**

Append to `style_audit/NOETHER_edit_log.md`:

```markdown
## Related Work

- Edited range: `\section{Background and Related Work}`.
- Main changes: made subsection openings more direct, reduced list-like method summaries, preserved citation keys.
- Claims changed: none.
- Citations changed: none.
```

## Task 5: Polish Theory Sections Without Weakening Formal Meaning

**Files:**
- Modify: `NOETHER_paper.tex`
- Modify: `style_audit/NOETHER_edit_log.md`

- [ ] **Step 1: Locate formal environments and definitions**

Run:

```bash
rtk rg -n "\\\\begin\\{definition\\}|\\\\begin\\{theorem\\}|\\\\begin\\{lemma\\}|\\\\begin\\{conjecture\\*\\}|\\\\section\\{Operator-Algebraic Preliminaries\\}|\\\\section\\{The NOETHER Framework\\}" NOETHER_paper.tex
```

Expected:
- The output identifies every formal block to protect during prose editing.

- [ ] **Step 2: Protect formal statements**

Do not change:
- theorem names;
- definition names;
- mathematical symbols;
- quantifier scope;
- algorithm step names;
- labels such as `\label{subsec:completeness}`.

Allowed edits:
- The sentence before a definition.
- The intuition paragraph after a definition.
- Example prose when it is wordy or translation-like.
- Discussion paragraphs explaining theorem scope.

- [ ] **Step 3: Rewrite intuition paragraphs**

For each definition with an `Intuition` paragraph:
- Keep it to one or two sentences.
- State what the object does in plain academic English.
- Avoid "simply", "obviously", "clearly", and "essentially" unless mathematically precise.

Example target style:

```latex
\emph{Intuition.} The operator algebra records the structural commitments shared by a program family: symmetries, linearities, comparison principles, and convergence laws. It abstracts these commitments away from any particular implementation.
```

- [ ] **Step 4: Rewrite theorem-scope discussion**

In the constructive-completeness discussion:
- Preserve the limitation that completeness is over the algebra-induced MR space.
- Preserve the distinction between Theorem 1 and the stronger open conjecture.
- Make the limitation sound like rigorous scope control, not an apology.

Example target style:

```latex
The theorem is intentionally scoped. It proves completeness for MRs reachable through the framework's `Translate` construction from invariants in the block decomposition. It does not claim completeness over every property one might write in an arbitrary logic over program executions.
```

- [ ] **Step 5: Compile after theory pass**

Run:

```bash
rtk tectonic NOETHER_paper.tex
```

Expected:
- No LaTeX syntax errors.
- Formal references still resolve after repeated compilation.

- [ ] **Step 6: Log the edit**

Append to `style_audit/NOETHER_edit_log.md`:

```markdown
## Theory Sections

- Edited range: operator-algebra preliminaries and NOETHER framework sections.
- Main changes: tightened intuition paragraphs and theorem-scope prose while preserving formal statements.
- Claims changed: none.
- Citations changed: none.
```

## Task 6: Polish Reactor And Cross-Domain Case Sections

**Files:**
- Modify: `NOETHER_paper.tex`
- Modify: `style_audit/NOETHER_edit_log.md`
- Reference: `PWR_MR_Analysis_Report.md`
- Reference: `PWR_MR_MetaPattern_Analysis_Report.md`

- [ ] **Step 1: Locate case-study sections**

Run:

```bash
rtk rg -n "\\\\section\\{.*Reactor|\\\\section\\{.*Cross|Boltzmann|equivariant|SE\\(3\\)|point-cloud" NOETHER_paper.tex
```

Expected:
- The command identifies the reactor instantiation and equivariant ML sections.

- [ ] **Step 2: Make case-study prose concrete**

For each case-study subsection:
- Start with the program family and algebraic structure.
- Then state the derived MetaPattern.
- Then state what this adds beyond the inductive catalogue.

Preferred paragraph shape:

```latex
For the Boltzmann transport equation, the relevant algebra contains geometric symmetries, order relations induced by cross-section perturbations, adjoint structure, and limiting regimes. CONSTRUCT-MP therefore returns the corresponding MetaPattern classes directly from these blocks. The result is not a new empirical catalogue; it is an algebraic reconstruction of why the catalogue has the shape it has.
```

- [ ] **Step 3: Remove unsupported empirical language**

Replace:
- `we show empirically` if no experiment is performed;
- `validated` if the section provides a worked derivation rather than validation;
- `demonstrates` when `illustrates` is more accurate.

Keep:
- `instantiate`;
- `derive`;
- `systematise`;
- `classify`;
- `illustrate transferability`.

- [ ] **Step 4: Compile after case-section pass**

Run:

```bash
rtk tectonic NOETHER_paper.tex
```

Expected:
- No LaTeX syntax errors.

- [ ] **Step 5: Log the edit**

Append to `style_audit/NOETHER_edit_log.md`:

```markdown
## Reactor And Cross-Domain Sections

- Edited range: reactor instantiation and equivariant ML instantiation.
- Main changes: made case-study prose more concrete, replaced validation-like wording with derivation/systematisation wording where appropriate.
- Claims changed: none.
- Citations changed: none.
```

## Task 7: Polish Discussion, Threats, Limitations, And Conclusion

**Files:**
- Modify: `NOETHER_paper.tex`
- Modify: `style_audit/NOETHER_edit_log.md`

- [ ] **Step 1: Locate discussion and conclusion**

Run:

```bash
rtk rg -n "\\\\section\\{Discussion\\}|\\\\section\\{Threats|\\\\section\\{Conclusion\\}|\\\\section\\{Limitations" NOETHER_paper.tex
```

Expected:
- The command identifies the closing sections.

- [ ] **Step 2: Make limitations direct and non-defensive**

Required rewrite direction:
- State the upstream curation limitation directly.
- State what the paper does not evaluate.
- State why those omissions are future work rather than current claims.

Example target style:

```latex
The main limitation is upstream. NOETHER assumes that a program family's operator algebra has already been distilled. This paper does not automate that distillation, nor does it compare MR-generation tools on a shared benchmark.
```

- [ ] **Step 3: Remove inflated closing rhetoric**

Replace broad closing claims with scoped claims:
- `has acquired its first constructively complete foundation` can remain only if the paragraph restates `under the stated algebra-induced scope`.
- Replace `transforms the field` with `changes the status of the downstream construction from empirical search to scoped derivation`.

- [ ] **Step 4: Compile after closing-section pass**

Run:

```bash
rtk tectonic NOETHER_paper.tex
```

Expected:
- No LaTeX syntax errors.

- [ ] **Step 5: Log the edit**

Append to `style_audit/NOETHER_edit_log.md`:

```markdown
## Discussion And Conclusion

- Edited range: discussion, threats/limitations, conclusion.
- Main changes: made limitations direct, reduced closing rhetoric, preserved scoped contribution.
- Claims changed: none.
- Citations changed: none.
```

## Task 8: Run Whole-Manuscript Terminology And Consistency Pass

**Files:**
- Modify: `NOETHER_paper.tex`
- Modify: `style_audit/NOETHER_final_language_check.md`
- Reference: `style_audit/NOETHER_style_sheet.md`

- [ ] **Step 1: Check canonical terms**

Run:

```bash
rtk rg -n "metamorphic relationship|MR recognition|meta pattern|meta-pattern|upper layer|lower layer|absolute completeness|entire MR space|operator-algebra theory" NOETHER_paper.tex
```

Expected:
- No matches, except `absolute completeness` if it appears only in the open conjecture discussion.

- [ ] **Step 2: Check abbreviation discipline**

Run:

```bash
rtk rg -n "\\bMT\\b|\\bMR\\b|\\bMP\\b|MetaPattern|metamorphic testing|metamorphic relation" NOETHER_paper.tex
```

Expected:
- First uses define abbreviations.
- Later uses are consistent.

- [ ] **Step 3: Re-run AI/translationese scan**

Run:

```bash
rtk rg -n "It is worth noting|Moreover|Furthermore|significant|comprehensive|robust|seamless|leverage|utilize|delve|underscore|paradigm|novel|effectively|in order to|from the perspective of|conduct|play an important role|very|clearly|obviously" NOETHER_paper.tex
```

Expected:
- Zero or few matches.
- Any remaining match is documented as intentionally retained.

- [ ] **Step 4: Write final language check**

Create `style_audit/NOETHER_final_language_check.md`:

```markdown
# NOETHER Final Language Check

## Terminology

- `metamorphic relation identification`: checked.
- `MetaPattern`: checked.
- `constructive completeness`: checked.
- `upstream layer` / `downstream layer`: checked.

## AI-Like Prose

- Scan rerun after edits.
- Remaining flagged phrases are retained only where technically justified.

## Translationese

- Long stacked sentences in abstract/introduction split.
- Topic sentences in related work made direct.
- Limitations phrased directly rather than defensively.

## Claim Calibration

- Completeness remains scoped to the algebra-induced MR space.
- Upstream empirical curation remains explicit.
- No new citation or theorem claim introduced during language polishing.
```

## Task 9: Final Build And Diff Review

**Files:**
- Verify: `NOETHER_paper.tex`
- Verify: `NOETHER_paper.pdf`
- Verify: `style_audit/NOETHER_edit_log.md`
- Verify: `style_audit/NOETHER_final_language_check.md`

- [ ] **Step 1: Run final LaTeX build**

Preferred:

```bash
rtk tectonic NOETHER_paper.tex
```

Expected:
- `NOETHER_paper.pdf` builds successfully.

Fallback:

```bash
rtk pdflatex -interaction=nonstopmode NOETHER_paper.tex
rtk bibtex NOETHER_paper
rtk pdflatex -interaction=nonstopmode NOETHER_paper.tex
rtk pdflatex -interaction=nonstopmode NOETHER_paper.tex
```

Expected:
- `NOETHER_paper.pdf` builds successfully.
- No undefined references remain in the final LaTeX output.

- [ ] **Step 2: Review manuscript diff against backup**

Run:

```bash
rtk diff -u NOETHER_paper.before-style-polish.tex NOETHER_paper.tex
```

Expected:
- Diff contains prose/style changes.
- No accidental deletion of theorem environments, labels, citation keys, equations, or appendices.

- [ ] **Step 3: Check labels and citations survived**

Run:

```bash
rtk rg -n "\\\\label\\{|\\\\ref\\{|\\\\cite\\{" NOETHER_paper.tex
```

Expected:
- Existing labels, references, and citation commands are present.

- [ ] **Step 4: Final audit log entry**

Append to `style_audit/NOETHER_edit_log.md`:

```markdown
## Final Build And Diff Review

- Build command: `rtk tectonic NOETHER_paper.tex`
- Build result: pass/fail recorded during execution.
- Diff reviewed against: `NOETHER_paper.before-style-polish.tex`
- Structural issues found: none, unless recorded below.
```

- [ ] **Step 5: Final acceptance criteria**

The pass is complete only when all of the following are true:
- `NOETHER_paper.tex` compiles.
- The abstract is shorter, clearer, and less stacked.
- The introduction no longer reads like AI-generated promotional prose.
- Related work has direct topic sentences and clear gap statements.
- Formal statements are preserved.
- Completeness claims remain explicitly scoped.
- Terminology follows `style_audit/NOETHER_style_sheet.md`.
- The final AI/translationese scan has no unexplained high-risk phrase.
- `style_audit/NOETHER_edit_log.md` records the edited ranges and confirms no scientific claim changes.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-02-noether-paper-style-polish.md`.

Two execution options:

1. **Subagent-Driven (recommended)** - dispatch a fresh subagent per task and review between tasks.
2. **Inline Execution** - execute tasks in this session using `superpowers:executing-plans`, with checkpoints after each major section.

Because this workspace is not currently a Git repository, execution should use `NOETHER_paper.before-style-polish.tex` and the `style_audit/` files for traceability unless the user first chooses to initialise Git.
