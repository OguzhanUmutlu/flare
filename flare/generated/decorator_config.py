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

@struct
class CarvingMaskConfig:
    step: str
    probability: float

@struct
class CaveSurface:
    surface: Union[Any, Any]
    floor_to_ceiling_search_range: int

@struct
class ChanceConfig:
    chance: int

@struct
class ConfiguredDecorator:
    type: str
    config: Any

@struct
class CountConfig:
    count: Union['UniformInt', 'IntProvider']

@struct
class CountExtraConfig:
    count: Union[int, int]
    extra_count: Union[int, int]
    extra_chance: float

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
class DecoratedConfig:
    outer: 'ConfiguredDecorator'
    inner: 'ConfiguredDecorator'

@struct
class DepthAverageConfig:
    baseline: int
    spread: int

@struct
class HeightmapConfig:
    heightmap: str

@struct
class OldRangeConfig:
    maximum: int
    bottom_offset: int
    top_offset: int

@struct
class WaterDepthThresholdConfig:
    max_water_depth: int