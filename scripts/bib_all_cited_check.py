#!/usr/bin/env python3
"""scripts/bib_all_cited_check.py — Bib all-cited / all-defined gate (CLAUDE.md §11.2.1).

Pre-submission hard gate: every \\cite key in the manuscript must be defined in the
.bib, and every .bib entry must be cited at least once. Exits non-zero on any
mismatch so it can be wired into a pre-submission pipeline.

Usage:
  python3 scripts/bib_all_cited_check.py
  python3 scripts/bib_all_cited_check.py --tex NOETHER_paper_arxiv.tex --bib NOETHER_paper.bib
"""
import argparse
import re
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", default="NOETHER_paper_arxiv.tex")
    ap.add_argument("--bib", default="NOETHER_paper.bib")
    args = ap.parse_args()

    tex = Path(args.tex).read_text(encoding="utf-8")
    bib = Path(args.bib).read_text(encoding="utf-8")

    cited = set()
    for chunk in re.findall(r"\\cite[a-z]*\{([^}]+)\}", tex):
        for k in chunk.split(","):
            if k.strip():
                cited.add(k.strip())
    defined = set(re.findall(r"@\w+\{\s*([^,]+?)\s*,", bib))

    uncited = defined - cited
    undefined = cited - defined

    ok = not uncited and not undefined
    if undefined:
        print(f"FAIL: {len(undefined)} cite key(s) not defined in {args.bib}:")
        for k in sorted(undefined):
            print(f"  - {k}")
    if uncited:
        print(f"FAIL: {len(uncited)} bib entry(ies) never cited in {args.tex}:")
        for k in sorted(uncited):
            print(f"  - {k}")
    if ok:
        print(f"OK: {len(cited)} cited, {len(defined)} defined, all match.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
