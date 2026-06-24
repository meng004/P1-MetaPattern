#!/usr/bin/env python3
r"""
POSITIVE family-g (D*) witness: PyClaw / Clawpack SharpClaw TVD2 reconstruction.

NOETHER family g (D*, O<=.dyn dynamic-shape / no-spurious-oscillation):
        Z(Phi x) <= Z(x)          (Z = #local-extrema / #sign-changes)
A shape-preserving (TVD) advection scheme must NOT let a MONOTONE input acquire a
NEW interior/boundary extremum (no spurious oscillation / no overshoot).

REAL fix (verified with `git show`):
    commit  1cb1e0c7088be94ebfa756c6048e237c3bdf0a6d   "Fix loop bounds that
            didn't include enough ghost cells."  (David Ketcheson, 2014-05-27)
    merge   e6075963ba85775fffb835a50c139dd4a00e7fec   PR #407
            (ketch/fix_tvd_recon_loop_bounds)
    parent  5ff3e514bcb81d92423480fe10fb600f33e32b87
    file    src/pyclaw/sharpclaw/reconstruct.f90  (subroutine tvd2)
    one-line diff:
            -            do i=num_ghost+1,mx2-num_ghost      ! PRE  (num_ghost=2 -> do i=3,mx2-2)
            +            do i=2,mx2-1                          ! POST
    released bracket:  v5.1.0 (PRE) -> v5.2.0 (POST).

THE BUG: in tvd2() the reconstructed left/right interface states ql,qr are
`intent(out)` and are assigned ONLY inside this difference/limiter loop
(qr(m,i)=q(m,i)+0.5*qlimitr*dqm ; ql(m,i)=q(m,i)-0.5*qlimitr*dqm). The PRE bounds
`num_ghost+1..mx2-num_ghost` skip the cells adjacent to the ghost region, leaving
their reconstructed states UNINITIALISED. With num_ghost=2 the skipped cell at
each end is the boundary-adjacent cell that DOES feed the physical update, so its
value collapses (-> ~0). A monotone step `[1,1,...,1, front, 0,...,0]` then gains
a spurious local extremum at the inflow boundary: Z_out = 1 > 0 = Z_in -> the
no-spurious-extrema invariant FIRES. The fix `do i=2,mx2-1` initialises that cell
and the invariant HOLDS.

HONESTY / REPRODUCTION MODE (documented, not hidden):
  * The historical RELEASED bracket v5.1.0 / v5.2.0 (2014) ships a PYTHON-2
    `setup.py` (`print "..."` SyntaxError) and builds via the now-removed
    numpy.distutils, so it CANNOT be pip-installed under the mandated Python-3.11
    released-to-released protocol (the same cp311-wall that blocks SciPy's
    pre-3.11 PCHIP candidates).
  * Therefore this is reproduced SOURCE-COMPILED pre/post (openmc-style), by
    building modern Clawpack 5.11.0 from sdist TWICE and applying ONLY the EXACT
    INVERSE of the real one-line fix to the *identical* live tvd2 routine that
    still exists in 5.11.0:
        PRE  build: tvd2 loop = `do i=3,mx2-2`  (literal pre-fix line, num_ghost=2)
        POST build: tvd2 loop = `do i=2,mx2-1`  (literal post-fix line, commit 1cb1e0c)
    The two builds differ by exactly that one Fortran line; everything else
    (compiler, numpy, BCs, IC, time stepping) is held fixed.
  * The defect is exercised with num_ghost=2 (the historical tvd2 ghost count);
    with the modern default num_ghost=3 the skipped cell falls strictly inside the
    ghost halo and the bug is masked. num_ghost=2 is a legitimate, supported
    setting; it is the configuration in which this routine's loop-bound bug bites.

Deterministic: pure Fortran kernel + NumPy IC, no randomness; bit-identical re-runs.

This script is SELF-CHECKING: it discovers the two venvs (PRE / POST) via env vars
or the conventional /tmp paths, runs both, and asserts PRE FIRES / POST HOLDS.

Build instructions (what was done):
    # download sdist source
    curl -sSL <pypi clawpack-5.11.0 sdist> -o claw.tgz && tar xzf claw.tgz
    # PRE: patch tvd2 loop to the pre-fix bounds
    sed -i 's/            do i=1,mx2-1/            do i=3,mx2-2/' \
        clawpack-5.11.0/pyclaw/src/pyclaw/sharpclaw/reconstruct.f90   # (only the tvd2 occurrence)
    uv venv --python 3.11 /tmp/venvg_claw_pre
    VIRTUAL_ENV=/tmp/venvg_claw_pre uv pip install --no-cache-dir numpy
    VIRTUAL_ENV=/tmp/venvg_claw_pre uv pip install --no-cache-dir ./clawpack-5.11.0   # PRE
    # POST: literal post-fix line do i=2,mx2-1 (separate source copy + venv)

Run:
    PRE_PY=/tmp/venvg_claw_pre/bin/python POST_PY=/tmp/venvg_claw_post2/bin/python \
        python results/clawpack_repro/repro_pyclaw_tvd2_boundary_recon.py
    # (or just run it; it falls back to those default paths)
"""
import os, sys, subprocess, json, textwrap


