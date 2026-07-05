### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class LinearPos:
    def __init__(
            self,
            min_dist: Optional[Union[int, Any]] = None,
            max_dist: Optional[Union[int, Any]] = None,
            min_chance: Optional[Union[float, Any]] = None,
            max_chance: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if min_dist is not None:
            self.components["min_dist"] = min_dist
        if max_dist is not None:
            self.components["max_dist"] = max_dist
        if min_chance is not None:
            self.components["min_chance"] = min_chance
        if max_chance is not None:
            self.components["max_chance"] = max_chance

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

class AxisAlignedLinearPos(LinearPos):
    def __init__(
            self,
            axis: Optional[Union[str, Any]] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if axis is not None:
            self.components["axis"] = axis

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

