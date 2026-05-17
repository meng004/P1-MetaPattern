# NOETHER — arXiv Submission Metadata

Ready-to-paste fields for the arXiv submission form (https://arxiv.org/submit).

## 1. Title

```
NOETHER: A Constructive Framework for Metamorphic Pattern Discovery from Operator Algebras
```

Length: 91 chars. arXiv limit: 240 chars. ✓

## 2. Authors

```
Meng Li (1,2,3), Xiaohua Yang (1,2,3), Jie Liu (1,2,3), Shiyu Yan (1,2,3)
```

Three shared affiliations (numbered for arXiv):
1. School of Computing, University of South China, Hengyang, 421001, China
2. Hunan Engineering Research Center of Software Evaluation and Testing for Intellectual Equipment, Hengyang, 421001, China
3. CNNC Key Laboratory on High Trusted Computing, Hengyang, 421001, China

Corresponding author: Meng Li (mlemon@usc.edu.cn)

## 3. Abstract (condensed for arXiv, ≤ 1920 chars)

**Char count: 1898 (within limit, structured Context/Objective/Method/Results/Conclusion preserved)**

```
Context. Metamorphic Testing is recognised in IEEE/ISO software-testing standards and increasingly recommended for AI systems, but its progress is bottlenecked by metamorphic relation (MR) identification: existing approaches (structured frameworks, mining and evolutionary pipelines, LLM-assisted methods, MetaPattern catalogues) share an inductive grounding that leaves three foundational questions open: origin, closure, and transferability.

Objective. We propose a framework whose downstream step from program-induced operator algebra to MetaPattern set is mechanical and provable, while the upstream curation of the algebra is a stated empirical hypothesis with explicit scope precondition.

Method. NOETHER is a two-layer framework. The upstream layer is an eight-block decomposition over recurrent mathematical structures (symmetry, order, self-adjoint, time-reversal, limit, qualitative-dynamics, method-comparison, relational equivalence). The downstream CONSTRUCT-MP algorithm produces a MetaPattern set with algebraic-closure (Theorem 1) and polynomial-time decidability (Theorem 2) guarantees. We test the framework on three operator-algebraic domains.

Results. On Boltzmann reactor physics NOETHER systematises a prior inductive catalogue; on equivariant ML it derives executable MRs for rotation invariance, adjoint duality, and training-trajectory reversibility; on relational query optimisers it exercises the relational-equivalence block. The central falsifiable prediction (L*-blindness on homogeneity-preserving mutators) holds on the in-scope substrate. The absolute-completeness conjecture (Theorem 1') is falsified on PWR core diffusion via two pairwise-independent counterexamples that identify five Translate-extension dimensions.

Conclusion. Induction is relocated from per-program MR sampling to a per-domain algebraic layer; the downstream step is deductive and mechanical.
```

## 4. Comments

```
71 pages, 18 tables, 1 figure. Under review at ACM Transactions on Software Engineering and Methodology. Supplementary materials (algorithm reference implementation, 84-MR PWR corpus, SE(3) case study harness, three-tier METRIC+ replication) at https://github.com/meng004/P1-MetaPattern (replace placeholder with real URL once published).
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
./build_arxiv.sh                                  # produces NOETHER_paper_arxiv.pdf + .bbl
tar czf noether_arxiv_v1.tar.gz \
    NOETHER_paper_arxiv.tex \
    NOETHER_paper.bib \
    NOETHER_paper_arxiv.bbl \
    ../texmf-dist/                                # custom sty files (e.g. hyperxmp)
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
| 6 | Upload `noether_arxiv_v1.tar.gz` from §8 | **User** |
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

- [x] Abstract ≤ 1920 chars (1898) ✓
- [x] Title ≤ 240 chars (91) ✓
- [x] Author block named (Meng Li, USC, mlemon@usc.edu.cn) ✓
- [x] Source compiles clean (`./build_arxiv.sh` exits 0) ✓
- [x] 0 em-dash, 0 undef refs, 0 undef cites ✓
- [x] Bibliography `.bbl` included in source tarball ✓
- [x] `\acmConference` placeholder set to "Manuscript under review for ACM TOSEM" ✓
- [ ] Sensitive-info scan (`grep -lE "sk-|/Users/"`) → 0 hits ⚠ user verification needed
- [ ] User endorsement obtained for `cs.SE` first-time submission ⚠ user action
