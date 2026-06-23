```json
{
  "overall_recommendation": "Reject",
  "reviewer_confidence_1to5": 5,
  "scores_1to5": {
    "soundness": 1,
    "novelty": 2,
    "significance": 2,
    "presentation": 1,
    "reproducibility": 2
  },
  "summary": "The paper proposes NOETHER, a framework for identifying metamorphic-relation MetaPatterns from a manually curated operator-block decomposition of a program family. It defines a Translate operator from block invariants to MRs, proves closure of the constructed MetaPattern set over the Translate image, and presents examples in reactor physics, equivariant ML, relational query optimizers, Java numerical routines, and several supplementary empirical comparisons. The paper explicitly limits claims about fault-detection superiority and frames most evidence as structural MR-identification evidence.",
  "strengths": [
    "The manuscript repeatedly distinguishes MR identification from MR fault-revealing effectiveness, which is an important distinction often blurred in MT papers.",
    "The negative PWR examples in Section 3.7 are useful because they identify concrete MR classes that the proposed single-block Translate mechanism cannot express.",
    "The paper attempts to expose boundaries and threats rather than claiming universal completeness; several out-of-scope classes are explicitly listed in Remarks 3.9 and 3.10.",
    "The idea of using algebraic structures such as symmetry, order, adjointness, and relational rewriting as an MR-design scaffold is potentially useful for domains with well-specified mathematical semantics."
  ],
  "publication_blockers": [
    {
      "section": "Sections 3.1--3.3, Theorem 1, Appendix C.1--C.3",
      "issue": "The central closure theorem is essentially definitional and does not establish a substantive completeness or discovery result.",
      "why_fatal": "Definition 3.4 defines MR(A_P) as exactly the image of Translate from a single block invariant; CONSTRUCT-MP then groups those same invariants into MetaPatterns; Theorem 1 proves every element of the image is in the constructed image. The manuscript acknowledges this is by construction, but still uses it throughout as the main theoretical warrant for structural adequacy. This cannot support the paper's claimed advance over empirical pattern catalogues at TOSEM level."
    },
    {
      "section": "Sections 3.1--3.3, Hypothesis 1, Remarks 3.6--3.11, Section 6",
      "issue": "The upstream block taxonomy and operator algebra are manually curated, underdefined, and not reproducibly derivable from programs.",
      "why_fatal": "The framework's substantive step is mapping a program family to A_P and to eight blocks, but this is an empirical hypothesis produced by expert judgment and sometimes by the same authors' prior catalogues. Definitions of 'operator algebra', 'block invariant', qualitative dynamics, method comparison, and relational equivalence are broad enough to classify examples post hoc but not precise enough for independent application. Without a reproducible algebra-distillation procedure, the claimed origin/transferability contribution is not technically established."
    },
    {
      "section": "Sections 4--5.5, especially Tables 4--18 and Sections 5.2--5.4",
      "issue": "The empirical evidence is not a valid test of the main claims and is heavily contaminated by constructed tasks, author-designed subjects, post hoc interpretation, and future/supplement-dependent results.",
      "why_fatal": "Many key comparisons are explicitly secondary, underpowered, constructed to target NOETHER blocks, or admitted to be future work. The case-study mutation set is designed so Set N uniquely covers category iv; the LLM baseline is template-matched into Set N and therefore cannot exceed it; the METRIC+ Java subjects are author re-implementations; several reported claims rely on supplementary artifacts or committed future work rather than manuscript evidence. These data cannot substantiate broader claims about coverage, transferability, maintenance, or practical value."
    },
    {
      "section": "Theorem 2, Table 1, Section 3.3.4, relational block discussion",
      "issue": "The complexity/decidability claim is vacuous or misleading because the hard problem is hidden inside assumed per-generator invariant computation costs t_i.",
      "why_fatal": "Theorem 2 assumes invariant extraction terminates in time t_i and then multiplies by max t_i; for relational equivalence and many operator identities, this is precisely the difficult or undecidable part. The claimed O(n max t_i log n) bound is therefore not a meaningful polynomial-time constructibility result in the input size of the algebraic specification, and it is repeatedly used as a theoretical contribution."
    },
    {
      "section": "Section 3.4, Theorem 3 and Section 5.6",
      "issue": "The Invariance-Blindness theorem is largely a restatement of the kernel definition under a faithfulness assumption and does not justify the empirical and theoretical weight placed on it.",
      "why_fatal": "The detection kernel is defined as the set of operators satisfying the MR witnesses, and faithfulness is defined as equality of that kernel with the full compatible set. The theorem then concludes the kernel equals the compatible set. The nontrivial condition is entirely in faithfulness, whose existence lemma is finite-dimensional linear algebra but does not show that the generated tests attain it in realistic programs. The theorem does not repair the tautological nature of the main closure result."
    },
    {
      "section": "Whole manuscript, especially Introduction, Sections 3--5, appendices",
      "issue": "The manuscript is not in a publishable TOSEM form: it is overlong, internally repetitive, contains unresolved contradictions, and mixes theory, protocols, pilots, future work, and supplementary claims without a coherent evidentiary hierarchy.",
      "why_fatal": "The paper repeatedly restates boundaries, introduces many side claims, reports numerous underpowered or non-load-bearing experiments, and depends on migrated appendices and supplementary files for central assertions. Several parts read as a response log rather than a mature article. This prevents reliable assessment and would require a complete rewrite, not a normal major revision."
    }
  ],
  "major_weaknesses": [
    {
      "section": "Related Work and Introduction",
      "issue": "Novelty over METRIC/METRIC+, symmetry-based testing, query-equivalence testing, and domain-specific MR taxonomies is overstated.",
      "suggested_fix": "Recast the contribution as an organizing design methodology for mathematically specified domains, not as a foundational closure theory. Provide a precise mapping of prior pattern systems to the proposed blocks and identify what genuinely cannot be expressed before claiming novelty."
    },
    {
      "section": "Definition 1 and Section 3.1",
      "issue": "The term 'operator algebra' is used nonstandardly for a tuple of operators, composition, and an equivalence relation, without closure, identities, linear structure, or semantic constraints.",
      "suggested_fix": "Either use a less formal term such as 'operator-structure specification' or give a rigorous algebraic definition with explicit domains, codomains, closure properties, and equality semantics."
    },
    {
      "section": "Definition 3.2 and CONSTRUCT-MP",
      "issue": "Block invariant extraction is specified as 'compute I_s' but no algorithm is given for the hard cases.",
      "suggested_fix": "For each block, define concrete input syntax, decision procedure or human protocol, failure modes, and output format. Separate executable algorithms from expert annotations."
    },
    {
      "section": "Section 3.6 equivariant ML",
      "issue": "Several derived MRs are questionable or artificial for the stated EGNN subject, especially the self-adjoint attention MR and training-time reversal MR.",
      "suggested_fix": "Use an actual architecture with the claimed attention bilinear form and reversible/vanilla-SGD fixture, or remove these as evidence and present them only as speculative templates."
    },
    {
      "section": "Section 3.5 reactor mapping",
      "issue": "The claimed prediction of m_adj and m_rev is circular because the blocks were curated partly from reactor physics and the comparator corpus is the authors' own prior catalogue.",
      "suggested_fix": "Use an independently authored reactor MR corpus not used in block curation, freeze the taxonomy beforehand, and have independent domain experts classify results."
    },
    {
      "section": "Section 5.1, Table 4",
      "issue": "The binary coverage table is too small and confusing; it treats 'Conservation' separately despite earlier saying conservation is a G-block instance.",
      "suggested_fix": "Use a consistent denominator, avoid counting a subcase as a separate block, and report per-corpus MR counts, executable status, and independent-labeler agreement."
    },
    {
      "section": "Sections 5.2--5.4",
      "issue": "The many empirical studies lack a clean preregistered primary endpoint and are hard to interpret collectively.",
      "suggested_fix": "Choose one or two primary evaluations aligned with the claim, preregister hypotheses and denominators, and move exploratory pilots/future protocols out of the main paper."
    },
    {
      "section": "Data and Artifact Availability",
      "issue": "The paper contains non-anonymized author metadata, emails, funding, and a public Zenodo DOI, which conflicts with double-blind review and also makes reproducibility claims unverifiable from the manuscript alone.",
      "suggested_fix": "Provide an anonymized artifact with fixed hash, complete manifest, scripts, and exact commands; remove identifying information in review versions."
    }
  ],
  "minor_issues": [
    "The title and Noether analogy are rhetorically strong but technically distracting; the analogy should be reduced substantially.",
    "There are many labels and section references that appear inconsistent or duplicated, e.g., repeated labels, migrated appendices, and references to supplementary items not included in the source.",
    "The manuscript alternates between seven and eight blocks in several places; conservation is sometimes counted separately despite being declared not a ninth block.",
    "Several citations appear prospective or difficult to verify from the source alone, including 2025/2026 items and unpublished supplementary protocols.",
    "The term 'polynomial-time' is repeatedly used without specifying the representation size of A_P.",
    "LLM-based inter-rater agreement is not a substitute for independent human expert agreement, especially for domain-specific block assignments.",
    "Many tables report statistical tests despite the authors acknowledging constructed or underpowered settings; these p-values should be removed or clearly relegated to exploratory appendices.",
    "The paper is far beyond normal TOSEM length and density; presentation quality is a serious barrier to review and replication."
  ],
  "questions_to_authors": [
    "What is the exact, independently reproducible procedure by which a new reviewer would derive A_P and D(A_P) for a previously unseen program family without using your judgment?",
    "What theorem remains if MR(A_P) is not defined as the image of Translate? Can NOETHER prove coverage over any externally specified MR language?",
    "Which empirical result is the single primary evidence for the main claim, and which results are exploratory or future work?",
    "How many of the block assignments and MR derivations have been validated by independent human domain experts rather than LLMs or authors?",
    "For Theorem 2, what is the input representation and why is invariant extraction not the dominant undecidable/intractable problem?",
    "Can the equivariant-ML self-adjoint and time-reversal MRs be demonstrated on an architecture that natively has the stated structures rather than via debug-time probes or fixtures?",
    "Why is conservation sometimes counted separately from G-block coverage after the paper explicitly says it is not a separate block?",
    "What artifacts are actually available at review time, and can every numeric table in the manuscript be regenerated from a single documented command?"
  ]
}
```

