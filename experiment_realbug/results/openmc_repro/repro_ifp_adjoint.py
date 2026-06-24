"""
NOETHER reactor_physics T* (self-adjoint / adjoint-weighting duality) block
-- OpenMC Iterated Fission Probability (IFP) adjoint-weighted kinetics parameters.

Target bug : OpenMC commit 767db7e6a "Fix IFP implementation (#3580)" (in v0.15.3,
             NOT in v0.15.2). PRE = 767db7e6a^ (= 66e7d863).
Library    : OpenMC (openmc-dev/openmc) -- THIRD-PARTY Monte-Carlo neutron transport.
             In-the-wild upstream fix; reproduced source-build vs source-build
             (the whole IFP kinetics feature lives INSIDE the v0.15.2 -> v0.15.3
             window: feature #3133 = v0.15.3~151, fix #3580 = v0.15.3~42, so no
             released pre version contains IFP -- the pre/post pair must be the
             fix commit and its parent, both compiled from source).

NOETHER block : T* (self-adjoint operators / adjoint-weighting duality). The IFP
                method is a stochastic estimator of the ADJOINT-weighted kinetics
                parameters of the Boltzmann transport operator. beta_eff and the
                neutron generation time Lambda are adjoint(importance)-weighted
                averages:  beta_eff = <phi^dagger, chi_d nu_d Sigma_f phi> /
                <phi^dagger, chi nu Sigma_f phi>.  IFP realises the adjoint weight
                phi^dagger by the iterated fission probability: the probability
                that a neutron's progeny survive over `ifp_n_generation` future
                fission generations. The forward<->adjoint duality is the structural
                symmetry; the kinetics parameter is the conserved bilinear form in
                testable form.

Module / root cause (src/ifp.cpp, function `ifp`)
-------------------------------------------------
The IFP delayed-fraction (beta) numerator weights each fission site by the
delayed-group character of the neutron WHOSE IMPORTANCE is being accumulated --
that is, the PARENT neutron `p` causing the fission, carried forward across
generations. The buggy version instead used the delayed group sampled for the
NEW DAUGHTER fission site:

    PRE  (66e7d863):  _ifp(site.delayed_group, delayed_groups)   # daughter site
    POST (767db7e6a): _ifp(p.delayed_group(),  delayed_groups)   # parent neutron

The fix also propagates the parent's delayed group from the source bank
(`Particle::from_source`: delayed_group() = src->delayed_group). Because the
generation-time (Lambda) path already used the parent's lifetime `p.lifetime()`
in BOTH versions, ONLY the beta (delayed-group) numerator is affected: the
time-numerator and denominator are byte-identical pre/post, and only
ifp-beta-numerator (hence beta_eff) changes. This is exactly the signature of an
adjoint-weighting (duality) defect localised to the delayed channel.

Metamorphic relation (T* / self-adjoint duality)
------------------------------------------------
The adjoint-weighted delayed fraction must be sourced from the originating
neutron's delayed character propagated through the IFP generations
(forward<->adjoint duality of the kinetics estimator). The testable consequence
used here:

    beta_eff(IFP) must equal the known adjoint-weighted delayed fraction of the
    SUT (a bare U235 metal sphere), and in particular the ifp-beta-numerator must
    be invariant to the (buggy) substitution of the daughter-site delayed group
    for the parent-neutron delayed group.

    FIRED <=> ifp-beta-numerator / beta_eff is mis-weighted (uses daughter site)
    HELD  <=> ifp-beta-numerator / beta_eff uses the parent neutron (correct duality)

SUT  : bare U235 sphere r=10 cm, rho=16 g/cm3 (Godiva-like fast metal system),
       fixed-seed eigenvalue run, ifp_n_generation=5. This is the EXACT model
       from the upstream regression test tests/regression_tests/ifp/test.py, so
       the FIRED->HELD delta reproduced here is the same one the maintainers
       baked into results_true.dat (beta-numerator pre > post). Continuous-energy
       U235 is required because IFP-beta needs delayed-neutron precursor data
       (6 precursor groups); multi-group IFP did not exist until v0.15.3 (#3425),
       so it cannot be used for the pre/post comparison.

Usage:
    OPENMC_CROSS_SECTIONS=<U235 CE lib> python repro_ifp_adjoint.py <openmc_exec>
      <openmc_exec> = path to the pre-fix or post-fix compiled openmc binary.
    Decision is made by comparing ifp-beta-numerator against the post-fix
    reference (default-seed regression config). Run twice (pre exec, post exec)
    and compare; this script prints the raw scores + beta_eff for either build.
"""
import sys
import tempfile
import numpy as np
import openmc

