import json
import re

from . import context as ctx
from .context import _runcmd
from .variables import score, BinaryOp, UnaryOp, getscore
from .variables.core import is_lazy, addr


def _compile_relational(node, invert=False):
    from .context import _emit_data_modify_from
    from .variables.nbt import nbt
    from .variables.core import is_lazy

    op_map = {"eq": ("if", "="), "ne": ("unless", "="), "lt": ("if", "<"), "le": ("if", "<="), "gt": ("if", ">"),
              "ge": ("if", ">=")}
    if node.op not in op_map:
        raise ValueError(f"Not a relational op: {node.op}")

    keyword, mcop = op_map[node.op]
    if invert:
        keyword = "unless" if keyword == "if" else "if"

    left, right = node.left, node.right

    def _peek_leaf(node):
        if isinstance(node, BinaryOp):
            return _peek_leaf(node.left)
        if isinstance(node, UnaryOp):
            return _peek_leaf(node.operand)
        if is_lazy(node) and hasattr(node, "operand") and node.operand is not None:
            return _peek_leaf(node.operand)
        return node

    left_leaf = _peek_leaf(left)
    right_leaf = _peek_leaf(right)

    is_nbt_op = (isinstance(left_leaf, nbt) or getattr(left_leaf, "_is_nbt_op", False) or isinstance(right_leaf,
                                                                                                     nbt) or getattr(
        right_leaf, "_is_nbt_op", False))
    if is_nbt_op and node.op in ("eq", "ne"):
        left_type = getattr(left, "_type", None)
        right_type = getattr(right, "_type", None)
        if left_type is not None and right_type is not None:
            if left_type != right_type:
                raise TypeError(f"Cannot compare NBT variables of different types: {left_type} and {right_type}")

        def _get_literal_value(v):
            if isinstance(v, (int, float, str, bool, dict, list)):
                return v
            return None

        nbt_var = None
        literal_val = None

        if isinstance(left, nbt) and _get_literal_value(right) is not None:
            nbt_var = left
            literal_val = _get_literal_value(right)
        elif isinstance(right, nbt) and _get_literal_value(left) is not None:
            nbt_var = right
            literal_val = _get_literal_value(left)

        if nbt_var is not None and literal_val is not None:
            path = nbt_var._path
            has_newline = isinstance(literal_val, str) and "\n" in literal_val
            if path != "" and re.match(r"^[\w\.]+$", path) and not has_newline:
                parts = path.split(".")
                match_dict = {parts[-1]: literal_val}
                for part in reversed(parts[:-1]):
                    match_dict = {part: match_dict}

                match_json = json.dumps(match_dict)
                is_eq = (node.op == "eq" and not invert) or (node.op == "ne" and invert)
                kw = "if" if is_eq else "unless"
                return f"{kw} data {nbt_var._target_type} {nbt_var._target} {match_json}"

        tmp_nbt_addr = f"storage {ctx.temp_storage} __nbt_cmp"
        tmp_score = score(addr=f"#n{ctx.next_temp_id()}")

        def _get_modify_cmd(target, source):
            if getattr(source, "_is_nbt_op", False):
                start_str = str(source.start) if source.start is not None else "0"
                stop_str = f" {source.stop}" if source.stop is not None else ""
                return f"data modify {target} set string {addr(source.operand)} {start_str}{stop_str}"
            if isinstance(source, nbt):
                return _emit_data_modify_from(target, "set", addr(source))
            elif isinstance(source, (dict, list, str, int, float, bool)):
                return f"data modify {target} set value {json.dumps(source)}"
            elif hasattr(source, "_addr"):
                return f"execute store result {target} int 1 run scoreboard players get {addr(source)}"
            else:
                raise TypeError(f"Cannot compare NBT with {type(source)}")

        if is_lazy(left):
            t = left._alloc_temp()
            left._compile_into(t)
            left = t

        if is_lazy(right):
            t = right._alloc_temp()
            right._compile_into(t)
            right = t

        _runcmd(_get_modify_cmd(tmp_nbt_addr, left))
        _runcmd(f"execute store success score {addr(tmp_score)} run {_get_modify_cmd(tmp_nbt_addr, right)}")

        condition = "0" if node.op == "eq" else "1.."
        keyword_to_use = "unless" if invert else "if"
        return f"{keyword_to_use} score {addr(tmp_score)} matches {condition}"

    node_op = node.op

    if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
        if isinstance(left, (int, float)):
            left, right = right, left
            swap_op = {"eq": "eq", "ne": "ne", "lt": "gt", "le": "ge", "gt": "lt", "ge": "le"}
            node_op = swap_op[node_op]

        if isinstance(right, (int, float)):
            if not isinstance(left, score):
                t = score(addr=f"#c{ctx.next_temp_id()}")
                if isinstance(left, (BinaryOp, UnaryOp)):
                    left._compile_into(t)
                else:
                    t[:] = left
                left = t

            val = int(round(right / left._multiplier))

            if node_op == "eq":
                match_str = str(val)
                kw = "unless" if invert else "if"
            elif node_op == "ne":
                match_str = str(val)
                kw = "if" if invert else "unless"
            elif node_op == "lt":
                match_str = f"..{val - 1}"
                kw = "unless" if invert else "if"
            elif node_op == "le":
                match_str = f"..{val}"
                kw = "unless" if invert else "if"
            elif node_op == "gt":
                match_str = f"{val + 1}.."
                kw = "unless" if invert else "if"
            elif node_op == "ge":
                match_str = f"{val}.."
                kw = "unless" if invert else "if"
            else:
                raise ValueError(f"Unknown operator: {node_op}")

            return f"{kw} score {addr(left)} matches {match_str}"

    if not isinstance(left, score):
        if isinstance(left, (int, float)):
            left = getscore(left)
        else:
            t = score(addr=f"#c{ctx.next_temp_id()}")
            if isinstance(left, (BinaryOp, UnaryOp)):
                left._compile_into(t)
            else:
                t[:] = left
            left = t

    if not isinstance(right, score):
        if isinstance(right, (int, float)):
            right = getscore(right, left._multiplier)
        else:
            t = score(addr=f"#c{ctx.next_temp_id()}", multiplier=left._multiplier)
            if isinstance(right, (BinaryOp, UnaryOp)):
                right._compile_into(t)
            else:
                t[:] = right
            right = t

    if left._multiplier != right._multiplier:
        t = score(addr=f"#c{ctx.next_temp_id()}", multiplier=left._multiplier)
        t[:] = right
        right = t

    return f"{keyword} score {addr(left)} {mcop} {addr(right)}"


def _eval_to_bool_score(node):
    dest = score(addr=f"#b{ctx.next_temp_id()}")
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
        t = score(addr=f"#b{ctx.next_temp_id()}")
        node._compile_into(t)
        _runcmd(f"execute unless score {addr(t)} matches 0 run scoreboard players set {addr(dest)} 1")
        return dest

    if is_lazy(node) or hasattr(node, "_addr"):
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
