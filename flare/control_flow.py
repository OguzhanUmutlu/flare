from __future__ import annotations

from math import isinf
from typing import Callable

import flare
from . import context as ctx
from .context import namespace
from .context import push_context, _runcmd, temp_obj, next_temp_id, next_func_id
from .execute_modifiers import ExecuteChain
from .variables.core import addr


class ScoreIf:
    def __init__(self, t: list[ScoreIf]):
        self.t = t

    def __and__(self, other):
        from .variables.score import score
        if isinstance(self.t, score):
            return ScoreIf([self, other])
        return ScoreIf([*self.t, other])

    def then(self, s: Callable):
        commands = []
        file_len = len(ctx.files[ctx.current_file])

        s()
        commands.extend(ctx.files[ctx.current_file][file_len:])
        ctx.files[ctx.current_file] = ctx.files[ctx.current_file][:file_len]

        str_self = str(self)
        for cmd in commands:
            _runcmd(str_self + str(cmd))

    def while_then(self, s, namespace=None):
        if isinstance(s, list):
            def body():
                for f in s: f()
        else:
            body = s
        _flare_while(lambda: self, body, namespace=namespace)

    def __str__(self):
        if isinstance(self.t, list):
            conds = []
            for x in self.t:
                if isinstance(x, ScoreIf):
                    conds.append(str(x).removeprefix("execute ").removesuffix(" run "))
                elif hasattr(x, "__branch__"):
                    conds.extend(x.__branch__())
                else:
                    conds.append(str(x).removeprefix("execute ").removesuffix(" run "))
            return f"execute {' '.join(conds)} run "
        raise NotImplementedError("ScoreIf.__str__ is not implemented")

    def __branch__(self, invert=False):
        from .compiler import _eval_to_bool_score  # avoid circular import
        if invert:
            if hasattr(self, "invert"):
                return self.invert().__branch__()
            dest = _eval_to_bool_score(self)
            return [f"unless score {addr(dest)} matches 1"]

        if isinstance(self.t, list):
            conds = []
            for x in self.t:
                if isinstance(x, ScoreIf):
                    conds.append(str(x).removeprefix("execute ").removesuffix(" run "))
                elif hasattr(x, "__branch__"):
                    conds.extend(x.__branch__())
                else:
                    conds.append(str(x).removeprefix("execute ").removesuffix(" run "))
            return conds

        return [str(self).removeprefix("execute ").removesuffix(" run ")]


class ScoreIfMatches(ScoreIf):
    def __init__(self, t: "flare.variables.score", rng: tuple[float, float] | float):
        super().__init__([])
        self.t = t
        if isinstance(rng, (int, float)): rng = (rng, rng)
        self.rng = rng

    def __str__(self):
        if isinstance(self.rng, str):
            st = self.rng
        else:
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

    def invert(self):
        return ScoreUnlessMatches(self.t, self.rng)


class ScoreUnlessMatches(ScoreIf):
    def __init__(self, t, rng):
        super().__init__([])
        self.t = t
        if isinstance(rng, (int, float)): rng = (rng, rng)
        self.rng = rng

    def __str__(self):
        if isinstance(self.rng, str):
            st = self.rng
        else:
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
        return f"execute unless score {addr(self.t)} matches {st} run "

    def invert(self):
        return ScoreIfMatches(self.t, self.rng)


class ScoreIfScore(ScoreIf):
    def __init__(self, t: "flare.variables.score", op: str, t2: "flare.variables.score"):
        super().__init__([])
        self.t = t
        self.op = op
        self.t2 = t2

    def __str__(self):
        return f"execute if score {addr(self.t)} {self.op} {addr(self.t2)} run "

    def invert(self):
        inv_op = {
            "<": ">=",
            "<=": ">",
            "=": "!=",
            ">": "<=",
            ">=": "<"
        }.get(self.op)
        if inv_op == "!=":
            return ScoreUnlessScore(self.t, "=", self.t2)
        elif inv_op:
            return ScoreIfScore(self.t, inv_op, self.t2)
        raise NotImplementedError(f"Cannot invert score operator {self.op}")


class ScoreUnlessScore(ScoreIf):
    def __init__(self, t: "flare.variables.score", op: str, t2: "flare.variables.score"):
        super().__init__([])
        self.t = t
        self.op = op
        self.t2 = t2

    def __str__(self):
        return f"execute unless score {addr(self.t)} {self.op} {addr(self.t2)} run "

    def invert(self):
        return ScoreIfScore(self.t, self.op, self.t2)


