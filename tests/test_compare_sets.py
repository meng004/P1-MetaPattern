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

HDR = "EXPERIMENT,MR,M1,M2,M3,M4,COUNT"


def _csv(experiment, mr_rows, union):
    lines = [HDR]
    for mr, vec in mr_rows:
        lines.append(f"{experiment},{mr}," + ",".join(map(str, vec)) + f",{sum(vec)}")
    lines.append(f"{experiment},*," + ",".join(map(str, union)) + f",{sum(union)}")
    lines.append("*,*," + ",".join(map(str, union)) + f",{sum(union)}")
    return "\n".join(lines) + "\n"


def main():
    # --- pure functions ---
    assert cs.mcnemar_exact_p(0, 0) == 1.0
    assert cs.wilson(0, 0) == [0.0, 0.0]
    lo, hi = cs.wilson(5, 10)
    assert lo < 0.5 < hi, (lo, hi)
    assert cs.mcnemar_exact_p(0, 6) < 0.05, "all-discordant-one-way should be significant"

    # --- integration on synthetic results ---
    tmp = Path(tempfile.mkdtemp())
    rdir = tmp / "seed11"
    # Math subject: Set N kills {M1,M2,M4}=3, Set G kills {M1,M3}=2 (mutants M1..M4)
    md = rdir / "MathClass?demo?0"; md.mkdir(parents=True)
    (md / "setn_mutants_killed.csv").write_text(
        _csv("setn_seed11", [("rho_a", [1, 1, 0, 1]), ("rho_b", [1, 0, 0, 0])], [1, 1, 0, 1]))
    (md / "setg_mutants_killed.csv").write_text(
        _csv("assertions_seed11", [("MR0", [1, 0, 1, 0])], [1, 0, 1, 0]))
    # Lang subject: Set N kills {M1}=1, Set G kills {M1,M2}=2
    ld = rdir / "LangClass?demo?0"; ld.mkdir(parents=True)
    (ld / "setn_mutants_killed.csv").write_text(
        _csv("setn_seed11", [("rho_id", [1, 0, 0, 0])], [1, 0, 0, 0]))
    (ld / "setg_mutants_killed.csv").write_text(
        _csv("assertions_seed11", [("MR0", [1, 1, 0, 0])], [1, 1, 0, 0]))

    out = tmp / "cmp.json"
    subprocess.run([sys.executable, str(ROOT / "scripts" / "compare_sets.py"),
                    "--results-dir", str(rdir), "--seed", "11", "--output", str(out)],
                   check=True, capture_output=True)
    res = json.loads(out.read_text())

    assert res["n_subjects"] == 2, res["n_subjects"]
    allc = res["strata"]["ALL"]
    # totals: 8 mutants; Set N 3+1=4, Set G 2+2=4
    assert allc["mutants_total"] == 8
    assert allc["setn"]["kills"] == 4 and allc["setg"]["kills"] == 4, allc
    assert allc["setn"]["valid_mrs"] == 3 and allc["setg"]["valid_mrs"] == 2, allc
    # paired (per mutant): Math M2,M4 = N-only (c+2), M3 = G-only (b+1);
    #                      Lang M2 = G-only (b+1). => b=2, c=2
    assert allc["mcnemar"]["b_setg_only"] == 2, allc["mcnemar"]
    assert allc["mcnemar"]["c_setn_only"] == 2, allc["mcnemar"]
    # stratification present + correct domain split
    assert res["strata"]["Math"]["setn"]["kills"] == 3, res["strata"]["Math"]
    assert res["strata"]["Lang"]["setg"]["kills"] == 2, res["strata"]["Lang"]

    print("OK: compare_sets pools, strata-splits Math/Lang, Wilson CI, McNemar b/c correct")


if __name__ == "__main__":
    main()
