# mr_sets applicability manifest — MR↔library-bug (workflow we8ipq0ti)

> 19-agent workflow: 9 设计 + 9 对抗验证 + 合成。逐条判定论文 5 条 Set N MR + 4 基线集对 e3nn/PyG 库级缺陷的适用性,给可执行实现(实现已落 `mr_sets/*.py`)。
> **关键诚信点**:Set G(GenMorph)报 **"not evaluable on library bugs"**(每 SUT 重演化、无固定目录),**不**报 "0 检出"(否则假装跑了又漏)。两处 `fix_needed`(rho_adj/set_M)已在对应 .py 头部标注精确缺陷+修法。

This is a synthesis task over already-provided JSON. No file access needed. Let me apply the verifier corrections and produce the manifest.

Two verdicts downgrade nothing to "not_applicable" but two are `fix_needed` (rho_adj, set_M_metric) — both keep `corrected_applicability: adaptable`. So no downgrades change the applicability label; the fixes are implementation bugs to wire, not applicability changes. One upgrade exists (rho_rot designer said "portable", verifier corrected to "portable" — consistent).

# B1 Real-Bug Leg — mr_sets Applicability Manifest

## (1) Per-MR final applicability

| mr_name | set | FINAL applicability | target bug categories |
|---|---|---|---|
| rho_rot | N | **portable** | SO(3) rotation-equivariance/invariance defects: spherical_harmonics normalization/ordering/sign, Wigner-D / w_3j / Clebsch-Gordan sign-index, tensor-product covariance breaks, scatter-on-geometry equivariance, l=0 scalar silently varying under rotation |
| rho_adj | N | **adaptable** (fix_needed) | CG sign/index role-swap asymmetry, irreps in1↔in2 slot mishandling, "symmetric" tensor-square not actually symmetric, swapped-order crashes |
| rho_train_rev | N | **not_applicable** | — (SGD-trajectory round-trip; no η/T/optimizer in pure library ops) |
| rho_mono | N | **adaptable** | idempotent scatter/segment reduce duplicate-row redundancy, max/min pooling dominated-point redundancy, feature-aggregation add/remove-redundant stability |
| rho_train_inf | N | **adaptable** | nondeterministic scatter/index_add ordering, in-place input mutation, stale/wrong-keyed cache (Wigner-D/CG/irreps), output-input aliasing, declared-idempotent norm/projection violations |
| set_L_llm | L | **adaptable** | rotation/equivariance (SH/TP), scatter/segment commutativity (permutation), opt-in homogeneity/normalization (L_scale deviating) |
| set_B_lit | B | **adaptable** | scatter/segment permutation-invariance, in-place mutation / idempotency, irreps/SH/TP rotation-or-scale equivariance (ctx-supplied) |
| set_G_genmorph | G | **not_applicable** | — (no fixed MR catalogue; requires per-SUT GP toolchain offline) |
| set_M_metric | M | **adaptable** (fix_needed) | scatter/segment perm-order, irreps ordering perm-sensitivity, homogeneity/scaling defects, additive-offset/centering, sign/parity even-odd irrep |

Note: no verifier verdict *downgraded* an applicability label — both `fix_needed` cases (rho_adj, set_M_metric) retain `adaptable`; the fixes are implementation soundness bugs (false positive on transpose-equal traces; false negative on perm_equivariant+index dead branch), not applicability changes.

## (2) Per-set portability and evaluability on library bugs

| Set | portable | adaptable | not_applicable | applicable total | Evaluable on B1 library bugs? |
|---|---|---|---|---|---|
| **N** | 1 (rho_rot) | 3 (rho_adj, rho_mono, rho_train_inf) | 1 (rho_train_rev) | **4 of 5** | **Yes** — strongest arm |
| **M** | 0 | 1 (set_M_metric, after fix) | 0 | **1 of 1** | **Yes**, conditional on dead-branch fix |
| **G** | 0 | 0 | 1 (set_G_genmorph) | **0 of 1** | **No** — not evaluable on library bugs (substrate-limitation: GP toolchain cannot run as `mr(fn,ctx,tol)`) |
| **L** | 0 | 1 (set_L_llm; internally splits: L_rot/L_perm live, L_scale opt-in, L_trans/L_noise N/A) | 0 | **1 of 1** | **Yes** |
| **B** | 0 | 1 (set_B_lit; internally splits: perm/idempotency/transform live, sub-sampling N/A) | 0 | **1 of 1** | **Yes** |

