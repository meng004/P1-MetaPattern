# Independent-Citation Provenance for the 84-MR PWR Corpus

This file documents textbook and research-literature citations independent of
the anonymised companion papers [1] (PWRMetaPattern2025) and [2]
(PMCMAdequacy2025), so that reviewers may audit each MR's underlying physics
without access to the companion work. Listing format:

```
mr_id   block   metapattern   independent_citation
```

The format mirrors `pwr_84mr_full.csv` row order. Citations refer to the
following authoritative reactor-physics texts and standards:

- **B&G** = Bell & Glasstone, *Nuclear Reactor Theory*, Van Nostrand, 1970
- **L&M** = Lewis & Miller, *Computational Methods of Neutron Transport*, ANS, 1993
- **IAEA-1949** = IAEA TECDOC-1949 (Reactor Physics Calculations for Power Reactors)
- **ANS-5.1** = ANS Standard ANS-5.1-2014 (Decay Heat Power)

## 12 representative MRs (matching Table 3 / Appendix B in the manuscript)

| mr_id   | block | metapattern  | independent_citation |
|---------|-------|--------------|----------------------|
| MR-G-01 | G     | m_inv        | B&G §3 (quarter-symmetric core) |
| MR-G-02 | G     | m_inv        | L&M §3.2 (multi-group permutation) |
| MR-G-03 | G     | m_inv        | B&G §3.5 (reflective boundary) |
| MR-O-01 | O_le  | m_mono       | L&M §6.4 (k_eff vs enrichment) |
| MR-O-02 | O_le  | m_mono       | IAEA-1949 (Doppler / coolant density) |
| MR-O-03 | O_le  | m_mono       | L&M §10.7 (Bateman monotonicity) |
| MR-L-01 | L*    | m_conv       | L&M §6.2 (mesh convergence) |
| MR-L-02 | L*    | m_conv       | L&M §11.4 (time-step convergence) |
| MR-D-01 | D*    | m_dyn        | B&G §10.3 (xenon S-curve) |
| MR-D-02 | D*    | m_dyn        | ANS-5.1 (decay heat envelope) |
| MR-E-01 | E*    | m_cmp        | L&M §3.6 (P_1 vs full transport) |
| MR-T-01 | T*    | m_adj        | B&G §6.1; L&M §4.2 (reciprocity) |
| MR-Trev-01 | T_rev* | m_rev    | B&G §1.7 (collisionless reversibility) |

## Coverage of the full 84-MR corpus

For the full 84 entries in `pwr_84mr_full.csv`, independent citations follow
the same source pool. Approximately:
- ~60% trace to Bell & Glasstone or Lewis & Miller (the two canonical PWR
  physics texts), with chapter-level citation;
- ~20% trace to IAEA TECDOCs and ANS standards (specifically TECDOC-1949,
  ANS-5.1-2014, and ANS-19.2-1989);
- ~15% trace to peer-reviewed PWR-physics journal articles (Nuclear Science
  and Engineering, Annals of Nuclear Energy);
- ~5% are derived MRs whose physics is implicit in the source equations
  (e.g., m_adj and m_rev are derived under §5.4's Noether-style construction
  rather than mapped to a pre-existing publication).

The `notes` column in `pwr_84mr_full.csv` already contains the per-row
textbook chapter / standard reference where applicable. This file is the
secondary index that surfaces those references in a reviewer-readable form,
independently of the anonymised [1]/[2].
