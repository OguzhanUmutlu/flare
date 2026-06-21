import inspect
import json

from .command_parser import interpolate_command

def addr(var):
    return var._addr

files = {"main": []}
current_file = "main"
_current_namespace = "flare"
functions = {}
constants = {}


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
_recursive_functions = set()
_in_recursive_context = False
return_types = {}
has_returns = {}
_logical_func = None

validation_level = "strict"
minecraft_version = "1.20.4"
nbt_schema_missing = "error"


def next_temp_id():
    global _temp_id
    got = _temp_id
    _temp_id += 1
    return got


def next_func_id():
    global _func_id
    got = _func_id
    _func_id += 1
    return got


def reset_context():
    global current_file, _current_namespace, _temp_id, _func_id, _objective_offset, _constant_offset, validation_level, minecraft_version, nbt_schema_missing, _in_recursive_context, _logical_func
    files.clear()
    files["main"] = []
    current_file = "main"
    _current_namespace = "flare"
    functions.clear()
    constants.clear()
    _temp_id = 0
    _func_id = 0
    _objective_offset = 0
    _constant_offset = 0
    _recursive_functions.clear()
    _in_recursive_context = False
    return_types.clear()
    has_returns.clear()
    _logical_func = None


def ensure_objective(obj: str):
    global _objective_offset, _constant_offset
    if not obj:
        return

    load_file = f"{_current_namespace}:load"
    if load_file not in files:
        files[load_file] = []

    cmd = f"scoreboard objectives add {obj} dummy"
    if cmd not in files[load_file]:
        files[load_file].insert(_objective_offset, cmd)
        _objective_offset += 1
        _constant_offset += 1


def ensure_constant(name: str, obj: str, val: int):
    global _constant_offset
    ensure_objective(obj)

    load_file = f"{_current_namespace}:load"
    cmd = f"scoreboard players set {name} {obj} {val}"
    if cmd not in files[load_file]:
        files[load_file].insert(_constant_offset, cmd)
        _constant_offset += 1


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
    global _current_namespace
    if name is not None:
        _current_namespace = name
    return _current_namespace


from .validator import validate_command, FlareCommandValidationError


def runcommand(command: str, local_vars=None, global_vars=None):
    if local_vars is not None and global_vars is not None:
        command = interpolate_command(command, local_vars, global_vars)

    if validation_level != "none":
        try:
            validate_command(command, minecraft_version)
        except FlareCommandValidationError as e:
            if validation_level == "strict":
                raise e
            elif validation_level == "warning":
                print(f"[Flare Compiler Warning] {e}")

    files[current_file].append(command)


import builtins


def dbg(*args):
    processed_str = " ".join(str(arg) for arg in args)
    builtins.print(processed_str)
    _flare_print(*args)


def _flare_print(*args):
    from .variables import score, nbt  # avoid circular import
    components = []
    for i, arg in enumerate(args):
        if i > 0:
            components.append({"text": " "})

        if hasattr(arg, "__icopy__") and getattr(type(arg), "__name__", "") in ("BinaryOp", "UnaryOp"):
            global _temp_id
            arg = arg.__icopy__(f"!print_{_temp_id}")
            _temp_id += 1

        if isinstance(arg, score):
            if getattr(arg, "multiplier", 1.0) != 1.0:
                scale_str = f"{arg._multiplier:.15f}".rstrip("0")
                if scale_str.endswith("."):
                    scale_str += "0"
                runcommand(
                    f"execute store result storage {temp_storage} __flare_debug_{i} double {scale_str} run scoreboard players get {addr(arg)}")
                components.append({"nbt": f"__flare_debug_{i}", "storage": str(temp_storage)})
            else:
                name, obj = arg._addr.split(" ", 1)
                components.append({"score": {"name": name, "objective": obj}})
        elif isinstance(arg, nbt):
            nbt_comp = {"nbt": arg._path or "{}"}
            if arg._path == "":
                nbt_comp["nbt"] = "{}"

            if arg._target_type == "storage":
                nbt_comp["storage"] = arg._target
            elif arg._target_type == "entity":
                nbt_comp["entity"] = arg._target
            elif arg._target_type == "block":
                nbt_comp["block"] = arg._target

            if arg._path == "":
                nbt_comp["nbt"] = "{}"

            components.append(nbt_comp)
        else:
            components.append({"text": str(arg)})

    if len(components) == 1:
        comp = components[0]
        if "text" in comp and len(comp) == 1:
            cmd_text = json.dumps(comp["text"])
        else:
            cmd_text = json.dumps(comp)
    else:
        cmd_text = json.dumps(components)

    runcommand(f"tellraw @a {cmd_text}")


