### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class OneArgument:
    argument: 'Any'

@struct
class Spline:
    spline: 'Any'
    min_value: 'Any'
    max_value: 'Any'

@struct
class InvervalSelect:
    input: 'Any'
    thresholds: list['Any']
    functions: list['Any']

@struct
class WeirdScaledSampler:
    rarity_value_mapper: 'Any'
    noise: str
    input: 'Any'

@struct
class YClampedGradient:
    from_y: int
    to_y: int
    from_value: 'Any'
    to_value: 'Any'

@struct
class Noise:
    noise: str
    xz_scale: float
    y_scale: float

@struct
class ShiftedNoise(Noise):
    shift_x: 'Any'
    shift_y: 'Any'
    shift_z: 'Any'

@struct
class RangeChoice:
    input: 'Any'
    min_inclusive: 'Any'
    max_exclusive: 'Any'
    when_in_range: 'Any'
    when_out_of_range: 'Any'

@struct
class Shift:
    argument: str

@struct
class OldBlendedNoise:
    xz_scale: float
    y_scale: float
    xz_factor: float
    y_factor: float
    smear_scale_multiplier: float

@struct
class TerrainShaperSpline:
    spline: 'Any'
    min_value: 'Any'
    max_value: 'Any'
    continentalness: 'Any'
    erosion: 'Any'
    weirdness: 'Any'

@struct
class Constant:
    argument: 'Any'

@struct
class FindTopSurface:
    density: 'Any'
    upper_bound: 'Any'
    lower_bound: int
    cell_height: int

@struct
class TwoArguments:
    argument1: 'Any'
    argument2: 'Any'

@struct
class Clamp:
    input: 'Any'
    min: 'Any'
    max: 'Any'