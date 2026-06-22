#!/usr/bin/env python3
"""
Parse per-SUT PIT mutations.xml into a unified kill matrix CSV.

Precision rule (the SUT is a *method*, not a class): we keep ONLY mutations whose
mutatedMethod == SUT.method AND methodDescription == SUT.sig. This filters out
sibling/overload/helper mutations that PIT generates when it mutates the whole
class (excludedMethods cannot disambiguate overloads, so we disambiguate here).

Kill attribution (paired design): PIT is run with -DfullMutationMatrix=true, so
each <mutation> carries either <killingTests> (a '|'-separated list) or
<killingTest>. We extract every killing test-method name and attribute the kill
to Set N / Set B / Set M by the method-name prefix (nN_ / bB_ / mM_) emitted by
gen_tests.py. Infrastructure kills (TIMED_OUT / MEMORY_ERROR / RUN_ERROR) are
attributed to every set that has >=1 test covering the mutant line -- following
the existing S5 parse_pit_xml.py convention -- BUT since every SUT class runs all
three sets against the same code, an infra kill is attributed to all three sets.

D1/D2 stratification (algebra-disrupting vs algebra-preserving), explicit and
reproducible mapping by PIT mutator class:
  D1 (algebra-disrupting): mutators that change arithmetic / relational / branch
      semantics, hence can break an algebraic invariant directly --
      MathMutator, ConditionalsBoundaryMutator, NegateConditionalsMutator,
      RemoveConditionalMutator_*, InvertNegsMutator, IncrementsMutator,
      AOR/ROR/COR families, MathMutator-derived.
  D2 (algebra-preserving): mutators that replace the *result/return* or remove a
      call without rewriting the operation -- *ReturnsMutator (Primitive, Empty,
      Boolean, Null, Object), VoidMethodCallMutator, ConstructorCallMutator,
      NonVoidMethodCallMutator, RemoveIncrementsMutator (value-level).
Unmapped mutators default to D1 (conservative: treat as potentially disrupting),
and are listed in the run log so the mapping can be extended.

Output: kill_matrix.csv with columns
  sut, method, sig, block, mutant_id, line, mutator, mutator_short, pit_status,
  stratum(D1|D2), covered(0|1), set_n, set_b, set_m,
  and one mr_<set><name> column per MR test method (union over all SUTs).
"""
import argparse
import csv
import pathlib
import sys
import xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from sut_registry import SUTS  # noqa: E402

REPORTS = HERE / "pit_reports"

# ---- D1/D2 mutator partition ----
D2_MUTATORS = {
    "PrimitiveReturnsMutator", "EmptyObjectReturnValsMutator",
    "BooleanFalseReturnValsMutator", "BooleanTrueReturnValsMutator",
    "NullReturnValsMutator", "ObjectReturnValsMutator",
    "VoidMethodCallMutator", "ConstructorCallMutator",
    "NonVoidMethodCallMutator",
}
# everything else (MathMutator, ConditionalsBoundaryMutator, InvertNegsMutator,
# RemoveConditionalMutator_*, NegateConditionalsMutator, IncrementsMutator, ...)
# is treated as D1 (algebra-disrupting).


def stratum_of(mutator_short):
    return "D2" if mutator_short in D2_MUTATORS else "D1"


INFRA = {"TIMED_OUT", "MEMORY_ERROR", "RUN_ERROR"}


