# NOETHER Dataset / Supplementary Material Manifest

This document describes every dataset and supplementary artefact referenced by the NOETHER manuscript, with provenance, version lineage, and a reverse lookup from manuscript sections to data files.

## Provenance summary

| Artefact | Location | Origin | License |
|---|---|---|---|
| 84-MR PWR corpus | `supplementary/S2_pwr_corpus/` | Authors' own inductive catalogue, distilled from standard PWR-physics literature (Bell & Glasstone 1970; Lewis & Miller 1993; Stamm'ler & Abbate 1983) | CC-BY-4.0 |
| 12-MR elementwise enumeration | `supplementary/S2_pwr_corpus/elementwise_12.md` | Sub-selection of 84-MR corpus, structurally representative | CC-BY-4.0 |
| 18-MR engineering catalogue (audit subset) | `supplementary/S2_pwr_corpus/18mr_audit/` | Authors' independently distilled audit set (orthogonal to 84-MR corpus) for κ measurement | CC-BY-4.0 |
| SE(3)-equivariant case study harness | `supplementary/S3_case_study/` | Authors' own implementation (`e3nn` library + custom mutation set) | MIT (code) + CC-BY-4.0 (data) |
| EGNN model checkpoint | `supplementary/S3_case_study/checkpoints/` | Trained on procedural 5-class point-cloud dataset (sphere / cube / torus / cone / helix); 5189 params | MIT |
| GenMorph pilot data | `supplementary/S5_genmorph_pilot/` | GAssert 30-min budget runs on 8 D4J SUTs | replication of (Cornejo et al. 2024) |
| Defects4J algebra-rich subset | `supplementary/S7_d4j_algebra_rich/` | Subset of Defects4J 2.0.0 (Just et al. 2014) with explicit physical-law content | inherits D4J license |
| Apache Commons Math pilot | within `supplementary/S4_reproducibility/future_work.md` | Authors' cross-codebase pilot, 3 SUTs × 5 Set N MRs × 77 PIT mutants | Apache 2.0 (Commons Math), MIT (analysis) |
| Sun 2021 METRIC+ subjects | `supplementary/S8_metricplus_sun2021_subjects/` | Re-implementation of (Sun et al. 2021) 4 subjects (SPhone/SBaggage/SExpense/SMeal) in Java + PIT 1.7.4 + Major | replication; original Python in (Sun et al. 2021) |
| Path A head-to-head results | `supplementary/S8_metricplus_sun2021_subjects/results_path_a*.md` | Authors' three-tier replication (Python n=219 / Java+PIT n=120 / Major n=555) | CC-BY-4.0 |
| Cost-component methodology | `supplementary/S4_reproducibility/cost_breakdown.md` | Authors' four-axis cost methodology | CC-BY-4.0 |
| PMCM Case A-bis decoding | `supplementary/S9_migrated_appendices/pmcm_case_abis_full.md` | Authors' decoding of Murphy et al. 2008 6-class taxonomy onto NOETHER blocks | CC-BY-4.0 |

## Version lineage

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-05-17 | Initial release: IMRaD-restructured paper (71 pp) + 9 supplementary directories (S1-S9) + 12-MR migration + cost methodology migration + Case A-bis decoding |

## Manuscript → data reverse lookup

| Manuscript section | Data file |
|---|---|
| §3.5.1 Boltzmann instantiation (tab:refinement, tab:elementwise) | `supplementary/S2_pwr_corpus/` + `supplementary/S2_pwr_corpus/elementwise_12.md` |
| §3.5.2 equivariant ML instantiation | `supplementary/S1_construct_mp/equivariant_instance.py` |
| §3.5.3 RDB / query optimiser instantiation | `supplementary/S6_query_optimiser/` |
| §3.6 Theorem 1' falsification (tab:five-obstructions) | Appendix C.6 in body |
| §4.3 SE(3) case study (tab:case-study) | `supplementary/S3_case_study/` |
| §4.3 DeepCrime pilot (tab:pilot, tab:deepcrime-contingency) | `supplementary/S3_case_study/deepcrime_pilot/` |
| §4.4 L*-blindness 5/6 (tab:l-blindness, tab:pit-block) | `supplementary/S7_d4j_algebra_rich/d4j/` |
| §4.5 Head-to-head GenMorph (tab:algebra-rich-pooled, tab:per-block-headtohead, tab:two-stratum, tab:gen-cost) | `supplementary/S5_genmorph_pilot/` + `supplementary/S4_reproducibility/cost_breakdown.md` |
| §4.6 METRIC+ Path A (tab:metricplus-sorting, tab:metricplus-headtohead-small, tab:metricplus-sun2021-scope) | `supplementary/S8_metricplus_sun2021_subjects/` |
| §4.7 Witnesses (tab:rediscovery) | `supplementary/S5_genmorph_pilot/midpoint_witnesses/` |
| Appendix C Proofs (tab:translate) | `supplementary/S1_construct_mp/construct_mp.py` (Translate per-block implementations) |

## Data integrity

The supplementary archive's SHA-256 content hash will be anchored in the camera-ready paper and `CITATION.cff` upon acceptance. The hash is computed over a sorted-file tar archive: `find supplementary -type f | sort | tar -czf - -T - | sha256sum`.

## Replication ladder

| Tier | Time | Scope |
|---|---|---|
| **Smoke** | ≤ 5 min | `cd supplementary/S1_construct_mp && python -m pytest -q test_construct_mp.py` |
| **Cache replay** | ≤ 30 min | Re-run SE(3) case study scorer against cached EGNN checkpoint + cached mutation outputs |
| **Full re-run** | ≈ 1-2 hours | Re-train EGNN + re-run mutation set + recompute all p-values (excludes GenMorph 30-min budget per SUT) |

Full replication of the GenMorph head-to-head (8 SUTs × 30 min) requires ≈ 4 hours wall on a parallel-4 machine; see `supplementary/S5_genmorph_pilot/REPLICATION.md` for the GAssert harness setup.

## Licensing summary

- **Code** (`supplementary/S{1,3,8}/*.py`, `scripts/*.py`): MIT (see `LICENSE`)
- **Data** (`supplementary/S{2,5,7}/`): CC-BY-4.0
- **Paper text and figures** (`NOETHER_paper.tex`, `figs/`): CC-BY-4.0

Third-party data inherits its upstream license: D4J (per `third_party/d4j/LICENSE`), Apache Commons Math (Apache 2.0), e3nn (MIT), and Sun 2021 subjects (replication of (Sun et al. 2021); original method copyright authors).
