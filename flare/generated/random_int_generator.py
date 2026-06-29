### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class UniformIntGenerator:
    min: int
    max: int

@struct
class BinomialIntGenerator:
    n: int
    p: float

@struct
class ConstantIntGenerator:
    value: int