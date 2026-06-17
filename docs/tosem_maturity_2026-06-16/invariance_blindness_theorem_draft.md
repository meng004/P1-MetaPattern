# DRAFT for author judgment — Invariance-Blindness Theorem (招1)

> Status: **DRAFT proposition + proof sketch + refutation conditions.** Not yet a
> committed theorem; not in paper body. Per author instruction "先起草命题再定".
> Marked **[需作者数学判断]** where the agent must not self-certify.
> Empirical backing already in hand: `supplementary/S10_noether_homefield/`
> (paired McNemar advdiff MR-battery vs neutral differential oracle).

---

## 0. Why this is the non-trivial theory core (vs Theorem 1)

Theorem 1 (closure under `Translate`) is **by-construction** — it states that the
construction does not drop what the construction can reach. It says nothing about
the world. The Invariance-Blindness Theorem (IBT) is a **limiting** result: it
characterizes, from the framework's own definitions, the faults an algebra-induced
MR **cannot** detect. It is non-tautological, falsifiable, and (per S10) confirmed.
It is the answer to "your theory is trivial."

---

## 1. Setup and notation (reusing paper §3.1)

- Program $P:\mathcal{X}\to\mathcal{Y}$ in family $\mathcal{F}$; algebra $\mathcal{A}_P$.
- Block $s\in\mathcal{D}(\mathcal{A}_P)$ carries a structure $T_s$:
  - $s=G$: a group action $g\cdot(-)$ on $\mathcal{X}$ with representation $\rho$ on $\mathcal{Y}$;
  - $s=O_\le$: a partial order $\le$ on inputs/outputs;
  - $s=T^*$: an inner-product duality $\langle L\,\cdot,\cdot\rangle=\langle\cdot,L\,\cdot\rangle$;
  - $s=\mathcal{T}^*_{\mathrm{rev}}$: a time-reversal involution;
  - $s=\mathcal{L}^*,\mathcal{D}^*,\mathcal{E}^*,\mathcal{B}^*_{\mathrm{rel}}$: limit / qualitative / method-comparison / rewrite structures.
- Algebra-induced MR $\rho_{\iota,s}=\texttt{Translate}(\iota,s)$ (paper Def. Translate)
  is a predicate $\Pi_s[P]$ asserting that $P$ **respects** $T_s$. E.g. for $s=G$:
  $$\Pi_G[P]\ :\quad P(g\cdot x)=\rho(g)\cdot P(x)\qquad\forall g\in T_s,\ \forall x.$$

**Fault model.** A fault is a perturbed program $\tilde P$ (a mutant). Write the
deviation $\delta=\tilde P\ominus P$ in the algebra (additive $\tilde P=P+\delta$,
or operator $\tilde P=D\circ P$ — the two are interchangeable for the statement).

**"Fault lives in the symmetry direction of $T_s$".** Define: $\tilde P$ is
**$T_s$-compatible** iff it satisfies the *same* structural identity that validates
$\rho_{\iota,s}$, i.e. $\Pi_s[\tilde P]$ holds. For $s=G$ this means $\delta$ is
itself $G$-equivariant: $\delta(g\cdot x)=\rho(g)\cdot\delta(x)$.

---

## 2. Proposition (Invariance-Blindness)

> **Proposition IBT (sufficient direction — provable now).**
> Let $\rho_{\iota,s}=\texttt{Translate}(\iota,s)$. If a fault $\tilde P$ is
> $T_s$-compatible (i.e. $\Pi_s[\tilde P]$ holds), then $\rho_{\iota,s}$ does **not**
> detect $\tilde P$: the MR passes on the mutant. Equivalently, the detection
> kernel
> $$\ker(\rho_{\iota,s})\ :=\ \{\,\tilde P:\ \rho_{\iota,s}(\tilde P)\ \text{holds}\,\}\ \supseteq\ \{\,\tilde P:\ \Pi_s[\tilde P]\,\}.$$