## Detailed referee report

### Overall recommendation: Reject

The manuscript contains an interesting intuition: many useful metamorphic relations in mathematically specified domains arise from recognizable structures such as symmetry, order, adjointness, convergence, qualitative dynamics, method comparison, and rewriting equivalence. As an MR-design heuristic, this is plausible and potentially useful. However, the submitted paper does not meet TOSEM’s bar for technical soundness, empirical rigor, or presentation. The main theorem is essentially definitional, the central upstream step is manual and under-specified, the complexity result hides the difficult part in an assumption, and the empirical evidence is a mixture of constructed case studies, pilots, protocols, future work, and supplement-dependent claims.

The manuscript is also far too long and internally diffuse. It reads less like a mature journal article and more like an accumulated response document containing a theory sketch, rebuttal caveats, many small empirical fragments, proposed protocols, future-work commitments, and migrated supplementary material. A publishable version would need to be rebuilt around a much narrower and more rigorously supported contribution.

---

## 1. Summary of the paper

The paper proposes NOETHER, a two-level framework for identifying metamorphic-relation classes from a program-family “operator algebra.” The upstream level manually curates an operator algebra and decomposes it into blocks such as symmetry, order, self-adjointness, time reversal, limits, qualitative dynamics, method comparison, and relational equivalence. The downstream level maps block invariants through `Translate` to MR classes / MetaPatterns and proves that the constructed MetaPattern set covers the `Translate`-reachable MR space.

