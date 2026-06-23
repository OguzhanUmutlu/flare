import builtins
import math
from math import *

_orig = {"floor": math.floor, "ceil": math.ceil, "round": builtins.round, "sqrt": math.sqrt, "sin": math.sin,
         "cos": math.cos, "tan": math.tan, "asin": math.asin, "acos": math.acos, "atan": math.atan, "atan2": math.atan2,
         "exp": math.exp, "log": math.log, "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh, "asinh": math.asinh,
         "acosh": math.acosh, "atanh": math.atanh, "pow": math.pow, "min": builtins.min, "max": builtins.max}


def _dispatch(name, *args, memoize=True):
    x = args[0]
    if hasattr(x, "_eval_into"):
        leaf = x._best_leaf()
        temp = leaf._alloc_temp()
        x._eval_into(temp)
        x = temp
        args = (x,) + args[1:]
    if hasattr(x, f"__{name}__"):
        if not memoize or not hasattr(x, "_addr"):
            return getattr(x, f"__{name}__")(*args[1:])

        type_name = type(x).__name__
        arg_types = "_".join(type(a).__name__ for a in args[1:])
        memo_key = f"{type_name}_{name}_{arg_types}" if arg_types else f"{type_name}_{name}"

        from . import context as ctx
        from .context import push_context, runcommand, next_temp_id, vars_obj

        def _clone_var(var, addr):
            kwargs = {}
            if hasattr(var, "_multiplier"):
                kwargs["multiplier"] = var._multiplier
            return type(var)(addr=addr, **kwargs)

        if not hasattr(ctx, "memoized_math"):
            ctx.memoized_math = {}

        if memo_key not in ctx.memoized_math:
            in_vars = [_clone_var(x, f"!{memo_key}_in0 {vars_obj}")]
            for i, arg in enumerate(args[1:]):
                in_vars.append(_clone_var(arg, f"!{memo_key}_in{i + 1} {vars_obj}"))

            out_var_addr = f"!{memo_key}_out {vars_obj}"

            ctx.memoized_math[memo_key] = {
                "in_vars": in_vars,
                "out_addr": out_var_addr,
                "func_path": f"__flare_stdlib__:__flare_math_{memo_key}"
            }

            with push_context(f"__flare_stdlib__:__flare_math_{memo_key}"):
                res = getattr(in_vars[0], f"__{name}__")(*in_vars[1:])
                ctx.memoized_math[memo_key]["out_var_prototype"] = res
                out_var = _clone_var(res, out_var_addr)
                if hasattr(out_var, "__iset__"):
                    out_var.__iset__(res)
                else:
                    out_var[:] = res

        memo = ctx.memoized_math[memo_key]

        x.__icopy__(f"!{memo_key}_in0")
        for i, arg in enumerate(args[1:]):
            if hasattr(arg, "__icopy__"):
                arg.__icopy__(f"!{memo_key}_in{i + 1}")
            else:
                in_var = memo["in_vars"][i + 1]
                if hasattr(in_var, "__iset__"):
                    in_var.__iset__(arg)
                else:
                    in_var[:] = arg

        runcommand(f"function {memo['func_path']}")

        out_var = _clone_var(memo["out_var_prototype"], memo["out_addr"])
        return out_var.__icopy__(f"!{memo_key}_res_{next_temp_id()}")

    return _orig[name](*args)


def min_(*args, **kwargs):
    if len(args) == 1 and hasattr(args[0], "__iter__"):
        search_args = list(args[0])
        if not any(hasattr(x, "__imin__") for x in search_args):
            return _orig["min"](search_args, **kwargs)
    else:
        search_args = args
        if not any(hasattr(x, "__imin__") for x in search_args):
            return _orig["min"](*args, **kwargs)

    var = next((x for x in search_args if hasattr(x, "__imin__")), None)
    res = var.__icopy__(f"!min_{next_temp_id()}")
    res[:] = search_args[0]
    for x in search_args[1:]:
        res.__imin__(x)
    return res


def max_(*args, **kwargs):
    if len(args) == 1 and hasattr(args[0], "__iter__"):
        search_args = list(args[0])
        if not any(hasattr(x, "__imax__") for x in search_args):
            return _orig["max"](search_args, **kwargs)
    else:
        search_args = args
        if not any(hasattr(x, "__imax__") for x in search_args):
            return _orig["max"](*args, **kwargs)

    var = next((x for x in search_args if hasattr(x, "__imax__")), None)
    res = var.__icopy__(f"!max_{next_temp_id()}")
    res[:] = search_args[0]
    for x in search_args[1:]:
        res.__imax__(x)
    return res


def floor(x): return _dispatch("floor", x, memoize=False)


