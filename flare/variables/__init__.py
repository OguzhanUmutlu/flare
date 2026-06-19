from .bigscore import bigscore, bigfixed
from .complex import complex_type
from .core import UnsupportedOperandError, BinaryOp, UnaryOp
from .float32 import float32
from .float64 import float64
from .nbt import nbt
from .score import score, fixed, getscore, INT32_LIMIT
from .selector import selector, tagged, ref
from .storage import _Storage
from ..types import byte, boolean, short, long, double

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
nbtdict = nbt[dict]
nbtbytearray = nbt[list[byte]]
nbtintarray = nbt[list[int]]
nbtlongarray = nbt[list[long]]
