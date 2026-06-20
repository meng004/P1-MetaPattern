```json
{
  "overall_recommendation": "Reject",
  "reviewer_confidence_1to5": 5,
  "scores_1to5": {
    "soundness": 1,
    "novelty": 2,
    "significance": 2,
    "presentation": 1,
    "reproducibility": 1
  },
  "summary": "The paper proposes NOETHER, a framework for deriving metamorphic-relation classes from an empirically curated operator-block decomposition of a program family's governing equations. It defines a Translate-based algebra-induced MR space, proves closure and decidability results over that space, and reports several theoretical instantiations and empirical sanity checks across reactor physics, equivariant ML, relational query optimizers, and Java/ML mutation studies.",
  "strengths": [
    "The paper correctly distinguishes MR identification from MR fault-detection effectiveness in several places and explicitly states that many empirical results are secondary sanity checks rather than average-effectiveness evidence.",
    "The negative PWR discussion usefully recognizes that single-block Translate-style derivations miss important compositional or higher-order engineering MRs, which is a valuable limitation to surface.",
    "The paper attempts to connect MR patterns to explicit mathematical structures rather than treating pattern taxonomies as purely empirical catalogues.",
    "Some sections make unusually explicit boundary statements about scope, out-of-scope program families, and candidate ninth blocks."
  ],
  "publication_blockers": [
    {
      "section": "Sections 3.2, Appendix C.2, Theorem 1",
      "issue": "The central closure theorem is essentially definitional and does not establish a substantive completeness or adequacy result.",
      "why_fatal": "Definition 3 defines MR(A_P) as exactly the image of Translate from single-block invariants, and Theorem 1 then proves that every element of this image is assigned to a MetaPattern by CONSTRUCT-MP. This is a tautological well-formedness property, not a theory of MR identification at TOSEM level. The paper repeatedly uses this result rhetorically as structural adequacy or closure evidence, but it follows by construction and has no demonstrated connection to the practically relevant MR space."
    },
    {
      "section": "Section 3.2.4, Table 1, Theorem 2",
      "issue": "The decidability and polynomial-time complexity theorem is unsupported and technically false at the stated level of generality.",
      "why_fatal": "The paper assumes invariant extraction costs t_i and then concludes O(n max t_i log n), but the hard problem is exactly computing I_s and deciding equivalence of invariants/templates. For several blocks this is undecidable or not polynomial in the given representation: query equivalence under SQL/bag semantics, group invariant discovery, monotonicity of programs, convergence-rate recognition, and qualitative-dynamics extraction. The proof is an accounting exercise over assumed oracle costs rather than a complexity result."
    },
    {
      "section": "Sections 3.1, 3.2, Hypothesis 1, Definitions 1-4",
      "issue": "Core formal objects are underspecified and inconsistent with the claims built on them.",
      "why_fatal": "The 'program-induced operator algebra' is not an algebra in the usual sense, the operator set may act on inputs, outputs, methods, expressions, or trajectories, and the equivalence relation is defined semantically over all programs in a family without an effective representation. Block invariants quantify over canonical orders and pi-relations that are not formally specified. Several examples violate the stated framework, e.g., SQL bag semantics is treated through an idempotent semiring, although bags are not idempotent; 'conservation' appears in empirical tables although it is not one of the eight blocks; and limit/scaling/linearity are conflated under L*. The formal layer is therefore not sound enough to support the stated theorems."
    },
    {
      "section": "Sections 4-5, especially 5.2-5.4 and 5.7",
      "issue": "The empirical evaluation is not a valid test of the central claims and is affected by severe selection, construction, and circularity biases.",
      "why_fatal": "Key results are based on hand-constructed mutants designed to target NOETHER blocks, single-model pilots, single-author MR derivation, LLM-only 'independent' raters, reimplemented comparator subjects by the framework author, post-hoc equivalent-mutant filtering via LLM votes, and extensive future-work protocols reported alongside completed results. The paper itself admits many results are construct-validity demonstrations, not independent effectiveness evidence. These data cannot support claims about broader MR design-space coverage, transferability, or comparison with GenMorph/METRIC+/LLM/MR-Scout at TOSEM's empirical standard."
    },
    {
      "section": "Whole paper, especially Introduction, Related Work, Sections 3-5, Conclusion",
      "issue": "The manuscript is internally inconsistent, overlong, and mixes theory, protocols, pilots, completed studies, future work, and supplementary claims in a way that prevents reliable assessment.",
      "why_fatal": "There are contradictory statements about whether Theorem 1' is open or falsified, whether H1 is a hypothesis or tautology, whether comparison results are primary or secondary, and whether generated blocks are seven, eight, or include additional 'conservation'/'idempotence' blocks. Many claims are deferred to supplementary artifacts, future work, or non-existent appendices while still being used in argumentation. This prevents a reader from reconstructing a coherent contribution or validating the evidence chain."
    }
  ],
  "major_weaknesses": [
    {
      "section": "Section 3.3 Invariance-Blindness Theorem",
      "issue": "The theorem is mathematically narrow and partly circular: the detection kernel is defined as the set satisfying the same structural equations, and faithfulness is defined as equality to the compatible set.",
      "suggested_fix": "Recast the result as a precise linear-algebra lemma for explicitly represented finite-dimensional operators; separate assumptions, prove existence and construction of faithful witnesses for concrete representations, and stop generalizing beyond G and T*."
    },
    {
      "section": "Section 3.4 reactor and equivariant-ML instantiations",
      "issue": "Several claimed MR derivations are not clearly valid executable MRs. For example, training-trajectory time reversal for SGD is a debug harness property under strong assumptions, not a program-family MR for equivariant classifiers; the attention-adjoint MR is introduced via instrumentation/probes not necessarily exposed by the SUT.",
      "suggested_fix": "For each MR, state the exact SUT interface contract, preconditions, executable inputs, observations, tolerance, and why the relation must hold for all conforming implementations."
    },
    {
      "section": "Section 3.5 relational query optimizers",
      "issue": "The relational algebra treatment is technically inaccurate: bag semantics and SQL NULLs do not fit the stated idempotent semiring assumptions, and several listed rewrite identities are conditional or false under bag/NULL semantics.",
      "suggested_fix": "Restrict to a formally specified set-semantics relational algebra fragment, or provide a correct bag-semantics algebra and prove each rewrite under its side conditions."
    },
    {
      "section": "Section 5.1 primary MR-identification evidence",
      "issue": "Tables 6-8 are too coarse to be probative: binary block coverage with small, heterogeneous corpora does not demonstrate broader design-space coverage or external transfer.",
      "suggested_fix": "Use independently curated MR corpora, predefine the block mapping protocol, obtain human domain-expert labels, report disagreements, and compare against concrete baselines under the same units of analysis."
    },
    {
      "section": "Section 5.3 empirical vs SOTA",
      "issue": "The GenMorph comparison is not a fair or interpretable SOTA comparison. The subject selection is narrow, the MR sets are hand-derived, the D1/D2 stratification is author-defined, and Set G is sometimes absent due to tooling issues rather than method limitations.",
      "suggested_fix": "Run a clean benchmark with pre-registered subjects, multiple random seeds, tool versions fixed, no LLM equivalent-mutant adjudication unless validated, and present the comparison as exploratory unless powered."
    },
    {
      "section": "Data and Artifact Availability",
      "issue": "Reproducibility is not established by naming a Zenodo DOI. Many decisive claims depend on supplementary files not present in the manuscript, unpublished future-work items, or artifacts whose anonymization and content hash are not actually specified.",
      "suggested_fix": "Provide a minimal, executable replication package for one coherent study; include exact commands, expected outputs, version hashes, and raw data needed to regenerate every table used as evidence."
    }
  ],
  "minor_issues": [
    "The manuscript is far beyond a reasonable TOSEM article length and should be radically shortened before any resubmission.",
    "The title and Noether analogy are rhetorically heavy relative to the actual formal content.",
    "The paper is not anonymized despite claiming review anonymity: author names, affiliations, emails, funding, and artifact DOI are included.",
    "Several references appear unverifiable or future-dated, and the paper cites a 2026 arXiv DOI in ACM metadata.",
    "The notation is unstable: A_P, A_F, blocks, MetaPatterns, MR sets, and coverage denominators change across sections.",
    "Table numbering and references are likely broken; several tables and appendices are referred to as supplementary, future, or migrated while still carrying claims in the main text.",
    "Using LLM panels as independent raters should not be described with standard inter-rater reliability language without strong caveats and validation against human experts.",
    "The paper repeatedly states that certain work is 'committed as follow-up'; future commitments are not evidence."
  ],
  "questions_to_authors": [
    "What exactly is the effective input to CONSTRUCT-MP: source code, mathematical equations, an operator list supplied by experts, or a manually written block decomposition?",
    "Can you provide a non-tautological completeness or adequacy statement over a pre-existing MR universe not defined as the image of Translate?",
    "How is invariant extraction implemented for each block, and what is the representation of invariants and pi-relations used to decide equivalence?",
    "Why is SQL bag semantics modeled through an idempotent semiring, and under what exact semantics are the relational MRs valid?",
    "Which empirical tables are claimed as completed experiments, which are protocols, and which are future work?",
    "How many MR/block labels were assigned by independent human domain experts rather than by the authors or LLMs?",
    "Can you reproduce the main empirical claims without LLM equivalent-mutant adjudication and without subjects reimplemented by the framework author?",
    "What claim remains if Theorem 1 is explicitly labeled as a definitional well-formedness lemma rather than a closure or adequacy theorem?"
  ]
}
```

