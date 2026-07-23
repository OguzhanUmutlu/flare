import builtins
import inspect
import json
import sys

from . import command_parser as _cp
from .command_parser import interpolate_command

_current_namespace: str = "flare"
files = {f"{_current_namespace}:__init__": []}
json_files = {}
resourcepack_textures = {}
current_file = f"{_current_namespace}:__init__"
functions = {}
constants = {}
return_targets = {}
recursive_locals = {}
_scope_stacks = []
_regex_cache = {}


class DynamicVar:
    def __init__(self, fmt):
        self.fmt = fmt

    def __str__(self):
        return self.fmt.format(ns=_current_namespace)

    def __format__(self, format_spec):
        return format(str(self), format_spec)

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)


constant_obj = DynamicVar("__{ns}__constant__")
vars_obj = DynamicVar("__{ns}__vars__")
temp_obj = DynamicVar("__{ns}__temp__")
temp_storage = DynamicVar("{ns}:__flare_temp__")
vars_storage = DynamicVar("{ns}:__flare_vars__")
args_storage = DynamicVar("{ns}:__flare_args__")
returns_storage = DynamicVar("{ns}:__flare_returns__")

_temp_id = 0
_func_id = 0
_objective_offset = 0
_constant_offset = 0
has_returns = {}
return_types = {}

_pending_exports = []
_pending_tags = []

tick_funcs = set()
load_funcs = set()
objectives = set()
_recursive_functions = set()

_in_recursive_context = False
_logical_func = None
memoized_math = {}

validation_level = "strict"
system_command_validation = "none"
minecraft_version = "1.20.4"
nbt_schema_missing = "error"


def next_temp_id():
    global _temp_id
    got = _temp_id
    _temp_id += 1
    return got


def next_temp_score(prefix: str = "t", **kwargs):
    from .variables.score import score

    return score(addr=f"#{prefix}_{next_temp_id()}", **kwargs)


def next_func_id():
    global _func_id
    got = _func_id
    _func_id += 1
    return got


def get_generated_func_name(prefix: str) -> str:
    global current_file, _current_namespace

    if current_file and ":" in current_file:
        ns, path = current_file.split(":", 1)
        if "/" in path:
            dir_path, filename = path.rsplit("/", 1)
            return f"{ns}:{dir_path}/_{filename}/{prefix}_{next_func_id()}"
        else:
            return f"{ns}:_{path}/{prefix}_{next_func_id()}"
    else:
        return f"{_current_namespace}:{prefix}_{next_func_id()}"


def reset_context():
    global current_file, _current_namespace, _temp_id, _func_id, _objective_offset, _constant_offset, validation_level, system_command_validation, minecraft_version, nbt_schema_missing, _in_recursive_context, _logical_func, memoized_math
    files.clear()
    json_files.clear()
    resourcepack_textures.clear()
    files[f"{_current_namespace}:__init__"] = []
    current_file = f"{_current_namespace}:__init__"
    _current_namespace = "flare"
    functions.clear()
    constants.clear()
    objectives.clear()
    tick_funcs.clear()
    load_funcs.clear()
    _temp_id = 0
    _func_id = 0
    _objective_offset = 0
    _constant_offset = 0
    _recursive_functions.clear()
    _in_recursive_context = False
    return_types.clear()
    has_returns.clear()
    return_targets.clear()
    _logical_func = None
    memoized_math.clear()
    _regex_cache.clear()
    _pending_exports.clear()
    _pending_tags.clear()


def evaluate_pending_exports():
    for func, tag_name, replace in _pending_tags:
        if hasattr(func, "_flare_proxy"):
            proxy = func._flare_proxy
        else:
            proxy = export(func)

        func_name = str(proxy)
        if ":" in tag_name:
            ns, path = tag_name.split(":", 1)
            key = f"{ns}:tags/functions/{path}.json"
        else:
            key = f"{_current_namespace}:tags/functions/{tag_name}.json"

        if key in json_files:
            existing = json_files[key]
            if "values" not in existing:
                existing["values"] = []
            if func_name not in existing["values"]:
                existing["values"].append(func_name)
            if replace:
                existing["replace"] = True
        else:
            json_files[key] = {"replace": replace, "values": [func_name]}

    _pending_tags.clear()

    while _pending_exports:
        eval_fn = _pending_exports.pop(0)
        eval_fn()


