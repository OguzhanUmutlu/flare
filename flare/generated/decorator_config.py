### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class CarvingMaskConfig:
    def __init__(
            self,
            step: Optional[Union[str, Any]] = None,
            probability: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if step is not None:
            self.components["step"] = step
        if probability is not None:
            self.components["probability"] = probability

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

class CaveSurface:
    def __init__(
            self,
            surface: Optional[Union[Union[Any, Any], Any]] = None,
            floor_to_ceiling_search_range: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if surface is not None:
            self.components["surface"] = surface
        if floor_to_ceiling_search_range is not None:
            self.components["floor_to_ceiling_search_range"] = floor_to_ceiling_search_range

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

class ChanceConfig:
    def __init__(
            self,
            chance: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if chance is not None:
            self.components["chance"] = chance

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

class ConfiguredDecorator:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
            config: Optional[Union[Any, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type
        if config is not None:
            self.components["config"] = config

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

class CountConfig:
    def __init__(
            self,
            count: Optional[Union[Union['UniformInt', 'IntProvider'], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if count is not None:
            self.components["count"] = count

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

class CountExtraConfig:
    def __init__(
            self,
            count: Optional[Union[Union[int, int], Any]] = None,
            extra_count: Optional[Union[Union[int, int], Any]] = None,
            extra_chance: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if count is not None:
            self.components["count"] = count
        if extra_count is not None:
            self.components["extra_count"] = extra_count
        if extra_chance is not None:
            self.components["extra_chance"] = extra_chance

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

class CountNoiseBiasedConfig:
    def __init__(
            self,
            noise_to_count_ratio: Optional[Union[int, Any]] = None,
            noise_factor: Optional[Union[float, Any]] = None,
            noise_offset: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if noise_to_count_ratio is not None:
            self.components["noise_to_count_ratio"] = noise_to_count_ratio
        if noise_factor is not None:
            self.components["noise_factor"] = noise_factor
        if noise_offset is not None:
            self.components["noise_offset"] = noise_offset

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

class CountNoiseConfig:
    def __init__(
            self,
            noise_level: Optional[Union[float, Any]] = None,
            below_noise: Optional[Union[int, Any]] = None,
            above_noise: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if noise_level is not None:
            self.components["noise_level"] = noise_level
        if below_noise is not None:
            self.components["below_noise"] = below_noise
        if above_noise is not None:
            self.components["above_noise"] = above_noise

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

class DecoratedConfig:
    def __init__(
            self,
            outer: Optional[Union['ConfiguredDecorator', Any]] = None,
            inner: Optional[Union['ConfiguredDecorator', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if outer is not None:
            self.components["outer"] = outer
        if inner is not None:
            self.components["inner"] = inner

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

class DepthAverageConfig:
    def __init__(
            self,
            baseline: Optional[Union[int, Any]] = None,
            spread: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if baseline is not None:
            self.components["baseline"] = baseline
        if spread is not None:
            self.components["spread"] = spread

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

class HeightmapConfig:
    def __init__(
            self,
            heightmap: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if heightmap is not None:
            self.components["heightmap"] = heightmap

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

class OldRangeConfig:
    def __init__(
            self,
            maximum: Optional[Union[int, Any]] = None,
            bottom_offset: Optional[Union[int, Any]] = None,
            top_offset: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if maximum is not None:
            self.components["maximum"] = maximum
        if bottom_offset is not None:
            self.components["bottom_offset"] = bottom_offset
        if top_offset is not None:
            self.components["top_offset"] = top_offset

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

class WaterDepthThresholdConfig:
    def __init__(
            self,
            max_water_depth: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if max_water_depth is not None:
            self.components["max_water_depth"] = max_water_depth

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

