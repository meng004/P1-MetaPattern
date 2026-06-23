#!/usr/bin/env python3
"""
Route B: evaluate NOETHER Set N MRs on the SAME PIT mutant set GenMorph used,
via GenMorph's authentic PITestGenerator + PIT (maven) toolchain.

For one (subject, seed):
  - source test inputs : GenMorph's Randoop output (already generated)
  - followup test inputs: produced HERE by applying Set N's deterministic
    transforms (swap / x2 / (p,q+p) / identity) to each source, with Java int32
    wrap, serialized in GenMorph's MethodTest XStream-XML format.
  - MR oracle (.jor)   : NOETHER Set N output relations (repo)
  - PITestGenerator -> JUnit test classes -> PIT mutation -> per-mutant verdicts.

FP rule (matches GenMorph): an MR whose test class fails on the ORIGINAL SUT
(FP>0) is invalid (its mutation score is not counted). Set N union kill = OR over
FP-free MRs. Output mutant vector is over gcd-method-line mutants (== published M1..Mk).
"""
import sys, os, glob, re, shutil, json, xml.etree.ElementTree as ET

_ROUTEB_DIR = os.path.dirname(os.path.abspath(__file__))  # repo path captured before chdir
GM = "/tmp/genmorph_pilot/genmorph_full/genmorph"
os.chdir(GM); sys.path.insert(0, os.path.join(GM, "scripts"))
from evaluation.pitest_generator import pitest_generator
from tools import pitest
from states.instrument_method import find_method_lines, format_java_source
from states.list_methods import list_methods_java_file

SUBJECT   = sys.argv[1] if len(sys.argv) > 1 else "MathClass?gcd?0"
SEED      = sys.argv[2] if len(sys.argv) > 2 else "11"
SUTCLASS, METHOD = "MathClass", SUBJECT.split("?")[1]
MIDX      = int(SUBJECT.split("?")[2])
NSAMPLE   = int(os.environ.get("NSAMPLE", "100"))   # align GenMorph max_tests=100
SETN_SRC  = f"{_ROUTEB_DIR}/../../aligned/set_n_mrs/{SUBJECT}"

OUT       = f"{GM}/output_dir_math"
SRC_DIR   = f"{OUT}/evaluation_test_inputs_seed{SEED}"          # has <SUBJECT>/*.methodinputs
WORK      = f"{OUT}/setn_run_seed{SEED}/{SUBJECT}"
FU_ROOT   = f"{WORK}/followup"; MRS_ROOT = f"{WORK}/mrs"; TESTS = f"{WORK}/tests"
EXP       = "setN"
SOURCES_JAVA = f"{GM}/configs/math-sut/src/main/java"
SUT_CLASSES  = f"{GM}/configs/math-sut/target/classes"
for d in (FU_ROOT+f"/{EXP}/{SUBJECT}", MRS_ROOT+f"/{EXP}/{SUBJECT}", TESTS): os.makedirs(d, exist_ok=True)

def i32(x):                     # simulate Java int overflow
    x &= 0xFFFFFFFF
    return x - 2**32 if x >= 2**31 else x
TRANSFORMS = {                  # followup = f(p,q)
    "rho_perm":  lambda p,q: (q, p),
    "rho_scale": lambda p,q: (i32(2*p), i32(2*q)),
    "rho_eqref": lambda p,q: (p, i32(q+p)),
    "rho_mono":  lambda p,q: (p, q),
}

# --- discover Set N MR names from repo (must have matching .jor) ---
MRS = sorted({os.path.basename(f).split("@")[1].split(".")[0]
              for f in glob.glob(f"{SETN_SRC}/*.jor.txt")})
print(f"[setn] subject={SUBJECT} seed={SEED} MRs={MRS}")

# --- gcd method lines (for verdict filtering => M1..Mk identical to published) ---
src_file = f"{SOURCES_JAVA}/{SUTCLASS}.java"
format_java_source(source_file=src_file)
sut_lines = set(find_method_lines(source_file=src_file, method_name=METHOD, method_index=MIDX))
all_methods = list_methods_java_file(source_file=src_file, container=set)
excluded = [m for m in all_methods if m != METHOD]
print(f"[setn] gcd lines={sorted(sut_lines)}  excluded_methods={len(excluded)}")

def parse_pq(xml_path):
    t = ET.parse(xml_path); r = t.getroot()
    vals = {}
    for mp in r.iter("ch.usi.methodtest.MethodParameter"):
        nm = mp.findtext("name"); ve = mp.find("value")
        if nm in ("p","q") and ve is not None: vals[nm] = int(ve.text)
    return t, vals

def write_followup(tree, p2, q2, out_path):
    r = tree.getroot()
    for mp in r.iter("ch.usi.methodtest.MethodParameter"):
        nm = mp.findtext("name"); ve = mp.find("value")
        if ve is None: continue
        if nm == "p": ve.text = str(p2)
        elif nm == "q": ve.text = str(q2)
    tree.write(out_path)