def ensure_objective(obj: str, obj_type: str = "dummy", display="", add: bool = True):
    global _objective_offset
    if not obj or obj in objectives:
        return

    objectives.add(obj)

    if not add:
        return

    load_file = f"{_current_namespace}:__constants__"
    if load_file not in files:
        files[load_file] = []

    cmd = f"scoreboard objectives add {obj} {obj_type}"
    if display:
        if isinstance(display, str):
            if display.startswith("{") and display.endswith("}"):
                display_str = display
            elif display.startswith('"') and display.endswith('"'):
                display_str = display
            else:
                display_str = json.dumps(display)
        elif hasattr(display, "__print__"):
            display_str = json.dumps(display.__print__())
        else:
            display_str = json.dumps(display)
        cmd += f" {display_str}"

    if cmd not in files[load_file]:
        files[load_file].insert(_objective_offset, cmd)
        _objective_offset += 1


def ensure_constant(name: str, obj: str, val: int):
    ensure_objective(obj)

    load_file = f"{_current_namespace}:__constants__"
    cmd = f"scoreboard players set {name} {obj} {val}"
    if cmd not in files[load_file]:
        files[load_file].append(cmd)


class _ContextManager:
    def __init__(self, new_file: str):
        self.new_file = new_file
        self.old_file = None

    def __enter__(self):
        global current_file
        self.old_file = current_file
        current_file = self.new_file

        if self.new_file not in files:
            files[self.new_file] = []

    def __exit__(self, exc_type, exc_val, exc_tb):
        global current_file
        current_file = self.old_file


def push_context(name: str):
    return _ContextManager(name)


def namespace(name: str | None = None):
    global _current_namespace, current_file
    if name is not None:
        old_init = f"{_current_namespace}:__init__"
        new_init = f"{name}:__init__"
        _current_namespace = name
        if old_init in files:
            files[new_init] = files.pop(old_init)
        if current_file == old_init:
            current_file = new_init
    return _current_namespace


from .validator import validate_command, FlareCommandValidationError


def _optimize_execute(cmd: str) -> str:
    if " run execute " not in cmd:
        return cmd
    result = []
    in_quote = None
    i = 0
    while i < len(cmd):
        if cmd[i] in "\"'":
            if in_quote == cmd[i]:
                in_quote = None
            elif not in_quote:
                in_quote = cmd[i]
            result.append(cmd[i])
        elif not in_quote and cmd[i: i + 13] == " run execute ":
            result.append(" ")
            i += 12
        else:
            result.append(cmd[i])
        i += 1
    return "".join(result)


def combine_execute(prefix: str, cmd: str) -> str:
    is_macro_cmd = cmd.startswith("$")
    is_macro_prefix = prefix.startswith("$")

    core_cmd = cmd[1:] if is_macro_cmd else cmd
    core_prefix = prefix[1:] if is_macro_prefix else prefix

    is_macro = is_macro_cmd or is_macro_prefix

    if core_cmd.startswith("execute "):
        res = f"{core_prefix} {core_cmd[8:]}"
    else:
        res = f"{core_prefix} run {core_cmd}"

    if is_macro:
        return f"${res}"
    return res


