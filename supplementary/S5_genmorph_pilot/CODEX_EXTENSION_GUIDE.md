# Codex Extension Guide: Adding Subjects to S5

This document tells codex (or any future implementer) how to add a new
subject to the S5 multi-subject pilot. Two subjects are already wired up
(`gcd`, `sin`). Adding a third (e.g.\ `pow`, `abbreviate`, `isSorted`,
`acos`) is a 5-step mechanical procedure.

## When to add a subject

Per the user's experimental-expansion goal, the priority order is:

| Priority | Subject       | Mutants | DSL helper deps   | Rationale                           |
|----------|---------------|---------|-------------------|-------------------------------------|
| 1        | abbreviate    | 39      | Sequence (string) | Largest sample boost; tests Lang    |
| 2        | log10         | 15      | none              | Numeric scalar, similar to sin/gcd  |
| 3        | acos          | 76      | none              | Highest mutant count                |
| 4        | sort          | 8       | Sequence (int[])  | Cross-domain (Guava)                |
| 5        | isSorted      | 11      | Sequence (int[])  | Boolean output, cross-domain        |
| 6        | pow           | 10      | none              | Exponential algebra; small N        |

The 5-step recipe below is identical for all subjects; the per-subject
cost is mainly **deriving Set N** (algebraic MRs from the SUT) and
**transcribing Set G** (the .jor.txt expressions to Java).

## Five-step recipe

### Step 1 — Inspect the GenMorph DSL files

```bash
SUBJECT="MathClass?log10?0"   # change per subject
ls "/tmp/genmorph_pilot/mrs/mrs/assertions_seed11/$SUBJECT/"
# Expect: SUBJECT@MR<n>.jir.txt + SUBJECT@MR<n>.jor.txt for each evolved MR
```

Note the MR labels (gcd uses `MR0..MR3`, pow uses `MR4..MR7`, sin uses
`MR20..MR23`, sort/isSorted/abbreviate use `NumericAddition`,
`SequenceFlip`, etc.). Just enumerate them as `MR<n>` in the test class
in arrival order.

Read the published kill rates so you know what to expect:

```bash
cat "/tmp/genmorph_pilot/evaluation/evaluation/pitest_seed11/$SUBJECT/mrs_status.csv"
grep "^assertions_seed11," "/tmp/genmorph_pilot/evaluation/evaluation/pitest_seed11/$SUBJECT/mutants_killed.csv"
```

### Step 2 — Derive Set N (algebraic MRs)

For each subject, write 3-5 algebraic MRs by inspecting the SUT's
operator algebra. Examples:

| Subject     | Set N suggestions                                                                   |
|-------------|-------------------------------------------------------------------------------------|
| log10       | `log10(1)=0`; `log10(x*y)=log10(x)+log10(y)`; `log10(10^k)=k`; mono                  |
| acos        | `acos(-x)=π-acos(x)`; `acos(1)=0`; `acos(0)=π/2`; mono on [-1,1]                    |
| pow         | `pow(k,0)=1`; `pow(1,e)=1`; `pow(-k,2e)=pow(k,2e)`; mono in e for k>1                |
| sort        | `sort(perm(a))=sort(a)`; `sort(sort(a))=sort(a)`; output mono; first==min            |
| isSorted    | `isSorted(sort(a))=true`; `isSorted(reverse(reverse(a)))=isSorted(a)`; singleton trivially sorted |
| abbreviate  | length bound; preserves first n chars; `abbreviate(s, len(s)+k)=s` for k≥0           |

Each MR follows the pattern:

```java
@Test
@DisplayName("Set N: ρ_<name> — <plain-English property>")
void testRho<Name>() {
    for (<input> x : SOURCE_INPUTS) {
        // Derive follow-up
        // Call SUT
        // Assert relation
    }
}
```

Tolerance choice:
- For exact algebraic identities (gcd commutativity, isSorted boolean):
  use `assertEquals` exactly.
- For floating-point identities (sin period, log10 product): use `1e-9`
  to `1e-12` tolerance.
- For inequalities (output bounds): allow tiny ULP slack
  (`1.0E-12`).

### Step 3 — Transcribe Set G (literal jor)

Mechanical translation rules from GenMorph DSL to Java:

| DSL token                         | Java substitution             |
|-----------------------------------|-------------------------------|
| `(double) i_<arg>_s`              | `(double) <arg>_s`            |
| `(double) i_<arg>_f`              | `(double) <arg>_f`            |
| `(double) o_return_s`             | `(double) o_s`                |
| `(double) o_return_f`             | `(double) o_f`                |
| `(double) i_this_s.PI`            | `Math.PI`                     |
| `(double) i_this_s.E`             | `Math.E`                      |
| `Math.abs(...)`                   | `Math.abs(...)` (verbatim)    |
| `(cond) ? 1.0 : (n / d)`          | `safeDiv(n, d)` helper        |
| `ch.usi.gassert.data.types.Sequence.fromValue(...)` | Add GAssert.jar dep, keep verbatim |

For sequence-typed subjects (sort, isSorted, abbreviate), add to
`build.gradle`:

```gradle
dependencies {
    testImplementation files('/tmp/genmorph_pilot/genmorph_full/genmorph/build/libs/GAssert-1.0-SNAPSHOT-all.jar')
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
    testImplementation 'org.junit.platform:junit-platform-launcher:1.10.0'
}
```

Failure-counter pattern (from MathClassMRTest.java):

```java
int failures = 0;
for (...) {
    if (!jorMR<n>(...)) failures++;
}
// Threshold = ceil(published_FP_pct / 100 * K_INPUTS), with +1 cushion.
assertTrue(failures <= <threshold>,
    "MR<n> violated " + failures + " / " + considered);
```

