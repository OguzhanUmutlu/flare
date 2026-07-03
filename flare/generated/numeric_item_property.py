### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
import typing
from typing import Any
if typing.TYPE_CHECKING:
    from typing import Union
else:

    class _DummyUnion:

        def __getitem__(self, items):
            return typing.Any
    Union = _DummyUnion()

@struct
class Compass:
    target: str
    wobble: bool

@struct
class Count:
    normalize: bool

@struct
class CustomModelDataFloats:
    index: int

@struct
class Damage:
    normalize: bool

@struct
class Time:
    source: str
    wobble: bool

@struct
class UseCycle:
    period: float

@struct
class UseDuration:
    remaining: bool