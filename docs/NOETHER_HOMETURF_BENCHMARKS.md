# NOETHER home-turf benchmark candidates (thermal 热工 / fluid 流体)

Purpose: broaden the §6.6 argument's **representativeness** by testing NOETHER on
its theorized home turf — programs governed by **explicit physical/engineering
equations whose operators carry algebraic structure** (symmetry, conservation,
scaling, monotonicity, limiting cases, inverse, equivalent formulations). The
GenMorph benchmark under-samples this domain; these candidates restore it.

Status: candidate list (no implementation yet). Selection of concrete SUTs from
`meng004/Minimum-MR-SubSet` is pending repo access (see SUBMISSION_READINESS /
chat). The criteria below apply to both that repo's SUTs and these equations.

---

## A. Selection criteria for a "usable" NOETHER-favorable SUT

A candidate is usable iff it satisfies all of:

1. **Deterministic single method**, numeric/array I/O (primitive or `[]`/`String`)
   → compatible with the existing `.methodinputs` + PITest harness.
2. **Governed by an explicit equation** with algebraic operators (not opaque
   control-flow utility code).
3. **Admits ≥3 independent NOETHER MRs** from distinct algebra blocks
   (so the comparison isn't a single-relation artifact).
4. **PIT-mutable arithmetic/logic** (operators to mutate → a meaningful mutant set).
5. **Range-bounded or relative-tolerance-friendly** outputs, OR partial domain
   explicitly known (so MR encoding uses relative tolerance + domain guards —
   the fix flagged in SUBMISSION_READINESS G1).

## B. Metric to add — the GenMorph-favorable-scenario advantage

Even where GenMorph detects more, NOETHER wins on **cost to first valid MR**:

| metric | Set N (NOETHER) | Set G (GenMorph) |
|---|---|---|
| MR derivation | deterministic, **<1 s** (algebra → DSL) | GAssert search **~30 min × 4 MRIPs/subject** (+ EvoSuite + Major) |
| reliability of obtaining *any* valid MR | always | **seed lottery** — 0 valid MRs in a single run for 6/13 Lang+Guava subjects; 0/12 seeds for `indexOf`,`sort` |
| interpretability | named algebraic law (e.g. `gcd` permutation) | opaque evolved predicate |
| determinism / reproducibility | exact | seed-dependent |

→ Add `time_to_first_valid_mr` and `mr_derivation_seconds` columns to the results
(cheap: GenMorph generation wall-clock is already in its logs; Set N is ~0).
This supports the §6.6 claim *in the GenMorph-favorable scenario itself*.

---

## C. Thermal engineering (热工) candidates

For each: governing equation · NOETHER MR blocks · example MRs · why GP struggles.

| # | SUT (method) | Equation | NOETHER blocks → example MRs |
|---|---|---|---|
| T1 | `fourierConduction(k,A,dT,dx)` | q = −k·A·ΔT/Δx | **scale** (2·ΔT→2·q; 2·A→2·q) · **sign/symmetry** (−ΔT→−q) · **limit** (ΔT=0→q=0) · **inverse** (q ∝ 1/Δx) |
| T2 | `lmtd(dT1,dT2)` | ΔT_lm=(ΔT1−ΔT2)/ln(ΔT1/ΔT2) | **G permutation** (swap ΔT1,ΔT2→same) · **O bounds** (min≤LMTD≤max) · **L limit** (ΔT1→ΔT2 ⇒ LMTD→ΔT1) · **scale** |
| T3 | `effectivenessNTU(NTU,Cr)` | ε=f(NTU,Cr) | **O monotone** (↑NTU⇒↑ε) · **O bounds** ([0,1]) · **L limit** (NTU→∞) · **E** (vs LMTD method) |
| T4 | `newtonCooling(T0,Tinf,h,A,m,c,t)` | T=T∞+(T0−T∞)e^(−hA t/mc) | **D decay/monotone** · **L limit** (t→∞⇒T→T∞) · **scale** · **sign** (T0↔T∞) |
| T5 | `stefanBoltzmann(eps,A,T1,T2)` | q=εσA(T1⁴−T2⁴) | **G antisymmetry** (swap T1,T2⇒−q) · **scale** (T⁴ law) · **L** (T1=T2⇒q=0) · **O monotone** |
| T6 | `thermalResistanceSeries(r[])` / `parallel(r[])` | R=Σrᵢ / 1/R=Σ1/rᵢ | **G permutation+associativity** (reorder r[]→same) · **O monotone** (add R⇒↑) · **E** (series vs parallel duality) · **I inverse** |
| T7 | `carnotEfficiency(Tc,Th)` | η=1−Tc/Th | **O monotone** (↑Th⇒↑η; ↑Tc⇒↓η) · **O bounds** ([0,1)) · **L** (Tc→0⇒η→1) · **scale** (Tc,Th×λ⇒same η) |
| T8 | `idealGas(P,V,n,T)` (solve any var) | PV=nRT | **I inverse** (P↔1/V at fixed T) · **scale** · **L** (Boyle/Charles limits) · **E** (different solved-for forms agree) |
| T9 | `finEfficiency(h,P,k,Ac,L)` | η=tanh(mL)/(mL) | **O monotone** · **L** (L→0⇒η→1) · **scale** · **bounds** |
| T10 | `radHeatExchangerLMTDcorrection(...)` / `antoineSatPressure(A,B,C,T)` | Antoine: log P=A−B/(C+T) | **O monotone** (↑T⇒↑P) · **L** · **inverse** (T↔P) · **E** (vs Clausius–Clapeyron) |

## D. Fluid mechanics (流体) candidates

| # | SUT (method) | Equation | NOETHER blocks → example MRs |
|---|---|---|---|
| F1 | `bernoulli(P,rho,v,g,h)` | P+½ρv²+ρgh = const | **conservation** (along streamline) · **datum invariance** (shift h ref⇒same) · **scale** · **G** |
| F2 | `continuity(A1,v1,A2)` → v2 | A1v1=A2v2 | **I inverse** (A↔1/v) · **scale** · **G permutation** (sections) |
| F3 | `reynolds(rho,v,D,mu)` | Re=ρvD/μ | **scale** (per variable) · **dimensionless invariance** (ρ,v,D,μ×λ patterns) · **O monotone** |
| F4 | `darcyWeisbach(f,L,D,v,g)` | h_f=f(L/D)(v²/2g) | **scale** (v² law; L linear) · **I** (∝1/D) · **L** (v=0⇒h_f=0) · **O monotone** |
| F5 | `hagenPoiseuille(dP,r,mu,L)` | Q=πΔP r⁴/(8μL) | **scale** (r⁴ law!) · **linear** (ΔP) · **I inverse** (1/μ,1/L) · **E** (vs Darcy laminar) |
| F6 | `colebrookFriction(Re,eps_D)` (implicit) | 1/√f=−2log(ε/D/3.7+2.51/(Re√f)) | **O monotone** (↑roughness⇒↑f; ↑Re⇒↓f) · **L** (smooth-pipe limit) · **bounds** · **E** (vs Haaland/Swamee–Jain) |
| F7 | `dragForce(rho,v,Cd,A)` | F=½ρv²Cd A | **scale** (v² law; A linear) · **L** (v=0⇒F=0) · **O monotone** · **G** |
| F8 | `orificeFlow(Cd,A,dP,rho)` | Q=Cd·A√(2ΔP/ρ) | **scale** (√ΔP; √(1/ρ)) · **I** · **O monotone** · **L** (ΔP=0⇒Q=0) |
| F9 | `pumpAffinity(Q1,H1,P1,N1,N2)` | Q∝N, H∝N², P∝N³ | **scale (power laws — ideal for the scaling block)** · **O monotone** · **E** (3 coupled laws consistent) |
| F10 | `hydrostatic(rho,g,h)` / `machNumber(v,a)` / `froude(v,g,L)` | P=ρgh ; M=v/a ; Fr=v/√(gL) | **linear/scale** · **L** (h=0⇒P=0) · **O monotone** · **dimensionless invariance** |

---

## E. NOETHER algebra-block coverage (representativeness check)

| Block | thermal | fluid |
|---|---|---|
| G symmetry/permutation | T2,T5,T6 | F1,F2,F7 |
| O order/monotonicity/bounds | T3,T7,T9 | F3,F4,F6,F8 |
| scale / dimensional | T1,T5,T7 | F3,F4,F5,F9,F10 |
| L limit/closure | T2,T3,T4,T7 | F4,F6,F8,F10 |
| E equivalence/method-comparison | T3,T8,T10 | F5,F6,F9 |
| I inverse | T1,T6,T8 | F2,F4,F5,F8 |
| D dynamics | T4 | (transient F variants) |
| T* self-adjoint/time-reversal | T6 (network duality), reversible cycles | F1 (reversible streamline) |

Every block is exercised → far better block coverage than the GenMorph
benchmark, where Set N's blocks frequently degrade to FP-prone transcendental
encodings.

## F. Recommended first wave (implement ~8 for a balanced result)

Strong, easy-to-encode, multi-MR, clearly GP-hard:
**T2 (LMTD), T5 (Stefan–Boltzmann), T6 (resistance network), T7 (Carnot),
F2 (continuity), F4 (Darcy–Weisbach), F5 (Hagen–Poiseuille), F9 (pump affinity).**
These span all 8 blocks, are exact/relative-tolerance-friendly, and have obvious
permutation/scaling/limit MRs that a GP search rarely discovers cleanly.

## G. Why these favor NOETHER (and challenge GenMorph)

- Continuous real-valued, multi-argument I/O with **conservation/scaling/symmetry
  laws** that follow from the physics — NOETHER derives them directly; GenMorph's
  GP must rediscover them from sampled data and often can't (cf. its 0-valid-MR
  runs on structurally-rich subjects).
- Relations are **exact under relative tolerance** (ratios, power laws,
  permutations) — avoiding the absolute-tolerance failure mode seen on the
  transcendental GenMorph-Math subjects.
- Implementable as the same single-method numeric SUTs the pipeline already
  handles (Java; or a Python harness variant if the source SUTs are Python).

## H. Implementation note

If the selected SUTs are **Java** they slot into the current pipeline directly
(add to a `*-sut` config). If they are **Python** (e.g. from the
`Minimum-MR-SubSet` workspace), either (a) port the handful of equation methods
to a small Java SUT, or (b) add a parallel Python scoring harness reusing
`mutmut`/`cosmic-ray` for mutation + the same union-kill/Wilson/McNemar
comparator. Decision deferred until the source SUTs are inspected.