def runcommand(command: str, local_vars=None, global_vars=None, validation: str = None):
    dynamic_macros = []

    if "$(" in command and not command.startswith("$"):
        command = "$" + command

    if local_vars is not None and global_vars is not None:
        command = interpolate_command(command, local_vars, global_vars, dynamic_macros)
        if _cp._macro_substituted and not command.startswith("$"):
            command = "$" + command

    if dynamic_macros:
        func_name = f"{_current_namespace}:macro_{next_func_id()}"
        from .variables.nbt import nbt

        for name, val in dynamic_macros:
            temp_nbt = nbt(addr=f"storage flare:macro {name}")
            temp_nbt[:] = val

        with push_context(func_name):
            runcommand(command, validation=validation)

        _runcmd(f"function {func_name} with storage flare:macro", validation=validation)
        return

    _runcmd(command, validation=validation)


def _runcmd(command: str, validation: str = None):
    command = _optimize_execute(command)

    if validation is None:
        val_level = system_command_validation
    else:
        val_level = validation

    if val_level != "none":
        try:
            validate_command(command, minecraft_version)
        except FlareCommandValidationError as e:
            if val_level == "strict":
                raise e
            elif val_level == "warning":
                print(f"[Flare Compiler Warning] {e}")

    files[current_file].append(command)


def _check_entity_nbt_transfer(addr1: str, addr2: str) -> bool:
    if not isinstance(addr1, str) or not isinstance(addr2, str):
        return False
    if not addr1.startswith("entity ") or not addr2.startswith("entity "):
        return False

    def extract_selector(addr: str) -> str:
        s = addr[len("entity "):]
        if s.startswith("@") and len(s) > 2 and s[2] == "[":
            bracket_count = 0
            for i, c in enumerate(s):
                if c == "[":
                    bracket_count += 1
                elif c == "]":
                    bracket_count -= 1
                    if bracket_count == 0:
                        return s[: i + 1]
        return s.split(" ")[0]

    sel1 = extract_selector(addr1)
    sel2 = extract_selector(addr2)

    return sel1 and sel1 == sel2 and not sel1.startswith("@s")


def _emit_data_modify_from(target_addr: str, action: str, source_addr: str) -> str:
    if _check_entity_nbt_transfer(target_addr, source_addr):

        def extract_selector(addr: str) -> str:
            s = addr[len("entity "):]
            if s.startswith("@") and len(s) > 2 and s[2] == "[":
                bracket_count = 0
                for i, c in enumerate(s):
                    if c == "[":
                        bracket_count += 1
                    elif c == "]":
                        bracket_count -= 1
                        if bracket_count == 0:
                            return s[: i + 1]
            return s.split(" ")[0]

        sel = extract_selector(target_addr)
        t_path = target_addr[len("entity ") + len(sel):].strip()
        s_path = source_addr[len("entity ") + len(sel):].strip()

        return f"execute as {sel} run data modify entity @s {t_path} {action} from entity @s {s_path}"

    return f"data modify {target_addr} {action} from {source_addr}"


def dbg(*args):
    processed_str = " ".join(str(arg) for arg in args)
    builtins.print(processed_str)
    _flare_print(processed_str)


def _invoke_stdlib(func_name, generator, inputs=None, outputs=None, with_=None):
    if inputs is None:
        inputs = {}
    if outputs is None:
        outputs = {}

    safe_func_name = func_name.replace(":", "_")
    std_inputs = {k: type(v)(addr=f"#{safe_func_name}_{k} __flare_stdlib__") for k, v in inputs.items()}
    std_outputs = {k: type(v)(addr=f"#{safe_func_name}_{k} __flare_stdlib__") for k, v in outputs.items()}

    if func_name not in files:
        with push_context(func_name):
            generator(std_inputs, std_outputs)

    for k, v in inputs.items():
        std_inputs[k][:] = v
    with_cmd = ""
    if isinstance(with_, nbt):
        with_cmd = f" with {addr(with_)}"
    elif isinstance(with_, str):
        with_cmd = f" {with_}"
    _runcmd(f"function {func_name}{with_cmd}")
    for k, v in outputs.items():
        v[:] = std_outputs[k]


from .variables.score import score
from .variables.nbt import nbt
from .variables.core import is_lazy, addr, macro


class FlareReturnException(Exception):
    pass


