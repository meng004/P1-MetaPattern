# B1 — Single Strongest Independent-Validation Leg: Real-Bug Evaluation on e3nn / PyG

> Deliverable for NOETHER authors (TOSEM Major Revision, B1 = one external leg that breaks the self-reference wall).
> Frozen-prereg + paste-ready cloud task + paper-integration note.
> Created 2026-06-21. Branch: `codex-tosem-maturity-review-2026-06-20`.

---

## 0. Decision: which leg, and why

**Chosen leg: Option (2) — real-bug evaluation on e3nn / PyTorch-Geometric public bug reports**, run as a CPU-only restricted variant of the paper's already-pre-registered §4.2 real-bug protocol (`para:real-bug-protocol`, L1374–1382) and hypothesis **H4** (`detection-rate non-inferiority on real faults`, L1369).

Justification, weighting `breaks_self_reference` highest, then `cloud_feasibility`/`data_availability`, then ROI:

1. **Self-reference (weighted highest): Option (2) is the only candidate scoring 5/5 that is also cloud-runnable.** It is the sole option drawing faults from a *fixed, pre-existing external defect distribution* (upstream maintainer bug commits in libraries NOETHER was demonstrably not designed against, paper L1382), so it attacks both the construct-validity threat (c) (L1333) and the binding G3 author-built-mutation critique (§3.1, §6 CRITICAL #1). Option (3) only externalises the operator *taxonomy* (DeepCrime/Humbatova) while faults stay author-injected into author-trained models — self-reference break = 2/5. Option (1) breaks it most completely (5/5) but ships no MR corpus off-the-shelf (PARCS/IAEA are physics benchmark *problems*, not MR catalogues) and would re-import self-reference if the authors author the MRs themselves.
2. **Cloud-feasibility / data-availability is the tie-breaker against Option (1).** Option (1) scores cloud_feasibility = 1 (binding work is non-author expert recruitment + manual coding, plus PARCS is RSICC export-controlled and cannot be spun up on a CPU VM) — it cannot land in a single Major-Revision cycle. Option (2)'s data (public GitHub issues/commits + their own test fixtures) is freely fetchable, and the GPU objection is dissolved by **scoping to CPU-reproducible faults only**: e3nn/PyG defects in tensor-product / spherical-harmonics / scatter / irreps-bookkeeping code reproduce on tiny hand-built tensors with **no training and no model forward pass** (see §B Step 3 selection filter). This converts the project's own "GPU-required, phase2" tag into a CPU-only subset that respects the hard constraint.
3. **ROI and HARKing-freeness.** Option (2) carries the highest maturity-lift band among B1 candidates (grok +18 / gpt +15 / qwen +12 / glm +10, §4 B1) and is *already in the paper as H4*, so freezing it before the run is genuinely HARKing-free rather than retrofitted. The only discipline required is anti-drift: H4 is framed as **non-inferiority** (MR identification scope), never as detection superiority (§C below).

**One-line verdict:** Option (2) is the strongest *actionable* B1 leg — best-in-class self-reference break that is also cloud-CPU-runnable and pre-registered; Option (1) stays the aspirational gold-standard for a later cycle, Option (3) is at best a supporting construct-validity robustness check, not the primary leg.

---

## A. PREREQUISITES (author must provide BEFORE launching)

### A.1 Cloud host spec (CPU-only)

| Item | Requirement |
|---|---|
| Compute | CPU-only VM (no GPU). 8 vCPU sufficient; 4 vCPU acceptable. |
| RAM | ≥ 16 GB (PyG + e3nn import + small-tensor reproduction; no training). |
| Disk | ≥ 30 GB free (multiple library version checkouts + two conda/venv envs + per-bug fixtures). |
| OS | Ubuntu 22.04 LTS (matches the s5_aligned scaffolding host). |
| Python | 3.10 or 3.11 (PyG/e3nn wheels). |
| Egress allowlist | `github.com`, `raw.githubusercontent.com`, `objects.githubusercontent.com`, `codeload.github.com` (clone + tarball); `pypi.org`, `files.pythonhosted.org` (pip); `download.pytorch.org` (CPU torch wheels); `data.pyg.org` (PyG CPU wheels); `conda.anaconda.org` + `repo.anaconda.com` (if conda). **Maven/Zenodo NOT needed** (this is a Python leg, distinct from s5_aligned). |
| No API keys | Zero LLM/API calls. `.env` holds filesystem paths only. CPU-only confirmed. |

### A.2 Repos / data to fetch (exact, known)

1. **Harness + frozen prereg (author repo, governance + code home):**
   `meng004/P1-MetaPattern`, branch `codex-tosem-maturity-review-2026-06-20` — holds this file, the frozen prereg (after A.4), and is where results are committed back. (Its `experiment/` is gitignored; the new harness lives in a *new* tracked dir `experiment_realbug/` created by the cloud task.)
2. **Upstream libraries under test (external, the source of self-reference break):**
   - e3nn: `https://github.com/e3nn/e3nn` (tags/commits per selected bugs).
   - PyTorch Geometric: `https://github.com/pyg-team/pytorch_geometric` (tags/commits per selected bugs).
3. **CPU PyTorch wheels:** `pip install torch --index-url https://download.pytorch.org/whl/cpu`.
4. **Bug source (data):** public GitHub Issues + linked fix PRs/commits of the two repos above. No private data. The author must NOT pre-curate which bugs "favor blocks" — see A.3.

### A.3 Human input needed (author side, BEFORE freeze)

The cloud agent cannot autonomously confirm that a GitHub issue is a genuine, fix-verified, CPU-reproducible defect mapping to a NOETHER category. The author must, **before** writing the frozen prereg, assemble a **candidate bug ledger** by a *mechanical, pre-stated* selection rule (to avoid HARKing / cherry-picking):

- **Selection rule (state verbatim in prereg, then apply once):** From the two repos' *closed* issues labelled `bug` (or equivalent) that have a *linked merged fix commit* and a *reproducing snippet or test in the issue/PR*, take the **N most-recently-fixed** that satisfy the CPU-reproducible filter (§B Step 3) — capped at the protocol target of 10, one per cat-(i)–(iv) where available, remainder by recency. Record each as `{repo, issue_url, fix_commit, pre_fix_parent_commit, cat, cpu_repro_snippet_path}`.
- The author provides this ledger as `experiment_realbug/bug_ledger.csv` committed in the SAME freeze commit as the prereg. The cloud agent then only *executes* against this frozen ledger — it does not choose bugs.
- **No author-written MRs for these bugs.** Set N/M/G/L/B are the *existing* author/baseline MR catalogues already in the paper; the only new external input is the bug distribution.

### A.4 Pre-registration step (commit a FROZEN hypothesis BEFORE the run)

Create `docs/review_2026-06-21/prereg_b1_realbug.md`, commit it together with `bug_ledger.csv`, record the commit hash, and make it the immutable reference (mirroring the s5_aligned `f2a5980` mechanism). The cloud task verifies `git diff <FREEZE_HASH> -- docs/review_2026-06-21/prereg_b1_realbug.md` is empty for the hypothesis section; non-empty ⇒ confirmatory status voided.

**Exact hypotheses to freeze (HARKing-free, anti-drift compliant):**

- **H4 (primary, pre-registered, non-inferiority — verbatim scope from paper L1369):** On the frozen real-bug ledger, Set N's real-bug detection rate is **within Δ = 0.10** of the best non-NOETHER set's detection rate (Δ fixed in advance). This is a *non-inferiority* claim on MR identification, **not** a superiority claim.
- **H4-complement (descriptive, secondary):** Report per-bug, per-set "MR fired = True/False" (detection iff ≥1 MR in the set surfaces buggy behaviour at the published tolerance, paper L1380). Report block-coverage of the fired MRs w.r.t. the algebraic decomposition. No superiority test.
- **H4-coverage (descriptive):** `coverage_NOETHER` (fraction of cat-(i)–(iv) categories present in the ledger for which Set N contains at least one block-aligned MR). Descriptive only.
- **Underpowered trigger (frozen rule, mirrors prereg `f2a5980`):** For the McNemar contrast Set N vs best-other, if discordant `b + c < 25`, report as **"underpowered, inconclusive"** with exact McNemar p (two-sided) + Wilson 95% CI, never as "confirmed non-inferiority" or "confirmed tie". If `b + c = 0`, record "test undefined".
- **Multiple-comparison correction (frozen):** Holm–Bonferroni across all pairwise Set-vs-Set McNemar tests (N vs M, N vs G, N vs L, N vs B = 4 primary; full 10-pair family if all five sets compared). Primary family = N-vs-others.
- **Direction honesty (frozen):** If Set N is NOT non-inferior (gap > 0.10), report it plainly as a negative result; do not relocate to a footnote, do not reframe as superiority elsewhere, do not drop GenMorph (Set G) loss.
- **Self-overlap red line (frozen):** The bug ledger must contain zero faults authored, injected, or selected-to-favor-blocks by the NOETHER authors; faults come only from upstream maintainer fix commits. Any ledger entry traceable to author injection voids confirmatory status.

---

## B. SELF-CONTAINED CLOUD TASK PROMPT (paste-ready; assumes a fresh cloud agent, NO prior context)

> Paste everything in the fenced block below into a fresh cloud agent session. It assumes nothing about NOETHER beyond what is stated.

```
ROLE
You are a fresh cloud agent on a CPU-only Ubuntu VM. Your job is ONE thing: execute a
pre-registered, frozen real-bug evaluation that tests whether a fixed catalogue of
metamorphic relations ("Set N") detects REAL upstream bugs in two SE(3)-equivariant
Python libraries (e3nn, PyTorch Geometric) as well as four baseline MR sets (M, G, L, B).
This is an MR-IDENTIFICATION study. You are testing NON-INFERIORITY only. You must NOT
claim or imply fault-detection superiority. CPU-only: no GPU, no model training, no
forward passes over real models, no LLM/API calls.

HARD CONSTRAINTS (do not violate)
1. Do NOT modify the frozen prereg or the bug ledger. They are immutable inputs.
2. Do NOT add, remove, or re-select bugs. Execute ONLY the bugs already in bug_ledger.csv.
3. Do NOT claim detection superiority anywhere. Frame every result as non-inferiority
   (within Δ=0.10) or as descriptive per-bug outcomes.
4. Report negative / non-significant / underpowered results honestly and prominently.
   If Set N is worse, say so plainly. Do not hide the GenMorph (Set G) comparison.
5. No self-overlap: every fault must come from an upstream maintainer fix commit listed
   in bug_ledger.csv. If any ledger row lacks {issue_url, fix_commit, pre_fix_parent_commit},
   mark it BLOCKED and exclude it from analysis (do not invent a fault).
6. CPU only. If reproducing a bug appears to require GPU, training, or a full model
   forward pass, mark that bug CPU-INFEASIBLE and exclude it (record the reason). Do NOT
   attempt GPU work.

STEP 0 — Fetch governance + ledger (read-only governance)
  git clone --branch codex-tosem-maturity-review-2026-06-20 \
    https://github.com/meng004/P1-MetaPattern.git
  cd P1-MetaPattern
  # Confirm the frozen prereg + ledger exist and record the freeze hash:
  test -f docs/review_2026-06-21/prereg_b1_realbug.md || { echo "ABORT: prereg missing"; exit 1; }
  test -f experiment_realbug/bug_ledger.csv          || { echo "ABORT: ledger missing"; exit 1; }
  FREEZE_HASH=$(git log -1 --format=%H -- docs/review_2026-06-21/prereg_b1_realbug.md)
  echo "Freeze hash: $FREEZE_HASH"
  # Read the prereg in full before doing anything else. The hypotheses, Δ, the
  # underpowered trigger (b+c<25), Holm-Bonferroni, and the self-overlap red line
  # are all defined there. Obey them verbatim.

STEP 1 — Environment (CPU-only Python)
  python3 -m venv .venv_realbug && . .venv_realbug/bin/activate
  pip install --upgrade pip
  pip install torch --index-url https://download.pytorch.org/whl/cpu
  pip install numpy scipy pandas statsmodels pytest
  # e3nn / PyG are installed PER-BUG at the bug's pre-fix commit (Step 3), not globally,
  # because different bugs pin different versions. Keep the base env clean.

STEP 2 — Validate the frozen ledger
  For each row in experiment_realbug/bug_ledger.csv expect columns:
    repo, issue_url, fix_commit, pre_fix_parent_commit, cat, cpu_repro_snippet_path
  Mark a row BLOCKED (and exclude) if any of {fix_commit, pre_fix_parent_commit,
  cpu_repro_snippet_path} is empty or the snippet file is missing. Print the count of
  usable vs blocked rows. Do NOT fill in missing data yourself.

STEP 3 — Per-bug reproduction (CPU, no training)  [for each USABLE row]
  3a. Shallow-checkout the library at the PRE-FIX parent commit into an isolated dir:
        git clone https://github.com/<repo>.git bug_<id>_src
        (cd bug_<id>_src && git checkout <pre_fix_parent_commit>)
        pip install -e bug_<id>_src      # CPU; if build needs GPU/CUDA, mark CPU-INFEASIBLE
  3b. CPU-reproducibility filter: run the cpu_repro_snippet on TINY hand-built tensors
      (irreps / spherical-harmonics / tensor-product / scatter / index-bookkeeping inputs).
      The snippet must reproduce the buggy behaviour WITHOUT training and WITHOUT a full
      model forward pass. If it needs GPU/training/full-model -> CPU-INFEASIBLE, exclude.
  3c. Run all five MR sets (N, M, G, L, B) against the BUGGY pre-fix code on the snippet's
      inputs, using the existing MR definitions shipped in experiment_realbug/mr_sets/
      (these are the SAME catalogues as in the paper; do NOT author new MRs).
      Record per set: "MR fired = True" iff >=1 MR in the set surfaces the buggy behaviour
      at the published tolerance (tolerance taken from the bug's fixture / issue).
  3d. Sanity gate (no self-overlap, no false detection): also run the SAME MR sets against
      the POST-FIX code (checkout <fix_commit>) on the SAME inputs. A correct MR must NOT
      fire on fixed code (false-positive check). Record post-fix firing; any set that fires
      on fixed code on that input is flagged FP for that bug.
  3e. Persist per-bug result JSON: experiment_realbug/results/bug_<id>.json with fields:
      {id, repo, cat, pre_fix_commit, fix_commit, tolerance,
       fired_pre:{N,M,G,L,B}, fired_post:{N,M,G,L,B}, fp_flags:{...},
       cpu_status:"OK|CPU-INFEASIBLE|BLOCKED", notes}

STEP 4 — Pre-registered analysis (exactly as frozen; clustered/paired where relevant)
  Build a bug x set detection matrix from the OK bugs only (exclude CPU-INFEASIBLE/BLOCKED;
  report their counts separately and transparently).
  4a. Per-set detection rate = (#bugs Set fired pre-fix AND not FP) / (#OK bugs).
      Report Wilson 95% CI per set. Note: bugs are the independent unit (one fault each),
      so per-bug binary outcomes are the natural unit; if multiple inputs per bug exist,
      aggregate to one bug-level binary first (fired on >=1 input), to avoid pseudo-
      replication within a bug.
  4b. Pairwise McNemar EXACT (paired by bug) for N vs each of {M,G,L,B}. For each pair
      compute discordant b,c. Apply the frozen underpowered trigger: if b+c<25 -> report
      "underpowered, inconclusive" + exact two-sided McNemar p + both Wilson CIs; if b+c=0
      -> "test undefined". Never upgrade an underpowered result to "confirmed".
  4c. Holm-Bonferroni correct the family of pairwise p-values (primary family = N-vs-others).
  4d. H4 non-inferiority verdict: gap = (best non-N set rate) - (Set N rate). If gap <= 0.10
      -> "H4 non-inferiority supported (within Δ=0.10)"; if gap > 0.10 -> "H4 NOT supported:
      Set N trails best baseline by <gap>" (state plainly, no reframing).
  4e. coverage_NOETHER (descriptive): fraction of cat-(i)-(iv) present in the OK ledger for
      which Set N has >=1 block-aligned MR. Descriptive only, no p.
  4f. Frozen-prereg integrity check:
        git diff <FREEZE_HASH> -- docs/review_2026-06-21/prereg_b1_realbug.md
      Must be empty for the hypothesis section. If not empty -> print
      "CONFIRMATORY STATUS VOIDED" and still report results as exploratory.

STEP 5 — Report back (fill this template; commit to a new branch)
  Create branch claude/b1-realbug-<runid>, write experiment_realbug/RESULTS.md using the
  template in section "RESULTS TEMPLATE" below, commit bug_<id>.json files + RESULTS.md +
  the analysis script, and push. Then paste RESULTS.md back as your final message.

ANTI-DRIFT GUARDS (restate in your RESULTS.md verbatim)
  - This is MR IDENTIFICATION. Claim only NON-INFERIORITY (within Δ=0.10) or descriptive
    per-bug outcomes. Do NOT claim Set N detects more / better.
  - Report every negative, non-significant, and underpowered result prominently.
  - Do NOT hide or soften the Set G (GenMorph) comparison.
  - Faults are external (upstream fix commits). State the bug provenance for every bug.
  - Exclude, with reasons, any CPU-INFEASIBLE or BLOCKED bug; never fabricate a fault.

SECRET / SAFETY HYGIENE
  - No API keys anywhere. .env (if any) holds filesystem paths only.
  - Before pushing: grep the diff for absolute home paths and any token-like strings;
    abort the push if found.
```

### RESULTS TEMPLATE (the cloud agent fills this and pastes it back)

```markdown
# B1 Real-Bug Evaluation (e3nn / PyG) — Results

Freeze hash: <FREEZE_HASH>     Prereg integrity: <intact | VOIDED>
Run id: <runid>                Branch: claude/b1-realbug-<runid>
CPU-only confirmed: yes        GPU used: no        LLM/API calls: none

## Ledger accounting
- Ledger rows: <total>
- OK (analysed): <n_ok>    CPU-INFEASIBLE (excluded): <n_inf>    BLOCKED (excluded): <n_blk>
- Category coverage in OK set: cat-(i) <k>, cat-(ii) <k>, cat-(iii) <k>, cat-(iv) <k>

## Per-set detection (OK bugs only)
| Set | fired/total | rate | Wilson 95% CI |
|-----|------------:|-----:|---------------|
| N   | x/n | r | [lo, hi] |
| M   | ... | . | ...           |
| G   | ... | . | ...           |
| L   | ... | . | ...           |
| B   | ... | . | ...           |

## Pairwise McNemar (paired by bug), Holm-Bonferroni corrected
| Pair  | b | c | b+c | exact p (2-sided) | Holm p | verdict |
|-------|--:|--:|----:|------------------:|-------:|---------|
| N vs M | . | . | . | . | . | <underpowered b+c<25 | inconclusive | ...> |
| N vs G | . | . | . | . | . | ... |
| N vs L | . | . | . | . | . | ... |
| N vs B | . | . | . | . | . | ... |

## H4 verdict (non-inferiority, Δ=0.10)
best non-N rate = <r>;  Set N rate = <r>;  gap = <g>
=> <H4 non-inferiority supported (within Δ=0.10) | H4 NOT supported: Set N trails by <g>>
(Underpowered? <yes/no, b+c per primary contrast>)

## coverage_NOETHER (descriptive)
<fraction> of cat-(i)-(iv) categories present have a block-aligned Set N MR.

## False-positive check (post-fix firing)
<sets that fired on fixed code, per bug; should be none for a correct MR>

## Honest negatives / limitations
- <e.g. "n_ok=7 < 10 target; underpowered for inferential conclusions; reported descriptively (C6).">
- <Set G comparison stated plainly: ...>
- <Excluded bugs and why.>

## Anti-drift attestation
- MR-identification scope only; non-inferiority framing; no superiority claim.
- All negatives/underpowered results reported above; GenMorph comparison not hidden.
- All faults are upstream maintainer fix commits (provenance per bug in bug_<id>.json).
```

---

## C. How the result plugs back into the paper (no overclaiming)

**Target sections to upgrade:**

1. **§4.2 Real-bug evaluation (`para:real-bug-protocol`, L1374–1382)** — currently a *protocol committed but not run* ("we mine cat-(i)–(iv) faults … Target: 10 confirmed real-bug commits"). The result converts this from a *promise* into an *executed external evaluation*. Replace the future-tense protocol prose with a results subsection reporting the H4 non-inferiority verdict, per-set Wilson CIs, Holm-corrected McNemar, and the honest underpowered/negative caveats.

2. **§Threats — Construct validity (L1333 threat (c), L2629)** — currently concedes the mutation set is "hand-constructed … constructed to cover one defect category per non-empty block", so the cat-(iv) 5/5 result is "construct validity … not NOETHER's superiority on a defect distribution sampled neutrally from real-world bug reports". This leg directly supplies that neutrally-sampled distribution. The threat text can move from "committed as comparative addition" to "addressed: on a fixed external defect distribution NOETHER was not designed against, Set N is non-inferior within Δ=0.10 (or: trails by <g> — stated plainly)".

3. **§6 / maturity binding constraint G3 (self-reference)** — this is the one claim it upgrades from *self-referential* to *independently corroborated*: the faults are author-independent (upstream maintainer fixes), so the EQ1/EQ3 author-vs-author loop is broken **for the real-bug leg**.

**What it does NOT do (anti-overclaim guardrails):**

- It does **not** make the mutation κ independent — that still requires B2 (independent human raters). State both legs are needed.
- It does **not** establish fault-detection *superiority*; H4 is non-inferiority only. The paper must keep detection demoted to a secondary executability check (matches C5, L262, and D1/D4 anti-drift).
- It does **not** generalise beyond e3nn/PyG SE(3)-equivariant code; cross-domain breadth and the reactor-corpus external leg (Option 1) remain future work.
- If `n_ok < 10` or the primary McNemar `b+c < 25`, the paper must label it **"n=<n_ok>, underpowered for α=0.05; reported as descriptive evidence"** (C6), not "confirmed". A non-inferiority PASS on a small external sample is still meaningful (it breaks self-reference) but must be reported with its Wilson CI and the underpowered caveat, not as a headline win.

**One-sentence claim the author may make after a clean run:** *"On a fixed set of upstream e3nn/PyG bug-fix commits that NOETHER was not designed against, Set N's real-bug detection rate is non-inferior (within Δ=0.10) to the best baseline (Holm-corrected; n reported with Wilson CIs), providing the first author-independent fault evidence for the identification protocol; mutation-label reliability remains to be confirmed by independent human raters (B2)."*
```
