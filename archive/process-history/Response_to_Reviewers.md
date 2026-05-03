# Response to Reviewers

**Manuscript:** NOETHER — A Constructive Framework for Metamorphic Pattern
Discovery from Operator Algebras
**Submission to:** ACM Transactions on Software Engineering and Methodology
**Round:** First revision
**Decision received:** Major Revision

---

## Cover note

Dear Editor and Reviewers,

We thank the reviewers for their careful and constructive reading. The
three core concerns — the by-construction nature of Theorem 1, the limited
scope of the equivariant ML instantiation, and the empirical status of the
seven-block decomposition — have led to substantive revisions of the
manuscript. Six minor concerns have also been addressed.

We have **not** attempted to prove Theorem 1' (absolute completeness over
arbitrary properties expressible in the operator algebra). Reviewer 1's
suggestion path (a) — proving a non-trivial bridging theorem on
well-behaved operator algebras — would, in our reading, amount to
positively resolving Theorem 1', which we identify as open. Attempting
this in the revision window would risk producing an unsound argument.
Instead we have implemented paths (b) and (c) in full: explicit theorem
renaming, calibrated wording across Abstract / Introduction / Conclusion,
and a new Appendix C.5 cataloguing three concrete classes of MRs that
fall outside Theorem 1's scope. Section "Items we respectfully decline to
pursue" at the end of this letter explains this position.

The structure of this response follows the **R→A→C** convention used in
TOSEM revision letters: each comment is reported as **R**eviewer remark,
followed by **A**uthor response, followed by the specific **C**hange to
the manuscript. Sections in the changes column refer to the revised
manuscript. A **Diff Summary Table** at the end of the letter cross-lists
each change against the manuscript section and the supplementary archive.

Sincerely,
The Authors

---

## Section 1 — Core Concerns

### Concern 1.1 — Theorem 1's by-construction status

**R:** "Definition 10 defines algebra-induced MR as MRs admitting a
Translate derivation, and Theorem 1 then proves that CONSTRUCT-MP covers
all such MRs. The theorem proves that MRs defined as reachable by the
construction are reachable by the construction. The authors themselves
note in §4.3 that 'a sceptical reading might object that the
by-construction status makes the theorem near-tautological', and append
Theorem 1' as a stronger open conjecture. The current defence — that
empirical-adequacy frameworks such as PMCM do not even guarantee
constructive completeness — reduces Theorem 1's value to a
well-formedness guarantee, which is insufficient for TOSEM."

**A:** We accept this diagnosis in full. The original phrasing oversold a
closure result as a completeness result. We have not attempted path (a)
of the reviewer's suggestion (proving a stronger bridging theorem),
because as noted in our cover note that path is co-extensive with
solving Theorem 1'. We have implemented paths (b) and (c):

- **(b) explicit renaming:** Theorem 1 is now titled "Algebraic Closure
  under Translate" rather than "Constructive Completeness". Abstract,
  Introduction, and Conclusion have been calibrated to match. The word
  "completeness" is no longer used to characterise Theorem 1's content;
  it is reserved for Theorem 1' which remains open.
- **(c) explicit out-of-scope analysis:** Appendix C.5 (new) catalogues
  three concrete classes of MRs that fall outside Theorem 1's scope:
  probabilistic / distributional MRs without operator-algebraic
  representation; adversarial / input-set MRs whose perturbation set
  does not carry a group structure; and compositional MRs across multiple
  blocks under non-canonical derivations.

The substantive value of Theorem 1 in the revised version is no longer
"completeness" but rather the more precise claim that, given an algebraic
input, the MetaPattern set is provably exhaustive of MRs reachable
through Translate, with the limit precisely characterised. We agree this
is a less ambitious claim than the original phrasing suggested, and we
believe the calibration makes the paper more truthful.

**C:**
- §4.3: theorem renamed to "Algebraic Closure under \texttt{Translate}";
  new Remark "Scope of Theorem 1" enumerating three out-of-scope MR
  classes; defence paragraph rewritten to centre on the closure value
  rather than the well-formedness comparison.
- Definition 10 (§4.1) labelled `def:alg-induced` with explicit caveat
  about non-Translate-reachable properties.
- Abstract, Introduction (Closure question phrasing + Contribution C2),
  Conclusion: "completeness" → "closure" wherever the original phrasing
  characterised Theorem 1; Theorem 1' is now mentioned in the Abstract
  and Introduction as the open problem.
- Appendix C.5 added (new subsection): three concrete classes of
  out-of-scope MRs documented with worked descriptions.
- Appendix C.4: minor edit to point forward to §C.5 examples.

### Concern 1.2 — Equivariant ML instantiation too weak for C4

