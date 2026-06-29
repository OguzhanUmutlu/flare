### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class NoiseParameters:
    firstOctave: int
    amplitudes: list[double]

@struct
class DirectMultiNoise:
    temperature_noise: 'NoiseParameters'
    humidity_noise: 'NoiseParameters'
    altitude_noise: 'NoiseParameters'
    weirdness_noise: 'NoiseParameters'
    biomes: list[dict]