Critical honesty point for **Set G**: report as **"not evaluable on library bugs"**, NOT as "0/N detections". Scoring it 0 would falsely imply the relations ran and missed; in fact no portable Set-G artefact exists for this substrate (same structural exclusion the paper applies to MR-Scout). This is a property of the real-bug port, not a Set-G capability deficit.

## (3) Honest consequence for denominators and H4

- **Denominators are per-set applicable counts, not raw catalogue size.** Set N's denominator is the count of bugs where ≥1 of {rho_rot, rho_adj, rho_mono, rho_train_inf} returns applicable (held/fired), with rho_train_rev contributing nothing. A bug where every set member returns `not_applicable` must be excluded from that set's denominator (it is "no definition," not "a miss") — otherwise you understate every set uniformly and bias toward the set with the broadest ctx coverage.
- **Set G has no denominator.** It drops out of the executable head-to-head entirely. H4 must not present a Set-N-vs-Set-G number on B1; the only legitimate Set-G statement is the substrate-limitation footnote.
- **What H4 *can* claim:** a head-to-head of detection rate among the **evaluable arms (N, M, L, B)** on the B1 real-bug set, where N carries 4 applicable MRs vs single-MR-equivalent arms M/L/B (each one composite dispatcher). Cross-set overlap is real and must be disclosed: rho_rot ≡ L_rot ≡ B-rotation-branch all fire on the same rotation-equivariance category; set-level detection counts are therefore correlated, not independent, so any "N beats B/L" margin should be reported with the overlap acknowledged.
- **What H4 *cannot* claim:** (a) any superiority over Set G on library bugs; (b) a clean "Set N detects k× more than baselines" if the extra k is driven by N members (rho_train_inf, rho_mono) whose bugs no baseline even has a ctx adapter for — that is coverage breadth, which should be stated as such, not as detection-power dominance on a shared bug set; (c) using rho_train_rev's `not_applicable` as if Set N had 5 working MRs.
- **Two fix_needed items gate validity:** until rho_adj's default contract is made transpose-symmetric and set_M_metric's perm_equivariant+index branch is fixed, rho_adj can false-positive (inflating N) and Set M can false-negative (deflating M). Both bias H4 and must be fixed before counting.

## (4) What the author must still wire

- **rho_adj (FIX, blocking):** replace `_weighted_contract` default with a trace-like / transpose-symmetric contraction so the paper's `Tr A` invariant holds for the `B(x1,x2)=outer(a,b)` vs `outer(b,a)` transpose case; current default false-positives on correct CG/tensor-product code.
- **set_M_metric (FIX, blocking):** in the perm branch, when `has_index and 'perm_equivariant' in props`, run the lockstep-(src,index) invariance check (or return `not_applicable`) instead of falling through to a vacuous `held`; otherwise order-dependent buggy scatter is silently passed. Secondary: guard integer-dtype truncation under c=0.5 scaling (low priority for float e3nn/PyG ops).
- **ctx adapters per bug class (required for fired/held, else `not_applicable`):**
  - rho_rot / L_rot / B-rotation: `ctx['x']`, `ctx['rotate']`, and `ctx['equivariant_out']` (or `out_transform`) for covariant e3nn ops; without `equivariant_out` an equivariant op degrades to an invariance check and may mis-hold/mis-fire.
  - rho_mono: `ctx['add_redundant']` / `ctx['drop_redundant']` defining "redundant" for the op.
  - rho_train_inf / B-idempotency: `ctx['idempotent']` flag to enable the true `fn(fn(x))==fn(x)` check (otherwise only determinism+purity runs).
  - rho_adj: two-argument bilinear callable signature so role-swap `B(x1,x2)` vs `B(x2,x1)` is defined; unary ops correctly return `not_applicable`.
  - set_L_llm L_scale: `ctx['scale_degree']` to opt into the deviating homogeneity reformulation (default `not_applicable`).
  - set_M_metric: `ctx['metric_props']` declaring which D×R categories the op claims (perm_invariant / perm_equivariant / scale degree / additive-shift / negation), plus `ctx['index']` for scatter cases.
- **Per-bug applicability ledger:** record for each B1 bug, per set, whether each MR returned held/fired/not_applicable, so denominators (§3) are auditable and the cross-set rotation overlap is visible.
- **Set G:** no wiring possible inside `mr(fn,ctx,tol)`; if a Set-G arm is genuinely wanted, it must be an external offline GenMorph tool-run per SUT (out of scope for the CPU-only contract) — otherwise leave it recorded as not_applicable / not evaluable.