class ReturnTypeStack:
    pass


from .print import style, hover_event, click_event, Color


def _flare_print(*args, sep: str = " ", color: str | int | Color | None = None, font: str | None = None,
                 bold: bool | None = None, italic: bool | None = None, underlined: bool | None = None,
                 strikethrough: bool | None = None, obfuscate: bool | None = None,
                 shadow_color: str | int | Color | None = None, insertion: str | None = None,
                 click_event: click_event | dict | None = None, hover_event: hover_event | dict | None = None):
    components = style(*args, color=color, font=font, bold=bold, italic=italic, underlined=underlined,
                       strikethrough=strikethrough, obfuscate=obfuscate, shadow_color=shadow_color, insertion=insertion,
                       click_event=click_event, hover_event=hover_event, sep=sep).__print__()
    while isinstance(components, list) and len(components) == 1:
        components = components[0]

    if len(components) == 1 and isinstance(components, dict) and "text" in components:
        cmd_text = json.dumps(components["text"])
    else:
        cmd_text = json.dumps(components)

    _runcmd(f"tellraw @a {cmd_text}")


def export(func=None, *, name=None, append=False, returns=None):
    from .variables.builtins import IntReturn

    if isinstance(func, str):
        name = func
        func = None

    if func is None:
        def wrapper(f):
            return export(f, name=name, append=append, returns=returns)

        return wrapper

    actual_name = name if name is not None else func.__name__
    if ":" in actual_name:
        func_name = actual_name
    else:
        func_name = f"{_current_namespace}:{actual_name}"
    if func_name in files and not append:
        raise ValueError(f"Function {func_name} already exists. Use @export(append=True) to append.")

    is_recursive = func.__name__ in _recursive_functions
    sig = inspect.signature(func)

    kwargs = {}

    for name, param in sig.parameters.items():
        anno = param.annotation

        if anno is macro or (isinstance(anno, type) and issubclass(anno, macro)):
            kwargs[name] = macro(name)
        elif hasattr(anno, "__name__") and anno.__name__ in ("score", "fixed", "_PrecisionScore"):
            if is_recursive:
                raise TypeError(
                    f"Recursive function '{func.__name__}' argument '{name}' needs a stack but it's a score.")
            if anno.__name__ == "_PrecisionScore" or anno.__name__ == "fixed":
                kwargs[name] = anno(addr=f"{func.__name__}_{name} {vars_obj}")
            else:
                kwargs[name] = score(addr=f"{func.__name__}_{name} {vars_obj}")
        elif hasattr(anno, "__name__") and anno.__name__ in ("nbt", "_TypedNBT"):
            if is_recursive:
                kwargs[name] = anno(addr=f"storage {args_storage} {func.__name__}_{name}[-1]")
            else:
                kwargs[name] = anno(addr=f"storage {args_storage} {func.__name__}_{name}")
        elif anno is not inspect.Signature.empty:
            raise TypeError(f"Argument '{name}' must be typed as score, nbt, or macro, not {anno}")
        else:
            kwargs[name] = score(addr=f"{func.__name__}_{name} {vars_obj}")

    if returns is not None:
        return_targets[func_name] = returns
        return_types[func_name] = type(returns)
    else:
        if sig.return_annotation is not inspect.Signature.empty:
            return_types[func_name] = sig.return_annotation
        else:
            return_types[func_name] = "UNKNOWN"
    has_returns[func_name] = False

    global _in_recursive_context, _logical_func
    prev_recursive = _in_recursive_context
    _in_recursive_context = is_recursive

    prev_logical = _logical_func
    _logical_func = func_name

    class ProxyFunction:
        __name__ = actual_name

        def __str__(self):
            return func_name

        @property
        def returns(self):
            if func_name in return_targets:
                return return_targets[func_name]

            ret_anno = return_types.get(func_name, sig.return_annotation)
            if ret_anno == int or ret_anno == "int":
                raise TypeError(f"Cannot access .returns on function '{func_name}' because it returns a raw int.")

            if hasattr(ret_anno, "__name__") and ret_anno.__name__ in ("score", "fixed", "_PrecisionScore"):
                target = score(addr=f"{func_name.replace(':', '_')}_ret {vars_obj}")
            else:
                if inspect.isclass(ret_anno) and issubclass(ret_anno, nbt):
                    target = ret_anno(addr=f"storage {returns_storage} {func_name.replace(':', '_')}")
                else:
                    datatype = None
                    if hasattr(ret_anno, "__origin__") or isinstance(ret_anno, type):
                        datatype = getattr(ret_anno, "__origin__", ret_anno)
                    target = nbt(addr=f"storage {returns_storage} {func_name.replace(':', '_')}", datatype=datatype)

            return_targets[func_name] = target
            return target

        @returns.setter
        def returns(self, value):
            self.returns.__iset__(value)

        def _write_non_macro_args(self, bound):
            global _temp_id

            for arg_name, arg_val in bound.arguments.items():
                target = kwargs[arg_name]
                if isinstance(target, macro):
                    continue
                if is_recursive and isinstance(target, nbt):
                    base_addr = f"storage {args_storage} {func.__name__}_{arg_name}"
                    if isinstance(arg_val, (int, float, str)):
                        _runcmd(f"data modify {base_addr} append value {json.dumps(arg_val)}")
                    elif isinstance(arg_val, nbt):
                        _runcmd(_emit_data_modify_from(base_addr, "append", addr(arg_val)))
                    elif isinstance(arg_val, score):
                        _runcmd(f"data modify {base_addr} append value 0")
                        _runcmd(
                            f"execute store result {base_addr}[-1] int {1 / arg_val._multiplier} run scoreboard players get {addr(arg_val)}")
                    elif is_lazy(arg_val):
                        temp = nbt(addr=f"storage {temp_storage} !t{_temp_id}", datatype=target._type)
                        _temp_id += 1
                        arg_val._compile_into(temp)
                        _runcmd(_emit_data_modify_from(base_addr, "append", addr(temp)))
                else:
                    target.__iset__(arg_val)

        def _emit_return(self):
            global _temp_id

            if func_name in return_targets:
                return return_targets[func_name]
            ret_anno = return_types.get(func_name, sig.return_annotation)
            if ret_anno == "UNKNOWN":
                return "UNKNOWN_RETURN"
            elif ret_anno is not inspect.Signature.empty and ret_anno is not None:
                if ret_anno == int or ret_anno == "int":
                    return IntReturn(func_name)
                elif hasattr(ret_anno, "__name__") and ret_anno.__name__ in ("score", "fixed", "_PrecisionScore"):
                    temp_ret = score(addr=f"#ret{_temp_id}")
                    _temp_id += 1
                    _runcmd(
                        f"scoreboard players operation {addr(temp_ret)} = {func_name.replace(':', '_')}_ret {vars_obj}")
                    return temp_ret
                else:
                    temp_ret = nbt(addr=f"storage {temp_storage} !ret{_temp_id}")
                    _temp_id += 1
                    _runcmd(_emit_data_modify_from(addr(temp_ret), "set",
                                                   f"storage {returns_storage} {func_name.replace(':', '_')}"))
                    return temp_ret

        def __call__(self, *args, **call_kwargs):
            global _temp_id
            from .variables.nbt import nbt

            macro_nbt = call_kwargs.pop("macro", None)

            if macro_nbt is not None:
                non_macro_params = [p for p in sig.parameters.values() if not isinstance(kwargs[p.name], macro)]
                new_sig = sig.replace(parameters=non_macro_params)
                bound = new_sig.bind(*args, **call_kwargs)
                bound.apply_defaults()

                self._write_non_macro_args(bound)

                if isinstance(macro_nbt, dict):
                    json_str = json.dumps(macro_nbt)
                    _runcmd(f"function {func_name} {json_str}")
                elif isinstance(macro_nbt, nbt):
                    macro_nbt._check_addr()
                    parts = [macro_nbt._target_type, macro_nbt._target]
                    if macro_nbt._path:
                        parts.append(macro_nbt._path)
                    with_src = " ".join(parts)
                    _runcmd(f"function {func_name} with {with_src}")
                else:
                    raise TypeError(f"macro= argument must be an nbt value or dict, got {type(macro_nbt).__name__}")
            else:
                bound = sig.bind(*args, **call_kwargs)
                bound.apply_defaults()

                macro_args = {}
                for arg_name, arg_val in bound.arguments.items():
                    if isinstance(kwargs[arg_name], macro):
                        macro_args[arg_name] = arg_val

                self._write_non_macro_args(bound)

                if macro_args:
                    all_literal = all(isinstance(v, (int, float, str, bool)) for v in macro_args.values())
                    if all_literal:
                        json_obj = {k: v for k, v in macro_args.items()}
                        _runcmd(f"function {func_name} {json.dumps(json_obj)}")
                    else:
                        storage_ns = _current_namespace
                        storage_path = f"{storage_ns}:__flare_macros__"
                        call_key = f"call_{_temp_id}"
                        _temp_id += 1
                        _runcmd(f"data modify storage {storage_path} {call_key} set value {{}}")
                        for k, v in macro_args.items():
                            if isinstance(v, (int, float, str, bool)):
                                val_str = json.dumps(v)
                                _runcmd(f"data modify storage {storage_path} {call_key}.{k} set value {val_str}")
                            else:
                                try:
                                    temp_arg = nbt(addr=f"storage {storage_path} {call_key}.{k}")
                                    temp_arg.__iset__(v)
                                except Exception as e:
                                    raise TypeError(
                                        f"Macro argument '{k}' cannot be initialized from {type(v).__name__}: {str(e)}")
                        _runcmd(f"function {func_name} with storage {storage_path} {call_key}")
                else:
                    _runcmd(f"function {func_name}")

            if is_recursive:
                for arg_name in bound.arguments.keys():
                    if isinstance(kwargs[arg_name], nbt):
                        base_addr = f"storage {args_storage} {func.__name__}_{arg_name}"
                        _runcmd(f"data remove {base_addr}[-1]")

                if func_name in recursive_locals:
                    for varid in recursive_locals[func_name]:
                        base_addr = f"storage {_current_namespace}:vars {varid}"
                        _runcmd(f"data remove {base_addr}[-1]")

            return self._emit_return()

        def with_(self, source_nbt, **call_kwargs):
            non_macro_bound_args = {}
            for arg_name, arg_val in call_kwargs.items():
                if arg_name not in kwargs:
                    raise TypeError(f"{func.__name__}() got unexpected keyword argument '{arg_name}'")
                if not isinstance(kwargs[arg_name], macro):
                    non_macro_bound_args[arg_name] = arg_val

            for arg_name, arg_val in non_macro_bound_args.items():
                target = kwargs[arg_name]
                target.__iset__(arg_val)

            if isinstance(source_nbt, nbt):
                source_nbt._check_addr()
                parts = [source_nbt._target_type, source_nbt._target]
                if source_nbt._path:
                    parts.append(source_nbt._path)
                with_src = " ".join(parts)
            else:
                raise TypeError(f"with_() source must be an nbt value, got {type(source_nbt).__name__}")

            _runcmd(f"function {func_name} with {with_src}")
            return self._emit_return()

    proxy = ProxyFunction()

    def _evaluate():
        global _in_recursive_context, _logical_func

        prev_recursive_inner = _in_recursive_context
        _in_recursive_context = is_recursive

        prev_logical_inner = _logical_func
        _logical_func = func_name

        with push_context(func_name):
            try:
                func(**kwargs)
            except FlareReturnException:
                pass

        _in_recursive_context = prev_recursive_inner
        _logical_func = prev_logical_inner

        if return_types[func_name] == "UNKNOWN":
            if has_returns.get(func_name, False):
                raise TypeError(
                    f"Function {func_name} has returns but return type could not be auto-detected. Please add an explicit return type annotation.")
            else:
                return_types[func_name] = None

    _pending_exports.append(_evaluate)

    if func is not None:
        func._flare_proxy = proxy

    return proxy


