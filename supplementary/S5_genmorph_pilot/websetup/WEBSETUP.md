# Claude Code Remote (Web) — Websetup spec for S5 Aligned Pilot

This document is the **single-source environment specification** for
running the S5 aligned-pipeline experiment on Claude Code Remote (Ubuntu
container). Paste the relevant section into `/websetup`, or use
`bootstrap.sh` + `verify_env.sh` + `run_all.sh` as direct setup +
verification + execution.

## What this experiment does

Compares NOETHER's algebraically-derived MRs (Set N) against GenMorph's
GP-evolved MRs (Set G) on `MathClass.gcd` and `MathClass.sin`, with all
confounders (mutants, test inputs, evaluator, JVM, SUT) held constant
under upstream GenMorph's exact pipeline. Only varying variable: MR
source.

**Prerequisite knowledge for /websetup**:

- This is a Java + Python pipeline running on Ubuntu.
- Local macOS run failed because: (a) JDK 8 not available natively, (b)
  Maven not installed, (c) upstream tested only on Linux.
- Claude Code Remote provides Ubuntu 22.04 → suitable substrate.

## Target environment

| Component                      | Version                     | Source                        |
|--------------------------------|----------------------------|-------------------------------|
| OS                             | Ubuntu 22.04 LTS           | Claude Code Remote default    |
| Java (upstream pipeline)       | OpenJDK 8                  | `apt install openjdk-8-jdk`   |
| Java (our Gradle / JUnit)      | OpenJDK 11                 | `apt install openjdk-11-jdk`  |
| Maven                          | 3.6+                       | `apt install maven`           |
| Python                         | 3.10+                      | OS default                    |
| Python deps                    | pandas, numpy, scipy, statsmodels | `pip install -r requirements.txt` |
| Randoop                        | 4.3.0 jar                  | bundled in genmorph.zip       |
| EvoSuite                       | 1.1.0 jar                  | bundled in genmorph.zip       |
| PITest wrapper                 | 1.7.4 jar                  | bundled in genmorph.zip       |
| GAssert evaluator              | 1.0-SNAPSHOT jar           | bundled in genmorph.zip       |
| Major (mutation testing tool)  | 2.0.0 — **not required**   | only for `gen` mode, we use `eval` |

## /websetup paste-in (high-level)

If the `/websetup` interface accepts a single setup script, paste:

```bash
# Install OS deps
sudo apt-get update && sudo apt-get install -y \
    openjdk-8-jdk openjdk-11-jdk maven python3-pip wget unzip

# Set Java env
export JAVA8=/usr/lib/jvm/java-8-openjdk-amd64
export JAVA11=/usr/lib/jvm/java-11-openjdk-amd64
export JAVA_HOME=$JAVA11
export PATH=$JAVA_HOME/bin:$PATH

# Clone or sync the project (assumes the supplementary/ tree is at /workspace/MR元模式/)
cd /workspace/MR元模式/supplementary/S5_genmorph_pilot/websetup

# Download GenMorph Zenodo package (one-time, ~80 MB total)
bash bootstrap.sh

# Verify everything
bash verify_env.sh

# Run aligned experiment for gcd + sin
bash run_all.sh
```

If `/websetup` is a multi-step interactive interface, follow the
sequence in **Sections 2–5** below.

## Section 2 — OS dependency installation

```bash
sudo apt-get update
sudo apt-get install -y \
    openjdk-8-jdk \
    openjdk-11-jdk \
    maven \
    python3-pip \
    wget unzip git curl

# Verify
java -version           # should show JDK 11 (default)
/usr/lib/jvm/java-8-openjdk-amd64/bin/java -version  # should show JDK 8
mvn -version
python3 --version
```

## Section 3 — GenMorph Zenodo package download

The replication package is at <https://zenodo.org/records/10067096>.
Three zip files: evaluation.zip (357 KB), mrs.zip (1 MB), genmorph.zip
(81 MB).

```bash
mkdir -p /tmp/genmorph_pilot
cd /tmp/genmorph_pilot

# Direct download URLs (Zenodo standard format):
ZENODO=https://zenodo.org/records/10067096/files
wget --no-check-certificate -nc "$ZENODO/evaluation.zip"
wget --no-check-certificate -nc "$ZENODO/mrs.zip"
wget --no-check-certificate -nc "$ZENODO/genmorph.zip"

# Unzip into separate directories
unzip -o -q evaluation.zip -d evaluation_unzip
unzip -o -q mrs.zip -d mrs_unzip
unzip -o -q genmorph.zip -d genmorph_unzip

# Adjust to the expected layout (evaluation/, mrs/, genmorph_full/)
mv evaluation_unzip ./evaluation
mv mrs_unzip ./mrs
mv genmorph_unzip ./genmorph_full

# Verify expected directory layout
ls evaluation/evaluation/pitest_seed11/  | head -3   # expects subject directories
ls mrs/mrs/assertions_seed11/            | head -3   # expects same subject directories
ls genmorph_full/genmorph/build/libs/    # expects GAssert-1.0-SNAPSHOT-all.jar
```

**Expected layout after unzip**:

