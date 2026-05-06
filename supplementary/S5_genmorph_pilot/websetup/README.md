# Quick-start — Claude Code Remote (Web) for S5 Aligned Pilot

## Three commands, in order

```bash
cd <repo>/supplementary/S5_genmorph_pilot/websetup
bash bootstrap.sh        # one-time, ~10 min: apt + Zenodo download + env vars
bash verify_env.sh       # ~5 sec: confirms all deps + paths green
bash run_all.sh          # 15-30 min: the actual aligned experiment
```

All three are **idempotent**: re-running them is safe and skips
already-completed work.

## Or — single paste-into-/websetup snippet

If `/websetup` accepts a one-line bootstrap command:

```bash
cd <repo>/supplementary/S5_genmorph_pilot/websetup && bash bootstrap.sh && bash verify_env.sh && bash run_all.sh
```

## Files

| File              | Role                                                      |
|-------------------|-----------------------------------------------------------|
| `WEBSETUP.md`     | Full spec — paste sections into `/websetup` if interactive |
| `bootstrap.sh`    | apt + Zenodo download + env-vars + Python deps             |
| `verify_env.sh`   | Sanity checklist — runs ~5s, prints PASS/FAIL/WARN counts  |
| `run_all.sh`      | Stage 1 (inject) + Stage 2 (upstream eval) + Stage 3 (parse) + Stage 4 (aggregate) |
| `README.md`       | This file                                                  |

## Outputs

After `run_all.sh` completes successfully:

```
<repo>/supplementary/S5_genmorph_pilot/aligned/
├── results/seed11/
│   ├── MathClass?gcd?0/
│   │   ├── mutants_killed.csv          # 8 MR rows (4 SetG + 4 SetN) × 25 mutant cols
│   │   ├── mrs_status.csv               # FP rates per MR
│   │   └── aligned_metrics.json         # M1-M5 metrics in aligned conditions
│   └── MathClass?sin?0/
│       └── (same layout, 26 mutant cols)
└── results/efficiency_metrics_aligned.json   # cross-subject aggregate
```

## Comparison vs the existing parallel pipeline

| Property                   | parallel (java_bridge/)        | aligned (this run)              |
|----------------------------|--------------------------------|---------------------------------|
| Set G MR semantics         | hand-transcribed JUnit         | upstream's `.jor.txt` verbatim  |
| jor evaluator              | JUnit `assertTrue`             | `ch.usi.gassert.EvaluateMRs`    |
| PIT version                | 1.15                           | 1.7 (upstream's wrapper)        |
| Test inputs                | seeded random + boundary       | Randoop + EvoSuite (upstream)   |
| Mutant set                 | PIT 1.15 default               | matches upstream's published 25 |
| Set N MR count             | 4 (incl single-execution)      | 4 (incl Path B encodings)       |
| Confounders for SetN vsSetG| pipeline-equal                 | substrate-equal                 |

Both pipelines run on the same SUT and same MR algebra; the aligned
pipeline removes pipeline differences as a confounder against the
published baseline.

## Troubleshooting

### `bootstrap.sh` Step 2 (Zenodo download) fails

Network firewall may block Zenodo. Try:
```bash
curl -L -o /tmp/genmorph_pilot/evaluation.zip https://zenodo.org/records/10067096/files/evaluation.zip
# repeat for mrs.zip and genmorph.zip
```

### `run_all.sh` Stage 2 fails (upstream pipeline)

Likely causes (check `aligned/results/upstream_eval.log`):

- **Maven repo blocked**: pre-populate `~/.m2/repository` from a working
  machine, or use a local mirror.
- **Major missing**: upstream's `eval` mode should not need Major (only
  `gen` mode does). If errors mention `MAJOR_HOME`, edit
  `genmorph_full/genmorph/scripts/config.py` to make MAJOR_HOME optional.
- **JDK path**: edit `scripts/config.py` line ~30 to set `JAVA8` to your
  actual JDK 8 path (`bootstrap.sh` exports `$JAVA8` but `config.py`
  may hard-code `/usr/lib/jvm/java-8-openjdk-amd64`).

Fall back:
```bash
bash run_all.sh --fallback
```
This skips Stage 2 and uses upstream's pre-computed `mutants_killed.csv`
as Set G's data, missing only the Set N rows. Document the limitation
in the paper.

### `verify_env.sh` reports FAIL on `python3 -c 'import pandas'`

```bash
pip3 install --user -r ../requirements.txt
export PATH=$HOME/.local/bin:$PATH
```

## When to run on Claude Code Remote vs local

| Run on Remote (Ubuntu)         | Run locally (macOS)            |
|--------------------------------|--------------------------------|
| Aligned pipeline (this dir)    | Parallel pipeline (`java_bridge/`) |
| Upstream's Linux-tested scripts | Our cross-platform Java bridge  |
| Set G transcription audited    | Quick iteration on Set N MR design |

Both are deliverables of the project; aligned is the publication-grade
comparison, parallel is the methodological supplement.
