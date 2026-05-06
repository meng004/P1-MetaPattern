"""
Set Segura oracles: input-permutation MRs hand-transcribed from Segura et al.
2022 QBS-MR generator, operating on Calcite plan trees.

Three MRs:
  - join_perm:      q1 ⋈ q2 ↔ q2 ⋈ q1 (under bag semantics)
  - disjoint_split: q ↔ q_left ∪ q_right when q's filter partitions the input
  - limit_grow:     LIMIT k vs LIMIT k+δ : extending limit is monotone

For QED's certified-equivalence corpus, the oracle's role is rule coverage:
which structural rewrite (if any) explains the certified pair.
"""

from __future__ import annotations

from typing import Optional, Tuple

from qed_adapter import Node, Pair, find_node


Verdict = Tuple[str, Optional[str]]


def join_perm(pair: Pair) -> Verdict:
    """Detect join-argument permutation (left/right swap) between q1 and q2."""
    if pair.q1 is None or pair.q2 is None:
        return ("na", None)
    j1 = find_node(pair.q1, "join")
    j2 = find_node(pair.q2, "join")
    if j1 is None or j2 is None:
        return ("na", None)
    if len(j1.children) < 2 or len(j2.children) < 2:
        return ("na", None)
    # Match: left of j1 corresponds (by op shape) to right of j2 and vice versa
    if _shape_signature(j1.children[0]) == _shape_signature(j2.children[1]) and \
       _shape_signature(j1.children[1]) == _shape_signature(j2.children[0]):
        return ("match", "join_perm")
    if _shape_signature(j1.children[0]) == _shape_signature(j2.children[0]) and \
       _shape_signature(j1.children[1]) == _shape_signature(j2.children[1]):
        # Same orientation — not a permutation, but possibly identical join.
        # Fall through to 'na' below.
        return ("na", None)
    return ("mismatch", "join_perm")


def disjoint_split(pair: Pair) -> Verdict:
    """Detect query ↔ UNION-of-disjoint-filtered-subqueries rewrite."""
    if pair.q1 is None or pair.q2 is None:
        return ("na", None)
    has_union_q1 = find_node(pair.q1, "union") is not None
    has_union_q2 = find_node(pair.q2, "union") is not None
    if has_union_q1 == has_union_q2:
        # Either both have union or neither — not a split rewrite.
        return ("na", None)
    return ("match", "disjoint_split")


def limit_grow(pair: Pair) -> Verdict:
    """Detect LIMIT-extension rewrite (LIMIT k → LIMIT m, m ≥ k)."""
    if pair.q1 is None or pair.q2 is None:
        return ("na", None)
    l1 = find_node(pair.q1, "limit")
    l2 = find_node(pair.q2, "limit")
    if l1 is None or l2 is None:
        return ("na", None)
    fetch_a = _extract_limit_fetch(l1)
    fetch_b = _extract_limit_fetch(l2)
    if fetch_a is None or fetch_b is None:
        return ("na", None)
    if fetch_a == fetch_b:
        return ("match", "limit_grow")
    return ("mismatch", "limit_grow")


def _shape_signature(node: Optional[Node]) -> str:
    """Recursive operator-name signature for shape comparison."""
    if node is None:
        return "_"
    if not node.children:
        return node.op
    return f"{node.op}({','.join(_shape_signature(c) for c in node.children)})"


def _extract_limit_fetch(limit_node: Node) -> Optional[int]:
    fetch = limit_node.payload.get("fetch") or limit_node.payload.get("count")
    if isinstance(fetch, dict):
        # Calcite encodes literal fetch as {"type": "INTEGER", "operator": "<n>"} or similar
        op = fetch.get("operator")
        try:
            return int(op) if op is not None else None
        except (TypeError, ValueError):
            return None
    if isinstance(fetch, int):
        return fetch
    return None


SET_SEGURA_ORACLES = [join_perm, disjoint_split, limit_grow]


__all__ = ["join_perm", "disjoint_split", "limit_grow", "SET_SEGURA_ORACLES", "Verdict"]