```
/tmp/genmorph_pilot/
├── evaluation/evaluation/pitest_seed{N}/<SUBJECT>/{mrs_status.csv, mutants_killed.csv}
├── mrs/mrs/assertions_seed{N}/<SUBJECT>/<SUBJECT>@MR{n}.{jir,jor}.txt
└── genmorph_full/genmorph/
    ├── build/libs/GAssert-1.0-SNAPSHOT-all.jar
    ├── pitest-wrapper-1.7.4.jar
    ├── randoop-all-4.3.0.jar
    ├── evosuite-1.1.0.jar
    ├── configs/{math,guava,lang}-sut/src/main/java/<SUT>.java
    └── scripts/run/genmorph.py        # upstream pipeline orchestrator
```

## Section 4 — Python dependencies

```bash
cd /workspace/MR元模式/supplementary/S5_genmorph_pilot
pip3 install -r requirements.txt
# requirements.txt: pandas, numpy, scipy, statsmodels
```

## Section 5 — Environment variables

The upstream `scripts/config.py` reads these from environment:

```bash
# Java paths
export JAVA8=/usr/lib/jvm/java-8-openjdk-amd64
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Tool jar locations (point to bundled jars)
export GENMORPH=/tmp/genmorph_pilot/genmorph_full/genmorph
export EVOSUITE_HOME=$GENMORPH
export EVOSUITE_JAR=evosuite-1.1.0.jar
export RANDOOP_HOME=$GENMORPH
export RANDOOP_JAR=randoop-all-4.3.0.jar
export PITEST_HOME=$GENMORPH
export PITEST_JAR=pitest-wrapper-1.7.4.jar
# MAJOR_HOME is required only for `gen` mode (which we don't use); skip
```

Place these in `~/.bashrc` or a `.env` file sourced by `run_all.sh`.

## Section 6 — Run aligned experiment

Once env is up:

```bash
cd /workspace/MR元模式/supplementary/S5_genmorph_pilot/websetup
bash run_all.sh
```

`run_all.sh` will:

1. Inject Set N MRs (`@rho_*.{jir,jor}.txt` files) into upstream's
   `mrs/assertions_seed11/` directory — alongside their MR0..MR3 / MR20..MR23.
2. Reproduce upstream's pipeline state for the chosen subject:
   ```
   cd $GENMORPH
   python3 scripts/run/genmorph.py eval configs/config-all-evaluation-math.json
   ```
   This executes Randoop + PIT 1.7 + state capture + EvaluateMRs in one
   pass per upstream's design.
3. Parse the augmented `mutants_killed.csv` from upstream's output.
4. Compute aligned M1-M5 metrics.
5. Write results to `aligned/results/seed11/<subject>/`.

## Section 7 — Expected outputs

After successful run:

```
aligned/results/seed11/MathClass?gcd?0/
├── mutants_killed.csv          # 8 MR rows (4 Set G + 4 Set N) × 25 mutant cols
├── mrs_status.csv              # FP rates for each MR
└── aligned_metrics.json        # M1-M5 in aligned conditions

aligned/results/seed11/MathClass?sin?0/
├── mutants_killed.csv          # 8 MR rows × 26 mutant cols
├── mrs_status.csv
└── aligned_metrics.json

aligned/results/efficiency_metrics_aligned.json   # cross-subject
```

## Section 8 — Acceptance criteria

The websetup + execution is "successful" if all of the following hold:

- [ ] `verify_env.sh` reports zero failures
- [ ] Upstream's pipeline reproduces the published Set G kill rate for at
      least one subject within 1 mutant of upstream's `mutants_killed.csv`
      (validates the pipeline reproduction)
- [ ] Our injected Set N MRs appear as additional rows in the augmented
      `mutants_killed.csv` (validates DSL injection)
- [ ] `aligned_metrics.json` contains finite per-MR + per-set values
- [ ] FP rates from `mrs_status.csv` show our Set N MRs at FP ≤ 5/100
      on the unmutated SUT (validates Set N DSL correctness)

## Section 9 — Fallback if Stage 2 (upstream pipeline reproduction) fails

If `python3 scripts/run/genmorph.py eval ...` fails on Ubuntu (likely
causes: Maven repo network issues, Major missing for some pipeline
branch, EvoSuite Java compatibility), then **fall back to "static"
mode**:

1. Use upstream's already-published `mutants_killed.csv` as Set G's row
2. Skip Stage 1; we cannot inject Set N into upstream's evaluator
3. Report aligned experiment as "blocked at Stage 1; parallel pipeline
   data (`java_bridge/`) is the deliverable for §6.6"
4. Document the blocker explicitly so future runs on a setup-validated
   environment can complete

`run_all.sh` includes the `--fallback` flag for this case.

## Section 10 — File inventory in this websetup/ directory

```
websetup/
├── WEBSETUP.md           # this document
├── bootstrap.sh          # automated apt + Zenodo download + env setup
├── verify_env.sh         # sanity-check all deps + paths
├── run_all.sh            # main aligned-pipeline driver
├── inject_set_n.sh       # Stage 1 helper (cp Set N DSL files)
└── README.md             # quick-start
```
