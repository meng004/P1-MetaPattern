"""Path A head-to-head orchestrator.

For each Sun 2021 subject, run Set N (NOETHER) and Set MP (METRIC+)
against the same mutant set; compute kill rates, McNemar, Wilson CIs.
"""
import sys, os, io, contextlib, json, math, importlib.util, copy
from typing import Dict, List, Any, Tuple
import ast

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "subjects"))
sys.path.insert(0, os.path.join(HERE, "identifiers"))
sys.path.insert(0, os.path.join(HERE, "engine"))

# Import after path setup
import sphone, sbaggage, sexpense, smeal  # type: ignore
from noether_identifier import NOETHER_REGISTRY
from metricplus_identifier import METRICPLUS_REGISTRY
from mutation_engine import generate_mutants, Mutant
from mr_types import MR

SUBJECTS = {
    "sphone": {
        "module": sphone,
        "fn_name": "compute_bill",
        "src_path": os.path.join(HERE, "subjects", "sphone.py"),
    },
    "sbaggage": {
        "module": sbaggage,
        "fn_name": "compute_fee",
        "src_path": os.path.join(HERE, "subjects", "sbaggage.py"),
    },
    "sexpense": {
        "module": sexpense,
        "fn_name": "compute_reimbursement",
        "src_path": os.path.join(HERE, "subjects", "sexpense.py"),
    },
    "smeal": {
        "module": smeal,
        "fn_name": "compute_meals",
        "src_path": os.path.join(HERE, "subjects", "smeal.py"),
    },
}


def _silent_generate_mutants(src: str, name: str):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        return generate_mutants(src, name)


def mr_kills_mutant(mr: MR, mutant: Mutant, fn_name: str,
                    samples: List[Dict[str, Any]],
                    original_module) -> bool:
    """Does mr kill mutant on at least one sample?"""
    if not hasattr(mutant.mutated_module, fn_name):
        return False
    f_mut = getattr(mutant.mutated_module, fn_name)
    f_orig = getattr(original_module, fn_name)

    for x in samples:
        x_clean = {k: v for k, v in x.items() if not k.startswith("_")}
        # Evaluate MR on original to ensure it normally holds on x
        try:
            x_prime = mr.transformer(x)
        except (ValueError, KeyError, ZeroDivisionError):
            continue
        if x_prime is None:
            continue
        try:
            y_orig = f_orig(**x_clean)
            x_prime_clean = {k: v for k, v in x_prime.items() if not k.startswith("_")}
            y_prime_orig = f_orig(**x_prime_clean)
        except (ValueError, KeyError, ZeroDivisionError):
            continue
        try:
            holds_on_orig = mr.relation(y_orig, y_prime_orig)
        except (TypeError, ValueError):
            continue
        if not holds_on_orig:
            # MR is buggy on this sample, skip (do not count toward kill)
            continue

        # Now run mutant
        try:
            y_mut = f_mut(**x_clean)
            y_prime_mut = f_mut(**x_prime_clean)
        except (ValueError, KeyError, ZeroDivisionError, TypeError):
            # Mutant crashed: count as killed
            return True
        try:
            holds_on_mut = mr.relation(y_mut, y_prime_mut)
        except (TypeError, ValueError):
            return True
        if not holds_on_mut:
            return True
    return False


def wilson_ci(k: int, n: int, z: float = 1.96) -> Tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    z2n = z * z / n
    center = p + z2n / 2
    half = z * math.sqrt(p * (1 - p) / n + z2n / (4 * n))
    denom = 1 + z2n
    return ((center - half) / denom, (center + half) / denom)


def mcnemar_exact_p(b: int, c: int) -> float:
    """Two-sided exact McNemar p-value from discordant counts (b, c)."""
    n = b + c
    if n == 0:
        return 1.0
    from math import comb
    k_obs = min(b, c)
    p_exact = 0.0
    for k in range(0, k_obs + 1):
        p_exact = p_exact + comb(n, k) * (0.5 ** n)
    two_sided = min(1.0, 2.0 * p_exact)
    return two_sided