The paper instantiates the idea in reactor physics, equivariant ML, relational query optimization, Java numerical routines, and several supplementary or semi-supplementary studies. It explicitly says the work is about MR identification rather than average fault-detection superiority.

---

## 2. Strengths

1. **The paper correctly separates MR identification from MR effectiveness.**  
   This is important. Many MT papers overclaim from mutation scores; this manuscript repeatedly states that it is not claiming average fault-detection superiority.

2. **The structural-design intuition is plausible.**  
   Symmetry, monotonicity, adjoint reciprocity, convergence, and query rewriting are real sources of MRs. Treating them as reusable design blocks could help practitioners in mathematical/scientific domains.

3. **The negative PWR discussion is useful.**  
   Section 3.7 is one of the more valuable parts: it identifies concrete reactor-physics MRs that the current single-block `Translate` mechanism cannot express. That is a real boundary analysis.

4. **The manuscript is unusually explicit about limitations.**  
   The authors repeatedly acknowledge circularity, constructed mutations, underpowered pilots, non-elimination of induction, and out-of-scope MR classes. This honesty is appreciated, but it also exposes that the claimed contribution is much weaker than the framing suggests.

---

## 3. Publication blockers

### Blocker 1: The central closure theorem is tautological

**Sections:** 3.2–3.3, Theorem 1, Appendix C.1–C.3.

