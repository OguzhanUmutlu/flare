from . import context as ctx
from .compiler import _flatten_and
from .context import push_context, runcommand, temp_obj
from .execute_modifiers import ExecuteChain
from .variables import score


def _flare_break():
    runcommand(f"scoreboard players set !break {temp_obj} 1")
    runcommand("return 0")


def _flare_continue():
    runcommand("return 0")


def _flare_if(*args):
    n = len(args) // 2
    conditions = args[:n]
    bodies = args[n:]

    sometemp = None
    has_else_or_elif = len(conditions) > 1 or conditions[0] is None

    if has_else_or_elif:
        sometemp = score(addr=f"!elif{ctx._temp_id} {temp_obj}")
        ctx._temp_id += 1
        runcommand(f"scoreboard players set {sometemp.addr} 0")

    for cond_func, body_func in zip(conditions, bodies):
        if cond_func is None:
            if sometemp is not None:
                func_name = f"{ctx._current_namespace}:generated_{ctx._func_id}"
                ctx._func_id += 1
                with push_context(func_name):
                    body_func()
                if ctx.files[func_name]:
                    if len(ctx.files[func_name]) == 1:
                        cmd = ctx.files[func_name][0]
                        del ctx.files[func_name]
                        if cmd.startswith("execute "):
                            runcommand(f"execute if score {sometemp.addr} matches 0 {cmd[8:]}")
                        else:
                            runcommand(f"execute if score {sometemp.addr} matches 0 run {cmd}")
                    else:
                        ctx.files[func_name].append("return 0")
                        ret_temp = score(addr=f"!ret{ctx._temp_id} {temp_obj}")
                        ctx._temp_id += 1
                        runcommand(
                            f"execute store result score {ret_temp.addr} if score {sometemp.addr} matches 0 run function {func_name}")
                        runcommand(f"execute if score {ret_temp.addr} matches 1 run return 1")
            else:
                body_func()
            break

        cond = cond_func()
        if isinstance(cond, bool):
            if cond is False:
                continue
            else:
                if sometemp is not None:
                    func_name = f"{ctx._current_namespace}:generated_{ctx._func_id}"
                    ctx._func_id += 1
                    with push_context(func_name):
                        body_func()
                    if ctx.files.get(func_name):
                        if len(ctx.files[func_name]) == 1:
                            cmd = ctx.files[func_name][0]
                            del ctx.files[func_name]
                            if cmd.startswith("execute "):
                                runcommand(f"execute if score {sometemp.addr} matches 0 {cmd[8:]}")
                            else:
                                runcommand(f"execute if score {sometemp.addr} matches 0 run {cmd}")
                        else:
                            ctx.files[func_name].append("return 0")
                            ret_temp = score(addr=f"!ret{ctx._temp_id} {temp_obj}")
                            ctx._temp_id += 1
                            runcommand(
                                f"execute store result score {ret_temp.addr} if score {sometemp.addr} matches 0 run function {func_name}")
                            runcommand(f"execute if score {ret_temp.addr} matches 1 run return 1")
                else:
                    body_func()
                break

        conds = _flatten_and(cond)
        prefix = f"execute {' '.join(conds)}"

        if sometemp is not None:
            prefix = f"execute if score {sometemp.addr} matches 0 {' '.join(conds)}"

        func_name = f"{ctx._current_namespace}:generated_{ctx._func_id}"
        ctx._func_id += 1
        with push_context(func_name):
            if sometemp is not None:
                runcommand(f"scoreboard players set {sometemp.addr} 1")
            body_func()

        if ctx.files.get(func_name):
            if len(ctx.files[func_name]) == 1:
                cmd = ctx.files[func_name][0]
                del ctx.files[func_name]
                if cmd.startswith("execute "):
                    runcommand(f"{prefix} {cmd[8:]}")
                else:
                    runcommand(f"{prefix} run {cmd}")
            else:
                ctx.files[func_name].append("return 0")
                ret_temp = score(addr=f"!ret{ctx._temp_id} {temp_obj}")
                ctx._temp_id += 1
                if prefix.startswith("execute "):
                    runcommand(f"execute store result score {ret_temp.addr} {prefix[8:]} run function {func_name}")
                else:
                    runcommand(f"execute store result score {ret_temp.addr} run function {func_name}")
                runcommand(f"execute if score {ret_temp.addr} matches 1 run return 1")


def _flare_while(cond_func, body_func, orelse_func=None, has_break=False, has_continue=False):
    func_name = f"{ctx._current_namespace}:while_{ctx._func_id}"
    ctx._func_id += 1

    with push_context(func_name):
        if has_break or has_continue:
            func_body = f"{ctx._current_namespace}:while_body_{ctx._func_id}"
            ctx._func_id += 1
            with push_context(func_body):
                body_func()

            ret_body = score(addr=f"!ret{ctx._temp_id} {temp_obj}")
            ctx._temp_id += 1
            runcommand(f"execute store result score {ret_body.addr} run function {func_body}")
            runcommand(f"execute if score {ret_body.addr} matches 1 run return 1")

            if has_break:
                runcommand(f"execute if score !break {temp_obj} matches 1 run return 0")
        else:
            body_func()

        cond = cond_func()
        conds = _flatten_and(cond)
        prefix = f"execute {' '.join(conds)}"
        ctx.files[func_name].append("return 0")
        ret_temp = score(addr=f"!ret{ctx._temp_id} {temp_obj}")
        ctx._temp_id += 1
        runcommand(f"execute store result score {ret_temp.addr} {' '.join(conds)} run function {func_name}")
        runcommand(f"execute if score {ret_temp.addr} matches 1 run return 1")

    if has_break:
        runcommand(f"scoreboard players set !break {temp_obj} 0")

    cond_init = cond_func()
    conds_init = _flatten_and(cond_init)
    prefix_init = f"execute {' '.join(conds_init)}"
    ret_temp_init = score(addr=f"!ret{ctx._temp_id} {temp_obj}")
    ctx._temp_id += 1
    runcommand(f"execute store result score {ret_temp_init.addr} {' '.join(conds_init)} run function {func_name}")
    runcommand(f"execute if score {ret_temp_init.addr} matches 1 run return 1")

    if orelse_func:
        if has_break:
            orelse_name = f"{ctx._current_namespace}:while_else_{ctx._func_id}"
            ctx._func_id += 1
            with push_context(orelse_name):
                orelse_func()
            runcommand(f"execute if score !break {temp_obj} matches 0 run function {orelse_name}")
        else:
            orelse_func()


def _flare_for(iterable, body_func, orelse_func=None, has_break=False, has_continue=False):
    if hasattr(iterable, "__for__"):
        iterable.__for__(body_func, orelse_func, has_break, has_continue)
    else:
        for item in iterable:
            body_func(item)


def _flare_with(*args):
    body_func = args[-1]
    chains = args[:-1]

    def wrap(idx):
        if idx == len(chains):
            body_func()
        else:
            obj = chains[idx]
            if hasattr(obj, "__with__"):
                obj.__with__(lambda: wrap(idx + 1))
            elif isinstance(obj, str):
                ExecuteChain(obj).__with__(lambda: wrap(idx + 1))
            else:
                raise TypeError(f"Object of type {type(obj).__name__} does not support __with__")

    wrap(0)
