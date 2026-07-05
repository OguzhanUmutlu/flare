### AUTO GENERATED DO NOT EDIT ###
from typing import Optional, Union, Any
from flare.generated.data_component import *

class BlockPositionSource:
    def __init__(
            self,
            pos: Optional[Union[list[int], Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if pos is not None:
            self.components["pos"] = pos

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

class EntityPositionSource:
    def __init__(
            self,
            source_entity: Optional[Union[list[int], Any]] = None,
            y_offset: Optional[Union[float, Any]] = None,
            **kwargs
    ):
        self.components = {}
        self.components.update(kwargs)
        if source_entity is not None:
            self.components["source_entity"] = source_entity
        if y_offset is not None:
            self.components["y_offset"] = y_offset

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

