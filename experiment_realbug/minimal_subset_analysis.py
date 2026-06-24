#!/usr/bin/env python3
"""
Minimal-detecting-subset / family-necessity analysis for the NOETHER B1 corpus
(task C). Data-driven from the curated corpus (COVERAGE_SUMMARY.md s1 fault list
+ s6 FIRED-type breakdown + the two new structure-present positives diffrax/e and
clawpack/g). No re-runs: this computes the NECESSITY structure that the existing
FIRED/HELD records already determine.

What this CAN establish rigorously from the recorded detections:
  (1) the set-cover minimal detecting subset under the recorded (one-family-per-
      fault) assignment, and
  (2) for each family, whether its necessity rests on a genuine *non-crash*
      law-violation witness (numeric / convergence / transport) or only on a
      crash that a generic smoke test would also surface.
What it CANNOT (honest limit): true pairwise orthogonality -- whether family X's
MR ALSO fires on family Y's fault -- which needs the full cross-detection matrix
(every family MR x every fault), i.e. rebuilding the torn-down per-fault library
environments. That remains future work.

FIRED-type categories: crash | numeric | convergence | transport.
A fault is a DISCRIMINATING witness for its family iff its type is non-crash.
"""

# (fault_id, family, mode, fired_type, note)
# Provenance: COVERAGE_SUMMARY.md table s1 (faults 1-21) + s6 type split,
# plus the two additional structure-present libraries (e<-diffrax, g<-clawpack).
CORPUS = [
    ("scipy.solve_ivp_lsoda",      "h", "I", "crash",       "event root-find"),
    ("scipy.ode_banded_jac",       "j", "M", "crash",       "dimension"),
    ("scipy.eigh_driver",          "c", "M", "crash",       "lwork"),
    ("scipy.complexsym_solve",     "c", "M", "numeric",     "max|X@a-I|=9.11"),
    ("pyscf.smearing_count",       "b", "I", "numeric",     "14 vs 13 electrons"),
    ("pyscf.diis_symm",            "h", "I", "convergence", "0/5 -> 5/5"),
    ("openmc.surface_normalize",   "a", "I", "numeric",     "sign loss"),
    ("openmc.no_reduce_mpi",       "j", "M", "numeric",     "bias 1/n_ranks"),
    ("openmc.rotperiodic_bc",      "a", "I", "transport",   "lost particles"),
    ("deepxde.neumann_robin",      "b", "I", "crash",       "residual not constructible"),
    ("deepxde.periodic_point",     "a", "I", "crash",       "symmetry map not constructible"),
    ("pyscf.d2h_orbsym",           "a", "I", "numeric",     "1/6 orientations agree"),
    ("scipy.akima_linear2pt",      "f", "I", "numeric",     "I(0.5)=1.25 != 1.0"),
    ("openmc.ifp_adjoint",         "d", "M", "numeric",     "beta_eff 687->499 pcm"),
    ("deepxde.train_next_batch",   "h", "I", "convergence", "5 -> 0 resample"),
    ("openmc.cram_clip",           "f", "I", "numeric",     "min N=-5.8e-2 -> 0"),
    ("scipy.fht_hermitian",        "a", "I", "numeric",     "marginal (signal edge)"),
    ("openmc.tally_trigger",       "h", "I", "crash",       "score round-trip"),
    ("deepxde.boundary_float32",   "f", "I", "numeric",     "boundary point dropout"),
    ("deepxde.forward_hessian",    "c", "I", "numeric",     "J-col 6.185 (reachability caveat)"),
    ("scipy.simpson_even_order",   "i", "M", "numeric",     "observed order 4->3"),
    # --- two additional structure-present libraries (task A) ---
    ("diffrax.srk_backward",       "e", "I", "numeric",     "round-trip ~0.67 flat (NEW)"),
    ("clawpack.tvd2_recon",        "g", "I", "numeric",     "spurious extremum Z 1->0 (NEW)"),
]

ALL_FAMILIES = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
NONCRASH = {"numeric", "convergence", "transport"}

def main():
    by_fam = {f: [] for f in ALL_FAMILIES}
    for fid, fam, mode, typ, note in CORPUS:
        by_fam[fam].append((fid, mode, typ, note))

    print("=" * 78)
    print("MINIMAL-DETECTING-SUBSET / FAMILY-NECESSITY ANALYSIS (NOETHER B1, n=%d)" % len(CORPUS))
    print("=" * 78)
    print("\nPer-family witnesses (* = discriminating non-crash witness):\n")
    hdr = "%-4s %-7s %-10s %s" % ("fam", "#faults", "#non-crash", "witnesses")
    print(hdr); print("-" * 78)
    necessary, thin, crash_only = [], [], []
    for fam in ALL_FAMILIES:
        faults = by_fam[fam]
        nonc = [x for x in faults if x[2] in NONCRASH]
        tag = lambda x: ("*" if x[2] in NONCRASH else " ") + x[0] + "[" + x[2][:4] + "]"
        print("%-4s %-7d %-10d %s" % (fam, len(faults), len(nonc),
              ", ".join(tag(x) for x in faults)))
        if len(nonc) >= 1:
            necessary.append(fam)
        if len(nonc) == 1:
            thin.append(fam)
        if len(faults) >= 1 and len(nonc) == 0:
            crash_only.append(fam)
    print("-" * 78)

    # set cover under the recorded (one-family-per-fault) partition
    covered = {fid for fid, *_ in CORPUS}
    populated = [f for f in ALL_FAMILIES if by_fam[f]]

    print("\nRESULT")
    print("  Populated families                     : %d / 10  (%s)" %
          (len(populated), ",".join(populated)))
    print("  Families w/ >=1 NON-CRASH witness      : %d / 10  (%s)" %
          (len(necessary), ",".join(necessary)))
    print("  Families resting ONLY on a crash       : %d  (%s)" %
          (len(crash_only), ",".join(crash_only) or "none"))
    print("  Families on a SINGLE non-crash witness : %d  (%s)" %
          (len(thin), ",".join(thin)))
    print("  Faults covered                         : %d / %d" % (len(covered), len(CORPUS)))
    print()
    print("  Minimal detecting subset (set cover, under the recorded")
    print("  one-family-per-fault partition)        : ALL %d populated families" % len(populated))
    print("  -> every populated family is necessary (removing it drops the")
    print("     fault(s) assigned only to it).")
    print()
    print("  Discriminating necessity: %d/10 families carry a non-crash witness," % len(necessary))
    print("  so NO family's necessity rests on crash-type faults alone")
    print("  (directly answers the paper's '6 of 21 are crash-type' threat).")
    print()
    print("HONEST LIMIT: true pairwise orthogonality (does family X's MR also fire")
    print("on family Y's fault?) needs the full cross-detection matrix -- every")
    print("family MR x every fault -- i.e. rebuilding the per-fault library")
    print("environments. Not run here; remains future work. This analysis")
    print("establishes NECESSITY (lower bound), not non-redundancy beyond the")
    print("recorded partition.")

if __name__ == "__main__":
    main()
