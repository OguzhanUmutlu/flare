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
        if isinstance(val, dict) or (hasattr(val, "_value_to_set") and isinstance(val._value_to_set, dict)):
            val_dict = val if isinstance(val, dict) else val._value_to_set
            items = []
            for k, v in val_dict.items():
                if not isinstance(k, (str, int, float, bool)):
                    raise TypeError("Invalid dict key for SNBT: " + str(type(k)))
                if isinstance(k, str) and not re.match(r'^[a-zA-Z0-9_\-.]+$', k):
                    k = json.dumps(k)
                v_str = json.dumps(v) if isinstance(v, (str, dict, list)) else str(v)
                items.append(f"{k}: {v_str}")
            return "{" + ", ".join(items) + "}"
        elif isinstance(val, list):
            return "[" + ", ".join(json.dumps(x) if isinstance(x, (str, dict, list)) else str(x) for x in val) + "]"
        elif hasattr(val, "addr") and type(val).__name__ != "_Storage":
            return val._addr
        elif hasattr(val, "target") and type(val).__name__ != "_Storage":
            return val.target
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

                        # Macro checks
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

                        # Macro checks
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
            open_bracket = command[i]
            close_bracket = '}' if open_bracket == '{' else ']'
            j = i + 1
            bracket_count = 1
            while j < n and bracket_count > 0:
                if command[j] == open_bracket:
                    bracket_count += 1
                elif command[j] == close_bracket:
                    bracket_count -= 1
                j += 1
            if bracket_count == 0:
                expr = command[start:j]
                try:
                    val = eval(expr, global_vars, local_vars)
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
