#!/usr/bin/env bash
# Fetch the third-party GenMorph replication package (Zenodo 10067096) needed to
# reproduce Route B. NOT vendored into the repo (size/licence); download here.
set -euo pipefail
GMROOT="${1:-/tmp/genmorph_pilot}"
mkdir -p "$GMROOT"; cd "$GMROOT"
for f in genmorph.zip mrs.zip evaluation.zip README.md; do
  echo "downloading $f ..."
  wget -q -O "$f" "https://zenodo.org/api/records/10067096/files/$f/content"
done
mkdir -p genmorph_full; cd genmorph_full
unzip -oq ../genmorph.zip                       # genmorph/ : SUT + prebuilt GAssert/Randoop/PIT jars
unzip -oq ../evaluation.zip -d eval_unpacked    # published Set G results (12 seeds)
unzip -oq ../mrs.zip       -d mrs_unpacked      # published Set G MR .jir/.jor
echo "OK: GenMorph package ready under $GMROOT/genmorph_full"
