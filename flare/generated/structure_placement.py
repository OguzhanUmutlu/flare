### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class ConcentricRingsPlacement:
    def __init__(
            self,
            distance: Optional[Union[int, Any]] = None,
            spread: Optional[Union[int, Any]] = None,
            count: Optional[Union[int, Any]] = None,
            preferred_biomes: Optional[Union[Union[list[str], str], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if distance is not None:
            self.components["distance"] = distance
        if spread is not None:
            self.components["spread"] = spread
        if count is not None:
            self.components["count"] = count
        if preferred_biomes is not None:
            self.components["preferred_biomes"] = preferred_biomes

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

class RandomSpreadPlacement:
    def __init__(
            self,
            spacing: Optional[Union[int, Any]] = None,
            separation: Optional[Union[int, Any]] = None,
            salt: Optional[Union[int, Any]] = None,
            spread_type: Optional[Union[str, Any]] = None,
            locate_offset: Optional[Union[list[int], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if spacing is not None:
            self.components["spacing"] = spacing
        if separation is not None:
            self.components["separation"] = separation
        if salt is not None:
            self.components["salt"] = salt
        if spread_type is not None:
            self.components["spread_type"] = spread_type
        if locate_offset is not None:
            self.components["locate_offset"] = locate_offset

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