**R:** "Section 6 only demonstrates: (i) declared decomposition of
A_equi; (ii) derived rho_rot from the most obvious invariant — rotation;
(iii) gave 12 lines of Python. Rotation invariance is the 'hello world'
of equivariant network testing. The paper writes 'this section does not
claim empirical validation' and the 75% coverage figure has denominator
4. C4 is a claim, not evidence."

**A:** We accept this in full. The original Section 6 was a
conceptual-transfer demonstration only. Two additions strengthen it:

1. **Two non-trivial MR derivations** (§6.4, §6.5):
   - $\rho_{\mathrm{adj}}$ — an attention-trace duality MR derived from
     the self-adjoint block $T^*_{\mathrm{att}}$ for Hermitian-attention
     equivariant transformers. To our knowledge this MR has not been
     catalogued in the equivariant-ML MR-testing literature.
   - $\rho_{\mathrm{train\text{-}rev}}$ — a training-trajectory
     time-reversal MR derived from $\mathcal{T}^*_{\mathrm{seq}}$ for
     non-momentum optimisers. The MR is structurally distinct from any
     invariance MR and surfaces gradient-reversal sign errors that
     invariance probes do not detect. Also not catalogued in the
     surveyed literature.
2. **A small-scale comparative case study** (§6.6, new):
   We compare three MR sets of equal size on a public e3nn-based
   SE(3)-Transformer:
   - **N (NOETHER):** the five MRs derived in §6.3–§6.5;
   - **L (LLM-prompt baseline):** five MRs from a controlled GPT-4 prompt;
   - **B (literature baseline):** five MRs from prior MT-for-ML studies.

   Twenty mutations in four categories are injected. Two pre-registered
   hypotheses (H1 coverage; H2 unique detection of gradient-reversal sign
   errors via $\rho_{\mathrm{train\text{-}rev}}$) make the case study
   falsifiable. We have stated in advance how each combination of H1/H2
   outcomes will be interpreted, including the case in which N's
   detection rate is *lower* than L's: this is consistent with the
   framework's design (NOETHER prioritises structural coverage, not raw
   detection on a particular mutation set) and is reported transparently.

We have **deliberately limited** this to a case study. Section 6.6's
"Threats specific to this case study" subsection acknowledges: budget
asymmetry between LLM and NOETHER, baseline selection bias, and
hand-constructed mutation set. Broader empirical validation remains
future work, in line with the conceptual-transfer framing of §6.

The "75% coverage" figure has been removed (as the reviewer
recommended). Coverage is now reported as explicit population statements
qualified by Hypothesis 1 (the seven-block sufficiency hypothesis).

**C:**
- §6.3 Step 6: "75% of non-empty patterns covered" removed; replaced
  with explicit population statement and forward pointer to §6.4–§6.5.
- §6.4 added (new subsection): full derivation of $\rho_{\mathrm{adj}}$
  from $T^*_{\mathrm{att}}$, including invariant, Translate result, and
  executable form with $\tau_{\mathrm{adj}}$ specification.
- §6.5 added (new subsection): full derivation of
  $\rho_{\mathrm{train\text{-}rev}}$ from $\mathcal{T}^*_{\mathrm{seq}}$,
  including the round-trip identity, the executable MR form, and the
  framework's prediction that the MR fails for momentum-based optimisers.
- §6.6 added (new subsection): comparative case study with three MR
  sets, twenty mutations, pre-registered H1/H2 hypotheses, and stated
  interpretation conditions. The numerical results are placeholders
  (\texttt{[TBR]}) at this revision stage; supplementary archive S3
  contains the complete experimental harness.
- Supplementary archive S3 (new): SE(3)-equivariant testing harness
  including the three MR sets, twenty mutation generators, and runner.

### Concern 1.3 — Circularity between blocks and predictions

**R:** "T* (self-adjoint) and T_rev* (time-reversal) blocks were
themselves curated from program families that include reactor physics,
and the m_adj and m_rev 'predictions' correspond to those blocks. The
prediction is therefore circular in explanation order; the authors
admit m_adj and m_rev are 'standard textbook material'. The framework
re-classifies known structures rather than discovering new ones."

**A:** We accept this observation in full and have made it explicit
rather than papering over it. Three changes implement this acceptance:

1. **§5.3 candor paragraph (substantially expanded):** the original
   "A note on prediction" admitted that m_adj and m_rev are textbook
   material but stopped short of acknowledging the explanation-order
   circularity. The revised paragraph states that T* and T_rev* were
   themselves partly induced from reactor-physics structures, that the
   "prediction" is therefore better described as a *re-projection*, and
   that the substantive contribution is the *re-classification under a
   uniform algebraic structure* — not de novo discovery.
2. **§3.10 Hypothesis 1 (new):** the seven-block decomposition is now
   stated as an explicit, versioned hypothesis (Hypothesis 1, version
   1.0) with four enumerated families of likely counterexamples
   (symplectic, sheaf-theoretic, martingale, topological). This makes
   the empirical status of the decomposition rigorously checkable in
   subsequent work.