def run_subject(name: str) -> Dict[str, Any]:
    info = SUBJECTS[name]
    print(f"\n=== {name} ===")
    with open(info["src_path"]) as f:
        src = f.read()
    print(f"  Generating mutants...")
    mutants = _silent_generate_mutants(src, name)
    print(f"  Mutants: {len(mutants)}")

    print(f"  Loading MR sets...")
    set_n = NOETHER_REGISTRY[name]()
    set_mp = METRICPLUS_REGISTRY[name]()
    print(f"  |Set N| = {len(set_n)}, |Set MP| = {len(set_mp)}")

    samples = info["module"].sample_inputs()
    # Reduce sample count for slow subjects
    if name == "smeal" and len(samples) > 300:
        samples = samples[::3]  # every 3rd
    if name == "sexpense" and len(samples) > 300:
        samples = samples[::2]
    print(f"  Samples per MR: {len(samples)}")

    print(f"  Running Set N vs Set MP on mutants...")
    n_kills = []  # per-mutant kill flags for Set N
    mp_kills = []
    for i, mut in enumerate(mutants):
        killed_by_n = any(mr_kills_mutant(r, mut, info["fn_name"], samples, info["module"])
                           for r in set_n)
        killed_by_mp = any(mr_kills_mutant(r, mut, info["fn_name"], samples, info["module"])
                            for r in set_mp)
        n_kills.append(killed_by_n)
        mp_kills.append(killed_by_mp)
        if (i + 1) % 20 == 0:
            print(f"    {i+1}/{len(mutants)} mutants evaluated")

    # Identify "both miss" mutants for equivalent-mutant flagging
    both_miss_idx = [i for i, (n, mp) in enumerate(zip(n_kills, mp_kills))
                      if not n and not mp]

    n_killed = sum(n_kills)
    mp_killed = sum(mp_kills)
    total = len(mutants)

    # Complementarity cells
    both = sum(1 for i in range(total) if n_kills[i] and mp_kills[i])
    n_only = sum(1 for i in range(total) if n_kills[i] and not mp_kills[i])
    mp_only = sum(1 for i in range(total) if not n_kills[i] and mp_kills[i])
    neither = sum(1 for i in range(total) if not n_kills[i] and not mp_kills[i])

    # McNemar: discordant cells (b = N-only, c = MP-only)
    mcn_p = mcnemar_exact_p(n_only, mp_only)

    # Wilson CIs
    n_ci = wilson_ci(n_killed, total)
    mp_ci = wilson_ci(mp_killed, total)

    # Per-block analysis (NOETHER side)
    block_kill_counts = {}
    for mr in set_n:
        if mr.block_or_pair not in block_kill_counts:
            block_kill_counts[mr.block_or_pair] = {"any_kills": 0}

    return {
        "subject": name,
        "n_mutants": total,
        "n_mrs_set_n": len(set_n),
        "n_mrs_set_mp": len(set_mp),
        "samples_per_mr": len(samples),
        "set_n_killed": n_killed,
        "set_mp_killed": mp_killed,
        "set_n_rate": n_killed / total if total else 0.0,
        "set_mp_rate": mp_killed / total if total else 0.0,
        "set_n_wilson95": n_ci,
        "set_mp_wilson95": mp_ci,
        "complementarity": {
            "both": both, "n_only": n_only,
            "mp_only": mp_only, "neither": neither,
        },
        "mcnemar_b_c": (n_only, mp_only),
        "mcnemar_exact_p_two_sided": mcn_p,
        "both_miss_count": neither,
        "noether_blocks_used": sorted(set(m.block_or_pair for m in set_n)),
        "metricplus_pairs_used": sorted(set(m.block_or_pair for m in set_mp)),
    }


def main():
    all_results = {}
    for subj in ["sphone", "sbaggage", "sexpense", "smeal"]:
        result = run_subject(subj)
        all_results[subj] = result

    # Pooled statistics
    pooled_n_killed = sum(r["set_n_killed"] for r in all_results.values())
    pooled_mp_killed = sum(r["set_mp_killed"] for r in all_results.values())
    pooled_total = sum(r["n_mutants"] for r in all_results.values())
    pooled_n_only = sum(r["complementarity"]["n_only"] for r in all_results.values())
    pooled_mp_only = sum(r["complementarity"]["mp_only"] for r in all_results.values())
    pooled_both = sum(r["complementarity"]["both"] for r in all_results.values())
    pooled_neither = sum(r["complementarity"]["neither"] for r in all_results.values())

    pooled = {
        "total_mutants": pooled_total,
        "set_n_killed": pooled_n_killed,
        "set_mp_killed": pooled_mp_killed,
        "set_n_rate": pooled_n_killed / pooled_total if pooled_total else 0.0,
        "set_mp_rate": pooled_mp_killed / pooled_total if pooled_total else 0.0,
        "set_n_wilson95": wilson_ci(pooled_n_killed, pooled_total),
        "set_mp_wilson95": wilson_ci(pooled_mp_killed, pooled_total),
        "complementarity": {
            "both": pooled_both, "n_only": pooled_n_only,
            "mp_only": pooled_mp_only, "neither": pooled_neither,
        },
        "mcnemar_b_c": (pooled_n_only, pooled_mp_only),
        "mcnemar_exact_p_two_sided": mcnemar_exact_p(pooled_n_only, pooled_mp_only),
    }
    all_results["_pooled"] = pooled

    out_path = os.path.join(HERE, "results", "head_to_head_raw.json")
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nResults written to: {out_path}")

    # Print summary
    print("\n=== Summary ===")
    print(f"{'Subject':<10} | {'mutants':>7} | {'|N|':>4} | {'|MP|':>4} | "
          f"{'N kill':>6} | {'MP kill':>7} | {'N-only':>6} | "
          f"{'MP-only':>7} | {'both':>4} | {'mcN p':>7}")
    for s, r in all_results.items():
        if s == "_pooled":
            continue
        c = r["complementarity"]
        print(f"{s:<10} | {r['n_mutants']:>7} | {r['n_mrs_set_n']:>4} | "
              f"{r['n_mrs_set_mp']:>4} | {r['set_n_killed']:>6} | "
              f"{r['set_mp_killed']:>7} | {c['n_only']:>6} | "
              f"{c['mp_only']:>7} | {c['both']:>4} | "
              f"{r['mcnemar_exact_p_two_sided']:>7.4f}")
    print("-" * 100)
    p = pooled
    c = p["complementarity"]
    print(f"{'POOLED':<10} | {p['total_mutants']:>7} | {'':>4} | {'':>4} | "
          f"{p['set_n_killed']:>6} | {p['set_mp_killed']:>7} | "
          f"{c['n_only']:>6} | {c['mp_only']:>7} | {c['both']:>4} | "
          f"{p['mcnemar_exact_p_two_sided']:>7.4f}")


if __name__ == "__main__":
    main()
