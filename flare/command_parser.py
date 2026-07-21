import json
import re

_macro_substituted = False
_dynamic_macros = []

_static_interp_cache: dict[str, tuple[str, bool]] = {}

_op_cache: dict[str, list] = {}

TOKEN_REGEX = re.compile(r'(?P<FSTRING>f\"(?:\\\\.|[^\\"])*\"|f\'(?:\\\\.|[^\\\'])*\')|'
                         r'(?P<STRING>\"(?:\\\\.|[^\\"])*\"|\'(?:\\\\.|[^\\\'])*\')|'
                         r'(?P<NUMBER>-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?(?:[dDfFsSbBL])?)|'
                         r'(?P<IDENTIFIER>[a-zA-Z_][a-zA-Z0-9_.\-:/]*)|'
                         r'(?P<SELECTOR>@[parse])|'
                         r'(?P<SYMBOL>[~^@{}\[\]:,=.!#$%&*+\-/<>?|\\`]+)|'
                         r'(?P<WHITESPACE>\s+)')


def interpolate_command(command: str, local_vars: dict, global_vars: dict, dynamic_macros: list = None) -> str:
    global _macro_substituted
    from .context import next_temp_id

    cached = _static_interp_cache.get(command)
    if cached is not None:
        _macro_substituted = cached[1]
        return cached[0]

    def format_val(val):
        global _macro_substituted
        nonlocal _any_var_resolved

        if getattr(val, "_is_macro_param", False) is True:
            _macro_substituted = True
            _any_var_resolved = True
            return f"$({val.name})"
        elif dynamic_macros is not None and type(val).__name__ in ("score", "nbt", "_TypedNBT", "fixed",
                                                                   "_PrecisionScore"):
            temp_name = f"arg_{next_temp_id()}"
            dynamic_macros.append((temp_name, val))
            _macro_substituted = True
            _any_var_resolved = True
            return f"$({temp_name})"
        elif isinstance(val, dict) or (hasattr(val, "_value_to_set") and isinstance(val._value_to_set, dict)):
            _any_var_resolved = True
            val_dict = val if isinstance(val, dict) else val._value_to_set
            items = []
            for k, v in val_dict.items():
                if not isinstance(k, (str, int, float, bool)):
                    raise TypeError("Invalid dict key for SNBT: " + str(type(k)))
                if isinstance(k, str) and not re.match(r'^[a-zA-Z0-9_\-.]+$', k):
                    k_str = json.dumps(k)
                else:
                    k_str = str(k)
                v_str = format_val(v)
                items.append(f"{k_str}: {v_str}")
            return "{" + ", ".join(items) + "}"
        elif isinstance(val, (list, tuple)):
            _any_var_resolved = True
            items = [format_val(x) for x in val]
            return "[" + ", ".join(items) + "]"
        elif isinstance(val, bool):
            return "true" if val else "false"
        elif isinstance(val, (int, float)):
            return str(val)
        elif isinstance(val, str):
            if val.startswith("$(") and val.endswith(")"):
                return val
            return json.dumps(val)
        elif hasattr(val, "addr") and type(val).__name__ != "_Storage":
            _any_var_resolved = True
            return str(val._addr)
        elif hasattr(val, "target") and type(val).__name__ != "_Storage":
            _any_var_resolved = True
            return str(val.target)
        return str(val)

    _macro_substituted = False
    _any_var_resolved = False
    output = []

    i = 0
    n = len(command)

    while i < n:
        if command[i] == '\\':
            if i + 1 < n and command[i + 1] in ('$', '{', '['):
                output.append(command[i + 1])
                i += 2
                continue
            else:
                output.append('\\')
                i += 1
                continue
        elif command[i] == '$':
            if i + 1 < n and command[i + 1] == '{':
                start = i + 2
                j = start
                bracket_count = 1
                while j < n and bracket_count > 0:
                    if command[j] == '{':
                        bracket_count += 1
                    elif command[j] == '}':
                        bracket_count -= 1
                    j += 1
                if bracket_count == 0:
                    expr = command[start:j - 1]
                    try:
                        val = eval(expr, global_vars, local_vars)

                        if getattr(val, "_is_macro_param", False) is True:
                            output.append(f"$({val.name})")
                            _macro_substituted = True
                            _any_var_resolved = True
                        elif dynamic_macros is not None and type(val).__name__ in ("score", "nbt", "_TypedNBT", "fixed",
                                                                                   "_PrecisionScore"):
                            temp_name = f"arg_{next_temp_id()}"
                            dynamic_macros.append((temp_name, val))
                            output.append(f"$({temp_name})")
                            _macro_substituted = True
                            _any_var_resolved = True
                        else:
                            _any_var_resolved = True
                            if isinstance(val, (dict, list)):
                                output.append(format_val(val))
                            else:
                                output.append(format_val(val))
                    except Exception as e:
                        output.append("${" + expr + "}")
                    i = j
                    continue
            else:
                m = re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*', command[i + 1:])
                if m:
                    var = m.group(0)
                    try:
                        val = eval(var, global_vars, local_vars)

                        if getattr(val, "_is_macro_param", False) is True:
                            output.append(f"$({val.name})")
                            _macro_substituted = True
                            _any_var_resolved = True
                        elif dynamic_macros is not None and type(val).__name__ in ("score", "nbt", "_TypedNBT", "fixed",
                                                                                   "_PrecisionScore"):
                            temp_name = f"arg_{next_temp_id()}"
                            dynamic_macros.append((temp_name, val))
                            output.append(f"$({temp_name})")
                            _macro_substituted = True
                            _any_var_resolved = True
                        else:
                            _any_var_resolved = True
                            output.append(format_val(val))
                    except Exception as e:
                        output.append("$" + var)
                    i += 1 + len(var)
                    continue
        elif command[i] in ('{', '['):
            start = i
            j = i
            bracket_counts = {'{': 0, '[': 0, '(': 0}
            bracket_matches = {'}': '{', ']': '[', ')': '('}
            in_string = False
            escape = False
            while j < n:
                c = command[j]
                if escape:
                    escape = False
                    j += 1
                    continue
                if c == '\\':
                    escape = True
                    j += 1
                    continue
                if c in ('"', "'"):
                    if in_string == c:
                        in_string = False
                    elif not in_string:
                        in_string = c
                    j += 1
                    continue
                if not in_string:
                    if c in bracket_counts:
                        bracket_counts[c] += 1
                    elif c in bracket_matches:
                        opener = bracket_matches[c]
                        if bracket_counts[opener] > 0:
                            bracket_counts[opener] -= 1
                    if j > start and sum(bracket_counts.values()) == 0:
                        j += 1
                        break
                j += 1

            if j > start and sum(bracket_counts.values()) == 0:
                expr = command[start:j]
                try:
                    eval_expr = re.sub(r'\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}', r'\1', expr)
                    eval_expr = re.sub(r'\$([a-zA-Z_][a-zA-Z0-9_]*)', r'\1', eval_expr)
                    val = eval(eval_expr, global_vars, local_vars)
                    if isinstance(val, (dict, list)) or (
                            hasattr(val, "_value_to_set") and isinstance(val._value_to_set, dict)):
                        output.append(format_val(val))
                        _any_var_resolved = True
                    else:
                        output.append(expr)
                except Exception as e:
                    output.append(expr)
                i = j
                continue

        output.append(command[i])
        i += 1

    result = "".join(output)

    if not _any_var_resolved:
        _static_interp_cache[command] = (result, _macro_substituted)

    return result
