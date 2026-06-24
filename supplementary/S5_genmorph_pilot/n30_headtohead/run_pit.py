#!/usr/bin/env python3
"""
Per-SUT PIT driver for the n>=30 commons-math head-to-head.

For each SUT in sut_registry.py:
  - run PIT (pitest-maven mutationCoverage) targeting the SUT's class, with the
    SUT's test class and excludedMethods (sibling methods by simple name), so PIT
    mutates (mostly) the target method's body. Overloaded targets are
    disambiguated downstream by methodDescription (parse_kill_matrix.py).
  - copy mutations.xml to pit_reports/<sut_key>/mutations.xml

Maven is invoked once per SUT. Compile is cached after the first run.
Pass --only key1,key2 to run a subset (used for de-risking / reruns).
"""
import argparse
import pathlib
import shutil
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).parent
HARNESS = HERE / "harness"
REPORTS = HERE / "pit_reports"
M2 = "/tmp/m2repo"

sys.path.insert(0, str(HERE))
from sut_registry import SUTS  # noqa: E402


def excl_simple_names(excl, keep_method):
    # PIT excludedMethods takes SIMPLE names and cannot distinguish overloads.
    # So we must NEVER exclude the target method's own simple name (that would
    # drop the SUT overload too). Different-name siblings are excluded to reduce
    # the mutant population; same-name overloads are left in and filtered out
    # downstream by methodDescription (parse_kill_matrix.py).
    out = []
    for e in excl:
        nm = e.split("(")[0]
        if nm == keep_method:
            continue
        out.append(nm)
    seen = set()
    res = []
    for e in out:
        if e not in seen:
            seen.add(e)
            res.append(e)
    return res


def run_one(s, timeout_s=600):
    key = s["key"]
    cls = s["cls"]
    test_cls = f"headtohead.T_{key}"
    excluded = ",".join(excl_simple_names(s["excl"], s["method"]))
    dest = REPORTS / key
    dest.mkdir(parents=True, exist_ok=True)

    cmd = [
        "mvn", "-q", f"-Dmaven.repo.local={M2}",
        "org.pitest:pitest-maven:1.15.3:mutationCoverage",
        f"-DtargetClasses={cls}",
        f"-DtargetTests={test_cls}",
        f"-DexcludedMethods={excluded}",
        "-DoutputFormats=XML",
        "-DtimestampedReports=false",
        "-DfullMutationMatrix=true",   # record ALL killing tests per mutant (for per-MR/per-set attribution)
        "-Dmutators=DEFAULTS",
        "-Dthreads=4",
        "-DtimeoutConstInMillis=5000",
        "-DtimeoutFactor=1.5",
    ]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=str(HARNESS), capture_output=True,
                           text=True, timeout=timeout_s)
    except subprocess.TimeoutExpired:
        return key, "TIMEOUT", 0, time.time() - t0, ""
    dt = time.time() - t0
    mx = HARNESS / "target" / "pit-reports" / "mutations.xml"
    if mx.exists():
        shutil.copy(mx, dest / "mutations.xml")
        # quick count
        import xml.etree.ElementTree as ET
        n = len(ET.parse(mx).getroot().findall("mutation"))
        status = "OK" if p.returncode == 0 else f"RC{p.returncode}"
        return key, status, n, dt, ""
    else:
        tail = (p.stdout or "")[-800:] + (p.stderr or "")[-800:]
        return key, "NO_XML", 0, dt, tail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="comma-separated SUT keys")
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args()

    REPORTS.mkdir(parents=True, exist_ok=True)
    targets = SUTS
    if args.only:
        want = set(args.only.split(","))
        targets = [s for s in SUTS if s["key"] in want]

    print(f"Running PIT on {len(targets)} SUTs...")
    results = []
    for i, s in enumerate(targets, 1):
        key, status, n, dt, tail = run_one(s, args.timeout)
        results.append((key, status, n, dt))
        print(f"[{i}/{len(targets)}] {key:18s} {status:8s} mutants={n:4d} {dt:6.1f}s")
        if status in ("NO_XML", "TIMEOUT") and tail:
            print("    ---- diagnostic tail ----")
            for ln in tail.splitlines()[-12:]:
                print("    " + ln)
    ok = sum(1 for _, st, _, _ in results if st in ("OK",) or st.startswith("RC"))
    print(f"\nDone. {ok}/{len(results)} produced mutations.xml. "
          f"Total mutants: {sum(n for _,_,n,_ in results)}")


if __name__ == "__main__":
    main()
