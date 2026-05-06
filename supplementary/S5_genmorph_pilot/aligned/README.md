# Aligned S5 — Controlled MR-Source Comparison via Upstream Pipeline

This directory implements the **gold-standard** experimental design for
comparing NOETHER's algebraically-derived MRs (Set N) against GenMorph's
GP-evolved MRs (Set G), with **all confounders held constant** except
the MR source itself.

The earlier `java_bridge/` pilot uses a parallel JUnit pipeline. That
design left 5 confounders uncontrolled (PIT version, test inputs,
evaluator, mutator scope, mutant byte-code). The aligned design here
uses upstream's exact toolchain so the only varying variable is the
MR set membership.

## Design summary

```
Substrate (held constant for both Set N and Set G):
  - JVM:           JDK 11 toolchain, Java 8 bytecode (matches upstream)
  - SUT:           /tmp/genmorph_pilot/genmorph_full/genmorph/configs/math-sut/
                   src/main/java/MathClass.java (verbatim from upstream)
  - Test inputs:   Randoop seed=0 + EvoSuite seed=0 (matches upstream config)
  - State capture: upstream's instrumentation (ch.usi.gassert.*)
  - Mutants:       PIT 1.7 via pitest-wrapper-1.7.4.jar (upstream's mutant set)
  - Evaluator:     ch.usi.gassert.EvaluateMRs (Java main class)
  - MR DSL:        .jir.txt (input relation) + .jor.txt (output relation),
                   Java expression syntax with i_<arg>_{s,f}, o_return_{s,f},
                   i_this_s.PI, i_this_s.E placeholders

Variable (the single dimension we compare):
  - MR set membership: { Set N (ours) } vs { Set G (upstream) }
```

## Set N MRs — three encoding paths for single-execution invariants

NOETHER's algebra produces both (a) two-execution metamorphic relations
(natural in (jir, jor) DSL) and (b) single-execution invariants like
`gcd ≤ min(|p|, |q|)` and `|sin(x)| ≤ 1`. The (jir, jor) DSL is built
around two-execution relations, so single-execution invariants need an
encoding bridge. **They are NOT inexpressible — they need a different
encoding path**.

### Three encoding paths

| Path | Form                  | Encoding cost        | Evaluator runtime |
|------|-----------------------|----------------------|-------------------|
| A    | JUnit `assertTrue`    | 1 line of Java       | PIT + JUnit       |
| B    | Degenerate jir (id)   | jir = identity, jor uses only `_s` vars | GAssert (if accepted) |
| C    | Perturb + conjunct    | jir perturbs, jor conjoins source-side and followup-side invariant | GAssert |

**Path A** is what `java_bridge/MathClassMRTest.java` uses (fully
executable, kills mutants like any other test). **Path B** packages
the same invariant into upstream's DSL by setting jir = identity (so
followup execution = source execution) and writing the invariant in the
jor using only `_s` variables — depends on whether GAssert's parser
allows this. **Path C** is the safest fallback: jir perturbs the
followup, and jor conjoins the same invariant on both source-side and
followup-side variables.

### gcd Set N (set_n_mrs/MathClass?gcd?0/)

| MR file                          | Property                                | Encoding |
|----------------------------------|-----------------------------------------|----------|
| `@rho_perm.{jir,jor}.txt`        | gcd(p, q) = gcd(q, p)                   | (jir, jor) two-execution |
| `@rho_scale.{jir,jor}.txt`       | gcd(2p, 2q) = 2·gcd(p, q)               | (jir, jor) two-execution |
| `@rho_eqref.{jir,jor}.txt`       | gcd(p, q + p) = gcd(p, q)               | (jir, jor) two-execution |
| `@rho_mono.{jir,jor}.txt`        | gcd ≤ min(|p|, |q|)  (single-exec inv)  | **Path B** (jir = identity) |

### sin Set N (set_n_mrs/MathClass?sin?0/)

| MR file                          | Property                                | Encoding |
|----------------------------------|-----------------------------------------|----------|
| `@rho_oddsym.{jir,jor}.txt`      | sin(-x) = -sin(x)                       | (jir, jor) two-execution |
| `@rho_period.{jir,jor}.txt`      | sin(x + 2π) = sin(x)                    | (jir, jor) two-execution |
| `@rho_complement.{jir,jor}.txt`  | sin(π − x) = sin(x)                     | (jir, jor) two-execution |
| `@rho_bound.{jir,jor}.txt`       | |sin(x)| ≤ 1   (single-exec inv)        | **Path B** (jir = identity) |

### Path B fallback to Path C

