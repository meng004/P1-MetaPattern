# B1 Real-Bug Evaluation (e3nn / PyG) — Results

Freeze hash: PENDING     Prereg integrity: intact
Run id: b1-pyscf                Branch: claude/b1-realbug-b1-pyscf
CPU-only confirmed: yes        GPU used: no        LLM/API calls: none

## Ledger accounting
- Ledger rows analysed: 9
- OK (analysed): 8    CPU-INFEASIBLE (excluded): 0    BLOCKED (excluded): 0
- Category coverage in OK set: L* convergence (dense-output self-consistency) 1, T* self-adjoint (driver-invariance of the eigenproblem) 1, cat-ii 1, conservation (Noether: electron-number conservation) 1, conservation / representation-invariance (same Jacobian, full vs banded storage) 1, m^eq_adj-family (graph symmetrization completeness) 1, m^eq_adj-family (role-swap duality, antisymmetric parity variant) 1, out-of-decomposition 1

## Per-set detection (OK bugs only; denominator = applicable bugs per set)
| Set | fired/total | rate | Wilson 95% CI |
|-----|------------:|-----:|---------------|
| N | 7/7 | 1.000 | [0.646, 1.000] |
| M | 1/1 | 1.000 | [0.207, 1.000] |
| G | — | — | **not evaluable on library bugs** (no portable Set-G artefact; manifest) |
| L | 0/0 | nan | [nan, nan] |
| B | 0/1 | 0.000 | [0.000, 0.793] |

## Pairwise McNemar (paired by bug), Holm-Bonferroni corrected (N-vs-others)
| Pair | b | c | b+c | exact p (2-sided) | Holm p | verdict |
|------|--:|--:|----:|------------------:|-------:|---------|
| N vs M | 0 | 0 | 0 | — | — | test undefined (b+c=0) |
| N vs L | 0 | 0 | 0 | — | — | test undefined (b+c=0) |
| N vs B | 1 | 0 | 1 | 1.0000 | 1.0000 | underpowered, inconclusive (b+c<25) |
| N vs G | — | — | — | — | — | Set G not evaluable (excluded) |

## H4 verdict (non-inferiority, Δ=0.1)
best non-N rate = 1.000;  Set N rate = 1.000;  gap = 0.000
=> **H4 non-inferiority SUPPORTED (gap=0.000 <= Δ=0.1)**
(Underpowered? YES; min primary discordant b+c = 0; n_ok = 8)

## coverage_NOETHER (descriptive)
7/8 = 0.875 of cat categories present have a block-aligned Set N MR.

## False-positive check (MR fired on POST-FIX code)
None.

## Honest negatives / limitations
- n_ok=8 < 10 target; **underpowered for α=0.05; reported as descriptive evidence (C6).**
- Set G stated plainly: not evaluable on library bugs (substrate limitation), reported as such, not as 0 detections.
- Cross-set overlap (rho_rot ≡ L_rot ≡ B-rotation on the same rotation category) makes set counts correlated, not independent.

## Anti-drift attestation
- MR-identification scope only; non-inferiority framing; **no superiority claim**.
- All negatives/underpowered results reported above; GenMorph (Set G) comparison not hidden (stated not-evaluable).
- All faults are upstream maintainer fix commits (provenance per bug in bug_<id>.json).
