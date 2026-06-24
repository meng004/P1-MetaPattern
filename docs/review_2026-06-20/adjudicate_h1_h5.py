#!/usr/bin/env python3
"""
H1–H5 裁决脚手架 —— s5_aligned seed12/13 confirmatory（预注册 prereg_s5_multiseed.md）

用途
----
执行会话在含 `meng004/S5_aligned_experiment` 访问权的环境跑完
`SEED=12/13 bash run_all.sh` 得到 `results/comparison_seed{12,13}.json` 后,
用本脚本按预注册 §4(钉死的检验/定义)+ §7.1(证伪判据)产出 H1–H5 裁决报告。
**本脚本不跑实验、不碰预注册 §3、不做 MR selection/domination(self-overlap 红线)。**

为什么是脚手架而非已执行
------------------------
harness `experiment/s5_aligned` 在私有 repo `meng004/S5_aligned_experiment`,
不在本会话 repo scope(p1-metapattern + minimum-mr-subset),本会话无 add_repo 工具,
故 confirmatory 无法在此执行。本脚本预先备好,使执行会话拿到结果后可一键裁决。

输入契约(comparison_seed{S}.json;若 s5_aligned 原生 schema 不同,写一个 adapter 映射到此)
-----------------------------------------------------------------------------------
{
  "seed": 12,
  "strata": {
    "Guava": { "subjects": {
        "GuavaClass?indexOf?0": { "setN": [0/1,...], "setG_single": [0/1,...] }, ...
    }},
    "Math":  { "subjects": { ... } },
    "Lang":  { "subjects": { ... } },
    "ALL":   { "subjects": { ... } }          # 可省略;省略则由 Math+Lang+Guava 合并
  },
  "setG_union12": {                            # 可选,H1 强形式(探索性);per stratum per subject
    "Guava": { "<subj>": [0/1,...], ... }
  }
}
- setN[i] / setG_single[i] 是同一 mutant i 的 0/1 杀死(同序);per-subject 向量长度 = 该 subject 的 mutant 数。
- 杀死定义(prereg §4.1):KILLED/TIMED_OUT/MEMORY_ERROR=1。valid MR=原始 SUT 上 FP=0。这些由 run_all.sh 上游裁定,本脚本只消费 0/1。

用法
----
python3 adjudicate_h1_h5.py comparison_seed12.json comparison_seed13.json \
    [--seed11 comparison_seed11.json] [--reliability reliability.json] \
    [--out adjudication_seed12_13.md]

依赖:Python 3.8+(标准库)。scipy 可选(paired Wilcoxon;缺则标注 skipped)。
"""
import sys, json, argparse, random, math
from math import comb

# ---------- 统计原语(prereg §4.2) ----------
def wilson_ci(k, n, z=1.959963984540054):
    if n == 0: return (float("nan"), float("nan"))
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = (z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))) / d
    return (max(0.0, c-h), min(1.0, c+h))

def mcnemar_exact(b, c, sided="two"):
    """exact McNemar:条件于 discordant 对的二项检验。sided: 'two' | 'N'(b>c 利于 Set N) | 'G'(c>b 利于 Set G)。"""
    n = b + c
    if n == 0: return None  # test undefined
    if sided == "two":
        k = min(b, c)
        return min(1.0, 2 * sum(comb(n, i) for i in range(k+1)) / (2**n))
    # one-sided
    if sided == "N":   # H1: 利于 Set N 即 b 大 → P(B >= b) under p=0.5
        return sum(comb(n, i) for i in range(b, n+1)) / (2**n)
    if sided == "G":   # H2: 利于 Set G 即 c 大 → P(C >= c)
        return sum(comb(n, i) for i in range(c, n+1)) / (2**n)
    raise ValueError(sided)

def cluster_bootstrap_ci(subjects, B=10000, seed=20260620):
    """subject-level cluster bootstrap:按 subject 有放回重采样,统计 pooled (Set N − Set G) kill-rate 差。"""
    rng = random.Random(seed)
    names = list(subjects)
    if not names: return (float("nan"), float("nan"))
    diffs = []
    for _ in range(B):
        kN=nN=kG=nG=0
        for _ in names:
            s = subjects[rng.choice(names)]
            kN += sum(s["setN"]); nN += len(s["setN"])
            kG += sum(s["setG_single"]); nG += len(s["setG_single"])
        if nN and nG: diffs.append(kN/nN - kG/nG)
    if not diffs: return (float("nan"), float("nan"))
    diffs.sort()
    lo = diffs[int(0.025*len(diffs))]; hi = diffs[min(len(diffs)-1, int(0.975*len(diffs)))]
    return (lo, hi)

