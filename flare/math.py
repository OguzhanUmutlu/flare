import builtins
import inspect
import math
from math import *

from . import context as ctx
from .context import next_temp_id, push_context, _runcmd, vars_obj
from .variables.core import is_lazy, FlareValue

_orig = {"floor": math.floor, "ceil": math.ceil, "round": builtins.round, "sqrt": math.sqrt, "sin": math.sin,
         "cos": math.cos, "tan": math.tan, "asin": math.asin, "acos": math.acos, "atan": math.atan, "atan2": math.atan2,
         "exp": math.exp, "log": math.log, "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh, "asinh": math.asinh,
         "acosh": math.acosh, "atanh": math.atanh, "pow": math.pow, "min": builtins.min, "max": builtins.max}


def _dispatch(name, *args):
    if any(is_lazy(a) or hasattr(a, "_addr") for a in args):
        from .variables.core import MathOp
        return MathOp(name, *args)
    return _orig[name](*args)


def _dispatch_eval(name, dest, *args):
    memoize = name not in ("floor", "ceil")

    eval_args = []
    for a in args:
        if is_lazy(a):
            temp = a._alloc_temp(dest)
            a._compile_into(temp)
            eval_args.append(temp)
        else:
            eval_args.append(a)

    x = eval_args[0]

    if hasattr(x, f"__{name}__"):
        if not memoize or not hasattr(x, "_addr"):
            res = getattr(x, f"__{name}__")(*eval_args[1:])
            if hasattr(dest, "__iset__"):
                dest.__iset__(res)
            else:
                dest[:] = res
            return dest

        type_name = type(x).__name__
        arg_types = "_".join(type(a).__name__ for a in eval_args[1:])
        memo_key = f"{type_name}_{name}_{arg_types}" if arg_types else f"{type_name}_{name}"

        def _clone_var(var, addr):
            kwargs = {}
            if hasattr(var, "_multiplier"):
                kwargs["multiplier"] = var._multiplier
            return type(var)(addr=addr, **kwargs)

        if memo_key not in ctx.memoized_math:
            in_vars = [_clone_var(x, f"!{memo_key}_in0 {vars_obj}")]
            for i, arg in enumerate(eval_args[1:]):
                in_vars.append(_clone_var(arg, f"!{memo_key}_in{i + 1} {vars_obj}"))

            out_var_addr = f"!{memo_key}_out {vars_obj}"

            ctx.memoized_math[memo_key] = {
                "in_vars": in_vars,
                "out_addr": out_var_addr,
                "func_path": f"__flare_stdlib__:__flare_math_{memo_key}"
            }

            with push_context(f"__flare_stdlib__:__flare_math_{memo_key}"):
                out_var = _clone_var(in_vars[0], out_var_addr)
                meth = getattr(in_vars[0], f"__{name}__")

                if "dest" in inspect.signature(meth).parameters:
                    res = meth(*in_vars[1:], dest=out_var)
                else:
                    res = meth(*in_vars[1:])

                ctx.memoized_math[memo_key]["out_var_prototype"] = res
                if res is not out_var:
                    if hasattr(out_var, "__iset__"):
                        out_var.__iset__(res)
                    else:
                        out_var[:] = res

        memo = ctx.memoized_math[memo_key]

        x.__icopy__(f"!{memo_key}_in0")
        for i, arg in enumerate(eval_args[1:]):
            if hasattr(arg, "__icopy__"):
                arg.__icopy__(f"!{memo_key}_in{i + 1}")
            else:
                in_var = memo["in_vars"][i + 1]
                if hasattr(in_var, "__iset__"):
                    in_var.__iset__(arg)
                else:
                    in_var[:] = arg

        _runcmd(f"function {memo['func_path']}")

        out_var = _clone_var(memo["out_var_prototype"], memo["out_addr"])

        if hasattr(dest, "__iset__"):
            dest.__iset__(out_var)
        else:
            dest[:] = out_var

        return dest

    raise TypeError(f"'{type(x).__name__}' does not support mathematical operation '{name}'")