## Detailed reviewer report

### Overall assessment

I recommend **Reject**. The manuscript is ambitious and contains some potentially interesting ideas: using mathematical structure to guide MR-class identification, making boundaries explicit, and recognizing blind spots of structural oracles. However, at present it does not meet TOSEM's standards for technical soundness, empirical validity, or presentation.

The main problem is that the paper's formal core is not strong enough to support the claims placed on it. The central “closure” theorem is true only because the MR universe is defined to be the image of the construction. The complexity theorem assumes away invariant extraction and equivalence checking, which are the hard parts. The empirical sections then try to compensate with a very large collection of case studies, pilots, protocols, and supplementary claims, but these are affected by severe selection and construct-validity threats and are not organized into a coherent evidentiary chain.

### Strengths

1. **Correct high-level problem motivation.** MR identification is genuinely a bottleneck in metamorphic testing. The paper's desire to ground MR classes in program-family semantics rather than in post-hoc catalogues is a reasonable research direction.

2. **Explicit limitation awareness.** The paper repeatedly acknowledges that it studies MR identification rather than average fault-detection effectiveness. It also explicitly lists out-of-scope families and admits that the upstream block decomposition is empirical.

3. **Negative examples are useful in spirit.** The PWR discussion of rod-bank non-additivity and mixed moderator-temperature/boron dependence usefully illustrates that single-block MR templates miss important compositional engineering properties. This is one of the more valuable parts of the paper.

