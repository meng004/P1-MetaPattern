#!/usr/bin/env python3
"""
tests/test_generate_mrs.py

Validates that scripts/generate_set_n_mrs.py produces:
  • Exactly 23 subjects under set_n_mrs/
  • Exactly 71 MRs total
  • Each MR has both .jir.txt and .jor.txt files
  • Every DSL string has balanced parentheses
  • No file is empty
  • Numeric MR DSLs only reference declared arg names (smoke check)
"""

from pathlib import Path
import re
import sys

REPO = Path(__file__).resolve().parent.parent
SET_N_DIR = REPO / "set_n_mrs"

EXPECTED_SUBJECTS = 23
EXPECTED_MR_COUNT = 71

# Per the README block-coverage table
EXPECTED_PER_SUBJECT = {
    "MathClass?gcd?0": 4, "MathClass?sin?0": 4, "MathClass?acos?0": 3,
    "MathClass?log10?0": 3, "MathClass?millerRabinPrimeTest?0": 3,
    "MathClass?nextPrime?0": 3, "MathClass?pow?0": 4, "MathClass?sinh?0": 3,
    "MathClass?stirlingS2?0": 4, "MathClass?tan?0": 3,
    "LangClass?abbreviate?0": 2, "LangClass?capitalize?0": 3,
    "LangClass?center?0": 3, "LangClass?difference?0": 3, "LangClass?isSorted?0": 3,
    "GuavaClass?indexOf?0": 3, "GuavaClass?join?0": 3, "GuavaClass?meanOf?0": 3,
    "GuavaClass?min?0": 3, "GuavaClass?padStart?0": 2, "GuavaClass?repeat?0": 4,
    "GuavaClass?sort?0": 3, "GuavaClass?truncate?0": 2,
}

failures = []


def fail(msg):
    failures.append(msg)


def test_subjects_count():
    subs = [d for d in SET_N_DIR.iterdir() if d.is_dir()]
    if len(subs) != EXPECTED_SUBJECTS:
        fail(f"subjects count = {len(subs)}, expected {EXPECTED_SUBJECTS}")


def test_per_subject_mr_counts():
    for subject, expected in EXPECTED_PER_SUBJECT.items():
        d = SET_N_DIR / subject
        if not d.is_dir():
            fail(f"missing subject dir: {subject}")
            continue
        jir = sorted(d.glob("*.jir.txt"))
        jor = sorted(d.glob("*.jor.txt"))
        if len(jir) != expected:
            fail(f"{subject}: {len(jir)} jir files, expected {expected}")
        if len(jor) != expected:
            fail(f"{subject}: {len(jor)} jor files, expected {expected}")
        # Each .jir.txt must have a matching .jor.txt
        jir_names = {p.name.replace(".jir.txt", "") for p in jir}
        jor_names = {p.name.replace(".jor.txt", "") for p in jor}
        if jir_names != jor_names:
            fail(f"{subject}: jir/jor name mismatch — only-jir={jir_names - jor_names} only-jor={jor_names - jor_names}")


def test_total_mr_count():
    total = sum(len(list((SET_N_DIR / s).glob("*.jir.txt")))
                for s in EXPECTED_PER_SUBJECT)
    if total != EXPECTED_MR_COUNT:
        fail(f"total MRs = {total}, expected {EXPECTED_MR_COUNT}")


def test_dsl_well_formed():
    """Every DSL file is non-empty and has balanced parens."""
    for path in SET_N_DIR.rglob("*.txt"):
        text = path.read_text().strip()
        if not text:
            fail(f"empty file: {path.relative_to(REPO)}")
            continue
        # Balanced parens (and balanced curly braces, square brackets)
        for open_c, close_c in [("(", ")"), ("{", "}"), ("[", "]")]:
            if text.count(open_c) != text.count(close_c):
                fail(f"{path.relative_to(REPO)}: unbalanced {open_c}{close_c}: "
                     f"open={text.count(open_c)} close={text.count(close_c)}")


def test_dsl_arg_naming():
    """Each DSL only references arg names known to its subject (smoke check)."""
    # Subject → set of expected `i_<arg>` tokens (from our generator design)
    SUBJECT_ARGS = {
        "MathClass?gcd?0": {"p", "q"},
        "MathClass?sin?0": {"x"},
        "MathClass?acos?0": {"x"},
        "MathClass?log10?0": {"x"},
        "MathClass?millerRabinPrimeTest?0": {"n"},
        "MathClass?nextPrime?0": {"n"},
        "MathClass?pow?0": {"e", "k"},
        "MathClass?sinh?0": {"x"},
        "MathClass?stirlingS2?0": {"n", "k"},
        "MathClass?tan?0": {"x"},
        "LangClass?abbreviate?0": {"str", "abbrevMarker", "offset", "maxWidth"},
        "LangClass?capitalize?0": {"str"},
        "LangClass?center?0": {"str", "size", "padStr"},
        "LangClass?difference?0": {"str1", "str2"},
        "LangClass?isSorted?0": {"array"},
        "GuavaClass?indexOf?0": {"array", "target"},
        "GuavaClass?join?0": {"separator", "array"},
        "GuavaClass?meanOf?0": {"values"},
        "GuavaClass?min?0": {"array"},
        "GuavaClass?padStart?0": {"string", "minLength"},
        "GuavaClass?repeat?0": {"string", "count"},
        "GuavaClass?sort?0": {"array", "fromIndex", "toIndex"},
        "GuavaClass?truncate?0": {"seq", "maxLength", "truncationIndicator"},
    }
    arg_pat = re.compile(r"i_([a-zA-Z][a-zA-Z0-9]*)_[sf]")
    for subject, allowed in SUBJECT_ARGS.items():
        d = SET_N_DIR / subject
        for path in d.rglob("*.txt"):
            text = path.read_text()
            for m in arg_pat.finditer(text):
                arg = m.group(1)
                if arg == "this":
                    continue  # this.PI / this.E / this.PRIMES_LAST are class consts
                if arg not in allowed:
                    fail(f"{path.relative_to(REPO)}: unknown arg 'i_{arg}_*' "
                         f"(allowed for {subject}: {sorted(allowed)})")


def test_jir_has_relation():
    """Each .jir.txt must contain at least one Math.abs equality or Sequence.equals
    relation — basic shape check that catches empty / placeholder files."""
    for path in SET_N_DIR.rglob("*.jir.txt"):
        text = path.read_text()
        if "Math.abs" not in text and "Sequence.fromValue" not in text and text.strip() != "true":
            fail(f"{path.relative_to(REPO)}: jir lacks Math.abs / Sequence (probably malformed)")


def main():
    test_subjects_count()
    test_per_subject_mr_counts()
    test_total_mr_count()
    test_dsl_well_formed()
    test_dsl_arg_naming()
    test_jir_has_relation()

    if failures:
        print(f"FAIL ({len(failures)} issue(s)):")
        for f in failures[:20]:
            print(f"  {f}")
        if len(failures) > 20:
            print(f"  ... and {len(failures) - 20} more")
        sys.exit(1)
    print("OK: 23 subjects, 71 MRs, 142 DSL files, all well-formed")


if __name__ == "__main__":
    main()
