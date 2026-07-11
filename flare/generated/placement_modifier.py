### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

HeightProvider = Union[Union[{'type': str}, 'VerticalAnchor'], Any]

VerticalAnchor = Union[Union[{'absolute': int}, {'above_bottom': int}, {'below_top': int}, {'relative_to_sea_level': int}], Any]

class BlockPredicate:
    def __init__(
            self,
            type: Optional[Union[str, Any]] = None,
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

class BlockPredicateFilter:
    def __init__(
            self,
            predicate: Optional[Union['BlockPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if predicate is not None:
            self.components["predicate"] = predicate

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

class CarvingMaskModifier:
    def __init__(
            self,
            step: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if step is not None:
            self.components["step"] = step

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

class CountModifier:
    def __init__(
            self,
            count: Optional[Union[Union['IntProvider', 'IntProvider'], Any]] = None,
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

class CountOnEveryLayerModifier:
    def __init__(
            self,
            count: Optional[Union['IntProvider', Any]] = None,
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

class CuboidModifier:
    def __init__(
            self,
            xz_size: Optional[Union['IntProvider', Any]] = None,
            y_size: Optional[Union['IntProvider', Any]] = None,
            include_interior: Optional[Union[bool, Any]] = None,
            include_edges: Optional[Union[bool, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if xz_size is not None:
            self.components["xz_size"] = xz_size
        if y_size is not None:
            self.components["y_size"] = y_size
        if include_interior is not None:
            self.components["include_interior"] = include_interior
        if include_edges is not None:
            self.components["include_edges"] = include_edges

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

class EnvironmentScanModifier:
    def __init__(
            self,
            direction_of_search: Optional[Union[str, Any]] = None,
            max_steps: Optional[Union[int, Any]] = None,
            target_condition: Optional[Union['BlockPredicate', Any]] = None,
            allowed_search_condition: Optional[Union['BlockPredicate', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if direction_of_search is not None:
            self.components["direction_of_search"] = direction_of_search
        if max_steps is not None:
            self.components["max_steps"] = max_steps
        if target_condition is not None:
            self.components["target_condition"] = target_condition
        if allowed_search_condition is not None:
            self.components["allowed_search_condition"] = allowed_search_condition

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

class FixedPlacementModifier:
    def __init__(
            self,
            positions: Optional[Union[list[list[int]], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if positions is not None:
            self.components["positions"] = positions

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

class HeightRangeModifier:
    def __init__(
            self,
            height: Optional[Union['HeightProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if height is not None:
            self.components["height"] = height

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

class HeightmapModifier:
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

class NoiseBasedCountModifier:
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

class NoiseThresholdCountModifier:
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

class OffsetModifier:
    def __init__(
            self,
            x: Optional[Union['IntProvider', Any]] = None,
            y: Optional[Union['IntProvider', Any]] = None,
            z: Optional[Union['IntProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if x is not None:
            self.components["x"] = x
        if y is not None:
            self.components["y"] = y
        if z is not None:
            self.components["z"] = z

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

class RandomChanceModifier:
    def __init__(
            self,
            chance: Optional[Union[float, Any]] = None,
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

class RandomOffsetModifier:
    def __init__(
            self,
            xz_spread: Optional[Union['IntProvider', Any]] = None,
            y_spread: Optional[Union['IntProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if xz_spread is not None:
            self.components["xz_spread"] = xz_spread
        if y_spread is not None:
            self.components["y_spread"] = y_spread

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

class RarityFilter:
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

class SurfaceRelativeThresholdFilter:
    def __init__(
            self,
            heightmap: Optional[Union[str, Any]] = None,
            min_inclusive: Optional[Union[int, Any]] = None,
            max_inclusive: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if heightmap is not None:
            self.components["heightmap"] = heightmap
        if min_inclusive is not None:
            self.components["min_inclusive"] = min_inclusive
        if max_inclusive is not None:
            self.components["max_inclusive"] = max_inclusive

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

class SurfaceWaterDepthFilter:
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

