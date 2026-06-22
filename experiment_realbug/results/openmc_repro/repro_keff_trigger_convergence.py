#!/usr/bin/env python
"""
NOETHER reactor_physics L* convergence block -- OpenMC eigenvalue trigger (convergence
criterion) score binding.

Target bug   : OpenMC commit b54de4d76 "Fix check for trigger score name (#3155)"
NOETHER block: L* convergence / limit operator (eigenvalue source-iteration convergence
               criterion -- the active-batch loop must keep iterating until the tallied
               quantity's statistical uncertainty falls below the trigger threshold).
Module       : src/tallies/tally.cpp  Tally::init_triggers (score <-> trigger binding)
Released pair: PRE = openmc 0.15.0  (fix NOT in v0.15.0)
               POST = openmc 0.15.3 (fix is v0.15.1~121, present in 0.15.1/0.15.2/0.15.3)

Root cause
----------
A `Trigger` declares a *convergence criterion*: with `settings.trigger_active = True`,
OpenMC runs additional active batches (in `trigger_batch_interval` steps, up to
`trigger_max_batches`) until the requested score's statistical uncertainty meets the
threshold. To enforce that, each trigger must be bound to a score INDEX on its tally.
The pre-fix binding in `init_triggers` was

    if (reaction_name(this->scores_[i_score]) == score_str)   # PRE  (v0.15.0)
        break;
    ...
    if (i_score == this->scores_.size())
        fatal_error("Could not find the score \"{}\" in tally {} ...", score_str, id_);

Here `scores_[i_score]` is an *integer score code*. For the particle-production scores
("He3-production", "H3-production", "H1-production", "He4-production"), that code is a
special SCORE constant (N_X3HE, N_XT, N_XP, N_XA), which `reaction_name(int)` does NOT
map back to the user's string (it returns "MT=<code>"). So the round-trip comparison
never matches even though the SAME score IS listed on the tally, and OpenMC aborts with
a fatal_error BEFORE any transport. The convergence criterion cannot be set up at all.

The fix compares the integer codes directly:

    if (this->scores_[i_score] == reaction_type(score_str))   # POST (v0.15.1+, b54de4d76)
        break;

`reaction_type("He3-production") == N_X3HE`, so the trigger binds and the convergence
loop runs.

Metamorphic relation (L* convergence)
-------------------------------------
A tally trigger is the discrete statement of an L* convergence criterion on the Monte
Carlo eigenvalue source iteration: starting from the minimum `batches`, the active-batch
loop must ITERATE (add batches) until rel_err(score) < threshold (a converged limit),
bounded by trigger_max_batches. Binding the trigger to its score is the precondition for
that limit operator to exist.

    FIRED <=> declaring a trigger on a *-production score makes setup crash
              (fatal_error: "Could not find the score ..."), so the convergence
              criterion is unenforceable (the L* limit operator cannot be formed).
    HELD  <=> the trigger binds; the active-batch loop iterates to convergence.

Domain anchoring
----------------
A bare U235 metal sphere (Godiva-like fast assembly), continuous-energy ENDF/B-VIII.0,
eigenvalue mode -- the canonical reactor-physics criticality problem. Triggers are the
standard OpenMC mechanism for "run until k_eff (or a reaction rate) is converged to a
target precision", i.e. the eigenvalue solver's convergence criterion in testable form.

The crash path (init_triggers XML parse) is deterministic and library-data-independent;
the fission-rate convergence demonstration (POST) shows the limit operator actually
iterating (15 -> N batches until rel_err < threshold).

Usage:
    micromamba run -n omc_pre  python repro_keff_trigger_convergence.py   # PRE  0.15.0
    micromamba run -n omc      python repro_keff_trigger_convergence.py   # POST 0.15.3

Requires CE data at $OPENMC_CROSS_SECTIONS (defaults to /tmp/ce_data/cross_sections.xml,
the U235 ENDF/B-VIII.0 library built by build_u235_ce_data.py for the IFP repro).
"""
import os
import sys
import tempfile

import openmc

