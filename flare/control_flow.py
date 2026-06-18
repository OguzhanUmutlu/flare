from . import context as ctx
from .compiler import _flatten_and
from .context import push_context, runcommand, temp_obj
from .types import NBTType
from .variables import score, nbt


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
                        runcommand(f"execute if score {sometemp.addr} matches 0 run function {func_name}")
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
                            runcommand(f"execute if score {sometemp.addr} matches 0 run function {func_name}")
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
                runcommand(f"{prefix} run function {func_name}")


def _flare_while(cond_func, body_func):
    func_name = f"{ctx._current_namespace}:while_{ctx._func_id}"
    ctx._func_id += 1

    with push_context(func_name):
        body_func()
        cond = cond_func()
        conds = _flatten_and(cond)
        prefix = f"execute {' '.join(conds)}"
        runcommand(f"{prefix} run function {func_name}")

    cond_init = cond_func()
    conds_init = _flatten_and(cond_init)
    prefix_init = f"execute {' '.join(conds_init)}"
    runcommand(f"{prefix_init} run function {func_name}")


def _flare_for(iterable, body_func):
    if isinstance(iterable, nbt) and iterable.is_sequence():
        elem_type = None
        if iterable.type == NBTType.ByteArray:
            elem_type = NBTType.Byte
        elif iterable.type == NBTType.IntArray:
            elem_type = NBTType.Int
        elif iterable.type == NBTType.LongArray:
            elem_type = NBTType.Long

        temp_arr = nbt(addr=f"flare:temp !for_arr_{ctx._temp_id}", datatype=iterable.type)
        temp_var = nbt(addr=f"{temp_arr.addr}[0]", datatype=elem_type)
        ctx._temp_id += 1

        temp_arr.__iset__(iterable)
        length_score = temp_arr.length()

        func_name = f"{ctx._current_namespace}:for_{ctx._func_id}"
        ctx._func_id += 1

        with push_context(func_name):
            body_func(temp_var)
            runcommand(f"data remove {temp_arr.addr}[0]")

            length_score -= 1
            runcommand(f"execute if score {length_score.addr} matches 1.. run function {func_name}")

        runcommand(f"execute if score {length_score.addr} matches 1.. run function {func_name}")

    else:
        from .variables import selector
        if isinstance(iterable, selector):
            _flare_with(iterable, lambda: body_func(selector("@s")))
        else:
            for item in iterable:
                body_func(item)


def _flare_with(*args):
    from .execute_modifiers import ExecuteChain, _as
    from .variables import selector

    body_func = args[-1]
    chains = args[:-1]

    combined_fragments = ["execute"]
    for chain in chains:
        if isinstance(chain, selector):
            chain = _as(chain)
        if isinstance(chain, ExecuteChain):
            if chain.fragments and chain.fragments[0] == "execute":
                combined_fragments.extend(chain.fragments[1:])
            else:
                combined_fragments.extend(chain.fragments)
        elif isinstance(chain, str):
            combined_fragments.append(chain)

    prefix = " ".join(combined_fragments)

    func_name = f"{ctx._current_namespace}:with_{ctx._func_id}"
    ctx._func_id += 1

    with push_context(func_name):
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
            runcommand(f"{prefix} run function {func_name}")
