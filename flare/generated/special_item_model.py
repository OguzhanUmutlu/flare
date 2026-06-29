### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class Book:
    open_angle: float
    page1: float
    page2: float

@struct
class StandingSign:
    wood_type: 'Any'
    texture: str
    attachement: 'Any'

@struct
class Bed:
    texture: str
    part: 'Any'

@struct
class Chest:
    texture: str
    openness: float
    chest_type: 'Any'

@struct
class Head:
    kind: 'Any'
    animation: float

@struct
class CopperGolemStatue:
    pose: 'Any'
    texture: str

@struct
class EndCube:
    effect: 'Any'

@struct
class HangingSign:
    wood_type: 'Any'
    texture: str
    attachment: 'Any'

@struct
class ShulkerBox:
    texture: str
    openness: float
    orientation: 'Any'

@struct
class Banner:
    color: 'Any'
    attachment: 'Any'