4. **Potentially useful vocabulary.** The notion of mapping MRs to structural sources such as symmetry, order, adjointness, limits, and rewriting could be useful as an organizing vocabulary if presented as a disciplined taxonomy rather than as a proved algebraic theory.

### Publication blockers

#### 1. The central closure theorem is tautological

**Location:** Section 3.2, Definition of algebra-induced MR, Theorem 1, Appendix C.2.

The paper defines an algebra-induced MR as one for which there exists a block invariant and a block such that:

\[
\rho = \mathrm{Translate}(\iota,s).
\]

CONSTRUCT-MP then constructs MetaPatterns from equivalence classes of such invariants. Theorem 1 states that every MR in this image is assigned to a MetaPattern. This follows immediately from the definition.

The manuscript sometimes admits this (“by-construction”), but still presents the result as a structural adequacy or closure guarantee. This is not a substantive completeness theorem. It does not show that NOETHER covers expert MRs, useful MRs, likely MRs, all MRs expressible over the program family, or even all natural single-block properties unless those are already encoded in the chosen Translate templates.

A TOSEM theory contribution must either prove a nontrivial property about an independently defined object or clearly present the result as a well-formedness lemma. Here the theorem is used as a pillar of the paper's contribution, but it is not strong enough to carry that role.

#### 2. The decidability and complexity theorem is unsupported

