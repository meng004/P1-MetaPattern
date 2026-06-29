# NOETHER — arXiv v2 Submission Metadata

Ready-to-paste fields for the arXiv submission form (https://arxiv.org/submit).

## 1. Title

```
NOETHER: Constructive Metamorphic Pattern Identification from Operator Algebras and a Falsifiable Invariance-Blindness Theorem
```

Length: 126 chars. arXiv limit: 240 chars. ✓

## 2. Authors

```
Meng Li (1,2,3), Jie Liu (1,2,3), Shiyu Yan (1,2,3), Xiaohua Yang (1,2,3)
```

Three shared affiliations (numbered for arXiv):
1. School of Computing, University of South China, Hengyang, 421001, China
2. Hunan Engineering Research Center of Software Evaluation and Testing for Intellectual Equipment, Hengyang, 421001, China
3. CNNC Key Laboratory on High Trusted Computing, Hengyang, 421001, China

Corresponding author: Meng Li (mlemon@usc.edu.cn)

## 3. Abstract (latest manuscript abstract for arXiv, ≤ 1920 chars)

**Char count: 1575 (within limit)**

```
Metamorphic Testing relies on metamorphic relations (MRs), yet MR identification remains experience- or search-driven. We study MR identification for operator-algebraic program families, not fault-detection superiority. We introduce NOETHER, a two-level framework for equation-governed or relational-semantics families whose behaviour admits an operator algebra. The upstream layer curates the family algebra and structural components: symmetry, order, self-adjointness, time reversal, limits, qualitative dynamics, method comparison, and relational equivalence. The downstream CONSTRUCT-MP procedure derives five MetaPatterns and ten MR families and checks whether program interfaces can instantiate executable MRs. The construction is closed under its derivation operator, giving a well-formedness guarantee over the algebra-induced MR space. For the G and T* MetaPatterns, an Invariance-Blindness Theorem characterises detectable and undetectable implementation faults within the stated fault class. Evaluation covers canonical coverage, origin/boundary explanation, cross-domain and real-fault recurrence, and executability/blind-spot checks. Across expert/search-derived MR corpora, three algebra instantiations, 21 in-scope real faults, and a 20-mutant equivariant-ML study, NOETHER maps real faults to 8 of 10 MR families, detects 7/20 mutants versus 2/20 for a large-language-model (LLM)-prompted set and 0/20 for a literature set, and identifies five obstructions bounding the current Translate signature. The evidence characterises NOETHER as auditable and bounded.
```

## 4. Comments

```
60 pages, 15 tables, 6 figures. Under review at ACM Transactions on Software Engineering and Methodology. Supplementary materials (algorithm reference implementation, 84-MR PWR corpus, SE(3) case study harness, three-tier METRIC+ replication) at https://github.com/meng004/P1-MetaPattern.
```

## 5. Categories

| Type | arXiv code | Reason |
|---|---|---|
| **Primary** | `cs.SE` | Software Engineering (metamorphic testing, MR identification) |
| Cross-list | `cs.LG` | Equivariant ML instantiation (SE(3) point-cloud classifier case study) |
| Cross-list | `cs.LO` | Theorem 1' falsification + algebraic closure proofs |

## 6. License

`CC BY 4.0` (recommended for preprints; compatible with subsequent ACM submission)

## 7. MSC / ACM CCS Classification

| System | Code | Topic |
|---|---|---|
| ACM CCS 2012 | `D.2.5` | Testing and Debugging |
| ACM CCS 2012 | `D.2.4` | Software/Program Verification |
| MSC 2020 (optional) | `68N30` | Mathematical aspects of software engineering |

## 8. Source tarball

Build with:

```bash
cd arxiv/
pdflatex -interaction=nonstopmode NOETHER_paper_arxiv.tex
bibtex NOETHER_paper_arxiv
pdflatex -interaction=nonstopmode NOETHER_paper_arxiv.tex
pdflatex -interaction=nonstopmode NOETHER_paper_arxiv.tex
tar czf noether_arxiv_v2.tar.gz \
    NOETHER_paper_arxiv.tex \
    NOETHER_paper.bib \
    NOETHER_paper_arxiv.bbl \
    acmart.cls \
    ACM-Reference-Format.bst \
    hyperxmp.sty \
    figures/ \
    theory/
```

arXiv expects: one main `.tex` file + `.bbl` (so bibtex is not re-run) + all custom `.sty` files. Figures should be relative-pathed and bundled.

## 9. arXiv submission workflow

| Step | Action | Who |
|---|---|---|
| 1 | Create arXiv account at https://arxiv.org/user/register (if first-time) | **User** |
| 2 | Obtain `cs.SE` endorsement (4+ established `cs.SE` authors must endorse; ask a co-author with prior arXiv submissions) | **User** |
| 3 | Submit at https://arxiv.org/submit → "New Submission" | **User** |
| 4 | Paste title, authors, abstract from §1-§3 above | **User** |
| 5 | Choose categories per §5 above | **User** |
| 6 | Upload `noether_arxiv_v2.tar.gz` from §8 | **User** |
| 7 | Preview generated PDF; verify renders match local build | **User** |
| 8 | Submit; arXiv assigns ID (e.g. `arXiv:2605.NNNNN`) within 24h moderation | **User** |
| 9 | Once live: anchor arXiv ID in `CITATION.cff` + `pyproject.toml` + `README.md` + `NOETHER_paper.tex` artefact statement; commit + re-build PDF | **Assistant (after user provides ID)** |

## 10. Post-publication anchoring

After arXiv ID is assigned:

```bash
# Replace placeholders (Assistant will do this once user provides ID)
sed -i.bak "s/<ARXIV_ID>/2605.NNNNN/g" CITATION.cff pyproject.toml README.md
# Re-build PDF with anchored ID
cd arxiv/ && ./build_arxiv.sh
```

## 11. Compliance verification

- [x] Abstract ≤ 1920 chars (1575) ✓
- [x] Title ≤ 240 chars (126) ✓
- [x] Author block named (Meng Li, USC, mlemon@usc.edu.cn) ✓
- [x] Source compiles clean (`./build_arxiv.sh` exits 0) ✓
- [x] 0 em-dash, 0 undef refs, 0 undef cites ✓
- [x] Bibliography `.bbl` included in source tarball ✓
- [x] `\acmConference` placeholder set to "Manuscript under review for ACM TOSEM" ✓
- [ ] Sensitive-info scan for API keys and absolute local paths → 0 hits
- [ ] User endorsement obtained for `cs.SE` first-time submission ⚠ user action
