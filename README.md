# S5 Aligned Experiment — NOETHER Set N vs GenMorph Set G

This repository implements the **single-variable** comparative experiment for
the NOETHER paper's §6.6 protocol: Set N (NOETHER algebra-derived MRs) versus
Set G (GenMorph GP-evolved MRs) on the **full 23-subject GenMorph benchmark**,
holding every other variable fixed to GenMorph upstream's exact toolchain.

## 1. Single-variable design

| Substrate | Held constant for both Set N and Set G |
|---|---|
| JVM | OpenJDK 8 (matches GenMorph upstream's runtime) |
| SUTs | GenMorph's 23 published Java methods (Math 10 + Lang 5 + Guava 8) |
| Test inputs | Randoop seed=11 + EvoSuite seed=11 (upstream's published config) |
| State capture | upstream's `ch.usi.gassert` instrumentation |
| Mutants | PIT 1.7.4 via `pitest-wrapper-1.7.4.jar` (upstream's mutant set) |
| Evaluator | `ch.usi.gassert.EvaluateMRs` (Java main class) |
| MR DSL | `.jir.txt` + `.jor.txt` GAssert format with `i_<arg>_{s,f}` and `o_return_{s,f}` |

| Variable | The single dimension we compare |
|---|---|
| MR set | Set N (NOETHER, 71 MRs across 23 subjects) vs Set G (GenMorph upstream) |

## 2. Repository layout

```
S5_aligned_experiment/
├── .env                           # local env vars (gitignored on cloud)
├── .env.example                   # template
├── .gitignore
├── setup.sh                       # one-shot Ubuntu setup (idempotent)
├── README.md                      # this file
├── set_n_mrs/                     # 71 NOETHER-derived MRs as (jir, jor) pairs
│   ├── MathClass?gcd?0/
│   │   ├── MathClass?gcd?0@rho_perm.jir.txt
│   │   ├── MathClass?gcd?0@rho_perm.jor.txt
│   │   ├── MathClass?gcd?0@rho_scale.jir.txt
│   │   └── ... (4 MRs total)
│   ├── MathClass?sin?0/   (4 MRs)
│   ├── MathClass?acos?0/  (3 MRs)
│   └── ... (23 subjects)
├── scripts/
│   ├── generate_set_n_mrs.py     # source of truth: derives all Set N MRs
│   ├── run_all.sh                # main orchestrator (Stage 1 + Stage 2)
│   ├── parse_results.py          # per-subject metric extraction
│   └── aggregate_metrics.py      # cross-subject pooled stats
└── results/                       # gitignored output
    ├── seed11/<subject>/{aligned_metrics.json, mutants_killed.csv, mrs_status.csv}
    └── aligned_summary.json       # cross-subject summary
```

## 3. Set N MR inventory (NOETHER 8-block decomposition)

| # | Subject | MRs | Algebra blocks |
|---|---|---|---|
| 1 | MathClass?gcd?0 | 4 | G (perm, scale), O_le (eqref, mono) |
| 2 | MathClass?sin?0 | 4 | G (oddsym, period, complement), O_le (bound) |
| 3 | MathClass?acos?0 | 3 | G (oddcomp), O_le (bound_lo, bound_hi) |
| 4 | MathClass?log10?0 | 3 | G (pow10), L* (unit), O_le (pos) |
| 5 | MathClass?millerRabinPrimeTest?0 | 3 | L* (boundary fixed points: 2, 0, 1) |
| 6 | MathClass?nextPrime?0 | 3 | O_le (lower_bound, min_two), G (succ) |
| 7 | MathClass?pow?0 | 4 | G (succ), L* (zero_exp, unit_base, one_exp) |
| 8 | MathClass?sinh?0 | 3 | G (oddsym), L* (zero), O_le (sign) |
| 9 | MathClass?stirlingS2?0 | 4 | L* (diag, one_k, zero_k), O_le (nonneg) |
| 10 | MathClass?tan?0 | 3 | G (oddsym, period_pi), L* (zero) |
| 11 | LangClass?abbreviate?0 | 2 | L* (idem_short), O_le (length_bound) |
| 12 | LangClass?capitalize?0 | 3 | L* (length, empty), G (idem_call) |
| 13 | LangClass?center?0 | 3 | L* (idem_short, size_zero), O_le (length_lower) |
| 14 | LangClass?difference?0 | 3 | L* (self, empty_left), G (swap) |
| 15 | LangClass?isSorted?0 | 3 | L* (singleton, empty), G (idem_call) |
| 16 | GuavaClass?indexOf?0 | 3 | L* (empty_target, self), O_le (lower_bound) |
| 17 | GuavaClass?join?0 | 3 | L* (empty_array), O_le (length_lower), G (separator_idem) |
| 18 | GuavaClass?meanOf?0 | 3 | G (flip), L* (singleton), O_le (le_max) |
| 19 | GuavaClass?min?0 | 3 | G (flip), L* (singleton), O_le (le_mean) |
| 20 | GuavaClass?padStart?0 | 2 | L* (idem_long), O_le (length) |
| 21 | GuavaClass?repeat?0 | 4 | L* (zero, one, length), G (succ) |
| 22 | GuavaClass?sort?0 | 3 | G (flip, sum_preserved), L* (length_preserved) |
| 23 | GuavaClass?truncate?0 | 2 | L* (idem_short), O_le (length_bound) |
| **Total** | **23 subjects** | **71 MRs** | |

Block-coverage breakdown (per the NOETHER 8-block decomposition):

| Block | MR count | % of Set N | Subjects covered |
|---|---|---|---|
| G (symmetry/permutation) | 21 | 30% | gcd, sin, acos, log10, sinh, tan, pow, nextPrime, capitalize, difference, isSorted, sort, meanOf, min, repeat, join |
| O_le (order/bound) | 19 | 27% | gcd, sin, acos, log10, sinh, stirlingS2, nextPrime, abbreviate, center, indexOf, join, meanOf, min, padStart, truncate |
| L* (limit/closure / fixed points) | 31 | 44% | log10, millerRabin, pow, sinh, stirlingS2, tan, abbreviate, capitalize, center, difference, isSorted, indexOf, join, meanOf, min, padStart, repeat, sort, truncate |
| T*, T*_2, D*, E*, I* | 0 | 0% | (these blocks are empty for the GenMorph subject domain) |

The empty blocks (T*, T*_2, D*, E*, I*) are themselves a finding: the GenMorph
benchmark consists of stateless utility methods, so blocks tied to dynamics,
inverses, time-reversal, and method-equivalence are vacuous here. NOETHER
predicts this — those blocks become non-empty in domains with explicit physical
or temporal structure (e.g., the Boltzmann reactor instantiation in §4 of the
paper).

## 4. How to run on a fresh Ubuntu cloud host

```bash
# 1. Sync the repo to the cloud
git clone <local-or-remote> S5_aligned_experiment
cd S5_aligned_experiment

# 2. One-shot environment setup
bash setup.sh
# Installs: openjdk-8, openjdk-11, maven, python3 + pandas/numpy/scipy/statsmodels
# Downloads: GenMorph Zenodo replication package (~80 MB) into /tmp/genmorph_pilot/
# Builds: GAssert fat-jar from upstream sources

# 3. Run the experiment
bash scripts/run_all.sh                  # full pipeline (Stage 1 + Stage 2)
# OR:
bash scripts/run_all.sh --reproduce      # just Randoop + PIT (slow, ~4-7 h)
bash scripts/run_all.sh --evaluate       # just inject Set N + evaluate (~30 min)
bash scripts/run_all.sh --subject 'MathClass?gcd?0'   # single subject

# 4. Inspect results
cat results/aligned_summary.json
ls results/seed11/MathClass?gcd?0/
```

## 5. Two-stage pipeline rationale

**Stage 1 — Reproduce upstream's pipeline state (`--reproduce`):**

Runs `randoop.py` and `pitest.py` from GenMorph upstream for each of the 23
subjects with seed 11. Generates the test inputs, instrumentation traces, and
the PIT 1.7.4 mutant set under exactly the conditions GenMorph published.

This stage is expensive (~4-7 h total on a typical cloud node) but only needs
to run once per fresh environment. Successful reproduction is *also the
alignment validation step*: re-running EvaluateMRs on Set G alone should
reproduce upstream's published `mutants_killed.csv` exactly. If it doesn't,
pipeline reproduction is broken and the experiment is not trustworthy.

**Stage 2 — Inject Set N + re-evaluate (`--evaluate`):**

Copies `set_n_mrs/<subject>/*.{jir,jor}.txt` into upstream's per-subject MR
directory, then re-runs `EvaluateMRs` so the augmented MR set (Set G ∪ Set N)
is scored on the same mutants. Cheap (~30 min total), repeatable as Set N
evolves through review iterations.

## 6. Output schema

`results/seed11/<subject>/aligned_metrics.json`:

```json
{
  "subject": "MathClass?gcd?0",
  "n_mutants": 25,
  "n_total_mrs": 8,
  "set_n": {"n_mrs": 4, "kill_vector": [1,0,1,...], "n_killed": 5},
  "set_g": {"n_mrs": 4, "kill_vector": [0,0,1,...], "n_killed": 17},
  "per_mr":  [{"mr": "rho_perm", "set": "N", "fp": 0.0, "n_killed": 3, "killed_indices": [...]}, ...],
  "m_metrics": {"M1_kill_rate_N": 0.20, "M1_kill_rate_G": 0.68, ...}
}
```

`results/aligned_summary.json`:

```json
{
  "n_subjects": 23,
  "total_mutants": 557,
  "set_n": {"kills": ..., "kill_rate": 0.xx, "wilson_95_ci": [..., ...]},
  "set_g": {"kills": ..., "kill_rate": 0.xx, "wilson_95_ci": [..., ...]},
  "paired_mcnemar": {"n_only_kills": ..., "g_only_kills": ..., "p_value_two_sided": ...},
  "per_subject": [...],
  "m_metrics_means": {...}
}
```

## 7. Encoding paths for Set N MRs

NOETHER's algebra produces both two-execution metamorphic relations and
single-execution invariants (e.g. `gcd ≤ min(|p|, |q|)`, `|sin(x)| ≤ 1`). The
GenMorph (jir, jor) DSL is built around two-execution relations, so single-
execution invariants need an encoding bridge:

| Path | Form | Used in this experiment |
|---|---|---|
| Path A | JUnit `assertTrue` (parallel pipeline) | not used — broken alignment |
| Path B | Degenerate jir = identity, jor uses only `_s` vars | preferred for single-execution invariants |
| Path C | Perturb + conjunct (jor uses both `_s` and `_f`) | fallback if GAssert rejects Path B |

If GAssert rejects a Path B MR (jor uses only `_s` vars), the script
`generate_set_n_mrs.py` can be rerun with the MR rewritten in Path C form.

## 8. Methodological note — block emptiness as a finding

The NOETHER framework's 8-block decomposition predicts the block structure of
the operator algebra `A_P`. For the GenMorph benchmark — stateless utility
methods on numbers, strings, and arrays — only three blocks (G, O_le, L*) are
non-empty. The other five (T*, T*_2, D*, E*, I*) are empty because:

* there is no inner-product self-adjointness (T*),
* no time-reversal involution (T*_2),
* no qualitative-dynamics trajectory (D*),
* no inverse closure relation (I*),
* and method-equivalence (E*) requires alternative implementations of the same
  function, which the GenMorph benchmark does not provide.

This is itself a structural prediction that the framework makes about the
domain. Domains with richer algebra (Boltzmann reactor in §4, equivariant ML in
§5, query optimisers in §6 of the paper) populate more blocks.

## 9. Data provenance

* GenMorph upstream source: `https://zenodo.org/records/10067096`
  (Ayerdi, Terragni, Jahangirova, Arrieta, Tonella, GenMorph 2024)
* Set N MRs: derived in this repository's `scripts/generate_set_n_mrs.py` from
  the eight-block decomposition described in NOETHER §3-§4.
* Reproduction seed: `11` (GenMorph published evaluation seed).

## 10. Citation

If you use this experimental design, please cite the NOETHER paper and the
GenMorph paper:

```bibtex
@article{Ayerdi2023GenMorph,
  author  = {Ayerdi, Jon and Terragni, Valerio and Arrieta, Aitor and Tonella, Paolo and others},
  title   = {{GenMorph}: Automatically Generating Metamorphic Relations via Genetic Programming},
  year    = {2024}
}
```