def tag(name: str, replace: bool = False):
    def wrapper(func):
        if func.__class__.__name__ == "ProxyFunction":
            func_name = str(func)

            if ":" in name:
                ns, path = name.split(":", 1)
                key = f"{ns}:tags/functions/{path}.json"
            else:
                key = f"{_current_namespace}:tags/functions/{name}.json"

            if key in json_files:
                existing = json_files[key]
                if "values" not in existing:
                    existing["values"] = []
                if func_name not in existing["values"]:
                    existing["values"].append(func_name)
                if replace:
                    existing["replace"] = True
            else:
                json_files[key] = {"replace": replace, "values": [func_name]}
        else:
            _pending_tags.append((func, name, replace))

        return func

    return wrapper


def _flare_in(item, container):
    if hasattr(container, "__in__"):
        return container.__in__(item)
    if hasattr(item, "__rin__"):
        res = item.__rin__(container)
        if res is not NotImplemented:
            return res
    return item in container


def _flare_enter_scope():
    _scope_stacks.append([])


def _flare_exit_scope():
    if _scope_stacks:
        for var in reversed(_scope_stacks.pop()):
            if hasattr(var, "__scope_exit__"):
                var.__scope_exit__()


def _flare_notin(item, container):
    if hasattr(container, "__notin__"):
        return container.__notin__(item)
    if hasattr(container, "__in__"):
        return ~container.__in__(item)
    if hasattr(item, "__rin__"):
        res = item.__rin__(container)
        if res is not NotImplemented:
            return ~res
    return item not in container


