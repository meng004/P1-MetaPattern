# Paste-into-/websetup snippet

This file contains the **exact strings** to paste into Claude Code
Remote's `/websetup` interface, in the order required.

---

## Option 1 — Single-bash blob (preferred if /websetup accepts shell)

```bash
sudo apt-get update -y && sudo apt-get install -y openjdk-8-jdk openjdk-11-jdk maven python3-pip wget unzip git curl ca-certificates && \
cd "$WORKSPACE_OR_REPO_PATH/supplementary/S5_genmorph_pilot/websetup" && \
bash bootstrap.sh && \
bash verify_env.sh && \
echo "Environment ready. Run 'bash run_all.sh' to execute the aligned experiment."
```

Replace `$WORKSPACE_OR_REPO_PATH` with the actual path Claude Code Remote
mounts the repo at (commonly `/workspace` or `/home/coder/project`).

---

## Option 2 — Step-wise commands (if /websetup is interactive)

### Step 1: install OS packages

```
sudo apt-get update -y
sudo apt-get install -y openjdk-8-jdk openjdk-11-jdk maven python3-pip wget unzip git curl ca-certificates
```

### Step 2: navigate to project + provision data + env

```
cd $REPO_ROOT/supplementary/S5_genmorph_pilot/websetup
bash bootstrap.sh
```

(downloads ~80 MB Zenodo zips; takes 2–5 min on typical bandwidth)

### Step 3: verify

```
bash verify_env.sh
```

Should print `PASS: 25+ FAIL: 0`. If FAIL > 0, follow remediation
hints in `WEBSETUP.md` §Troubleshooting.

### Step 4: run aligned experiment

```
bash run_all.sh
```

Takes 15–30 minutes. Result files appear in
`../aligned/results/seed11/`.

### Step 5: aggregate

```
python3 ../efficiency_metrics.py \
    --results ../results/gcd/results.csv ../results/sin/results.csv \
    --subjects gcd sin \
    --output ../results/efficiency_metrics.json
```

---

## Option 3 — Dev container (if /websetup uses devcontainer.json)

If `/websetup` produces or expects a `.devcontainer/devcontainer.json`
file, here is a minimal spec:

```json
{
  "name": "S5 Aligned Pilot",
  "image": "mcr.microsoft.com/devcontainers/java:0-11-jdk-bullseye",
  "features": {
    "ghcr.io/devcontainers/features/java:1": {
      "version": "8",
      "installMaven": "true",
      "mavenVersion": "3.6.3"
    },
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.10"
    }
  },
  "postCreateCommand": "cd ${containerWorkspaceFolder}/supplementary/S5_genmorph_pilot/websetup && bash bootstrap.sh && bash verify_env.sh",
  "remoteEnv": {
    "JAVA8": "/usr/lib/jvm/java-8-openjdk-amd64",
    "JAVA11": "/usr/lib/jvm/java-11-openjdk-amd64",
    "GENMORPH": "/tmp/genmorph_pilot/genmorph_full/genmorph"
  }
}
```

After devcontainer comes up, run `bash run_all.sh` manually inside the
container (it's not in `postCreateCommand` because it takes 15–30 min
which would block container creation).

---

## What to expect after /websetup completes

| Phase                | Time est. | What's there                                 |
|----------------------|-----------|----------------------------------------------|
| OS deps installed    | 1–2 min   | jdk-8, jdk-11, maven, python deps            |
| Zenodo data unzipped | 2–5 min   | /tmp/genmorph_pilot/{evaluation,mrs,genmorph_full}/  |
| Env vars set         | <1 sec    | ~/.bashrc-genmorph                           |
| Python deps installed| 30 sec    | pandas, scipy, statsmodels, numpy            |
| Verify reports green | <5 sec    | 25+ checks pass                              |
| (manual) run_all.sh  | 15–30 min | aligned/results/seed11/<subject>/aligned_metrics.json |

---

## After /websetup — handover for actual experiment

Open a new chat/turn in the same Claude Code Remote session and run:

```
bash $REPO_ROOT/supplementary/S5_genmorph_pilot/websetup/run_all.sh
```

Then ask Claude Code to:

> "Read `aligned/results/seed11/*/aligned_metrics.json` and summarise the
> Set N vs Set G comparison under aligned pipeline conditions. Compare
> to the parallel-pipeline numbers in `results/efficiency_metrics.json`.
> Identify which Set N MRs in (jir, jor) form (Path B) survived the FP
> baseline check (FP ≤ 5/100), and which fell back to Path C or were
> rejected by GAssert's parser."

That instruction is the bridge from "environment ready" to "data
回填到论文 §6.6".

---

## File-by-file paste references

If `/websetup` requires uploading specific files, the minimum set is:

```
supplementary/S5_genmorph_pilot/
├── requirements.txt                              # python deps
├── aligned/
│   ├── README.md
│   ├── parse_aligned_results.py
│   └── set_n_mrs/                                # 16 .jir/.jor files
│       ├── MathClass?gcd?0/                       # 8 files (4 MRs × 2)
│       └── MathClass?sin?0/                       # 8 files
├── efficiency_metrics.py                         # cross-subject aggregator
└── websetup/
    ├── bootstrap.sh
    ├── verify_env.sh
    ├── run_all.sh
    └── WEBSETUP.md
```

Total: ~30 files, well under any /websetup file-count cap.