If GAssert's parser rejects Path B (because jor uses only `_s`
variables and the parser requires both `_s` and `_f` to appear), the
fallback is Path C:

```
# rho_mono Path C jir
((Math.abs(((double) i_p_f) - (((double) i_p_s) + 1.0)) < 1.0E-4) && (Math.abs(((double) i_q_f) - ((double) i_q_s)) < 1.0E-4))

# rho_mono Path C jor
((<source-side invariant>) && (<followup-side invariant>))
```

Both paths are executable; only Path B is more elegant.

If even Path C fails (parser rejects `Math.min` etc.), single-execution
invariants stay in `java_bridge/MathClassMRTest.java` (Path A) and the
aligned experiment reports them in a "framework-extension" footnote
rather than as part of the aligned MR comparison.

The methodological finding either way: **NOETHER's algebra produces
MRs across multiple expressibility tiers; GenMorph's GP-evolved MRs
naturally live only in the (jir, jor) two-execution tier**. This is a
representational difference between the two MR sources, independent of
their kill-rate performance.

## Pipeline (codex execution)

```bash
# 0. Prereqs
export JAVA_HOME=/opt/homebrew/opt/openjdk@11
export PATH="$JAVA_HOME/bin:$PATH"
GENMORPH=/tmp/genmorph_pilot/genmorph_full/genmorph
ALIGNED=<REPO>/supplementary/S5_genmorph_pilot/aligned

# 1. Reproduce upstream's pipeline state for chosen (subject, seed)
#    This generates states/, classifications/, mutants/ directories
#    that EvaluateMRs needs as input.
cd $GENMORPH
python3 scripts/run/randoop.py --config configs/evaluation-config-math.json --seed 11 --subject 'MathClass?gcd?0'
python3 scripts/run/pitest.py --config configs/evaluation-config-math.json --seed 11 --subject 'MathClass?gcd?0'
# (Repeat for sin)

# 2. Augment upstream's MR directory with our Set N files
SEED=11
SUBJECT='MathClass?gcd?0'
UPSTREAM_MRS_DIR="$GENMORPH/output_dir_math/assertions_seed${SEED}/${SUBJECT}"
cp $ALIGNED/set_n_mrs/${SUBJECT}/*.txt "$UPSTREAM_MRS_DIR/"
ls "$UPSTREAM_MRS_DIR/"
# Should now show MR0..MR3 (Set G) plus rho_perm/rho_scale/rho_eqref (Set N)

# 3. Invoke EvaluateMRs with combined MR set
java -cp "$GENMORPH/build/libs/GAssert-1.0-SNAPSHOT-all.jar" \
     ch.usi.gassert.EvaluateMRs \
     "$UPSTREAM_MRS_DIR" \
     "$GENMORPH/output_dir_math/states_seed${SEED}/source/${SUBJECT}" \
     "$GENMORPH/output_dir_math/states_seed${SEED}/followup/${SUBJECT}" \
     "$GENMORPH/output_dir_math/states_seed${SEED}/source_classification/${SUBJECT}" \
     "$GENMORPH/output_dir_math/states_seed${SEED}/followup_classification/${SUBJECT}" \
     "MathClass" \
     "$ALIGNED/results/seed${SEED}/${SUBJECT}/"

# 4. Parse augmented mutants_killed.csv
python3 $ALIGNED/parse_aligned_results.py \
    --csv "$ALIGNED/results/seed${SEED}/${SUBJECT}/mutants_killed.csv" \
    --output "$ALIGNED/results/seed${SEED}/${SUBJECT}/aligned_metrics.json"
```

The output `aligned_metrics.json` contains:
- Per-MR per-mutant binary kill matrix (no parallel pipeline; same
  evaluator on the same state capture)
- Per-set aggregate kill rates (Set N vs Set G under identical conditions)
- M1-M5 efficiency metrics (re-derived in aligned conditions)

## Why this beats the parallel pipeline (java_bridge/)

