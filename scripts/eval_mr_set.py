#!/usr/bin/env python3
"""scripts/eval_mr_set.py — score one MR set through GenMorph's own evaluator.

Thin driver around upstream `ch.usi ... strategy.genmorph.evaluation()`: it
reuses GenMorph's PITestGenerator + PIT path verbatim, so the mutant set and the
kill definition are upstream-native. It assumes the substrate already exists in
`<output_dir>`:
  * source test inputs at  <sources_subdir>/<system_id>/*.methodinputs
  * follow-up inputs at    <followups_subdir>/<experiment>/<system_id>/*.methodinputs (+ .cmrip)
  * MR DSL staged at       <mrs_subdir>/<experiment>/<system_id>/*.{jir,jor}.txt
  * compiled SUT at        <build_subdir>/

and writes `<pitest_workdir>/<system_id>/mutants_killed.csv` (+ mrs_status.csv).

For Set N the follow-ups/MRs are produced by scripts/setn_followups.py; for a
native Set G regeneration they come from a prior `genmorph` gen. Either way the
scoring here is identical, which is what makes the comparison fair.
"""
import argparse
import os
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--genmorph", required=True,
                    help="GenMorph root (cwd for the run; holds scripts/, configs/)")
    ap.add_argument("--sut-config", required=True,
                    help="SUT config path relative to --genmorph")
    ap.add_argument("--output-dir", required=True,
                    help="output_dir name relative to --genmorph (e.g. output_dir_math)")
    ap.add_argument("--experiment-template", default="setn_seed{seed}",
                    help="assertions_dir template; experiment label = this .format(seed)")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--build-subdir", default="build")
    ap.add_argument("--sources-subdir", default="evaluation_test_inputs_seed11")
    ap.add_argument("--followups-subdir", default="setn_followups")
    ap.add_argument("--mrs-subdir", default="setn_mrs")
    ap.add_argument("--pitest-suite-subdir", default="pitest_setn_suite")
    ap.add_argument("--pitest-workdir", default="pitest_setn")
    args = ap.parse_args()

    gen = os.path.realpath(args.genmorph)
    os.chdir(gen)
    sys.path.insert(0, os.path.join(gen, "scripts"))

    from filetypes.sut_config import SUTConfig
    from strategy.genmorph import evaluation
    from states.generate_test_executions import SYSTEM_ID

    config = {
        "generation_seeds": [args.seed],
        "paths": {
            "output_dir": args.output_dir,
            "build_dir": args.build_subdir,
            "mrs_dir": args.mrs_subdir,
            "test_inputs_dir": args.sources_subdir,
            "test_inputs_followup_dir": args.followups_subdir,
            "states_dir": "states_seed{seed}",          # only used if mrs missing
            "assertions_dir": args.experiment_template,  # -> experiment label
        },
        "pitest": {
            "tests_dir": args.pitest_suite_subdir,
            "tests_class_prefix": "TestSuite",
            "workdir": args.pitest_workdir,
            "mrs_status": "mrs_status.csv",
            "mutants_killed": "mutants_killed.csv",
        },
    }

    sut_config = SUTConfig.from_filename(args.sut_config)
    n = 0
    for sut in sut_config.iter_methods():
        sid = SYSTEM_ID(*sut)
        out = os.path.join(gen, args.output_dir, args.pitest_workdir, sid, "mutants_killed.csv")
        print(f"=== eval {sid} (experiment {args.experiment_template.format(seed=args.seed)}) ===",
              flush=True)
        evaluation(sut_config, sut, config)
        if os.path.isfile(out):
            print(f"  -> {out}", flush=True)
            n += 1
        else:
            print(f"  !! no mutants_killed.csv produced for {sid}", file=sys.stderr, flush=True)
    print(f"=== eval_mr_set done: {n} subject(s) scored ===", flush=True)


if __name__ == "__main__":
    main()
