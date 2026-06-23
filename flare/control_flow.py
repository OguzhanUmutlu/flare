from __future__ import annotations

from math import isinf
from typing import Callable

from . import context as ctx
from .context import namespace
from .context import push_context, runcommand, temp_obj, next_temp_id, next_func_id
from .execute_modifiers import ExecuteChain
from .variables.core import addr
from .variables.score import score


class ScoreIf:
    def __init__(self, t: list[ScoreIf]):
        self.t = t

    def __and__(self, other):
        if isinstance(self.t, score):
            return ScoreIf([self, other])
        return ScoreIf([*self.t, other])

    def then(self, s: str | Callable | list[str | Callable]):
        if not isinstance(s, list): s = [s]
        for i in range(len(s)):
            if callable(s[i]):
                file_len = len(ctx.files[ctx.current_file])
                s[i]()
                commands = ctx.files[ctx.current_file][file_len:]
                if len(commands) != 1:
                    raise AssertionError(f"Expected a single command in ScoreIf .then action, got {commands}")
                ctx.files[ctx.current_file] = ctx.files[ctx.current_file][:file_len]
                s[i] = commands[0]

        str_self = str(self)
        for x in s:
            runcommand(str_self + str(x))

    def __str__(self):
        if isinstance(self.t, list):
            conds = [str(x).removeprefix("execute ").removesuffix(" run ") for x in self.t]
            return f"execute {' '.join(conds)} run "
        raise NotImplementedError("ScoreIf.__str__ is not implemented")

    def __branch__(self, invert=False):
        from .compiler import _eval_to_bool_score  # avoid circular import
        if invert:
            dest = _eval_to_bool_score(self)
            return [f"unless score {addr(dest)} matches 1"]

        if isinstance(self.t, list):
            return [str(x).removeprefix("execute ").removesuffix(" run ") for x in self.t]

        return [str(self).removeprefix("execute ").removesuffix(" run ")]


class ScoreIfMatches(ScoreIf):
    def __init__(self, t: score, rng: tuple[float, float] | float):
        super().__init__([])
        self.t = t
        if isinstance(rng, (int, float)): rng = (rng, rng)
        self.rng = rng

    def __str__(self):
        a, b = self.rng
        if not isinf(a): a = int(a * self.t._multiplier)
        if not isinf(b): b = int(b * self.t._multiplier)
        st = f"{a}..{b}"
        if a == b:
            st = f"{a}"
        elif isinf(a):
            st = f"..{b}"
        elif isinf(b):
            st = f"{a}.."
        return f"execute if score {addr(self.t)} matches {st} run "


class ScoreIfScore(ScoreIf):
    def __init__(self, t: score, op: str, t2: score):
        super().__init__([])
        self.t = t
        self.op = op
        self.t2 = t2

    def __str__(self):
        return f"execute if score {addr(self.t)} {self.op} {addr(self.t2)} run "


def _has_early_return(func_name):
    for cmd in ctx.files.get(func_name, []):
        if cmd == "return 1" or cmd.endswith(" run return 1"):
            return True
    return False


def _invoke_block(func_name, cond_str):
    if _has_early_return(func_name):
        if not (ctx.files[func_name] and ctx.files[func_name][-1] in ("return 0", "return 1")):
            ctx.files[func_name].append("return 0")
        ret_temp = score(addr=f"!ret{next_temp_id()} {temp_obj}")

        if cond_str:
            runcommand(f"execute store result score {addr(ret_temp)} {cond_str} run function {func_name}")
        else:
            runcommand(f"execute store result score {addr(ret_temp)} run function {func_name}")
        runcommand(f"execute if score {addr(ret_temp)} matches 1 run return 1")
    else:
        if cond_str:
            runcommand(f"execute {cond_str} run function {func_name}")
        else:
            runcommand(f"function {func_name}")


def _flare_break():
    runcommand(f"scoreboard players set !break {temp_obj} 1")
    runcommand("return 0")


def _flare_continue():
    runcommand("return 0")


class expand:
    def __init__(self, cond):
        self.cond = cond


