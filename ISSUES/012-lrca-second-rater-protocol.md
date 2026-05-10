# ISSUE-012: LRCA two-rater κ on Set N derivation

**Status**: open (deferred to P3 phase per CLAUDE.md §5)
**Owner**: local + second rater (TBD)
**Branch**: protocol/lrca-second-rater
**Opened**: 2026-05-10

## Why

The ARS R2 audit (round 1, Dimension 1.1) flagged that Set N's 30
hand-derived NOETHER MRs were produced by a single author following
CONSTRUCT-MP's four-step procedure, with no inter-rater reliability
check. Set N is the empirical product through which the framework's
"mechanical, polynomial-time" claim (Theorem 2) is evidenced; a
single-author derivation is method-evidence inconsistency a careful
TOSEM reviewer will catch.

The ARS-R2 revision (commit f07fe0b) added an explicit disclosure
in §subsec:reactor-mapping construct-validity paragraph (M10), but
deferred the actual two-rater κ to "industrial-port phase of
follow-up work" (CLAUDE.md §5 P3 phase: "工业 Java / C++ port + LRCA
二评者 κ — 未启动").

This issue formalises the LRCA (Limited-Rater Conformance Audit)
protocol, identifies the second rater, and executes a 3-5 SUT pilot
to obtain a Cohen's κ value. A pilot κ ≥ 0.7 corroborates
CONSTRUCT-MP's reproducibility under independent application.

## Scope

Concrete deliverables:
- `protocol/lrca_protocol.md`: written protocol for the second rater.
  Includes (i) CONSTRUCT-MP four-step description, (ii) 8-block
  reference card, (iii) per-SUT signature description, (iv) blind
  derivation procedure (rater does not see Set N's MRs prior to
  derivation), (v) coding scheme for κ computation (per-block MR
  agreement on each SUT).
- Second rater identification + onboarding (target: a software
  engineer or applied mathematician with domain familiarity but no
  prior involvement in NOETHER's design).
- Pilot SUT subset: 3-5 SUTs from §6.6's substrate, chosen to span
  block-coverage diversity (e.g., midpoint for G+T, exactLog2 for I,
  hypotSig for L+G, ComplexSignal.add for instance-method coverage).
- Independent rater outputs: `set_n_mrs_rater2/<subject>/<MR>.{jir,jor}.txt`,
  derived blind from Set N rater 1.
- κ computation: per-block agreement matrix, Cohen's κ aggregate +
  per-block breakdown, per-SUT verdict.
- `protocol/lrca_results.md`: report including κ value, per-block
  agreement table, disagreement analysis (where rater 2 derived a
  different MR for the same block, document why).

## Out of scope

- Full re-derivation of all 30 Set N MRs across 10 SUTs; pilot
  scale 3-5 SUTs is sufficient for Round 2.
- Cross-rater LLM ensemble (using LLMs as raters): out of scope
  because LRCA tests human rater reproducibility, not LLM-assisted.
  LLM-rater agreement is a separate question (not Dim 1.1).
- Fleiss κ across 3+ raters: pilot is two-rater Cohen's κ.

## Success criteria

- [ ] Protocol document committed; second rater onboarded.
- [ ] 3-5 SUTs derived independently by rater 2; rater 2's outputs
      committed.
- [ ] Cohen's κ computed; aggregate value reported.
- [ ] κ ≥ 0.7 (substantial agreement) on at least 3 of the 5 SUTs.
      If κ < 0.7, document the disagreements and update CONSTRUCT-MP's
      protocol description in `\S\ref{sec:framework}` to clarify
      ambiguous steps.
- [ ] Paper-side: §subsec:reactor-mapping construct-validity
      paragraph updated with the κ value; if κ ≥ 0.7, the M10
      "committed for industrial-port phase" sentence reframed as
      "pilot completed at κ = X.XX; full industrial port scheduled
      for P3".
- [ ] No SOP changes during the pilot (keep protocol stable across
      raters).

## References

- Paper commit `f07fe0b` §subsec:reactor-mapping construct-validity
  paragraph M10 (single-author disclosure + LRCA commitment)
- ARS R2 report Dimension 1.1: `../docs/review_round_ars_r2/ars_r2_round1.md`
- CLAUDE.md §5 P-series roadmap: P3 phase already-anchored slot for
  this work ("工业 Java / C++ port + LRCA 二评者 κ — 未启动")
- CONSTRUCT-MP four-step procedure: `\S\ref{sec:framework}` of
  `NOETHER_paper.tex`
- 8-block reference: Hypothesis~\ref{hyp:seven-blocks},
  §subsec:decomposition