Definition 3.4 defines an algebra-induced MR as one for which there exists a block invariant and a block such that

\[
\rho = \mathrm{Translate}(\iota, s).
\]

CONSTRUCT-MP then forms MetaPatterns by grouping those same invariants and their translated MRs. Theorem 1 states that every \(\rho \in \mathrm{MR}(\mathcal{A}_P)\) belongs to a unique constructed MetaPattern. This follows immediately from the definition of \(\mathrm{MR}(\mathcal{A}_P)\) as the `Translate` image and from the construction.

The manuscript acknowledges the by-construction nature, but still uses the theorem as a central theoretical warrant for “closure,” “structural adequacy,” and an advance over empirical catalogues. At TOSEM level, this is not enough. The theorem proves that the framework does not drop what it already defined as reachable. It does not show:

- that the block list is complete;
- that `Translate` captures practically important MRs;
- that independent users can derive the same MR space;
- that NOETHER discovers anything not already encoded by the expert who wrote the algebra;
- that the resulting MetaPatterns are superior to prior category systems.

The negative PWR examples in fact emphasize how narrow the theorem is.

### Blocker 2: The real contribution—the upstream algebra/block derivation—is manual and under-specified

**Sections:** 3.1, Hypothesis 1, Remarks 3.6–3.11, Section 6.

The crucial step is not Theorem 1; it is obtaining \(\mathcal{A}_P\) and \(\mathcal{D}(\mathcal{A}_P)\). This step is explicitly empirical and human-curated. The paper has no reproducible algorithm for it. The proposed six-step audit protocol appears only as future work in Section 7.2.

Definitions are too permissive:

- “Program-induced operator algebra” is not really an algebra in the standard sense; it is a set of operators with composition and an equivalence relation.
- “Qualitative-dynamics operator” includes extrema, inflection points, overshoot, S-curves, phase portraits, and broad comparison-theorem ideas.
- “Method-comparison operator” depends on a specified error norm and conditions, but these are not part of a formal input language.
- The relational block is defined by finite rewrite rules, but query equivalence and bag semantics subtleties are not rigorously handled.
- “Block invariant” assumes a relation \(\pi\) that already holds for every program in the family, but the hard task is discovering and validating such \(\pi\).

As a result, the method is not independently reproducible. A different expert could plausibly classify the same relation under a different block or introduce a new block. The paper’s LLM agreement audits do not solve this, because LLMs are not independent domain experts and may simply mirror the manuscript’s terminology.

### Blocker 3: The complexity theorem is not a meaningful polynomial-time result

**Sections:** 3.3.4, Theorem 2, Table 1.

Theorem 2 assumes each generator’s invariant computation terminates in time \(t_i\), then concludes time

\[
O(n \cdot \max_i t_i \cdot \log n).
\]

This hides the hard part inside \(t_i\). For many blocks, invariant extraction is exactly the difficult problem:

- discovering symmetries from a program or specification;
- proving monotonicity;
- proving self-adjointness under the correct inner product;
- proving convergence rates;
- checking method-comparison error bounds;
- proving query equivalence.

The paper admits relational query equivalence is undecidable in general and restricts to fixed rewrite sets. That is fine, but then the theorem should not be advertised as a general polynomial-time constructibility contribution. It is an accounting identity conditional on already-solved invariant extraction.

The input representation size is also not specified. “Polynomial in \(n\) and realized generator costs” is not the same as polynomial in the size of the algebra specification.

### Blocker 4: The Invariance-Blindness theorem is also mostly definitional

**Sections:** 3.4 and 5.6.

The theorem defines the detection kernel as the set of \(L\) satisfying the witness equations. It defines faithfulness as equality of the test kernel with the full compatible set. The theorem then proves that, under faithfulness, the kernel equals the compatible set. The only nontrivial issue is whether a practical finite witness set is faithful.

Lemma 3.1 says a finite faithful witness set exists in finite-dimensional linear spaces by choosing a spanning set of linear functionals. That is mathematically true, but it does not show that the framework’s generated tests find such a set, nor that realistic software interfaces expose the necessary witnesses. The empirical rank checks at \(N=8\) are limited sanity checks, not general support.

This result does not meaningfully strengthen the main closure theorem.

### Blocker 5: Empirical evidence is not a valid test of the main claims

