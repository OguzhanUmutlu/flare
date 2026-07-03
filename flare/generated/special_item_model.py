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
class Banner:
    color: 'DyeColor'
    attachment: str

@struct
class Bed:
    texture: str
    part: str

@struct
class Book:
    open_angle: float
    page1: float
    page2: float

@struct
class Chest:
    texture: str
    openness: float
    chest_type: str

@struct
class CopperGolemStatue:
    pose: str
    texture: str

@struct
class EndCube:
    effect: str

@struct
class HangingSign:
    wood_type: str
    texture: str
    attachment: str

@struct
class Head:
    kind: str
    animation: float

@struct
class ShulkerBox:
    texture: str
    openness: float
    orientation: str

@struct
class StandingSign:
    wood_type: str
    texture: str
    attachement: str