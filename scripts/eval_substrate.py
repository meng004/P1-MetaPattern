#!/usr/bin/env python3
"""scripts/eval_substrate.py — generate the minimal Set N substrate for a subject.

Calls GenMorph's `evaluation_states` only (Randoop source test inputs + method
input capture). This is all Set N needs from the toolchain: source inputs to
transform into follow-ups, plus the build dir. It deliberately skips GAssert MR
learning and the per-mutant state loop (those exist only for *generating* MRs,
which we don't do — Set N is hand-authored, Set G is published). PIT regenerates
the mutant set at scoring time.

Writes <output_dir>/evaluation_test_inputs_seed<seed>/<system_id>/*.methodinputs.
"""
import argparse
import os
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--genmorph", required=True)
    ap.add_argument("--sut-config", required=True, help="relative to --genmorph")
    ap.add_argument("--output-dir", required=True, help="e.g. output_dir_math")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--randoop-budget", type=int, default=300)
    ap.add_argument("--randoop-execs", type=int, default=3)
    ap.add_argument("--max-tests", type=int, default=100)
    args = ap.parse_args()

    gen = os.path.realpath(args.genmorph)
    os.chdir(gen)
    sys.path.insert(0, os.path.join(gen, "scripts"))

    from filetypes.sut_config import SUTConfig
    from strategy.genmorph import evaluation_states
    from states.generate_test_executions import SYSTEM_ID

    config = {
        "paths": {
            "output_dir": args.output_dir,
            "build_dir": "build",
            "instrumented_build_dir": "instrumented_build",
            "test_inputs_dir": f"evaluation_test_inputs_seed{args.seed}",
        },
        "test_inputs_generator": "randoop",
        "max_tests": args.max_tests,
        "random_seed": args.seed,
        "randoop": {
            "workdir": f"randoop_seed{args.seed}",
            "random_seed": args.seed,
            "time_budget_seconds": args.randoop_budget,
            "num_executions": args.randoop_execs,
        },
    }

    sut_config = SUTConfig.from_filename(args.sut_config)
    for sut in sut_config.iter_methods():
        sid = SYSTEM_ID(*sut)
        out = os.path.join(gen, args.output_dir, f"evaluation_test_inputs_seed{args.seed}", sid)
        print(f"=== substrate {sid} ===", flush=True)
        evaluation_states(sut_config, sut, config)
        n = len([f for f in os.listdir(out)]) if os.path.isdir(out) else 0
        print(f"  -> {n} source .methodinputs in {out}", flush=True)
    print("=== substrate done ===", flush=True)


if __name__ == "__main__":
    main()
