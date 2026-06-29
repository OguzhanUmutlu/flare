### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class VerticalGradientCondition:
    random_name: str
    true_at_and_below: 'Any'
    false_at_and_above: 'Any'

@struct
class NoiseThresholdCondition:
    noise: str
    min_threshold: float
    max_threshold: float
    is_3d: bool

@struct
class BiomeCondition:
    biome_is: Any

@struct
class StoneDepthCondition:
    offset: int
    surface_type: 'CaveSurface'
    add_surface_depth: bool
    add_surface_secondary_depth: bool
    secondary_depth_range: int

@struct
class WaterCondition:
    offset: int
    surface_depth_multiplier: int
    add_stone_depth: bool

@struct
class YAboveCondition:
    anchor: 'Any'
    surface_depth_multiplier: int
    add_stone_depth: bool

@struct
class NotCondition:
    invert: 'Any'