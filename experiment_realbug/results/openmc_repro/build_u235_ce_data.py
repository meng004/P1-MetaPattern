"""
Helper: build the minimal continuous-energy nuclear-data library needed by the
IFP adjoint-weighting reproduction (repro_ifp_adjoint.py).

IFP beta_eff requires DELAYED-NEUTRON PRECURSOR data, which only continuous-energy
data carry (multi-group IFP did not exist until OpenMC v0.15.3 / PR #3425, so it
cannot be used for the v0.15.2 -> v0.15.3 pre/post comparison). The existing
multi-group helper build_two_group_mgxs (used by the conservation / G-symmetry
reproductions) is therefore insufficient for the T* IFP block, and a single
continuous-energy nuclide (U235, with its 6 delayed precursor groups) is built
from ENDF/B-VIII.0 via NJOY.

Steps:
  1. Download ENDF/B-VIII.0 U-235 (MAT=9228) from IAEA:
       https://www-nds.iaea.org/public/download-endf/ENDF-B-VIII.0/n/n_9228_92-U-235.zip
     unzip -> n_9228_92-U-235.dat
  2. Run this script (needs NJOY on PATH; openmc.data.IncidentNeutron.from_njoy):
       python build_u235_ce_data.py n_9228_92-U-235.dat /path/to/out
  3. Point OpenMC at the produced cross_sections.xml:
       export OPENMC_CROSS_SECTIONS=/path/to/out/cross_sections.xml

Single temperature (293.6 K) keeps NJOY processing to a few minutes.
The produced U235.h5 has MT=18 fission with 6 delayed-neutron precursor groups.
"""
import sys
import os
import time

import openmc.data


def main():
    endf = sys.argv[1] if len(sys.argv) > 1 else "n_9228_92-U-235.dat"
    outdir = sys.argv[2] if len(sys.argv) > 2 else "."
    os.makedirs(outdir, exist_ok=True)
    h5 = os.path.join(outdir, "U235.h5")
    xml = os.path.join(outdir, "cross_sections.xml")

    t0 = time.time()
    u235 = openmc.data.IncidentNeutron.from_njoy(
        endf, temperatures=[293.6], njoy_exec="njoy",
    )
    u235.export_to_hdf5(h5, "w")
    print(f"wrote {h5} in {time.time() - t0:.1f} s")

    lib = openmc.data.DataLibrary()
    lib.register_file(h5)
    lib.export_to_xml(xml)
    print(f"wrote {xml}")

    # sanity: confirm delayed-neutron data is present (required for IFP beta)
    u = openmc.data.IncidentNeutron.from_hdf5(h5)
    n_delayed = sum(
        1 for p in u[18].products if getattr(p, "emission_mode", None) == "delayed"
    )
    print(f"U235 MT=18 fission present; delayed precursor groups = {n_delayed}")


if __name__ == "__main__":
    main()
