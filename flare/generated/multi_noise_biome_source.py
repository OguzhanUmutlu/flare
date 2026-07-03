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
ClimateParameter = Union[float, list[float]]

@struct
class ClimateParameters:
    temperature: 'ClimateParameter'
    humidity: 'ClimateParameter'
    altitude: float
    continentalness: 'ClimateParameter'
    erosion: 'ClimateParameter'
    weirdness: 'ClimateParameter'
    depth: 'ClimateParameter'
    offset: float

@struct
class DirectMultiNoise:
    temperature_noise: 'NoiseParameters'
    humidity_noise: 'NoiseParameters'
    altitude_noise: 'NoiseParameters'
    weirdness_noise: 'NoiseParameters'
    biomes: list[{'biome': str, 'parameters': 'ClimateParameters'}]

@struct
class NoiseParameters:
    firstOctave: int
    amplitudes: list[double]