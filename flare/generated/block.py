### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class BlockEntity:
    def __init__(
            self,
            id: Optional[Union[str, Any]] = None,
            x: Optional[Union[int, Any]] = None,
            y: Optional[Union[int, Any]] = None,
            z: Optional[Union[int, Any]] = None,
            keepPacked: Optional[Union[bool, Any]] = None,
            components: Optional[Union['DataComponentPatch', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if id is not None:
            self.components["id"] = id
        if x is not None:
            self.components["x"] = x
        if y is not None:
            self.components["y"] = y
        if z is not None:
            self.components["z"] = z
        if keepPacked is not None:
            self.components["keepPacked"] = keepPacked
        if components is not None:
            self.components["components"] = components

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

class DataComponentPatch:
    def __init__(
            self,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)

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

