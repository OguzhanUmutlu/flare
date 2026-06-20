import inspect
import json

from .command_parser import interpolate_command

files = {"main": []}
current_file = "main"
_current_namespace = "flare"
functions = {}
constants = {}
constant_obj = "__flare__constant__"
vars_obj = "__flare__vars__"
temp_obj = "__flare__temp__"
_temp_id = 0
_func_id = 0
_objective_offset = 0
_constant_offset = 0
_recursive_functions = set()
_in_recursive_context = False
return_types = {}
_logical_func = None


def reset_context():
    global files, current_file, _current_namespace, functions, constants, _temp_id, _func_id, _objective_offset, _constant_offset
    files = {"main": []}
    current_file = "main"
    _current_namespace = "flare"
    functions = {}
    constants = {}
    _temp_id = 0
    _func_id = 0
    _objective_offset = 0
    _constant_offset = 0
    _recursive_functions = set()
    _in_recursive_context = False
    return_types = {}
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


def namespace(name: str):
    global _current_namespace
    _current_namespace = name


def __float_prec(x: float) -> int:
    return len(str(x).split(".")[-1])


def runcommand(command: str, local_vars=None, global_vars=None):
    if local_vars is not None and global_vars is not None:
        command = interpolate_command(command, local_vars, global_vars)
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

        if hasattr(arg, '__icopy__') and getattr(type(arg), '__name__', '') in ("BinaryOp", "UnaryOp"):
            arg = arg.__icopy__(f"{_current_namespace}_temp_print_{i}")

        if isinstance(arg, score):
            if getattr(arg, 'multiplier', 1.0) != 1.0:
                scale_str = f"{arg.multiplier:.15f}".rstrip("0")
                if scale_str.endswith("."):
                    scale_str += "0"
                runcommand(
                    f"execute store result storage flare:temp __flare_debug_{i} double {scale_str} run scoreboard players get {arg.addr}")
                components.append({"nbt": f"__flare_debug_{i}", "storage": "flare:temp"})
            else:
                name, obj = arg.addr.split(" ", 1)
                components.append({"score": {"name": name, "objective": obj}})
        elif isinstance(arg, nbt):
            nbt_comp = {"nbt": arg.path or "{}"}
            if arg.path == "":
                nbt_comp["nbt"] = "{}"

            if arg.target_type == "storage":
                nbt_comp["storage"] = arg.target
            elif arg.target_type == "entity":
                nbt_comp["entity"] = arg.target
            elif arg.target_type == "block":
                nbt_comp["block"] = arg.target

            if arg.path == "":
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


