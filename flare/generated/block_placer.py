### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class ColumnPlacer:
    def __init__(
            self,
            min_size: Optional[Union[int, Any]] = None,
            extra_size: Optional[Union[int, Any]] = None,
            size: Optional[Union['IntProvider', Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if min_size is not None:
            self.components["min_size"] = min_size
        if extra_size is not None:
            self.components["extra_size"] = extra_size
        if size is not None:
            self.components["size"] = size

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