**Location:** Section 3.2.4, Theorem 2, Table 1.

Theorem 2 assumes a finite generating set and per-generator invariant-computation costs \(t_i\), then derives \(O(n \max_i t_i \log n)\). This is not a meaningful decidability result. The hard work is hidden in \(t_i\): computing invariants, checking equivalence of templates, and deciding whether a program family satisfies a block invariant.

For the blocks listed, these problems can be undecidable, representation-dependent, or computationally hard:

- program monotonicity is generally undecidable;
- SQL/query equivalence is undecidable in broad fragments and subtle even in restricted bag/NULL semantics;
- invariant discovery for group actions depends on the representation and can be nontrivial;
- convergence-rate recognition is not a generic computable property of programs;
- qualitative-dynamics classification is not an \(O(d)\) primitive in any general program representation.

The proof in Appendix C.2 is only an accounting proof conditional on oracles for the hard operations. It cannot support the statement “\(\mathbb{M}(\mathcal{A}_P)\) is computable in polynomial time” at the stated level.

#### 3. The formal definitions are too underspecified and inconsistent

**Location:** Section 3.1, Definitions 1-4, Hypothesis 1, Appendix C.1.

The paper's “program-induced operator algebra” is a tuple \((\mathcal{O}, \circ, \sim)\), but \(\mathcal{O}\) contains objects of different kinds: input transformations, output transformations, numerical methods, ODE trajectory feature extractors, SQL rewrite rules, training procedures, and method-comparison orders. This is not a coherent algebraic object without many additional typing and semantic constraints.

The definition of block invariant relies on:

- a finite operator set \(\Phi\);
- a relation \(\pi \subseteq (\mathcal{X}\times\mathcal{Y})^k\);
- a “canonical order specified by \(s\)”;
- equivalence “up to relabelling”.

These are not formally specified in a way that would allow independent reconstruction. Consequently, the quotient MetaPattern construction is not mathematically grounded.

There are also concrete inconsistencies:

- “Conservation” appears as an empirical block in later tables, but it is not one of the eight canonical blocks.
- The relational block is defined using an idempotent semiring, but the examples use SQL bag semantics; bag union is not idempotent.
- The limit block \(\mathcal{L}^*\) is used for scaling, linearity, training-size stability, inference idempotency, and convergence, which are different structures.
- The paper sometimes treats time reversal, SGD rollback, reversible networks, and training-script fixtures as the same kind of operator.

These issues are not cosmetic; they undermine the formal framework.

#### 4. The empirical evaluation is not valid evidence for the main claims

**Location:** Sections 4-5, especially Sections 5.2-5.7.

The empirical material is extensive but not convincing. Major problems include:

- **Constructed mutants:** Several mutation categories are explicitly designed so that a NOETHER MR uniquely detects them. The paper acknowledges this, but still uses the results as evidence of non-redundancy or transfer.
- **Single-author derivation:** Set N is derived by one author following the proposed method, creating a serious confirmation-bias risk.
- **LLM raters:** Several classification and equivalent-mutant decisions rely on LLM panels. Standard inter-rater reliability statistics are not appropriate evidence of independent expert agreement here.
- **Reimplemented comparator subjects:** The METRIC+ Path A subjects are reimplemented from prose by the same author who designed NOETHER.
- **Protocol/results/future-work blending:** The paper reports some items as protocols, some as completed results, some as “committed future work,” and some as supplementary claims. It is very difficult to identify what was actually performed and what evidential weight each result has.
- **Baseline unfairness:** GenMorph being N/A due to instance-method deserialization or JOR grammar limitations is a tooling comparison, not evidence that the underlying MR identification method is structurally weaker. MR-Scout is not run. METRIC+ is mostly mapped manually.

The evaluation could be valuable as exploratory evidence, but it cannot support the broad claims made in the abstract and conclusion.

#### 5. Presentation is not reviewable as a TOSEM manuscript

The manuscript is far too long and internally inconsistent. It contains:

