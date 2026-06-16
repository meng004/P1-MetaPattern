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
  * parse its input relation (.jir) into a per-argument constructive transform
  * for each upstream source `.methodinputs`, write a follow-up `.methodinputs`
    with the transformed values, named `<subject>@<testid>@<name>`
  * write the `<subject>@<name>.cmrip` marker PITestGenerator enumerates MRs by
  * stage the MR's `.jir`/`.jor` into the mrs dir under `<experiment>/<subject>/`

Input-relation conjunct grammar emitted by generate_set_n_mrs.py
(one conjunct fixes one follow-up variable):
  numeric          Math.abs(((double) i_<v>_f) - <EXPR over _s>) < 1.0E-4
  receiver-ident   Math.abs(((double) i_this_f.<C>) - ((double) i_this_s.<C>)) < 1.0E-4
  sequence-ident   Sequence.fromValue(i_<v>_f)).equals((..Sequence.fromValue(i_<v>_s)), 1.0E-4)
  sequence-reverse Sequence.fromValue(i_<v>_f)).equals((..Sequence.fromValue(i_<v>_s)).flip(), 1.0E-4)
Every follow-up variable must be covered by exactly one recognised conjunct,
otherwise parse_jir raises (fail-loud) rather than silently leaving it untouched.
"""
import argparse
import copy
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SEP = "@"  # ch.usi.gassert.util.FileUtils SEPARATORS[0]
_NUMERIC_CLASSES = {"int", "long", "short", "byte", "double", "float",
                    "java.lang.Integer", "java.lang.Long", "java.lang.Double",
                    "java.lang.Float", "java.lang.Short", "java.lang.Byte"}

# ---------------------------------------------------------------------------
# .jir input-relation parsing  ->  [(var, kind, spec)]
#   kind 'num'  spec = python expression over source vars dict `s`
#   kind 'id'   spec = None   (follow-up value == source value)
#   kind 'rev'  spec = None   (follow-up value == reversed source sequence)
# ---------------------------------------------------------------------------
_NUM = re.compile(
    r"Math\.abs\(\(\((?:double|float|int|long)\)\s*i_(\w+)_f\)\s*-\s*(.+?)\)\s*<\s*1\.0E-4")
_RECV = re.compile(r"i_this_f\.\w+")
_SEQ = re.compile(
    r"Sequence\.fromValue\(i_(\w+)_f\)\)\.equals\(\([^,]*?Sequence\.fromValue\(i_(\w+)_s\)\)(\.flip\(\))?\s*,")
_BOOL = re.compile(r"\(\s*i_(\w+)_f\s*==\s*(.+?)\)\s*(?:&&|\)\s*$)")


def _java_expr_to_py(expr: str) -> str:
    expr = re.sub(r"\(\((?:double|float|int|long|short|byte)\)\s*i_(\w+)_s\)", r"s['\1']", expr)
    expr = re.sub(r"\((?:double|float|int|long|short|byte)\)\s*", "", expr)
    expr = re.sub(r"i_(\w+)_s", r"s['\1']", expr)
    expr = expr.replace("Math.abs", "abs")
    expr = re.sub(r"Math\.(\w+)", r"math.\1", expr)
    return expr


def parse_jir(jir_text: str):
    t = jir_text.strip()
    assigns = {}
    for var, expr in _NUM.findall(t):
        assigns[var] = ("num", _java_expr_to_py(expr.strip()))
    for vf, vs, flip in _SEQ.findall(t):
        if vf == vs:
            assigns[vf] = ("rev" if flip else "id", None)
        elif not flip:
            assigns[vf] = ("copyfrom", vs)        # swap: i_<vf>_f == i_<vs>_s
        else:
            raise ValueError(f"unsupported flip+swap for i_{vf}_f in:\n{jir_text}")
    if _RECV.search(t):
        assigns["this"] = ("id", None)
    for var, expr in _BOOL.findall(t):
        assigns.setdefault(var, ("num", _java_expr_to_py(expr.strip())))
    if not assigns:
        raise ValueError(f"unrecognised .jir input-relation form:\n{jir_text}")
    # coverage: every i_<v>_f mentioned must be assigned
    mentioned = set(re.findall(r"i_(\w+)_f", t))
    missing = mentioned - set(assigns)
    if missing:
        raise ValueError(f"unhandled follow-up vars {sorted(missing)} in:\n{jir_text}")
    return [(v, k, s) for v, (k, s) in assigns.items()]


# ---------------------------------------------------------------------------
# .methodinputs (XStream-serialised ch.usi.methodtest.MethodTest)
# ---------------------------------------------------------------------------
def read_method_inputs(path: Path):
    tree = ET.parse(path)
    params = {}
    for mp in tree.getroot().findall(".//ch.usi.methodtest.MethodParameter"):
        name = mp.findtext("name")
        clazz = mp.findtext("clazz")
        vnode = mp.find("value")
        params[name] = (clazz, None if vnode is None else vnode.text)
    return tree, params


def _is_numeric(clazz):
    return clazz in _NUMERIC_CLASSES


def _cast(value: float, clazz: str):
    # Non-finite doubles must use Java's spelling (NaN/Infinity), not Python's
    # repr ('nan'/'inf'), or XStream's DoubleConverter throws NumberFormatException.
    if isinstance(value, float) and not math.isfinite(value):
        if math.isnan(value):
            return "NaN"
        return "Infinity" if value > 0 else "-Infinity"
    if clazz in ("int", "long", "short", "byte", "java.lang.Integer",
                 "java.lang.Long", "java.lang.Short", "java.lang.Byte"):
        return str(int(round(value)))
    if clazz in ("double", "float", "java.lang.Double", "java.lang.Float"):
        return repr(float(value))
    return str(value)


def _reverse_value(val, clazz):
    if val is None:
        return None
    if clazz in ("string", "java.lang.String", "String"):
        return val[::-1]
    raise NotImplementedError(f"reverse not implemented for clazz={clazz!r} "
                              "(need the .methodinputs array serialisation)")


def write_followup(src_tree, src_params, assigns, out_path: Path):
    s = {n: float(v) for n, (c, v) in src_params.items()
         if v is not None and _is_numeric(c)}
    new_vals = {}
    for var, kind, spec in assigns:
        if var not in src_params:
            raise KeyError(f"transform sets i_{var}_f but source has no param {var}")
        clazz, val = src_params[var]
        if kind == "id":
            continue                       # follow-up == source: leave untouched
        if kind == "num":
            r = eval(spec, {"__builtins__": {}}, {"s": s, "abs": abs, "math": math})  # noqa: S307
            new_vals[var] = _cast(r, clazz)
        elif kind == "rev":
            new_vals[var] = _reverse_value(val, clazz)
        elif kind == "copyfrom":
            src_val = src_params.get(spec, (None, None))[1]
            if src_val is None:
                raise ValueError(f"copyfrom source {spec} has no value")
            new_vals[var] = src_val
        else:
            raise ValueError(f"unknown transform kind {kind!r}")
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


def _cmrip_lines(assigns):
    out = []
    for var, kind, spec in assigns:
        if kind == "id":
            out.append(f"(i_{var}_f == i_{var}_s)\n")
        elif kind == "rev":
            out.append(f"(i_{var}_f == reverse(i_{var}_s))\n")
        elif kind == "copyfrom":
            out.append(f"(i_{var}_f == i_{spec}_s)\n")
        else:  # num
            expr = spec.replace("s['", "i_").replace("']", "_s")
            out.append(f"(i_{var}_f == ({expr}))\n")
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description="Construct Set N follow-up inputs.")
    ap.add_argument("--subject", required=True, help="e.g. 'MathClass?gcd?0'")
    ap.add_argument("--set-n-dir", required=True, type=Path)
    ap.add_argument("--sources-dir", required=True, type=Path)
    ap.add_argument("--followups-dir", required=True, type=Path)
    ap.add_argument("--mrs-dir", required=True, type=Path)
    ap.add_argument("--experiment", default="setn_seed11")
    ap.add_argument("--strict", action="store_true",
                    help="abort on the first MR whose transform is unsupported")
    args = ap.parse_args()

    subject = args.subject
    sources = sorted((args.sources_dir / subject).glob(f"{subject}{SEP}*.methodinputs"))
    if not sources:
        sys.exit(f"FATAL: no source .methodinputs in {args.sources_dir / subject}")

    fu_dir = args.followups_dir / args.experiment / subject
    mrs_dir = args.mrs_dir / args.experiment / subject
    fu_dir.mkdir(parents=True, exist_ok=True)
    mrs_dir.mkdir(parents=True, exist_ok=True)

    mrs = sorted(p.name[:-len(".jir.txt")]
                 for p in args.set_n_dir.glob(f"{subject}{SEP}*.jir.txt"))
    print(f"[{subject}] {len(sources)} source inputs, {len(mrs)} Set N MRs")

    staged, skipped = 0, []
    for mr in mrs:
        name = mr.split(SEP, 1)[1]
        jir = (args.set_n_dir / f"{mr}.jir.txt").read_text()
        jor = (args.set_n_dir / f"{mr}.jor.txt").read_text()
        try:
            assigns = parse_jir(jir)
            for src in sources:
                testid = src.name[len(f"{subject}{SEP}"):-len(".methodinputs")]
                tree, params = read_method_inputs(src)
                write_followup(tree, params, assigns,
                               fu_dir / f"{subject}{SEP}{testid}{SEP}{name}.methodinputs")
            (fu_dir / f"{subject}{SEP}{name}.cmrip").write_text(_cmrip_lines(assigns))
            (mrs_dir / f"{mr}.jir.txt").write_text(jir)
            (mrs_dir / f"{mr}.jor.txt").write_text(jor)
            staged += 1
            print(f"  {name}: staged ({', '.join(f'{v}:{k}' for v, k, _ in assigns)})")
        except (ValueError, KeyError, NotImplementedError) as e:
            skipped.append((name, str(e).splitlines()[0]))
            print(f"  {name}: UNSUPPORTED — {str(e).splitlines()[0]}", file=sys.stderr)
            if args.strict:
                raise

    print(f"[{subject}] staged {staged}/{len(mrs)} MRs"
          + (f"; UNSUPPORTED: {[n for n, _ in skipped]}" if skipped else ""))
    return 1 if (skipped and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