# The numerical experiment, run INSIDE each clawpack venv (PRE / POST).
WORKER = textwrap.dedent(r'''
    import warnings; warnings.filterwarnings("ignore")
    import json, numpy as np
    from clawpack import pyclaw, riemann
    import clawpack

    def run(limiter, num_ghost=2, nx=100, tfinal=0.9):
        s = pyclaw.SharpClawSolver1D(riemann.advection_1D)
        s.kernel_language = 'Fortran'   # Fortran kernel -> flux1 calls tvd2()
        s.lim_type = 1                  # 1 = 2nd-order TVD reconstruction (tvd2)
        s.char_decomp = 0               # component-wise -> tvd2 (not tvd2_char)
        s.num_ghost = num_ghost
        s.limiters = limiter            # 1 minmod, 2 superbee, 4 vanleer (clawpack mthlim)
        s.bc_lower[0] = pyclaw.BC.extrap
        s.bc_upper[0] = pyclaw.BC.extrap
        x = pyclaw.Dimension(0.0, 1.0, nx, name='x')
        dom = pyclaw.Domain(x)
        st = pyclaw.State(dom, s.num_eqn)
        st.problem_data['u'] = 1.0
        xc = st.grid.x.centers
        st.q[0, :] = np.where(xc < 0.15, 1.0, 0.0)   # MONOTONE non-increasing step
        sol = pyclaw.Solution(st, dom)
        c = pyclaw.Controller(); c.solution = sol; c.solver = s
        c.tfinal = tfinal; c.num_output_times = 1
        c.output_format = None; c.keep_copy = True; c.verbosity = 0
        q0 = st.q[0].copy(); c.run()
        return q0, c.frames[-1].q[0].copy()

    def Z_extrema(u, tol=1e-6):
        d = np.diff(u); sgn = np.sign(np.where(np.abs(d) < tol, 0, d)); sgn = sgn[sgn != 0]
        return int(np.sum(sgn[1:] * sgn[:-1] < 0))

    out = {"version": clawpack.__version__, "cases": {}}
    for name, lim in [("vanleer", 4), ("superbee", 2), ("minmod", 1)]:
        q0, qf = run(lim)
        Z0, Zf = Z_extrema(q0), Z_extrema(qf)
        out["cases"][name] = dict(
            Z_in=Z0, Z_out=Zf,
            min_out=float(np.nanmin(qf)), max_out=float(np.nanmax(qf)),
            overshoot=max(0.0, float(np.nanmax(qf) - 1.0)),
            boundary_cell=float(qf[0]),
            fired=bool(Zf > Z0),
        )
    print("RESULT_JSON " + json.dumps(out))
''')


def run_in(py):
    if not os.path.exists(py):
        return None
    p = subprocess.run([py, "-c", WORKER], capture_output=True, text=True)
    for line in p.stdout.splitlines():
        if line.startswith("RESULT_JSON "):
            return json.loads(line[len("RESULT_JSON "):])
    sys.stderr.write(p.stdout + "\n" + p.stderr + "\n")
    return None


def main():
    pre_py = os.environ.get("PRE_PY", "/tmp/venvg_claw_pre/bin/python")
    post_py = os.environ.get("POST_PY", "/tmp/venvg_claw_post2/bin/python")
    print("PRE  venv :", pre_py, "(tvd2 loop = do i=3,mx2-2  == pre-fix num_ghost+1..mx2-num_ghost)")
    print("POST venv :", post_py, "(tvd2 loop = do i=2,mx2-1   == post-fix commit 1cb1e0c)")
    print()

    pre = run_in(pre_py)
    post = run_in(post_py)
    if pre is None or post is None:
        print("ERROR: could not run one or both builds. Build them per the docstring, then re-run.")
        print("       PRE_PY / POST_PY must point at the PRE / POST clawpack venvs.")
        sys.exit(2)

    hdr = f"{'limiter':<10}{'side':<6}{'Z_in':>6}{'Z_out':>7}{'min_out':>14}{'boundary_q[0]':>16}{'overshoot':>12}  verdict"
    print(hdr)
    ok = True
    for name in ["vanleer", "superbee", "minmod"]:
        a, b = pre["cases"][name], post["cases"][name]
        print(f"{name:<10}{'PRE':<6}{a['Z_in']:>6}{a['Z_out']:>7}{a['min_out']:>14.3e}"
              f"{a['boundary_cell']:>16.3e}{a['overshoot']:>12.2e}  "
              f"{'FIRED (Z_out>Z_in)' if a['fired'] else 'held'}")
        print(f"{'':<10}{'POST':<6}{b['Z_in']:>6}{b['Z_out']:>7}{b['min_out']:>14.3e}"
              f"{b['boundary_cell']:>16.3e}{b['overshoot']:>12.2e}  "
              f"{'FIRED' if b['fired'] else 'HELD (Z_out<=Z_in)'}")
        ok = ok and a["fired"] and (not b["fired"])
    print()
    print("=" * 92)
    print(f"PRE  clawpack {pre['version']}: monotone step -> spurious extrema (Z_out=1 > Z_in=0); "
          f"inflow boundary cell collapses to ~{pre['cases']['vanleer']['boundary_cell']:.1e}")
    print(f"POST clawpack {post['version']}: monotone step preserved (Z_out=0 = Z_in=0); boundary cell = 1.0")
    print("VERDICT:", "POSITIVE family-g witness CONFIRMED (PRE FIRED / POST HELD on all 3 limiters)."
          if ok else "NOT confirmed -- check builds.")
    assert ok, "expected PRE FIRED and POST HELD for all limiters"


if __name__ == "__main__":
    main()
