### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class RandomOffsetModifier:
    xz_spread: 'IntProvider'
    y_spread: 'IntProvider'

@struct
class CountModifier:
    count: Union['IntProvider', 'IntProvider']

@struct
class HeightRangeModifier:
    height: 'HeightProvider'

@struct
class SurfaceWaterDepthFilter:
    max_water_depth: int
VerticalAnchor = Union[{'absolute': int}, {'above_bottom': int}, {'below_top': int}]

@struct
class BlockPredicate:
    type: str
HeightProvider = Union[{'type': str}, 'VerticalAnchor']

@struct
class RarityFilter:
    chance: int

@struct
class NoiseBasedCountModifier:
    noise_to_count_ratio: int
    noise_factor: float
    noise_offset: float

@struct
class NoiseThresholdCountModifier:
    noise_level: float
    below_noise: int
    above_noise: int

@struct
class EnvironmentScanModifier:
    direction_of_search: str
    max_steps: int
    target_condition: 'BlockPredicate'
    allowed_search_condition: 'BlockPredicate'

@struct
class CarvingMaskModifier:
    step: str

@struct
class CountOnEveryLayerModifier:
    count: 'IntProvider'

@struct
class FixedPlacementModifier:
    positions: list[list[int]]

@struct
class HeightmapModifier:
    heightmap: str

@struct
class SurfaceRelativeThresholdFilter:
    heightmap: str
    min_inclusive: int
    max_inclusive: int

@struct
class BlockPredicateFilter:
    predicate: 'BlockPredicate'