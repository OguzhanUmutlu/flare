import builtins

from . import context as ctx
from .context import _runcmd, addr
from .variables import score
from .variables.builtins import flare_len as len
from .variables.nbt import nbt


def randint(a, b):
    dest = score(addr=f"!rand_{ctx.next_temp_id()}")
    if isinstance(a, int) and isinstance(b, int):
        _runcmd(f"execute store result score {addr(dest)} run random value {a}..{b}")
        return dest
    else:
        _id = ctx.next_temp_id()
        macro_args = nbt(addr=f"{ctx.temp_storage} __rand_args_{_id}")
        macro_args.min = a
        macro_args.max = b

        def macro_generator(*_):
            _runcmd(f"$execute store result score {addr(dest)} run random value $(min)..$(max)")

        ctx._invoke_stdlib(f"__flare_stdlib__:__flare_rand_{_id}", macro_generator, with_=macro_args)
        return dest


def choice(seq):
    idx = randint(0, len(seq) - 1)
    _id = ctx.next_temp_id()
    macro_args = nbt(addr=f"{ctx.temp_storage} __choice_args_{_id}")
    macro_args["index"] = idx
    dest = nbt(addr=f"flare:temp choice_{_id}")

    def macro_generator(*_):
        from .variables.core import addr
        _runcmd(f"$data modify {addr(dest)} set from {addr(seq)}[$(index)]")

    ctx._invoke_stdlib(f"__flare_stdlib__:__flare_choice_{_id}", macro_generator, with_=macro_args)
    return dest


def random(*, dest=None, type=None):
    from .variables.core import FlareValue

    if dest is not None:
        if hasattr(dest, "__rrandom__"):
            return dest.__rrandom__()
        t = builtins.type(dest)
    else:
        t = type

    if t is not None:
        if isinstance(t, builtins.type) and issubclass(t, FlareValue):
            if hasattr(t, "__random__"):
                res = t.__random__()
                if dest is not None:
                    res._compile_into(dest)
                    return dest
                return res

    from .variables import fixed
    res = fixed(randint(0, 1000000)) / 1000000.0
    if dest is not None:
        res._compile_into(dest)
        return dest
    return res
