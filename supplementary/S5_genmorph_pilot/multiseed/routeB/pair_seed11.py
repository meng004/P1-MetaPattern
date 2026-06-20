#!/usr/bin/env python3
"""Alignment check + paired Set N vs published Set G (seed11 gcd).
Re-run PIT for one Set N MR to capture mutations.csv (mutant descriptions),
then pair my Set N union vector against GenMorph's published Set G seed11 union."""
import sys, os, glob, json, shutil, csv
GM="/tmp/genmorph_pilot/genmorph_full/genmorph"; os.chdir(GM); sys.path.insert(0,GM+"/scripts")
from tools import pitest
from states.instrument_method import find_method_lines, format_java_source

SUBJECT="MathClass?gcd?0"; SEED="11"
W=f"{GM}/output_dir_math/setn_run_seed{SEED}/{SUBJECT}"
SOURCES_JAVA=f"{GM}/configs/math-sut/src/main/java"; TESTS=f"{W}/tests"
src_file=f"{SOURCES_JAVA}/MathClass.java"; format_java_source(source_file=src_file)
sut_lines=set(find_method_lines(source_file=src_file,method_name="gcd",method_index=0))
from states.list_methods import list_methods_java_file
excluded=[m for m in list_methods_java_file(source_file=src_file,container=set) if m!="gcd"]

# re-run PIT for rho_eqref, keep mutations.csv
tc="TestSuite_setN_MathClass_gcd_0_rho_eqref"
pitest.write_pitest_pom(dir=W,sources_dir=SOURCES_JAVA,tests_dir=TESTS,
    target_classes=["MathClass"],target_tests=[tc],excluded_methods=excluded)
pitest.pitest(workdir=W)
mut=f"{W}/target/pit-reports/mutations.csv"
shutil.copy(mut, f"{W}/mutations_eqref.csv")

# parse all mutants on gcd lines, in file order (== M1..Mk order)
rows=[]
with open(mut) as fp:
    for l in fp:
        p=l.strip().split(",")
        if len(p)<7: continue
        line=int(p[4])
        if line in sut_lines: rows.append((line,p[2].split(".")[-1],p[5]))
print(f"[align] my PIT produced {len(rows)} gcd-line mutants (published gcd = 25)")
print("[align] mutant (line, operator, verdict_under_eqref):")
for i,(ln,op,v) in enumerate(rows,1): print(f"   M{i}: line {ln:3d} {op:28s} {v}")

# my Set N union vector
d=json.load(open(f"{W}/setn_result.json")); setN=d["setN_union_vector"]
# published Set G seed11 union vector (assertions_seed11,*)
pub=f"/tmp/genmorph_pilot/genmorph_full/eval_unpacked/evaluation/pitest_seed11/{SUBJECT}/mutants_killed.csv"
setG=None
with open(pub) as fp:
    for r in csv.reader(fp):
        if len(r)>3 and r[0]=="assertions_seed11" and r[1]=="*":
            setG=[int(x) for x in r[2:2+25]]
print(f"\n[pair] n_mutants: setN={len(setN)} setG={len(setG)}")
print(f"[pair] Set N union killed = {sum(setN)}/{len(setN)}")
print(f"[pair] Set G (published) union killed = {sum(setG)}/{len(setG)}")
# 2x2 paired (assumes aligned mutant order under identical PIT toolchain)
both=n_only=g_only=neither=0
for a,b in zip(setN,setG):
    if a and b: both+=1
    elif a and not b: n_only+=1
    elif b and not a: g_only+=1
    else: neither+=1
print(f"[pair] both={both} setN_only={n_only} setG_only={g_only} neither={neither}")
# McNemar exact (two-sided)
from math import comb
b,c=n_only,g_only; n=b+c
p=1.0 if n==0 else min(1.0, 2*sum(comb(n,k) for k in range(0,min(b,c)+1))/(2**n))
print(f"[pair] McNemar exact two-sided p = {p:.4f}  (b={b}, c={c})")
print(f"\n[caveat] pairing assumes my PIT mutant order == published M1..M25 "
      f"(same SUT, same PIT 1.7.4, same excludedMethods -> deterministic). "
      f"mutant count match ({len(rows)}==25) is the first alignment signal.")
json.dump({"setN_union":setN,"setG_published_union":setG,"both":both,"setN_only":n_only,
           "setG_only":g_only,"neither":neither,"mcnemar_p":p,
           "my_mutants":rows}, open(f"{W}/pair_seed11.json","w"), indent=2)
print(f"[pair] saved {W}/pair_seed11.json")
