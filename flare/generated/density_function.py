### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class Clamp:
    def __init__(
            self,
            input: Optional[Union['DensityFunction', Any]] = None,
            min: Optional[Union['NoiseRange', Any]] = None,
            max: Optional[Union['NoiseRange', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if input is not None:
            self.components["input"] = input
        if min is not None:
            self.components["min"] = min
        if max is not None:
            self.components["max"] = max

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class Constant:
    def __init__(
            self,
            argument: Optional[Union['NoiseRange', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if argument is not None:
            self.components["argument"] = argument

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

CubicSpline = Union[Union[float, {'coordinate': Union[str, 'DensityFunctionRef'], 'points': list['SplinePoint']}], Any]

DensityFunction = Union[Union['NoiseRange', {'type': str}], Any]

DensityFunctionRef = Union[Union[str, 'DensityFunction'], Any]

class FindTopSurface:
    def __init__(
            self,
            density: Optional[Union['DensityFunctionRef', Any]] = None,
            upper_bound: Optional[Union['DensityFunctionRef', Any]] = None,
            lower_bound: Optional[Union[int, Any]] = None,
            cell_height: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if density is not None:
            self.components["density"] = density
        if upper_bound is not None:
            self.components["upper_bound"] = upper_bound
        if lower_bound is not None:
            self.components["lower_bound"] = lower_bound
        if cell_height is not None:
            self.components["cell_height"] = cell_height

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class InvervalSelect:
    def __init__(
            self,
            input: Optional[Union['DensityFunctionRef', Any]] = None,
            thresholds: Optional[Union[list['NoiseRange'], Any]] = None,
            functions: Optional[Union[list['DensityFunctionRef'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if input is not None:
            self.components["input"] = input
        if thresholds is not None:
            self.components["thresholds"] = thresholds
        if functions is not None:
            self.components["functions"] = functions

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class Noise:
    def __init__(
            self,
            noise: Optional[Union[str, Any]] = None,
            xz_scale: Optional[Union[float, Any]] = None,
            y_scale: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if noise is not None:
            self.components["noise"] = noise
        if xz_scale is not None:
            self.components["xz_scale"] = xz_scale
        if y_scale is not None:
            self.components["y_scale"] = y_scale

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class OldBlendedNoise:
    def __init__(
            self,
            xz_scale: Optional[Union[float, Any]] = None,
            y_scale: Optional[Union[float, Any]] = None,
            xz_factor: Optional[Union[float, Any]] = None,
            y_factor: Optional[Union[float, Any]] = None,
            smear_scale_multiplier: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if xz_scale is not None:
            self.components["xz_scale"] = xz_scale
        if y_scale is not None:
            self.components["y_scale"] = y_scale
        if xz_factor is not None:
            self.components["xz_factor"] = xz_factor
        if y_factor is not None:
            self.components["y_factor"] = y_factor
        if smear_scale_multiplier is not None:
            self.components["smear_scale_multiplier"] = smear_scale_multiplier

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class OneArgument:
    def __init__(
            self,
            argument: Optional[Union['DensityFunctionRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if argument is not None:
            self.components["argument"] = argument

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class RangeChoice:
    def __init__(
            self,
            input: Optional[Union['DensityFunctionRef', Any]] = None,
            min_inclusive: Optional[Union['NoiseRange', Any]] = None,
            max_exclusive: Optional[Union['NoiseRange', Any]] = None,
            when_in_range: Optional[Union['DensityFunctionRef', Any]] = None,
            when_out_of_range: Optional[Union['DensityFunctionRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if input is not None:
            self.components["input"] = input
        if min_inclusive is not None:
            self.components["min_inclusive"] = min_inclusive
        if max_exclusive is not None:
            self.components["max_exclusive"] = max_exclusive
        if when_in_range is not None:
            self.components["when_in_range"] = when_in_range
        if when_out_of_range is not None:
            self.components["when_out_of_range"] = when_out_of_range

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class Shift:
    def __init__(
            self,
            argument: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if argument is not None:
            self.components["argument"] = argument

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class ShiftedNoise(Noise):
    def __init__(
            self,
            shift_x: Optional[Union['DensityFunctionRef', Any]] = None,
            shift_y: Optional[Union['DensityFunctionRef', Any]] = None,
            shift_z: Optional[Union['DensityFunctionRef', Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if shift_x is not None:
            self.components["shift_x"] = shift_x
        if shift_y is not None:
            self.components["shift_y"] = shift_y
        if shift_z is not None:
            self.components["shift_z"] = shift_z

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class Spline:
    def __init__(
            self,
            spline: Optional[Union['CubicSpline', Any]] = None,
            min_value: Optional[Union['NoiseRange', Any]] = None,
            max_value: Optional[Union['NoiseRange', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if spline is not None:
            self.components["spline"] = spline
        if min_value is not None:
            self.components["min_value"] = min_value
        if max_value is not None:
            self.components["max_value"] = max_value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class SplinePoint:
    def __init__(
            self,
            location: Optional[Union[float, Any]] = None,
            derivative: Optional[Union[float, Any]] = None,
            value: Optional[Union['CubicSpline', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if location is not None:
            self.components["location"] = location
        if derivative is not None:
            self.components["derivative"] = derivative
        if value is not None:
            self.components["value"] = value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class TerrainShaperSpline:
    def __init__(
            self,
            spline: Optional[Union[str, Any]] = None,
            min_value: Optional[Union['NoiseRange', Any]] = None,
            max_value: Optional[Union['NoiseRange', Any]] = None,
            continentalness: Optional[Union['DensityFunctionRef', Any]] = None,
            erosion: Optional[Union['DensityFunctionRef', Any]] = None,
            weirdness: Optional[Union['DensityFunctionRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if spline is not None:
            self.components["spline"] = spline
        if min_value is not None:
            self.components["min_value"] = min_value
        if max_value is not None:
            self.components["max_value"] = max_value
        if continentalness is not None:
            self.components["continentalness"] = continentalness
        if erosion is not None:
            self.components["erosion"] = erosion
        if weirdness is not None:
            self.components["weirdness"] = weirdness

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class TwoArguments:
    def __init__(
            self,
            argument1: Optional[Union['DensityFunctionRef', Any]] = None,
            argument2: Optional[Union['DensityFunctionRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if argument1 is not None:
            self.components["argument1"] = argument1
        if argument2 is not None:
            self.components["argument2"] = argument2

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class WeirdScaledSampler:
    def __init__(
            self,
            rarity_value_mapper: Optional[Union[str, Any]] = None,
            noise: Optional[Union[str, Any]] = None,
            input: Optional[Union['DensityFunctionRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if rarity_value_mapper is not None:
            self.components["rarity_value_mapper"] = rarity_value_mapper
        if noise is not None:
            self.components["noise"] = noise
        if input is not None:
            self.components["input"] = input

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

class YClampedGradient:
    def __init__(
            self,
            from_y: Optional[Union[int, Any]] = None,
            to_y: Optional[Union[int, Any]] = None,
            from_value: Optional[Union['NoiseRange', Any]] = None,
            to_value: Optional[Union['NoiseRange', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if from_y is not None:
            self.components["from_y"] = from_y
        if to_y is not None:
            self.components["to_y"] = to_y
        if from_value is not None:
            self.components["from_value"] = from_value
        if to_value is not None:
            self.components["to_value"] = to_value

    def to_dict(self):
        res = {}
        for k, v in self.components.items():
            if hasattr(v, 'to_dict'):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [x.to_dict() if hasattr(x, 'to_dict') else x for x in v]
            else:
                res[k] = v
        return res

