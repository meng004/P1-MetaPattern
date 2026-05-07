# CLAUDE.md — S5 Aligned Experiment (project-level guidance)

This file is the **first thing** any agent (Claude Code local, Claude Code
Remote, claude.ai web, Codex, Gemini CLI, …) must read when working in this
repo. The rules below override default agent behavior where they conflict.

---

## Project context (one paragraph)

Single-variable comparative experiment for the NOETHER paper §6.6: Set N
(NOETHER algebra-derived MRs) versus Set G (GenMorph GP-evolved MRs) on the
full 23-subject GenMorph benchmark. Substrate (JVM, SUTs, test inputs,
mutants, evaluator, DSL) is held constant to GenMorph upstream's exact
toolchain; only the MR set varies. Stage 1 (Randoop + PIT) is **heavy
compute** (~4–7 h, ~10 GB intermediate state); Stage 2 (EvaluateMRs re-run)
is **light** (~30 min, ~50 MB).

---

## The 8 collaboration rules

### Rule 1 — CLAUDE.md is mandatory for every project

Read this file before any other action. If a sub-tree adds its own CLAUDE.md,
read that too — sub-tree rules extend (do not replace) repo-root rules.

### Rule 2 — Issues or plans before code

Every non-trivial task starts with one of:

| Doc | Path | Purpose |
|---|---|---|
| Issue | `ISSUES/<NNN>-<slug>.md` | Why: motivation, scope, success criteria |
| Plan  | `PLANS/<NNN>-<slug>.md`  | How: file-by-file changes, test gate, branch name |

A pure issue suffices for typo/format/doc fixes. Anything that touches
`scripts/`, `set_n_mrs/`, or pipeline behavior **needs both**: issue first,
plan second. Templates are in `ISSUES/TEMPLATE.md` and `PLANS/TEMPLATE.md`.

### Rule 3 — Small tasks: web execution is fine

Single-file edits, doc fixes, README updates, `.gitignore` tweaks,
typo/grammar fixes — these can be performed in claude.ai web or Claude Code
Remote without a local plan. The issue alone is enough.

### Rule 4 — Complex tasks: plan locally, execute remotely

If a task touches the pipeline (`scripts/run_all.sh`, `scripts/generate_set_n_mrs.py`,
`scripts/parse_results.py`, `scripts/aggregate_metrics.py`, the `set_n_mrs/`
DSL specifications, or the GAssert/PIT toolchain glue) **the plan must be
authored on the local Claude Code session**. Remote execution is then fine
once the plan is on disk and committed.

Rationale: the local session has full access to the GenMorph upstream
sources at `/tmp/genmorph_pilot/`, the paper draft, and reviewer notes that
the web tier does not.

### Rule 5 — One task = one branch

Branch naming convention:

| Prefix | Use for |
|---|---|
| `feat/<slug>` | new MRs, new pipeline stages, new analyses |
| `fix/<slug>`  | bug fixes in scripts or DSL files |
| `exp/<slug>`  | experimental side branches not intended for merge |
| `docs/<slug>` | README, CLAUDE.md, issue/plan additions |
| `chore/<slug>` | tooling, CI, dependency bumps |

`main` is the only persistent branch. Direct commits to `main` are
forbidden (except the very first initial commit). Merge by fast-forward or
squash from a topic branch only.

### Rule 6 — No tests, no merge

Adding or changing anything under `scripts/` requires a corresponding test
under `tests/`. The minimum bar:

* `scripts/generate_set_n_mrs.py` change → re-run + diff `set_n_mrs/` for
  expected file count, balanced parens, well-formed DSL strings.
* `scripts/parse_results.py` change → fixture-based test against a known
  `mutants_killed.csv`.
* `scripts/aggregate_metrics.py` change → synthetic per-subject metrics
  → assert pooled rates + Wilson CI.

Entry point: `bash tests/run.sh`. Must exit 0 before merge. CI hook
optional but recommended.

### Rule 7 — Web tier MUST NOT see high-sensitive secrets

This repo's `.env` and `.env.example` hold **only filesystem paths**
(JDK locations, GenMorph data root, jar paths). They contain **no API keys,
no proxy credentials, no tokens**.

Hard rules:

1. Never add real API keys (OpenAI / Anthropic / DeepSeek / Zhipu / Moonshot
   / Gemini / 阿里灵积 / etc.) to `.env`, `.env.example`, scripts, or any
   committed file.
2. Never add personal absolute paths (`/Users/<name>/…`, `C:\Users\<name>\…`)
   to committed files. Use `<REPO_ROOT>` or environment variables instead.
3. If a future task needs cloud-side credentials, generate them in the cloud
   platform's secret manager (e.g. GitHub Actions secrets, Cloudflare env
   vars), never in this repo.
4. Pre-commit grep:
   ```bash
   grep -rIn -E "(/Users/[^/]+|sk-[A-Za-z0-9]{16,}|Bearer\s+[A-Za-z0-9]+|api_key\s*=\s*['\"][^'\"]{8,})" \
     --exclude-dir=.git --exclude-dir=tests/fixtures
   # Must return no output.
   ```

### Rule 8 — Workload locality

| Workload | Cost | Where |
|---|---|---|
| `setup.sh` (apt + pip + Zenodo download + GAssert build) | ~10 min, ~80 MB | local or remote |
| Stage 1 of `run_all.sh` (Randoop + PIT for 23 subjects) | ~4–7 h, ~10 GB | local or remote |
| Stage 2 of `run_all.sh` (EvaluateMRs re-run after Set N injection) | ~30 min, ~50 MB | local or remote |
| `scripts/aggregate_metrics.py` | <1 sec | anywhere |
| Re-derive Set N MRs (`scripts/generate_set_n_mrs.py`) | <1 sec | anywhere |

Stage 1 was originally local-only out of caution about session timeouts
and disk quota; the Claude Remote environment in use has ≥30 GB persistent
disk and tolerates long-running sessions, so cloud runs are now permitted.
For long Stage 1 runs, launch with `nohup … &` so the job survives a
session disconnect — `run_all.sh` is resumable (per-subject Randoop and PIT
artifacts are cached, so a re-run skips finished subjects).

Future on-device LLM inference, private inference services, or proprietary
data **must never** be triggered from claude.ai web or Claude Code Remote.

---

## Practical workflow

```
1. Open issue:    ISSUES/<NNN>-<slug>.md          (rule 2)
2. Write plan:    PLANS/<NNN>-<slug>.md           (rules 2, 4)
3. Branch:        git checkout -b feat/<slug>     (rule 5)
4. Implement
5. Add/update test: tests/test_<area>.py          (rule 6)
6. Run gate:      bash tests/run.sh
7. Pre-commit grep for secrets/paths              (rule 7)
8. Commit + open PR (or local merge to main)
9. Close issue with link to commit
```

---

## Pointers

| Need | Path |
|---|---|
| Pipeline orchestrator | `scripts/run_all.sh` |
| MR source of truth    | `scripts/generate_set_n_mrs.py` |
| Test gate             | `tests/run.sh` |
| Issue templates       | `ISSUES/TEMPLATE.md` |
| Plan templates        | `PLANS/TEMPLATE.md` |
| Project README        | `README.md` |
| Parent paper          | `../MR元模式/NOETHER_paper.tex` (read-only reference) |

---

## Memory / state

This is a self-contained git repo separate from the parent paper
repository. Do not write paper-content edits here, and do not write
experiment-state files (results, intermediate logs) into the parent paper
repo. The boundary keeps `main` reproducible from `setup.sh + run_all.sh`
alone.
