# B1 Real-Bug Evaluation (paper SUT domains; 5 MetaPatterns / 10 MR families a-j) -- Results

Freeze hash: <FREEZE_HASH>     Prereg integrity: intact
Run id: local                Branch: claude/b1-realbug-local
CPU-only confirmed: yes        GPU used: no        LLM/API calls: none

## Ledger accounting
- Ledger rows analysed: 27
- OK (analysed): 26    CPU-INFEASIBLE (excluded): 0    BLOCKED (excluded): 0
- Category coverage in OK set: G symmetry (Hermitian-symmetry preservation of the real-FFT (rfft/irfft) round-trip) 1, G symmetry (Noether: molecular point-group invariance of orbital irrep labels) 1, G symmetry (geometric equivalence invariance) 1, G symmetry (rotational geometric-equivalence invariance) 1, L* convergence (dense-output self-consistency) 1, L* convergence / limit operator (NOETHER L* block: a tally trigger is the discrete statement of an L* convergence criterion on the eigenvalue source iteration -- iterate active batches until rel_err(score) < threshold, a converged limit bounded by trigger_max_batches; binding the trigger to its score is the precondition for that limit operator to exist). reactor_physics 4th block. 1, L* convergence / limit operator (a PINN minimises a residual loss on a FIXED collocation set X; training is a discrete limit theta_t -> theta* converging to the minimiser of L(theta;X); if X is re-sampled every step the objective L(theta;X_t) moves and the limit operator is broken; NOETHER L* block) 1, L*.rep representation/method-invariance (family j; Mode M: same fixed-source problem, MPI tally reduction must not change the normalized tally) 1, L*.rep representation/method-invariance (family j; Mode M: the SAME Jacobian in full vs banded storage must give the SAME stiff trajectory -- y_banded==y_full) 1, O<= (monotone / linear shape-preservation: monotone data must give a monotone interpolant; two points must give the linear chord) 1, O<= (parabolic maximum principle) 1, O<= monotonicity / boundary-value / order-preservation (NOETHER O<= block: a Dirichlet boundary condition u=g must be ENFORCED at boundary collocation points; a point lying ON the boundary must be detected as boundary -- on_boundary=True, nonzero outward normal -- and selected by the BC filter. The boundary-value side of the order/boundary block). 1, O<= positivity (physical-quantity non-negativity: number densities N >= 0) 1, T* self-adjoint (driver-invariance of the eigenproblem) 1, T* self-adjoint / adjoint-weighting duality (NOETHER T* block: IFP estimates the ADJOINT(importance)-weighted kinetics parameters beta_eff = <phi-dagger, chi_d nu_d Sigma_f phi> / <phi-dagger, chi nu Sigma_f phi>; the iterated fission probability realises the adjoint weight phi-dagger; the forward<->adjoint duality is the structural symmetry and beta_eff/Lambda are the conserved bilinear forms in testable form) 1, T* self-adjoint / operator-symmetry (NOETHER T* block: the Hessian of a scalar field is self-adjoint -- H[i,j] == H[j,i], the discrete mixed-partial / Schwarz symmetry; a forward-mode Jacobian-indexing bug breaks that operator symmetry). pde_sciml T* block. 1, T* self-adjoint/symmetric structure (structure-invariance of solve/inv: A == A^T) 1, Trev* (time-reversal symmetry) 1, cat-ii 1, conservation (Noether: electron-number conservation) 1, conservation / flux (Neumann no-flux == mass/energy conservation boundary; Noether) 1, m^eq_adj-family (graph symmetrization completeness) 1, m^eq_adj-family (role-swap duality, antisymmetric parity variant) 1, out-of-decomposition 1, self-consistency / convergence (NOETHER L* block) 1, symmetry / equivariance (a periodic BC u(x)=u(x+L e_k) is a discrete translation symmetry; periodic_point is the group-action / orbit map; Noether symmetry block) 1

## Per-set detection (OK bugs only; denominator = applicable bugs per set)
| Set | fired/total | rate | Wilson 95% CI |
|-----|------------:|-----:|---------------|
| N | 25/25 | 1.000 | [0.867, 1.000] |
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
(Underpowered? YES; min primary discordant b+c = 0; n_ok = 26)

## coverage_NOETHER (descriptive)
25/26 = 0.962 of cat categories present have a block-aligned Set N MR.

## False-positive check (MR fired on POST-FIX code)
None.

## Honest negatives / limitations
- Set G stated plainly: not evaluable on library bugs (substrate limitation), reported as such, not as 0 detections.
- Cross-set overlap (rho_rot ≡ L_rot ≡ B-rotation on the same rotation category) makes set counts correlated, not independent.

## Anti-drift attestation
- MR-identification scope only; non-inferiority framing; **no superiority claim**.
- All negatives/underpowered results reported above; GenMorph (Set G) comparison not hidden (stated not-evaluable).
- All faults are upstream maintainer fix commits (provenance per bug in bug_<id>.json).