def ceil(x): return _dispatch("ceil", x, memoize=False)


def round_(x, ndigits=None):
    if hasattr(x, "__round__"):
        return x.__round__() if ndigits is None else x.__round__(ndigits)
    return _orig["round"](x) if ndigits is None else _orig["round"](x, ndigits)


def sqrt(x): return _dispatch("sqrt", x)


def sin(x): return _dispatch("sin", x)


def cos(x): return _dispatch("cos", x)


def exp(x): return _dispatch("exp", x)


def atan2(y, x):
    if hasattr(y, "__atan2__"):
        return y.__atan2__(x)
    if hasattr(x, "_addr") and isinstance(y, (int, float)):
        return type(x)(y).__atan2__(x)
    return _orig["atan2"](y, x)


def log(x, base=None):
    if hasattr(x, "__log__"):
        if base is None:
            return x.__log__()
        return x.__log__() / log(base)
    if base is None:
        return _orig["log"](x)
    return _orig["log"](x, base)


def ln(x): return log(x)


def pow(x, y):
    if hasattr(x, "__pow__"):
        return x.__pow__(y)
    if hasattr(x, "_addr") or hasattr(x, "real"):
        return exp(y * ln(x))
    return _orig["pow"](x, y)


def tan(x):
    if hasattr(x, "__tan__"): return x.__tan__();
    if hasattr(x, "_addr") or hasattr(x, "real"): return sin(x) / cos(x)
    return _orig["tan"](x)


def asin(x):
    if hasattr(x, "__asin__"): return x.__asin__();
    if hasattr(x, "_addr") or hasattr(x, "real"): return atan2(x, sqrt(1 - x * x))
    return _orig["asin"](x)


def acos(x):
    if hasattr(x, "__acos__"): return x.__acos__();
    if hasattr(x, "_addr") or hasattr(x, "real"): return atan2(sqrt(1 - x * x), x)
    return _orig["acos"](x)


def atan(x):
    if hasattr(x, "__atan__"): return x.__atan__();
    if hasattr(x, "_addr") or hasattr(x, "real"): return atan2(x, 1)
    return _orig["atan"](x)


def csc(x): return 1 / sin(x)


def sec(x): return 1 / cos(x)


def cot(x): return 1 / tan(x)


def acsc(x): return asin(1 / x)


def asec(x): return acos(1 / x)


def acot(x): return atan(1 / x)


def sinh(x):
    if hasattr(x, "__sinh__"): return x.__sinh__();
    if hasattr(x, "_addr") or hasattr(x, "real"): return (exp(x) - exp(-x)) / 2
    return _orig["sinh"](x)


def cosh(x):
    if hasattr(x, "__cosh__"): return x.__cosh__();
    if hasattr(x, "_addr") or hasattr(x, "real"): return (exp(x) + exp(-x)) / 2
    return _orig["cosh"](x)


def tanh(x):
    if hasattr(x, "__tanh__"): return x.__tanh__();
    if hasattr(x, "_addr") or hasattr(x, "real"): return sinh(x) / cosh(x)
    return _orig["tanh"](x)


def csch(x): return 1 / sinh(x)


def sech(x): return 1 / cosh(x)


def coth(x): return 1 / tanh(x)


def asinh(x):
    if hasattr(x, "__asinh__"): return x.__asinh__();
    if hasattr(x, "_addr") or hasattr(x, "real"): return ln(x + sqrt(x * x + 1))
    return _orig["asinh"](x)


def acosh(x):
    if hasattr(x, "__acosh__"): return x.__acosh__();
    if hasattr(x, "_addr") or hasattr(x, "real"): return ln(x + sqrt(x * x - 1))
    return _orig["acosh"](x)


def atanh(x):
    if hasattr(x, "__atanh__"): return x.__atanh__();
    if hasattr(x, "_addr") or hasattr(x, "real"): return 0.5 * ln((1 + x) / (1 - x))
    return _orig["atanh"](x)


def acsch(x): return ln(1 / x + sqrt(1 / (x * x) + 1))


def asech(x): return ln(1 / x + sqrt(1 / x - 1) * sqrt(1 / x + 1))


def acoth(x): return 0.5 * ln((x + 1) / (x - 1))


def fastsin(x):
    if hasattr(x, "__fastsin__"):
        return x.__fastsin__()
    return sin(x)


def fastsqrt(x):
    if hasattr(x, "fastsqrt"):
        return x.fastsqrt()
    return sqrt(x)


def rsqrt(x):
    if hasattr(x, "rsqrt"):
        return x.rsqrt()
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
math.pow = pow
builtins.round = round_
builtins.min = min_
builtins.max = max_