**Proof (sufficient direction).** $\rho_{\iota,s}(\tilde P)$ is, by Def. Translate,
exactly the assertion $\Pi_s[\tilde P]$. By hypothesis $\Pi_s[\tilde P]$ holds.
Hence $\rho_{\iota,s}(\tilde P)$ holds; the mutant survives. $\square$

> **Corollary IBT-1 (single-block incompleteness).** For any block $s$, the family
> $\{\rho_{\iota,s}\}_{\iota\in\mathcal{I}_s}$ cannot detect any fault that preserves
> $T_s$. A symmetry-based battery is therefore incomplete: its kernel contains the
> nontrivial set of $T_s$-compatible faults.

> **Corollary IBT-2 (joint-kernel completeness condition).** A family of oracles
> $\{O_j\}$ detects every nontrivial fault only if $\bigcap_j\ker(O_j)=\{P\}$
> (only the no-op survives all). Completeness thus requires oracles whose
> structural kernels jointly intersect trivially — *not* more MRs of the same
> symmetry class.

> **Corollary IBT-3 (differential oracle is the algebraic complement).** The
> neutral cross-implementation differential oracle $O_{\mathrm{diff}}$ has kernel
> $\ker(O_{\mathrm{diff}})=\{$faults that are **common-mode** across the two
> implementations (identical effect on both)$\}$. Since common-mode $\ne$
> $T_s$-compatible in general, $\ker(\rho_{\iota,s})\cap\ker(O_{\mathrm{diff}})$ is
> strictly smaller than either — the two oracles are complementary, and a fault
> escapes both only if it is *simultaneously* structure-preserving and common-mode.

---

## 3. Empirical confirmation already in hand (S10)

- **IBT / IBT-1 (symmetry block, advection).** The MR battery missed **every**
  advection-speed fault (`fv_adv_speed_x2`, `sp_adv_speed_x2`) and wavenumber-sign
  faults. These are exactly faults that preserve translation/Galilean equivariance
  (a uniform speed change keeps $P(g\cdot x)=\rho(g)P(x)$ form) — predicted blind,
  observed blind.
- **IBT-3 (complementarity).** Paired McNemar over the same 29 real mutants:
  MR-only $=6$, differential-only $=5$; differential-only is dominated by the
  speed / symbol-sign faults IBT predicts the MR battery misses, while MR-only is
  dominated by conservation/boundary faults that are common-mode (both impls fault
  identically) and so lie in $\ker(O_{\mathrm{diff}})$.
- **Joint kernel (IBT-2).** Self-consistent coefficient faults (`fv_lap_coeff_x2`,
  `*_coeff_half`) survive *both* oracles — they are both structure-preserving and
  (for a one-sided mutation, below the discretisation floor) effectively common-mode
  in signature. Predicted by IBT-2's "escapes both" set; observed.

### 3.1 Live multi-SUT confirmation (radxfer, grayscott executed here)

Differential oracles run **live** on three multi-implementation SUTs, paired against
the algebra-MR battery on the same real mutants (MR side: advdiff executed here;
radxfer/grayscott reused-committed; differential side always live):

| SUT | MR | diff | MR-only | diff-only | both | neither | union | McNemar $p$ |
|---|---|---|---|---|---|---|---|---|
| advdiff-2d | 13/29 | 12/29 | 6 | 5 | 7 | 11 | 18/29 | 1.0 |
| radxfer-G2 | 25/31 | 10/31 | 17 | 2 | 8 | 4 | 27/31 | 7.3e-4 |
| grayscott | 41/44 | 28/44 | 16 | 3 | 25 | **0** | **44/44** | 4.4e-3 |

- **IBT-3 (kernel $=$ common-mode), confirmed live on 3 SUTs.** The differential
  oracle misses exactly the faults patching operators SHARED by both
  implementations: radxfer absorption/scatter/source $0/18$; grayscott
  feed/reaction-rate $0/12$. Implementation-specific faults are detected: radxfer
  diffusion $8/8$, grayscott diffusion $15/15$ ($\delta_{\mathrm{radxfer}}=0.0017$,
  $\delta_{\mathrm{grayscott}}=1.1\!\times\!10^{-5}$; baselines survive both).
