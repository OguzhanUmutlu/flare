from .bigscore import bigscore, bigfixed
from .complex import complex
from .core import UnsupportedOperandError, BinaryOp, UnaryOp
from .float32 import float32
from .float64 import float64
from .nbt import nbt
from .score import score, fixed, getscore, INT32_LIMIT
from .selector import selector, tagged, ref
from .storage import _Storage
from ..types import byte, boolean, short, long, double

storage = _Storage()


class macro:
    _is_macro_param = True

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"$({self.name})"

    def __format__(self, format_spec):
        return format(str(self), format_spec)

    def __repr__(self):
        return f"macro({self.name!r})"

    def _bad_op(self, *_):
        raise TypeError(
            f"Macro '{self.name}' cannot be used in arithmetic expressions. "
            "Use it inside commands or NBT string assignments."
        )

    __add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = _bad_op

nbtbyte = nbt[byte]
nbtbool = nbt[boolean]
nbtshort = nbt[short]
nbtint = nbt[int]
nbtlong = nbt[long]
nbtfloat = nbt[float]
nbtdouble = nbt[double]
nbtstr = nbt[str]
nbtlist = nbt[list]
nbtdict = nbt[dict]
nbtbytearray = nbt[list[byte]]
nbtintarray = nbt[list[int]]
nbtlongarray = nbt[list[long]]
