import builtins
import math

_orig = {"floor": math.floor, "ceil": math.ceil, "round": builtins.round, "sqrt": math.sqrt, "sin": math.sin,
         "cos": math.cos, "tan": math.tan, "asin": math.asin, "acos": math.acos, "atan": math.atan, "atan2": math.atan2,
         "exp": math.exp, "log": math.log, "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh, "asinh": math.asinh,
         "acosh": math.acosh, "atanh": math.atanh, "pow": math.pow}


def _dispatch(name, *args):
    x = args[0]
    if hasattr(x, f"__{name}__"):
        return getattr(x, f"__{name}__")(*args[1:])
    return _orig[name](*args)


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
    if hasattr(x, "addr") or hasattr(x, "real"):
        return exp(y * ln(x))
    return _orig["pow"](x, y)


def tan(x):
    if hasattr(x, "addr") or hasattr(x, "real"): return sin(x) / cos(x)
    return _orig["tan"](x)


def asin(x):
    if hasattr(x, "addr") or hasattr(x, "real"): return atan2(x, sqrt(1 - x * x))
    return _orig["asin"](x)


def acos(x):
    if hasattr(x, "addr") or hasattr(x, "real"): return atan2(sqrt(1 - x * x), x)
    return _orig["acos"](x)


def atan(x):
    if hasattr(x, "addr") or hasattr(x, "real"): return atan2(x, 1)
    return _orig["atan"](x)


def csc(x): return 1 / sin(x)


def sec(x): return 1 / cos(x)


def cot(x): return 1 / tan(x)


def acsc(x): return asin(1 / x)


def asec(x): return acos(1 / x)


def acot(x): return atan(1 / x)


def sinh(x):
    if hasattr(x, "addr") or hasattr(x, "real"): return (exp(x) - exp(-x)) / 2
    return _orig["sinh"](x)


def cosh(x):
    if hasattr(x, "addr") or hasattr(x, "real"): return (exp(x) + exp(-x)) / 2
    return _orig["cosh"](x)


def tanh(x):
    if hasattr(x, "addr") or hasattr(x, "real"): return sinh(x) / cosh(x)
    return _orig["tanh"](x)


def csch(x): return 1 / sinh(x)


def sech(x): return 1 / cosh(x)


def coth(x): return 1 / tanh(x)


def asinh(x):
    if hasattr(x, "addr") or hasattr(x, "real"): return ln(x + sqrt(x * x + 1))
    return _orig["asinh"](x)


def acosh(x):
    if hasattr(x, "addr") or hasattr(x, "real"): return ln(x + sqrt(x * x - 1))
    return _orig["acosh"](x)


def atanh(x):
    if hasattr(x, "addr") or hasattr(x, "real"): return 0.5 * ln((1 + x) / (1 - x))
    return _orig["atanh"](x)


def acsch(x): return ln(1 / x + sqrt(1 / (x * x) + 1))


def asech(x): return ln(1 / x + sqrt(1 / x - 1) * sqrt(1 / x + 1))


def acoth(x): return 0.5 * ln((x + 1) / (x - 1))


def fastsin(x):
    if hasattr(x, "__fastsin__"):
        return x.__fastsin__()
    return sin(x)


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