def _flare_if(*args):
    n = len(args) // 2
    conditions = args[:n]
    bodies = args[n:]

    elif_temp = None
    has_else_or_elif = len(conditions) > 1 or conditions[0] is None

    if has_else_or_elif:
        elif_temp = score(addr=f"!elif{next_temp_id()}")
        elif_temp.__iset__(0)

    is_dynamic_chain = None

    for cond_func, body_func in zip(conditions, bodies):
        if cond_func is None:
            if elif_temp is not None:
                func_name = f"{namespace()}:generated_{next_func_id()}"
                with push_context(func_name):
                    body_func()
                if ctx.files[func_name]:
                    if len(ctx.files[func_name]) == 1:
                        cmd = ctx.files[func_name][0]
                        del ctx.files[func_name]
                        if cmd.startswith("execute "):
                            runcommand(f"execute if score {addr(elif_temp)} matches 0 {cmd[8:]}")
                        else:
                            runcommand(f"execute if score {addr(elif_temp)} matches 0 run {cmd}")
                    else:
                        _invoke_block(func_name, f"if score {addr(elif_temp)} matches 0")
            else:
                body_func()
            break

        cond = cond_func()

        is_expand = isinstance(cond, expand)
        if is_expand:
            cond = cond.cond

        current_is_dynamic = not isinstance(cond, bool)
        if is_dynamic_chain is None:
            is_dynamic_chain = current_is_dynamic
        elif is_dynamic_chain != current_is_dynamic:
            raise TypeError(
                "Cannot mix compile-time (static) and run-time (dynamic) conditions in the same if/elif chain. Please use nested if statements instead.")

        if isinstance(cond, bool):
            if not cond:
                continue
            else:
                if elif_temp is not None:
                    func_name = f"{namespace()}:generated_{ctx.next_func_id()}"
                    with push_context(func_name):
                        body_func()
                    if ctx.files.get(func_name):
                        if len(ctx.files[func_name]) == 1:
                            cmd = ctx.files[func_name][0]
                            del ctx.files[func_name]
                            if cmd.startswith("execute "):
                                runcommand(f"execute if score {addr(elif_temp)} matches 0 {cmd[8:]}")
                            else:
                                runcommand(f"execute if score {addr(elif_temp)} matches 0 run {cmd}")
                        else:
                            _invoke_block(func_name, f"if score {addr(elif_temp)} matches 0")
                else:
                    body_func()
                break

        from .compiler import _flatten_and  # avoid circular import
        conds = _flatten_and(cond)
        prefix = f"execute {' '.join(conds)}"

        if elif_temp is not None:
            prefix = f"execute if score {addr(elif_temp)} matches 0 {' '.join(conds)}"

        if is_expand:
            start_len = len(ctx.files[ctx.current_file])
            if elif_temp is not None:
                runcommand(f"scoreboard players set {addr(elif_temp)} 1")
            body_func()
            for i in range(start_len, len(ctx.files[ctx.current_file])):
                cmd = ctx.files[ctx.current_file][i]
                if cmd.startswith("execute "):
                    ctx.files[ctx.current_file][i] = f"{prefix} {cmd[8:]}"
                else:
                    ctx.files[ctx.current_file][i] = f"{prefix} run {cmd}"
        else:
            func_name = f"{ctx._current_namespace}:generated_{ctx.next_func_id()}"
            with push_context(func_name):
                if elif_temp is not None:
                    runcommand(f"scoreboard players set {addr(elif_temp)} 1")
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
                    _invoke_block(func_name, prefix[8:] if prefix.startswith("execute ") else "")


def _get_func_prefix(namespace=None):
    if not namespace and ":" in ctx.current_file:
        file_path = ctx.current_file.split(":", 1)[1]
        if "/" in file_path:
            return file_path.rsplit("/", 1)[0] + "/"
    return ""


def _flare_while(cond_func, body_func, orelse_func=None, has_break=False, has_continue=False, namespace=None):
    from .compiler import _flatten_and  # avoid circular import
    ns = namespace or ctx._current_namespace
    prefix = _get_func_prefix(namespace)
    func_name = f"{ns}:{prefix}__flare__while__/while_{ctx.next_func_id()}"

    with push_context(func_name):
        if has_break or has_continue:
            func_body = f"{ns}:{prefix}__flare__while__/while_body_{ctx.next_func_id()}"
            with push_context(func_body):
                body_func()

            _invoke_block(func_body, "")

            if has_break:
                runcommand(f"execute if score !break {temp_obj} matches 1 run return 0")
        else:
            body_func()

        cond = cond_func()
        conds = _flatten_and(cond)
        prefix = f"execute {' '.join(conds)}"
        _invoke_block(func_name, " ".join(conds))

    if has_break:
        runcommand(f"scoreboard players set !break {temp_obj} 0")

    cond_init = cond_func()
    conds_init = _flatten_and(cond_init)
    ret_temp_init = score(addr=f"!ret{ctx.next_temp_id()} {temp_obj}")
    runcommand(f"execute store result score {addr(ret_temp_init)} {' '.join(conds_init)} run function {func_name}")
    runcommand(f"execute if score {addr(ret_temp_init)} matches 1 run return 1")

    if orelse_func:
        if has_break:
            orelse_name = f"{ctx._current_namespace}:{prefix}while_else_{ctx.next_func_id()}"
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
