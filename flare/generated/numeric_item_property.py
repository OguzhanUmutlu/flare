### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class Compass:
    target: 'Any'
    wobble: bool

@struct
class Time:
    source: 'Any'
    wobble: bool

@struct
class UseDuration:
    remaining: bool

@struct
class CustomModelDataFloats:
    index: int

@struct
class Count:
    normalize: bool

@struct
class Damage:
    normalize: bool

@struct
class UseCycle:
    period: float