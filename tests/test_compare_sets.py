#!/usr/bin/env python3
"""tests/test_compare_sets.py — Set N vs Set G comparator (rule 6)."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import compare_sets as cs  # noqa: E402

HDR = "EXPERIMENT,MR,M1,M2,M3,M4,COUNT\n"

MATH_SETN = HDR + (
    "setn_seed11,rho_a,1,1,0,1,3\n"
    "setn_seed11,rho_b,1,0,0,0,1\n"
    "setn_seed11,*,1,1,0,1,3\n"
    "*,*,1,1,0,1,3\n")
MATH_SETG = HDR + (
    "assertions_seed11,MR0,1,0,1,0,2\n"
    "assertions_seed11,*,1,0,1,0,2\n"
    "assertions_seed12,MR0,1,1,1,1,4\n"
    "assertions_seed12,*,1,1,1,1,4\n"
    "*,*,1,1,1,1,4\n")
# Lang: Set G found NO valid MR at seed11 (only seed12) -> seed11 strict = 0
LANG_SETN = HDR + (
    "setn_seed11,rho_id,1,0,0,0,1\n"
    "setn_seed11,*,1,0,0,0,1\n"
    "*,*,1,0,0,0,1\n")
LANG_SETG = HDR + (
    "assertions_seed12,MR0,1,1,0,0,2\n"
    "assertions_seed12,*,1,1,0,0,2\n"
    "*,*,1,1,0,0,2\n")
# Guava: Set G present but NO Set N file (0 valid Set N MRs) -> N must record 0
GUAVA_SETG = HDR + (
    "assertions_seed11,MR0,1,1,1,0,3\n"
    "assertions_seed11,*,1,1,1,0,3\n"
    "*,*,1,1,1,0,3\n")


def main():
    # pure functions
    assert cs.mcnemar_exact_p(0, 0) == 1.0
    assert cs.wilson(0, 0) == [0.0, 0.0]
    lo, hi = cs.wilson(5, 10); assert lo < 0.5 < hi
    assert cs.mcnemar_exact_p(0, 6) < 0.05

    tmp = Path(tempfile.mkdtemp()); rdir = tmp / "seed11"
    for subj, sn, sg in (("MathClass?demo?0", MATH_SETN, MATH_SETG),
                         ("LangClass?demo?0", LANG_SETN, LANG_SETG)):
        d = rdir / subj; d.mkdir(parents=True)
        (d / "setn_mutants_killed.csv").write_text(sn)
        (d / "setg_mutants_killed.csv").write_text(sg)
    gd = rdir / "GuavaClass?demo?0"; gd.mkdir(parents=True)
    (gd / "setg_mutants_killed.csv").write_text(GUAVA_SETG)  # no setn file

    out = tmp / "cmp.json"
    subprocess.run([sys.executable, str(ROOT / "scripts" / "compare_sets.py"),
                    "--results-dir", str(rdir), "--seed", "11", "--output", str(out)],
                   check=True, capture_output=True)
    res = json.loads(out.read_text())

    a = res["strata"]["ALL"]
    assert res["n_subjects"] == 3, res["n_subjects"]
    assert a["mutants_total"] == 12, a["mutants_total"]
    assert a["setn"]["kills"] == 4 and a["setn"]["valid_mrs"] == 3, a["setn"]
    # Set G seed11: Math 2 + Lang 0 + Guava 3 = 5; Lang has zero valid MRs
    assert a["setg_seed"]["kills"] == 5, a["setg_seed"]
    assert a["setg_seed"]["valid_mrs"] == 2, a["setg_seed"]
    assert a["setg_seed"]["subjects_with_zero_valid_mr"] == 1, a["setg_seed"]
    # Set G all-seeds union: 4 + 2 + 3 = 9
    assert a["setg_allseeds"]["kills"] == 9, a["setg_allseeds"]
    # paired vs seed11: b=4 (Math M3 + Guava M1,M2,M3), c=3 (Math M2,M4 + Lang M1)
    assert a["mcnemar_vs_seed"]["b_setg_only"] == 4, a["mcnemar_vs_seed"]
    assert a["mcnemar_vs_seed"]["c_setn_only"] == 3, a["mcnemar_vs_seed"]
    assert a["mcnemar_vs_allseeds"]["b_setg_only"] == 5, a["mcnemar_vs_allseeds"]
    assert a["mcnemar_vs_allseeds"]["c_setn_only"] == 0

    # 0-valid Set N subject (Guava) recorded honestly as N=0, not dropped
    guava = next(r for r in res["per_subject"] if r["domain"] == "Guava")
    assert guava["setn_kills"] == 0 and guava["setn_valid_mrs"] == 0, guava
    assert guava["setg_seed_kills"] == 3, guava
    assert res["strata"]["Guava"]["setn"]["kills"] == 0
    assert res["strata"]["Math"]["setn"]["kills"] == 3
    assert res["strata"]["Lang"]["setg_seed"]["kills"] == 0
    lang = next(r for r in res["per_subject"] if r["domain"] == "Lang")
    assert lang["setg_seeds_with_valid_mr"] == 1 and lang["setg_seed_kills"] == 0
    assert lang["setg_seed_kill_dist"] == {"12": 2}, lang["setg_seed_kill_dist"]

    print("OK: compare_sets — seed-strict + all-seeds Set G, per-seed dist, "
          "strata split, Wilson, McNemar (both refs) all correct")


if __name__ == "__main__":
    main()
