### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class CustomModelDataFloats:
    index: int

@struct
class UseCycle:
    period: float

@struct
class UseDuration:
    remaining: bool

@struct
class Time:
    source: str
    wobble: bool

@struct
class Damage:
    normalize: bool

@struct
class Compass:
    target: str
    wobble: bool

@struct
class Count:
    normalize: bool