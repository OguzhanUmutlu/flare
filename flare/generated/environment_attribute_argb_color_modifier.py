### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class BlendToGray:
    def __init__(
            self,
            brightness: Optional[Union[float, Any]] = None,
            factor: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if brightness is not None:
            self.components["brightness"] = brightness
        if factor is not None:
            self.components["factor"] = factor

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

StringARGB = Union[Union[int, list[float], str], Any]

StringRGB = Union[Union[int, list[float], str], Any]