| Property                          | Parallel (java_bridge/)         | Aligned (this dir)              |
|-----------------------------------|---------------------------------|----------------------------------|
| Set G MR semantics                | hand-transcribed to JUnit Java  | upstream's `.jor.txt` verbatim   |
| jor evaluator                     | JUnit `assertTrue`              | `ch.usi.gassert.EvaluateMRs`     |
| PIT version                       | 1.15                            | 1.7 (upstream's wrapper)         |
| Test inputs                       | seeded random + boundary        | Randoop seed=0 (upstream)        |
| Mutant set                        | PIT 1.15 default                | identical to upstream's published mutants_killed.csv |
| Per-mutant attribution            | not directly comparable to upstream | exact match per mutant index |
| Confounders in Set N vs Set G     | 5 confounders held constant     | 0 confounders                    |
| Replicates upstream's published numbers | only by coincidence       | exactly (Set G column = published)|
| Set N MR count                    | 4 (incl.\ ρ_mono / ρ_bound)     | 3 (single-execution invariants excluded by framework) |

## Codex execution checklist

Two stages:

### Stage 1: Pipeline reproduction (one-time, expensive)

- [ ] Verify `/tmp/genmorph_pilot/genmorph_full/genmorph/scripts/` is intact
- [ ] Run `python3 scripts/run/randoop.py` for chosen subject(s) + seed 11
- [ ] Run `python3 scripts/run/pitest.py` for the same subjects + seed
- [ ] Verify `output_dir_math/states_seed11/...` directories are populated
- [ ] Verify `output_dir_math/mutants_seed11/...` is populated
- [ ] Cross-check: re-derive upstream's published `mutants_killed.csv` by
  running EvaluateMRs ONLY on their MR0-MR3, then diff against
  `evaluation/pitest_seed11/MathClass?gcd?0/mutants_killed.csv`. Should
  match exactly. **This is the alignment validation step**: if not exact,
  pipeline reproduction is broken and aligned numbers are not trustworthy.

### Stage 2: Set N injection + joint evaluation (cheap, repeatable)

- [ ] Copy `aligned/set_n_mrs/<SUBJECT>/*.txt` into the per-subject
  upstream MR directory
- [ ] Re-run EvaluateMRs (now picks up 4 Set G + 3 Set N MR files = 7 MRs total)
- [ ] Parse the new `mutants_killed.csv` — should have 7 MR rows
- [ ] Run `parse_aligned_results.py` to extract per-set kill rates +
  M1-M5 metrics

After Stage 2 completes for one (subject, seed), we have:

- One row per MR (3 Set N + 4 Set G = 7 rows) × 25 mutant columns =
  binary kill matrix
- Direct per-mutant attribution: which Set N MR caught mutant M_k? which
  Set G MR? overlap?
- Pooled across multiple subjects/seeds: cross-subject EMR distribution,
  workhorse identity, MCD per-MR

## Methodological note — the (jir, jor) framework's expressiveness limit

NOETHER's 8-block decomposition produces MRs in two qualitative classes:

1. **Two-execution relations**: source-followup metamorphic relations.
   Examples: ρ_perm (G), ρ_scale (G), ρ_eqref (O_le), ρ_oddsym (G),
   ρ_period (G), ρ_complement (G). All expressible in the (jir, jor)
   DSL → included in aligned Set N.

2. **Single-execution invariants**: properties of a single execution.
   Examples: ρ_mono (gcd ≤ min(|p|, |q|)), ρ_bound (|sin(x)| ≤ 1),
   ρ_idem (sort(sort(a)) = sort(a) only requires one execution if
   re-applying is treated as identity). Some of these are partially
   expressible by setting jir = identity (i_p_f = i_p_s, i_q_f = i_q_s)
   and putting the invariant in jor — but for relations like
   `gcd ≤ min(|p|, |q|)` that don't relate two outputs, the framework
   cannot encode them naturally.

This mismatch is itself a finding: GP-evolved MR frameworks like
GenMorph implicitly restrict the MR space to two-execution relations.
NOETHER's algebraic derivation produces a strictly larger space, of
which the (jir, jor)-expressible subset is what we compare in aligned
mode. The single-execution invariants are evaluated separately in the
parallel pipeline (`java_bridge/`) and tracked as a "framework-extension"
contribution of NOETHER.

## Files in this directory

```
aligned/
├── README.md                              (this file)
├── set_n_mrs/
│   ├── MathClass?gcd?0/
│   │   ├── @rho_perm.{jir,jor}.txt
│   │   ├── @rho_scale.{jir,jor}.txt
│   │   └── @rho_eqref.{jir,jor}.txt
│   └── MathClass?sin?0/
│       ├── @rho_oddsym.{jir,jor}.txt
│       ├── @rho_period.{jir,jor}.txt
│       └── @rho_complement.{jir,jor}.txt
├── run_aligned_pipeline.sh                (codex orchestrator skeleton)
├── parse_aligned_results.py               (post-EvaluateMRs analysis)
└── results/                               (gitignored output)
    └── seed{N}/<SUBJECT>/
        ├── mutants_killed.csv            (augmented with Set N rows)
        ├── mrs_status.csv                 (FP rates per MR)
        └── aligned_metrics.json           (M1-M5 in aligned conditions)
```
