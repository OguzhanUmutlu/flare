### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

VerticalAnchor = Union[Union[{'absolute': int}, {'above_bottom': int}, {'below_top': int}, {'relative_to_sea_level': int}], Any]

class BiomeCondition:
    def __init__(
            self,
            biome_is: Optional[Union[Union[list[str], str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if biome_is is not None:
            self.components["biome_is"] = biome_is

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

class MaterialCondition:
    def __init__(
            self,
            type: Optional[Union[Union[str, str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if type is not None:
            self.components["type"] = type

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

MaterialConditionRef = Union[Union[str, 'MaterialCondition'], Any]

class NoiseThresholdCondition:
    def __init__(
            self,
            noise: Optional[Union[str, Any]] = None,
            min_threshold: Optional[Union[float, Any]] = None,
            max_threshold: Optional[Union[float, Any]] = None,
            is_3d: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if noise is not None:
            self.components["noise"] = noise
        if min_threshold is not None:
            self.components["min_threshold"] = min_threshold
        if max_threshold is not None:
            self.components["max_threshold"] = max_threshold
        if is_3d is not None:
            self.components["is_3d"] = is_3d

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

class NotCondition:
    def __init__(
            self,
            invert: Optional[Union['MaterialConditionRef', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if invert is not None:
            self.components["invert"] = invert

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

class StoneDepthCondition:
    def __init__(
            self,
            offset: Optional[Union[int, Any]] = None,
            surface_type: Optional[Union['CaveSurface', Any]] = None,
            add_surface_depth: Optional[Union[bool, Any]] = None,
            add_surface_secondary_depth: Optional[Union[bool, Any]] = None,
            secondary_depth_range: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if offset is not None:
            self.components["offset"] = offset
        if surface_type is not None:
            self.components["surface_type"] = surface_type
        if add_surface_depth is not None:
            self.components["add_surface_depth"] = add_surface_depth
        if add_surface_secondary_depth is not None:
            self.components["add_surface_secondary_depth"] = add_surface_secondary_depth
        if secondary_depth_range is not None:
            self.components["secondary_depth_range"] = secondary_depth_range

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

class VerticalGradientCondition:
    def __init__(
            self,
            random_name: Optional[Union[str, Any]] = None,
            true_at_and_below: Optional[Union['VerticalAnchor', Any]] = None,
            false_at_and_above: Optional[Union['VerticalAnchor', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if random_name is not None:
            self.components["random_name"] = random_name
        if true_at_and_below is not None:
            self.components["true_at_and_below"] = true_at_and_below
        if false_at_and_above is not None:
            self.components["false_at_and_above"] = false_at_and_above

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

class WaterCondition:
    def __init__(
            self,
            offset: Optional[Union[int, Any]] = None,
            surface_depth_multiplier: Optional[Union[int, Any]] = None,
            add_stone_depth: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if offset is not None:
            self.components["offset"] = offset
        if surface_depth_multiplier is not None:
            self.components["surface_depth_multiplier"] = surface_depth_multiplier
        if add_stone_depth is not None:
            self.components["add_stone_depth"] = add_stone_depth

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

class YAboveCondition:
    def __init__(
            self,
            anchor: Optional[Union['VerticalAnchor', Any]] = None,
            surface_depth_multiplier: Optional[Union[int, Any]] = None,
            add_stone_depth: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if anchor is not None:
            self.components["anchor"] = anchor
        if surface_depth_multiplier is not None:
            self.components["surface_depth_multiplier"] = surface_depth_multiplier
        if add_stone_depth is not None:
            self.components["add_stone_depth"] = add_stone_depth

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

