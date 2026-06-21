from . import context as ctx
from .context import runcommand, temp_obj
from .variables import score, BinaryOp, UnaryOp, getscore


def _compile_relational(node, invert=False):
    op_map = {"eq": ("if", "="), "ne": ("unless", "="), "lt": ("if", "<"), "le": ("if", "<="), "gt": ("if", ">"),
              "ge": ("if", ">=")}
    if node.op not in op_map:
        raise ValueError(f"Not a relational op: {node.op}")

    keyword, mcop = op_map[node.op]
    if invert:
        keyword = "unless" if keyword == "if" else "if"

    left, right = node.left, node.right

    if not isinstance(left, score):
        if isinstance(left, (int, float)):
            left = getscore(left)
        else:
            t = score(addr=f"!c{ctx._temp_id} {temp_obj}")
            ctx._temp_id += 1
            if isinstance(left, (BinaryOp, UnaryOp)):
                left._eval_into(t)
            else:
                t.__iset__(left)
            left = t

    if not isinstance(right, score):
        if isinstance(right, (int, float)):
            right = getscore(right, left.multiplier)
        else:
            t = score(addr=f"!c{ctx._temp_id} {temp_obj}", multiplier=left.multiplier)
            ctx._temp_id += 1
            if isinstance(right, (BinaryOp, UnaryOp)):
                right._eval_into(t)
            else:
                t.__iset__(right)
            right = t

    if left.multiplier != right.multiplier:
        t = score(addr=f"!c{ctx._temp_id} {temp_obj}", multiplier=left.multiplier)
        ctx._temp_id += 1
        t.__iset__(right)
        right = t

    return f"{keyword} score {left.addr} {mcop} {right.addr}"


def _eval_to_bool_score(node):
    dest = score(addr=f"!b{ctx._temp_id} {temp_obj}")
    ctx._temp_id += 1
    runcommand(f"scoreboard players set {dest.addr} 0")

    if isinstance(node, BinaryOp) and node.op == "or":
        left_conds = _flatten_and(node.left)
        runcommand(f"execute {' '.join(left_conds)} run scoreboard players set {dest.addr} 1")
        right_conds = _flatten_and(node.right)
        runcommand(
            f"execute if score {dest.addr} matches 0 {' '.join(right_conds)} run scoreboard players set {dest.addr} 1")
        return dest

    if isinstance(node, UnaryOp) and node.op == "not":
        sub_dest = _eval_to_bool_score(node.operand)
        runcommand(f"execute if score {sub_dest.addr} matches 0 run scoreboard players set {dest.addr} 1")
        return dest

    if isinstance(node, (BinaryOp, UnaryOp)):
        t = score(addr=f"!b{ctx._temp_id} {temp_obj}")
        ctx._temp_id += 1
        node._eval_into(t)
        runcommand(f"execute unless score {t.addr} matches 0 run scoreboard players set {dest.addr} 1")
        return dest

    if node:
        runcommand(f"scoreboard players set {dest.addr} 1")
    return dest


def _flatten_and(node, invert=False):
    if hasattr(node, "__branch__"):
        return node.__branch__(invert)

    dest = _eval_to_bool_score(node)
    keyword = "unless" if invert else "if"
    return [f"{keyword} score {dest.addr} matches 1"]