def _flare_alone(val):
    if hasattr(val, "__alone__"):
        val.__alone__()
    return val


def _flare_assign(var_name, value, local_env, global_env, is_local=False):
    from .variables.nbt import nbt

    target = None
    if is_local:
        target = local_env.get(var_name)
    else:
        frame = sys._getframe(1)
        while frame:
            if var_name in frame.f_locals:
                target = frame.f_locals[var_name]
                break
            frame = frame.f_back

        if target is None:
            if var_name in global_env:
                target = global_env[var_name]
    if target is not None and hasattr(target, "__iset__"):
        try:
            target.__iset__(value)
            return target
        except Exception:
            pass

    if target is None and hasattr(value, "__icopy__"):
        if "is_recursive" in inspect.signature(value.__icopy__).parameters:
            result = value.__icopy__(varid=f"{_current_namespace}_{var_name}", is_recursive=_in_recursive_context)
            if _in_recursive_context and _logical_func:
                if isinstance(result, nbt):
                    if _logical_func not in recursive_locals:
                        recursive_locals[_logical_func] = set()
                    recursive_locals[_logical_func].add(f"{_current_namespace}_{var_name}")
            if getattr(result, "_stack", False) and _scope_stacks:
                _scope_stacks[-1].append(result)
            return result

        result = value.__icopy__(varid=f"{_current_namespace}_{var_name}")
        if getattr(result, "_stack", False) and _scope_stacks:
            _scope_stacks[-1].append(result)
        return result

    return value


