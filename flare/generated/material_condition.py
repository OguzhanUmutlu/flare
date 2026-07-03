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
VerticalAnchor = Union[{'absolute': int}, {'above_bottom': int}, {'below_top': int}, {'relative_to_sea_level': int}]

@struct
class BiomeCondition:
    biome_is: Union[list[str], str]

@struct
class MaterialCondition:
    type: Union[str, str]
MaterialConditionRef = Union[str, 'MaterialCondition']

@struct
class NoiseThresholdCondition:
    noise: str
    min_threshold: float
    max_threshold: float
    is_3d: bool

@struct
class NotCondition:
    invert: 'MaterialConditionRef'

@struct
class StoneDepthCondition:
    offset: int
    surface_type: 'CaveSurface'
    add_surface_depth: bool
    add_surface_secondary_depth: bool
    secondary_depth_range: int

@struct
class VerticalGradientCondition:
    random_name: str
    true_at_and_below: 'VerticalAnchor'
    false_at_and_above: 'VerticalAnchor'

@struct
class WaterCondition:
    offset: int
    surface_depth_multiplier: int
    add_stone_depth: bool

@struct
class YAboveCondition:
    anchor: 'VerticalAnchor'
    surface_depth_multiplier: int
    add_stone_depth: bool