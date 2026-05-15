# Stage 4.5 FINAL INTEGRITY — Round 5

**Manuscript**: NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
**Reviewed commit**: `0019b91` (after Round 3 P2 minor + Mode 1/3 fix)
**Auditor**: integrity_verification_agent (Stage 4.5 R5)
**Audit date**: 2026-05-15
**Audit mode**: final-check (Anti-Pattern #6 — verified from scratch, not just re-check known issues)

---

## 1. Overall verdict

**PASS** with one fix applied during this round (Mode 1/3, see §3).

| Gate | Threshold | Actual | Status |
|---|---|---|---|
| LaTeX undefined refs | 0 | 0 | PASS |
| BibTeX unresolved | 0 | 0 | PASS |
| Missing character warnings | 0 | 0 | PASS |
| em-dash (U+2014) | 0 | 0 | PASS |
| bib cited == defined | 0 mismatch | 58 == 58 | PASS |
| Pages | (TOSEM 30-50 pp.) | 83 | EXCEEDED (escalated to EIC, see Round 3 Editorial Decision §4 EIC-m1) |

---

## 2. 5-phase citation audit

### Phase 1: Reference verification

All 14 Round 3 newly-cited references verified via `paper-search-mcp` three-tier fallback (CrossRef → arXiv → DBLP):

| Bib key | Verification | Source |
|---|---|---|
| `SunMETRICplus2021` | ✓ CrossRef | DOI 10.1109/TSE.2019.2934848 (Sun/Fu/Poon/Xie/Liu/Chen) |
| `Wang2024QED` | ✓ CrossRef | DOI 10.14778/3681954.3682024 (Wang/Pan/Cheung, VLDB 2024; abstract confirms 299/444 Calcite) |
| `Mohamed2024SQLTables` | ✓ CrossRef | DOI 10.29007/rlt7 (Mohamed/Reynolds/Tinelli/Barrett) |
| `Zhou2020SymmetryMRP` | ✓ CrossRef | DOI 10.1109/TSE.2018.2876433 (Zhou/Sun/Chen/Towey, TSE 2020 vol 46 issue 10) |
| `CohenWelling2016` | ✓ arXiv | 1602.07576 (Cohen/Welling) |
| `ThomasSmidt2018` | ✓ arXiv | 1802.08219 (Thomas/Smidt/Kearnes/Yang/Li/Kohlhoff/Riley) |
| `FuchsTransformer2020` | ✓ arXiv | 2006.10503 (Fuchs/Worrall/Fischer/Welling) |
| `Satorras2021EGNN` | ✓ arXiv | 2102.09844 (Satorras/Hoogeboom/Welling) |
| `Gomez2017Reversible` | ✓ arXiv | 1707.04585 (Gomez/Ren/Urtasun/Grosse) |
| `Cohen2019Gauge` | ✓ arXiv | 1902.04615 (Cohen/Weiler/Kicanaoglu/Welling) |
| `Zhou2022SPES` | ✓ DBLP | conf/icde/ZhouANHW22, DOI 10.1109/ICDE53745.2022.00250 |
| `BellGlasstone1970` | ✓ Textbook | Pre-existing — canonical reactor-physics textbook |
| `LewisMiller1993` | ✓ Textbook | Pre-existing — canonical neutron-transport textbook |
| `StammlerAbbate1983` | ✓ Textbook ISBN | 0-12-663320-7, Academic Press |

**Verdict**: zero unverifiable references; zero ✗ Phase 1.

### Phase 2: Citation context verification

Spot-checked the load-bearing new claims against cited source content:

| Claim | Citation | Source content | Match |
|---|---|---|---|
| QED verified 299/444 Calcite query pairs | `Wang2024QED` | CrossRef abstract: "Qed can verify 299 out of 444 query pairs extracted from the Calcite framework" | ✓ exact |
| Adjoint flux treatment in §6.3 of Bell & Glasstone | `BellGlasstone1970[\S6.3]` | Bell & Glasstone Ch.6 is variational methods including adjoint flux | ✓ textbook-canonical |
| MTC three-mechanism decomposition | `Stacey2007[\S3.4]`, `LamarshBaratta2001[\S8.3]` | Stacey §3.4 is moderator temperature coefficient | ✓ textbook-canonical |
| EGNN joint SO(3) × S_n action on point sets | `Satorras2021EGNN` | arXiv abstract: "equivariant to rotations, translations, reflections and permutations" | ✓ |
| SPES bag-semantics commutativity | `Zhou2022SPES` | DBLP title: "Symbolic Approach to Proving Query Equivalence Under Bag Semantics" | ✓ |
| Mohamed et al. SMT theory of tables and relations | `Mohamed2024SQLTables` | CrossRef abstract: "first- and second-order extensions to SMT theories ... for SQL queries with join, projection, and selection operations" | ✓ |
| Sun 2021 four subjects SPHONE/SBAGGAGE/SEXPENSE/SMEAL with 142/735/1130/3152 MR counts | `SunMETRICplus2021` | Sun 2021 §V experimental subjects + Table 17 (verified in prior reading) | ✓ |

**Verdict**: zero Mode 2 (citation hallucination) findings.

### Phase 3: Statistical data verification

| Claim | Numeric | Source / verification | Status |
|---|---|---|---|
| Commons-Math pooled Set N kill rate | 10/77 = 13.0% Wilson 95% CI [7.2%, 22.3%] | Hand-computed Wilson formula on (10, 77) — matches text | ✓ |
| Commons-Math G-block kill rate | 6/21 = 28.6% Wilson 95% CI [13.8%, 50.0%] | Pre-existing — independently verified | ✓ |
| Commons-Math D2 stratum kill rate | 2/29 = 6.9% (passes ≤ 10% prediction) | Pre-existing — independently verified | ✓ |
| McNemar pooled p | 0.0043 | Pre-existing — verified Round 2 | ✓ |
| McNemar D1-only p | 0.019 | Pre-existing — verified Round 2 | ✓ |
| OR = 3.75 / RD = +0.212 on (b, c) = (15, 4) | Round 2 addition | Standard formulas yield these values | ✓ |
| DeepCrime pilot N vs L paired test p | Text claimed Fisher p = 1.00 | **FAILED — Mode 1/3** | ✗ (fixed in commit 0019b91) |
| DeepCrime pilot N vs B paired test p | Text claimed Fisher p = 1.00 | **FAILED — Mode 1/3** | ✗ (fixed in commit 0019b91) |

**Verdict**: one Mode 1 + Mode 3 finding caught and fixed. Details in §3.

### Phase 4: Originality / anti-fabrication

No fabricated data in Round 3. Path A is citation-based corroboration (published literature mapping); Path B is NOETHER eight-block analysis applied to Sun 2021's published 4 subjects (independent corpus, not author-engineered).

The eight-block scope verdicts on Sun 2021 subjects are derivative from NOETHER's framework applied to Sun 2021's published category-choice specifications, not new empirical data collection.

**Verdict**: zero fabrication findings.

### Phase 5: Load-bearing claims

| Claim | Evidence chain | Status |
|---|---|---|
| Theorem 1 closure within explicit scope | Definition 13 scope qualifier + §3.3 by-construction disclosure | ✓ |
| Theorem 1' falsified on A_PWR | Appendix C.6.1 five-extension exhaustion proof | ✓ |
| Three-domain structural transferability | Three §subsec instantiations + Path A citation corroboration | ✓ |
| L*-blindness 5/6 on 12-PUT | §7.4 verdict, robustness check at 9 thresholds | ✓ |
| Aggregate D1 dominance of Set G | §6.6 head, McNemar p=0.019/0.0043 explicit | ✓ |
| Per-block T* dominance of Set N | §6.6 per-block analysis | ✓ |
| NOETHER in-scope on Sun 2021 corpus | Path B Table tab:metricplus-sun2021-scope | ✓ |

---

## 3. Mode 1+3 finding: Fisher exact p=1.0 column-degenerate misuse

### Root cause

`supplementary/S3_case_study/deepcrime_pilot_stats.json` reported `fisher_NvsL.p_value = 1.0` and `fisher_NvsB.p_value = 1.0` by calling `scipy.stats.fisher_exact` on the 2x2 layout `[[a_both, b_N_only], [c_other_only, d_neither]] = [[0, 2], [0, 3]]`. Column 1 of that layout has sum = 0, so scipy returns p = 1.0 trivially — Fisher exact cannot reject when one column is structurally empty. The paired comparison was therefore never actually statistically tested.

### Correct tests

For n=5 paired binary outcomes:

| Test | Computation | Two-sided p |
|---|---|---|
| McNemar exact (paired) | binomial X=0 in n=2 trials at p_0=0.5 under H_0 | **0.500** |
| Fisher exact (unpaired analogue) | [[2, 3], [0, 5]] rows = Sets, cols = (detected, missed) | 0.4444 |

Both fail to reject H_0 at α=0.05; the qualitative reading ("underpowered at n=5") is preserved, only the numeric values change.

### Fixes applied (commit `0019b91`)

1. `NOETHER_paper.tex` Table `tab:deepcrime-contingency` caption: rewritten with McNemar exact two-sided p=0.500 + Fisher unpaired analogue p=0.444 + explicit test-choice rationale.
2. `NOETHER_paper.tex` paragraph "Reading the pilot (inferential verdict)": replaced "Fisher-exact p = 1.00" with the corrected McNemar / Fisher unpaired statement.
3. `supplementary/S3_case_study/deepcrime_pilot_stats.json`: added `mcnemar_exact_NvsL` and `mcnemar_exact_NvsB` (paired, correct test) plus `fisher_unpaired_NvsL` and `fisher_unpaired_NvsB` (unpaired analogue); deprecated the prior `fisher_NvsL` / `fisher_NvsB` p=1.0 entries with explicit `_status: INCORRECT` flag and root-cause explanation.

### 论点 preservation check

The pilot's载论文 reading "2/5 detection by Set N vs 0/5 by Set L and Set B, underpowered for α=0.05 inference, descriptive evidence consistent with framework's L*-block prediction direction" is preserved. Only the numeric value of the inferential test (now correctly stated as p=0.500 paired / p=0.444 unpaired) changes.

---

## 4. 7-mode AI failure mode checklist

| # | Mode | Status | Note |
|---|---|---|---|
| 1 | Implementation bug | **SUSPECTED → FIXED** | fisher_exact column-degenerate misuse (deepcrime_pilot_stats.json) caught and corrected |
| 2 | Citation hallucination | **CLEAR** | All 14 Round 3 cites verified via paper-search-mcp |
| 3 | Hallucinated results | **SUSPECTED → FIXED** | p=1.0 claim in §subsec:deepcrime-pilot was the downstream effect of Mode 1; both fixed jointly in commit `0019b91` |
| 4 | Shortcut reliance | **CLEAR** | Path A is explicit citation-based corroboration (disclosed at L599-602, L615-624, L905-910); Path B is independent corpus analysis (disclosed at §para:metricplus-sun2021-scope) |
| 5 | Bug-as-insight | **CLEAR** | No new findings dressing bugs as insights |
| 6 | Methodology fabrication | **CLEAR** | Path A method (citation-based corroboration) is standard; Path B method (eight-block scope analysis on Sun 2021's published subjects) is documented in supplementary S8 |
| 7 | Frame-lock | **CLEAR** | Round 3 Editorial Synthesis (`docs/review_round_polish/round3/editorial_decision.md`) adjudicates each DA CRITICAL against a 论点-drift check before accepting or refuting |

**Verdict**: Modes 1 + 3 were SUSPECTED, jointly fixed in commit `0019b91`; user acknowledgement of the fix is recorded by commit-message authorship (not a separate override). All other modes CLEAR.

No `--no-block` flag was invoked; this audit triggered a fix-and-re-verify cycle rather than a pipeline bypass.

---

## 5. CLAUDE.md §3 step 2a/2b automated audit

```
$ python3 -c "import re, pathlib; tex=pathlib.Path('NOETHER_paper.tex').read_text(); bib=pathlib.Path('NOETHER_paper.bib').read_text(); cited_groups=re.findall(r'\\\\cite[a-z]*(?:\\[[^\\]]*\\])?\\{([^}]+)\\}', tex); cited={k.strip() for chunk in cited_groups for k in chunk.split(',')}; defined=set(re.findall(r'@\\w+\\{([^,]+),', bib)); print(f'Cited: {len(cited)} Defined: {len(defined)} Uncited: {sorted(defined-cited)} Undefined: {sorted(cited-defined)}')"
Cited: 58 Defined: 58 Uncited: [] Undefined: []
```

PASS.

---

## 6. CLAUDE.md §1 sensitive info audit

```
$ grep -rIn -E "/Users/[^/]+|sk-[A-Za-z0-9]{16,}|Bearer\s+[A-Za-z0-9]+" supplementary/ docs/review_round_polish/ NOETHER_paper.tex
(no output)
```

PASS.

---

## 7. Next-stage handoff

The manuscript is now ready for **Stage 5 FINALIZE** with the following caveats from the Round 3 Editorial Decision:

- EIC-m1 length reduction (move C.6.1 / F to supplementary; target 50-55 pp.) — **deferred to user direction** before Stage 5 because moving appendix C.6.1 (Theorem 1' falsification per-block exhaustion proof) is structurally load-bearing
- EIC-m2 abstract tightening (~574 words → ≤350 words; empirical numbers → body) — **deferred to user direction** for the same reason (precision edit benefits from user oversight)

Both can be addressed pre-submission as part of camera-ready polish or executed before Stage 5 if the user prefers.

**MANDATORY CHECKPOINT (Stage 5 entry)**: format-conversion pipeline (MD → DOCX via Pandoc → LaTeX → tectonic PDF) requires explicit user confirmation before launch.

---

## 8. Quality trajectory

| Round | Manuscript verdict | Pages | Outstanding CRITICAL / fix-blocking |
|---|---|---|---|
| Round 1 | Major Revision | ~75 | 8 (DA + R2) |
| Round 2 | Minor Revision | 80 | 5 DA |
| Round 3 | Minor Revision | 82 | 0 DA CRITICAL unaddressed |
| **Round 5 audit** | **PASS** | **83** | **0 (Mode 1+3 caught and fixed during this audit)** |

Monotone-improving trajectory; each round closes substantive items without introducing new CRITICAL findings.
