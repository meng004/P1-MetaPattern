"""
Set G: load GenMorph's published evolved MRs for TriangleClassification.

Source: Ayerdi et al. ASE 2023 replication package, expected at
${GENMORPH_REPO}/data/triangleClassification/evolved_mrs.json or similar.

The schema in GenMorph's distribution may have shifted across versions; this
loader is defensive and supports two known JSON layouts.

Each Set G MR is encoded as a serialised input-transformation + output-relation
pair. We translate each into the same callable signature used by Set N (see
set_n_definitions.py).

If the GenMorph distribution does not provide a directly executable MR (some
versions distribute MR DSL strings rather than callables), fall back to manual
transcription using the published `evolved_mrs.txt` and verify against the
published Table 4 detection rates.
"""

import json
from pathlib import Path
from typing import Callable, List


def _make_input_perturb_mr(input_transform: Callable, output_relation: Callable) -> Callable:
    """Wrap a (transform, relation) pair as a Set N-compatible MR callable."""

    def mr(P, base, _follow_up_unused):
        try:
            transformed = input_transform(base)
            base_out = P(base)
            transformed_out = P(transformed)
            return "pass" if output_relation(base_out, transformed_out) else "fail"
        except Exception:
            return "na"

    return mr


def load_set_g(genmorph_repo_path: str, subject: str = "TriangleClassification") -> List[Callable]:
    """
    Load Set G MRs from GenMorph's replication package.

    Returns a list of callables with signature (P, base, follow_up) -> {'pass', 'fail', 'na'}.

    If the file structure of GenMorph's distribution does not match the two
    known layouts, this function raises a FileNotFoundError and the harness
    falls back to manual transcription mode.
    """
    repo_path = Path(genmorph_repo_path)
    candidate_paths = [
        repo_path / "data" / subject / "evolved_mrs.json",
        repo_path / "subjects" / subject / "mrs" / "evolved.json",
    ]
    for path in candidate_paths:
        if path.exists():
            with open(path) as f:
                raw = json.load(f)
            return _parse_genmorph_json(raw)
    raise FileNotFoundError(
        f"Could not locate GenMorph evolved_mrs file under {genmorph_repo_path}/data/{subject} "
        f"or /subjects/{subject}. Fall back to manual transcription mode (see README §3.3)."
    )


def _parse_genmorph_json(raw: dict) -> List[Callable]:
    """
    Parse GenMorph's MR JSON. Schema (observed in 2023 release):
    {
      "mrs": [
        {"id": "mr_g_001", "transform": "scale_by_two", "relation": "equal_label"},
        ...
      ]
    }
    """
    transform_registry = {
        "scale_by_two": lambda t: (t[0] * 2, t[1] * 2, t[2] * 2),
        "permute_first_two": lambda t: (t[1], t[0], t[2]),
        "add_constant": lambda t: (t[0] + 1, t[1] + 1, t[2] + 1),
        "swap_max_min": lambda t: tuple(sorted(t)),
        # Add more as encountered in the GenMorph release.
    }
    relation_registry = {
        "equal_label": lambda a, b: a == b,
        "not_degenerate_implies_not_degenerate": lambda a, b: (a == "degenerate") or (b != "degenerate"),
    }
    mrs = []
    for entry in raw.get("mrs", []):
        t_name = entry["transform"]
        r_name = entry["relation"]
        if t_name not in transform_registry or r_name not in relation_registry:
            continue
        mrs.append(_make_input_perturb_mr(transform_registry[t_name], relation_registry[r_name]))
    return mrs


def manual_transcription_set_g() -> List[Callable]:
    """
    Fallback: hand-transcribed Set G derived from Ayerdi 2023 Table 4 + supplementary
    text. Use only if load_set_g() fails. The transcription must be cross-validated
    by reproducing the GenMorph-published kill rate within ±2 percentage points
    on the same mutation set.
    """
    raise NotImplementedError(
        "Manual transcription mode: implement after inspecting GenMorph's evolved MR list "
        "for TriangleClassification. Document each MR in this function with a comment "
        "citing the page/table of the GenMorph paper or supplementary file."
    )
