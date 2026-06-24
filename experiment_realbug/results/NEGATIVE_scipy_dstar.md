# Negative result: SciPy 𝒟\* (O≤.dyn, family g — dynamic-shape / overshoot) is genuinely scarce

> Honest scarcity confirmation for the NOETHER **family g** (𝒟\*, `O≤.dyn`
> dynamic-shape) block in the `pde_numerical` (SciPy) domain — the *richest*
> domain for the order/positivity meta-pattern 𝔐_{O≤}. Family g is the
> **dynamic-shape** sibling of family f (`O≤.stat`, static pointwise
> monotonicity/positivity, already filled by `bug_scipy_akima_linear2pt.json`).
> The g invariant is `Z(Φx) ≤ Z(x)`: a solution/interpolant must not gain
> spurious shape structure — bounded oscillation, no overshoot beyond the data
> range `[min,max]`, non-increasing count of local extrema / sign-changes
> (Gibbs ringing, overshoot/undershoot, TVD/monotonicity-of-the-solution).

## Claim

There is **no** in-the-wild, fixed SciPy bug with a modern released-to-released
bracket (both endpoints carrying CPython-3.11 wheels, i.e. scipy ≥ 1.9.3) whose
fix **restores a dynamic-shape (𝒟\*) guarantee** — no overshoot / no spurious
extrema / no oscillation on monotone (or otherwise shape-constrained) data. Two
independent structural facts make family g empty in SciPy:

1. SciPy's **only** shape-*preserving* 1-D interpolant family is **PCHIP**
   (`PchipInterpolator` / `pchip_interpolate`), and PCHIP is **monotone by
   construction** — its slopes are a harmonic mean of *same-signed* secant
   slopes (Fritsch–Carlson), so the interpolant **cannot** overshoot or add an
   interior extremum on monotone data, *regardless* of the exact slope-pairing
   or endpoint recipe. Consequently the PCHIP "slope" bug-fixes that look like g
   candidates change **accuracy**, not **shape** (demonstrated below).