### Step 4 — Wire the subject into Gradle

Edit `java_bridge/build.gradle`:

```gradle
def subjectMethod = [
    gcd : 'gcd',
    sin : 'sin',
    log10 : 'log10',          // new
] [selectedSubject]

def subjectTestClass = [
    gcd : 'MathClassMRTest',
    sin : 'MathClassSinMRTest',
    log10 : 'MathClassLog10MRTest',   // new
] [selectedSubject]

def subjectKeepMethods = [
    gcd : ['gcd'],
    sin : ['sin'],
    log10 : ['log10'],         // new — match GenMorph's mutator scope
] [selectedSubject]
```

And edit `java_bridge/build.gradle` `test {}` block to add a new
filter clause:

```gradle
} else if (selected == 'log10') {
    filter { includeTestsMatching 'MathClassLog10MRTest' }
}
```

### Step 5 — Wire the subject into the parser + metrics

Edit `parse_pit_xml.py` `SUBJECT_REGISTRY`:

```python
SUBJECT_REGISTRY = {
    "gcd": {...},
    "sin": {...},
    "log10": {
        "set_n": {"testRhoOne", "testRhoProduct", "testRhoPow10", "testRhoMono"},
        "set_g": {"testGenMorphMR<n0>", "testGenMorphMR<n1>", ...},
        "set_b": {"testRhoOne"},
    },
}
```

Edit `efficiency_metrics.py` `MR_SETS`:

```python
MR_SETS = {
    "gcd": {...},
    "sin": {...},
    "log10": {
        "set_n": {"testRhoOne", ...},
        "set_g": {"testGenMorphMR<n0>", ...},
    },
}
```

### Pipeline (per subject)

```bash
# Baseline (must pass — no FP on original SUT)
JAVA_HOME=/opt/homebrew/opt/openjdk@11 ./gradlew test -Psubject=<subj>

# Mutation testing
./gradlew pitest -Psubject=<subj> --rerun-tasks

# Parse + stats + cross-validate
cd ..
python3 parse_pit_xml.py --pit-report-dir java_bridge/build_outputs/pit_report/<subj> \
    --subject <subj> --output results/<subj>/results.csv
python3 stats.py --results results/<subj>/results.csv \
    --output results/<subj>/pilot_stats.json
python3 cross_validate.py --our-stats results/<subj>/pilot_stats.json \
    --our-results results/<subj>/results.csv \
    --genmorph-csv "/tmp/genmorph_pilot/evaluation/evaluation/pitest_seed11/<SUBJECT_DIR>/mutants_killed.csv" \
    --subject-label "<SUBJECT_DIR>" \
    --output results/<subj>/cross_validation.json

# Aggregate efficiency metrics across all subjects so far
python3 efficiency_metrics.py \
    --results results/gcd/results.csv results/sin/results.csv results/<subj>/results.csv \
    --subjects gcd sin <subj> \
    --output results/efficiency_metrics.json
```

## Common gotchas

1. **MR labels start at non-zero**: pow uses `MR4..MR7`, sin uses
   `MR20..MR23`. The label is just a record of evolution-order;
   transcribe each `.jor.txt` verbatim and use `testGenMorphMR<n>`
   matching the file's `<n>`.

2. **GenMorph DSL has dead sub-expressions**: e.g.\ `(x_f - x_f)` in
   sin's MR20 always evaluates to 0. Keep them verbatim — the evolved
   expression is what we're transcribing, regardless of its
   simplifiability.

3. **MR with FP > 0 in seed11**: if `mrs_status.csv` reports
   `FP > 0/100` (e.g.\ MR1 in gcd's seed11 reports `1/28`), the literal
   transcription will fail on baseline with similar rate. Use either
   a `failures <= threshold` pattern OR `@Disabled` if MS is also `0/0`
   (vacuous on this seed).

4. **Sequence-helper subjects need the GAssert jar**: sort, isSorted,
   abbreviate, and others use `ch.usi.gassert.data.types.Sequence`.
   Add the GAssert jar as a `testImplementation files(...)` dependency.

5. **Default PIT mutator scope is too broad**: PIT 1.15 mutates ALL
   methods in `targetClasses`. Restrict via `excludedMethods` so PIT
   only mutates the subject method's body. See the existing
   `MATHCLASS_METHODS` list and `subjectKeepMethods` map.

6. **Boundary inputs matter**: domain-aware boundary values (0, ±π/2,
   MAX_VALUE) should be hardcoded in `@BeforeAll`; random fill
   afterwards. Per-subject boundary list is part of the methodology
   (documented in each test class).

## Verification

After Step 5:

- `./gradlew test -Psubject=<subj>` should PASS (baseline FP=0)
- `./gradlew pitest -Psubject=<subj>` should produce a mutations.xml
  whose KILLED mutations are attributed to your test methods
- `efficiency_metrics.json` should now contain a third subject entry
- The `pareto_points` array should have 6 points (3 subjects × 2 MR
  sets) for plotting

## Once you have ≥3 subjects

Per-subject results.csv files enable:

- **Pooled cross-subject statistics** (Wilson CI, McNemar, Fisher)
  with N ≈ 60-100 mutants
- **Pareto frontier plot** in (kill_rate, generation_cost) space
- **Per-subject EMR distribution** (does the "1 effective MR per set"
  pattern generalise?)
- **Workhorse identification across subjects** (which Set N MR is the
  most reliably-discriminating across SUTs?)

These feed §6.6 of the main paper as a multi-axis methodological
narrative rather than a single kill-rate comparison.