def _has_early_return(func_name):
    for cmd in ctx.files.get(func_name, []):
        if cmd.startswith("return ") or " run return " in cmd:
            return True
    return False


def _invoke_block(func_name, cond_str):
    from .variables.score import score
    if _has_early_return(func_name):
        if not (ctx.files[func_name] and ctx.files[func_name][-1] in ("return 0", "return 1")):
            ctx.files[func_name].append("return 0")
        ret_temp = score(addr=f"!ret{next_temp_id()}")

        if cond_str:
            _runcmd(f"execute store result score {addr(ret_temp)} {cond_str} run function {func_name}")
        else:
            _runcmd(f"execute store result score {addr(ret_temp)} run function {func_name}")
        _runcmd(f"execute if score {addr(ret_temp)} matches 1 run return 1")
    else:
        if cond_str:
            _runcmd(f"execute {cond_str} run function {func_name}")
        else:
            _runcmd(f"function {func_name}")


def _flare_break():
    _runcmd(f"scoreboard players set !break {temp_obj} 1")
    _runcmd("return 0")


def _flare_continue():
    _runcmd("return 0")


class expand:
    def __init__(self, cond):
        self.cond = cond


def _flare_if(*args):
    from .variables.score import score
    from .compiler import _flatten_and

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
                if ctx.files.get(func_name):
                    if len(ctx.files[func_name]) == 1:
                        cmd = ctx.files[func_name][0]
                        del ctx.files[func_name]
                        ctx._runcmd(ctx.combine_execute(f"execute if score {addr(elif_temp)} matches 0", cmd))
                    else:
                        _invoke_block(func_name, f"if score {addr(elif_temp)} matches 0")
            else:
                body_func()
            break

        raw_cond = cond_func()
        is_expand = isinstance(raw_cond, expand)
        cond = raw_cond.cond if is_expand else raw_cond

        current_is_dynamic = not isinstance(cond, bool)
        if is_dynamic_chain is None:
            is_dynamic_chain = current_is_dynamic
        elif is_dynamic_chain != current_is_dynamic:
            raise TypeError(
                "Cannot mix compile-time (static) and run-time (dynamic) conditions in the same if/elif chain. Please use nested if statements instead."
            )

        if isinstance(cond, bool):
            if not cond:
                continue
            else:
                if elif_temp is not None:
                    if is_expand:
                        start_len = len(ctx.files[ctx.current_file])
                        body_func()

                        _runcmd(f"scoreboard players set {addr(elif_temp)} 1")

                        prefix = f"execute if score {addr(elif_temp)} matches 0"
                        for i in range(start_len, len(ctx.files[ctx.current_file])):
                            cmd = ctx.files[ctx.current_file][i]
                            ctx.files[ctx.current_file][i] = ctx.combine_execute(prefix, cmd)
                    else:
                        func_name = f"{namespace()}:generated_{next_func_id()}"
                        with push_context(func_name):
                            body_func()
                        if ctx.files.get(func_name):
                            if len(ctx.files[func_name]) == 1:
                                cmd = ctx.files[func_name][0]
                                del ctx.files[func_name]
                                _runcmd(ctx.combine_execute(f"execute if score {addr(elif_temp)} matches 0", cmd))
                            else:
                                _invoke_block(func_name, f"if score {addr(elif_temp)} matches 0")
                else:
                    body_func()
                break

        conds = _flatten_and(cond)
        prefix = f"execute {' '.join(conds)}"

        if elif_temp is not None:
            prefix = f"execute if score {addr(elif_temp)} matches 0 {' '.join(conds)}"

        if is_expand:
            start_len = len(ctx.files[ctx.current_file])

            body_func()

            if elif_temp is not None:
                _runcmd(f"scoreboard players set {addr(elif_temp)} 1")

            for i in range(start_len, len(ctx.files[ctx.current_file])):
                cmd = ctx.files[ctx.current_file][i]
                ctx.files[ctx.current_file][i] = ctx.combine_execute(prefix, cmd)
        else:
            func_name = f"{namespace()}:generated_{next_func_id()}"
            with push_context(func_name):
                if elif_temp is not None:
                    _runcmd(f"scoreboard players set {addr(elif_temp)} 1")
                body_func()

            if ctx.files.get(func_name):
                if len(ctx.files[func_name]) == 1:
                    cmd = ctx.files[func_name][0]
                    del ctx.files[func_name]
                    _runcmd(ctx.combine_execute(prefix, cmd))
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
    from .variables.score import score
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
                _runcmd(f"execute if score !break {temp_obj} matches 1 run return 0")
        else:
            body_func()

        cond = cond_func()
        conds = _flatten_and(cond)
        prefix = f"execute {' '.join(conds)}"
        _invoke_block(func_name, " ".join(conds))

    if has_break:
        _runcmd(f"scoreboard players set !break {temp_obj} 0")

    cond_init = cond_func()
    conds_init = _flatten_and(cond_init)
    ret_temp_init = score(addr=f"!ret{ctx.next_temp_id()}")
    _runcmd(f"execute store result score {addr(ret_temp_init)} {' '.join(conds_init)} run function {func_name}")
    _runcmd(f"execute if score {addr(ret_temp_init)} matches 1 run return 1")

    if orelse_func:
        if has_break:
            orelse_name = f"{ctx._current_namespace}:{prefix}while_else_{ctx.next_func_id()}"
            with push_context(orelse_name):
                orelse_func()
            _runcmd(f"execute if score !break {temp_obj} matches 0 run function {orelse_name}")
        else:
            orelse_func()