- **IBT-1 / diff-only $>0$ everywhere ($5/2/3$).** The neutral oracle catches faults
  the algebra-MR battery misses even where the battery has higher recall.
- **IBT-2 (union completeness), live.** On grayscott the two kernels intersect
  trivially: neither $=0$, union $=44/44$. The MR battery alone reaches $41/44$;
  the complementary-symmetry oracle closes the gap — the strongest available
  confirmation that completeness needs oracles with trivial joint kernel.
- Honest direction note: on radxfer/grayscott the MR battery has significantly
  higher raw recall ($p<0.01$); the claim is complementarity (different kernels,
  union approaches completeness), not differential superiority.

---

## 4. What is NOT yet proved — [需作者数学判断]

1. **Tightness (the "only if").** Proposition IBT gives $\ker\supseteq\{T_s\text{-compatible}\}$.
   Is it equality? A fault could survive $\rho_{\iota,s}$ for reasons other than
   $T_s$-compatibility (e.g. the executable test probes only finitely many $g$, or
   the deviation is non-equivariant but vanishes on the probed orbit). A tight
   characterization likely needs a **faithfulness/probing-completeness** hypothesis
   on the executable MR (the test exercises a generating set of $T_s$). **[需作者]**
   decide whether to (a) state only the sufficient direction (clean, weaker), or
   (b) add a faithfulness assumption and claim equality.
2. **Cross-block generalization.** §2 is cleanest for $s=G$. For $O_\le$ (order),
   $T^*$ (self-adjoint), $\mathcal{T}^*_{\mathrm{rev}}$ (time-reversal), the analogue
   "fault preserving the order / duality / reversal is invisible" must be stated
   per block and the deviation model ($\delta$ preserves $\le$? preserves
   $\langle\cdot,\cdot\rangle$-symmetry?) made precise. **[需作者]** confirm the
   structure-preservation predicate for each non-$G$ block.
3. **Kernel non-emptiness in general.** IBT-1's force depends on $\{T_s\text{-compatible
   faults}\}\ne\{P\}$ for the SUTs of interest. Provable per instance (exhibit one
   nontrivial compatible fault, e.g. equivariant coefficient rescale), but a
   *general* guarantee needs an argument that every nontrivial $T_s$ admits a
   nontrivial compatible deviation. **[需作者]**
4. **Relation to Composite-`Translate` (protocol_theory T2).** IBT-2 says
   completeness needs trivial joint kernel; Composite-`Translate` is one mechanism
   to enlarge reach. Whether IBT-2's completeness condition is *achievable* within
   a poly-time-decidable extension is the same open problem as T2. **[需作者]**

---

## 5. Refutation conditions (courage to be questioned)

- **Refute IBT:** exhibit an algebra-induced MR $\rho_{\iota,s}$ and a $T_s$-compatible
  fault $\tilde P$ that the MR *detects*. (Would break Def. Translate's semantics.)
- **Refute IBT-1:** exhibit a single-block battery that detects a structure-preserving
  fault — e.g. a Galilean-invariant MR flagging an advection-speed error.
- **Refute IBT-3:** show MR and differential detected-sets are nested (one $\subseteq$
  other) rather than crossing, on a SUT with one-sided mutations.

---

## 6. Drafting note for paper placement (pending招1 decision + P0)

If accepted: new subsection after CONSTRUCT-MP (proposed §3.4 in
`argument_architecture_plan.md`), stating Proposition IBT + Corollaries, with the
sufficient-direction proof in-text and the tightness/cross-block items either
(a) deferred to "open" or (b) proved by the author. Empirical confirmation goes to
§5.2 (L2). Do **not** write paper-body text until招1 is decided and the P0 math
judgments (tightness, per-block predicate) are returned.
