### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class ThreeLayersFeatureSize:
    def __init__(
            self,
            min_clipped_height: Optional[Union[float, Any]] = None,
            limit: Optional[Union[int, Any]] = None,
            upper_limit: Optional[Union[int, Any]] = None,
            lower_size: Optional[Union[int, Any]] = None,
            middle_size: Optional[Union[int, Any]] = None,
            upper_size: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if min_clipped_height is not None:
            self.components["min_clipped_height"] = min_clipped_height
        if limit is not None:
            self.components["limit"] = limit
        if upper_limit is not None:
            self.components["upper_limit"] = upper_limit
        if lower_size is not None:
            self.components["lower_size"] = lower_size
        if middle_size is not None:
            self.components["middle_size"] = middle_size
        if upper_size is not None:
            self.components["upper_size"] = upper_size

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

class TwoLayersFeatureSize:
    def __init__(
            self,
            min_clipped_height: Optional[Union[float, Any]] = None,
            limit: Optional[Union[int, Any]] = None,
            lower_size: Optional[Union[int, Any]] = None,
            upper_size: Optional[Union[int, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if min_clipped_height is not None:
            self.components["min_clipped_height"] = min_clipped_height
        if limit is not None:
            self.components["limit"] = limit
        if lower_size is not None:
            self.components["lower_size"] = lower_size
        if upper_size is not None:
            self.components["upper_size"] = upper_size

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