def _flare_for(iterable, body_func, orelse_func=None, has_break=False, has_continue=False):
    if hasattr(iterable, "__for__"):
        iterable.__for__(body_func, orelse_func, has_break, has_continue)
    else:
        for item in iterable:
            body_func(item)


class schedule:
    def __init__(self, time: str, append: bool = False):
        self._time = time
        self._mode = "append" if append else "replace"
        self._func_name = None

    def __with__(self, body_func):
        ns = ctx._current_namespace
        func_name = f"{ns}:__flare__schedule__/sched_{ctx.next_func_id()}"
        self._func_name = func_name

        with ctx.push_context(func_name):
            body_func()

        _runcmd(f"schedule function {func_name} {self._time} {self._mode}")

    def clear(self):
        if self._func_name is None:
            raise RuntimeError("schedule.clear() called before the 'with schedule(...)' block was executed")
        _runcmd(f"schedule clear {self._func_name}")


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


def _flare_as_var(obj):
    if hasattr(obj, "__as_var__"):
        return obj.__as_var__()
    return obj


def _flare_not(val):
    if hasattr(val, "__branch__"):
        from .variables.core import UnaryOp
        return UnaryOp(val, "not")
    return not val


def _flare_and(*args):
    from .variables.core import BinaryOp
    current_flare = None
    for arg in args:
        val = arg()
        if hasattr(val, "__branch__"):
            if current_flare is None:
                current_flare = val
            else:
                current_flare = BinaryOp(current_flare, val, "and")
        else:
            if not val:
                return False
    if current_flare is not None:
        return current_flare
    return True


def _flare_or(*args):
    from .variables.core import BinaryOp
    current_flare = None
    for arg in args:
        val = arg()
        if hasattr(val, "__branch__"):
            if current_flare is None:
                current_flare = val
            else:
                current_flare = BinaryOp(current_flare, val, "or")
        else:
            if val:
                return True
    if current_flare is not None:
        return current_flare
    return False


class BlockIfMatches(ScoreIf):
    def __init__(self, pos: str, target: str):
        super().__init__([])
        self.pos = pos
        self.target = target

    def __str__(self):
        return f"execute if block {self.pos} {self.target} run "

    def invert(self):
        return BlockUnlessMatches(self.pos, self.target)

    def __branch__(self, invert=False):
        if invert:
            return [f"unless block {self.pos} {self.target}"]
        return [f"if block {self.pos} {self.target}"]


class BlockUnlessMatches(ScoreIf):
    def __init__(self, pos: str, target: str):
        super().__init__([])
        self.pos = pos
        self.target = target

    def __str__(self):
        return f"execute unless block {self.pos} {self.target} run "

    def invert(self):
        return BlockIfMatches(self.pos, self.target)

    def __branch__(self, invert=False):
        if invert:
            return [f"if block {self.pos} {self.target}"]
        return [f"unless block {self.pos} {self.target}"]