**Sections:** 4–5.6.

The paper contains a large amount of empirical material, but most of it is not load-bearing, not independent, or not aligned with the main claim.

Examples:

- **Equivariant ML case study:** The cat-(iv) mutations are constructed so that the NOETHER time-reversal MR uniquely detects them. The paper admits this is construct-validity-controlled. This cannot support general effectiveness or even strong non-redundancy.
- **LLM baseline:** In the later Java study, Set L is template-matched against Set N’s catalogue. The paper explicitly says every executable Set L MR is by construction a byte-identical copy of a Set N pair, so Set L cannot exceed Set N. This is not a fair LLM baseline.
- **METRIC+ comparison:** The Path A Java/PIT subjects are re-implementations by the same author from Sun et al.’s prose specification. This is a major construct threat. Also, the result is parity, not evidence that NOETHER is better.
- **GenMorph comparison:** The aggregate D1 result favors GenMorph. The paper reframes this as per-block complementarity and cost-axis support, which may be acceptable as exploratory analysis but not as evidence of superiority.
- **Industrial reactor evidence:** The industrial corpora mainly show monotonicity/order relations. This supports only a narrow block, not the full framework.
- **Many claims rely on supplementary files or future work:** The manuscript repeatedly says full protocols, artifacts, and detailed results are in S3–S12 or committed as follow-up. A TOSEM paper cannot rely on “committed future work” as evidence.

The empirical section needs a single clean primary endpoint tied to the actual claim. Instead it gives many partial analyses whose interpretation changes depending on the result.

### Blocker 6: Presentation is not publishable

The manuscript is enormous, repetitive, and structurally unstable. It repeatedly restates the same boundary box, mixes theorem statements with caveats and future work, reports underpowered pilots next to formal claims, and moves central material into supplementary files. Many subsections read as rebuttal fragments rather than as an integrated article.

Specific presentation problems:

- The paper alternates between seven and eight blocks in places.
- “Conservation” is sometimes counted separately despite being declared a \(G\)-block instance.
- There are many prospective or unavailable references and many supplementary dependencies.
- The article includes author names, emails, funding, and a public DOI despite being described as anonymized for review.
- The paper’s contribution list is too long and overqualified.
- The Noether analogy is rhetorically overused and technically not necessary.

A major rewrite would be required even if the technical core were sound.

---

## 4. Additional major weaknesses

### 4.1 Novelty is overstated

The core idea that symmetries, monotonicity, conservation, and algebraic equivalences generate MRs is not new. Prior work on symmetric testing, METRIC/METRIC+, query-based MR patterns, compiler equivalence testing, ML invariance testing, and domain-specific scientific MRs already uses these structures, though often not under the “operator algebra” label.

The paper’s claimed novelty is the closure/derivation theory, but the closure theorem is definitional and the derivation is manual. Thus the novelty reduces to a broad taxonomy and a design methodology. That may be useful, but it should be framed modestly.

### 4.2 The block taxonomy lacks a principled basis

The eight blocks appear to be a heterogeneous list of useful mathematical structures:

1. symmetry;
2. order/linearity;
3. self-adjointness;
4. time reversal;
5. limits;
6. qualitative dynamics;
7. method comparison;
8. relational equivalence.

These are not derived from a common algebraic principle. Some are semantic properties, some are operator identities, some are testing strategies, and some are domain-specific artifacts. The paper admits this, but then uses the taxonomy as if it were a structural foundation.

The taxonomy also expands whenever counterexamples appear: metric stability, label consistency, probabilistic/martingale invariants, topological invariants, symplectic structure, sheaf/categorical constructions, empirical parameter-distribution divergence, aggregation-as-algebra, etc. This makes the framework look open-ended rather than foundational.

### 4.3 The definitions do not support independent mechanization

`CONSTRUCT-MP` says “compute the set of invariants \(\mathcal{I}_s\).” This is the hard part. Without a formal input language and block-specific extraction procedures, the algorithm is not executable in the sense required for a method paper.

The reference implementation cannot fix this if it only implements the examples chosen by the authors.

### 4.4 The equivariant-ML example is weak

The paper claims an adjoint-attention MR and a training-trajectory time-reversal MR. But the case-study subject is a compact EGNN, not a full SE(3)-Transformer with the stated attention structure. The manuscript admits the \(T^*\) block instantiation is an explicitly added symmetrized QK probe, not a property of the EGNN architecture. Similarly, the training-reversal MR is a debug-time fixture for vanilla SGD, while real equivariant pipelines use Adam/AdamW and would fail by construction.

