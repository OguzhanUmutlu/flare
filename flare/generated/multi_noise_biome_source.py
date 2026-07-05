### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

ClimateParameter = Union[Union[float, list[float]], Any]

class ClimateParameters:
    def __init__(
            self,
            temperature: Optional[Union['ClimateParameter', Any]] = None,
            humidity: Optional[Union['ClimateParameter', Any]] = None,
            altitude: Optional[Union[float, Any]] = None,
            continentalness: Optional[Union['ClimateParameter', Any]] = None,
            erosion: Optional[Union['ClimateParameter', Any]] = None,
            weirdness: Optional[Union['ClimateParameter', Any]] = None,
            depth: Optional[Union['ClimateParameter', Any]] = None,
            offset: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if temperature is not None:
            self.components["temperature"] = temperature
        if humidity is not None:
            self.components["humidity"] = humidity
        if altitude is not None:
            self.components["altitude"] = altitude
        if continentalness is not None:
            self.components["continentalness"] = continentalness
        if erosion is not None:
            self.components["erosion"] = erosion
        if weirdness is not None:
            self.components["weirdness"] = weirdness
        if depth is not None:
            self.components["depth"] = depth
        if offset is not None:
            self.components["offset"] = offset

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

class DirectMultiNoise:
    def __init__(
            self,
            temperature_noise: Optional[Union['NoiseParameters', Any]] = None,
            humidity_noise: Optional[Union['NoiseParameters', Any]] = None,
            altitude_noise: Optional[Union['NoiseParameters', Any]] = None,
            weirdness_noise: Optional[Union['NoiseParameters', Any]] = None,
            biomes: Optional[Union[list[{'biome': str, 'parameters': 'ClimateParameters'}], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if temperature_noise is not None:
            self.components["temperature_noise"] = temperature_noise
        if humidity_noise is not None:
            self.components["humidity_noise"] = humidity_noise
        if altitude_noise is not None:
            self.components["altitude_noise"] = altitude_noise
        if weirdness_noise is not None:
            self.components["weirdness_noise"] = weirdness_noise
        if biomes is not None:
            self.components["biomes"] = biomes

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

class NoiseParameters:
    def __init__(
            self,
            firstOctave: Optional[Union[int, Any]] = None,
            amplitudes: Optional[Union[list[double], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if firstOctave is not None:
            self.components["firstOctave"] = firstOctave
        if amplitudes is not None:
            self.components["amplitudes"] = amplitudes

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

