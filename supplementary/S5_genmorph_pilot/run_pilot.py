"""
Main harness for the NOETHER vs. GenMorph comparative pilot.

Usage:
    python run_pilot.py --subject TriangleClassification \\
        --genmorph-path /tmp/genmorph_pilot/GenMorph \\
        --K 100 --seed 42 \\
        --output results/results.csv

The harness:
  1. Loads the original program and each PIT mutant for the subject.
  2. Generates K random Triangle inputs under the seed.
  3. For each mutation, evaluates Set N, Set G, Set B against the K inputs.
  4. Records detection (binary per (mutation, set) pair) into results.csv.

After this script completes, run stats.py on results.csv to produce
pilot_stats.json.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import importlib.util
import random
import sys
from pathlib import Path
from typing import Callable, List, Tuple

from set_n_definitions import SET_N
import set_g_loader

Triangle = Tuple[float, float, float]


def _load_classifier_from_file(path: Path, symbol: str = "classify") -> Callable:
    """
    Load a Python classifier file (the harness expects PIT mutants compiled
    to either Java .class files invoked via subprocess, or Python ports).

    For pilots where the subject is Java (the GenMorph 23-Java benchmark),
    swap this loader for a JNI/subprocess-based one. The pilot README
    documents both modes; this Python loader is the simpler default.
    """
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, symbol)


def _generate_triangles(K: int, seed: int) -> List[Triangle]:
    """Generate K base triangle inputs under a fixed seed.

    Mixed distribution: 40% definitely valid triangles, 30% near-degenerate,
    20% definitely degenerate, 10% with a zero side. This ensures coverage
    across non-empty regions of the classification.
    """
    rng = random.Random(seed)
    inputs: List[Triangle] = []
    for _ in range(K):
        category = rng.random()
        if category < 0.40:
            # valid
            a, b, c = rng.uniform(1, 10), rng.uniform(1, 10), rng.uniform(1, 10)
            # ensure triangle inequality
            sides = sorted([a, b, c])
            if sides[2] >= sides[0] + sides[1]:
                sides[2] = sides[0] + sides[1] - 0.01
            inputs.append((sides[0], sides[1], sides[2]))
        elif category < 0.70:
            # near-degenerate
            a, b = rng.uniform(1, 5), rng.uniform(1, 5)
            c = a + b - rng.uniform(0.001, 0.1)
            inputs.append((a, b, c))
        elif category < 0.90:
            # degenerate
            a, b = rng.uniform(1, 5), rng.uniform(1, 5)
            c = a + b + rng.uniform(0, 5)
            inputs.append((a, b, c))
        else:
            # zero side
            inputs.append((rng.uniform(1, 10), rng.uniform(1, 10), 0.0))
    return inputs


def _generate_follow_up(base: Triangle, seed: int) -> Triangle:
    """Generate a deterministic follow-up for ρ_mono / ρ_eqref."""
    rng = random.Random(seed ^ hash(base))
    delta = rng.uniform(0.01, 0.5)
    a, b, c = base
    return (a + delta, b, c - delta)


def _evaluate_set(P: Callable, mr_set: List[Callable], inputs: List[Triangle], seed: int) -> bool:
    """Return True iff the set detects the mutant on at least one input."""
    for base in inputs:
        follow_up = _generate_follow_up(base, seed)
        for mr in mr_set:
            try:
                verdict = mr(P, base, follow_up)
            except Exception:  # noqa: BLE001
                verdict = "na"
            if verdict == "fail":
                return True
    return False


def _enumerate_mutations(genmorph_path: Path, subject: str) -> List[Path]:
    """Enumerate compiled mutant artefact paths.

    For Java subjects, this returns paths to compiled .class mutants. For
    Python ports, returns .py files. The default scan looks for a
    `mutations/` directory under the subject folder.
    """
    candidates = [
        genmorph_path / "subjects" / subject / "mutations",
        genmorph_path / "data" / subject / "mutants",
    ]
    for candidate in candidates:
        if candidate.exists():
            return sorted(candidate.glob("**/*.py")) + sorted(candidate.glob("**/*.class"))
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", default="TriangleClassification")
    parser.add_argument("--genmorph-path", required=True)
    parser.add_argument("--original", required=True, help="Path to original (un-mutated) classifier .py")
    parser.add_argument("--K", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="results/results.csv")
    args = parser.parse_args()

    genmorph_path = Path(args.genmorph_path)
    original_path = Path(args.original)
    if not original_path.exists():
        print(f"ERROR: original classifier not found at {original_path}", file=sys.stderr)
        return 1
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load Set G
    try:
        set_g = set_g_loader.load_set_g(str(genmorph_path), subject=args.subject)
    except FileNotFoundError as exc:
        print(f"WARNING: {exc}", file=sys.stderr)
        print("Falling back to manual transcription (set_g_loader.manual_transcription_set_g).", file=sys.stderr)
        set_g = set_g_loader.manual_transcription_set_g()

    set_n = SET_N
    set_b = [SET_N[0]]  # Set B = {ρ_perm} only

    inputs = _generate_triangles(args.K, args.seed)
    mutation_paths = _enumerate_mutations(genmorph_path, args.subject)
    if not mutation_paths:
        print(f"ERROR: no mutations found under {genmorph_path}/subjects/{args.subject}/mutations", file=sys.stderr)
        return 2

    rows: List[dict] = []
    for mut_path in mutation_paths:
        mut_id = mut_path.stem
        mut_class = mut_path.parent.name  # PIT operator class encoded in directory
        try:
            P_mut = _load_classifier_from_file(mut_path)
        except Exception as exc:  # noqa: BLE001
            print(f"  skip {mut_id}: {exc}", file=sys.stderr)
            continue

        rows.append({
            "mutation_id": mut_id,
            "mutation_class": mut_class,
            "subject": args.subject,
            "set_n_detected": int(_evaluate_set(P_mut, set_n, inputs, args.seed)),
            "set_g_detected": int(_evaluate_set(P_mut, set_g, inputs, args.seed)),
            "set_b_detected": int(_evaluate_set(P_mut, set_b, inputs, args.seed)),
            "seed": args.seed,
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        })

    fieldnames = list(rows[0].keys()) if rows else [
        "mutation_id", "mutation_class", "subject",
        "set_n_detected", "set_g_detected", "set_b_detected",
        "seed", "timestamp",
    ]
    with open(output_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} mutation rows to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