2. The one **non**-monotone-by-design interpolant whose shape genuinely *can*
   break — **Akima** — already has its dynamic-shape cell consumed by other
   families: the two-point case is `O≤.stat` (family **f**,
   `ef7437afc`, `bug_scipy_akima_linear2pt.json`) and the only modern Akima
   shape-region fix (`9930630d6`, #23019) is genuinely an **overflow**-robustness
   fix (its regression test is `test_no_overflow`, a jump near `√float_max`),
   already recorded weakly as `bug_scipy_akima_overflow.json` — not 𝒟\*.

SciPy is *not* a hyperbolic-PDE / conservation-law library: it has **no**
TVD / WENO / flux-limiter / slope-limiter solver substrate where Gibbs ringing
or overshoot is the natural failure mode. So the prototypical g defect has no
place to occur.

## Evidence (git archaeology on a full-history scipy clone)

Clone: `git clone --filter=blob:none https://github.com/scipy/scipy /tmp/scipy_g`
HEAD `8d4aa03a9` (Merge PR #25444), **37755 commits**, 187 `vX.Y.Z` release tags.

Method note: `git log` rejects the combined `-iE` flag
(`fatal: unrecognized argument: -iE`); flags must be separated as `-i -E`, and
`grep` alternation needs `-E`. Every count below was produced with the corrected
forms and genuinely returns the stated number.

| Search (𝒟\* vocabulary) | Command | Result |
|---|---|---|
| overshoot / undershoot | `git log --all -i -E --grep='overshoot|undershoot' --oneline` | **1** commit — `417532421 TST: add tests for PCHIP` (a *test*, no shape-bug fix) |
| shape-preserving | `git log --all -i -E --grep='shape.?preserv' --oneline` | **0** commits |
| Gibbs / ringing | `git log --all -i -E --grep='ringing|gibbs' --oneline` | **1** commit — `fbc67f509 Fix-up merge issues …` (unrelated `io` merge) |
| non-monotone | `git log --all -i -E --grep='non.?monoton' --oneline` | **0** commits |
| TVD / total variation | `git log --all -i -E --grep='TVD|total.?variation' --oneline` | **0** commits |
| spurious extrema / new extrema / wiggle | `git log --all -i -E --grep='wiggl|spurious.?extrem|new.?extrem' --oneline` | **0** commits |
| positivity/bound-preserving | `git log --all -i -E --grep='positivity.?preserv|bound.?preserv' --oneline` | **0** commits |
| oscillation | `git log --all -i -E --grep='oscillat' --oneline` | **2** commits (hyp2f1 transform; RBFInterpolator ENH) — neither a shape-bug fix |
| monotonic (BUG/FIX only) | `git log --all -i -E --grep='monoton' --oneline \| grep -icE 'bug\|fix'` | **2** commits — `0ec926145` (odeint repeated-`t` crash), `2bda1f4d0` (missing import) — neither a shape guarantee |
| flux-/slope-limiter | `git log --all -i -E --grep='ENO|WENO|flux.?limiter|slope.?limiter' --oneline` | **0** *solver* limiters (the 146 `limiter` hits are memory/iteration limiters) |

The only routine in SciPy that *enforces* monotonicity, `optimize.isotonic_regression`,
is **ENH-only** (`3a604534a` add pava + isotonic; `ed65b6754` remove copies) — no
shape-violation bug ever fixed.

## Candidates examined and rejected (real full SHAs from `git log`)

| Full SHA | First release | What it is | Why it is **not** family g (𝒟\*) |
|---|---|---|---|
| `b127884e79ef5f10e0ba6d0ec58ebd6a799a8878` | v0.17.0 | "make PCHIP slopes agree with the literature" (#5351) | **Accuracy, not shape.** Changes the interior slope pairing to match MATLAB/NAG/Fritsch–Carlson. PCHIP stays monotone *both* before and after (harmonic mean of same-signed slopes). Empirically HELD on monotone data for PRE *and* POST (see repro). Also pre-cp311 (v0.16→v0.17, 2015). |
| `2e60b7c8e58e62a8b2ea3bc6a8b132765d0d1d05` | v0.17.0 | "change the prescription for PCHIP endslopes" (#3453) | **Accuracy, not shape.** The PRE `_edge_case` returns `1/(1/m0+1/d1)` — a harmonic mean, hence *same sign as `m0` and smaller in magnitude*, i.e. already shape-safe; POST uses the larger Moler 3-point estimate *with* clamps. Both keep the curve monotone/in-range (repro). Pre-cp311. |
| `c488c7f7c99bb61c7cf90a33d49e9b383a0e740f` | v0.18.0 | "pchip should work for length-2 arrays" (#6223) | PCHIP analog of the already-used Akima two-point bug — a length-2 **construction** edge case (family **f** territory), and pre-cp311 (2016). |
| `9930630d65ad7167b02f10f750da91a5708ce844` | v1.17.0 | "Akima1DInterpolator: Identical Rearrangement Fixes" (#23019) | **Overflow**, not shape. Regression test is `test_no_overflow` (jump of `1e6·√float_max`); fixes the `m2=m3` / high-dynamic-range numerical path. Already recorded weakly as `bug_scipy_akima_overflow.json`. |
| `ef7437afc38b3b4f9d2263dc4394dcc2b4fb08c4` | v1.16.0 | "Akima … linear interpolant for `y.shape[0]==2`" (#22278) | Already used as the family **f** (`O≤.stat`) witness (`bug_scipy_akima_linear2pt.json`): two-point **static** linear/monotone shape-preservation, not the dynamic Z(·) invariant. |
| `d6930b26488cc79edfa6085eb067adbe0c8374ab` | v1.13.0 | "CubicSpline with periodic data" (#20054) | A NumPy **array-shape** (broadcasting for n=3 multidim) bug, not a *curve*-shape invariant; and `CubicSpline` is not shape-preserving anyway. |
| `9d88ff1739705d8c9f483eca014d6293d499c260` | v1.18.0 | "fix VODE Jacobian transposition" (#24934) | Closest *solution*-shape candidate (transposed Jacobian on the stiff Robertson problem), but its regression test checks **step count / `successful()`**, not a shape invariant, and it has **no released-to-released bracket** (PRE and POST both land in v1.18.0). The Robertson problem is already used for family **j** (`cb0538877`, banded vs full Jacobian). |

### cp311-wheel feasibility wall (why the clean conceptual candidates are unreproducible)

The required reproduction is `uv venv --python 3.11` + pip released-to-released. PyPI
wheel availability:

| scipy version | cp311 wheel |
|---|---|
| 0.16.1 / 0.17.0 / 0.17.1 / 0.18.1 / 1.1.0 / 1.5.4 / 1.7.3 | **No** |
| 1.9.3 / 1.11.4 / 1.15.2 / 1.15.3 / 1.16.0 (and later) | Yes |

The only *conceptually* PCHIP-shaped candidates (`b127884e7`, `2e60b7c8e`, `c488c7f7c`)
are all v0.16→v0.18 (2015–2016) — **no cp311 wheels** — so even if one *did* break the
shape invariant (it does not), it could not be reproduced under the mandated protocol.

## Empirical core (reproducible)

`results/scipy_repro/repro_pchip_slope_no_shape_break.py` reconstructs **both** the
pre-fix and post-fix PCHIP interior + endpoint slope formulas (verbatim from the
`b127884e7` and `2e60b7c8e` diffs) in pure NumPy, builds the resulting cubic Hermite
interpolant with the modern, *unrelated* `CubicHermiteSpline`, and measures the g
invariants (`non_monotone_steps`, `overshoot` beyond `[min,max]`, interior
`local_extrema`) on five monotone datasets. Output (deterministic across re-runs,
scipy 1.17.1 / numpy 2.4.6):

```
[convex_mono]  PRE/POST: non_monotone_steps=0  overshoot=0.0e+00  local_extrema=0  (shape held)
[concave_mono] PRE/POST: non_monotone_steps=0  overshoot~1.8e-15 local_extrema=0  (shape held)
[step_up]      PRE/POST: non_monotone_steps=0  overshoot=0.0e+00  local_extrema=0  (shape held)
[NAG_sigmoid]  PRE/POST: non_monotone_steps=0  overshoot=0.0e+00  local_extrema=0  (shape held)
[sharp_first]  PRE/POST: non_monotone_steps=0  overshoot~8.9e-16 local_extrema=0  (shape held)
VERDICT: NEGATIVE — PCHIP is monotone-by-construction; the slope/endslope fixes
         change ACCURACY, not SHAPE. These commits cannot witness family g.
```

Reproduce:
```bash
git clone --filter=blob:none https://github.com/scipy/scipy /tmp/scipy_g   # archaeology
uv venv --python 3.11 /tmp/venv_g
VIRTUAL_ENV=/tmp/venv_g uv pip install scipy numpy
cd experiment_realbug
/tmp/venv_g/bin/python results/scipy_repro/repro_pchip_slope_no_shape_break.py
```

## Why it is structurally absent (not just "we didn't find it")

1. **Family g distinct from f (the discriminating point).** Family f (`O≤.stat`)
   tests *static pointwise* order/positivity (value never negative, monotone data →
   monotone output at the nodes); family g (`O≤.dyn` = 𝒟\*) tests the *dynamic
   shape* of the whole curve (no overshoot between nodes, no new interior extrema,
   bounded oscillation). In SciPy the static cell is real and filled (Akima
   two-point, CRAM N≥0, boundary float32); the **dynamic** cell needs an interpolant
   or solver that is *allowed* to wiggle yet is *required* not to.
2. **PCHIP removes the failure mode by design.** The one shape-*preserving*
   interpolant cannot produce a 𝒟\* violation: its monotonicity is a theorem of the
   construction (harmonic mean over same-signed slopes), so every PCHIP bug ever
   fixed is either a crash/edge-case (length-2, all-zeros, complex dtype) or an
   *accuracy* refinement (slopes/endslopes) — never a shape-guarantee restoration.
3. **Akima's dynamic-shape cell is already spoken for.** Akima *is* free to
   overshoot, but its two recorded fixes map elsewhere: two-point linear → **f**
   (static), and the m2=m3 high-dynamic-range fix → **overflow** boundary. No
   *third* Akima fix restores a no-overshoot/no-extrema guarantee.
4. **No hyperbolic / conservation-law substrate.** `scipy.integrate` solves IVP/BVP
   for ODEs (Bateman-style decay, stiff Robertson) and quadrature; `scipy.signal`
   does LTI filtering. None integrate a hyperbolic PDE with a TVD/WENO/flux-limiter
   scheme, which is where Gibbs ringing / spurious extrema / TVD-monotonicity failure
   classically live. The 0 hits for `TVD`, `flux-limiter`, `shape-preserv`,
   `overshoot`(-as-bugfix) reflect this absence of substrate, not an incomplete search.

## Cross-domain corroboration (g is empty in every paper SUT domain)

Per the task escalation order (scipy richest → others only if scipy is clean), the
other three paper domains were swept for the same 𝒟\* vocabulary; all are barren:

| Domain (clone HEAD) | `overshoot\|undershoot` | `monoton` | `oscillat` | `ringing\|gibbs` | `TVD\|limiter` |
|---|---|---|---|---|---|
| openmc (`09ee8308d`) | 0 | 0 | 0 | 0 | 0 |
| deepxde (`b8d69c4`) | 0 | 0 | 0 | 0 | 0 |
| pyscf (`90777ccc`) | 0 | 0 | 4† | 0 | 0 |

† pyscf's 4 `oscillat` hits are *oscillator strengths* (TDSCF/ADC spectroscopy) and
"prevent oscillation in MCSCF optimization" — neither is a solution-shape MR. None is
a 𝒟\* witness. (openmc/deepxde transport/PINN solve forward stationary or
residual-minimisation problems with no shape-preserving-interpolant guarantee to
violate.)

## Conclusion

Family **g** (𝒟\*, `O≤.dyn` dynamic-shape) is **genuinely scarce in SciPy** — the
richest domain — for two reinforcing structural reasons: the only shape-preserving
interpolant (PCHIP) is monotone-by-construction so its fixes are accuracy-not-shape
(empirically demonstrated for both the pre- and post-fix slope formulas), and the
only interpolant that *can* break shape (Akima) has its cell already consumed by
families f (static two-point) and the overflow boundary. SciPy has no
TVD/WENO/flux-limiter solver substrate where overshoot/Gibbs is the natural defect.
The three other paper domains (openmc, deepxde, pyscf) corroborate with 0 genuine
hits. This is recorded as an honest negative result, consistent with CLAUDE.md's
"诚实优先于救援" and the existing `NEGATIVE_pyscf_o_le.md` / Trev\* scarcity notes.
The 𝒟\* (family g) cell of the coverage matrix therefore stays **gap** with a
documented structural reason, exactly as `i` (ℰ\* accuracy-order) does — both are
present-by-derivation, absent-by-instance.
