# Human inter-rater κ study — turnkey package (P3 / ISSUE-012)

A ready-to-deploy kit for an **independent human** inter-rater reliability study
of the NOETHER MetaPattern / MR-family classification. It replaces the LLM panel
(whose three raters share pre-training, see `supplementary/S3_case_study/lrca_audit.md`)
with independent humans, removing that construct-validity caveat. Same 36 Set N
MRs, classified into the **ten MR families** (Layer 2, a–j) that roll up to the
**five MetaPatterns** (Layer 1); the human κ is reported at **both layers** and
compared to the LLM panel at the MetaPattern layer (the LLM block labels roll up
the same way; the LLM-majority-vs-author Cohen κ = 0.931 is the existing anchor).

> Honest boundary: a model cannot *be* a human rater. This package prepares
> everything; the actual labelling must be done by real people (see roles below).
> No labels here are fabricated as "human" data.

## Why this study

A careful TOSEM reviewer will flag two threats the paper currently carries:
1. the real-bug / Set N family labels were assigned by the **authors**
   (researcher bias);
2. the corroborating κ is from an **LLM panel with shared pre-training** (not
   independent raters).

A human κ at substantial-or-better agreement (κ ≥ 0.6, ideally ≥ 0.8) shows the
taxonomy is **objective and reproducible** by people given only the codebook,
which neutralises both threats. (It also validates that the MetaPattern / family
definitions and examples are clear enough to apply.)

## Files

| file | purpose |
|---|---|
| `CODEBOOK.md` | the rater-facing manual (plain-language, with examples) — give this to raters |
| `RATER_GUIDE.md` | rater usage guide (purpose → calibrate → rate independently) |
| `rating_sheet_TEMPLATE.xlsx` | **recommended** answer sheet: readable formulas + a `category` **dropdown** (a–j/orphan) |
| `rating_sheet_TEMPLATE.csv` | CSV fallback answer sheet (no Excel) |
| `items_to_rate.csv` | the 36 MRs in **readable** form (blind; no answer key) |
| `items_to_rate.pdf` | the 36 MRs as cleanly typeset LaTeX formulas |
| `items_raw.csv` | the original raw Java predicates (traceability) |
| `compute_kappa.py` | family + MetaPattern κ, 95% CI, per-category, disagreements, human-vs-author; reads `.xlsx` and `.csv` |
| `make_rater_materials.py` | regenerates all items/sheets/PDF + gold from source (reproducible) |
| `build_rater_packet.py` | bundles the rater-facing files into `noether_rater_packet.zip` |
| `_gold_author_labels.csv` | the author's labels — **HIDDEN KEY**, do NOT show raters before they finish |

## Raters: how many and who

- **Number:** ≥ 3 (enables Fleiss κ, matches the 3-model panel). 2 is the minimum
  (Cohen κ only).
- **Profile:** software engineers or applied mathematicians with **metamorphic-
  testing familiarity** and enough math background to read the input/output
  relations. **Not** authors of NOETHER; **no** prior involvement in its design.
- **Independence:** raters work **alone**, do not see each other's labels, do not
  see `_gold_author_labels.csv`, and do not discuss items during labelling.

## Procedure (turnkey, ~1–2 hours per rater)

1. **Recruit** ≥ 3 qualified independent raters.
2. **Brief:** give each rater the `noether_rater_packet.zip` (RATER_GUIDE +
   CODEBOOK + items + their own copy of `rating_sheet_TEMPLATE.xlsx`, the dropdown
   sheet; CSV fallback included). Never share `_gold_author_labels.csv`.
3. **Calibrate (not scored):** raters first do the 11 worked examples in
   CODEBOOK §5 and reconcile understanding (these are NOT the 36 test items).
4. **Label independently:** each rater fills the `category` column for all 36
   items, saving as `ratings/rater_<name>.csv`. No discussion.
5. **Compute:** coordinator drops the filled sheets into `ratings/` and runs
   `python3 compute_kappa.py`.
6. **Report:** Fleiss κ + 95% CI, pairwise Cohen κ, % agreement, the
   disagreement list, and (optional) human-majority-vs-author κ next to the
   LLM 0.931. Analyse every disagreement (codebook ambiguity vs genuine
   borderline) and, if a category is systematically confused, sharpen its
   CODEBOOK entry.

## Run

```bash
cd experiment_realbug/human_kappa
# (raters have placed rater_*.csv in ./ratings/)
python3 compute_kappa.py

# sanity-check the pipeline on fabricated data (clearly labelled SYNTHETIC):
python3 compute_kappa.py --selftest
```

## Categories (one MR family per item)

Raters assign one **MR family** (Layer 2) or `orphan`; each family rolls up to one
of the **five MetaPatterns** (Layer 1):

| MetaPattern (Layer 1) | MR families (Layer 2) |
|---|---|
| `G` symmetry | `a` equivariance, `b` conservation |
| `T_star` self-adjoint | `c` self-adjoint, `d` adjoint-duality |
| `T_rev` time-reversal | `e` time-reversal |
| `O_le` order | `f` static-order, `g` dynamic-shape |
| `L_star` limit | `h` convergence, `i` accuracy-order, `j` representation-invariance |

`orphan` catches anything outside the taxonomy. The script reports κ at the family
layer (11 categories) and at the rolled-up MetaPattern layer (6 categories).

## Pass criterion (per ISSUE-012)

A pilot Fleiss/Cohen κ ≥ 0.7 corroborates that the taxonomy is reproducible under
independent human application; report the exact value with its 95% CI and band
(Landis–Koch) regardless of outcome. This study is the human anchor that the
paper currently commits as future work (`lrca_audit.md` caveat; CLAUDE.md §5 P3).