3. **§7.3 PMCM worked example (substantially expanded from one
   paragraph to a full subsection):** as the reviewer correctly
   observed, the deflationary direction — revealing that an inductive
   catalogue *over-counts* structurally distinct patterns — is
   resistant to the circularity caveat, since the over-counting is
   exposed by the canonical-block ordering itself, not by physics
   knowledge of T* / T_rev*. We have therefore developed §7.3 into
   NOETHER's most concrete contribution to practice. Two cases (Case A:
   sorting library; Case B: 84-MR PWR corpus) work through the
   re-grounding. We have introduced a formal definition of
   $\mathrm{coverage}_{\mathrm{NOETHER}}$ as the algebraically grounded
   analogue of PMCM's empirical coverage, and noted that the
   deflationary direction is not uniformly toward smaller grids — it is
   toward "the algebraically determined grid for the algebra in
   question", which may be larger or smaller than an inductive grid.

We do not claim the framework predicts patterns "out of nowhere". We
claim it provides a uniform algebraic placement for patterns that
domain experts had previously known but the inductive testing
catalogue had not isolated as structurally distinct.

**C:**
- §5.3 "A note on prediction (and an interpretive caveat)": expanded
  to acknowledge T* / T_rev* originated partly from reactor-physics
  inspection; recharacterise "prediction" as "re-projection";
  highlight non-circular deflationary direction (forward reference to
  §7.3).
- §3.10: new Hypothesis 1 (`hyp:seven-blocks`) with versioning,
  followed by Remark `rem:counterex` enumerating four counterexample
  families. Existing prose retained but updated to reference the
  hypothesis.
- §7.3 expanded from one paragraph to a full subsection with two case
  studies (sorting library, reactor-physics corpus), formal
  $\mathrm{coverage}_{\mathrm{NOETHER}}$ definition, and the
  observation that deflationary directionality is bidirectional.
- Conclusion updated to reference Hypothesis 1 and the open status of
  Theorem 1'.

---

## Section 2 — Minor Concerns

### Concern 2.1 — Theorem 2 complexity for infinite groups

**R:** "Table 1 gives O(|G|^2) for the symmetry block, which does not
apply to Lie groups (SO(3), §6) or unbounded discrete groups."

**A:** Accepted. Table 1 has been augmented with separate rows for
finite groups, Lie groups (with $d_G = \dim_{\mathbb{R}} \mathfrak{g}$),
and finitely generated infinite discrete groups (with truncation
parameter $K$). A new paragraph "On infinite groups" explains the
parameterisation and notes that closure is over the algebra of the
truncated group when truncation is required.

**C:** §4.4 Table 1 (`tab:complexity`) augmented; new paragraph added
after the table; instantiation parameters reported for Boltzmann
($n \le 14$, finite) and equivariant ML ($d_{\mathrm{SO}(3)}=3$, Lie).

### Concern 2.2 — Abstract / §4.3 wording inconsistency

**R:** "Abstract uses 'provable completeness' but §4.3 has retreated to
'well-formedness and closure guarantee'."

**A:** Accepted. Resolved jointly with Concern 1.1: Abstract,
Introduction, and Conclusion now use "closure" wherever they
characterise Theorem 1, and explicitly mention Theorem 1' as the open
absolute-completeness conjecture.

**C:** Abstract (line 67), Introduction (Closure question phrasing,
Contribution C2), §4.3 (theorem statement and surrounding text),
Conclusion (Closure summary).

### Concern 2.3 — Table 3 sampling principle

**R:** "Table 3 contains 12 of 84 MRs (14%) without stated sampling
principle."

**A:** Accepted. The selection protocol is now explicit (every
non-empty block represented; most-frequent canonical-form MR per block
selected first; sub-categories given at least one representative;
predicted MetaPatterns indicated in italics). The full 84-MR mapping
is provided as supplementary material S2.

**C:** §5.3 paragraph following Table 3 expanded with the four-step
selection protocol; §7.4 supplementary materials section now lists S2
explicitly.

### Concern 2.4 — Appendix A too brief

**R:** "Four equations, each only one paragraph. If used as
'confidence-strengthening evidence' at least one needs detailed
treatment."

**A:** Partially accepted. We have expanded the momentum equation
(§A.3, Galilean invariance) into a complete Step 1–4 derivation
parallel to §5 in detail, including the seven-block decomposition,
six concrete MRs, and the resulting MetaPattern set. The remaining
three subsections (heat, continuity, resonance slowing-down) retain
their concise form but each now carries a cross-reference to §A.3 as
the derivation template.

