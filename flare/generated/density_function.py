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
class Clamp:
    input: 'DensityFunction'
    min: 'NoiseRange'
    max: 'NoiseRange'

@struct
class Constant:
    argument: 'NoiseRange'
CubicSpline = Union[float, {'coordinate': Union[str, 'DensityFunctionRef'], 'points': list['SplinePoint']}]
DensityFunction = Union['NoiseRange', {'type': str}]
DensityFunctionRef = Union[str, 'DensityFunction']

@struct
class FindTopSurface:
    density: 'DensityFunctionRef'
    upper_bound: 'DensityFunctionRef'
    lower_bound: int
    cell_height: int

@struct
class InvervalSelect:
    input: 'DensityFunctionRef'
    thresholds: list['NoiseRange']
    functions: list['DensityFunctionRef']

@struct
class Noise:
    noise: str
    xz_scale: float
    y_scale: float

@struct
class OldBlendedNoise:
    xz_scale: float
    y_scale: float
    xz_factor: float
    y_factor: float
    smear_scale_multiplier: float

@struct
class OneArgument:
    argument: 'DensityFunctionRef'

@struct
class RangeChoice:
    input: 'DensityFunctionRef'
    min_inclusive: 'NoiseRange'
    max_exclusive: 'NoiseRange'
    when_in_range: 'DensityFunctionRef'
    when_out_of_range: 'DensityFunctionRef'

@struct
class Shift:
    argument: str

@struct
class ShiftedNoise(Noise):
    shift_x: 'DensityFunctionRef'
    shift_y: 'DensityFunctionRef'
    shift_z: 'DensityFunctionRef'

@struct
class Spline:
    spline: 'CubicSpline'
    min_value: 'NoiseRange'
    max_value: 'NoiseRange'

@struct
class SplinePoint:
    location: float
    derivative: float
    value: 'CubicSpline'

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
class WeirdScaledSampler:
    rarity_value_mapper: str
    noise: str
    input: 'DensityFunctionRef'

@struct
class YClampedGradient:
    from_y: int
    to_y: int
    from_value: 'NoiseRange'
    to_value: 'NoiseRange'