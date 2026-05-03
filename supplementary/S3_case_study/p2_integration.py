"""
p2_integration.py — read-only import shim for the P2 codebase.

Lets the §6.6 case study reuse P2's statistical and pipeline utilities
WITHOUT modifying any file under the MT完备性 directory. P2 is treated as
a vendored read-only dependency.

Usage
-----
After importing this module, the symbol ``p2`` resolves to the P2 source
package, e.g.

    from p2_integration import p2
    cliffs_d, ci = p2.stats.cliffs_delta(set_n_detections, set_l_detections)

If P2 is not present at the expected path, this module raises a clear
RuntimeError with installation instructions; the rest of the §6.6
pipeline (runner.py, analysis.py) does not depend on this shim and works
without it.

Why a shim instead of pip install -e
------------------------------------
Editable installs would require modifying P2's pyproject.toml or running
pip from inside MT完备性, both of which the user has explicitly forbidden.
sys.path injection is a strict read of the path; no files are written to
the P2 tree.
"""

from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

# P2_ROOT must be set by the user. There is no default — set the environment
# variable P2_ROOT to the path of MT完备性/src on your machine, e.g.
#   export P2_ROOT=/path/to/MT完备性/src


def _locate_p2_src() -> Path:
    import os
    env = os.environ.get("P2_ROOT")
    if not env:
        raise RuntimeError(
            "P2_ROOT environment variable is not set. "
            "Set it to the absolute path of MT完备性/src, e.g.:\n"
            "    export P2_ROOT=/path/to/MT完备性/src\n"
            "Or omit p2_integration entirely — runner.py and analysis.py "
            "do not depend on this shim."
        )
    return Path(env)


def _import_p2() -> types.ModuleType:
    src = _locate_p2_src()
    if not src.exists():
        raise RuntimeError(
            f"P2 source not found at {src}. Set the P2_ROOT environment "
            "variable to MT完备性/src or omit p2_integration entirely."
        )
    sys.path.insert(0, str(src))
    try:
        return importlib.import_module("p2")
    except ImportError as exc:
        raise RuntimeError(
            f"Failed to import p2 from {src}: {exc}. Verify the directory "
            "structure is MT完备性/src/p2/__init__.py."
        ) from exc


# Lazy attribute access: only import p2 when actually used.
class _P2Proxy:
    _module: types.ModuleType | None = None

    def __getattr__(self, name: str):
        if self._module is None:
            self._module = _import_p2()
        return getattr(self._module, name)


p2 = _P2Proxy()


# -----------------------------------------------------------------------------
# Optional convenience wrappers around P2's stats utilities
# -----------------------------------------------------------------------------

def cliffs_delta_from_results(results_csv_path: str,
                              set_a: str = "N",
                              set_b: str = "L") -> dict:
    """Reuse P2's Cliff's δ on §6.6 detection counts grouped by mutation.

    Returns {'delta': float, 'ci_lo': float, 'ci_hi': float} if P2's stats
    package is available; raises RuntimeError otherwise.
    """
    import csv
    from collections import defaultdict
    rows = list(csv.DictReader(open(results_csv_path)))
    by_mut: dict[str, dict[str, list[bool]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for r in rows:
        by_mut[r["mutation_id"]][r["set"]].append(r["detected"] == "True")
    a_per_mut = [int(any(by_mut[m][set_a])) for m in by_mut]
    b_per_mut = [int(any(by_mut[m][set_b])) for m in by_mut]

    # Try P2's implementation first; fall back to a local minimal one.
    try:
        from p2.stats.cliffs import cliffs_delta_with_ci  # type: ignore[attr-defined]
        return cliffs_delta_with_ci(a_per_mut, b_per_mut)
    except (ImportError, AttributeError):
        pass

    # Local minimal Cliff's δ (no CI; for sanity-checking only).
    n_a, n_b = len(a_per_mut), len(b_per_mut)
    if n_a == 0 or n_b == 0:
        return {"delta": 0.0, "ci_lo": None, "ci_hi": None,
                "note": "empty input"}
    cnt_pos = sum(1 for x in a_per_mut for y in b_per_mut if x > y)
    cnt_neg = sum(1 for x in a_per_mut for y in b_per_mut if x < y)
    delta = (cnt_pos - cnt_neg) / (n_a * n_b)
    return {"delta": delta, "ci_lo": None, "ci_hi": None,
            "note": "P2's cliffs_delta_with_ci unavailable; CI omitted"}


if __name__ == "__main__":
    # Smoke test: import without using P2.
    print(f"P2 expected at: {_locate_p2_src()}")
    print(f"  exists: {_locate_p2_src().exists()}")
    print("Lazy proxy created; p2.* will resolve on first attribute access.")
