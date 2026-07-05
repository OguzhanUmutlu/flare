import builtins
import string
from math import inf


def addr(var):
    return var._addr


class flare_len:
    def __new__(cls, x):
        if hasattr(x, "__len__"):
            return x.__len__()
        return builtins.len(x)


class _FailType:
    pass


fail = _FailType()


class IntReturn:
    def __init__(self, func_name):
        self.func_name = func_name

    def __icopy__(self, varid=None, is_recursive=False):
        return self


class flare_range:
    def __init__(self, *args):
        from .score import score
        from .core import FlareValue

        self.args = args
        self.is_flare = any(isinstance(a, FlareValue) for a in args)
        if not self.is_flare:
            self._native = builtins.range(*args)
        else:
            self._args = [a if isinstance(a, FlareValue) else score(a) for a in args]

    def __for__(self, body_func, orelse_func=None, has_break=False, has_continue=False):
        from ..control_flow import _flare_for
        from .. import context as ctx
        from .score import score
        from ..control_flow import _flare_while

        if not self.is_flare:
            return _flare_for(self._native, body_func, orelse_func, has_break, has_continue)

        start = score(0)
        step = score(1)
        if len(self._args) == 1:
            stop = self._args[0]
        elif len(self._args) == 2:
            start = self._args[0]
            stop = self._args[1]
        else:
            start = self._args[0]
            stop = self._args[1]
            step = self._args[2]

        is_neg = False
        if len(self.args) == 3 and isinstance(self.args[2], (int, float)) and self.args[2] < 0:
            is_neg = True

        i = score(0, addr=f"!range_i_{ctx.next_temp_id()}")
        i[:] = start

        def loop_body():
            body_func(i)
            i.__iadd__(step)

        cond = i > stop if is_neg else i < stop
        return _flare_while(cond, loop_body, orelse_func, has_break, has_continue)


def flare_ord(s):
    from .core import FlareValue
    from ..context import _runcmd
    from .score import score
    from .. import context as ctx
    from .core import LazyOp

    if not isinstance(s, FlareValue):
        return builtins.ord(s)

    def eval_ord(dest):
        dest[:] = 0
        _id = ctx.next_temp_id()

        _runcmd(f"data modify storage flare:temp ord_char_{_id} set from {addr(s)} 0 1")

        for c in string.printable:
            safe_c = c.replace('\\', '\\\\').replace('"', '\\"')
            _runcmd(
                f"execute if data storage flare:temp {{\"ord_char_{_id}\": \"{safe_c}\"}} run scoreboard players set {addr(dest)} {builtins.ord(c)}")
        return dest

    def alloc_temp():
        return score(addr=f"!ord_out_{ctx.next_temp_id()}")

    return LazyOp(s, eval_ord, alloc_temp)


def flare_bin(n):
    from .core import FlareValue
    from ..context import _runcmd
    from .score import score
    from .nbt import nbt
    from ..types import NBTType
    from .. import context as ctx
    from ..control_flow import ScoreIfMatches
    from .core import LazyOp

    if not isinstance(n, FlareValue):
        return builtins.bin(n)

    def eval_bin(dest):
        _id = ctx.next_temp_id()
        n_score = score(0, addr=f"!bin_n_{_id}")
        n_score[:] = n

        dest[:] = ""
        func_name = f"{ctx._current_namespace}:bin_{ctx.next_func_id()}"

        char_temp = nbt(addr=f"flare:temp bin_char_{_id}", datatype=NBTType.String)

        def loop():
            nonlocal n_score
            modulo = n_score % 2
            ScoreIfMatches(modulo, 0).then(lambda: char_temp.__iset__("0"))
            ScoreIfMatches(modulo, 1).then(lambda: char_temp.__iset__("1"))

            dest.prepend(char_temp)

            n_score //= 2
            ScoreIfMatches(n_score, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        with ctx.push_context(func_name):
            loop()

        ScoreIfMatches(n_score, (1, inf)).then(lambda: _runcmd(f"function {func_name}"))

        char_temp[:] = 0
        dest.prepend(char_temp)
        return dest

    def alloc_temp():
        return nbt(addr=f"!bin_out_{ctx.next_temp_id()}", datatype=NBTType.String)

    return LazyOp(n, eval_bin, alloc_temp)