def export(func=None, *, name=None, append=False):
    from flare import score  # avoid circular import

    if isinstance(func, str):
        name = func
        func = None

    if func is None:
        def wrapper(f):
            return export(f, name=name, append=append)

        return wrapper

    actual_name = name if name is not None else func.__name__
    func_name = f"{_current_namespace}:{actual_name}"
    if func_name in files and not append:
        raise ValueError(f"Function {func_name} already exists. Use @export(append=True) to append.")

    is_recursive = func.__name__ in _recursive_functions
    sig = inspect.signature(func)

    kwargs = {}

    for name, param in sig.parameters.items():
        anno = param.annotation

        if hasattr(anno, "__name__") and anno.__name__ in ("score", "fixed", "_PrecisionScore"):
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
            raise TypeError(f"Argument '{name}' must be typed as score or nbt, not {anno}")
        else:
            kwargs[name] = score(addr=f"{func.__name__}_{name} {vars_obj}")

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
        def __call__(self, *args, **call_kwargs):
            from .variables import score, nbt  # avoid circular import
            global _temp_id
            bound = sig.bind(*args, **call_kwargs)
            bound.apply_defaults()
            from .variables.core import addr
            for arg_name, arg_val in bound.arguments.items():
                target = kwargs[arg_name]

                if is_recursive and isinstance(target, nbt):
                    base_addr = f"storage {args_storage} {func.__name__}_{arg_name}"
                    if isinstance(arg_val, (int, float, str)):
                        runcommand(f"data modify {base_addr} append value {json.dumps(arg_val)}")
                    elif isinstance(arg_val, nbt):
                        runcommand(f"data modify {base_addr} append from {addr(arg_val)}")
                    elif isinstance(arg_val, score):
                        runcommand(f"data modify {base_addr} append value 0")
                        runcommand(
                            f"execute store result {base_addr}[-1] int {1 / arg_val._multiplier} run scoreboard players get {addr(arg_val)}")
                    elif hasattr(type(arg_val), "_eval_into"):
                        temp = nbt(addr=f"storage {temp_storage} !t{_temp_id}", datatype=target._type)
                        _temp_id += 1
                        arg_val._eval_into(temp)
                        runcommand(f"data modify {base_addr} append from {addr(temp)}")
                else:
                    target.__iset__(arg_val)

            runcommand(f"function {func_name}")

            if is_recursive:
                for arg_name in bound.arguments.keys():
                    if isinstance(kwargs[arg_name], nbt):
                        base_addr = f"storage {args_storage} {func.__name__}_{arg_name}"
                        runcommand(f"data remove {base_addr}[-1]")

            ret_anno = return_types.get(func_name, sig.return_annotation)
            if ret_anno == "UNKNOWN":
                return "UNKNOWN_RETURN"
            elif ret_anno is not inspect.Signature.empty and ret_anno is not None:
                if hasattr(ret_anno, "__name__") and ret_anno.__name__ in ("score", "fixed", "_PrecisionScore"):
                    temp_ret = score(addr=f"!ret{_temp_id} {temp_obj}")
                    _temp_id += 1
                    runcommand(
                        f"scoreboard players operation {addr(temp_ret)} = {func_name.replace(":", "_")}_ret {vars_obj}")
                    if ret_anno.__name__ in ("fixed", "_PrecisionScore"):
                        pass
                    return temp_ret
                else:
                    temp_ret = nbt(addr=f"storage {temp_storage} !ret{_temp_id}")
                    _temp_id += 1
                    runcommand(
                        f"data modify {addr(temp_ret)} set from storage {returns_storage} {func_name.replace(':', '_')}")
                    return temp_ret

    proxy = ProxyFunction()

    func_globals = getattr(func, "__globals__", {})
    prev_func = func_globals.get(func.__name__)
    func_globals[func.__name__] = proxy

    with push_context(func_name):
        func(**kwargs)

    _in_recursive_context = prev_recursive
    _logical_func = prev_logical

    if prev_func is not None:
        func_globals[func.__name__] = prev_func
    else:
        func_globals.pop(func.__name__, None)

    if return_types[func_name] == "UNKNOWN":
        if has_returns.get(func_name, False):
            raise TypeError(
                f"Function {func_name} has returns but return type could not be auto-detected. Please add an explicit return type annotation.")
        else:
            return_types[func_name] = None

    return proxy


def _flare_in(item, container):
    if hasattr(container, "__in__"):
        return container.__in__(item)
    return item in container

def _flare_notin(item, container):
    if hasattr(container, "__notin__"):
        return container.__notin__(item)
    if hasattr(container, "__in__"):
        return ~container.__in__(item)
    return item not in container

def _flare_assign(var_name, value, local_env, global_env):
    if var_name in local_env:
        target = local_env[var_name]
    elif var_name in global_env:
        target = global_env[var_name]
    else:
        target = None

    if target is not None and hasattr(target, "__iset__"):
        try:
            target.__iset__(value)
            return target
        except Exception:
            pass

    if target is None and hasattr(value, "__icopy__"):
        if "is_recursive" in inspect.signature(value.__icopy__).parameters:
            return value.__icopy__(varid=f"{_current_namespace}_{var_name}", is_recursive=_in_recursive_context)
        return value.__icopy__(varid=f"{_current_namespace}_{var_name}")

    return value


def _flare_aug_assign(var_name, op_name, value, _locals, _globals):
    if var_name in _locals:
        var = _locals[var_name]
    elif var_name in _globals:
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


def _flare_return(value):
    from .variables import score, nbt  # avoid circular import
    func_name = _logical_func
    if func_name is None:
        raise Exception("Return outside of exported function")
    ret_anno = return_types.get(func_name, None)

    if isinstance(value, str) and value == "UNKNOWN_RETURN":
        has_returns[func_name] = True
        return

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
        else:
            raise TypeError(f"Cannot auto-detect return type from value of type {type(leaf)}")
        return_types[func_name] = ret_anno

    has_returns[func_name] = True

    if ret_anno is None or ret_anno == type(None):
        if value is not None:
            raise TypeError(f"Function {func_name} returned a value but has no return type annotation")
        return

    if hasattr(ret_anno, "__name__") and ret_anno.__name__ in ("score", "fixed", "_PrecisionScore"):
        target = score(addr=f"{func_name.replace(":", "_")}_ret {vars_obj}")
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

    runcommand("return 1")


def tick(func=None):
    if func is None:
        def wrapper(f):
            return tick(f)

        return wrapper

    func_name = f"{_current_namespace}:tick"
    with push_context(func_name):
        func()
    return func