def min_(*args, **kwargs):
    if len(args) == 1 and hasattr(args[0], "__iter__"):
        search_args = list(args[0])
        if not any(hasattr(x, "__imin__") for x in search_args):
            return _orig["min"](search_args, **kwargs)
    else:
        search_args = args
        if not any(hasattr(x, "__imin__") for x in search_args):
            return _orig["min"](*args, **kwargs)

    res = next((x for x in search_args if hasattr(x, "__imin__")), None)
    res = res.__icopy__(f"!min_{next_temp_id()}")
    res[:] = search_args[0]
    for x in search_args[1:]:
        res.__imin__(x)
    return res


def max_(*args, **kwargs):
    if len(args) == 1 and hasattr(args[0], "__iter__"):
        search_args = list(args[0])
        if not any(isinstance(x, FlareValue) for x in search_args):
            return _orig["max"](search_args, **kwargs)
    else:
        search_args = args
        if not any(isinstance(x, FlareValue) for x in search_args):
            return _orig["max"](*args, **kwargs)

    var = next((x for x in search_args if isinstance(x, FlareValue)), None)
    res = var.__icopy__(f"!max_{next_temp_id()}")
    res[:] = search_args[0]
    for x in search_args[1:]:
        res.__imax__(x)
    return res


def floor(x): return _dispatch("floor", x)


def ceil(x): return _dispatch("ceil", x)


def round_(x, ndigits=None):
    if hasattr(x, "__round__"):
        return x.__round__() if ndigits is None else x.__round__(ndigits)
    return _orig["round"](x) if ndigits is None else _orig["round"](x, ndigits)


def sqrt(x): return _dispatch("sqrt", x)


def sin(x): return _dispatch("sin", x)


def cos(x): return _dispatch("cos", x)


def exp(x): return _dispatch("exp", x)


def atan2(y, x):
    if is_lazy(y) or hasattr(y, "_addr") or is_lazy(x) or hasattr(x, "_addr") or hasattr(x, "real"):
        from .variables.core import MathOp
        return MathOp("atan2", y, x)
    return _orig["atan2"](y, x)


def log(x, base=None):
    from .variables.core import MathOp

    if is_lazy(x) or hasattr(x, "_addr") or hasattr(x, "real"):
        leaf = x._best_leaf() if is_lazy(x) else x
        if hasattr(leaf, "__log__"):
            if base is None:
                return MathOp("log", x)
            return MathOp("log", x) / log(base)
    if base is None:
        return _orig["log"](x)
    return _orig["log"](x, base)


def ln(x): return log(x)


def pow_(x, y):
    from .variables.core import MathOp

    if is_lazy(x) or hasattr(x, "_addr") or hasattr(x, "real") or is_lazy(y) or hasattr(y, "_addr"):
        leaf = x._best_leaf() if is_lazy(x) else x
        if hasattr(leaf, "__pow__"):
            return MathOp("pow", x, y)
        return exp(y * ln(x))
    return _orig["pow"](x, y)


def tan(x):
    from .variables.core import MathOp

    if is_lazy(x) or hasattr(x, "_addr") or hasattr(x, "real"):
        leaf = x._best_leaf() if is_lazy(x) else x
        if hasattr(leaf, "__tan__"):
            return MathOp("tan", x)
        return sin(x) / cos(x)
    return _orig["tan"](x)


def asin(x):
    from .variables.core import MathOp

    if is_lazy(x) or hasattr(x, "_addr") or hasattr(x, "real"):
        leaf = x._best_leaf() if is_lazy(x) else x
        if hasattr(leaf, "__asin__"):
            return MathOp("asin", x)
        return atan2(x, sqrt(1 - x * x))
    return _orig["asin"](x)


def acos(x):
    from .variables.core import MathOp

    if is_lazy(x) or hasattr(x, "_addr") or hasattr(x, "real"):
        leaf = x._best_leaf() if is_lazy(x) else x
        if hasattr(leaf, "__acos__"):
            return MathOp("acos", x)
        return atan2(sqrt(1 - x * x), x)
    return _orig["acos"](x)


def atan(x):
    from .variables.core import MathOp

    if is_lazy(x) or hasattr(x, "_addr") or hasattr(x, "real"):
        leaf = x._best_leaf() if is_lazy(x) else x
        if hasattr(leaf, "__atan__"):
            return MathOp("atan", x)
        return atan2(x, 1)
    return _orig["atan"](x)


def csc(x): return 1 / sin(x)


def sec(x): return 1 / cos(x)


def cot(x): return 1 / tan(x)


def acsc(x): return asin(1 / x)


