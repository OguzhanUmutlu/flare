import json

_macro_substituted = False
import re

TOKEN_REGEX = re.compile(r'(?P<FSTRING>f\"(?:\\\\.|[^\\"])*\"|f\'(?:\\\\.|[^\\\'])*\')|'
                         r'(?P<STRING>\"(?:\\\\.|[^\\"])*\"|\'(?:\\\\.|[^\\\'])*\')|'
                         r'(?P<NUMBER>-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?(?:[dDfFsSbBL])?)|'
                         r'(?P<IDENTIFIER>[a-zA-Z_][a-zA-Z0-9_.\-]*)|'
                         r'(?P<SELECTOR>@[parse])|'
                         r'(?P<SYMBOL>[~^@{}\[\]:,=.!#$%&*+\-/<>?|\\`]+)|'
                         r'(?P<WHITESPACE>\s+)')


def interpolate_command(command: str, local_vars: dict, global_vars: dict) -> str:
    global _macro_substituted
    _macro_substituted = False
    tokens = []
    for match in TOKEN_REGEX.finditer(command):
        tokens.append({"type": match.lastgroup, "value": match.group(str(match.lastgroup)), "start": match.start(),
                       "end": match.end()})

    output = []
    bracket_depth = 0
    i = 0
    while i < len(tokens):
        tok = tokens[i]

        if tok["type"] == "FSTRING":
            try:
                val = eval(tok["value"], global_vars, local_vars)
                output.append(json.dumps(val))
            except:  # noqa
                output.append(tok["value"])

        elif tok["type"] == "WHITESPACE":
            if bracket_depth == 0:
                output.append(tok["value"])
            else:
                pass

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
                    output.append(inner)
                else:
                    output.append(val)
            else:
                output.append(val)

        elif tok["type"] == "IDENTIFIER":
            ident = tok["value"]

            is_key = False
            for j in range(i + 1, len(tokens)):
                if tokens[j]["type"] == "WHITESPACE":
                    continue
                if tokens[j]["type"] == "SYMBOL" and ":" in tokens[j]["value"]:
                    is_key = True
                break

            _resolved_val = local_vars.get(ident) if not is_key else None
            if _resolved_val is None and not is_key:
                _resolved_val = global_vars.get(ident)
            if _resolved_val is not None and getattr(_resolved_val, "_is_macro_param", False):
                output.append(f"$({_resolved_val.name})")
                _macro_substituted = True
                i += 1
                continue

            if ident in ("true", "false", "null", "run", "execute", "summon", "say", "as", "at", "positioned", "if",
                         "unless", "store", "result", "success"):
                output.append(ident)
            elif not is_key and ident in local_vars:
                val = local_vars[ident]
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
            elif not is_key and ident in global_vars:
                val = global_vars[ident]
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

        elif tok["type"] == "SYMBOL":
            val = tok["value"]
            for char in val:
                if char in "{[":
                    bracket_depth += 1
                elif char in "]}":
                    bracket_depth = max(0, bracket_depth - 1)
            output.append(val)

        else:
            output.append(tok["value"])

        i += 1

    return "".join(output)
