### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class CanyonShape:
    distance_factor: 'Any'
    thickness: 'Any'
    width_smoothness: int
    horizontal_radius_factor: 'Any'
    vertical_radius_default_factor: float
    vertical_radius_center_factor: float

@struct
class CanyonConfig:
    vertical_rotation: 'Any'
    shape: 'CanyonShape'

@struct
class CaveConfig:
    horizontal_radius_multiplier: 'Any'
    vertical_radius_multiplier: 'Any'
    floor_level: 'Any'