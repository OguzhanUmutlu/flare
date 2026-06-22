import builtins
import math
from math import *

_orig = {"floor": math.floor, "ceil": math.ceil, "round": builtins.round, "sqrt": math.sqrt, "sin": math.sin,
         "cos": math.cos, "tan": math.tan, "asin": math.asin, "acos": math.acos, "atan": math.atan, "atan2": math.atan2,
         "exp": math.exp, "log": math.log, "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh, "asinh": math.asinh,
         "acosh": math.acosh, "atanh": math.atanh, "pow": math.pow, "min": builtins.min, "max": builtins.max}


def _dispatch(name, *args):
    x = args[0]
    if hasattr(x, "_eval_into"):
        leaf = x._best_leaf()
        temp = leaf._alloc_temp()
        x._eval_into(temp)
        x = temp
        args = (x,) + args[1:]
    if hasattr(x, f"__{name}__"):
        return getattr(x, f"__{name}__")(*args[1:])
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
