# ISSUE-011: Theorem 1' counterexample search for 𝒜_equi and 𝒜_rel

**Status**: open
**Owner**: local
**Branch**: theory/thm1prime-counterexample-search
**Opened**: 2026-05-10

## Why

The ARS-R2 revision (commit f07fe0b) added an "open Theorem 1'
question" paragraph in §subsec:third-domain (RDB section), conjecturing
that 𝒜_equi (SE(3)-equivariant ML algebra) and 𝒜_rel (relational
query optimiser idempotent semiring algebra) may admit Theorem 1'
counterexamples analogous to the two PWR counterexamples exhibited
on 𝒜_PWR in §subsec:negative-pwr (non-additivity of rod-bank
reactivity worth + second-order mixed dependence of k_eff).

The Theorem 1' open conjecture (absolute completeness of 𝕄(𝒜_P)
over arbitrary properties expressible in 𝒜_P) is currently:
- Falsified on 𝒜_PWR (two counterexamples, five structural
  obstructions in `\texttt{Translate}`'s signature; §subsec:negative-pwr).
- Open on 𝒜_equi (we conjecture SO(3) Lie-algebra forces closure;
  untested).
- Open on 𝒜_rel (we conjecture idempotent-semiring admits
  rewrite-template counterexamples among Wang2024QED's 145
  unverified cases; untested).

This issue tests both conjectures by searching for at least one
counterexample per algebra, with the same depth of structural
analysis as §subsec:negative-pwr (5 pairwise-independent
obstructions identified there).

## Scope

Concrete deliverables:
- `theory/equi_thm1prime_search.md`: structural analysis of 𝒜_equi.
  Catalogue candidate MRs of equivariant-ML programs that:
  (i) are formulable in 𝒜_equi's operator vocabulary;
  (ii) are not derivable from any single block of the 8-block
       decomposition under \texttt{Translate};
  (iii) have a published canonical form (citation required).
  Goal: identify ≥1 candidate or prove no candidate exists in the
  searched literature subset.
- `theory/rel_thm1prime_search.md`: same analysis for 𝒜_rel.
  Anchor against Wang2024QED's 145 unverified cases (Calcite
  + CockroachDB benchmarks). For each unverified case, classify
  whether (a) the equivalence is single-block-derivable (then it
  is not a Thm 1' counterexample), or (b) requires multi-block
  composition or extra structure (then it may be a counterexample).
- `theory/translate_extensions.md`: if counterexamples are found,
  draft sketch of the \texttt{Translate}-operator extensions
  required to absorb them (paralleling the 5 obstructions catalogue
  in §subsec:negative-pwr).
- Paper-side update: §subsec:third-domain open-question paragraph
  upgraded with the verdict (counterexample found / not found / open
  with documented search bounds).

## Out of scope

- Full formal proof of all candidate counterexamples; this is
  exploratory and identifies candidates with structural-obstruction
  sketches.
- Implementation of the \texttt{Translate}-extension proposals.
- Cross-domain generalisation beyond 𝒜_equi and 𝒜_rel; other
  domains (probabilistic / topological / etc.) are tracked under
  Remark~\ref{rem:counterex} ninth-block candidates.

## Success criteria

- [ ] 𝒜_equi: ≥3 candidate counterexamples surveyed (drawn from
      published equivariant-ML work: ThomasSmidt2018, Satorras2021EGNN,
      and similar). Verdict per candidate: counterexample /
      single-block-derivable / requires further analysis.
- [ ] 𝒜_rel: ≥10 of Wang2024QED's 145 unverified cases classified
      under the (a)/(b) scheme above. Verdict: how many are Thm 1'
      counterexample candidates.
- [ ] If ≥1 counterexample found in either algebra: structural-
      obstruction sketch drafted in `translate_extensions.md`,
      identifying which specific operator-signature extension is
      required.
- [ ] Paper-side: §subsec:third-domain open-question paragraph
      revised to report the verdict; if counterexamples found, also
      update C2 contribution + §1 Boundary-of-contribution list.
- [ ] Audit log of literature searched (papers consulted, search
      terms, dates) for reviewer transparency.

## References

- Paper commit `f07fe0b` §subsec:third-domain "open Theorem 1'
  question" paragraph
- §subsec:negative-pwr: the 𝒜_PWR counterexample template this
  issue mirrors
- Theorem 1' (Conjecture~\ref{conj:absolute}): the conjecture being
  tested
- Wang2024QED~\cite{Wang2024QED}: 145 unverified Calcite + CockroachDB
  pairs as the search substrate for 𝒜_rel
- Equivariant-ML literature: ThomasSmidt2018, Satorras2021EGNN, e3nn
  documentation; Murphy 2008's six-class characterisation as a
  starting taxonomy for 𝒜_equi candidates
