"""Driver: NOETHER home-field generation->detection experiment.

Runs each registered SUT's algebra-MR battery against its operator-fault pool,
then computes the §2 generation/detection metrics (Wilson CI, per-block,
per-fault-class; NO selection / k* / collapse). Writes results/<sut>/.

Usage (from this directory):
    python run_homefield_detection.py                 # all available SUTs
    python run_homefield_detection.py --sut heat      # one SUT
    T2_ROOT=/path/to/Minimum-MR-SubSet/scripts python run_homefield_detection.py
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import noether_metrics as nm
from suts import heat_sut, advdiff_sut

RESULTS = _HERE / "results"


def _report_md(s: dict) -> str:
    md = s["M_detect"]
    lines = [
        f"# NOETHER home-field detection -- {s['sut']}",
        "",
        f"**Equation**: {s['equation']}",
        f"**Implementations**: {', '.join(s['impls'])}",
        f"**Alignment gate (baseline_control all survive)**: "
        f"{'PASS' if s['alignment_ok'] else 'FAIL'}",
        "",
        "## Generation / detection (no selection / k* reported)",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| M-yield (MRs derived) | {s['M_yield']} |",
        f"| M-block (NOETHER blocks covered) | {s['M_block']} ({', '.join(s['blocks_covered'])}) |",
        f"| M-detect (real mutants killed) | {md['killed']}/{md['n_real_mutants']} "
        f"= {md['rate']:.3f} |",
        f"| Wilson 95% CI | [{md['wilson95'][0]:.3f}, {md['wilson95'][1]:.3f}] |",
        f"| Underpowered (n<10) | {md['underpowered']} |",
        f"| GenMorph feasible | {s['genmorph'].get('feasible')} |",
        "",
        "## Per-block detection",
        "",
        "| Block | MRs | detected/n | rate | Wilson95 |",
        "|---|---|---|---|---|",
    ]
    for blk, d in s["per_block"].items():
        lines.append(f"| {blk} | {', '.join(d['mrs'])} | {d['detected']}/{d['n']} "
                     f"| {d['rate']:.3f} | [{d['wilson95'][0]:.3f}, {d['wilson95'][1]:.3f}] |")
    lines += ["", "## Per-fault-class detection", "",
              "| fault_class | detected/n | rate |", "|---|---|---|"]
    for fc, d in s["per_fault_class"].items():
        lines.append(f"| {fc} | {d['detected']}/{d['n']} | {d['rate']:.3f} |")
    lines += ["", "## Per-MR kill counts (real mutants)", "",
              "| MR | block | kills |", "|---|---|---|"]
    for m, d in s["per_mr"].items():
        lines.append(f"| {m} | {d['block']} | {d['kills']} |")
    lines += ["", "## GenMorph feasibility (M-feasible)", "",
              f"- feasible: {s['genmorph'].get('feasible')}",
              f"- reason: {s['genmorph'].get('reason','')}",
              f"- expressibility tier: {s['genmorph'].get('expr_tier','')}", ""]
    return "\n".join(lines)


def run_one(name: str, evaluate) -> dict | None:
    try:
        result = evaluate()
    except ImportError as e:
        print(f"[skip] {name}: {e}", file=sys.stderr)
        return None
    s = nm.summarize(result)
    out = RESULTS / s["sut"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "detection_metrics.json").write_text(
        json.dumps(s, indent=2), encoding="utf-8")
    (out / "REPORT.md").write_text(_report_md(s), encoding="utf-8")
    flag = "OK" if s["alignment_ok"] else "ALIGNMENT-FAIL"
    md = s["M_detect"]
    print(f"[{flag}] {s['sut']}: M-yield={s['M_yield']} M-block={s['M_block']} "
          f"M-detect={md['killed']}/{md['n_real_mutants']}={md['rate']:.3f} "
          f"CI[{md['wilson95'][0]:.3f},{md['wilson95'][1]:.3f}] "
          f"-> {out.relative_to(_HERE)}")
    return s


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--sut", default="all",
                    help="comma list: heat,advdiff (default: all available)")
    args = ap.parse_args(argv)

    registry = {"heat": heat_sut.evaluate, "advdiff": advdiff_sut.evaluate}
    want = list(registry) if args.sut == "all" else [s.strip() for s in args.sut.split(",")]

    summaries = {}
    for name in want:
        if name not in registry:
            print(f"[skip] unknown SUT {name!r}", file=sys.stderr)
            continue
        s = run_one(name, registry[name])
        if s is not None:
            summaries[s["sut"]] = {
                "M_yield": s["M_yield"], "M_block": s["M_block"],
                "blocks": s["blocks_covered"],
                "M_detect": s["M_detect"], "alignment_ok": s["alignment_ok"],
                "genmorph_feasible": s["genmorph"].get("feasible"),
            }

    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "summary.json").write_text(json.dumps(summaries, indent=2),
                                          encoding="utf-8")
    print(f"\n[done] {len(summaries)} SUT(s) -> {(RESULTS / 'summary.json').relative_to(_HERE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
