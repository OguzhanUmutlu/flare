### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class CarvingMaskConfig:
    step: 'Any'
    probability: float

@struct
class CountNoiseBiasedConfig:
    noise_to_count_ratio: int
    noise_factor: float
    noise_offset: float

@struct
class CountNoiseConfig:
    noise_level: float
    below_noise: int
    above_noise: int

@struct
class HeightmapConfig:
    heightmap: 'Any'

@struct
class ChanceConfig:
    chance: int

@struct
class WaterDepthThresholdConfig:
    max_water_depth: int

@struct
class ConfiguredDecorator:
    type: str
    config: Any

@struct
class DepthAverageConfig:
    baseline: int
    spread: int

@struct
class OldRangeConfig:
    maximum: int
    bottom_offset: int
    top_offset: int

@struct
class DecoratedConfig:
    outer: 'ConfiguredDecorator'
    inner: 'ConfiguredDecorator'

@struct
class CaveSurface:
    surface: Any
    floor_to_ceiling_search_range: int

@struct
class CountExtraConfig:
    count: Any
    extra_count: Any
    extra_chance: float

@struct
class CountConfig:
    count: Any