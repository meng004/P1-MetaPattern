#!/usr/bin/env python3
"""
Build the rater hand-out bundle `noether_rater_packet.zip` from the committed
source files. The zip is tracked in git (per request); regenerate after changes with:

    python3 build_rater_packet.py

The packet contains ONLY rater-facing materials. The answer key
(_gold_author_labels.csv) and coordinator scripts (compute_kappa.py,
make_items.py, this script) are deliberately excluded; the build asserts they
never leak in.
"""
import os, zipfile, pathlib

HERE = pathlib.Path(__file__).parent
# Minimal set for time-limited raters: read (PDF) + classify (CODEBOOK) + record
# (xlsx dropdown) + how-to (GUIDE). Redundant duplicates are deliberately excluded
# from the packet: items_to_rate.csv (same items as the PDF), items_raw.csv
# (raw-Java traceability, coordinator-only), rating_sheet_TEMPLATE.csv (CSV copy of
# the xlsx). Those source files stay in the repo for the coordinator.
RATER_FILES = ["RATER_GUIDE.md", "CODEBOOK.md", "items_to_rate.pdf", "rating_sheet_TEMPLATE.xlsx"]
FORBIDDEN = {"_gold_author_labels.csv", "compute_kappa.py", "make_rater_materials.py", "build_rater_packet.py"}
OUT = HERE / "noether_rater_packet.zip"

def main():
    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for f in RATER_FILES:
            src = HERE / f
            assert src.exists(), "missing source file: " + f
            z.write(src, arcname="noether_rater_packet/" + f)
    names = zipfile.ZipFile(OUT).namelist()
    leak = [n for n in names if os.path.basename(n) in FORBIDDEN]
    assert not leak, "FORBIDDEN file leaked into packet: %s" % leak
    print("built %s (%d bytes) with:" % (OUT.name, OUT.stat().st_size))
    for n in names:
        print("  ", n)
    print("answer key / scripts excluded: OK")

if __name__ == "__main__":
    main()
