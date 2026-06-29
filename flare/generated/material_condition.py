### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class YAboveCondition:
    anchor: 'VerticalAnchor'
    surface_depth_multiplier: int
    add_stone_depth: bool
MaterialConditionRef = Union[str, 'MaterialCondition']

@struct
class StoneDepthCondition:
    offset: int
    surface_type: 'CaveSurface'
    add_surface_depth: bool
    add_surface_secondary_depth: bool
    secondary_depth_range: int
VerticalAnchor = Union[{'absolute': int}, {'above_bottom': int}, {'below_top': int}]

@struct
class NotCondition:
    invert: 'MaterialConditionRef'

@struct
class BiomeCondition:
    biome_is: Union[list[str], str]

@struct
class NoiseThresholdCondition:
    noise: str
    min_threshold: float
    max_threshold: float
    is_3d: bool

@struct
class WaterCondition:
    offset: int
    surface_depth_multiplier: int
    add_stone_depth: bool

@struct
class VerticalGradientCondition:
    random_name: str
    true_at_and_below: 'VerticalAnchor'
    false_at_and_above: 'VerticalAnchor'

@struct
class MaterialCondition:
    type: Union[str, str]