def _flare_aug_assign(var_name, op_name, value, _locals, _globals):
    var = None
    frame = sys._getframe(1)
    while frame:
        if var_name in frame.f_locals:
            var = frame.f_locals[var_name]
            break
        frame = frame.f_back

    if var is None:
        if var_name in _globals:
            var = _globals[var_name]
        else:
            raise NameError(f"name '{var_name}' is not defined")

    op_map = {"Add": "__iadd__", "Sub": "__isub__", "Mult": "__imul__", "Div": "__itruediv__", "Mod": "__imod__"}
    method_name = op_map.get(op_name)

    if hasattr(var, method_name):
        getattr(var, method_name)(value)
    else:
        if op_name == "Add":
            var += value
        elif op_name == "Sub":
            var -= value
        elif op_name == "Mult":
            var *= value
        elif op_name == "Div":
            var /= value
        elif op_name == "Mod":
            var %= value
        _flare_assign(var_name, var, _locals, _globals)

    return value


def _flare_return(value_fn):
    from .variables.score import addr
    from .variables.builtins import fail

    func_name = _logical_func
    if func_name is None:
        raise Exception("Return outside of exported function")

    if isinstance(value_fn, str) and value_fn == "UNKNOWN_RETURN":
        has_returns[func_name] = True
        return

    start_len = len(files.get(current_file, []))
    value = value_fn() if callable(value_fn) else value_fn

    if value is fail or isinstance(value, fail):
        _runcmd("return fail")
        return

    added_cmds = files.get(current_file, [])[start_len:]

    ret_anno = return_types.get(func_name, None)

    if ret_anno == "UNKNOWN":
        if hasattr(value, "_best_leaf"):
            leaf = value._best_leaf()
        else:
            leaf = value

        if leaf is None:
            ret_anno = type(None)
        elif hasattr(type(leaf), "__name__") and type(leaf).__name__ in ("score", "fixed", "_PrecisionScore", "nbt",
                                                                         "_TypedNBT"):
            ret_anno = type(leaf)
        elif isinstance(leaf, int):
            ret_anno = int
        else:
            raise TypeError(f"Cannot auto-detect return type from value of type {type(leaf)}")
        return_types[func_name] = ret_anno

    has_returns[func_name] = True

    if ret_anno is None or ret_anno == type(None):
        if value is not None:
            raise TypeError(f"Function {func_name} returned a value but has no return type annotation")
        _runcmd("return 1")
        return

    if ret_anno == int:
        if len(added_cmds) == 1:
            cmd = added_cmds[0]
            files[current_file].pop()
            _runcmd(f"return run {cmd}")
            return
        elif len(added_cmds) == 0 and isinstance(value, int):
            _runcmd(f"return {value}")
            return
        elif (len(added_cmds) == 0 and hasattr(type(value), "__name__") and type(value).__name__ == "score"):
            value._check_addr()
            _runcmd(f"return run scoreboard players get {addr(value)}")
            return
        else:
            raise TypeError(
                f"Function {func_name} has return type int but returned multiple commands or a non-integer value")

    if func_name in return_targets:
        target = return_targets[func_name]
        target.__iset__(value)
    elif hasattr(ret_anno, "__name__") and ret_anno.__name__ in ("score", "fixed", "_PrecisionScore"):
        target = score(addr=f"{func_name.replace(':', '_')}_ret {vars_obj}")
        target.__iset__(value)
    else:
        if inspect.isclass(ret_anno) and issubclass(ret_anno, nbt):
            target = ret_anno(addr=f"storage {returns_storage} {func_name.replace(':', '_')}")
        else:
            datatype = None
            if hasattr(ret_anno, "__origin__") or isinstance(ret_anno, type):
                datatype = getattr(ret_anno, "__origin__", ret_anno)
            target = nbt(addr=f"storage {returns_storage} {func_name.replace(':', '_')}", datatype=datatype)
        target.__iset__(value)

    _runcmd("return 1")


def tick(func=None, **kwargs):
    if func is None:
        def wrapper(f):
            return tick(f, **kwargs)

        return wrapper

    exported = export(**kwargs)(func)
    tick_funcs.add(f"{namespace()}:{kwargs.get('name', func.__name__)}")
    return exported


def load(func=None, **kwargs):
    if func is None:
        def wrapper(f):
            return load(f, **kwargs)

        return wrapper

    exported = export(**kwargs)(func)
    load_funcs.add(f"{namespace()}:{kwargs.get('name', func.__name__)}")
    return exported
