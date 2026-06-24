try:
    from importlib.metadata import version as _get_version

    __version__ = _get_version("flaremc")
except Exception:
    __version__ = "latest"

from .compiler import _flatten_and, _eval_to_bool_score, _compile_relational
from .context import namespace, export, tick, push_context, runcommand, files, temp_obj, constant_obj, vars_obj, \
    constants, _flare_assign, _flare_aug_assign, _flare_print, dbg, _flare_return, _flare_in, _flare_notin, \
    _flare_print as print, style
from .control_flow import _flare_if, _flare_while, _flare_for, _flare_with, _flare_break, _flare_continue, expand, \
    schedule
from .execute_modifiers import _as, at, positioned, aligned, facing, anchored, rotated, dimension, applyon, on, summon, \
    store, ExecuteChain, StoreExecuteChain
from .math import round_, floor, ceil
from .types import NBTType, byte, boolean, short, long, double, array
from .variables import score, nbt, fixed, tagged, ref, getscore, storage, nbtbyte, nbtbool, nbtshort, nbtint, nbtlong, \
    nbtfloat, nbtdouble, nbtstr, nbtlist, nbtdict, nbtbytearray, nbtintarray, nbtlongarray, selector, bigscore, \
    bigfixed, float64, float32, complex, macro

__all__ = ["round_", "floor", "ceil", "namespace", "export", "tick", "score", "nbt", "fixed", "tagged", "ref",
           "getscore", "storage", "_flare_print", "dbg", "nbtbyte", "nbtbool", "nbtshort", "nbtint", "nbtlong",
           "nbtfloat", "nbtdouble", "nbtstr", "nbtlist", "nbtdict", "nbtbytearray", "nbtintarray", "nbtlongarray",
           "selector", "_as", "at", "positioned", "aligned", "facing", "anchored", "rotated", "dimension", "applyon",
           "on", "summon", "store", "ExecuteChain", "StoreExecuteChain", "array", "bigscore", "bigfixed", "float32",
           "float64", "complex", "byte", "boolean", "short", "long", "double", "expand", "macro", "schedule", "print",
           "style"]
