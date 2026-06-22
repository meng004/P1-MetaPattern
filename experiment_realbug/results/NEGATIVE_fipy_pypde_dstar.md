# Negative companions to the Clawpack family-g (𝒟\*) positive: FiPy and py-pde

> Recorded alongside the **positive** `bug_clawpack_tvd2_recon_bounds.json` (the
> first in-the-wild family-g / 𝒟\* witness: PyClaw SharpClaw TVD2 reconstruction
> loop-bound fix `1cb1e0c` / PR #407). While probing for that positive I also
> swept two other pure-Python PDE libraries with the same 𝒟\* vocabulary; both
> came up empty for a *released, right-direction* no-overshoot fix. They are
> documented here so the search is auditable and the positive's framing
> (substrate-bearing vs substrate-free) is grounded.

The family-g invariant (Mode I): `Z(Φx) ≤ Z(x)` — a TVD / shape-preserving scheme
applied to a monotone (or shock) input must not gain spurious extrema / overshoot
(`Z` = #local-extrema / #sign-changes).

---

## 1. FiPy (usnistgov/fipy) — has the substrate, but the only *released* limiter fix is wrong-direction

**Clone:** `git clone --filter=blob:none https://github.com/usnistgov/fipy /tmp/g_fipy`
(HEAD `64635bf8`, 5708 commits, tags 1.2.2 … 4.0.3). FiPy is a pure-Python
finite-volume PDE solver and **does** carry a flux-limited convection substrate:
`VanLeerConvectionTerm`, plus `minmod`/`superbee`/`MUSCL` machinery and a Roe
solver. Empirically (FiPy 4.0.3, pip, Python 3.11) the substrate genuinely
enforces the 𝒟\* invariant — advecting a monotone step (periodic, Co=0.2):

| scheme | min | max | overshoot | undershoot | spurious extrema | TV ratio | verdict |
|---|---|---|---|---|---|---|---|
| Upwind / ExplicitUpwind / PowerLaw | 0.0000 | 1.0000 | 0 | 0 | 0 | 2.0 | HELD |
| **VanLeer (TVD)** | −0.0000 | 1.0000 | 0 | 9.1e-26 | 0 | 2.0 | HELD |
| CentralDifference (non-TVD) | **−0.1104** | **1.1104** | **0.110** | **0.110** | **81** | 6.05 | FIRED |

So FiPy is a real shape-preserving substrate (unlike SciPy). **But its only
modern, released convection-limiter bug-fix is accuracy-not-shape, in the wrong
direction:**

- **`a1dd901d`** "Correcting issues in Van Leer raised by Jason Furtney"
  (ticket:564 / GitHub issue **#377** *"VanLeerConvectionTerm MinMod slope limiter
  is broken"*), first released in **FiPy 3.1** (parent `0c8a5a63` in the 3.0.1
  line). One-line slope-limiter change:
  - PRE : `min3 = min(|a|, |b|, avg)`  with `avg = ½(|a|+|b|)` → since
    `min(|a|,|b|,avg) = min(|a|,|b|)` this is **MinMod**, a TVD-safe,
    *over-diffusive* limiter.
  - POST: `min3 = min(2|a|, 2|b|, avg)` → the **true Van Leer / monotonized-central
    (MC)** limiter, *less* diffusive / *sharper*.

  Reconstructing **both** limiter formulas verbatim from the `a1dd901d` diff and
  advecting the same monotone step shows **zero overshoot on BOTH sides** (PRE
  overshoot = 0, POST overshoot = 0; both TVD). The fix makes the scheme sharper
  (an accuracy refinement), the **opposite** of the family-g signature (which
  needs PRE = overshoots, POST = clean). This is the FiPy analogue of SciPy's
  PCHIP slope/endslope fixes: a shape-preserving scheme whose fixes change
  accuracy, never restore a shape guarantee.

- **`55071cea`** "Fixed bug in the MC limiter function that broke the rotation
  example … the acoustics example is now broken" — a genuinely oscillation-flavoured
  Roe / MC-limiter fix, **but it lives only on the unmerged `remotes/origin/riemann`
  branch and was NEVER released** (`roeConvectionTerm.py` and
  `examples/riemann/{acoustics,rotation}.py` are **not on HEAD**; no release tag
  contains it). No released-to-released bracket exists.

- **`5912c03c`** (2005) the original `faceTerm.py` VanLeer fix uses Python-2
  `weave` C-inline — unbuildable on Python 3.11.

CHANGELOG confirmation: `docs/source/CHANGELOG.rst` line 948 lists issue #377
"VanLeerConvectionTerm MinMod slope limiter is broken" (the `a1dd901d` accuracy
fix); no released entry mentions an overshoot/oscillation *restoration*.

**Verdict:** FiPy has the 𝒟\* substrate (VanLeer HELD, CentralDifference FIRED),
but no *released* fix witnesses the no-overshoot invariant in the FIRED→HELD
direction. Empirical demonstration:
`results/fipy_repro/repro_fipy_vanleer_no_shape_break.py` (Part A: invariant is
real; Part B: the `a1dd901d` PRE and POST are both clean).

---

## 2. py-pde (zwicker-group/py-pde) — no flux-limiter substrate at all

**Clone:** `git clone --filter=blob:none https://github.com/zwicker-group/py-pde /tmp/g_pypde`
(HEAD `db06281`, 1751 commits). Pure-Python finite-difference / spectral PDE.
𝒟\* vocabulary archaeology (separate `-i -E` flags) returns **no substrate**:

| term | hits | what they are |
|---|---|---|
| `overshoot\|undershoot` | 0 | — |
| `limiter` | 0 | — |
| `TVD\|total.?variation` | 0 | — |
| `upwind` | 0 | — |
| `oscillat` | 0 | — |
| `flux` | 1 | `afe944b` — a *no-flux boundary condition* bug (Neumann BC), not a limiter |
| `monoton` | 1 | `db8344a` — "Skip plotting frames when update is too fast" (plotting, not shape) |
| `positiv` | 3 | all `lgtm.com` false-positive linter suppressions |

py-pde uses central-difference / spectral discretisations with no slope/flux
limiter, so it has no monotonicity guarantee to break — the prototypical 𝒟\*
defect has no place to occur. Same structural reason as SciPy.

---

## 3. Other pure-Python candidates swept (all not 𝒟\* witnesses)

| lib | finding |
|---|---|
| **econforge `interpolation`** (2.2.7) | 0 monoton/overshoot/limiter hits; its `hermite` spline is plain (not monotone). No shape guarantee. |
| **`scikit-fdiff` / `skfdiff`** (0.7.0) | "upwind" is a *symbolic finite-difference stencil* substitution in its compiler (`fix upwind` = stencil/sign bug), **no TVD/limiter/monotonicity guarantee** to violate. |
| **`interpax`** (0.3.14, JAX) | has monotonic splines, but its fixes are reverse-mode-AD (`2a4fcd5`) and nd-array-broadcasting (`340fe2b`) bugs — not a forward no-overshoot violation; the monotonic method is, like PCHIP, monotone-by-construction. JAX is also a heavy dependency. |
| **`weno4` (Goobley)** | one fix `bfbd69d` (Ngrid≤3 + numba uninitialised-memory) — an edge-case/memory bug, not an oscillation restoration. |

---

## Conclusion

Family g (𝒟\*, `O≤.dyn`) is **non-empty in the wild** — witnessed by the Clawpack
PyClaw SharpClaw TVD2 reconstruction loop-bound fix (`bug_clawpack_tvd2_recon_bounds.json`,
the right-direction positive this search was after). Among the *other* pure-Python
PDE/interpolation libraries probed, none yields a *released, right-direction*
no-overshoot fix: FiPy has the substrate but its released limiter fix is
accuracy-not-shape (and its oscillatory Roe fix was never released); py-pde,
econforge-interpolation, scikit-fdiff, interpax and weno4 either lack a TVD/limiter
substrate or carry only AD/array-shape/memory edge-case fixes. This matches and
extends the SciPy 𝒟\* negative (`NEGATIVE_scipy_dstar.md`): shape-preserving
schemes are constructively non-oscillatory, so a 𝒟\* positive requires a genuine
hyperbolic flux-/slope-limiter substrate *and* a limiter/reconstruction bug that
actually breaks the guarantee — which Clawpack supplies and the others do not.
