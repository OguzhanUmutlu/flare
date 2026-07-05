### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class BlockStateProvider:
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

class MangroveRootPlacement:
    def __init__(
            self,
            max_root_width: Optional[Union[int, Any]] = None,
            max_root_length: Optional[Union[int, Any]] = None,
            random_skew_chance: Optional[Union[float, Any]] = None,
            can_grow_through: Optional[Union[Union[list[str], str], Any]] = None,
            muddy_roots_in: Optional[Union[Union[list[str], str], Any]] = None,
            muddy_roots_provider: Optional[Union['BlockStateProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if max_root_width is not None:
            self.components["max_root_width"] = max_root_width
        if max_root_length is not None:
            self.components["max_root_length"] = max_root_length
        if random_skew_chance is not None:
            self.components["random_skew_chance"] = random_skew_chance
        if can_grow_through is not None:
            self.components["can_grow_through"] = can_grow_through
        if muddy_roots_in is not None:
            self.components["muddy_roots_in"] = muddy_roots_in
        if muddy_roots_provider is not None:
            self.components["muddy_roots_provider"] = muddy_roots_provider

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

class MangroveRootPlacer:
    def __init__(
            self,
            mangrove_root_placement: Optional[Union['MangroveRootPlacement', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if mangrove_root_placement is not None:
            self.components["mangrove_root_placement"] = mangrove_root_placement

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

