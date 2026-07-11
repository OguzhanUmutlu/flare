from .bigscore import bigscore, bigfixed
from .block import block
from .builtins import fail
from .complex import complex
from .core import UnsupportedOperandError, BinaryOp, UnaryOp, macro, ref
from .float32 import float32
from .float64 import float64
from .item import item
from .nbt import nbt, struct
from .objective import Objective
from .score import score, fixed, getscore, INT32_LIMIT
from .selector import selector
from .storage import _Storage
from ..types import byte, boolean, short, long, double, array, compound

storage = _Storage()

nbtbyte = nbt[byte]
nbtbool = nbt[boolean]
nbtshort = nbt[short]
nbtint = nbt[int]
nbtlong = nbt[long]
nbtfloat = nbt[float]
nbtdouble = nbt[double]
nbtstr = nbt[str]
nbtlist = nbt[list]
nbtcompound = nbt[compound]
nbtbytearray = nbt[array[byte]]
nbtintarray = nbt[array[int]]
nbtlongarray = nbt[array[long]]

__all__ = ["bigscore", "bigfixed", "fail", "complex", "UnsupportedOperandError", "BinaryOp", "UnaryOp", "macro", "ref",
           "float32", "float64", "nbt", "struct", "Objective", "score", "fixed", "getscore", "INT32_LIMIT", "selector",
           "storage", "nbtbyte", "nbtbool", "nbtshort", "nbtint", "nbtlong", "nbtfloat", "nbtdouble", "nbtstr",
           "nbtlist", "nbtcompound", "nbtbytearray", "nbtintarray", "nbtlongarray", "block", "item"]
