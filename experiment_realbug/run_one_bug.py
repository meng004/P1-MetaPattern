#!/usr/bin/env python3
"""run_one_bug.py — B1 STEP-3 executor (per-bug reproduction -> MR evaluation -> bug_<id>.json).

Drives ONE frozen-ledger bug through the metamorphic evaluation, emitting the
results/bug_<id>.json consumed by analyze_b1.py (STEP-4). Designed for batch use:
the same executor runs every bug; only the per-bug *spec* differs.

A bug spec is a Python module exposing:

    def build():
        '''Return the per-bug reproduction handles. CPU-only, no training.'''
        return {
            "id":   "pyg_6199",
            "repo": "pyg-team/pytorch_geometric",
            "cat":  "cat-ii",                # cat-(i)..(iv) per paper
            "fix_commit": "25abbb15", "parent_commit": "bc47556f",
            "tol":  1e-5,
            "fn_pre":  callable,             # the BUGGY (pre-fix) library callable under test
            "fn_post": callable,             # the FIXED (post-fix) callable (false-positive gate)
            "ctx":  { ... },                 # ctx adapter feeding the MRs (x / index / metric_props / rotate ...)
            "cpu_status": "OK",              # OK | CPU-INFEASIBLE | BLOCKED (spec author sets if it cannot run)
            "notes": "...",
        }

The executor loads every MR in mr_sets/, groups by set (N/M/G/L/B), runs each
applicable MR on fn_pre (detection) and fn_post (false-positive gate), and records
per-set firing. A set FIRES on a bug iff >=1 of its MRs returns 'fired'; a set is
not_applicable iff ALL its MRs are not_applicable.

Honesty: never edits the bug; never relabels not_applicable as held; Set G stays
'not_applicable' (no portable artefact). Output schema matches analyze_b1.py.

Usage: python3 run_one_bug.py --spec specs/bug_pyg_6199.py [--out-dir results]
Deps: the bug's env-class stack (torch / library) + numpy. mr_sets/ on the path.
"""
import argparse, importlib.util, json, os, sys, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
MR_DIR = os.path.join(HERE, "mr_sets")
SETS = ["N", "M", "G", "L", "B"]


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_mrs():
    """Load every mr_sets/*.py exposing an MR = {name,set,callable} marker."""
    mrs = []
    for fn in sorted(os.listdir(MR_DIR)):
        if not fn.endswith(".py") or fn.startswith("_"):
            continue
        path = os.path.join(MR_DIR, fn)
        try:
            mod = _load_module(path, f"mr_{fn[:-3]}")
        except Exception as e:  # noqa: BLE001
            print(f"  [warn] could not load {fn}: {type(e).__name__}: {e}", file=sys.stderr)
            continue
        mr = getattr(mod, "MR", None)
        if isinstance(mr, dict) and "callable" in mr and "set" in mr:
            mrs.append(mr)
    return mrs


def _run_mr(mr, fn, ctx, tol):
    try:
        r = mr["callable"](fn, ctx, tol)
        st = r.get("status", "not_applicable")
        return st, r.get("detail", "")
    except Exception as e:  # noqa: BLE001
        return "error", f"{type(e).__name__}: {e}"


def _set_firing(mrs, fn, ctx, tol):
    """Per-set status: fired iff any member fired; else held if any held; else not_applicable.
    Returns (per_set_bool_or_None, detail_map). True=fired, False=held, None=not_applicable."""
    per_set, detail = {}, {}
    for s in SETS:
        members = [m for m in mrs if m["set"] == s]
        if not members:
            per_set[s] = None
            detail[s] = "no MR defined for this set in mr_sets/"
            continue
        statuses = []
        for m in members:
            st, dt = _run_mr(m, fn, ctx, tol)
            statuses.append((m["name"], st, dt))
        names_fired = [n for n, st, _ in statuses if st == "fired"]
        names_held = [n for n, st, _ in statuses if st == "held"]
        if names_fired:
            per_set[s] = True
            detail[s] = "fired: " + ", ".join(names_fired)
        elif names_held:
            per_set[s] = False
            detail[s] = "held: " + ", ".join(names_held)
        else:
            per_set[s] = None
            detail[s] = "not_applicable: " + "; ".join(f"{n}({st})" for n, st, _ in statuses)
    return per_set, detail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="path to per-bug spec .py exposing build()")
    ap.add_argument("--out-dir", default="results")
    a = ap.parse_args()

    spec_mod = _load_module(a.spec, "bug_spec")
    bug = spec_mod.build()
    os.makedirs(a.out_dir, exist_ok=True)
    out = {
        "id": bug["id"], "repo": bug.get("repo"), "cat": bug.get("cat"),
        "fix_commit": bug.get("fix_commit"), "parent_commit": bug.get("parent_commit"),
        "tolerance": bug.get("tol", 1e-5),
        "cpu_status": bug.get("cpu_status", "OK"),
        "fired_pre": {s: None for s in SETS},
        "fired_post": {s: None for s in SETS},
        "detail_pre": {}, "detail_post": {},
        "notes": bug.get("notes", ""),
    }

    if out["cpu_status"] != "OK":
        # spec author already declared it cannot run (CPU-INFEASIBLE / BLOCKED): record + stop.
        json.dump(out, open(os.path.join(a.out_dir, f"bug_{bug['id']}.json"), "w"), indent=2)
        print(f"bug_{bug['id']}: {out['cpu_status']} (not run) — {out['notes']}")
        return

    mrs = _load_mrs()
    tol = out["tolerance"]
    ctx = bug["ctx"]
    # Detection on buggy (pre-fix) code:
    out["fired_pre"], out["detail_pre"] = _set_firing(mrs, bug["fn_pre"], ctx, tol)
    # False-positive gate on fixed (post-fix) code (a correct MR must NOT fire):
    if bug.get("fn_post") is not None:
        out["fired_post"], out["detail_post"] = _set_firing(mrs, bug["fn_post"], ctx, tol)

    path = os.path.join(a.out_dir, f"bug_{bug['id']}.json")
    json.dump(out, open(path, "w"), indent=2)
    det = lambda s: out["fired_pre"][s]
    print(f"wrote {path}")
    print("  per-set fired_pre:", {s: det(s) for s in SETS})
    fps = [s for s in SETS if out["fired_post"].get(s) is True]
    if fps:
        print("  ⚠ false positives (fired on FIXED code):", fps)


if __name__ == "__main__":
    main()