def export(func=None, *, append=False):
    from flare import score  # avoid circular import
    if func is None:
        def wrapper(f):
            return export(f, append=append)

        return wrapper

    func_name = f"{_current_namespace}:{func.__name__}"
    if func_name in files and not append:
        raise ValueError(f"Function {func_name} already exists. Use @export(append=True) to append.")

    is_recursive = func.__name__ in _recursive_functions
    sig = inspect.signature(func)

    kwargs = {}

    for name, param in sig.parameters.items():
        anno = param.annotation

        if hasattr(anno, '__name__') and anno.__name__ in ('score', 'fixed', '_PrecisionScore'):
            if is_recursive:
                raise TypeError(
                    f"Recursive function '{func.__name__}' argument '{name}' needs a stack but it's a score.")
            if anno.__name__ == '_PrecisionScore' or anno.__name__ == 'fixed':
                kwargs[name] = anno(addr=f"{func.__name__}_{name} {vars_obj}")
            else:
                kwargs[name] = score(addr=f"{func.__name__}_{name} {vars_obj}")
        elif hasattr(anno, '__name__') and anno.__name__ in ('nbt', '_TypedNBT'):
            if is_recursive:
                kwargs[name] = anno(addr=f"storage flare:args {func.__name__}_{name}[-1]")
            else:
                kwargs[name] = anno(addr=f"storage flare:args {func.__name__}_{name}")
        elif anno is not inspect.Signature.empty:
            raise TypeError(f"Argument '{name}' must be typed as score or nbt, not {anno}")
        else:
            kwargs[name] = score(addr=f"{func.__name__}_{name} {vars_obj}")

    if sig.return_annotation is not inspect.Signature.empty:
        return_types[func_name] = sig.return_annotation
    else:
        return_types[func_name] = None

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
            for arg_name, arg_val in bound.arguments.items():
                target = kwargs[arg_name]

                if is_recursive and isinstance(target, nbt):
                    base_addr = f"storage flare:args {func.__name__}_{arg_name}"
                    if isinstance(arg_val, (int, float, str)):
                        runcommand(f"data modify {base_addr} append value {json.dumps(arg_val)}")
                    elif isinstance(arg_val, nbt):
                        runcommand(f"data modify {base_addr} append from {arg_val.addr}")
                    elif isinstance(arg_val, score):
                        runcommand(f"data modify {base_addr} append value 0")
                        runcommand(
                            f"execute store result {base_addr}[-1] int {1 / arg_val.multiplier} run scoreboard players get {arg_val.addr}")
                    elif hasattr(type(arg_val), "_eval_into"):
                        temp = nbt(addr=f"storage flare:temp !t{_temp_id}", datatype=target.type)
                        _temp_id += 1
                        arg_val._eval_into(temp)
                        runcommand(f"data modify {base_addr} append from {temp.addr}")
                else:
                    target.__iset__(arg_val)

            runcommand(f"function {func_name}")

            if is_recursive:
                for arg_name in bound.arguments.keys():
                    if isinstance(kwargs[arg_name], nbt):
                        base_addr = f"storage flare:args {func.__name__}_{arg_name}"
                        runcommand(f"data remove {base_addr}[-1]")

            ret_anno = sig.return_annotation
            if ret_anno is not inspect.Signature.empty:
                if hasattr(ret_anno, '__name__') and ret_anno.__name__ in ('score', 'fixed', '_PrecisionScore'):
                    temp_ret = score(addr=f"!ret{_temp_id} {temp_obj}")
                    _temp_id += 1
                    runcommand(
                        f"scoreboard players operation {temp_ret.addr} = {func_name.replace(':', '_')}_ret {vars_obj}")
                    if ret_anno.__name__ in ('fixed', '_PrecisionScore'):
                        pass
                    return temp_ret
                else:
                    temp_ret = nbt(addr=f"storage flare:temp !ret{_temp_id}")
                    _temp_id += 1
                    runcommand(
                        f"data modify {temp_ret.addr} set from storage flare:returns {func_name.replace(':', '_')}")
                    return temp_ret

    proxy = ProxyFunction()

    func_globals = getattr(func, '__globals__', {})
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

    return proxy


def _flare_assign(var_name, value, local_env, global_env):
    if var_name in local_env:
        target = local_env[var_name]
    elif var_name in global_env:
        target = global_env[var_name]
    else:
        target = None

    if target is not None and hasattr(target, "__iset__"):
        target.__iset__(value)
        return target

    if target is None and hasattr(value, "__icopy__"):
        if "is_recursive" in inspect.signature(value.__icopy__).parameters:
            return value.__icopy__(varid=f"{_current_namespace}_{var_name}", is_recursive=_in_recursive_context)
        return value.__icopy__(varid=f"{_current_namespace}_{var_name}")

    return value


def _flare_return(value):
    from .variables import score, nbt  # avoid circular import
    func_name = _logical_func
    if func_name is None:
        raise Exception("Return outside of exported function")
    ret_anno = return_types.get(func_name, None)

    if ret_anno is None:
        if value is not None:
            raise TypeError(f"Function {func_name} returned a value but has no return type annotation")
        return

    if hasattr(ret_anno, '__name__') and ret_anno.__name__ in ('score', 'fixed', '_PrecisionScore'):
        target = score(addr=f"{func_name.replace(':', '_')}_ret {vars_obj}")
        target.__iset__(value)
    else:
        if inspect.isclass(ret_anno) and issubclass(ret_anno, nbt):
            target = ret_anno(addr=f"storage flare:returns {func_name.replace(':', '_')}")
        else:
            datatype = None
            if hasattr(ret_anno, '__origin__') or isinstance(ret_anno, type):
                datatype = getattr(ret_anno, '__origin__', ret_anno)
            target = nbt(addr=f"storage flare:returns {func_name.replace(':', '_')}", datatype=datatype)
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
