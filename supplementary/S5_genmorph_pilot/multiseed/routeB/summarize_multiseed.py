#!/usr/bin/env python3
"""Aggregate Set N (Route B, authentic PIT) vs published Set G across seeds.
Pairs my Set N union kill vector against GenMorph's published Set G matched-seed
union vector, per seed, with exact McNemar."""
import json, os, csv, sys
from math import comb
GM="/tmp/genmorph_pilot/genmorph_full/genmorph"
PUB="/tmp/genmorph_pilot/genmorph_full/eval_unpacked/evaluation"
SEEDS=[11,12,13,21,22,23,31,32,33,41,42,43]
SUBJECTS=sys.argv[1:] or ["MathClass?gcd?0","MathClass?sin?0"]

def pub_setg(subject,seed):
    f=f"{PUB}/pitest_seed{seed}/{subject}/mutants_killed.csv"
    if not os.path.isfile(f): return None
    with open(f) as fp:
        for r in csv.reader(fp):
            if len(r)>3 and r[0]==f"assertions_seed{seed}" and r[1]=="*":
                return [int(x) for x in r[2:-1]]
    return None

def mcnemar(b,c):
    n=b+c
    return 1.0 if n==0 else min(1.0, 2*sum(comb(n,k) for k in range(min(b,c)+1))/2**n)

out={}
for subject in SUBJECTS:
    print("="*78); print(subject); print("="*78)
    print(f"{'seed':>5} {'setN':>5} {'setG':>5} {'both':>5} {'N_only':>7} {'G_only':>7} {'mcnemar_p':>10}  valid_MRs")
    rows=[]; pooledN=[]; pooledG=[]
    for s in SEEDS:
        rf=f"{GM}/output_dir_math/setn_run_seed{s}/{subject}/setn_result.json"
        if not os.path.isfile(rf): print(f"{s:>5}  (no Set N result)"); continue
        d=json.load(open(rf)); setN=d["setN_union_vector"]; valid=d["setN_valid_MRs"]
        setG=pub_setg(subject,s)
        if setG is None or len(setG)!=len(setN):
            print(f"{s:>5}  setG/len mismatch (setN={len(setN)}, setG={None if setG is None else len(setG)})"); continue
        both=sum(1 for a,b in zip(setN,setG) if a and b)
        no=sum(1 for a,b in zip(setN,setG) if a and not b)
        go=sum(1 for a,b in zip(setN,setG) if b and not a)
        p=mcnemar(no,go)
        print(f"{s:>5} {sum(setN):>5} {sum(setG):>5} {both:>5} {no:>7} {go:>7} {p:>10.4f}  {','.join(valid)}")
        rows.append(dict(seed=s,setN=sum(setN),setG=sum(setG),both=both,N_only=no,G_only=go,mcnemar_p=p,valid=valid))
        pooledN+=setN; pooledG+=setG
    if rows:
        import statistics as st
        sN=[r['setN'] for r in rows]; sG=[r['setG'] for r in rows]
        pb=sum(1 for a,b in zip(pooledN,pooledG) if a and b)
        pno=sum(1 for a,b in zip(pooledN,pooledG) if a and not b)
        pgo=sum(1 for a,b in zip(pooledN,pooledG) if b and not a)
        print(f"\n  setN mean={st.mean(sN):.1f} (min {min(sN)} max {max(sN)}); "
              f"setG mean={st.mean(sG):.1f} (min {min(sG)} max {max(sG)})")
        print(f"  Set N >= Set G in {sum(1 for r in rows if r['setN']>=r['setG'])}/{len(rows)} seeds; "
              f"Set N > Set G in {sum(1 for r in rows if r['setN']>r['setG'])}/{len(rows)}")
        print(f"  POOLED paired: both={pb} N_only={pno} G_only={pgo} McNemar p={mcnemar(pno,pgo):.4g}")
        out[subject]=dict(per_seed=rows, pooled=dict(both=pb,N_only=pno,G_only=pgo,mcnemar_p=mcnemar(pno,pgo)))
json.dump(out, open("/tmp/multiseed_pair_summary.json","w"), indent=2)
print("\nsaved /tmp/multiseed_pair_summary.json")
