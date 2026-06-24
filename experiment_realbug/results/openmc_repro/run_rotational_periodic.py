#!/usr/bin/env python
"""Driver: run the rotational-periodic G-symmetry MR on the SOURCE-BUILT PRE and
POST OpenMC kernels and emit results/bug_openmc_rotperiodic.json.

Target bug : OpenMC c7d7fa461 "Fix a bug in rotational periodic boundary
             conditions (#3692)". First appears at v0.15.4-dev31; NOT in any
             tagged release -> no conda post-binary -> both PRE (parent
             818fd11b1) and POST (c7d7fa461) are built FROM SOURCE.

The MR (G-symmetry / rotational equivalence) is defined in
repro_rotational_periodic.py: the four sign-flip representations of the SAME
6-fold rotational-periodic wedge must give the same k_eff.

This driver invokes that repro twice (once per source-built kernel, selected by
OPENMC_BIN) in the omc_src conda env, parses the FIRED/HELD verdict + per-flip
k_eff, and writes the bug_json. It assumes the two kernels have already been
built (see BUILD_NOTE below); it does not itself compile.

BUILD_NOTE (reproduce the binaries)
-----------------------------------
  export MAMBA_ROOT_PREFIX=/tmp/mamba
  micromamba create -n omc_src -c conda-forge cmake ninja gxx_linux-64 \
      gcc_linux-64 hdf5 openmpi eigen fmt pugixml xtensor xtl gsl libpng \
      python=3.11 numpy h5py scipy pandas lxml matplotlib
  micromamba run -n omc_src pip install uncertainties endf
  git -C /tmp/openmc_git worktree add --detach /tmp/omc_post  c7d7fa461
  git -C /tmp/openmc_git worktree add --detach /tmp/omc_pre_wt c7d7fa461~1
  # in each worktree: fetch vendored submodules, then
  cmake -G Ninja -S . -B build -DCMAKE_BUILD_TYPE=Release -DOPENMC_USE_MPI=ON \
        -DOPENMC_BUILD_TESTS=OFF -DOPENMC_FORCE_VENDORED_LIBS=ON -DGIT_SUBMODULE=OFF
  cmake --build build -j
  # POST python API (fix touches no .py): pip install -e . --no-deps --no-build-isolation
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPRO = os.path.join(HERE, "repro_rotational_periodic.py")
RESULTS_DIR = os.path.abspath(os.path.join(HERE, ".."))
OUT_JSON = os.path.join(RESULTS_DIR, "bug_openmc_rotperiodic.json")

# Source-built kernels (override via env if rebuilt elsewhere).
PRE_BIN = os.environ.get("OPENMC_PRE_BIN", "/tmp/omc_pre_wt/build/bin/openmc")
POST_BIN = os.environ.get("OPENMC_POST_BIN", "/tmp/omc_post/build/bin/openmc")
PY = os.environ.get("OMC_SRC_PYTHON", "/tmp/mamba/envs/omc_src/bin/python")
LIBDIR = os.environ.get("OMC_SRC_LIB", "/tmp/mamba/envs/omc_src/lib")

FIX_COMMIT = "c7d7fa461"
PARENT_COMMIT = "818fd11b1"


def run_kernel(openmc_bin):
    """Run the repro with the given source-built kernel; return (rc, stdout)."""
    env = dict(os.environ)
    env["OPENMC_BIN"] = openmc_bin
    env["LD_LIBRARY_PATH"] = LIBDIR + ":" + env.get("LD_LIBRARY_PATH", "")
    proc = subprocess.run([PY, REPRO], env=env, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def parse(out):
    """Extract verdict, per-flip k_eff, and failed reps from repro stdout."""
    fired = "FIRED" in out and "HELD" not in out.split("NOETHER")[-1]
    held = "HELD (MR satisfied" in out
    kmap = {}
    for m in re.finditer(
            r"k_eff\(flip1=(\w+)\s*,\s*flip2=(\w+)\s*\)\s*=\s*([\d.]+)\s*\+/-\s*([\d.]+)",
            out):
        f1 = m.group(1) == "True"
        f2 = m.group(2) == "True"
        kmap[f"{f1}-{f2}"] = [float(m.group(3)), float(m.group(4))]
    failed = []
    mfail = re.search(r"transport-failed reps\s*=\s*\[(.*?)\]", out)
    if mfail:
        for pair in re.finditer(r"\((\w+),\s*(\w+)\)", mfail.group(1)):
            failed.append(f"{pair.group(1)=='True'}-{pair.group(2)=='True'}")
    return held, fired, kmap, failed


def main():
    for name, b in (("PRE", PRE_BIN), ("POST", POST_BIN)):
        if not os.path.exists(b):
            sys.exit(f"ERROR: {name} kernel not found at {b} (build it first; see BUILD_NOTE)")

    print(f"=== PRE kernel  ({PARENT_COMMIT}) : {PRE_BIN} ===")
    rc_pre, out_pre = run_kernel(PRE_BIN)
    print(out_pre)
    print(f"=== POST kernel ({FIX_COMMIT}) : {POST_BIN} ===")
    rc_post, out_post = run_kernel(POST_BIN)
    print(out_post)

    held_pre, fired_pre, kpre, failed_pre = parse(out_pre)
    held_post, fired_post, kpost, failed_post = parse(out_post)

    # Sanity: PRE must FIRE (rc 1), POST must HELD (rc 0).
    assert rc_pre == 1 and fired_pre, f"expected PRE FIRED, got rc={rc_pre}"
    assert rc_post == 0 and held_post, f"expected POST HELD, got rc={rc_post}"

    bug = {
        "id": "openmc_rotational_periodic",
        "repo": "openmc-dev/openmc",
        "domain": "paper SUT domain (reactor_physics: OpenMC)",
        "sut_family": "RotationalPeriodicBC (rotational periodic boundary "
                      "conditions) -- 2-group multi-group eigenvalue transport "
                      "on a 6-fold rotational-periodic wedge",
        "cat": "G symmetry (rotational geometric-equivalence invariance)",
        "fix_commit": FIX_COMMIT,
        "parent_commit": PARENT_COMMIT,
        "pre_version": "0.15.4-dev30 (source-built, parent 818fd11b1)",
        "post_version": "0.15.4-dev31 (source-built, fix c7d7fa461)",
        "tolerance": 5.0e-3,
        "cpu_status": "OK (SOURCE-BUILT pre/post via micromamba omc_src; "
                      "MPI/OpenMP; multi-group XS; no CE nuclear data)",
        "build": "FROM SOURCE -- fix is UNRELEASED (v0.15.4-dev31, no conda "
                 "post-binary). PRE=parent 818fd11b1, POST=c7d7fa461; both "
                 "cmake+ninja Release, vendored libs, fix touches only C++ "
                 "(Python API identical pre/post, verified by diff).",
        "fired_pre": {"N": None, "M": None, "G": bool(fired_pre),
                      "L": None, "B": None},
        "fired_post": {"N": None, "M": None, "G": bool(fired_post),
                       "L": None, "B": None},
        "k_eff_pre": kpre,
        "k_eff_post": kpost,
        "pre_failed_reps": failed_pre,
        "mr_used": "k_eff(flip1,flip2) == k_eff(False,False) for all (flip1,"
                   "flip2) in {False,True}^2: the four algebraically-opposite "
                   "sign conventions of the two periodic bounding planes "
                   "describe the IDENTICAL rotational-periodic wedge, so the "
                   "eigenvalue must be invariant to the plane sense.",
        "fired_type": "TRANSPORT FAILURE under sign-flip (NOT a crash in setup): "
                      "pre, the mixed-sign reps (False,True) and (True,False) hit "
                      "'Maximum number of lost particles' because the rotational-"
                      "periodic BC does not map particles across the boundary for "
                      "the flipped plane sense; (False,False) and (True,True) run "
                      "and agree at k=1.527569. post, all four reps run and agree "
                      "at k=1.527569. On byte-identical input XML the PRE kernel "
                      "aborts (exit 255, lost particles) while the POST kernel "
                      "gives Combined k-eff=1.52757 -- the C++ BC fix is the only "
                      "difference.",
        "verified": "SELF-RUN source-built: PRE 818fd11b1 FIRED (exit 1; reps "
                    "(False,True)/(True,False) lose all particles) / POST "
                    "c7d7fa461 HELD (exit 0; all four reps k=1.527569). Also "
                    "confirmed by running both kernels on identical exported XML.",
        "upstream": "gh-3692",
        "note": "reactor_physics 3rd block (G-symmetry, rotational). Fix rewrites "
                "RotationalPeriodicBC: signed angle atan2((n1 x n2).a, n1.n2) with "
                "surface signs folded in via copysign, plus flip_sense_ = "
                "(i_sign*j_sign>0) to flip the partner surface sense; "
                "handle_particle no longer branches on which surface was struck. "
                "Geometry ported from OpenMC's own fix-commit regression test "
                "tests/regression_tests/periodic_6fold/test.py (which asserts all "
                "four flip cases give the same k-combined), instantiated in "
                "2-group multi-group (shared build_two_group_mgxs with sibling "
                "reactor_physics repros) since no CE nuclear data is available. "
                "Distinct from the conda-reproducible openmc blocks: "
                "Surface.normalize (3bf1486f4, G geometry-canonicalization) and "
                "no_reduce tally (bd76fc056, conservation/MPI); this one is the "
                "rotational-BC transport bug whose fix is unreleased.",
    }

    with open(OUT_JSON, "w") as f:
        json.dump(bug, f, indent=2)
    print(f"\nWROTE {OUT_JSON}")
    print(f"  PRE  : rc={rc_pre}  G-FIRED={fired_pre}  failed_reps={failed_pre}")
    print(f"  POST : rc={rc_post} G-HELD={held_post}")


if __name__ == "__main__":
    main()
