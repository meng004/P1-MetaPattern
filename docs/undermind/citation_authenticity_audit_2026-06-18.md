# Citation Authenticity and Metadata Audit

Date: 2026-06-18

Scope: `NOETHER_paper.bib`, with special attention to references selected from the Undermind bibliography and references used to position MR identification, operator-block coverage, search-based MR generation, and related database/ML testing comparators.

Evidence sources:

- Local bibliography: `NOETHER_paper.bib`.
- Undermind bibliography: `/Users/limeng/Downloads/Undermind - Scholarly metamorphic testing methods characterizing MR identification modes and operatoralgebraic MR class derivation.bib`.
- Paper-search MCP:
  - CrossRef DOI lookup for publisher metadata.
  - CrossRef title search where DOI was missing.
  - Semantic Scholar search for arXiv-only records.

## Summary

No fabricated DOI-backed reference was found among the audited core references. Several entries were real but incomplete or slightly inaccurate. The main corrections were metadata normalization: missing volume/issue/pages, wrong or incomplete proceedings title, one author-name correction, and replacing arXiv-only records with formal publisher metadata where available.

BibTeX validation improved from 65 warnings before the audit to 38 warnings after correction. Remaining warnings are mostly style metadata gaps for old conference records, PMLR/NeurIPS-style entries, standards/books, and records for which CrossRef itself does not provide page numbers.

## Corrected Entries

| BibTeX key | Issue found | Evidence | Correction |
|---|---|---|---|
| `LiTOSEM2025` | Missing TOSEM volume/issue/pages | CrossRef DOI `10.1145/3708521` | Added volume 34, issue 5, pages 1--25 |
| `MRScout2024` | Missing TOSEM volume/issue/pages | CrossRef DOI `10.1145/3656340` | Added volume 33, issue 6, pages 1--28 |
| `GenMorph2024` | Missing TSE volume/issue/pages | CrossRef DOI `10.1109/TSE.2024.3407840` | Added volume 50, issue 7, pages 1888--1900 |
| `SunMETRICplus2021` | Missing final TSE volume/issue/pages | Undermind bibliography; CrossRef DOI resolves title/authors but reports early-access pages | Added volume 47, issue 9, pages 1764--1785 |
| `Yan2022InputPattern` | Author spelling mismatch; title capitalization mismatch | CrossRef DOI `10.1109/DSA56465.2022.00057` | Corrected `Zhongjiang Lu` to `Zhongjian Lu`; title matched CrossRef capitalization |
| `Lin2018HierarchicalMR` | Proceedings title too specific compared with CrossRef container | CrossRef DOI `10.1145/3194747.3194750`; Undermind confirms DOI/pages | Updated booktitle to CrossRef container title |
| `Zhang2014PolynomialMR` | First-author middle initial not present in CrossRef; proceedings title normalized | CrossRef DOI `10.1145/2642937.2642994` | Changed `Jie M. Zhang` to `Jie Zhang`; normalized booktitle |
| `AutoMT2025` | arXiv DOI missing | Semantic Scholar record for arXiv `2510.19438` | Added DOI `10.48550/arXiv.2510.19438` |
| `DeepXplore2017` | DOI/publisher/address missing | CrossRef title search | Added DOI `10.1145/3132747.3132785`, publisher/address |
| `Segura2022QBSAutoMR` | Pages/publisher/address missing; booktitle normalized | CrossRef DOI `10.1145/3524846.3527338` | Added pages 48--55, ACM publisher/address |
| `Wang2024QED` | PVLDB volume/issue/pages missing | CrossRef DOI `10.14778/3681954.3682024` | Added volume 17, issue 11, pages 3602--3614 |
| `Humbatova2021DeepCrime` | DOI/publisher/address missing | CrossRef title search | Added DOI `10.1145/3460319.3464825`, publisher/address |
| `Nolasco2024MemoRIA` | Entry type incorrect; missing PACMSE volume/issue/pages | CrossRef DOI `10.1145/3643747` | Changed from `@inproceedings` to `@article`; added journal, volume 1, issue FSE, pages 450--472 |
| `Deng2021VectorNeurons` | DOI/pages/publisher/address missing | CrossRef title search | Added DOI `10.1109/ICCV48922.2021.01198`, pages 12180--12189 |
| `Markl2022LearnedQO` | SIGMOD Record volume/issue/pages missing | CrossRef DOI `10.1145/3542700.3542702` | Added volume 51, issue 1, pages 5--5 |
| `Ba2024DQP` | DOI/volume/issue/pages missing; journal title included venue parenthetical | CrossRef title search | Added DOI `10.1145/3654991`, volume 2, issue 3, pages 1--26; normalized journal |
| `Zhong2025SQLancerPP` | arXiv-only record despite formal ACM publication; year changed | CrossRef title search | Changed to `@inproceedings`, year 2026, DOI `10.1145/3779212.3790215`, pages 1677--1692 |

