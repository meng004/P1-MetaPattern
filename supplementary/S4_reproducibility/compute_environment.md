# Compute environment

## Hardware (manuscript's actual reproduction platform)

- **Host machine**: Apple MacBook Pro (MacBookPro18,3), Apple M1 Pro
  10-core SoC (8 performance + 2 efficiency cores), 32 GB unified memory,
  macOS 24.6.0 (Darwin)
- **Accelerator**: M1 Pro integrated GPU via PyTorch MPS backend
  (`torch.backends.mps`). No discrete GPU.
- **Disk**: 411 GB free (only ~5 GB needed for the full archive plus
  trained checkpoint plus dataset)

## Hardware (reference higher-performance configuration)

For collaborators with CUDA hosts, the reference platform we have also
tested is:

- single NVIDIA A100 (40 GB), AMD EPYC 7763, 256 GB RAM, Ubuntu 22.04,
  CUDA 12.1, cuDNN 8.9

Switching between platforms only requires picking block (A) or (B) of
`environment.yml`; no source-code changes.

## Software

- OS: macOS 24.6.0 (primary) / Ubuntu 22.04 LTS (reference)
- Python 3.11 (3.12 also tested)
- PyTorch 2.4 (MPS on Apple Silicon; CUDA 12.1 build on Linux host)
- e3nn 0.5.1
- (full dependency manifest in `environment.yml`)

## Expected wall-clock budget on M1 Pro

| Step | M1 Pro MPS | A100 (reference) |
|---|---|---|
| Install env (conda + pip) | 5–10 min | 5–10 min |
| Download ModelNet10 (~800 MB) | 2–5 min | 2–5 min |
| Train SE(3)-Transformer baseline (30 epochs) | 1.5–3 h | ~30 min |
| Run §6.6 case study (`runner.py`) | 2–5 min | <1 min |
| Run `analysis.py` (deterministic) | <5 s | <5 s |

The training step is the only one that benefits significantly from a
discrete GPU. The case study itself (the published Table 4 numbers) is
fast on M1 Pro. The `runner.py --stub` smoke test is independent of
torch/e3nn entirely and finishes in ~30 s on any machine.

## Reproducibility commitments

- All randomised steps use the seeds in `seeds.txt`.
- The reference checkpoint is bit-identical across re-runs *on the same
  hardware* given the seed and dataset hashes in `dataset_versions.txt`.
  Cross-platform bit-reproducibility is **not** claimed: PyTorch's MPS
  backend on M1 Pro and CUDA on A100 produce slightly different
  intermediate floats. The resulting differences in Table 4 entries are
  bounded by ±1 mutation per MR-set in our internal cross-platform
  spot-check.
- The 20-mutation set is statically defined (each mutation is a code
  diff or a `Mutation` object); see `S3_case_study/mutations/manifest.json`
  for diff hashes.

## Apple-Silicon-specific notes

- The MPS backend is enabled by default in PyTorch 2.4. Verify with:
  ```python
  import torch; print(torch.backends.mps.is_available())  # → True on M1 Pro
  ```
- A subset of e3nn ops (most prominently spherical-harmonics tensor
  products at high `lmax`) currently fall back to CPU on MPS in torch
  2.4. To force CPU fallback for any unsupported op, run with:
  ```
  export PYTORCH_ENABLE_MPS_FALLBACK=1
  ```
- If you encounter an MPS-only crash, the simplest workaround is to add
  `--device cpu` to the training script; the case-study `runner.py`
  also works on CPU with a 2–3× slowdown vs MPS.
- An alternative if e3nn proves troublesome on MPS: substitute EGNN
  (Equivariant GNN) for the SE(3)-Transformer. EGNN has full MPS support
  and the §6 instantiation goes through unchanged at the
  operator-algebra level (only the architecture description in §6.1
  needs a one-sentence update).

## To re-run the case study from scratch

```bash
cd supplementary/
conda env create -f S4_reproducibility/environment.yml   # block (A) by default
conda activate noether-equivariant
cd S3_case_study

# Smoke test: stub mode, no torch/e3nn required, ~30 s
python runner.py --stub --output results_stub.csv
python analysis.py results_stub.csv --output-dir .

# Real run (after training the checkpoint, see model/README)
python runner.py --checkpoint model/se3_transformer_modelnet10.pt \
                 --output results.csv
python analysis.py results.csv --output-dir .
```

## Pre-flight checks

- `pytest test_construct_mp.py` (in S1) should report 13 passed.
- `python boltzmann_instance.py` (in S1) should output 7 MetaPatterns
  with `coverage_NOETHER (full set) = 1.00`.
- `python equivariant_instance.py` (in S1) should output 5 non-empty
  MetaPatterns with `coverage_NOETHER (full N set) = 1.00`.
- `python runner.py --stub --output /tmp/r.csv` followed by
  `python analysis.py /tmp/r.csv` should print `H1 verdict: HOLDS`
  and `H2 verdict: HOLDS`.

If any of these pre-flight checks fails, do not proceed with the real
case study — the failure indicates an environment misconfiguration that
will contaminate the results.
