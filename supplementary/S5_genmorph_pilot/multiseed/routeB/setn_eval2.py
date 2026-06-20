#!/usr/bin/env python3
"""Generalised Route B evaluator (gcd + sin). See setn_eval.py for the gcd-only
original; this version is SUBJECT_SPEC-driven so sin (double param x, with PI
constant) works too. Authentic GenMorph PITestGenerator + PIT toolchain."""
import sys, os, glob, shutil, json, math, xml.etree.ElementTree as ET
GM="/tmp/genmorph_pilot/genmorph_full/genmorph"; os.chdir(GM); sys.path.insert(0,GM+"/scripts")
from evaluation.pitest_generator import pitest_generator
from tools import pitest
from states.instrument_method import find_method_lines, format_java_source
from states.list_methods import list_methods_java_file

def i32(x):
    x &= 0xFFFFFFFF
    return x - 2**32 if x >= 2**31 else x
PI = math.pi
SPEC = {
 "MathClass?gcd?0": dict(params=["p","q"], ptype="int", transforms={
     "rho_perm":  lambda v: {"p":v["q"], "q":v["p"]},
     "rho_scale": lambda v: {"p":i32(2*v["p"]), "q":i32(2*v["q"])},
     "rho_eqref": lambda v: {"p":v["p"], "q":i32(v["q"]+v["p"])},
     "rho_mono":  lambda v: dict(v)}),
 "MathClass?sin?0": dict(params=["x"], ptype="double", transforms={
     "rho_bound":      lambda v: dict(v),
     "rho_complement": lambda v: {"x": PI - v["x"]},
     "rho_oddsym":     lambda v: {"x": -v["x"]},
     "rho_period":     lambda v: {"x": v["x"] + 2*PI}}),
}
SUBJECT = sys.argv[1]; SEED = sys.argv[2]
spec = SPEC[SUBJECT]; METHOD = SUBJECT.split("?")[1]; MIDX = int(SUBJECT.split("?")[2])
NSAMPLE = int(os.environ.get("NSAMPLE","100"))
SETN_SRC = f"/home/user/P1-MetaPattern/supplementary/S5_genmorph_pilot/aligned/set_n_mrs/{SUBJECT}"
OUT=f"{GM}/output_dir_math"; SRC_DIR=f"{OUT}/evaluation_test_inputs_seed{SEED}"
W=f"{OUT}/setn_run_seed{SEED}/{SUBJECT}"; FU=f"{W}/followup"; MRS=f"{W}/mrs"; TESTS=f"{W}/tests"
EXP="setN"; SJAVA=f"{GM}/configs/math-sut/src/main/java"; SCL=f"{GM}/configs/math-sut/target/classes"
for d in (f"{FU}/{EXP}/{SUBJECT}", f"{MRS}/{EXP}/{SUBJECT}", TESTS): os.makedirs(d, exist_ok=True)

MRLIST = sorted({os.path.basename(f).split("@")[1].split(".")[0] for f in glob.glob(f"{SETN_SRC}/*.jor.txt")})
print(f"[setn2] {SUBJECT} seed={SEED} MRs={MRLIST}")
srcf=f"{SJAVA}/MathClass.java"; format_java_source(source_file=srcf)
sut_lines=set(find_method_lines(source_file=srcf, method_name=METHOD, method_index=MIDX))
excluded=[m for m in list_methods_java_file(source_file=srcf, container=set) if m!=METHOD]

def parse_vals(p):
    t=ET.parse(p); vals={}
    for mp in t.getroot().iter("ch.usi.methodtest.MethodParameter"):
        nm=mp.findtext("name"); ve=mp.find("value")
        if nm in spec["params"] and ve is not None:
            vals[nm]= int(ve.text) if spec["ptype"]=="int" else float(ve.text)
    return t, vals
def fmt(v):
    if spec["ptype"]=="int": return str(int(v))
    if math.isinf(v): return "Infinity" if v>0 else "-Infinity"
    if math.isnan(v): return "NaN"
    return repr(float(v))
