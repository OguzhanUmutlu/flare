### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class HeightRangeModifier:
    height: 'Any'

@struct
class SurfaceRelativeThresholdFilter:
    heightmap: 'Any'
    min_inclusive: int
    max_inclusive: int

@struct
class CountModifier:
    count: Any

@struct
class BlockPredicate:
    type: str

@struct
class HeightmapModifier:
    heightmap: 'Any'

@struct
class NoiseBasedCountModifier:
    noise_to_count_ratio: int
    noise_factor: float
    noise_offset: float

@struct
class FixedPlacementModifier:
    positions: list[list[int]]

@struct
class CarvingMaskModifier:
    step: 'Any'

@struct
class RarityFilter:
    chance: int

@struct
class RandomOffsetModifier:
    xz_spread: 'Any'
    y_spread: 'Any'

@struct
class NoiseThresholdCountModifier:
    noise_level: float
    below_noise: int
    above_noise: int

@struct
class CountOnEveryLayerModifier:
    count: 'Any'

@struct
class EnvironmentScanModifier:
    direction_of_search: 'Any'
    max_steps: int
    target_condition: 'BlockPredicate'
    allowed_search_condition: 'BlockPredicate'

@struct
class SurfaceWaterDepthFilter:
    max_water_depth: int

@struct
class BlockPredicateFilter:
    predicate: 'BlockPredicate'