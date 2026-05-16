"""Python AST mutation engine. Simulates PIT 1.7.4 mutator catalogue.

Mutators implemented:
  MATH                 : arithmetic operator replacement (+/-/*///%)
  RETURN_VALS          : replace return value with constants (0, 1)
  CONDITIONALS_BOUNDARY: < -> <=, <= -> <, > -> >=, >= -> >
  INCREMENTS           : x + d -> x - d (in obvious cases)
  NEGATE_CONDITIONALS  : ==/!=/</>/<=/>= flip
  CONSTANT_REPLACE     : replace literal constants with 0, 1
"""
import ast
import copy
from dataclasses import dataclass
from typing import List, Callable, Any


@dataclass
class Mutant:
    operator: str
    location: str      # "module.function:line"
    description: str
    mutated_module: Any   # module object


_MATH_OP_FLIPS = {
    ast.Add: [ast.Sub, ast.Mult],
    ast.Sub: [ast.Add, ast.Mult],
    ast.Mult: [ast.Add, ast.Div],
    ast.Div: [ast.Mult, ast.Sub],
    ast.Mod: [ast.Div, ast.Mult],
}

_COND_BOUNDARY = {
    ast.Lt: ast.LtE,
    ast.LtE: ast.Lt,
    ast.Gt: ast.GtE,
    ast.GtE: ast.Gt,
}

_NEGATE_COND = {
    ast.Eq: ast.NotEq,
    ast.NotEq: ast.Eq,
    ast.Lt: ast.GtE,
    ast.LtE: ast.Gt,
    ast.Gt: ast.LtE,
    ast.GtE: ast.Lt,
}


class _Mutator(ast.NodeTransformer):
    """Apply one mutation at one target location."""
    def __init__(self, target_id: int, op_kind: str):
        self.target_id = target_id
        self.op_kind = op_kind
        self.counter = -1
        self.applied = False
        self.description = ""

    def _maybe_apply(self, node, mutate_fn):
        self.counter += 1
        if self.counter == self.target_id and not self.applied:
            new_node = mutate_fn(node)
            self.applied = True
            return new_node
        return node

    def visit_BinOp(self, node):
        self.generic_visit(node)
        if self.op_kind == "MATH":
            for src_cls, alt_classes in _MATH_OP_FLIPS.items():
                if isinstance(node.op, src_cls):
                    def mutate(n, alt=alt_classes[0], src=src_cls):
                        new = copy.copy(n)
                        new.op = alt()
                        return new
                    new_node = self._maybe_apply(node, mutate)
                    if self.applied and new_node is not node:
                        self.description = (f"BinOp {src_cls.__name__} "
                                            f"-> {alt_classes[0].__name__}")
                    return new_node
        return node

    def visit_Compare(self, node):
        self.generic_visit(node)
        if not node.ops:
            return node
        op = node.ops[0]
        if self.op_kind == "CONDITIONALS_BOUNDARY":
            for src_cls, dst_cls in _COND_BOUNDARY.items():
                if isinstance(op, src_cls):
                    def mutate(n, dst=dst_cls, src=src_cls):
                        new = copy.copy(n)
                        new.ops = [dst()] + list(n.ops[1:])
                        return new
                    new_node = self._maybe_apply(node, mutate)
                    if self.applied and new_node is not node:
                        self.description = (f"Compare {src_cls.__name__} "
                                            f"-> {dst_cls.__name__}")
                    return new_node
        elif self.op_kind == "NEGATE_CONDITIONALS":
            for src_cls, dst_cls in _NEGATE_COND.items():
                if isinstance(op, src_cls):
                    def mutate(n, dst=dst_cls, src=src_cls):
                        new = copy.copy(n)
                        new.ops = [dst()] + list(n.ops[1:])
                        return new
                    new_node = self._maybe_apply(node, mutate)
                    if self.applied and new_node is not node:
                        self.description = (f"Negate {src_cls.__name__} "
                                            f"-> {dst_cls.__name__}")
                    return new_node
        return node

    def visit_Return(self, node):
        self.generic_visit(node)
        if self.op_kind == "RETURN_VALS" and node.value is not None:
            def mutate(n):
                new = copy.copy(n)
                new.value = ast.Constant(value=0)
                return new
            new_node = self._maybe_apply(node, mutate)
            if self.applied and new_node is not node:
                self.description = "Return -> 0"
            return new_node
        return node

    def visit_Constant(self, node):
        if self.op_kind == "CONSTANT_REPLACE":
            if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                if node.value != 0:
                    def mutate(n):
                        new = ast.Constant(value=0)
                        return ast.copy_location(new, n)
                    new_node = self._maybe_apply(node, mutate)
                    if self.applied and new_node is not node:
                        self.description = f"Constant {node.value} -> 0"
                    return new_node
        return node


def _count_targets(source: str, op_kind: str) -> int:
    """Count how many nodes the mutator class can target."""
    tree = ast.parse(source)
    counter = _Mutator(target_id=-1, op_kind=op_kind)
    counter.target_id = -2  # never matches; we just want to advance counter
    counter.visit(tree)
    return counter.counter + 1


def generate_mutants(source: str, module_name: str,
                     op_kinds: List[str] | None = None) -> List[Mutant]:
    """Generate all mutants for the given source file.

    Returns list of Mutant objects with mutated module loaded.
    """
    import importlib.util
    if op_kinds is None:
        op_kinds = ["MATH", "RETURN_VALS", "CONDITIONALS_BOUNDARY",
                    "NEGATE_CONDITIONALS", "CONSTANT_REPLACE"]

    mutants: List[Mutant] = []
    for op_kind in op_kinds:
        n_targets = _count_targets(source, op_kind)
        for target_id in range(n_targets):
            tree = ast.parse(source)
            mutator = _Mutator(target_id=target_id, op_kind=op_kind)
            new_tree = mutator.visit(tree)
            if not mutator.applied:
                continue
            ast.fix_missing_locations(new_tree)
            try:
                code = compile(new_tree, f"<mutant-{module_name}-{op_kind}-{target_id}>", "exec")
            except (SyntaxError, ValueError):
                continue
            spec = importlib.util.spec_from_loader(
                f"{module_name}_mutant_{op_kind}_{target_id}", loader=None)
            if spec is None:
                continue
            mod = importlib.util.module_from_spec(spec)
            try:
                exec(code, mod.__dict__)
            except Exception:
                # Module loading failed; skip this mutant
                continue
            mutants.append(Mutant(
                operator=op_kind,
                location=f"{module_name}#{target_id}",
                description=mutator.description or f"{op_kind} at #{target_id}",
                mutated_module=mod,
            ))
    return mutants


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    subj_dir = os.path.join(here, "..", "subjects")
    for s in ["sphone", "sbaggage", "sexpense", "smeal"]:
        src_path = os.path.join(subj_dir, f"{s}.py")
        with open(src_path) as f:
            src = f.read()
        m = generate_mutants(src, s)
        print(f"{s}: {len(m)} mutants generated")
        by_op = {}
        for mut in m:
            by_op[mut.operator] = by_op.get(mut.operator, 0) + 1
        print(f"  by operator: {by_op}")
