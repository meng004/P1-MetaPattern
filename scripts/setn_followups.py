#!/usr/bin/env python3
"""scripts/setn_followups.py — construct Set N follow-up test inputs.

Set N MRs are hand-authored (jir, jor) predicates that never went through
GenMorph's generation pipeline, so the upstream evaluator (which derives
follow-up inputs from a constructive `transformations.txt`) cannot produce their
follow-up inputs. This script supplies exactly that missing piece, so Set N can
then be scored by GenMorph's *own* PITestGenerator + PIT — on the same mutant
set and with the same kill definition as Set G (CLAUDE.md: substrate held
constant, only the MR set varies).

For each Set N MR `<subject>@<name>`:
  * parse its input relation (.jir) into a constructive transform
        i_<var>_f = expr(i_*_s)
  * for each upstream source `.methodinputs`, write a follow-up `.methodinputs`
    with the transformed parameter values, named `<subject>@<testid>@<name>`
  * write the `<subject>@<name>.cmrip` marker PITestGenerator enumerates MRs by
  * stage the MR's `.jir`/`.jor` into the mrs dir under `<experiment>/<subject>/`

The Set N .jir forms emitted by generate_set_n_mrs.py are regular conjunctions:
    numeric:  (Math.abs(((double) i_<v>_f) - (<EXPR over _s>)) < 1.0E-4)
    boolean:  (i_<v>_f == (<EXPR over _s>))
Each conjunct fixes one follow-up variable. Anything that does not match a known
form raises (fail-loud) rather than silently skipping a relation.
"""

import argparse
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SEP = "@"  # ch.usi.gassert.util.FileUtils SEPARATORS[0]

# ---------------------------------------------------------------------------
# .jir input-relation parsing  ->  {var: java_expr_over_source_vars}
# ---------------------------------------------------------------------------
# numeric:  Math.abs( ((double) i_<v>_f) - <EXPR> ) < 1.0E-4
_NUM = re.compile(
    r"Math\.abs\(\s*\(\((?:double|float|int|long)\)\s*i_(\w+)_f\)\s*-\s*(.+?)\)\s*<\s*1\.0E-4"
)
# boolean / exact:  ( i_<v>_f == <EXPR> )
_BOOL = re.compile(r"i_(\w+)_f\s*==\s*(.+?)\s*\)")


def _java_expr_to_py(expr: str) -> str:
    """Translate the (small, generated) Java arithmetic grammar to Python."""
    # ((double) i_VAR_s) and friends -> s['VAR']
    expr = re.sub(r"\(\((?:double|float|int|long|short|byte)\)\s*i_(\w+)_s\)",
                  r"s['\1']", expr)
    # any stray cast token (TYPE) -> drop
    expr = re.sub(r"\((?:double|float|int|long|short|byte)\)\s*", "", expr)
    # bare i_VAR_s -> s['VAR']
    expr = re.sub(r"i_(\w+)_s", r"s['\1']", expr)
    # Math.* -> abs(...) / math.*
    expr = expr.replace("Math.abs", "abs")
    expr = re.sub(r"Math\.(\w+)", r"math.\1", expr)
    return expr


def parse_jir(jir_text: str):
    """Return list of (var, py_expr, java_expr) constructive assignments."""
    jir_text = jir_text.strip()
    assigns = []
    for var, java_expr in _NUM.findall(jir_text):
        assigns.append((var, _java_expr_to_py(java_expr), java_expr.strip()))
    if not assigns:
        # try boolean/exact form, conjunct by conjunct
        for conj in re.split(r"\)\s*&&\s*\(", jir_text):
            m = _BOOL.search(conj)
            if m:
                var, java_expr = m.group(1), m.group(2)
                assigns.append((var, _java_expr_to_py(java_expr), java_expr.strip()))
    if not assigns:
        raise ValueError(f"unrecognised .jir input-relation form:\n{jir_text}")
    return assigns


# ---------------------------------------------------------------------------
# .methodinputs  (XStream-serialised ch.usi.methodtest.MethodTest)
# ---------------------------------------------------------------------------
def read_method_inputs(path: Path):
    """-> (ElementTree, {param_name: (clazz, value_or_None)})."""
    tree = ET.parse(path)
    params = {}
    for mp in tree.getroot().findall(".//ch.usi.methodtest.MethodParameter"):
        name = mp.findtext("name")
        clazz = mp.findtext("clazz")
        vnode = mp.find("value")
        params[name] = (clazz, None if vnode is None else vnode.text)
    return tree, params


