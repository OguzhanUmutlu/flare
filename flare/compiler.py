import json

from . import context as ctx
from .context import _runcmd, temp_obj
from .variables import score, BinaryOp, UnaryOp, getscore
from .variables.core import addr


def _compile_relational(node, invert=False):
    from .variables.nbt import nbt
    op_map = {"eq": ("if", "="), "ne": ("unless", "="), "lt": ("if", "<"), "le": ("if", "<="), "gt": ("if", ">"),
              "ge": ("if", ">=")}
    if node.op not in op_map:
        raise ValueError(f"Not a relational op: {node.op}")

    keyword, mcop = op_map[node.op]
    if invert:
        keyword = "unless" if keyword == "if" else "if"

    left, right = node.left, node.right

    is_nbt_op = isinstance(left, nbt) or getattr(left, "_is_nbt_op", False) or isinstance(right, nbt) or getattr(right,
                                                                                                                 "_is_nbt_op",
                                                                                                                 False)
    if is_nbt_op and node.op in ("eq", "ne"):
        left_type = getattr(left, "_type", None)
        right_type = getattr(right, "_type", None)
        if left_type is not None and right_type is not None:
            if left_type != right_type:
                raise TypeError(f"Cannot compare NBT variables of different types: {left_type} and {right_type}")

        tmp_nbt_addr = f"storage {ctx.temp_storage} __nbt_cmp"
        tmp_score = score(addr=f"!n{ctx.next_temp_id()} {temp_obj}")

        def _get_modify_cmd(target, source):
            if getattr(source, "_is_nbt_op", False):
                start_str = str(source.start) if source.start is not None else "0"
                stop_str = f" {source.stop}" if source.stop is not None else ""
                return f"data modify {target} set string {addr(source.operand)} {start_str}{stop_str}"
            elif isinstance(source, nbt):
                return f"data modify {target} set from {addr(source)}"
            elif isinstance(source, (dict, list, str, int, float, bool)):
                return f"data modify {target} set value {json.dumps(source)}"
            else:
                raise TypeError(f"Cannot compare NBT with {type(source)}")

        _runcmd(_get_modify_cmd(tmp_nbt_addr, left))
        _runcmd(f"execute store success score {addr(tmp_score)} run {_get_modify_cmd(tmp_nbt_addr, right)}")

        condition = "0" if node.op == "eq" else "1.."
        keyword_to_use = "unless" if invert else "if"
        return f"{keyword_to_use} score {addr(tmp_score)} matches {condition}"

    if not isinstance(left, score):
        if isinstance(left, (int, float)):
            left = getscore(left)
        else:
            t = score(addr=f"!c{ctx.next_temp_id()} {temp_obj}")
            if isinstance(left, (BinaryOp, UnaryOp)):
                left._eval_into(t)
            else:
                t[:] = left
            left = t

    if not isinstance(right, score):
        if isinstance(right, (int, float)):
            right = getscore(right, left._multiplier)
        else:
            t = score(addr=f"!c{ctx.next_temp_id()} {temp_obj}", multiplier=left._multiplier)
            if isinstance(right, (BinaryOp, UnaryOp)):
                right._eval_into(t)
            else:
                t[:] = right
            right = t

    if left._multiplier != right._multiplier:
        t = score(addr=f"!c{ctx.next_temp_id()} {temp_obj}", multiplier=left._multiplier)
        t[:] = right
        right = t

    return f"{keyword} score {addr(left)} {mcop} {addr(right)}"


def _eval_to_bool_score(node):
    dest = score(addr=f"!b{ctx.next_temp_id()} {temp_obj}")
    _runcmd(f"scoreboard players set {addr(dest)} 0")

    if isinstance(node, BinaryOp) and node.op == "or":
        left_conds = _flatten_and(node.left)
        _runcmd(f"execute {' '.join(left_conds)} run scoreboard players set {addr(dest)} 1")
        right_conds = _flatten_and(node.right)
        _runcmd(
            f"execute if score {addr(dest)} matches 0 {' '.join(right_conds)} run scoreboard players set {addr(dest)} 1")
        return dest

    if isinstance(node, UnaryOp) and node.op == "not":
        sub_dest = _eval_to_bool_score(node.operand)
        _runcmd(f"execute if score {addr(sub_dest)} matches 0 run scoreboard players set {addr(dest)} 1")
        return dest

    if isinstance(node, (BinaryOp, UnaryOp)):
        t = score(addr=f"!b{ctx.next_temp_id()}")
        node._eval_into(t)
        _runcmd(f"execute unless score {addr(t)} matches 0 run scoreboard players set {addr(dest)} 1")
        return dest

    if hasattr(type(node), "_eval_into") or hasattr(node, "_addr"):
        _runcmd(f"execute unless score {addr(node)} matches 0 run scoreboard players set {addr(dest)} 1")
        return dest

    if node:
        _runcmd(f"scoreboard players set {addr(dest)} 1")
    return dest


def _flatten_and(node, invert=False):
    if hasattr(node, "__branch__"):
        return node.__branch__(invert)

    dest = _eval_to_bool_score(node)
    keyword = "unless" if invert else "if"
    return [f"{keyword} score {addr(dest)} matches 1"]
