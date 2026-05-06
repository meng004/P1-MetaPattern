"""
QED Calcite plan-JSON adapter.

The QED artifact (qed-solver/prover) ships 444 Calcite logical-plan pairs as
JSON files at tests/calcite/*.json. Each file has the schema:

    {
      "help":    [<text-rendered plan q1>, <text-rendered plan q2>],
      "schemas": [<table schema dicts>],
      "queries": [<plan-tree q1>, <plan-tree q2>]
    }

Each plan tree is a nested dict whose top-level operator key is one of:
  scan, project, filter, join, group, union, sort, limit, distinct
with operator-specific child keys. We represent each operator as a `Node`
named tuple for ergonomic pattern matching.

Ground truth: every QED test pair is by construction an equivalent rewrite
that Calcite's optimizer (or the test author) certifies. The pilot therefore
measures **rule coverage** (does our oracle recognise the rewrite class) on
a corpus of certified equivalences, not detection of equivalence vs.
inequivalence.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Iterator, List, Optional


OPERATOR_KEYS = {"scan", "project", "filter", "join", "group", "union", "sort", "limit", "distinct"}


@dataclass(frozen=True)
class Node:
    """Generic Calcite plan node — operator name + raw payload."""

    op: str
    payload: dict
    children: tuple

    def __repr__(self) -> str:
        kids = ", ".join(c.op for c in self.children)
        return f"Node({self.op}{'(' + kids + ')' if kids else ''})"


def _parse(node: Any) -> Optional[Node]:
    """Walk a plan-tree dict into a Node. Returns None for leaf scalars."""
    if not isinstance(node, dict):
        return None
    op_key = next((k for k in node if k in OPERATOR_KEYS), None)
    if op_key is None:
        return None
    body = node[op_key]
    if not isinstance(body, dict):
        return Node(op=op_key, payload={}, children=())

    children: List[Node] = []
    if op_key == "scan":
        return Node(op="scan", payload=body, children=())
    if op_key == "project":
        src = body.get("source")
        kid = _parse(src)
        if kid is not None:
            children.append(kid)
    elif op_key == "filter":
        src = body.get("source")
        kid = _parse(src)
        if kid is not None:
            children.append(kid)
    elif op_key == "join":
        for side in ("left", "right"):
            kid = _parse(body.get(side))
            if kid is not None:
                children.append(kid)
    elif op_key == "group":
        src = body.get("source")
        kid = _parse(src)
        if kid is not None:
            children.append(kid)
    elif op_key == "union":
        for k in ("left", "right", "sources", "operand"):
            v = body.get(k)
            if isinstance(v, list):
                for entry in v:
                    kid = _parse(entry)
                    if kid is not None:
                        children.append(kid)
            elif isinstance(v, dict):
                kid = _parse(v)
                if kid is not None:
                    children.append(kid)
    elif op_key in ("sort", "limit", "distinct"):
        src = body.get("source")
        kid = _parse(src)
        if kid is not None:
            children.append(kid)
    return Node(op=op_key, payload=body, children=tuple(children))


def parse_query(query_dict: dict) -> Optional[Node]:
    return _parse(query_dict)


@dataclass(frozen=True)
class Pair:
    pair_id: str
    q1: Optional[Node]
    q2: Optional[Node]
    schemas: tuple = field(default_factory=tuple)
    is_equivalent: bool = True
    raw: dict = field(default_factory=dict)


def load_pair(path: Path) -> Pair:
    with open(path) as fh:
        raw = json.load(fh)
    queries = raw.get("queries", [])
    q1 = parse_query(queries[0]) if queries else None
    q2 = parse_query(queries[1]) if len(queries) > 1 else None
    pair_id = path.stem
    name = pair_id.lower()
    is_equivalent = not any(tok in name for tok in ("disprove", "negative", "noteq", "nonequal"))
    return Pair(
        pair_id=pair_id,
        q1=q1,
        q2=q2,
        schemas=tuple(raw.get("schemas", [])),
        is_equivalent=is_equivalent,
        raw=raw,
    )


def iterate_calcite_pairs(qed_root: Path) -> Iterator[Path]:
    calcite_dir = qed_root / "tests" / "calcite"
    if not calcite_dir.exists():
        raise FileNotFoundError(f"QED Calcite test dir not found: {calcite_dir}")
    yield from sorted(calcite_dir.glob("*.json"))


# Helpers shared by the oracles
def _column_refs(condition: Any, accum: Optional[set] = None) -> set:
    """Collect all column-index references in a condition expression tree."""
    accum = set() if accum is None else accum
    if isinstance(condition, dict):
        if "column" in condition:
            try:
                accum.add(int(condition["column"]))
            except (TypeError, ValueError):
                pass
        for v in condition.values():
            _column_refs(v, accum)
    elif isinstance(condition, list):
        for v in condition:
            _column_refs(v, accum)
    return accum


def left_schema_width(join_node: Node) -> int:
    """Number of columns contributed by the left child of a join.

    Walks the left subtree and sums the column counts of all `scan` leaves;
    ignores intermediate `project` widening (we use the conservative
    union-of-scan-widths bound).
    """
    if join_node.op != "join":
        return 0

    width = 0

    def visit(n: Optional[Node]):
        nonlocal width
        if n is None:
            return
        if n.op == "scan":
            payload = n.payload
            # The plan JSON `scan` is sometimes just an int index into schemas.
            # We approximate by the explicit schema width if present in payload.
            if isinstance(payload, dict) and "fields" in payload:
                width += len(payload.get("fields", []))
            elif isinstance(payload, dict) and "types" in payload:
                width += len(payload.get("types", []))
            return
        for kid in n.children:
            visit(kid)

    visit(join_node.children[0]) if join_node.children else None
    return width


def has_pattern(node: Optional[Node], shape: Iterable[str]) -> bool:
    """Test whether `node` matches a top-down operator chain `shape`.

    Example: has_pattern(q, ["project", "filter", "join"]) returns True iff
    q is a project whose immediate (only) child is a filter whose immediate
    (only) child is a join.
    """
    if node is None:
        return False
    chain = list(shape)
    cur: Optional[Node] = node
    for op in chain:
        if cur is None or cur.op != op:
            return False
        cur = cur.children[0] if cur.children else None
    return True


def find_node(node: Optional[Node], op: str) -> Optional[Node]:
    """Depth-first search for the first node with the given operator name."""
    if node is None:
        return None
    if node.op == op:
        return node
    for kid in node.children:
        found = find_node(kid, op)
        if found is not None:
            return found
    return None
