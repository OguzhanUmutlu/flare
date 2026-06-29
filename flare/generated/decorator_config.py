### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class ConfiguredDecorator:
    type: str
    config: Any

@struct
class CountNoiseBiasedConfig:
    noise_to_count_ratio: int
    noise_factor: float
    noise_offset: float

@struct
class DecoratedConfig:
    outer: 'ConfiguredDecorator'
    inner: 'ConfiguredDecorator'

@struct
class CountConfig:
    count: Union['UniformInt', 'IntProvider']

@struct
class CountExtraConfig:
    count: Union[int, int]
    extra_count: Union[int, int]
    extra_chance: float

@struct
class HeightmapConfig:
    heightmap: str

@struct
class CarvingMaskConfig:
    step: str
    probability: float

@struct
class DepthAverageConfig:
    baseline: int
    spread: int

@struct
class WaterDepthThresholdConfig:
    max_water_depth: int

@struct
class ChanceConfig:
    chance: int

@struct
class OldRangeConfig:
    maximum: int
    bottom_offset: int
    top_offset: int

@struct
class CountNoiseConfig:
    noise_level: float
    below_noise: int
    above_noise: int

@struct
class CaveSurface:
    surface: Union[Any, Any]
    floor_to_ceiling_search_range: int