def write_fu(src_path, newvals, out):
    t=ET.parse(src_path)
    for mp in t.getroot().iter("ch.usi.methodtest.MethodParameter"):
        nm=mp.findtext("name"); ve=mp.find("value")
        if nm in newvals and ve is not None: ve.text=fmt(newvals[nm])
    t.write(out)

srcs=sorted(glob.glob(f"{SRC_DIR}/{SUBJECT}/*.methodinputs"))
import random; random.seed(int(SEED))
if len(srcs)>NSAMPLE: srcs=random.sample(srcs, NSAMPLE)
print(f"[setn2] sources={len(srcs)}")
for mr in MRLIST:
    open(f"{FU}/{EXP}/{SUBJECT}/{SUBJECT}@{mr}.cmrip","w").close()
    shutil.copy(f"{SETN_SRC}/{SUBJECT}@{mr}.jor.txt", f"{MRS}/{EXP}/{SUBJECT}/{SUBJECT}@{mr}.jor.txt")
nok=0
for sp in srcs:
    sid=os.path.basename(sp)[:-len(".methodinputs")].split("@")[1]
    try: _, vals = parse_vals(sp)
    except Exception: continue
    if any(p not in vals for p in spec["params"]): continue
    nok+=1
    for mr in MRLIST:
        nv=spec["transforms"][mr](vals)
        write_fu(sp, nv, f"{FU}/{EXP}/{SUBJECT}/{SUBJECT}@{sid}@{mr}.methodinputs")
print(f"[setn2] followup for {nok} sources")
rc=pitest_generator(classpath=[SCL], sut=SUBJECT, mrs=MRS, source_test_inputs=SRC_DIR,
                    followup_test_inputs=FU, output_test_prefix=f"{TESTS}/TestSuite")
gen=sorted(glob.glob(f"{TESTS}/*.java"))
print(f"[setn2] PITestGenerator rc={rc} classes={len(gen)}")
if not gen: print("[setn2] FATAL no tests"); sys.exit(2)
pitest.write_test_pom(dir=W, sources_dir=SJAVA, tests_dir=TESTS); pitest.test(workdir=W)
results={}
for g in gen:
    tc=os.path.basename(g)[:-5]; mr=tc.split("_")[-1]
    fails=list(pitest.get_test_failures(workdir=W, target_test=tc))
    fp=sum(1 for _,ty in fails if ty=="FAILURE")
    results[mr]={"test_class":tc,"fp":fp,"killed":None}
    print(f"[setn2]  {mr}: FP={fp}")
for g in gen:
    tc=os.path.basename(g)[:-5]; mr=tc.split("_")[-1]
    if results[mr]["fp"]!=0: print(f"[setn2]  skip {mr} (FP>0)"); continue
    pitest.write_pitest_pom(dir=W, sources_dir=SJAVA, tests_dir=TESTS, target_classes=["MathClass"],
                            target_tests=[tc], excluded_methods=excluded)
    pitest.pitest(workdir=W)
    mc=f"{W}/target/pit-reports/mutations.csv"
    if not os.path.isfile(mc): print(f"[setn2]  WARN no mutations {mr}"); continue
    verds=pitest.get_verdicts(mutations=mc, sut_lines=sut_lines)
    killed=[int(v in ("KILLED","TIMED_OUT","MEMORY_ERROR")) for v in verds]
    results[mr]["killed"]=killed; results[mr]["n_killed"]=sum(killed); results[mr]["n_mutants"]=len(killed)
    print(f"[setn2]  {mr}: killed {sum(killed)}/{len(killed)}")
    shutil.rmtree(f"{W}/target/pit-reports", ignore_errors=True)
valid=[m for m in results if results[m]["killed"] is not None]
nm=max((results[m]["n_mutants"] for m in valid), default=0)
union=[0]*nm
for m in valid:
    for i,k in enumerate(results[m]["killed"]): union[i]|=k
json.dump({"subject":SUBJECT,"seed":SEED,"n_mutants":nm,"setN_valid_MRs":valid,
           "setN_invalid_MRs":[m for m in results if m not in valid],"per_mr":results,
           "setN_union_killed":sum(union),"setN_union_vector":union}, open(f"{W}/setn_result.json","w"), indent=2)
print(f"[setn2] DONE union killed = {sum(union)}/{nm} via {valid}")
