### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

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