## Verified Without Change

The following important entries were checked and found consistent enough for the current manuscript:

- `Barr2015OracleProblem`: CrossRef DOI `10.1109/TSE.2014.2372785`, TSE 41(5), 507--525.
- `Fu2024MTAdequacy`: CrossRef did not resolve the arXiv DOI, but Semantic Scholar resolved title/authors/date/DOI `10.48550/arXiv.2412.20692`.
- `Segura2019QBSMRPatterns`: CrossRef DOI `10.1109/MET.2019.00012`, title/authors/venue/year match.
- `Li2020TabularMR`: CrossRef DOI `10.1002/spe.2818`, SP&E 50(8), 1345--1380.
- `Su2015LikelyMR`: CrossRef DOI `10.1109/AST.2015.19`, title/authors/pages match.
- `Zhang2019AutoMR`: CrossRef DOI `10.1109/ICSME.2019.00035`, title/authors/pages match.
- `Blasi2021MeMo`: CrossRef DOI `10.1016/j.jss.2021.111041`, JSS 181:111041.
- `Clark2023CausalMT`: CrossRef DOI `10.1109/ICST57152.2023.00023`, title/authors/pages match.
- `GPTMR2025`: CrossRef DOI `10.1016/j.infsof.2025.107828`, IST 187:107828.
- `ChenMETRIC2016`: CrossRef DOI `10.1016/j.jss.2015.07.037`, JSS 116, 177--190.
- `Liu2014MTEffectiveness`: CrossRef DOI `10.1109/TSE.2013.46`, TSE 40(1), 4--22.
- `Segura2016`: CrossRef DOI `10.1109/TSE.2016.2532875`, TSE 42(9), 805--824.

## Remaining Caveats

- `Chen1998` is a classic HKUST technical report, not a CrossRef DOI-backed journal/conference record. Google Scholar found the title through later arXiv indexing, but this does not invalidate the tech-report citation.
- Several ML/proceedings references (`CohenWelling2016`, `FuchsTransformer2020`, `Gomez2017Reversible`, `Satorras2021EGNN`, etc.) are conference-proceedings records where DOI metadata is absent or not necessary for ACM style. They were not the main Undermind-derived MR-identification corpus.
- `Ying2025MRPatterns` has CrossRef volume/issue metadata but no page field in CrossRef; the remaining BibTeX warning is therefore not treated as an error.
- `Altamimi2022MRSLR` similarly resolves through CrossRef but lacks page information in the returned metadata.

## Verification

Commands run:

```sh
rtk bibtex NOETHER_paper_arxiv
rtk pdflatex -interaction=nonstopmode -halt-on-error NOETHER_paper_arxiv.tex
rtk pdflatex -interaction=nonstopmode -halt-on-error NOETHER_paper_arxiv.tex
rtk rg -n "undefined citations|Citation .* undefined|undefined references|LaTeX Error|BibTeX.*Error|There were undefined|Citation\\(s\\) may have changed" NOETHER_paper_arxiv.log NOETHER_paper_arxiv.blg
```

Result: no undefined citations, no undefined references, no LaTeX/BibTeX errors, and no remaining citation-change warning.
