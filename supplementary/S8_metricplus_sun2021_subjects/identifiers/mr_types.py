"""Common MR datatype + evaluation harness."""
from dataclasses import dataclass, field
from typing import Callable, Any, Dict, List, Optional
import math


@dataclass
class MR:
    name: str
    block_or_pair: str        # NOETHER block (e.g. "O_le") or D×R pair (e.g. "(D1,R2)")
    transformer: Callable[[Dict[str, Any]], Optional[Dict[str, Any]]]
    relation: Callable[[Any, Any], bool]
    set_label: str = ""        # "N" for NOETHER, "MP" for METRIC+

    def evaluate(self, f: Callable, x: Dict[str, Any]) -> Optional[bool]:
        """Evaluate MR on input x using subject function f.

        Returns True if MR holds, False if violated, None if MR's
        transformer is out-of-domain on x (skip).
        """
        try:
            x_prime = self.transformer(x)
        except (ValueError, ZeroDivisionError, KeyError):
            return None
        if x_prime is None:
            return None
        try:
            # Strip metadata before calling f
            x_clean = {k: v for k, v in x.items() if not k.startswith("_")}
            x_prime_clean = {k: v for k, v in x_prime.items() if not k.startswith("_")}
            y = f(**x_clean)
            y_prime = f(**x_prime_clean)
        except (ValueError, ZeroDivisionError, KeyError):
            return None
        try:
            return self.relation(y, y_prime)
        except (ValueError, ZeroDivisionError, TypeError):
            return None


def approx_eq(a: float, b: float, rel: float = 1e-6, abs_tol: float = 1e-6) -> bool:
    """Floating-point equality with tolerance."""
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a.keys()) != set(b.keys()):
            return False
        return all(approx_eq(a[k], b[k], rel, abs_tol) for k in a)
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=rel, abs_tol=abs_tol)
    return a == b


def approx_le(a: float, b: float, abs_tol: float = 1e-6) -> bool:
    """a <= b with tolerance."""
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a.keys()) != set(b.keys()):
            return False
        return all(approx_le(a[k], b[k], abs_tol) for k in a)
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a <= b + abs_tol
    return a <= b


def approx_ge(a: float, b: float, abs_tol: float = 1e-6) -> bool:
    return approx_le(b, a, abs_tol)


def scale_outputs(y, k: float):
    """Multiply numeric output by k; recurse into dict."""
    if isinstance(y, dict):
        return {key: scale_outputs(v, k) for key, v in y.items()}
    if isinstance(y, (int, float)):
        return y * k
    return y