def paired_wilcoxon(subjects):
    """subject-level paired Wilcoxon signed-rank,逐 subject (setN_rate − setG_rate)。"""
    diffs = []
    for s in subjects.values():
        if s["setN"] and s["setG_single"]:
            diffs.append(sum(s["setN"])/len(s["setN"]) - sum(s["setG_single"])/len(s["setG_single"]))
    if not diffs: return None, "no subjects"
    try:
        from scipy.stats import wilcoxon
        nz = [d for d in diffs if d != 0]
        if not nz: return None, "all-zero diffs"
        stat, p = wilcoxon(nz)
        return p, f"W={stat:.3f}, n_nonzero={len(nz)}"
    except Exception as e:
        return None, f"scipy unavailable ({type(e).__name__}); install scipy to enable"

# ---------- 层级聚合 ----------
def pool(stratum):
    subs = stratum["subjects"]
    setN = [v for s in subs.values() for v in s["setN"]]
    setG = [v for s in subs.values() for v in s["setG_single"]]
    b = sum(1 for a,g in zip(setN,setG) if a and not g)   # N_only
    c = sum(1 for a,g in zip(setN,setG) if g and not a)   # G_only
    both = sum(1 for a,g in zip(setN,setG) if a and g)
    return dict(n=len(setN), kN=sum(setN), kG=sum(setG), b=b, c=c, both=both,
                rateN=sum(setN)/len(setN) if setN else float("nan"),
                rateG=sum(setG)/len(setG) if setG else float("nan"), subjects=subs)

def ensure_all(strata):
    if "ALL" in strata: return strata
    merged = {"subjects": {}}
    for k in ("Math","Lang","Guava"):
        if k in strata: merged["subjects"].update(strata[k]["subjects"])
    strata = dict(strata); strata["ALL"] = merged
    return strata

def stratum_line(name, st):
    p = pool(st)
    up = "  ⚠ UNDERPOWERED (b+c<25)" if (p["b"]+p["c"])<25 else ""
    wN = wilson_ci(p["kN"], p["n"]); wG = wilson_ci(p["kG"], p["n"])
    cb = cluster_bootstrap_ci(p["subjects"])
    wp, wnote = paired_wilcoxon(p["subjects"])
    return p, dict(
        rateN=p["rateN"], rateG=p["rateG"], b=p["b"], c=p["c"], both=p["both"], n=p["n"],
        wilsonN=wN, wilsonG=wG, cluster_boot_diff_ci=cb, wilcoxon_p=wp, wilcoxon_note=wnote,
        underpowered=(p["b"]+p["c"])<25, discordant=p["b"]+p["c"]) , up