# --- build followup + cmrip + mrs(jor) ---
srcs = sorted(glob.glob(f"{SRC_DIR}/{SUBJECT}/*.methodinputs"))
import random; random.seed(int(SEED));
if len(srcs) > NSAMPLE: srcs = random.sample(srcs, NSAMPLE)
print(f"[setn] sources used={len(srcs)}")
for mr in MRS:
    open(f"{FU_ROOT}/{EXP}/{SUBJECT}/{SUBJECT}@{mr}.cmrip", "w").close()
    shutil.copy(f"{SETN_SRC}/{SUBJECT}@{mr}.jor.txt", f"{MRS_ROOT}/{EXP}/{SUBJECT}/{SUBJECT}@{mr}.jor.txt")
n_ok = 0
for sp in srcs:
    base = os.path.basename(sp)[:-len(".methodinputs")]      # MathClass?gcd?0@testNNN
    sid  = base.split("@")[1]
    try: tree, pq = parse_pq(sp)
    except Exception as e: continue
    if "p" not in pq or "q" not in pq: continue
    n_ok += 1
    for mr, fn in TRANSFORMS.items():
        if mr not in MRS: continue
        p2, q2 = fn(pq["p"], pq["q"])
        write_followup(ET.parse(sp), p2, q2,
                       f"{FU_ROOT}/{EXP}/{SUBJECT}/{SUBJECT}@{sid}@{mr}.methodinputs")
print(f"[setn] followup built for {n_ok} sources x {len(MRS)} MRs")

# --- PITestGenerator: source+followup -> JUnit test classes ---
prefix = f"{TESTS}/TestSuite"
rc = pitest_generator(classpath=[SUT_CLASSES], sut=SUBJECT, mrs=MRS_ROOT,
                      source_test_inputs=SRC_DIR, followup_test_inputs=FU_ROOT,
                      output_test_prefix=prefix)
gen = sorted(glob.glob(f"{TESTS}/*.java"))
print(f"[setn] PITestGenerator rc={rc}  test classes={[os.path.basename(g) for g in gen]}")
if not gen:
    print("[setn] FATAL: no test classes generated"); sys.exit(2)

# --- compile + run tests on ORIGINAL SUT (FP detection) ---
pitest.write_test_pom(dir=WORK, sources_dir=SOURCES_JAVA, tests_dir=TESTS)
print("[setn] running JUnit on original SUT ...")
pitest.test(workdir=WORK)

results = {}
for g in gen:
    tc = os.path.basename(g)[:-len(".java")]
    fails = list(pitest.get_test_failures(workdir=WORK, target_test=tc))
    fp = sum(1 for _,ty in fails if ty == "FAILURE")
    err = [t for t,ty in fails if ty == "ERROR"]
    mr  = tc.split("_")[-1]
    results[mr] = {"test_class": tc, "fp": fp, "errors": len(err), "killed": None}
    print(f"[setn]   {mr}: FP={fp} ERR={len(err)}")

# --- PIT per FP-free MR ---
for g in gen:
    tc = os.path.basename(g)[:-len(".java")]
    mr = tc.split("_")[-1]
    if results[mr]["fp"] != 0:
        print(f"[setn]   skip PIT for {mr} (FP>0 -> invalid)"); continue
    pitest.write_pitest_pom(dir=WORK, sources_dir=SOURCES_JAVA, tests_dir=TESTS,
                            target_classes=[SUTCLASS], target_tests=[tc], excluded_methods=excluded)
    print(f"[setn]   PIT on {mr} ({tc}) ...")
    pitest.pitest(workdir=WORK)
    mutcsv = f"{WORK}/target/pit-reports/mutations.csv"
    if not os.path.isfile(mutcsv):
        print(f"[setn]   WARN no mutations.csv for {mr}"); continue
    verds = pitest.get_verdicts(mutations=mutcsv, sut_lines=sut_lines)
    killed = [int(v in ("KILLED","TIMED_OUT","MEMORY_ERROR")) for v in verds]
    results[mr]["killed"] = killed
    results[mr]["n_killed"] = sum(killed); results[mr]["n_mutants"] = len(killed)
    print(f"[setn]   {mr}: killed {sum(killed)}/{len(killed)}")
    shutil.rmtree(f"{WORK}/target/pit-reports", ignore_errors=True)

# --- Set N union over FP-free MRs ---
valid = [m for m in results if results[m]["killed"] is not None]
nm = max((results[m]["n_mutants"] for m in valid), default=0)
union = [0]*nm
for m in valid:
    for i,k in enumerate(results[m]["killed"]): union[i] |= k
summary = {"subject": SUBJECT, "seed": SEED, "n_mutants": nm,
           "setN_valid_MRs": valid, "setN_invalid_MRs": [m for m in results if m not in valid],
           "per_mr": results, "setN_union_killed": sum(union), "setN_union_vector": union}
outp = f"{WORK}/setn_result.json"; json.dump(summary, open(outp,"w"), indent=2)
print(f"[setn] DONE union killed = {sum(union)}/{nm} via {valid}")
print(f"[setn] saved {outp}")