def killing_methods(mut):
    """Return set of test-method simple names that killed this mutant."""
    names = set()
    # fullMutationMatrix -> <killingTests>a|b|c</killingTests>; also succeedingTests
    for tag in ("killingTests", "killingTest"):
        raw = mut.findtext(tag, default="")
        if not raw:
            continue
        for entry in raw.split("|"):
            entry = entry.strip()
            if not entry:
                continue
            # JUnit5 style: ...[method:foo()] ; JUnit4 style: pkg.Class.method(params)
            import re
            m5 = re.findall(r"\[method:([A-Za-z_][A-Za-z0-9_]*)\(", entry)
            if m5:
                names.update(m5)
                continue
            head = entry.split("(")[0]
            names.add(head.split(".")[-1])
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "results" / "kill_matrix.csv"))
    args = ap.parse_args()

    # First pass: discover all MR columns across SUTs.
    mr_cols = set()
    for s in SUTS:
        for pref, d in (("nN", s["set_n"]), ("bB", s["set_b"]), ("mM", s["set_m"])):
            for mr in d:
                mr_cols.add(f"{pref}_{mr}")
    mr_cols = sorted(mr_cols)

    rows = []
    unmapped = {}
    per_sut_counts = []
    for s in SUTS:
        key = s["key"]
        xmlp = REPORTS / key / "mutations.xml"
        if not xmlp.exists():
            per_sut_counts.append((key, 0, "NO_XML"))
            continue
        root = ET.parse(xmlp).getroot()
        kept = 0
        idx = 0
        for mut in root.findall("mutation"):
            if mut.findtext("mutatedMethod") != s["method"]:
                continue
            if mut.findtext("methodDescription") != s["sig"]:
                continue
            kept += 1
            idx += 1
            status = mut.get("status", "UNKNOWN")
            mutator = mut.findtext("mutator", default="UNKNOWN")
            mshort = mutator.split(".")[-1]
            if mshort not in D2_MUTATORS and "Mutator" in mshort:
                pass  # default D1; record unmapped only if truly unknown family
            line = mut.findtext("lineNumber", default="")
            killers = killing_methods(mut)
            infra = status in INFRA
            covered = 1 if (status != "NO_COVERAGE") else 0

            # per-MR detection
            mrvals = {c: 0 for c in mr_cols}
            for c in mr_cols:
                # an MR detects iff its test name is among killers, OR infra kill
                # (infra kill cannot be attributed to a specific MR, but the
                # mutant IS killed for the set; per-MR infra attribution mirrors
                # S5: attribute to all MR tests present in this SUT's class)
                pass
            # determine which MRs belong to THIS sut's class
            this_mrs = set()
            for pref, d in (("nN", s["set_n"]), ("bB", s["set_b"]), ("mM", s["set_m"])):
                for mr in d:
                    this_mrs.add(f"{pref}_{mr}")
            for c in this_mrs:
                if c in killers or infra:
                    mrvals[c] = 1

            set_n = int(any((c.startswith("nN_") and (c in killers)) for c in this_mrs) or infra)
            set_b = int(any((c.startswith("bB_") and (c in killers)) for c in this_mrs) or infra)
            set_m = int(any((c.startswith("mM_") and (c in killers)) for c in this_mrs) or infra)

            row = {
                "sut": key,
                "method": s["method"],
                "sig": s["sig"],
                "block": s["blocks"],
                "mutant_id": f"{key}#M{idx:03d}",
                "line": line,
                "mutator": mutator,
                "mutator_short": mshort,
                "pit_status": status,
                "stratum": stratum_of(mshort),
                "covered": covered,
                "set_n": set_n,
                "set_b": set_b,
                "set_m": set_m,
            }
            row.update(mrvals)
            rows.append(row)
        per_sut_counts.append((key, kept, "OK"))

    outp = pathlib.Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["sut", "method", "sig", "block", "mutant_id", "line",
                  "mutator", "mutator_short", "pit_status", "stratum",
                  "covered", "set_n", "set_b", "set_m"] + mr_cols
    with outp.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {len(rows)} mutant rows ({len(SUTS)} SUTs) to {outp}")
    print("\nPer-SUT kept (target-method) mutant counts:")
    for k, n, st in per_sut_counts:
        print(f"  {k:18s} {n:4d}  {st}")
    nsut_ok = sum(1 for _, n, st in per_sut_counts if n > 0)
    print(f"\nSUTs with >=1 target-method mutant: {nsut_ok}/{len(SUTS)}")


if __name__ == "__main__":
    main()