# ---------- 裁决 ----------
def adjudicate(seed_data, seed11_rates=None):
    out = []
    seed = seed_data["seed"]
    strata = ensure_all(seed_data["strata"])
    role = "primary" if seed == 12 else ("replication" if seed == 13 else "exploratory")
    out.append(f"## seed{seed}（{role}）\n")
    metrics = {}
    for name in ("ALL","Math","Lang","Guava"):
        if name not in strata: continue
        p, m, up = stratum_line(name, strata[name])
        metrics[name] = m
        def fmt(ci): return f"[{ci[0]:.3f},{ci[1]:.3f}]"
        out.append(f"- **{name}**: Set N {m['rateN']:.3f} {fmt(m['wilsonN'])} vs "
                   f"Set G(single) {m['rateG']:.3f} {fmt(m['wilsonG'])}; "
                   f"b(N_only)={m['b']} c(G_only)={m['c']} both={m['both']} n={m['n']}; "
                   f"cluster-boot Δ 95%CI {fmt(m['cluster_boot_diff_ci'])}; "
                   f"Wilcoxon p={m['wilcoxon_p']}({m['wilcoxon_note']}){up}")
    # H1 Guava 单侧
    g = metrics.get("Guava")
    if g:
        p1 = mcnemar_exact(g["b"], g["c"], "N")
        verdict = ("test undefined (b+c=0)" if p1 is None else
                   ("支持 H1(单侧 p<0.05,方向利于 Set N)" if (p1<0.05 and g["b"]>g["c"]) else
                    "不支持/inconclusive" + (" — UNDERPOWERED" if g["underpowered"] else "")))
        out.append(f"- **H1（Guava,弱形式,单侧 McNemar）**: p={p1}; 裁决={verdict}"
                   + ("（强形式 vs 12-seed union 为探索性,见 setG_union12,不计 confirmatory）" if "setG_union12" in seed_data else ""))
    # H2 Math 单侧（预测我方失利）
    m2 = metrics.get("Math")
    if m2:
        p2 = mcnemar_exact(m2["b"], m2["c"], "G")
        # §7.1: H2 被证伪 iff Set N >= Set G（失利未现）
        falsified = (m2["b"] >= m2["c"])
        verdict = ("test undefined (b+c=0)" if p2 is None else
                   ("支持 H2(单侧 p<0.05,Set G 压制 Set N,符合诚实先验)" if (p2<0.05 and m2["c"]>m2["b"]) else
                    ("H2 被证伪(Set N≥Set G,失利未现)" if falsified else "inconclusive")
                    + (" — UNDERPOWERED" if m2["underpowered"] else "")))
        out.append(f"- **H2（Math,单侧 McNemar,预测失利）**: p={p2}; 裁决={verdict}")
    # H3 Lang 双侧（描述,无方向）
    l3 = metrics.get("Lang")
    if l3:
        p3 = mcnemar_exact(l3["b"], l3["c"], "two")
        verdict = ("no discordant pairs, test undefined, rates identical" if p3 is None else
                   ("存在差异(双侧 p<0.05)" if p3<0.05 else
                    "underpowered, inconclusive（非显著≠等价;预注册禁记 confirmed tie）"))
        out.append(f"- **H3（Lang,双侧 McNemar,描述性）**: p={p3}; 裁决={verdict}")
    return "\n".join(out), {name: metrics[name]["rateN"] for name in metrics}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seed12"); ap.add_argument("seed13")
    ap.add_argument("--seed11"); ap.add_argument("--reliability")
    ap.add_argument("--out", default="adjudication_seed12_13.md")
    a = ap.parse_args()
    rep = ["# H1–H5 裁决报告（s5_aligned seed12/13 confirmatory）\n",
           "> 预注册 `prereg_s5_multiseed.md`（§3 冻结于 f2a5980,已校验 §3 区段对 f2a5980 为空）。",
           "> self-overlap 红线:仅 detection/generation sufficiency;禁 k*/selection/domination。",
           "> 每假设 primary=seed12、replication=seed13;b+c<25 标 underpowered;b+c=0 记 test undefined。\n"]
    rates_by_seed = {}
    for f in (a.seed12, a.seed13):
        d = json.load(open(f))
        block, rates = adjudicate(d)
        rep.append(block); rep.append("")
        rates_by_seed[d["seed"]] = rates
    # H4 跨 seed 离散度（描述性,需 seed11 rates）
    rep.append("## H4（鲁棒性,跨 seed 离散度,描述性,无 p）")
    s11 = {}
    if a.seed11:
        _, s11 = adjudicate(json.load(open(a.seed11)))
    for name in ("ALL","Math","Lang","Guava"):
        vals = [rates_by_seed.get(s,{}).get(name) for s in (12,13)] + ([s11.get(name)] if s11 else [])
        vals = [v for v in vals if v is not None]
        if not vals: continue
        rng = max(vals)-min(vals); mean = sum(vals)/len(vals)
        sd = (sum((v-mean)**2 for v in vals)/len(vals))**0.5
        rep.append(f"- **{name}**: Set N per-seed rates={[round(v,3) for v in vals]} "
                   f"(range={rng:.3f}, SD={sd:.3f}) — 描述性,变异仅来自 Randoop 输入(MR 集确定性)")
    # H5（描述性,reliability;受 G1 caveat 约束）
    rep.append("\n## H5（生成可靠性,描述性,不同-n,无配对 p）")
    if a.reliability:
        rel = json.load(open(a.reliability))
        rep.append(f"- Set G(GenMorph 单跑)valid-MR 成功率(分母=12 发表 seed): 见 reliability.json")
        rep.append(f"- 明细: {json.dumps(rel, ensure_ascii=False)[:800]}")
    else:
        rep.append("- (未提供 --reliability;用 analyze_published_multiseed.py 从发表 12-seed 数据算"
                   " #seeds-with-valid-MR/12;Set N 确定性=每跑相同 MR 集)")
    rep.append("- **G1 caveat（强制,prereg §2.3/§7.2）**: Set N 目前在 acos/pow 因 1e-4 绝对容差 artifact"
               " 产 0 有效 MR;**G1 修复前不得断言 “Set N 始终有效”**。")
    # 冻结/红线提醒
    rep.append("\n## 执行前必须复核(prereg §6/§7.2)")
    rep.append("- `git diff f2a5980 -- docs/review_2026-06-20/prereg_s5_multiseed.md` 的 §3 区段须为空,否则 confirmatory 作废。")
    rep.append("- 每 seed 跑 routeB/pair_seed11.py 同款对齐 sanity(mutant 集与发表一致);对齐破裂即停,不聚合。")
    rep.append("- ALL/Math 负结果(若有)McNemar p 写正文,不藏脚注(反漂移红线)。")
    open(a.out, "w").write("\n".join(rep))
    print(f"wrote {a.out}")

if __name__ == "__main__":
    main()