- multiple restatements of the same boundary claims;
- many future-work commitments presented alongside evidence;
- migrated appendices and supplementary references used as if they were in the paper;
- contradictory descriptions of Theorem 1′ as open, falsified, and committed to follow-up;
- shifting terminology and denominators;
- excessive rhetorical framing around Noether.

A reviewer cannot reliably reconstruct the contribution, the completed experiments, or the precise claims.

### Additional major weaknesses

#### Invariance-Blindness Theorem is much narrower than advertised

The theorem applies only to finite-dimensional linear operator-implementation faults and only to \(G\) and \(T^*\) blocks under a faithfulness condition. The faithfulness condition is defined as the equality the theorem needs. The result is therefore a standard kernel/commutant observation, useful but not a broad statement about MR blind spots.

The empirical evidence in Section 5.9 is consistent with the theorem but does not substantially validate the full framework. It validates finite-dimensional linear algebra facts on small artificial instances.

#### Some MR examples are not valid program-family MRs

The training-trajectory time-reversal MR requires a special vanilla-SGD fixture, rollback, batch reordering, and carefully controlled optimizer assumptions. That is a debug harness property, not a general MR for equivariant ML programs. Similarly, the attention-adjoint MR may require forward hooks or probes not exposed by a standard interface.

For MR identification, this distinction matters: an algebraic identity is not an executable MR unless the SUT exposes the relevant controls and observations.

#### Relational optimizer section needs substantial correction

The relational section conflates relational algebra, SQL, bag semantics, NULL semantics, idempotent semirings, rewrite rules, and query-plan equivalence. Several listed equivalences require side conditions or fail under SQL bag/NULL semantics. This section should be rewritten around a formally specified fragment.

#### Binary block coverage is too weak

Binary coverage treats a block as covered if one MR is present. This ignores whether the MR is valid, executable, useful, nontrivial, or representative. A method can score high by enumerating one relation per author-defined block. This is not sufficient evidence of broader MR design-space coverage.

### Threats to validity

The paper acknowledges many threats, but acknowledgement is not mitigation. The most serious unresolved threats are:

- author-induced bias in block curation and MR derivation;
- circularity in deriving blocks from domains later used to “predict” MetaPatterns;
- lack of independent human expert validation;
- reliance on LLMs for labeling and equivalent-mutant adjudication;
- small and hand-selected empirical substrates;
- extensive use of constructed rather than naturally occurring defects;
- inadequate baseline execution for MR-Scout, METRIC+, and LLM methods;
- artifacts and supplementary files carrying essential claims not inspectable from the manuscript alone.

### What a revision would need to do

A publishable version would need to be a different, much narrower paper. I recommend the authors choose one of the following paths.

#### Option A: A taxonomy/framework paper

If the main contribution is a structured vocabulary for algebraically grounded MR identification:

1. Remove or demote Theorem 1 to a simple well-formedness lemma.
2. Remove the polynomial-time decidability claim unless invariant extraction is formally represented and proved.
3. Provide a precise, typed definition of the objects in the framework.
4. Present the eight blocks as an empirical taxonomy, not a theory with completeness implications.
5. Validate the taxonomy against independently curated MR corpora with human expert raters.

#### Option B: A formal-theory paper

If the main contribution is theory:

1. Restrict to one mathematically clean setting, e.g., finite-dimensional linear programs with group symmetries and adjoint operators.
2. Define the MR universe independently of the construction.
3. Prove a nontrivial characterization theorem over that universe.
4. Provide executable algorithms for invariant extraction and equivalence checking in that restricted setting.
5. Drop the broad empirical claims.

#### Option C: An empirical MR-identification paper

If the main contribution is empirical:

1. Pre-register a benchmark with independent subjects and baselines.
2. Use human expert labeling for block assignments.
3. Run GenMorph, MR-Scout, METRIC+/manual category enumeration, and LLM baselines under comparable conditions.
4. Avoid constructed mutants designed to favor NOETHER.
5. Report all results as exploratory unless adequately powered.

### Recommendation

The current manuscript should be rejected. It contains an interesting intuition, but the formal claims are either tautological or unsupported, and the empirical evidence is not sufficiently independent or coherent. A substantially narrowed and technically disciplined resubmission could become valuable, but the present paper is not close to TOSEM acceptance.