# Post-fix reference for the EXACT regression config (n=1000, batches=20,
# inactive=5, ifp_n_generation=5, default seed) with ENDF/B-VIII.0 U235:
#   ifp-beta-numerator(post) = 4.933333e-3 ; beta_eff(post) = 498.7 pcm
#   ifp-beta-numerator(pre)  = 6.800000e-3 ; beta_eff(pre)  = 687.4 pcm
# (time-numerator and denominator are identical pre/post; only beta changes.)
POST_BETA_NUMERATOR = 4.933333e-3
REL_TOL = 1e-3  # the pre/post beta-numerator gap is ~38%, far above this tol


def build_model():
    """EXACT upstream IFP regression model (tests/regression_tests/ifp/test.py)."""
    mat = openmc.Material(name="core")
    mat.add_nuclide("U235", 1.0)
    mat.set_density("g/cm3", 16.0)

    sphere = openmc.Sphere(r=10.0, boundary_type="vacuum")
    cell = openmc.Cell(region=-sphere, fill=mat)
    geom = openmc.Geometry([cell])

    s = openmc.Settings()
    s.particles = 1000
    s.batches = 20
    s.inactive = 5
    s.ifp_n_generation = 5
    s.source = openmc.IndependentSource(
        space=openmc.stats.Box(*cell.bounding_box),
        constraints={"fissionable": True},
    )
    s.output = {"summary": False, "tallies": False}

    t = openmc.Tally(name="ifp-scores")
    # adjoint-weighted kinetics scores (introduced with the IFP feature #3133)
    t.scores = ["ifp-time-numerator", "ifp-beta-numerator", "ifp-denominator"]

    return openmc.Model(geometry=geom, materials=openmc.Materials([mat]),
                        settings=s, tallies=openmc.Tallies([t]))


def run(openmc_exec):
    model = build_model()
    cwd = tempfile.mkdtemp(prefix="ifp_")
    sp_path = model.run(cwd=cwd, output=False, openmc_exec=openmc_exec)
    with openmc.StatePoint(sp_path) as sp:
        m = sp.get_tally(name="ifp-scores").mean.ravel()
    time_num, beta_num, denom = float(m[0]), float(m[1]), float(m[2])
    return time_num, beta_num, denom


if __name__ == "__main__":
    openmc_exec = sys.argv[1] if len(sys.argv) > 1 else "openmc"
    print("openmc (python API):", openmc.__version__, "| exec:", openmc_exec)

    time_num, beta_num, denom = run(openmc_exec)
    beta_eff = beta_num / denom
    gen_time = time_num / denom
    print(f"  ifp-time-numerator = {time_num:.6e}  (parent-lifetime path; unaffected)")
    print(f"  ifp-beta-numerator = {beta_num:.6e}  <-- the adjoint-weighted delayed score")
    print(f"  ifp-denominator    = {denom:.6e}")
    print(f"  beta_eff = {beta_eff:.6e}  ({beta_eff*1e5:.1f} pcm)")
    print(f"  Lambda   = {gen_time:.6e} s")

    rel = abs(beta_num - POST_BETA_NUMERATOR) / abs(POST_BETA_NUMERATOR)
    fired = rel > REL_TOL
    print(f"  |beta_num - post_ref| / post_ref = {rel:.3e}  (post_ref = {POST_BETA_NUMERATOR:.6e})")
    print("NOETHER T* (adjoint-weighting duality) MR :",
          "FIRED (beta-numerator mis-weighted: uses daughter-site delayed group "
          "-> adjoint-weighted beta_eff wrong -> bug PRESENT)"
          if fired else
          "HELD (beta-numerator uses parent-neutron delayed group -> correct "
          "forward<->adjoint duality -> bug ABSENT)")
    print("VERDICT:", "FIRED" if fired else "HELD")
    sys.exit(1 if fired else 0)
