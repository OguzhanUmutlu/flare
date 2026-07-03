### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union
HeightProvider = Union[{'type': str}, 'VerticalAnchor']
VerticalAnchor = Union[{'absolute': int}, {'above_bottom': int}, {'below_top': int}, {'relative_to_sea_level': int}]

@struct
class CarverConfigBase:
    probability: float
    replaceable: Union[list[str], str]
    y: 'HeightProvider'

@struct
class CanyonConfig(CarverConfigBase):
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
    y_scale: 'FloatProvider'

@struct
class CarverDebugSettings:
    debug_mode: bool
    air_state: 'BlockState'
    water_state: 'BlockState'
    lava_state: 'BlockState'
    barrier_state: 'BlockState'

@struct
class CaveConfig(CarverConfigBase):
    count: 'IntProvider'
    thickness: 'FloatProvider'
    weird_thickness_bias: bool
    room_vertical_radius_multiplier: 'FloatProvider'
    horizontal_radius_multiplier: 'FloatProvider'
    vertical_radius_multiplier: 'FloatProvider'
    start_vertical_radiues_multiplier: 'FloatProvider'
    floor_level: 'FloatProvider'

@struct
class BlockState:
    Name: str
    Properties: Any