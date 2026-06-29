### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class CaveConfig:
    horizontal_radius_multiplier: 'FloatProvider'
    vertical_radius_multiplier: 'FloatProvider'
    floor_level: 'FloatProvider'

@struct
class CanyonConfig:
    vertical_rotation: 'FloatProvider'
    shape: 'CanyonShape'

@struct
class CanyonShape:
    distance_factor: 'FloatProvider'
    thickness: 'FloatProvider'
    width_smoothness: int
    horizontal_radius_factor: 'FloatProvider'
    vertical_radius_default_factor: float
    vertical_radius_center_factor: float