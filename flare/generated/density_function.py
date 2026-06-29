### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

@struct
class Constant:
    argument: 'NoiseRange'

@struct
class InvervalSelect:
    input: 'DensityFunctionRef'
    thresholds: list['NoiseRange']
    functions: list['DensityFunctionRef']

@struct
class FindTopSurface:
    density: 'DensityFunctionRef'
    upper_bound: 'DensityFunctionRef'
    lower_bound: int
    cell_height: int

@struct
class OldBlendedNoise:
    xz_scale: float
    y_scale: float
    xz_factor: float
    y_factor: float
    smear_scale_multiplier: float

@struct
class YClampedGradient:
    from_y: int
    to_y: int
    from_value: 'NoiseRange'
    to_value: 'NoiseRange'

@struct
class WeirdScaledSampler:
    rarity_value_mapper: str
    noise: str
    input: 'DensityFunctionRef'

@struct
class SplinePoint:
    location: float
    derivative: float
    value: 'CubicSpline'

@struct
class Noise:
    noise: str
    xz_scale: float
    y_scale: float
DensityFunction = Union['NoiseRange', {'type': str}]

@struct
class Shift:
    argument: str
DensityFunctionRef = Union[str, 'DensityFunction']

@struct
class Spline:
    spline: 'CubicSpline'
    min_value: 'NoiseRange'
    max_value: 'NoiseRange'

@struct
class Clamp:
    input: 'DensityFunction'
    min: 'NoiseRange'
    max: 'NoiseRange'

@struct
class OneArgument:
    argument: 'DensityFunctionRef'

@struct
class TerrainShaperSpline:
    spline: str
    min_value: 'NoiseRange'
    max_value: 'NoiseRange'
    continentalness: 'DensityFunctionRef'
    erosion: 'DensityFunctionRef'
    weirdness: 'DensityFunctionRef'

@struct
class TwoArguments:
    argument1: 'DensityFunctionRef'
    argument2: 'DensityFunctionRef'

@struct
class RangeChoice:
    input: 'DensityFunctionRef'
    min_inclusive: 'NoiseRange'
    max_exclusive: 'NoiseRange'
    when_in_range: 'DensityFunctionRef'
    when_out_of_range: 'DensityFunctionRef'
CubicSpline = Union[float, {'coordinate': Union[str, 'DensityFunctionRef'], 'points': list['SplinePoint']}]

@struct
class ShiftedNoise(Noise):
    shift_x: 'DensityFunctionRef'
    shift_y: 'DensityFunctionRef'
    shift_z: 'DensityFunctionRef'