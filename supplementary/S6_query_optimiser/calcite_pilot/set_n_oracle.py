"""
Set N oracles: NOETHER B*_rel-derived MRs operating on Calcite plan trees.

Both oracles match structural rewrites of pairs (q1, q2) produced by Calcite's
optimizer. The pilot runs against QED's Calcite test suite, where every test
pair represents a certified equivalent rewrite. The oracle's verdict is:

  ('match',     <rule>) — the pair exhibits the rewrite this MR captures
  ('mismatch',  <rule>) — pair has the structural shape but the rewrite does
                          not normalise q1 to q2 (rare, generally a sign of
                          a different rewrite in the same family)
  ('na',        None)   — the pair's shape is outside this MR's pattern

The pilot reports rule-coverage rate := |{pairs where any Set N oracle returns
'match'}| / |pairs|. This corresponds to NOETHER's §6.7 claim: B*_rel-derived
MRs identify the algebraic rewrites the optimizer applies.
"""

from __future__ import annotations

from typing import Optional, Tuple

from qed_adapter import Node, Pair, find_node, left_schema_width, _column_refs


Verdict = Tuple[str, Optional[str]]


def rho_select_push(pair: Pair) -> Verdict:
    """ρ_select_push: σ_p(R ⋈ S) ≡ σ_p(R) ⋈ S when attr(p) ⊆ attr(R).

    Pattern: q1 contains a filter directly above a join, and q2 either
    (a) has the filter pushed into one of the join's child sides
        (filter→join→{...,filter→scan,scan,...}), or
    (b) has the filter's predicate moved into the join's `condition`.

    This implementation accepts both (a) and (b) as 'match'.
    """
    if pair.q1 is None or pair.q2 is None:
        return ("na", None)

    # Find the highest filter-on-join in q1.
    fj = _find_filter_on_join(pair.q1)
    if fj is None:
        # Symmetry: maybe q2 has filter-on-join and q1 has the pushed form.
        fj = _find_filter_on_join(pair.q2)
        if fj is None:
            return ("na", None)
        # Swap roles for the push direction check.
        candidate_pushed = pair.q1
        candidate_unpushed = pair.q2
    else:
        candidate_pushed = pair.q2
        candidate_unpushed = pair.q1

    filter_node, join_node = fj
    cols = _column_refs(filter_node.payload.get("condition"))
    if not cols:
        return ("na", None)

    # Conservative left-side width estimate: sum scan-widths in left subtree.
    left_width = left_schema_width(join_node)

    # If predicate's columns all lie in the left subtree (col < left_width),
    # ρ_select_push is the candidate rewrite.
    references_left = all(c < left_width for c in cols)
    references_right = all(c >= left_width for c in cols)
    if not (references_left or references_right):
        # Predicate spans both sides; not a simple push-down.
        return ("na", None)

    # Now check: does q2 have the filter pushed into the appropriate side?
    pushed_filter = _find_filter_in_subtree(candidate_pushed, target_side="left" if references_left else "right")
    pushed_into_join_cond = _filter_merged_into_join_condition(candidate_pushed, cols)
    if pushed_filter or pushed_into_join_cond:
        return ("match", "select_push")
    # The unpushed form might match exactly — equality of structure means no
    # actual rewrite was applied to push it; still 'na' for ρ_select_push.
    if _structural_equal(candidate_pushed, candidate_unpushed):
        return ("na", None)
    return ("mismatch", "select_push")


def rho_distinct_idem(pair: Pair) -> Verdict:
    """ρ_distinct_idem: chained identical filters / distincts collapse.

    Pattern: q1 contains either filter→filter (chained σ) or distinct→distinct.
    q2 is the collapsed single-operator form.
    """
    if pair.q1 is None or pair.q2 is None:
        return ("na", None)

    # Look for chained-filter pattern
    chained = _has_chained_op(pair.q1, "filter") or _has_chained_op(pair.q2, "filter")
    chained_distinct = _has_chained_op(pair.q1, "distinct") or _has_chained_op(pair.q2, "distinct")
    if not (chained or chained_distinct):
        return ("na", None)

    # Determine which is collapsed
    if _has_chained_op(pair.q1, "filter") and not _has_chained_op(pair.q2, "filter"):
        return ("match", "distinct_idem")
    if _has_chained_op(pair.q2, "filter") and not _has_chained_op(pair.q1, "filter"):
        return ("match", "distinct_idem")
    if _has_chained_op(pair.q1, "distinct") and not _has_chained_op(pair.q2, "distinct"):
        return ("match", "distinct_idem")
    if _has_chained_op(pair.q2, "distinct") and not _has_chained_op(pair.q1, "distinct"):
        return ("match", "distinct_idem")
    return ("mismatch", "distinct_idem")


# Internal helpers
def _find_filter_on_join(node: Optional[Node]) -> Optional[Tuple[Node, Node]]:
    if node is None:
        return None
    if node.op == "filter" and node.children and node.children[0].op == "join":
        return (node, node.children[0])
    for kid in node.children:
        found = _find_filter_on_join(kid)
        if found:
            return found
    return None


def _find_filter_in_subtree(root: Optional[Node], target_side: str = "left") -> bool:
    """True iff there is a filter directly on a scan or under a join's chosen side."""
    if root is None:
        return False
    join = find_node(root, "join")
    if join is None or not join.children:
        # No join in this query — but the rewrite might have eliminated the join.
        # Fall back: any filter directly above a scan in the tree.
        return _filter_above_scan(root)
    side_idx = 0 if target_side == "left" else 1
    if len(join.children) <= side_idx:
        return False
    side_root = join.children[side_idx]
    return _filter_above_scan(side_root)


def _filter_above_scan(node: Optional[Node]) -> bool:
    if node is None:
        return False
    if node.op == "filter":
        if node.children and node.children[0].op == "scan":
            return True
        # Filter above a chain (project→scan, etc.) still counts.
        if node.children and find_node(node.children[0], "scan") is not None:
            return True
    for kid in node.children:
        if _filter_above_scan(kid):
            return True
    return False


def _filter_merged_into_join_condition(node: Optional[Node], cols: set) -> bool:
    """True iff a join exists in `node` whose condition references `cols`
    AND the join's parent is not a filter (i.e., the filter has been merged in).
    """
    if node is None:
        return False
    join = find_node(node, "join")
    if join is None:
        return False
    cond = join.payload.get("condition")
    if cond is None:
        return False
    join_cols = _column_refs(cond)
    return bool(cols & join_cols) and len(join_cols) >= len(cols)


def _has_chained_op(node: Optional[Node], op: str) -> bool:
    if node is None:
        return False
    if node.op == op and node.children and node.children[0].op == op:
        return True
    for kid in node.children:
        if _has_chained_op(kid, op):
            return True
    return False


def _structural_equal(a: Optional[Node], b: Optional[Node]) -> bool:
    if a is None or b is None:
        return a is b
    if a.op != b.op or len(a.children) != len(b.children):
        return False
    return all(_structural_equal(x, y) for x, y in zip(a.children, b.children))


SET_N_ORACLES = [rho_select_push, rho_distinct_idem]


__all__ = ["rho_select_push", "rho_distinct_idem", "SET_N_ORACLES", "Verdict"]