CROSS_SECTIONS = os.environ.get(
    "OPENMC_CROSS_SECTIONS", "/tmp/ce_data/cross_sections.xml"
)

# The production scores whose integer code does NOT round-trip through reaction_name()
# -> a trigger on them crashes init_triggers in PRE (v0.15.0). Same score listed on the
# tally itself is fine; only the trigger->score binding is broken.
AFFECTED_SCORE = "He3-production"
# A control score that DOES round-trip (so its trigger binds in both versions).
CONTROL_SCORE = "fission"


def _build_model(score, threshold, min_batches, max_batches):
    os.environ["OPENMC_CROSS_SECTIONS"] = CROSS_SECTIONS
    mat = openmc.Material(name="u235")
    mat.add_nuclide("U235", 1.0)
    mat.set_density("g/cm3", 18.0)  # Godiva-like fast metal
    mats = openmc.Materials([mat])
    mats.cross_sections = CROSS_SECTIONS

    sph = openmc.Sphere(r=8.0, boundary_type="vacuum")
    geom = openmc.Geometry([openmc.Cell(fill=mat, region=-sph)])

    s = openmc.Settings()
    s.run_mode = "eigenvalue"
    s.particles = 300
    s.batches = min_batches
    s.inactive = 5
    s.seed = 1
    s.trigger_active = True          # turn ON the convergence criterion
    s.trigger_batch_interval = 5
    s.trigger_max_batches = max_batches

    tally = openmc.Tally(name="t")
    tally.scores = [score]
    trig = openmc.Trigger(trigger_type="rel_err", threshold=threshold)
    trig.scores = [score]            # bind the convergence criterion to this score
    tally.triggers = [trig]

    return openmc.Model(geom, mats, s, openmc.Tallies([tally]))


def _run(model):
    """Return (ran, n_batches, rel_err, err). ran=False on crash."""
    d = tempfile.mkdtemp()
    cwd = os.getcwd()
    os.chdir(d)
    try:
        sp_path = model.run(output=False)
        with openmc.StatePoint(sp_path) as sp:
            n_batches = sp.n_realizations + sp.n_inactive
            tal = sp.get_tally(name="t")
            mean = float(tal.mean.ravel()[0])
            std = float(tal.std_dev.ravel()[0])
            rel = std / mean if mean else float("inf")
        return True, n_batches, rel, None
    except Exception as e:  # noqa: BLE001
        return False, None, None, f"{type(e).__name__}: {str(e).splitlines()[0][:140]}"
    finally:
        os.chdir(cwd)


def main():
    print(f"openmc {openmc.__version__}")

    # (1) The affected score: trigger binding is the L* convergence criterion.
    ran, nb, rel, err = _run(
        _build_model(AFFECTED_SCORE, threshold=0.2, min_batches=15, max_batches=40)
    )
    if not ran:
        print(
            f"[{AFFECTED_SCORE}] VERDICT=FIRED  -- convergence criterion UNENFORCEABLE: {err}"
        )
        affected_verdict = "FIRED"
    else:
        print(
            f"[{AFFECTED_SCORE}] VERDICT=HELD   -- trigger bound, convergence loop ran "
            f"{nb} batches (rel_err={rel:.5f})"
        )
        affected_verdict = "HELD"

    # (2) Control score (fission): trigger binds in BOTH versions; with a tight
    #     threshold the active-batch loop must ITERATE past the 15-batch minimum
    #     until rel_err < threshold -- the L* limit operator in action.
    ran_c, nb_c, rel_c, err_c = _run(
        _build_model(CONTROL_SCORE, threshold=0.01, min_batches=15, max_batches=80)
    )
    if ran_c:
        print(
            f"[{CONTROL_SCORE}]    convergence loop: 15 -> {nb_c} batches until "
            f"rel_err={rel_c:.5f} < 0.01 (L* limit reached)"
        )
    else:
        print(f"[{CONTROL_SCORE}]    crash: {err_c}")

    # Summary verdict for this NOETHER L* block.
    print(
        f"NOETHER-L* VERDICT={affected_verdict}  "
        f"(PRE 0.15.0 expected FIRED / POST 0.15.3 expected HELD)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
