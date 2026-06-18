import json

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


def runcommand(command: str):
    files[current_file].append(command)


import builtins


def dbg(*args):
    processed_str = " ".join(str(arg) for arg in args)
    builtins.print(processed_str)
    _flare_print(*args)


def _flare_print(*args):
    from .variables import score, nbt  # to avoid circular import
    components = []
    for i, arg in enumerate(args):
        if i > 0:
            components.append({"text": " "})

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
    if func is None:
        def wrapper(f):
            return export(f, append=append)

        return wrapper

    func_name = f"{_current_namespace}:{func.__name__}"
    if func_name in files and not append:
        raise ValueError(f"Function {func_name} already exists. Use @export(append=True) to append.")

    with push_context(func_name):
        func()

    return func


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
        return value.__icopy__(varid=f"{_current_namespace}_{var_name}")

    return value


def tick(func=None):
    if func is None:
        def wrapper(f):
            return tick(f)

        return wrapper

    func_name = f"{_current_namespace}:tick"
    with push_context(func_name):
        func()
    return func
