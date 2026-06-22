# B1 Real-Bug Evaluation (e3nn / PyG) — Results

Freeze hash: PENDING     Prereg integrity: intact
Run id: b1-complexsym                Branch: claude/b1-realbug-b1-complexsym
CPU-only confirmed: yes        GPU used: no        LLM/API calls: none

## Ledger accounting
- Ledger rows analysed: 18
- OK (analysed): 17    CPU-INFEASIBLE (excluded): 0    BLOCKED (excluded): 0
- Category coverage in OK set: G symmetry (geometric equivalence invariance) 1, G symmetry (rotational geometric-equivalence invariance) 1, L* convergence (dense-output self-consistency) 1, O<= (parabolic maximum principle) 1, T* self-adjoint (driver-invariance of the eigenproblem) 1, T* self-adjoint/symmetric structure (structure-invariance of solve/inv: A == A^T) 1, Trev* (time-reversal symmetry) 1, cat-ii 1, conservation (Noether: electron-number conservation) 1, conservation / flux (Neumann no-flux == mass/energy conservation boundary; Noether) 1, conservation / method-invariance (MPI tally reduction must not change normalized tally) 1, conservation / representation-invariance (same Jacobian, full vs banded storage) 1, m^eq_adj-family (graph symmetrization completeness) 1, m^eq_adj-family (role-swap duality, antisymmetric parity variant) 1, out-of-decomposition 1, self-consistency / convergence (NOETHER L* block) 1, symmetry / equivariance (a periodic BC u(x)=u(x+L e_k) is a discrete translation symmetry; periodic_point is the group-action / orbit map; Noether symmetry block) 1

## Per-set detection (OK bugs only; denominator = applicable bugs per set)
| Set | fired/total | rate | Wilson 95% CI |
|-----|------------:|-----:|---------------|
| N | 16/16 | 1.000 | [0.806, 1.000] |
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
(Underpowered? YES; min primary discordant b+c = 0; n_ok = 17)

## coverage_NOETHER (descriptive)
16/17 = 0.941 of cat categories present have a block-aligned Set N MR.

## False-positive check (MR fired on POST-FIX code)
None.

## Honest negatives / limitations
- Set G stated plainly: not evaluable on library bugs (substrate limitation), reported as such, not as 0 detections.
- Cross-set overlap (rho_rot ≡ L_rot ≡ B-rotation on the same rotation category) makes set counts correlated, not independent.

## Anti-drift attestation
- MR-identification scope only; non-inferiority framing; **no superiority claim**.
- All negatives/underpowered results reported above; GenMorph (Set G) comparison not hidden (stated not-evaluable).
- All faults are upstream maintainer fix commits (provenance per bug in bug_<id>.json).