def asec(x): return acos(1 / x)


def acot(x): return atan(1 / x)


def sinh(x):
    from .variables.core import MathOp

    if is_lazy(x) or hasattr(x, "_addr") or hasattr(x, "real"):
        leaf = x._best_leaf() if is_lazy(x) else x
        if hasattr(leaf, "__sinh__"):
            return MathOp("sinh", x)
        return (exp(x) - exp(-x)) / 2
    return _orig["sinh"](x)


def cosh(x):
    from .variables.core import MathOp

    if is_lazy(x) or hasattr(x, "_addr") or hasattr(x, "real"):
        leaf = x._best_leaf() if is_lazy(x) else x
        if hasattr(leaf, "__cosh__"):
            return MathOp("cosh", x)
        return (exp(x) + exp(-x)) / 2
    return _orig["cosh"](x)


def tanh(x):
    from .variables.core import MathOp

    if is_lazy(x) or hasattr(x, "_addr") or hasattr(x, "real"):
        leaf = x._best_leaf() if is_lazy(x) else x
        if hasattr(leaf, "__tanh__"):
            return MathOp("tanh", x)
        return sinh(x) / cosh(x)
    return _orig["tanh"](x)


def csch(x): return 1 / sinh(x)


def sech(x): return 1 / cosh(x)


def coth(x): return 1 / tanh(x)


def asinh(x):
    from .variables.core import MathOp

    if is_lazy(x) or hasattr(x, "_addr") or hasattr(x, "real"):
        leaf = x._best_leaf() if is_lazy(x) else x
        if hasattr(leaf, "__asinh__"):
            return MathOp("asinh", x)
        return ln(x + sqrt(x * x + 1))
    return _orig["asinh"](x)


def acosh(x):
    from .variables.core import MathOp

    if is_lazy(x) or hasattr(x, "_addr") or hasattr(x, "real"):
        leaf = x._best_leaf() if is_lazy(x) else x
        if hasattr(leaf, "__acosh__"):
            return MathOp("acosh", x)
        return ln(x + sqrt(x * x - 1))
    return _orig["acosh"](x)


def atanh(x):
    from .variables.core import MathOp

    if is_lazy(x) or hasattr(x, "_addr") or hasattr(x, "real"):
        leaf = x._best_leaf() if is_lazy(x) else x
        if hasattr(leaf, "__atanh__"):
            return MathOp("atanh", x)
        return 0.5 * ln((1 + x) / (1 - x))
    return _orig["atanh"](x)


def acsch(x): return ln(1 / x + sqrt(1 / (x * x) + 1))


def asech(x): return ln(1 / x + sqrt(1 / x - 1) * sqrt(1 / x + 1))


def acoth(x): return 0.5 * ln((x + 1) / (x - 1))


def fastsin(x):
    from .variables.core import MathOp

    if is_lazy(x) or hasattr(x, "_addr") or hasattr(x, "real"):
        leaf = x._best_leaf() if is_lazy(x) else x
        if hasattr(leaf, "__fastsin__"):
            return MathOp("fastsin", x)
        return sin(x)
    return sin(x)


def fastsqrt(x):
    from .variables.core import MathOp

    if is_lazy(x) or hasattr(x, "_addr") or hasattr(x, "real"):
        leaf = x._best_leaf() if is_lazy(x) else x
        if hasattr(leaf, "fastsqrt"):
            return MathOp("fastsqrt", x)
        return sqrt(x)
    return sqrt(x)


def rsqrt(x):
    from .variables.core import MathOp

    if is_lazy(x) or hasattr(x, "_addr") or hasattr(x, "real"):
        leaf = x._best_leaf() if is_lazy(x) else x
        if hasattr(leaf, "rsqrt"):
            return MathOp("rsqrt", x)
        return 1 / sqrt(x)
    return 1 / sqrt(x)


math.floor = floor
math.ceil = ceil
math.sqrt = sqrt
math.sin = sin
math.cos = cos
math.tan = tan
math.asin = asin
math.acos = acos
math.atan = atan
math.atan2 = atan2
math.exp = exp
math.log = log
math.sinh = sinh
math.cosh = cosh
math.tanh = tanh
math.asinh = asinh
math.acosh = acosh
math.atanh = atanh
math.pow = pow_
builtins.round = round_
builtins.min = min_
builtins.max = max_
