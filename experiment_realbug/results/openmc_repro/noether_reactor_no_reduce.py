"""
NOETHER reactor_physics conservation block -- OpenMC tally normalization with no_reduce.
Fix: bd76fc056 "Fix bug in normalization of tally results with no_reduce (#3619)" (v0.15.3)
Bug: tally norm used total_source/(n_particles*gen) always; with no_reduce it must use
     contributing_particles = work_per_rank. Under MPI with >1 rank, no_reduce tallies
     were normalized by the FULL particle count instead of per-rank work -> wrong by ~n_ranks.

MR (conservation / method-invariance): the SAME fixed-source problem must give the SAME
normalized flux whether or not tallies are MPI-reduced:
    flux(no_reduce=True, mpi=2) == flux(no_reduce=False, mpi=2)
Single-rank shows no difference (work_per_rank==n_particles); the bug is an MPI-multi-rank
normalization error, so we drive it with mpiexec -n 2.
"""
import sys, tempfile
import numpy as np
import openmc


def build_mgxs(path="/tmp/mgxs_nr.h5"):
    groups = openmc.mgxs.EnergyGroups([0., 0.625, 2.0e7])
    xs = openmc.XSdata("fuel", groups)
    xs.order = 0
    xs.set_total([1.0, 1.5])
    xs.set_absorption([5.0e-3, 8.0e-2])
    xs.set_scatter_matrix(np.array([[[0.92, 0.075], [0.0, 1.40]]]).reshape(2, 2, 1))
    xs.set_fission([2.0e-3, 5.0e-2])
    xs.set_nu_fission([5.0e-3, 1.25e-1])
    xs.set_chi([1.0, 0.0])
    lib = openmc.MGXSLibrary(groups)
    lib.add_xsdata(xs)
    lib.export_to_hdf5(path)
    return path


def run(no_reduce):
    path = build_mgxs()
    fuel = openmc.Material(name="fuel")
    fuel.set_density("macro", 1.0)
    fuel.add_macroscopic("fuel")
    mats = openmc.Materials([fuel]); mats.cross_sections = path
    L = 0.63
    xmin = openmc.XPlane(-L, boundary_type="vacuum"); xmax = openmc.XPlane(+L, boundary_type="vacuum")
    ymin = openmc.YPlane(-L, boundary_type="vacuum"); ymax = openmc.YPlane(+L, boundary_type="vacuum")
    zmin = openmc.ZPlane(-L, boundary_type="reflective"); zmax = openmc.ZPlane(+L, boundary_type="reflective")
    cell = openmc.Cell(fill=fuel, region=+xmin & -xmax & +ymin & -ymax & +zmin & -zmax)
    geom = openmc.Geometry([cell])
    s = openmc.Settings()
    s.energy_mode = "multi-group"
    s.run_mode = "fixed source"
    s.particles = 2000
    s.batches = 10
    s.no_reduce = no_reduce
    s.source = openmc.IndependentSource(space=openmc.stats.Box([-L, -L, -L], [L, L, L]))
    s.output = {"summary": False, "tallies": False}
    t = openmc.Tally(name="flux")
    t.filters = [openmc.CellFilter([cell])]
    t.scores = ["flux"]
    model = openmc.Model(geometry=geom, materials=mats, settings=s, tallies=openmc.Tallies([t]))
    cwd = tempfile.mkdtemp(prefix=f"nr_{no_reduce}_")
    import os
    mpiexec = os.path.join(os.path.dirname(sys.executable), "mpiexec")
    sp_path = model.run(cwd=cwd, output=False,
                        mpi_args=[mpiexec, "--allow-run-as-root", "--oversubscribe", "-n", "2"])
    with openmc.StatePoint(sp_path) as sp:
        flux = float(sp.get_tally(name="flux").mean.ravel()[0])
    return flux


if __name__ == "__main__":
    print("openmc", openmc.__version__)
    f_nr = run(True)
    f_rd = run(False)
    rel = abs(f_nr - f_rd) / abs(f_rd) if f_rd else float("inf")
    print(f"  flux(no_reduce=True, mpi2)  = {f_nr:.6e}")
    print(f"  flux(no_reduce=False, mpi2) = {f_rd:.6e}")
    print(f"  rel_diff = {rel:.3e}")
    verdict = "FIRED (no_reduce changes normalized flux -> conservation/method-invariance broken)" if rel > 1e-6 else "HELD (consistent)"
    print(f"NOETHER conservation MR : {verdict}")
    sys.exit(1 if rel > 1e-6 else 0)