These are not strong demonstrations of transfer. They are speculative templates plus a constructed harness.

### 4.5 The PWR negative examples undermine the stronger theoretical narrative

The negative PWR examples are useful, but they show that the current `Translate` signature misses important real MRs in the very domain used to motivate the framework. The manuscript tries to turn this into a contribution, but it weakens the “origin–closure–transferability” claim: the framework can classify what its templates already express and explicitly cannot express some standard domain MRs.

### 4.6 Statistical reporting is excessive and sometimes misleading

The paper reports many p-values and confidence intervals while simultaneously acknowledging that the corresponding designs are constructed, underpowered, or exploratory. This gives a false sense of inferential strength.

Examples:

- The 20-mutation EGNN case study is constructed around the MR blocks.
- The DeepCrime-style pilot has \(n=5\) and is explicitly underpowered.
- The D2 stratum has \(n=5\) after exclusions.
- Several per-block comparisons have overlapping Wilson intervals and are read directionally.

The paper should remove most inferential statistics or move them to exploratory appendices.

---

## 5. Reproducibility concerns

The paper claims artifacts on Zenodo and many supplementary materials S1–S12. However, from the manuscript alone it is not possible to verify the majority of numeric claims. The manuscript also says the camera-ready version will record hashes, which is not sufficient for review.

Specific concerns:

- Non-anonymized metadata conflicts with review-stage anonymization.
- Many claims depend on supplementary files not included in the LaTeX source.
- The artifact DOI may identify the authors.
- Some results are described as “committed future work” but are also integrated into the evidentiary narrative.
- The exact command needed to regenerate every table is not provided in the manuscript.
- LLM prompts, raw outputs, and equivalence votes are essential to several results but are external.

For a TOSEM artifact-heavy method paper, the artifact must be fixed, complete, and separable from future plans.

---

## 6. What a revision would need to do

This is beyond a normal major revision, but a viable future paper could emerge if radically narrowed.

### Required conceptual changes

1. **Stop presenting Theorem 1 as a substantive completeness theorem.**  
   Present it as a well-formedness invariant only.

2. **Define a precise input language for algebra specifications.**  
   For each block, specify:
   - required inputs;
   - admissible operators;
   - invariant syntax;
   - executable MR template;
   - failure modes;
   - whether extraction is automatic or human-certified.

3. **Make algebra distillation auditable.**  
   The six-step protocol in Section 7.2 should be moved to the method section and actually applied by independent human raters.

4. **Reframe novelty.**  
   The contribution should be: “a structured design methodology for MR identification in mathematically specified program families,” not a foundational theory solving the MetaPattern origin/closure problem.

5. **Choose one or two domains.**  
   The current paper covers too many domains superficially. A stronger version might focus on:
   - reactor physics plus one external mathematical library; or
   - relational query optimizers; or
   - Java numerical functions with GenMorph/METRIC+ comparison.

### Required empirical changes

1. **Define one primary evaluation question and endpoint.**  
   For example: “Do independent engineers using the NOETHER block protocol identify MR classes missed by a baseline protocol on held-out mathematical programs?”

2. **Use independent human subjects or independent expert raters.**  
   LLM agreement is not enough.

3. **Avoid constructed mutation categories as primary evidence.**  
   Use real bugs or neutral mutant sets not selected to favor NOETHER blocks.

4. **Compare to baselines fairly.**  
   Do not template-match LLM outputs into Set N and then compare coverage. Do not use author re-implementations as the main METRIC+ comparator.

5. **Separate exploratory pilots from confirmatory results.**  
   Underpowered pilots and future protocols should not be in the main evidence chain.

### Required presentation changes

1. Reduce the manuscript by at least half.
2. Remove repeated boundary boxes.
3. Move all nonessential pilots and protocols to supplementary material.
4. Use consistent block counting.
5. Remove the rhetorical Noether framing except perhaps in the introduction.
6. Provide a clean artifact manifest and exact reproduction commands.

---

## 7. Final assessment

The paper contains a potentially useful design idea, but the submitted manuscript does not establish it with the technical precision or empirical rigor required for TOSEM. The central theorem is tautological, the main upstream step is manual and underdefined, the empirical evidence is not a clean test of the claims, and the presentation is not journal-ready. I recommend rejection.