**C:** §A.3 expanded from one paragraph to a full derivation (≈ 1
page). §A.1, §A.2, §A.4 augmented with cross-references to §A.3.

### Concern 2.5 — §1 Noether analogy too long

**R:** "The opening paragraph on Noether's theorem (about a paragraph
long) is disproportionate to its actual function (just a naming
inspiration)."

**A:** Accepted. The opening has been compressed to its operational
content; historical and biographical detail has been moved to a
footnote.

**C:** §1 paragraph 1 (formerly lines 103–104) compressed by
approximately one-third; details moved to a footnote.

### Concern 2.6 — Anonymous references unverifiable

**R:** "References [1] and [2] are anonymised. The 84-MR corpus and
PWR analysis report (which support §5.3 and §A) cannot be
independently verified by reviewers without anonymised supplementary
materials."

**A:** Accepted. We have prepared a two-stage artefact release:

- **Review-stage:** an anonymised supplementary archive containing
  S1 (CONSTRUCT-MP implementation), S2 (full 84-MR PWR corpus with
  block annotations), S3 (SE(3)-equivariant case-study harness), and
  S4 (reproducibility manifest), submitted alongside the manuscript
  with a SHA-256 content hash.
- **Acceptance-stage:** the same archive will be deposited on Zenodo
  with a permanent DOI; the SHA-256 hash and DOI will be anchored in
  the camera-ready version; the blinded references "[1]" and "[2]"
  will be replaced by the canonical citations.

**C:** §7.4 (`subsec:artefact`) rewritten with two-stage structure
and explicit listing of S1–S4. `supplementary_README.md` provided as
the archive's manifest with anonymisation status documented.

---

## Section 3 — Items We Respectfully Decline to Pursue

### Concern 1.1 path (a) — proving a non-trivial bridging theorem

**R (suggestion path):** "Prove that on some class of well-behaved
operator algebras (e.g. finitely generated, separable Hilbert-space
acting), any MR expressible in first-order logic over $\mathcal{A}_P$'s
operators can be reduced to Translate-reachable form."

**Reason for declining:** As noted in our cover note, this path is
co-extensive with positively resolving Theorem 1' — which we identify
as an open problem (§C.4) and which we attempted before submission
without success. Accepting this path in the revision window risks
producing an unsound argument under deadline pressure. We believe
paths (b) (explicit renaming) and (c) (out-of-scope analysis) — both
of which we have implemented in full — adequately address the
rhetorical concern about "completeness" while leaving the open
question honestly open.

We respectfully request that the editor assess whether implementing
(b) + (c) is sufficient to meet the bar of TOSEM acceptance, given
that the alternative is to either (i) postpone publication until
Theorem 1' is resolved or (ii) attempt the proof under time pressure
and risk withdrawal.

---

## Diff Summary Table

| Concern | Manuscript section(s) | New environment(s) | Supplementary |
|---|---|---|---|
| 1.1 | §4.1, §4.3, Abstract, §1, §C.4, §C.5 (new) | `thm:closure`, `def:alg-induced`, `rem:scope`, `app:out-of-scope` | — |
| 1.2 | §6.3, §6.4 (new), §6.5 (new), §6.6 (new) | `subsec:rho-adj`, `subsec:rho-rev`, `subsec:case-study`, `tab:case-study` | S3 |
| 1.3 | §3.10, §5.3, §7.3 | `hyp:seven-blocks`, `rem:counterex`, `subsec:pmcm-worked` | — |
| 2.1 | §4.4 Table 1 + new paragraph | (table augmented) | — |
| 2.2 | Abstract, §1, §4.3, §8 | — | — |
| 2.3 | §5.3 protocol paragraph | — | S2 |
| 2.4 | §A.3 (expanded), §A.1, A.2, A.4 (cross-refs) | `app:momentum` | — |
| 2.5 | §1 paragraph 1 | — | — |
| 2.6 | §7.4 | `subsec:artefact` | S1, S2, S3, S4, README |

---

## Statistics on changes

| Metric | Before | After | Δ |
|---|---|---|---|
| Lines in `NOETHER_paper.tex` | 663 | 903 | +240 (+36%) |
| Sections (`\section`) | 8 | 8 | 0 |
| Subsections (`\subsection`) | 25 | 31 | +6 |
| Theorem-like environments | 12 | 16 | +4 |
| Cross-referenced labels | (existing) | +9 new | +9 |
| Supplementary files | 0 | 4 (S1–S4) | +4 |

The new subsections are §6.4 ($\rho_{\mathrm{adj}}$), §6.5
($\rho_{\mathrm{train\text{-}rev}}$), §6.6 (case study), §7.3 (PMCM
worked example), and the rewritten §7.4 (artefact). The new
theorem-like environments are `thm:closure` (renamed),
`hyp:seven-blocks`, and two `remark` environments.
