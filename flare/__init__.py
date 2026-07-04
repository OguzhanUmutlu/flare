try:
    from importlib.metadata import version as _get_version

    __version__ = _get_version("flaremc")
except Exception:
    __version__ = "latest"

from .compiler import _flatten_and, _eval_to_bool_score, _compile_relational
from .context import namespace, export, tick, load, push_context, runcommand, files, temp_obj, constant_obj, vars_obj, \
    constants, _flare_assign, _flare_aug_assign, _flare_print, dbg, _flare_return, _flare_in, _flare_notin, \
    _flare_print as print, style, _flare_enter_scope, _flare_exit_scope
from .control_flow import _flare_if, _flare_while, _flare_for, _flare_not, _flare_with, _flare_as_var, _flare_break, \
    _flare_continue, \
    expand, schedule, _flare_and, _flare_or
from .data_driven import *
from .execute_modifiers import _as, at, positioned, aligned, facing, anchored, rotated, dimension, applyon, on, summon, \
    store, ExecuteChain, StoreExecuteChain, if_, unless, if_block, unless_block
from .math import round_, floor, ceil, sin, cos, tan, asin, acos, atan, atan2, exp, log, ln, pow_, csc, sec, cot, acsc, \
    asec, acot, sinh, cosh, tanh, asinh, acosh, atanh, csch, sech, coth, acsch, asech, acoth, sqrt, fastsin, fastsqrt, \
    rsqrt, min_, max_
from .print import translate, keybind, click_event, hover_event
from .types import NBTType, byte, boolean, short, long, double, array
from .variables import score, nbt, fixed, tagged, ref, getscore, storage, nbtbyte, nbtbool, nbtshort, nbtint, nbtlong, \
    nbtfloat, nbtdouble, nbtstr, nbtlist, nbtcompound, nbtbytearray, nbtintarray, nbtlongarray, selector, bigscore, \
    bigfixed, float64, float32, complex, macro, struct, compound, fail, Objective, block

__all__ = ["round_", "floor", "ceil", "namespace", "export", "tick", "load", "score", "nbt", "fixed", "tagged", "ref",
           "getscore", "storage", "_flare_print", "dbg", "nbtbyte", "nbtbool", "nbtshort", "nbtint", "nbtlong",
           "nbtfloat", "nbtdouble", "nbtstr", "nbtlist", "nbtcompound", "nbtbytearray", "nbtintarray", "nbtlongarray",
           "selector", "_as", "at", "positioned", "aligned", "facing", "anchored", "rotated", "dimension", "applyon",
           "on", "summon", "store", "if_", "unless", "if_block", "unless_block", "ExecuteChain", "StoreExecuteChain",
           "array", "bigscore", "bigfixed", "float32", "float64", "complex", "byte", "boolean", "short", "long",
           "double", "expand", "macro", "schedule", "print", "style", "translate", "keybind", "click_event",
           "hover_event", "struct", "sin", "cos", "tan", "asin", "acos", "atan", "atan2", "exp", "log", "ln", "pow_",
           "csc", "coth", "acsch", "asech", "acoth", "sqrt", "fastsin", "fastsqrt", "rsqrt", "min_", "max_", "block"]

from .data_driven import __all__ as _dd_all

__all__.extend(_dd_all)

try:
    from .beet import beet_default as beet_default  # noqa: F401
except ImportError:
    pass

from .variables.builtins import flare_len as len
from .variables.core import nostack
from .variables.regex import re_patch as re