def _cast(value: float, clazz: str):
    if clazz in ("int", "long", "short", "byte", "java.lang.Integer", "java.lang.Long"):
        return str(int(round(value)))
    if clazz in ("double", "float", "java.lang.Double", "java.lang.Float"):
        return repr(float(value))
    return str(value)


def write_followup(src_tree: ET.ElementTree, src_params: dict,
                   assigns, out_path: Path):
    """Apply the transform to a copy of the source inputs; write follow-up."""
    # numeric source bindings for expression evaluation
    s = {n: float(v) for n, (c, v) in src_params.items() if v is not None}
    # compute all follow-up values from the *source* state first
    new_vals = {}
    for var, py_expr, _ in assigns:
        if var not in src_params:
            raise KeyError(f"transform sets i_{var}_f but source has no param {var}")
        val = eval(py_expr, {"__builtins__": {}}, {"s": s, "abs": abs, "math": math})  # noqa: S307
        new_vals[var] = _cast(val, src_params[var][0])
    # serialise a modified copy
    import copy
    tree = copy.deepcopy(src_tree)
    for mp in tree.getroot().findall(".//ch.usi.methodtest.MethodParameter"):
        name = mp.findtext("name")
        if name in new_vals:
            vnode = mp.find("value")
            if vnode is None:
                raise ValueError(f"param {name} has no <value> to transform")
            vnode.text = new_vals[name]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(out_path, encoding="unicode")


def main():
    ap = argparse.ArgumentParser(description="Construct Set N follow-up inputs.")
    ap.add_argument("--subject", required=True, help="e.g. 'MathClass?gcd?0'")
    ap.add_argument("--set-n-dir", required=True, type=Path)
    ap.add_argument("--sources-dir", required=True, type=Path,
                    help="evaluation_test_inputs_seed<seed> (contains <subject>/)")
    ap.add_argument("--followups-dir", required=True, type=Path,
                    help="evaluation_test_inputs_transform_seed<seed>")
    ap.add_argument("--mrs-dir", required=True, type=Path)
    ap.add_argument("--experiment", default="setn_seed11")
    args = ap.parse_args()

    subject = args.subject
    src_sut_dir = args.sources_dir / subject
    sources = sorted(src_sut_dir.glob(f"{subject}{SEP}*.methodinputs"))
    if not sources:
        sys.exit(f"FATAL: no source .methodinputs in {src_sut_dir}")

    fu_sut_dir = args.followups_dir / args.experiment / subject
    mrs_sut_dir = args.mrs_dir / args.experiment / subject
    mrs_sut_dir.mkdir(parents=True, exist_ok=True)
    fu_sut_dir.mkdir(parents=True, exist_ok=True)

    mrs = sorted(p.name[:-len(".jir.txt")] for p in args.set_n_dir.glob(f"{subject}{SEP}*.jir.txt"))
    print(f"[{subject}] {len(sources)} source inputs, {len(mrs)} Set N MRs")

    for mr in mrs:
        name = mr.split(SEP, 1)[1]              # transform name (after '<subject>@')
        jir = (args.set_n_dir / f"{mr}.jir.txt").read_text()
        jor = (args.set_n_dir / f"{mr}.jor.txt").read_text()
        assigns = parse_jir(jir)

        # follow-up inputs, one per source test
        n_ok = 0
        for src in sources:
            testid = src.name[len(f"{subject}{SEP}"):-len(".methodinputs")]
            tree, params = read_method_inputs(src)
            out = fu_sut_dir / f"{subject}{SEP}{testid}{SEP}{name}.methodinputs"
            write_followup(tree, params, assigns, out)
            n_ok += 1

        # .cmrip marker (records the relation; PITestGenerator enumerates by filename)
        cmrip = fu_sut_dir / f"{subject}{SEP}{name}.cmrip"
        cmrip.write_text("".join(
            f"(i_{v}_f == ({je}))\n".replace("(double) ", "").replace("(int) ", "")
            for v, _, je in assigns))

        # stage MR DSL into the mrs dir where PITestGenerator reads the .jor
        (mrs_sut_dir / f"{mr}.jir.txt").write_text(jir)
        (mrs_sut_dir / f"{mr}.jor.txt").write_text(jor)
        print(f"  {name}: {n_ok} follow-ups + cmrip + jor staged")

    print(f"[{subject}] done -> {fu_sut_dir}")


if __name__ == "__main__":
    main()
