import json
import re

_macro_substituted = False

_static_interp_cache: dict[str, tuple[str, bool]] = {}

_op_cache: dict[str, list] = {}

TOKEN_REGEX = re.compile(r'(?P<FSTRING>f\"(?:\\\\.|[^\\"])*\"|f\'(?:\\\\.|[^\\\'])*\')|'
                         r'(?P<STRING>\"(?:\\\\.|[^\\"])*\"|\'(?:\\\\.|[^\\\'])*\')|'
                         r'(?P<NUMBER>-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?(?:[dDfFsSbBL])?)|'
                         r'(?P<IDENTIFIER>[a-zA-Z_][a-zA-Z0-9_.\-]*)|'
                         r'(?P<SELECTOR>@[parse])|'
                         r'(?P<SYMBOL>[~^@{}\[\]:,=.!#$%&*+\-/<>?|\\`]+)|'
                         r'(?P<WHITESPACE>\s+)')


def interpolate_command(command: str, local_vars: dict, global_vars: dict) -> str:
    global _macro_substituted

    cached = _static_interp_cache.get(command)
    if cached is not None:
        _macro_substituted = cached[1]
        return cached[0]

    ops = _op_cache.get(command)
    if ops is None:
        tokens = []
        for match in TOKEN_REGEX.finditer(command):
            tokens.append({"type": match.lastgroup, "value": match.group(str(match.lastgroup))})

        ops = []
        bracket_depth = 0
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            if tok["type"] == "FSTRING":
                ops.append(("fstring", tok["value"]))
            elif tok["type"] == "WHITESPACE":
                if bracket_depth == 0:
                    ops.append(("static", tok["value"]))
            elif tok["type"] == "STRING":
                is_key = False
                for j in range(i + 1, len(tokens)):
                    if tokens[j]["type"] == "WHITESPACE":
                        continue
                    if tokens[j]["type"] == "SYMBOL" and ":" in tokens[j]["value"]:
                        is_key = True
                    break

                val = tok["value"]
                if is_key:
                    inner = val[1:-1]
                    if re.match(r'^[a-zA-Z0-9_\-.]+$', inner):
                        ops.append(("static", inner))
                    else:
                        ops.append(("static", val))
                else:
                    ops.append(("static", val))
            elif tok["type"] == "SELECTOR":
                ops.append(("static", tok["value"].replace(" ", "")))
            elif tok["type"] == "IDENTIFIER":
                ident = tok["value"]
                is_key = False
                for j in range(i + 1, len(tokens)):
                    if tokens[j]["type"] == "WHITESPACE":
                        continue
                    if tokens[j]["type"] == "SYMBOL" and ":" in tokens[j]["value"]:
                        is_key = True
                    break

                if ident in ("true", "false", "null", "run", "execute", "summon", "say", "as", "at", "positioned", "if",
                             "unless", "store", "result", "success") or is_key:
                    ops.append(("static", ident))
                else:
                    ops.append(("ident", ident))
            elif tok["type"] == "SYMBOL":
                val = tok["value"]
                for char in val:
                    if char in "{[":
                        bracket_depth += 1
                    elif char in "]}":
                        bracket_depth = max(0, bracket_depth - 1)
                ops.append(("static", val))
            else:
                ops.append(("static", tok["value"]))
            i += 1

        collapsed_ops = []
        for op in ops:
            if op[0] == "static" and collapsed_ops and collapsed_ops[-1][0] == "static":
                collapsed_ops[-1] = ("static", collapsed_ops[-1][1] + op[1])
            else:
                collapsed_ops.append(op)
        ops = collapsed_ops
        _op_cache[command] = ops

    _macro_substituted = False
    _any_var_resolved = False
    output = []

    for op in ops:
        if op[0] == "static":
            output.append(op[1])
        elif op[0] == "fstring":
            try:
                val = eval(op[1], global_vars, local_vars)
                output.append(json.dumps(val))
            except:
                output.append(op[1])
        elif op[0] == "ident":
            ident = op[1]
            _resolved_val = local_vars.get(ident)
            if _resolved_val is None:
                _resolved_val = global_vars.get(ident)

            if _resolved_val is not None and getattr(_resolved_val, "_is_macro_param", False):
                output.append(f"$({_resolved_val.name})")
                _macro_substituted = True
                _any_var_resolved = True
            elif ident in local_vars:
                val = local_vars[ident]
                _any_var_resolved = True
                if hasattr(val, "addr"):
                    output.append(val._addr)
                elif hasattr(val, "target"):
                    output.append(val.target)
                elif isinstance(val, dict) and output and output[-1].endswith("**"):
                    output[-1] = output[-1][:-2]
                    items = []
                    for k, v in val.items():
                        if isinstance(k, str) and not re.match(r'^[a-zA-Z0-9_\-.]+$', k):
                            k = json.dumps(k)
                        v_str = json.dumps(v) if isinstance(v, (str, dict, list)) else str(v)
                        items.append(f"{k}: {v_str}")
                    output.append(", ".join(items))
                else:
                    output.append(str(val))
            elif ident in global_vars:
                val = global_vars[ident]
                _any_var_resolved = True
                if hasattr(val, "addr"):
                    output.append(val._addr)
                elif hasattr(val, "target"):
                    output.append(val.target)
                elif isinstance(val, dict) and output and output[-1].endswith("**"):
                    output[-1] = output[-1][:-2]
                    items = []
                    for k, v in val.items():
                        if isinstance(k, str) and not re.match(r'^[a-zA-Z0-9_\-.]+$', k):
                            k = json.dumps(k)
                        v_str = json.dumps(v) if isinstance(v, (str, dict, list)) else str(v)
                        items.append(f"{k}: {v_str}")
                    output.append(", ".join(items))
                else:
                    output.append(str(val))
            else:
                output.append(ident)

    result = "".join(output)

    if not _any_var_resolved:
        _static_interp_cache[command] = (result, _macro_substituted)

    return result
